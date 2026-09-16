"""Exception hierarchy for the passivlingo_dictionary public API.

All errors raised by the ``Wordnet``/``Word``/``Sense``/``Synset`` interface
in :mod:`passivlingo_dictionary.core` derive from :class:`Error`, so a caller
can catch every library-specific failure with a single ``except
passivlingo_dictionary.Error:`` clause, the same way :class:`wn.Error` works
in the `wn <https://wn.readthedocs.io>`_ package.

The legacy :class:`~passivlingo_dictionary.Dictionary.Dictionary` /
:class:`~passivlingo_dictionary.models.SearchParam.SearchParam` interface is
unaffected and continues to raise plain :class:`ValueError` as before.
"""


class Error(Exception):
    """Base class for all errors raised by the passivlingo_dictionary API."""


class BackendError(Error):
    """A lookup failed in the underlying WordNet backend (``wn`` or NLTK).

    Typically wraps a :class:`wn.Error` or an NLTK lookup failure that
    occurred while resolving a word, synset, or sense id.
    """


class LanguageError(Error):
    """A language code could not be resolved by the selected backend.

    Raised for language codes that are recognized by neither the ``omw``
    nor the ``nltk`` backend's language tables.
    """


class InvalidQueryError(Error):
    """The combination of arguments given to a query method is not valid."""
