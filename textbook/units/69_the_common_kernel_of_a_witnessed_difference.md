# Unit 69: The Common Kernel of a Witnessed Difference

**Claim.** A witnessed difference records a difference map, a zero test, and a pair whose difference is nonzero. This common interface does not supply every law of an observer or native relation.

## First pass

Read the record as a checklist: a way to compare two items, a test for zero, and one pair that fails that zero test.

The record establishes that particular witnessed distinction. Symmetry, transitivity, and other stronger laws must be supplied separately.

The lesson compares constructions into this common interface. Sharing the interface does not make the source constructions identical.

## Detailed claim and formal anchors

`CL-PD2-CONTACT-KERNEL`, `CL-PD2-CONTACT-COUNTERMODELS`, `CL-PD2-CONTACT-ENTRY` (`FROZEN` / `VERIFIED_FINITE` / `CONDITIONAL` / `REFUTED` / `OPEN`) — `lean4/Derivation/ContactKernel.lean`, `code/run_primitive_contact.py`, `artifacts/primitive_contact.json`
**Prerequisites**: Unit 44 (`DiffInterface`: `DiffObs`, `ZeroRel`), Unit 51 (`PrimitiveCore`: `Setting`, candidates `W`–`F`, `Cotrans`, `Located`, `located_of_decidable`, `imp_a_d`, `e_empty_iff_d`), Unit 52 (`PrimitiveCats`: `PtdRel`, `Hom`, `Initial`, `d2Obj`, `d2_initial`, `d2_map_injective`, `SymObj`, `IrreflObj`), Unit 53 (`PrimitiveContact`: `NativeKernel`), Unit 54 (`PrimitivePassage`: `preRetained`, `inducedSetting`, `obstP`, `kernel_enters_preretained`, `obst_requires_observation`), Unit 56 (`Apartness`: `triSymRel`, `symm_without_cotrans_breaks_trans`), Unit 67 (`ObsDescent`: `collapseAllObs`), Unit 68 (`ContactBridge`: `obsApart`)

## Question

Units 67 and 68 showed that the native difference programme and the arriving observer stratum (`DiffObs`) are incomparable at signature grade in one direction (`d2_not_obs_complement`) and reconstructible in the other (`ObsDescent`). What is the largest common structure that both a native candidate-`A` setting and an inhabited observer can realize, what additional data must an observer supply to produce one, and which of the observer's laws and the nine native candidate readings are absent from that common kernel?

## What we already possess

- From Unit 44 (`DiffInterface`): `DiffObs X R` (`delta : X → X → R`, `Zero : R → Prop`, `zero_refl`, `zero_symm`, `zero_trans`) and `ZeroRel O x y := O.Zero (O.delta x y)`.
- From Unit 51 (`PrimitiveCore`): `Setting` (`X`, `r`, `a`, `b`, `ret`, `prot`, `Ops`), candidates `W` (`r a b`), `A` (`r a b ∧ ∀ x, ¬ r x x`), `Bs`, `Bc`, `Bl`, `C`, `D` (`a ≠ b`), `E`, `F`, and the implications `imp_a_d` and `e_empty_iff_d`.
- From Unit 52 (`PrimitiveCats`): pointed witnessed relations `PtdRel`, morphisms `Hom`, the oriented two-element initial object `d2Obj`, `d2_initial`, and `d2_map_injective`.
- From Unit 53 (`PrimitiveContact`): `NativeKernel := Σ S : Setting, PLift (A S)`.
- From Unit 54 (`PrimitivePassage`): the pre-retention passage state `preRetained`, `inducedSetting`, `obstP`, `kernel_enters_preretained`, and `obst_requires_observation`.
- From Unit 67 (`ObsDescent`) and Unit 68 (`ContactBridge`): `collapseAllObs` and `obsApart O x y := ¬ ZeroRel O x y`.

## New concept

`ContactKernel` defines the common replacement kernel `WitnessedDiff X R` (`lean4/Derivation/ContactKernel.lean`):

- **Structure (`WitnessedDiff X R`)**:
  - `delta : X → X → R` (difference map),
  - `Zero : R → Prop` (zero predicate),
  - `a : X` and `b : X` (designated endpoints),
  - `diag_zero : ∀ x, Zero (delta x x)` (diagonal-zero law),
  - `apart_ab : ¬ Zero (delta a b)` (refutation-grade non-zero witness at the designated pair).
  Deliberately absent are zero-symmetry, zero-transitivity, retention (`ret`), protection (`prot`), and any operation family (`Ops`).
- **Induced apartness and immediate consequences**:
  - `kernelApart K x y := ¬ K.Zero (K.delta x y)`.
  - `kernelApart_irrefl`: `∀ x, ¬ kernelApart K x x` (contrapositive of `diag_zero`).
  - `kernel_endpoints_ne`: `K.a ≠ K.b` (from `apart_ab` against `diag_zero`).
  - `no_kernel_on_subsingleton`: `[Subsingleton X] → WitnessedDiff X R → False`.
  - `boolKernel : WitnessedDiff Bool Bool`: `delta x y := (!x) && y`, `Zero v := (v = false)`, `a := false`, `b := true`.
