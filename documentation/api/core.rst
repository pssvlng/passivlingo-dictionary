passivlingo_dictionary
=======================

.. module:: passivlingo_dictionary

This is the primary public API: a :class:`Wordnet` entry point and the
:class:`Word`, :class:`Sense`, and :class:`Synset` objects it returns.

Module-level functions
-----------------------

For one-off queries against a single backend, the top-level ``words()``,
``synsets()``, and ``senses()`` functions construct a throwaway
:class:`Wordnet` internally:

.. autofunction:: words
.. autofunction:: synsets
.. autofunction:: senses

Wordnet
-------

.. autoclass:: Wordnet
   :members:

Synset
------

.. autoclass:: passivlingo_dictionary.core.Synset
   :members:

Word
----

.. autoclass:: passivlingo_dictionary.core.Word
   :members:

Sense
-----

.. autoclass:: passivlingo_dictionary.core.Sense
   :members:

RelationCounts
--------------

.. autoclass:: RelationCounts
   :members:
