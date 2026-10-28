# Unit 56. Sameness earned from difference, and what orientation adds

**Claim.** Under admitted irreflexivity, symmetry, and cotransitivity, the negation of apartness is an equivalence relation. Countermodels show why each law matters.

**Status:** FROZEN (every theorem);
ADMITTED (the three laws of `IsApart`, each a priced admission);
VERIFIED_FINITE (the equivalence on every relation of carriers 1-3, the
censuses to carrier 4). **Lean:** `lean4/Derivation/Apartness.lean`
lines 55-336, imports `PrimitiveCore`. **Axioms:** 28 exported reports;
`propext` for the three `Fin 3` facts, `Quot.sound` for the three
function-equality facts, none otherwise. **Depends on:** Unit 24
(`irrefl_witness_ne`), Unit 51 (`Cotrans`, `cotrans_auto_on_two`),
Unit 52 (`D2`, `S2`, the swap), Unit 37 (`Clos`).

## First pass

Read apartness as the relation the system positively records. Indistinguishability means that this apartness relation does not hold.

Irreflexivity makes each item indistinguishable from itself. Symmetry gives symmetry of indistinguishability. Cotransitivity supplies its transitivity. The lesson tests what fails when each assumption is removed.

## Detailed claim and formal anchors

`Apartness` takes a relation `r` read as "apart" and asks what
laws on `r` make its negation, *indistinguishable*, behave as sameness
should.

The answer is three admitted laws, bundled as `IsApart r`:
irreflexive, symmetric, cotransitive.

Under them `Indist r` is an
equivalence (`indist_equivalence`), and each law is spent at exactly
one clause: irreflexivity buys reflexivity, symmetry buys symmetry,
cotransitivity buys transitivity.

Each omission is refuted by a minimal
finite countermodel: bare assertion on one point breaks reflexivity
(`bare_breaks_refl`); the oriented two-point relation breaks symmetry
(`irrefl_alone_breaks_symm`), and no one-point relation can
(`subsingleton_indist_total`); one symmetrised edge on three points
breaks transitivity (`symm_without_cotrans_breaks_trans`), and no
two-point relation can (`two_point_indist_trans`).

The oriented relation
`D2` and its reverse generate the same apartness and so the same
sameness (`orientations_same_apartness`) while remaining different data
(`orientations_differ`); the swap fixes the apartness and moves the
retained witness (`retained_orientation_not_swap_invariant`).

On two
points, exactly the identity preserves the oriented witness
(`oriented_preserver_unique`), exactly the identity and the swap preserve
the apartness (`apart_preserver_pair`), the two constants preserve
neither (`collapse_preserves_neither`), and the closure of an admitted
family preserves the orientation exactly when every generator does
(`clos_oriented_iff`).

## Question

The derivation starts from asserted difference, never from asserted
sameness. If "the same" is to mean anything, it has to be "not
different". When does "not different" behave as sameness should, with
everything the same as itself, sameness running both ways, and sameness
passing through a middle term? And once the difference is made symmetric
to get there, what has been thrown away?

## What we already possess

- `Irrefl r`: `∀ x, ¬ r x x`; and from it, a related pair is a pair of
  different things, `irrefl_witness_ne` (Unit 24).
- `Cotrans r`: `∀ x y, r x y → ∀ z, r x z ∨ r z y`, and the fact that on
  two points irreflexivity alone gives it, `cotrans_auto_on_two`
  (Unit 51).
- `D2 x y := x = false ∧ y = true`, its reverse `D2rev`, the
  symmetrisation `Sym r x y := r x y ∨ r y x`, `S2 := Sym D2`, and the
  swap `Bool.not` as an automorphism of `S2` (Unit 52).
- `Clos F`, the closure of a family of operations under identity and
  composition (Unit 37).

## New concept: apartness, and sameness as its negation

