"""Unit tests for the plain-data model classes: SearchParam, BaseWord/Word/ContextWord,
LanguageDescriptions, GenericLanguageDescriptions, LinguisticCounter, and WordEncoder.
"""
import json

import pytest

from passivlingo_dictionary.models.SearchParam import SearchParam
from passivlingo_dictionary.models.BaseWord import BaseWord
from passivlingo_dictionary.models.Word import Word
from passivlingo_dictionary.models.ContextWord import ContextWord
from passivlingo_dictionary.models.LanguageDescriptions import LanguageDescriptions
from passivlingo_dictionary.models.GenericLanguageDescriptions import GenericLanguageDescriptions
from passivlingo_dictionary.models.LinguisticCounter import LinguisticCounter
from passivlingo_dictionary.encoders.WordEncoder import WordEncoder


class TestSearchParam:
    def test_defaults_are_all_none(self):
        p = SearchParam()
        assert p.wordkey is None
        assert p.category is None
        assert p.lang is None
        assert p.woi is None
        assert p.lemma is None
        assert p.pos is None
        assert p.filterLang is None
        assert p.wordnetId is None
        assert p.googleApiKey is None
        assert p.ili is None

    def test_reset_clears_all_fields(self):
        p = SearchParam()
        p.woi = 'house'
        p.lang = 'en'
        p.category = 'hypernym'
        p.wordkey = 'house.n.01'
        p.filterLang = 'de,fr'
        p.wordnetId = 'own'
        p.ili = 'i12345'
        p.googleApiKey = 'key'
        p.lemma = 'house'
        p.pos = 'Noun'

        p.reset()

        assert p.woi is None
        assert p.lang is None
        assert p.category is None
        assert p.wordkey is None
        assert p.filterLang is None
        assert p.wordnetId is None
        assert p.ili is None
        assert p.googleApiKey is None
        assert p.lemma is None
        assert p.pos is None

    def test_repr_contains_key_fields(self):
        p = SearchParam()
        p.woi = 'house'
        p.filterLang = 'de'
        assert 'house' in repr(p)
        assert 'de' in repr(p)


class TestWordModels:
    def test_base_word_defaults(self):
        w = BaseWord()
        assert w.name == ''
        assert w.pos == ''
        assert w.offset == ''
        assert w.wordKey == ''
        assert w.ili == ''
        assert w.lang == ''
        assert w.wordnetId == ''

    def test_word_extends_base_word_with_extra_fields(self):
        w = Word()
        assert isinstance(w, BaseWord)
        assert w.definition == ''
        assert w.example == ''
        assert w.linguisticCounter is None
        assert w.languageDescriptions is None
        assert w.genericLanguageDescriptions is None
        assert w.synonyms == ''

    def test_word_repr_uses_word_key(self):
        w = Word()
        w.wordKey = 'house.n.01'
        assert repr(w) == 'Word(house.n.01)'
        # str() should fall back to __repr__ since no separate __str__ is defined
        assert str(w) == repr(w)

    def test_context_word_extends_base_word_with_lemma(self):
        cw = ContextWord()
        assert isinstance(cw, BaseWord)
        assert cw.lemma == ''
        cw.lemma = 'house'
        assert repr(cw) == 'ContextWord(house)'
        assert str(cw) == repr(cw)


