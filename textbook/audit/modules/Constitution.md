# Audit: Constitution

| field | value |
|---|---|
| Path | lean4/Derivation/Constitution.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | c77bef4b6ec965cc |
| Lines | 393 |
| Imported by root `Derivation.lean` | yes (line 26) |
| Imports | Derivation.Completion (and through it Represented, RefusalFrontier) |
| Declarations | 1 inductive (Policy), 2 structure (GWorld, ConstitutionDesc), 10 def, 16 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 16 lines; axioms seen: none / propext / propext, Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

Stage V asks whether the event stream that `Represented` had to supply from outside (`histUpTo`) can instead be produced from represented state. The module adds a `Policy` field (idle / tower / close) beside the kernel world, a fixed function `nextFamily` from that pair to the complete family of next event blocks, and a driver `towerGen` that at each stage replays the history so far, asks `nextFamily` for the family, and appends its unique member. The headline theorem `driver_reproduces_tower` says the generated history is exactly the previously supplied stream, stage by stage. The module also writes the kernel constitution as data: a six-Boolean descriptor `ConstitutionDesc` (one toggle per guard), a fixed family interpreter `interpStep` that executes any descriptor, and the theorem `interp_describe` that the all-true descriptor executes to exactly the sealed `step`. Stage VI assesses the driver against a nine-level autonomy ladder and states level 4 (internal triggering) as not attained. The module says, in its header and docstrings, that the iteration, the interpreter and the fresh-name arithmetic are fixed metatheory, and that the family interpreter is not a member of the family it interprets — the named irreducible obligation and the single OPEN row of the dependency map.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| Policy | 44 | inductive | idle / tower / close | ADMITTED (declared generation policy) |
| GWorld | 50 | structure | a World plus a Policy | ADMITTED |
| freshName | 62 | def | `w.data.length`: the canonical numeral | ADMITTED (declared fresh-name function; imports arithmetic/ordering, stated) |
| towerBlock | 64 | def | `[setBudget 1, admitTok n, require 0 n, addView [n]]` with n = freshName w | ADMITTED (declared block shape) |
| closeBlocks | 71 | def | for every violated requirement, every accepted mark and every accepted augmentation (`Completion.augFamily`), each as a one-event block | ADMITTED |
| nextFamily | 80 | def | idle ↦ []; tower ↦ [towerBlock w]; close ↦ closeBlocks w | ADMITTED (the fixed interpreter; constitution) |
| towerGen | 152 | def | `Nat → List Event`: metatheoretic iteration of nextFamily with the `.tower` policy hard-wired at every stage | ADMITTED (declared metatheoretic driver) |
| genWorld | 214 | def | ⟨replay (towerGen k) genesis, .tower⟩ | ADMITTED |
| ConstitutionDesc | 303 | structure | six Bools: dedupAdmit, guardRequire, guardAccept, gateBudget, gateLicense, certRefusal | ADMITTED (the declared description family) |
| kernelDesc | 312 | def | all six true | ADMITTED |
| interpStep | 318 | def | the family interpreter: a copy of `step` whose five guards are each disabled by the matching toggle | ADMITTED (constitution; metatheory) |
| bools / allDescs | 377 / 379 | def | enumeration of the 64 descriptors | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| nextFamily_tower_singleton | 87 | the tower family has length 1 (rfl) | FROZEN (definitional) | propext, Quot.sound | A |
| closeBlocks_complete_repair | 92 | r ∈ reqs, violated, m ∈ repairFamily w r ⇒ [mark m] ∈ closeBlocks w | FROZEN | propext, Quot.sound | S |
| closeBlocks_complete_aug | 106 | r ∈ reqs, violated, c ∈ augFamily w r ⇒ [addView c] ∈ closeBlocks w | FROZEN | propext, Quot.sound | S |
| nextFamily_stop | 120 | quiescentB w ⇒ nextFamily ⟨w, close⟩ = [] | CONDITIONAL: quiescentB (that is the point) | propext, Quot.sound | S |
| towerBlock_eq | 158 | towerBlock (worldAt k) = blockEvents (k+1) | FROZEN | propext, Quot.sound | A |
| freshName_fresh_on_tower | 165 | freshName (worldAt k) ∉ (worldAt k).data | FROZEN (on the tower invariant) | propext, Quot.sound | S |
| freshName_not_fresh_generally | 176 | on the world with data [1], freshName = 1 ∈ [1] | VERIFIED_FINITE / REFUTED (refutes general freshness) | propext, Quot.sound | S |
| driver_reproduces_tower | 189 | ∀ k, towerGen k = histUpTo k | FROZEN | propext, Quot.sound | S |
| nextFamily_complete | 204 | nextFamily (genWorld k) = [towerBlock ...] (rfl) | FROZEN (definitional) | propext, Quot.sound | A |
| budget_replenishment_represented | 211 | (towerBlock w).head? = some (setBudget 1) (rfl) | FROZEN (definitional) | none | A |
| gen_growth | 217 | (genWorld k).w.data.length = k+1 | FROZEN | propext, Quot.sound | A |
| gen_three_quiescent | 227 | quiescentB (genWorld 3).w | VERIFIED_FINITE (k = 3, via worldAt_three_quiescent) | propext, Quot.sound | A |
| tower_driver_autonomy | 255 | six conjuncts: prefix compatibility; family = singleton; append equation; family length 1; block head is setBudget 1; strict carrier growth | FROZEN (four conjuncts rfl) | propext, Quot.sound | S |
| interp_describe | 348 | ∀ w e, interpStep kernelDesc w e = step w e | FROZEN | propext, Quot.sound | S |
| allDescs_length | 384 | allDescs has 64 entries | VERIFIED_FINITE | none | A |
| allDescs_complete | 386 | every ConstitutionDesc is in allDescs | FROZEN (64-way case split + decide) | propext | S |

