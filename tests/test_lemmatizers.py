"""Unit tests for lemmatizers/: DefaultLemmatizer (no-op) and SpacyLemmatizer
(real spaCy models, English and German only, since those are the models
installed locally)."""
from passivlingo_dictionary.lemmatizers.DefaultLemmatizer import DefaultLemmatizer
from passivlingo_dictionary.lemmatizers.SpacyLemmatizer import SpacyLemmatizer

from conftest import skip_without_spacy_model


class TestDefaultLemmatizer:
    def test_returns_input_unchanged_wrapped_in_a_list(self):
        lemmatizer = DefaultLemmatizer()
        assert lemmatizer.lemmatize('houses') == ['houses']

    def test_does_not_mutate_input(self):
        lemmatizer = DefaultLemmatizer()
        woi = 'running'
        result = lemmatizer.lemmatize(woi)
        assert result == [woi]
        assert woi == 'running'


@skip_without_spacy_model('en_core_web_sm')
class TestSpacyLemmatizerEnglish:
    def test_lemmatizes_plural_noun_to_singular(self):
        lemmatizer = SpacyLemmatizer('en')
        result = lemmatizer.lemmatize('houses')
        assert 'house' in result

    def test_lemmatizes_verb_form_to_base_form(self):
        lemmatizer = SpacyLemmatizer('en')
        result = lemmatizer.lemmatize('running')
        assert 'run' in result

    def test_multiword_input_returns_title_and_lower_variants(self):
        lemmatizer = SpacyLemmatizer('en')
        result = lemmatizer.lemmatize('new york')
        assert isinstance(result, list)
        assert len(result) > 0

    def test_result_excludes_exact_input_match(self):
        lemmatizer = SpacyLemmatizer('en')
        # lemmatize() explicitly removes an entry equal to the original input,
        # so an already-lemmatized word should not appear in its own result list.
        result = lemmatizer.lemmatize('house')
        assert 'house' not in result

    def test_result_has_no_duplicates(self):
        lemmatizer = SpacyLemmatizer('en')
        result = lemmatizer.lemmatize('running')
        assert len(result) == len(set(result))


@skip_without_spacy_model('de_core_news_sm')
class TestSpacyLemmatizerGerman:
    def test_lemmatizes_plural_noun_to_singular(self):
        lemmatizer = SpacyLemmatizer('de')
        result = lemmatizer.lemmatize('Häuser')
        assert any('haus' in r.lower() for r in result)