class TestLanguageDescriptions:
    @pytest.mark.parametrize("lang", ['fra', 'fr'])
    def test_set_and_get_french(self, lang):
        ld = LanguageDescriptions()
        ld.setWordDescription(lang, 'maison')
        assert ld.getWordDescription('fr') == 'maison'
        assert ld.getWordDescription('fra') == 'maison'

    @pytest.mark.parametrize("lang,attr", [
        ('spa', 'spanish'), ('es', 'spanish'),
        ('por', 'portuguese'), ('pt', 'portuguese'),
        ('ita', 'italian'), ('it', 'italian'),
        ('eng', 'english'), ('en', 'english'),
        ('ger', 'german'), ('de', 'german'),
        ('nld', 'dutch'), ('nl', 'dutch'),
    ])
    def test_set_and_get_each_supported_language(self, lang, attr):
        ld = LanguageDescriptions()
        ld.setWordDescription(lang, 'value')
        assert getattr(ld, attr) == 'value'
        assert ld.getWordDescription(lang) == 'value'

    def test_unknown_language_get_returns_empty_string(self):
        ld = LanguageDescriptions()
        assert ld.getWordDescription('xx') == ''

    def test_unknown_language_set_is_a_silent_no_op(self):
        ld = LanguageDescriptions()
        # Should not raise, and should not affect any known attribute
        ld.setWordDescription('xx', 'value')
        assert ld.english == ''
        assert ld.french == ''

    def test_get_word_descriptions_joins_all_seven_languages(self):
        ld = LanguageDescriptions()
        ld.setWordDescription('en', 'house')
        ld.setWordDescription('fr', 'maison')
        ld.setWordDescription('de', 'Haus')
        ld.setWordDescription('es', 'casa')
        ld.setWordDescription('it', 'casa')
        ld.setWordDescription('pt', 'casa')
        ld.setWordDescription('nl', 'huis')
        # Documented join order: french, spanish, portuguese, italian, english, german, dutch
        assert ld.getWordDescriptions('|') == 'maison|casa|casa|casa|house|Haus|huis'


class TestGenericLanguageDescriptions:
    def test_covers_more_languages_than_language_descriptions(self):
        gld = GenericLanguageDescriptions()
        gld.setWordDescription('de', 'Haus')
        assert gld.getWordDescription('de') == 'Haus'
        # Accepts NLTK-style codes too, mapped through langMap
        gld2 = GenericLanguageDescriptions()
        gld2.setWordDescription('deu', 'Haus')
        assert gld2.getWordDescription('de') == 'Haus'

    def test_unknown_language_raises_value_error_on_get(self):
        gld = GenericLanguageDescriptions()
        with pytest.raises(ValueError):
            gld.getWordDescription('not-a-lang')

    def test_unknown_language_raises_value_error_on_set(self):
        gld = GenericLanguageDescriptions()
        with pytest.raises(ValueError):
            gld.setWordDescription('not-a-lang', 'value')

    def test_repr_reports_langmap_size(self):
        gld = GenericLanguageDescriptions()
        assert repr(gld) == f'GenericLanguageDescriptions({len(gld.langMap)})'


class TestLinguisticCounter:
    def test_defaults_are_zero(self):
        lc = LinguisticCounter()
        assert lc.antonym == 0
        assert lc.hypernym == 0
        assert lc.hyponym == 0
        assert lc.holonym == 0
        assert lc.meronym == 0
        assert lc.entailment == 0
        assert lc.mt == 0

    def test_add_accumulates_all_fields_and_returns_self(self):
        lc1 = LinguisticCounter()
        lc1.antonym = 1
        lc1.hypernym = 2
        lc1.hyponym = 3
        lc1.holonym = 4
        lc1.meronym = 5
        lc1.entailment = 6
        lc1.mt = 7

        lc2 = LinguisticCounter()
        lc2.antonym = 10
        lc2.hypernym = 20
        lc2.hyponym = 30
        lc2.holonym = 40
        lc2.meronym = 50
        lc2.entailment = 60
        lc2.mt = 70

        result = lc1.add(lc2)

        assert result is lc1
        assert lc1.antonym == 11
        assert lc1.hypernym == 22
        assert lc1.hyponym == 33
        assert lc1.holonym == 44
        assert lc1.meronym == 55
        assert lc1.entailment == 66
        assert lc1.mt == 77


class TestWordEncoder:
    def test_encodes_word_instance_dict(self):
        w = Word()
        w.name = 'house'
        w.wordKey = 'house.n.01'
        w.pos = 'Noun'
        w.linguisticCounter = None
        w.languageDescriptions = None
        w.genericLanguageDescriptions = None

        encoded = json.dumps(w, cls=WordEncoder)
        decoded = json.loads(encoded)

        assert decoded['name'] == 'house'
        assert decoded['wordKey'] == 'house.n.01'
        assert decoded['pos'] == 'Noun'

    def test_encodes_nested_plain_objects(self):
        w = Word()
        w.name = 'house'
        w.linguisticCounter = LinguisticCounter()
        w.linguisticCounter.hypernym = 3

        encoded = json.dumps(w, cls=WordEncoder)
        decoded = json.loads(encoded)

        assert decoded['linguisticCounter']['hypernym'] == 3
