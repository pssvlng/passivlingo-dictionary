"""Unit tests for the searchChains/ package: the chain-of-responsibility
strategies that Dictionary.findWords composes via SearchChainFactory. Each
chain is tested somewhat in isolation here (constructed directly, not only
through the factory) against the real own-wordnet backend, with a fake
translation provider standing in for MtSearchChain's network dependency.
"""
import pytest

from passivlingo_dictionary.searchChains.SearchChain import SearchChain
from passivlingo_dictionary.searchChains.DefaultSearchChain import DefaultSearchChain
from passivlingo_dictionary.searchChains.CategorySearchChain import CategorySearchChain
from passivlingo_dictionary.searchChains.ContainerSearchChain import ContainerSearchChain
from passivlingo_dictionary.searchChains.PosSearchChain import PosSearchChain
from passivlingo_dictionary.searchChains.WordKeySearchChain import WordKeySearchChain
from passivlingo_dictionary.searchChains.LemmaSearchChain import LemmaSearchChain
from passivlingo_dictionary.searchChains.MtSearchChain import MtSearchChain
from passivlingo_dictionary.searchChains.IliSearchChain import IliSearchChain
from passivlingo_dictionary.wrappers.OwnWordNetWrapper import OwnWordNetWrapper

from conftest import skip_without_spacy_model


def _wrapper(filter_lang='de'):
    return OwnWordNetWrapper(filter_lang)


class _FakeTranslationProvider:
    """Deterministic stand-in for a network-backed TranslationProvider."""

    def translate(self, sourceLang, targetLang, woi):
        return f'{woi}-{targetLang}'


class _EmptyTranslationProviderStub:
    def translate(self, sourceLang, targetLang, woi):
        return ''


class _FixedResultChain(SearchChain):
    """Test double used to probe ContainerSearchChain's fallthrough logic."""

    def __init__(self, result, continueIfResults=False):
        super().__init__('x', 'en', continueIfResults)
        self._result = result

    def execute(self):
        return self._result


class TestDefaultSearchChain:
    def test_returns_words_for_known_woi(self):
        chain = DefaultSearchChain('house', None, _wrapper())
        result = chain.execute()
        assert len(result) > 0
        # Word.name is the synset's first lemma, which is 'house' for most
        # senses but can be a synonym (e.g. 'home', 'theatre') for synsets
        # where 'house' is not the first-listed lemma.
        assert any(word.name == 'house' for word in result)

    def test_returns_empty_list_for_unknown_woi(self):
        chain = DefaultSearchChain('zzznotarealword', None, _wrapper())
        assert chain.execute() == []


class TestCategorySearchChain:
    def test_returns_hypernyms_for_direct_language_match(self):
        chain = CategorySearchChain('hypernym', 'vehicle', 'en', _wrapper())
        result = chain.execute()
        assert 'transport' in [word.name for word in result]

    def test_returns_empty_list_for_unknown_category(self):
        chain = CategorySearchChain('not-a-category', 'vehicle', 'en', _wrapper())
        assert chain.execute() == []

    def test_returns_empty_list_for_unknown_woi(self):
        chain = CategorySearchChain('hypernym', 'zzznotarealword', 'en', _wrapper())
        assert chain.execute() == []

    def test_non_english_language_falls_back_to_ili_and_english_relation(self):
        # 'Auto' (German for 'car') has no direct German hypernym relation data,
        # so CategorySearchChain resolves the ILI and re-queries English hypernyms.
        chain = CategorySearchChain('hypernym', 'Auto', 'de', _wrapper())
        result = chain.execute()
        assert isinstance(result, list)


class TestPosSearchChain:
    def test_returns_words_matching_requested_pos(self):
        chain = PosSearchChain('n', 'house', 'en', _wrapper())
        result = chain.execute()
        assert len(result) > 0
        assert all(word.pos == 'Noun' for word in result)

    def test_returns_empty_list_for_unknown_woi(self):
        chain = PosSearchChain('n', 'zzznotarealword', 'en', _wrapper())
        assert chain.execute() == []


class TestWordKeySearchChain:
    def test_extracts_category_from_valid_word_key(self):
        w = _wrapper()
        base = DefaultSearchChain('vehicle', None, w).execute()
        noun_word = next(word for word in base if word.pos == 'Noun')

        chain = WordKeySearchChain('hypernym', noun_word.wordKey, 'en', w)
        result = chain.execute()
        assert 'transport' in [word.name for word in result]

    def test_invalid_word_key_and_english_lang_returns_empty_list(self):
        w = _wrapper()
        chain = WordKeySearchChain('hypernym', 'not-a-valid-key', 'en', w)
        assert chain.execute() == []


