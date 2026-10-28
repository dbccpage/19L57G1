# Audit: ObsDescent

| field | value |
|---|---|
| Path | lean4/Derivation/ObsDescent.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 33b0ec0df9e7fe5a |
| Lines | 539 |
| Imported by root `Derivation.lean` | yes (line 39) |
| Imports | Derivation.DiffInterface, Derivation.Compression |
| Declarations | 8 def (2 of them `DiffObs` instances), 37 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 37 lines; axioms seen: none / propext / Quot.sound / propext, Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The sealed observer interface `DiffInterface.DiffObs X R` packages a typed difference map `delta`, a zero predicate on difference values, and the three laws making `ZeroRel` an equivalence; the sealed quotient `ObsQuotient O` and its soundness half already exist. This module, written at the 2026-08-13 contact collision, completes the descent theory that quotient earns and nothing more: exactness of the quotient and surjectivity of the projection; a view descends to the quotient iff it is constant on zero-classes, uniquely, and one zero-pair with distinct values blocks it; the same three facts for the difference map in both arguments; pairing splits componentwise, giving the flagship shape (a view descends alone, its pairing with a blocked component does not); descent into a further quotient of the value side reduces to the equality layer at `Quotient.mk S ∘ f`. Two concrete observers are added: the integer subtraction observer, whose five one-line arithmetic lemmas subsume the arriving development's "integer tail", and the all-zero observer on `Bool`, a countermodel where the declared zero relation identifies everything while the difference map still separates. The final section is a dictionary: for a kernel observer on `Nat`, global quotient descent is exactly the target-relative factorization of `Compression` quantified over every represented domain, and the `∀ D` is not removable.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| ClassConstant | 104 | def | `∀ x y, ZeroRel O x y → f x = f y` | ADMITTED |
| descend | 108 | def | `Quotient.lift f hf : ObsQuotient O → Y` | ADMITTED |
| DeltaConstant | 151 | def | `delta` constant on zero-classes in both arguments | ADMITTED |
| deltaDescend | 156 | def | `Quotient.lift₂ O.delta _` | ADMITTED |
| coarsenMap | 261 | def | transport `Quotient S → Quotient T` along `S ⊆ T` | ADMITTED |
| pairSetoid | 318 | def | product setoid on `Y × Z` | ADMITTED |
| intDiffObs | 359 | def (DiffObs Int Int) | `delta a b := a − b`, `Zero v := v = 0`; the three laws proved by `omega` | ADMITTED instance; laws PROVED by arithmetic, not by `kernelObs` — **not a kernel observer** |
| collapseAllObs | 437 | def (DiffObs Bool Bool) | `delta x _ := x`, `Zero _ := True`; laws by `trivial` | ADMITTED instance (countermodel); laws trivially PROVED — **not a kernel observer** |

