# Audit: Compression

| field | value |
|---|---|
| Path | lean4/Derivation/Compression.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 61dae37d53399ef4 |
| Lines | 787 |
| Imported by root `Derivation.lean` | yes (line 47) |
| Imports | Derivation.PrimitiveCore |
| Declarations | 14 def, 38 theorem (inventory also lists 1 `class`; no `class` declaration exists in the source — the docstring word "class" was scanned) |
| Axiom reports in `artifacts/lean_axioms.txt` | 22 lines; axioms seen: none / propext / Quot.sound / propext, Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

Presentation compression relative to a declared target. A represented finite domain is a list `D : List Nat`; a question family is a list `Q : List (Nat → Nat)` (represented data, not a view from nowhere); a presentation is `p : Nat → Nat`. The module proves, each scoped to `D` and `Q`: a question factors through a presentation on `D` iff the presentation's fibres over `D` are question-constant, with the factoring map unique on the image of `D` and not off it; the signature quotient `pQ D Q`, built by first-match selection with no choice principle, is exact, adequate and factors through every adequate presentation ("coarsest", in that sense only); a descent failure is always witnessed by an explicit separating question; enlarging the family only refines, and a class splits exactly when a new separator crosses an old agreement; adequacy for every family is injectivity on `D`, so there is no absolute compression; duplicating the family or appending a digest of its answers separates nothing, so a genuine split needs a question that is not signature-determined; refinement is not unique and equal-length refinements tie; and the class count is a strictly monotone `Nat` measure bounded by `|D|`, so any strictly refining chain over a nonempty domain has fewer than `|D|` steps. No observer in the `DiffObs` sense appears here; the connection to observers is made in `ObsDescent` (dictionary section).

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| sigList | 66 | def | `Q.map (fun q => q x)` | ADMITTED |
| SigEq | 71 | def | `∀ q ∈ Q, q x = q x'` | ADMITTED |
| Adequate | 95 | def | merged points of `D` agree on every declared question | ADMITTED |
| FiberConstant | 100 | def | fibres of `p` over `D` are `q`-constant | ADMITTED |
| FactorsOn | 104 | def | `∃ g, ∀ x ∈ D, g (p x) = q x` | ADMITTED |
| pick | 110 | def | first element of `D` satisfying a Boolean test | ADMITTED (replaces library search) |
| pQ | 223 | def | first element of `D` with the same signature; `0` off `D` | ADMITTED |
| SplitsAt | 345 | def | some `x' ∈ D` agrees with `x` on `Q` and not on `Q'` | ADMITTED |
| ind | 447 | def | indicator question of a point | ADMITTED |
| memB | 519 | def | Boolean membership for signature lists | ADMITTED |
| dedupL | 549 | def | deduplication keeping last occurrences | ADMITTED |
| classCount | 584 | def | `(dedupL (D.map (sigList Q))).length` | ADMITTED (the declared measure) |
| StrictRefine | 732 | def | subfamily plus some split on `D` | ADMITTED (declared step relation) |
| StrictChain | 737 | def | consecutive pairs strictly refine | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| sigEq_iff_sigList | 75 | `SigEq Q x x' ↔ sigList Q x = sigList Q x'` | FROZEN | none | A |
| pick_cons | 115 | unfolding equation (rfl) | FROZEN | not in artifact | A |
| pick_mem | 118 | `pick D P = some r → r ∈ D` | FROZEN | not in artifact | A |
| pick_holds | 134 | `pick D P = some r → P r = true` | FROZEN | not in artifact | A |
| pick_some_of_mem | 151 | a member satisfying `P` guarantees `pick` finds something | FROZEN | not in artifact | A |
| factors_iff_fiberConstant | 171 | `FactorsOn D p q ↔ FiberConstant D p q` (factoring map by first match) | FROZEN | Quot.sound | S |
| factor_unique_on_image | 192 | two factoring maps agree on `p '' D` | FROZEN | none | S |
| factor_not_unique_off_image | 200 | witness `D = [0]`, `g = id`, `g' 5 = 6`: distinct factoring maps | REFUTED (of off-image uniqueness) | none | S |
| pQ_spec | 229 | on `D`, `pQ D Q x ∈ D` and carries `x`'s signature | FROZEN | not in artifact | A |
| pQ_exact | 248 | on `D`, `pQ D Q x = pQ D Q x' ↔ SigEq Q x x'` | FROZEN | Quot.sound | S |
| pQ_adequate | 267 | `Adequate D Q (pQ D Q)` | FROZEN | Quot.sound | S |
| pQ_coarsest | 275 | `Adequate D Q p → FactorsOn D p (pQ D Q)` | CONDITIONAL: Adequate D Q p | Quot.sound | S |
| pQ_unique_on_image | 286 | instance of `factor_unique_on_image` (the `Adequate` hypothesis `_hp` is unused) | FROZEN | none | A |
| sigEq_decompose | 298 | disagreement with `q :: T` is head disagreement or tail disagreement (by `decide` on the head) | FROZEN | not in artifact | A |
| exists_separator_of_not_sigEq | 312 | `¬ SigEq Q x x' → ∃ q ∈ Q, q x ≠ q x'` (list recursion) | FROZEN | not in artifact | A |
| descent_witness | 328 | merged points of `D` that disagree on `Q` have a declared separator that is not fibre-constant for `p` | CONDITIONAL: p x = p x', ¬ SigEq Q x x' | none | S |
| enlarge_refines | 338 | `Q ⊆ Q'` ⇒ `SigEq Q' → SigEq Q` | FROZEN | none | S |
| splits_iff_new_separator | 353 | `SplitsAt D Q Q' x ↔ ∃ x' ∈ D, SigEq Q x x' ∧ ∃ q' ∈ Q', q' x ≠ q' x'` (the `Q ⊆ Q'` hypothesis `_hsub` is unused) | FROZEN | none | S |
| absolute_adequacy_iff_injective | 375 | `(∀ Q, Adequate D Q p) ↔ p` injective on `D` (forward by an indicator question) | FROZEN | none | S |
| dup_no_refine | 398 | `SigEq (Q ++ Q) ↔ SigEq Q` | FROZEN | propext | S |
| postcompose_no_refine | 410 | appending `f ∘ sigList Q` separates nothing new | FROZEN | propext | S |
| refine_requires_separator | 432 | a split needs some `q' ∈ Q'` that is not a function of the old signature | CONDITIONAL: SplitsAt D Q Q' x | none | S |
| refinement_not_unique | 455 | on `[0,1,2]` from the empty family, `[ind 0]` and `[ind 1]` both split and induce different agreements | REFUTED (of unique refinement) | none | S |
| refinement_tie | 487 | the same two enlargements have equal length and differ | REFUTED (of a unique minimum-length refinement) | none | S |
| memB_cons | 523 | unfolding (rfl) | FROZEN | not in artifact | A |
| memB_iff | 526 | `memB s l = true ↔ s ∈ l` | FROZEN | not in artifact | A |
| dedupL_cons | 553 | unfolding (rfl) | FROZEN | not in artifact | A |
| length_dedupL_le | 557 | `(dedupL l).length ≤ l.length` | FROZEN | not in artifact | A |
| dedupL_ne_nil | 567 | nonempty input gives nonempty output | FROZEN | not in artifact | A |
| memG_of_memF | 590 | repeated fine head-value forces repeated coarse head-value under determination | FROZEN | not in artifact | A |
| count_le_of_determines | 602 | determination ⇒ no more distinct coarse values than fine | FROZEN | not in artifact | A |
| count_lt_of_split | 631 | determination plus one merged-but-fine-distinct pair ⇒ strictly fewer | FROZEN | not in artifact | A |
| refine_bounded | 693 | `classCount D Q ≤ D.length` | FROZEN | propext, Quot.sound | S |
| classCount_pos | 701 | `D ≠ [] → 1 ≤ classCount D Q` | CONDITIONAL: D ≠ [] | none | S |
| strict_split_increases | 715 | `Q ⊆ Q'`, `x ∈ D`, `SplitsAt D Q Q' x` ⇒ `classCount D Q < classCount D Q'` | CONDITIONAL: subfamily and a split | propext, Quot.sound | S |
| chain_count | 745 | along a strict chain, head count + steps ≤ `D.length` | FROZEN | not in artifact | A |
| chain_bounded | 766 | `D ≠ []` ⇒ every strict chain has length ≤ `D.length` | CONDITIONAL: D ≠ [] | propext, Quot.sound | S |
| strict_steps_lt | 780 | `D ≠ []` ⇒ steps of a strict chain `< D.length` | CONDITIONAL: D ≠ [] | propext, Quot.sound | S |

