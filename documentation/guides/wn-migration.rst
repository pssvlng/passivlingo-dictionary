Migrating from wn
====================

If you have existing code using the `wn <https://wn.readthedocs.io>`_
package directly, passivlingo-dictionary's ``omw`` backend reads the same
underlying lexicon data and mirrors ``wn``'s object model closely, so most
code translates directly.

Entry point
-------------

.. code-block:: python

    # wn
    import wn
    w = wn.Wordnet(lang="de")

    # passivlingo_dictionary
    import passivlingo_dictionary as pld
    w = pld.Wordnet(backend="omw", lang="de")

Lookups
---------

.. code-block:: python

    # wn
    wn.synsets("house", pos="n")
    w.synsets("house", pos="n")

    # passivlingo_dictionary — identical call shape
    pld.synsets("house", pos="n")
    w.synsets("house", pos="n")

Relations and translation
----------------------------

``Synset.hypernyms()``, ``.hyponyms()``, ``.holonyms()``, ``.meronyms()``,
and ``.translate(lang=...)`` all exist with the same names and signatures
on :class:`passivlingo_dictionary.core.Synset` as on ``wn.Synset``.

Differences to be aware of
------------------------------

- passivlingo-dictionary adds ``antonyms()`` and ``entailments()`` as
  direct methods; in ``wn`` these are reached via the generic
  ``relations("antonym")`` / ``relations("entails")`` interface.
- :meth:`passivlingo_dictionary.core.Synset.descriptions` (multilingual
  glosses in one call) has no direct ``wn`` equivalent; the closest ``wn``
  approach is calling ``translate()`` once per target language and reading
  ``.lemmas()`` from each result.
- passivlingo-dictionary adds a second backend (``nltk``, NLTK's WordNet
  corpus) and automatic lemmatization/machine-translation fallback (see
  :doc:`fallback`) — features with no ``wn`` equivalent, since ``wn`` reads
  Open Multilingual WordNet-family data exclusively and does not fall back
  to any other source.
- ``wn``'s ``normalizer``/``lemmatizer`` constructor hooks and
  passivlingo-dictionary's ``lemmatizer`` constructor argument serve a
  similar purpose but are not interchangeable — ``wn``'s lemmatizer
  produces query *expansions* tried alongside the original form, while
  passivlingo-dictionary's is a strict fallback tried only after a direct
  match fails.

If your code only uses the pieces above, you can point it at
passivlingo-dictionary by changing the import and construction call —
everything downstream should work unchanged.
