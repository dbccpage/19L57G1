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

The audit ran on branch `closeout/alpha-audit` from the frozen scope
(`ccd0ab06`). Its adversarial tests are in
`research/alpha_engine/tests/test_admission_boundary.py`. Each test goes
through the real path (`evaluate`, then `make_license`, then
`apply_licensed` or `explore`) and is paired with a positive control that
admits a legitimate transition.

| hypothesis | guarantee | result | evidence |
|---|---|---|---|
| B1: a substituted member of a legitimate key | M1 | **REPRODUCED** | An empty substituted member produced a child that ends in a bare `Impose(0, 1)`. A member of another class produced a child whose key is not the authorized one. The same happened through `explore`, and a forged cost was accepted (`B1SubstitutedMember.*`). |
| B2: a parent that does not replay | M2 | **REPRODUCED** | A `Node` with the F history and the L regime was accepted by both entry points (`B2NodeIntegrity.*`). |
| B3: an authorization reused elsewhere | M3 | **REPRODUCED**, for all four fields | A license granted at L was accepted at a relabelled source that has the *same canonical keys* and evidence, so binding by canonical identity would not have caught it. It was also accepted at another history, for another target, for another measure and under other bounds (`B3LicenseBinding.*`). |
| 4: uniqueness promoted to admission | M4 | **REFUTED** without a license. **REPRODUCED** with an inapplicable one | A unique mu2 class was admitted under a license granted for mu1. The root cause is B3's. |
| 5: a retained alternative disappearing | M5 | **REFUTED** through `explore` (`CensusError`, `FabricatedClassError`). **REPRODUCED** through `apply_licensed` | `apply_licensed` accepted evidence from which two of the three retained classes had disappeared. |
| 6: an inert proposal, and typed stops | M6 | **REFUTED** | Proposal and evaluation leave the declared base unchanged. Under `Bounds(1, 2)` the result is `found=False` with cost `None`, and nothing is admitted. |

**Repairs.** One pass sufficed (commit `b698cf7f`); the second pass of the
budget was not used. All repairs are inside `research/alpha_engine/`:

- A `License` now records the source history digest, the target, the
  measure and the bounds. `check_license_binding` refuses reuse and names
  each field that does not match.
- `check_node_integrity` refuses a parent that does not replay to its
  regime, at the point of use.
- `apply_licensed` and `explore` recompute the evaluation from the sealed
  kernel. They refuse caller evidence that differs (`SubstitutedMemberError`,
  `ForgedEvaluationError`) and execute the recomputed member, never the
  caller's.
- `make_license` still refuses an integer selector.
- `evidence/three_phase.json` was regenerated deliberately with
  `run.py --write`, with no injection live. Its only change is the added
  license binding.

**Live injections.** `python research/alpha_engine/inject_boundary.py`
reverts each repair in the real `driver_a.py`, shows the named failure, and
restores the file. The coordinator re-ran it at the final audit on the
joined branch. Every injection fired and recovered, and the tree was clean
afterwards:

- B1: four failures, e.g. "apply_licensed executed an empty substituted
  member of an authorized key";
- H5: "apply_licensed accepted evidence from which two retained classes had
  disappeared";
- B2: two failures;
- B3 and H4: seven failures, e.g. "a License granted at one source node was
  accepted at a relabelled source".

These injections are recorded in `research/alpha_engine/STATUS.md`. Their
rows for `docs/injection_record.md` are a blocked write (§9.3).

**Correction to the frozen trust-boundary hypothesis (§3).** §3 said that
"the host constructs authorizations through `make_license`". The audit
found that a `License` can be checked for *consistency* with the call, but
not for *provenance*. **The host's call is the authorization**, so a host
must never forward a license it did not build itself. The trusted parties
are:

- the six sealed runtime modules at the pinned baseline;
- the harness's own code;
- the host that calls `apply_licensed` or `explore`.

Checked at use: the `EvalResult`, the parent `Node`, the license's binding
and keys, the census, and proposer offerings (which are never executed).

Excluded: process compromise (including objects that override equality or
use `object.__setattr__`), tampering with the kernel or the harness,
SHA-256 collisions, concurrent use, and any network or identity
authentication. A scope string, digest or Python type is not
authentication, and is not claimed to be.

