"""Unit tests for tokenizers/ and posTaggers/. GenericTokenizer + SpacyPosTagger
are the pair actually used by FactoryMethods.getTokenizer (and thus
TextProcessor); DefaultTokenizer, EnglishTokenizer, and NltkPosTagger are
alternates not currently wired into that factory, but are still part of the
package's public surface and are smoke-tested directly here.
"""
import pytest

from passivlingo_dictionary.tokenizers.DefaultTokenizer import DefaultTokenizer
from passivlingo_dictionary.tokenizers.EnglishTokenizer import EnglishTokenizer
from passivlingo_dictionary.tokenizers.GenericTokenizer import GenericTokenizer
from passivlingo_dictionary.posTaggers.SpacyPosTagger import SpacyPosTagger
from passivlingo_dictionary.posTaggers.NltkPosTagger import NltkPosTagger
from passivlingo_dictionary.models.ContextWord import ContextWord

from conftest import skip_without_spacy_model

SENTENCE = 'The big dogs run quickly on www.example.com!'


class TestDefaultTokenizer:
    def test_extracts_content_words_tagged_as_unknown_pos(self):
        tokenizer = DefaultTokenizer(SENTENCE, None)
        result = tokenizer.tokenize()
        names = [word.name for word in result]
        assert 'dogs' in names
        assert all(word.pos == 'x' for word in result)

    def test_excludes_stopwords_and_domain_names(self):
        tokenizer = DefaultTokenizer(SENTENCE, None)
        result = tokenizer.tokenize()
        names = [word.name for word in result]
        assert 'the' not in names
        assert 'on' not in names
        assert 'www.example.com' not in names

    def test_returns_context_words(self):
        tokenizer = DefaultTokenizer(SENTENCE, None)
        result = tokenizer.tokenize()
        assert all(isinstance(word, ContextWord) for word in result)


class TestEnglishTokenizer:
    def test_tags_words_with_wordnet_pos_via_nltk(self):
        tokenizer = EnglishTokenizer(SENTENCE, None)
        result = tokenizer.tokenize()
        by_name = {word.name: word for word in result}
        assert by_name['dogs'].pos == 'n'
        assert by_name['run'].pos == 'v'
        assert by_name['quickly'].pos == 'r'
        assert by_name['big'].pos == 'a'

    def test_excludes_stopwords_and_domain_names(self):
        tokenizer = EnglishTokenizer(SENTENCE, None)
        result = tokenizer.tokenize()
        names = [word.name for word in result]
        assert 'the' not in names
        assert 'www.example.com' not in names


@skip_without_spacy_model('en_core_web_sm')
class TestGenericTokenizerWithSpacyPosTagger:
    def test_tags_words_with_wordnet_pos_and_lemma(self):
        tagger = SpacyPosTagger('en')
        tokenizer = GenericTokenizer(SENTENCE, 'en', tagger)
        result = tokenizer.tokenize()

        by_name = {word.name: word for word in result}
        assert by_name['dogs'].lemma == 'dog'
        assert by_name['dogs'].pos == 'n'
        assert by_name['run'].pos == 'v'
        assert by_name['quickly'].pos == 'r'
        assert by_name['big'].pos == 'a'

    def test_excludes_stopwords_and_domain_names(self):
        tagger = SpacyPosTagger('en')
        tokenizer = GenericTokenizer(SENTENCE, 'en', tagger)
        result = tokenizer.tokenize()
        names = [word.name for word in result]
        assert 'the' not in names
        assert 'on' not in names

    def test_disambiguation_disabled_by_default(self):
        tagger = SpacyPosTagger('en')
        tokenizer = GenericTokenizer(SENTENCE, 'en', tagger)
        assert tokenizer.useDisambiguation is False


@skip_without_spacy_model('en_core_web_sm')
class TestSpacyPosTagger:
    def test_tags_words_with_pos_and_lemma_triples(self):
        tagger = SpacyPosTagger('en')
        result = tagger.tagText('The dogs run quickly.')
        by_text = {text: (pos, lemma) for text, pos, lemma in result}
        assert by_text['dogs'] == ('NOUN', 'dog')
        assert by_text['run'] == ('VERB', 'run')
        assert by_text['quickly'] == ('ADV', 'quickly')


@skip_without_spacy_model('de_core_news_sm')
class TestSpacyPosTaggerGerman:
    def test_tags_german_words(self):
        tagger = SpacyPosTagger('de')
        result = tagger.tagText('Die Hunde laufen schnell.')
        texts = [text for text, pos, lemma in result]
        assert 'Hunde' in texts


class TestNltkPosTagger:
    def test_tags_words_with_penn_treebank_pos(self):
        tagger = NltkPosTagger()
        result = tagger.tagText('The dogs run quickly.')
        by_text = dict(result)
        assert by_text['dogs'] == 'NNS'
        assert by_text['run'] == 'VBP'
        assert by_text['quickly'] == 'RB'
