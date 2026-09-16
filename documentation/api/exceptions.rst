passivlingo_dictionary.exceptions
===================================

.. module:: passivlingo_dictionary.exceptions

All errors raised by the :class:`~passivlingo_dictionary.Wordnet` /
:class:`~passivlingo_dictionary.Word` / :class:`~passivlingo_dictionary.Sense`
/ :class:`~passivlingo_dictionary.Synset` interface derive from
:class:`Error`, so a single ``except passivlingo_dictionary.Error:`` clause
catches every library-specific failure.

.. autoclass:: Error
.. autoclass:: BackendError
.. autoclass:: LanguageError
.. autoclass:: InvalidQueryError
