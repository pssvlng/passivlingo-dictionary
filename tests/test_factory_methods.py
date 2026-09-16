"""Unit tests for helpers.FactoryMethods: the central dispatch point for
extractors, lemmatizers, and OwnSynsetWrapper construction.
"""
import pytest

from passivlingo_dictionary.helpers.FactoryMethods import FactoryMethods
from passivlingo_dictionary.extractors.AntonymExtractor import AntonymExtractor
from passivlingo_dictionary.extractors.HypernymExtractor import HypernymExtractor
from passivlingo_dictionary.extractors.HyponymExtractor import HyponymExtractor
from passivlingo_dictionary.extractors.HolonymExtractor import HolonymExtractor
from passivlingo_dictionary.extractors.MeronymExtractor import MeronymExtractor
from passivlingo_dictionary.extractors.EntailmentExtractor import EntailmentExtractor
from passivlingo_dictionary.extractors.PosExtractor import PosExtractor
from passivlingo_dictionary.extractors.AdjectiveExtractor import AdjectiveExtractor
from passivlingo_dictionary.extractors.CombinedExtractor import CombinedExtractor
from passivlingo_dictionary.lemmatizers.DefaultLemmatizer import DefaultLemmatizer
from passivlingo_dictionary.lemmatizers.SpacyLemmatizer import SpacyLemmatizer
from passivlingo_dictionary.wrappers.OwnSynsetWrapper import OwnSynsetWrapper
from passivlingo_dictionary.wrappers.OwnWordNetWrapper import OwnWordNetWrapper

from conftest import skip_without_spacy_model


class TestGetExtractor:
    @pytest.mark.parametrize("category,expected_type", [
        ('antonym', AntonymExtractor),
        ('hypernym', HypernymExtractor),
        ('hyponym', HyponymExtractor),
        ('holonym', HolonymExtractor),
        ('meronym', MeronymExtractor),
        ('entailment', EntailmentExtractor),
    ])
    def test_known_category_returns_correct_extractor_type(self, category, expected_type):
        extractor = FactoryMethods.getExtractor(category, None)
        assert isinstance(extractor, expected_type)

    def test_unknown_category_returns_none(self):
        assert FactoryMethods.getExtractor('not-a-category', None) is None


class TestGetExtractorByPos:
    @pytest.mark.parametrize("pos,expected_type", [
        ('v', PosExtractor),
        ('n', PosExtractor),
        ('r', PosExtractor),
        ('a', AdjectiveExtractor),
    ])
    def test_known_pos_returns_correct_extractor_type(self, pos, expected_type):
        extractor = FactoryMethods.getExtractorByPos(pos, None)
        assert isinstance(extractor, expected_type)

    def test_unknown_pos_defaults_to_combined_extractor(self):
        extractor = FactoryMethods.getExtractorByPos('not-a-pos', None)
        assert isinstance(extractor, CombinedExtractor)


class TestGetLemmatizer:
    def test_non_wordnet_language_returns_default_lemmatizer(self):
        lemmatizer = FactoryMethods.getLemmatizer('not-a-lang')
        assert isinstance(lemmatizer, DefaultLemmatizer)

    @skip_without_spacy_model('en_core_web_sm')
    def test_english_wordnet_language_returns_spacy_lemmatizer(self):
        lemmatizer = FactoryMethods.getLemmatizer('en')
        assert isinstance(lemmatizer, SpacyLemmatizer)

    @skip_without_spacy_model('de_core_news_sm')
    def test_german_wordnet_language_returns_spacy_lemmatizer(self):
        lemmatizer = FactoryMethods.getLemmatizer('de')
        assert isinstance(lemmatizer, SpacyLemmatizer)


class TestGetOwnSynsetWrappers:
    def test_wraps_each_synset_with_given_lang(self):
        raw_synsets = OwnWordNetWrapper('de').translate('house', 'en')
        wrapped = FactoryMethods.getOwnSynsetWrappers(raw_synsets, 'de')
        assert len(wrapped) == len(raw_synsets)
        assert all(isinstance(w, OwnSynsetWrapper) for w in wrapped)
        assert all(w.lang == 'de' for w in wrapped)
