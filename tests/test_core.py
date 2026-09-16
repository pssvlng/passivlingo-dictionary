"""Tests for the new public API: Wordnet, Word, Sense, Synset, RelationCounts,
and the module-level convenience functions. Exercised against the same real
locally-installed WordNet data (own-wordnet lexicons en/de/es/fr/it/nl/pt,
NLTK English data) as the legacy test suite, with network calls mocked for
the machine-translation fallback path.

These tests also serve as a parity check: the underlying matching/relation
logic is unchanged from the legacy Dictionary/SearchParam path (this is a
thin layer over the same wrappers), so results are checked against the same
known word/relation fixtures already proven in tests/test_wrappers.py and
tests/test_search_chains.py.
"""
import dataclasses

import pytest

import passivlingo_dictionary as pld
from passivlingo_dictionary.core import RelationCounts, Sense, Synset, Word, Wordnet
from passivlingo_dictionary.exceptions import BackendError, LanguageError
from passivlingo_dictionary.Dictionary import Dictionary
from passivlingo_dictionary.models.SearchParam import SearchParam

from conftest import skip_without_lexicon


class _FakeTranslator:
    def translate(self, source_lang, target_lang, woi):
        return f'{woi}-{target_lang}'


class _EmptyTranslator:
    def translate(self, source_lang, target_lang, woi):
        return ''


class TestWordnetConstruction:
    def test_default_backend_is_omw(self):
        assert Wordnet().backend == 'omw'

    def test_nltk_backend_selection(self):
        assert Wordnet(backend='nltk').backend == 'nltk'

    def test_unknown_backend_raises_language_error(self):
        with pytest.raises(LanguageError, match='Unknown backend'):
            Wordnet(backend='not-a-backend')

    def test_lang_accepts_space_separated_string(self):
        wordnet = Wordnet(backend='omw', lang='de fr es')
        assert set(wordnet._wrapper.filterLang) >= {'de', 'fr', 'es'}

    def test_lang_accepts_comma_separated_string(self):
        wordnet = Wordnet(backend='omw', lang='de,fr,es')
        assert set(wordnet._wrapper.filterLang) >= {'de', 'fr', 'es'}

    def test_lang_accepts_a_list(self):
        wordnet = Wordnet(backend='omw', lang=['de', 'fr'])
        assert set(wordnet._wrapper.filterLang) >= {'de', 'fr'}

    def test_unresolvable_language_code_raises_language_error(self):
        with pytest.raises(LanguageError):
            Wordnet(backend='omw', lang='zz-totally-unknown')

    def test_repr(self):
        assert repr(Wordnet(backend='nltk')) == "Wordnet(backend='nltk')"


