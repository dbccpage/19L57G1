# Audit: Minimality

| field | value |
|---|---|
| Path | lean4/Derivation/Minimality.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 647e56fee0f00f27 |
| Lines | 487 |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.Basic, Derivation.Inertia |
| Declarations | 1 structure (`Iso`), 15 def (incl. 3 `Iso`-valued defs `isoRefl`, `isoU1U0`), 26 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 22 lines; axioms seen: none (`deltaK_length`), propext (`cost1_insufficient*`, `markK_pairwise_noniso`), propext+Quot.sound (the rest). Not in artifact: `applyDelta_single`, `applyDelta_pair`, `validResponse_R2L`, `no_insts_no_separation` |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
Minimality answers Challenge 3 for reading L: what is the least augmentation that makes the two admitted data internally separable, and is it unique? All statements are relative to the declared candidate space (`Item` deltas) and the two declared cost measures (`mu1` = item count; `mu2` = item count, then new-form arity sum). It exhibits the four surviving two-item responses (unary mark on either datum, binary link, binary self-loop), proves each valid, proves that no delta of at most one item can be valid on any form-less instance-less regime, declares the implemented isomorphism relation `Iso` (two bijections on the admitted ranges preserving arities, instances, rules and sorted requirement pairs), proves the three tied classes pairwise non-isomorphic and the two marks isomorphic, and assembles the non-uniqueness theorem for `mu1`. It then exhibits the arity-indexed family of `k`-ary marks — valid, two items, pairwise non-isomorphic for distinct arities — and finally proves that under `mu2` every valid two-item response with new-form arity sum at most one yields a regime isomorphic to the unary mark.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `aritySum` | 15 | def | sum of arities of `newForm` items in a delta (second component of `mu2`) | ADMITTED (declared cost measure) |
| `U0`, `U1` | 38, 40 | def | unary mark on datum 0 / 1 over `R2L` | ADMITTED |
| `BL`, `BD` | 42, 44 | def | binary link `(0,[0,1])` / binary self-loop `(0,[0,0])` | ADMITTED |
| `deltaU0`, `deltaU1`, `deltaBL`, `deltaBD` | 60–63 | def | the four two-item deltas | ADMITTED |
| `sortPair` | 169 | def | order a pair ascending | ADMITTED |
| `Iso r s` | 176 | structure (Type-valued) | `dmap/dinv/fmap/finv : Nat → Nat`, two-sided inverse and bound on `List.range` of the admitted ranges, arity preserved, instances/rules in both directions, requirements via `sortPair` | ADMITTED (declared isomorphism; docstring: "Mirrors `code/derivation/iso.py`") |
| `isoRefl` | 199 | def | identity `Iso r r` when every requirement pair is sorted | ADMITTED |
| `swap01` | 223 | def | transposition of data 0, 1 | ADMITTED |
| `isoU1U0` | 227 | def | `Iso U1 U0` via `swap01`, all fields by `decide` | ADMITTED (data; VERIFIED_FINITE fields) |
| `markK k` | 297 | def | `⟨2,[k],[(0, replicate k 1)],[],[(0,1)]⟩`, the `k`-ary mark | ADMITTED |
| `deltaK k` | 300 | def | `[newForm k, newInst 0 (replicate k 1)]` | ADMITTED |

