# Unit 52. The two-point witness is initial, and that is all initiality says

**Claim.** `PrimitiveCats` packages a witnessed pointed relation as an
object (`PtdRel`: carrier, relation, two points, one asserted edge) and
point-and-edge-preserving maps as morphisms (`Hom`), proves the category
laws, and settles: the oriented two-point object `d2Obj` is initial among
all objects (`d2_initial`), with no irreflexivity required of the target,
so initiality characterises the bare-witness reading W of Unit 51 and
does not select A; the symmetric object `s2Obj` is initial exactly against
symmetric targets (`s2_initial_sym`) and has no map at all into `d2Obj`
(`s2_no_hom_to_d2`); two initial objects are isomorphic (`initials_iso`)
and need not be the same presentation (`two_initials_not_identical`); a
three-point object admits two maps into `d2Obj` and is not initial
(`larger_not_initial`); every pointed endomorphism of either two-point
object fixes both points (`pointed_rigid`) while the swap is an unpointed
automorphism of `S2` only. For presentations of the three-point source the
two maximal cuts are incomparable and nothing is weakly terminal
(`no_terminal_pres`); for the two-point source unrestricted terminality
fails at a free point (`no_terminal_pres2`) and uniqueness survives
against surjective presentations (`phom2_unique_of_epi`). **Status:**
FROZEN; `s2_initial_sym` and `phom2_unique_of_epi` CONDITIONAL on their
hypotheses; terminality of `idPres2` among surjective presentations
neither proved nor refuted. **Lean:** `lean4/Derivation/PrimitiveCats.lean`
lines 36-721, imports `PrimDiff`. **Axioms:** 49 exported reports within
`{propext, Quot.sound}`; the initiality proofs use `Quot.sound` through
`funext`. **Depends on:** Units 23-24 (`D2`, `S2`, irreflexivity,
`irrefl_witness_ne`, `oriented_rigid`, `swap_is_S2_automorphism`), Unit 51
(readings W and A, `imp_a_d`, `nimp_w_d`).

## Question

Unit 51 ordered the readings of a difference by implication. Here the
question changes shape: among all the ways of realising one witnessed
pair, is there a *first* one, a realisation that maps uniquely into every
other? If so, what does being first buy, and what does it leave open: the
law of irreflexivity, the choice between two orientations, the choice of
how to write the points down?

## What we already possess

- `D2` (the edge `false → true`) and `S2` (both directions) on `Bool`;
  `D2_irrefl`, `S2_irrefl`, `irrefl_witness_ne` (Units 23-24).
- `oriented_rigid`: a map preserving and reflecting `D2` fixes both
  points; `swap_is_S2_automorphism` (Unit 24).
- Unit 51's readings W and A, and the pair `imp_a_d` / `nimp_w_d`: A
  forces the endpoints apart, W does not.
- What a structure-preserving map is: a function on carriers that sends
  the designated points to the designated points and every edge to an
  edge.

## New concept: initial object, up to isomorphism

An object `R` is *initial* when into every object `T` there is exactly
one morphism `R → T`; *weakly initial* when there is at least one. Two
objects are *isomorphic* when morphisms both ways compose to identities.
A *presentation* of a source is a map out of its carrier that keeps the
witnessed pair apart; a morphism of presentations is a map commuting
with both. *Terminal* reverses the arrows: exactly one morphism in from
everything.

The point to hold on to: "exactly one morphism" is a statement about
maps, and two different presentations can both satisfy it. Initiality
pins an object down up to isomorphism and no further.

## Plain-language interpretation

The oriented pair is the smallest thing that is a witnessed pointed
relation at all: to map it into any target you send its two points to
the target's two points, and the one edge lands on the target's own
witness. There is nothing else to decide, so there is exactly one map.
That is why it is first, and the argument never asks whether the target
is irreflexive. So being first does not justify irreflexivity; Unit 51's
`imp_a_d` against `nimp_w_d` does that, independently, and the module
says the two arguments are not to be merged.

The symmetric pair is not first. Its reversed edge needs somewhere to
go, and in an oriented target there is nowhere. It is first only among
symmetric targets, where the target's own symmetry supplies the image.

