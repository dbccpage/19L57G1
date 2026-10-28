# Unit 68. What an observer buys from an apartness, and what it costs back

**Claim.** `ContactBridge` compares the observer presentation of difference
(`DiffInterface.DiffObs`, Unit 44) with the relational candidate readings
(`PrimitiveCore`, Unit 51) and positive apartness (`Apartness.IsApart`,
Unit 56), in both directions. From any observer `O : DiffObs X R`, the
zero-complement `obsApart O x y := ¬ ZeroRel O x y` gets irreflexivity,
symmetry, and double-negation stability for free by contraposing `O`'s law
fields (`obsApart_irrefl`, `obsApart_symm`, `obsApart_stable`,
`zeroRel_indist`). Given a complement-witnessed pair `hab : obsApart O a b`,
the empty-store setting `obsSetting O a b` satisfies candidate readings W, A,
Bs, D, and E-at-empty-stores outright (`obsSetting_w`, `obsSetting_a`,
`obsSetting_bs`, `obsSetting_d`, `obsSetting_e`), while Bc, Bl, and positive
apartness of `obsApart O` hold under an explicit pointwise decidability
hypothesis `[∀ x y, Decidable (ZeroRel O x y)]` (`obsApart_cotrans`,
`obsSetting_bc`, `obsSetting_bl`, `obsApart_isApart`, `indist_obsApart_iff`;
under that hypothesis indistinguishability of `obsApart O` is transitive,
`obsApart_indist_trans`). In the converse direction, an admitted apartness
`h : IsApart r` builds a Prop-valued observer `apartObs r h` by spending its
three admitted laws one for one (`apartObs_zeroRel`), and recovers
`obsApart (apartObs r h) x y ↔ r x y` under a *different*, non-interchangeable
decidability hypothesis `[∀ x y, Decidable (r x y)]` (`apartObs_roundtrip`,
`isApart_repr`). A relation `r : X → X → Prop` is the zero-complement of some
`DiffObs X Prop` if and only if `¬ r` is an equivalence and `r` is
double-negation stable (`obsApart_repr_iff`); four finite countermodels
refute representability or witness transport at carriers 1, 2, 3, and 2
(`unit_total_not_repr`, `d2_not_obs_complement`, `triSym_not_obs_complement`,
`d_not_witnessed_repr`), with carrier 3 proved minimal for Bs by
`bool_bs_repr`. Dropping decidability across all observers is priced against
constructive logic: the unconditional cotransitivity schema is equivalent to
the weak law of excluded middle (`cotrans_schema_iff_wlem`), the stability
schema is equivalent to double-negation elimination (`stability_schema_iff_dne`),
and the locatedness schema implies the weak law (`located_schema_implies_wlem`).
At the passage's declared observation stage, the Boolean zero predicate
`zeroP cols` equals the zero relation of `kernelObs (colView cols)`
(`declared_zero_as_view`, `observation_stage_realizes_observer`), where the
parked `DiffAnchor` module names `colObs cols := kernelObs (colView cols)`
and establishes exact quotient identification (`colObs_quotient_eq_iff_zeroP`) and
binary difference descent (`colObs_deltaConstant`), guarded against root
name collisions by the parked probe `DiffAnchorCompat`. Finally, a zero-pair
separated by a view is equivalent to a `CollapseCollision` at the quotient
projection (`pair_blocked_iff_collapse_collision`). **Status:** FROZEN
(free laws, representability crown, pricing schemas, passage placement,
`DiffAnchor` corollaries); CONDITIONAL (candidate cells and round trips under
`hab` and the two decidability admissions); REFUTED (the four countermodels;
C and F at empty stores); OPEN (`open_bridge_cotrans`, `open_bridge_located`,
converse of `located_schema_implies_wlem`); VERIFIED_FINITE (E1 and E2
enumerations in Python). **Lean:** `lean4/Derivation/ContactBridge.lean`
lines 105-710 (imports `ObsDescent`, `PrimitiveCore`, `PrimitiveCats`,
`Apartness`, `PrimitivePassage`), plus parked `lean4/Derivation/DiffAnchor.lean`
lines 39-73 and `lean4/Derivation/DiffAnchorCompat.lean` lines 1-17.
**Axioms:** 35 reports for `ContactBridge` (`artifacts/lean_axioms.txt` lines
1113-1147: 29 none, 1 `propext`, 1 `Quot.sound`, 4 `propext, Quot.sound`) and
3 reports for `DiffAnchor` (lines 1490-1492: all `propext, Quot.sound`).
**Depends on:** Unit 44 (`DiffObs`, `ZeroRel`, `kernelObs`), Unit 51
(`Setting`, W..F, `Cotrans`, `Located`), Unit 54 (`zeroP`), Unit 56
(`IsApart`, `Indist`, `triSymRel`), Unit 67 (`ObsQuotient`,
`obsQuotient_mk_eq_iff`, `DeltaConstant`).

