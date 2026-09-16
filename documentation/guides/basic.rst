Basic Usage
=============

Module-level functions vs. :class:`~passivlingo_dictionary.Wordnet`
------------------------------------------------------------------------

For a one-off query, the top-level functions are the quickest way in:

.. doctest::

    >>> import passivlingo_dictionary as pld
    >>> pld.synsets("house", pos="n")[0].definition()
    'a dwelling that serves as living quarters for one or more families'

Each call to :func:`~passivlingo_dictionary.words`,
:func:`~passivlingo_dictionary.synsets`, or
:func:`~passivlingo_dictionary.senses` constructs a throwaway
:class:`~passivlingo_dictionary.Wordnet` internally. If you're making more
than one query, or want to fix a backend, a set of languages, or a
translation fallback, construct a :class:`~passivlingo_dictionary.Wordnet`
once instead:

.. doctest::

    >>> wordnet = pld.Wordnet(backend="omw", lang="de fr es it nl pt")
    >>> len(wordnet.words("house"))
    30

Words, synsets, and senses
-----------------------------

Three related but distinct concepts, matching WordNet's own terminology
(and `wn`'s object model):

- A :class:`~passivlingo_dictionary.core.Word` is a lexical entry — a
  spelling, independent of meaning.
- A :class:`~passivlingo_dictionary.core.Synset` is a set of synonymous
  word senses corresponding to one concept — this is where definitions,
  examples, and relations (hypernyms, antonyms, ...) live.
- A :class:`~passivlingo_dictionary.core.Sense` is the pairing of one word
  with one synset — the specific meaning that word has in that synset.

.. doctest::

    >>> synset = wordnet.synsets("house", pos="n")[0]
    >>> synset.id
    'house.n.03549540.ewn'
    >>> synset.pos
    'n'
    >>> synset.lang
    'en'
    >>> synset.examples()
    ['he has a house on Cape Cod', 'she felt she had to get out of the house']
    >>> [word.lemma() for word in synset.words()]
    ['house']

Filtering by part of speech
------------------------------

Pass ``pos`` as a single-letter WordNet part-of-speech code (``n``, ``v``,
``a`` for adjective, ``r`` for adverb) to any query method:

.. doctest::

    >>> nouns = wordnet.synsets("house", pos="n")
    >>> verbs = wordnet.synsets("house", pos="v")
    >>> all(s.pos == "n" for s in nouns)
    True

Without ``pos``, a query returns matches across every part of speech.

Choosing a backend
---------------------

``backend="omw"`` (the default) reads Open Multilingual WordNet-family
lexicons via the :mod:`wn` package and is the right choice for anything
multilingual. ``backend="nltk"`` reads NLTK's WordNet corpus instead. See
:doc:`../faq` for when each is appropriate.

.. doctest::

    >>> nltk_wordnet = pld.Wordnet(backend="nltk")
    >>> nltk_wordnet.synsets("house", pos="n")[0].id
    'house.n.01'
