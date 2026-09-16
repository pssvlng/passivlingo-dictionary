"""Unit tests for the OwnWordNetWrapper (wn/OMW-backed) and NltkWordNetWrapper
(NLTK WordNet-backed) classes, exercised against real, locally installed
WordNet data. The 'own' backend has lexicons for en/de/es/fr/it/nl/pt; NLTK's
local install only has English data (no OMW multilingual corpora), so
NLTK-backend tests stick to English per project decision.
"""
import pytest

from passivlingo_dictionary.wrappers.OwnWordNetWrapper import OwnWordNetWrapper
from passivlingo_dictionary.wrappers.NltkWordNetWrapper import NltkWordNetWrapper
from passivlingo_dictionary.models.LinguisticCounter import LinguisticCounter


# ---------------------------------------------------------------------------
# OwnWordNetWrapper (wn / OMW backend)
# ---------------------------------------------------------------------------

class TestOwnWordNetWrapperTranslateAndPos:
    def test_translate_returns_synsets_for_known_word(self):
        w = OwnWordNetWrapper('de')
        synsets = w.translate('house', 'en')
        assert len(synsets) > 0

    def test_translate_returns_empty_list_for_unknown_word(self):
        w = OwnWordNetWrapper('de')
        synsets = w.translate('zzznotarealword', 'en')
        assert synsets == []

    def test_translate_pos_filters_by_part_of_speech(self):
        w = OwnWordNetWrapper('de')
        nouns = w.translatePos('house', 'n', 'en')
        assert all(s.pos == 'n' for s in nouns)
        assert len(nouns) > 0

    def test_get_pos_description_maps_known_codes(self):
        w = OwnWordNetWrapper(None)
        assert w.getPOSDescription('n') == 'Noun'
        assert w.getPOSDescription('v') == 'Verb'
        assert w.getPOSDescription('a') == 'Adjective'
        assert w.getPOSDescription('s') == 'Adjective'
        assert w.getPOSDescription('r') == 'Adverb'

    def test_get_pos_description_raises_for_unknown_code(self):
        w = OwnWordNetWrapper(None)
        with pytest.raises(ValueError):
            w.getPOSDescription('not-a-pos')


class TestOwnWordNetWrapperGetWord:
    def test_get_word_populates_core_fields(self):
        w = OwnWordNetWrapper('de')
        synsets = w.translatePos('house', 'n', 'en')
        word = w.getWord(synsets[0])
        assert word.name == 'house'
        assert word.pos == 'Noun'
        assert word.definition
        assert word.lang == 'en'
        assert word.wordnetId == 'own'
        assert word.wordKey.startswith('house.')
        assert word.wordKey.endswith('.ewn')
        assert isinstance(word.linguisticCounter, LinguisticCounter)

    def test_get_word_by_pos_filters_correctly(self):
        w = OwnWordNetWrapper('de')
        synsets = w.translate('house', 'en')
        nouns = w.getWordByPos(synsets, 'n', 'Noun')
        assert len(nouns) > 0
        assert all(word.pos == 'Noun' for word in nouns)


class TestOwnWordNetWrapperRelations:
    def test_antonyms_of_hot_include_cold(self):
        w = OwnWordNetWrapper('de')
        synsets = [s for s in w.translate('hot', 'en') if s.pos == 'a']
        antonyms = w.getAntonyms(synsets)
        names = [a.name for a in antonyms]
        assert 'cold' in names

    def test_hypernyms_of_vehicle_include_transport(self):
        w = OwnWordNetWrapper('de')
        synsets = [s for s in w.translate('vehicle', 'en') if s.pos == 'n']
        hypernyms = w.getHypernyms(synsets)
        names = [h.name for h in hypernyms]
        assert 'transport' in names

    def test_hyponyms_of_vehicle_include_rocket(self):
        w = OwnWordNetWrapper('de')
        synsets = [s for s in w.translate('vehicle', 'en') if s.pos == 'n']
        hyponyms = w.getHyponyms(synsets)
        names = [h.name for h in hyponyms]
        assert 'rocket' in names

    def test_meronyms_of_house_include_porch(self):
        w = OwnWordNetWrapper('de')
        synsets = [s for s in w.translate('house', 'en') if s.pos == 'n']
        meronyms = w.getMeronyms(synsets)
        names = [m.name for m in meronyms]
        assert 'porch' in names

    def test_entailments_of_snore_include_sleep(self):
        w = OwnWordNetWrapper('de')
        synsets = [s for s in w.translate('snore', 'en') if s.pos == 'v']
        entailments = w.getEntailments(synsets)
        names = [e.name for e in entailments]
        assert 'sleep' in names

    def test_relation_extractors_return_empty_list_when_no_relation_exists(self):
        w = OwnWordNetWrapper('de')
        # A word chosen for having no antonym relation recorded, e.g. 'table' (noun)
        synsets = [s for s in w.translate('table', 'en') if s.pos == 'n']
        antonyms = w.getAntonyms(synsets)
        assert antonyms == []