Being first does not choose an orientation or a presentation. Point the
oriented pair the other way round and it is first again; the two
presentations are not the same structure, and they are isomorphic by the
swap. A third point ruins it: a free point can go to either value, two
maps, uniqueness lost. And once points are designated, nothing can move
them: both two-point objects are rigid, so the symmetry of `S2` lives
only in the unpointed relation.

Reading the same three points as *presentations* turns the picture
round. The identity presentation is first. But there is no last one:
the two ways of collapsing the free point onto one of the designated
points are incomparable, and anything receiving maps from both would
have to collapse the designated pair. With only two points there is no
free point to cut, yet a presentation with a spare carrier point still
has two maps into any target. What survives is: from a presentation that
uses its whole carrier, at most one map.

## Pseudocode

```
object  = (X, r, a, b, witness r a b)
hom P Q = f : P.X → Q.X with f a = a', f b = b', and r x y ⇒ r' (f x) (f y)
initial R        = for every T: exactly one hom R T
d2_initial       : into T send false ↦ T.a, true ↦ T.b; the edge lands on T.w;
                   any hom agrees on both points, and Bool has no other point
s2 into oriented : the reversed edge has no image → no hom
third point      : send it to false or to true → two homs → not initial
presentation of Fin 3 = q : Fin 3 → Q with q 0 ≠ q 1
cut A: {0,2} vs {1};  cut B: {1,2} vs {0};  no map either way;
a receiver of both would force q 0 = q 1
```

## Python

Genesis has no Python mirror of this module. The check below is
**Python (book)**: it reuses Genesis's `derivation.primdiff` (pointed
structures, point-preserving maps, edge preservation, automorphisms) and
counts morphisms by exhaustive search on carriers of at most three
points. Every count is bounded and labelled so.

```python
def homs(src: Pointed, dst: Pointed) -> list[Func]:
    """Lean's `Hom src dst`: point-preserving maps that carry every edge."""
    return [f for f in pointed_maps(src, dst) if preserves_rel(f, src, dst)]

def phoms(p, r):
    """Lean's `PHom p r`: maps h with h (p.q x) = r.q x at every occurrence x."""
    (mp, qp), (mr, qr) = p, r
    return [h for h in product(range(mr), repeat=mp)
            if all(h[qp[x]] == qr[x] for x in range(len(qp)))]
```

The check's run:

```text
objects of PtdRel on 1..3 points (bounded search): 2337
maps out of d2Obj: every target receives exactly one: True (d2_initial)
maps out of d2SwapObj: exactly one each: True; d2SwapObj == d2Obj as a presentation: False (two_initials_not_identical)
wideObj 0 is d2Obj: True; its maps out, one each: True (audit finding 1)
into irreflexive targets the unique map is injective: True (d2_map_injective); into the one-point self-witness it is (0, 0): collapsed (d2_map_not_injective_without_irrefl)
objects initial against every target within the bound: [{'n': 2, 'rel': [(0, 1)], 'a': 0, 'b': 1}, {'n': 2, 'rel': [(1, 0)], 'a': 1, 'b': 0}]
maps out of s2Obj into symmetric targets: {1} (s2_initial_sym); into d2Obj: 0 (s2_no_hom_to_d2); non-symmetric targets receiving none: 776
maps bigObj 0 -> d2Obj: [(0, 1, 0), (0, 1, 1)] (bigHomA, bigHomB; larger_not_initial)
pointed automorphisms: d2Obj [(0, 1)], s2Obj [(0, 1)] (pointed_rigid); unpointed: d2 [(0, 1)], s2 [(0, 1), (1, 0)] (s2_swap_isRelAuto, d2_swap_not_isRelAuto)
faithful presentations of Fin 3 into carriers of at most 3 points: 22
  phoms mergeA -> mergeB: 0, mergeB -> mergeA: 0 (no_phom_merge*)
  maps out of idPres3: one into each: True (pres_initial)
  presentations receiving a map from every presentation within the bound: 0 (no_terminal_pres)
faithful presentations of Bool into carriers of at most 3 points: 8
  phoms into idPres2 from idPres2 1, from swapPres2 1 (phom2_unique_exists_*)
  surjective presentations send at most one map into idPres2: True (phom2_unique_of_epi)
  maps out of freePres2 into each target = size of the target's carrier: True; never one: True (no_terminal_pres2)
failures: []
```

