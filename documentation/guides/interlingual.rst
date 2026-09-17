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

Each language yields at most one synset, because the ILI identifies a single
concept per lexicon. A single-language request therefore returns a list of
one, which is why the example above indexes with ``[0]`` — or unpacks it:

.. doctest::

    >>> italian, = happy.translate(lang="it")
    >>> italian.lemmas()
    ['felice']

``lang`` accepts the same forms as :class:`~passivlingo_dictionary.Wordnet`
itself: a single code, a space- or comma-separated string, or a list.

.. doctest::

    >>> sorted(s.lang for s in happy.translate(lang="de fr"))
    ['de', 'fr']
    >>> sorted(s.lang for s in happy.translate(lang=["de", "it"]))
    ['de', 'it']

Omit ``lang`` entirely to get every language the
:class:`~passivlingo_dictionary.Wordnet` was configured with:

.. doctest::

    >>> sorted(s.lang for s in happy.translate())
    ['de', 'en', 'es', 'fr', 'it', 'nl', 'pt']

.. note::

   The result includes the source synset itself, under its own language —
   ``en`` above. This follows ``wn``, whose ``translate()`` behaves the same
   way: the operation resolves an Interlingual Index identifier across
   lexicons, and the source lexicon is one of them.

   It is not what the name suggests, so filter explicitly when you want only
   the other languages:

   .. doctest::

       >>> others = [s for s in happy.translate() if s.lang != happy.lang]
       >>> sorted(s.lang for s in others)
       ['de', 'es', 'fr', 'it', 'nl', 'pt']

Every returned synset reports its own language, so results can be keyed by
language without tracking which request produced them:

.. doctest::

    >>> {s.lang: s.lemmas()[0] for s in happy.translate(lang="de fr it")}
    {'de': 'glücklich', 'fr': 'heureux', 'it': 'felice'}

:meth:`~passivlingo_dictionary.core.Word.translate` works the same way, at
the word level, returning a mapping of each of the word's senses to its
translated words:

.. doctest::

    >>> word = wordnet.words("happy", pos="a")[0]
    >>> {s: [w.lemma() for w in ws] for s, ws in word.translate(lang="it").items()}
    {Sense('happy', 'happy.a.01151786.ewn'): ['felice']}

Choosing between the three methods
--------------------------------------

Three methods reach across languages, and they differ in what they return
rather than in how they resolve:

.. list-table::
   :header-rows: 1
   :widths: 22 30 48

   * - Method
     - Returns
     - Use when you want
   * - ``translate(lang=...)``
     - ``list[Synset]``
     - Whole synsets, to read relations, examples, or ids from them
   * - ``descriptions(lang=...)``
     - ``dict[str, list[str]]``
     - Just the **word forms** per language
   * - ``definitions(lang=...)``
     - ``dict[str, str]``
     - Just the **glosses** per language

All three take ``lang`` in the same forms, and all three return empty results
on a backend without an ILI. ``translate()`` is the general case; the other
two are conveniences over it for the two things most callers want.

Which one to reach for
^^^^^^^^^^^^^^^^^^^^^^^^^

**Building a glossary or lookup table** — you want word forms, so
``descriptions()`` is the shortest route:

.. doctest::

    >>> glossary = pld.Wordnet(lang="de")
    >>> for term in ["vehicle", "engine"]:
    ...     forms = glossary.synsets(term, pos="n")[0].descriptions(lang="de")
    ...     print(term, "→", ", ".join(forms["de"][:3]))
    vehicle → Gefährt, Fahrgerät, Fahrmaschine
    engine → Motor

**Showing a definition to a reader in their own language** — you want the
gloss, so ``definitions()``:

.. doctest::

    >>> synset = wordnet.synsets("happy", pos="a")[0]
    >>> synset.definitions(lang="fr")["fr"]
    'qui jouit ou montre ou est marqué par la joie ou le plaisir.'

**Checking whether a concept is lexicalised in a language** — an empty list
of forms answers it directly:

.. doctest::

    >>> forms = synset.descriptions(lang="de fr")
    >>> {lang: bool(values) for lang, values in sorted(forms.items())}
    {'de': True, 'fr': True}

.. warning::

   This test is only meaningful against lexicons that record lexical gaps.
   The hybrid lexicons generate a lemma for every synset, so an empty result
   there means the lexicon is missing, not that the concept is unlexicalised.
   See :doc:`../faq`.