class TestOwnWordNetWrapperLinguisticCounter:
    def test_counts_match_relation_extractor_lengths(self):
        w = OwnWordNetWrapper('de')
        synsets = [s for s in w.translate('vehicle', 'en') if s.pos == 'n']
        counter = w.getLinguisticCounter(synsets[0])
        assert counter.hypernym == len(synsets[0].hypernyms())
        assert counter.hyponym == len(synsets[0].hyponyms())
        assert counter.mt == 1


class TestOwnWordNetWrapperLanguageDescriptions:
    def test_generic_language_descriptions_populated_for_filter_langs(self):
        w = OwnWordNetWrapper('de,fr')
        synsets = [s for s in w.translate('house', 'en') if s.pos == 'n']
        gld = w.getGenericLanguageDescriptions(synsets[0])
        assert gld.getWordDescription('de') != ''
        assert gld.getWordDescription('fr') != ''

    def test_language_descriptions_and_generic_agree(self):
        w = OwnWordNetWrapper('de,fr')
        synsets = [s for s in w.translate('house', 'en') if s.pos == 'n']
        ld = w.getLanguageDescriptions(synsets[0])
        gld = w.getGenericLanguageDescriptions(synsets[0])
        assert ld.german == gld.getWordDescription('de')
        assert ld.french == gld.getWordDescription('fr')

    def test_synonyms_excludes_the_source_lemma(self):
        w = OwnWordNetWrapper('de')
        synsets = [s for s in w.translate('house', 'en') if s.pos == 'n']
        synonyms = w.getSynonyms(synsets[0], synsets[0].lemmas()[0])
        assert synsets[0].lemmas()[0] not in synonyms


class TestOwnWordNetWrapperWordKeys:
    def test_is_valid_word_key_requires_more_than_three_segments(self):
        w = OwnWordNetWrapper(None)
        assert w.isValidWordKey('house.v.02707688.ewn') is True
        assert w.isValidWordKey('house.02707688') is False

    def test_get_word_key_round_trips_through_synset_lookup(self):
        w = OwnWordNetWrapper('de')
        synsets = [s for s in w.translate('house', 'en') if s.pos == 'n']
        word = w.getWord(synsets[0])
        synset_id = w.getWordKey(word.wordKey)
        resolved = w.getWordKeySynset(synset_id, 'en')
        assert resolved.id == synsets[0].id


class TestOwnWordNetWrapperIli:
    def test_get_words_from_ili_returns_translation(self):
        w = OwnWordNetWrapper('de')
        synsets = [s for s in w.translate('house', 'en') if s.pos == 'n']
        ili = synsets[0].ili
        words = w.getWordsFromIli(ili, 'de')
        assert len(words) > 0
        assert all(word.lang == 'de' for word in words)

    def test_get_synsets_from_ili_returns_own_synset_wrappers(self):
        w = OwnWordNetWrapper('de')
        synsets = [s for s in w.translate('house', 'en') if s.pos == 'n']
        ili = synsets[0].ili
        result = w.getSynsetsFromIli(ili, 'de')
        assert len(result) > 0
        assert all(s.lang == 'de' for s in result)

    def test_unknown_ili_returns_empty_list(self):
        w = OwnWordNetWrapper('de')
        assert w.getWordsFromIli('i-does-not-exist', 'de') == []


class TestOwnWordNetWrapperLanguageCode:
    def test_maps_own_code_and_exclusions(self):
        w = OwnWordNetWrapper(None)
        assert w.getWordnetLanguageCode('de') == 'de'
        assert w.getWordnetLanguageCode('deu') == 'de'  # via exclusions map

    def test_filter_results_is_a_passthrough(self):
        w = OwnWordNetWrapper(None)
        assert w.filterResults(['a', 'b'], []) == ['a', 'b']


# ---------------------------------------------------------------------------
# NltkWordNetWrapper (NLTK WordNet backend, English data only)
# ---------------------------------------------------------------------------

class TestNltkWordNetWrapperTranslateAndPos:
    def test_translate_returns_synsets_for_known_word(self):
        w = NltkWordNetWrapper(None)
        synsets = w.translate('house', 'eng')
        assert len(synsets) > 0

    def test_translate_returns_empty_list_for_unknown_word(self):
        w = NltkWordNetWrapper(None)
        assert w.translate('zzznotarealword', 'eng') == []

    def test_translate_pos_filters_by_part_of_speech(self):
        w = NltkWordNetWrapper(None)
        nouns = w.translatePos('house', 'n', 'eng')
        assert len(nouns) > 0
        assert all(s.name().split('.')[1] == 'n' for s in nouns)

    def test_get_pos_description_maps_known_codes(self):
        w = NltkWordNetWrapper(None)
        assert w.getPOSDescription('n') == 'Noun'
        assert w.getPOSDescription('v') == 'Verb'
        assert w.getPOSDescription('a') == 'Adjective'
        assert w.getPOSDescription('s') == 'Adjective'
        assert w.getPOSDescription('r') == 'Adverb'

    def test_get_pos_description_raises_for_unknown_code(self):
        w = NltkWordNetWrapper(None)
        with pytest.raises(ValueError):
            w.getPOSDescription('not-a-pos')


