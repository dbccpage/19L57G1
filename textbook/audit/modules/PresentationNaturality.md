# Audit: PresentationNaturality

| field | value |
|---|---|
| Path | lean4/Derivation/PresentationNaturality.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 9ceaf49adcd21ca0 |
| Lines | 665 |
| Imported by root `Derivation.lean` | yes (line 50) |
| Imports | Derivation.ContactKernel |
| Declarations | 5 structures (`Bij`, `PresIso`, `Viable`, `Family`, `HFamily`), 2 inductives (`Card4`, `Two`), 33 defs, 30 theorems. (The inventory JSON lists a 31st "theorem `stands`": that is the prose phrase "the sealed theorem stands on its own scope" at line 16, not a declaration.) |
| Axiom reports in `artifacts/lean_axioms.txt` | 29 lines (`Derivation.lean:1336`–`1365`); axioms seen: none for 28 theorems, `Quot.sound` for `bool_obstruction_and_sealed_selector`. Only `tw_involutive` and `negIso_fixed_point_free` are listed in the root inventory; both are present. All 30 theorems are reported. |
| Forbidden tokens (sorry/admit/axiom) | none found (`grep -n "sorry\|admit\|^\s*axiom\|unsafe\|partial"` over the file: no hits; the only "axiom" strings are in `#print axioms` lines in the root, not here) |

## 1. Mathematical purpose