An *apartness* is a relation with three laws: nothing is apart from
itself; if `x` is apart from `y` then `y` is apart from `x`; and if `x`
is apart from `y` then any third `z` is apart from `x` or from `y`. The
third law, *cotransitivity*, is the one with content: it says a
difference between two things cannot be hidden from a third, the third
must differ from at least one of them.

*Indistinguishability* is the negation: `Indist r x y := ¬ r x y`. It is
a negative notion by construction. Nothing about it is assumed; each of
its three laws has to be bought from one law of `r`.

A *countermodel* here is a small relation that has some of the three
laws and whose `Indist` fails one clause. *Minimal* means no smaller
carrier can do it, and that is proved, not asserted.

*Preserving* the oriented witness means `f` sends `(false, true)` to
`(false, true)`; preserving the apartness means `f` sends it to an apart
pair, either way round.

## Plain-language interpretation

Suppose the only thing you can ever say is "these two are different".
You would still like to say "these two are the same", and the only way
open is "I cannot say they are different". For that to be a decent
notion of sameness it needs three properties. Each costs one law on
"different".

Everything is the same as itself: that is exactly "nothing is different
from itself". If you drop it, the one-point world where the single
thing is different from itself refuses to be the same as itself.

Sameness runs both ways: that is exactly symmetry of difference. Drop
it and keep the oriented two-point relation, "0 differs from 1" but not
"1 differs from 0": then 1 is the same as 0 but 0 is not the same as 1.
And you cannot find this failure on one point, because with
irreflexivity a one-point relation is empty and everything is the same
as everything.

Sameness passes through a middle term: if `x` is the same as `y` and `y`
the same as `z`, then `x` is the same as `z`. Contrapose: if `x` differs
from `z`, then `x` differs from `y` or `y` differs from `z`. That is
cotransitivity, word for word. Drop it on three points, keeping one
symmetric edge between 0 and 1 and a third point 2 differing from
nothing: 0 is the same as 2 and 2 is the same as 1, yet 0 differs from
1. And you cannot find this on two points, because there cotransitivity
comes free from irreflexivity.

So far the module has made difference symmetric to get sameness. The
second half asks what that cost. The oriented relation "0 then 1" and
its reverse "1 then 0" give the same symmetric apartness, hence the
same sameness; but they are not the same relation. The swap of the two
points leaves the apartness alone and turns one orientation into the
other. So orientation is data that the sameness layer cannot see.

The last part counts. Of the four functions from two points to two
points, only the identity keeps the oriented witness where it is; the
identity and the swap keep the pair apart; the two constant functions,
which send both points to one, keep neither. And a family of admitted
operations keeps the orientation exactly when each of its generators
does, since the identity does and composition preserves it.

## Pseudocode

```
apart(r)        := irrefl(r) and symm(r) and cotrans(r)
indist(r, x, y) := not r(x, y)

claim: apart(r) implies
    indist(r, x, x)                                    -- from irrefl
    indist(r, x, y) implies indist(r, y, x)            -- from symm
    indist(r, x, y) and indist(r, y, z) implies indist(r, x, z)  -- from cotrans

countermodels:
    1 point,  r = {(0,0)}            : indist(0,0) fails
    2 points, r = {(0,1)}            : indist(1,0) holds, indist(0,1) fails
    3 points, r = {(0,1),(1,0)}      : indist(0,2), indist(2,1) hold, indist(0,1) fails

preservesOriented(f) := f(0) = 0 and f(1) = 1
preservesApart(f)    := (f(0), f(1)) in {(0,1), (1,0)}
```

## Python

Genesis's mirror, `code/derivation/apartness.py`: the laws, the
negation, and the exhaustive form of the theorem.

```python
def is_cotrans(n: int, r: Rel) -> bool:
    return all((x, z) in r or (z, y) in r
               for (x, y) in r for z in range(n))


def is_apart(n: int, r: Rel) -> bool:
    return is_irrefl(n, r) and is_symm(n, r) and is_cotrans(n, r)


def indist(r: Rel, x: int, y: int) -> bool:
    return (x, y) not in r


def equivalence_theorem_exhaustive(max_n: int) -> bool:
    """Mirror of ``indist_equivalence``: on every relation of every
    carrier up to the bound, positive apartness makes
    indistinguishability an equivalence."""
    return all(indist_is_equivalence(n, r)
               for n in range(1, max_n + 1)
               for r in all_relations(n) if is_apart(n, r))
```