class TestWordnetSynsets:
    def test_basic_lookup_returns_synsets(self):
        wordnet = Wordnet(lang='de')
        synsets = wordnet.synsets('house', pos='n')
        assert len(synsets) > 0
        assert all(isinstance(s, Synset) for s in synsets)
        assert any(s.lemmas()[0] == 'house' for s in synsets)

    def test_unknown_word_returns_empty_list(self):
        wordnet = Wordnet(lang='de')
        assert wordnet.synsets('zzznotarealwordatall', pos='n') == []

    def test_pos_filters_results(self):
        wordnet = Wordnet(lang='de')
        synsets = wordnet.synsets('house', pos='n')
        assert all(s.pos == 'n' for s in synsets)

    def test_single_synset_lookup_by_id(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synset('house.n.03549540.ewn')
        assert synset.id == 'house.n.03549540.ewn'
        assert synset.definition() == (
            'a dwelling that serves as living quarters for one or more families'
        )

    def test_unresolvable_id_raises_backend_error(self):
        wordnet = Wordnet(lang='de')
        with pytest.raises(BackendError):
            wordnet.synset('not.a.real.key.ewn')

    def test_nltk_backend_synsets(self):
        wordnet = Wordnet(backend='nltk')
        synsets = wordnet.synsets('house', pos='n')
        assert len(synsets) > 0
        assert synsets[0].backend == 'nltk'
        assert synsets[0].id == 'house.n.01'
        assert synsets[0].lang == 'en'


class TestWordnetWords:
    def test_basic_lookup(self):
        wordnet = Wordnet(lang='de')
        words = wordnet.words('house', pos='n')
        assert len(words) > 0
        assert all(isinstance(w, Word) for w in words)
        assert all(w.source == 'wordnet' for w in words)

    def test_lemmatization_fallback_tags_source(self):
        wordnet = Wordnet(lang='de')
        words = wordnet.words('houses')
        assert len(words) > 0
        assert any(w.lemma() == 'house' for w in words)
        assert all(w.source == 'lemmatized' for w in words)

    def test_machine_translation_fallback(self):
        wordnet = Wordnet(lang='de', translator=_FakeTranslator())
        words = wordnet.words('zzznotarealwordatall')
        assert len(words) == 1
        assert words[0].source == 'machine_translation'
        assert words[0].lemma() == 'zzznotarealwordatall-de'

    def test_no_translator_configured_returns_empty_on_total_miss(self):
        wordnet = Wordnet(lang='de')
        assert wordnet.words('zzznotarealwordatall') == []

    def test_translator_returning_empty_string_falls_through_to_empty_list(self):
        wordnet = Wordnet(lang='de', translator=_EmptyTranslator())
        assert wordnet.words('zzznotarealwordatall') == []

    def test_nltk_backend_words(self):
        wordnet = Wordnet(backend='nltk')
        words = wordnet.words('happy', pos='a')
        assert len(words) > 0
        assert words[0].lemma() == 'happy'
        assert words[0].backend == 'nltk'


class TestWordnetSenses:
    def test_basic_lookup(self):
        wordnet = Wordnet(lang='de')
        senses = wordnet.senses('house', pos='n')
        assert len(senses) > 0
        assert all(isinstance(s, Sense) for s in senses)

    def test_nltk_backend_senses(self):
        wordnet = Wordnet(backend='nltk')
        senses = wordnet.senses('house', pos='n')
        assert len(senses) > 0


class TestSynsetRelations:
    """Same fixture words/relations already proven against the legacy
    wrapper/extractor path in tests/test_wrappers.py, exercised here through
    the new Synset API to confirm identical underlying behavior."""

    def test_hypernyms(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synsets('vehicle', pos='n')[0]
        assert 'transport' in [s.lemmas()[0] for s in synset.hypernyms()]

    def test_hyponyms(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synsets('vehicle', pos='n')[0]
        names = [s.lemmas()[0] for s in synset.hyponyms()]
        assert 'rocket' in names

    def test_antonyms(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synsets('hot', pos='a')[0]
        assert 'cold' in [s.lemmas()[0] for s in synset.antonyms()]

    def test_meronyms(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synsets('house', pos='n')[0]
        assert 'porch' in [s.lemmas()[0] for s in synset.meronyms()]

    def test_holonyms_returns_a_list(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synsets('house', pos='n')[0]
        assert isinstance(synset.holonyms(), list)

    def test_entailments(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synsets('snore', pos='v')[0]
        assert 'sleep' in [s.lemmas()[0] for s in synset.entailments()]

    def test_relations_returns_all_by_default(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synsets('vehicle', pos='n')[0]
        result = synset.relations()
        assert set(result.keys()) == {
            'antonym', 'hypernym', 'hyponym', 'holonym', 'meronym', 'entailment',
        }

    def test_relations_restricts_to_requested_names(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synsets('vehicle', pos='n')[0]
        result = synset.relations('hypernym', 'hyponym')
        assert set(result.keys()) == {'hypernym', 'hyponym'}

    def test_relations_rejects_unknown_name(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synsets('vehicle', pos='n')[0]
        with pytest.raises(ValueError, match='Unknown relation'):
            synset.relations('not-a-relation')

    def test_nltk_backend_hypernyms(self):
        wordnet = Wordnet(backend='nltk')
        synset = wordnet.synsets('vehicle', pos='n')[0]
        assert 'conveyance' in [s.lemmas()[0] for s in synset.hypernyms()]

    def test_nltk_backend_antonyms(self):
        wordnet = Wordnet(backend='nltk')
        synset = wordnet.synsets('hot', pos='a')[0]
        assert 'cold' in [s.lemmas()[0] for s in synset.antonyms()]


@skip_without_lexicon('hyde')
class TestSynsetTranslate:
    def test_translate_by_ili(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synsets('happy', pos='a')[0]
        translated = synset.translate(lang='it')
        assert 'felice' in [s.lemmas()[0] for s in translated]

    def test_translate_with_nltk_style_language_code(self):
        # Regression coverage matching the earlier IliSearchChain fix:
        # an NLTK/ISO-639-3-style code ('deu') must resolve through the
        # wrapper's language map before the ILI lookup runs.
        wordnet = Wordnet(lang='de')
        synset = wordnet.synsets('house', pos='n')[0]
        translated = synset.translate(lang='deu')
        assert len(translated) > 0
        assert all(s.lang == 'de' for s in translated)

    def test_translate_without_ili_returns_empty_list(self):
        wordnet = Wordnet(backend='nltk')
        synset = wordnet.synsets('house', pos='n')[0]
        assert synset.translate(lang='de') == []

    def test_translate_without_any_ili_returns_empty_list(self):
        # A synset with no ILI at all (e.g. a raw object lacking one) should
        # short-circuit to [] rather than error.
        wordnet = Wordnet(lang='de')
        synset = Synset(wordnet._wrapper, _NoIliSynset())
        assert synset.translate(lang='de') == []


class _NoIliSynset:
    ili = None


@skip_without_lexicon('hyde')
class TestSynsetDescriptions:
    def test_defaults_to_configured_languages(self):
        wordnet = Wordnet(lang='de fr')
        synset = wordnet.synsets('house', pos='n')[0]
        descriptions = synset.descriptions()
        assert set(descriptions.keys()) >= {'de', 'fr'}
        assert descriptions['de'] != []

    def test_single_language_filter(self):
        wordnet = Wordnet(lang='de fr')
        synset = wordnet.synsets('house', pos='n')[0]
        assert synset.descriptions(lang='de') == {
            'de': ['Behausung', 'Bude', 'Haus', 'Heim', 'Hütte']
        }

    def test_list_of_languages_filter(self):
        wordnet = Wordnet(lang='de fr')
        synset = wordnet.synsets('house', pos='n')[0]
        result = synset.descriptions(lang=['de', 'fr'])
        assert set(result.keys()) == {'de', 'fr'}

    def test_nltk_style_code_resolves_to_canonical_key(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synsets('house', pos='n')[0]
        assert synset.descriptions(lang='deu') == synset.descriptions(lang='de')

    def test_unknown_language_raises_language_error(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synsets('house', pos='n')[0]
        with pytest.raises(LanguageError):
            synset.descriptions(lang='not-a-lang')


class TestSynsetRelationCounts:
    def test_matches_underlying_wrapper_counts(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synsets('vehicle', pos='n')[0]
        counts = synset.relation_counts()
        raw_counts = wordnet._wrapper.getLinguisticCounter(synset._raw)
        assert counts.hypernym == raw_counts.hypernym
        assert counts.hyponym == raw_counts.hyponym
        assert counts.mt == raw_counts.mt

    def test_is_immutable(self):
        counts = RelationCounts(0, 0, 0, 0, 0, 0, 0)
        with pytest.raises(dataclasses.FrozenInstanceError):
            counts.antonym = 99


class TestSynsetEqualityAndRepr:
    def test_equal_synsets_from_same_backend_compare_equal(self):
        wordnet = Wordnet(lang='de')
        a = wordnet.synset('house.n.03549540.ewn')
        b = wordnet.synset('house.n.03549540.ewn')
        assert a == b
        assert hash(a) == hash(b)

    def test_repr_contains_id(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synset('house.n.03549540.ewn')
        assert repr(synset) == "Synset('house.n.03549540.ewn')"


class TestWordMethods:
    def test_lemma_and_forms(self):
        wordnet = Wordnet(lang='de')
        word = wordnet.words('house', pos='n')[0]
        assert word.lemma() == 'house'
        assert isinstance(word.forms(), list)

    def test_synsets_and_senses(self):
        wordnet = Wordnet(lang='de')
        word = wordnet.words('house', pos='n')[0]
        assert len(word.synsets()) == 1
        assert len(word.senses()) >= 1

    def test_translate(self):
        wordnet = Wordnet(lang='de')
        word = wordnet.words('happy', pos='a')[0]
        translations = word.translate(lang='it')
        assert any(
            any(w.lemma() == 'felice' for w in words)
            for words in translations.values()
        )

    def test_repr(self):
        wordnet = Wordnet(lang='de')
        word = wordnet.words('house', pos='n')[0]
        assert repr(word) == "Word('house')"


class TestSenseMethods:
    def test_word_and_synset_for_omw_backend(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synsets('house', pos='n')[0]
        sense = synset.senses()[0]
        assert sense.word().lemma() == 'house'
        assert sense.synset() == synset

    def test_word_and_synset_for_nltk_backend(self):
        wordnet = Wordnet(backend='nltk')
        synset = wordnet.synsets('house', pos='n')[0]
        sense = synset.senses()[0]
        assert sense.word().lemma() == 'house'
        assert sense.synset().id == synset.id

    def test_examples_for_omw_backend(self):
        wordnet = Wordnet(lang='de')
        synset = wordnet.synsets('house', pos='n')[0]
        sense = synset.senses()[0]
        assert isinstance(sense.examples(), list)


class TestModuleLevelFunctions:
    def test_words(self):
        assert pld.words('house', pos='n')[0].lemma() == 'house'

    def test_synsets(self):
        assert pld.synsets('house', pos='n')[0].lemmas()[0] == 'house'

    def test_senses(self):
        assert len(pld.senses('house', pos='n')) > 0

    def test_backend_argument(self):
        assert pld.synsets('house', pos='n', backend='nltk')[0].backend == 'nltk'


@skip_without_lexicon('hyde')
class TestParityWithLegacyApi:
    """Confirms the new API is a thin layer over the same matching logic
    the legacy Dictionary/SearchParam path uses, not a re-implementation."""

    def test_same_hypernym_result_as_legacy_category_search(self):
        dictionary = Dictionary()
        param = SearchParam()
        param.woi = 'vehicle'
        legacy_result = dictionary.findWords(param)
        noun_word = next(w for w in legacy_result if w.pos == 'Noun')

        param.reset()
        param.wordkey = noun_word.wordKey
        param.category = 'hypernym'
        param.lang = noun_word.lang
        legacy_hypernyms = {w.name for w in dictionary.findWords(param)}

        new_hypernyms = {
            s.lemmas()[0]
            for s in Wordnet(lang='de').synsets('vehicle', pos='n')[0].hypernyms()
        }
        assert new_hypernyms == legacy_hypernyms

    def test_same_definition_as_legacy_lookup(self):
        dictionary = Dictionary()
        param = SearchParam()
        param.woi = 'house'
        legacy_result = dictionary.findWords(param)
        legacy_word = next(w for w in legacy_result if w.wordKey == 'house.n.03549540.ewn')

        new_synset = Wordnet(lang='de').synset('house.n.03549540.ewn')
        assert new_synset.definition() == legacy_word.definition


class TestErrorHandlingRegressions:
    """Regressions for defects found by probing the public API directly.

    Each case previously either leaked an untyped backend exception or
    returned a plausible-looking but wrong result.
    """

    def test_missing_lexicon_raises_backend_error_not_wn_error(self):
        # Japanese has no installed lexicon; wn.Error previously escaped.
        wordnet = Wordnet(lang='ja')
        with pytest.raises(BackendError):
            wordnet.synsets('house')

    def test_missing_lexicon_raises_on_words_and_senses(self):
        wordnet = Wordnet(lang='ja')
        with pytest.raises(BackendError):
            wordnet.words('house')
        with pytest.raises(BackendError):
            wordnet.senses('house')

    def test_translate_to_uninstalled_language_raises_backend_error(self):
        synset = Wordnet(lang='de').synsets('house', pos='n')[0]
        with pytest.raises(BackendError):
            synset.translate(lang='ja')

    def test_module_level_functions_also_raise_typed_errors(self):
        with pytest.raises(BackendError):
            pld.synsets('house', lang='ja')

    def test_every_public_error_derives_from_error(self):
        from passivlingo_dictionary.exceptions import Error
        wordnet = Wordnet(lang='ja')
        with pytest.raises(Error):
            wordnet.synsets('house')

    @pytest.mark.parametrize('form', ['', '   ', '\t\n'])
    def test_empty_query_returns_no_results(self, form):
        # Previously returned an arbitrary synset, because the backends treat
        # an empty form as an unfiltered query.
        assert Wordnet(lang='de').synsets(form) == []
        assert Wordnet(lang='de').words(form) == []

    @pytest.mark.parametrize('bad_id', ['nonsense', '', '   '])
    def test_unresolvable_synset_id_raises_rather_than_returning_a_synset(self, bad_id):
        # 'nonsense' previously returned Synset('psyche.n.05619057.ewn').
        with pytest.raises(BackendError):
            Wordnet().synset(bad_id)

    def test_unresolvable_word_id_raises(self):
        with pytest.raises(BackendError):
            Wordnet().word('nonsense')

    def test_nltk_synset_id_does_not_require_optional_omw_corpus(self):
        """Synset.id previously derived the identifier through the wrapper's
        getWord(), which eagerly builds multilingual descriptions and so
        required NLTK's optional OMW corpus. Reading it from the synset keeps
        the core attribute usable with only the base wordnet corpus."""
        synset = Wordnet(backend='nltk').synsets('vehicle', pos='n')[0]
        assert synset.id == 'vehicle.n.01'

    def test_nltk_relations_do_not_require_optional_omw_corpus(self):
        """NltkWordNetWrapper.getWord() eagerly builds multilingual
        descriptions, which read NLTK's optional OMW corpus. With only the
        core wordnet corpus installed that raised LookupError from every
        relation call; missing translations now degrade to empty."""
        synset = Wordnet(backend='nltk').synsets('vehicle', pos='n')[0]
        assert 'conveyance' in [s.lemmas()[0] for s in synset.hypernyms()]
        descriptions = synset.descriptions()
        assert descriptions['en']  # English is always available