The module asks whether an observer's admissible pair (a pair of carrier elements the observer separates, `NonZeroPair O`) can be selected *naturally* — that is, compatibly with a declared relabelling of the presentation — rather than merely selected. It first makes the question well typed: a presentation isomorphism `PresIso O O'` is a bijection of carriers and a bijection of residual values (both inverses given as data) under which `delta` and `Zero` correspond; `zeroRel_transport` shows the induced zero relation corresponds, and `PresIso.mapPair` therefore carries admissible pairs across. A *family* is a declared list of observers and isomorphisms between them (no closure assumed); a section picks an admissible pair at every object; it is natural when every declared isomorphism carries the pair at its source to the pair at its target. The obstruction (`no_natural_section_of_fixed_point_free`, `no_natural_section_of_endo`) is that a declared automorphism fixing no admissible pair rules out every natural section. Two finite fixtures bound the result in both directions: at the two-element equality observer with negation there is a raw section but no natural one; at a four-element observer with a transposition fixing two elements a natural section exists. The module explicitly does not derive the sealed `ContactKernel.no_equivariant_pair_valued_map` from the general obstruction; it co-states them and records the derivation as OPEN.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `Bij A B` | 82 | structure | A function with a two-sided inverse, both round-trip laws as fields. | ADMITTED |
| `Bij.rfl'` | 88 | def | Identity bijection. | ADMITTED |
| `Bij.symm` | 94 | def | Inverse bijection (swap fwd/bwd). | ADMITTED |
| `Bij.trans` | 100 | def | Composite bijection. | ADMITTED |
| `PresIso O O'` | 118 | structure | Carrier bijection + residual bijection + `delta_transport` + `zero_transport` (the Zero predicate corresponds under the residual bijection). | ADMITTED (the notion of "presentation isomorphism" is declared here, not derived) |
| `PresIso.refl` | 140 | def | Identity presentation isomorphism. | ADMITTED |
| `PresIso.symm` | 146 | def | Inverse; proof of transport laws uses the `Bij` round trips. | ADMITTED |
| `PresIso.trans` | 162 | def | Composite. | ADMITTED |
| `Viable X R` | 196 | structure | An observer with `Nonempty (NonZeroPair obs)`. Never used by any theorem in this file (checked: no later reference). | ADMITTED |
| `PresIso.mapPair` | 204 | def | Transports an admissible pair along the carrier bijection; admissibility preserved via `zeroRel_transport`. | ADMITTED |
| `Family X R` | 222 | structure | Declared observers `Obj → DiffObs X R` (one carrier `X`, one residual `R` for all objects) plus arrows `Arr` with `src`,`tgt`,`iso`. No composition/inverse/identity required. | ADMITTED (declared family) |
| `Sec D` | 232 | def | `∀ a : D.Obj, NonZeroPair (D.obs a)` — a pair at every object. | ADMITTED |
| `IsNatural D s` | 236 | def | `∀ f : D.Arr, (D.iso f).mapPair (s (src f)) = s (tgt f)`. | ADMITTED |
| `autoFamily O F` | 242 | def | One object (`Unit`), one arrow (`Unit`), iso `F`. | ADMITTED |
| `notBij` | 293 | def | `not` as a `Bij Bool Bool` (`decide`). | ADMITTED |
| `negIso` | 301 | def | Negation as a `PresIso boolEqObs boolEqObs` with identity on residuals; `delta_transport` by `decide`. | ADMITTED (fixture) |
| `boolEqPair` | 325 | def | `(false,true)` as admissible pair of `boolEqObs`. | ADMITTED |
| `boolEqRawSection` | 328 | def | Constant section at `boolEqPair`. | ADMITTED |
| `Card4` | 349 | inductive | Four-element carrier `e1..e4`. | ADMITTED |
| `tw` | 354 | def | Swap `e1,e2`, fix `e3,e4`. | ADMITTED |
| `twBij` | 363 | def | `tw` as a bijection. | ADMITTED |
| `card4Obs` | 371 | def | `kernelObs id` on `Card4` (zero relation = equality). | ADMITTED |
| `twPairBij` | 373 | def | `tw × tw` on residual pairs. | ADMITTED |
| `twIso` | 388 | def | The transposition as a `PresIso card4Obs card4Obs`. | ADMITTED |
| `card4Pair` | 399 | def | `(e3,e4)`, admissible. | ADMITTED |
| `card4Section` | 402 | def | Constant section at `card4Pair`. | ADMITTED |
| `HFamily` | 497 | structure | Objects with object-indexed carrier and residual types, `Hom a b : Type`, `iso`. No closure assumed. | ADMITTED (declared family) |
| `HSec D` | 505 | def | Dependent section over an `HFamily`. | ADMITTED |
| `HIsNatural D s` | 507 | def | Naturality w.r.t. every `h : Hom a b`. | ADMITTED |
| `hAutoFamily O F` | 525 | def | One-object `HFamily` with `Hom _ _ := Unit`, iso `F`. | ADMITTED |
| `Two` | 556 | inductive | Two object names `bool`, `four`. | ADMITTED |
| `twoCar`, `twoRes`, `twoObs` | 560, 564, 568 | def | Carriers `Bool`/`Card4`, residuals `Bool`/`Card4×Card4`, observers `boolEqObs`/`card4Obs`. | ADMITTED |
| `twoHom` | 573 | def | `Unit` on the diagonal, `Empty` across. | ADMITTED |
| `twoIsoNeg` | 579 | def | `negIso` at `bool`, `twIso` at `four`. | ADMITTED |
| `twoFamilyNeg` | 585 | def | The negative two-object family. | ADMITTED |
| `twoIsoPos` | 601 | def | `PresIso.refl` at `bool`, `twIso` at `four`. | ADMITTED |
| `twoFamilyPos` | 607 | def | The positive two-object family. | ADMITTED |
| `twoSectionPos` | 615 | def | `boolEqPair` at `bool`, `card4Pair` at `four`. | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `Bij.fwd_injective` | 108 | A `Bij`'s forward map is injective (via `bwd_fwd`). | FROZEN | none | A |
| `zeroRel_transport` | 128 | For any `F : PresIso O O'` and `x y`, `ZeroRel O x y ↔ ZeroRel O' (F.car.fwd x) (F.car.fwd y)`. | FROZEN | none | S |
| `refl_car` | 174 | `(PresIso.refl O).car.fwd x = x` (rfl). | FROZEN | none | A |
| `trans_car` | 177 | `(F.trans G).car.fwd x = G.car.fwd (F.car.fwd x)` (rfl). | FROZEN | none | A |
| `symm_car_left` | 181 | `F.symm.car.fwd (F.car.fwd x) = x`. | FROZEN | none | A |
| `symm_car_right` | 185 | `F.car.fwd (F.symm.car.fwd x') = x'`. | FROZEN | none | A |
| `symm_symm_car` | 189 | `F.symm.symm.car.fwd x = F.car.fwd x` (rfl). | FROZEN | none | A |
| `viable_transport` | 211 | If `NonZeroPair O` is nonempty and `F : PresIso O O'` then `NonZeroPair O'` is nonempty. | FROZEN | none | A |
| `no_natural_section_of_fixed_point_free` | 272 | For any `O`, `F : PresIso O O`, if `∀ p : NonZeroPair O, F.mapPair p ≠ p` then there is no natural section of `autoFamily O F`. | FROZEN (near-definitional: see §11) | none | S |
| `fixed_pair_of_natural_section` | 282 | A natural section over `autoFamily O F` yields `p` with `F.mapPair p = p`. | FROZEN | none | A |
| `negIso_fixed_point_free` | 309 | `negIso.mapPair p ≠ p` for every admissible pair of `boolEqObs`. | VERIFIED_FINITE (`decide` on `Bool`) | none | S |
| `no_natural_section_boolEq` | 318 | No natural section over `autoFamily boolEqObs negIso`. | VERIFIED_FINITE (instance of the general theorem at a concrete observer) | none | S |
| `selection_is_possible_naturality_is_not` | 335 | `Sec (autoFamily boolEqObs negIso)` is nonempty and no natural section exists there. | VERIFIED_FINITE | none | S |
| `tw_involutive` | 360 | `tw (tw x) = x` (cases). | VERIFIED_FINITE | none | A |
| `card4_natural_section` | 409 | `card4Section` is natural over `autoFamily card4Obs twIso` (rfl after `Subtype.ext`). | VERIFIED_FINITE | none | S |
| `card4_has_natural_section` | 417 | Existential form of the previous. | VERIFIED_FINITE | none | S |
| `naturality_separates_presentations` | 427 | `card4` has a natural section and `boolEq`/`negIso` has none. | VERIFIED_FINITE | none | S |
| `bool_obstruction_and_sealed_selector` | 446 | Conjunction of `negIso_fixed_point_free`, `no_natural_section_boolEq`, and `ContactKernel.no_equivariant_pair_valued_map`; no implication between them. | VERIFIED_FINITE (co-statement) | Quot.sound (inherited from `swapObs_boolEqObs`'s `funext`) | S (as a record of non-derivation) |
| `mapPair_refl` | 462 | `(PresIso.refl O).mapPair p = p`. | FROZEN | none | A |
| `mapPair_trans` | 467 | `(F.trans G).mapPair p = G.mapPair (F.mapPair p)`. | FROZEN | none | A |
| `mapPair_symm_left` | 474 | `F.symm.mapPair (F.mapPair p) = p`. | FROZEN | none | A |
| `mapPair_symm_right` | 481 | `F.mapPair (F.symm.mapPair q) = q`. | FROZEN | none | A |
| `no_natural_section_of_endo` | 517 | For any `HFamily D`, object `a`, `h : Hom a a` fixing no admissible pair of `D.obs a`, no `HSec D` is `HIsNatural`. | FROZEN | none | S |
| `hAuto_iff_auto` | 538 | Natural section over `hAutoFamily O F` exists iff one exists over `autoFamily O F`. | FROZEN (one-object only, by construction of both sides) | none | A |
| `twIso_fixes_card4Pair` | 619 | `twIso.mapPair card4Pair = card4Pair`. | VERIFIED_FINITE | none | A |
| `twoFamilyNeg_no_section` | 597 | No natural section of `twoFamilyNeg`. | VERIFIED_FINITE | none | S |
| `twoFamilyPos_natural` | 627 | `twoSectionPos` is natural over `twoFamilyPos`. | VERIFIED_FINITE | none | S |
| `twoFamilyPos_has_section` | 635 | Existential form. | VERIFIED_FINITE | none | A |
| `heterogeneous_naturality_separates` | 643 | `twoFamilyPos` has a natural section, `twoFamilyNeg` has none. | VERIFIED_FINITE | none | S |

## 4. External and admitted assumptions

- Structures: `DiffObs X R` (DiffInterface: `delta`, `Zero`, three equivalence laws as fields), `NonZeroPair`, `kernelObs`, `boolEqObs`, `swapObs`, and the sealed theorem `no_equivariant_pair_valued_map` (ContactKernel). All taken as given.
- `PresIso` is an **admitted** notion of presentation change: a bijection on carrier *and* a bijection on residual values with two transport laws. Nothing in the module derives that this is the "right" notion of sameness of presentation; it is declared. Which bijections are presentation isomorphisms is therefore a modelling decision.
- `Family`/`HFamily` are **declared** collections: naturality is relative to exactly the arrows listed. The obstruction theorems quantify over whatever family is supplied; no closure under composition/inverse/identity is assumed or needed.
- Universe/Type parameters: `X R X' R' …: Type`; `Family.Obj : Type`, `Family.Arr : Type`, `HFamily.Hom : Obj → Obj → Type`. These are metatheoretic indexing types; the fixtures instantiate them with `Unit`, `Two`, `Empty`.
- Unearned identity: none found (every equality proved is `rfl`, `Subtype.ext`+`rfl`, or a `Bij` round-trip rewrite).
- Unrestricted external universe: none found beyond the metatheoretic `Type` parameters above (flagged under the finitude rule: `Sec D : Type := ∀ a : D.Obj, …` is a Lean Π-type, not a system-internal container; the docstring does not read it as one).
- Unbounded function treated as internally available: none found. (`Bij.fwd : A → B` is data; both fixtures are finite.)
- Silently assumed observer: none found — every statement names its `DiffObs`.
- Unspecified correspondence between presentations: none found; the correspondence is the explicit `PresIso`, with both inverses as data.
- Cost function: none in this module.
- Admitted condition later described as forced: none found. The docstrings and ledger consistently say "declared family", "relative to the declared family".
- Finite computation presented as universal: none found; the finite fixtures are labelled as fixtures, the general theorems are the two `no_natural_section_*` statements.
- Library lemmas doing real work: `Subtype.ext`, `Bool.noConfusion`, `Card4.noConfusion`, `decide` over `Bool`/`Card4`, `Empty.elim`. No choice principle.

## 5. Derived consequences

- `PresentationDescent` (imports this module) reuses `Bij`, `PresIso`, `zeroRel_transport`, `mapPair` for its translation/round-trip notions (checked by grep: `PresIso` used there).
- `NoOutsideFidelity` does not use `Bij` or `PresIso` (grep: no occurrence). `FidelityClosure` uses `Bij`, `Bij.rfl'`, `Bij.symm`, `Bij.trans` (via `FidelityPath.toBij`), and `PresentationDescent` uses `Bij` (`coherent_to_bij`); both reach this module through the import chain.
- Downstream citations of theorem names outside this module: none found in `lean4/Derivation/*.lean` other than `PresentationDescent` (grep for `no_natural_section`, `autoFamily`, `negIso`, `twIso`: only this file and `PresentationDescent` [for `PresIso`]).
- The paper spine (`paper/paper.md`) does not cite this module (grep for `PresentationNaturality`, `natural section`: no hits). The claim ledger has two entries, CL-PN-NATURAL-SELECTION and CL-PN-HETEROGENEOUS-TRANSPORT, and the change log has two dated entries (2026-08-14).

## 6. Counterexamples and limitations

- Countermodels: `negIso_fixed_point_free` + `no_natural_section_boolEq` refute "a natural selector exists at `boolEqObs` under negation" (witness: `Bool` negation has no fixed point). `selection_is_possible_naturality_is_not` refutes the reading "no selector exists" (witness `boolEqRawSection`). `card4_has_natural_section` refutes "the obstruction is universal" (witness `(e3,e4)` fixed by `tw`). `twoFamilyNeg_no_section`/`twoFamilyPos_has_section` repeat both boundaries over two objects.
- Not proved (and the module says so): any categorical structure on `PresIso`; a general embedding `Family → HFamily`; naturality under arrows crossing objects of different carriers (the two-object fixtures have `Hom bool four = Empty`); any derivation of `ContactKernel.no_equivariant_pair_valued_map` from the section-level obstruction.
- `Viable` is defined and never used.
- `hAuto_iff_auto` is between two one-object constructions whose sections and naturality conditions are definitionally the same up to `Unit` arguments; it is a bookkeeping bridge, not a result about families in general.

## 7. Axiom dependencies

28 of 29 reported theorems are axiom-free; `bool_obstruction_and_sealed_selector` depends on `Quot.sound` only, inherited from `ContactKernel.swapObs_boolEqObs` (`funext`). Nothing exceeds {propext, Quot.sound}: none.

## 8. Verification status

- Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0).
- All 30 theorems appear in `artifacts/lean_axioms.txt` at `Derivation.lean:1336`–`1365` (the inventory JSON missed `Bij.fwd_injective` because of its dotted name; the artifact line is 1217).
- Paper: not cited in `paper/paper.md`; cited in `paper/paper_claim_ledger.md` (CL-PN-NATURAL-SELECTION, CL-PN-HETEROGENEOUS-TRANSPORT) and `paper/paper_change_log.md` (two 2026-08-14 entries); listed in `artifacts/completion_dependency_graph.json`.
- Probe run: `/tmp/claude-0/-home-claude/47be43b5-43cb-5429-bc31-b53a81ca595d/scratchpad/probes/F2/pn_probe.lean` via `lake env lean` inside `lean4/`, exit 0. Output: `no_natural_section_of_fixed_point_free` — no axioms; `bool_obstruction_and_sealed_selector` — `[Quot.sound]`; `heterogeneous_naturality_separates` — no axioms. The probe also checked (and Lean accepted) that over `autoFamily O F` the existence of a natural section is *equivalent* to the existence of an admissible pair fixed by `F.mapPair`, confirming the docstring's "near-definitional" self-assessment.