## Line-by-line Python explanation

`homs` is the definition of `Hom` as a filter: Genesis's `pointed_maps`
lists every function between the carriers that fixes the two designated
points, and `preserves_rel` keeps those that send every edge of the
source to an edge of the target. `phoms` is `PHom`: a map on the
presentation carriers that commutes with the two presenting maps at every
occurrence.

The first block enumerates every witnessed pointed structure on one, two
and three points, 2337 of them, and counts the maps out of `d2Obj`: one
each. The same for the oppositely pointed object, which is a different
Python value. `wideObj 0` is literally `d2Obj`, which is the audit's
point about the paper's "every one of them". The injectivity line reads
the unique map into each irreflexive target and checks it has two
distinct values; into the one-point self-witness it is `(0, 0)`.

The census line asks which objects within the bound are initial against
every target within the bound and finds exactly the two pointings of the
single edge. This is a bounded statement: Lean proves initiality against
all targets for those two, and the search adds that no other small object
is initial even against small targets.

The `s2Obj` line counts maps into symmetric targets (always one), into
`d2Obj` (none), and how many non-symmetric targets receive nothing. The
three-point line prints the two maps `(0, 1, 0)` and `(0, 1, 1)`, which
are `bigHomA 0` and `bigHomB 0`: the free point `2` goes to `0` or to `1`.
Automorphisms: pointed, only the identity for both; unpointed, `S2` also
has the swap.

The presentation blocks enumerate faithful maps out of three or two
occurrences into carriers of at most three points. The two cuts have no
map either way; the identity presentation maps once into each; no
presentation within the bound receives from all. For two occurrences,
the surjective presentations send at most one map into the identity
presentation, and the presentation with a spare point sends as many maps
as the target has points, never one.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/PrimitiveCats.lean lines 36-51, 97-110, 132-137
structure PtdRel where
  X : Type
  r : X → X → Prop
  a : X
  b : X
  w : r a b

structure Hom (P Q : PtdRel) where
  f : P.X → Q.X
  ha : f P.a = Q.a
  hb : f P.b = Q.b
  hr : ∀ x y, P.r x y → Q.r (f x) (f y)

def d2Obj : PtdRel :=
  ⟨Bool, PrimDiff.D2, false, true, PrimDiff.D2_witness⟩

def s2Obj : PtdRel :=
  ⟨Bool, PrimDiff.S2, false, true, Or.inl PrimDiff.D2_witness⟩

def d2SwapObj : PtdRel :=
  ⟨Bool, fun x y => x = true ∧ y = false, true, false, ⟨rfl, rfl⟩⟩

def Initial (R : PtdRel) : Prop :=
  ∀ T : PtdRel, ∃ h : Hom R T, ∀ h' : Hom R T, h' = h

def WeaklyInitial (R : PtdRel) : Prop :=
  ∀ T : PtdRel, Nonempty (Hom R T)
```

```lean
-- Lean (Genesis), lean4/Derivation/PrimitiveCats.lean lines 156-203, 234-249
theorem d2_initial : Initial d2Obj := by
  intro T
  refine ⟨⟨fun t => cond t T.b T.a, rfl, rfl, ?_⟩, ?_⟩
  · intro x y hxy
    have hx : x = false := hxy.1
    have hy : y = true := hxy.2
    subst hx; subst hy
    exact T.w
  · intro h'
    apply hom_ext
    funext t
    cases t with
    | false => exact h'.ha
    | true => exact h'.hb

theorem d2_map_injective (P : PtdRel) (hP : IrreflObj P)
    (h : Hom d2Obj P) :
    ∀ x y : Bool, h.f x = h.f y → x = y := by
  have hne : P.a ≠ P.b := PrimDiff.irrefl_witness_ne hP P.w
  intro x y hxy
  cases x <;> cases y
  · rfl
  · exact absurd ((h.ha.symm.trans hxy).trans h.hb) hne
  · exact absurd ((h.hb.symm.trans hxy).trans h.ha) (fun e => hne e.symm)
  · rfl

theorem d2_map_not_injective_without_irrefl :
    ∃ (P : PtdRel) (h : Hom d2Obj P) (x y : Bool),
      h.f x = h.f y ∧ x ≠ y := by
  refine ⟨⟨Unit, fun _ _ => True, (), (), trivial⟩,
    ⟨fun _ => (), rfl, rfl, fun _ _ _ => trivial⟩,
    false, true, rfl, by decide⟩

