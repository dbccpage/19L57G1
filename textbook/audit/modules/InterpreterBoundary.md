# Audit: InterpreterBoundary

| field | value |
|---|---|
| Path | lean4/Derivation/InterpreterBoundary.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 1b8ed7bccefff85f |
| Lines | 394 |
| Imported by root `Derivation.lean` | yes (line 35) |
| Imports | Derivation.Constitution, Derivation.PrimitiveCore |
| Declarations | 13 def (5 of them `String` labels), 13 theorem (inventory lists 15: the docstring words "worth" and "applies" were scanned as names) |
| Axiom reports in `artifacts/lean_axioms.txt` | 13 lines; axioms seen: none / propext / propext, Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

Phase VIII of PR #12 attacks the one bridge the completion left OPEN: the family interpreter `interpStep` is not a member of the 64-descriptor family it runs, so the outermost interpretation relation sits in the metatheory. The module records what can be proved about that boundary along the declared routes I0–I5. I1 is a diagonal: for any finite code list and any evaluation map there is a step function of the same type differing from every coded member (`tower_persists`), the difference being one extra element in the operationally inert `notes` field. I2 restates that `interpStep` with `ConstitutionDesc` covers the declared class exactly. I3 adjoins one uncoded "refusing" top to the family as an `Option`-valued evaluator and records its two defining equations. I5 declares a `PrimitiveCore.Setting` on `Option ConstitutionDesc` whose witnessed, retained, protected pair is (the kernel's description, the uncoded interpreter role), proves it satisfies the native candidates A and F, and proves that any presentation identifying the two endpoints loses irreflexivity. The module then states, as a string label and a docstring, that the denotational bridge — which would connect the uncoded role to interpretation behaviour and make the boundary difference operationally effective — is OPEN; `arbitrary_uncoded_assignment` proves the obvious candidate bridge is vacuous.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| i0_status | 103 | def (String) | label restating the sealed I0 status (quotation / description / verified self-description separated) | ADMITTED (label, not a proposition) |
| indexWorld | 114 | def | `⟨List.range i, [], [], [], 0, true, []⟩`: the world whose carrier length is `i` | ADMITTED |
| diag | 127 | def | `{C : Type} (cs : List C) (ev : C → World → Event → World) w e`: look up code `cs[w.data.length]?`; if present, run it and append `999` to the output's notes, else return `w` | ADMITTED (diagonal construction) |
| tag_quotation … tag_verified_fixed_point | 205–218 | def (String ×5) | five level labels | ADMITTED (labels) |
| evalOpt | 233 | def | `Option ConstitutionDesc → World → Event → Option World`: `some d ↦ some ∘ interpStep d`, `none ↦ fun _ _ => none` | ADMITTED (one declared extension) |
| boundarySetting | 286 | def | `PrimitiveCore.Setting` with `X := Option ConstitutionDesc`, `r = ret = prot := fun x y => x = some kernelDesc ∧ y = none`, `a := some kernelDesc`, `b := none`, `Ops := fun _ => False` | ADMITTED (declared model; relation, retention and protection inserted by definition) |
| openDenotationalBridge | 371 | def (String) | OPEN obligation label | OPEN (label) |
| conclusionTags | 380 | def (List String) | the tag list for the receipt | ADMITTED (labels) |
| frontierConjecture | 390 | def (String) | INTERPRETER_BOUNDARY_IS_PRIMITIVE_DIFFERENCE, stated as a conjecture | OPEN (label) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| indexWorld_len | 117 | `(indexWorld i).data.length = i` | FROZEN | propext | A |
| diag_hit | 132 | if `cs[w.data.length]? = some c` then `diag cs ev w e = {ev c w e with notes := … ++ [999]}` | FROZEN | propext | A |
| tower_persists | 156 | for any `C : Type`, any `cs : List C` and any `ev : C → World → Event → World`, `∃ f, ∀ c ∈ cs, f ≠ ev c` (witness: `diag cs ev`, differing at `indexWorld i` for the index of `c`) | FROZEN (metatheoretic function-space statement) | propext, Quot.sound | S |
| i2_universal_in_class | 199 | `(∀ d, d ∈ allDescs) ∧ (∀ w e, interpStep kernelDesc w e = step w e)`: the pair `⟨allDescs_complete, interp_describe⟩` | FROZEN (re-packaging of two Constitution theorems) | propext, Quot.sound | A |
| i3_refusal_code_returns_none | 241 | `evalOpt none w e = none` (rfl) | FROZEN (definitional) | propext, Quot.sound | A |
| i3_coded_member_returns_some | 246 | `evalOpt (some d) w e = some (interpStep d w e)` (rfl) | FROZEN (definitional) | propext, Quot.sound | A |
| family_missed | 264 | `tower_persists allDescs interpStep`: some step function differs from every `interpStep d` | FROZEN | propext, Quot.sound | S |
| i5_carrier_occurrences | 297 | the declared carrier list (64 coded + `none`) has 65 entries, by `decide` | VERIFIED_FINITE | none | A |
| i5_boundary_is_A | 306 | `PrimitiveCore.A boundarySetting`: the declared pair is related and the declared relation is irreflexive | FROZEN (but every conjunct is by definition of `boundarySetting`) | none | S |
| i5_boundary_is_F | 314 | `PrimitiveCore.F boundarySetting`: A plus `ret a b` and `prot a b` (both definitional) | FROZEN (definitional) | none | S |
| i5_collapse_obstructed | 322 | for any `c : Option ConstitutionDesc → β` with `c (some kernelDesc) = c none`, `PrimDiff.FidelityObstruction PrimDiff.Irrefl boundarySetting.r c` | CONDITIONAL: the presentation identifies the two endpoints | none | S |
| i5_family_not_extensionally_complete | 349 | identical statement to `family_missed` (renamed from `i5_difference_grounded` in the 2026-08-13 audit repair) | FROZEN | propext, Quot.sound | A |
| arbitrary_uncoded_assignment | 356 | for every `f : World → Event → World` there is `I : Option ConstitutionDesc → World → Event → World` with `I none = f` and `I (some d) = interpStep d` for all `d` | FROZEN (trivially true: define `I` by cases) | propext, Quot.sound | S (as a negative result) |