## Question

Which of the nine candidate readings of difference (Unit 51) and the three
laws of positive apartness (Unit 56) does the complement of an observer's zero
relation satisfy for free, which require a decidability admission, why are the
two decidability admissions in the round trip between observers and
apartnesses not interchangeable, and what happens at the passage's declared
observation columns?

## What we already possess

- From Unit 44 and Unit 67: `DiffObs X R`, `ZeroRel O x y`, `kernelObs view`,
  `ObsQuotient.mk O`, `obsQuotient_mk_eq_iff`, and `DeltaConstant`.
- From Unit 51 (`PrimitiveCore`): `Setting`, the nine readings `W`, `A`, `Bs`,
  `Bc`, `Bl`, `C`, `D`, `E`, `F`, `Cotrans`, `Located`, `imp_a_d`,
  `e_empty_iff_d`, and `located_of_decidable`.
- From Unit 54 (`PrimitivePassage`): `zeroP cols i j : Bool`, testing whether
  no declared column `c ∈ cols` separates `i` and `j`.
- From Unit 56 (`Apartness`): `IsApart r` (irreflexivity, symmetry,
  cotransitivity), `Indist r x y := ¬ r x y`, `triSymRel` on `Fin 3`, and
  `symm_without_cotrans_breaks_trans`.

## New concept: zero-complements, two decidability prices, and schema pricing

1. **The zero-complement (`obsApart`).** An observer `O : DiffObs X R` defines
   `obsApart O x y := ¬ ZeroRel O x y`. Because `O.zero_refl` and
   `O.zero_symm` hold for `ZeroRel O`, contraposition gives irreflexivity
   (`¬ obsApart O x x`) and symmetry (`obsApart O x y → obsApart O y x`) with
   no extra hypothesis. Because `obsApart` is already a negation, triple
   negation collapses constructively (`¬¬ obsApart O x y → obsApart O x y`,
   `obsApart_stable`), and every zero-pair is indistinguishable in `obsApart O`
   (`zeroRel_indist`).
2. **Why cotransitivity and the round trips cost two distinct decidability
   admissions.**
   - *Observer to apartness:* To show `obsApart O x y → obsApart O x z ∨ obsApart O z y`
     from `O.zero_trans`, we must split cases on whether `ZeroRel O x z` holds:
     if `ZeroRel O x z` fails, we have `obsApart O x z` (left disjunct); if
     `ZeroRel O x z` holds, then `ZeroRel O z y` would compose via
     `O.zero_trans` to give `ZeroRel O x y`, contradicting `obsApart O x y`,
     so `obsApart O z y` holds (right disjunct). That case split requires
     `[∀ x y, Decidable (ZeroRel O x y)]` (`obsApart_cotrans`). Under the same
     hypothesis, `Indist (obsApart O) x y := ¬¬ ZeroRel O x y` collapses back
     to `ZeroRel O x y` (`indist_obsApart_iff`), so indistinguishability of
     `obsApart O` is transitive (`obsApart_indist_trans`).
   - *Apartness to observer:* Given `h : IsApart r`, `apartObs r h` sets
     `delta := r` and `Zero := Not`, so `ZeroRel (apartObs r h) x y` is
     `¬ r x y`, and `obsApart (apartObs r h) x y` is `¬¬ r x y`. Recovering
     `r x y` from `¬¬ r x y` (`apartObs_roundtrip`) requires
     `[∀ x y, Decidable (r x y)]`. Decidability of `ZeroRel (apartObs r h) x y`
     is decidability of `¬ r x y`, which does not constructively give
     decidability of `r x y`. Thus the two decidability admissions cannot
     substitute for each other.
3. **Pricing schemas without classical axioms.** Why can we not exhibit a
   concrete observer inside Lean whose `obsApart` fails cotransitivity?
   Because `Cotrans (obsApart O)` is classically true for every observer, so no
   consistent internal countermodel exists. Instead, `ContactBridge` builds a
   three-point observer `wlemZero P` parametrized by an arbitrary proposition
   `P : Prop` and shows that `∀ X R O, Cotrans (obsApart O)` is logically
   equivalent to the weak law of excluded middle `∀ P : Prop, ¬ P ∨ ¬¬ P`
   (`cotrans_schema_iff_wlem`), and similarly `Indist (obsApart O) x y → ZeroRel O x y`
   across all observers is equivalent to double-negation elimination
   `∀ P : Prop, ¬¬ P → P` (`stability_schema_iff_dne`). Neither proof uses any
   classical axiom; the classical principles sit inside the quantified
   statements being equated.