theorem s2_no_hom_to_d2 : ¬ Nonempty (Hom s2Obj d2Obj) := by
  intro ⟨h⟩
  have hrev : s2Obj.r true false := Or.inr PrimDiff.D2_witness
  have hedge := h.hr true false hrev
  have h1 : h.f true = false := hedge.1
  have h2 : h.f true = true := h.hb
  rw [h1] at h2
  exact Bool.noConfusion h2

theorem s2_not_weakly_initial : ¬ WeaklyInitial s2Obj :=
  fun h => s2_no_hom_to_d2 (h d2Obj)
```

```lean
-- Lean (Genesis), lean4/Derivation/PrimitiveCats.lean lines 275-294, 320-359, 426-429
theorem two_initials_not_identical : d2Obj ≠ d2SwapObj := by
  intro h
  have h2 : HEq d2Obj.a d2SwapObj.a := by rw [h]
  have h3 : (false : Bool) = true := eq_of_heq h2
  exact Bool.noConfusion h3

theorem initials_iso (P Q : PtdRel) (hP : Initial P) (hQ : Initial Q) :
    ∃ (u : Hom P Q) (v : Hom Q P),
      comp v u = idH P ∧ comp u v = idH Q := by
  obtain ⟨u, _⟩ := hP Q
  obtain ⟨v, _⟩ := hQ P
  obtain ⟨iP, hiP⟩ := hP P
  obtain ⟨iQ, hiQ⟩ := hQ Q
  exact ⟨u, v, (hiP (comp v u)).trans (hiP (idH P)).symm,
    (hiQ (comp u v)).trans (hiQ (idH Q)).symm⟩

def bigObj (n : Nat) : PtdRel :=
  ⟨Fin (n + 3),
   fun x y => x = ⟨0, by omega⟩ ∧ y = ⟨1, by omega⟩,
   ⟨0, by omega⟩, ⟨1, by omega⟩, ⟨rfl, rfl⟩⟩

def bigHomA (n : Nat) : Hom (bigObj n) d2Obj :=
  ⟨fun x => x.val == 1, rfl, rfl, by
    intro x y hxy
    rw [hxy.1, hxy.2]
    exact PrimDiff.D2_witness⟩

def bigHomB (n : Nat) : Hom (bigObj n) d2Obj :=
  ⟨fun x => !(x.val == 0), rfl, rfl, by
    intro x y hxy
    rw [hxy.1, hxy.2]
    exact PrimDiff.D2_witness⟩

theorem larger_not_initial (n : Nat) : ¬ Initial (bigObj n) := by
  intro hinit
  obtain ⟨u, huniq⟩ := hinit d2Obj
  exact bigHomA_ne_bigHomB n
    ((huniq (bigHomA n)).trans (huniq (bigHomB n)).symm)

theorem pointed_rigid :
    (∀ h : Hom d2Obj d2Obj, h.f false = false ∧ h.f true = true) ∧
    (∀ h : Hom s2Obj s2Obj, h.f false = false ∧ h.f true = true) :=
  ⟨fun h => ⟨h.ha, h.hb⟩, fun h => ⟨h.ha, h.hb⟩⟩
```

```lean
-- Lean (Genesis), lean4/Derivation/PrimitiveCats.lean lines 446-456, 502-520, 548-563, 608-625, 666-700
structure Pres where
  Q : Type
  q : Fin 3 → Q
  faithful : q 0 ≠ q 1

structure PHom (P R : Pres) where
  h : P.Q → R.Q
  comm : ∀ x, h (P.q x) = R.q x

def mergeA : Pres := ⟨Bool, fun x => decide (x = 1), by decide⟩
def mergeB : Pres := ⟨Bool, fun x => decide (x = 0), by decide⟩

theorem no_phom_mergeA_mergeB : ¬ Nonempty (PHom mergeA mergeB) := by
  intro ⟨u⟩
  have h0 := u.comm 0
  have h2 := u.comm 2
  have h02 : mergeA.q 0 = mergeA.q 2 := rfl
  rw [h02] at h0
  have hcontra : mergeB.q 0 = mergeB.q 2 := h0.symm.trans h2
  have hb : (true : Bool) = false := hcontra
  exact Bool.noConfusion hb