Count check: 13 theorems, all 13 in the artifact.

## 4. External and admitted assumptions

- `ConstitutionDesc`, `interpStep`, `kernelDesc`, `allDescs`, `allDescs_complete`, `interp_describe` from Constitution; `PrimitiveCore.Setting`, `A`, `F`; `PrimDiff.Irrefl`, `FidelityObstruction`, `obstruction_under_irrefl`.
- `tower_persists` is parametric in a universe-level `{C : Type}` and concludes an existential over the function type `World → Event → World`. Finitude flag: both are metatheory. The system holds no object "the function type of step functions"; the theorem says only that a Lean list of codes does not enumerate that Lean type. The docstring (lines 136–155, read) and the paper state this exactly ("extensional incompleteness", "nothing more").
- `boundarySetting`'s relation, retention and protection are inserted by definition; nothing derives them from behaviour. The paper says so in those words. Admitted condition later described as forced: no — the paper and the ledger both say DECLARED. Unearned identity: none; the module explicitly refuses to identify `none` with the diagonal's missed function. Unspecified correspondence between presentations: the correspondence between the uncoded occurrence `none` and "the interpreter" is a reading, not a theorem (the docstring says so). Cost function: none. Silently assumed observer: none. Finite computation presented as universal: `i5_carrier_occurrences` is a `decide` over 65 entries and is presented as such.
- The five tag strings, `i0_status`, `openDenotationalBridge`, `conclusionTags`, `frontierConjecture` are data: they prove nothing and are not propositions. A reader of `#print axioms` output will see no axioms for them only because they are not theorems.

## 5. Derived consequences