The book's check, `textbook/checks/u56_apartness.py`, adds a clause
census, Python (book):

```python
    for n in (1, 2, 3):
        for r in all_relations(n):
            refl, symm, trans = clauses(n, r)
            law_buys["irrefl<->refl"] &= (is_irrefl(n, r) == refl)
            if is_irrefl(n, r):
                law_buys["symm->symm"] &= (not is_symm(n, r)) or symm
                if is_symm(n, r):
                    law_buys["cotrans->trans"] &= (not is_cotrans(n, r)) or trans
```

## Line-by-line Python explanation

- `is_cotrans`: for every related pair `(x, y)` and every point `z`,
  `(x, z)` or `(z, y)` is related. The quantifier over `z` runs over
  the whole carrier, including `x` and `y` themselves, where
  irreflexivity makes one disjunct false and the other is the original
  pair.
- `indist`: membership negated. There is no separate data for
  sameness; it is read off the difference relation.
- `equivalence_theorem_exhaustive(3)`: every relation on 1, 2 and 3
  points is listed, `2^1 + 2^4 + 2^9` of them; the apart ones number
  `1, 2, 5`, and for each the three clauses are evaluated. This is a
  finite check of the theorem's instances up to carrier 3, not the
  theorem; the Lean proof is for every carrier.
- The clause census: `irrefl<->refl` records that the reflexive clause
  holds exactly when `r` is irreflexive, on every relation; the two
  other lines record that, given irreflexivity, symmetry of `r` gives
  the symmetric clause, and given both, cotransitivity gives the
  transitive clause. This is the "spent at exactly one clause" reading
  checked as a census of implications. It does not show the converse
  for symmetry and cotransitivity, and the module does not claim it:
  the countermodels show that dropping the law *can* break the clause,
  not that it always does.

## Lean 4

The structure, the negation and the bundled theorem
(`lean4/Derivation/Apartness.lean` lines 55-95, abridged):

```lean
structure IsApart {X : Type} (r : X → X → Prop) : Prop where
  irrefl : ∀ x, ¬ r x x
  symm : ∀ x y, r x y → r y x
  cotrans : ∀ x y, r x y → ∀ z, r x z ∨ r z y

def Indist {X : Type} (r : X → X → Prop) (x y : X) : Prop := ¬ r x y

theorem indist_equivalence {X : Type} {r : X → X → Prop}
    (h : IsApart r) :
    (∀ x, Indist r x x) ∧
    (∀ x y, Indist r x y → Indist r y x) ∧
    (∀ x y z, Indist r x y → Indist r y z → Indist r x z) :=
  ⟨indist_refl h,
   fun _ _ => indist_symm h,
   fun _ _ _ => indist_trans h⟩
```

Two of the countermodels (lines 107-124, 143-164):

```lean
theorem irrefl_alone_breaks_symm :
    Indist D2 true false ∧ ¬ Indist D2 false true := by
  constructor
  · intro h
    exact absurd h.1 (by decide)
  · intro h
    exact h (by decide)

theorem subsingleton_indist_total {X : Type} [Subsingleton X]
    {r : X → X → Prop} (hi : PrimDiff.Irrefl r) (x y : X) :
    Indist r x y := by
  intro hxy
  exact PrimDiff.irrefl_witness_ne hi hxy (Subsingleton.elim x y)

theorem two_point_indist_trans (r : Bool → Bool → Prop)
    (hi : PrimDiff.Irrefl r) {x y z : Bool}
    (hxy : Indist r x y) (hyz : Indist r y z) : Indist r x z :=
  fun hxz =>
    match cotrans_auto_on_two r hi x z hxz y with
    | Or.inl hxy' => hxy hxy'
    | Or.inr hyz' => hyz hyz'
```