theorem no_terminal_pres :
    ¬ ∃ T : Pres, ∀ P : Pres, Nonempty (PHom P T) := by
  intro ⟨T, hT⟩
  obtain ⟨uA⟩ := hT mergeA
  obtain ⟨uB⟩ := hT mergeB
  have hA0 := uA.comm 0
  have hA2 := uA.comm 2
  have h02 : mergeA.q 0 = mergeA.q 2 := rfl
  rw [h02] at hA0
  have hT02 : T.q 0 = T.q 2 := hA0.symm.trans hA2
  have hB1 := uB.comm 1
  have hB2 := uB.comm 2
  have h12 : mergeB.q 1 = mergeB.q 2 := rfl
  rw [h12] at hB1
  have hT12 : T.q 1 = T.q 2 := hB1.symm.trans hB2
  exact T.faithful (hT02.trans hT12.symm)

def Epi2 (P : Pres2) : Prop := ∀ z : P.Q, ∃ x : Bool, P.q x = z

theorem phom2_unique_of_epi (P : Pres2) (he : Epi2 P)
    (u v : PHom2 P idPres2) : u = v := by
  apply phom2_ext
  funext z
  obtain ⟨x, hx⟩ := he z
  rw [← hx, u.comm, v.comm]

def freePres2 : Pres2 :=
  ⟨Fin 3, fun x => cond x 1 0, by decide⟩

theorem no_terminal_pres2 :
    ¬ ∃ T : Pres2, ∀ P : Pres2,
      ∃ h : PHom2 P T, ∀ h' : PHom2 P T, h' = h := by
  intro ⟨T, hT⟩
  obtain ⟨h, huniq⟩ := hT freePres2
  -- two commuting maps that differ at the free point ⟨2, _⟩ ...
  ...
  exact T.faithful hat2
```

The book's Lean instantiates the universal property at the one-point
self-witness and at `s2Obj`, re-proves the audit's probe that `wideObj 0`
is initial, writes the swap isomorphism out and recovers it from
`initials_iso`, reads the two maps at the free point, writes the two cuts'
values and the two maps out of the free-point presentation, and shows that
presentation is not surjective.

```lean
-- Lean (book), textbook/checks/u52_lean.py
def unitObj : PtdRel := ⟨Unit, fun _ _ => True, (), (), trivial⟩

theorem unit_receives_one : ∃ h : Hom d2Obj unitObj, ∀ h' : Hom d2Obj unitObj, h' = h :=
  d2_initial unitObj

theorem unit_collapses (h : Hom d2Obj unitObj) : h.f false = h.f true := rfl

theorem d2_to_s2 : ∃ h : Hom d2Obj s2Obj, ∀ h' : Hom d2Obj s2Obj, h' = h :=
  d2_initial s2Obj

theorem s2_not_initial_full : ¬ ∀ T : PtdRel, ∃ h : Hom s2Obj T, ∀ h' : Hom s2Obj T, h' = h :=
  fun h => s2_not_initial h

theorem wideObj0_initial : Initial (wideObj 0) := by
  intro T
  refine ⟨⟨fun t => if t.val = 0 then T.a else T.b, rfl, rfl, ?_⟩, ?_⟩
  · intro x y hxy
    have hx : x = ⟨0, by omega⟩ := hxy.1
    have hy : y = ⟨1, by omega⟩ := hxy.2
    subst hx; subst hy
    exact T.w
  · intro h'
    apply hom_ext
    funext t
    match t with
    | ⟨0, _⟩ => exact h'.ha
    | ⟨1, _⟩ => exact h'.hb

theorem big0_free_point :
    (bigHomA 0).f ⟨2, by omega⟩ = false ∧ (bigHomB 0).f ⟨2, by omega⟩ = true :=
  ⟨rfl, rfl⟩

def toSwap : Hom d2Obj d2SwapObj :=
  ⟨Bool.not, rfl, rfl, fun x y h => ⟨by rw [h.1]; rfl, by rw [h.2]; rfl⟩⟩

