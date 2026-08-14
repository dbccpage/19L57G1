# Lean definition map: the 103 supplied declarations against the native corpus

Run: primitive-difference contact collision, 2026-08-13. Pre-contact base
`a5caee2`; sealed blind-native-base `ccd3a53`; contact Lean spine committed at
`ebb1e0b`.  The original collision/packet-2 audit tracked **seven declarations
added after that commit**, all verified absent at `ebb1e0b`:
`ContactKernel.toDiffObs`, `.toDiffObs_fields`,
`.toDiffObs_apart`, `ContactBridge.collapse_collision_is_pair_blocked`,
`.pair_blocked_iff_collapse_collision`,
`ContactKernel.kernel_from_obs_iff_pair`, and
`.eq_ofDiffObs_of_fields` (see the anchor note in
`lean_theorem_transport.md`).  That list is historical, not a current-tree
census: packet 2R, packet 5R, and `SeparationCapacity` were added later.
"On disk" below means PR #21 base `de080af` plus this repair diff, and line
numbers are working-tree line numbers.

Supplied external file
`docs_external_to_this_repo/primitive_difference.lean`, sha256
`d9cdb350a53c513e3e211e72f17262be6ba85d7da6159f910388c7137e814a89`, 980 lines,
READ-ONLY, never copied into the repository.

`contact/analysis/` is the only repository location permitted to quote the
supplied development's vocabulary. Every quotation below is labeled
**SUPPLIED_INPUT**.

## Declaration count

**The supplied file declares exactly 103 top-level declarations**: 3 structures
+ 29 defs + 71 theorems. Evidence FINITE_COMPUTATION (enumeration of the file;
independently corroborated by the axiom pass, which emitted exactly 71
`#print axioms` reports — one per theorem — from a clean compile, exit code 0).
Every one of the 103 appears **exactly once** below, numbered 1–103 in file
order and grouped by the supplied file's own section boundaries (A–L). The
per-section accounting that closes this document sums to 103.

## Evidence classes

Every substantive claim below carries exactly one of METATHEORY,
SUPPLIED_INPUT, DEFINITION, DECLARED_POLICY, DERIVED_THEOREM,
CONDITIONAL_THEOREM, FINITE_COMPUTATION, COUNTERMODEL, CONJECTURE, OPEN,
REFUSED. **Comments and doc-strings are never evidence** — neither the supplied
file's nor this repository's. Only formal statements are. The supplied file's
comments are quoted only in the gap table of
`lean_theorem_transport.md`, where they are ruled non-evidential.

## Relation-status legend

| status | meaning |
|---|---|
| `native-implies` | the named native statement implies the supplied statement (possibly after instantiation); the converse is not claimed here |
| `contact-implies` | the supplied statement implies the named native statement; the converse is not claimed here |
| `equivalent-under-H` | the two statements are inter-derivable under the stated hypothesis `H` |
| `incomparable` | neither direction holds; a countermodel is cited |
| `same-third-notion` | both statements are instances of one further notion, each priced differently; neither is a specialization of the other |
| `instance-material` | concrete data (an instance, a carrier, a value assignment), not a proposition; compared by exhibiting the native instance |
| `NONE` | no native counterpart; the reason is stated |

### The standing hypothesis `H_struct`

`H_struct` = **the field-for-field structure identification at `Type 0`**: the
supplied core structure and the native `DiffInterface.DiffObs` (sealed at base
`a5caee2`, `lean4/Derivation/DiffInterface.lean:33`) carry the same five fields
in the same order — a valued difference map, a zero predicate on values, and
three equivalence law FIELDS. The differences are: field spelling (`δ` vs
`delta`), binder implicitness on two law fields, and universe polymorphism
(supplied `Type u`/`Type v`, native monomorphic `Type`). Evidence
FINITE_COMPUTATION: a scratch bridge file (kept outside the repository; hashes
recorded in `contact_countermodels.json`) compiles both, converts in both
directions, and proves both round trips and the zero-relation match, with all
three reports "does not depend on any axioms". `H_struct` is therefore
*definitional* at `Type 0` and is **not** a mathematical admission; it is a
universe restriction plus renaming. Every `equivalent-under-H` row below with
no further qualification means `H = H_struct` alone.

Where a row needs more than `H_struct`, the extra hypothesis is named in the
row (e.g. pointwise `Decidable` of the zero relation).

### Assumption-graph shorthands

- **[CORE 1–9]** = supplied items 1–9: `PrimitiveDifference`, `ZeroRel`,
  `zeroRel_refl`, `zeroRel_symm`, `zeroRel_trans`, `zeroRel_equivalence`,
  `zeroSetoid`, `ResidualQuotient`, `classOf`.
- **[CORE 1–10]** = [CORE 1–9] plus item 10 `classOf_eq_of_zero`.
- **Metatheory of the supplied file (uniform):** the Lean core prelude only —
  the file has *no* import statement at all (FINITE_COMPUTATION). No
  `Decidable` anywhere, no `Classical.*`, no `by_contra`, no `by_cases`
  (FINITE_COMPUTATION by inspection, corroborated by the axiom pass: no report
  mentions `Classical.choice`).

### Axiom-report convention

`#print axioms` was run for the 71 theorems only. Definitions and structures
emit no report of their own; their axiom load appears in the theorems that
consume them. Rows for defs/structures therefore say **"no report (not a
theorem)"** — this is a fact about the pass, not a claim of axiom-freedom.
Raw output: `contact_scratch/axiom_report.txt`, 71 entries, from a clean
compile (`lake env lean`, pinned toolchain `leanprover/lean4:v4.33.0`, exit
code 0). FINITE_COMPUTATION throughout.

### Native module locations cited below

| module | path |
|---|---|
| `DiffInterface` (sealed at base) | `lean4/Derivation/DiffInterface.lean` |
| `Compression` (sealed at base) | `lean4/Derivation/Compression.lean` |
| `PrimDiff`, `PrimitiveCore`, `PrimitiveCats`, `Apartness`, `PrimitivePassage`, `Derivation.Quot` (sealed at base) | `lean4/Derivation/` |
| `ObsDescent` (NEW this run) | `lean4/Derivation/ObsDescent.lean` |
| `ContactBridge` (NEW this run) | `lean4/Derivation/ContactBridge.lean` |
| `ContactKernel` (NEW this run) | `lean4/Derivation/ContactKernel.lean` |

---

## Section A — core structure and induced relation (supplied lines 13–65)

### 1. `PrimitiveDifference` — structure (lines 13–18)

**SUPPLIED_INPUT**
```lean
structure PrimitiveDifference (α : Type u) (β : Type v) where
  δ : α → α → β
  Zero : β → Prop
  zero_refl : ∀ x : α, Zero (δ x x)
  zero_symm : ∀ x y : α, Zero (δ x y) → Zero (δ y x)
  zero_trans : ∀ x y z : α, Zero (δ x y) → Zero (δ y z) → Zero (δ x z)
```
- **Assumption graph.** Root of the supplied dependency graph: no supplied
  dependencies. Binders: two universe-polymorphic type arguments. The three
  equivalence laws are **fields**, i.e. data demanded of every instance —
  nothing in the supplied file derives them from anything more primitive
  (FINITE_COMPUTATION).
- **Axiom report.** No report (not a theorem).
- **Neutral content.** A *difference datum*: a carrier with a value-typed
  binary difference map and a designated zero-set of values, together with
  assumed reflexivity, symmetry and transitivity of the induced relation.
- **Native counterpart.** `DiffInterface.DiffObs` (`DiffInterface.lean:33`),
  **sealed at base `a5caee2`, i.e. pre-contact native property**.
- **Relation status.** `equivalent-under-H_struct`. (This is the load-bearing
  identification of the entire collision: the arriving primitive is
  field-for-field the native observer, which the native corpus had already
  sealed before contact.)

### 2. `ZeroRel` — def (lines 24–25)

**SUPPLIED_INPUT**
```lean
def ZeroRel (P : PrimitiveDifference α β) (x y : α) : Prop :=
  P.Zero (P.δ x y)
```
- **Assumption graph.** Direct: item 1 (fields `δ`, `Zero`). Transitive
  closure: {1}. Metatheory: definition unfolding only.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The induced relation: two carrier points are related iff
  their difference value lies in the zero-set.
- **Native counterpart.** `DiffInterface.ZeroRel` (`DiffInterface.lean:42`),
  sealed at base — *same identifier natively*, verified native property at
  `a5caee2` (FINITE_COMPUTATION).
- **Relation status.** `equivalent-under-H_struct` (definitionally equal after
  the field renaming).

### 3. `zeroRel_refl` — theorem (lines 27–29)

**SUPPLIED_INPUT**
```lean
theorem zeroRel_refl (P : PrimitiveDifference α β) :
    ∀ x : α, P.ZeroRel x x :=
  P.zero_refl
```
- **Assumption graph.** Direct: items 1 (field `zero_refl`), 2. Closure: {1,2}.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.zeroRel_refl' does not depend on any axioms`
- **Neutral content.** The induced relation is reflexive. **Content: a pure
  re-export of an admitted field** — no derivation occurs.
- **Native counterpart.** `DiffInterface.zeroRel_equivalence`
  (`DiffInterface.lean:45`), `refl` component, sealed at base. Additionally,
  the native side *proves* the same law (equality-grade, not admitted) at the
  kernel observer `DiffInterface.kernelObs` (`DiffInterface.lean:54`,
  `zero_refl _ := rfl`) and at the passage's declared observation stage via
  `ContactBridge.declared_zero_as_view` (`ContactBridge.lean:628`).
- **Relation status.** `equivalent-under-H_struct`. Recorded asymmetry
  (METATHEORY): identical statements, different provenance — admitted field on
  the supplied side, proved construction on the native side.

### 4. `zeroRel_symm` — theorem (lines 31–33)

**SUPPLIED_INPUT**
```lean
theorem zeroRel_symm (P : PrimitiveDifference α β) :
    ∀ {x y : α}, P.ZeroRel x y → P.ZeroRel y x :=
  fun {x y} => P.zero_symm x y
```
- **Assumption graph.** Direct: items 1 (field `zero_symm`), 2. Closure: {1,2}.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.zeroRel_symm' does not depend on any axioms`
- **Neutral content.** Symmetry of the induced relation; re-export of an
  admitted field.
- **Native counterpart.** `DiffInterface.zeroRel_equivalence`
  (`DiffInterface.lean:45`), `symm` component, sealed at base; proved
  (not admitted) at `kernelObs` (`zero_symm h := h.symm`).
- **Relation status.** `equivalent-under-H_struct`.

### 5. `zeroRel_trans` — theorem (lines 35–37)

**SUPPLIED_INPUT**
```lean
theorem zeroRel_trans (P : PrimitiveDifference α β) :
    ∀ {x y z : α}, P.ZeroRel x y → P.ZeroRel y z → P.ZeroRel x z :=
  fun {x y z} => P.zero_trans x y z
```
- **Assumption graph.** Direct: items 1 (field `zero_trans`), 2. Closure:
  {1,2}.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.zeroRel_trans' does not depend on any axioms`
- **Neutral content.** Transitivity of the induced relation; re-export of an
  admitted field.
- **Native counterpart.** `DiffInterface.zeroRel_equivalence`
  (`DiffInterface.lean:45`), `trans` component, sealed at base; proved at
  `kernelObs` (`zero_trans h1 h2 := h1.trans h2`).
- **Relation status.** `equivalent-under-H_struct`.

### 6. `zeroRel_equivalence` — theorem (lines 39–43)

**SUPPLIED_INPUT**
```lean
theorem zeroRel_equivalence (P : PrimitiveDifference α β) :
    Equivalence P.ZeroRel where
  refl := zeroRel_refl P
  symm := zeroRel_symm P
  trans := zeroRel_trans P
```
- **Assumption graph.** Direct: items 3, 4, 5. Closure: {1,2,3,4,5}.
  Metatheory: the core `Equivalence` bundle.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.zeroRel_equivalence' does not depend on any axioms`
- **Neutral content.** The induced relation is an equivalence relation
  (packaging of items 3–5).
- **Native counterpart.** `DiffInterface.zeroRel_equivalence`
  (`DiffInterface.lean:45`), sealed at base — **the same identifier is native
  property at `a5caee2`** (FINITE_COMPUTATION; recorded in the denylist as a
  native collision, not a coinage).
- **Relation status.** `equivalent-under-H_struct`.

### 7. `zeroSetoid` — def (lines 45–47)

**SUPPLIED_INPUT**
```lean
def zeroSetoid (P : PrimitiveDifference α β) : Setoid α where
  r := P.ZeroRel
  iseqv := zeroRel_equivalence P
```
- **Assumption graph.** Direct: items 2, 6. Closure: {1,…,6}. Metatheory:
  core `Setoid`.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The setoid on the carrier whose relation is the induced
  relation.
- **Native counterpart.** `DiffInterface.obsSetoid` (`DiffInterface.lean:69`),
  sealed at base.
- **Relation status.** `equivalent-under-H_struct`.

### 8. `ResidualQuotient` — def (lines 49–50)

**SUPPLIED_INPUT**
```lean
def ResidualQuotient (P : PrimitiveDifference α β) : Type u :=
  Quotient (zeroSetoid P)
```
- **Assumption graph.** Direct: item 7. Closure: {1,…,7}. Metatheory: core
  `Quotient`.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The canonical quotient `Q` of the carrier by the induced
  relation.
- **Native counterpart.** `DiffInterface.ObsQuotient`
  (`DiffInterface.lean:72`), sealed at base.
- **Relation status.** `equivalent-under-H_struct`.

### 9. `classOf` — def (lines 52–53)

**SUPPLIED_INPUT**
```lean
def classOf (P : PrimitiveDifference α β) (x : α) : P.ResidualQuotient :=
  Quotient.mk (zeroSetoid P) x
```
- **Assumption graph.** Direct: items 7, 8. Closure: {1,…,8}. Metatheory:
  `Quotient.mk`.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The class projection `[·] : α → Q`.
- **Native counterpart.** `DiffInterface.ObsQuotient.mk`
  (`DiffInterface.lean:74`), sealed at base. (The bare identifier `classOf`
  also occurs natively at base in `TransitionAlphabet.lean` — an unrelated
  native declaration, recorded as a native collision in the denylist.)
- **Relation status.** `equivalent-under-H_struct`.

### 10. `classOf_eq_of_zero` — theorem (lines 55–58)

**SUPPLIED_INPUT**
```lean
theorem classOf_eq_of_zero
    (P : PrimitiveDifference α β) {x y : α} (hxy : P.ZeroRel x y) :
    P.classOf x = P.classOf y :=
  Quotient.sound hxy
```
- **Assumption graph.** Direct: items 2, 9. Closure: [CORE 1–9]. Explicit
  hypothesis: `hxy` — the two points are in the induced relation. Metatheory:
  `Quotient.sound`.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.classOf_eq_of_zero' depends on axioms: [Quot.sound]`
- **Neutral content.** Related points have equal classes (quotient soundness).
- **Native counterpart.** `DiffInterface.obsQuotient_eq_of_zero`
  (`DiffInterface.lean:78`), sealed at base.
- **Relation status.** `equivalent-under-H_struct`.

