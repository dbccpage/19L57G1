import SecondResponse.Kernel
import SecondResponse.IsoKernel
import SecondResponse.Carry

/-!
# Exhaustion: a form that distinguishes nobody

Native to rung ten.

* `Distinguishes r f`: some well-formed context on form `f` tells two
  admitted data apart by positive derivability.
* `Exhausted r f`: every well-formed context on form `f` reads every two
  admitted data alike -- the reading of the census row "exhaustion, as a
  form that distinguishes nobody" this rung declares.
* `HasExhausted r`: some admitted form of `r` is exhausted.
* `exhausted_iff_not_distinguishes`: a form is exhausted exactly when it
  does not distinguish.  Constructive: derivability is decidable, and no
  classical step is taken.
* `holdsTwo_iff_distinguishes`: a regime holds two exactly when some form
  distinguishes.  `HoldsTwo` is rung nine's definition, stated again.
* `exhausted_of_rule`, `exhausted_of_no_inst`, `exhausted_of_le_one`: a
  form carrying a uniform rule, a form on which no held instance lies,
  and every form of a regime holding at most one datum, are exhausted,
  with no hypothesis on the regime.
* `exhausted_iso`: a form admitted in the source is exhausted exactly
  when its image under an inhabitant of the sealed isomorphism is, with
  no hypothesis on either regime.
* `no_exhausted_at_genesis`, `exhaustion_at_one`: the sealed empty regime
  has no exhausted form; one form admission of arity one reaches a regime
  that has one.

AuthorityEffect: None.
-/

namespace SecondResponse
namespace Exhaust

open Sealed
open Carry (isoSymm mapCtx wfCtx_mapCtx derivable_mapCtx)

