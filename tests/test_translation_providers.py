"""Unit tests for translationProviders/. EmptyTranslationProvider is tested
directly since it makes no network calls. Google/MyMemory/TextBlob providers
have their network calls mocked so the suite stays hermetic and fast; these
tests focus on request construction and response parsing/error handling.
"""
import json
from unittest.mock import patch, MagicMock

import pytest

from passivlingo_dictionary.translationProviders.EmptyTranslationProvider import EmptyTranslationProvider
from passivlingo_dictionary.translationProviders.GoogleTranslationProvider import GoogleTranslationProvider
from passivlingo_dictionary.translationProviders.MyMemTranslationProvider import MyMemTranslationProvider
from passivlingo_dictionary.translationProviders.TextBlobTranslationProvider import TextBlobTranslationProvider


class TestEmptyTranslationProvider:
    def test_translate_always_returns_empty_string(self):
        provider = EmptyTranslationProvider()
        assert provider.translate('en', 'de', 'house') == ''
        assert provider.translate(None, None, '') == ''


class _FakeHttpResponse:
    def __init__(self, body: bytes, status=200):
        self._body = body
        self.status = status

    def read(self):
        return self._body


class TestGoogleTranslationProvider:
    def test_builds_url_with_api_key_and_encodes_word(self):
        provider = GoogleTranslationProvider('my-api-key')
        assert 'my-api-key' in provider.baseUrl
        assert provider.baseUrl.startswith('https://translation.googleapis.com/language/translate/v2')

    @patch('passivlingo_dictionary.translationProviders.GoogleTranslationProvider.urlopen')
    def test_translate_parses_successful_response(self, mock_urlopen):
        body = json.dumps({'data': {'translations': [{'translatedText': 'Haus'}]}}).encode('utf-8')
        mock_urlopen.return_value = _FakeHttpResponse(body, status=200)

        provider = GoogleTranslationProvider('my-api-key')
        result = provider.translate('en', 'de', 'house')

        assert result == 'Haus'
        called_url = mock_urlopen.call_args[0][0].full_url
        assert 'house' in called_url
        assert 'target=de' in called_url

    @patch('passivlingo_dictionary.translationProviders.GoogleTranslationProvider.urlopen')
    def test_translate_joins_multiple_translations_with_comma(self, mock_urlopen):
        body = json.dumps({'data': {'translations': [
            {'translatedText': 'Haus'}, {'translatedText': 'Gebäude'},
        ]}}).encode('utf-8')
        mock_urlopen.return_value = _FakeHttpResponse(body, status=200)

        provider = GoogleTranslationProvider('my-api-key')
        result = provider.translate('en', 'de', 'house')

        assert result == 'Haus, Gebäude'

    @patch('passivlingo_dictionary.translationProviders.GoogleTranslationProvider.urlopen')
    def test_translate_returns_empty_string_on_non_200_status(self, mock_urlopen):
        mock_urlopen.return_value = _FakeHttpResponse(b'{}', status=500)

        provider = GoogleTranslationProvider('my-api-key')
        result = provider.translate('en', 'de', 'house')

        assert result == ''

    @patch('passivlingo_dictionary.translationProviders.GoogleTranslationProvider.urlopen')
    def test_translate_returns_empty_string_on_network_error(self, mock_urlopen):
        mock_urlopen.side_effect = OSError('network down')

        provider = GoogleTranslationProvider('my-api-key')
        result = provider.translate('en', 'de', 'house')

        assert result == ''

    @patch('passivlingo_dictionary.translationProviders.GoogleTranslationProvider.urlopen')
    def test_translate_returns_empty_string_on_malformed_json(self, mock_urlopen):
        mock_urlopen.return_value = _FakeHttpResponse(b'not json', status=200)

        provider = GoogleTranslationProvider('my-api-key')
        result = provider.translate('en', 'de', 'house')

        assert result == ''


class TestMyMemTranslationProvider:
    @patch('passivlingo_dictionary.translationProviders.MyMemTranslationProvider.urlopen')
    def test_translate_parses_successful_response(self, mock_urlopen):
        body = json.dumps({
            'responseStatus': 200,
            'responseData': {'translatedText': 'Haus'},
        }).encode('utf-8')
        mock_urlopen.return_value = _FakeHttpResponse(body, status=200)

        provider = MyMemTranslationProvider()
        result = provider.translate('en', 'de', 'house')

        assert result == 'Haus'
        called_url = mock_urlopen.call_args[0][0].full_url
        assert 'house' in called_url
        assert 'en|de' in called_url

    @patch('passivlingo_dictionary.translationProviders.MyMemTranslationProvider.urlopen')
    def test_translate_returns_empty_string_when_response_status_not_200(self, mock_urlopen):
        body = json.dumps({'responseStatus': 403, 'responseData': {}}).encode('utf-8')
        mock_urlopen.return_value = _FakeHttpResponse(body, status=200)

        provider = MyMemTranslationProvider()
        result = provider.translate('en', 'de', 'house')

        assert result == ''

    @patch('passivlingo_dictionary.translationProviders.MyMemTranslationProvider.urlopen')
    def test_translate_propagates_network_errors(self, mock_urlopen):
        # Unlike Google/TextBlob providers, MyMemTranslationProvider has no
        # try/except around the request, so network failures propagate.
        mock_urlopen.side_effect = OSError('network down')

        provider = MyMemTranslationProvider()
        with pytest.raises(OSError):
            provider.translate('en', 'de', 'house')


class TestTextBlobTranslationProvider:
    @patch('passivlingo_dictionary.translationProviders.TextBlobTranslationProvider.TextBlob')
    def test_translate_returns_translated_text(self, mock_textblob_cls):
        mock_blob = MagicMock()
        mock_blob.translate.return_value = 'Haus'
        mock_textblob_cls.return_value = mock_blob

        provider = TextBlobTranslationProvider()
        result = provider.translate('en', 'de', 'house')

        assert result == 'Haus'
        mock_blob.translate.assert_called_once_with(to='de')

    @patch('passivlingo_dictionary.translationProviders.TextBlobTranslationProvider.TextBlob')
    def test_translate_returns_empty_string_on_error(self, mock_textblob_cls):
        mock_blob = MagicMock()
        mock_blob.translate.side_effect = Exception('translation service unavailable')
        mock_textblob_cls.return_value = mock_blob

        provider = TextBlobTranslationProvider()
        result = provider.translate('en', 'de', 'house')

        assert result == ''
