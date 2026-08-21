import Derivation.PrimDiff

/-!
# The alternation, as one general theorem

POST-SEAL extension experiment artifact.  Imports `Derivation.PrimDiff`
unmodified; read-only proof receipt via `lake env lean`.  The abstract engine is
self-contained; the instantiation recovers the concrete rung-3 (sign gap) and
rung-4 (pointed) results from the general theorem, proving the abstraction is
faithful.  No new primitive/parameter/menu/policy/oracle is introduced.

## Statement of the alternation

A **symmetry space** is a type of objects with a relabelling action of a type of
symmetries.  Two objects are *isomorphic* when a symmetry carries one to the
other; a property is *invariant* when it is constant along the action.

Half 1 (`invariant_blind`, needs NO axioms): an invariant cannot separate
isomorphic objects.

Half 2 — enrichment by a datum with a diagonal action:
  * `enrich_new_tie`: the connecting symmetry `g` carries `(a,d)` to `(b, g·d)`,
    a fresh isomorphic pair — a NEW tie, blind again (recursion);
  * `enrich_separates`: if every symmetry connecting `a,b` MOVES the datum `d`,
    then `(a,d)` and `(b,d)` are no longer isomorphic — the tie is RESOLVED;
  * with inverses present, non-isomorphic objects are separated by the orbit
    invariant (`resolution_by_invariant`) — resolution is witnessed by an
    invariant, not merely by non-isomorphism.

`alternation` packages Half 1 + the two Half-2 facts as one theorem.  The tower
is its iteration: resolve-by-invariant → new sign residual → invariant-blind →
enrich (a priced name) → resolve-by-invariant → …
-/

namespace Alt

/-! ## The abstract engine (axiom-free) -/

/-- A symmetry space: objects, symmetries, and a relabelling action. -/
structure SymSpace where
  Obj : Type
  Sym : Type
  act : Sym → Obj → Obj

/-- Isomorphic: some symmetry carries `a` to `b`. -/
def Iso (S : SymSpace) (a b : S.Obj) : Prop := ∃ g, S.act g a = b

/-- Invariant: constant along the action. -/
def Invariant (S : SymSpace) (P : S.Obj → Prop) : Prop := ∀ g a, P (S.act g a) ↔ P a

/-- **HALF 1 — the engine.**  An invariant cannot separate isomorphic objects.
No axioms on the action are used. -/
theorem invariant_blind (S : SymSpace) {a b : S.Obj} (hab : Iso S a b)
    {P : S.Obj → Prop} (hP : Invariant S P) : P a ↔ P b := by
  obtain ⟨g, hg⟩ := hab
  rw [← hg]; exact (hP g a).symm

/-! ## Enrichment (diagonal action on an added datum) -/

/-- Enrich a space by a datum type `D` with its own action, acting diagonally. -/
def enrich (S : SymSpace) (D : Type) (actD : S.Sym → D → D) : SymSpace where
  Obj := S.Obj × D
  Sym := S.Sym
  act := fun g p => (S.act g p.1, actD g p.2)

/-- **HALF 2a — recursion.**  The connecting symmetry carries `(a,d)` to
`(b, g·d)`: a fresh isomorphic pair at the enriched level. -/
theorem enrich_new_tie (S : SymSpace) (D : Type) (actD : S.Sym → D → D)
    {a b : S.Obj} {g : S.Sym} (hg : S.act g a = b) (d : D) :
    Iso (enrich S D actD) (a, d) (b, actD g d) :=
  ⟨g, by show (S.act g a, actD g d) = (b, actD g d); rw [hg]⟩

/-- **HALF 2b — resolution.**  If every symmetry connecting `a` and `b` MOVES the
datum `d`, then `(a,d)` and `(b,d)` are no longer isomorphic. -/
theorem enrich_separates (S : SymSpace) (D : Type) (actD : S.Sym → D → D)
    {a b : S.Obj} {d : D}
    (hmove : ∀ g, S.act g a = b → actD g d ≠ d) :
    ¬ Iso (enrich S D actD) (a, d) (b, d) := by
  rintro ⟨g, hg⟩
  have hg' : (S.act g a, actD g d) = (b, d) := hg
  exact hmove g (congrArg Prod.fst hg') (congrArg Prod.snd hg')

/-! ## Resolution is witnessed by an invariant (given inverses) -/