- **Realizations from both sides**:
  - Native setting from a kernel: `toSetting K` sets `r := kernelApart K`, endpoints `K.a, K.b`, and empty stores `ret := False`, `prot := False`, `Ops := False`. `toSetting_A` shows `A (toSetting K)`, and `toNativeKernel K : PrimitiveContact.NativeKernel` honors the pre-contact interface.
  - Kernel from a native setting: `ofSetting S h : WitnessedDiff S.X Prop` sets `delta := S.r` and `Zero := Not`. Its induced apartness `¬¬ S.r x y` equals `S.r x y` under `[∀ x y, Decidable (S.r x y)]` (`ofSetting_exact`, with `open_kernel_grade` recording the undecidable residual). `ofSetting_ret_irrelevant` shows by `rfl` that replacing `ret`, `prot`, and `Ops` yields the identical kernel.
  - Kernel from an observer plus a chosen pair: `ofDiffObs O a b hw` requires an explicit non-zero pair `hw : ¬ ZeroRel O a b`. `kernel_from_obs_iff_pair` shows `(∃ K, K.delta = O.delta ∧ K.Zero = O.Zero) ↔ (∃ a b, ¬ ZeroRel O a b)`, and `eq_ofDiffObs_of_fields` shows every same-data kernel is `ofDiffObs` at its own endpoints.
  - Observer from a kernel plus two law declarations: `toDiffObs K hs ht` packages `K` together with zero-symmetry `hs` and zero-transitivity `ht` into a `DiffObs X R`. `toDiffObs_fields` and `toDiffObs_apart` hold by `rfl` / `Iff.rfl` — a record identity at definition grade, not a derivation.
- **One-to-one pair correspondence, transpose non-uniqueness, and the fixed-point selector obstruction**:
  - For a fixed observer `O`, `NonZeroPair O := { p : X × X // ¬ ZeroRel O p.1 p.2 }` and `SameDataKernel O := { K : WitnessedDiff X R // K.delta = O.delta ∧ K.Zero = O.Zero }` are in bijection via `toPair` and `ofPair` (`toPair_ofPair`, `ofPair_toPair`, `ofPair_injective`).
  - Because `O.zero_symm` is an admitted field of `DiffObs`, every admissible pair `(a, b)` has an admissible transpose `(b, a)` whose kernel differs in the first endpoint (`transpose_kernel_ne`, `kernel_not_unique_of_pair`, and on `boolEqObs`, `two_kernels_from_one_observer` and `pair_choice_not_unique`). This non-uniqueness is at presentation grade (`K₁ ≠ K₂` via `K₁.a ≠ K₂.a`; both kernels induce the same `kernelApart`).
  - Under the negation relabelling `swapObs O` (`delta x y := O.delta (!x) (!y)`), `swapObs_boolEqObs` shows `swapObs boolEqObs = boolEqObs` (spending `funext`, hence `Quot.sound`). Because no pair `(a, b) : Bool × Bool` satisfies `(!a, !b) = (a, b)`, `no_equivariant_pair_at_fixed_point` and `no_equivariant_pair_valued_map` refute the existence of a total map `sel : DiffObs Bool Bool → Bool × Bool` commuting with `swapObs`.
- **Pricing what the kernel does not carry**:
  - `kernel_not_observer` (carrier 2, `Prop`-valued): the oriented kernel on `PrimDiff.D2` shares its `delta` and `Zero` with no `DiffObs Bool Prop`.
  - `kernel_not_bs` (carrier 2): `kernelApart` on the `D2` kernel is not symmetric.
  - `kernel_zero_not_trans` (carrier 3): the kernel on `Apartness.triSymRel` with `Zero := Not` breaks zero-transitivity through point `2`.
  - `kernel_not_bc` (carrier 3): `kernelApart` on the `triSymRel` kernel is not cotransitive.
  - `kernel_located_of_decidable`: under `[∀ v, Decidable (K.Zero v)]`, `Located (kernelApart K)` holds (`open_kernel_bl` records the undecidable case).
  - `kernel_not_c` and `kernel_not_f` hold definitionally because `toSetting K` has empty `prot` and `ret` stores; `kernel_to_w`, `kernel_to_d`, and `kernel_to_e_empty` hold on `toSetting K`, while `kernel_not_e_merged` shows that declaring one constant merger kills `E` without changing the kernel. `no_kernel_over_allzero` and `kernel_no_witness_from_collapse` show that `collapseAllObs` supports no kernel.