The two characterisations (lines 242-249, 255-260, abridged):

```lean
theorem oriented_preserver_unique (f : Bool → Bool)
    (h : PreservesOriented f) : f = id := by
  funext x
  cases x with
  | false => exact h.1
  | true => exact h.2

theorem apart_preserver_pair (f : Bool → Bool)
    (h : PreservesApart f) : f = id ∨ f = Bool.not := by
  have hne : f false ≠ f true := by
    intro heq
    have h2 : S2 (f false) (f true) := h
    exact S2_irrefl (f true) (heq ▸ h2)
  ...
```

Lean (book), from `textbook/checks/u56_lean.py`: the three-point
countermodel fails exactly cotransitivity; a three-point apartness whose
sameness is equality; and the swap composed with itself through both
characterisations.

```lean
theorem tri_not_cotrans : ¬ Cotrans triSymRel := by
  intro h
  have := h 0 1 (Or.inl ⟨rfl, rfl⟩) 2
  rcases this with h | h <;> simp [triSymRel] at h

def ne3 : Fin 3 → Fin 3 → Prop := fun x y => x ≠ y

theorem ne3_isApart : IsApart ne3 :=
  { irrefl := fun x h => h rfl,
    symm := fun _ _ h => fun e => h e.symm,
    cotrans := by
      intro x y hxy z
      by_cases hxz : x = z
      · exact Or.inr (fun e => hxy (hxz.trans e))
      · exact Or.inl hxz }

theorem ne3_indist_iff (x y : Fin 3) : Indist ne3 x y ↔ x = y := by
  unfold Indist ne3
  constructor
  · intro h; exact Decidable.of_not_not h
  · intro h hne; exact hne h

theorem swap_twice_is_id_or_swap :
    (Bool.not ∘ Bool.not) = id ∨ (Bool.not ∘ Bool.not) = Bool.not :=
  apart_preserver_pair _ swap_twice_apart

theorem swap_twice_is_id : (Bool.not ∘ Bool.not) = id :=
  oriented_preserver_unique _ ⟨rfl, rfl⟩
```

## Line-by-line Lean explanation

- `structure IsApart … : Prop where irrefl … symm … cotrans …`: a
  structure in `Prop` is a bundle of three proofs. Writing it as a
  structure rather than a conjunction gives the three laws names, so a
  proof can say which one it spends: `h.irrefl`, `h.symm`, `h.cotrans`.
- `def Indist … := ¬ r x y`: one negation. Every property of `Indist`
  below is a property of `r` read through this negation.
- `theorem indist_equivalence … := ⟨indist_refl h, fun _ _ =>
  indist_symm h, fun _ _ _ => indist_trans h⟩`: the three clauses come
  from three separate theorems (lines 67-86), each using one field.
  `indist_refl` is `h.irrefl x` restated; `indist_symm` is
  contraposition of `h.symm`; `indist_trans` contraposes `h.cotrans`:
  given `¬ r x y`, `¬ r y z` and supposing `r x z`, cotransitivity gives
  `r x y ∨ r y z`, and both are refuted.
- `irrefl_alone_breaks_symm`: `Indist D2 true false` is `¬ (true = false
  ∧ false = true)`; the proof takes such an `h` and refutes its first
  component by `decide`. `¬ Indist D2 false true` is `¬ ¬ D2 false
  true`; the proof applies the double negation to the witness `D2 false
  true`, which `decide` supplies.
- `subsingleton_indist_total … [Subsingleton X]`: the hypothesis in
  square brackets says any two elements of `X` are equal. Given a
  supposed `r x y`, `irrefl_witness_ne` yields `x ≠ y`, contradicting
  `Subsingleton.elim x y`. This is the minimality of the two-point
  countermodel: on one point, irreflexive relations are empty.
- `two_point_indist_trans … match cotrans_auto_on_two r hi x z hxz y
  with …`: Unit 51's theorem gives cotransitivity on `Bool` from
  irreflexivity alone, so transitivity of `Indist` follows there
  without assuming it. This is the minimality of the three-point
  countermodel.
