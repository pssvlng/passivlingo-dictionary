"""Unit tests for helpers.SearchChainFactory: translates a SearchParam into
one or more executable SearchChain instances. This is the central dispatch
logic behind Dictionary.findWords, so it's tested against every documented
parameter combination plus the invalid ones that should raise ValueError.
"""
import pytest

from passivlingo_dictionary.helpers.SearchChainFactory import SearchChainFactory
from passivlingo_dictionary.models.SearchParam import SearchParam
from passivlingo_dictionary.searchChains.ContainerSearchChain import ContainerSearchChain
from passivlingo_dictionary.searchChains.IliSearchChain import IliSearchChain
from passivlingo_dictionary.wrappers.OwnWordNetWrapper import OwnWordNetWrapper
from passivlingo_dictionary.wrappers.NltkWordNetWrapper import NltkWordNetWrapper


@pytest.fixture
def factory():
    return SearchChainFactory()


class TestValidParamCombinations:
    def test_woi_only(self, factory):
        p = SearchParam()
        p.woi = 'house'
        chains = factory.getSearchChains(p)
        assert len(chains) == 1
        assert isinstance(chains[0], ContainerSearchChain)

    def test_woi_lang_category(self, factory):
        p = SearchParam()
        p.woi = 'vehicle'
        p.lang = 'en'
        p.category = 'hypernym'
        chains = factory.getSearchChains(p)
        assert len(chains) == 1
        result = chains[0].execute()
        assert 'transport' in [word.name for word in result]

    def test_woi_lang_pos_lemma(self, factory):
        p = SearchParam()
        p.woi = 'dogs'
        p.lang = 'en'
        p.pos = 'n'
        p.lemma = 'dog'
        chains = factory.getSearchChains(p)
        assert len(chains) == 1

    def test_wordkey_lang_category(self, factory):
        p = SearchParam()
        p.wordkey = 'house.n.03549540.ewn'
        p.lang = 'en'
        p.category = 'hypernym'
        chains = factory.getSearchChains(p)
        assert len(chains) == 1

    def test_ili_and_lang(self, factory):
        p = SearchParam()
        p.ili = 'i54960'
        p.lang = 'en'
        chains = factory.getSearchChains(p)
        assert len(chains) == 1
        assert isinstance(chains[0], IliSearchChain)


class TestInvalidParamCombinations:
    def test_nothing_set_raises(self, factory):
        p = SearchParam()
        with pytest.raises(ValueError, match="'woi' or 'wordkey' or 'ili' required"):
            factory.getSearchChains(p)

    def test_woi_with_only_lemma_raises(self, factory):
        p = SearchParam()
        p.woi = 'dog'
        p.lemma = 'dog'
        with pytest.raises(ValueError, match='possible combinations'):
            factory.getSearchChains(p)

    def test_woi_with_only_pos_raises(self, factory):
        p = SearchParam()
        p.woi = 'dog'
        p.pos = 'n'
        with pytest.raises(ValueError, match='possible combinations'):
            factory.getSearchChains(p)

    def test_wordkey_without_lang_or_category_raises(self, factory):
        p = SearchParam()
        p.wordkey = 'house.n.01'
        with pytest.raises(ValueError, match="'wordkey', 'lang' and 'category' required"):
            factory.getSearchChains(p)

    def test_ili_without_lang_raises(self, factory):
        """Regression test for a bug fix: previously, ili set with no lang
        matched none of the branches in __getSearchChain and the method fell
        off the end, implicitly returning None (which crashed callers with
        AttributeError instead of a clear error). It must now raise ValueError."""
        p = SearchParam()
        p.ili = 'i54960'
        with pytest.raises(ValueError):
            factory.getSearchChains(p)


class TestWordnetIdSelection:
    def test_own_backend_used_by_default(self, factory):
        p = SearchParam()
        p.woi = 'house'
        chains = factory.getSearchChains(p)
        assert isinstance(chains[0].wordNetWrapper, OwnWordNetWrapper)

    def test_nltk_backend_selected_explicitly(self, factory):
        p = SearchParam()
        p.woi = 'house'
        p.wordnetId = 'nltk'
        chains = factory.getSearchChains(p)
        assert isinstance(chains[0].wordNetWrapper, NltkWordNetWrapper)

    def test_unrecognized_backend_id_defaults_to_own(self, factory):
        p = SearchParam()
        p.woi = 'house'
        p.wordnetId = 'not-a-real-backend'
        chains = factory.getSearchChains(p)
        assert isinstance(chains[0].wordNetWrapper, OwnWordNetWrapper)


class TestFilterLangRouting:
    def test_single_supported_language_produces_one_chain(self, factory):
        p = SearchParam()
        p.woi = 'house'
        p.filterLang = 'de'
        chains = factory.getSearchChains(p)
        assert len(chains) == 1

    def test_language_excluded_from_own_backend_routes_to_nltk_chain(self, factory):
        # 'fa'/'fas' (Farsi) is present in NLTK's language list but excluded
        # from the own-wordnet backend's language handling, so requesting it
        # alongside a supported own-wordnet language produces a second,
        # NLTK-backed search chain for the excluded language.
        p = SearchParam()
        p.woi = 'house'
        p.filterLang = 'de,fa'
        chains = factory.getSearchChains(p)
        assert len(chains) == 2
        wrapper_types = {type(c.wordNetWrapper) for c in chains}
        assert OwnWordNetWrapper in wrapper_types
        assert NltkWordNetWrapper in wrapper_types

    def test_language_excluded_from_nltk_backend_routes_to_own_chain(self, factory):
        # 'de'/'deu'/'ger' is excluded from the NLTK backend's language handling
        # in this factory (no OMW multilingual data assumed), so requesting it
        # alongside a supported NLTK language produces a second, own-backed chain.
        p = SearchParam()
        p.woi = 'house'
        p.wordnetId = 'nltk'
        p.filterLang = 'fr,de'
        chains = factory.getSearchChains(p)
        assert len(chains) == 2
        wrapper_types = {type(c.wordNetWrapper) for c in chains}
        assert NltkWordNetWrapper in wrapper_types
        assert OwnWordNetWrapper in wrapper_types

    def test_filter_lang_whitespace_is_stripped(self, factory):
        p = SearchParam()
        p.woi = 'house'
        p.filterLang = ' de , fr '
        chains = factory.getSearchChains(p)
        assert len(chains) == 1
        assert p.filterLang == 'de,fr'

    def test_completely_unrecognized_language_code_raises(self, factory):
        # A filterLang value recognized by neither backend's valid-language
        # list nor its exclusion list is passed straight through to the
        # wrapper constructor, which rejects it. Documenting current behavior;
        # not one of the bugs in scope for this pass.
        p = SearchParam()
        p.woi = 'house'
        p.filterLang = 'zz-totally-unknown'
        with pytest.raises(ValueError, match='Invalid Language Code'):
            factory.getSearchChains(p)