- **Value presentation fork and `VHom` rigidity**:
  - `unitValKernel` (edge value `1 : Nat`) and `twoValKernel` (edge value `2 : Nat`) induce the same `kernelApart` while `unitValKernel.delta ≠ twoValKernel.delta` (`value_presentation_fork`).
  - A valued kernel morphism `VHom K K'` consists of `f : X → X'`, `g : R → R'`, endpoint preservation `ha`, `hb`, `hdelta : ∀ x y, K'.delta (f x) (f y) = g (K.delta x y)`, and `hzero : ∀ v, K.Zero v → K'.Zero (g v)`.
  - Off the image of `K.delta`, `g` is unconstrained (`vhom_not_unique`: two morphisms `unitValKernel → boolKernel` with `f = id` that differ at `g 2`). Under `DeltaOnto K` (`∀ v, ∃ x y, K.delta x y = v`), `f` uniquely determines the morphism (`vhom_unique_of_onto`).
- **Pointed-relation initiality, branching, passage entry, and the 37-cell matrix**:
  - `apartObj K : PrimitiveCats.PtdRel` forgets `R` and retains `(X, kernelApart K, K.a, K.b, K.apart_ab)`. By `PrimitiveCats.d2_initial`, `d2Obj` has a unique injective morphism into `apartObj K` (`kernel_gateway_unique`, `kernel_gateway_injective`), while `boolKernel ≠ boolKernelSwap` (`kernel_gateways_not_identical`).
  - The three-point `freeKernel` (one oriented edge `0 → 1` on `Fin 3`, point `2` free) has two distinct morphisms into every `apartObj K'` (`kernel_no_terminal`), so no kernel presents a terminal collector in `PtdRel` (`kernel_no_terminal_collector`).
  - `passageObj`, `passage_gateway_unique`, `kernel_licenses_entry`, `entry_pre_observation`, and `kernel_two_point_presentation` record the pre-retention passage state alongside endpoint distinctness, and `contactCells` (`contactCells_length : contactCells.length = 37`) lists the 37 collision cells.

## Plain-language interpretation

Think of `WitnessedDiff` as a distance or difference table `delta(x, y)` together with a label `Zero(v)` telling which table entries count as zero, plus two pinned rows/columns `(a, b)` where the table entry is guaranteed not to be zero (`¬ Zero(delta(a, b))`), while every diagonal entry `delta(x, x)` is zero.

1. **Why an observer does not hand you a kernel for free**: A `DiffObs` has `delta`, `Zero`, and three laws (`zero_refl`, `zero_symm`, `zero_trans`), but it does not name any pair `(a, b)` where `delta(a, b)` is non-zero. If the observer is `collapseAllObs` (where everything is zero), no such pair exists at all (`no_kernel_over_allzero`). If an observer does have a non-zero pair `(a, b)`, its symmetry law `zero_symm` forces the swapped pair `(b, a)` to be non-zero as well, giving a second distinct kernel (`transpose_kernel_ne`). Even on `Bool`, you cannot write a rule `sel(O)` that picks one of `(false, true)` or `(true, false)` in a way that commutes with flipping `false ↔ true`, because `boolEqObs` is unchanged when you flip `false ↔ true` (`swapObs_boolEqObs`), whereas every pair on `Bool` moves (`no_equivariant_pair_valued_map`).
2. **Why a kernel is not an observer**: A kernel drops `zero_symm` and `zero_trans`. On 2 points, the oriented relation `D2` (`false → true` only) is a valid kernel (`boolKernel`), but its zero relation is asymmetric (`kernel_not_observer`, `kernel_not_bs`). On 3 points, `triSymRel` (`0 — 1` only, point `2` isolated) is a valid symmetric kernel, but its zero relation has `0 ~ 2` and `2 ~ 1` without `0 ~ 1` (`kernel_zero_not_trans`, `kernel_not_bc`). Adding `zero_symm` and `zero_trans` back to a kernel gives a `DiffObs` by copying the fields directly (`toDiffObs` — a record identity, not a theorem that derives those laws).
3. **Why value data is finer than apartness**: Whether the non-zero entry at `(false, true)` is `1` (`unitValKernel`) or `2` (`twoValKernel`), the set of non-zero pairs is the same (`value_presentation_fork`). When mapping `unitValKernel` to `boolKernel`, the value `2` never appears in `unitValKernel.delta`, so the value map `g` can send `2` to either `false` or `true` (`vhom_not_unique`), unless `delta` hits every value in `R` (`DeltaOnto`, `vhom_unique_of_onto`).

## Pseudocode

```text
STRUCTURE WitnessedDiff(X, R):
    delta     : (X, X) -> R
    Zero      : R -> Prop
    a, b      : X
    diag_zero : forall x, Zero(delta(x, x))
    apart_ab  : NOT Zero(delta(a, b))

FUNCTION kernelApart(K)(x, y):
    RETURN NOT K.Zero(K.delta(x, y))

BIJECTION NonZeroPair(O) <-> SameDataKernel(O):
    toPair(K) := (K.a, K.b)
    ofPair(a, b, hw) := WitnessedDiff(O.delta, O.Zero, a, b, O.zero_refl, hw)

RECORD IDENTITY toDiffObs(K, hs_symm, ht_trans):
    RETURN DiffObs(K.delta, K.Zero, K.diag_zero, hs_symm, ht_trans)

VALUE FORK & VHom RIGIDITY:
    unitValKernel.delta(x, y) := 1 if (not x and y) else 0
    twoValKernel.delta(x, y)  := 2 if (not x and y) else 0
    # Same kernelApart; distinct delta tables.
    # Off the image of delta (v = 2), VHom.g(2) is free (vhom_not_unique).
    # If DeltaOnto(K), carrier map f uniquely fixes value map g (vhom_unique_of_onto).
```

