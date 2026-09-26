# Genesis closeout and the Alpha reference contract

AuthorityEffect: None. This is a closeout record prepared under the
author's closeout scope of 2026-09-25 (`CLAUDE.md`, gate 11, "Genesis
closeout scope"). It changes no sealed path, no seed, no prompt, no
prediction and no historical receipt. It is the single source of truth for
the closeout; the residual ledger lives here and nowhere else.

**Status of this document.** Sections 0–6 are the acceptance scope. They
were written and committed **before any repair**, and they are frozen:
defects found later against the mandatory guarantees in §3 are blockers,
and new aspirations do not enlarge the scope. Sections 7–10 are filled at
the final audit.

## 0. Starting state

- **Starting commit:** `01876f3a43490c3518e5c2c03c975ea9d21f49c0` (the
  merge of #266, the author's continuation ruling).
- **Research in flight at the start:** continuation attempt 1 (Challenge 3,
  the engine), launched headless from `01876f3a` on branch
  `research/second-engine-continuation`. It had made no commit when this
  closeout began. Continuation attempt 2 (Challenge 4) had not begun.
- **Other sessions' state, left untouched:** the main checkout sits at
  `b55fc96a` with an untracked `.grok/` directory belonging to another
  session; several other sessions' worktrees exist under `C:/wt/` and
  elsewhere. None is modified by this closeout.
- **Baseline receipt, before any change:** `python verify.py` in
  `research/alpha_engine/` at `01876f3a` passes all seven steps: sources
  (pinned at `a4dcddff`), 133 unit tests, coverage (statements 98.37%,
  branches 96.75%), mypy, the fresh Lean build and census, and the PEA
  record bytes. This is a local receipt.

## 1. Carriers, kept distinct

Results of different carriers are not combined without a checked bridge.

| carrier | what it is | where | how it is evidenced |
|---|---|---|---|
| **Admission kernel** (sealed) | `Regime`, the six sealed `Event` constructors, stepping and `replay`, admission, the declared candidate space and `min_responses`, canonical keys | `code/derivation/{model,observe,candidates,iso,engine}.py`; `lean4/Derivation/Basic.lean` and the root inventory `lean4/Derivation.lean` | Python tests and artifacts (gates 3 and 5); Lean with the axiom boundary `{propext, Quot.sound}` (gate 6). The Lean development is a token-erased abstraction; Python and Lean are connected by executable checks, **not** by a refinement proof (`CL-TOKEN-ERASURE`). |
| **Alpha harness** | `Proposal`, `EvalResult`, `License`, `Node`; `evaluate`; `apply_licensed`; `explore`; search policies and the census | `research/alpha_engine/` | Its own `verify.py` (a local receipt, not gate 11). It consumes the kernel **by import**, pinned at baseline `a4dcddff`. Its local Lean (`lean/Harness.lean`) is about harness datatypes; `evidence/lean.json` records `python_driver_refinement: NOT_PROVED`. |
| **Passage system** | primitive passage and contact modules, and the foundations trees built on them | `lean4/Derivation/` passage and contact modules; `research/native_bridge`, `native_structure`, `conservation_ladder`, `domain_adapters` | Their own registered verifiers (gate 11). **Not in the Alpha slice.** No checked bridge from the passage system to the Alpha harness is claimed by this closeout. |
| **Second derivation** | the blind research run | `research/second/`, `research/second_*` | Its rungs' registered verifiers. Reported by the closeout (§8 and `research/second/paper.md`), **not** part of the Alpha slice. |
| **Other research carriers** | every other research tree | `research/*` | Their own receipts. Not in the slice. |

## 2. The retained Alpha reference slice

### 2.1 Retained claims

**From the admission kernel** (sealed; cited, not re-proved here):

| claim | kind, as the sealed ledger states it |
|---|---|
| `CL-0-INERTIA` | theorem: with nothing admitted, nothing is derivable |
| `CL-0-NO-PROPOSAL-MUTATION` | theorem (model-scoped): a proposed transition cannot alter admitted state without admission |
| `CL-1-SUPPLY-NOT-ADMISSION` | theorem: supply is not admission |
| `CL-3-MIN-TWO` | theorem: the Challenge-3 minimum valid response cost |
| `CL-3-TIE-CLASSES` | bounded theorem: the tied minima form the stated iso classes |
| `CL-REPLAY` | theorem (compositionality) plus finite computation: every certified regime equals the replay of its recorded history |
| `CL-DETERMINISM` | finite computation: byte-identical artifacts |
| `CL-ISO-SOUND` | finite computation only; the Lean side is unresolved |
| `CL-TOKEN-ERASURE` | the Python/Lean relationship, by executable checks only |

**From the Alpha harness** (`research/alpha_engine/CLAIM_LEDGER.md`):
`AE-PEA-FOLD`, `AE-EVAL-INERT`, `AE-TIE-RETENTION`,
`AE-LICENSE-NOT-EVENT`, `AE-POLICY-SUBSET`, `AE-NO-AUTO-APPLY`,
`AE-SOLE-LICENSE-IS-APPLY`, `AE-NO-INTEGER-SELECTOR`,
`AE-GRADE-NOT-LICENSE`, `AE-FABRICATED-REFUSED`, `AE-LEFTOVER-OBS`,
`AE-RECEIPT-NOT-PROOF`, and the Lean claims `AE-LEAN-LICENSE-NOT-EVENT`,
`AE-LEAN-POLICY-SUBSET`, `AE-LEAN-NO-AUTO-APPLY`, `AE-LEAN-EVAL-INERT`.
Retained as OPEN: `AE-DEMAND-OPEN` (no endogenous demand generator) and
`AE-DRIVER-B-OPEN` (no lift needing a new sealed `Event` kind).

### 2.2 Executable entry points

`evaluate.evaluate`, `evaluate.fresh_retained_keys`,
`driver_a.apply_licensed`, `driver_a.explore`, `harness.make_license`,
`harness.present`, `harness.Node`, the search-policy constructors with
`search_policy.record_census`, `run.py --check`, and `verify.py`.

### 2.3 Source dependencies

The six runtime modules pinned in `research/alpha_engine/SOURCE_MANIFEST.json`
(`code/derivation/__init__.py`, `model.py`, `observe.py`, `candidates.py`,
`iso.py`, `engine.py`) and the Lean files it pins (`lean4/Derivation.lean`,
`lean4/Derivation/Basic.lean`, the Lake configuration and toolchain), at
baseline `a4dcddff`.

### 2.4 Proof dependencies

`research/alpha_engine/lean/Harness.lean`, which imports
`Derivation.Basic`; axiom boundary `{propext, Quot.sound}`. No Lean
theorem refines the Python driver.

### 2.5 Tests

`research/alpha_engine/tests/` (15 files at the start), and for the kernel
claims the sealed test suite under `tests/` run by gate 3.

## 3. Mandatory guarantees: the acceptance scope for `alpha_reference`

Each guarantee needs an executable check through the **real public path**,
a **positive control** that admits a legitimate transition, and a **live
injection** of the named defect that fails by name and recovers when the
injection is reversed. A helper that always raises is not evidence about
the real path, and a synthetic parser test is not a live mutation test.

- **M1. Authorized admission executes only a checked member.** The delta that
  `apply_licensed` and `explore` execute must belong to the authorized class
  **as freshly recomputed from the sealed kernel**, not as read from a
  caller-supplied `EvalResult`: its payload, cost and applicability must be
  checked, and its resulting key must match the authorized key.
  *Falsifier:* a legitimate retained key paired, in a forged `EvalResult`,
  with a substituted representative delta (including an empty delta)
  produces a child.
- **M2. Node integrity.** An admission step refuses a parent `Node` whose
  history does not replay to its stated regime.
  *Falsifier:* a `Node(history=h, regime=r)` with `replay(h) != r` is
  accepted as a parent.
- **M3. Authorization binding.** An authorization is bound to the
  contract-relevant declaration: the source state, the demand (target
  pair), the measure and the bounds. Reuse with any of these changed is
  refused.
  *Falsifier:* a `License` granted for one source node and target is
  accepted at a different source node, target, measure or bound.
- **M4. Uniqueness is not authorization.** No path admits without an
  applicable authorization, including when a result is unique.
- **M5. No silent loss of alternatives.** Every retained class receives an
  explicit disposition (explored, pruned or open); none disappears.
- **M6. Inert proposal and evaluation; typed stops.** Proposal and
  evaluation never change admitted state, and an OPEN, bound or guard
  outcome is never presented as an admitted success.
- **M7. Offline replay.** The reference slice replays and verifies without
  contacting any model provider.
- **M8. One local command.** A single documented command verifies the
  slice, fails when a required check fails, and reports any skipped check.

**Trust boundary, as a hypothesis for the audit to confirm or correct:**
the harness is a local library. The host constructs authorizations
through `make_license`. Values that reach the harness from a proposer
(`Proposal`, `EvalResult`, a `Node`, a `License`) are untrusted data. The
threat model excludes process compromise, tampering with the sealed
kernel's code, and any network or identity authentication; a scope string
or a Python type is not authentication and is not claimed to be.

## 4. Outstanding work, classified at the start

### CORE_BLOCKER (hypotheses the audit must reproduce or refute)

| id | guarantee | the suspected defect, as read in the code at `01876f3a` | reproducible falsifier |
|---|---|---|---|
| B1 | M1 | `driver_a.apply_licensed` checks the claimed keys against a fresh sealed re-quotient, then executes `representative_delta(result, key)`, the first member stored in the caller-supplied `EvalResult` (`driver_a.py`, lines 98–102). The executed delta is not checked against the key. | a forged `EvalResult` with a legitimate key and a substituted or empty member yields a child |
| B2 | M2 | `Node` has no replay check, and `apply_licensed` extends `node.history` while replaying only the new events onto `node.regime`. | a parent `Node` whose history does not replay to its regime is accepted |
| B3 | M3 | `License` holds only a granter, a scope string and keys. `apply_licensed` takes the measure and bounds from the `EvalResult`, and nothing binds the license to a source node or target. | a license reused at another node, target, measure or bound is accepted |

### EVIDENCE_OR_REPORTING_DEBT

- **D1.** `research/second/paper.md`, `change_log.md` and `claim_ledger.md`
  do not exist (seed §9; ruling #266, item 4).
- **D2.** Three alpha_engine gates (G10, G13, G14) are not live injections
  of their named defects. `STATUS.md` already says so. The handoff relies
  only on live injections.
- **D3.** `CL-ISO-SOUND` has no Lean evidence (finite computation only).
- **D4.** `python_driver_refinement: NOT_PROVED`. The harness Lean is not a
  refinement of the Python driver.
- **D5.** The original seed completion gate is not established. The
  declared-input count is reported as two, with no floor proved; the
  engine class has not been run; the comparison has not been written.
- **D6.** The existing G1 test forges an `EvalResult` with an absent key.
  It does not test a substituted member of a present key (that is B1).

### SUCCESSOR_RESEARCH (not closeout work)

- **S1.** Continuation attempts 1 and 2 (Challenge 3, then Challenge 4 with
  the FORCED census), authorized separately by #266. Attempt 1 is running.
- **S2.** Endogenous demand generation (OB-1).
- **S3.** Driver B, and any seventh sealed `Event` kind.
- **S4.** The FORCED census columns.
- **S5.** Mode I, and any tree shaped by the outside level table.
- **S6.** A refinement proof between the Python driver and the harness Lean.
- **S7.** A checked bridge from the passage system to the Alpha harness.
- **S8.** Other trees' OPEN items (NB-17, the action half of NS-17, NB-15,
  DA-9, DA-10, the smooth tier).

## 5. Engineering budget

At most **two repair-and-retest passes** over the slice in §2. This is an
engineering budget, not additional research rungs. If a mandatory
guarantee still fails after the second pass, it stays a blocker and the
verdict is not ready.

## 6. Scope freeze

The acceptance scope above (§§0–5) is frozen by the commit that adds this
file. Later defects against M1–M8 remain blockers; later aspirations do not
enlarge the scope, and no mandatory obligation is dropped to reach a ready
verdict.

## 7. Audit results

*(Filled at the final audit.)*

## 8. Disposition of the second derivation

*(Filled at the final audit.)*

## 9. Residual ledger, manifest and freeze

*(Filled at the final audit.)*

## 10. The three axes

*(Filled at the final audit.)*
