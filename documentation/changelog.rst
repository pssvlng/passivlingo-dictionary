Changelog
===========

2.0.1
-------

Added
^^^^^^^

- :meth:`~passivlingo_dictionary.core.Synset.definitions`, returning the gloss
  per language — the multilingual counterpart of
  :meth:`~passivlingo_dictionary.core.Synset.definition`, as
  ``descriptions()`` is to ``lemmas()``.

Changed
^^^^^^^^^

- ``translate()`` accepts multiple languages, in the same forms as
  :class:`~passivlingo_dictionary.Wordnet` and ``descriptions()``: a single
  code, a space- or comma-separated string, or a sequence. Previously only a
  single code was accepted and ``'de fr'`` raised
  :class:`~passivlingo_dictionary.exceptions.LanguageError`. Existing
  single-language calls are unaffected.

- ``descriptions()`` now includes the synset's own language, whose entry
  equals :meth:`~passivlingo_dictionary.core.Synset.lemmas`. It previously
  returned an empty list for that language, on the reasoning that restating
  the queried lemmas added nothing — but this made a result incomplete with
  respect to the languages asked for, and disagreed with ``definitions()``,
  which already included it.

- ``translate()`` with no ``lang`` argument now returns the languages the
  owning :class:`~passivlingo_dictionary.Wordnet` was configured with, rather
  than every installed lexicon. It previously disagreed with
  ``descriptions()``, which already honoured the configuration, and with its
  own documentation. Callers who configured a narrow language set and relied
  on the wider result should pass ``lang`` explicitly.

Fixed
^^^^^^^

- ``translate()`` called with no ``lang`` argument returned synsets whose
  ``lang`` attribute was ``None``, because the requested language was stored
  on each result rather than the language the result belongs to. Each synset
  now reports its own language, which is what makes language-keyed mappings
  such as ``{s.lang: s.definition() for s in synset.translate()}`` possible.
  Calls that passed an explicit language were never affected.

- The configured languages were deduplicated through a set, leaving their
  order unspecified between runs. Anything iterating them — the default
  ``translate()``, the machine-translation fallback — could vary from one
  process to the next. Order now follows the configuration.

2.0.0
-------

The interface described throughout this documentation — :class:`Wordnet`,
:class:`Word`, :class:`Sense`, :class:`Synset` — is new in this release. The
earlier ``Dictionary`` / ``SearchParam`` interface remains available and
unchanged at its existing import paths; see :doc:`guides/legacy`.

Added
^^^^^^^

- :class:`~passivlingo_dictionary.Wordnet` as a configured entry point over
  both the ``omw`` and ``nltk`` backends, with a single object model across
  the two (:doc:`guides/basic`).
- Semantic relations as direct methods on
  :class:`~passivlingo_dictionary.core.Synset` (:doc:`guides/relations`).
- Interlingual Index lookup via
  :meth:`~passivlingo_dictionary.core.Synset.translate`, and multilingual
  word forms via :meth:`~passivlingo_dictionary.core.Synset.descriptions`
  (:doc:`guides/interlingual`).
- Retrieval-step provenance on results via ``Word.source``
  (:doc:`guides/fallback`).
- A typed exception hierarchy rooted at
  :class:`~passivlingo_dictionary.exceptions.Error`.

Fixed
^^^^^^^

- Queries against a language with no installed lexicon, and other failures
  originating in an underlying backend, now raise
  :class:`~passivlingo_dictionary.exceptions.BackendError` rather than
  letting a backend-specific exception escape.

- An empty or whitespace-only query form now returns no results. Previously
  the backends treated it as an unfiltered query and returned an arbitrary
  synset.

- :meth:`~passivlingo_dictionary.Wordnet.synset` raises
  :class:`~passivlingo_dictionary.exceptions.BackendError` for an
  unresolvable identifier. Previously a malformed identifier could return an
  unrelated synset.

- The ``nltk`` backend no longer fails when NLTK's optional Open Multilingual
  Wordnet corpus is absent; multilingual results are empty instead. The
  corpus is named differently across NLTK releases (``omw-1.4``,
  ``omw-2.0``), so requiring it made the backend fragile.