## Python

Genesis (`code/run_primitive_contact.py`, lines 177-242 and 442-456 abridged) defines the 37-row `COLLISION_CELLS` mirror of `ContactKernel.contactCells` and the value-fork enumeration `enum_value_fork` (E5), alongside `enum_bool_observers` (E1) and `enum_settings_kernels` (E2):

```python
def enum_value_fork() -> dict[str, Json]:
    """E5 (value fork): on the two-point carrier with a three-element
    value type, the oriented apartness class contains at least two
    distinct difference presentations."""
    tables = list(product((0, 1, 2), repeat=4))
    oriented = [
        t for t in tables
        if t[0] == 0 and t[3] == 0 and t[1] != 0 and t[2] == 0]
    _require(len(oriented) >= 2,
             "value fork collapsed to one presentation")
    return {
        "value_type_size": 3,
        "tables": len(tables),
        "oriented_class_presentations": len(oriented),
    }
```

The book's check script, `textbook/checks/u69_contact_kernel.py`, verifies E1 (`witnessed_kernel_quadruples == 8`), E2 (`witnessed_kernel_counts_matching == [0, 4, 192]`), E5 (`tables == 81`, `oriented_class_presentations == 2`), `COLLISION_CELLS` (37 distinct cell IDs matching `artifacts/primitive_contact.json`), `SCOPE_KERNEL`, and Python (book) checks for the `NonZeroPair`/`SameDataKernel` correspondence across all 20 `DiffObs Bool Bool` instances, the `swapObs` fixed-point obstruction at `boolEqObs`, `vhom_not_unique`, and `freeKernel` branching.

## Line-by-line Python explanation

- `tables = list(product((0, 1, 2), repeat=4))`: enumerates all $3^4 = 81$ difference tables `delta : Bool × Bool → {0, 1, 2}` with `Zero(v) := (v == 0)`.
- `oriented = [t for t in tables if t[0] == 0 and t[3] == 0 and t[1] != 0 and t[2] == 0]`: filters for tables whose induced apartness `delta(x, y) != 0` is the oriented witness `D2` (`(False, True)` non-zero; `(False, False)`, `(True, False)`, `(True, True)` all zero). Exactly 2 tables survive: `(0, 1, 0, 0)` (`unitValKernel`) and `(0, 2, 0, 0)` (`twoValKernel`), confirming `value_presentation_fork`.
- In `u69_contact_kernel.py`:
  - `e1['witnessed_kernel_quadruples'] == 8` counts the 8 quadruples `(delta, Zero, a, b)` on `Bool` that form a valid `WitnessedDiff Bool Bool`.
  - `e2['witnessed_kernel_counts_matching'] == [0, 4, 192]` counts exact `{0, 1}`-valued kernels on carriers `1, 2, 3`: `0` on carrier 1 (`no_kernel_on_subsingleton`), `4` on carrier 2, and `192` on carrier 3, matching `a_setting_counts`.
  - Across all 64 `(delta, Zero)` pairs on `Bool`, 20 satisfy the three `DiffObs` laws: 18 are collapsed (`0` non-zero pairs, `0` same-data kernels) and 2 (`boolEqObs` and its value-negated twin) have 2 non-zero pairs (`(False, True)` and `(True, False)`), giving 2 same-data kernels each (`toPair_ofPair`, `ofPair_toPair`, `transpose_kernel_ne`).

## Lean 4

The kernel signature, both-side translations, and pair correspondence (`lean4/Derivation/ContactKernel.lean`, lines 106-399 abridged):