Observer classification requested by the task. Kernel observers in this module (laws proved once, in `DiffInterface.kernelObs`, from equality of a view): `kernelObs (fun p : K × X => φ p.2)` in `tag_view_zeroRel`; `kernelObs p` with `p : Nat → Nat` in `classConstant_iff_fiberConstant_all`, `descend_iff_factorsOn_all`, `fiberConstant_fixed_D_not_classConstant`. Observers whose laws are admitted fields: every theorem over a parameter `O : DiffObs X R` (items 1–5 of the header) takes the three laws as fields of the hypothesis `O`; the module proves nothing about where they come from. The two concrete non-kernel observers `intDiffObs` and `collapseAllObs` discharge their law fields per instance (arithmetic; `trivial`) rather than inheriting them from a view, which is what `native_derivation_map.md` (tail) means by "not kernel observers".

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| obsQuotient_exact | 83 | equal classes give a zero-pair | FROZEN | propext | S |
| obsQuotient_mk_eq_iff | 88 | classes equal ↔ zero-pair | FROZEN | propext, Quot.sound | S |
| obsQuotient_mk_surjective | 96 | every class is `mk` of a point | FROZEN | none | S |
| descend_mk | 113 | `descend O f hf (mk x) = f x` (rfl) | FROZEN | none | A |
| descend_exists_iff | 119 | a factorization through the quotient exists ↔ `ClassConstant O f` | FROZEN | Quot.sound | S |
| descend_unique | 134 | two factorizations agreeing on classes are equal as functions | FROZEN | Quot.sound | S |
| descend_blocked_of_witness | 142 | a zero-pair with `f x ≠ f y` refutes existence | REFUTED (of descent, given a witness) | Quot.sound | S |
| deltaDescend_mk | 161 | computation rule (rfl) | FROZEN | none | A |
| deltaDescend_exists_iff | 169 | binary factorization exists ↔ `DeltaConstant O` | FROZEN | Quot.sound | S |
| deltaDescend_unique | 188 | uniqueness of the descended difference map | FROZEN | Quot.sound | S |
| deltaDescend_blocked_of_witness | 200 | two zero-pairs with distinct difference values block descent | REFUTED (of descent, given witnesses) | Quot.sound | S |
| classConstant_pair_iff | 212 | pair view class-constant ↔ both components | FROZEN | none | S |
| pair_descend_exists_iff | 225 | pair descends ↔ both components descend | FROZEN | Quot.sound | S |
| view_descends_pair_blocked | 248 | given `ClassConstant O f`, a zero-pair and `g x ≠ g y`: `f` descends and `(f, g)` does not | CONDITIONAL: ClassConstant O f, ZeroRel O x y, g x ≠ g y | Quot.sound | S |
| coarsenMap_mk | 267 | computation rule (rfl) | FROZEN | Quot.sound | A |
| classConstant_comp_mk_iff | 276 | `ClassConstant O (mk S ∘ f)` ↔ `f` compatible up to `S` | FROZEN | propext, Quot.sound | S |
| descendMod_exists_iff | 284 | existence form of mod-setoid descent for views | FROZEN | propext, Quot.sound | A |
| deltaDescendMod_exists_iff | 293 | existence form for the difference map | FROZEN | propext, Quot.sound | A |
| pairSetoid_mk_eq_iff | 327 | product-setoid classes equal ↔ componentwise | FROZEN | propext, Quot.sound | A |
| descendMod_exists_of_coarsen | 334 | mod-setoid descent transports along `S ⊆ T` | FROZEN | Quot.sound | A |
| tag_view_zeroRel | 350 | `ZeroRel (kernelObs (φ ∘ snd)) s t ↔ φ s.2 = φ t.2` (Iff.rfl) | FROZEN (definitional) | none | A |
| intDiffObs_zeroRel | 374 | `ZeroRel intDiffObs a b ↔ a = b` | FROZEN | propext, Quot.sound | A |
| int_sub_ne_zero_iff | 385 | `a − b ≠ 0 ↔ a ≠ b` | FROZEN (integer arithmetic) | propext, Quot.sound | A |
| int_sub_ne_zero_of_gt | 393 | `b < a → a − b ≠ 0` | FROZEN | propext, Quot.sound | A |
| int_shift_cancel | 398 | `(a + c + 2b) − (a + c) = 2b` | FROZEN | propext, Quot.sound | A |
| int_two_mul_eq_zero_iff | 403 | `2b = 0 ↔ b = 0` | FROZEN | propext, Quot.sound | A |
| int_add_sub_cancel | 411 | `(s + d) − s = d` | FROZEN | propext, Quot.sound | A |
| value_orientation_survives | 417 | `delta 0 1 ≠ delta 1 0` while `ZeroRel 0 1 ↔ ZeroRel 1 0` (both false) | VERIFIED_FINITE (two integers) | propext, Quot.sound | S |
| collapseAllObs_all_zero | 445 | every pair is a zero-pair (`trivial`) | FROZEN (trivially true by definition of `Zero`) | none | A |
| collapseAllObs_not_deltaConstant | 452 | `¬ DeltaConstant collapseAllObs` (witness `true, false`) | REFUTED | none | S |
| collapseAllObs_no_delta_descend | 458 | the difference map does not descend | REFUTED | Quot.sound | S |
| collapseAllObs_id_not_classConstant | 469 | the identity view is not class-constant | REFUTED | none | A |
| collapseAllObs_no_view_descend | 476 | the identity view does not descend | REFUTED | Quot.sound | S |
| classConstant_iff_fiberConstant_all | 494 | for `p q : Nat → Nat`: `ClassConstant (kernelObs p) q ↔ ∀ D, FiberConstant D p q` | FROZEN | none | S |
| descend_iff_factorsOn_all | 507 | descent to the quotient of `kernelObs p` ↔ `∀ D, FactorsOn D p q` | FROZEN | Quot.sound | S |
| fiberConstant_fixed_D_not_classConstant | 523 | `FiberConstant [] (const 0) id` yet `¬ ClassConstant (kernelObs (const 0)) id` | REFUTED (of removing `∀ D`) | none | S |
| sigEq_append_iff | 532 | `SigEq (Q₁ ++ Q₂) x x' ↔ SigEq Q₁ x x' ∧ SigEq Q₂ x x'` | FROZEN | propext | A |