## 3. Theorems and lemmas
Convention used below: a concrete-regime fact proved by `decide` is VERIFIED_FINITE; a concrete-regime fact obtained by instantiating a general lemma is FROZEN (instance); a `¬`/`→ False` theorem refuting a candidate claim is REFUTED.

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `applyDelta_single` | 21 | `applyDelta r [a] = applyItem r a` | FROZEN | not in artifact | A |
| `applyDelta_pair` | 27 | `applyDelta r [a,b] = (applyItem r a).bind (applyItem · b)` | FROZEN | not in artifact | A |
| `U0_separable` | 46 | `separable U0 0 1`, witness `⟨0,[none]⟩` | VERIFIED_FINITE | propext, Quot.sound | S |
| `U1_separable` | 49 | `separable U1 0 1` | VERIFIED_FINITE | propext, Quot.sound | A |
| `BL_separable` | 52 | `separable BL 0 1`, witness `⟨0,[none, some 1]⟩` | VERIFIED_FINITE | propext, Quot.sound | S |
| `BD_separable` | 55 | `separable BD 0 1`, witness `⟨0,[none, some 0]⟩` | VERIFIED_FINITE | propext, Quot.sound | S |
| `validResponse_R2L` | 67 | on `R2L`, a delta that applies to `s` with `separable s 0 1` is a valid response (the only requirement is the target) | FROZEN (instance over `R2L`, general in `δ`, `s`) | not in artifact | A |
| `deltaU0_valid` … `deltaBD_valid` | 79–89 | each of the four deltas is a valid response on `R2L` to `(0,1)` | VERIFIED_FINITE (application by `decide`) | propext, Quot.sound | S |
| `no_insts_no_separation` | 94 | `s.insts = [] → separable s d d' → False` | CONDITIONAL: `insts = []` | not in artifact | A |
| `cost1_insufficient_general` | 102 | for any regime with `forms = []` and `insts = []`, any `i j`, any delta of length ≤ 1 is not a valid response | CONDITIONAL: `forms = []`, `insts = []` (general over the whole item grammar and all regimes of that shape) | propext | S |
| `cost1_insufficient` | 144 | instance at `R2L`, target `(0,1)` | FROZEN (instance) | propext | S |
| `cost1_insufficient_F` | 149 | instance at `R2F`, target `(1,2)` | FROZEN (instance) | propext | S |
| `deltaU0F_valid` | 155 | `[newForm 1, newInst 0 [1]]` is a valid response on `R2F` to `(1,2)` | VERIFIED_FINITE | propext, Quot.sound | S |
| `U0_not_iso_BL` | 250 | no `Iso U0 BL` (arity is an invariant) | REFUTED (over all `Iso` structures; symbolic proof, not `decide`) | propext, Quot.sound | S |
| `U0_not_iso_BD` | 259 | no `Iso U0 BD` | REFUTED | propext, Quot.sound | S |
| `BL_not_iso_BD` | 270 | no `Iso BL BD` (instance preservation would force `dmap 0 = dmap 1 = 0`, contradicting two-sided inverse) | REFUTED | propext, Quot.sound | S |
| `mu1_minimum_not_unique` | 284 | on `R2L` (reading L): `deltaU0` and `deltaBL` are valid, both of length 2, no delta of length ≤ 1 is valid, they produce `U0` and `BL`, and `Iso U0 BL → False` | REFUTED (refutes uniqueness of the `mu1` minimum, reading L, up to the declared `Iso`); components VERIFIED_FINITE + `cost1_insufficient` + `U0_not_iso_BL` | propext, Quot.sound | S |
| `deltaK_applies` | 303 | for `1 ≤ k`, `applyDelta R2L (deltaK k) = some (markK k)` | CONDITIONAL: `1 ≤ k` | propext, Quot.sound | A |
| `markK_separable` | 325 | for `1 ≤ k`, `separable (markK k) 0 1`, witness the all-holes `k`-slot context | CONDITIONAL: `1 ≤ k` | propext, Quot.sound | S |
| `deltaK_valid` | 346 | for `1 ≤ k`, `deltaK k` is a valid response on `R2L` | CONDITIONAL: `1 ≤ k` | propext, Quot.sound | S |
| `deltaK_length` | 351 | `(deltaK k).length = 2` (`rfl`) | FROZEN | none | A |
| `markK_pairwise_noniso` | 355 | `j ≠ k → Iso (markK j) (markK k) → False` (no `1 ≤` hypothesis) | REFUTED (general in `j`, `k`) | propext | S |
| `mu2_unique` | 371 | for any items `a b`, if `[a,b]` is a valid response on `R2L` to `(0,1)` and `aritySum [a,b] ≤ 1`, then `applyDelta R2L [a,b] = some s` with `Nonempty (Iso s U0)` | FROZEN (general over the item grammar; the hypotheses `hval`, `har` are the claim's scope: reading L, two items, `mu2` second component ≤ 1) | propext, Quot.sound | S |

## 4. External and admitted assumptions
- Declared cost measures `mu1` (length) and `mu2` (length, `aritySum`): declared, not derived; the paper says uniqueness is "measure-relative" and names the measure on every statement. Cost function without justification: the measures are admitted by declaration (paper 3.7); no Lean theorem justifies the choice. Flagged as ADMITTED policy, consistent with the paper's tagging.
- `Iso` is Type-valued data with total `Nat → Nat` maps constrained only on `List.range r.data` / `List.range r.forms.length`. These are metatheoretic relabellings. Its docstring "Mirrors `code/derivation/iso.py`" is a declared correspondence (the Python relation is the computational side, CL-ISO-SOUND); no proof relates them (none possible).
- Recurring hypotheses: `forms = []`, `insts = []` (the Challenge 3 base shape), `1 ≤ k` (arity at least one), `aritySum ≤ 1`.
- Library lemmas: `List.eq_of_mem_replicate`, `List.mem_replicate`, `List.map_replicate`, `Option.some.inj`, `omega`, `decide` on `Regime`/`Inst` equality. Core only.
- Universe parameters: none.
- Unearned identity: none. Unrestricted external universe: none. Unbounded function treated as internal: the `Nat → Nat` fields of `Iso` (metatheory; not read as system content). Silent observer: none (contexts are explicit witnesses). Unspecified correspondence between presentations: the Lean `Iso` vs Python `isomorphic` is declared, not proved (ledger CL-ISO-SOUND carries the Python side). Admitted condition later described as forced: none found — the paper writes "measure-relative" and "up to the implemented isomorphism". Finite computation presented as universal: none found; the `decide` facts are instance facts and the paper's grammar-wide claims rest on `cost1_insufficient_general`, `deltaK_*`, `markK_pairwise_noniso`, `mu2_unique`, which are general.

## 5. Derived consequences
MinimalityF reuses `aritySum`, `Iso`, `isoRefl`, `applyDelta_pair`, `no_insts_no_separation` and mirrors `mu2_unique` for reading F. `Iso` is the relation transported by IsoCollapse, IsoCanon, IsoBridge, FormRenaming, FormTransport; `sortPair` by IsoCanon/IsoBridge. RuleBridge reuses `aritySum`. The ledger rows CL-3-COST1-IMPOSSIBLE, CL-3-MIN-TWO, CL-3-NONUNIQUE-MU1, CL-3-TIE-CLASSES, CL-3-INFINITE-TIES, CL-3-UNIQUE-MU2-L and `paper/representative_selection.md` (layer 1 table; "the obstruction bites within a tie class and not across") rest on this module.

## 6. Counterexamples and limitations
- `mu1_minimum_not_unique` refutes "the minimum corrective augmentation is unique" for `mu1`, reading L, up to the declared `Iso`. Witnesses `U0` (unary mark) and `BL` (binary link). It says nothing about reading F (the F count 5 is engine enumeration; ledger says so since 2026-08-18).
- `U0_not_iso_BL`, `U0_not_iso_BD`, `BL_not_iso_BD`, `markK_pairwise_noniso` refute isomorphisms between the named concrete regimes.
- Not proved here: that the three reading-L classes are ALL the `mu1` minima within `max_arity 2` (bounded enumeration, CL-3-TIE-CLASSES); any reading-F class distinctness; that `markK k` is `wf` (true for `k ≥ 1`, unstated); a single theorem "the `mu2` minimum is unique up to iso" — the paper assembles it from `cost1_insufficient` + `deltaU0_valid` + `mu2_unique` + the remark that no valid `(2,0)` delta exists (paper 7.4), and the last step is prose, though it is also a by-product of `mu2_unique`'s proof (`c = 1` is forced).
- `mu2_unique` is stated for two-item deltas only; it does not quantify over longer deltas with smaller `aritySum` (irrelevant for a lexicographic measure, but unstated).

## 7. Axiom dependencies
All 22 artifact lines within {propext, Quot.sound}. The four helpers not in the artifact were probed (`#print axioms`, probe2.lean, exit 0): `applyDelta_single` propext; `applyDelta_pair` propext, Quot.sound; `validResponse_R2L` propext; `no_insts_no_separation` propext; the def `isoU1U0` propext, Quot.sound. None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). 22 theorems in the artifact (root lines 98–119). Paper 7.2–7.4, 10.6, `representative_selection.md` and the six CL-3-* ledger rows cite them. Probe: `lake env lean /tmp/claude-0/-home-claude/47be43b5-43cb-5429-bc31-b53a81ca595d/scratchpad/probes/A/probe2.lean` (exit 0) — axioms of the four un-artifacted helpers and of `isoU1U0` as listed in section 7.