```lean
structure WitnessedDiff (X R : Type) where
  delta : X → X → R
  Zero : R → Prop
  a : X
  b : X
  diag_zero : ∀ x, Zero (delta x x)
  apart_ab : ¬ Zero (delta a b)

def kernelApart (K : WitnessedDiff X R) : X → X → Prop :=
  fun x y => ¬ K.Zero (K.delta x y)

theorem kernelApart_irrefl (K : WitnessedDiff X R) :
    ∀ x, ¬ kernelApart K x x :=
  fun x h => h (K.diag_zero x)

theorem kernel_endpoints_ne (K : WitnessedDiff X R) : K.a ≠ K.b :=
  fun he => K.apart_ab (by rw [he]; exact K.diag_zero K.b)

theorem no_kernel_on_subsingleton {X R : Type} [Subsingleton X]
    (K : WitnessedDiff X R) : False :=
  kernel_endpoints_ne K (Subsingleton.elim K.a K.b)

def ofSetting (S : PrimitiveCore.Setting) (h : PrimitiveCore.A S) :
    WitnessedDiff S.X Prop where
  delta := S.r
  Zero p := ¬ p
  a := S.a
  b := S.b
  diag_zero := h.2
  apart_ab hn := hn h.1

theorem ofSetting_exact (S : PrimitiveCore.Setting)
    (h : PrimitiveCore.A S) [inst : ∀ x y, Decidable (S.r x y)] :
    ∀ x y, kernelApart (ofSetting S h) x y ↔ S.r x y :=
  fun x y =>
    ⟨fun hnn =>
      match inst x y with
      | isTrue hr => hr
      | isFalse hn => absurd hn hnn,
     fun hr hn => hn hr⟩

def ofDiffObs (O : DiffObs X R) (a b : X)
    (hw : ¬ ZeroRel O a b) : WitnessedDiff X R where
  delta := O.delta
  Zero := O.Zero
  a := a
  b := b
  diag_zero := O.zero_refl
  apart_ab := hw

theorem kernel_from_obs_iff_pair (O : DiffObs X R) :
    (∃ K : WitnessedDiff X R, K.delta = O.delta ∧ K.Zero = O.Zero) ↔
      (∃ a b : X, ¬ ZeroRel O a b) := ...

abbrev NonZeroPair (O : DiffObs X R) : Type :=
  { p : X × X // ¬ ZeroRel O p.1 p.2 }

abbrev SameDataKernel (O : DiffObs X R) : Type :=
  { K : WitnessedDiff X R // K.delta = O.delta ∧ K.Zero = O.Zero }

def toPair (O : DiffObs X R) (K : SameDataKernel O) : NonZeroPair O := ...
def ofPair (O : DiffObs X R) (p : NonZeroPair O) : SameDataKernel O := ...

theorem toPair_ofPair (O : DiffObs X R) (p : NonZeroPair O) :
    toPair O (ofPair O p) = p := by apply Subtype.ext; rfl

theorem ofPair_toPair (O : DiffObs X R) (K : SameDataKernel O) :
    ofPair O (toPair O K) = K := by
  apply Subtype.ext
  exact (eq_ofDiffObs_of_fields O K.val K.property.1 K.property.2).symm

theorem transpose_kernel_ne (O : DiffObs X R) (a b : X)
    (hw : ¬ ZeroRel O a b) :
    ofDiffObs O a b hw ≠
      ofDiffObs O b a (fun h => hw (O.zero_symm h)) := by
  intro he
  have hab : a = b := congrArg (fun K => K.a) he
  apply hw
  rw [hab]
  exact O.zero_refl b
```

The fixed-point selector obstruction, `toDiffObs` record identity, pricing refutations, value fork, and non-terminality (lines 450-899 abridged):

```lean
def swapObs (O : DiffObs Bool R) : DiffObs Bool R where
  delta x y := O.delta (!x) (!y)
  Zero := O.Zero
  zero_refl := fun x => O.zero_refl (!x)
  zero_symm := fun h => O.zero_symm h
  zero_trans := fun h₁ h₂ => O.zero_trans h₁ h₂

theorem swapObs_boolEqObs : swapObs boolEqObs = boolEqObs := by
  refine obs_eq_of_fields _ _ ?_ rfl
  funext x y; revert x y; decide

theorem no_equivariant_pair_valued_map :
    ¬ ∃ sel : DiffObs Bool Bool → Bool × Bool,
        ∀ O : DiffObs Bool Bool,
          sel (swapObs O) = (!((sel O).1), !((sel O).2)) := by
  rintro ⟨sel, heq⟩
  exact no_equivariant_pair_at_fixed_point sel (heq boolEqObs)

def toDiffObs (K : WitnessedDiff X R)
    (hs : ∀ x y, K.Zero (K.delta x y) → K.Zero (K.delta y x))
    (ht : ∀ x y z, K.Zero (K.delta x y) → K.Zero (K.delta y z) →
      K.Zero (K.delta x z)) : DiffObs X R where
  delta := K.delta
  Zero := K.Zero
  zero_refl := K.diag_zero
  zero_symm := fun {x y} h => hs x y h
  zero_trans := fun {x y z} h₁ h₂ => ht x y z h₁ h₂

theorem toDiffObs_fields (K : WitnessedDiff X R) (hs : ...) (ht : ...) :
    (toDiffObs K hs ht).delta = K.delta ∧
      (toDiffObs K hs ht).Zero = K.Zero ∧
      ofDiffObs (toDiffObs K hs ht) K.a K.b K.apart_ab = K :=
  ⟨rfl, rfl, rfl⟩

theorem kernel_not_observer :
    ∃ K : WitnessedDiff Bool Prop,
      ¬ ∃ O : DiffObs Bool Prop, O.delta = K.delta ∧ O.Zero = K.Zero := ...

theorem kernel_zero_not_trans :
    ∃ K : WitnessedDiff (Fin 3) Prop,
      K.Zero (K.delta 0 2) ∧ K.Zero (K.delta 2 1) ∧ ¬ K.Zero (K.delta 0 1) := ...

theorem vhom_not_unique :
    ∃ h₁ h₂ : VHom unitValKernel boolKernel, h₁.f = h₂.f ∧ h₁ ≠ h₂ := ...

theorem vhom_unique_of_onto {X R X' R' : Type} (K : WitnessedDiff X R)
    (K' : WitnessedDiff X' R') (hsurj : DeltaOnto K)
    (h₁ h₂ : VHom K K') (hf : h₁.f = h₂.f) : h₁ = h₂ := ...

theorem kernel_gateway_unique (K : WitnessedDiff X R) :
    ∃ h : PrimitiveCats.Hom PrimitiveCats.d2Obj (apartObj K),
      ∀ h' : PrimitiveCats.Hom PrimitiveCats.d2Obj (apartObj K), h' = h :=
  PrimitiveCats.d2_initial (apartObj K)

theorem kernel_no_terminal_collector :
    ¬ ∃ (X' R' : Type) (K' : WitnessedDiff X' R'),
        ∀ (X R : Type) (K : WitnessedDiff X R),
          ∃ h : PrimitiveCats.Hom (apartObj K) (apartObj K'),
            ∀ h', h' = h := ...
```