## 9. Related Python implementations

None found. `grep -rn "PresIso\|natural_section\|IsNatural\|autoFamily\|negIso" code tests` returns only two index-maintenance tests mentioning the unrelated research tree name `natural_sections`. The ledger states "Python evidence: none. This claim is Lean-only by construction."

## 10. Textbook placement proposal

- Prerequisites: `DiffObs` and `ZeroRel` (DiffInterface); `NonZeroPair`, `boolEqObs`, `swapObs`, `kernelObs` (ContactKernel); the sealed `no_equivariant_pair_valued_map`; the distinction between presentation identity and internal identity (CLAUDE.md assumption discipline).
- Substantive: `PresIso` + `zeroRel_transport` + `mapPair` (the transport machinery); `no_natural_section_of_fixed_point_free` / `no_natural_section_of_endo` (taught together with the warning that they are one-line); the four boundary fixtures (`selection_is_possible_naturality_is_not`, `card4_has_natural_section`, `naturality_separates_presentations`, `heterogeneous_naturality_separates`); the co-statement `bool_obstruction_and_sealed_selector` as a lesson in *not* deriving.
- Auxiliary: `Bij` and its three operations, `refl_car`…`symm_symm_car`, `mapPair_refl/trans/symm_*`, `viable_transport`, `tw_involutive`, `twIso_fixes_card4Pair`, `hAuto_iff_auto`, the existential restatements.
- Suggested lesson: "Can a pair be chosen in a way every relabelling respects?" — answering: only if some relabelling-fixed admissible pair exists; at the two-element observer with negation none does, at a four-element observer with a transposition one does, and selection as such is never in question.
- Recommend omitting: `Viable` (unused); `Family` (the flat version, retained in Lean for historical reasons but superseded for teaching by `HFamily`, with a note that `hAuto_iff_auto` only bridges one object); `twoFamilyPos_has_section` and `card4_has_natural_section` as separate items (restatements).

