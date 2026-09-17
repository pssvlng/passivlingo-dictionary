passivlingo-dictionary
=======================

**passivlingo-dictionary** is a Python library for multilingual WordNet
access. It provides a single, `wn <https://wn.readthedocs.io>`_-shaped
interface over two backends — the Open Multilingual WordNet family (via the
:mod:`wn` package) and NLTK's WordNet corpus — and adds:

- **Cross-lingual queries** out of the box, via the Interlingual Index (ILI):
  look up a word in one language and get its synonyms, definitions, and
  relations in every other configured language.
- **Automatic fallback** through lemmatization and, optionally, machine
  translation when a query word has no direct wordnet entry.
- **Relation methods on the objects themselves** (``synset.hypernyms()``,
  ``synset.antonyms()``, ...), so working with hypernymy, antonymy,
  meronymy, holonymy, and entailment relations doesn't require a second
  round-trip query.

.. doctest::

    >>> import passivlingo_dictionary as pld
    >>> synset = pld.synsets("house", pos="n")[0]
    >>> synset.definition()
    'a dwelling that serves as living quarters for one or more families'
    >>> [s.lemmas()[0] for s in synset.hypernyms()]
    ['home', 'edifice']

    >>> wordnet = pld.Wordnet(lang="de fr es it nl pt")
    >>> happy = wordnet.synsets("happy", pos="a")[0]
    >>> [s.lemmas()[0] for s in happy.translate(lang="it")]
    ['felice']

Getting started
---------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   setup
   faq
   changelog

Guides
------

.. toctree::
   :maxdepth: 2
   :caption: Guides

   guides/basic
   guides/relations
   guides/interlingual
   guides/fallback
   guides/wn-migration
   guides/legacy

API Reference
-------------

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/core
   api/exceptions
   api/legacy

Indices
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