4. **The declared-column anchor (`colView` and `DiffAnchor`).** For a list of
   declared observation columns `cols : List (List Nat)`,
   `colView cols i := cols.map (fun c => decide (i ∈ c))` records which columns
   contain `i`. `declared_zero_as_view` establishes by induction on `cols` that
   `zeroP cols i j = true ↔ ZeroRel (kernelObs (colView cols)) i j`. The
   parked module `DiffAnchor` names `colObs cols := kernelObs (colView cols)`
   and notes that its quotient identifies `i` and `j` if and only if
   `zeroP cols i j = true` (`colObs_quotient_eq_iff_zeroP`) and its difference
   map is `DeltaConstant` (`colObs_deltaConstant`).

## Plain-language interpretation

Suppose an outside development arrives with an observer `O` (a difference map,
a zero test, and the three equivalence laws for "zero difference"), while the
native development works either with the nine candidate readings W through F
(Unit 51) or with a three-law positive apartness relation `r` (Unit 56). How
much of one can be built from the other?

Start with an observer `O` and define "apart" to mean "not zero-related"
(`obsApart O`). Because every item has zero difference from itself, no item is
apart from itself (`obsApart_irrefl`). Because zero difference is symmetric,
apartness is symmetric (`obsApart_symm`). If you are also handed a pair `(a, b)`
that is apart, you immediately have a witnessed irreflexive symmetric setting
(readings W, A, Bs, D, and E when no operations are admitted). You do *not*
get protection (C) or retention (F), because an observer carries no stores
(`obsSetting_not_c`, `obsSetting_not_f`). And you do *not* get cotransitivity
(Bc) or locatedness (Bl) for free: turning transitivity of `ZeroRel` into
cotransitivity of `¬ ZeroRel` requires being able to decide whether a third
point `z` is zero-related to `x`. If you pay that decidability price, you get
Bc, Bl, and a full `IsApart` structure (`obsApart_isApart`).

Now go the other way: start with a relation `r` on `X`. When is `r` the
zero-complement of *some* observer? Since `obsApart O` is always irreflexive
and symmetric, any relation that fails irreflexivity (`unit_total_not_repr` on
1 point) or fails symmetry (`d2_not_obs_complement` on 2 points, for *any*
value type `R`) can never be represented as `obsApart O`. Even if `r` is
irreflexive and symmetric, its complement `¬ r` must be transitive: on 2 points
every irreflexive symmetric relation with a witness is representable without
any decidability hypothesis (`bool_bs_repr`), but on 3 points `triSymRel`
(which relates `(0, 1)` and `(1, 0)` and leaves `2` unrelated to both) has
`0` not apart from `2` and `2` not apart from `1` while `0` is apart from `1`,
breaking transitivity of `ZeroRel` (`triSym_not_obs_complement`). The exact
condition for a Prop-valued observer to represent `r` is that `¬ r` is an
equivalence relation and `r` is double-negation stable (`obsApart_repr_iff`).

Finally, in the passage dynamics of Unit 54, once observation columns `cols`
are declared, `zeroP cols i j` checks whether `i` and `j` have the same
membership bit in every column. That is literally view equality for the
membership-profile view `colView cols`, so at the declared observation stage
the three equivalence laws of `kernelObs (colView cols)` are proved from list
equality rather than admitted as bare hypotheses (`declared_zero_as_view`).

## Pseudocode

```text
obsApart(O, x, y) := not ZeroRel(O, x, y)
free laws:
    obsApart_irrefl : not obsApart(O, x, x)                 -- from O.zero_refl
    obsApart_symm   : obsApart(O, x, y) -> obsApart(O, y, x) -- from O.zero_symm
    obsApart_stable : not not obsApart(O, x, y) -> obsApart(O, x, y)

given hab : obsApart(O, a, b), obsSetting(O, a, b) (empty ret, prot, Ops):
    free cells      : W, A, Bs, D, E
    refuted cells   : not C, not F (stores empty by policy)
    priced at Decidable(ZeroRel O x y) : Cotrans (Bc), Located (Bl), IsApart

converse (apartObs(r, h) with delta := r, Zero := Not):
    ZeroRel(apartObs(r, h), x, y) <-> Indist(r, x, y)       -- Iff.rfl
    priced at Decidable(r x y)    : obsApart(apartObs(r, h), x, y) <-> r(x, y)
    (note: Decidable(ZeroRel) and Decidable(r) are NOT interchangeable)

obsApart_repr_iff(r):
    (exists O : DiffObs X Prop, obsApart O <-> r)
        <-> Equivalence(not r) and (for all x, y: not not r x y -> r x y)
countermodels:
    n=1: unit_total_not_repr        (breaks irreflexivity)
    n=2: d2_not_obs_complement      (breaks symmetry, any R)
    n=3: triSym_not_obs_complement  (breaks zero-transitivity, minimal by bool_bs_repr at n=2)
    n=2: d_not_witnessed_repr       (all-zero observer has no witness)

schema prices (over all X, R, O):
    (forall O, Cotrans(obsApart O))              <->  forall P, not P or not not P   (WLEM)
    (forall O x y, Indist(obsApart O) -> ZeroRel) <-> forall P, not not P -> P       (DNE)
    (forall O, Located(obsApart O))              ->   forall P, not P or not not P   (WLEM)

passage placement & DiffAnchor (parked):
    colView(cols)(i) := [i in c for c in cols]
    zeroP(cols, i, j) = true  <->  ZeroRel(colObs(cols), i, j)
                              <->  ObsQuotient.mk(colObs(cols), i) = ObsQuotient.mk(colObs(cols), j)
    DeltaConstant(colObs(cols)) holds
```

