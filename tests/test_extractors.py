"""Unit tests for the extractors/ package: thin adapters that pull a specific
relation (antonym, hypernym, ...) or part-of-speech off a list of synsets via
the injected WordNetWrapper. Exercised against the real own-wordnet backend.
"""
from passivlingo_dictionary.wrappers.OwnWordNetWrapper import OwnWordNetWrapper
from passivlingo_dictionary.extractors.AdjectiveExtractor import AdjectiveExtractor
from passivlingo_dictionary.extractors.AntonymExtractor import AntonymExtractor
from passivlingo_dictionary.extractors.CombinedExtractor import CombinedExtractor
from passivlingo_dictionary.extractors.EntailmentExtractor import EntailmentExtractor
from passivlingo_dictionary.extractors.GenericExtractor import GenericExtractor
from passivlingo_dictionary.extractors.HolonymExtractor import HolonymExtractor
from passivlingo_dictionary.extractors.HypernymExtractor import HypernymExtractor
from passivlingo_dictionary.extractors.HyponymExtractor import HyponymExtractor
from passivlingo_dictionary.extractors.MeronymExtractor import MeronymExtractor
from passivlingo_dictionary.extractors.PosExtractor import PosExtractor


def _wrapper():
    return OwnWordNetWrapper('de')


class TestPosExtractor:
    def test_extracts_only_matching_pos(self):
        w = _wrapper()
        synsets = w.translate('house', 'en')
        result = PosExtractor(w, 'n').extract(synsets)
        assert len(result) > 0
        assert all(word.pos == 'Noun' for word in result)

    def test_returns_empty_list_when_no_matching_pos(self):
        w = _wrapper()
        synsets = [s for s in w.translate('house', 'en') if s.pos == 'n']
        result = PosExtractor(w, 'v').extract(synsets)
        assert result == []


class TestAdjectiveExtractor:
    def test_extracts_both_adjective_and_adjective_satellite(self):
        w = _wrapper()
        synsets = w.translate('hot', 'en')
        result = AdjectiveExtractor(w).extract(synsets)
        assert len(result) > 0
        assert all(word.pos == 'Adjective' for word in result)


class TestAntonymExtractor:
    def test_extracts_antonyms(self):
        w = _wrapper()
        synsets = [s for s in w.translate('hot', 'en') if s.pos == 'a']
        result = AntonymExtractor(w).extract(synsets)
        assert 'cold' in [word.name for word in result]


class TestHypernymExtractor:
    def test_extracts_hypernyms(self):
        w = _wrapper()
        synsets = [s for s in w.translate('vehicle', 'en') if s.pos == 'n']
        result = HypernymExtractor(w).extract(synsets)
        assert 'transport' in [word.name for word in result]


class TestHyponymExtractor:
    def test_extracts_hyponyms(self):
        w = _wrapper()
        synsets = [s for s in w.translate('vehicle', 'en') if s.pos == 'n']
        result = HyponymExtractor(w).extract(synsets)
        assert 'rocket' in [word.name for word in result]


class TestHolonymExtractor:
    def test_extracts_holonyms(self):
        w = _wrapper()
        synsets = [s for s in w.translate('house', 'en') if s.pos == 'n']
        result = HolonymExtractor(w).extract(synsets)
        assert isinstance(result, list)


class TestMeronymExtractor:
    def test_extracts_meronyms(self):
        w = _wrapper()
        synsets = [s for s in w.translate('house', 'en') if s.pos == 'n']
        result = MeronymExtractor(w).extract(synsets)
        assert 'porch' in [word.name for word in result]


class TestEntailmentExtractor:
    def test_extracts_entailments(self):
        w = _wrapper()
        synsets = [s for s in w.translate('snore', 'en') if s.pos == 'v']
        result = EntailmentExtractor(w).extract(synsets)
        assert 'sleep' in [word.name for word in result]


class TestCombinedExtractor:
    def test_combines_all_parts_of_speech(self):
        w = _wrapper()
        synsets = w.translate('house', 'en')
        result = CombinedExtractor(w).extract(synsets)
        poses = {word.pos for word in result}
        assert 'Noun' in poses
        assert 'Verb' in poses


class TestGenericExtractor:
    """Regression test for a bug fix: extract() previously called each sub-extractor
    without collecting return values, so it always returned None. It now
    accumulates and returns the combined results, matching CombinedExtractor's
    pattern for the same input.
    """

    def test_extract_accumulates_results_from_all_extractors(self):
        w = _wrapper()
        synsets = [s for s in w.translate('vehicle', 'en') if s.pos == 'n']
        generic = GenericExtractor([HypernymExtractor(w), HyponymExtractor(w)], w)
        result = generic.extract(synsets)

        assert result is not None
        expected = HypernymExtractor(w).extract(synsets) + HyponymExtractor(w).extract(synsets)
        assert [word.name for word in result] == [word.name for word in expected]

    def test_extract_with_empty_extractor_list_returns_empty_list(self):
        w = _wrapper()
        synsets = w.translate('house', 'en')
        generic = GenericExtractor([], w)
        assert generic.extract(synsets) == []
