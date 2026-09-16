Interlingual Queries
======================

Cross-lingual lookup is this library's core differentiator over a
single-language wordnet interface. It works through the `Interlingual Index
<https://globalwordnet.github.io/gwadoc/>`_ (ILI): an identifier shared by
synsets across different language lexicons that represent the same concept.

Translating a synset
------------------------

.. doctest::

    >>> import passivlingo_dictionary as pld
    >>> wordnet = pld.Wordnet(lang="de fr es it nl pt")
    >>> happy = wordnet.synsets("happy", pos="a")[0]
    >>> [s.lemmas()[0] for s in happy.translate(lang="it")]
    ['felice']

Omit ``lang`` to get translations in every language the
:class:`~passivlingo_dictionary.Wordnet` was configured with:

.. doctest::

    >>> [s.lemmas() for s in happy.translate()]
    [['happy'], ['glücklich'], ['contento', 'feliz'], ['heureux'], ['felice'], ['gelukkig'], ['contente', 'feliz']]

:meth:`~passivlingo_dictionary.core.Word.translate` works the same way, at
the word level, returning a mapping of each of the word's senses to its
translated words:

.. doctest::

    >>> word = wordnet.words("happy", pos="a")[0]
    >>> {s: [w.lemma() for w in ws] for s, ws in word.translate(lang="it").items()}
    {Sense('happy', 'happy.a.01151786.ewn'): ['felice']}

Multilingual glosses in one call
------------------------------------

:meth:`~passivlingo_dictionary.core.Synset.descriptions` returns a synset's
word forms across every configured language as a single dictionary, so you
don't need to call :meth:`translate` once per language:

.. doctest::

    >>> descriptions = happy.descriptions()
    >>> {lang: descriptions[lang] for lang in sorted(descriptions)}
    {'de': ['glücklich'], 'en': [], 'es': ['contento', 'feliz'], 'fr': ['heureux'], 'it': ['felice'], 'nl': ['gelukkig'], 'pt': ['contente', 'feliz']}

.. note::

   The synset's own language always comes back with an empty list, since
   ``descriptions()`` reports *other* languages' word forms for the
   concept, not a restatement of the language you already queried in.

Pass ``lang`` to restrict the result to one language or a specific list:

.. doctest::

    >>> happy.descriptions(lang="de")
    {'de': ['glücklich']}

Requirements
--------------

Cross-lingual lookup requires the ``omw`` backend (the default) and the
target language's lexicon to be downloaded locally — see :doc:`../setup`.
It always returns an empty result on the ``nltk`` backend, which has no ILI
concept (see :doc:`../faq`). No network access is required; ILI resolution
is entirely local.
