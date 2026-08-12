# PR #11 correction ledger (PR #12, Phase I)

Pre-contact audit of the twelve overstrong-label risks named in the
run prompt (§2) and the six correction areas (§4.1–4.6).  Every claim
was audited against the current Lean statements — never against
comments, theorem names, or paper prose.  Verdicts: 2 hold as
labeled, 6 were already corrected by the PR #11 correction pass
(42a33d9), 2 were genuine defects and are repaired here.  Base:
`blind-native-base` = ccd3a53 (merged main after PR #11).

## Verdicts

### C1 — CommonState separation: HOLDS AS LABELED
`CommonState` keeps `posWitness`, `views`, `retained`,
`protectedReqs` as four literally distinct fields
(`Completion.lean:41`); `zeroC` reads only `views`; `obstC` reads
three disjoint parts of the state and never reads `posWitness`.  The
only identification is the kernel transport `ofWorld`, which
instantiates `retained := w.reqs` and `protectedReqs := w.reqs` from
the kernel's single store — disclosed in the source and ledger as a
stated identification, and conservative by the exact transport
theorems `ofWorld_obstruction`, `ofWorld_sep`, `ofWorld_quiescent`.
`witness_not_separation` / `separation_not_witness` keep witness and
observer separation provably unmerged.

### C2 — obstC three-condition conjunction: HOLDS AS LABELED
`obstC` is a conjunction over three independent fields;
`obstC_conditions_independent` realizes all three maximal proper
subsets (retained+zero without protection, protected+zero without
retention, retained+protected without zero) as failing states plus
the non-vacuity witness.  Since `obstC` is a Bool conjunction, every
proper subset of conditions is contained in a failing maximal subset,
so every proper subset has a countermodel.

### C3 — symmetry transport: ALREADY CORRECTED (42a33d9, item 6)
`s2_transport_symmetric` is scoped to the relation store;
`s2_state_not_swap_invariant` explicitly REFUTES whole-state swap
invariance (the ordered `retained`/`protectedReqs` fields, inherited
from `d2Common`, break it).  The exact whole-structure result under
swap is stated: relation store invariant, whole state not.

### C4 — trichotomy naming: ALREADY CORRECTED (42a33d9, item 7)
`rule1_trichotomy` was renamed `rule1_repair_or_extension`; the
action alternative is binary (repair | extension family), refusal is
a parallel non-absorbing record (`refusal_object_inert`,
`refusal_non_absorbing`), and budget/license execution is a separate
gate.  No trichotomy is claimed.

### C5 — towerGen driver boundary: ALREADY CORRECTED (42a33d9)
`towerGen` invokes `nextFamily` on the replayed represented state
with the represented `.tower` policy (`Constitution.lean:152`); the
recursion is declared metatheoretic in the source ("the iteration is
metatheory; no represented transition invokes the interpreter"), and
`tower_driver_autonomy` states level 4 (internal trigger) as NOT
attained.  Relative generative closure is claimed; self-triggering is
not.

### C6 — horizon lawfulness: OVERSTATED → REPAIRED UPWARD (this PR)
Defect: the only Lean lawfulness fact for the generated run was the
stage-3 instance (`gen_three_quiescent` →
`worldAt_three_quiescent`), while ledger entry CL-NC-AUTONOMY cited
"lawfulness across extension" against `tower_driver_autonomy` — a
theorem with no lawfulness conjunct.  Repair (upward): new module
`Derivation/Horizon.lean` proves the complete record characterization
`worldAt_spec : ∀ k, worldAt k = specWorld k` by induction, and from
it `worldAt_quiescent`, `worldAt_wf`, `block_all_accepted`,
`genesis_accepted` — quiescence, well-formedness, and per-event
acceptance at every horizon — lifted to the driver by
`gen_quiescent` and `gen_wf` through `driver_reproduces_tower`.
CL-NC-AUTONOMY now records both the old defect and the new evidence.

### C7 — length freshness: ALREADY CORRECTED (42a33d9, item 3)
`freshName_fresh_on_tower` proves freshness on the tower invariant;
`freshName_not_fresh_generally` refutes it in general.  The scope of
the freshness claim is the invariant, nothing wider.

### C8 — initiality label: ALREADY CORRECTED (42a33d9, item 4)
Terminal renamed INITIAL_KERNEL_PROVED →
UNIQUE_PROBE_COMPLIANT_DESCRIPTOR_IN_DECLARED_TOGGLE_CLASS.
`Initiality.lean` scopes minimality and the retract to the declared
64-member class and probe battery ("nothing wider"); the split
retract is recorded as evidence about that extension only.  The
genuine universal-property question is reopened in Phase VII of this
run with an actual controller category.

### C9 — dependency graph completeness: ALREADY CORRECTED
(42a33d9, item 9)  The receipt and papers state the graph classifies
the declared bridges and does not claim to exhaust every possible
bridge; one OPEN edge is recorded.

### C10 — Nat semantics: FALSE → REPAIRED (this PR)
Defect: the family-interpreter mirror `interp_step`
(`code/derivation/completion.py`) computed `budget - 1` with
unsaturated integer subtraction; for any `gateBudget`-off descriptor
at budget 0 the mirror produced budget `-1`, unrepresentable in the
Lean carrier, while Lean `Nat` subtraction saturates at 0.  Concrete
countermodel (audit): descriptor `(T,T,F,F,T,T)`, world
`{data=(10,20), views=((0,),), reqs=((0,1),), budget=0}`, event
`mark (1,) 0` — Lean no-op, Python state change to budget `-1`.  The
42a33d9 change-log item 8 claim ("disabled guards can never license
states unavailable in Lean") was refuted by this countermodel: the
negative-payload rejections guard event inputs, not the subtraction
result.  Repair: the mirror now saturates
(`max(0, budget - 1)`) at both decrement sites; the shared semantics
is pinned in Lean by `Horizon.interp_budget_bound` (budget trichotomy
for every descriptor and every event), `Horizon.budget_saturation_noop`
(the audit countermodel), and `Horizon.mark_saturation_all_descs`
(all 64 descriptors, decided); the Python suite asserts the identical
facts on the same declared basis
(`test_budget_saturation_matches_lean_nat`,
`test_budget_trichotomy_every_descriptor_event`).  The kernel-level
`step` was never affected (its `budget > 0` guard precedes every
decrement, matching Lean).

## Affected claims

- CL-NC-AUTONOMY (rewritten with old defect recorded).
- paper_change_log.md 42a33d9 item 8 (refuted claim recorded in the
  new change-log entry; the historical entry is left in place as
  sealed history).
- `Constitution.lean` module docstring level-8 parenthetical updated
  to cite the Horizon theorems (comment, not evidence).

No other PR #1–#11 claims were rewritten.