**Anything beyond forms and glosses** needs ``translate()``, because only it
returns whole synsets. Relations, examples and identifiers in the target
language are reachable no other way:

.. doctest::

    >>> german, = wordnet.synsets("vehicle", pos="n")[0].translate(lang="de")
    >>> german.id
    'Gefährt.n.04531608.inde'
    >>> [h.lemmas()[0] for h in german.hyponyms()][:3]
    ['Autoskooter', 'Fahrzeug', 'Militärfahrzeug']

Multilingual word forms in one call
----------------------------------------

:meth:`~passivlingo_dictionary.core.Synset.descriptions` returns a synset's
word forms across every configured language as a single dictionary, so you
don't need to call :meth:`translate` once per language:

.. doctest::

    >>> descriptions = happy.descriptions()
    >>> {lang: descriptions[lang] for lang in sorted(descriptions)}
    {'de': ['glücklich'], 'en': ['happy'], 'es': ['contento', 'feliz'], 'fr': ['heureux'], 'it': ['felice'], 'nl': ['gelukkig'], 'pt': ['contente', 'feliz']}

The synset's own language is included, and its entry is what
:meth:`~passivlingo_dictionary.core.Synset.lemmas` returns:

.. doctest::

    >>> happy.descriptions()[happy.lang] == happy.lemmas()
    True

Pass ``lang`` to restrict the result to one language or a specific list:

.. doctest::

    >>> happy.descriptions(lang="de")
    {'de': ['glücklich']}

Multilingual definitions
----------------------------

:meth:`~passivlingo_dictionary.core.Synset.descriptions` reports word forms.
For the glosses themselves, use
:meth:`~passivlingo_dictionary.core.Synset.definitions`, which resolves the
synset across languages and collects each one's definition:

.. doctest::

    >>> definitions = happy.definitions()
    >>> definitions["de"]
    'sich freuen oder Freude zeigen oder von Freude oder Vergnügen geprägt sein'
    >>> definitions["fr"]
    'qui jouit ou montre ou est marqué par la joie ou le plaisir.'

As with ``descriptions()``, the synset's own language is included:

.. doctest::

    >>> definitions["en"] == happy.definition()
    True

The ``lang`` argument works as it does for ``translate()`` and
``descriptions()`` — a single code, a space- or comma-separated string, or a
list:

.. doctest::

    >>> sorted(happy.definitions(lang="de fr"))
    ['de', 'fr']

Putting it together
-----------------------

A common task is assembling everything known about one concept across
languages — the word forms and the gloss side by side:

.. doctest::

    >>> synset = wordnet.synsets("happy", pos="a")[0]
    >>> descriptions = synset.descriptions()
    >>> definitions = synset.definitions()
    >>> for lang in ["de", "fr"]:
    ...     print(lang, "|", ", ".join(descriptions[lang]))
    ...     print("   ", definitions[lang])
    de | glücklich
        sich freuen oder Freude zeigen oder von Freude oder Vergnügen geprägt sein
    fr | heureux
        qui jouit ou montre ou est marqué par la joie ou le plaisir.

Note that a word usually has several senses, and each is a separate synset
with its own translations. Iterate over all of them rather than taking the
first, unless you have already disambiguated:

.. doctest::

    >>> rows = [
    ...     (synset.pos, synset.lemmas()[0],
    ...      synset.definitions(lang="de").get("de", "—").split(",")[0])
    ...     for synset in wordnet.synsets("happy")
    ... ]
    >>> for pos, lemma, german in sorted(rows):
    ...     print(pos, "|", lemma, "|", german)
    a | happy | sich freuen oder Freude zeigen oder von Freude oder Vergnügen geprägt sein
    a | happy | zufrieden oder mit den Dingen zufrieden
    s | gut gewählt | gut ausgedrückt und auf den Punkt gebracht
    s | happy | eifrig bereit
    s | happy | vom Glück begünstigt
    s | well-chosen | gut ausgedrückt und auf den Punkt gebracht

Requirements
--------------

Cross-lingual lookup requires the ``omw`` backend (the default) and the
target language's lexicon to be downloaded locally — see :doc:`../setup`.
It always returns an empty result on the ``nltk`` backend, which has no ILI
concept (see :doc:`../faq`). No network access is required; ILI resolution
is entirely local.