**Mandatory guarantees after the repair pass.** M1 to M8 all hold within
that trust boundary. For M8, the one command is
`cd research/alpha_engine; python verify.py`. At the final audit it passed
all nine steps on the joined branch:

- sources;
- 169 tests;
- coverage, statements 98.71% and branches 97.75%;
- mypy strict (30 files);
- the fresh Lean build and census;
- the PEA record bytes;
- the four handoff demonstrations;
- the sealed kernel's 66 tests.

It reported 0 skipped checks. A failed or skipped check fails the command;
that was shown by injection (a changed byte in `evidence/handoff_demo.json`,
and a moved `evidence/lean.json`). For M7, the demonstrations and the
replay contact no model provider.

**The frozen scope's test count.** §2.5 says 15 test files at the start.
The audit added `test_admission_boundary.py` and `test_handoff.py`, so there
are now 17.

## 8. Disposition of the second derivation

- **Original stage:** twelve research attempts under the unchanged seed,
  with eleven ordinal labels (0 to 10). Counted by attempts, the budget is
  exhausted (ruling #266). The next-rung rule selected no leftover after
  rung ten.
- **Continuation attempt 1 (Challenge 3): CLOSED.** It was merged by the
  author as #267 (`dabe9a92`), with the tree `research/second_engine`. At
  landing the operator regenerated `docs/index/pins.md`, a generated view
  only.
  - The attempt declared a 144-engine class (108 without the HALT member it
    added) and counted capabilities (six to ten per engine).
  - Minimal members exist in every subclass. None is unique up to
    probe-isomorphism, and none is initial, a refusal stated for inclusion
    of declarations only.
  - No engine was run forward and no census row was decided. The input
    count stays two, with no floor proved.
- **Continuation attempt 2 (Challenge 4 and the FORCED census): CLOSED.**
  *(Updated 2026-09-28.)* At the closeout of 2026-09-25 it was legally
  startable and not begun. On 2026-09-28 the author instructed that the
  pending work be completed, and the coordinator launched it headless from
  `b368f28c` with the same isolated recipe. It opened #269 (tree
  `research/second_run`), which was merged at the author's instruction
  after the full `python` job and its four registered steps ran on the
  branch. The full job failed one test: the attempt's manifest recorded no
  pin of the seed, so the new-tree contract applied to it. The
  coordinator made one landing repair (`938b91fc`), adding the seed's
  path and sha256 to the manifest as every earlier rung records them and
  regenerating the pin index. It changed no research content. After the
  repair the targeted checks and the custody census passed, and #269 was
  merged at `d67523f9`.
  - It ran all 144 engines from both readings to declared bounds (288
    runs; fifteen rounds; a node guard of 250 per run; growth below four
    data), replaying every node and edge.
  - In Lean, for every history of every engine, no step lowers the
    element count and no run returns to a regime it has left.
  - It decided the FORCED column for all twelve census rows at its bounds.
    The element count and irreversibility are FORCED, beyond the bounds
    by proof. Two-ness is FORCED over the 64 LIVE engines. Every other
    row is NOT FORCED, each with a countermodel.
  - At its bounds only, four engines carry the grammar forward declaring
    the stake and not the stream. The attempt calls this neither a floor
    proof nor a reduction outside the bounds.
  - No third attempt is authorized, so the continuation is spent.
- **The run's reporting files** (`research/second/paper.md`,
  `change_log.md`, `claim_ledger.md`) were drafted on 2026-09-25 as an
  explicitly **UNFROZEN DRAFT**. On 2026-09-28 they were reconciled with
  attempt 2 and are now a **FREEZE CANDIDATE**, not frozen.
  - They include the Challenge 0 to 5 dispositions, every attempt, the
    author interventions, and the operator acts. Acts not previously
    committed are attested by the closeout coordinator.
  - The ledger has about 108 claim rows, and every cited Lean statement was
    read in source.
  - The reconciliation added thirty-four rows: `SD-R-1` to `SD-R-22` for
    attempt 2, and `SD-CF-1` to `SD-CF-12` for the FORCED column.
  - The files are frozen only on the author's approval (§9.5).
