# Proposed public API redesign

This is a concrete proposal for a new public interface, modeled on the
object shape of [`wn`](https://wn.readthedocs.io) (the de facto standard
Python WordNet library) but built around what this library actually adds on
top of `wn`: a unified view across two backends (OMW/`wn` and NLTK), relation
extraction as first-class methods, ILI-based cross-lingual lookup as a single
`.translate()` call instead of a second search round-trip, and machine
translation as an automatic fallback rather than a separate code path the
caller has to know to invoke.

Nothing here is implemented yet — this is the shape to agree on before any
code changes, because the docs, the paper, and the test suite all follow
from it.

## Why change the shape, not just the names

Renaming `findWords` to `find_words` and calling it done would keep every
structural problem the current design has:

- `SearchParam` is a mutable bag of ~10 optional fields where validity
  depends on *which combination* is set, discovered only at call time via
  string-keyed `ValueError`s. A reader can't tell from the type what a valid
  call looks like.
- Category traversal (hypernym, antonym, ...) requires two round-trips
  through the same method — search once to get a `wordKey`, mutate/reset the
  same `SearchParam`, search again with `category` set. `wn.Synset` just
  exposes `.hypernyms()` as a method.
- Cross-lingual (ILI) lookup is the same two-step dance, when `wn.Synset`
  and `wn.Word` expose it as `.translate(lang=...)` directly on the object
  you already have.
- "Which backend, which languages" is threaded through every call via
  `wordnetId`/`filterLang` strings instead of being configured once on an
  entry-point object, which is what `wn.Wordnet(lexicon=..., lang=...)`
  does.

The redesign below fixes all four by returning real objects with relation
methods, and by making a `Wordnet`-like object hold the backend/language
configuration once.

## Top-level shape

```python
import passivlingo_dictionary as pld

# Configure once: which backend(s), which language(s) to resolve
# translations/descriptions against. Mirrors wn.Wordnet(lexicon=..., lang=...).
wordnet = pld.Wordnet(backend="omw", lang="de fr es it nl pt")

# Word lookup — returns real Word objects, not a flat, backend-tagged DTO.
words = wordnet.words("house")                  # List[Word]
words = wordnet.words("house", pos="n")          # filtered by POS

# Synset lookup — most relation/translation methods live here, matching wn.
synsets = wordnet.synsets("house", pos="n")      # List[Synset]

# Relations are methods on the Synset, not a separate category search.
synsets[0].hypernyms()                           # List[Synset]
synsets[0].hyponyms()
synsets[0].antonyms()
synsets[0].holonyms()
synsets[0].meronyms()
synsets[0].entailments()

# Cross-lingual lookup is .translate(), not a second SearchParam round-trip.
synsets[0].translate(lang="it")                  # List[Synset], via ILI

# Multilingual glosses across configured languages, without a second call.
synsets[0].descriptions()                        # Dict[str, List[str]]
synsets[0].descriptions(lang=["de", "fr"])       # subset

# Falls back to lemmatization, then machine translation, automatically —
# no separate "MtSearchChain" the caller has to know to reach for.
wordnet.words("houses")                          # lemmatized to 'house'
wordnet.words("Kühlschrank", lang="de")          # MT fallback if not in wordnet
```

`import passivlingo_dictionary as pld` then `pld.words(...)` /
`pld.synsets(...)` module-level convenience functions should also exist,
exactly mirroring `wn.words()` / `wn.synsets()`, for the common case of "one
backend, no persistent config" — this is what most of `wn`'s own
Quick Start and examples use, and it's the one-liner a paper's code listing
wants.

## Object model

### `Wordnet`

The configured entry point. Replaces `Dictionary` + implicitly threading
`wordnetId`/`filterLang` through every call.

```python
class Wordnet:
    def __init__(
        self,
        backend: Literal["omw", "nltk"] = "omw",
        *,
        lang: str | Sequence[str] | None = None,
        translator: TranslationProvider | None = None,
        lemmatizer: Callable[[str, str], list[str]] | None = None,
    ) -> None: ...

    def words(self, form: str, *, pos: str | None = None, lang: str | None = None) -> list[Word]: ...
    def synsets(self, form: str, *, pos: str | None = None, lang: str | None = None) -> list[Synset]: ...
    def senses(self, form: str, *, pos: str | None = None, lang: str | None = None) -> list[Sense]: ...

    def synset(self, id: str) -> Synset:
        """Look up a single synset by its opaque id (was `wordkey`)."""

    def word(self, id: str) -> Word: ...
```

- `backend` replaces the `wordnetId` string ('own'/'nltk'), with an honest
  name (`'omw'`) instead of the internal codename `'own'`.
- `lang` accepts a single BCP-47-ish code or a sequence, replacing the
  comma-joined `filterLang` string — still easy to pass `"de fr es"` for CLI
  parity with `wn`, but a `list[str]` is also accepted and preferred.
  `lang=None` mirrors `wn.Wordnet(lang=None)`: no restriction.
  Non-fatal, unresolvable individual codes should log a warning (mirroring
  `wn.WnWarning`) rather than raising deep inside a wrapper constructor,
  which is a real bug in the current `filterLang` handling (see the
  "current behavior to preserve, not copy" note below).
