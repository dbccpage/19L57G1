# 19L57G1

Forcing a universe without observers from nowhere.

A formal system derived from an opaque seed under externally imposed
challenges, carried out **blind** — no external research, no target
theory, no prior instructions — and verified across four independent
layers that each constrain the others.

---

## What is actually here

A finite object language (data, forms, instances, rules, requirements)
that changes state only through admission events, together with a
complete audit trail of what was derived, what was computed, what was
proved, and — stated with equal precision — what was not.

| | |
|---|---|
| Python | 54 modules; the computational object language and its studies |
| Lean 4 | 61 modules, 59 imported and audited, 2 parked |
| Tests | 34 files, 435 tests, line 99.10% / branch 96.73% |
| Artifacts | 37 deterministic JSON exports plus 6 full gzipped trees |
| Claims | 127 ledger entries, each naming its own evidence |
| Axioms | 1417 `#print axioms` reports, all within `{propext, Quot.sound}` |

The derivation's result is not that some structure was built. It is
that at the first point where the system had to answer, **the
mathematics did not say which answer**: the minimum response costs
exactly two items in both readings, and the minima are tied — three
non-isomorphic classes in reading L and five in reading F within the
declared bounds, with a countably infinite tie family indexed by arity
in reading L. Selecting one requires declaring a further measure, and a
declaration is not a derivation.

Each of those scopes is load-bearing and each is stated wherever the
result is cited. Reading L and reading F are two surviving readings of
the same challenge text, and no internal fact separates them.

## The engineering: four layers that check each other

No single layer is trusted. Each produces evidence a different layer
can contradict.

```
  Python  ──deterministic──▶  artifacts/*.json  ──regeneration──▶  byte-identical?
    │                              ▲
    │ implements                   │ cited by
    ▼                              │
  claim ledger  ◀──names──  Lean theorems  ──#print axioms──▶  axiom inventory
    │                              │                                  │
    │ every citation               │ every module                     │ every report
    ▼                              ▼                                  ▼
  resolution gate            census pin                       whitelist audit
```

* **Determinism, not description.** Every runner writes sorted, timestamp-free
  JSON. Regenerating and byte-comparing catches drift in both directions:
  a committed artifact nobody regenerates, and a regenerated artifact
  nobody committed.
* **Equality, minimality, isomorphism, and survivor counts are decided by
  implemented algorithms**, never by judgement in prose. The isomorphism
  relation is cross-checked against brute force over all bijection pairs.
* **The Lean layer is censused, not sampled.** Every module under
  `lean4/Derivation/` is elaborated as its own build target against a
  pinned census, so a module the root does not import cannot escape
  typechecking.
* **The ledger is the join.** Each claim carries a class, its Python
  evidence (artifact key and/or test name), its Lean theorem names, and
  its falsifier. A gate verifies every one of those names still resolves.

## Nine gate families

```
1  prompt byte-identity          6  Lean build, forbidden-token and axiom audit
2  transport citations           7  skills well formed, declaring no authority
3  dual 95% line/branch gates    8  paper cross-references resolve
4  strict typing (mypy)          9  ledger evidence citations resolve
5  artifact regeneration
```

Run them with `.claude/skills/gates`, which enforces freshness so a
stale input cannot produce a false pass.

## What the gates do NOT prove

This is the part most repositories leave out, and the reason to trust
the rest.

* **A gate proves a receipt, not a payload.** Hashes, test passes, and
  byte comparisons say what the commands printed. They do not say the
  mathematics is right.
* **"Axiom-clean" is a claim about the enumerated reports** (1417), not
  about every declaration in the tree. Two parked modules elaborate but
  emit no report; their axioms are unchecked. This is recorded as an
  open obstruction, not closed quietly.
* **The ledger gate checks that names resolve, never that wording
  matches proof.** `Class: theorem` with no Lean evidence passes it.
  Whether a claim overclaims is a judgement no gate can make — it was
  audited by hand, and the findings are in the change log.
* **Four clauses of the stopping conditions are operator claims**, not
  gate-discharged: that every notion carries a source classification,
  that every theorem-level claim has Lean evidence or is downgraded,
  that tied minima are retained unless eliminated by proof, and that the
  paper states the strongest defensible terminal result.
* **Cost measures, the candidate grammar, the isomorphism relation, and
  the continuation policy are declared, not derived.** Different
  declarations yield different towers; the `mu1`/`mu2` split documents
  one such sensitivity exactly.

## Reading order

**The result** — `paper/paper.md`. Sections 1–3 set the boundary and the
metatheory; 4–8 are the derivation; **11 is the strongest defensible
terminal result** and 12 is the limitations register.

**The evidence** — `paper/paper_claim_ledger.md`. Every `CL-*` entry
names what backs it. Start here when you doubt a sentence in the paper.

**The kernel** — read these six in order; the other ~25 Python modules
are studies layered on them:

```
code/derivation/model.py       regimes, events, replay
             observe.py        contexts, profiles, separability
             candidates.py     the candidate space and cost measures
             iso.py            the implemented isomorphism relation
             engine.py         challenges 0-3 and the branch tree
             export.py         deterministic JSON and replay verification
```

**The apparatus** — `CLAUDE.md` is the operating manual: commands,
invariants that break CI, and an injection record showing each gate
failing on the exact defect it exists to catch.

## Quick start

```powershell
python -m pytest                    # 435 tests
python -m mypy                      # strict, over code/
cd lean4; lake build; cd ..         # 61 modules, no sorry/axiom/unsafe/partial
```

Artifacts regenerate deterministically:

```powershell
$env:PYTHONPATH = "code"
Get-ChildItem code/run_*.py | ForEach-Object { python $_.FullName --artifacts artifacts2 }
python ci/compare_artifacts.py artifacts artifacts2
```

## Boundary

`prompt/prompt.md` and `prompt/seed_prompt.md` are read-only inputs and
must remain byte-identical; their hashes are recorded in the paper. The
blind protocol governs the whole repository: no external theory,
architecture, or terminology appears anywhere outside the sealed seed
prompt. That is why the paper's post-hoc comparison section is withheld,
and it is the only thing that makes the derivation evidence rather than
a retelling.

`AuthorityEffect: None` — this repository records. It does not certify.
