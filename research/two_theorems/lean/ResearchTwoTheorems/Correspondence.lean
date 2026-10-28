import Derivation.Represented
import Derivation.Compression
import Derivation.PresentationRelativity
import ResearchTwoTheorems.Observer
import ResearchTwoTheorems.Institution

/-!
# Correspondences and their fidelity

A correspondence carries the points of a carrier to the points an observer
or an institution reads.  An unrestricted map can merge two points before
any observer evaluates them, and then the observer's collapse of the images
says nothing about the observer: `verdictB E (f x) (f y) = false` holds for
every `E` as soon as `f x = f y`.  This module names the fidelity contract
that rules that out (a correspondence is *faithful* on a carrier when it
merges no two of its points), shows that the constant map fails it, shows
that the contract is exactly what sharp observation of the identity through
a correspondence requires, and identifies it with a knowledge statement:
the actor of an institution is a faithful correspondence exactly when the
institution knows the identity.

Fidelity is relative to the actor observed.  Sharpness for an actor `p`
transports along *every* correspondence (`sharp_pullback_iff`); what a
sharp observation through `f` forces is that `f` merges only points the
actor merges (`fiberConstant_of_sharp_pullback`).  Injectivity is the
special case of the identity actor.
-/

namespace ResearchTwoTheorems.Correspondence

open Represented Compression PresentationRelativity Institution

/-- A correspondence is faithful on a carrier when it merges no two of its
points. -/
def Faithful (D : List Nat) (f : Nat → Nat) : Prop :=
  ∀ x, x ∈ D → ∀ y, y ∈ D → f x = f y → x = y

/-- Under any map, collapse of the images of a merged pair is automatic for
every observer: the collapse is the map's doing, not the observer's. -/
theorem collapsed_of_merged (E : Evaluator) (f : Nat → Nat) {x y : Nat}
    (h : f x = f y) : verdictB E (f x) (f y) = false := by
  rw [h]
  exact verdict_irrefl E (f y)

/-- The constant correspondence collapses every pair under every observer. -/
theorem constant_collapses_all (E : Evaluator) (x y : Nat) :
    verdictB E ((fun _ => 0) x) ((fun _ => 0) y) = false :=
  verdict_irrefl E 0

/-- The constant correspondence is not faithful on the two-point carrier. -/
theorem constant_not_faithful : ¬ Faithful [0, 1] (fun _ => 0) := by
  intro h
  exact Nat.zero_ne_one (h 0 (by decide) 1 (by decide) rfl)

