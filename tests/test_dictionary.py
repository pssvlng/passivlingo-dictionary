"""Integration-level tests for Dictionary, the package's main public entry
point (findWords / getExampleSentences), exercised against the real own- and
NLTK-backed WordNet data installed locally. These largely mirror the
scenarios demonstrated in examples.py.
"""
import pytest
import wn

from passivlingo_dictionary.Dictionary import Dictionary
from passivlingo_dictionary.models.SearchParam import SearchParam
from passivlingo_dictionary.helpers.Constants import WORDNET_IDENTIFIER_OWN, WORDNET_IDENTIFIER_NLTK


@pytest.fixture
def dictionary():
    return Dictionary()


class TestFindWordsBasicSearch:
    def test_basic_word_search_returns_results(self, dictionary):
        p = SearchParam()
        p.woi = 'house'
        result = dictionary.findWords(p)
        assert len(result) > 0
        assert any(word.name == 'house' for word in result)

    def test_unknown_wordnet_id_defaults_to_own(self, dictionary):
        p = SearchParam()
        p.woi = 'house'
        p.wordnetId = 'not-a-real-backend'
        result = dictionary.findWords(p)
        assert all(word.wordnetId == 'own' for word in result)

    def test_nltk_only_search_returns_nltk_backed_results(self, dictionary):
        p = SearchParam()
        p.woi = 'happy'
        p.wordnetId = 'nltk'
        result = dictionary.findWords(p)
        assert len(result) > 0
        assert all(word.wordnetId == 'nltk' for word in result)

    def test_own_only_search_returns_own_backed_results(self, dictionary):
        p = SearchParam()
        p.woi = 'happy'
        p.wordnetId = 'own'
        result = dictionary.findWords(p)
        assert len(result) > 0
        assert all(word.wordnetId == 'own' for word in result)


class TestFindWordsLanguageFilter:
    def test_single_language_filter(self, dictionary):
        p = SearchParam()
        p.woi = 'house'
        p.filterLang = 'de'
        result = dictionary.findWords(p)
        assert len(result) > 0
        assert any(word.genericLanguageDescriptions.getWordDescription('de') for word in result)

    def test_multi_language_filter(self, dictionary):
        p = SearchParam()
        p.woi = 'house'
        p.filterLang = 'de, fr, es'
        result = dictionary.findWords(p)
        assert len(result) > 0
        first = result[0]
        assert first.genericLanguageDescriptions.getWordDescription('de') != '' or \
            first.genericLanguageDescriptions.getWordDescription('fr') != '' or \
            first.genericLanguageDescriptions.getWordDescription('es') != ''


class TestFindWordsCategorySearch:
    def test_hypernym_category_search_two_step_flow(self, dictionary):
        p = SearchParam()
        p.woi = 'vehicle'
        result = dictionary.findWords(p)
        noun_word = next(word for word in result if word.pos == 'Noun')

        p.reset()
        p.wordkey = noun_word.wordKey
        p.category = 'hypernym'
        p.lang = noun_word.lang
        result2 = dictionary.findWords(p)

        assert 'transport' in [word.name for word in result2]

    def test_antonym_category_search_two_step_flow(self, dictionary):
        p = SearchParam()
        p.woi = 'happy'
        result = dictionary.findWords(p)
        adjective_word = next(word for word in result if word.pos == 'Adjective')

        p.reset()
        p.wordkey = adjective_word.wordKey
        p.category = 'antonym'
        p.lang = adjective_word.lang
        result2 = dictionary.findWords(p)

        assert 'unhappy' in [word.name for word in result2]

    def test_entailment_category_search_two_step_flow(self, dictionary):
        p = SearchParam()
        p.woi = 'snore'
        result = dictionary.findWords(p)
        verb_word = next(word for word in result if word.pos == 'Verb')

        p.reset()
        p.wordkey = verb_word.wordKey
        p.category = 'entailment'
        p.lang = verb_word.lang
        result2 = dictionary.findWords(p)

        assert 'sleep' in [word.name for word in result2]

    def test_direct_woi_category_search_without_wordkey(self, dictionary):
        p = SearchParam()
        p.woi = 'fancy'
        p.category = 'hypernym'
        p.lang = 'en'
        p.filterLang = 'en'
        result = dictionary.findWords(p)
        assert len(result) > 0


class TestFindWordsIliLookup:
    def test_ili_lookup_finds_corresponding_word_in_another_language(self, dictionary):
        p = SearchParam()
        p.woi = 'happy'
        p.wordnetId = 'own'
        result = dictionary.findWords(p)
        adjective_word = next(word for word in result if word.pos == 'Adjective')

        p.reset()
        p.ili = adjective_word.ili
        p.lang = 'it'
        result2 = dictionary.findWords(p)

        assert 'felice' in [word.name for word in result2]


class TestFindWordsValidation:
    def test_raises_when_no_search_criteria_given(self, dictionary):
        p = SearchParam()
        with pytest.raises(ValueError):
            dictionary.findWords(p)


class TestGetExampleSentences:
    def test_returns_examples_for_own_backend_word(self, dictionary):
        p = SearchParam()
        p.woi = 'happy'
        p.wordnetId = 'own'
        result = dictionary.findWords(p)
        adjective_word = next(word for word in result if word.pos == 'Adjective')

        examples = dictionary.getExampleSentences(adjective_word.wordKey)
        assert len(examples) > 0
        assert all('"' not in example for example in examples)

    def test_returns_examples_for_nltk_backend_word(self, dictionary):
        p = SearchParam()
        p.woi = 'happy'
        p.wordnetId = 'nltk'
        result = dictionary.findWords(p)
        adjective_word = next(word for word in result if word.pos == 'Adjective')

        examples = dictionary.getExampleSentences(adjective_word.wordKey, wordnetId=WORDNET_IDENTIFIER_NLTK)
        assert isinstance(examples, list)

    def test_raises_for_too_short_word_key(self, dictionary):
        with pytest.raises(ValueError, match='Invalid word key'):
            dictionary.getExampleSentences('short.key')

    def test_unknown_wordnet_id_defaults_to_own_backend(self, dictionary):
        p = SearchParam()
        p.woi = 'happy'
        p.wordnetId = 'own'
        result = dictionary.findWords(p)
        adjective_word = next(word for word in result if word.pos == 'Adjective')

        examples_default_backend = dictionary.getExampleSentences(adjective_word.wordKey, wordnetId='own')
        examples_bad_backend = dictionary.getExampleSentences(adjective_word.wordKey, wordnetId='not-a-backend')
        assert examples_default_backend == examples_bad_backend

    def test_unresolvable_word_key_raises_from_underlying_backend(self, dictionary):
        with pytest.raises(wn.Error):
            dictionary.getExampleSentences('not.a.real.key')


class TestDictionaryRepr:
    def test_repr_and_str(self, dictionary):
        assert repr(dictionary) == 'Dictionary()'
        assert str(dictionary) == 'Dictionary()'