- `translator` replaces the ad hoc `googleApiKey` field on `SearchParam` —
  pass a configured `TranslationProvider` instance (already exists as a
  concept in the code; just needs promoting to a constructor argument
  instead of a string threaded through `SearchChainFactory`).
- Backend and language selection happen once, at construction, not per call.

### `Word`, `Sense`, `Synset` — thin, real objects

```python
class Word:
    id: str                 # backend-qualified id, e.g. 'ewn-house-n' or 'nltk-house.n.01'
    pos: str                # single-letter POS code: n, v, a, r, ...
    lang: str
    backend: Literal["omw", "nltk"]

    def lemma(self) -> str: ...
    def forms(self) -> list[str]: ...          # synonyms/alternate forms
    def senses(self) -> list[Sense]: ...
    def synsets(self) -> list[Synset]: ...
    def translate(self, lang: str) -> dict[Sense, list[Word]]: ...

class Synset:
    id: str                 # was `wordKey`
    ili: str | None
    pos: str
    lang: str
    backend: Literal["omw", "nltk"]

    def definition(self) -> str | None: ...
    def examples(self) -> list[str]: ...
    def lemmas(self) -> list[str]: ...          # was `synonyms` + the primary name
    def words(self) -> list[Word]: ...
    def senses(self) -> list[Sense]: ...

    # Relations — replace the `category` string + CategorySearchChain dance.
    def hypernyms(self) -> list[Synset]: ...
    def hyponyms(self) -> list[Synset]: ...
    def holonyms(self) -> list[Synset]: ...
    def meronyms(self) -> list[Synset]: ...
    def antonyms(self) -> list[Synset]: ...
    def entailments(self) -> list[Synset]: ...
    def relations(self, *names: str) -> dict[str, list[Synset]]: ...  # generic, mirrors wn

    # Cross-lingual — replaces the ili+lang SearchParam round-trip.
    def translate(self, lang: str | None = None) -> list[Synset]: ...

    # This library's actual value-add over wn: glosses across every
    # configured language in one call, not one SearchParam per language.
    def descriptions(self, lang: str | Sequence[str] | None = None) -> dict[str, list[str]]: ...

    # Diagnostic counts, was `LinguisticCounter` — keep, but as a method
    # returning a small dataclass, not a mutable object built up via .add().
    def relation_counts(self) -> RelationCounts: ...

class Sense:
    id: str
    def word(self) -> Word: ...
    def synset(self) -> Synset: ...
    def examples(self) -> list[str]: ...
    def translate(self, lang: str | None = None) -> list[Sense]: ...
```

Notes on naming choices, since these are exactly the kind of thing a paper
reviewer or a `wn` user switching over will notice immediately:

- `wordKey` → `id`. Matches `wn.Synset.id` / `wn.Word.id` exactly. The
  current `wordKey` format concatenation (`'.'.join([lemma, offset, pos,
  lexicon])` for OMW, bare `synset.name()` for NLTK) can stay as the
  underlying string — only the attribute name changes.
- `synonyms` → `lemmas()` (method, not attribute — matches `wn.Synset.lemmas()`
  exactly, and being a method rather than a stored attribute means it isn't
  silently stale if the synset is re-fetched).
- `category` (a string like `'hypernym'` passed back into `findWords`) is
  gone entirely — each relation is its own method. `relations(*names)`
  remains as an escape hatch for programmatic/dynamic access, matching
  `wn.Synset.relations()`.
- `pos` values move from human-readable strings (`'Noun'`, `'Adjective'`) to
  the single-letter WordNet convention (`'n'`, `'a'`) that `wn` and NLTK
  both already use internally — `'Noun'` was a display-string leaking into
  the data model. A `Synset.pos_name` convenience property can supply the
  human-readable form for UI code that wants it, without making it the
  primary representation.
- `RelationCounts` replaces `LinguisticCounter`: an immutable
  `@dataclass(frozen=True)` with the same fields, computed fresh by
  `relation_counts()` rather than mutated in place via `.add()`. This is a
  case where the *behavior* (the counts themselves) is unchanged but the
  *shape* (immutable value object vs. mutable accumulator) is fixed, per the
  "don't change outcomes" instinct from the last pass — the outcome (the
  numbers) is identical, only how you obtain and hold them changes.

### `LanguageDescriptions` / `GenericLanguageDescriptions` → `descriptions()`

These two classes (one hardcoded to 7 EU languages with silent no-ops on
unknown codes, one dynamic with `ValueError` on unknown codes — a real,
previously-flagged inconsistency) collapse into a single
`Synset.descriptions(lang=...)` returning a plain `dict[str, list[str]]`.
This is a strict simplification: no separate class, no two divergent
error-handling behaviors, no fixed language list to maintain. Unknown
requested language codes should behave one way, consistently — the
`ValueError`-raising behavior is the right one to keep as the sole
behavior, since it fails loudly at the call site instead of silently
returning `''` deep in a hard-coded 7-language special case.