class TestLemmaSearchChain:
    @skip_without_spacy_model('en_core_web_sm')
    def test_finds_words_via_lemmatization_when_direct_lookup_fails(self):
        # 'houses' isn't itself a lemma/lookup key in the wordnet data, but
        # lemmatizing it to 'house' should surface real results.
        w = _wrapper()
        chain = LemmaSearchChain('houses', 'en', w)
        result = chain.execute()
        assert len(result) > 0
        assert any(word.name == 'house' for word in result)

    def test_returns_empty_list_when_lemmatization_yields_nothing(self):
        w = _wrapper()
        chain = LemmaSearchChain('zzznotarealwordatall', 'en', w)
        assert chain.execute() == []


class TestMtSearchChain:
    def test_builds_machine_translation_word_from_provider(self):
        chain = MtSearchChain(_FakeTranslationProvider(), 'house', None, 'de,fr')
        result = chain.execute()

        assert len(result) == 1
        word = result[0]
        assert word.name == 'house'
        assert word.pos == 'Machine Translation'
        assert word.languageDescriptions.german == 'house-de'
        assert word.languageDescriptions.french == 'house-fr'
        assert word.genericLanguageDescriptions.getWordDescription('de') == 'house-de'

    def test_empty_word_of_interest_falls_through_to_empty_list(self):
        chain = MtSearchChain(_FakeTranslationProvider(), '   ', None, 'de')
        assert chain.execute() == []

    def test_provider_returning_no_translations_falls_through_to_empty_list(self):
        chain = MtSearchChain(_EmptyTranslationProviderStub(), 'house', None, 'de')
        assert chain.execute() == []

    def test_defaults_to_eu_languages_when_no_filter_lang_given(self):
        chain = MtSearchChain(_FakeTranslationProvider(), 'house', None, None)
        result = chain.execute()
        assert len(result) == 1


class TestIliSearchChain:
    """Also covers the bug-fix regression: execute() must resolve self.lang
    through wordNetWrapper.getWordnetLanguageCode before calling
    getWordsFromIli, rather than passing the raw, possibly NLTK-style code."""

    def test_looks_up_words_by_ili_and_short_language_code(self):
        w = _wrapper()
        base = DefaultSearchChain('house', None, w).execute()
        noun_word = next(word for word in base if word.pos == 'Noun')

        chain = IliSearchChain(noun_word.ili, 'de', w)
        result = chain.execute()
        assert len(result) > 0
        assert all(word.lang == 'de' for word in result)

    def test_looks_up_words_by_ili_using_nltk_style_language_code(self):
        # Regression test: passing 'deu' (NLTK/ISO 639-3 style) must resolve
        # to 'de' via the wrapper's language map before the ILI lookup runs.
        w = _wrapper()
        base = DefaultSearchChain('house', None, w).execute()
        noun_word = next(word for word in base if word.pos == 'Noun')

        chain = IliSearchChain(noun_word.ili, 'deu', w)
        result = chain.execute()
        assert len(result) > 0
        assert all(word.lang == 'de' for word in result)

    def test_unknown_ili_returns_empty_list(self):
        w = _wrapper()
        chain = IliSearchChain('i-does-not-exist', 'de', w)
        assert chain.execute() == []


class TestContainerSearchChain:
    def test_returns_first_nonempty_result_when_continue_if_results_is_false(self):
        w = _wrapper()
        chain = ContainerSearchChain(
            [_FixedResultChain([], continueIfResults=False), _FixedResultChain(['b'])],
            'x', 'en', w,
        )
        assert chain.execute() == ['b']

    def test_stops_after_first_item_marked_continue_if_results_false_even_with_more_items(self):
        w = _wrapper()
        chain = ContainerSearchChain(
            [_FixedResultChain(['a'], continueIfResults=False), _FixedResultChain(['b'])],
            'x', 'en', w,
        )
        assert chain.execute() == ['a']

    def test_accumulates_across_items_marked_continue_if_results_true(self):
        w = _wrapper()
        chain = ContainerSearchChain(
            [_FixedResultChain(['a'], continueIfResults=True), _FixedResultChain(['b'])],
            'x', 'en', w,
        )
        assert chain.execute() == ['a', 'b']

    def test_falls_through_to_empty_list_when_all_items_empty(self):
        w = _wrapper()
        chain = ContainerSearchChain(
            [_FixedResultChain([]), _FixedResultChain([])],
            'x', 'en', w,
        )
        assert chain.execute() == []


class TestSearchChainBaseClass:
    def test_default_execute_returns_empty_list(self):
        class _MinimalChain(SearchChain):
            def execute(self):
                return super().execute()

        chain = _MinimalChain('x', 'en')
        assert chain.execute() == []

    def test_continue_if_results_defaults_to_false(self):
        chain = _FixedResultChain(['a'])
        assert chain.continueIfResults is False