Count check: 16 theorems, all in the artifact.

## 4. External and admitted assumptions

- The whole of `nextFamily`, `towerBlock`, `freshName`, `interpStep` is declared constitution. The docstrings say so each time.
- `Policy` is a field of `GWorld` but no event changes it: `Event` has no policy-setting constructor, and `towerGen` writes `.tower` into the pair at every stage by hand (line 156). "Admitted into the generative state" (docstring line 40–41) describes a field, not an admission event. The policy is represented in the weak sense of being a datum of a Lean structure that nothing in the kernel can write.
- `towerGen : Nat → List Event` is metatheoretic recursion; the module says so ("the recursion here is metatheory; no represented transition invokes the interpreter"). Finitude flag: `∀ k` in `driver_reproduces_tower` and `tower_driver_autonomy` quantifies over Lean's Nat; the system holds no unbounded run.
- `freshName` imports arithmetic and ordering (`length`, `List.range`, `omega`); the paper prices this.
- `ConstitutionDesc` carries six bits. Everything else about the kernel's semantics — the event grammar, `markApply`, `augApply`, the exact guard predicates `reqOkB`, `markOkB`, `augOkB`, `obstructedB`, `markApply`'s matching-by-value, budget decrement, the `notes` field — is hard-coded in `interpStep` itself. The descriptor selects which of five guards are consulted; it does not describe the guards. See §11.
- Library: `List.mem_flatMap`, `List.mem_filter`, `List.mem_map`, `List.mem_range`, `List.headD`, `List.head?`, `omega`.
- Unearned identity: none found. Unrestricted external universe: none. Unbounded function treated as internally available: `towerGen`, flagged and disclosed. Silently assumed observer: none. Unspecified correspondence: none. Cost function: none here. Admitted condition later described as forced: the freshness of `freshName` is proved only on the tower invariant and explicitly refuted in general (`freshName_not_fresh_generally`) — correctly scoped. Finite computation presented as universal: `gen_three_quiescent` is k = 3; the docstring says "concrete stage" and Horizon generalises it.

## 5. Derived consequences

`Horizon.lean` lifts `gen_three_quiescent` to every stage (`gen_quiescent`, `gen_wf`, `block_all_accepted`) through `driver_reproduces_tower`. `Initiality.lean` uses `interpStep`, `kernelDesc`, `allDescs` for the six load-bearing separations and `unique_compliant`. `InterpreterBoundary.lean` uses `interpStep`, `allDescs`, `genWorld`/`towerGen` for the diagonal argument. Map rows: "next-event source internalized as policy" PROVED (`driver_reproduces_tower`, `nextFamily_complete`); "kernel constitution represented as data" PROVED (`interp_describe`); "kernel constitution interprets itself absolutely" OPEN. Ledger CL-NC-EVENT-SOURCE, CL-NC-AUTONOMY, CL-NC-CONSTITUTION.

## 6. Counterexamples and limitations

