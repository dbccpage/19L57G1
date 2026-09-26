# Alpha handoff: what downstream code may rely on

AuthorityEffect: None.  Written 2026-09-25 as work package D of the
author's Genesis closeout (`docs/GENESIS_CLOSEOUT.md`, which holds the
frozen acceptance scope M1 to M8).  It specifies the Alpha reference
slice as it stands after the closeout audit (work package C, recorded in
`research/alpha_engine/STATUS.md`).  It amends nothing sealed, adds no
language, no provider integration, no interface and no solver, and
claims no equivalence.

## 1. The one command

```powershell
cd research/alpha_engine
python verify.py
```

It runs nine required steps in order, each a separate verifier:

| step | what it checks |
|---|---|
| `sources` | the six sealed runtime modules and the pinned Lean files match their blobs at baseline `a4dcddff` (up to CRLF checkout normalization) |
| `tests` | this tree's unit tests, under branch coverage |
| `coverage_json`, `coverage` | at least 95% of statements and, separately, of branches |
| `mypy` | strict typing of the tree |
| `lean` | a fresh build of the tree's local Lean, its theorem census and axiom reports within `{propext, Quot.sound}` |
| `computation` | `run.py --check`: the PEA record bytes |
| `handoff` | `handoff_demo.py --check`: the four demonstrations of section 10 and their independent checks |
| `kernel_tests` | the sealed kernel's own tests of the six consumed modules (`tests/test_model.py`, `test_observe.py`, `test_candidates.py`, `test_iso.py`, `test_engine.py`); gate 3 runs them with the whole sealed suite |

The command exits 1 when a step fails, and lists the steps after it as
`NOT RUN`.  A skipped test is a skipped check: it is printed as
`SKIPPED CHECK: <step>: <test>` and fails the command, because no check of
the slice is optional.  The last lines are a table of every step's state
and the count of skipped checks.  No step contacts a model provider or
the network.  A pass is a local receipt: it is not hosted CI, and this
tree is not gate 11.

The closeout repairs have live injections, `python inject_boundary.py`,
run by hand on a clean worktree.  The command never runs them.

## 2. Carriers

Only the **Alpha harness** (`research/alpha_engine/`) and the sealed
**admission kernel** it imports (`code/derivation/model.py`,
`observe.py`, `candidates.py`, `iso.py`, `engine.py`) are in this
handoff.  The passage system and the second derivation are not; no
bridge from either to the harness is claimed.  The harness's Lean
(`lean/Harness.lean`) is about harness datatypes; it is not a refinement
of the Python driver (`python_driver_refinement: NOT_PROVED`), and it
does not model the License binding, node integrity or the member check.
The sealed Lean is connected to the sealed Python by executable checks
only (`CL-TOKEN-ERASURE`).

## 3. State and observation

- **State** is a sealed `Regime`: admitted data (presentation tokens,
  identified internally by index), judgment forms with arities,
  instances, uniform rules, and imposed separation requirements.
- **History** is a tuple of the six sealed `Event` kinds: `Supply`,
  `AdmitDatum`, `AdmitForm`, `AdmitInst`, `AdmitRuleAll`, `Impose`.
  `Supply` changes nothing.  State changes only by the admission events
  and `Impose`.
- **Replay**: `derivation.model.replay(history)` rebuilds the regime from
  genesis.  A harness `Node` is `(history, regime, license)`; an
  admission step refuses a parent whose history does not replay to its
  regime (`NodeIntegrityError`).
- **Observation** is the sealed `derivation.observe`: contexts,
  profiles, `separable`, `witness`, `collapsed_pairs`, and `satisfies`
  (every imposed pair is separated).  After an admission, `explore`
  returns each child's collapsed pairs as observations.  They are not a
  next demand (`leftover_as_demand` refuses).
- **Event history is not domain state.**  A `Node`'s history records
  admissions in the sealed object language.  It represents no
  consumer's domain state unless the consumer supplies and checks a
  mapping (section 12).