Lean (book), from `textbook/checks/u69_lean.py`:

```lean
theorem boolKernel_deltaOnto : DeltaOnto boolKernel := by
  intro v
  cases v with
  | false => exact ⟨false, false, rfl⟩
  | true => exact ⟨false, true, rfl⟩

theorem boolKernel_vhom_unique {X' R' : Type} (K' : WitnessedDiff X' R')
    (h₁ h₂ : VHom boolKernel K') (hf : h₁.f = h₂.f) : h₁ = h₂ :=
  vhom_unique_of_onto boolKernel K' boolKernel_deltaOnto h₁ h₂ hf

theorem unitValKernel_not_deltaOnto : ¬ DeltaOnto unitValKernel := by
  intro h
  obtain ⟨x, y, hxy⟩ := h 2
  revert x y hxy
  decide

theorem kernel_licenses_entry_split {X R : Type} (K : WitnessedDiff X R) :
    (kernel_licenses_entry K).1 = kernel_endpoints_ne K ∧
    (kernel_licenses_entry K).2 = PrimitivePassage.kernel_enters_preretained :=
  ⟨rfl, rfl⟩

theorem toSetting_empty_stores {X R : Type} (K : WitnessedDiff X R) :
    (toSetting K).ret = (fun _ _ => False) ∧
    (toSetting K).prot = (fun _ _ => False) ∧
    (toSetting K).Ops = (fun _ => False) :=
  ⟨rfl, rfl, rfl⟩
```

## Line-by-line Lean explanation

- `WitnessedDiff` and `kernelApart`: `diag_zero` states `∀ x, Zero (delta x x)` and `apart_ab` states `¬ Zero (delta a b)`. Because `kernelApart K x y := ¬ K.Zero (K.delta x y)`, `kernelApart_irrefl` is `fun x h => h (K.diag_zero x)` and `kernel_endpoints_ne` rewrites `K.a = K.b` into `K.apart_ab` to contradict `K.diag_zero K.b`.
- `ofSetting` and `ofSetting_exact`: given `h : A S`, `ofSetting S h` sets `delta := S.r` and `Zero := Not`, so `kernelApart (ofSetting S h) x y` is `¬¬ S.r x y`. Under `[inst : ∀ x y, Decidable (S.r x y)]`, matching on `inst x y` eliminates the double negation.
- `toPair_ofPair`, `ofPair_toPair`, and `ofPair_injective`: `toPair` extracts `(K.val.a, K.val.b)` with its transported witness; `ofPair` applies `ofDiffObs`. Because `diag_zero` and `apart_ab` live in `Prop`, `eq_ofDiffObs_of_fields` recovers any same-data kernel by `cases` and `rfl`.
- `transpose_kernel_ne`: uses `O.zero_symm` to show `(b, a)` is also a non-zero pair of `O`. If `ofDiffObs O a b _ = ofDiffObs O b a _`, projecting `.a` via `congrArg` gives `a = b`, which contradicts `hw : ¬ ZeroRel O a b` by `O.zero_refl b`.
- `swapObs_boolEqObs` and `no_equivariant_pair_valued_map`: `obs_eq_of_fields` reduces equality of `DiffObs` records to equality of `delta` and `Zero` (since the three law fields are in `Prop`). `funext x y; revert x y; decide` checks `xor (!x) (!y) = xor x y`. At the fixed point `boolEqObs`, `heq boolEqObs` forces `!(sel boolEqObs).1 = (sel boolEqObs).1`, which `decide` refutes.
- `toDiffObs` and `toDiffObs_fields`: copies `K.delta`, `K.Zero`, and `K.diag_zero` into a `DiffObs` alongside the two supplied hypotheses `hs` and `ht`; all three conjuncts of `toDiffObs_fields` hold by `rfl`.
- `kernel_not_observer`, `kernel_not_bs`, `kernel_zero_not_trans`, `kernel_not_bc`: package `PrimDiff.D2` (on `Bool`) and `Apartness.triSymRel` (on `Fin 3`) as `Prop`-valued kernels with `Zero := Not`, replaying the two-point orientation refutation and the three-point `symm_without_cotrans_breaks_trans` witness at the kernel stratum.
- `vhom_not_unique` and `vhom_unique_of_onto`: `vhom_not_unique` exhibits two morphisms `unitValKernel → boolKernel` with `f = id` and value maps `v == 1` versus `v != 0`, which disagree at `v = 2`. When `hsurj : DeltaOnto K` holds, every `v : R` is `K.delta x y` for some `(x, y)`, so `h₁.g v = K'.delta (h₁.f x) (h₁.f y) = K'.delta (h₂.f x) (h₂.f y) = h₂.g v` by `funext`.
- `kernel_no_terminal` and `kernel_no_terminal_collector`: on `freeKernel` (carrier `Fin 3`, single edge `(0, 1)`), sending `2` to `K'.a` and sending `2` to `K'.b` both preserve the single edge `(0, 1) ↦ (K'.a, K'.b)` and differ at `2` by `kernel_endpoints_ne K'`.
- Book `kernel_licenses_entry_split` and `toSetting_empty_stores`: demonstrate by `rfl` that `kernel_licenses_entry K` is the pair of `kernel_endpoints_ne K` with the kernel-independent constant `PrimitivePassage.kernel_enters_preretained`, and that `toSetting K` sets `ret`, `prot`, and `Ops` to `False` by policy.