- **Lean names whose wording outruns their statements** are flagged in the
  ledger and stated exactly there:
  - rung ten's `response_collapses_a_pair`, which is about one instance
    admission, not a sealed-responder minimum;
  - rung nine's `separable_iso` and `collapsed_iso`, which are one
    direction only;
  - rung two's `no_first_demand` and `grammar_carries_no_stake`;
  - attempt 1's `minima_differ_at_genL`, whose non-isomorphism conclusion
    goes through the Python probe;
  - attempt 1's E3 and E4 invariance, proved in the Lean mirror only;
  - attempt 2's `not_separable_through`, which is about one regime; that no
    response of any size separates the pair rests on the Python validity
    clause, not on Lean;
  - attempt 2's history theorems, which speak of every history of sealed
    events and switch markers. That each edge of a Python run is such a
    history is read, not proved.

## 9. Residual ledger, manifest and freeze

### 9.1 Residual ledger at the final audit

**CORE_BLOCKER:** none remains inside the frozen scope. B1, B2 and B3 were
reproduced and repaired, and each repair was proved by live injection.

**EVIDENCE_OR_REPORTING_DEBT**

| id | status at the final audit |
|---|---|
| D1 | Resolved 2026-09-28: the run's paper, change log and ledger were reconciled with both continuation attempts, and the author approved the freeze of the §9.5 snapshot (§9.4). |
| D2 | Open. G10, G13 and G14 are still not live injections, and are not relied on by the handoff. |
| D3 | Open. `CL-ISO-SOUND` has no Lean evidence. |
| D4 | Open. `python_driver_refinement` is NOT_PROVED, and the harness Lean does not model the new license binding. |
| D5 | Open. The original completion gate is not satisfied (§10). |
| D6 | Resolved: `B1SubstitutedMember` now covers a substituted member of a present key. |
| D7 | Resolved: the injection-record rows were written after the author's instruction to finish (§9.3). |
| D8 | New: the Lean names whose wording outruns their statements (§8) are recorded exactly in the run's ledger. |
| D9 | New: the operator acts for rungs four to ten and for attempt 1 were not in any committed file until the draft `change_log.md` recorded them as the coordinator's attestation. The acts for attempt 2 are recorded the same way (2026-09-28). |
| D10 | New (2026-09-28): the completion gate's input-count clause admits two readings of attempt 2's bounded one-input carriers. The run's paper records NOT_ESTABLISHED and leaves the reading to the author at the freeze. Frozen as NOT_ESTABLISHED: the author approved the freeze without a separate ruling (§9.4). |

**SUCCESSOR_RESEARCH**