Not imported by any other Derivation module (checked: only the root imports it). Ledger CL-NC-INTERPRETER-BOUNDARY (lines ~1715–1745) cites `tower_persists`, `family_missed`, `i5_boundary_is_A`, `i5_boundary_is_F`, `i5_collapse_obstructed`, `i5_family_not_extensionally_complete`, `arbitrary_uncoded_assignment`; `paper/primitive_interpreter_boundary.md` is the write-up; `paper_change_log.md` lines ~755–780 record the rename; `paper/native_derivation_map.md` last row ("kernel constitution interprets itself absolutely | OPEN | stratification boundary") is the dependency-map placement.

## 6. Counterexamples and limitations

- Countermodel content: `tower_persists`/`family_missed` exhibit, for the 64-member family, a step function missed by all 64 — the diagonal that appends `999` to `notes`. Since `notes` is inert (`Represented.notes_inert`, `supp` drops it), the missed function has the same support behaviour as `interpStep kernelDesc` at the indexed world; so this is extensional, not operational, incompleteness.
- `arbitrary_uncoded_assignment` is a countermodel to the proposal "existence of an interpretation sending `none` to the missed function grounds the boundary": any function can be so assigned, hence the existence is vacuous.
- The OPEN boundary, stated precisely. **Proved:** (i) the sealed `step` is reproduced by the fixed family interpreter at the kernel's descriptor, `interpStep kernelDesc = step` extensionally (`Constitution.interp_describe`); (ii) the descriptor family is exactly `allDescs` (`allDescs_complete`); (iii) the kernel's descriptor is the unique probe-compliant member (`Initiality.unique_compliant`); (iv) the generated tower is reproduced by the driver (`Constitution.driver_reproduces_tower`, `nextFamily_complete`); (v) no finite code family exhausts the function type (`tower_persists`); (vi) a declared Setting on `Option ConstitutionDesc` satisfies A and F and its endpoint-collapse is obstructed. All of (i)–(iv) are family-relative: "the constitution represented as data" means a six-Bool toggle vector read by an interpreter that is itself fixed metatheoretic code and is not one of the 64 toggle vectors. **Not proved:** that `interpStep` (or any evaluator) has a code in the family it runs; that running such a code reproduces `interpStep`'s own behaviour on itself; that the uncoded occurrence `none` means anything (no interpretation relation is defined on it beyond `evalOpt none = none`, which is a refusal); that the description/interpretation boundary is a primitive difference in the operational sense (no accessible verdict changes under its collapse — the only proved difference is in `notes`); absolute no-outside in either direction.
- The six-way vocabulary, with its Lean referent: a **represented transition** is `step w e` (Represented), a World-to-World map driven by a represented `Event`; a **coded interpreter** is `interpStep d` for `d : ConstitutionDesc`, a step function selected by data; a **behavioural distinction** is a probe on which two coded interpreters disagree (Initiality `*_load_bearing`, Python `distinct_on_basis`); a **denotational interpretation** would be a relation from codes (and the uncoded role) to step functions constrained by behaviour — none is defined; `evalOpt` and `arbitrary_uncoded_assignment` show the candidate definitions are either refusal or unconstrained; a **self-description** is `interp_describe`: the kernel's own transition appears in the family at `kernelDesc`, verified by proof; an **absolute self-interpreter** would be a code `c` with `ev c = ev`, or an interpreter in the family of what it interprets — not constructed, not refuted, OPEN.

## 7. Axiom dependencies

All 13 within {propext, Quot.sound}; the five I5 theorems use none. Theorems exceeding the set: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 13 theorems in the artifact; ledger and paper cite them. No probe run. Proofs read: `tower_persists` uses `indexWorld_len` and `diag_hit` to show the notes lists differ in length at the indexed world; `i5_collapse_obstructed` is a direct application of `PrimDiff.obstruction_under_irrefl` with `h : r a b := ⟨rfl, rfl⟩`.

## 9. Related Python implementations

