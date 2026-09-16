The Legacy Dictionary API
============================

Before the :class:`~passivlingo_dictionary.Wordnet` interface, this library
exposed a :class:`~passivlingo_dictionary.Dictionary.Dictionary` /
:class:`~passivlingo_dictionary.models.SearchParam.SearchParam` interface.
It remains fully supported at its existing import paths — nothing about it
has changed — but new code should prefer
:class:`~passivlingo_dictionary.Wordnet`. This guide is for maintaining
existing code, not for starting something new.

Side-by-side comparison
---------------------------

Basic lookup:

.. code-block:: python

    # legacy
    from passivlingo_dictionary.Dictionary import Dictionary
    from passivlingo_dictionary.models.SearchParam import SearchParam

    dictionary = Dictionary()
    param = SearchParam()
    param.woi = "house"
    results = dictionary.findWords(param)

    # current
    import passivlingo_dictionary as pld
    results = pld.words("house")

Category traversal (e.g. hypernyms) required a second round-trip through
the same method in the legacy API, resetting the same mutable
``SearchParam``:

.. code-block:: python

    # legacy
    param.reset()
    param.wordkey = results[0].wordKey
    param.category = "hypernym"
    param.lang = results[0].lang
    hypernyms = dictionary.findWords(param)

    # current — a direct method on the Synset you already have
    synset = pld.synsets("vehicle", pos="n")[0]
    hypernyms = synset.hypernyms()

Cross-lingual (ILI) lookup was likewise a second round-trip:

.. code-block:: python

    # legacy
    param.reset()
    param.ili = results[0].ili
    param.lang = "it"
    translated = dictionary.findWords(param)

    # current
    translated = synset.translate(lang="it")

Field name changes
---------------------

.. list-table::
   :header-rows: 1

   * - Legacy (``Word``)
     - Current (``Synset`` / ``Word``)
   * - ``word.wordKey``
     - ``synset.id``
   * - ``word.synonyms``
     - ``synset.lemmas()``
   * - ``word.pos`` (``'Noun'``, ...)
     - ``synset.pos`` (``'n'``, ...)
   * - ``word.linguisticCounter``
     - ``synset.relation_counts()``
   * - ``word.languageDescriptions`` / ``word.genericLanguageDescriptions``
     - ``synset.descriptions()``

Should I migrate existing code?
-----------------------------------

Not urgently. The legacy interface is not deprecated and has no planned
removal date. Migrate incrementally, or only for new code, at your own
pace.
