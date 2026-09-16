Frequently Asked Questions
============================

Why two backends?
-------------------

:class:`passivlingo_dictionary.Wordnet` supports both an ``omw`` backend
(Open Multilingual WordNet-family lexicons, read via the :mod:`wn` package)
and an ``nltk`` backend (NLTK's WordNet corpus). They are not equivalent:

- The ``omw`` backend has genuinely per-language lexicon data (English,
  German, Spanish, French, Italian, Dutch, Portuguese, and more, depending
  on what you've downloaded — see :doc:`setup`), and every synset carries
  an Interlingual Index (ILI) identifier, which is what makes
  :meth:`~passivlingo_dictionary.core.Synset.translate` and
  :meth:`~passivlingo_dictionary.core.Synset.descriptions` work.
- The ``nltk`` backend's WordNet corpus is fundamentally the (English-only)
  Princeton WordNet; NLTK's separate ``omw`` add-on package provides some
  additional languages, but with materially thinner data and no ILI
  concept — :meth:`~passivlingo_dictionary.core.Synset.translate` always
  returns an empty list on this backend, and
  :meth:`~passivlingo_dictionary.core.Synset.descriptions` relies on a
  different code path (see
  :meth:`~passivlingo_dictionary.wrappers.NltkWordNetWrapper.NltkWordNetWrapper.getLanguageStr`).

If your use case is genuinely multilingual, use ``omw`` (the default). Use
``nltk`` when you specifically want Princeton WordNet's English synset
inventory or need compatibility with existing NLTK-based code.

Why do relation methods sometimes return unexpected words?
--------------------------------------------------------------

Because the underlying lexicons are lexical resources, not curated by this
library. For example, one of English WordNet's holonyms for ``house`` is
``zodiac`` — this is the sense of "house" as an astrological division
("planetary house"), which happens to be genuinely holonymically related to
one of the noun senses of "house" in the source data. Synset methods return
*all* matching relations for *all* senses of the queried word; if you only
want one sense, disambiguate first by inspecting
:meth:`~passivlingo_dictionary.core.Synset.definition` or
:meth:`~passivlingo_dictionary.core.Synset.pos`.

Does :meth:`Synset.translate` require an internet connection?
------------------------------------------------------------------

No. Cross-lingual lookup via :meth:`~passivlingo_dictionary.core.Synset.translate`
is entirely local: it resolves the shared Interlingual Index identifier
against whatever lexicons you've downloaded (see :doc:`setup`). It returns
an empty list if the target language's lexicon isn't downloaded, or if the
synset has no ILI (as is always the case on the ``nltk`` backend).

Machine translation (:doc:`guides/fallback`) is the only feature that makes
a network call, and only when you've explicitly configured a
``translator``.

How is this different from just using ``wn`` directly?
-----------------------------------------------------------

``wn`` is an excellent, focused library for reading Open Multilingual
WordNet-family data, and this library depends on it for the ``omw``
backend. passivlingo-dictionary adds:

- A second backend (NLTK's WordNet) behind the same interface.
- Automatic lemmatization and machine-translation fallback when a query
  word has no direct wordnet match — ``wn`` requires you to normalize word
  forms yourself (see ``wn``'s own :meth:`normalizer <wn.Wordnet>` and
  :meth:`lemmatizer <wn.Wordnet>` hooks, which passivlingo-dictionary wires
  up to spaCy by default).
- :meth:`~passivlingo_dictionary.core.Synset.descriptions`, returning a
  synset's word forms across every configured language in a single call.

See :doc:`guides/wn-migration` if you have existing ``wn``-based code and
want to switch.

I get a ``LanguageError`` for a language code I expect to work — why?
--------------------------------------------------------------------------

Both backends recognize a specific, fixed set of language codes (BCP-47-ish
short codes like ``de``, or ISO 639-3 codes like ``deu``, depending on
backend), listed in
:data:`passivlingo_dictionary.helpers.Constants.VALID_WORDNET_LANGS_OWN` and
:data:`passivlingo_dictionary.helpers.Constants.VALID_WORDNET_LANGS`. A
handful of languages are supported by one backend but explicitly excluded
from the other (for example, Farsi is recognized by ``nltk`` but not
``omw``) because the underlying lexicon data doesn't exist for that
backend/language combination. Check :doc:`faq` above for the ``omw`` vs.
``nltk`` distinction, and consider whether the other backend supports your
language.