## 9. Related Python implementations
`code/derivation/candidates.py` (`mu1`, `mu2`, `iter_cost1_items`, `iter_cost2_deltas`, `min_responses`, `response_valid_naive`); `code/derivation/iso.py` (`isomorphic`, `canonical`, `rename`); `code/derivation/engine.py` Challenge 3. Tests: `tests/test_candidates.py::test_c3_cost1_all_fail_and_min_is_two`, `::test_c3_mu2_minimum_is_unary_mark`, `tests/test_iso.py::test_mark_variants_are_isomorphic`, `::test_direction_relative_to_requirement_matters`, `tests/test_independent_oracles.py::test_c3_mu2_minimum_is_exactly_the_two_unary_marks`, `tests/test_observe.py::test_unary_mark_separates_and_witness`, `tests/test_engine.py::test_challenge3_reading_f_has_five_classes`.

## 10. Textbook placement proposal
- Prerequisites: Basic, Inertia (`collapsed_of_no_insts`), the declared measures `mu1`/`mu2`, and the notion of an isomorphism of regimes.
- Substantive: `cost1_insufficient_general`, the four witnesses and their validity, `Iso`, the three non-iso theorems, `mu1_minimum_not_unique`, the `markK` family (`deltaK_valid`, `markK_pairwise_noniso`), `mu2_unique`. Auxiliary: `applyDelta_single/pair`, `validResponse_R2L`, `no_insts_no_separation`, `deltaK_applies`, `deltaK_length`, `isoRefl`, `swap01`.
- Lesson title: "Two items, three answers, one measure". Question: is the cheapest repair that separates `<a>` from `<ab>` unique — and unique relative to what?
- Omit: `U1_separable`/`deltaU1_valid` as displayed results (mention as the swapped twin); `applyDelta_single/pair`.

