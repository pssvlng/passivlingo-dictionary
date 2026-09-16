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


#: The German hybrid lexicon stands in for multilingual availability
#: generally: every multilingual fixture in the suite queries it.
HAS_MULTILINGUAL = has_lexicon('hyde')

#: Tests that assert on non-English wordnet content. Without a multilingual
#: lexicon installed the underlying `wn` package raises rather than returning
#: an empty result, so these are skipped wholesale instead of failing. The
#: English-only tests in these modules are skipped too; separating them would
#: mean annotating individual tests across six modules, and the English paths
#: are covered by the modules that remain.
_MULTILINGUAL_MODULES = frozenset({
    'test_wrappers',
    'test_search_chains',
    'test_extractors',
    'test_own_synset_wrapper',
})


def pytest_collection_modifyitems(config, items):
    """Skip multilingual tests when no multilingual lexicon is installed."""
    if HAS_MULTILINGUAL:
        return
    skip = pytest.mark.skip(
        reason="no multilingual wordnet lexicon installed (e.g. 'hyde'); "
               "install the hybrid lexicons to run the multilingual tests"
    )
    for item in items:
        if item.module.__name__.split('.')[-1] in _MULTILINGUAL_MODULES:
            item.add_marker(skip)


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