## What has been proved

- **The replacement kernel and its realizations**: `WitnessedDiff` satisfies `kernelApart_irrefl`, `kernel_endpoints_ne`, `no_kernel_on_subsingleton`, `toSetting_A`, `toNativeKernel`, `ofSetting_exact` (under `[∀ x y, Decidable (S.r x y)]`), and `ofSetting_ret_irrelevant`.
- **Observer-to-kernel pair correspondence and non-uniqueness**: `kernel_from_obs_iff_pair`, `eq_ofDiffObs_of_fields`, `obs_eq_of_fields`, `toPair_ofPair`, `ofPair_toPair`, `ofPair_injective`, `transpose_kernel_ne`, `kernel_not_unique_of_pair`, `two_kernels_from_one_observer`, `pair_choice_not_unique`, `swapObs_boolEqObs`, `no_equivariant_pair_at_fixed_point`, `no_equivariant_pair_valued_map`, and `kernel_no_witness_from_collapse`.
- **Record identity on the observer side**: `toDiffObs`, `toDiffObs_fields`, and `toDiffObs_apart` show definitionally (`rfl` / `Iff.rfl`) that `WitnessedDiff` plus zero-symmetry and zero-transitivity is `DiffObs`.
- **Pricing of omitted laws and candidate readings**: `kernel_not_observer` and `kernel_not_bs` (carrier 2), `kernel_zero_not_trans` and `kernel_not_bc` (carrier 3), `kernel_located_of_decidable` (under `[∀ v, Decidable (K.Zero v)]`), `kernel_not_c`, `kernel_not_f`, `kernel_to_w`, `kernel_to_d`, `kernel_to_e_empty`, `kernel_not_e_merged`, and `no_kernel_over_allzero`.
- **Value fork, `VHom` rigidity, and `apartObj` initiality/non-terminality**: `value_presentation_fork`, `vhom_not_unique`, `vhom_unique_of_onto`, `boolKernel_apart_iff`, `apartObj_irrefl`, `apartObj_sym_of_observer`, `kernel_gateway_unique`, `kernel_gateway_injective`, `kernel_gateways_not_identical`, `kernel_no_terminal`, `kernel_no_terminal_collector`, `passage_gateway_unique`, `kernel_licenses_entry`, `entry_pre_observation`, `kernel_two_point_presentation`, and `contactCells_length`.

## What has not been proved

