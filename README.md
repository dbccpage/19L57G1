# 19L57G1

A blind finite derivation of what follows from an opaque seed — and where
derivation stops.

A finite formal record developed from an opaque seed under externally imposed
challenges, carried out **blind** — no external research, no target
theory, no prior instructions — and verified across four cross-checking
layers that each constrain the others.

---

## What is actually here

A finite object language (data, forms, instances, rules, requirements)
that changes state only through admission events, together with an
explicit audit trail of what was derived, what was computed, what was
proved, and — stated with equal precision — what was not.

| | |
|---|---|
| Python | 60 typed source files; the computational object language and its studies |
| Lean 4 | 75 modules, 63 in the root's import closure, 12 parked and audited separately |
| Tests | 55 files, 787 collected: 786 passed / 1 skipped; line 99.10% / branch 96.71% |
| Artifacts | 40 deterministic JSON exports plus 6 full gzipped trees |
| Claims | 140 `CL-*` headings; schema and evidence ratchets expose the remaining legacy gaps |
| Axioms | 1530 axiom reports, all within `{propext, Quot.sound}` |

The Tests row records the local Python-job run of 2026-09-19. The earlier
claim of a current census of 41 files and 481 collected tests is withdrawn
as of that date; it was a historical count.

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
* **The ledger is the join, with explicit legacy debt.** Its 140 `CL-*`
  headings provide the schema for class, Python evidence, Lean names, and
  falsifier fields. Conformance ratchets expose the known missing fields;
  the evidence gate verifies that citations which are present still resolve.

## Twelve gate families

```
1   prompt byte-identity          7   skills well formed, declaring no authority
2   transport citations           8   paper cross-references resolve
3   dual 95% line/branch gates    9   ledger evidence citations resolve
4   strict typing (mypy)         10   parked-module census and audit wiring
5   artifact regeneration        11   research provenance, tests, and typing
6   Lean build, forbidden-token  12   prose-watchlist digest census
    and axiom audit
```

Run them with `.claude/skills/gates`, which enforces freshness so a
stale input cannot produce a false pass.

## What the gates do NOT prove

This is the part most repositories leave out, and the reason to trust
the rest.

* **A gate proves a receipt, not a payload.** Hashes, test passes, and
  byte comparisons say what the commands printed. They do not say the
  mathematics is right.
* **"Axiom-clean" is a claim about the enumerated reports** (1530), not
  about every declaration in the tree. An earlier version of this bullet
  said thirteen parked modules "emit no report; their axioms are unchecked";
  that is WITHDRAWN — `lean4/ParkedAudit.lean` now reports the twelve
  modules outside the root's import closure. What the phrase still excludes:
  **definitions**, since the census reports theorems, and any top-level
  `lean4/*.lean`, since every census is rooted at `lean4/Derivation/`.
  The definition exclusion is not hypothetical: the census program's own
  four apparatus definitions in `lean4/ParkedAudit.lean` carry
  `Classical.choice` (measured 2026-09-18 with
  `ci/check_declaration_axioms.py`, a local tool and not a registered
  gate, which reads every constant the `Derivation` modules add from the
  compiled environment, definitions, instances and internal details
  included, and found none of those outside `propext` and `Quot.sound`).
* **The ledger gate checks that names resolve, never that wording
  matches proof.** `Class: theorem` with no Lean evidence passes it.
  Whether a claim overclaims is a judgement no gate can make — it was
  audited by hand, and the findings are in the change log. Resolution is
  by final name segment, so a bare name can resolve to a same-named
  theorem elsewhere and a cited theorem can lack a report; both are
  pinned residuals, and closing them is sealed and record-only.
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

**The evidence ledger** — `paper/paper_claim_ledger.md`. It records backing
where present and keeps known legacy gaps explicit rather than treating a
green ratchet as completion. Start here when you doubt a paper sentence.

**The kernel** — read these six in order; 26 study modules plus the package
initializer are layered on them:

```
code/derivation/model.py       regimes, events, replay
             observe.py        contexts, profiles, separability
             candidates.py     the candidate space and cost measures
             iso.py            the implemented isomorphism relation
             engine.py         challenges 0-3 and the branch tree
             export.py         deterministic JSON and replay verification
```

**The apparatus** — `CLAUDE.md` is the operating manual: commands,
invariants that break CI, and an injection record for the gate failure modes
that have actually been tested.

## Quick start

```powershell
python -m pytest                    # 786 passed, 1 skipped in the 2026-09-19 local run
python -m mypy                      # strict, over code/
cd lean4; lake build; cd ..         # default targets; the census elaborates all 75 modules
```

Artifacts regenerate deterministically. Family 5 in
`.claude/skills/gates/SKILL.md` first proves its scratch path is inside the
repository, clears it, rejects an empty runner census, runs every top-level
runner, and compares both export sets.

## Boundary

`prompt/prompt.md` and `prompt/seed_prompt.md` are read-only inputs and
must remain byte-identical; their hashes are recorded in the paper. The seal
contract names `prompt/`, `paper/`, `code/`, `lean4/Derivation/`, and
`artifacts/`; none of those paths is amended here. The evidence-backed
blindness claim is narrower: `prompt/`, `code/`, `lean4/Derivation/`,
and `artifacts/` retain their sealed derivational boundary; historical
blindness is the author's attestation. The six existing paper comparison
surfaces are fenced historical apparatus. The author's 2026-09-23 ruling
preserves their existing positions and permits explicitly classified
supplied vocabulary in research outside the seal; `CLAUDE.md` and
`paper/paper.md` section 13 record its exact scope.
`research/` is outside the derivational seal. Its current registration is
generated by `ci/research_index.py` and recorded in `research/README.md`:
that index distinguishes gate-11 trees, local-receipt-only trees, and parked
trees. Each tree's own provenance, test, and typing checks determine its
receipt scope; registration does not extend a result to another tree.
The comparison sections supply no derivational inputs, theorem evidence,
or authorization to extend comparison inside the seal. External citations
remain prohibited throughout the repository. The vocabulary ruling closes
the recorded precedence and placement question without establishing a new
mathematical bridge.

The dated [section 3 correction record](docs/section3_claim_corrections.md)
withdraws the identified broad readings and lists the finite evidence and
open proof obligations for the affected research trees.

`AuthorityEffect: None` — this repository records. It does not certify.