`code/derivation/interpreter_boundary.py`: `Desc`, `all_descs`, `interp_step`, `behavior_vector`, `distinct_on_basis`, `self_description_on_basis`, `index_world`, `diag`, `diagonal_misses_all`, `eval_opt`, `carrier`, `boundary_rel`, `irrefl`, `candidate_a`, `candidate_f`, `collapse_obstructed`, `interpreter_report`; artifact `artifacts/primitive_interpreter.json`. Tests: `tests/test_interpreter_boundary.py` (`test_kernel_matches_sealed_step_eventwise`, `test_each_toggle_load_bearing_on_its_probe`, `test_all_64_behaviorally_distinct_on_basis`, `test_truncated_basis_fails_to_separate`, `test_diagonal_misses_every_member_exhaustively`, and the fake-diagonal negative test).

## 10. Textbook placement proposal

- Prerequisites: `ConstitutionDesc` / `interpStep` / `interp_describe` (Constitution); `notes_inert` and `supp` (Represented); `PrimitiveCore.Setting`, A, F; `PrimDiff.FidelityObstruction`.
- Substantive: `tower_persists` with its exact scope; `arbitrary_uncoded_assignment` as the vacuity proof; `boundarySetting` with `i5_boundary_is_A`/`_F`/`i5_collapse_obstructed` as "a declared model, not a derived one"; the OPEN statement in §6 above.
- Auxiliary: `indexWorld`, `indexWorld_len`, `diag_hit`, `i2_universal_in_class`, the two `evalOpt` equations, `i5_carrier_occurrences`, `i5_family_not_extensionally_complete`, every String label.
- Lesson title: "The interpreter is not in its own family: what a notes-diagonal does and does not show." The one question: what, exactly, separates a verified self-description from a self-interpreter, and why is the remaining gap OPEN rather than closed either way?
- Omit: the String labels (report them as receipt text, not as declarations); `i5_family_not_extensionally_complete` (a duplicate name for `family_missed`, kept for the audit trail).

## 11. Interpretation findings

1. Theorem name `tower_persists` and the I1 route label ("every finite closure has a new top" in the Phase VIII framing) versus the Lean statement `∃ f, ∀ c ∈ cs, f ≠ ev c`. Smallest reading of the gap: the witness differs from every coded member only in the `notes` field, which `supp` discards; on supports the diagonal at `indexWorld i` agrees with `ev c`. So "tower" and "top" are not earned; "extensionally incomplete" is. The paper's review pass and the ledger already say exactly this, and the renamed theorem `i5_family_not_extensionally_complete` fixes the name on the I5 side; the I1 name remains. Classification: INTERPRETATION DEFECT (mild; scoped in prose, unscoped in the identifier).
2. `i5_boundary_is_A`, `i5_boundary_is_F` docstrings and the paper's terminal DECLARED_BOUNDARY_MODEL_SATISFIES_A_AND_F. Lean: A and F hold because `r`, `ret`, `prot` are each defined as "x is the kernel code and y is the uncoded occurrence"; irreflexivity holds because `some _ ≠ none`. Nothing about interpretation enters. The paper says "inserted BY DEFINITION". Classification: none as a defect (the scoping is explicit); recorded so the textbook presents these as "the declared model is consistent with A and F", not as "the boundary is a primitive difference".
3. `i2_universal_in_class` ("universal code and evaluator, in the declared class"): the theorem is the pair `⟨allDescs_complete, interp_describe⟩`, i.e. "the list is complete and the kernel is in it"; "universal" is a name. Classification: INTERPRETATION DEFECT (mild): no universality property (e.g. every coded interpreter's behaviour obtained by running one fixed code on data) is stated beyond what `interpStep d` already is by definition.
4. Finitude: `{C : Type}` and `∃ f : World → Event → World` are metatheoretic; the docstring of `tower_persists` says "uniform in the level" and "recoding the missed function yields a new finite family to which it applies again" — a metatheoretic iteration over Lean lists, not a tower the system builds. Classification: INTERPRETATION DEFECT (mild, finitude); the paper's "nothing more" clause bounds it.
5. Vacuity: `arbitrary_uncoded_assignment` is trivially true (its proof is a case split on `Option`), and the module says so: it is recorded precisely as the proof that a candidate bridge is vacuous. `i3_*` are `rfl`. No hypothesis set is unsatisfiable; `i5_collapse_obstructed`'s hypothesis `c a = c b` is satisfiable (any constant `c`).