## Python

Genesis's finite enumerations E1 (`enum_bool_observers`) and E2
(`enum_settings_kernels`) live in `code/run_primitive_contact.py`, and the
countermodel checks on carriers 1, 2, and 3 live in
`code/derivation/apartness.py`:

```python
# Python (Genesis), code/run_primitive_contact.py lines 339-381 (abridged)
        def symm_comp(r: tuple[bool, ...]) -> bool:
            return all(not r_at(r, j, i)
                       for i in pts for j in pts
                       if not r_at(r, i, j))

        def trans_comp(r: tuple[bool, ...]) -> bool:
            return all(not r_at(r, i, k)
                       for i in pts for j in pts for k in pts
                       if not r_at(r, i, j) and not r_at(r, j, k))

        def representable(r: tuple[bool, ...]) -> bool:
            return irrefl(r) and symm_comp(r) and trans_comp(r)

        repr_counts.append(sum(1 for r in rels if representable(r)))
        wa, wb = 0, (1 if n > 1 else 0)
        witnessed_counts.append(sum(
            1 for r in rels if representable(r) and r_at(r, wa, wb)))

        def cotrans(r: tuple[bool, ...]) -> bool:
            return all(
                r_at(r, i, k) or r_at(r, k, j)
                for i in pts for j in pts for k in pts
                if r_at(r, i, j))

        _require(all(cotrans(r) == trans_comp(r) for r in rels),
                 f"cotransitivity vs complement-transitivity, n={n}")
```

The book's check script, `textbook/checks/u68_contact_bridge.py`, runs E1, E2,
and `apartness.insufficiency_countermodels()`, verifies the scope strings in
`artifacts/primitive_contact.json`, and adds Python (book) checks for
`bool_bs_repr`, `colView`/`zeroP`, and `DiffAnchor`'s `DeltaConstant`.

## Line-by-line Python explanation

- `symm_comp(r)` and `trans_comp(r)`: test whether the complement `not r` is
  symmetric and transitive on `range(n)`. Together with `irrefl(r)` (which is
  reflexivity of `not r`), `representable(r)` is the exact finite-carrier slice
  of `obsApart_repr_iff` (where double-negation stability is automatic because
  `r` is Bool-valued).
- `repr_counts`: counts how many relations on $n = 1, 2, 3$ points are
  observer complements. Because `r` is determined by its complement equivalence
  relation, the counts are the Bell numbers `[1, 2, 5]`; requiring the witness
  `(0, 1)` gives `[0, 1, 3]`.
- `cotrans(r) == trans_comp(r)`: on decidable (Boolean) tables, cotransitivity
  of `r` is identical to transitivity of `not r` across all $2 + 16 + 512 = 530$
  relations on $n = 1, 2, 3$ points, mirroring `obsApart_cotrans` and
  `apartObs.zero_trans`.

## Lean 4

The zero-complement, candidate cells, and apartness round trip
(`lean4/Derivation/ContactBridge.lean` lines 116-283, abridged):