class TestNltkWordNetWrapperGetWord:
    def test_get_word_populates_core_fields(self):
        w = NltkWordNetWrapper(None)
        synsets = w.translatePos('house', 'n', 'eng')
        word = w.getWord(synsets[0])
        assert word.name == 'house'
        assert word.pos == 'Noun'
        assert word.definition
        assert word.lang == 'en'
        assert word.wordnetId == 'nltk'
        assert word.wordKey == synsets[0].name()

    def test_get_word_by_pos_filters_correctly(self):
        w = NltkWordNetWrapper(None)
        synsets = w.translate('house', 'eng')
        nouns = w.getWordByPos(synsets, 'n', 'Noun')
        assert len(nouns) > 0
        assert all(word.pos == 'Noun' for word in nouns)


class TestNltkWordNetWrapperRelations:
    def test_antonyms_of_hot_include_cold(self):
        w = NltkWordNetWrapper(None)
        synsets = w.translatePos('hot', 'a', 'eng')
        antonyms = w.getAntonyms(synsets)
        names = [a.name for a in antonyms]
        assert 'cold' in names

    def test_hypernyms_of_vehicle_include_conveyance(self):
        # NLTK's Princeton WordNet uses 'conveyance' here, where the OMW/EWN
        # data behind OwnWordNetWrapper uses the synonym 'transport'.
        w = NltkWordNetWrapper(None)
        synsets = w.translatePos('vehicle', 'n', 'eng')
        hypernyms = w.getHypernyms(synsets)
        names = [h.name for h in hypernyms]
        assert 'conveyance' in names

    def test_hyponyms_of_vehicle_include_rocket(self):
        w = NltkWordNetWrapper(None)
        synsets = w.translatePos('vehicle', 'n', 'eng')
        hyponyms = w.getHyponyms(synsets)
        names = [h.name for h in hyponyms]
        assert 'rocket' in names

    def test_entailments_of_snore_include_sleep(self):
        w = NltkWordNetWrapper(None)
        synsets = w.translatePos('snore', 'v', 'eng')
        entailments = w.getEntailments(synsets)
        names = [e.name for e in entailments]
        assert 'sleep' in names


class TestNltkWordNetWrapperLinguisticCounter:
    def test_counts_match_relation_lengths(self):
        w = NltkWordNetWrapper(None)
        synsets = w.translatePos('vehicle', 'n', 'eng')
        counter = w.getLinguisticCounter(synsets[0])
        assert counter.hypernym == len(synsets[0].hypernyms())
        assert counter.hyponym == len(synsets[0].hyponyms())
        assert counter.mt == 1


class TestNltkWordNetWrapperWordKeys:
    def test_is_valid_word_key_requires_exactly_three_segments(self):
        w = NltkWordNetWrapper(None)
        assert w.isValidWordKey('house.n.01') is True
        assert w.isValidWordKey('house.n.01.extra') is False

    def test_get_word_key_is_identity(self):
        w = NltkWordNetWrapper(None)
        assert w.getWordKey('house.n.01') == 'house.n.01'

    def test_get_word_key_synset_resolves_real_synset(self):
        w = NltkWordNetWrapper(None)
        synset = w.getWordKeySynset('house.n.01', 'eng')
        assert synset.name() == 'house.n.01'


class TestNltkWordNetWrapperIliStubs:
    """NLTK backend has no ILI concept; both methods are intentionally stubbed to return []."""

    def test_get_words_from_ili_returns_empty_list(self):
        w = NltkWordNetWrapper(None)
        assert w.getWordsFromIli('i54960', 'eng') == []

    def test_get_synsets_from_ili_returns_empty_list(self):
        w = NltkWordNetWrapper(None)
        assert w.getSynsetsFromIli('i54960', 'eng') == []


class TestNltkWordNetWrapperLanguageCode:
    def test_maps_nltk_code_and_exclusions(self):
        w = NltkWordNetWrapper(None)
        assert w.getWordnetLanguageCode('eng') == 'eng'
        assert w.getWordnetLanguageCode('de') == 'deu'  # via exclusions map

    def test_filter_results_is_currently_a_passthrough(self):
        # NltkWordNetWrapper.filterResults has its filtering logic commented out
        # and unconditionally returns the input unchanged; documenting current behavior.
        w = NltkWordNetWrapper(None)
        assert w.filterResults(['a', 'b'], []) == ['a', 'b']