- `oriented_preserver_unique … funext x; cases x`: two functions on
  `Bool` are equal when they agree at `false` and at `true`; `h.1` and
  `h.2` are exactly those two equations. `funext` is where `Quot.sound`
  enters the axiom report.
- `apart_preserver_pair … have hne : f false ≠ f true`: if the images
  were equal, `S2 (f false) (f true)` would be a self-relation, refuted
  by `S2_irrefl`. The rest of the proof (lines 261-285) cases on the
  two image values and lands on `id` or `Bool.not`.
- Book `tri_not_cotrans`: apply the supposed cotransitivity to the edge
  `(0, 1)` and the third point `2`; both disjuncts, `triSymRel 0 2` and
  `triSymRel 2 1`, unfold to false equations on `Fin 3`, which `simp`
  closes. So the three-point countermodel fails cotransitivity and
  only that; `triSymRel_irrefl` and `triSymRel_symm` are Genesis's.
- Book `ne3_isApart`: the relation "different points" on three points
  is an apartness, and the cotransitivity case is a `by_cases` on
  whether `x = z`. Its `Indist` is equality (`ne3_indist_iff`), which
  needs `Decidable.of_not_not` to pass from `¬ (x ≠ y)` to `x = y`;
  equality on `Fin 3` is decidable, so no classical axiom is used.
- Book `swap_twice_is_id_or_swap` and `swap_twice_is_id`: the same
  operation through the two characterisations. The apartness one says
  "identity or swap"; the orientation one decides "identity". That is
  what strictly finer means in practice.

## What has been proved

- `indist_refl` (67), `indist_symm` (71), `indist_trans` (78),
  `indist_equivalence` (88): under `IsApart r`, `Indist r` is reflexive,
  symmetric and transitive, each from one field.
- `bare_breaks_refl` (101), `irrefl_alone_breaks_symm` (107),
  `symm_without_cotrans_breaks_trans` (143): the three countermodels, on
  `Unit`, `Bool` and `Fin 3`.
- `subsingleton_indist_total` (118), `two_point_indist_trans` (158): the
  two- and three-point countermodels are minimal; `triSymRel_irrefl`
  (132), `triSymRel_symm` (136): the three-point relation has the two
  laws it is supposed to have.
- `s2_isApart` (170): `S2` is an apartness, cotransitivity from
  `cotrans_auto_on_two`; `s2_indist_equivalence` (179).
- `orientations_same_apartness` (188), `orientations_same_indist`
  (194), `orientations_differ` (207),
  `retained_orientation_not_swap_invariant` (215).
- `oriented_pres_iff` (236), `oriented_preserver_unique` (242),
  `id_preserves_oriented` (251), `apart_preserver_pair` (255),
  `id_preserves_apart` (287), `swap_preserves_apart` (289),
  `swap_breaks_oriented` (294), `collapse_preserves_neither` (299),
  `oriented_comp` (305), `clos_oriented_iff` (316),
  `oriented_family_trivial` (332).

## What has not been proved

- That the three laws are the *only* way to earn an equivalence. The
  module shows they suffice and that each is used; the countermodels
  show each omission *can* fail. Whether some weaker or different set of
  laws would also do is not asked here. The header's claim that none of
  the three follows from the others cites Unit 51's implication matrix,
  not anything in this module (audit finding 2: consistent, and the
  module proves the more specific fact).
