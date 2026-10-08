"""Reproduce every quantitative claim in the paper.

Run:  python3 reproduce_measurements.py [path/to/passivlingo-dictionary]

The paper is maintained separately from the library source, so the location of
the checkout is configurable: pass it as the first argument, set the PLD_REPO
environment variable, or rely on the default search below.

Requires the environment described in paper.md §4 (Python 3.10, wn 0.9.4,
NLTK 3.8.1, spaCy 3.7.2) with the hybrid lexicons installed.

Outputs, in order: Table 1 (API divergence between wn and NLTK); Figure 1
(backend unification); the relationship to wn's own API (§1.1, §2.3); the
lexicon inventory reported in footnote 1; the §5
construction-provenance metadata audit; and the §4 software measurements.
"""
import os
import subprocess
import sys
from pathlib import Path


def _resolve_repo() -> Path:
    """Locate the passivlingo-dictionary checkout."""
    candidates = []
    if len(sys.argv) > 1:
        candidates.append(Path(sys.argv[1]).expanduser())
    if os.environ.get('PLD_REPO'):
        candidates.append(Path(os.environ['PLD_REPO']).expanduser())
    candidates.append(Path(__file__).resolve().parent.parent)
    candidates.append(Path.home() / 'Source' / 'Passivlingo' / 'passivlingo-dictionary')

    for candidate in candidates:
        if (candidate / 'passivlingo_dictionary' / 'core.py').exists():
            return candidate.resolve()

    raise SystemExit(
        'Could not locate the passivlingo-dictionary checkout. Pass its path '
        'as the first argument, or set the PLD_REPO environment variable.'
    )


REPO = _resolve_repo()


def rule(title):
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")


def table1_api_divergence():
    rule("TABLE 1 - API divergence between wn and NLTK")
    import wn
    from nltk.corpus import wordnet as nwn

    s_wn = wn.synsets("vehicle", lexicon="ewn", pos="n")[0]
    s_nl = nwn.synsets("vehicle", pos="n")[0]

    print(f"  pos        wn: .pos={s_wn.pos!r} (attribute)")
    print(f"             nltk: .pos()={s_nl.pos()!r} (METHOD - attribute access "
          f"returns {type(getattr(s_nl, 'pos')).__name__})")
    print(f"  lemmas     wn: {type(s_wn.lemmas()[0]).__name__}  "
          f"nltk: {type(s_nl.lemmas()[0]).__name__}")
    print(f"  id         wn: {s_wn.id!r}  nltk: {s_nl.name()!r}")
    print(f"  ili        wn: {s_wn.ili.id!r}  nltk: absent "
          f"(hasattr={hasattr(s_nl, 'ili')})")


def figure1_backend_unification():
    rule("FIGURE 1 - One implementation, either backend")
    import passivlingo_dictionary as pld

    def describe(backend):
        synset = pld.Wordnet(backend=backend).synsets("vehicle", pos="n")[0]
        return (synset.id, synset.pos, synset.lang, synset.lemmas()[0],
                [h.lemmas()[0] for h in synset.hypernyms()])

    for backend in ("omw", "nltk"):
        print(f"  describe({backend!r}) -> {describe(backend)}")

    from nltk.corpus import wordnet as nwn
    nltk_synset = nwn.synsets("vehicle", pos="n")[0]
    print("\n  Silent-failure trap in the native NLTK API:")
    print(f"    s.pos          -> {nltk_synset.pos!r}")
    print(f"    bool(s.pos)    -> {bool(nltk_synset.pos)}")
    print(f"    s.pos == 'n'   -> {nltk_synset.pos == 'n'}")


def table_lexicon_inventory():
    rule("FOOTNOTE 1 - Lexicon inventory (synset counts, ILI coverage)")
    import wn

    print(f"  {'lexicon':10} {'lang':5} {'version':8} {'synsets':>9} {'words':>9}")
    for lex in wn.lexicons():
        n_ss = len(wn.synsets(lexicon=lex.id))
        n_w = len(wn.words(lexicon=lex.id))
        print(f"  {lex.id:10} {lex.language:5} {lex.version:8} {n_ss:>9} {n_w:>9}")




