# instance_demand: status

AuthorityEffect: None. OB-1 remains **OPEN**.

## Target 1 negative handoff

Route: negative. For every E1-shaped program `P` on this grammar, the
`admitInst` write that would discharge Target 1 item 3 is an added host
rule. Item 3 is therefore **unavoidable** as a gap: no member of that
shape produces the existing instance-admission event from admitted
structure alone.

Named obstruction (already proved; this handoff adds no lemma):

- `Emitter.no_native_join_rule` — an enabled two-edge output is not
  universally derivable from the stored instruction and premises. The
  reachable unruled seed has both and lacks the conclusion. Covering the
  output form makes every tuple on that form derivable; it does not make
  a uniform rule perform the admission event.
- `Emitter.represented_run_keeps_graph` — successful represented
  execution keeps its input graph. The existing `Execution.run` does not
  write the computed output into the regime.

`step_insts_mem` / `new_stored_instance_needs_event` still require an
actual `Event.admitInst` for a new stored instance. That event is not
emitted by the represented run, and it is not supplied by sealed
derivability of the join. The Stage 3 admission wrapper remains a host
procedure.

This is not a scoped impossibility theorem and does not close OB-1.

## Scoped no-go for the two-edge instruction class

`lean/NoGo.lean` names class `InClass`: stored form-0 ternary instructions
(the Stage-3 program shape). It is nonempty (`class_nonempty`) and contains
every `Enabled` program's instruction (`class_covers_enabled`). Membership
does not mention E1, owed-separation, or separability.

E1 is defined as a sealed step storing a new instance *without* being that
instance's `admitInst`. That is unsatisfiable
(`e1_impossible` / `new_stored_instance_needs_event`). Therefore no member
satisfies E1 ∧ E2′ ∧ E3 (`no_member_is_endogenous`).

Per-shape:
- unruled Enabled output is not derivable (`shape_uncovered_fails_native_join`);
- an `impose` step is not an E2′ origin (`shape_imposed_fails_E2p`);
- the I1 singleton already separates (`shape_separated_fails_E3`).

The missing operation that would write instances without `admitInst` of the
new tuple is outside the sealed `Event` type
(`missing_operation_is_extension`).

Scope: this class only — represented two-edge programs with form-0
instructions. Host emitters, other encodings, and a seventh constructor
are outside `C`. OB-1 remains OPEN outside this class.

Injection: a class that required `c.2.getD 0 0 = 9` would exclude the
seed instruction; `test_cheating_class_that_drops_enabled_instruction_is_rejected`
records that `InClass` does not.
