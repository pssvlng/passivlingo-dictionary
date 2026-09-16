# passivlingo-dictionary

Unified multilingual WordNet access in Python, across two backends.

`passivlingo-dictionary` provides a single object model over the
[`wn`](https://wn.readthedocs.io) library (Open Multilingual Wordnet-family
data) and NLTK's WordNet corpus reader. It adds cross-lingual lookup via the
Interlingual Index, multilingual lexicalisation retrieval in one call, and
retrieval-step provenance on every result.

```python
import passivlingo_dictionary as pld

synset = pld.synsets("house", pos="n")[0]
synset.definition()
# 'a dwelling that serves as living quarters for one or more families'

[s.lemmas()[0] for s in synset.hypernyms()]
# ['home', 'edifice']
```

## Why

The two dominant Python wordnet libraries expose incompatible object models
for the same operations — part of speech is an attribute in one and a method
in the other, lemmas are strings in one and objects in the other, and the
Interlingual Index is central to one and absent from the other. Code written
against either is not portable to the other.

This library adopts `wn`'s object model as the common abstraction and makes
NLTK's data available through it, so the same code runs against either
backend:

```python
def describe(backend):
    synset = pld.Wordnet(backend=backend).synsets("vehicle", pos="n")[0]
    return synset.id, synset.pos, [h.lemmas()[0] for h in synset.hypernyms()]

describe("omw")   # ('vehicle.n.04531608.ewn', 'n', ['transport'])
describe("nltk")  # ('vehicle.n.01',           'n', ['conveyance'])
```

## Cross-lingual queries

Configure the languages once, then resolve concepts across them:

```python
wordnet = pld.Wordnet(lang="de fr es it nl pt")
happy = wordnet.synsets("happy", pos="a")[0]

[s.lemmas()[0] for s in happy.translate(lang="it")]
# ['felice']

happy.descriptions()
# {'de': ['glücklich'], 'fr': ['heureux'], 'it': ['felice'], ...}
```

Cross-lingual operations require the `omw` backend and the target language's
lexicon to be installed. They return empty results on the `nltk` backend,
which has no Interlingual Index.

## Provenance

Queries fall back from direct lexical match, to lemmatisation, to machine
translation (only if a translator is configured). Every result records which
step produced it:

```python
wordnet.words("house")[0].source    # 'wordnet'
wordnet.words("houses")[0].source   # 'lemmatized'
```

This records *how the query was satisfied*, not how the underlying lexical
data was constructed — see the documentation for that distinction.

## Installation

```bash
pip install passivlingo-dictionary
```

Optional extras:

```bash
pip install "passivlingo-dictionary[translate]"  # TextBlob translation provider
pip install "passivlingo-dictionary[audio]"      # TTS / audio helpers
```

Wordnet data is downloaded separately via the `wn` package:

```python
import wn
wn.download("ewn:2020")   # English WordNet — required
```

See the documentation for the full setup guide, including optional spaCy
models for lemmatisation and NLTK corpora for the `nltk` backend.

## Documentation

Full guides and API reference are built with Sphinx from the `documentation/`
directory.

## Legacy interface

The earlier `Dictionary` / `SearchParam` interface remains available and
unchanged at its existing import paths. New code should prefer `Wordnet`.

## Licence

GPL-3.0.
