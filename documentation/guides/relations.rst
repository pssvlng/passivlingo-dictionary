Semantic Relations
=====================

Every :class:`~passivlingo_dictionary.core.Synset` exposes its semantic
relations to other synsets as methods — no separate query or category
parameter needed.

.. doctest::

    >>> import passivlingo_dictionary as pld
    >>> wordnet = pld.Wordnet(lang="de")
    >>> vehicle = wordnet.synsets("vehicle", pos="n")[0]

Hypernyms and hyponyms
------------------------

Hypernyms are more general concepts; hyponyms are more specific ones.

.. doctest::

    >>> [s.lemmas()[0] for s in vehicle.hypernyms()]
    ['transport']
    >>> [s.lemmas()[0] for s in vehicle.hyponyms()][:3]
    ['Dodgem', 'craft', 'military vehicle']

Antonyms
----------

.. doctest::

    >>> hot = wordnet.synsets("hot", pos="a")[0]
    >>> [s.lemmas()[0] for s in hot.antonyms()]
    ['cold']

Meronyms and holonyms
------------------------

Meronyms are parts of the queried concept; holonyms are wholes the queried
concept is a part of.

.. doctest::

    >>> house = wordnet.synsets("house", pos="n")[0]
    >>> [s.lemmas()[0] for s in house.meronyms()][:4]
    ['library', 'garret', 'porch', 'study']

.. note::

   Relations reflect the full lexical data for every sense of the queried
   word, which can surface results that look surprising out of context —
   see :doc:`../faq` for a worked example with ``house``'s holonyms.

Entailments
-------------

For verbs: an entailment is an action necessarily implied by the queried
action.

.. doctest::

    >>> snore = wordnet.synsets("snore", pos="v")[0]
    >>> [s.lemmas()[0] for s in snore.entailments()]
    ['sleep']

Relation counts
------------------

To get a quick summary of how many related synsets exist for each relation
type, without fetching the synsets themselves:

.. doctest::

    >>> counts = vehicle.relation_counts()
    >>> counts.hypernym, counts.hyponym
    (1, 9)

Generic relation access
--------------------------

:meth:`~passivlingo_dictionary.core.Synset.relations` returns a dictionary
of relation name to related synsets, useful when the relation type is
chosen dynamically:

.. doctest::

    >>> result = vehicle.relations("hypernym", "hyponym")
    >>> sorted(result.keys())
    ['hypernym', 'hyponym']

Called with no arguments, it returns every supported relation
(``antonym``, ``hypernym``, ``hyponym``, ``holonym``, ``meronym``,
``entailment``).