```lean
def obsApart (O : DiffObs X R) (x y : X) : Prop := ¬ ZeroRel O x y

theorem obsApart_irrefl (O : DiffObs X R) :
    PrimDiff.Irrefl (obsApart O) :=
  fun x h => h (O.zero_refl x)

theorem obsApart_symm (O : DiffObs X R) :
    ∀ x y, obsApart O x y → obsApart O y x :=
  fun _ _ hxy hz => hxy (O.zero_symm hz)

theorem obsApart_stable (O : DiffObs X R) :
    ∀ x y, ¬ ¬ obsApart O x y → obsApart O x y :=
  fun _ _ h3 hz => h3 fun hn => hn hz

theorem obsApart_cotrans (O : DiffObs X R)
    [inst : ∀ x y, Decidable (ZeroRel O x y)] :
    PrimitiveCore.Cotrans (obsApart O) :=
  fun x _ hxy z =>
    match inst x z with
    | isTrue hxz => Or.inr fun hzy => hxy (O.zero_trans hxz hzy)
    | isFalse hxz => Or.inl hxz

def apartObs (r : X → X → Prop) (h : Apartness.IsApart r) :
    DiffObs X Prop where
  delta x y := r x y
  Zero := Not
  zero_refl x := h.irrefl x
  zero_symm := fun {x y} hxy hyx => hxy (h.symm y x hyx)
  zero_trans := fun {x y z} hxy hyz hxz =>
    match h.cotrans x z hxz y with
    | Or.inl h1 => hxy h1
    | Or.inr h2 => hyz h2

theorem apartObs_roundtrip (r : X → X → Prop)
    (h : Apartness.IsApart r) [inst : ∀ x y, Decidable (r x y)] :
    ∀ x y, obsApart (apartObs r h) x y ↔ r x y :=
  fun x y =>
    ⟨fun hnn =>
      match inst x y with
      | isTrue hr => hr
      | isFalse hn => absurd hn hnn,
     fun hr hn => hn hr⟩

theorem indist_obsApart_iff (O : DiffObs X R)
    [inst : ∀ x y, Decidable (ZeroRel O x y)] :
    ∀ x y, Apartness.Indist (obsApart O) x y ↔ ZeroRel O x y := ...
```

Representability crown, countermodels, pricing schemas, and passage placement
(lines 319-709, abridged):

```lean
theorem obsApart_repr_iff (r : X → X → Prop) :
    (∃ O : DiffObs X Prop, ∀ x y, obsApart O x y ↔ r x y) ↔
      (Equivalence (fun x y => ¬ r x y) ∧
        ∀ x y, ¬ ¬ r x y → r x y) := by ...

theorem unit_total_not_repr :
    ¬ ∃ O : DiffObs Unit Prop,
        ∀ x y, obsApart O x y ↔ (fun _ _ : Unit => True) x y := ...

theorem d2_not_obs_complement :
    ¬ ∃ (R : Type) (O : DiffObs Bool R),
        ∀ x y, obsApart O x y ↔ PrimDiff.D2 x y := ...

theorem triSym_not_obs_complement :
    ¬ ∃ (R : Type) (O : DiffObs (Fin 3) R),
        ∀ x y, obsApart O x y ↔ Apartness.triSymRel x y := ...

theorem bool_bs_repr (r : Bool → Bool → Prop) (hw : r false true)
    (hi : PrimDiff.Irrefl r) (hs : ∀ x y, r x y → r y x) :
    ∃ O : DiffObs Bool Prop, ∀ x y, obsApart O x y ↔ r x y := ...

theorem cotrans_schema_iff_wlem :
    (∀ (X R : Type) (O : DiffObs X R),
        PrimitiveCore.Cotrans (obsApart O)) ↔
      ∀ P : Prop, ¬ P ∨ ¬ ¬ P := ...

theorem stability_schema_iff_dne :
    (∀ (X R : Type) (O : DiffObs X R) (x y : X),
        Apartness.Indist (obsApart O) x y → ZeroRel O x y) ↔
      ∀ P : Prop, ¬ ¬ P → P := ...

theorem located_schema_implies_wlem :
    (∀ (X R : Type) (O : DiffObs X R),
        PrimitiveCore.Located (obsApart O)) →
      ∀ P : Prop, ¬ P ∨ ¬ ¬ P := ...

def colView (cols : List (List Nat)) : Nat → List Bool :=
  fun i => cols.map fun c => decide (i ∈ c)

theorem declared_zero_as_view (cols : List (List Nat)) (i j : Nat) :
    PrimitivePassage.zeroP cols i j = true ↔
      ZeroRel (kernelObs (colView cols)) i j := ...
```

Parked `DiffAnchor` (`lean4/Derivation/DiffAnchor.lean` lines 44-72):

```lean
def colObs (cols : List (List Nat)) : DiffObs Nat (List Bool × List Bool) :=
  kernelObs (ContactBridge.colView cols)

theorem colObs_quotient_eq_iff_zeroP (cols : List (List Nat)) (i j : Nat) :
    ObsQuotient.mk (colObs cols) i = ObsQuotient.mk (colObs cols) j
      ↔ PrimitivePassage.zeroP cols i j = true := by
  rw [obsQuotient_mk_eq_iff, colObs_zeroRel_iff_zeroP]

theorem colObs_deltaConstant (cols : List (List Nat)) :
    DeltaConstant (colObs cols) := by
  intro x x' y y' hx hy
  have hx' : ContactBridge.colView cols x = ContactBridge.colView cols x' := hx
  have hy' : ContactBridge.colView cols y = ContactBridge.colView cols y' := hy
  show (ContactBridge.colView cols x, ContactBridge.colView cols y)
     = (ContactBridge.colView cols x', ContactBridge.colView cols y')
  rw [hx', hy']
```