## 4. Demand policy: host-supplied

A demand is a target pair `(i, j)`, `0 <= i < j < n_data`: the requirement
that data `i` and `j` become internally separable.  The **host** supplies
it, together with the measure (`"mu1"`: item count; `"mu2"`: item count,
then new-form arity sum) and the declared `Bounds(max_items, max_arity)`.
The fixtures use each Challenge-3 reading's target: L `(0, 1)`, F
`(1, 2)`.  **Endogenous demand generation is OPEN** (`AE-DEMAND-OPEN`,
OB-1): nothing in the harness chooses a next demand, and a consumer must
not expect it.  The sealed engine's pair-separation closure policy is a
declared policy of the sealed derivation, not a harness function.

## 5. Proposals

A `Proposal(token, offerings)` is Supply-shaped: `present(regime,
proposal)` returns the regime unchanged, and `as_admit` refuses to treat
it as an admission.  `proposer.occupy(proposer, node)` records a
proposer's offerings.  An offering must be a `Delta` (a tuple of
`NewDatum`, `NewForm`, `NewInst`, `NewRuleAll`), and a proposer that
exposes `emit`, `materialize` or `host_next_demand` is refused.  **No
offering is ever executed.**  Only members recomputed from the sealed
kernel are.

## 6. Evaluation evidence

`evaluate.evaluate(base, target, measure, bounds)` enumerates the sealed
`min_responses` and groups them by the sealed `canonical` key of the
replayed child.  It returns an `EvalResult` and never admits:

- `measure`, `cost` (`None` when nothing is found), `raw_minima`;
- `retained`: every iso class as `RetainedClass(key, members)`, in
  sealed-key order, with members in `min_responses` order;
- `found`, `max_items`, `max_arity`.

It never returns a grade (`Tie`, `UniqueClass`, `UniqueDelta`) or `None`.
A score is not a license.  **An `EvalResult` is evidence only.**  The
admission path recomputes it, and refuses a caller's copy that differs
(section 7).  "Minimum" and "iso class" are relative to the declared
candidate space and bounds; they are not claims beyond them.

## 7. Authorized admission and its binding

The host authorizes with

```python
license = make_license(
    granter=..., scope=...,            # labels, not authentication
    authorized=keys,                   # sorted, distinct CanonKeys
    source=node, target=(i, j), measure="mu1", bounds=Bounds(2, 2),
)
```

