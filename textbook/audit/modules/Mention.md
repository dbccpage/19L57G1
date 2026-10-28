# Audit: Mention

| field | value |
|---|---|
| Path | lean4/Derivation/Mention.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 68722b804252dd95 |
| Lines | 199 |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.Basic |
| Declarations | 7 theorem (no definitions) |
| Axiom reports in `artifacts/lean_axioms.txt` | 7 lines; axioms seen: none (`not_mem_of_arg_out_of_range`), propext (`exists_out_of_range_slot`, `getD_append_left`, `collapsed_fresh_form`), propext+Quot.sound (the other three) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
Mention proves the three structural irrelevance facts (residuals R1, R2, R3) that license the cost-2 enumeration to prune, and it shows they are one argument. The mention lemma (R3): every well-formed context has a hole, so a plugged instance always mentions its datum; hence appending instances that mention neither target datum leaves the collapse of that pair exactly as it was. The corollaries (R1, R2): admitting a fresh datum that no instance mentions, or a fresh form that no instance uses and no rule names, enlarges the space of well-formed contexts, but every new context reaches outside the regime, so both plugs fail derivability for the same reason and nothing new is separated. The hypotheses of R1 and R2 are conjuncts of `Regime.wf`. The module states in its closing paragraph what it does not say: nothing here says a fresh datum or form is useless, only that the unmentioning part of a candidate cannot contribute.

## 2. Definitions and structures
None.

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `mem_plug_of_hole` | 40 | if `none ∈ c.slots` then `d ∈ (plug c d).2` | FROZEN | propext, Quot.sound | A |
| `not_mem_of_arg_out_of_range` | 47 | if every instance argument of `r` is `< r.data`, an instance with an argument `≥ r.data` is not in `r.insts` | CONDITIONAL: instance-argument conjunct of `wf` | none | A |
| `exists_out_of_range_slot` | 56 | a slot list not everywhere `slotOk n` has some `some x` with `¬ x < n` (constructive witness by induction) | FROZEN | propext | A |
| `collapsed_append_unmentioning` | 88 | **R3**: if no instance in `new` mentions `d` or `d'` in its arguments, `collapsed {r with insts := r.insts ++ new} d d' ↔ collapsed r d d'` | CONDITIONAL: `hd`, `hd'` (non-mention) | propext, Quot.sound | S |
| `collapsed_fresh_datum` | 124 | **R1**: if every instance argument is `< r.data`, `collapsed {r with data := r.data+1} d d' ↔ collapsed r d d'` | CONDITIONAL: instance-argument conjunct of `wf` | propext, Quot.sound | S |
| `getD_append_left` | 157 | `(l ++ m).getD i dflt = l.getD i dflt` for `i < l.length` | FROZEN | propext | A |
| `collapsed_fresh_form` | 168 | **R2**: if every instance form and every rule is `< r.forms.length`, `collapsed {r with forms := r.forms ++ [k]} d d' ↔ collapsed r d d'` for any arity `k` | CONDITIONAL: instance-form and rule conjuncts of `wf` | propext | S |

## 4. External and admitted assumptions
- Recurring hypotheses: conjuncts of `Regime.wf` (instance arguments below `data`; instance forms and rules below `forms.length`); for R3 the non-mention of the two target data by the appended instances.
- The appended instances in R3 are not required to be well-formed, and `d`, `d'` are not required to be `< r.data`; the statements are wider than the pruning needs.
- Library lemmas: `List.mem_map`, `List.mem_append`, `List.mem_cons`, `List.getElem?_append_left`, `Nat.lt_succ_of_lt`. Core only; the docstring notes `by_contra` was avoided because it is Mathlib.
- Universe parameters: `getD_append_left` is polymorphic in `α : Type`.
- `Nat → X` as data: none. Unearned identity / unrestricted universe / unbounded internal function / silent observer / presentation correspondence / cost / admitted-as-forced / finite-as-universal: none found.

## 5. Derived consequences
`collapsed_append_unmentioning` is used by MinimalityF (`genesis_mark_not_separable`: the mark on the genesis datum mentions neither required datum, so the pair stays collapsed), which closes the one extra case of `mu2_unique_F`. The other six theorems are used by no other Lean module. The ledger (CL-PRUNE-STRUCTURAL) cites all seven; the paper's residual register (rows R1–R3) and section 8.3 cite the three main ones.

## 6. Counterexamples and limitations
No countermodels. Not proved here: (i) the delta-level statement "the pruned cost-2 enumeration contains every minimum" — the ledger says explicitly this stays a bounded computational result; (ii) the bridge from an instance-only delta applied by `applyDelta` (which uses `insertNew`, i.e. dedup) to the `insts ++ new` form the lemma takes (collapse depends only on membership, so Ext's `collapsed_ext` would close this, but no lemma states it); (iii) any statement about responses, as opposed to collapse of existing pairs. The module's final paragraph says the same.

## 7. Axiom dependencies
All within {propext, Quot.sound}; `not_mem_of_arg_out_of_range` axiom-free. None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All seven in the artifact. Paper 8.3, 12 (register rows R1–R3) and ledger CL-PRUNE-STRUCTURAL, CL-3-UNIQUE-MU2-F cite them. No extra probe.

## 9. Related Python implementations
`code/derivation/candidates.py::_mentions`, `iter_cost2_deltas` (the pruned enumeration), `iter_full_deltas`, `response_valid_fast`/`response_valid_naive`. Tests: `tests/test_candidates.py::test_pruned_cost2_contains_every_valid_full_delta`, `::test_new_datum_alone_never_separates`, `::test_fast_equals_naive_on_full_space`.

## 10. Textbook placement proposal
- Prerequisites: Basic (`wfCtx` with its hole clause, `plug`, `derivable`, `collapsed`).
- Substantive: `collapsed_append_unmentioning`, `collapsed_fresh_datum`, `collapsed_fresh_form`, and the one-sentence reason (`mem_plug_of_hole`). Auxiliary: `not_mem_of_arg_out_of_range`, `exists_out_of_range_slot`, `getD_append_left`.
- Lesson title: "A context that reaches outside the regime separates nothing". Question: which parts of a candidate augmentation can be discarded before checking whether it separates the target pair?
- Omit: the three list helpers.

## 11. Interpretation findings
- Paper 12, register rows R1/R2 (lines 782–783): "Unreferenced fresh **data** never affect a minimum response … `collapsed_fresh_datum` (Lean)". Lean: the collapse of an already-existing pair is unchanged by adding a fresh unmentioned datum. The step from "collapse unchanged" to "never affect a minimum response" needs a delta-level argument (that the sub-delta without the fresh item still applies and is valid), which is in Python only; ledger CL-PRUNE-STRUCTURAL's "Scope, exactly" and paper 8.3 ("What that does NOT do is promote CL-PRUNE-STRUCTURAL to a theorem") state this. INTERPRETATION DEFECT (minor: register-row headline reads delta-level; the Lean is collapse-level; scope stated elsewhere).
- Ledger CL-PRUNE-STRUCTURAL: "an instance-only delta changes the target pair's separability only if some instance mentions a target datum". Lean R3 appends a raw list `new`; an `applyDelta` of `newInst` items yields `insertNew`-deduplicated instances. The two agree in membership, hence in collapse (Ext), but that connecting lemma is not written. INTERPRETATION DEFECT (minor; the gap is closable from Ext).
- Vacuity check: all hypotheses satisfiable (any `wf` regime); conclusions are genuine iffs, non-trivial because contexts do change on both sides.
- Finitude: none found.