Lean (book), from `textbook/checks/u68_lean.py`:

```lean
theorem obsApart_indist_trans {X R : Type} (O : DiffObs X R)
    [∀ x y, Decidable (ZeroRel O x y)] :
    ∀ x y z, Apartness.Indist (obsApart O) x y →
      Apartness.Indist (obsApart O) y z →
      Apartness.Indist (obsApart O) x z :=
  fun x y z hxy hyz =>
    (indist_obsApart_iff O x z).mpr
      (O.zero_trans ((indist_obsApart_iff O x y).mp hxy)
        ((indist_obsApart_iff O y z).mp hyz))

theorem apartObs_refl_is_irrefl {X : Type} (r : X → X → Prop)
    (h : Apartness.IsApart r) :
    @(apartObs r h).zero_refl = fun {x} => h.irrefl x := rfl

theorem unit_total_not_repr_any_R :
    ¬ ∃ (R : Type) (O : DiffObs Unit R),
        ∀ x y, obsApart O x y ↔ (fun _ _ : Unit => True) x y := by
  rintro ⟨R, O, hO⟩
  exact obsApart_irrefl O () ((hO () ()).mpr trivial)

theorem colObs_empty_merges :
    ObsQuotient.mk (DiffAnchor.colObs []) 0 =
      ObsQuotient.mk (DiffAnchor.colObs []) 1 :=
  (DiffAnchor.colObs_quotient_eq_iff_zeroP [] 0 1).mpr rfl

theorem colObs_singleton_separates :
    ObsQuotient.mk (DiffAnchor.colObs [[0]]) 0 ≠
      ObsQuotient.mk (DiffAnchor.colObs [[0]]) 1 := by
  intro h
  have hz := (DiffAnchor.colObs_quotient_eq_iff_zeroP [[0]] 0 1).mp h
  revert hz
  decide
```

## Line-by-line Lean explanation

- `obsApart_irrefl` and `obsApart_symm`: apply the negation `h : ¬ ZeroRel O x x`
  to `O.zero_refl x`, and compose `hz : ZeroRel O x y` with `O.zero_symm`
  against `hxy : ¬ ZeroRel O x y`.
- `obsApart_cotrans`: matches on `inst x z : Decidable (ZeroRel O x z)`. In the
  `isTrue hxz` arm, any `hzy : ZeroRel O z y` yields `O.zero_trans hxz hzy`,
  contradicting `hxy`, so `¬ ZeroRel O z y` holds (`Or.inr`); in the
  `isFalse hxz` arm, `¬ ZeroRel O x z` holds directly (`Or.inl`).
- `apartObs`: packages `r` as `delta` and `Not` as `Zero`. As the book's
  `apartObs_refl_is_irrefl` checks by `rfl`, `(apartObs r h).zero_refl` is
  definitionally `h.irrefl`; `zero_symm` and `zero_trans` similarly spend
  `h.symm` and `h.cotrans`.
- `obsApart_repr_iff`: forward uses `O.zero_refl`, `O.zero_symm`, `O.zero_trans`,
  and `obsApart_stable` to show `¬ r` is an equivalence and `¬¬ r x y → r x y`;
  backward builds `{ delta := r, Zero := Not, ... }` using the equivalence
  fields of `¬ r` and discharges `obsApart O x y ↔ r x y` using `hstab`.
- `cotrans_schema_iff_wlem`: instantiates the quantified schema at the
  three-point observer `wlemZero P`, where `t0 ~ t2` is labelled by `P`,
  `t1 ~ t2` is labelled by `¬ P`, and transitivity across `t2` closes by
  `absurd hP hP'`. Since `t0` and `t1` are apart, cotransitivity against `t2`
  returns either `obsApart t0 t2` (which entails `¬ P`) or `obsApart t2 t1`
  (which entails `¬¬ P`).
- `declared_zero_as_view`: inducts on `cols : List (List Nat)`, using
  `PrimitivePassage.zeroP_cons` and the Boolean lemma
  `(!(a != b)) = true ↔ a = b` to match each column's separation test with
  head equality of `colView cols i` and `colView cols j`.
- `DiffAnchor.colObs_quotient_eq_iff_zeroP` and `colObs_deltaConstant`: rewrite
  with `obsQuotient_mk_eq_iff` and `declared_zero_as_view`, then rewrite the
  pair `(colView cols x, colView cols y)` along `hx` and `hy`.