| id | status |
|---|---|
| S1 | Resolved 2026-09-28: continuation attempt 2 ran and was merged (#269). No further attempt is authorized. Its leftovers H-1 to H-9 are successor research, unassigned. |
| S2 to S8 | Unchanged from §4. |

### 9.2 Manifest

- **Snapshot:** commit `dd39fac5d094708a6933aba6a7ddf2b59110d401` (root
  tree `95eac073efede1eec3a0121fa2260970dfe7d9fb`), the joined closeout
  branch immediately before the commit that adds this section.
- **Self-exclusion:** this file, `docs/GENESIS_CLOSEOUT.md`, is excluded
  from the manifest. The commit that adds this section changes only this
  file.
- **Hashes:** a git tree id binds every file beneath it. The SHA-256 values
  are of LF-normalized bytes.

| path | kind | git object id | files | sha256 (LF bytes) |
|---|---|---|---:|---|
| `research/alpha_engine/` | tree | `1a8802bd2693896b95380d82c696c943815dbde8` | 45 | (tree id binds every file) |
| `research/second/` | tree | `91565ce086beb40ef3c53c28cb1b5184dfb4eadb` | 9 | (tree id binds every file) |
| `research/second_class/` | tree | `7db5d3d9267046dd88a7020a5865b900214fa49e` | 32 | (tree id binds every file) |
| `research/second_duration/` | tree | `1d114702799922c4066248517852c2895ad6e600` | 28 | (tree id binds every file) |
| `research/second_engine/` | tree | `cfda4b00d240de163a3d61481f8b96d63edb31c3` | 34 | (tree id binds every file) |
| `research/second_index/` | tree | `b44d5b9c7d18bf40a25749819c049bc7b46c72b7` | 29 | (tree id binds every file) |
| `research/second_inheritance/` | tree | `5583714fd6f8b2b6e3a5f7f61c9d27dc27cc9254` | 12 | (tree id binds every file) |
| `research/second_iso/` | tree | `00e5b2c1bfdcce8dc8b4e7c9d4fc31ac32389339` | 33 | (tree id binds every file) |
| `research/second_nofirst/` | tree | `34a1a4fc5aee74998f0c092d688a4bbe397495b2` | 34 | (tree id binds every file) |
| `research/second_profile/` | tree | `2b39622c94e1efd0727220e0a62c2b6b1e783e1f` | 31 | (tree id binds every file) |
| `research/second_response/` | tree | `09f1ba8742086080d1377f023962cbaee2b9fa20` | 31 | (tree id binds every file) |
| `research/second_stake/` | tree | `989eed925195c6cb7438bfc26b860e5c6b811fe5` | 18 | (tree id binds every file) |
| `research/second_stream/` | tree | `58029f3c6a3db0f691eb660a58763e96ac7d8f08` | 15 | (tree id binds every file) |
| `research/second_succession/` | tree | `ca8e6f65d5126b80dfeae480fd71a7e098c631b9` | 28 | (tree id binds every file) |
| `research/second_symmetry/` | tree | `1c6f9fdf203ecfa8827b259c903726e1c18c1d43` | 31 | (tree id binds every file) |
| `docs/ALPHA_HANDOFF.md` | blob | `d6b7d1f6d634f3aed33b88c648193fc39a3dc5fc` | 1 | `e2c99d7f61841b0475ac9e81fb37afb9f15fadb71aa1b9e06868b9774cfe36d8` |
| `CLAUDE.md` | blob | `c4210d409880114ef11e9836ab3c9999d3428064` | 1 | `5c0c30ebba8aed2d9075287962096794314ab44d00921924b8a4f090882f19b0` |
| `code/derivation/__init__.py` | blob | `8c239e66976fadaa9e5a04f9451ec4c500c266d4` | 1 | `0fabcb53dc46712447a727f6ceb661e5aab3267a3e8b50bdea11044b64f853af` |
| `code/derivation/model.py` | blob | `b6f95a673853d423a0d73b4faa95b2cd22f306a3` | 1 | `6a7fd2ba9688d47e9291514c623a811cde3c6b9e8fda1d12a608dc9bb0b1f3c2` |
| `code/derivation/observe.py` | blob | `2552c0412d472ae9ff5d31f9068684cfa531aad9` | 1 | `78443d67e613d9cc9924538fe2e0a5acaf81f4654440bfe8586e16652f0317ba` |
| `code/derivation/candidates.py` | blob | `9fa609d8a797f74f1620ce39e377c7dc54ee53b7` | 1 | `856ce42faba2dc2ae1217207ecc8af893eac29b50ae8a374dc06d2ba22c957bb` |
| `code/derivation/iso.py` | blob | `f05399fe6bdfbd2311bf34fa6fe927af194f586f` | 1 | `b0f1f3bcf05126111a07706f4388a9fff5e30455d4b8f127966cf99ab0d0886e` |
| `code/derivation/engine.py` | blob | `343290d82a7fcda91f3ff85751af7af99f9a0359` | 1 | `23803a3dcce2adf0dee623caba33791d41a25d2da3fdfd226da3cad2ee140b5e` |
| `lean4/Derivation.lean` | blob | `e28e855bd17460b86b08eacb169e0c00e4f9de08` | 1 | `97384b4ab806336332d6dceda984a77d6d407526311ef6027ce8b06f58a46b6e` |
| `lean4/Derivation/Basic.lean` | blob | `610d8fc982853807eb892eaaf683fc4eb2959cc1` | 1 | `1520b392f4061af568e00ca4fd235feb03facf6d3612c030c1d60018539e3eed` |
| `lean4/lakefile.toml` | blob | `7a714802e3af2c6a4ad362dfc073a4eb064f209a` | 1 | `e75cbde5829dc2efbb5612fbfdba9301c20ccbf2d21ab80bc87db52f4ead0f3c` |
| `lean4/lake-manifest.json` | blob | `8e201944fa9d35190015955f1e21d458bc2cae14` | 1 | `df949b280480c0c2a766e8e6dd33245fe85923c517f6c0d121b79b6f2b2cab91` |
| `lean4/lean-toolchain` | blob | `025e59548e48cf71f2744154e2890beefe30a258` | 1 | `302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b` |

**Declared exclusions.** The following are not part of this closeout's
frozen content:

- the rest of the repository;
- the sealed paper, artifacts and the Lean modules outside the pins above;
- the passage-system and foundations trees;
- every other research tree;
- the_symbol_game, H3V7N5QF, the level engine and all companion material.

**Proof and build evidence at the final audit:**

- `python ci/run_gates.py --job python --keep-going --workers 8` passed
  13 of 13 steps at `fdd63af6`, with 918 tests passed and 1 skipped. The
  report files merged afterwards change no tested code.
- The Alpha one command passed nine of nine steps at `fdd63af6`.
- The injection script passed: every injection fired and recovered.
- All 48 registered second-derivation steps passed at `ccd0ab06`.
- Continuation attempt 1's four registered steps passed at `b205bb4e`. They
  were run from the workflow text directly, because another session held
  the runner lock.
- The custody census matches its pin: 108 verifiers, 107 green, 1 pinned
  red (`described_replay`, pinned before this work).
- The prose watchlist and the refused-words test are clean.

**Could not be reproduced here:**

- a hosted CI run (none exists, by design);
- the `lean` and `research` jobs in full (only their second-derivation and
  Alpha steps ran);
- the companion comparison (not written, and not permitted before the
  freeze).

### 9.3 Blocked writes

- `docs/injection_record.md`: rows for the closeout's live injections
  (B1, H5, B2, B3 and H4, plus the M8 command checks). This file is outside
  the closeout scope recorded in `CLAUDE.md`, so it was first held as a
  blocked write. **Resolved:** the author instructed on 2026-09-25 that
  the closeout be finished and merged, and the six rows were then
  written. The file is not in the §9.2 manifest, so the manifest is
  unaffected.

### 9.4 Freeze

This manifest is prepared, not applied. The author approves the freeze.
The run's reporting files freeze only after the authorized continuation
stops. The comparison follows the freeze, and only in the permitted
companion repository.

*(Updated 2026-09-28.)* The authorized continuation has stopped: both
attempts are closed and merged. The final manifest the author is asked
to approve is §9.5. It is prepared, not applied.

**FREEZE APPLIED, 2026-09-28.** The author approved the freeze of the §9.5
snapshot on 2026-09-28, in the words "merge #270 and approve the freeze".
#270 was merged at `50d15a44`. At that commit the coordinator checked all
33 entries of §9.5 against `main`: every git object id and every
LF-normalized SHA-256 matches, with no mismatch. What the freeze means:

- **What is frozen:** every file bound by §9.5. That is the three
  reporting files, and everything else under `research/second/` (the seed,
  the plan and the manual included). It is also every `research/second_*`
  tree, the Alpha tree, and the other pinned blobs, as they stand at
  snapshot `90ab34a0`. None of them may change.
- **The headers:** the three reporting files still say "FREEZE
  CANDIDATE ... Not frozen" in their headers. That describes their state
  before this approval. They are left byte-identical, because the freeze
  fixes their bytes. This record, which §9.5 excludes by construction,
  is where the freeze is stated.
- **What follows:** the comparison may now be written, and only in the
  companion repository. It may cause no revision here.
- **D10 was not ruled on separately.** The frozen paper's reading of the
  input-count clause, NOT_ESTABLISHED, stands as frozen.
- **Enforcement:** no gate enforces the freeze. The trees' own pin
  verifiers and the custody census cover their own sources. Nothing fails
  if `research/second/` changes after this commit.

### 9.5 Final manifest for the author's freeze (2026-09-28)

This section is prepared after both authorized continuation attempts
closed and the run's reporting files were reconciled. It supersedes §9.2
as the snapshot the author is asked to freeze; §9.2 stands as the record
of the 2026-09-25 closeout.

- **Snapshot:** commit `90ab34a056d80bb1048d926abcfdfef81e578fe1` (root tree `a82d22d5981713b566767972024a581ae1beb190`), the
  head of the closeout branch immediately before the commit that writes
  this section. The branch's base on `main` is `d67523f9`, the merge of
  #269.
- **Self-exclusion:** this file, `docs/GENESIS_CLOSEOUT.md`, is excluded.
  The commit that adds this section changes only this file.
- **Hashes:** a git tree id binds every file beneath it. The SHA-256 values
  are of LF-normalized bytes. The three reporting files are also bound by
  the `research/second/` tree id, and are listed separately so they can be
  checked on their own.

| path | kind | git object id | files | sha256 (LF bytes) |
|---|---|---|---:|---|
| `research/alpha_engine/` | tree | `1a8802bd2693896b95380d82c696c943815dbde8` | 45 | (tree id binds every file) |
| `research/second/` | tree | `165c64904ebc38ecf522a8dc850a51bb20eab013` | 9 | (tree id binds every file) |
| `research/second_class/` | tree | `7db5d3d9267046dd88a7020a5865b900214fa49e` | 32 | (tree id binds every file) |
| `research/second_duration/` | tree | `1d114702799922c4066248517852c2895ad6e600` | 28 | (tree id binds every file) |
| `research/second_engine/` | tree | `cfda4b00d240de163a3d61481f8b96d63edb31c3` | 34 | (tree id binds every file) |
| `research/second_index/` | tree | `b44d5b9c7d18bf40a25749819c049bc7b46c72b7` | 29 | (tree id binds every file) |
| `research/second_inheritance/` | tree | `5583714fd6f8b2b6e3a5f7f61c9d27dc27cc9254` | 12 | (tree id binds every file) |
| `research/second_iso/` | tree | `00e5b2c1bfdcce8dc8b4e7c9d4fc31ac32389339` | 33 | (tree id binds every file) |
| `research/second_nofirst/` | tree | `34a1a4fc5aee74998f0c092d688a4bbe397495b2` | 34 | (tree id binds every file) |
| `research/second_profile/` | tree | `2b39622c94e1efd0727220e0a62c2b6b1e783e1f` | 31 | (tree id binds every file) |
| `research/second_response/` | tree | `09f1ba8742086080d1377f023962cbaee2b9fa20` | 31 | (tree id binds every file) |
| `research/second_run/` | tree | `7c9b11df24534f78ee693c98f7e436c30c87012f` | 29 | (tree id binds every file) |
| `research/second_stake/` | tree | `989eed925195c6cb7438bfc26b860e5c6b811fe5` | 18 | (tree id binds every file) |
| `research/second_stream/` | tree | `58029f3c6a3db0f691eb660a58763e96ac7d8f08` | 15 | (tree id binds every file) |
| `research/second_succession/` | tree | `ca8e6f65d5126b80dfeae480fd71a7e098c631b9` | 28 | (tree id binds every file) |
| `research/second_symmetry/` | tree | `1c6f9fdf203ecfa8827b259c903726e1c18c1d43` | 31 | (tree id binds every file) |
| `research/second/paper.md` | blob | `11b64eef6ba4fc51c34fd0e77ba1dd65a2a30589` | 1 | `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad` |
| `research/second/change_log.md` | blob | `1a86de272a4a8e8e7d0ec7741005308e290e69f9` | 1 | `b6833db2cd140d5ed5e8fab7e7ff3e425f222bd28eae5342736efefe32f8e2e4` |
| `research/second/claim_ledger.md` | blob | `f4023e1eefb10057a6b18de03568154d77f0eb23` | 1 | `8d333fcc077d9ff33d73644f6172f637bf8ef70e9a7392dca02bc6c6b0451a5b` |
| `research/second/SEED.md` | blob | `bc27dccdd4497197922e5f72723fcee9a38347e1` | 1 | `52439e5f75d1c599ce52dc716beb88f1dd7bfc83856ee73ce85f3a7eeec5e70e` |
| `docs/ALPHA_HANDOFF.md` | blob | `d6b7d1f6d634f3aed33b88c648193fc39a3dc5fc` | 1 | `e2c99d7f61841b0475ac9e81fb37afb9f15fadb71aa1b9e06868b9774cfe36d8` |
| `CLAUDE.md` | blob | `c4210d409880114ef11e9836ab3c9999d3428064` | 1 | `5c0c30ebba8aed2d9075287962096794314ab44d00921924b8a4f090882f19b0` |
| `code/derivation/__init__.py` | blob | `8c239e66976fadaa9e5a04f9451ec4c500c266d4` | 1 | `0fabcb53dc46712447a727f6ceb661e5aab3267a3e8b50bdea11044b64f853af` |
| `code/derivation/model.py` | blob | `b6f95a673853d423a0d73b4faa95b2cd22f306a3` | 1 | `6a7fd2ba9688d47e9291514c623a811cde3c6b9e8fda1d12a608dc9bb0b1f3c2` |
| `code/derivation/observe.py` | blob | `2552c0412d472ae9ff5d31f9068684cfa531aad9` | 1 | `78443d67e613d9cc9924538fe2e0a5acaf81f4654440bfe8586e16652f0317ba` |
| `code/derivation/candidates.py` | blob | `9fa609d8a797f74f1620ce39e377c7dc54ee53b7` | 1 | `856ce42faba2dc2ae1217207ecc8af893eac29b50ae8a374dc06d2ba22c957bb` |
| `code/derivation/iso.py` | blob | `f05399fe6bdfbd2311bf34fa6fe927af194f586f` | 1 | `b0f1f3bcf05126111a07706f4388a9fff5e30455d4b8f127966cf99ab0d0886e` |
| `code/derivation/engine.py` | blob | `343290d82a7fcda91f3ff85751af7af99f9a0359` | 1 | `23803a3dcce2adf0dee623caba33791d41a25d2da3fdfd226da3cad2ee140b5e` |
| `lean4/Derivation.lean` | blob | `e28e855bd17460b86b08eacb169e0c00e4f9de08` | 1 | `97384b4ab806336332d6dceda984a77d6d407526311ef6027ce8b06f58a46b6e` |
| `lean4/Derivation/Basic.lean` | blob | `610d8fc982853807eb892eaaf683fc4eb2959cc1` | 1 | `1520b392f4061af568e00ca4fd235feb03facf6d3612c030c1d60018539e3eed` |
| `lean4/lakefile.toml` | blob | `7a714802e3af2c6a4ad362dfc073a4eb064f209a` | 1 | `e75cbde5829dc2efbb5612fbfdba9301c20ccbf2d21ab80bc87db52f4ead0f3c` |
| `lean4/lake-manifest.json` | blob | `8e201944fa9d35190015955f1e21d458bc2cae14` | 1 | `df949b280480c0c2a766e8e6dd33245fe85923c517f6c0d121b79b6f2b2cab91` |
| `lean4/lean-toolchain` | blob | `025e59548e48cf71f2744154e2890beefe30a258` | 1 | `302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b` |

**Declared exclusions:** as in §9.2, plus the_symbol_game's level engine
and every companion comparison.

**What the freeze would fix.** The author's approval of this snapshot
freezes the three reporting files and the trees above as the record of
the second derivation's research stage. After the freeze the comparison
may be written, and only in the companion repository. No file in this
repository is revised because of it.

**What remains unmet at this snapshot** (`research/second/paper.md` §14):
every gate proved by injection (UNMET) and the post-freeze comparison
(UNMET). Several clauses are NOT_ESTABLISHED, including the input-count
floor, whose reading at the freeze is the author's (D10).

## 10. The three axes

| axis | value | why |
|---|---|---|
| `research_phase` | **CLOSED_WITH_OPEN_OBSTRUCTIONS** | *(Updated 2026-09-28; it was RUNNING at the closeout of 2026-09-25.)* The original budget is spent, and both authorized continuation attempts have closed and been merged (#267, #269). No further attempt is authorized. Obstructions remain OPEN: runs past the declared bounds, the 970 refused same demands, Challenge 1 at four items, the responder in Lean, and the input-count floor. The run's report was frozen on 2026-09-28 at the §9.5 snapshot, by the author's approval (§9.4). |
| `alpha_reference` | **READY_WITHIN_DECLARED_SCOPE** | M1 to M8 hold within the trust boundary of §7. B1, B2 and B3 were repaired in one pass and proved by live injection. The one command passes nine of nine steps with no skips and no model provider. Not universal: the refinement to Lean is NOT_PROVED, demand generation is OPEN, and consumer bridges are OPEN. |
| `original_seed_completion_gate` | **UNSATISFIED** | *(Updated 2026-09-28.)* Two clauses are UNMET: not every gate is proved by injection, and the comparison is not written. Several clauses are NOT_ESTABLISHED, including the input-count floor. No floor is proved; a bounded one-input carrier exists and its reading is the author's. Two clauses moved to MET at the computed scope after attempt 2: every engine run to bounds, and every census row decided. See `research/second/paper.md` §14. |

These axes are independent. A closed stage does not imply readiness,
readiness does not imply universality, and an unmet clause of the original
completion gate stays unmet.