def fromSwap : Hom d2SwapObj d2Obj :=
  ⟨Bool.not, rfl, rfl, fun x y h => ⟨by rw [h.1]; rfl, by rw [h.2]; rfl⟩⟩

theorem swap_iso : comp fromSwap toSwap = idH d2Obj ∧ comp toSwap fromSwap = idH d2SwapObj := by
  refine ⟨hom_ext ?_, hom_ext ?_⟩ <;> funext t <;> cases t <;> rfl

theorem swap_iso_by_initiality :
    ∃ (u : Hom d2Obj d2SwapObj) (v : Hom d2SwapObj d2Obj),
      comp v u = idH d2Obj ∧ comp u v = idH d2SwapObj :=
  initials_iso _ _ d2_initial d2Swap_initial

theorem s2_two_unpointed : IsRelAuto PrimDiff.S2 id ∧ IsRelAuto PrimDiff.S2 Bool.not :=
  ⟨⟨⟨fun _ _ h => h, fun z => ⟨z, rfl⟩⟩, s2_id_auto⟩, s2_swap_isRelAuto⟩

theorem cuts_values :
    mergeA.q 0 = false ∧ mergeA.q 1 = true ∧ mergeA.q 2 = false ∧
    mergeB.q 0 = true ∧ mergeB.q 1 = false ∧ mergeB.q 2 = false :=
  ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩

def free0 : PHom2 freePres2 idPres2 := ⟨fun z => z.val == 1, by intro x; cases x <;> rfl⟩
def free1 : PHom2 freePres2 idPres2 := ⟨fun z => !(z.val == 0), by intro x; cases x <;> rfl⟩

theorem free_maps_differ : free0 ≠ free1 := by
  intro h
  have h2 := congrArg (fun u : PHom2 freePres2 idPres2 => u.h ⟨2, by omega⟩) h
  exact Bool.noConfusion h2

theorem freePres2_not_epi : ¬ Epi2 freePres2 := by
  intro h
  obtain ⟨x, hx⟩ := h ⟨2, by omega⟩
  cases x <;> exact absurd (congrArg Fin.val hx) (by decide)

theorem swap_maps_agree (u v : PHom2 swapPres2 idPres2) : u = v :=
  phom2_unique_of_epi _ swapPres2_epi u v
```

## Line-by-line Lean explanation

**Objects and morphisms (36-51).** `PtdRel` is Unit 51's `Setting`
without the stores and the operation family, plus the witness `w` as a
field: an object *is* a witnessed pair. `Hom` has one datum, the carrier
map `f`, and three proofs. `hom_ext` (54-63) says two morphisms with the
same `f` are equal: the proof fields are propositions and Lean treats
proofs of one proposition as the same. `idH`, `comp` and the three
category laws (65-85) are definitional.

**`d2_initial` (156-168).** Fix any target `T`. The map is `cond t T.b
T.a`: `false ↦ T.a`, `true ↦ T.b`; `ha`, `hb` are `rfl`. Edge
preservation: an edge of `D2` is `x = false ∧ y = true`, so after
`subst` the goal is `T.r T.a T.b`, which is `T.w`. Uniqueness: any `h'`
agrees with ours by `hom_ext` and `funext`, case `false` by `h'.ha`,
case `true` by `h'.hb`. Nothing about `T.r` beyond `T.w` was used; that
is the scope note.

**Injectivity (185-203).** Into an irreflexive target the two images are
`P.a` and `P.b`, apart by `irrefl_witness_ne`; the four cases on `Bool`
close. The countermodel is the one-point self-witness, the book's
`unitObj`, where `unit_collapses` is `rfl`: both images are `()`.

**`s2_initial_sym` (209-231) and `s2_no_hom_to_d2` (234-242).** The
same map; the reversed half of the edge is sent to `hsym _ _ T.w`, which
is where the hypothesis is spent. Into `d2Obj` the reversed edge `true →
false` would need `h.f true = false`, against `hb`. `s2_not_weakly_initial`
applies that at `d2Obj`; the book's `s2_not_initial_full` unfolds
`Initial` to show which quantifier fails.