## 11. Interpretation findings
- `mu1_minimum_not_unique` scope. Paper 7.3 and ledger CL-3-NONUNIQUE-MU1: "reading L", "up to the implemented isomorphism", "measure mu1". Lean: over `R2L`, deltas `deltaU0`/`deltaBL`, non-iso under the declared `Iso`. Match; the reading-F non-uniqueness is explicitly bounded enumeration. None found (scope repaired 2026-08-18 per the ledger).
- `deltaK` family. Paper 7.3 / ledger CL-3-INFINITE-TIES: "**the mu1 tie class is countably infinite**" (reading L). Lean: for every Lean `k ≥ 1`, `deltaK k` is a valid two-item response and `markK j ≇ markK k` for `j ≠ k`. The family is indexed by Lean's `Nat`; "countably infinite" is a metatheoretic statement about the candidate grammar (`newForm (arity : Nat)` is unbounded by declaration), not an internal totality of the system. Finitude flag: the prose should be read as "unbounded by arity, hence no finite enumeration is complete", which the paper adds in the next sentence. INTERPRETATION DEFECT (minor, finitude wording: "countably infinite" attributes a completed infinity to a family the system never possesses; the Lean quantifier is metatheory).
- Which proofs are `decide` over concrete regimes: `U0/U1/BL/BD_separable`, `deltaU0/U1/BL/BD_valid` (application part), `deltaU0F_valid`, the regime equalities inside `mu1_minimum_not_unique`, all fields of `isoU1U0`, and the side conditions of `isoRefl` uses. General (symbolic) proofs: `cost1_insufficient_general`, `U0_not_iso_*`, `BL_not_iso_BD`, `deltaK_applies`, `markK_separable`, `markK_pairwise_noniso`, `mu2_unique`. The paper's "[theorem] … absolute over the grammar" tags attach only to the general ones; the `[bounded theorem]` class-count table rests on Python. No mismatch found.
- `mu2_unique`. Paper 7.4: "the mu2-minimum is unique up to isomorphism: mu2 = (2,1)" — assembled from the theorem plus the cost floor plus "the absence of valid (2,0) deltas". The last conjunct is not a named theorem; it is a prose remark (true, and implicit in `mu2_unique`'s case analysis). INTERPRETATION DEFECT (minor: an unnamed lemma in the prose chain).
- `markK_pairwise_noniso` holds also for `k = 0` or `j = 0`, where `markK 0` is not well-formed and not a response; the paper restricts to `k ≥ 1` so no overreach. Noted only.
- Vacuity: hypotheses of `mu2_unique` satisfiable (`deltaU0`); `cost1_insufficient_general` satisfiable (`R2L`); `Iso U0 BL → False` is not vacuous because `Iso` is inhabited in general (`isoRefl`).
