# instance_demand: status

AuthorityEffect: None. OB-1 remains **OPEN** outside `NoGo.InClass`.

## Scoped no-go for the two-edge instruction class

`lean/NoGo.lean` names class `InClass`: stored form-0 ternary instructions
(the Stage-3 program shape). Membership does not mention E1, owed-separation,
or separability. It is nonempty (`class_nonempty`) independently of output
coverage (`class_independent_of_coverage`). Every `Enabled` output names a
member as its instruction (`class_covers_enabled`).

E1 is a sealed step storing a new instance *without* being that instance's
`admitInst`. That is unsatisfiable on the sealed grammar (`e1_impossible` /
`new_stored_instance_needs_event`). The endogenous triple E1 ∧ E2′ ∧ E3
therefore fails because E1 does. Class membership is not a hypothesis of
that unsat: the same fact holds outside `InClass`. The class is the scope
of the claim, via nonempty cover, not an unused binder.

Per-shape, inside this class:
- unruled Enabled output is not derivable (`Emitter.native_closure_counterexample`);
- an `impose` step is not an E2′ origin (`shape_imposed_fails_E2p`);
- after unruled emission the endpoints separate, so E3 fails
  (`shape_unruled_emission_fails_E3` / `unruled_emission_separates`).

The Stage-1 I1 singleton `(0,[x,y])` is a different encoding and is not a
member of `InClass` (form 0 is binary there, ternary here).

A constructor that wrote instances without `admitInst` of the new tuple
would sit outside sealed `Event`. That is the content of
`new_stored_instance_needs_event`, not a renamed alias.

Scope: this class only — represented two-edge programs with form-0
instructions. Host emitters, other encodings, and a seventh constructor
are outside `C`. OB-1 remains OPEN outside this class. Literal `reqs` E2
is not used.

Injection: a class that required `c.2.getD 0 0 = 9` would exclude the
seed instruction that every Enabled output on this seed names;
`test_cheating_class_that_drops_enabled_instruction_is_rejected` records
that `InClass` does not. `test_every_stored_form0_ternary_is_in_class`
pins the unrestricted direction.

Named Stage-3 walls that remain (already proved; this file adds no lemma
about them): `Emitter.no_native_join_rule`,
`Emitter.represented_run_keeps_graph`. Host `emit` still writes through
`AdmitInst`.