- Countermodel: `freshName_not_fresh_generally` (the canonical numeral collides on an arbitrary world).
- Not proved: that `nextFamily` is the right or a unique interpreter; that any represented transition invokes it (level 4, stated not attained); lawfulness at every stage (proved in Horizon, not here); that `closeBlocks` is ever used by a driver (no `closeGen` exists; the `close` policy has completeness theorems but no generation theorem); that the policy field can be changed by any event; anything about an interpreter that interprets `interpStep` (the OPEN row).
- The precise content of `interp_describe`: for every world and event, the family interpreter run on the all-true descriptor returns the same world as `step`. It is a proof of extensional equality of two Lean functions, one of which is a parameterised copy of the other. It is a *verified self-description relative to `interpStep`*: the six-bit descriptor "kernelDesc" denotes `step` under the fixed interpreter. It is not: a coded interpreter in the represented world (no `World` field or `Event` carries a descriptor or a program); a denotational interpretation of the kernel in some independent semantics (the only semantics is `interpStep`'s own operational output); an absolute self-interpreter (no represented object evaluates `interpStep`, and `interpStep` is not an element of `allDescs`). The vocabulary the brief asks for, applied here: *represented transition* = `step w e`; *coded interpreter* = `interpStep d` (code in the metatheory, parameterised by a datum); *behavioural distinction* = the `*_load_bearing` theorems of Initiality (two descriptors differ on a probe); *denotational interpretation* = none in this module; *self-description* = `interp_describe`; *absolute self-interpreter* = not formulated, OPEN.

## 7. Axiom dependencies

All 16 within {propext, Quot.sound}; `budget_replenishment_represented` and `allDescs_length` use none; `allDescs_complete` uses propext only. Theorems exceeding the set: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 16 theorems in the artifact; all cited in the ledger (CL-NC-EVENT-SOURCE, CL-NC-AUTONOMY, CL-NC-CONSTITUTION) and in `paper/native_derivation_completion.md` §9–§11, §18; `paper/primitive_interpreter_boundary.md` cites `interp_describe`, `allDescs_complete`. No probe run; proofs read in full.

## 9. Related Python implementations

`code/derivation/completion.py`: `fresh_name`, `tower_block`, `aug_family`, `close_blocks`, `next_family`, `tower_gen`, `protocols_report` (reproduction and acceptance to 15 rounds), `all_descs`, `interp_step` (with the note that budget decrement saturates to match Lean `Nat`), `KERNEL_DESC`. Tests: `tests/test_completion.py::test_driver_reproduces_supplied_stream`, `test_tower_family_is_singleton_and_stop_is_empty`, `test_close_family_complete_and_tie_retained`, `test_interp_kernel_desc_matches_step`, `test_budget_saturation_matches_lean_nat`, `test_freshness_scoped_to_tower_invariant`.

## 10. Textbook placement proposal

- Prerequisites: the Represented kernel and its supplied stream `histUpTo`/`worldAt`; `Completion.augFamily`; the idea of a family of next events versus a chosen next event.
- Substantive: `nextFamily` and the two completeness theorems, `nextFamily_stop`, `driver_reproduces_tower`, `freshName_fresh_on_tower` with its refutation `freshName_not_fresh_generally`, `tower_driver_autonomy` (taught as a ladder with level 4 missing), `ConstitutionDesc`/`interpStep`/`interp_describe`, `allDescs_complete`.
- Auxiliary: `nextFamily_tower_singleton`, `towerBlock_eq`, `nextFamily_complete`, `budget_replenishment_represented`, `gen_growth`, `gen_three_quiescent`, `allDescs_length`.
- Lesson title: "Generating the stream from the state, and describing the kernel to itself — and the one thing that stays outside." The one question: what changes when the event source is computed from represented state rather than supplied, and what does `interp_describe` actually say?
- Omit: `nextFamily_complete` and `budget_replenishment_represented` as separate items (both `rfl`; fold into the discussion of `towerBlock`).

## 11. Interpretation findings

1. `interp_describe` / header line 19–22 "Stage V also represents the kernel constitution as data ... the kernel's own description executes to exactly the sealed step"; map row "kernel constitution | represented as data | PROVED". Lean: `interpStep kernelDesc w e = step w e` where `kernelDesc` is six Booleans and `interpStep` is a Lean function containing the complete kernel semantics with five optional guards. What is represented as data is a six-bit choice among 64 relaxations of one hard-coded machine; the event grammar, the laws, the guard predicates, the menu, the application functions and the `notes` field are not described by any datum. Classification: INTERPRETATION DEFECT (moderate): "the kernel constitution is represented as data" overreads a correct theorem. The paper partly concedes this ("the interpreter is constitution, not state"; "the family interpreter ... is not a member of the family"), and `primitive_interpreter_boundary.md` scopes "universal" to the 64-member class, but the phrase "constitution as data" survives in the header, the ledger title CL-NC-CONSTITUTION and the map row. A faithful reading: *a six-parameter family of relaxations of the kernel is represented as data, and the kernel is the all-guards-on member.*
2. `Policy` docstring (line 40–41) "The policy store: first-order data, admitted into the generative state." No event admits or changes a policy; `towerGen` hard-wires `.tower` at each stage; `GWorld.pol` is never read by `step`. Classification: INTERPRETATION DEFECT (mild): "admitted" suggests an admission event that does not exist. The paper's phrase "the policy is first-order data" is accurate; "admitted" is not.
3. `tower_driver_autonomy` docstring: nine levels, with (8) lawfulness "instance-verified here at stage 3; proved at every stage by Horizon". The theorem has no lawfulness conjunct; `pr11_correction_ledger.md` C6 records this and Horizon repairs it. Already corrected in the ledger; the docstring is accurate after the repair.
4. `driver_reproduces_tower` docstring "what entered PR #10 as a metatheoretic history producer is now computed, stage by stage, by the next-family interpreter from the replayed represented state". Faithful, with the stated caveat that the iteration itself and `nextFamily` remain metatheory. Note for the textbook: because `towerBlock` is built from `freshName w` and `towerGen` is defined to append `nextFamily`'s head, the reproduction theorem is an induction on a definitional unfolding plus `worldAt_growth`; its content is that `freshName (worldAt k) = k + 1`.
5. Vacuity: none found; all hypotheses satisfiable (`nextFamily_stop` at any quiescent world, e.g. `worldAt 3`).
