# instance_demand: status

AuthorityEffect: None. OB-1 remains **OPEN** outside `NoGo.InClass`.

## Scoped no-go for the two-edge instruction class

`lean/NoGo.lean` names class `InClass`: stored form-0 ternary instructions
(the Stage-3 program shape). Membership does not mention E1, owed-separation,
or separability. It is nonempty (`class_nonempty`) independently of output
coverage (`class_independent_of_coverage`). Every `Enabled` output names a
member as its instruction (`class_covers_enabled`). A successful
functional-graph run of a stored instruction is `Enabled`
(`class_covers_functional`).

E1 is a reading of a class member that yields an output, together with a
sealed step that stores that output. The storing event **may be**
`admitInst`. Forbidding every `admitInst` would exclude the channel under
test. Native store without that tuple's `admitInst` is a separate predicate
(`NativeStore`) and is unsatisfiable (`native_store_impossible` /
`missing_operation_is_extension` / `new_stored_instance_needs_event`). A
constructor that wrote instances without `admitInst` of the new tuple would
sit outside sealed `Event`.

E2′ is an owed pair at the post-state, not an `impose` origin, produced by
`Enabled` firing. The pair need not be in `reqs`. Literal `reqs` E2 is not
used.

E3 is a freshly owed pair whose payload is rule-produced. Already-separable
pairs, and admitted-not-rule-produced payloads, do not qualify. A ruled
`admitInst` leaves separability unchanged
(`owed_iff_of_ruled_admitInst`), so the pair cannot be freshly owed.

`no_member_is_endogenous` uses class membership: the reading names the
stored instruction. The endogenous triple therefore fails on this class
because any storing step of a class member's output is `admitInst` of that
output, and E3 then requires a ruled form whose store cannot freshly owe
the pair.

Per-shape, inside this class:
- unruled Enabled output is not derivable
  (`Emitter.native_closure_counterexample`); E3 fails as
  admitted-not-rule-produced (`shape_unruled_fails_E3`); after unruled
  emission the endpoints separate, so the pair is not owed
  (`shape_unruled_emission_fails_owed`);
- covered / ruled store: E3 fails as not freshly owed
  (`shape_ruled_fails_E3`);
- an `impose` step is not an E2′ origin (`shape_imposed_fails_E2p`);
- host `emit` is channel E1 (an `AdmitInst` write) and not `NativeStore`.

The Stage-1 I1 singleton `(0,[x,y])` is a different encoding and is not a
member of `InClass` (form 0 is binary there, ternary here).

Scope: this class only — represented two-edge programs with form-0
instructions, including the functional-graph reading of those programs.
Host emitters as extra grammar, other encodings, and a seventh constructor
are outside `C`. OB-1 remains OPEN outside this class.

Injection: a class that required `c.2.getD 0 0 = 9` would exclude the
seed instruction that every Enabled output on this seed names;
`test_cheating_class_that_drops_enabled_instruction_is_rejected` records
that `InClass` does not. `test_every_stored_form0_ternary_is_in_class`
pins the unrestricted direction. `test_weak_e3_without_freshness_would_pass_covered`
records that dropping freshness from E3 would accept the covered host
emit; the live E3 rejects it because the pair was already owed.

Named Stage-3 walls that remain (already proved):
`Emitter.no_native_join_rule`, `Emitter.represented_run_keeps_graph`. Host
`emit` still writes through `AdmitInst`.