/-- Some two admitted data are separable (rung nine's definition). -/
def HoldsTwo (r : Regime) : Prop :=
  ∃ d d', d < r.data ∧ d' < r.data ∧ separable r d d'

/-- Some well-formed context on form `f` tells two admitted data apart. -/
def Distinguishes (r : Regime) (f : Nat) : Prop :=
  ∃ c d d', wfCtx r c ∧ c.form = f ∧ d < r.data ∧ d' < r.data ∧
    ¬ (derivable r (plug c d) ↔ derivable r (plug c d'))

/-- Every well-formed context on form `f` reads every two admitted data
alike. -/
def Exhausted (r : Regime) (f : Nat) : Prop :=
  ∀ c, wfCtx r c → c.form = f → ∀ d d', d < r.data → d' < r.data →
    (derivable r (plug c d) ↔ derivable r (plug c d'))

/-- Some admitted form is exhausted. -/
def HasExhausted (r : Regime) : Prop :=
  ∃ f, f < r.forms.length ∧ Exhausted r f

/-- A form is exhausted exactly when it does not distinguish. -/
theorem exhausted_iff_not_distinguishes (r : Regime) (f : Nat) :
    Exhausted r f ↔ ¬ Distinguishes r f := by
  constructor
  · intro h ⟨c, d, d', hc, hf, hd, hd', hne⟩
    exact hne (h c hc hf d d' hd hd')
  · intro h c hc hf d d' hd hd'
    by_cases h1 : derivable r (plug c d)
    · by_cases h2 : derivable r (plug c d')
      · exact iff_of_true h1 h2
      · exact absurd ⟨c, d, d', hc, hf, hd, hd', fun e => h2 (e.mp h1)⟩ h
    · by_cases h2 : derivable r (plug c d')
      · exact absurd ⟨c, d, d', hc, hf, hd, hd', fun e => h1 (e.mpr h2)⟩ h
      · exact iff_of_false h1 h2

/-- A regime holds two exactly when some form distinguishes. -/
theorem holdsTwo_iff_distinguishes (r : Regime) :
    HoldsTwo r ↔ ∃ f, Distinguishes r f := by
  constructor
  · intro ⟨d, d', hd, hd', c, hc, hne⟩
    exact ⟨c.form, c, d, d', hc, rfl, hd, hd', hne⟩
  · intro ⟨_, c, d, d', hc, _, hd, hd', hne⟩
    exact ⟨d, d', hd, hd', c, hc, hne⟩

/-- A form carrying a uniform rule is exhausted. -/
theorem exhausted_of_rule {r : Regime} {f : Nat} (h : f ∈ r.rules) :
    Exhausted r f := by
  intro c _ hf d d' _ _
  have hr : (plug c d).1 ∈ r.rules := by
    show c.form ∈ r.rules
    rw [hf]; exact h
  have hr' : (plug c d').1 ∈ r.rules := by
    show c.form ∈ r.rules
    rw [hf]; exact h
  exact iff_of_true (Or.inr hr) (Or.inr hr')

/-- A form on which no held instance lies is exhausted: every plugging on
it is derivable exactly when the form carries a rule. -/
theorem exhausted_of_no_inst {r : Regime} {f : Nat}
    (h : ∀ p ∈ r.insts, p.1 ≠ f) : Exhausted r f := by
  intro c _ hf d d' _ _
  have key : ∀ x, derivable r (plug c x) ↔ c.form ∈ r.rules := by
    intro x
    constructor
    · intro hx
      cases hx with
      | inl hx => exact absurd hf (h _ hx)
      | inr hx => exact hx
    · intro hx
      exact Or.inr hx
  exact (key d).trans (key d').symm

/-- Every form of a regime holding at most one datum is exhausted. -/
theorem exhausted_of_le_one {r : Regime} (h : r.data ≤ 1) (f : Nat) :
    Exhausted r f := by
  intro c _ _ d d' hd hd'
  have e1 : d = 0 := Nat.eq_zero_of_le_zero (Nat.le_of_lt_succ (Nat.lt_of_lt_of_le hd h))
  have e2 : d' = 0 := Nat.eq_zero_of_le_zero (Nat.le_of_lt_succ (Nat.lt_of_lt_of_le hd' h))
  rw [e1, e2]

/-- A form admitted in the source is exhausted exactly when its image
under an inhabitant of the sealed isomorphism is.  The forward direction
reads every well-formed context of the target back along the exchanged
structure; the backward direction is the forward one along it. -/
theorem exhausted_iso {r s : Regime} (σ : Iso r s) {f : Nat}
    (hf : f < r.forms.length) : Exhausted r f ↔ Exhausted s (σ.fmap f) := by
  have fwd : ∀ {a b : Regime} (τ : Iso a b) {g : Nat}, g < a.forms.length →
      Exhausted a g → Exhausted b (τ.fmap g) := by
    intro a b τ g hg h c hc hcg d d' hd hd'
    have hx : τ.dinv d < a.data := τ.dinv_lt d (List.mem_range.mpr hd)
    have hx' : τ.dinv d' < a.data := τ.dinv_lt d' (List.mem_range.mpr hd')
    have e1 := derivable_mapCtx (isoSymm τ) hc hd
    have e2 := derivable_mapCtx (isoSymm τ) hc hd'
    have hback : (mapCtx (isoSymm τ) c).form = g := by
      show τ.finv c.form = g
      rw [hcg]
      exact τ.finv_fmap g (List.mem_range.mpr hg)
    exact e1.trans ((h _ (wfCtx_mapCtx (isoSymm τ) hc) hback _ _ hx hx').trans e2.symm)
  constructor
  · exact fwd σ hf
  · intro h
    have hlt : σ.fmap f < s.forms.length := σ.fmap_lt f (List.mem_range.mpr hf)
    have h' := fwd (isoSymm σ) hlt h
    have hb : (isoSymm σ).fmap (σ.fmap f) = f := σ.finv_fmap f (List.mem_range.mpr hf)
    rw [hb] at h'
    exact h'

/-- The sealed empty regime has no exhausted form: it has no form. -/
theorem no_exhausted_at_genesis : ¬ HasExhausted genesis := by
  intro ⟨f, hf, _⟩
  exact absurd hf (Nat.not_lt_zero f)

/-- One form admission of arity one reaches a regime with an exhausted
form. -/
theorem exhaustion_at_one :
    ∃ r, replayE [.admitForm 1] genesis = some r ∧ HasExhausted r := by
  refine ⟨⟨0, [1], [], [], []⟩, by decide, 0, by decide, ?_⟩
  exact exhausted_of_le_one (by decide) 0

end Exhaust
end SecondResponse
