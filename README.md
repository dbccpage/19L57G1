# 19L57G1

A blind finite derivation of what follows from an opaque seed — and where
derivation stops.

A finite formal record developed from an opaque seed under externally imposed
challenges, carried out **blind** — no external research, no target
theory, no prior instructions — and verified across four cross-checking
layers that each constrain the others.

---

## Part of a three-repository programme

This is the first of three public repositories by the same author. They use
different methods and make different kinds of claim. This section says how
they connect, and where the connection is a recorded gap and not a
derivation.

| Repository | Role |
|---|---|
| **19L57G1** (this repository), Genesis | A blind, sealed, finite derivation from an opaque seed, and the point where it stops: the minimum response is tied across readings L and F. |
| [**H3V7N5QF**](https://github.com/dbccpage/H3V7N5QF), Genesis-Ongoing | 25 further blind derivations, each from its own seed, on terms, assertions and a short list of changes: obstruction and answer, fewest changes, counted assertions, two relations, an admission gate, and three operator-targeted climbing rounds. |
| [**theory_of_finite_quantum_mechanics**](https://github.com/dbccpage/theory_of_finite_quantum_mechanics), finite QM | A derivation graph of 892 nodes in 35 stages. It starts from the inert inscription `<>`, passes through Pre-Genesis, Genesis, S(n) and MSS-N, the witnessed-difference programme (WDP), L1 and L1 to L2, and asks how far finite exact constructions reach toward finite QM. Every node carries a status and an evidence grade E0 to E4. |

**How they connect.** The early stages of the finite QM graph are built from
results in this repository and in H3V7N5QF. At finite QM commit `8f1f7ca`
(2026-10-22), 106 nodes cite one or both: 90 cite this repository, and 16
cite H3V7N5QF. By stage, 71 of the 90 are in GENESIS, 9 in PREGENESIS, 8 in
MSSN_SN, and 1 each in IMPLEMENTATION and AUTHORIZATION.

* **Pre-Genesis and Genesis.** The inert inscription `<>` is this
  repository's Challenge 0 (paper section 4; `PG-INERT-DIAMOND`).
  `PG-SIX-OPERATIONS` keeps six operations apart, among them supply and
  admission, which paper section 2 also separates. Supply is a no-op
  (`PG-GEN-SUPPLY-NO-OP`), and the first separation costs two items with
  tied minima (`PGW-MU1-MINIMUM-NOT-UNIQUE-L`). The terminal statement of
  paper section 11 is `PGW-SEALED-TERMINAL-STATEMENT`.
* **What stays open at the join.** Paper section 11, clause (f), says no
  endogenous demand generator was derived. In the finite QM graph that is
  `PGW-ENDOGENOUS-DEMAND-OB1`, status `OPEN`. Its computation chain then
  declares unbounded supply of fresh marks as an import
  (`COMP-C4-UNBOUNDED-SUPPLY-IMPORT`), not as a result.
* **Second derivation.** The rung results under `research/second*` (stake,
  first-demand index, symmetry, succession, duration, engine class and
  others) are recorded as `PGW-RUNG*`, `PGW-C1-ENGINE-CLASS-144` and
  `PGW-C2-RUN-FORWARD-EVERY-HISTORY`. Most are `CONDITIONAL`, and their Lean
  is cited only at this repository.
* **Authorization.** The Alpha harness and its License binding
  (`docs/ALPHA_HANDOFF.md`) are recorded as `PGW-ALPHA-LICENSE-BINDING-M1-M8`
  and feed `TFQ-0506`, a law that keeps repair, extension and promotion of
  evidence apart.
* **Genesis-Ongoing.** The 16 H3V7N5QF nodes record its obstruction and
  fewest-changes results and its contraction, counted-assertion,
  two-relation, admission-gate and leftover derivations (`PG-GEN-ONGOING-*`,
  `PGW-GO-*`). They cite that repository by a sibling path and not by a
  pinned commit.
* **The gap.** The three routes from GENESIS to WDP are
  `GAP_NO_DERIVATION`. Five bridge obligations (`GEN-WDP-O01` to `O05`) are
  open in `PG-WDP-GENESIS-BRIDGE-OBLIGATIONS`. The newer stage
  GENESIS_TO_HIGHER (higher-categorical language over Genesis) is open steps
  and named imports, and its three routes from GENESIS and MSSN_SN are also
  `GAP_NO_DERIVATION`. The sealed derivation does
  not derive a Born rule, a complex field, an inner product or any other
  structure of finite QM. The finite QM graph records each of those as
  conditional, imported or open, with its price.

**What the evidence map says about this repository.** Of the 106 nodes, 100
are grade E0 in the finite QM evidence map. E0 means that map's checkout has
no counted evidence file for the node. For these nodes that is mostly because
the Lean and code they cite are here, not there. All 43 Lean references that
finite QM pins to commit `85a83ae` (the head of `main` here when this section
was written) name a file that exists here and a last name component that
occurs in it. That is a citation check. It is not a replay of the Lean and
not a review that each theorem states its node's claim. The checks that bear
on this repository are the gates below.

* Finite QM [README](https://github.com/dbccpage/theory_of_finite_quantum_mechanics#readme)
  and [evidence map](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/docs/evidence/README.md),
  with the [GENESIS stage table](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/docs/evidence/stages/GENESIS.md).
  Its status page is built by a workflow in that repository for GitHub Pages
  and is not published yet; [`docs/index.md`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/docs/index.md)
  is its source.

This section is navigation for readers. It is not a derivational input, a
citation of an outside result or a comparison. It adds nothing to the sealed
paths, and nothing in them refers to it.

---

## What is actually here

A finite object language (data, forms, instances, rules, requirements)
that changes state only through admission events, together with an
explicit audit trail of what was derived, what was computed, what was
proved, and — stated with equal precision — what was not.

| | |
|---|---|
| Python | 60 typed source files; the computational object language and its studies |
| Lean 4 | 75 modules, 63 in the root's import closure, 12 parked and audited separately; toolchain `leanprover/lean4:v4.33.0`, no Mathlib dependency |
| Tests | 61 files, 919 tests collected at `85a83ae` (`pytest --collect-only`, 2026-10-22) |
| Artifacts | 40 deterministic JSON exports plus 6 full gzipped trees |
| Claims | 140 `CL-*` headings; schema and evidence ratchets expose the remaining legacy gaps |
| Axioms | 1530 axiom reports, all within `{propext, Quot.sound}` |
| Research | 118 registered trees under `research/`, outside the seal; 31 are enumerated by the `research` job (gate 11) and the rest are local receipts, per `research/README.md` |

The Tests row is a collection count, not a pass count. The last recorded
passes are local receipts and were not re-run for this row: 786 passed and 1
skipped (55 files, 787 collected; line 99.10% / branch 96.71%) on 2026-09-19,
and 918 passed and 1 skipped at `fdd63af6` in `docs/GENESIS_CLOSEOUT.md`. The
earlier claim of a current census of 41 files and 481 collected tests was
withdrawn on 2026-09-19; it was a historical count. The row above supersedes
the 2026-09-19 row.

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

**The hand-off** — `docs/ALPHA_HANDOFF.md` states what code built on the
sealed kernel may rely on, what stays host-supplied, and what is not
provided. `docs/GENESIS_CLOSEOUT.md` records the closeout of the research
stage. The finite QM graph cites both.

## Quick start

```powershell
python -m pytest                    # 919 collected at 85a83ae; last recorded run: 918 passed, 1 skipped (fdd63af6)
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