Count check: 37 theorems, all 37 in the artifact.

## 4. External and admitted assumptions

- `DiffObs`, `ZeroRel`, `ObsQuotient`, `obsQuotient_eq_of_zero`, `kernelObs` (DiffInterface); `Compression.FiberConstant`, `FactorsOn`, `factors_iff_fiberConstant`, `SigEq`.
- Library doing real work: `Quotient.lift`, `Quotient.lift₂`, `Quotient.sound`, `Quotient.exact`, `Quotient.inductionOn`/`inductionOn₂`, `funext`, `omega`, `Bool.noConfusion`. The module's header declares exactly this list ("no choice, no excluded middle"); the axiom reports confirm it.
- Type parameters `{X R Y Z : Type}`, `Setoid Y`, `Int`: metatheory. Finitude flag: the quotient `ObsQuotient O` over an arbitrary carrier and "every class is the class of a point" are statements in the metalanguage about Lean quotient types; nothing here is a container the system holds, and the docstrings do not say otherwise ("the quotient machinery of the metalanguage").
- Unearned identity: none. Unrestricted external universe: the `Type` parameters, declared. Unbounded function treated as internally available: `p q : Nat → Nat` in the dictionary are presentations/questions in the Compression sense (metatheoretic functions over a represented finite `D`); the dictionary's `∀ D : List Nat` quantifies over all Lean lists. Silently assumed observer: none — every theorem names its `O` or its `kernelObs`. Unspecified correspondence between presentations: none. Cost function: none. Admitted condition later described as forced: none. Finite computation presented as universal: none (`value_orientation_survives` is presented as two concrete values).

## 5. Derived consequences

Imported by `ContactBridge`, `ContactKernel`, `DiffAnchor` (checked by grep for `ObsDescent.`/`open ObsDescent`). Ledger: CL-PD2-CONTACT-RECONSTRUCTION (all 37 names), CL-PD2-CONTACT-DICTIONARY (the five dictionary names); write-ups `paper/primitive_difference_contact.md` §(180–190), `paper/primitive_difference_ascent.md` table rows 50–55; `paper_change_log.md` 962–982; `native_derivation_map.md` tail (the observer classification).

## 6. Counterexamples and limitations

- `collapseAllObs_*` (four theorems): refute "a total collapse of the zero relation collapses the difference map" and "the identity view descends through a one-class quotient"; witness the two Booleans. The docstring states, correctly, that `Bool` minimality is metatheory (a subsingleton carrier admits no such obstruction) and is not a Lean theorem.
- `fiberConstant_fixed_D_not_classConstant`: refutes removing the `∀ D` from the dictionary; witness `D = []`.
- `value_orientation_survives`: not a refutation of anything proved; it records that the integer observer's values carry orientation that `ZeroRel` cannot.
- Not proved: anything about observers on carriers other than those named; the dictionary is proved for `kernelObs p` with `p : Nat → Nat` only (the ledger says so); no transport between quotient descent and the passage obstruction `obstP` (ledger marks that comparison METATHEORY); the arriving development's "non-derivability" claim is not reconstructed (refused; see `primitive_interpreter_boundary.md` scope note).