/-- Faithfulness is fiber identity with the identity presentation: a faithful
correspondence has the finest fibers on the carrier. -/
theorem faithful_iff_fiberIdentity (D : List Nat) (f : Nat → Nat) :
    Faithful D f ↔ FiberIdentityOn D f (fun x => x) := by
  constructor
  · intro h x hx y hy
    constructor
    · exact h x hx y hy
    · intro hxy
      have hxy' : x = y := hxy
      rw [hxy']
  · intro h x hx y hy hf
    exact (h x hx y hy).mp hf

/-- The actor of an institution is a faithful correspondence on the carrier
exactly when the institution knows the identity, that is, resolves every
point of the carrier. -/
theorem faithful_actor_iff (D : List Nat) (Q : Institution) :
    Faithful D (pQ D Q) ↔ Knows D Q (fun x => x) := by
  rw [knows_iff_determined]
  constructor
  · intro h x hx y hy hs
    exact h x hx y hy ((pQ_exact D Q x hx y hy).mpr hs)
  · intro h x hx y hy hp
    exact h x hx y hy ((pQ_exact D Q x hx y hy).mp hp)

/-- The empty institution's actor is constant on the carrier: every point has
the empty signature. -/
theorem empty_actor_constant (D : List Nat) :
    ∀ x, x ∈ D → ∀ y, y ∈ D → pQ D [] x = pQ D [] y := by
  intro x hx y hy
  exact (pQ_exact D [] x hx y hy).mpr (fun _ hq => nomatch hq)

/-- Hence the empty institution's actor is not faithful on a two-point
carrier: it is the constant correspondence there. -/
theorem empty_actor_not_faithful : ¬ Faithful [0, 1] (pQ [0, 1] []) := by
  intro h
  exact Nat.zero_ne_one
    (h 0 (by decide) 1 (by decide) (empty_actor_constant [0, 1] 0 (by decide) 1 (by decide)))

/-! ## Reading an observer through a correspondence -/

/-- The views of an observer read back along a correspondence onto a
carrier. -/
def pullback (D : List Nat) (f : Nat → Nat) (E : Evaluator) : Evaluator :=
  E.map (fun c => D.filter (fun x => decide (f x ∈ c)))

theorem mem_pullback_view {D : List Nat} {f : Nat → Nat} {c : View} {x : Nat}
    (hx : x ∈ D) :
    x ∈ D.filter (fun z => decide (f z ∈ c)) ↔ f x ∈ c := by
  rw [List.mem_filter]
  constructor
  · intro h
    exact of_decide_eq_true h.2
  · intro h
    exact ⟨hx, decide_eq_true h⟩

theorem sep_pullback {D : List Nat} {f : Nat → Nat} (c : View) {x y : Nat}
    (hx : x ∈ D) (hy : y ∈ D) :
    sepB (D.filter (fun z => decide (f z ∈ c))) x y = sepB c (f x) (f y) := by
  unfold sepB
  rw [decide_eq_decide.mpr (mem_pullback_view (c := c) hx),
    decide_eq_decide.mpr (mem_pullback_view (c := c) hy)]

/-- A pulled-back observer renders on the source exactly the verdicts the
observer renders on the images. -/
theorem verdict_pullback (D : List Nat) (f : Nat → Nat) (E : Evaluator) {x y : Nat}
    (hx : x ∈ D) (hy : y ∈ D) :
    verdictB (pullback D f E) x y = verdictB E (f x) (f y) := by
  unfold pullback verdictB
  rw [List.any_map]
  exact congrArg (List.any E) (funext fun c => sep_pullback c hx hy)

/-- Sharpness transports along every correspondence: an observer is sharp
for an actor on the image carrier exactly when its pullback is sharp for the
composed actor on the source carrier.  No fidelity is needed. -/
theorem sharp_pullback_iff (D : List Nat) (f : Nat → Nat) (E : Evaluator)
    (p : Presentation) :
    Sharp (D.map f) E p ↔ Sharp D (pullback D f E) (fun x => p (f x)) := by
  unfold Sharp
  constructor
  · intro h x hx y hy
    rw [verdict_pullback D f E hx hy]
    exact h (f x) (List.mem_map.mpr ⟨x, hx, rfl⟩) (f y) (List.mem_map.mpr ⟨y, hy, rfl⟩)
  · intro h x' hx' y' hy'
    obtain ⟨x, hx, rfl⟩ := List.mem_map.mp hx'
    obtain ⟨y, hy, rfl⟩ := List.mem_map.mp hy'
    rw [← verdict_pullback D f E hx hy]
    exact h x hx y hy

/-- What a sharp observation through a correspondence forces of the
correspondence: it may merge only points the observed actor merges. -/
theorem fiberConstant_of_sharp_pullback (D : List Nat) (f : Nat → Nat) (E : Evaluator)
    (q : Presentation) (h : Sharp D (pullback D f E) q) : FiberConstant D f q := by
  intro x hx y hy hf
  have hv : verdictB (pullback D f E) x y = false := by
    rw [verdict_pullback D f E hx hy]
    exact collapsed_of_merged E f hf
  exact (h x hx y hy).mp hv

/-- The identity case: an observer read through a correspondence can be
sharp for the identity of the source carrier only if the correspondence is
faithful.  A merged pair is collapsed by every observer, so the merge would
be a failure of sharpness. -/
theorem faithful_of_sharp_identity (D : List Nat) (f : Nat → Nat) (E : Evaluator)
    (h : Sharp D (pullback D f E) (fun x => x)) : Faithful D f :=
  fiberConstant_of_sharp_pullback D f E (fun x => x) h

/-- Conversely, through a faithful correspondence an observer sharp for the
identity on the image is sharp for the identity on the source. -/
theorem sharp_identity_pullback (D : List Nat) (f : Nat → Nat) (E : Evaluator)
    (hf : Faithful D f) (h : Sharp (D.map f) E (fun x => x)) :
    Sharp D (pullback D f E) (fun x => x) := by
  intro x hx y hy
  rw [verdict_pullback D f E hx hy]
  constructor
  · intro hv
    exact hf x hx y hy
      ((h (f x) (List.mem_map.mpr ⟨x, hx, rfl⟩) (f y) (List.mem_map.mpr ⟨y, hy, rfl⟩)).mp hv)
  · intro hxy
    have hxy' : x = y := hxy
    rw [hxy']
    exact verdict_irrefl E (f y)

end ResearchTwoTheorems.Correspondence
