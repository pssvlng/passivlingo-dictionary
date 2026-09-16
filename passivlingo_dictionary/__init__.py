"""Multilingual WordNet access.

This package exposes a `wn <https://wn.readthedocs.io>`_-shaped interface
over two WordNet backends: the Open Multilingual WordNet family (via the
:mod:`wn` package) and NLTK's WordNet corpus. It additionally layers
lemmatization and machine-translation fallback on top of plain wordnet
lookups, and supports cross-lingual queries via the Interlingual Index.

Quick start:

    >>> import passivlingo_dictionary as pld
    >>> pld.synsets("house", pos="n")[0].definition()
    'a dwelling that serves as living quarters for one or more families'

For persistent configuration (a particular backend, a fixed set of
languages, a translation fallback), construct a :class:`Wordnet` once:

    >>> wordnet = pld.Wordnet(backend="omw", lang="de fr es it nl pt")
    >>> [s.lemmas()[0] for s in wordnet.synsets("vehicle", pos="n")[0].hypernyms()]
    ['transport']

The legacy :class:`~passivlingo_dictionary.Dictionary.Dictionary` /
:class:`~passivlingo_dictionary.models.SearchParam.SearchParam` interface
remains available, unchanged, at its existing import paths
(``passivlingo_dictionary.Dictionary``, ``passivlingo_dictionary.models``).
"""

from typing import List, Optional, Sequence, Union

from passivlingo_dictionary.core import RelationCounts, Sense, Synset, Word, Wordnet
from passivlingo_dictionary.exceptions import (
    BackendError,
    Error,
    InvalidQueryError,
    LanguageError,
)
from passivlingo_dictionary.translationProviders.TranslationProvider import (
    TranslationProvider,
)

#: Keep in step with the version declared in setup.py.
__version__ = '2.0.0'

__all__ = (
    '__version__',
    'Wordnet',
    'Word',
    'Sense',
    'Synset',
    'RelationCounts',
    'words',
    'senses',
    'synsets',
    'TranslationProvider',
    'Error',
    'BackendError',
    'LanguageError',
    'InvalidQueryError',
)


def words(
    form: str,
    *,
    pos: Optional[str] = None,
    lang: Union[str, Sequence[str], None] = None,
    backend: str = 'omw',
) -> List[Word]:
    """Return the list of matching words.

    This creates a :class:`Wordnet` using the *backend* and *lang*
    arguments; the remaining arguments are passed to
    :meth:`Wordnet.words`.

    Example:

        >>> words("houses")[0].lemma()
        'house'
    """
    return Wordnet(backend=backend, lang=lang).words(form, pos=pos, lang=None)


def synsets(
    form: str,
    *,
    pos: Optional[str] = None,
    lang: Union[str, Sequence[str], None] = None,
    backend: str = 'omw',
) -> List[Synset]:
    """Return the list of matching synsets.

    This creates a :class:`Wordnet` using the *backend* and *lang*
    arguments; the remaining arguments are passed to
    :meth:`Wordnet.synsets`.

    Example:

        >>> synsets("house", pos="n")[0].lemmas()[0]
        'house'
    """
    return Wordnet(backend=backend, lang=lang).synsets(form, pos=pos, lang=None)


def senses(
    form: str,
    *,
    pos: Optional[str] = None,
    lang: Union[str, Sequence[str], None] = None,
    backend: str = 'omw',
) -> List[Sense]:
    """Return the list of matching senses.

    This creates a :class:`Wordnet` using the *backend* and *lang*
    arguments; the remaining arguments are passed to
    :meth:`Wordnet.senses`.
    """
    return Wordnet(backend=backend, lang=lang).senses(form, pos=pos, lang=None)