- Book `obsApart_indist_trans`: combines `indist_obsApart_iff` and
  `O.zero_trans` to show that under `[∀ x y, Decidable (ZeroRel O x y)]`,
  indistinguishability of `obsApart O` is transitive.
- Book `colObs_empty_merges` and `colObs_singleton_separates`: show that the
  quotient of `colObs cols` depends on the declared columns `cols`: when
  `cols = []` it merges `0` and `1`, and when `cols = [[0]]` it separates them.

## What has been proved

- Free complement laws: `obsApart_irrefl` (119), `obsApart_symm` (124),
  `obsApart_stable` (130), `zeroRel_indist` (135).
- Observer-induced setting cells: `obsSetting_w` (156), `obsSetting_a` (161),
  `obsSetting_bs` (166), `obsApart_cotrans` (175), `obsSetting_bc` (184),
  `obsSetting_bl` (193), `obsSetting_d` (203), `obsSetting_e` (211), and the
  negative cells `obsSetting_not_c` (290), `obsSetting_not_f` (297),
  `kernel_prot_independent` (304).
- Apartness-observer meet under the two decidability admissions:
  `apartObs_zeroRel` (236), `apartObs_roundtrip` (244), `isApart_repr` (256),
  `obsApart_isApart` (265), `indist_obsApart_iff` (274).
- Representability characterization and four countermodels:
  `obsApart_repr_iff` (319), `unit_total_not_repr` (350),
  `d2_not_obs_complement` (362), `triSym_not_obs_complement` (377),
  `bool_bs_repr` (398), `d_not_witnessed_repr` (426).
- Classical pricing schemas: `cotrans_schema_iff_wlem` (519),
  `stability_schema_iff_dne` (550), `located_schema_implies_wlem` (578).
- Passage placement and collapse collision: `declared_zero_as_view` (628),
  `observation_stage_realizes_observer` (648), `kernel_stage_no_obstruction`
  (666), `pair_blocked_is_collapse_collision` (678),
  `collapse_collision_is_pair_blocked` (688),
  `pair_blocked_iff_collapse_collision` (701).
- Parked `DiffAnchor` corollaries: `colObs_zeroRel_iff_zeroP` (48),
  `colObs_quotient_eq_iff_zeroP` (56), `colObs_deltaConstant` (64).

## What has not been proved

- `ContactBridge` audit finding 1 (header item 7 vs `declared_zero_as_view`):
  The module header says the declared observation stage derives — at the
  sealed `kernelObs`, equality-grade — the three laws an arriving observer
  carries as proof fields". That is an instance-level fact about
  `kernelObs (colView cols)`, where `ZeroRel` is view equality. A general
  `DiffObs X R` still carries its three laws as admitted fields, and
  `apartObs r h` in this same module discharges them one-for-one from the
  admitted `IsApart` fields (`apartObs_refl_is_irrefl`).
- `ContactBridge` audit finding 2 (policy read-backs):
  `kernel_stage_no_obstruction` (`fun _ _ h => h.1`), `obsSetting_not_c`, and
  `obsSetting_not_f` hold because `kernelStage` and `obsSetting` set
  `retained := False` and `prot := False` by definition; they prove nothing
  about the observer `O` itself.