### 11. `classOf_eq_iff_zeroRel` — theorem (lines 60–65)

**SUPPLIED_INPUT (statement)**
```lean
theorem classOf_eq_iff_zeroRel
    (P : PrimitiveDifference α β) {x y : α} :
    P.classOf x = P.classOf y ↔ P.ZeroRel x y := by
```
- **Assumption graph.** Direct: items 9, 10, 2. Closure: [CORE 1–10].
  Metatheory: `Quotient.exact` (effectiveness) and `Quot.sound`; `propext`
  enters through the `↔`.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.classOf_eq_iff_zeroRel' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** Classes are equal **iff** the points are related:
  soundness plus effectiveness.
- **Native counterpart.** `ObsDescent.obsQuotient_mk_eq_iff`
  (`ObsDescent.lean:88`) — **NEW this run**; its exactness half is
  `ObsDescent.obsQuotient_exact` (`ObsDescent.lean:83`), the converse of the
  sealed `obsQuotient_eq_of_zero`. The native base had only the soundness half.
- **Relation status.** `equivalent-under-H_struct`. Native axiom profile
  matches: `[propext, Quot.sound]`.

---

## Section B — descent of the difference map, equality version (lines 67–143)

### 12. `DeltaCongruent` — def (lines 67–71)

**SUPPLIED_INPUT**
```lean
def DeltaCongruent (P : PrimitiveDifference α β) : Prop :=
  ∀ x x' y y' : α,
    P.ZeroRel x x' →
    P.ZeroRel y y' →
    P.δ x y = P.δ x' y'
```
- **Assumption graph.** Direct: items 1, 2. Closure: {1,2}. Metatheory:
  propositional equality on the value type.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** Two-sided compatibility of the difference map with the
  induced relation, up to *equality* on values.
- **Native counterpart.** `ObsDescent.DeltaConstant` (`ObsDescent.lean:151`) —
  NEW this run.
- **Relation status.** `equivalent-under-H_struct` (statement-for-statement
  identical after renaming).

### 13. `deltaFactor` — def (lines 73–82)

**SUPPLIED_INPUT**
```lean
def deltaFactor
    (P : PrimitiveDifference α β) (hcongr : P.DeltaCongruent) :
    P.ResidualQuotient → P.ResidualQuotient → β :=
  Quotient.lift₂
    (s₁ := zeroSetoid P)
    (s₂ := zeroSetoid P)
    (fun x y => P.δ x y)
    (by
      intro x y x' y' hx hy
      exact hcongr x x' y y' hx hy)
```
- **Assumption graph.** Direct: items 7, 8, 12. Closure: {1,…,8, 12}. Explicit
  hypothesis: `hcongr : DeltaCongruent`. Metatheory: `Quotient.lift₂`.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** Under two-sided compatibility, the difference map
  descends to a binary map `Q → Q → β`.
- **Native counterpart.** `ObsDescent.deltaDescend` (`ObsDescent.lean:156`) —
  NEW this run.
- **Relation status.** `equivalent-under-H_struct`.

### 14. `deltaFactor_classOf_classOf` — theorem (lines 84–88)

**SUPPLIED_INPUT (statement)**
```lean
theorem deltaFactor_classOf_classOf
    (P : PrimitiveDifference α β) (hcongr : P.DeltaCongruent)
    (x y : α) :
    P.deltaFactor hcongr (P.classOf x) (P.classOf y) = P.δ x y := by
```
- **Assumption graph.** Direct: items 9, 13. Closure: {1,…,9, 12, 13}.
  Hypotheses: `hcongr`, two carrier points. Proof is definitional.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.deltaFactor_classOf_classOf' does not depend on any axioms`
- **Neutral content.** Computation rule: the descended map commutes with the
  projection.
- **Native counterpart.** `ObsDescent.deltaDescend_mk` (`ObsDescent.lean:161`),
  proved by `rfl` — NEW this run. Native axiom profile matches (axiom-free).
- **Relation status.** `equivalent-under-H_struct`.

### 15. `deltaFactor_requires_congruence` — theorem (lines 90–100)

**SUPPLIED_INPUT (statement)**
```lean
theorem deltaFactor_requires_congruence
    (P : PrimitiveDifference α β)
    (F : P.ResidualQuotient → P.ResidualQuotient → β)
    (hF : ∀ x y : α, F (P.classOf x) (P.classOf y) = P.δ x y) :
    P.DeltaCongruent := by
```
- **Assumption graph.** Direct: items 8, 9, 10, 12. Closure: [CORE 1–10] ∪
  {12}. Explicit hypotheses: an arbitrary binary map `F` on the quotient and
  `hF`, that `F` computes the difference map on classes.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.deltaFactor_requires_congruence' depends on axioms: [Quot.sound]`
- **Neutral content.** Necessity of compatibility: *any* binary map on the
  quotient computing the difference map on classes forces two-sided
  compatibility.
- **Native counterpart.** `ObsDescent.deltaDescend_exists_iff`
  (`ObsDescent.lean:169`), **`.mp` direction** — NEW this run. No separately
  named native declaration; the supplied statement is one `obtain` away from
  the native `↔`.
- **Relation status.** `equivalent-under-H_struct`.

### 16. `deltaFactor_exists_iff_deltaCongruent` — theorem (lines 102–112)

**SUPPLIED_INPUT (statement)**
```lean
theorem deltaFactor_exists_iff_deltaCongruent
    (P : PrimitiveDifference α β) :
    (∃ F : P.ResidualQuotient → P.ResidualQuotient → β,
        ∀ x y : α, F (P.classOf x) (P.classOf y) = P.δ x y)
      ↔ P.DeltaCongruent := by
```
- **Assumption graph.** Direct: items 13, 14, 15. Closure: [CORE 1–10] ∪
  {12,13,14,15}. No hypotheses beyond the difference datum.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.deltaFactor_exists_iff_deltaCongruent' depends on axioms: [Quot.sound]`
- **Neutral content.** **Existence-iff-compatibility** for the difference map:
  the supplied file's first universal-property statement.
- **Native counterpart.** `ObsDescent.deltaDescend_exists_iff`
  (`ObsDescent.lean:169`) — NEW this run.
- **Relation status.** `equivalent-under-H_struct`.

### 17. `deltaFactor_unique` — theorem (lines 114–124)

**SUPPLIED_INPUT (statement)**
```lean
theorem deltaFactor_unique
    (P : PrimitiveDifference α β) (hcongr : P.DeltaCongruent)
    (F : P.ResidualQuotient → P.ResidualQuotient → β)
    (hF : ∀ x y : α, F (P.classOf x) (P.classOf y) = P.δ x y) :
    F = P.deltaFactor hcongr := by
```
- **Assumption graph.** Direct: items 8, 9, 13, 14. Closure: {1,…,9, 12, 13,
  14}. Explicit hypotheses: `hcongr`, `F`, `hF`. Metatheory: `funext`,
  `Quotient.inductionOn₂`.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.deltaFactor_unique' depends on axioms: [Quot.sound]`
- **Neutral content.** **Uniqueness of the binary factorization**, stated
  against the canonical lift.
- **Native counterpart.** `ObsDescent.deltaDescend_unique`
  (`ObsDescent.lean:188`) — NEW this run, in the **symmetric two-map form**
  (`F = G` for any two maps computing the difference map on classes).