Count check: 38 theorems; 22 in the artifact; 16 helpers not.

## 4. External and admitted assumptions

- No structures are imported for use; `PrimitiveCore` is imported but no `PrimitiveCore` name is used in this file (checked by reading: the import is for placement in the build order). The domain, family and presentation are parameters of every theorem.
- Library doing real work: `DecidableEq Nat` through `decide (p z = y)` and `decide (sigList Q z = sigList Q x)` (list equality decidable), `Option.getD`, `List.mem_map`, `List.mem_append`, `List.mem_cons_self`, `omega`, `simp` (once, for `length_map`). Declared in the header ("the decidability apparatus of the metalanguage").
- `Q : List (Nat → Nat)` and `p : Nat → Nat` are Lean functions on an unbounded type. Finitude flag: the module's own framing restricts every claim to membership in the finite list `D`, so the functions are evaluated only on a represented finite set — except in `absolute_adequacy_iff_injective`, whose left side quantifies over every Lean list of every Lean function (see §11). Unearned identity: none. Unrestricted external universe: none beyond `Nat → Nat`. Unbounded function treated as internally available: see the flag just given. Silently assumed observer: none; no observer appears. Unspecified correspondence between presentations: none (factoring maps are explicit). Cost function: `refinement_tie` uses family length `Q1.length` as "cost" with no justification beyond declaration (the docstring says "equal-cost"). Admitted condition later described as forced: none. Finite computation presented as universal: the two countermodels are explicit finite witnesses and are presented as such.
- Idle hypotheses: `splits_iff_new_separator` carries `_hsub` and `pQ_unique_on_image` carries `_hp`, neither used in the proof; the statements hold without them. Not a defect (the hypotheses record the intended setting), but a textbook should not list them as needed.