- `ContactBridge` audit finding 3 (`unit_total_not_repr` scope):
  `unit_total_not_repr` in `ContactBridge` is stated for `DiffObs Unit Prop`
  only, although `obsApart_irrefl` refutes `obsApart O () ()` for any
  `R : Type` (proved in the book's `unit_total_not_repr_any_R`). The `∃ R : Type`
  refutations (`d2_not_obs_complement`, `triSym_not_obs_complement`,
  `d_not_witnessed_repr`) range over `Type` (universe 0).
- Converse of `located_schema_implies_wlem` (`open_bridge_located`): OPEN;
  routing a locating Boolean function back from `∀ P, ¬ P ∨ ¬¬ P` would require
  a function-comprehension principle beyond the weak law.
- `DiffAnchor` audit findings 1 and 2: `colObs_deltaConstant` is called "the
  genuinely new content" in `DiffAnchor`'s docstring, but `colObs cols` is a
  `kernelObs` and `DeltaConstant` holds by the same two-line proof for every
  `kernelObs view` (Unit 67's `kernelObs_deltaConstant`). Furthermore, `cols`
  is declared data, not forced (`colObs_empty_merges` vs
  `colObs_singleton_separates`). And `DiffAnchor`'s docstring note "verified by
  hand, not by the root gate" is stale: `ParkedAudit.lean` (the second default
  target) elaborates both `DiffAnchor` and the 17-line import-collision probe
  `DiffAnchorCompat` and emits the three `DiffAnchor` axiom reports into
  `artifacts/lean_axioms.txt` (lines 1490-1492).

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `{X R : Type}`, `∃ R : Type` | carrier and value types in universe 0 | metatheoretic types |
| `[∀ x y, Decidable (ZeroRel O x y)]`, `[∀ x y, Decidable (r x y)]` | the two non-interchangeable decidability hypotheses | conditional metatheoretic assumptions |
| `∀ P : Prop, ¬ P ∨ ¬¬ P`, `∀ P : Prop, ¬¬ P → P` | pricing schemas (`cotrans_schema_iff_wlem`, `stability_schema_iff_dne`, `located_schema_implies_wlem`) | quantified propositions inside theorem statements; never invoked as axioms |
| `colView cols : Nat → List Bool` | passage placement (`declared_zero_as_view`) and `DiffAnchor.colObs` | metatheoretic total function on `Nat` built from a finite list `cols` |

**What the system holds.** In `PrimitivePassage`, a state holds a finite list
`cols : List (List Nat)`. Turning `cols` into `colView cols : Nat → List Bool`
and forming `DiffObs Nat (List Bool × List Bool)` and its quotient
`ObsQuotient (colObs cols)` over all of `Nat` are metatheoretic constructions
about the state's column list.

## Student exercise

Explain why `[∀ x y, Decidable (ZeroRel (apartObs r h) x y)]` is weaker than
`[∀ x y, Decidable (r x y)]`, and identify which theorem in `ContactBridge`
prices the gap between `Indist r x y` (or `¬¬ r x y`) and `r x y` across all
observers.

## Answer

By definition of `apartObs r h`, `ZeroRel (apartObs r h) x y` is `¬ r x y`. So
`Decidable (ZeroRel (apartObs r h) x y)` is `Decidable (¬ r x y)`, which lets
you decide between `¬ r x y` and `¬¬ r x y`. To conclude `r x y` from the
second branch `¬¬ r x y`—which is what `apartObs_roundtrip` needs in order to
prove `obsApart (apartObs r h) x y ↔ r x y`—you need `¬¬ r x y → r x y`.
Having `Decidable (r x y)` gives `r x y ∨ ¬ r x y` directly, whereas
`Decidable (¬ r x y)` stops at `¬¬ r x y`. Across all observers, the schema
that collapses double negation (`Indist (obsApart O) x y → ZeroRel O x y`) is
priced by `stability_schema_iff_dne` at full double-negation elimination
`∀ P : Prop, ¬¬ P → P`.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/ContactBridge.lean` lines 116-150 (`obsApart`, free laws, `obsSetting`), 156-214 (candidate cells), 224-283 (`apartObs`, round trips), 290-309 (negative cells), 319-431 (`obsApart_repr_iff`, four countermodels, `bool_bs_repr`), 443-613 (`Tri`, `wlemZero`, pricing schemas), 620-709 (`colView`, `declared_zero_as_view`, `pair_blocked_iff_collapse_collision`); `lean4/Derivation/DiffAnchor.lean` lines 44-72 (`colObs`, `colObs_quotient_eq_iff_zeroP`, `colObs_deltaConstant`); `lean4/Derivation/DiffAnchorCompat.lean` lines 1-17 |
| Axiom report | `artifacts/lean_axioms.txt` lines 1113-1147 (`ContactBridge`, 35 theorems) and lines 1490-1492 (`DiffAnchor`, 3 theorems via `ParkedAudit.lean`) |
| Paper | `paper/primitive_difference_contact.md`; `paper/paper_claim_ledger.md` `CL-PD2-CONTACT-BRIDGE`, `CL-PD2-CONTACT-COUNTERMODELS` |
| Python | `code/run_primitive_contact.py` (`enum_bool_observers`, `enum_settings_kernels`, `SCOPE_EQUIVALENT`, `SCOPE_INCOMPARABLE`), `code/derivation/apartness.py` (`insufficiency_countermodels`), `artifacts/primitive_contact.json` |
| Audit | `textbook/audit/modules/ContactBridge.md` findings 1-6, `textbook/audit/modules/DiffAnchor.md` findings 1-3, `textbook/audit/modules/DiffAnchorCompat.md` |
| Check (Python) | `python textbook/checks/u68_contact_bridge.py`: E1 and E2 censuses, Bell counts `[1, 2, 5]`, cotransitivity vs complement-transitivity on 530 relations, `apartness` countermodels, scope checks, `colView`/`zeroP` and `DiffAnchor` checks |
| Check (book Lean) | `python textbook/checks/u68_lean.py`: eight book declarations plus twenty-one Genesis theorems (including all three parked `DiffAnchor` theorems) kernel-checked, Lean 4.33.0 |