/-- With inverses and composition, the orbit predicate `Iso a ·` is an invariant. -/
theorem orbit_invariant (S : SymSpace)
    (invS : S.Sym → S.Sym) (compS : S.Sym → S.Sym → S.Sym)
    (hcomp : ∀ g h x, S.act (compS g h) x = S.act g (S.act h x))
    (hinvL : ∀ g x, S.act (invS g) (S.act g x) = x)
    (a : S.Obj) : Invariant S (fun x => Iso S a x) := by
  intro g x
  constructor
  · rintro ⟨k, hk⟩
    exact ⟨compS (invS g) k, by rw [hcomp, hk, hinvL]⟩
  · rintro ⟨k, hk⟩
    exact ⟨compS g k, by rw [hcomp, hk]⟩

/-- Non-isomorphic objects are separated by an invariant: the orbit predicate of
`a` holds of `a` and fails of `b`.  Resolution is witnessed by an invariant. -/
theorem resolution_by_invariant (S : SymSpace)
    (invS : S.Sym → S.Sym) (compS : S.Sym → S.Sym → S.Sym)
    (hcomp : ∀ g h x, S.act (compS g h) x = S.act g (S.act h x))
    (hinvL : ∀ g x, S.act (invS g) (S.act g x) = x)
    (oneS : S.Sym) (hone : ∀ x, S.act oneS x = x)
    {a b : S.Obj} (hnab : ¬ Iso S a b) :
    ∃ P, Invariant S P ∧ P a ∧ ¬ P b :=
  ⟨fun x => Iso S a x, orbit_invariant S invS compS hcomp hinvL a,
   ⟨oneS, hone a⟩, hnab⟩

/-! ## THE ALTERNATION (single theorem) -/

/-- **The alternation.**  In any symmetry space, given an isomorphic tie `a ≈ b`
via `g`, and an enrichment by a datum `d` that every connecting symmetry moves:
  (1) the base tie is invariant-blind;
  (2) the enriched same-datum pair `(a,d),(b,d)` is no longer isomorphic — the
      tie is RESOLVED;
  (3) the enriched moved-datum pair `(a,d),(b,g·d)` IS isomorphic — a NEW tie,
      blind again.
Resolution creates the next residual; iterate for the tower. -/
theorem alternation (S : SymSpace) (D : Type) (actD : S.Sym → D → D)
    {a b : S.Obj} {g : S.Sym} (d : D)
    (hg : S.act g a = b)
    (hmove : ∀ h, S.act h a = b → actD h d ≠ d) :
    (∀ P, Invariant S P → (P a ↔ P b)) ∧
    (¬ Iso (enrich S D actD) (a, d) (b, d)) ∧
    (Iso (enrich S D actD) (a, d) (b, actD g d)) :=
  ⟨fun _ hP => invariant_blind S ⟨g, hg⟩ hP,
   enrich_separates S D actD hmove,
   enrich_new_tie S D actD hg d⟩

/-! ## Instantiation: the primitive-difference sign tower

Recovering rungs 3 and 4 from the general theorem proves the abstraction faithful.
-/

open PrimDiff

/-- Swap-relabelling of a relation. -/
def swapRel (r : Bool → Bool → Prop) : Bool → Bool → Prop :=
  fun x y => r (Bool.not x) (Bool.not y)

theorem swapRel_swapRel (r : Bool → Bool → Prop) : swapRel (swapRel r) = r := by
  funext x y
  show r (Bool.not (Bool.not x)) (Bool.not (Bool.not y)) = r x y
  rw [Bool.not_not, Bool.not_not]

/-- The symmetry action on relations: `false` = identity, `true` = swap. -/
def actS (g : Bool) (r : Bool → Bool → Prop) : Bool → Bool → Prop :=
  cond g (swapRel r) r

/-- The sign symmetry space: relations under the swap. -/
def signSpace : SymSpace where
  Obj := Bool → Bool → Prop
  Sym := Bool
  act := actS

theorem D2rev_iso_D2 : ∀ x y, D2rev x y ↔ D2 (Bool.not x) (Bool.not y) := by decide

theorem D2_ne_D2rev : D2 ≠ D2rev := by
  intro h
  have hc := congrFun (congrFun h false) true
  simp [D2, D2rev] at hc

