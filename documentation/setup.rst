Installation and Setup
========================

Installing the package
-----------------------

.. code-block:: console

   $ pip install passivlingo-dictionary

Downloading wordnet data
--------------------------

The Open Multilingual WordNet family lexicons used by the ``omw`` backend
(the default — see :class:`passivlingo_dictionary.Wordnet`) are downloaded
via the :mod:`wn` package, and are not bundled with the package itself.
Download at least the English WordNet plus any other languages you plan to
query:

.. code-block:: python

   import wn

   wn.download('ewn:2020')     # English WordNet — always required
   wn.download('odenet:1.3')   # German
   wn.download('spawn:1.3+omw')  # Spanish
   wn.download('itawn:1.3+omw')  # Italian
   wn.download('omw-fr:1.4')     # French
   wn.download('omw-nl:1.4')     # Dutch
   wn.download('omw-pt:1.4')     # Portuguese

See the `wn documentation on lexicons
<https://wn.readthedocs.io/en/latest/guides/lexicons.html>`_ for the full
list of available projects, and :func:`wn.projects` to list what's
available versus what's already downloaded locally.

If you plan to use the ``nltk`` backend instead of (or in addition to) the
``omw`` backend, download NLTK's WordNet corpus:

.. code-block:: python

   import nltk

   nltk.download('wordnet')
   nltk.download('omw')

Note that NLTK's ``omw`` package provides limited multilingual coverage
compared to the dedicated per-language lexicons downloaded via :mod:`wn` —
see :doc:`faq` for details on the practical difference between the two
backends.

Optional: lemmatization support
---------------------------------

The lemmatization fallback (see :doc:`guides/fallback`) is backed by
spaCy. Install spaCy and the model(s) for the languages you query:

.. code-block:: console

   $ pip install spacy
   $ python -m spacy download en_core_web_sm
   $ python -m spacy download de_core_news_sm

A :class:`~passivlingo_dictionary.Wordnet` still works without spaCy
installed; queries simply skip the lemmatization fallback step for
languages with no available spaCy model.

Optional: machine-translation fallback
-----------------------------------------

To enable the machine-translation fallback for words with no wordnet entry
at all, construct a
:class:`~passivlingo_dictionary.translationProviders.GoogleTranslationProvider.GoogleTranslationProvider`
(requires a Google Cloud Translation API key) and pass it to
:class:`~passivlingo_dictionary.Wordnet`:

.. code-block:: python

   import passivlingo_dictionary as pld
   from passivlingo_dictionary.translationProviders.GoogleTranslationProvider import (
       GoogleTranslationProvider,
   )

   wordnet = pld.Wordnet(translator=GoogleTranslationProvider("your-api-key"))

This step is entirely optional — omit ``translator`` and
:meth:`~passivlingo_dictionary.Wordnet.words` simply returns an empty list
for words with no wordnet or lemmatized match.
