"""Unit tests for helpers.CommonHelper: language-code resolution, POS mapping,
spaCy model-name resolution, and word sanitization.
"""
import pytest

from passivlingo_dictionary.helpers.CommonHelper import CommonHelper
from passivlingo_dictionary.helpers.Constants import (
    VALID_WORDNET_LANGS,
    VALID_WORDNET_LANGS_OWN,
    OWN_TO_NLTK_LANGMAP,
    OWN_TO_NLTK_LANGMAP_EXCLUSIONS,
    NLTK_TO_OWN_LANGMAP,
    NLTK_TO_OWN_LANGMAP_EXCLUSIONS,
)


class TestGetWordnetLanguageCode:
    def test_none_returns_none(self):
        assert CommonHelper.getWordnetLanguageCode(None, VALID_WORDNET_LANGS_OWN, {}) is None

    def test_lang_already_valid_is_returned_unchanged(self):
        assert CommonHelper.getWordnetLanguageCode('de', VALID_WORDNET_LANGS_OWN, {}) == 'de'

    def test_lang_mapped_via_langmap(self):
        langMap = {**OWN_TO_NLTK_LANGMAP, **OWN_TO_NLTK_LANGMAP_EXCLUSIONS}
        assert CommonHelper.getWordnetLanguageCode('de', VALID_WORDNET_LANGS, langMap) == 'deu'

    def test_unmapped_invalid_lang_raises_value_error(self):
        with pytest.raises(ValueError, match="Invalid Language Code"):
            CommonHelper.getWordnetLanguageCode('not-a-lang', VALID_WORDNET_LANGS_OWN, {})


class TestGetLangVariant:
    def test_own_code_gets_nltk_variant_appended(self):
        result = CommonHelper.getLangVariant('de')
        assert 'de' in result
        assert 'deu' in result

    def test_nltk_code_gets_own_variant_appended(self):
        result = CommonHelper.getLangVariant('deu')
        assert 'deu' in result
        assert 'de' in result

    def test_unrecognized_code_returns_only_itself(self):
        result = CommonHelper.getLangVariant('zzz-unknown')
        assert result == ['zzz-unknown']


class TestSanitizeWord:
    def test_strips_wrapping_quotes(self):
        assert CommonHelper.sanitizeWord('"house"') == 'house'

    def test_strips_leading_and_trailing_punctuation(self):
        assert CommonHelper.sanitizeWord('...house!') == 'house'

    def test_strips_leading_apostrophe_contractions(self):
        assert CommonHelper.sanitizeWord("l'ami") == 'ami'
        assert CommonHelper.sanitizeWord("n'ecoute") == 'ecoute'

    def test_strips_trailing_possessive(self):
        assert CommonHelper.sanitizeWord("dog's") == 'dog'

    def test_leaves_clean_word_unchanged(self):
        assert CommonHelper.sanitizeWord('house') == 'house'

    def test_deprecated_alias_still_works(self):
        assert CommonHelper.sanatizeWord('"house"') == CommonHelper.sanitizeWord('"house"')


class TestGetCountryCode:
    @pytest.mark.parametrize("lang,expected", [
        ('fra', 'fr'), ('spa', 'es'), ('ita', 'it'), ('nld', 'nl'),
        ('por', 'pt'), ('ger', 'de'), ('eng', 'en'), ('fas', 'fa'),
        ('jpn', 'ja'), ('pol', 'pl'), ('tha', 'th'),
    ])
    def test_known_language_returns_mapped_country(self, lang, expected):
        assert CommonHelper.getCountryCode(lang) == expected

    def test_unknown_language_defaults_to_en(self):
        assert CommonHelper.getCountryCode('not-a-lang') == 'en'


class TestSpacyModelName:
    @pytest.mark.parametrize("lang,expected", [
        ('fr', 'fr_core_news_sm'),
        ('fra', 'fr_core_news_sm'),
        ('de', 'de_core_news_sm'),
        ('deu', 'de_core_news_sm'),
        ('ger', 'de_core_news_sm'),
        ('es', 'es_core_news_sm'),
        ('it', 'it_core_news_sm'),
        ('nl', 'nl_core_news_sm'),
        ('pt', 'pt_core_news_sm'),
    ])
    def test_known_languages_map_to_expected_model(self, lang, expected):
        result = CommonHelper.getSpacyModelName(lang)
        assert result.endswith(expected)

    def test_unknown_language_defaults_to_english_model(self):
        result = CommonHelper.getSpacyModelName('not-a-lang')
        assert result.endswith('en_core_web_sm')


class TestPosMapping:
    @pytest.mark.parametrize("spacy_pos,expected", [
        ('VERB', 'v'), ('NOUN', 'n'), ('ADV', 'r'), ('ADJ', 'a'), ('PRON', 'x'),
    ])
    def test_spacy_to_wordnet_pos_mapping(self, spacy_pos, expected):
        assert CommonHelper.getSpacyToWordnetPosMapping(spacy_pos) == expected

    @pytest.mark.parametrize("nltk_pos,expected", [
        ('NN', 'n'), ('NNS', 'n'), ('VB', 'v'), ('VBZ', 'v'),
        ('JJ', 'a'), ('JJR', 'a'), ('RB', 'r'), ('RBS', 'r'), ('DT', 'x'),
    ])
    def test_nltk_to_wordnet_pos_mapping(self, nltk_pos, expected):
        assert CommonHelper.getWordnetPosMapping(nltk_pos) == expected