## 5. Derived consequences

Imported by `ClosureSymmetry`, `ContactKernel`, `ObsDescent`, `PresentationRelativity`, `ResidualClosure` (grep for `Compression.`/`open Compression`). In `ObsDescent`, `factors_iff_fiberConstant`, `FiberConstant`, `FactorsOn`, `SigEq` are the Compression side of the dictionary. Ledger CL-PD2-COMPRESSION cites all 22 artifact names; CL-PD2-CONTACT-DICTIONARY cites `factor_unique_on_image` and `factor_not_unique_off_image`.

## 6. Counterexamples and limitations

- `factor_not_unique_off_image` (witness `D = [0]`): refutes uniqueness of factoring maps off the image.
- `refinement_not_unique`, `refinement_tie` (witness `D = [0,1,2]`, `Q = []`, `Q1 = [ind 0]`, `Q2 = [ind 1]`): refute a unique or unique-minimum refinement; hence no endogenous selection of "the" next question.
- Not proved: anything off `D`; anything for a family not given as a list; that the class-count bound terminates any process the system runs (the chain bound is a statement about Lean lists of families under the declared `StrictRefine`; the docstring of `chain_bounded` says "nothing is claimed for other step relations"); that a split is "evidential" in any sense beyond `refine_requires_separator`'s literal content (see §11); the ledger's "exhaustive within declared bounds n ≤ 3, m ≤ 3, |Q| ≤ 2" is the Python computation's scope, not a Lean statement.

## 7. Axiom dependencies

All 22 artifact lines within {propext, Quot.sound}; 13 of them use none. Theorems exceeding the set: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). 22 of 38 theorems in the artifact, the rest helpers; the ledger cites the 22. No probe run; proofs read in full, including the two list inductions `count_le_of_determines` and `count_lt_of_split` on which the chain bound rests (both case-split on `memB` of the head value and use `memG_of_memF`; checked).

## 9. Related Python implementations

