# Instance-channel claims: Stage 1

AuthorityEffect: None. Outcome **OPEN** for OB-1. The existing `C_reqs`
result is unchanged. No instance generator has yet been exhibited.

| ID | Classification and statement | Evidence | Falsifier or remaining obligation |
|---|---|---|---|
| CL-ID-01 | Proved theorem: after any successful event, instance membership is old membership or that exact instance's admission event. | `step_insts_mem`, `new_stored_instance_needs_event` | A successful sealed event violating the stated membership equivalence. No claim about event authorship. |
| CL-ID-02 | Proved theorem: arbitrary successful histories preserve this exact event provenance; every faithful instance reader returns an instance with that provenance. | `replay_insts_mem`, `genesis_instance_origin`, `faithful_read_origin`; `replay_nil`, `replay_cons` | A faithful read without the corresponding event occurrence from genesis. Faithfulness alone is not E1. |
| CL-ID-03 | Proved theorem: uniform rule admission does not write instances; unstored derivable tuples imply coverage of their entire form. | `uniform_rule_keeps_instances`, `new_derivable_is_uniform` | A native conditional-premise rule, or a rule admission that writes `insts`. Materialization is not supplied by either theorem. |
| CL-ID-04 | Proved theorem: the singleton I1 encoding already separates its distinct endpoints. | `lone_pair_separates`; `probe.sample` for both readings | At distinct endpoints with admitted second endpoint, the displayed context fails. The finite samples also have admitted first endpoints. |
| CL-ID-05 | Proved theorem: the rule-covered control remains collapsed, despite storing the same instance. | `covered_pair_collapsed`; `probe.sample` for both readings | A well-formed separating context in that control. This prevents overgeneralizing CL-ID-04. |
| CL-ID-06 | Proved theorem: all four samples are well-formed and the two requirement-free reading histories, with and without uniform coverage, replay exactly. | `samples_well_formed`, `both_readings_replay`, `both_readings_covered_replay` | Replay or well-formedness failure. These are not replays of the requirement-bearing Challenge-3 endpoints. |
| CL-ID-07 | Deterministic computation: exhaustive one-binary-form sweep on 0..3 data, with every instance/rule subset and empty initial requirements. | `probe.sweep`, `evidence/computation.json` | 1,062 states, 17,762 successful extensions, or 2,337 uniform-conclusion cases fail to reproduce. No unbounded Python claim. |
| CL-ID-08 | Open obstruction: existence of an admitted program whose interpreter emits a fresh demand-instance satisfying E1, owed-separation E2, E3, E4 and a dynamics theorem. | Stages 2–4 in README; prior `endogenous_demand/CLAIMS.md` CL-ED-OPEN | A construction with those proofs, or a justified class-specific impossibility. Not resolved by occurrence being recorded as `AdmitInst`. |

CL-ID-01/02 and the preservation part of CL-ID-03 use `propext`; the uniform
conclusion theorem is axiom-free. CL-ID-04/05 and sample well-formedness use
`propext` and `Quot.sound`; the two replay statements use `propext`.
The nine generated theorem reports are included in `evidence/lean.json`.

## Notions and assumptions

- Supplied task: attempt instance-channel demand production under the stated
  E1–E4 conditions. The alternate E2 reading is examined separately from `reqs`.
- Metatheory apparatus: the fixed verifier, compiler, history census, finite
  state enumeration, and the abstract faithful reader parameter.
- Admitted primitives: the sealed data, forms, instance admission, and uniform
  rules. This stage adds none to the sealed grammar.
- Derived definitions: the two sample regimes and their histories.
- Proved theorems and computations: exactly the rows above and their scopes.
- Open obstruction: event generation and obligation semantics for a represented
  emitter. No host routine in this stage selects an endogenous target.

## Negative controls

The tests inject a changed instance store after `Supply` and require
`INSTANCE_WRITER: Supply`; a wrong replay endpoint and require
`REPLAY_MISMATCH`; a missing event-population entry and require
`INSTANCE_ORIGIN`; and a nonuniform conclusion and require
`UNIFORM_CONCLUSION`. Each replacement is scoped in memory and recovery is
checked. Invalid admissions and unknown reading labels are rejected.
Verifier tests additionally exercise source-population, theorem-census,
dependency, and coverage failures. These guard tests are finite checks, not
proofs that arbitrary tampering or semantic dishonesty can be detected.