- **What `kernel_licenses_entry` does and does not connect**: The module header says "the kernel enters the sealed passage at the pre-retention state." In Lean, `kernel_licenses_entry (K : WitnessedDiff X R)` has type `K.a ≠ K.b ∧ A (inducedSetting preRetained 0 1) ∧ preRetained.wit = []`. As `Textbook.U69.kernel_licenses_entry_split` checks by `rfl`, only the first conjunct (`K.a ≠ K.b`) mentions `K`; the second and third conjuncts are the sealed constant `PrimitivePassage.kernel_enters_preretained` about the fixed state `preRetained` on `Nat`, and no map from an arbitrary kernel `K` into a passage state `PState` is constructed.
- **Scope of `apartObj` non-terminality and categorical vocabulary**: `apartObj K : PrimitiveCats.PtdRel` discards the value type `R` and the map `K.delta`, retaining only `kernelApart K`. Consequently, `kernel_no_terminal` and `kernel_no_terminal_collector` refute a terminal collector at the `PrimitiveCats.Hom` grade of induced pointed relations; nothing is claimed about terminality in `VHom`. Moreover, `ContactKernel` defines no identity or composition for `VHom`, builds no subcategory for `SymObj` (`apartObj_sym_of_observer`), and uses "epi grade" in the docstring of `vhom_unique_of_onto` to mean `DeltaOnto` (surjectivity of `K.delta`).
- **Sufficiency-only conditions**: `vhom_unique_of_onto` establishes that `DeltaOnto K` is sufficient for carrier-map uniqueness of `VHom` (paired with one non-onto countermodel `vhom_not_unique`), and `kernel_two_point_presentation` establishes that `[DecidableEq X]` is sufficient for `∃ p : X → Nat, p K.a = 0 ∧ p K.b = 1`; neither converse is proved.
- **Policy read-backs and textual matrix evidence**: `kernel_not_c`, `kernel_not_f`, and `kernel_to_e_empty` hold because `toSetting K` sets `prot`, `ret`, and `Ops` to `False` by definition (`Textbook.U69.toSetting_empty_stores`). In `contactCells`, Lean checks `contactCells.length = 37` (`contactCells_length`), while the evidence strings are checked textually by `tests/test_primitive_contact.py`.

## Outside the system

- **Metatheoretic types, function spaces, and `Nat` carriers**: `WitnessedDiff X R` is polymorphic over `X R : Type`; `kernel_no_terminal_collector` quantifies over all `(X R : Type)` at type level 0; `no_equivariant_pair_valued_map` quantifies over the total function space `DiffObs Bool Bool → Bool × Bool`; `passageObj` has carrier `Nat`; and `kernel_two_point_presentation` returns `p : X → Nat`. All of these are Lean metatheory; no system state owns a `WitnessedDiff`.
- **Two distinct decidability hypotheses**: `ofSetting_exact` assumes `[∀ x y, Decidable (S.r x y)]` on the native setting's relation, whereas `kernel_located_of_decidable` assumes `[∀ v, Decidable (K.Zero v)]` on the kernel's zero predicate (`open_kernel_grade` and `open_kernel_bl` record the undecidable cases as `OPEN`).
- **Axiom budget**: All 53 theorems in `ContactKernel.lean` lie within `{propext, Quot.sound}`: 41 are axiom-free, 4 use `propext` (`kernel_zero_not_trans`, `kernel_not_bc`, `kernel_no_terminal`, `kernel_no_terminal_collector`), 5 use `Quot.sound` via `funext` (`vhom_unique_of_onto`, `kernel_gateway_unique`, `swapObs_boolEqObs`, `no_equivariant_pair_at_fixed_point`, `no_equivariant_pair_valued_map`), and 3 use both (`passage_gateway_unique`, `kernel_licenses_entry`, `entry_pre_observation`).

## Student exercise

Using `Textbook.U69.boolKernel_deltaOnto` and `Textbook.U69.unitValKernel_not_deltaOnto` as models, explain why every `VHom boolKernel K'` is completely determined by its carrier map `f : Bool → X'`, whereas `VHom unitValKernel boolKernel` admits two distinct morphisms sharing `f = id`. Which specific value in `Nat` lies outside the image of `unitValKernel.delta`, and how do the two morphisms in `vhom_not_unique` assign that value?

## Answer

Because `boolKernel.delta : Bool → Bool → Bool` takes both `false` (at `(false, false)`) and `true` (at `(false, true)`), `boolKernel` satisfies `DeltaOnto` (`Textbook.U69.boolKernel_deltaOnto`). By `vhom_unique_of_onto` (`Textbook.U69.boolKernel_vhom_unique`), any two morphisms `h₁, h₂ : VHom boolKernel K'` with `h₁.f = h₂.f` must agree on every `v : Bool` because `hᵢ.g v = K'.delta (hᵢ.f x) (hᵢ.f y)` at a pair `(x, y)` with `boolKernel.delta x y = v`. By contrast, `unitValKernel.delta : Bool → Bool → Nat` takes only the values `0` and `1`, so `2 : Nat` (and every `n ≥ 2`) lies outside its image (`Textbook.U69.unitValKernel_not_deltaOnto`). In `vhom_not_unique`, both morphisms use `f = id` and send `0 ↦ false` and `1 ↦ true`, but the first uses `g₁ := (· == 1)` (sending `2 ↦ false`) while the second uses `g₂ := (· != 0)` (sending `2 ↦ true`).

## Verification

Run from the repository root:

```sh
python textbook/checks/u69_contact_kernel.py
python textbook/checks/u69_lean.py
```

Both scripts must exit `0` with `failures: []`.