**Two initials (256-294).** `d2Swap_initial` is `d2_initial` with the
roles exchanged (`cond t T.a T.b`). `two_initials_not_identical`: if the
structures were equal their `a` fields would be, and `false ≠ true`.
`initials_iso`: take the unique maps both ways; `comp v u` and `idH P`
are both endomorphisms of `P`, and `P` has only one, so they are equal.
The book's `swap_iso` writes the isomorphism out: it is the swap, both
ways, and the composite is the identity by `cases t <;> rfl`.

**Three points (320-359).** `bigObj n` has one edge and a free point of
index 2. `bigHomA` sends `x` to `x.val == 1`, so the free point goes to
`false`; `bigHomB` sends it to `!(x.val == 0)`, so to `true`; both
preserve the edge. `larger_not_initial` feeds both to uniqueness. The
book's `big0_free_point` reads the two values by `rfl`, and
`wideObj0_initial` is the audit's probe: `wideObj 0` is on `Fin 2` and
is initial, with the same proof as `d2_initial` written over `Fin 2`.

**Automorphisms (373-429).** `IsRelAuto` is bijective plus preserve and
reflect. The swap is one for `S2` and not for `D2` (`decide`). `pointed_rigid`
is two projections: `ha` and `hb` are exactly "fixes both points".

**Presentations (446-563).** `Pres` is a map out of `Fin 3` with `q 0 ≠
q 1`; `PHom` commutes at every occurrence. `pres_initial`: `R.q` itself
commutes, and any commuting map is determined on all of `Fin 3`. The two
cuts: `mergeA` is `decide (x = 1)`, values `false, true, false`; `mergeB`
is `decide (x = 0)`, values `true, false, false` (the book's
`cuts_values`). `no_phom_mergeA_mergeB`: a commuting `u` would give `u
(mergeA.q 0) = mergeB.q 0` and `u (mergeA.q 2) = mergeB.q 2`, but
`mergeA.q 0 = mergeA.q 2`, so `mergeB.q 0 = mergeB.q 2`, that is `true =
false`. `no_terminal_pres` runs the same two steps through a receiver
`T` of both cuts and lands on `T.q 0 = T.q 1`, against `faithful`.

**Two points (579-700).** `Epi2`: every carrier point is an occurrence.
`phom2_unique_of_epi`: at `z = P.q x` both maps give `idPres2.q x` by
`comm`, and every `z` is of that form. `freePres2` presents into `Fin 3`
with index 2 unused; `no_terminal_pres2` builds two commuting maps into
any `T` that differ at index 2 by `T.faithful`. The book's `free0`,
`free1` are those two maps into `idPres2`, differing by `rfl` at the free
point, and `freePres2_not_epi` shows no occurrence hits index 2.

## What has been proved

- `d2Obj` is initial among all witnessed pointed relations; the
  irreflexive restriction is a corollary (`d2_initial_irrefl` is
  `d2_initial P`, hypothesis unused).
- The unique map is injective into irreflexive targets and not in
  general.
- `s2Obj` is initial against symmetric targets and has no map into
  `d2Obj`, hence is not weakly initial.
- Any two initial objects are isomorphic; `d2Obj` and `d2SwapObj` are
  both initial and are not the same presentation.
- `bigObj n` admits two maps into `d2Obj` and is not initial, for every
  `n`.
- Pointed endomorphisms of both two-point objects fix both points; the
  swap is an unpointed automorphism of `S2` and not of `D2`.
- The identity presentation of three occurrences is initial; the two
  cuts are incomparable; no presentation is weakly terminal.
- No presentation of two occurrences is terminal; maps from a surjective
  presentation into the identity presentation are unique.
- Within carriers of at most three points, the bounded search finds
  exactly the two pointings of the single edge initial (book, bounded).

## What has not been proved

- "Every witnessed structure on a larger carrier admits two distinct
  morphisms out" (paper, item 4) is not what Lean proves:
  `ptd_on_every_larger_carrier n` produces `wideObj n` on `Fin (n+2)`,
  and `larger_not_initial n` refutes the different family `bigObj n` on
  `Fin (n+3)`. For `n = 0` the produced object is `d2Obj` and is initial
  (`wideObj0_initial`). The true general statement, that an initial
  object's carrier is in bijection with `Bool`, follows from
  `initials_iso` and is not formalised.
- Terminality of `idPres2` among surjective presentations: uniqueness is
  proved, existence of a map `P → idPres2` for an arbitrary surjective
  `P` is not (it needs a retraction of `P.q`). The module's own comment
  says so; neither proved nor refuted.