`code/derivation/compression.py`: `sig_list`, `sig_eq`, `adequate`, `fiber_constant`, `factors_on`, `valid_factor_maps`, `first_with_sig`, `p_quotient`, `injective_on`, `splits_at`, `sig_determined`, `digests`, `class_count`, and the exhaustive checkers `factorization_iff_exhaustive`, `quotient_exact/adequate/coarsest_exhaustive`, `descent_witnessed_exhaustive`, `enlarge_refines_exhaustive`, `split_characterization_exhaustive`, `absolute_adequacy_iff_exhaustive`, `dup_no_refine_exhaustive`, `digest_no_refine_exhaustive`, `separator_required_exhaustive`, `class_bound_exhaustive`, `class_pos_exhaustive`, `strict_split_increases_exhaustive`, `off_image_countermodel`, `countermodel_instances`. Tests: `tests/test_compression.py` (20 tests, including `test_bounds_declared`, the `*_exhaustive_small` set and `test_runner_byte_stable`).

## 10. Textbook placement proposal

- Prerequisites: lists as represented finite domains; "presentation" as a map; the difference between a statement on `D` and a statement everywhere; first-match selection as the choice-free constructor.
- Substantive: `factors_iff_fiberConstant` with `factor_unique_on_image`/`factor_not_unique_off_image`; `pQ_exact`, `pQ_coarsest` (as "coarsest means: factors through every adequate presentation"); `descent_witness`; `splits_iff_new_separator`; `absolute_adequacy_iff_injective`; `postcompose_no_refine` + `refine_requires_separator`; `refinement_not_unique`; `strict_split_increases` + `strict_steps_lt`.
- Auxiliary: `sigEq_iff_sigList`, the `pick_*`, `memB_*`, `dedupL_*`, `memG_of_memF`, `count_*`, `chain_count`, `pQ_spec`, `pQ_unique_on_image`, `pQ_adequate`, `enlarge_refines`, `dup_no_refine`, `refinement_tie`, `classCount_pos`, `refine_bounded`.
- Lesson title: "Compressing a presentation against a declared question list: exactness, witnesses, and the class-count bound." The one question: relative to which questions is a merge of two points harmless, and what shows up when it is not?
- Omit: `refinement_tie` as a separate theorem (same witnesses as `refinement_not_unique`, plus a length equation); the `memB`/`dedupL` apparatus (explain `classCount` as "number of distinct signatures" inline).

## 11. Interpretation findings

1. Docstrings of `refine_requires_separator` (lines 427–431) and header F: "Replay is evidential only when it carries a new represented separator." Lean: if `SplitsAt D Q Q' x` then some `q' ∈ Q'` is not of the form `f ∘ sigList Q`. "Replay" and "evidential" have no Lean referent in this module; the theorem is about signature-determination of a question. Classification: INTERPRETATION DEFECT (mild): the gloss imports vocabulary (replay, evidence, hash, record) from elsewhere in the programme; the theorem supports only "a split needs a non-signature-determined question".
2. Header E and docstring of `absolute_adequacy_iff_injective`: "the family, its source, and its revisions are represented data, never a view from nowhere". The theorem's left side `∀ Q : List (Nat → Nat), Adequate D Q p` quantifies over every Lean family, which is exactly a metatheoretic totality; the theorem uses it to show absolute adequacy collapses to injectivity. Finitude flag only: the quantifier is metatheory and the module uses it to refute, not to assert, an absolute notion. Classification: none as a defect; recorded under the finitude rule.
3. `pQ_coarsest` named "coarsest": Lean proves `FactorsOn D p (pQ D Q)` for every adequate `p`, i.e. `pQ` is at least as coarse as every adequate presentation on `D`. It does not prove `pQ` is the unique such presentation up to image-isomorphism (there is no isomorphism statement). The docstring says "this is the sense — and the only sense claimed". Classification: none.
4. `refinement_tie` docstring "equal-cost refinements tie": cost is `List.length` of the family, declared, not derived. Classification: INTERPRETATION DEFECT (mild): "cost" names a measure the module never justifies; the theorem is "two one-question enlargements split the same class and differ".
5. Vacuity: no theorem has unsatisfiable hypotheses (`D ≠ []` and the split hypotheses are all realised by the countermodels). `splits_iff_new_separator` and `pQ_unique_on_image` carry unused hypotheses (noted in §4); their conclusions are not trivial.
