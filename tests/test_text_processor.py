"""Unit tests for TextProcessor: sentence/paragraph tokenization built on
NLTK's sentence splitter and a spaCy-backed GenericTokenizer. Uses the real
English spaCy model since it's installed locally.
"""
import pytest

from passivlingo_dictionary.TextProcessor import TextProcessor
from passivlingo_dictionary.models.ContextWord import ContextWord

from conftest import skip_without_spacy_model


@pytest.fixture
def text_processor():
    return TextProcessor()


class TestTokenizeParagraph:
    def test_splits_paragraph_into_sentences(self, text_processor):
        result = text_processor.tokenizeParagraph('Hello world. This is a test sentence.')
        assert result == ['Hello world.', 'This is a test sentence.']

    def test_raises_when_paragraph_is_none(self, text_processor):
        with pytest.raises(ValueError, match="'paragraph' required"):
            text_processor.tokenizeParagraph(None)

    def test_url_decodes_input(self, text_processor):
        result = text_processor.tokenizeParagraph('Hello%20world.')
        assert result == ['Hello world.']


@skip_without_spacy_model('en_core_web_sm')
class TestTokenizeSentence:
    def test_extracts_content_words_with_lemma_and_pos(self, text_processor):
        result = text_processor.tokenizeSentence(
            'The big black dogs came into the living room quietly.', 'en'
        )
        assert all(isinstance(word, ContextWord) for word in result)

        by_name = {word.name: word for word in result}
        assert by_name['dogs'].lemma == 'dog'
        assert by_name['dogs'].pos == 'n'
        assert by_name['came'].lemma == 'come'
        assert by_name['came'].pos == 'v'
        assert by_name['quietly'].pos == 'r'
        assert by_name['big'].pos == 'a'

    def test_excludes_stopwords_and_function_words(self, text_processor):
        result = text_processor.tokenizeSentence(
            'The big black dogs came into the living room quietly.', 'en'
        )
        names = [word.name for word in result]
        assert 'the' not in names
        assert 'into' not in names

    def test_raises_when_sentence_is_none(self, text_processor):
        with pytest.raises(ValueError, match="'lang' and 'sent' required"):
            text_processor.tokenizeSentence(None, 'en')

    def test_raises_when_lang_is_none(self, text_processor):
        with pytest.raises(ValueError, match="'lang' and 'sent' required"):
            text_processor.tokenizeSentence('The dog runs.', None)