## 11. Interpretation findings

1. **Docstring §12 vs Lean, `no_natural_section_of_endo`** — the docstring says "The obstruction over many objects … already rules out a natural section of the whole family". Lean: the hypothesis is a *declared* `h : D.Hom a a` with `∀ p, (D.iso a a h).mapPair p ≠ p`. Correct as stated; but a reader might take "many objects" to mean the arrows between objects play a role. They do not: the proof uses only `hs a a h`. Smallest illustration: `twoFamilyNeg` has `Hom bool four = Empty`; the result holds identically for any `Hom` across objects. Classification: not a defect (docstring §14 and ledger both say cross-object arrows are not exercised); recorded as a reading hazard only.
2. **Near-definitional status** — the docstring (lines 261–271) and ledger both flag that `no_natural_section_of_fixed_point_free` is near-definitional. The probe above verifies the stronger fact: over `autoFamily O F`, natural-section existence is *equivalent* to a fixed admissible pair. So the theorem adds no content beyond unfolding `IsNatural` at a one-object family. The ledger's "The general theorem" heading reads slightly stronger than this, but the same entry's "Weight, recorded honestly" paragraph corrects it. INTERPRETATION DEFECT (minor, self-corrected in the same entry).
3. **Change log heading "Naturality obstruction across presentations"** — the Lean obstructions are about *automorphisms of one presentation* (endomorphisms `Hom a a`), never about an isomorphism between two different presentations. "Across presentations" is accurate only for the transport machinery (`PresIso`, `mapPair`), not for the obstruction theorems. INTERPRETATION DEFECT (wording).
4. Vacuity check: `no_natural_section_of_fixed_point_free`'s hypotheses are satisfiable (`negIso`) and its conclusion is not trivially true (`card4` is a positive instance). `IsNatural` over `autoFamily` with `Arr := Unit` is satisfiable. Not vacuous.
5. `bool_obstruction_and_sealed_selector` — stated as a conjunction; the ledger and docstring say "CO-STATEMENT, not a derivation". Checked: the Lean proof is a triple of previously proved terms; no implication is proved. The prose matches. None found.