- Audit finding 1. `oriented_family_trivial` says that on `Bool` any
  family whose members fix both points is a family of identities; the
  docstring's "the retained orientation is rigid" is this two-point
  fact, a one-line corollary of `oriented_preserver_unique`. On a larger
  carrier the oriented preservers number `n^(n-2)` (the artifact and the
  book's check): fixing two points leaves the others free. "Rigid" is a
  statement about two points.
- Minimality of the one-point countermodel is not stated because there
  is nothing smaller; the module says so in prose only.
- The censuses to carrier 4 and the formula `n^(n-2)` are finite
  computations and a book observation; no Lean theorem states the count
  for any carrier but two.

## Outside the system

- `Fin 3`, `Unit`, `Subsingleton` and `funext` are the metatheory's.
  Each countermodel is a finite relation written out; the quantifier
  over all relations in the Python check is the reader's enumeration.
- The reading of `Indist` as "sameness" is a reading. The module names
  it indistinguishability and proves what the negation satisfies; that
  one would *call* an equivalence "sameness" is outside.
- Cotransitivity is admitted, not derived. On two points it comes free
  (`cotrans_auto_on_two`); on three it does not (`tri_not_cotrans`), so
  from the third point on it is a priced law like the other two.

## Student exercise

Take the three-point relation `r = {(0, 1), (1, 0), (1, 2), (2, 1)}`:
two symmetric edges sharing the point 1. Decide whether it is
irreflexive, symmetric, cotransitive; then compute `Indist r` on the
pairs `(0, 2)`, `(2, 0)`, `(0, 1)` and say which clause of the
equivalence, if any, fails and at which triple.

## Answer

Irreflexive: yes, no pair `(x, x)` is in `r`. Symmetric: yes, both
edges appear both ways. Cotransitive: check every related pair against
every third point. For `(0, 1)`: `z = 0` needs `(0, 0)` or `(0, 1)`,
the second holds; `z = 1` needs `(0, 1)` or `(1, 1)`, the first holds;
`z = 2` needs `(0, 2)` or `(2, 1)`, the second holds. For `(1, 0)`:
`z = 2` needs `(1, 2)` or `(2, 0)`, the first holds; `z = 0, 1` are the
pair itself. For `(1, 2)`: `z = 0` needs `(1, 0)` or `(0, 2)`, the first
holds. For `(2, 1)`: `z = 0` needs `(2, 0)` or `(0, 1)`, the second
holds. Every instance passes, so `r` is cotransitive, hence an
apartness, and `Indist r` is an equivalence.

`Indist r 0 2` holds (no edge), `Indist r 2 0` holds, `Indist r 0 1`
fails. No clause fails. Transitivity would need some `y` with
`Indist r 0 y` and `Indist r y 1`: the first forces `y ∈ {0, 2}`, the
second forces `y ∉ {0, 2}`, so there is none. The lesson of the
exercise is the shape of cotransitivity: the countermodel
`{(0, 1), (1, 0)}` failed because the third point differed from nothing;
adding the edge to 2 repaired it, because 2 now differs from the middle
point 1. (The book's Python check confirms `is_apart(3, r)` and
`indist_is_equivalence(3, r)` on this relation.)

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Apartness.lean` lines 55-63 (`IsApart`, `Indist`), 67-95 (the equivalence), 101-124 (one- and two-point countermodels, minimality), 126-164 (three-point countermodel, minimality), 170-219 (the orientation separation), 226-336 (preservers, closure) |
| Axiom report | `artifacts/lean_axioms.txt` lines 552-579 |
| Paper | `paper/primitive_difference_map.md` section 1; `paper/primitive_difference_passage.md` P4 and the "three ADMITTED `Apartness.IsApart` fields" note; `paper/paper_claim_ledger.md` `CL-PD2-APARTNESS` |
| Python | `code/derivation/apartness.py`, `code/run_apartness.py`, `tests/test_apartness.py`, `artifacts/apartness.json` |
| Audit | `textbook/audit/modules/Apartness.md` findings 1-4 |
| Check (Python) | `python textbook/checks/u56_apartness.py`: the exhaustive equivalence on carriers 1-3, the clause census (Python (book)), the countermodels and minimality, the orientation separation, the censuses to carrier 4 with the `n^(n-2)` formula, against the artifact |
| Check (book Lean) | `python textbook/checks/u56_lean.py`: seventeen book declarations plus sixteen Genesis theorems kernel-checked, Lean 4.33.0 |