- "Initial in the symmetric subcategory" is a per-target conditional
  (`SymObj T → …`); no subcategory is formed.
- That initiality selects irreflexivity: it does not, and the module
  says the argument for A is Unit 51's, separately.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `PtdRel.X : Type`, `Pres.Q : Type` | objects, presentations | metatheoretic containers |
| `∀ T : PtdRel` in `Initial`; `∃ T : Pres` in `no_terminal_pres` | universal properties | quantification over all Lean types in universe 0 |
| `funext` (through `hom_ext`) | uniqueness of morphisms | `Quot.sound` |
| `Unit`, `Bool`, `Fin 2`, `Fin 3`, `Nat` | the named objects and families | library types |
| `decide` on `Bool` and `Fin` | model facts | metatheory |

**What the system holds.** Nothing new: the objects are Lean structures
and the maps Lean functions. "Among ALL pointed witnessed relations" in
the paper means over every `T : PtdRel` in Lean's universe 0, not over a
totality the system possesses.

**Phrases to read with care.**

- "Initial" is a statement about maps, proved up to isomorphism; the
  module itself keeps "same presentation" and "isomorphic" apart.
- "The free pointed object on one witnessed arrow" (docstring): a gloss
  on `d2_initial`; no free construction is formalised.
- "The observer cut" (docstrings on the cuts): `mergeA` and `mergeB` are
  two maps; "observer" is the reading the paper gives them.
- "Review-pass closure of the former OPEN cell" closes unrestricted
  terminality only; the surjective case stays open, as above.

## Student exercise

`s2Obj` and `d2Obj` have the same carrier and the same points. Explain,
using only the four fields of `Hom`, why there is exactly one map
`d2Obj → s2Obj` and no map `s2Obj → d2Obj`, and say which single field
makes the difference.

## Answer

A map either way is a function `Bool → Bool` with `f false = false` and
`f true = true` by `ha` and `hb`, so `f` is the identity in both
directions; only `hr` can fail. From `d2Obj` the only edge is `false →
true`, and `S2 false true` holds, so the identity is a morphism and, the
function being forced, it is the only one. From `s2Obj` the edge `true →
false` must be sent to `D2 (f true) (f false) = D2 true false`, which is
false. So `hr` is satisfiable one way and not the other. The field is
`hr`; `ha` and `hb` are identical on both sides.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/PrimitiveCats.lean` lines 36-85 (objects, morphisms, laws), 87-130 (`IrreflObj`, `SymObj`, the three two-point objects), 132-203 (initiality, `d2_initial`, injectivity), 209-249 (`s2_initial_sym`, `s2_no_hom_to_d2`), 256-294 (`d2Swap_initial`, `two_initials_not_identical`, `initials_iso`), 302-359 (`wideObj`, `bigObj`, `larger_not_initial`), 373-429 (automorphisms, `pointed_rigid`), 446-563 (`Pres`, cuts, `no_terminal_pres`), 579-700 (`Pres2`, `phom2_unique_of_epi`, `no_terminal_pres2`), 709-719 (`catsFindings`) |
| Axiom report | `artifacts/lean_axioms.txt` lines 330-376 and 723-724: 49 reports, all within `{propext, Quot.sound}` |
| Paper | `paper/primitive_difference_contact.md` "Categories and the true universal properties" and "The observer branching theorem"; `paper/paper_claim_ledger.md` `CL-PD2-INITIALITY`, `CL-PD2-BRANCHING` |
| Python | none in Genesis for this module; the check reuses `code/derivation/primdiff.py` (`enumerate_pointed`, `pointed_maps`, `preserves_rel`, `automorphisms`) |
| Audit probe | `textbook/audit/probes/D/cats_probe.lean` (`wideObj0_initial`), `textbook/audit/modules/PrimitiveCats.md` finding 1 |
| Check (Python (book)) | `python textbook/checks/u52_primitive_cats.py`: 2337 objects on 1-3 points, morphism counts for every claim above, 22 and 8 presentations, bounded searches labelled |
| Check (book Lean) | `python textbook/checks/u52_lean.py`: eighteen book declarations plus nineteen Genesis theorems kernel-checked, Lean 4.33.0 |