The `License` records `source` as `history_digest(node.history)` (a
SHA-256 digest of the node's history), plus the target, measure and
bounds.  It is not an `Event`.  It has no revoke API and no integer
selector (`make_license` refuses any extra field, including `index`).

`driver_a.apply_licensed(node, result, license, key, target)` then, in
order:

1. refuses a parent that does not replay (`NodeIntegrityError`);
2. refuses the License if its source, target, measure or bounds differ
   from the call, naming each mismatch (`LicenseBindingError`);
3. recomputes the evaluation from the sealed kernel for the License's
   declaration;
4. returns `None` if `key` is not in `license.authorized`;
5. refuses keys absent from the recomputation (`FabricatedClassError`);
6. refuses evidence that differs from the recomputation: claimed members
   of the class (`SubstitutedMemberError`), or anything else
   (`ForgedEvaluationError`);
7. returns a **new** `Node` whose history is the parent's plus
   `Impose(i, j)` and the admission events of the recomputed class's
   first member, whose regime is their replay, and whose `license` is the
   License.

The parent is never modified.  A unique minimum is never admitted
without a License (`apply_unique_delta` refuses), and a License of a
sole class is still an apply, but only at its own declaration.

## 8. Replay

Every child satisfies `replay(child.history) == child.regime`, extends
its parent's history, has the authorized canonical key, and satisfies
every imposed requirement.  The demonstrations check this with the
sealed `replay`, not with the harness.  `history_digest` makes a history
comparable for binding.  It is a binding, not a credential.

## 9. Alternatives, dispositions and typed stopping outcomes

A declared `SearchPolicy` partitions the retained keys into explored,
pruned and open (`declared_explore_first`, `declared_bounded_priority`,
`declared_constraint_pruned`, `declared_cost_budgeted`).
`record_census` refuses a silent drop (`CensusError`) and a key outside
the retained set.  `explore(node, result, license, census, target)`
applies the same checks as section 7, re-checks the census against the
recomputed keys, admits exactly the explored keys (each must be licensed,
or `UnlicensedExploreError`), and returns
`ExploreResult(children, leftover_pairs, leftover_are_observations,
census)`.  Every retained class has exactly one disposition.  None
disappears.

Outcomes, and how each is typed:

| outcome | how it appears | admitted? |
|---|---|---|
| admitted | a returned `Node`; `ExploreResult.children` | yes |
| not authorized | `apply_licensed` returns `None` | no |
| no valid response within the declared bounds | `EvalResult.found is False`, `cost is None`, no classes; `explore` returns no children and `census.tie_set_size == 0`; OPEN beyond the bounds | no |
| open alternative | a key in `census.open_keys` | no |
| pruned alternative | a key in `census.pruned` | no |
| refused request | a named `HarnessError` subclass: `NodeIntegrityError`, `LicenseBindingError`, `FabricatedClassError`, `SubstitutedMemberError`, `ForgedEvaluationError`, `CensusError`, `UnlicensedExploreError`, `UniqueDeltaAutoApplyError`, `LicenseSelectorError`, `SeventhEventError` and the other refusals in `harness.py` | no |
| kernel guard | `ValueError` from the sealed kernel: an unknown measure, or a base regime carrying a uniform rule (the fast path's precondition) | no |
| a lift needing a new sealed `Event` kind | OPEN (`AE-DRIVER-B-OPEN`); `append_sealed_event` refuses a seventh constructor | no |

Only a returned `Node` is an admission.  No other outcome is.

## 10. The four demonstrations

`research/alpha_engine/handoff_demo.py`, record
`research/alpha_engine/evidence/handoff_demo.json`.  They use the sealed
Challenge-3 fixtures `READING_L` and `READING_F` and run with no model
provider.  Each is checked independently of the harness's verdict: by
sealed `replay`, and by a recomputation from `min_responses`,
`delta_events`, `canonical`, `observe.satisfies` and
`engine.challenge3_report` that does not use `evaluate`.  All 25
independent checks hold.

1. **Accepted transition** (L, mu1, `Bounds(2, 2)`, policy
   `declared-first-key-explored`).  One child, admitted by `Impose(0, 1)`,
   `AdmitForm(1)`, `AdmitInst(0, (0,))`.  It replays from genesis, has
   the authorized key, satisfies its requirement, and its delta is a
   member of the independently recomputed class.  Two alternatives stay
   open.
2. **Retained ties.**  L retains three classes and F five, each of size
   two.  Keys and members equal the independent recomputation, and the
   sizes equal the sealed engine's own quotient.  Each class has exactly
   one disposition.
3. **Refusals.**  A substituted empty member is refused
   (`SubstitutedMemberError`), as is a License reused for mu2
   (`LicenseBindingError: ... measure`) and a parent that does not
   replay (`NodeIntegrityError`).  A retained key the License does not
   name is not authorized (`None`).  Independently: the forged member is
   not a class member and would not satisfy the requirement; mu2 has
   other classes; the bad parent does not replay; the parent is
   unchanged.
4. **Bounded stop** (L, mu1, `Bounds(1, 2)`).  `found=False`, nothing
   admitted, and the frontier is exported as the unresolved declaration
   (source digest, target, measure, bounds), `open_beyond_declared_bounds`.
   Independently, the sealed `min_responses` finds nothing under
   `Bounds(1, 2)` and finds a response under `Bounds(2, 2)`, so the bound
   caused the stop, not an absence of responses.

## 11. What remains host-supplied

- the demand (target pair), the measure and the bounds;
- the search policy and its justification, and the authorization
  decision (which keys, at which node);
- any loop over rounds, its round bound, and when to stop;
- any proposer;
- persistence of nodes and records;
- the mapping between the sealed object language and any domain.

## 12. Trust boundary

The harness is a local, in-process Python library.

- **Trusted:** the six sealed runtime modules at the pinned baseline
  (custody-checked by the `sources` step), the harness's own code, and
  the host.  The host is the code that calls `apply_licensed` or
  `explore`.
- **How authorization is established:** by the host's call.  The host
  builds each License itself with `make_license`, from its own declared
  policy, at the declaration it chose.  A License is a record, not a
  credential.  The harness checks that it is consistent with the call
  (binding and keys), but cannot check who built it.  A host must never
  forward a License it did not build.  A granter string, a scope
  string, a digest and a Python type are not authentication.
- **Untrusted and checked at use:** the `EvalResult` (must equal the
  recomputation, and is never executed), the parent `Node` (must replay),
  the License's binding and keys, the census (re-checked against the
  recomputed keys), and proposer offerings (Supply-shaped, never
  executed).
- **Excluded:**
  - process compromise, including objects that override equality,
    hashing or attribute access, and `object.__setattr__` on frozen
    values;
  - tampering with the sealed kernel or the harness (the custody check
    detects edits to pinned files; it does not defend against a live
    attacker);
  - SHA-256 collisions;
  - concurrent use;
  - any network, identity or multi-party authentication.

## 13. Obligations of a Symbol Game or Omega consumer

These are **obligations**, not established results.  **No bridge** is
established from Symbol Game state or Omega-engine state to the sealed
`Regime`, in either direction.  Each such bridge is **OPEN**, and no
equivalence between any consumer notion and a sealed notion is claimed.

- **O1. Encoding.**  Supply an explicit, total encoding of the domain
  state into a `Regime`, and a decoding of admitted results back, with
  the consumer's own evidence that the encoding is faithful for the
  purpose.  Until it exists, the bridge is OPEN.
- **O2. History versus domain state.**  Keep `Node.history` (sealed
  events) distinct from the domain state it is taken to represent.
  Claim a domain change only through a replayed admission, and never
  write domain state into the history.
- **O3. Demand.**  Supply and record each demand (target, measure,
  bounds).  Do not treat leftover collapsed pairs, grades or proposer
  output as demands.
- **O4. Authorization.**  Build each License with `make_license` at the
  node, target, measure and bounds where it is used.  Never forward a
  License obtained from a proposer or another party.
- **O5. Evidence.**  Treat an `EvalResult` as evidence, and rely on the
  admission path's recomputation, not on a stored copy.
- **O6. Dispositions.**  Give every retained class a disposition
  (explored, pruned or open), through a declared policy and
  `record_census`.  A tie is not resolved by an integer index or by a
  grade.
- **O7. Typed outcomes.**  Distinguish the outcomes of section 9.
  Never report `found=False`, an open or pruned class, `None` or a
  refusal as an admission.
- **O8. Words.**  "Minimum", "canonical" and "iso class" are relative to
  the declared candidate space and bounds.  Do not carry them to a
  consumer notion without a proof or a stated conditional scope.
- **O9. Re-verification.**  Re-run `python verify.py` after any change to
  a pinned input or to `research/alpha_engine/`.

## 14. Not provided, and residuals

Not provided:

- endogenous demand generation (OB-1);
- Driver B, or any seventh `Event` kind;
- a refinement proof between the Python driver and the harness Lean;
- Lean evidence for `CL-ISO-SOUND`;
- a bridge from the passage system;
- any consumer bridge.

Of the harness's older injection rows, G10, G13 and G14 are still not
live injections.  The handoff relies only on the live ones.  Those are
listed in `research/alpha_engine/STATUS.md`.