def section5_metadata_audit():
    rule("SECTION 5 - Construction-provenance metadata audit")
    import collections
    import wn

    hybrid_ids = sorted(lex.id for lex in wn.lexicons() if lex.id.startswith("hy"))
    print(f"  hybrid lexicons audited: {', '.join(hybrid_ids)}")

    for lid in hybrid_ids:
        try:
            lexicon = wn.lexicons(lexicon=lid)[0]
            synsets = wn.synsets(lexicon=lid)
        except Exception as exc:
            print(f"  {lid}: SKIPPED ({exc})")
            continue

        # Metadata keys present at each level of the lexicon.
        keys = {"lexicon": collections.Counter(list(lexicon.metadata() or {})),
                "synset": collections.Counter(), "sense": collections.Counter(),
                "word": collections.Counter()}
        confidence = collections.Counter()
        values = collections.Counter()
        ilis = collections.Counter()
        for s in synsets:
            meta = s.metadata() or {}
            keys["synset"].update(list(meta))
            if "source" in meta:
                values[str(meta["source"])] += 1
            if s.ili is not None:
                ilis[s.ili.id] += 1
            for sense in s.senses():
                keys["sense"].update(list(sense.metadata() or {}))
                if "confidenceScore" in (sense.metadata() or {}):
                    confidence["sense"] += 1
            if "confidenceScore" in meta:
                confidence["synset"] += 1
        for w in wn.words(lexicon=lid):
            keys["word"].update(list(w.metadata() or {}))

        total = sum(values.values())
        print(f"\n  {lid}: 'source' key on {total}/{len(synsets)} synsets "
              f"({100.0 * total / len(synsets):.1f}%)")
        for value, count in values.most_common():
            print(f"      {count:6d}  {value}")
        for level, counter in keys.items():
            print(f"    {level:8} metadata keys: {dict(counter) or 'none'}")
        print(f"    confidenceScore present: {dict(confidence) or 'none'}")
        shared = sum(1 for n in ilis.values() if n > 1)
        print(f"    ILIs shared by more than one synset: {shared}")


def section3_wn_compatibility():
    rule("SECTION 1.1/2.3 - Relationship to wn's own API")
    import wn
    import passivlingo_dictionary as pld

    s_wn = wn.synsets("house", lexicon="ewn", pos="n")[0]
    langs = sorted({t.lexicon().language for t in s_wn.translate()})
    print(f"  wn translate(), no arguments, one call -> languages {langs}")

    w = pld.Wordnet(backend="omw", lang="de")
    s = w.synsets("vehicle", pos="n")[0]
    native = wn.synsets("vehicle", lexicon="ewn", pos="n")[0]
    print(f"  identifier   library: {s.id!r}  wn: {native.id!r}")
    try:
        w.synset(native.id)
        print("  wn identifier accepted by Wordnet.synset(): yes")
    except Exception as exc:
        print(f"  wn identifier accepted by Wordnet.synset(): no "
              f"({type(exc).__name__})")
    print(f"  lemma type   library: {type(s.lemmas()[0]).__name__}  "
          f"wn: {type(native.lemmas()[0]).__name__}")

    n = pld.Wordnet(backend="nltk").synsets("vehicle", pos="n")[0]
    print(f"  NLTK backend translate() -> {n.translate()!r}, "
          f"descriptions(lang='de') -> {n.descriptions(lang='de')!r}")



def software_measurements():
    rule("SECTION 4 - Software measurements")
    for name in ["core.py", "exceptions.py", "__init__.py"]:
        path = REPO / "passivlingo_dictionary" / name
        if path.exists():
            print(f"  {name}: {len(path.read_text().splitlines())} lines")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "--collect-only"],
        cwd=REPO, capture_output=True, text=True,
    )
    for line in result.stdout.splitlines():
        if "collected" in line:
            print(f"  tests: {line.strip()}")


if __name__ == "__main__":
    table1_api_divergence()
    figure1_backend_unification()
    section3_wn_compatibility()
    table_lexicon_inventory()
    section5_metadata_audit()
    software_measurements()
    print("\nDone.")