theorem act_true_D2 : signSpace.act true D2 = D2rev := by
  show swapRel D2 = D2rev
  funext x y
  apply propext
  exact (D2rev_iso_D2 x y).symm

/-- **Rung 3, recovered from the engine.**  `D2 ≈ D2rev`, so every invariant is
blind to the sign gap. -/
theorem D2_iso_D2rev : Iso signSpace D2 D2rev := ⟨true, act_true_D2⟩

theorem sign_gap_blind (P : (Bool → Bool → Prop) → Prop)
    (hP : Invariant signSpace P) : P D2 ↔ P D2rev :=
  invariant_blind signSpace D2_iso_D2rev hP

/-! ### Rung 4, recovered from the enrichment -/

/-- The mark action: `true` swaps the marked point. -/
def actMark (g : Bool) (m : Bool) : Bool := cond g (Bool.not m) m

/-- The pointed (enriched) space. -/
def signEnriched : SymSpace := enrich signSpace Bool actMark

/-- **Rung-4 new tie, from `enrich_new_tie`.**  `(D2, false) ≈ (D2rev, true)`. -/
theorem enriched_new_tie : Iso signEnriched (D2, false) (D2rev, true) :=
  enrich_new_tie signSpace Bool actMark act_true_D2 false

/-- **Rung-4 resolution, from `enrich_separates`.**  `(D2, false)` and
`(D2rev, false)` are no longer isomorphic. -/
theorem enriched_separates : ¬ Iso signEnriched (D2, false) (D2rev, false) := by
  apply enrich_separates signSpace Bool actMark
  intro g hg
  cases g
  · exact absurd (show D2 = D2rev from hg) D2_ne_D2rev
  · decide

/-! ### Enriched group facts, and resolution witnessed by an invariant -/

theorem ehcomp (g h : Bool) (p : (Bool → Bool → Prop) × Bool) :
    signEnriched.act (Bool.xor g h) p = signEnriched.act g (signEnriched.act h p) := by
  cases g <;> cases h
  · rfl
  · rfl
  · rfl
  · show p = (swapRel (swapRel p.1), Bool.not (Bool.not p.2))
    rw [swapRel_swapRel, Bool.not_not]

theorem ehinvL (g : Bool) (p : (Bool → Bool → Prop) × Bool) :
    signEnriched.act g (signEnriched.act g p) = p := by
  cases g
  · rfl
  · show (swapRel (swapRel p.1), Bool.not (Bool.not p.2)) = p
    rw [swapRel_swapRel, Bool.not_not]

/-- **Rung-4 resolution, witnessed by an invariant.**  There is an invariant of
the pointed space that holds of `(D2, false)` and fails of `(D2rev, false)` — the
tie is resolved by an invariant, exactly as the alternation predicts. -/
theorem enriched_resolution :
    ∃ P, Invariant signEnriched P ∧ P (D2, false) ∧ ¬ P (D2rev, false) :=
  resolution_by_invariant signEnriched id Bool.xor ehcomp ehinvL
    false (fun _ => rfl) enriched_separates

/-! ### The instantiated alternation, as one statement -/

/-- **The alternation, instantiated at the sign tower.**  A single theorem: the
sign gap is invariant-blind; enriching by the mark resolves it; and it spawns the
mark-choice tie. -/
theorem sign_tower_alternation :
    (∀ P, Invariant signSpace P → (P D2 ↔ P D2rev)) ∧
    (¬ Iso signEnriched (D2, false) (D2rev, false)) ∧
    (Iso signEnriched (D2, false) (D2rev, true)) := by
  have h := alternation signSpace Bool actMark (a := D2) (b := D2rev) (g := true)
    false act_true_D2 (by
      intro g hg
      cases g
      · exact absurd (show D2 = D2rev from hg) D2_ne_D2rev
      · decide)
  -- (b, actMark true false) = (D2rev, true) by reduction
  exact h

/-! ## Axiom receipts -/

#print axioms invariant_blind
#print axioms enrich_new_tie
#print axioms enrich_separates
#print axioms orbit_invariant
#print axioms resolution_by_invariant
#print axioms alternation
#print axioms sign_gap_blind
#print axioms enriched_new_tie
#print axioms enriched_separates
#print axioms enriched_resolution
#print axioms sign_tower_alternation

end Alt
