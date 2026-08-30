import Derivation.PrimDiff

/-!
# P1 -- S9.1, the axiom lattice: the carrier-general half (PROMPT.md step 13)

The finite sweep of `research/s9_obligations/axiom_lattice.py` is a table
over carriers 1..4.  This module formalizes the clause syntax and the two
transfer definitions exactly as that module declares them, then proves the
carrier-general statements P1 proposed as Lean targets T1-T4, T6, T7
(`P1_FINDINGS.md`, section 8).  Each theorem below names in its doc string
which sweep cell it carries.

Encoding (P1's, section 8): five atoms `r x x`, `r x y`, `r y x`, `r y y`
and the identity atom `x = y`; a head is one atom or falsum; a body is a
list of atoms (a subset; repetition is harmless because the body is read
as a conjunction); a clause set is a list of clauses whose truth is the
conjunction of its members'.  A clause is PURE when it mentions no
identity atom, in body or head; the EQ_BEARING fragment is the clauses
that do.  A theorem stated over the whole syntax therefore covers the
object P1 labels `MERGED_PURE_AND_EQ_BEARING` and restricts to each
fragment; the pure-only theorems take an explicit `Pure` hypothesis.  The
type of clause sets is named `ClauseSet` here, not the name P1 suggested,
so that no line of this file begins with the token the plain-text scan of
`verify_lean.py` forbids.

Transfer (P1 step 7, both definitions), with the finite range "carriers
1..N" replaced by every type, and "carriers 2..N" by every type with two
distinct points:

* `Transfers phi`: for every type, relation `r`, and points `a`, `b`,
  if `phi` holds on `r` and `r a b` then `a` is not `b`
  (P1's `TRANSFER_ALL_CARRIERS`).
* `TransfersAbovePoint phi`: the same, restricted to types with two
  distinct points (P1's `TRANSFER_ABOVE_POINT`).
* `EntailsIrrefl phi`: every relation on which `phi` holds is irreflexive
  in the sealed sense `PrimDiff.Irrefl`.

Sealed names are reused, never restated: `Irrefl`, `irrefl_witness_ne`.
The one-point full relation of `selfdiff_consistent` reappears as
`full Unit`, and the two-point full relation as `full Bool`.

AuthorityEffect: None.  Nothing under `lean4/Derivation/` is touched; this
module proposes, and a theorem here carries one cell of P1's table beyond
its carrier bound only within the scope its statement names.
-/

namespace S9Obligations.AxiomLattice

open PrimDiff

/-! ## Syntax -/

/-- The atoms of P1's clause space: the four `r`-atoms and the identity
atom `x = y` (index 4 in `axiom_lattice.py`, the EQ_BEARING marker). -/
inductive Atom where
  | xx
  | xy
  | yx
  | yy
  | eq
  deriving DecidableEq

/-- A clause head: one atom, or falsum. -/
inductive Head where
  | atom (a : Atom)
  | falsum
  deriving DecidableEq

/-- A universally quantified Horn clause `body -> head`. -/
structure Clause where
  body : List Atom
  head : Head
  deriving DecidableEq

/-- A finite clause set; P1's "axiom is a finite set of clauses". -/
abbrev ClauseSet := List Clause

/-! ## Semantics -/

/-- Reading an atom at the pair `(x, y)`. -/
def Atom.eval {α : Type} (r : α → α → Prop) (x y : α) : Atom → Prop
  | .xx => r x x
  | .xy => r x y
  | .yx => r y x
  | .yy => r y y
  | .eq => x = y

/-- Reading a head at the pair `(x, y)`; falsum reads as `False`. -/
def Head.eval {α : Type} (r : α → α → Prop) (x y : α) : Head → Prop
  | .atom a => a.eval r x y
  | .falsum => False

/-- The body holds at `(x, y)` when every listed atom does. -/
def Clause.BodyHolds {α : Type} (r : α → α → Prop) (x y : α) (c : Clause) : Prop :=
  ∀ a, a ∈ c.body → a.eval r x y

/-- The universally quantified clause holds on `r`. -/
def Clause.Holds {α : Type} (r : α → α → Prop) (c : Clause) : Prop :=
  ∀ x y, c.BodyHolds r x y → c.head.eval r x y

/-- A clause set holds on `r` when each of its clauses does. -/
def ClauseSet.Holds {α : Type} (r : α → α → Prop) (phi : ClauseSet) : Prop :=
  ∀ c, c ∈ phi → c.Holds r

/-- The clause mentions the identity atom, in head or body (P1's
`mentions_eq`; membership in the EQ_BEARING fragment). -/
def Clause.MentionsEq (c : Clause) : Prop :=
  c.head = .atom .eq ∨ Atom.eq ∈ c.body

/-- A pure clause: one of the PURE fragment. -/
def Clause.Pure (c : Clause) : Prop := ¬ c.MentionsEq

/-- A pure clause set: every member is pure. -/
def ClauseSet.Pure (phi : ClauseSet) : Prop := ∀ c, c ∈ phi → c.Pure

/-- Some member has head falsum (P1's `falsum_headed`, lifted to sets). -/
def ClauseSet.HasFalsumClause (phi : ClauseSet) : Prop :=
  ∃ c, c ∈ phi ∧ c.head = .falsum

instance (phi : ClauseSet) : Decidable phi.HasFalsumClause := by
  unfold ClauseSet.HasFalsumClause
  infer_instance

/-- The full relation on a carrier.  On `Unit` it is the structure of the
sealed `selfdiff_consistent`; on `Bool` it is the two-point full relation
P1's pure-fragment lemma turns on. -/
def full (α : Type) : α → α → Prop := fun _ _ => True

/-! ## The two transfer definitions and entailment of irreflexivity -/

/-- P1's `TRANSFER_ALL_CARRIERS`, over every type. -/
def Transfers (phi : ClauseSet) : Prop :=
  ∀ (α : Type) (r : α → α → Prop) (a b : α), phi.Holds r → r a b → a ≠ b

/-- P1's `TRANSFER_ABOVE_POINT`, over every type with two distinct points. -/
def TransfersAbovePoint (phi : ClauseSet) : Prop :=
  ∀ (α : Type) (r : α → α → Prop) (a b : α),
    (∃ u v : α, u ≠ v) → phi.Holds r → r a b → a ≠ b

/-- P1's "phi entails irreflexivity", over every type, in the sealed sense. -/
def EntailsIrrefl (phi : ClauseSet) : Prop :=
  ∀ (α : Type) (r : α → α → Prop), phi.Holds r → Irrefl r

/-- The clause `r x x -> falsum`. -/
def irreflClause : Clause := ⟨[.xx], .falsum⟩

/-- The clause `r x x -> x = y` (P1's `REFLEXIVE_POINT_FORCES_SINGLETON`,
the generator realizing W under `TRANSFER_ABOVE_POINT` in the EQ_BEARING
and merged lattices). -/
def reflexivePointForcesSingleton : Clause := ⟨[.xx], .atom .eq⟩

/-- The syntactic clause `r x x -> falsum` holds exactly on the irreflexive
relations, in the sealed sense.  Ties P1's "irreflexivity's extent" to
`PrimDiff.Irrefl` on every carrier. -/
theorem irreflClause_holds_iff {α : Type} (r : α → α → Prop) :
    irreflClause.Holds r ↔ Irrefl r := by
  constructor
  · intro h x hxx
    exact h x x (fun a ha => by
      have ha' : a = Atom.xx := List.mem_singleton.mp ha
      subst ha'
      exact hxx)
  · intro hi x y hb
    exact hi x (hb .xx (List.Mem.head _))

/-! ## T1, T2, T3: what atom heads and falsum heads do on every carrier -/

/-- T1 (`atom_head_clause_holds_on_full`): a clause whose head is an
`r`-atom is satisfied by the full relation on every carrier, whatever its
body.  Carries P1's key
`T1_atom_headed_generators_admit_full_relation_on_carriers_1_to_N` in all
three fragments beyond the bound. -/
theorem atom_head_clause_holds_on_full (α : Type) (c : Clause) (a : Atom)
    (hh : c.head = .atom a) (ha : a ≠ .eq) : c.Holds (full α) := by
  intro x y _
  rw [hh]
  cases a with
  | xx => exact trivial
  | xy => exact trivial
  | yx => exact trivial
  | yy => exact trivial
  | eq => exact absurd rfl ha

/-- T2 (`non_falsum_clause_set_admits_selfdiff`; P1 proposed it under a
name that embedded the type name this module renamed, see the module
docstring): a clause set with no falsum-headed clause -- heads may be
`r`-atoms or the identity atom -- is satisfied by the full relation on the
one-point carrier, which asserts a self-difference.  Generalizes the
sealed `selfdiff_consistent` (its
statement is the case of the empty clause set) to every such clause set,
and carries P1's key `T2_non_falsum_generators_admit_one_point_full` in
all three fragments beyond the bound. -/
theorem non_falsum_clause_set_admits_selfdiff (phi : ClauseSet)
    (h : ∀ c, c ∈ phi → c.head ≠ .falsum) :
    ∃ r : Unit → Unit → Prop, ClauseSet.Holds r phi ∧ r () () := by
  refine ⟨full Unit, ?_, trivial⟩
  intro c hc x y _
  cases hhead : c.head with
  | falsum => exact absurd hhead (h c hc)
  | atom a =>
    cases a with
    | xx => exact trivial
    | xy => exact trivial
    | yx => exact trivial
    | yy => exact trivial
    | eq =>
      cases x
      cases y
      exact rfl

/-- T3 (`falsum_clause_entails_irrefl`): a falsum-headed clause, whatever
its body (identity atom included), entails irreflexivity on every carrier:
at a reflexive point every atom of the body is true, so the clause
refutes the point.  Carries P1's key
`T3_falsum_headed_generators_entail_irreflexivity` in all three fragments
beyond the bound. -/
theorem falsum_clause_entails_irrefl {α : Type} (c : Clause)
    (hhead : c.head = .falsum) (r : α → α → Prop) (h : c.Holds r) : Irrefl r := by
  intro x hxx
  have hb : c.BodyHolds r x x := fun a _ => by
    cases a with
    | xx => exact hxx
    | xy => exact hxx
    | yx => exact hxx
    | yy => exact hxx
    | eq => exact rfl
  have hfalse := h x x hb
  rw [hhead] at hfalse
  exact hfalse

/-- A clause set with a falsum-headed member entails irreflexivity. -/
theorem has_falsum_clause_entails_irrefl (phi : ClauseSet)
    (h : phi.HasFalsumClause) : EntailsIrrefl phi := by
  intro α r hphi
  obtain ⟨c, hc, hhead⟩ := h
  exact falsum_clause_entails_irrefl c hhead r (hphi c hc)

/-! ## The default definition: transfer is entailing irreflexivity -/

/-- Under `TRANSFER_ALL_CARRIERS`, transferring and entailing
irreflexivity are the same property, on every carrier.  This is the
carrier-general form of P1's "empty by definitional identity" (the
step-11 set under the default is empty because the two tests coincide),
which the sweep recorded only at N = 4; it carries the `F3_UNTESTED`
cells of all three fragments beyond the bound.  The converse direction is
the sealed `irrefl_witness_ne`. -/
theorem transfers_iff_entails_irrefl (phi : ClauseSet) :
    Transfers phi ↔ EntailsIrrefl phi := by
  constructor
  · intro h α r hphi x hxx
    exact h α r x x hphi hxx rfl
  · intro h α r a b hphi hab
    exact irrefl_witness_ne (h α r hphi) hab

/-- T4 (`transfers_iff_has_falsum_clause`): under `TRANSFER_ALL_CARRIERS`
a clause set transfers exactly when some member has head falsum -- on
every carrier, in every fragment.  Left to right: with no falsum head, T2
gives the one-point self-difference, which transfer forbids.  Right to
left: T3 with the sealed `irrefl_witness_ne`.  The case split is on the
decidable membership question, not on an undecidable proposition.
Carries P1's key `T4_lattice_transfers_iff_representative_has_falsum_head`
in all three fragments beyond the bound, and carries the
`S9_1_TRANSFER_CHARACTERIZED` cells under the default definition. -/
theorem transfers_iff_has_falsum_clause (phi : ClauseSet) :
    Transfers phi ↔ phi.HasFalsumClause := by
  constructor
  · intro h
    by_cases hf : phi.HasFalsumClause
    · exact hf
    · exfalso
      have hnf : ∀ c, c ∈ phi → c.head ≠ .falsum := fun c hc hh => hf ⟨c, hc, hh⟩
      obtain ⟨r, hholds, hsd⟩ := non_falsum_clause_set_admits_selfdiff phi hnf
      exact h Unit r () () hholds hsd rfl
  · intro hf
    exact (transfers_iff_entails_irrefl phi).mpr (has_falsum_clause_entails_irrefl phi hf)

/-- The prompt's step-13 question, answered on every carrier: a clause
whose head is an atom -- any atom, the identity atom included -- does not
transfer, because the one-point full relation satisfies it and already
hosts a self-difference. -/
theorem atom_head_clause_does_not_transfer (c : Clause) (a : Atom)
    (hh : c.head = .atom a) : ¬ Transfers [c] := by
  intro ht
  obtain ⟨c', hc', hhead⟩ := (transfers_iff_has_falsum_clause [c]).mp ht
  have hc'' : c' = c := List.mem_singleton.mp hc'
  subst hc''
  rw [hh] at hhead
  cases hhead

/-- Entailing irreflexivity is also exactly having a falsum-headed member;
with T4 this makes the three properties -- transferring under the default,
entailing irreflexivity, containing a falsum head -- one property on every
carrier. -/
theorem entails_irrefl_iff_has_falsum_clause (phi : ClauseSet) :
    EntailsIrrefl phi ↔ phi.HasFalsumClause :=
  (transfers_iff_entails_irrefl phi).symm.trans (transfers_iff_has_falsum_clause phi)

/-! ## Transfer above the point -/

/-- Under `TRANSFER_ABOVE_POINT`, transferring is entailing irreflexivity
on every carrier with two distinct points.  This is the carrier-general
form of P1's "transfer is containment in a fixed extent W", with W read
as "irreflexive wherever two points differ"; the converse direction is
again the sealed `irrefl_witness_ne`. -/
theorem transfers_above_point_iff (phi : ClauseSet) :
    TransfersAbovePoint phi ↔
      ∀ (α : Type) (r : α → α → Prop), phi.Holds r → (∃ u v : α, u ≠ v) → Irrefl r := by
  constructor
  · intro h α r hphi huv x hxx
    exact h α r x x huv hphi hxx rfl
  · intro h α r a b huv hphi hab
    exact irrefl_witness_ne (h α r hphi huv) hab

/-- The syntactic clause `r x x -> x = y` holds on `r` exactly when every
reflexive point of `r` equals every point. -/
theorem reflexivePointForcesSingleton_holds_iff {α : Type} (r : α → α → Prop) :
    reflexivePointForcesSingleton.Holds r ↔ ∀ x y, r x x → x = y := by
  constructor
  · intro h x y hxx
    exact h x y (fun a ha => by
      have ha' : a = Atom.xx := List.mem_singleton.mp ha
      subst ha'
      exact hxx)
  · intro h x y hb
    exact h x y (hb .xx (List.Mem.head _))

/-- If every reflexive point equals every point, then on a carrier with
two distinct points there is no reflexive point at all. -/
theorem reflexive_point_forces_singleton_irrefl_of_two_points {α : Type}
    (r : α → α → Prop) (h : ∀ x y, r x x → x = y) (huv : ∃ u v : α, u ≠ v) :
    Irrefl r := by
  intro x hxx
  obtain ⟨u, v, huv⟩ := huv
  exact huv ((h x u hxx).symm.trans (h x v hxx))

/-- T6, transfer half
(`reflexive_point_forces_singleton_transfers_above_point`): the clause
`r x x -> x = y` transfers above the point on every carrier.  The sweep
checked this on carriers 2..4 only (P1 key
`T6_reflexive_point_forces_singleton.transfers_above_point`); the
statement below removes that bound for the EQ_BEARING and merged cells. -/
theorem reflexive_point_forces_singleton_transfers_above_point :
    TransfersAbovePoint [reflexivePointForcesSingleton] := by
  intro α r a b huv hphi hab
  have hc := hphi reflexivePointForcesSingleton (List.Mem.head _)
  exact irrefl_witness_ne
    (reflexive_point_forces_singleton_irrefl_of_two_points r
      ((reflexivePointForcesSingleton_holds_iff r).mp hc) huv) hab

/-- T6, non-entailment half
(`reflexive_point_forces_singleton_admits_selfdiff`): the one-point full
relation satisfies `r x x -> x = y` and asserts a self-difference, because
its head is the identity atom and the carrier is a point. -/
theorem reflexive_point_forces_singleton_admits_selfdiff :
    ∃ r : Unit → Unit → Prop,
      ClauseSet.Holds r [reflexivePointForcesSingleton] ∧ r () () := by
  refine ⟨full Unit, ?_, trivial⟩
  intro c hc
  have hc' : c = reflexivePointForcesSingleton := List.mem_singleton.mp hc
  subst hc'
  intro x y _
  cases x
  cases y
  exact rfl

/-- The clause `r x x -> x = y` does not entail irreflexivity: its
one-point model is reflexive. -/
theorem reflexive_point_forces_singleton_not_entails_irrefl :
    ¬ EntailsIrrefl [reflexivePointForcesSingleton] := by
  intro h
  obtain ⟨r, hholds, hr⟩ := reflexive_point_forces_singleton_admits_selfdiff
  exact h Unit r hholds () hr

/-- The F3_REFUTED cells, carrier-general: one clause set of the
EQ_BEARING fragment transfers above the point on every carrier, entails
irreflexivity on no reading, and does not transfer under the default
definition.  Its head is the identity atom, so this is a countermodel to
F3 extended to A3's bill under the weaker soundness that discounts the
one-point carrier, and says nothing about F3 as written, whose one-point
countermodel the default definition keeps (`selfdiff_consistent`). -/
theorem reflexive_point_forces_singleton_f3_countermodel_above_point :
    reflexivePointForcesSingleton.MentionsEq ∧
    TransfersAbovePoint [reflexivePointForcesSingleton] ∧
    ¬ EntailsIrrefl [reflexivePointForcesSingleton] ∧
    ¬ Transfers [reflexivePointForcesSingleton] :=
  ⟨Or.inl rfl,
   reflexive_point_forces_singleton_transfers_above_point,
   reflexive_point_forces_singleton_not_entails_irrefl,
   fun h => reflexive_point_forces_singleton_not_entails_irrefl
     ((transfers_iff_entails_irrefl _).mp h)⟩

/-! ## The pure fragment above the point -/

/-- A pure clause set with no falsum head is satisfied by the full
relation on every carrier: each head is an `r`-atom, and T1 applies. -/
theorem pure_non_falsum_clause_set_holds_on_full (phi : ClauseSet) (hp : phi.Pure)
    (hnf : ∀ c, c ∈ phi → c.head ≠ .falsum) (α : Type) : phi.Holds (full α) := by
  intro c hc
  cases hhead : c.head with
  | falsum => exact absurd hhead (hnf c hc)
  | atom a =>
    exact atom_head_clause_holds_on_full α c a hhead
      (fun hae => hp c hc (Or.inl (by rw [hhead, hae])))

/-- The general form of the lemma P1 checked at N = 4 as
`one_point_full_implies_two_point_full_on_lattice`: a pure clause set that
holds on the one-point full relation holds on the two-point full relation
(indeed on the full relation of every carrier), because the one-point
model already rules out every falsum head. -/
theorem pure_one_point_full_implies_two_point_full (phi : ClauseSet) (hp : phi.Pure)
    (h1 : phi.Holds (full Unit)) : phi.Holds (full Bool) := by
  apply pure_non_falsum_clause_set_holds_on_full phi hp
  intro c hc hhead
  have hb : c.BodyHolds (full Unit) () () := fun a _ => by
    cases a with
    | xx => exact trivial
    | xy => exact trivial
    | yx => exact trivial
    | yy => exact trivial
    | eq => exact rfl
  have hfalse := h1 c hc () () hb
  rw [hhead] at hfalse
  exact hfalse

/-- T7 (`pure_transfer_above_point_iff_has_falsum_clause`): in the pure
fragment, transferring above the point is again exactly having a
falsum-headed member, on every carrier.  Left to right: with no falsum
head the full relation on `Bool` -- two distinct points and a reflexive
one -- satisfies the set.  Carries P1's key
`T7_lattice_extents_admitting_one_point_full_and_transferring_above_point`
(= 0 in PURE) beyond the bound, and carries the PURE cell of
`S9_1_TRANSFER_CHARACTERIZED` under `TRANSFER_ABOVE_POINT`. -/
theorem pure_transfer_above_point_iff_has_falsum_clause (phi : ClauseSet)
    (hp : phi.Pure) : TransfersAbovePoint phi ↔ phi.HasFalsumClause := by
  constructor
  · intro h
    by_cases hf : phi.HasFalsumClause
    · exact hf
    · exfalso
      have hnf : ∀ c, c ∈ phi → c.head ≠ .falsum := fun c hc hh => hf ⟨c, hc, hh⟩
      have hholds := pure_non_falsum_clause_set_holds_on_full phi hp hnf Bool
      exact h Bool (full Bool) false false ⟨false, true, Bool.noConfusion⟩ hholds trivial rfl
  · intro hf α r a b _ hphi hab
    exact irrefl_witness_ne (has_falsum_clause_entails_irrefl phi hf α r hphi) hab

/-- The `F3_SUPPORTED_BOUNDED` cell (PURE under `TRANSFER_ABOVE_POINT`),
carrier-general: a pure clause set transfers above the point exactly when
it entails irreflexivity, so the set of pure clause sets that transfer
above the point without entailing irreflexivity is empty on every
carrier, not only up to N = 4.  Scope: the pure fragment and this
definition of transfer; the EQ_BEARING countermodel above shows the
`Pure` hypothesis cannot be dropped. -/
theorem pure_transfers_above_point_iff_entails_irrefl (phi : ClauseSet)
    (hp : phi.Pure) : TransfersAbovePoint phi ↔ EntailsIrrefl phi :=
  (pure_transfer_above_point_iff_has_falsum_clause phi hp).trans
    (entails_irrefl_iff_has_falsum_clause phi).symm

/-! ## W under `TRANSFER_ABOVE_POINT`, and where decidable identity enters -/

/-- On a carrier with decidable identity, `r x x -> x = y` holds exactly
when `r` is irreflexive whenever two points differ.  The right-to-left
direction is where decidability is used: from "no two points differ
while `r x x`" to "`x = y`" is a case split on `x = y`. -/
theorem reflexivePointForcesSingleton_holds_iff_of_decidableEq {α : Type}
    [DecidableEq α] (r : α → α → Prop) :
    reflexivePointForcesSingleton.Holds r ↔ ((∃ u v : α, u ≠ v) → Irrefl r) := by
  rw [reflexivePointForcesSingleton_holds_iff]
  constructor
  · intro h huv
    exact reflexive_point_forces_singleton_irrefl_of_two_points r h huv
  · intro h x y hxx
    by_cases hxy : x = y
    · exact hxy
    · exact absurd hxx (h ⟨x, y, hxy⟩ x)

/-- One half of P1's "W is the extent of `r x x -> x = y`" under
`TRANSFER_ABOVE_POINT`, on every carrier: a clause set whose every model
satisfies `r x x -> x = y` transfers above the point. -/
theorem transfers_above_point_of_entails_reflexive_point_forces_singleton
    (phi : ClauseSet)
    (h : ∀ (α : Type) (r : α → α → Prop),
      phi.Holds r → reflexivePointForcesSingleton.Holds r) :
    TransfersAbovePoint phi := by
  intro α r a b huv hphi hab
  exact irrefl_witness_ne
    (reflexive_point_forces_singleton_irrefl_of_two_points r
      ((reflexivePointForcesSingleton_holds_iff r).mp (h α r hphi)) huv) hab

/-- The other half, on every carrier with decidable identity -- which
includes every finite carrier, hence every carrier the sweep ranged over:
a clause set that transfers above the point has `r x x -> x = y` true on
each of its models there.  What is not proved: this direction on carriers
without decidable identity; that residual is named, not closed. -/
theorem transfers_above_point_imp_entails_reflexive_point_forces_singleton
    (phi : ClauseSet) (h : TransfersAbovePoint phi) (α : Type) [DecidableEq α]
    (r : α → α → Prop) (hphi : phi.Holds r) :
    reflexivePointForcesSingleton.Holds r :=
  (reflexivePointForcesSingleton_holds_iff_of_decidableEq r).mpr
    ((transfers_above_point_iff phi).mp h α r hphi)

end S9Obligations.AxiomLattice
