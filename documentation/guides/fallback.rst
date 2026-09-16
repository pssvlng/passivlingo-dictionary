Fallback: Lemmatization and Machine Translation
===================================================

:meth:`~passivlingo_dictionary.Wordnet.words`,
:meth:`~passivlingo_dictionary.Wordnet.synsets`, and
:meth:`~passivlingo_dictionary.Wordnet.senses` try, in order:

1. A direct match against the configured wordnet backend.
2. If nothing matches, lemmatize the query word and retry.
3. If still nothing matches and a ``translator`` was configured, fall back
   to machine translation.

Every :class:`~passivlingo_dictionary.core.Word` result carries a
:attr:`~passivlingo_dictionary.core.Word.source` attribute reporting which
of these three steps produced it: ``"wordnet"``, ``"lemmatized"``, or
``"machine_translation"``.

Lemmatization fallback
-------------------------

Enabled by default, backed by spaCy (see :doc:`../setup` for installing
language models). No configuration needed:

.. doctest::

    >>> import passivlingo_dictionary as pld
    >>> wordnet = pld.Wordnet(lang="de")
    >>> words = wordnet.words("houses")
    >>> words[0].lemma()
    'house'
    >>> words[0].source
    'lemmatized'

A direct match (no lemmatization needed) reports ``source == "wordnet"``
instead:

.. doctest::

    >>> wordnet.words("house")[0].source
    'wordnet'

Machine-translation fallback
--------------------------------

Opt-in: pass a
:class:`~passivlingo_dictionary.translationProviders.TranslationProvider.TranslationProvider`
instance when constructing the :class:`~passivlingo_dictionary.Wordnet`.
This is only reached for query words with no wordnet entry and no
lemmatized match:

.. doctest::

    >>> from passivlingo_dictionary.translationProviders.GoogleTranslationProvider import (
    ...     GoogleTranslationProvider,
    ... )
    >>> wordnet = pld.Wordnet(lang="de", translator=GoogleTranslationProvider("your-api-key"))
    >>> words = wordnet.words("some-word-genuinely-absent-from-wordnet")
    >>> words[0].source  # doctest: +SKIP
    'machine_translation'

Without a configured ``translator``, a query with no wordnet or lemmatized
match simply returns an empty list — it never raises.

Custom lemmatizers
--------------------

Pass a callable ``lemmatizer=lambda word: [...]`` to
:class:`~passivlingo_dictionary.Wordnet` to override the default
spaCy-backed lemmatizer, for example to plug in a lemmatizer for a language
spaCy doesn't support, or to disable lemmatization entirely by returning an
empty list.
