"""Shared pytest fixtures and resource-availability helpers for the passivlingo_dictionary test suite.

Tests in this suite run against real, locally-installed WordNet data (the ``wn``
package's OMW-based lexicons and NLTK's WordNet corpus) and real spaCy models
where available. Only outbound network calls (Google Translate, MyMemory,
TextBlob) are mocked, since hitting live translation services in a unit test
suite would make it slow, flaky, and dependent on API keys/quotas.

Resource availability is machine-dependent, so tests that need a resource not
installed locally are skipped with a clear reason rather than failed.
"""
import pytest
import spacy.util


INSTALLED_SPACY_MODELS = set(spacy.util.get_installed_models())


def _installed_lexicons():
    try:
        import wn
        return {lexicon.id for lexicon in wn.lexicons()}
    except Exception:
        return set()


INSTALLED_LEXICONS = _installed_lexicons()

#: Lexicons required by the multilingual tests. The hybrid wordnets of Bergh
#: et al. (2025) are not on the public `wn` project index, so an environment
#: that has not installed them (a fresh CI runner, for instance) skips the
#: tests that need them rather than failing.
MULTILINGUAL_LEXICONS = ('hyde', 'hyes', 'hyfr', 'hyit', 'hynl', 'hypt')


def has_spacy_model(model_name: str) -> bool:
    return model_name in INSTALLED_SPACY_MODELS


def skip_without_spacy_model(model_name: str):
    return pytest.mark.skipif(
        not has_spacy_model(model_name),
        reason=f"spaCy model '{model_name}' is not installed locally",
    )


def has_lexicon(lexicon_id: str) -> bool:
    return lexicon_id in INSTALLED_LEXICONS


def skip_without_lexicon(lexicon_id: str):
    return pytest.mark.skipif(
        not has_lexicon(lexicon_id),
        reason=f"wordnet lexicon '{lexicon_id}' is not installed locally",
    )


@pytest.fixture
def mock_translation_response(monkeypatch):
    """Patch urlopen so translation providers never make real network calls.

    Usage: mock_translation_response(json_body, status=200) configures the
    canned HTTP response; the fixture returns the configurator function.
    """
    import json as json_module
    import io

    class _FakeResponse:
        def __init__(self, body: bytes, status: int):
            self._body = body
            self.status = status

        def read(self):
            return self._body

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    def _configure(json_body=None, status=200, raw_body=None, module=None):
        body = raw_body if raw_body is not None else json_module.dumps(json_body).encode('utf-8')

        def _fake_urlopen(req, *args, **kwargs):
            return _FakeResponse(body, status)

        monkeypatch.setattr(module + '.urlopen', _fake_urlopen)

    return _configure
