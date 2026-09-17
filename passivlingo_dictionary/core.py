"""The passivlingo_dictionary public API: :class:`Wordnet`, :class:`Word`,
:class:`Sense`, :class:`Synset`, and :class:`RelationCounts`.

This module's object model is deliberately shaped like the `wn
<https://wn.readthedocs.io>`_ package's: construct a :class:`Wordnet` once
with the backend and languages you care about, then query it for
:class:`Word`/:class:`Synset`/:class:`Sense` objects that expose relations
(:meth:`Synset.hypernyms`, :meth:`Synset.antonyms`, ...) and cross-lingual
lookup (:meth:`Synset.translate`) as methods, instead of building up a
mutable search-parameter object and re-issuing a second search.

Unlike ``wn``, which only reads Open Multilingual WordNet-family data, this
module additionally supports an NLTK WordNet backend, layers a
lemmatization + machine-translation fallback on top of plain lookups, and
exposes multilingual glosses for a synset in one call
(:meth:`Synset.descriptions`).

This is a thin layer over the existing backend implementations in
:mod:`passivlingo_dictionary.wrappers`; none of the underlying matching or
relation-extraction logic changes here. The legacy
:class:`~passivlingo_dictionary.Dictionary.Dictionary` /
:class:`~passivlingo_dictionary.models.SearchParam.SearchParam` interface
that this module wraps remains available, unchanged, at its existing import
paths.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
from typing import Callable, Dict, List, Optional, Sequence, Union

from passivlingo_dictionary.exceptions import (
    BackendError,
    Error as PassivlingoError,
    LanguageError,
)
from passivlingo_dictionary.helpers.Constants import (
    VALID_WORDNET_LANGS,
    VALID_WORDNET_LANGS_OWN,
    WORDNET_IDENTIFIER_NLTK,
    WORDNET_IDENTIFIER_OWN,
)
from passivlingo_dictionary.helpers.FactoryMethods import FactoryMethods
from passivlingo_dictionary.translationProviders.TranslationProvider import (
    TranslationProvider,
)
from passivlingo_dictionary.wrappers.NltkWordNetWrapper import NltkWordNetWrapper
from passivlingo_dictionary.wrappers.OwnWordNetWrapper import OwnWordNetWrapper
from passivlingo_dictionary.wrappers.WordNetWrapper import WordNetWrapper

__all__ = ('Wordnet', 'Word', 'Sense', 'Synset', 'RelationCounts')

_RELATION_METHODS = (
    'antonym', 'hypernym', 'hyponym', 'holonym', 'meronym', 'entailment',
)

LemmatizeFunction = Callable[[str], List[str]]


@dataclass(frozen=True)
class RelationCounts:
    """An immutable snapshot of how many related synsets a synset has.

    Example:

        >>> wordnet = Wordnet(lang="de")
        >>> synset = wordnet.synsets("vehicle", pos="n")[0]
        >>> synset.relation_counts().hypernym
        1
    """

    antonym: int
    hypernym: int
    hyponym: int
    holonym: int
    meronym: int
    entailment: int
    mt: int


def _backend_name(wrapper: WordNetWrapper) -> str:
    return 'nltk' if isinstance(wrapper, NltkWordNetWrapper) else 'omw'


def _normalize_lang(lang: Union[str, Sequence[str], None]) -> Optional[str]:
    """Convert a language argument into the comma-joined string the
    underlying wrapper classes expect."""
    if lang is None:
        return None
    if isinstance(lang, str):
        # Accept both space- and comma-separated strings, mirroring wn's
        # BCP-47-list convention (e.g. "de fr es") as well as this
        # library's existing comma convention.
        parts = lang.replace(',', ' ').split()
    else:
        parts = list(lang)
    return ','.join(parts) if parts else None


#: Public backend name -> internal wordnet-identifier constant. The 'own'
#: identifier is this library's historical internal codename for the
#: OMW/wn-package-backed data; 'omw' is the honest public name for it.
_BACKEND_IDENTIFIERS = {
    'omw': WORDNET_IDENTIFIER_OWN,
    'nltk': WORDNET_IDENTIFIER_NLTK,
}


def _make_wrapper(backend: str, lang: Optional[str]) -> WordNetWrapper:
    identifier = _BACKEND_IDENTIFIERS.get(backend)
    if identifier is None:
        raise LanguageError(
            f"Unknown backend: '{backend}' (expected 'omw' or 'nltk')"
        )
    if identifier == WORDNET_IDENTIFIER_NLTK:
        return NltkWordNetWrapper(lang)
    return OwnWordNetWrapper(lang)


def _wrap_language_errors(func):
    """Translate errors raised beneath the public API into the documented
    exception hierarchy.

    A bare ``ValueError`` from the language-map lookups in the legacy wrapper
    classes becomes :class:`LanguageError`. Errors raised by an underlying
    backend — for example :class:`wn.Error` when no lexicon is installed for a
    requested language — become :class:`BackendError`, so that callers can rely
    on ``except passivlingo_dictionary.Error`` catching every failure this
    package originates.
    """

    @wraps(func)
    def _wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PassivlingoError:
            raise
        except ValueError as exc:
            raise LanguageError(str(exc)) from exc
        except Exception as exc:
            if _is_backend_error(exc):
                raise BackendError(str(exc)) from exc
            raise

    return _wrapped


def _is_backend_error(exc: BaseException) -> bool:
    """True if *exc* originates in one of the wrapped backend libraries.

    Covers both exception types defined by those libraries (``wn.Error`` and
    NLTK's own exceptions) and the builtin :class:`LookupError` that NLTK
    raises when a required corpus has not been downloaded — the latter is a
    builtin, so it is matched by traceback origin rather than by module.
    """
    if type(exc).__module__.split('.')[0] in ('wn', 'nltk'):
        return True
    if isinstance(exc, LookupError):
        # NLTK signals a missing corpus with a plain LookupError; attribute it
        # to the backend if any frame in the traceback comes from nltk or wn.
        traceback = exc.__traceback__
        while traceback is not None:
            module = traceback.tb_frame.f_globals.get('__name__', '')
            if module.split('.')[0] in ('wn', 'nltk'):
                return True
            traceback = traceback.tb_next
    return False


class Synset:
    """A set of synonymous word senses, corresponding to a single concept.

    Synset objects are not constructed directly; obtain them from
    :meth:`Wordnet.synsets`, :meth:`Wordnet.synset`, or from another
    Synset's relation methods.
    """

    __slots__ = ('_wrapper', '_raw')

    def __init__(self, wrapper: WordNetWrapper, raw_synset):
        self._wrapper = wrapper
        self._raw = raw_synset

    @property
    def id(self) -> str:
        """The backend-qualified identifier of this synset."""
        if _backend_name(self._wrapper) == 'nltk':
            # Read the identifier straight from the synset. Deriving it via
            # the wrapper's getWord() would eagerly build multilingual
            # descriptions, which requires NLTK's optional OMW corpus and
            # fails when only the core wordnet corpus is installed.
            return self._raw.name()
        return self._wrapper.getWord(self._raw).wordKey

    @property
    def ili(self) -> Optional[str]:
        """The Interlingual Index identifier linking this synset across
        languages, or ``None`` if unavailable (e.g. the NLTK backend, which
        has no ILI concept)."""
        return getattr(self._raw, 'ili', None) or None

    @property
    def pos(self) -> str:
        """The single-letter part-of-speech code (``n``, ``v``, ``a``, ``r``, ...)."""
        if _backend_name(self._wrapper) == 'nltk':
            # NLTK synsets encode POS in their name, e.g. 'house.n.01';
            # Synset.pos is a *method* there, not a plain attribute.
            return self._raw.name().split('.')[1]
        return self._raw.pos

    @property
    def lang(self) -> str:
        """The BCP-47-style language code of this synset."""
        if _backend_name(self._wrapper) == 'nltk':
            # NLTK's Synset has no language attribute; this backend is English-only.
            return 'en'
        return self._raw.lang

    @property
    def backend(self) -> str:
        """Which backend this synset came from: ``'omw'`` or ``'nltk'``."""
        return _backend_name(self._wrapper)

    def definition(self) -> Optional[str]:
        """Return the synset's gloss/definition in its own language.

        Example:

            >>> Wordnet().synsets("house", pos="n")[0].definition()
            'a dwelling that serves as living quarters for one or more families'
        """
        raw_def = self._raw.definition()
        return raw_def if raw_def else None

    @_wrap_language_errors
    def definitions(
        self, lang: Union[str, Sequence[str], None] = None
    ) -> Dict[str, str]:
        """Return this synset's definition in each language, keyed by language
        code.

        Where :meth:`definition` gives the gloss in the synset's own language,
        this resolves the synset across languages through its Interlingual
        Index and collects each one's gloss.

        Arguments:
            lang: restrict the result to one or more languages, given the same
                way as to :class:`Wordnet` — a single code (``'de'``), a
                space- or comma-separated string (``'de fr'``), or a list of
                codes. If omitted, returns every language configured on the
                owning :class:`Wordnet`.

        The synset's own language is included when it falls within the
        requested set. Languages whose counterpart carries no gloss are
        omitted, and the result is empty on a backend without an ILI.

        Example:

            >>> synset = Wordnet(lang="de fr").synsets("happy", pos="a")[0]
            >>> synset.definitions(lang="de")
            {'de': 'sich freuen oder Freude zeigen oder von Freude oder Vergnügen geprägt sein'}
        """
        result = {}
        for translated in self.translate(lang=lang):
            definition = translated.definition()
            if translated.lang and definition:
                result[translated.lang] = definition
        return result

    def examples(self) -> List[str]:
        """Return example sentences using this synset's words."""
        return [ex.replace('"', '') for ex in self._raw.examples()]

    def lemmas(self) -> List[str]:
        """Return every word form belonging to this synset.

        Example:

            >>> Wordnet().synsets("house", pos="n")[0].lemmas()[0]
            'house'
        """
        raw_lemmas = self._raw.lemmas()
        names = [lemma.name() if hasattr(lemma, 'name') else lemma for lemma in raw_lemmas]
        return [name.replace('_', ' ') for name in names]

    def words(self) -> List['Word']:
        """Return the words that are members of this synset."""
        return [Word(self._wrapper, self, lemma) for lemma in self.lemmas()]

    def senses(self) -> List['Sense']:
        """Return the individual word senses that make up this synset."""
        if _backend_name(self._wrapper) == 'nltk':
            # NLTK has no distinct sense object; a Lemma (word+synset pair)
            # already is the sense-equivalent.
            raw_senses = self._raw.lemmas()
        else:
            raw_senses = self._raw.senses()
        return [Sense(self._wrapper, raw_sense, self) for raw_sense in raw_senses]

    def _relation(self, name: str) -> List['Synset']:
        getter = getattr(self._wrapper, f'get{name.capitalize()}s')
        related_words = getter([self._raw])
        return [self._resolve(word) for word in related_words]

    def _resolve(self, word) -> 'Synset':
        """Turn a legacy Word DTO (as returned by the wrapper relation
        methods) back into a Synset by resolving its raw synset object."""
        key = self._wrapper.getWordKey(word.wordKey)
        raw = self._wrapper.getWordKeySynset(key, word.lang)
        return Synset(self._wrapper, raw)

    def hypernyms(self) -> List['Synset']:
        """Return more general synsets that this synset is a kind of.

        Example:

            >>> [s.lemmas()[0] for s in Wordnet().synsets("vehicle", pos="n")[0].hypernyms()]
            ['transport']
        """
        return self._relation('hypernym')

    def hyponyms(self) -> List['Synset']:
        """Return more specific synsets that are a kind of this synset."""
        return self._relation('hyponym')

    def holonyms(self) -> List['Synset']:
        """Return synsets that this synset is a part or member of."""
        return self._relation('holonym')

    def meronyms(self) -> List['Synset']:
        """Return synsets that are parts or members of this synset."""
        return self._relation('meronym')

    def antonyms(self) -> List['Synset']:
        """Return synsets with the opposite meaning of this synset.

        Example:

            >>> [s.lemmas()[0] for s in Wordnet().synsets("hot", pos="a")[0].antonyms()]
            ['cold']
        """
        return self._relation('antonym')

    def entailments(self) -> List['Synset']:
        """Return verb synsets entailed by this (verb) synset.

        Example:

            >>> [s.lemmas()[0] for s in Wordnet().synsets("snore", pos="v")[0].entailments()]
            ['sleep']
        """
        return self._relation('entailment')

    def relations(self, *names: str) -> Dict[str, List['Synset']]:
        """Return a mapping of relation name to related synsets.

        Without arguments, returns every supported relation
        (``antonym``, ``hypernym``, ``hyponym``, ``holonym``, ``meronym``,
        ``entailment``). With one or more relation names, restricts the
        result to those relations.
        """
        selected = names or _RELATION_METHODS
        unknown = set(selected) - set(_RELATION_METHODS)
        if unknown:
            raise ValueError(f'Unknown relation(s): {", ".join(sorted(unknown))}')
        return {name: self._relation(name) for name in selected}

    @_wrap_language_errors
    def translate(
        self, lang: Union[str, Sequence[str], None] = None
    ) -> List['Synset']:
        """Return the synsets in other languages that share this synset's
        Interlingual Index (ILI), i.e. the same concept expressed in
        other languages.

        Arguments:
            lang: restrict results to one or more languages, given the same
                way as to :class:`Wordnet` — a single code (``'de'``), a
                space- or comma-separated string (``'de fr'``), or a list of
                codes. If omitted, returns translations in every language
                configured on the owning :class:`Wordnet`.

        Each language yields at most one synset, since the ILI identifies one
        concept per lexicon, so a single-language request returns a list of
        one. Languages with no counterpart are omitted rather than yielding a
        placeholder, and the list is empty on a backend without an ILI.

        The result includes this synset itself, under its own language: the
        operation resolves an ILI across lexicons, and the source lexicon is
        one of them. This follows :mod:`wn`, whose ``translate()`` behaves the
        same way. Filter on :attr:`lang` to exclude it::

            others = [s for s in synset.translate() if s.lang != synset.lang]

        Example:

            >>> synset = Wordnet(backend="omw").synsets("happy", pos="a")[0]
            >>> [s.lemmas()[0] for s in synset.translate(lang="it")]
            ['felice']
            >>> sorted(s.lang for s in synset.translate(lang="de fr"))
            ['de', 'fr']
        """
        if not self.ili:
            return []

        normalized = _normalize_lang(lang)
        if normalized is None:
            # Default to the languages the owning Wordnet was configured with,
            # as descriptions() does. Passing None to the backend would instead
            # return every installed lexicon, ignoring that configuration.
            normalized = ','.join(self._wrapper.filterLang)

        results = []
        for code in normalized.split(','):
            resolved = self._wrapper.getWordnetLanguageCode(code)
            results.extend(
                Synset(self._wrapper, raw)
                for raw in self._wrapper.getSynsetsFromIli(self.ili, resolved)
            )
        return results

    @_wrap_language_errors
    def descriptions(
        self, lang: Union[str, Sequence[str], None] = None
    ) -> Dict[str, List[str]]:
        """Return this synset's word forms in each language, keyed by language
        code.

        Where :meth:`lemmas` gives the forms in the synset's own language,
        this resolves the synset across languages through its Interlingual
        Index and collects each one's forms.

        Arguments:
            lang: restrict the result to one or more languages, given the same
                way as to :class:`Wordnet` — a single code (``'de'``), a
                space- or comma-separated string (``'de fr'``), or a list of
                codes. If omitted, returns every language the owning
                :class:`Wordnet` was configured with.

        The synset's own language is included when it falls within the
        requested set, and its entry equals :meth:`lemmas`.

        Example:

            >>> synset = Wordnet(lang="de fr").synsets("house", pos="n")[0]
            >>> synset.descriptions(lang="de")
            {'de': ['Behausung', 'Bude', 'Haus', 'Heim', 'Hütte']}
        """
        generic = self._wrapper.getGenericLanguageDescriptions(self._raw)
        if lang is None:
            # Default to the languages the owning Wordnet was configured
            # with (wrapper.filterLang), not every language wn/NLTK know
            # about — matching this method's documented default.
            requested_codes = list(self._wrapper.filterLang)
        elif isinstance(lang, str):
            requested_codes = _normalize_lang(lang).split(',')
        else:
            requested_codes = list(lang)

        own_language = self.lang

        result = {}
        for code in requested_codes:
            description = generic.getWordDescription(code)
            # Canonicalize through the same langMap getWordDescription used,
            # so e.g. 'deu' and 'de' land under the same result key.
            resolved_code = code if code in generic.descriptionLookup else generic.langMap.get(code, code)
            if resolved_code == own_language:
                # The underlying wrapper omits the synset's own language,
                # since the legacy interface treated these as translations.
                # Supply it from the synset itself so that this method covers
                # every requested language, as definitions() does.
                result[resolved_code] = self.lemmas()
            else:
                result[resolved_code] = (
                    [w.strip() for w in description.split(',')] if description else []
                )
        return result

    def relation_counts(self) -> RelationCounts:
        """Return how many related synsets exist for each relation type.

        Example:

            >>> Wordnet(lang="de").synsets("vehicle", pos="n")[0].relation_counts().hyponym
            9
        """
        counter = self._wrapper.getLinguisticCounter(self._raw)
        return RelationCounts(
            antonym=counter.antonym,
            hypernym=counter.hypernym,
            hyponym=counter.hyponym,
            holonym=counter.holonym,
            meronym=counter.meronym,
            entailment=counter.entailment,
            mt=counter.mt,
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, Synset) and self.id == other.id and self.backend == other.backend

    def __hash__(self) -> int:
        return hash((self.backend, self.id))

    def __repr__(self) -> str:
        return f'Synset({self.id!r})'


class Sense:
    """A single word sense: the pairing of one word with one synset.

    Sense objects are not constructed directly; obtain them from
    :meth:`Synset.senses`, :meth:`Word.senses`, or :meth:`Wordnet.senses`.
    """

    __slots__ = ('_wrapper', '_raw', '_synset')

    def __init__(self, wrapper: WordNetWrapper, raw_sense, synset: Optional[Synset] = None):
        self._wrapper = wrapper
        self._raw = raw_sense
        self._synset = synset

    @property
    def backend(self) -> str:
        """Which backend this sense came from: ``'omw'`` or ``'nltk'``."""
        return _backend_name(self._wrapper)

    def word(self) -> 'Word':
        """Return the word this sense belongs to."""
        if _backend_name(self._wrapper) == 'nltk':
            return Word(self._wrapper, self.synset(), self._raw.name().replace('_', ' '))
        raw_word = self._raw.word()
        return Word(self._wrapper, self.synset(), str(raw_word.lemma()).replace('_', ' '))

    def synset(self) -> Synset:
        """Return the synset this sense belongs to."""
        if self._synset is not None:
            return self._synset
        raw_synset = self._raw.synset()
        return Synset(self._wrapper, raw_synset)

    def examples(self) -> List[str]:
        """Return example sentences specific to this sense, if any."""
        if _backend_name(self._wrapper) == 'nltk':
            return []
        return [ex.replace('"', '') for ex in self._raw.examples()]

    @_wrap_language_errors
    def translate(
        self, lang: Union[str, Sequence[str], None] = None
    ) -> List['Sense']:
        """Return corresponding senses in another language, via the
        parent synset's Interlingual Index."""
        return [
            sense
            for translated_synset in self.synset().translate(lang=lang)
            for sense in translated_synset.senses()
        ]

    def __repr__(self) -> str:
        return f'Sense({self.word().lemma()!r}, {self.synset().id!r})'


class Word:
    """A word (lexical entry), independent of any particular sense.

    Word objects are not constructed directly; obtain them from
    :meth:`Wordnet.words`, :meth:`Synset.words`, or :meth:`Sense.word`.
    """

    __slots__ = ('_wrapper', '_synset', '_lemma', 'source')

    def __init__(
        self,
        wrapper: WordNetWrapper,
        synset: Synset,
        lemma: str,
        source: str = 'wordnet',
    ):
        self._wrapper = wrapper
        self._synset = synset
        self._lemma = lemma
        #: Which *retrieval step* produced this result: ``'wordnet'`` (direct
        #: lexical match), ``'lemmatized'`` (matched only after lemmatising the
        #: query form), or ``'machine_translation'`` (no wordnet entry was
        #: found; produced by a configured
        #: :class:`~passivlingo_dictionary.translationProviders.TranslationProvider.TranslationProvider`).
        #:
        #: .. note::
        #:
        #:    This records *how the query was satisfied*, not how the
        #:    underlying lexical data was **constructed**. A lemma returned
        #:    with ``source == 'wordnet'`` may itself have been hand-curated
        #:    or automatically generated, depending on the lexicon; wordnet
        #:    lexicons do not generally expose per-entry construction
        #:    metadata, so the library cannot report it. See the
        #:    "Provenance" section of the documentation.
        self.source = source

    @property
    def backend(self) -> str:
        """Which backend this word came from: ``'omw'`` or ``'nltk'``."""
        return _backend_name(self._wrapper)

    @property
    def lang(self) -> str:
        """The BCP-47-style language code of this word."""
        return self._synset.lang

    @property
    def pos(self) -> str:
        """The single-letter part-of-speech code."""
        return self._synset.pos

    def lemma(self) -> str:
        """Return the canonical form of this word.

        Example:

            >>> Wordnet().words("house", pos="n")[0].lemma()
            'house'
        """
        return self._lemma

    def forms(self) -> List[str]:
        """Return alternate forms (synonyms within the synset) of this word."""
        return self._wrapper.getSynonyms(self._synset._raw, self._lemma)

    def synsets(self) -> List[Synset]:
        """Return the synset(s) this word belongs to."""
        return [self._synset]

    def senses(self) -> List[Sense]:
        """Return the senses of this word."""
        return [s for s in self._synset.senses() if s.word().lemma() == self._lemma]

    @_wrap_language_errors
    def translate(
        self, lang: Union[str, Sequence[str], None] = None
    ) -> Dict[Sense, List['Word']]:
        """Return a mapping of this word's senses to translated words.

        Example:

            >>> w = Wordnet(backend="omw").words("happy", pos="a")[0]
            >>> {s: [tw.lemma() for tw in ws] for s, ws in w.translate(lang="it").items()}
            {Sense('happy', 'happy.a.01151786.ewn'): ['felice']}
        """
        result = {}
        for sense in self.senses():
            translated_senses = sense.translate(lang=lang)
            result[sense] = [ts.word() for ts in translated_senses]
        return result

    def __repr__(self) -> str:
        return f'Word({self._lemma!r})'


class Wordnet:
    """The entry point for querying a WordNet backend.

    A ``Wordnet`` object selects a backend and, optionally, a set of
    languages once; every query method (`words`, `synsets`, `senses`)
    then searches only within that selection.

    Arguments:
        backend: which WordNet data to query: ``'omw'`` (the default; Open
            Multilingual WordNet-family data via the :mod:`wn` package) or
            ``'nltk'`` (NLTK's WordNet corpus).
        lang: one or more BCP-47-style language codes that queries resolve
            translations and glosses against: a single code (``'de'``), a
            space- or comma-separated string of codes (``'de fr es'`` or
            ``'de,fr,es'``), or a list of codes. If omitted, a default set
            of major European languages is used.
        translator: an optional
            :class:`~passivlingo_dictionary.translationProviders.TranslationProvider.TranslationProvider`
            used as a machine-translation fallback when a query word has no
            match in the wordnet data.
        lemmatizer: an optional callable ``(word) -> list[str]`` used
            instead of the default spaCy-backed lemmatizer for the
            lemmatization fallback.

    Example:

        >>> wordnet = Wordnet(backend="omw", lang="de fr es it nl pt")
        >>> len(wordnet.words("house")) > 0
        True
    """

    __slots__ = ('_backend', '_wrapper', '_translator', '_lemmatizer', '_requested_langs')

    def __init__(
        self,
        backend: str = 'omw',
        *,
        lang: Union[str, Sequence[str], None] = None,
        translator: Optional[TranslationProvider] = None,
        lemmatizer: Optional[LemmatizeFunction] = None,
    ):
        self._backend = backend
        normalized_lang = _normalize_lang(lang)
        try:
            self._wrapper = _make_wrapper(backend, normalized_lang)
        except ValueError as exc:
            raise LanguageError(str(exc)) from exc
        self._translator = translator
        self._lemmatizer = lemmatizer
        # wrapper.filterLang is deduplicated via set() and always includes
        # 'en', so it does not preserve the caller's requested order/values;
        # keep the original request around for anything (like the MT
        # fallback) that needs "the first language the caller asked for".
        self._requested_langs = normalized_lang.split(',') if normalized_lang else []

    @property
    def backend(self) -> str:
        """Which backend this Wordnet queries: ``'omw'`` or ``'nltk'``."""
        return _backend_name(self._wrapper)

    def _lemmatize(self, form: str, lang: Optional[str]) -> List[str]:
        if self._lemmatizer is not None:
            return self._lemmatizer(form)
        resolved_lang = lang or 'en'
        return FactoryMethods.getLemmatizer(resolved_lang).lemmatize(form)

    def _machine_translate(self, form: str, lang: Optional[str]) -> Optional[Word]:
        if self._translator is None:
            return None
        target_lang = lang or (self._requested_langs[0] if self._requested_langs else 'en')
        translation = self._translator.translate(None, target_lang, form)
        if not translation:
            return None
        placeholder_synset = Synset(self._wrapper, None)
        return Word(self._wrapper, placeholder_synset, translation, source='machine_translation')

    @_wrap_language_errors
    def synsets(
        self,
        form: str,
        *,
        pos: Optional[str] = None,
        lang: Optional[str] = None,
    ) -> List[Synset]:
        """Return the list of matching synsets.

        A *form* argument is required. A *pos* argument restricts synsets
        to the given single-letter part of speech. If nothing matches
        directly, *form* is lemmatized and the lemmatized forms are
        searched instead.

        Example:

            >>> Wordnet(lang="de").synsets("house", pos="n")[0].lemmas()[0]
            'house'
        """
        return self._synsets_with_source(form, pos=pos, lang=lang)[0]

    def _synsets_with_source(
        self, form: str, *, pos: Optional[str], lang: Optional[str],
    ) -> 'tuple[List[Synset], str]':
        """Like synsets(), but also reports whether the direct match or the
        lemmatization fallback produced the result, so words() can tag its
        Word.source accordingly."""
        # An empty or whitespace-only query matches nothing. Guard here rather
        # than passing it down: the underlying backends treat an empty form as
        # an unfiltered query and return an arbitrary synset.
        if form is None or not str(form).strip():
            return [], 'wordnet'

        # translatePos(), unlike translate(), requires an explicit language
        # rather than searching across every configured filter language, so
        # POS-filtered queries default to English, matching how the legacy
        # search chains are always invoked with an explicit `lang`.
        pos_lang = lang or 'en'

        raw_synsets = (
            self._wrapper.translatePos(form, pos, pos_lang)
            if pos
            else self._wrapper.translate(form, lang)
        )
        if raw_synsets:
            return [Synset(self._wrapper, raw) for raw in raw_synsets], 'wordnet'

        for lemma in self._lemmatize(form, lang):
            raw_synsets = (
                self._wrapper.translatePos(lemma, pos, pos_lang)
                if pos
                else self._wrapper.translate(lemma, lang)
            )
            if raw_synsets:
                return [Synset(self._wrapper, raw) for raw in raw_synsets], 'lemmatized'

        return [], 'wordnet'

    @_wrap_language_errors
    def words(
        self,
        form: str,
        *,
        pos: Optional[str] = None,
        lang: Optional[str] = None,
    ) -> List[Word]:
        """Return the list of matching words.

        Falls back to lemmatization, then to the configured *translator*
        (see :meth:`Wordnet.__init__`), if *form* has no direct wordnet
        match. Check :attr:`Word.source` to see how a given result was
        produced.

        Example:

            >>> Wordnet().words("houses")[0].lemma()
            'house'
        """
        synsets, source = self._synsets_with_source(form, pos=pos, lang=lang)
        if synsets:
            words = [
                word
                for synset in synsets
                for word in synset.words()
                if pos is None or word.pos == pos
            ]
            for word in words:
                word.source = source
            return words

        translated = self._machine_translate(form, lang)
        return [translated] if translated else []

    @_wrap_language_errors
    def senses(
        self,
        form: str,
        *,
        pos: Optional[str] = None,
        lang: Optional[str] = None,
    ) -> List[Sense]:
        """Return the list of matching senses.

        See :meth:`Wordnet.synsets` for the matching and fallback rules.
        """
        return [
            sense
            for synset in self.synsets(form, pos=pos, lang=lang)
            for sense in synset.senses()
        ]

    def word(self, id: str) -> Word:
        """Return the word for a given synset id, by its first lemma.

        Raises:
            BackendError: if no synset with this id exists.
        """
        return self.synset(id).words()[0]

    def synset(self, id: str) -> Synset:
        """Return the synset with the given id.

        Raises:
            BackendError: if no synset with this id exists.

        Example:

            >>> Wordnet(lang="de").synset("house.n.03549540.ewn").definition()
            'a dwelling that serves as living quarters for one or more families'
        """
        if not id or not str(id).strip():
            raise BackendError('no such synset: empty identifier')
        try:
            key = self._wrapper.getWordKey(id)
            # A malformed identifier can reduce to an empty backend key, which
            # the backends treat as an unfiltered query and answer with an
            # arbitrary synset rather than an error.
            if not str(key).strip():
                raise BackendError(f'no such synset: {id}')
            raw = self._wrapper.getWordKeySynset(key, None)
            return Synset(self._wrapper, raw)
        except BackendError:
            raise
        except Exception as exc:
            raise BackendError(f'no such synset: {id}') from exc

    def __repr__(self) -> str:
        return f'Wordnet(backend={self.backend!r})'