### Exceptions

Mirror `wn`'s `wn.Error` / `wn.DatabaseError` hierarchy instead of raising
bare `ValueError` for every failure mode:

```python
class Error(Exception): ...
class BackendError(Error): ...          # wraps underlying wn.Error / nltk errors
class LanguageError(Error): ...         # unresolvable/unsupported language code
class InvalidQueryError(Error): ...     # replaces today's ValueError('Invalid argument list...')
```

This is what lets a `except pld.Error` catch-all work for library users, the
way `except wn.Error` does today — currently our only failure signal is a
generic `ValueError`, indistinguishable from a Python built-in error.

## Machine-translation fallback: automatic, not a separate mode

Today, getting a machine-translated result requires the caller to know that
plain wordnet lookup failed and to understand `MtSearchChain`/
`ContainerSearchChain`'s fallthrough order. In the new design this is purely
an implementation detail of `Wordnet.words()`/`.synsets()`: if nothing
matches in the configured backend, the same call transparently falls back to
lemmatization, then to the configured `TranslationProvider` if one was
given at construction. The returned `Word`/`Synset` gets a
`Word.source: Literal["wordnet", "lemmatized", "machine_translation"]`
field so callers can tell how a result was produced without needing a
different method or a `pos == 'Machine Translation'` string sentinel (today's
actual mechanism, which overloads the POS field to signal a completely
different thing).

## Module-level convenience functions

```python
# passivlingo_dictionary/__init__.py
def words(form: str, *, pos: str | None = None, lang: str | None = None, backend: str = "omw") -> list[Word]: ...
def synsets(form: str, *, pos: str | None = None, lang: str | None = None, backend: str = "omw") -> list[Synset]: ...
def senses(form: str, *, pos: str | None = None, lang: str | None = None, backend: str = "omw") -> list[Sense]: ...
```

These construct a throwaway `Wordnet()` under the hood, exactly mirroring
how `wn.synsets()` is documented as "creates a `Wordnet` object ... and
passes the remaining arguments to `Wordnet.synsets()`" (confirmed from `wn`'s
own docstring). This is the one-liner used in the paper's code examples and
in the docs' Quick Start.

## `__all__` and module layout

```python
__all__ = (
    "__version__",
    "Wordnet", "Word", "Sense", "Synset", "RelationCounts",
    "words", "senses", "synsets",
    "TranslationProvider",
    "Error", "BackendError", "LanguageError", "InvalidQueryError",
)
```

Internal implementation modules (today's `helpers/SearchChainFactory.py`,
`searchChains/*`, `extractors/*`, `wrappers/*`) become underscore-prefixed
or nested under a private subpackage, matching `wn`'s `_core.py`/
`_queries.py` convention — so Sphinx autodoc and IDE autocomplete only
surface the intended public surface, and internal refactors don't count as
breaking changes.

## What stays, functionally unchanged

This is a reshaping of the interface, not a rewrite of the underlying
matching logic:

- Two-backend support (OMW-based `wn` package + NLTK WordNet) stays exactly
  as-is underneath `Wordnet(backend=...)`.
- The relation extraction logic in today's `wrappers/OwnWordNetWrapper.py` /
  `NltkWordNetWrapper.py` and the `extractors/*` classes is the actual
  correct implementation and is preserved; only its call surface changes
  (method on `Synset` instead of `Extractor` class + `CategorySearchChain`).
- ILI-based cross-lingual resolution logic is preserved; only surfaced as
  `.translate()` instead of a second `SearchParam` round trip.
- Lemmatization (spaCy-backed) and machine-translation fallback
  (Google/MyMemory/TextBlob providers) are preserved as pluggable strategies
  behind `Wordnet(lemmatizer=..., translator=...)`.

## Migration path for existing internal callers

Since `Dictionary`/`SearchParam` may already be used elsewhere (the
Passivlingo app itself), propose keeping `passivlingo_dictionary.legacy`
as a thin compatibility shim re-exporting today's `Dictionary`/`SearchParam`
unchanged, deprecated via `DeprecationWarning`, for one major version — this
is the same strategy `wn` itself uses for NLTK migrators
(`guides/nltk-migration.html`) and gives internal call sites a real deadline
without a flag day.

## Next steps once this shape is agreed

1. Implement `Word`/`Sense`/`Synset`/`Wordnet` as thin wrappers over the
   *existing* `wrappers/OwnWordNetWrapper.py` / `NltkWordNetWrapper.py` and
   `extractors/*` logic — no changes to matching behavior, only to what
   surrounds it.
2. Add full type hints + Sphinx-style docstrings with doctest examples on
   every public method (this is what autodoc will render verbatim).
3. Add `pyproject.toml`, split extras (`[spacy]`, `[translate]`, `[audio]`),
   add `__all__`.
4. Stand up Sphinx + `sphinx-rtd-theme` + Read the Docs, structured exactly
   like `wn`'s: Setup / CLI / FAQ, then Guides (Basic Usage, Cross-lingual
   Queries, Category Traversal, Machine-Translation Fallback, Migrating from
   `wn`), then autodoc-generated API Reference.