## 7. Axiom dependencies

All 37 within {propext, Quot.sound}; 11 use none. Theorems exceeding the set: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 37 in the artifact; ledger cites all. No probe run; every proof read (short terms; the two `calc` blocks rewrite along `obsQuotient_eq_of_zero`).

## 9. Related Python implementations

No direct mirror of the quotient-descent layer found in `code/derivation/` (grep for `ClassConstant`, `descend`, `collapseAll`, `intDiffObs`: none). The dictionary's Compression side is mirrored by `code/derivation/compression.py` (`fiber_constant`, `factors_on`); the observer side by `code/derivation/observe.py` / `observer_inventory.py` only in the sense of the sealed view observers (not checked in detail). The contact collision's computed side lives in `contact/analysis/contact_countermodels.json` (outside `code/`; not checked).

## 10. Textbook placement proposal

- Prerequisites: `DiffObs`, `ZeroRel`, `zeroRel_equivalence`, `ObsQuotient`, `obsQuotient_eq_of_zero`, `kernelObs` (DiffInterface); `FiberConstant`/`FactorsOn` (Compression); Lean quotients as metatheory.
- Substantive: `obsQuotient_mk_eq_iff` + `obsQuotient_mk_surjective`; `descend_exists_iff`, `descend_unique`, `descend_blocked_of_witness`; `view_descends_pair_blocked`; `classConstant_comp_mk_iff` (the one reduction that collapses the mod-setoid layer); `collapseAllObs` with `collapseAllObs_not_deltaConstant`; `descend_iff_factorsOn_all` with `fiberConstant_fixed_D_not_classConstant`.
- Auxiliary: the `_mk` computation rules, the binary forms (teach as "same again, two arguments"), `pairSetoid`, `coarsenMap`, `descendMod_*`, `tag_view_zeroRel`, the five `int_*` lemmas, `intDiffObs_zeroRel`.
- Lesson title: "Descending a view through the observer quotient: exactly when, and the one countermodel." The one question: what does a zero relation license you to forget, and what survives it (the orientation of values; the pair that blocks)?
- Omit: the five `int_*` arithmetic lemmas and `int_shift_cancel` (they exist to subsume an external tail and teach nothing about Genesis); `tag_view_zeroRel` (an `Iff.rfl`).

## 11. Interpretation findings

1. Header item 6 "Tag realization: a tag-augmented view observer is the native `kernelObs` of the view composed with the second projection" versus `tag_view_zeroRel`, which is `Iff.rfl`: the Lean states that `ZeroRel` of an already-kernel observer unfolds to equality of the view. No arriving "tag observer" is defined in Lean and shown equal to this; the realization is the choice to write it as `kernelObs`. The docstring says "definitionally", which is accurate. Classification: none as a defect; noted so the textbook does not present it as a theorem relating two structures.
2. Ledger CL-PD2-CONTACT-RECONSTRUCTION: "the arriving integer tail never instantiates its own core structure; it is subsumed by one native instance plus five one-line lemmas". The five lemmas are integer arithmetic with no Genesis content; "subsumption" is a claim about an external text not present in the repository. Classification: none in Lean; recorded as unverifiable from the sealed tree (the arriving text is in `contact/analysis/`, not checked).
3. Vacuity check: `collapseAllObs_all_zero` has a trivially true conclusion (`Zero _ := True`); it is a component of a deliberate countermodel and is labelled as such. `view_descends_pair_blocked`'s hypotheses are jointly satisfiable (e.g. `collapseAllObs`, `f` constant, `g = id`, `x = true, y = false`). No other trivialities found.
4. Finitude: none found; the header declares the quotient machinery as metatheory.