- **Relation status.** `equivalent-under-H_struct`. **Hypothesis delta
  (recorded):** the supplied form pins one side to the canonical lift; the two
  forms are inter-derivable given the computation rule
  (`ObsDescent.deltaDescend_mk`, item 14's counterpart). The native form is the
  weaker-hypothesis one and implies the supplied form directly; the reverse
  needs `deltaDescend_mk`.

### 18. `deltaFactor_no_factor_of_not_deltaCongruent` — theorem (lines 126–131)

**SUPPLIED_INPUT (statement)**
```lean
theorem deltaFactor_no_factor_of_not_deltaCongruent
    (P : PrimitiveDifference α β) (hδ : ¬ P.DeltaCongruent) :
    ¬ (∃ F : P.ResidualQuotient → P.ResidualQuotient → β,
        ∀ x y : α, F (P.classOf x) (P.classOf y) = P.δ x y) := by
```
- **Assumption graph.** Direct: item 16. Closure: [CORE 1–10] ∪ {12,…,16}.
  Explicit hypothesis: compatibility fails. Intuitionistically clean: the
  `¬`-form of an `↔`, no excluded middle.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.deltaFactor_no_factor_of_not_deltaCongruent' depends on axioms: [Quot.sound]`
- **Neutral content.** No factorization exists when compatibility fails.
- **Native counterpart.** `ObsDescent.deltaDescend_exists_iff`
  (`ObsDescent.lean:169`) — **no separately named native declaration**; the
  supplied statement is its contrapositive, one step.
- **Relation status.** `equivalent-under-H_struct`.

### 19. `deltaFactor_no_factor_of_zeroRel_ne` — theorem (lines 133–143)

**SUPPLIED_INPUT (statement)**
```lean
theorem deltaFactor_no_factor_of_zeroRel_ne
    (P : PrimitiveDifference α β)
    {x x' y y' : α}
    (hxx : P.ZeroRel x x') (hyy : P.ZeroRel y y')
    (hne : P.δ x y ≠ P.δ x' y') :
    ¬ (∃ F : P.ResidualQuotient → P.ResidualQuotient → β,
        ∀ x y : α, F (P.classOf x) (P.classOf y) = P.δ x y) := by
```
- **Assumption graph.** Direct: items 2, 16. Closure: [CORE 1–10] ∪ {12,…,16}.
  Explicit hypotheses: a concrete four-point witness — two related pairs whose
  difference values differ.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.deltaFactor_no_factor_of_zeroRel_ne' depends on axioms: [Quot.sound]`
- **Neutral content.** Witness-based non-descent: one concrete violation blocks
  every factorization.
- **Native counterpart.** `ObsDescent.deltaDescend_blocked_of_witness`
  (`ObsDescent.lean:200`) — NEW this run, same four-point witness hypotheses.
- **Relation status.** `equivalent-under-H_struct`.

---

## Section C — descent of the difference map modulo a value-side equivalence (lines 145–219)

The native side collapses this entire layer to the equality layer through one
reduction lemma, `ObsDescent.classConstant_comp_mk_iff`
(`ObsDescent.lean:276`), plus the two named existence corollaries. That is a
*coverage* claim about statements, recorded row by row below — not a claim that
the supplied declarations were individually transcribed.

### 20. `DeltaCongruentMod` — def (lines 145–149)

**SUPPLIED_INPUT**
```lean
def DeltaCongruentMod (P : PrimitiveDifference α β) (S : Setoid β) : Prop :=
  ∀ x x' y y' : α,
    P.ZeroRel x x' →
    P.ZeroRel y y' →
    S.r (P.δ x y) (P.δ x' y')
```
- **Assumption graph.** Direct: items 1, 2. Closure: {1,2}. Extra data: a
  user-supplied setoid `S` on the value type (replacing equality).
- **Axiom report.** No report (not a theorem).
- **Neutral content.** Two-sided compatibility up to a value-side equivalence.
- **Native counterpart.** The right-hand side of
  `ObsDescent.deltaDescendMod_exists_iff` (`ObsDescent.lean:293`) — the same
  proposition, stated inline rather than named. **No separately named native
  definition**; naming it was judged unnecessary because
  `classConstant_comp_mk_iff` reduces it to the equality layer.
- **Relation status.** `equivalent-under-H_struct`.

### 21. `deltaFactorMod` — def (lines 151–161)

**SUPPLIED_INPUT**
```lean
def deltaFactorMod
    (P : PrimitiveDifference α β) (S : Setoid β)
    (hcongr : P.DeltaCongruentMod S) :
    P.ResidualQuotient → P.ResidualQuotient → Quotient S :=
  Quotient.lift₂
    (s₁ := zeroSetoid P)
    (s₂ := zeroSetoid P)
    (fun x y => Quotient.mk S (P.δ x y))
    (by
      intro x y x' y' hx hy
      exact Quotient.sound (hcongr x x' y y' hx hy))
```
- **Assumption graph.** Direct: items 7, 8, 20. Closure: {1,…,8, 20}. Explicit
  hypothesis: compatibility mod `S`. Metatheory: `Quotient.lift₂` on the
  carrier side, `Quotient.mk`/`Quotient.sound` on the value side.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** "Difference, then value-side class" descends to
  `Q → Q → β/S`.
- **Native counterpart.** The `mpr` witness inside
  `ObsDescent.deltaDescendMod_exists_iff` (declared at `ObsDescent.lean:293`;
  the `mpr` witness term itself at `:313–315`) — the
  same `Quotient.lift₂` term, supplied as the existential witness rather than
  as a top-level def.
- **Relation status.** `equivalent-under-H_struct`.

### 22. `deltaFactorMod_classOf_classOf` — theorem (lines 163–168)

**SUPPLIED_INPUT (statement)**
```lean
theorem deltaFactorMod_classOf_classOf
    (P : PrimitiveDifference α β) (S : Setoid β)
    (hcongr : P.DeltaCongruentMod S) (x y : α) :
    P.deltaFactorMod S hcongr (P.classOf x) (P.classOf y) =
      Quotient.mk S (P.δ x y) :=
  rfl
```
- **Assumption graph.** Direct: items 9, 21. Closure: {1,…,9, 20, 21}.
  Definitional proof.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.deltaFactorMod_classOf_classOf' depends on axioms: [Quot.sound]`
- **Neutral content.** Computation rule for the mod-`S` descended map.
- **Native counterpart.** The computation clause `fun _ _ => rfl` of the
  `mpr` witness in `ObsDescent.deltaDescendMod_exists_iff`
  (`ObsDescent.lean:315`). No separately named native declaration.
- **Relation status.** `equivalent-under-H_struct`.

### 23. `deltaFactorMod_requires_congruence` — theorem (lines 170–183)

**SUPPLIED_INPUT (statement)**
```lean
theorem deltaFactorMod_requires_congruence
    (P : PrimitiveDifference α β) (S : Setoid β)
    (F : P.ResidualQuotient → P.ResidualQuotient → Quotient S)
    (hF : ∀ x y : α,
      F (P.classOf x) (P.classOf y) = Quotient.mk S (P.δ x y)) :
    P.DeltaCongruentMod S := by
```
- **Assumption graph.** Direct: items 9, 10, 20. Closure: [CORE 1–10] ∪ {20}.
  Explicit hypotheses: `F`, `hF`. Metatheory: `Quotient.exact` on the value
  side.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.deltaFactorMod_requires_congruence' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** Necessity of mod-`S` compatibility.
- **Native counterpart.** `ObsDescent.deltaDescendMod_exists_iff`
  (`ObsDescent.lean:293`), **`.mp` direction**.
- **Relation status.** `equivalent-under-H_struct`.

### 24. `deltaFactorMod_exists_iff_deltaCongruentMod` — theorem (lines 185–197)

**SUPPLIED_INPUT (statement)**
```lean
theorem deltaFactorMod_exists_iff_deltaCongruentMod
    (P : PrimitiveDifference α β) (S : Setoid β) :
    (∃ F : P.ResidualQuotient → P.ResidualQuotient → Quotient S,
        ∀ x y : α,
          F (P.classOf x) (P.classOf y) = Quotient.mk S (P.δ x y))
      ↔ P.DeltaCongruentMod S := by
```
- **Assumption graph.** Direct: items 21, 22, 23. Closure: [CORE 1–10] ∪
  {20,21,22,23}.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.deltaFactorMod_exists_iff_deltaCongruentMod' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** Existence-iff-compatibility, mod-`S` binary version.
- **Native counterpart.** `ObsDescent.deltaDescendMod_exists_iff`
  (`ObsDescent.lean:293`) — NEW this run; identical statement with the
  compatibility side written out inline. Native axiom profile matches:
  `[propext, Quot.sound]`.
- **Relation status.** `equivalent-under-H_struct`.

### 25. `deltaFactorMod_no_factor_of_not_deltaCongruentMod` — theorem (lines 199–206)

**SUPPLIED_INPUT (statement)**
```lean
theorem deltaFactorMod_no_factor_of_not_deltaCongruentMod
    (P : PrimitiveDifference α β) (S : Setoid β)
    (hδ : ¬ P.DeltaCongruentMod S) :
    ¬ (∃ F : P.ResidualQuotient → P.ResidualQuotient → Quotient S,
        ∀ x y : α,
          F (P.classOf x) (P.classOf y) = Quotient.mk S (P.δ x y)) := by
```
- **Assumption graph.** Direct: item 24. Closure: [CORE 1–10] ∪ {20,…,24}.
  Explicit hypothesis: mod-`S` compatibility fails.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.deltaFactorMod_no_factor_of_not_deltaCongruentMod' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** Contrapositive packaging of item 24.
- **Native counterpart.** `ObsDescent.deltaDescendMod_exists_iff`
  (`ObsDescent.lean:293`) — **no separately named native declaration**;
  contrapositive, one step.
- **Relation status.** `equivalent-under-H_struct`.

### 26. `deltaFactorMod_no_factor_of_zeroRel_not_rel` — theorem (lines 208–219)

**SUPPLIED_INPUT (statement)**
```lean
theorem deltaFactorMod_no_factor_of_zeroRel_not_rel
    (P : PrimitiveDifference α β) (S : Setoid β)
    {x x' y y' : α}
    (hxx : P.ZeroRel x x') (hyy : P.ZeroRel y y')
    (hne : ¬ S.r (P.δ x y) (P.δ x' y')) :
    ¬ (∃ F : P.ResidualQuotient → P.ResidualQuotient → Quotient S,
        ∀ x y : α,
          F (P.classOf x) (P.classOf y) = Quotient.mk S (P.δ x y)) := by
```
- **Assumption graph.** Direct: items 2, 24. Closure: [CORE 1–10] ∪ {20,…,24}.
  Explicit hypotheses: a four-point witness with `S`-unrelated difference
  values.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.deltaFactorMod_no_factor_of_zeroRel_not_rel' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** Witness-based non-descent mod `S`.
- **Native counterpart.** `ObsDescent.deltaDescendMod_exists_iff`
  (`ObsDescent.lean:293`) contraposed at the witness — no separately named
  native declaration.
- **Relation status.** `equivalent-under-H_struct`.

---

## Section D — transport along a coarsening of the value-side equivalence (lines 221–263)

### 27. `quotientMapOfSetoidImp` — def (lines 221–228)

**SUPPLIED_INPUT**
```lean
def quotientMapOfSetoidImp
    (S T : Setoid γ) (hST : ∀ a b : γ, S.r a b → T.r a b) :
    Quotient S → Quotient T :=
  Quotient.lift
    (fun a => Quotient.mk T a)
    (by
      intro a b hab
      exact Quotient.sound (hST a b hab))
```
- **Assumption graph.** **No supplied dependencies** (closure = ∅): this
  declaration does not mention the core structure at all. Data: two setoids on
  a common type and a pointwise implication. Metatheory: `Quotient.lift`,
  `Quotient.sound`.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The canonical map between quotients induced by an
  inclusion of equivalence relations.
- **Native counterpart.** `ObsDescent.coarsenMap` (`ObsDescent.lean:261`) —
  NEW this run, identical term.
- **Relation status.** `equivalent-under-H_struct` (in fact independent of
  `H_struct`: neither side mentions the difference datum).

### 28. `quotientMapOfSetoidImp_mk` — theorem (lines 230–234)

**SUPPLIED_INPUT (statement)**
```lean
theorem quotientMapOfSetoidImp_mk
    (S T : Setoid γ) (hST : ∀ a b : γ, S.r a b → T.r a b)
    (a : γ) :
    quotientMapOfSetoidImp S T hST (Quotient.mk S a) = Quotient.mk T a :=
  rfl
```
- **Assumption graph.** Direct: item 27. Closure: {27}. Definitional proof.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.quotientMapOfSetoidImp_mk' depends on axioms: [Quot.sound]`
- **Neutral content.** The induced map commutes with the two projections.
- **Native counterpart.** `ObsDescent.coarsenMap_mk` (`ObsDescent.lean:267`),
  proved by `rfl` — NEW this run.
- **Relation status.** `equivalent-under-H_struct`.

### 29. `deltaCongruentMod_of_setoid_imp` — theorem (lines 236–242)

**SUPPLIED_INPUT (statement)**
```lean
theorem deltaCongruentMod_of_setoid_imp
    (P : PrimitiveDifference α β) (S T : Setoid β)
    (hST : ∀ a b : β, S.r a b → T.r a b)
    (hδ : P.DeltaCongruentMod S) :
    P.DeltaCongruentMod T := by
```
- **Assumption graph.** Direct: item 20. Closure: {1, 2, 20}. Explicit
  hypotheses: the coarsening implication and compatibility mod `S`. No
  quotient machinery.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.deltaCongruentMod_of_setoid_imp' does not depend on any axioms`
- **Neutral content.** Compatibility is monotone under coarsening the
  value-side equivalence.
- **Native counterpart.** Pointwise composition of the right-hand side of
  `ObsDescent.deltaDescendMod_exists_iff` (`ObsDescent.lean:293`) with the
  coarsening implication — a one-line consequence with **no separately named
  native declaration**. The unary analogue is named:
  `ObsDescent.descendMod_exists_of_coarsen` (`ObsDescent.lean:334`).
- **Relation status.** `equivalent-under-H_struct`.

### 30. `deltaFactorMod_exists_of_setoid_imp` — theorem (lines 244–263)

**SUPPLIED_INPUT (statement)**
```lean
theorem deltaFactorMod_exists_of_setoid_imp
    (P : PrimitiveDifference α β) (S T : Setoid β)
    (hST : ∀ a b : β, S.r a b → T.r a b) :
    (∃ F : P.ResidualQuotient → P.ResidualQuotient → Quotient S,
        ∀ x y : α,
          F (P.classOf x) (P.classOf y) = Quotient.mk S (P.δ x y)) →
      ∃ F : P.ResidualQuotient → P.ResidualQuotient → Quotient T,
        ∀ x y : α,
          F (P.classOf x) (P.classOf y) = Quotient.mk T (P.δ x y) := by
```
- **Assumption graph.** Direct: items 9, 27, 28. Closure: {1,…,9, 27, 28}.
  Explicit hypotheses: the coarsening implication and a mod-`S` factorization.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.deltaFactorMod_exists_of_setoid_imp' depends on axioms: [Quot.sound]`
- **Neutral content.** Factorizations transport along coarsening, by composing
  with the canonical map of item 27.
- **Native counterpart.** `ObsDescent.descendMod_exists_of_coarsen`
  (`ObsDescent.lean:334`) — NEW this run, stated in the **unary** form. The
  binary form is the same composition against
  `ObsDescent.deltaDescendMod_exists_iff`; no separately named binary native
  declaration.
- **Relation status.** `equivalent-under-H_struct`. **Hypothesis delta
  (recorded):** native names the unary transport, the supplied file names the
  binary one; each yields the other by the same `coarsenMap` composition.

---

## Section E — the all-zero countermodel on `Bool` (lines 265–295 and 740–755)

### 31. `boolAllZeroNonconstant` — def (lines 265–276)

**SUPPLIED_INPUT**
```lean
def boolAllZeroNonconstant : PrimitiveDifference Bool Bool where
  δ := fun x _ => x
  Zero := fun _ => True
  zero_refl := by
    intro x
    exact True.intro
  zero_symm := by
    intro x y hxy
    exact True.intro
  zero_trans := by
    intro x y z hxy hyz
    exact True.intro
```
- **Assumption graph.** Direct: item 1. Closure: {1}. Closed instance — no
  free parameters, no hypotheses.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** A difference datum on the booleans: the difference map
  returns its first argument; the zero-set is everything, so the induced
  relation is total and all points collapse into one class, yet the difference
  map is not constant.
- **Native counterpart.** `ObsDescent.collapseAllObs` (`ObsDescent.lean:437`)
  — NEW this run, same three data fields.
- **Relation status.** `instance-material` (identical instance, native
  vocabulary).

### 32. `boolAllZeroNonconstant_not_deltaCongruent` — theorem (lines 278–283)

**SUPPLIED_INPUT (statement)**
```lean
theorem boolAllZeroNonconstant_not_deltaCongruent :
    ¬ boolAllZeroNonconstant.DeltaCongruent := by
```
- **Assumption graph.** Direct: items 12, 31. Closure: {1, 2, 12, 31}. No
  hypotheses. Proof by constructor discrimination (`true = false` refuted) —
  no classical logic.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.boolAllZeroNonconstant_not_deltaCongruent' does not depend on any axioms`
- **Neutral content.** The all-zero instance violates two-sided compatibility.
- **Native counterpart.** `ObsDescent.collapseAllObs_not_deltaConstant`
  (`ObsDescent.lean:452`) — NEW this run; same discrimination
  (`Bool.noConfusion`), axiom-free.
- **Relation status.** `equivalent-under-H_struct`; evidence class
  COUNTERMODEL on both sides. Carrier size 2, **minimal**: on a subsingleton
  carrier every map is class-constant (`Subsingleton.elim`), so no descent
  obstruction can live below size 2 (METATHEORY).

### 33. `boolAllZeroNonconstant_no_factorization` — theorem (lines 285–295)

**SUPPLIED_INPUT (statement)**
```lean
theorem boolAllZeroNonconstant_no_factorization :
    ¬ (∃ F :
          boolAllZeroNonconstant.ResidualQuotient →
          boolAllZeroNonconstant.ResidualQuotient →
          Bool,
        ∀ x y : Bool,
          F (boolAllZeroNonconstant.classOf x)
            (boolAllZeroNonconstant.classOf y) =
          boolAllZeroNonconstant.δ x y) := by
```
- **Assumption graph.** Direct: items 18 (equivalently 16), 31, 32. Closure:
  [CORE 1–10] ∪ {12,…,16, 18, 31, 32}. No hypotheses.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.boolAllZeroNonconstant_no_factorization' depends on axioms: [Quot.sound]`
- **Neutral content.** Fully concrete negative existence: for the all-zero
  instance no factorization of the difference map through the quotient exists.
- **Native counterpart.** `ObsDescent.collapseAllObs_no_delta_descend`
  (`ObsDescent.lean:458`) — NEW this run, via
  `deltaDescend_exists_iff` at the instance.
- **Relation status.** `equivalent-under-H_struct`; COUNTERMODEL, carrier 2,
  minimal as in item 32.

### 34. `boolAllZeroNonconstant_classifier_not_invariantCongruent` — theorem (lines 740–745)

**SUPPLIED_INPUT (statement)**
```lean
theorem boolAllZeroNonconstant_classifier_not_invariantCongruent :
    ¬ boolAllZeroNonconstant.InvariantCongruent (fun x : Bool => x) := by
```
- **Assumption graph.** Direct: items 31, 36. Closure: {1, 2, 31, 36}. No
  hypotheses; constructor discrimination.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.boolAllZeroNonconstant_classifier_not_invariantCongruent' does not depend on any axioms`
- **Neutral content.** For the all-zero instance the identity observable is not
  constant on classes.
- **Native counterpart.** `ObsDescent.collapseAllObs_id_not_classConstant`
  (`ObsDescent.lean:469`) — NEW this run, axiom-free.
- **Relation status.** `equivalent-under-H_struct`; COUNTERMODEL, carrier 2,
  minimal as in item 32.

### 35. `boolAllZeroNonconstant_no_invariant_factorization` — theorem (lines 747–755)

**SUPPLIED_INPUT (statement)**
```lean
theorem boolAllZeroNonconstant_no_invariant_factorization :
    ¬ (∃ F : boolAllZeroNonconstant.ResidualQuotient → Bool,
        ∀ x : Bool,
          F (boolAllZeroNonconstant.classOf x) = x) := by
```
- **Assumption graph.** Direct: items 31, 34, 42 (equivalently 41). Closure:
  [CORE 1–10] ∪ {31, 34, 36, 37, 38, 40, 41, 42}. No hypotheses.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.boolAllZeroNonconstant_no_invariant_factorization' depends on axioms: [Quot.sound]`
- **Neutral content.** Concrete negative existence for observables: nothing on
  the one-class quotient recovers the two points.
- **Native counterpart.** `ObsDescent.collapseAllObs_no_view_descend`
  (`ObsDescent.lean:476`) — NEW this run.
- **Relation status.** `equivalent-under-H_struct`; COUNTERMODEL, carrier 2,
  minimal as in item 32. Cross-reference (METATHEORY): this is the observer
  incarnation of the sealed native raw-quotient barrier
  `Derivation.quot_barrier` (`lean4/Derivation/Quot.lean:23`), which is
  strictly more general — it needs no setoid.

---

## Section F — observable descent, equality version (lines 297–369)

### 36. `InvariantCongruent` — def (lines 297–298)

**SUPPLIED_INPUT**
```lean
def InvariantCongruent (P : PrimitiveDifference α β) (φ : α → γ) : Prop :=
  ∀ x y : α, P.ZeroRel x y → φ x = φ y
```
- **Assumption graph.** Direct: items 1, 2. Closure: {1,2}. Extra data: an
  observable `φ` into an arbitrary target. Metatheory: equality on the target.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The observable is constant on classes of the induced
  relation.
- **Native counterpart.** `ObsDescent.ClassConstant` (`ObsDescent.lean:104`) —
  NEW this run.
- **Relation status.** `equivalent-under-H_struct`.

### 37. `invariantFactor` — def (lines 300–309)

**SUPPLIED_INPUT**
```lean
def invariantFactor
    (P : PrimitiveDifference α β) (φ : α → γ)
    (hcongr : P.InvariantCongruent φ) :
    P.ResidualQuotient → γ :=
  Quotient.lift
    (s := zeroSetoid P)
    φ
    (by
      intro x y hxy
      exact hcongr x y hxy)
```
- **Assumption graph.** Direct: items 7, 8, 36. Closure: {1,…,8, 36}. Explicit
  hypothesis: class-constancy. Metatheory: `Quotient.lift`.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** A class-constant observable descends to the quotient.
- **Native counterpart.** `ObsDescent.descend` (`ObsDescent.lean:108`) — NEW
  this run, identical term.
- **Relation status.** `equivalent-under-H_struct`.

### 38. `invariantFactor_classOf` — theorem (lines 311–315)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantFactor_classOf
    (P : PrimitiveDifference α β) (φ : α → γ)
    (hcongr : P.InvariantCongruent φ) (x : α) :
    P.invariantFactor φ hcongr (P.classOf x) = φ x :=
  rfl
```
- **Assumption graph.** Direct: items 9, 37. Closure: {1,…,9, 36, 37}.
  Definitional proof.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantFactor_classOf' does not depend on any axioms`
- **Neutral content.** Computation rule for the descended observable.
- **Native counterpart.** `ObsDescent.descend_mk` (`ObsDescent.lean:113`),
  proved by `rfl` — NEW this run; axiom profiles match (axiom-free).
- **Relation status.** `equivalent-under-H_struct`.

### 39. `invariantFactor_unique` — theorem (lines 317–327)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantFactor_unique
    (P : PrimitiveDifference α β) (φ : α → γ)
    (hcongr : P.InvariantCongruent φ)
    (F : P.ResidualQuotient → γ)
    (hF : ∀ x : α, F (P.classOf x) = φ x) :
    F = P.invariantFactor φ hcongr := by
```
- **Assumption graph.** Direct: items 9, 37, 38. Closure: {1,…,9, 36, 37, 38}.
  Explicit hypotheses: `hcongr`, `F`, `hF`. Metatheory: `funext`,
  `Quotient.inductionOn`.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantFactor_unique' depends on axioms: [Quot.sound]`
- **Neutral content.** Uniqueness of the observable's factorization, stated
  against the canonical lift.
- **Native counterpart.** `ObsDescent.descend_unique`
  (`ObsDescent.lean:134`) — NEW this run, **symmetric two-map form**.
- **Relation status.** `equivalent-under-H_struct`. **Hypothesis delta
  (recorded):** as in item 17 — supplied pins one side to the canonical lift;
  the forms are inter-derivable given `ObsDescent.descend_mk`. Scope note
  (METATHEORY): this uniqueness is **global**, and the reason is exactly that
  the projection is epi — `ObsDescent.obsQuotient_mk_surjective`
  (`ObsDescent.lean:96`). The native *presentation* uniqueness in
  `Compression` is image-scoped (`Compression.factor_unique_on_image`,
  `Compression.factor_not_unique_off_image`); the difference is precisely
  codomain coverage by the projection, nothing more.

### 40. `invariantFactor_requires_congruence` — theorem (lines 329–339)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantFactor_requires_congruence
    (P : PrimitiveDifference α β) (φ : α → γ)
    (F : P.ResidualQuotient → γ)
    (hF : ∀ x : α, F (P.classOf x) = φ x) :
    P.InvariantCongruent φ := by
```
- **Assumption graph.** Direct: items 9, 10, 36. Closure: [CORE 1–10] ∪ {36}.
  Explicit hypotheses: `F`, `hF`.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantFactor_requires_congruence' depends on axioms: [Quot.sound]`
- **Neutral content.** Necessity: any factorization forces class-constancy.
- **Native counterpart.** `ObsDescent.descend_exists_iff`
  (`ObsDescent.lean:119`), **`.mp` direction**.
- **Relation status.** `equivalent-under-H_struct`.

### 41. `invariantFactor_exists_iff_invariantCongruent` — theorem (lines 341–351)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantFactor_exists_iff_invariantCongruent
    (P : PrimitiveDifference α β) (φ : α → γ) :
    (∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = φ x)
      ↔ P.InvariantCongruent φ := by
```
- **Assumption graph.** Direct: items 37, 38, 40. Closure: [CORE 1–10] ∪
  {36, 37, 38, 40}.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent' depends on axioms: [Quot.sound]`
- **Neutral content.** Existence-iff-compatibility for observables — the
  universal-property core for unary maps.
- **Native counterpart.** `ObsDescent.descend_exists_iff`
  (`ObsDescent.lean:119`) — NEW this run.
- **Relation status.** `equivalent-under-H_struct`.

### 42. `invariantFactor_no_factor_of_not_invariant` — theorem (lines 353–359)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantFactor_no_factor_of_not_invariant
    (P : PrimitiveDifference α β) (φ : α → γ)
    (hφ : ¬ P.InvariantCongruent φ) :
    ¬ (∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = φ x) := by
```
- **Assumption graph.** Direct: item 41. Closure: [CORE 1–10] ∪
  {36, 37, 38, 40, 41}. Explicit hypothesis: class-constancy fails.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantFactor_no_factor_of_not_invariant' depends on axioms: [Quot.sound]`
- **Neutral content.** Contrapositive packaging of item 41.
- **Native counterpart.** `ObsDescent.descend_exists_iff`
  (`ObsDescent.lean:119`) — **no separately named native declaration**;
  contrapositive, one step.
- **Relation status.** `equivalent-under-H_struct`.

### 43. `invariantFactor_no_factor_of_zeroRel_ne` — theorem (lines 361–369)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantFactor_no_factor_of_zeroRel_ne
    (P : PrimitiveDifference α β) (φ : α → γ)
    {x y : α} (hxy : P.ZeroRel x y) (hne : φ x ≠ φ y) :
    ¬ (∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = φ x) := by
```
- **Assumption graph.** Direct: items 2, 41. Closure: [CORE 1–10] ∪
  {36, 37, 38, 40, 41}. Explicit hypotheses: a two-point witness — related
  points with different observable values.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantFactor_no_factor_of_zeroRel_ne' depends on axioms: [Quot.sound]`
- **Neutral content.** Witness-based non-descent for observables.
- **Native counterpart.** `ObsDescent.descend_blocked_of_witness`
  (`ObsDescent.lean:142`) — NEW this run, same two-point witness hypotheses.
- **Relation status.** `equivalent-under-H_struct`.

---

## Section G — pairing of observables and the two-observable obstruction (lines 371–473)

### 44. `invariantCongruent_pair_iff` — theorem (lines 371–383)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantCongruent_pair_iff
    (P : PrimitiveDifference α β) (φ : α → γ) (ψ : α → η) :
    P.InvariantCongruent (fun x : α => (φ x, ψ x)) ↔
      P.InvariantCongruent φ ∧ P.InvariantCongruent ψ := by
```
- **Assumption graph.** Direct: item 36. Closure: {1, 2, 36}. Extra data: two
  observables into possibly different targets. Metatheory: product types,
  `Prod.ext`. No quotient.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantCongruent_pair_iff' does not depend on any axioms`
- **Neutral content.** The paired observable is class-constant iff both
  components are.
- **Native counterpart.** `ObsDescent.classConstant_pair_iff`
  (`ObsDescent.lean:212`) — NEW this run; native proof uses
  `congrArg Prod.fst/snd`, also axiom-free.
- **Relation status.** `equivalent-under-H_struct`.

### 45. `invariantFactor_pair_exists_iff` — theorem (lines 385–392)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantFactor_pair_exists_iff
    (P : PrimitiveDifference α β) (φ : α → γ) (ψ : α → η) :
    (∃ F : P.ResidualQuotient → γ × η,
        ∀ x : α, F (P.classOf x) = (φ x, ψ x))
      ↔ P.InvariantCongruent φ ∧ P.InvariantCongruent ψ :=
```
- **Assumption graph.** Direct: items 41, 44. Closure: [CORE 1–10] ∪
  {36, 37, 38, 40, 41, 44}.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantFactor_pair_exists_iff' depends on axioms: [Quot.sound]`
- **Neutral content.** A joint pair-valued factorization exists iff both
  components are class-constant.
- **Native counterpart.** `ObsDescent.descend_exists_iff`
  (`ObsDescent.lean:119`) composed with `ObsDescent.classConstant_pair_iff`
  (`ObsDescent.lean:212`); the existence-side statement is
  `ObsDescent.pair_descend_exists_iff` (`ObsDescent.lean:225`). No separately
  named native declaration for this exact chaining (it is `Iff.trans` of two
  named theorems).
- **Relation status.** `equivalent-under-H_struct`.

### 46. `invariantFactor_pair_exists_iff_component_factors` — theorem (lines 394–412)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantFactor_pair_exists_iff_component_factors
    (P : PrimitiveDifference α β) (φ : α → γ) (ψ : α → η) :
    (∃ F : P.ResidualQuotient → γ × η,
        ∀ x : α, F (P.classOf x) = (φ x, ψ x))
      ↔
        (∃ Fφ : P.ResidualQuotient → γ,
          ∀ x : α, Fφ (P.classOf x) = φ x) ∧
        (∃ Fψ : P.ResidualQuotient → η,
          ∀ x : α, Fψ (P.classOf x) = ψ x) := by
```
- **Assumption graph.** Direct: items 41, 44. Closure: [CORE 1–10] ∪
  {36, 37, 38, 40, 41, 44}.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantFactor_pair_exists_iff_component_factors' depends on axioms: [Quot.sound]`
- **Neutral content.** Joint factorization exists iff each component
  factorization exists: existence distributes over pairing.
- **Native counterpart.** `ObsDescent.pair_descend_exists_iff`
  (`ObsDescent.lean:225`) — NEW this run, statement-for-statement.
- **Relation status.** `equivalent-under-H_struct`.

### 47. `invariantPair_no_factor_of_left_not_invariant` — theorem (lines 414–420)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantPair_no_factor_of_left_not_invariant
    (P : PrimitiveDifference α β) (φ : α → γ) (ψ : α → η)
    (hφ : ¬ P.InvariantCongruent φ) :
    ¬ (∃ F : P.ResidualQuotient → γ × η,
        ∀ x : α, F (P.classOf x) = (φ x, ψ x)) := by
```
- **Assumption graph.** Direct: item 45/46. Closure: [CORE 1–10] ∪
  {36, 37, 38, 40, 41, 44, 45, 46}. Explicit hypothesis: the first component
  fails class-constancy.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantPair_no_factor_of_left_not_invariant' depends on axioms: [Quot.sound]`
- **Neutral content.** Left-component failure blocks the joint factorization.
- **Native counterpart.** `ObsDescent.pair_descend_exists_iff`
  (`ObsDescent.lean:225`) with `ObsDescent.descend_exists_iff`
  (`ObsDescent.lean:119`) — **no separately named native declaration**;
  contrapositive on the left conjunct, one step.
- **Relation status.** `equivalent-under-H_struct`.

### 48. `invariantPair_no_factor_of_right_not_invariant` — theorem (lines 422–428)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantPair_no_factor_of_right_not_invariant
    (P : PrimitiveDifference α β) (φ : α → γ) (ψ : α → η)
    (hψ : ¬ P.InvariantCongruent ψ) :
    ¬ (∃ F : P.ResidualQuotient → γ × η,
        ∀ x : α, F (P.classOf x) = (φ x, ψ x)) := by
```
- **Assumption graph.** Direct: item 45/46. Closure: as item 47. Explicit
  hypothesis: the second component fails class-constancy.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantPair_no_factor_of_right_not_invariant' depends on axioms: [Quot.sound]`
- **Neutral content.** Right-component failure blocks the joint factorization.
- **Native counterpart.** `ObsDescent.pair_descend_exists_iff`
  (`ObsDescent.lean:225`) — no separately named native declaration;
  contrapositive on the right conjunct. The witness-form specialization *is*
  named: `ObsDescent.view_descends_pair_blocked` (`ObsDescent.lean:248`),
  second conjunct.
- **Relation status.** `equivalent-under-H_struct`.

### 49. `not_invariantCongruent_of_zeroRel_ne` — theorem (lines 430–435)

**SUPPLIED_INPUT (statement)**
```lean
theorem not_invariantCongruent_of_zeroRel_ne
    (P : PrimitiveDifference α β) (φ : α → γ)
    {x y : α} (hxy : P.ZeroRel x y) (hne : φ x ≠ φ y) :
    ¬ P.InvariantCongruent φ := by
```
- **Assumption graph.** Direct: item 36. Closure: {1, 2, 36}. Explicit
  hypotheses: a two-point witness. No quotient machinery.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.not_invariantCongruent_of_zeroRel_ne' does not depend on any axioms`
- **Neutral content.** A two-point witness refutes class-constancy.
- **Native counterpart.** The witness step inside
  `ObsDescent.descend_blocked_of_witness` (`ObsDescent.lean:142`,
  `fun h => hne (… h x y hxy)`) — **no separately named native declaration**;
  the native module states the blocking form directly rather than factoring
  out this one-liner.
- **Relation status.** `equivalent-under-H_struct`.

### 50. `localGreenGlobalRed_pair_obstruction` — theorem (lines 437–447)

**SUPPLIED_INPUT (statement)**
```lean
theorem localGreenGlobalRed_pair_obstruction
    (P : PrimitiveDifference α β) (φ : α → γ) (ψ : α → η)
    (hφ : P.InvariantCongruent φ)
    (hψ : ¬ P.InvariantCongruent ψ) :
    (∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = φ x) ∧
      ¬ (∃ F : P.ResidualQuotient → γ × η,
        ∀ x : α, F (P.classOf x) = (φ x, ψ x)) := by
```
- **Assumption graph.** Direct: items 41 (`.mpr`), 48. Closure: [CORE 1–10] ∪
  {36, 37, 38, 40, 41, 44, 45, 46, 48}. Explicit hypotheses: `φ`
  class-constant; `ψ` not class-constant.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.localGreenGlobalRed_pair_obstruction' depends on axioms: [Quot.sound]`
- **Neutral content.** One observable descends alone while the pair with a
  non-class-constant second observable does not — a conjunction of item 41's
  `mpr` and item 48. (The declaration name carries an interpretive slogan; the
  slogan is *not* evidence and is not imported. The formal content is exactly
  the stated conjunction and is correctly proved — gap row G20.)
- **Native counterpart.** `ObsDescent.view_descends_pair_blocked`
  (`ObsDescent.lean:248`), **negation-hypothesis variant**: the native theorem
  is stated in witness form (`hxy : ZeroRel O x y`, `hg : g x ≠ g y`); the
  supplied negation-hypothesis form follows from
  `ObsDescent.pair_descend_exists_iff` + `ObsDescent.descend_exists_iff` in one
  step. No separately named native declaration for the negation-hypothesis
  form.
- **Relation status.** `equivalent-under-H_struct`. **Hypothesis delta
  (recorded):** witness form (native, constructively primary) vs
  negation-of-class-constancy form (supplied); the witness form implies the
  negation form by item 49's content, the reverse needs no extra input beyond
  `descend_exists_iff`.

### 51. `localGreenGlobalRed_pair_obstruction_of_witness` — theorem (lines 449–458)

**SUPPLIED_INPUT (statement)**
```lean
theorem localGreenGlobalRed_pair_obstruction_of_witness
    (P : PrimitiveDifference α β) (φ : α → γ) (ψ : α → η)
    (hφ : P.InvariantCongruent φ)
    {x y : α} (hxy : P.ZeroRel x y) (hne : ψ x ≠ ψ y) :
    (∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = φ x) ∧
      ¬ (∃ F : P.ResidualQuotient → γ × η,
        ∀ x : α, F (P.classOf x) = (φ x, ψ x)) := by
```
- **Assumption graph.** Direct: items 49, 50. Closure: closure(50) ∪ {49, 50}.
  Explicit hypotheses: `φ` class-constant plus a two-point witness for `ψ`.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.localGreenGlobalRed_pair_obstruction_of_witness' depends on axioms: [Quot.sound]`
- **Neutral content.** Same conjunction with the failure hypothesis replaced by
  a concrete witness.
- **Native counterpart.** `ObsDescent.view_descends_pair_blocked`
  (`ObsDescent.lean:248`) — NEW this run, **exact hypothesis match**
  (`hf : ClassConstant O f`, `hxy : ZeroRel O x y`, `hg : g x ≠ g y`). This is
  the direct native counterpart of the supplied flagship shape.
- **Relation status.** `equivalent-under-H_struct`.

### 52. `localGreenGlobalRed_pair_witness_and_obstruction` — theorem (lines 460–473)

**SUPPLIED_INPUT (statement)**
```lean
theorem localGreenGlobalRed_pair_witness_and_obstruction
    (P : PrimitiveDifference α β) (φ : α → γ) (ψ : α → η)
    (hφ : P.InvariantCongruent φ)
    {x y : α} (hxy : P.ZeroRel x y) (hne : ψ x ≠ ψ y) :
    φ x = φ y ∧
      (φ x, ψ x) ≠ (φ y, ψ y) ∧
      (∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = φ x) ∧
      ¬ (∃ F : P.ResidualQuotient → γ × η,
        ∀ x : α, F (P.classOf x) = (φ x, ψ x)) := by
```
- **Assumption graph.** Direct: items 36, 51. Closure: closure(51) ∪ {51}.
  Same hypotheses as item 51.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.localGreenGlobalRed_pair_witness_and_obstruction' depends on axioms: [Quot.sound]`
- **Neutral content.** Four-part conjunction: the witness pair agrees under the
  first observable, disagrees as a pair, the first observable factors, the pair
  does not.
- **Native counterpart.** `ObsDescent.view_descends_pair_blocked`
  (`ObsDescent.lean:248`) for the last two conjuncts; the first conjunct is
  `hf x y hxy` (the class-constancy hypothesis applied to the witness) and the
  second is `fun he => hg (congrArg Prod.snd he)`, which appears verbatim
  inside the native proof. **No separately named native declaration** for the
  four-part packaging.
- **Relation status.** `equivalent-under-H_struct`.

---

## Section H — context-tagged construction (lines 475–530)

### 53. `contextFingerprintPD` — def (lines 475–487)

**SUPPLIED_INPUT**
```lean
def contextFingerprintPD (κ : Type z) (φ : α → γ) :
    PrimitiveDifference (κ × α) Prop where
  δ := fun x y => φ x.2 = φ y.2
  Zero := fun h => h
  zero_refl := by
    intro x
    rfl
  zero_symm := by
    intro _ _ h
    exact h.symm
  zero_trans := by
    intro _ _ _ hxy hyz
    exact hxy.trans hyz
```
- **Assumption graph.** Direct: item 1. Closure: {1}. Data: a tag type and an
  observable. **The only place in the supplied file where the value type is
  `Prop`** (FINITE_COMPUTATION).
- **Axiom report.** No report (not a theorem).
- **Neutral content.** A difference datum on the tagged carrier whose
  difference value is the *proposition* that the untagged components have equal
  observable values; the zero-set is propositional truth. The induced relation
  ignores tags entirely.
- **Native counterpart.** `DiffInterface.kernelObs` (`DiffInterface.lean:54`)
  applied to the tag-forgetting view, as recorded by
  `ObsDescent.tag_view_zeroRel` (`ObsDescent.lean:350`), which proves
  `ZeroRel (kernelObs fun p : K × X => φ p.2) s t ↔ φ s.2 = φ t.2` by
  `Iff.rfl`.
- **Relation status.** `same-third-notion`. The third notion is the induced
  relation "equal fingerprints under the reference observable". The two
  presentations differ in **value type only** — supplied `Prop` with the
  identity predicate as zero-set, native the ordered pair of views with
  equality as zero-set; the induced relations agree *definitionally*
  (`Iff.rfl`). Neither value presentation is a specialization of the other, so
  this is not an implication row.

### 54. `contextLocal` — def (lines 489–490)

**SUPPLIED_INPUT**
```lean
def contextLocal (φ : α → γ) (x : κ × α) : γ :=
  φ x.2
```
- **Assumption graph.** **No supplied dependencies** (closure = ∅). Metatheory:
  product projection.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The tag-forgetting observable induced by `φ`.
- **Native counterpart.** `fun p : K × X => φ p.2` — plain function
  composition, exactly the argument of `kernelObs` in
  `ObsDescent.tag_view_zeroRel` (`ObsDescent.lean:350`). **No native
  declaration was coined**, because naming a projection composite adds nothing
  formal.
- **Relation status.** `equivalent-under-H_struct` (definitionally the same
  function; independent of `H_struct` in fact).

### 55. `contextGlobal` — def (lines 492–493)

**SUPPLIED_INPUT**
```lean
def contextGlobal (ψ : α → η) (x : κ × α) : η :=
  ψ x.2
```
- **Assumption graph.** No supplied dependencies (closure = ∅).
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The same construction for a second observable.
- **Native counterpart.** `fun p : K × X => ψ p.2`, the second component
  argument in `ObsDescent.view_descends_pair_blocked` when instantiated at the
  tag observer. No native declaration coined, same reason as item 54.
- **Relation status.** `equivalent-under-H_struct`.

### 56. `contextFingerprint_invariant` — theorem (lines 495–499)

**SUPPLIED_INPUT (statement)**
```lean
theorem contextFingerprint_invariant (φ : α → γ) :
    (contextFingerprintPD κ φ).InvariantCongruent
      (contextLocal (κ := κ) φ) := by
```
- **Assumption graph.** Direct: items 2, 36, 53, 54. Closure: {1, 2, 36, 53,
  54}. No hypotheses; the induced relation *is* the equality of fingerprints,
  so the proof is the identity.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.contextFingerprint_invariant' does not depend on any axioms`
- **Neutral content.** On the tagged datum the tag-forgetting observable is
  class-constant.
- **Native counterpart.** `ObsDescent.tag_view_zeroRel`
  (`ObsDescent.lean:350`) `.mp`, which *is* the class-constancy statement for
  the tag-forgetting view (`ClassConstant (kernelObs …) (fun p => φ p.2)`
  unfolds to it). No separately named native declaration.
- **Relation status.** `equivalent-under-H_struct`.

### 57. `context_witness_zero_related` — theorem (lines 501–504)

**SUPPLIED_INPUT**
```lean
theorem context_witness_zero_related
    (φ : α → γ) {x y : α} (c₀ c₁ : κ) (hφxy : φ x = φ y) :
    (contextFingerprintPD κ φ).ZeroRel (c₀, x) (c₁, y) :=
  hφxy
```
- **Assumption graph.** Direct: items 2, 53. Closure: {1, 2, 53}. Explicit
  hypotheses: two tags and an equality of observable values. Proof is the
  identity.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.context_witness_zero_related' does not depend on any axioms`
- **Neutral content.** Two tagged points with equal observable values are
  related regardless of tags.
- **Native counterpart.** `ObsDescent.tag_view_zeroRel`
  (`ObsDescent.lean:350`) `.mpr` — no separately named native declaration
  (both directions live in one `Iff.rfl`).
- **Relation status.** `equivalent-under-H_struct`.

### 58. `context_global_differs` — theorem (lines 506–510)

**SUPPLIED_INPUT**
```lean
theorem context_global_differs
    (ψ : α → η) {x y : α} (c₀ c₁ : κ) (hne : ψ x ≠ ψ y) :
    contextGlobal (κ := κ) ψ (c₀, x) ≠
      contextGlobal (κ := κ) ψ (c₁, y) :=
  hne
```
- **Assumption graph.** Direct: item 55. Closure: {55}. Explicit hypothesis: a
  separating pair for the second observable. Proof is the identity.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.context_global_differs' does not depend on any axioms`
- **Neutral content.** If the second observable separates two points, the
  induced tagged observable separates their tagged versions.
- **Native counterpart.** The `hg : g x ≠ g y` hypothesis slot of
  `ObsDescent.view_descends_pair_blocked` (`ObsDescent.lean:248`), instantiated
  at the tag observer — **no separately named native declaration**, since the
  statement is definitionally its own hypothesis.
- **Relation status.** `equivalent-under-H_struct`.

### 59. `localGreenGlobalRed_context_obstruction_of_witness` — theorem (lines 512–530)

**SUPPLIED_INPUT (statement)**
```lean
theorem localGreenGlobalRed_context_obstruction_of_witness
    (φ : α → γ) (ψ : α → η)
    {x y : α} (c₀ c₁ : κ)
    (hφxy : φ x = φ y) (hne : ψ x ≠ ψ y) :
    (∃ F : (contextFingerprintPD κ φ).ResidualQuotient → γ,
        ∀ s : κ × α,
          F ((contextFingerprintPD κ φ).classOf s) =
            contextLocal (κ := κ) φ s) ∧
      ¬ (∃ F : (contextFingerprintPD κ φ).ResidualQuotient → γ × η,
        ∀ s : κ × α,
          F ((contextFingerprintPD κ φ).classOf s) =
            (contextLocal (κ := κ) φ s, contextGlobal (κ := κ) ψ s)) := by
```
- **Assumption graph.** Direct: items 51, 53, 54, 55, 56, 57, 58. Closure:
  closure(51) ∪ {51, 53, 54, 55, 56, 57, 58}. Explicit hypotheses: two
  observables, two tags, a two-point witness where `φ` agrees and `ψ`
  separates.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.localGreenGlobalRed_context_obstruction_of_witness' depends on axioms: [Quot.sound]`
- **Neutral content.** The flagship shape instantiated at the tagged datum:
  the fingerprint observable factors through the quotient, the pair with any
  separating second observable does not.
- **Native counterpart.** `ObsDescent.view_descends_pair_blocked`
  (`ObsDescent.lean:248`) instantiated at `kernelObs (fun p => φ p.2)`, with
  the zero-pair supplied by `ObsDescent.tag_view_zeroRel`
  (`ObsDescent.lean:350`). No separately named native instantiation.
- **Relation status.** `equivalent-under-H_struct`.

---

## Section I — observable descent modulo a target-side equivalence (lines 532–623)

### 60. `InvariantCongruentMod` — def (lines 532–534)

**SUPPLIED_INPUT**
```lean
def InvariantCongruentMod
    (P : PrimitiveDifference α β) (φ : α → γ) (S : Setoid γ) : Prop :=
  ∀ x y : α, P.ZeroRel x y → S.r (φ x) (φ y)
```
- **Assumption graph.** Direct: items 1, 2. Closure: {1, 2}. Extra data: a
  setoid on the observable's target.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The observable is constant on classes up to a
  target-side equivalence.
- **Native counterpart.** The right-hand side of
  `ObsDescent.descendMod_exists_iff` (`ObsDescent.lean:284`), and the
  right-hand side of the reduction lemma
  `ObsDescent.classConstant_comp_mk_iff` (`ObsDescent.lean:276`). No separately
  named native definition — deliberately, because the reduction lemma shows
  this notion *is* `ClassConstant O (Quotient.mk S ∘ f)`.
- **Relation status.** `equivalent-under-H_struct`.

### 61. `invariantFactorMod` — def (lines 536–545)

**SUPPLIED_INPUT**
```lean
def invariantFactorMod
    (P : PrimitiveDifference α β) (φ : α → γ) (S : Setoid γ)
    (hcongr : P.InvariantCongruentMod φ S) :
    P.ResidualQuotient → Quotient S :=
  Quotient.lift
    (s := zeroSetoid P)
    (fun x => Quotient.mk S (φ x))
    (by
      intro x y hxy
      exact Quotient.sound (hcongr x y hxy))
```
- **Assumption graph.** Direct: items 7, 8, 60. Closure: {1,…,8, 60}. Explicit
  hypothesis: mod-`S` class-constancy.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** "Observable, then target-side class" descends to
  `Q → γ/S`.
- **Native counterpart.** `ObsDescent.descend` (`ObsDescent.lean:108`) applied
  to `fun x => Quotient.mk S (f x)`, with class-constancy supplied by
  `ObsDescent.classConstant_comp_mk_iff` (`ObsDescent.lean:276`) — this is
  precisely the `mpr` witness of `ObsDescent.descendMod_exists_iff`
  (`ObsDescent.lean:284`).
- **Relation status.** `equivalent-under-H_struct`.

### 62. `invariantFactorMod_classOf` — theorem (lines 547–552)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantFactorMod_classOf
    (P : PrimitiveDifference α β) (φ : α → γ) (S : Setoid γ)
    (hcongr : P.InvariantCongruentMod φ S) (x : α) :
    P.invariantFactorMod φ S hcongr (P.classOf x) =
      Quotient.mk S (φ x) :=
  rfl
```
- **Assumption graph.** Direct: items 9, 61. Closure: {1,…,9, 60, 61}.
  Definitional proof.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantFactorMod_classOf' depends on axioms: [Quot.sound]`
- **Neutral content.** Computation rule for the mod-`S` descended observable.
- **Native counterpart.** `ObsDescent.descend_mk` (`ObsDescent.lean:113`) at
  `fun x => Quotient.mk S (f x)`; equivalently the `fun _ => rfl` clause of the
  `mpr` witness of `ObsDescent.descendMod_exists_iff`. No separately named
  native declaration.
- **Relation status.** `equivalent-under-H_struct`.

### 63. `invariantFactorMod_requires_congruence` — theorem (lines 554–565)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantFactorMod_requires_congruence
    (P : PrimitiveDifference α β) (φ : α → γ) (S : Setoid γ)
    (F : P.ResidualQuotient → Quotient S)
    (hF : ∀ x : α, F (P.classOf x) = Quotient.mk S (φ x)) :
    P.InvariantCongruentMod φ S := by
```
- **Assumption graph.** Direct: items 9, 10, 60. Closure: [CORE 1–10] ∪ {60}.
  Explicit hypotheses: `F`, `hF`. Metatheory: `Quotient.exact` on the target
  side.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantFactorMod_requires_congruence' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** Necessity of mod-`S` class-constancy.
- **Native counterpart.** `ObsDescent.descendMod_exists_iff`
  (`ObsDescent.lean:284`), **`.mp` direction**; the value-side effectiveness
  step is isolated as `ObsDescent.classConstant_comp_mk_iff`
  (`ObsDescent.lean:276`).
- **Relation status.** `equivalent-under-H_struct`.

### 64. `invariantFactorMod_exists_iff_invariantCongruentMod` — theorem (lines 567–578)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantFactorMod_exists_iff_invariantCongruentMod
    (P : PrimitiveDifference α β) (φ : α → γ) (S : Setoid γ) :
    (∃ F : P.ResidualQuotient → Quotient S,
        ∀ x : α, F (P.classOf x) = Quotient.mk S (φ x))
      ↔ P.InvariantCongruentMod φ S := by
```
- **Assumption graph.** Direct: items 61, 62, 63. Closure: [CORE 1–10] ∪
  {60, 61, 62, 63}.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantFactorMod_exists_iff_invariantCongruentMod' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** Existence-iff-compatibility for observables, mod-`S`.
- **Native counterpart.** `ObsDescent.descendMod_exists_iff`
  (`ObsDescent.lean:284`) — NEW this run, proved as
  `(descend_exists_iff …).trans (classConstant_comp_mk_iff …)`. Native axiom
  profile matches: `[propext, Quot.sound]`.
- **Relation status.** `equivalent-under-H_struct`.

### 65. `invariantFactorMod_no_factor_of_not_invariantCongruentMod` — theorem (lines 580–586)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantFactorMod_no_factor_of_not_invariantCongruentMod
    (P : PrimitiveDifference α β) (φ : α → γ) (S : Setoid γ)
    (hφ : ¬ P.InvariantCongruentMod φ S) :
    ¬ (∃ F : P.ResidualQuotient → Quotient S,
        ∀ x : α, F (P.classOf x) = Quotient.mk S (φ x)) := by
```
- **Assumption graph.** Direct: item 64. Closure: [CORE 1–10] ∪ {60,…,64}.
  Explicit hypothesis: mod-`S` class-constancy fails.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantFactorMod_no_factor_of_not_invariantCongruentMod' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** Contrapositive packaging of item 64.
- **Native counterpart.** `ObsDescent.descendMod_exists_iff`
  (`ObsDescent.lean:284`) — **no separately named native declaration**;
  contrapositive, one step.
- **Relation status.** `equivalent-under-H_struct`.

### 66. `invariantFactorMod_no_factor_of_zeroRel_not_rel` — theorem (lines 588–596)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantFactorMod_no_factor_of_zeroRel_not_rel
    (P : PrimitiveDifference α β) (φ : α → γ) (S : Setoid γ)
    {x y : α} (hxy : P.ZeroRel x y) (hne : ¬ S.r (φ x) (φ y)) :
    ¬ (∃ F : P.ResidualQuotient → Quotient S,
        ∀ x : α, F (P.classOf x) = Quotient.mk S (φ x)) := by
```
- **Assumption graph.** Direct: items 2, 64. Closure: [CORE 1–10] ∪ {60,…,64}.
  Explicit hypotheses: a two-point witness `S`-unrelated on the target.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantFactorMod_no_factor_of_zeroRel_not_rel' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** Witness-based non-descent mod `S`.
- **Native counterpart.** `ObsDescent.descendMod_exists_iff`
  (`ObsDescent.lean:284`) contraposed at the witness; equivalently
  `ObsDescent.descend_blocked_of_witness` (`ObsDescent.lean:142`) at
  `Quotient.mk S ∘ f` with the inequality supplied by
  `ObsDescent.classConstant_comp_mk_iff`. No separately named native
  declaration.
- **Relation status.** `equivalent-under-H_struct`.

### 67. `invariantCongruentMod_of_setoid_imp` — theorem (lines 598–604)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantCongruentMod_of_setoid_imp
    (P : PrimitiveDifference α β) (φ : α → γ) (S T : Setoid γ)
    (hST : ∀ a b : γ, S.r a b → T.r a b)
    (hφ : P.InvariantCongruentMod φ S) :
    P.InvariantCongruentMod φ T := by
```
- **Assumption graph.** Direct: item 60. Closure: {1, 2, 60}. Explicit
  hypotheses: the coarsening implication and mod-`S` class-constancy. No
  quotient machinery.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantCongruentMod_of_setoid_imp' does not depend on any axioms`
- **Neutral content.** Mod-class-constancy is monotone under coarsening the
  target-side equivalence.
- **Native counterpart.** Pointwise composition of the right-hand side of
  `ObsDescent.descendMod_exists_iff` (`ObsDescent.lean:284`) with the
  coarsening implication — a one-liner with **no separately named native
  declaration**; the *factorization* transport it feeds is named
  (`ObsDescent.descendMod_exists_of_coarsen`, `ObsDescent.lean:334`).
- **Relation status.** `equivalent-under-H_struct`.

### 68. `invariantFactorMod_exists_of_setoid_imp` — theorem (lines 606–623)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantFactorMod_exists_of_setoid_imp
    (P : PrimitiveDifference α β) (φ : α → γ) (S T : Setoid γ)
    (hST : ∀ a b : γ, S.r a b → T.r a b) :
    (∃ F : P.ResidualQuotient → Quotient S,
        ∀ x : α, F (P.classOf x) = Quotient.mk S (φ x)) →
      ∃ F : P.ResidualQuotient → Quotient T,
        ∀ x : α, F (P.classOf x) = Quotient.mk T (φ x) := by
```
- **Assumption graph.** Direct: items 9, 27, 28. Closure: {1,…,9, 27, 28}
  (note: this statement does **not** depend on item 60 — it is stated purely at
  the factorization level). Explicit hypotheses: the coarsening implication and
  a mod-`S` factorization.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantFactorMod_exists_of_setoid_imp' depends on axioms: [Quot.sound]`
- **Neutral content.** Mod-`S` factorizations transport along coarsening by
  composing with the canonical map of item 27.
- **Native counterpart.** `ObsDescent.descendMod_exists_of_coarsen`
  (`ObsDescent.lean:334`) — NEW this run, **exact statement match** (same
  hypotheses, same conclusion), built from `ObsDescent.coarsenMap` and
  `ObsDescent.coarsenMap_mk`.
- **Relation status.** `equivalent-under-H_struct`.

---

## Section J — product setoid and paired mod-descent (lines 625–738)

### 69. `productSetoid` — def (lines 625–634)

**SUPPLIED_INPUT**
```lean
def productSetoid (S : Setoid γ) (T : Setoid η) : Setoid (γ × η) where
  r p q := S.r p.1 q.1 ∧ T.r p.2 q.2
  iseqv := by
    constructor
    · intro p
      exact ⟨S.refl p.1, T.refl p.2⟩
    · intro p q hpq
      exact ⟨S.symm hpq.1, T.symm hpq.2⟩
    · intro p q r hpq hqr
      exact ⟨S.trans hpq.1 hqr.1, T.trans hpq.2 hqr.2⟩
```
- **Assumption graph.** **No supplied dependencies** (closure = ∅): setoids on
  two types only; the core structure is not mentioned.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** Componentwise product of two equivalence relations.
- **Native counterpart.** `ObsDescent.pairSetoid` (`ObsDescent.lean:318`) —
  NEW this run, same relation, same three law components.
- **Relation status.** `equivalent-under-H_struct` (independent of `H_struct`
  in fact). The native module additionally names the effectiveness fact
  `ObsDescent.pairSetoid_mk_eq_iff` (`ObsDescent.lean:327`), which the supplied
  file does not state.

### 70. `invariantCongruentMod_pair_iff` — theorem (lines 636–649)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantCongruentMod_pair_iff
    (P : PrimitiveDifference α β) (φ : α → γ) (ψ : α → η)
    (S : Setoid γ) (T : Setoid η) :
    P.InvariantCongruentMod (fun x : α => (φ x, ψ x)) (productSetoid S T)
      ↔ P.InvariantCongruentMod φ S ∧ P.InvariantCongruentMod ψ T := by
```
- **Assumption graph.** Direct: items 60, 69. Closure: {1, 2, 60, 69}. No
  quotient machinery.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantCongruentMod_pair_iff' does not depend on any axioms`
- **Neutral content.** Mod-version of item 44: the paired observable is
  class-constant modulo the product equivalence iff each component is
  class-constant modulo its factor.
- **Native counterpart.** `ObsDescent.classConstant_comp_mk_iff`
  (`ObsDescent.lean:276`) at `pairSetoid`, combined with
  `ObsDescent.pairSetoid_mk_eq_iff` (`ObsDescent.lean:327`) and
  `ObsDescent.classConstant_pair_iff` (`ObsDescent.lean:212`). **No separately
  named native declaration** — the native route is the reduction lemma plus the
  equality-layer pairing theorem.
- **Relation status.** `equivalent-under-H_struct`.

### 71. `invariantFactorMod_pair_exists_iff` — theorem (lines 651–661)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantFactorMod_pair_exists_iff
    (P : PrimitiveDifference α β) (φ : α → γ) (ψ : α → η)
    (S : Setoid γ) (T : Setoid η) :
    (∃ F : P.ResidualQuotient → Quotient (productSetoid S T),
        ∀ x : α,
          F (P.classOf x) =
            Quotient.mk (productSetoid S T) (φ x, ψ x))
      ↔ P.InvariantCongruentMod φ S ∧ P.InvariantCongruentMod ψ T :=
```
- **Assumption graph.** Direct: items 64, 69, 70. Closure: [CORE 1–10] ∪
  {60, 61, 62, 63, 64, 69, 70}.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantFactorMod_pair_exists_iff' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** A joint factorization into the product-equivalence
  quotient exists iff both mod-compatibilities hold.
- **Native counterpart.** `ObsDescent.descendMod_exists_iff`
  (`ObsDescent.lean:284`) at `ObsDescent.pairSetoid` (`ObsDescent.lean:318`),
  with the componentwise reading supplied by
  `ObsDescent.pairSetoid_mk_eq_iff` (`ObsDescent.lean:327`). No separately
  named native declaration.
- **Relation status.** `equivalent-under-H_struct`.

### 72. `invariantFactorMod_pair_exists_iff_component_factors` — theorem (lines 663–684)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantFactorMod_pair_exists_iff_component_factors
    (P : PrimitiveDifference α β) (φ : α → γ) (ψ : α → η)
    (S : Setoid γ) (T : Setoid η) :
    (∃ F : P.ResidualQuotient → Quotient (productSetoid S T),
        ∀ x : α,
          F (P.classOf x) =
            Quotient.mk (productSetoid S T) (φ x, ψ x))
      ↔
        (∃ Fφ : P.ResidualQuotient → Quotient S,
          ∀ x : α, Fφ (P.classOf x) = Quotient.mk S (φ x)) ∧
        (∃ Fψ : P.ResidualQuotient → Quotient T,
          ∀ x : α, Fψ (P.classOf x) = Quotient.mk T (ψ x)) := by
```
- **Assumption graph.** Direct: items 64, 69, 70, 71. Closure: closure(71) ∪
  {71}.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantFactorMod_pair_exists_iff_component_factors' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** Joint mod-factorization exists iff each component
  mod-factorization exists.
- **Native counterpart.** `ObsDescent.descendMod_exists_iff`
  (`ObsDescent.lean:284`) applied three times (jointly and componentwise), glued
  by `ObsDescent.pairSetoid_mk_eq_iff` (`ObsDescent.lean:327`); the
  equality-layer archetype is `ObsDescent.pair_descend_exists_iff`
  (`ObsDescent.lean:225`). No separately named native declaration.
- **Relation status.** `equivalent-under-H_struct`.

### 73. `invariantPairMod_no_factor_of_left_not_invariantCongruentMod` — theorem (lines 686–695)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantPairMod_no_factor_of_left_not_invariantCongruentMod
    (P : PrimitiveDifference α β) (φ : α → γ) (ψ : α → η)
    (S : Setoid γ) (T : Setoid η)
    (hφ : ¬ P.InvariantCongruentMod φ S) :
    ¬ (∃ F : P.ResidualQuotient → Quotient (productSetoid S T),
        ∀ x : α,
          F (P.classOf x) =
            Quotient.mk (productSetoid S T) (φ x, ψ x)) := by
```
- **Assumption graph.** Direct: item 71. Closure: closure(71) ∪ {71}. Explicit
  hypothesis: the left component fails mod-`S` class-constancy.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantPairMod_no_factor_of_left_not_invariantCongruentMod' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** Left-component failure blocks the joint
  mod-factorization.
- **Native counterpart.** `ObsDescent.descendMod_exists_iff`
  (`ObsDescent.lean:284`) at `pairSetoid`, contraposed on the left conjunct —
  **no separately named native declaration**.
- **Relation status.** `equivalent-under-H_struct`.

### 74. `invariantPairMod_no_factor_of_right_not_invariantCongruentMod` — theorem (lines 697–706)

**SUPPLIED_INPUT (statement)**
```lean
theorem invariantPairMod_no_factor_of_right_not_invariantCongruentMod
    (P : PrimitiveDifference α β) (φ : α → γ) (ψ : α → η)
    (S : Setoid γ) (T : Setoid η)
    (hψ : ¬ P.InvariantCongruentMod ψ T) :
    ¬ (∃ F : P.ResidualQuotient → Quotient (productSetoid S T),
        ∀ x : α,
          F (P.classOf x) =
            Quotient.mk (productSetoid S T) (φ x, ψ x)) := by
```
- **Assumption graph.** Direct: item 71. Closure: closure(71) ∪ {71}. Explicit
  hypothesis: the right component fails mod-`T` class-constancy.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.invariantPairMod_no_factor_of_right_not_invariantCongruentMod' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** Right-component failure blocks the joint
  mod-factorization.
- **Native counterpart.** `ObsDescent.descendMod_exists_iff`
  (`ObsDescent.lean:284`) at `pairSetoid`, contraposed on the right conjunct —
  no separately named native declaration.
- **Relation status.** `equivalent-under-H_struct`.

### 75. `localGreenGlobalRed_pair_mod_obstruction` — theorem (lines 708–722)

**SUPPLIED_INPUT (statement)**
```lean
theorem localGreenGlobalRed_pair_mod_obstruction
    (P : PrimitiveDifference α β) (φ : α → γ) (ψ : α → η)
    (S : Setoid γ) (T : Setoid η)
    (hφ : P.InvariantCongruentMod φ S)
    (hψ : ¬ P.InvariantCongruentMod ψ T) :
    (∃ F : P.ResidualQuotient → Quotient S,
        ∀ x : α, F (P.classOf x) = Quotient.mk S (φ x)) ∧
      ¬ (∃ F : P.ResidualQuotient → Quotient (productSetoid S T),
        ∀ x : α,
          F (P.classOf x) =
            Quotient.mk (productSetoid S T) (φ x, ψ x)) := by
```
- **Assumption graph.** Direct: items 64 (`.mpr`), 69, 70, 71, 74. Closure:
  closure(71) ∪ {71, 74}. Explicit hypotheses: `φ` mod-`S` class-constant, `ψ`
  not mod-`T` class-constant.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.localGreenGlobalRed_pair_mod_obstruction' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** Mod-version of item 50: one observable mod-factors
  alone; the pair into the product-equivalence quotient does not. (Slogan in
  the name is not evidence — gap row G20.)
- **Native counterpart.** `ObsDescent.view_descends_pair_blocked`
  (`ObsDescent.lean:248`) at the `Quotient.mk`-composed views, with
  compatibility translated by `ObsDescent.classConstant_comp_mk_iff`
  (`ObsDescent.lean:276`) and the product side by
  `ObsDescent.pairSetoid_mk_eq_iff` (`ObsDescent.lean:327`). No separately
  named native declaration.
- **Relation status.** `equivalent-under-H_struct`.

### 76. `localGreenGlobalRed_pair_mod_obstruction_of_witness` — theorem (lines 724–738)

**SUPPLIED_INPUT (statement)**
```lean
theorem localGreenGlobalRed_pair_mod_obstruction_of_witness
    (P : PrimitiveDifference α β) (φ : α → γ) (ψ : α → η)
    (S : Setoid γ) (T : Setoid η)
    (hφ : P.InvariantCongruentMod φ S)
    {x y : α} (hxy : P.ZeroRel x y) (hne : ¬ T.r (ψ x) (ψ y)) :
    (∃ F : P.ResidualQuotient → Quotient S,
        ∀ x : α, F (P.classOf x) = Quotient.mk S (φ x)) ∧
      ¬ (∃ F : P.ResidualQuotient → Quotient (productSetoid S T),
        ∀ x : α,
          F (P.classOf x) =
            Quotient.mk (productSetoid S T) (φ x, ψ x)) := by
```
- **Assumption graph.** Direct: items 2, 66, 75. Closure: closure(75) ∪ {75}.
  Explicit hypotheses: `φ` mod-`S` class-constant plus a two-point witness
  `T`-unrelated under `ψ`.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.PrimitiveDifference.localGreenGlobalRed_pair_mod_obstruction_of_witness' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** Item 75 with a concrete witness for the second
  observable's mod-failure.
- **Native counterpart.** `ObsDescent.view_descends_pair_blocked`
  (`ObsDescent.lean:248`) at `Quotient.mk`-composed views — **exact hypothesis
  shape match** once `ObsDescent.classConstant_comp_mk_iff` translates the
  compatibility and `ObsDescent.pairSetoid_mk_eq_iff` translates the pair
  inequality. No separately named native instantiation.
- **Relation status.** `equivalent-under-H_struct`.

---

## Section K — extended structures (lines 759–780)

### 77. `QuotientCompatiblePrimitiveDifference` — structure (lines 759–761)

**SUPPLIED_INPUT**
```lean
structure QuotientCompatiblePrimitiveDifference (α : Type u) (β : Type v)
    extends PrimitiveDifference α β where
  delta_congr : toPrimitiveDifference.DeltaCongruent
```
- **Assumption graph.** Direct: items 1, 12. Closure: {1, 2, 12}. **No
  theorems are proved about this structure anywhere in the supplied file**
  (FINITE_COMPUTATION) — declaration-only material.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** A difference datum bundled with two-sided compatibility
  as an additional field, so binary descent is available by assumption.
- **Native counterpart.** `DiffInterface.DiffObs` (`DiffInterface.lean:33`)
  together with an `ObsDescent.DeltaConstant` (`ObsDescent.lean:151`)
  hypothesis. **No native bundle was coined**: bundling a hypothesis into a
  field is presentation, and the native modules take the hypothesis as an
  argument (e.g. `ObsDescent.deltaDescend`, `ObsDescent.lean:156`).
- **Relation status.** `equivalent-under-H_struct` (bundling only; the
  inhabitants of the supplied structure are exactly the pairs
  `⟨O, h⟩ : Σ O, DeltaConstant O`).

### 78. `PointedPrimitiveDifference` — structure (lines 763–765)

**SUPPLIED_INPUT**
```lean
structure PointedPrimitiveDifference (α : Type u) (β : Type v)
    extends PrimitiveDifference α β where
  zero : α
```
- **Assumption graph.** Direct: item 1. Closure: {1}. **No laws relate the
  designated point to anything**, and no theorems are proved about this
  structure (FINITE_COMPUTATION).
- **Axiom report.** No report (not a theorem).
- **Neutral content.** A difference datum with a designated carrier point —
  bare data.
- **Native counterpart.** The input data of `ContactKernel.ofDiffObs`
  (`ContactKernel.lean:220`): an observer *plus a chosen pair* `a b : X`
  *plus a refutation-grade non-zero witness* `hw : ¬ ZeroRel O a b`; the
  resulting structure is `ContactKernel.WitnessedDiff`
  (`ContactKernel.lean:106`) with fields `a`, `b`, `apart_ab`.
- **Relation status.** **`incomparable`.** Neither direction holds:
  1. Supplied → native fails: the supplied bundle carries **one** law-free
     point, from which no witnessed pair can be extracted. Witness:
     `ContactKernel.kernel_no_witness_from_collapse`
    (`ContactKernel.lean:507`) — over the all-zero observer *no* pair is
     complement-witnessed, so an observer plus any point yields no kernel.
     Carrier 2; minimality is inherited from item 32's remark (subsingleton
     carriers admit no obstruction at all).
  2. Native → supplied fails as a *determination*: whenever an observer has
     one admissible pair, it has two distinct same-data kernel presentations —
     `ContactKernel.kernel_not_unique_of_pair`, presentation grade.  The
     concrete `Bool` witness uses the two ordered off-diagonal pairs
     (`pair_choice_not_unique`).  No claim is made up to isomorphism, `VHom`,
     or observational equivalence.

### 79. `zeroClass` — def (lines 771–773, in `namespace PointedPrimitiveDifference`)

**SUPPLIED_INPUT**
```lean
def zeroClass (P : PointedPrimitiveDifference α β) :
    PrimitiveDifference.ResidualQuotient P.toPrimitiveDifference :=
  PrimitiveDifference.classOf P.toPrimitiveDifference P.zero
```
- **Assumption graph.** Direct: items 9, 78. Closure: {1,…,9, 78}. No
  theorems are proved about it (FINITE_COMPUTATION).
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The class of the designated point in the quotient.
- **Native counterpart.** `DiffInterface.ObsQuotient.mk`
  (`DiffInterface.lean:74`) applied to the designated point — **no native
  declaration coined**: naming one application of the projection adds nothing
  formal.
- **Relation status.** `equivalent-under-H_struct`.

### 80. `IsZeroClass` — def (lines 775–778)

**SUPPLIED_INPUT**
```lean
def IsZeroClass
    (P : PointedPrimitiveDifference α β)
    (q : PrimitiveDifference.ResidualQuotient P.toPrimitiveDifference) : Prop :=
  q = P.zeroClass
```
- **Assumption graph.** Direct: items 8, 79. Closure: {1,…,9, 78, 79}. No
  theorems are proved about it (FINITE_COMPUTATION).
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The predicate "this quotient element is the class of the
  designated point".
- **Native counterpart.** `q = DiffInterface.ObsQuotient.mk O p`; on
  representatives this is decided by `ObsDescent.obsQuotient_mk_eq_iff`
  (`ObsDescent.lean:88`), and every `q` *has* a representative by
  `ObsDescent.obsQuotient_mk_surjective` (`ObsDescent.lean:96`). No native
  declaration coined.
- **Relation status.** `equivalent-under-H_struct`. Recorded strengthening
  (METATHEORY): the supplied file proves nothing about this predicate; the two
  native theorems just cited turn it into the induced relation on
  representatives, which the supplied file could have stated from item 11 and
  did not.

---

## Section L — integer-subtraction tail (lines 782–979)

**Structural fact, recorded once and applying to every one of items 81–103
(FINITE_COMPUTATION by inspection):** none of these 23 declarations mentions
the supplied core structure, its induced relation, its quotient, or any of
items 1–80. **The assumption graph of every item in this section is disjoint
from the assumption graph of every item in sections A–K**; the two halves of
the supplied file share only a word stem in their names. In particular **the
supplied file never instantiates its own core structure at an integer
difference**. Every proof here is `dsimp` unfolding plus `omega` (or `simpa`).

The native side closes that gap: `ObsDescent.intDiffObs`
(`ObsDescent.lean:359`) **is** an instance of the native counterpart structure
on `Int` with difference `a - b`, zero predicate `v = 0`, and all three law
fields **proved** by linear arithmetic — not admitted; its induced relation is
equality (`ObsDescent.intDiffObs_zeroRel`, `ObsDescent.lean:374`).

Uniform axiom fact for this section (FINITE_COMPUTATION): every one of the 14
tail theorems reports `[propext, Quot.sound]`; `Classical.choice` appears
nowhere, contrary to the usual expectation for `omega`.

Comment-borne physics vocabulary attached to these declarations is **REFUSED**
transport; the per-row dispositions G1–G20 are in
`lean_theorem_transport.md` and `contact_countermodels.json`.

### 81. `interferencePrimitiveDifference` — def (lines 786–787)

**SUPPLIED_INPUT**
```lean
def interferencePrimitiveDifference (w1 w2 delta_int : Int) : Int :=
  (w1 + w2 + delta_int) - (w1 + w2)
```
- **Assumption graph.** No supplied dependencies (closure = ∅). Three free
  integers.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The integer `(w1 + w2 + d) - (w1 + w2)`, identically
  `d`.
- **Native counterpart.** `ObsDescent.intDiffObs.delta (w1 + w2 + d) (w1 + w2)`
  (`ObsDescent.lean:359`).
- **Relation status.** `instance-material` (a value of the native difference
  map at shifted arguments; gap row G1 REFUSED for the comment's norm reading).

### 82. `interferencePrimitiveDifference_eq` — theorem (lines 789–793)

**SUPPLIED_INPUT**
```lean
@[simp]
theorem interferencePrimitiveDifference_eq (w1 w2 delta_int : Int) :
    interferencePrimitiveDifference w1 w2 delta_int = delta_int := by
```
- **Assumption graph.** Direct: item 81. Closure: {81}. **The only
  `@[simp]`-tagged declaration in the supplied file** (FINITE_COMPUTATION).
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.interferencePrimitiveDifference_eq' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** `(s + d) - s = d` over `Int`.
- **Native counterpart.** `ObsDescent.int_add_sub_cancel`
  (`ObsDescent.lean:411`) — `(s + d) - s = d`, at `s := w1 + w2`,
  `d := delta_int`.
- **Relation status.** `native-implies` (instantiation of the native lemma
  yields the supplied statement; the native lemma is the general form).

### 83. `interference_nonzero_of_delta_nonzero` — theorem (lines 798–800)

**SUPPLIED_INPUT**
```lean
theorem interference_nonzero_of_delta_nonzero (w1 w2 delta_int : Int) (h : delta_int ≠ 0) :
    interferencePrimitiveDifference w1 w2 delta_int ≠ 0 := by
```
- **Assumption graph.** Direct: items 81, 82. Closure: {81, 82}. Explicit
  hypothesis: `delta_int ≠ 0`. After item 82 the statement is `d ≠ 0 → d ≠ 0`.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.interference_nonzero_of_delta_nonzero' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** `d ≠ 0 → d ≠ 0`.
- **Native counterpart.** `ObsDescent.int_add_sub_cancel`
  (`ObsDescent.lean:411`) followed by `ObsDescent.int_sub_ne_zero_iff`
  (`ObsDescent.lean:385`).
- **Relation status.** `native-implies`. Gap row G2 REFUSED: the declaration's
  "non-factorization" branding has no formal counterpart in the statement.

### 84. `productDefectPrimitiveDifference` — def (lines 806–807)

**SUPPLIED_INPUT**
```lean
def productDefectPrimitiveDifference (w_ab marg_a marg_b total : Int) : Int :=
  w_ab * total - marg_a * marg_b
```
- **Assumption graph.** No supplied dependencies. Four free integers.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The integer `u - v` at `u := w_ab * total`,
  `v := marg_a * marg_b`.
- **Native counterpart.** `ObsDescent.intDiffObs.delta (w_ab * total) (marg_a * marg_b)`
  (`ObsDescent.lean:359`).
- **Relation status.** `instance-material` (gap row G3 REFUSED).

### 85. `product_defect_nonzero_of_nonfactor` — theorem (lines 812–816)

**SUPPLIED_INPUT**
```lean
theorem product_defect_nonzero_of_nonfactor (w_ab marg_a marg_b total : Int)
    (h : w_ab * total ≠ marg_a * marg_b) :
    productDefectPrimitiveDifference w_ab marg_a marg_b total ≠ 0 := by
```
- **Assumption graph.** Direct: item 84. Closure: {84}. Explicit hypothesis:
  the two products differ.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.product_defect_nonzero_of_nonfactor' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** `u ≠ v → u - v ≠ 0` over `Int`.
- **Native counterpart.** `ObsDescent.int_sub_ne_zero_iff`
  (`ObsDescent.lean:385`), `.mpr` direction.
- **Relation status.** `native-implies` (the native `↔` is strictly stronger
  than the supplied one-way form). Gap row G4 REFUSED.

### 86. `contextualityPrimitiveDifference` — def (lines 822–823)

**SUPPLIED_INPUT**
```lean
def contextualityPrimitiveDifference (local_prod global_target : Int) : Int :=
  local_prod - global_target
```
- **Assumption graph.** No supplied dependencies. Two free integers.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The difference of two free integers.
- **Native counterpart.** `ObsDescent.intDiffObs.delta` (`ObsDescent.lean:359`).
- **Relation status.** `instance-material` (gap row G5 REFUSED).

### 87. `contextuality_nonzero_of_parity_failure` — theorem (lines 828–832)

**SUPPLIED_INPUT**
```lean
theorem contextuality_nonzero_of_parity_failure (local_prod global_target : Int)
    (h : local_prod ≠ global_target) :
    contextualityPrimitiveDifference local_prod global_target ≠ 0 := by
```
- **Assumption graph.** Direct: item 86. Closure: {86}. Explicit hypothesis:
  `a ≠ b`.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.contextuality_nonzero_of_parity_failure' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** `a ≠ b → a - b ≠ 0`.
- **Native counterpart.** `ObsDescent.int_sub_ne_zero_iff`
  (`ObsDescent.lean:385`), `.mpr`.
- **Relation status.** `native-implies`. Gap row G6 REFUSED.

### 88. `cptpTraceNormPrimitiveDifference` — def (lines 838–839)

**SUPPLIED_INPUT**
```lean
def cptpTraceNormPrimitiveDifference (dist_orig dist_cptp : Int) : Int :=
  dist_orig - dist_cptp
```
- **Assumption graph.** No supplied dependencies. Two free integers.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The difference of two free integers.
- **Native counterpart.** `ObsDescent.intDiffObs.delta` (`ObsDescent.lean:359`).
- **Relation status.** `instance-material` (gap row G7 REFUSED).

### 89. `cptp_trace_norm_nonzero_of_residual` — theorem (lines 844–848)

**SUPPLIED_INPUT**
```lean
theorem cptp_trace_norm_nonzero_of_residual (dist_orig dist_cptp : Int)
    (h : dist_orig > dist_cptp) :
    cptpTraceNormPrimitiveDifference dist_orig dist_cptp ≠ 0 := by
```
- **Assumption graph.** Direct: item 88. Closure: {88}. Explicit hypothesis:
  **strict inequality** — one of only two tail theorems with an order
  hypothesis (the other is item 101).
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.cptp_trace_norm_nonzero_of_residual' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** `a > b → a - b ≠ 0` over `Int` (weaker than the
  derivable `a - b > 0`).
- **Native counterpart.** `ObsDescent.int_sub_ne_zero_of_gt`
  (`ObsDescent.lean:393`), stated as `(h : b < a) : a - b ≠ 0` — the same
  hypothesis, since `a > b` is notation for `b < a`.
- **Relation status.** `native-implies`. Gap row G8 REFUSED (the comment claims
  positivity; only nonzero-ness is stated).

### 90. `holonomyCurvaturePrimitiveDifference` — def (lines 854–855)

**SUPPLIED_INPUT**
```lean
def holonomyCurvaturePrimitiveDifference (flat_hol nonabelian_hol : Int) : Int :=
  flat_hol - nonabelian_hol
```
- **Assumption graph.** No supplied dependencies. Two free integers.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The difference of two free integers.
- **Native counterpart.** `ObsDescent.intDiffObs.delta` (`ObsDescent.lean:359`).
- **Relation status.** `instance-material` (gap row G9 REFUSED).

### 91. `holonomy_curvature_nonzero_of_nonabelian` — theorem (lines 860–864)

**SUPPLIED_INPUT**
```lean
theorem holonomy_curvature_nonzero_of_nonabelian (flat_hol nonabelian_hol : Int)
    (h : flat_hol ≠ nonabelian_hol) :
    holonomyCurvaturePrimitiveDifference flat_hol nonabelian_hol ≠ 0 := by
```
- **Assumption graph.** Direct: item 90. Closure: {90}. Explicit hypothesis:
  `a ≠ b`.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.holonomy_curvature_nonzero_of_nonabelian' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** `a ≠ b → a - b ≠ 0`.
- **Native counterpart.** `ObsDescent.int_sub_ne_zero_iff`
  (`ObsDescent.lean:385`), `.mpr`.
- **Relation status.** `native-implies`. Gap row G10 REFUSED.

### 92. `authorityNonPromotionPrimitiveDifference` — def (lines 870–871)

**SUPPLIED_INPUT**
```lean
def authorityNonPromotionPrimitiveDifference (derived_score auth_sealed : Int) : Int :=
  derived_score - auth_sealed
```
- **Assumption graph.** No supplied dependencies. Two free integers.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The difference of two free integers.
- **Native counterpart.** `ObsDescent.intDiffObs.delta` (`ObsDescent.lean:359`).
- **Relation status.** `instance-material` (gap row G11 REFUSED).

### 93. `authority_non_promotion_nonzero_of_unsealed` — theorem (lines 876–880)

**SUPPLIED_INPUT**
```lean
theorem authority_non_promotion_nonzero_of_unsealed (derived_score auth_sealed : Int)
    (h : derived_score ≠ auth_sealed) :
    authorityNonPromotionPrimitiveDifference derived_score auth_sealed ≠ 0 := by
```
- **Assumption graph.** Direct: item 92. Closure: {92}. Explicit hypothesis:
  `a ≠ b`.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.authority_non_promotion_nonzero_of_unsealed' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** `a ≠ b → a - b ≠ 0`.
- **Native counterpart.** `ObsDescent.int_sub_ne_zero_iff`
  (`ObsDescent.lean:385`), `.mpr`.
- **Relation status.** `native-implies` **for the formal content only**. Gap
  row G12 is the largest gap in the supplied file and is **REFUSED**: the
  attached comment asserts a proof-theoretic non-derivability between two
  predicates that are never defined anywhere in the file, with no proof system
  and no derivability relation present, and with hypotheses (`> 0`, `= 0`)
  that differ from the actual hypothesis (`≠`). Nothing of that claim is
  transported. Comments are not evidence.

### 94. `gellMannDecoherencePrimitiveDifference` — def (lines 887–888)

**SUPPLIED_INPUT**
```lean
def gellMannDecoherencePrimitiveDifference (total_prob diag_sum : Int) : Int :=
  total_prob - diag_sum
```
- **Assumption graph.** No supplied dependencies. Two free integers.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The difference of two free integers.
- **Native counterpart.** `ObsDescent.intDiffObs.delta` (`ObsDescent.lean:359`).
- **Relation status.** `instance-material` (gap row G13: the attached comment
  is honest — it explicitly disclaims probability, positivity and
  normalization; the residual gap is name-flavor only).

### 95. `gellMannDecoherencePrimitiveDifference_eq_offdiagonal` — theorem (lines 893–899)

**SUPPLIED_INPUT**
```lean
theorem gellMannDecoherencePrimitiveDifference_eq_offdiagonal
    (d11 d12 d22 : Int) :
    gellMannDecoherencePrimitiveDifference
        (d11 + d22 + 2 * d12) (d11 + d22) =
      2 * d12 := by
```
- **Assumption graph.** Direct: item 94. Closure: {94}. Three free integers,
  no hypotheses.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.gellMannDecoherencePrimitiveDifference_eq_offdiagonal' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** `(a + c + 2b) - (a + c) = 2b` over `Int`.
- **Native counterpart.** `ObsDescent.int_shift_cancel`
  (`ObsDescent.lean:398`) — the identical identity,
  `(a + c + 2 * b) - (a + c) = 2 * b`.
- **Relation status.** `native-implies` (statement-for-statement after renaming
  `a := d11`, `c := d22`, `b := d12`; in fact `equivalent-under-H_struct` holds
  too, since the two statements are the same proposition). Gap row G14
  RECORDED: the identity is real; the matrix reading is the caller's
  substitution.

### 96. `gellMannDecoherencePrimitiveDifference_eq_zero_iff` — theorem (lines 903–914)

**SUPPLIED_INPUT (statement)**
```lean
theorem gellMannDecoherencePrimitiveDifference_eq_zero_iff
    (d11 d12 d22 : Int) :
    gellMannDecoherencePrimitiveDifference
        (d11 + d22 + 2 * d12) (d11 + d22) = 0 ↔
      d12 = 0 := by
```
- **Assumption graph.** Direct: items 94, 95. Closure: {94, 95}.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.gellMannDecoherencePrimitiveDifference_eq_zero_iff' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** `2b = 0 ↔ b = 0` over `Int` (uses that `Int` has no
  2-torsion).
- **Native counterpart.** `ObsDescent.int_shift_cancel`
  (`ObsDescent.lean:398`) followed by `ObsDescent.int_two_mul_eq_zero_iff`
  (`ObsDescent.lean:403`).
- **Relation status.** `native-implies`. Gap row G15 RECORDED (naming only).

### 97. `gellMannDecoherencePrimitiveDifference_ne_zero_iff` — theorem (lines 918–929)

**SUPPLIED_INPUT (statement)**
```lean
theorem gellMannDecoherencePrimitiveDifference_ne_zero_iff
    (d11 d12 d22 : Int) :
    gellMannDecoherencePrimitiveDifference
        (d11 + d22 + 2 * d12) (d11 + d22) ≠ 0 ↔
      d12 ≠ 0 := by
```
- **Assumption graph.** Direct: items 94, 96. Closure: {94, 95, 96}. Proved
  intuitionistically from item 96 by shuttling refutations — no excluded
  middle.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.gellMannDecoherencePrimitiveDifference_ne_zero_iff' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** Negation of item 96 on both sides.
- **Native counterpart.** `ObsDescent.int_shift_cancel`
  (`ObsDescent.lean:398`) with `ObsDescent.int_two_mul_eq_zero_iff`
  (`ObsDescent.lean:403`), negated on both sides.
- **Relation status.** `native-implies`. Gap row G15 RECORDED.

### 98. `decoherence_nonzero_of_offdiagonal` — theorem (lines 933–937)

**SUPPLIED_INPUT**
```lean
theorem decoherence_nonzero_of_offdiagonal (total_prob diag_sum : Int)
    (h : total_prob ≠ diag_sum) :
    gellMannDecoherencePrimitiveDifference total_prob diag_sum ≠ 0 := by
```
- **Assumption graph.** Direct: item 94. Closure: {94}. Explicit hypothesis:
  `a ≠ b`.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.decoherence_nonzero_of_offdiagonal' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** `a ≠ b → a - b ≠ 0`.
- **Native counterpart.** `ObsDescent.int_sub_ne_zero_iff`
  (`ObsDescent.lean:385`), `.mpr`.
- **Relation status.** `native-implies`. Gap row G16 RECORDED.

### 99. `decoherence_nonzero_of_offdiagonal_weight` — theorem (lines 941–946)

**SUPPLIED_INPUT (statement)**
```lean
theorem decoherence_nonzero_of_offdiagonal_weight
    (d11 d12 d22 : Int) (h : d12 ≠ 0) :
    gellMannDecoherencePrimitiveDifference
        (d11 + d22 + 2 * d12) (d11 + d22) ≠ 0 := by
```
- **Assumption graph.** Direct: item 94 (and, mathematically, the content of
  items 95–96). Closure: {94, 95, 96}. Explicit hypothesis: `d12 ≠ 0`.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.decoherence_nonzero_of_offdiagonal_weight' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** `b ≠ 0 → 2b ≠ 0` over `Int`, phrased through the
  substituted definition.
- **Native counterpart.** `ObsDescent.int_shift_cancel`
  (`ObsDescent.lean:398`) with `ObsDescent.int_two_mul_eq_zero_iff`
  (`ObsDescent.lean:403`).
- **Relation status.** `native-implies`. Gap row G16 RECORDED.

### 100. `thresholdRepairCapacityPrimitiveDifference` — def (lines 952–953)

**SUPPLIED_INPUT**
```lean
def thresholdRepairCapacityPrimitiveDifference (physical_defects repair_absorbed : Int) : Int :=
  physical_defects - repair_absorbed
```
- **Assumption graph.** No supplied dependencies. Two free integers.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The difference of two free integers.
- **Native counterpart.** `ObsDescent.intDiffObs.delta` (`ObsDescent.lean:359`).
- **Relation status.** `instance-material` (gap row G17 REFUSED).

### 101. `threshold_repair_nonzero_of_unabsorbed` — theorem (lines 958–962)

**SUPPLIED_INPUT**
```lean
theorem threshold_repair_nonzero_of_unabsorbed (physical_defects repair_absorbed : Int)
    (h : physical_defects > repair_absorbed) :
    thresholdRepairCapacityPrimitiveDifference physical_defects repair_absorbed ≠ 0 := by
```
- **Assumption graph.** Direct: item 100. Closure: {100}. Explicit hypothesis:
  strict inequality (the second and last order hypothesis in the tail).
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.threshold_repair_nonzero_of_unabsorbed' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** `a > b → a - b ≠ 0`.
- **Native counterpart.** `ObsDescent.int_sub_ne_zero_of_gt`
  (`ObsDescent.lean:393`).
- **Relation status.** `native-implies`. Gap row G17 REFUSED (the comment
  claims strict positivity and a coboundary space; only nonzero-ness is
  stated, and no such space exists in the file).

### 102. `classicalLimitPrimitiveDifference` — def (lines 968–969)

**SUPPLIED_INPUT**
```lean
def classicalLimitPrimitiveDifference (phase_state classical_proj : Int) : Int :=
  phase_state - classical_proj
```
- **Assumption graph.** No supplied dependencies. Two free integers.
- **Axiom report.** No report (not a theorem).
- **Neutral content.** The difference of two free integers.
- **Native counterpart.** `ObsDescent.intDiffObs.delta` (`ObsDescent.lean:359`).
- **Relation status.** `instance-material` (gap row G18 REFUSED).

### 103. `classical_limit_nonzero_of_unprojected` — theorem (lines 974–978)

**SUPPLIED_INPUT**
```lean
theorem classical_limit_nonzero_of_unprojected (phase_state classical_proj : Int)
    (h : phase_state ≠ classical_proj) :
    classicalLimitPrimitiveDifference phase_state classical_proj ≠ 0 := by
```
- **Assumption graph.** Direct: item 102. Closure: {102}. Explicit hypothesis:
  `a ≠ b`.
- **Axiom report (FINITE_COMPUTATION).**
  `'OmegaCore.classical_limit_nonzero_of_unprojected' depends on axioms: [propext, Quot.sound]`
- **Neutral content.** `a ≠ b → a - b ≠ 0`.
- **Native counterpart.** `ObsDescent.int_sub_ne_zero_iff`
  (`ObsDescent.lean:385`), `.mpr`.
- **Relation status.** `native-implies`. Gap row G18 REFUSED.

---

## Accounting: the map is complete and non-redundant

| section | supplied lines | items | count |
|---|---|---|---|
| A — core structure and induced relation | 13–65 | 1–11 | 11 |
| B — descent of the difference map (equality) | 67–143 | 12–19 | 8 |
| C — descent of the difference map (mod setoid) | 145–219 | 20–26 | 7 |
| D — transport along coarsening | 221–263 | 27–30 | 4 |
| E — the all-zero countermodel | 265–295, 740–755 | 31–35 | 5 |
| F — observable descent (equality) | 297–369 | 36–43 | 8 |
| G — pairing and the two-observable obstruction | 371–473 | 44–52 | 9 |
| H — context-tagged construction | 475–530 | 53–59 | 7 |
| I — observable descent (mod setoid) | 532–623 | 60–68 | 9 |
| J — product setoid and paired mod-descent | 625–738 | 69–76 | 8 |
| K — extended structures | 759–780 | 77–80 | 4 |
| L — integer-subtraction tail | 782–979 | 81–103 | 23 |
| **total** | | **1–103** | **103** |

11+8+7+4+5+8+9+7+9+8+4+23 = **103**. Each item number 1–103 appears exactly
once as a heading; the section ranges partition 1–103 with no overlap and no
gap. Kind split: 3 structures (items 1, 77, 78) + 29 defs + 71 theorems = 103,
and the 71 theorem rows are in bijection with the 71 lines of
`contact_scratch/axiom_report.txt` (FINITE_COMPUTATION).

## Relation-status tally

| status | items | count |
|---|---|---|
| `equivalent-under-H_struct` | 1–30 (30), 32–35 (4), 36–52 (17), 54–77 (24), 79–80 (2) | 77 |
| `same-third-notion` | 53 | 1 |
| `instance-material` | 31, 81, 84, 86, 88, 90, 92, 94, 100, 102 | 10 |
| `native-implies` | 82, 83, 85, 87, 89, 91, 93, 95, 96, 97, 98, 99, 101, 103 | 14 |
| `incomparable` | 78 | 1 |
| `contact-implies` | — | 0 |
| `NONE` | — | 0 |
| **total** | | **103** |

Arithmetic: 30 + 4 + 17 + 24 + 2 = 77; 77 + 1 + 10 + 14 + 1 = **103**.

Four of the 77 `equivalent-under-H_struct` rows carry an explicitly recorded
**hypothesis delta** — items 17 and 39 (canonical-lift form vs symmetric
two-map form), item 30 (binary vs unary coarsening transport), and item 50
(negation-hypothesis form vs witness form). In each case the delta is stated in
the row and is discharged by a named native theorem; none of the four is an
unpriced gap.

**No row is `NONE`.** Every supplied declaration has at least one native
counterpart named above. Rows marked "no separately named native declaration"
are *not* `NONE`: in each case a named native theorem is cited from which the
supplied statement follows in one recorded step (contraposition,
instantiation, `Iff.mp`/`Iff.mpr`, or `Iff.trans`). Those single steps are not
themselves in the Lean corpus; the claim carried by such a row is exactly
"the named native theorem, plus this one step" — no more.

## What this map does not claim

1. It does **not** claim that the native corpus contains a declaration for each
   of the 103. It claims the mapping above, row by row, at the stated grade.
2. It does **not** import any interpretive branding from the supplied
   declaration names (`localGreenGlobalRed_*`) or from any comment. Gap row G20
   records that the branding is naming only and that the formal statements
   under it are correct as stated.
3. It does **not** claim the two sides are equivalent as *developments*. The
   directional verdict, its countermodels, and its priced admissions are in
   `lean_theorem_transport.md`.

