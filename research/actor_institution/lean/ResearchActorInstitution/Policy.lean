import ResearchTwoTheorems.Reading
import ResearchActorInstitution.Chain

/-!
# Assert or demur: a policy with retained residuals

The two-theorems tree showed that `Wise` (knowing every member's question)
holds of every institution and so names nothing, and that `Grounded`
(knowing the claim one makes) is the non-overclaiming notion.  This module
turns `Grounded` into a response policy and proves what the policy can and
cannot do.

* `respond`: assert when the claim is known, otherwise demur, carrying the
  residual pairs (the data the institution cannot tell apart on which the
  claim differs).  `respond_assert_iff`, `respond_demur_iff`,
  `demur_carries_witness`.
* `residual_answerable`: every residual names an observation that would
  remove it (a member separating the pair); `evidence_is_not_a_digest`: that
  observation is never a function of the institution's present signatures.
* `demurred`: the claim with every unsettled datum marked.  It is known by
  every institution (`demurred_known`), it decodes (`demurred_zero_iff`), and
  it is total exactly when the claim is known (`demurred_total_iff`).  So an
  institution can always make a grounded claim that says where it demurs.
* Authorization rules.  `ScopedSound`: a rule that authorizes only known
  claims.  `knowsB_scoped_sound`: the knowledge test is such a rule;
  `scoped_sound_refuses_residual`: such a rule never authorizes a claim with
  an unresolved relevant distinction; `authorization_not_correctness`: such a
  rule authorizes claims that disagree everywhere, so authorization is
  relative to the certificate, not to a target.  Any rule stronger than this
  (what a *rightful* authority may do) is an admission, not a theorem.
* Pair claims.  `same x y` is refuted by one separator and never supported;
  `apart x y` is supported by one separator and then persists under every
  extension.  `same_never_established`: for `x ≠ y` every institution has an
  extension refuting `same x y`; `established_iff_eq`: identity survives all
  extensions only for a datum with itself.  `scoped_identity_not_absolute`:
  the identity verdict is relative to the institution.

Every quantifier below ranges over Lean's `Nat` and `List`, which are
metatheory.  The responses are proposals of a policy, not verdicts of an
authority.  AuthorityEffect: None.
-/

namespace ResearchActorInstitution
namespace Policy

open Compression ResearchTwoTheorems.Institution ResearchTwoTheorems.Reading
open ResearchActorInstitution.Chain

/-- A response to a claim: assert it, or demur and retain the residual. -/
inductive Response where
  | assert
  | demur (residual : List (Nat × Nat))
  deriving DecidableEq, Repr

/-- The policy: assert a known claim, otherwise demur with the residual. -/
def respond (D : List Nat) (Q : Institution) (s : Nat → Nat) : Response :=
  if knowsB D Q s then .assert else .demur (residuals D Q s)

theorem respond_assert_iff (D : List Nat) (Q : Institution) (s : Nat → Nat) :
    respond D Q s = .assert ↔ Knows D Q s := by
  unfold respond
  rw [knows_iff_knowsB]
  cases h : knowsB D Q s with
  | true => rw [if_pos rfl]; exact ⟨fun _ => rfl, fun _ => rfl⟩
  | false =>
    rw [if_neg Bool.false_ne_true]
    constructor
    · intro e; cases e
    · intro e; cases e

theorem respond_demur_iff (D : List Nat) (Q : Institution) (s : Nat → Nat) :
    respond D Q s = .demur (residuals D Q s) ↔ ¬ Knows D Q s := by
  unfold respond
  rw [knows_iff_knowsB]
  cases h : knowsB D Q s with
  | true =>
    rw [if_pos rfl]
    constructor
    · intro e; cases e
    · intro e; exact (e rfl).elim
  | false =>
    rw [if_neg Bool.false_ne_true]
    constructor
    · intro _ e; cases e
    · intro _; rfl

/-- A demurral is never empty-handed: it carries a pair the institution
cannot tell apart on which the claim differs. -/
theorem demur_carries_witness {D : List Nat} {Q : Institution} {s : Nat → Nat}
    {R : List (Nat × Nat)} (h : respond D Q s = .demur R) :
    ∃ x y, (x, y) ∈ R ∧ x ∈ D ∧ y ∈ D ∧ SigEq Q x y ∧ s x ≠ s y := by
  unfold respond at h
  cases hk : knowsB D Q s with
  | true => rw [hk, if_pos rfl] at h; cases h
  | false =>
    rw [hk, if_neg Bool.false_ne_true] at h
    injection h with hR
    have hn : ¬ Knows D Q s := by
      rw [knows_iff_knowsB, hk]; exact Bool.false_ne_true
    obtain ⟨x, hx, y, hy, hs, hne⟩ := (not_knows_iff_witness D Q s).mp hn
    refine ⟨x, y, ?_, hx, hy, hs, hne⟩
    rw [← hR]
    exact (mem_residuals D Q s x y).mpr ⟨hx, hy, hs, hne⟩

/-- **Every residual is answerable.**  Admitting a member that separates the
pair removes that residual. -/
theorem residual_answerable {D : List Nat} {Q : Institution} {s : Nat → Nat} {x y : Nat}
    (h : (x, y) ∈ residuals D Q s) :
    (x, y) ∉ residuals D (Q ++ [fun z => if z = x then 1 else 0]) s := by
  rw [residual_removed_iff h]
  obtain ⟨_, _, _, hne⟩ := (mem_residuals D Q s x y).mp h
  have hyx : y ≠ x := fun e => hne (by rw [e])
  intro hs
  have h1 : (if x = x then 1 else 0) = (if y = x then 1 else 0) :=
    hs (fun z => if z = x then 1 else 0) (List.mem_append_right _ List.mem_cons_self)
  rw [if_pos rfl, if_neg hyx] at h1
  exact absurd h1 (by decide)

/-- **Evidence is not a digest.**  A member that would remove a residual is
never a function of the institution's present signatures: the required
observation is new, not a re-reading of what is held. -/
theorem evidence_is_not_a_digest {D : List Nat} {Q : Institution} {s : Nat → Nat}
    {x y : Nat} (h : (x, y) ∈ residuals D Q s) (p : Nat → Nat) (hp : p x ≠ p y) :
    ¬ ∃ f : List Nat → Nat, ∀ z, p z = f (sigList Q z) := by
  rintro ⟨f, hf⟩
  obtain ⟨_, _, hs, _⟩ := (mem_residuals D Q s x y).mp h
  apply hp
  rw [hf x, hf y, (sigEq_iff_sigList Q x y).mp hs]

/-! ## The demurred claim -/

/-- `x` is settled for `s`: every datum the institution cannot tell from `x`
gets the same value under `s`. -/
def settledB (D : List Nat) (Q : Institution) (s : Nat → Nat) (x : Nat) : Bool :=
  D.all (fun y => decide (sigList Q x = sigList Q y → s x = s y))

theorem settledB_iff (D : List Nat) (Q : Institution) (s : Nat → Nat) (x : Nat) :
    settledB D Q s x = true ↔ ∀ y, y ∈ D → sigList Q x = sigList Q y → s x = s y := by
  unfold settledB
  rw [List.all_eq_true]
  constructor
  · intro h y hy; exact of_decide_eq_true (h y hy)
  · intro h y hy; exact decide_eq_true (h y hy)

/-- The claim `s` where it is settled, and the demurral mark `0` elsewhere
(values of `s` are shifted by one so the mark is distinguishable). -/
def demurred (D : List Nat) (Q : Institution) (s : Nat → Nat) : Nat → Nat :=
  fun x => if settledB D Q s x then s x + 1 else 0

theorem demurred_zero_iff (D : List Nat) (Q : Institution) (s : Nat → Nat) (x : Nat) :
    demurred D Q s x = 0 ↔ settledB D Q s x = false := by
  unfold demurred
  cases h : settledB D Q s x with
  | true =>
    rw [if_pos rfl]
    constructor
    · intro e; exact absurd e (Nat.succ_ne_zero _)
    · intro e; cases e
  | false => rw [if_neg Bool.false_ne_true]; exact ⟨fun _ => rfl, fun _ => rfl⟩

theorem demurred_settled (D : List Nat) (Q : Institution) (s : Nat → Nat) (x : Nat)
    (h : settledB D Q s x = true) : demurred D Q s x = s x + 1 := by
  unfold demurred; rw [h, if_pos rfl]

/-- **The demurred claim is always grounded.** -/
theorem demurred_known (D : List Nat) (Q : Institution) (s : Nat → Nat) :
    Knows D Q (demurred D Q s) := by
  rw [knows_iff_determined]
  intro x hx y hy hs
  have hl : sigList Q x = sigList Q y := (sigEq_iff_sigList Q x y).mp hs
  have hsx : settledB D Q s x = true → settledB D Q s y = true := by
    intro h
    rw [settledB_iff] at h ⊢
    intro z hz hyz
    rw [← h y hy hl]
    exact h z hz (hl.trans hyz)
  have hsy : settledB D Q s y = true → settledB D Q s x = true := by
    intro h
    rw [settledB_iff] at h ⊢
    intro z hz hxz
    rw [← h x hx hl.symm]
    exact h z hz (hl.symm.trans hxz)
  show (if settledB D Q s x then s x + 1 else 0) = (if settledB D Q s y then s y + 1 else 0)
  cases hbx : settledB D Q s x with
  | true =>
    rw [hsx hbx]
    show s x + 1 = s y + 1
    rw [(settledB_iff D Q s x).mp hbx y hy hl]
  | false =>
    cases hby : settledB D Q s y with
    | true => rw [hsy hby] at hbx; cases hbx
    | false => rw [if_neg Bool.false_ne_true, if_neg Bool.false_ne_true]

/-- The demurred claim is total (demurs nowhere) exactly when the claim is
known. -/
theorem demurred_total_iff (D : List Nat) (Q : Institution) (s : Nat → Nat) :
    (∀ x, x ∈ D → settledB D Q s x = true) ↔ Knows D Q s := by
  rw [knows_iff_determined]
  constructor
  · intro h x hx y hy hs
    exact (settledB_iff D Q s x).mp (h x hx) y hy ((sigEq_iff_sigList Q x y).mp hs)
  · intro h x hx
    rw [settledB_iff]
    intro y hy hl
    exact h x hx y hy ((sigEq_iff_sigList Q x y).mpr hl)

/-! ## Authorization rules -/

/-- An authorization rule reads the carrier, the institution and the claim,
and returns a verdict. -/
abbrev Rule := List Nat → Institution → (Nat → Nat) → Bool

/-- A rule is sound relative to the institution's own evidence when it
authorizes only known claims. -/
def ScopedSound (A : Rule) : Prop := ∀ D Q s, A D Q s = true → Knows D Q s

theorem knowsB_scoped_sound : ScopedSound knowsB := by
  intro D Q s h
  exact (knows_iff_knowsB D Q s).mpr h

theorem scoped_sound_le_knowsB {A : Rule} (h : ScopedSound A) :
    ∀ D Q s, A D Q s = true → knowsB D Q s = true := by
  intro D Q s hA
  exact (knows_iff_knowsB D Q s).mp (h D Q s hA)

/-- **No authorization over an unresolved relevant distinction.**  A scoped
sound rule refuses every claim with a residual. -/
theorem scoped_sound_refuses_residual {A : Rule} (h : ScopedSound A)
    {D : List Nat} {Q : Institution} {s : Nat → Nat} {x y : Nat}
    (hr : (x, y) ∈ residuals D Q s) : A D Q s = false := by
  cases hA : A D Q s with
  | false => rfl
  | true =>
    exfalso
    have hk := h D Q s hA
    rw [← residuals_nil_iff] at hk
    rw [hk] at hr
    cases hr

/-- **Authorization is relative to the certificate, not to a target.**  The
knowledge test authorizes, on any nonempty carrier, two claims that agree
nowhere. -/
theorem authorization_not_correctness (D : List Nat) (Q : Institution) (hD : D ≠ []) :
    knowsB D Q (fun _ => 0) = true ∧ knowsB D Q (fun _ => 1) = true ∧
    ¬ Corr D (fun _ => 0) (fun _ => 1) := by
  refine ⟨(knows_iff_knowsB D Q _).mp (knows_const D Q 0),
    (knows_iff_knowsB D Q _).mp (knows_const D Q 1), ?_⟩
  intro h
  cases D with
  | nil => exact hD rfl
  | cons x _ => exact Nat.zero_ne_one (h x List.mem_cons_self)

/-! ## Pair claims -/

inductive PairClaim where
  | same (x y : Nat)
  | apart (x y : Nat)
  deriving DecidableEq, Repr

inductive Outcome where
  | supported
  | refuted
  | unresolved
  deriving DecidableEq, Repr

/-- Some member tells `x` and `y` apart. -/
def separatesB (Q : Institution) (x y : Nat) : Bool := Q.any (fun p => decide (p x ≠ p y))

theorem separatesB_iff (Q : Institution) (x y : Nat) :
    separatesB Q x y = true ↔ ¬ SigEq Q x y := by
  unfold separatesB
  rw [List.any_eq_true]
  constructor
  · rintro ⟨p, hp, hd⟩ hs
    exact (of_decide_eq_true hd) (hs p hp)
  · intro hs
    obtain ⟨p, hp, hne⟩ := exists_separator_of_not_sigEq Q x y hs
    exact ⟨p, hp, decide_eq_true hne⟩

/-- The outcome of a pair claim against an institution's evidence. -/
def outcome (Q : Institution) : PairClaim → Outcome
  | .same x y => if separatesB Q x y then .refuted else .unresolved
  | .apart x y => if separatesB Q x y then .supported else .unresolved

theorem same_refuted_iff (Q : Institution) (x y : Nat) :
    outcome Q (.same x y) = .refuted ↔ ¬ SigEq Q x y := by
  rw [← separatesB_iff]
  show (if separatesB Q x y then Outcome.refuted else Outcome.unresolved) = .refuted ↔ _
  cases separatesB Q x y with
  | true => rw [if_pos rfl]; exact ⟨fun _ => rfl, fun _ => rfl⟩
  | false => rw [if_neg Bool.false_ne_true]; constructor <;> intro e <;> cases e

theorem same_unresolved_iff (Q : Institution) (x y : Nat) :
    outcome Q (.same x y) = .unresolved ↔ SigEq Q x y := by
  show (if separatesB Q x y then Outcome.refuted else Outcome.unresolved) = .unresolved ↔ _
  cases h : separatesB Q x y with
  | true =>
    rw [if_pos rfl]
    constructor
    · intro e; cases e
    · intro hs; exact absurd hs ((separatesB_iff Q x y).mp h)
  | false =>
    rw [if_neg Bool.false_ne_true]
    constructor
    · intro _
      cases decEq (sigList Q x) (sigList Q y) with
      | isTrue e => exact (sigEq_iff_sigList Q x y).mpr e
      | isFalse ne =>
        have := (separatesB_iff Q x y).mpr (fun hs => ne ((sigEq_iff_sigList Q x y).mp hs))
        rw [h] at this; cases this
    · intro _; rfl

/-- A claim of identity is never supported by evidence. -/
theorem same_never_supported (Q : Institution) (x y : Nat) :
    outcome Q (.same x y) ≠ .supported := by
  show (if separatesB Q x y then Outcome.refuted else Outcome.unresolved) ≠ .supported
  cases separatesB Q x y with
  | true => rw [if_pos rfl]; intro e; cases e
  | false => rw [if_neg Bool.false_ne_true]; intro e; cases e

theorem apart_supported_iff (Q : Institution) (x y : Nat) :
    outcome Q (.apart x y) = .supported ↔ ¬ SigEq Q x y := by
  rw [← separatesB_iff]
  show (if separatesB Q x y then Outcome.supported else Outcome.unresolved) = .supported ↔ _
  cases separatesB Q x y with
  | true => rw [if_pos rfl]; exact ⟨fun _ => rfl, fun _ => rfl⟩
  | false => rw [if_neg Bool.false_ne_true]; constructor <;> intro e <;> cases e

/-- A claim of apartness is never refuted by evidence. -/
theorem apart_never_refuted (Q : Institution) (x y : Nat) :
    outcome Q (.apart x y) ≠ .refuted := by
  show (if separatesB Q x y then Outcome.supported else Outcome.unresolved) ≠ .refuted
  cases separatesB Q x y with
  | true => rw [if_pos rfl]; intro e; cases e
  | false => rw [if_neg Bool.false_ne_true]; intro e; cases e

/-- **Apartness persists.**  Once supported, an apartness claim stays
supported under every extension. -/
theorem apart_persists {Q Q' : Institution} (hext : Extends Q Q') {x y : Nat}
    (h : outcome Q (.apart x y) = .supported) : outcome Q' (.apart x y) = .supported := by
  rw [apart_supported_iff] at h ⊢
  intro hs
  exact h (fun p hp => hs p (hext p hp))

/-- A refutation of identity persists too. -/
theorem same_refuted_persists {Q Q' : Institution} (hext : Extends Q Q') {x y : Nat}
    (h : outcome Q (.same x y) = .refuted) : outcome Q' (.same x y) = .refuted := by
  rw [same_refuted_iff] at h ⊢
  intro hs
  exact h (fun p hp => hs p (hext p hp))

/-- **Identity is never established.**  For two different data every
institution has an extension that refutes their identity. -/
theorem same_never_established {x y : Nat} (hxy : x ≠ y) (Q : Institution) :
    ∃ Q', Extends Q Q' ∧ outcome Q' (.same x y) = .refuted := by
  refine ⟨Q ++ [fun z => if z = x then 1 else 0], fun p hp => List.mem_append_left _ hp, ?_⟩
  rw [same_refuted_iff]
  intro hs
  have h1 : (if x = x then 1 else 0) = (if y = x then 1 else 0) :=
    hs (fun z => if z = x then 1 else 0) (List.mem_append_right _ List.mem_cons_self)
  rw [if_pos rfl, if_neg (fun e => hxy e.symm)] at h1
  exact absurd h1 (by decide)

/-- Identity survives every extension exactly for a datum and itself. -/
theorem established_iff_eq (Q : Institution) (x y : Nat) :
    (∀ Q', Extends Q Q' → SigEq Q' x y) ↔ x = y := by
  constructor
  · intro h
    cases Nat.decEq x y with
    | isTrue e => exact e
    | isFalse ne =>
      exfalso
      obtain ⟨Q', hext, hr⟩ := same_never_established ne Q
      rw [same_refuted_iff] at hr
      exact hr (h Q' hext)
  · intro e Q' _ p _
    rw [e]

/-- The identity verdict, scoped to an institution. -/
def sameRel (Q : Institution) (x y : Nat) : Bool := Q.all (fun p => decide (p x = p y))

theorem sameRel_iff (Q : Institution) (x y : Nat) : sameRel Q x y = true ↔ SigEq Q x y := by
  unfold sameRel
  rw [List.all_eq_true]
  constructor
  · intro h p hp; exact of_decide_eq_true (h p hp)
  · intro h p hp; exact decide_eq_true (h p hp)

/-- The same two data are "the same" for the empty institution and "apart"
for the institution holding the identity presentation. -/
theorem scoped_identity_not_absolute :
    sameRel [] 0 1 = true ∧ sameRel [fun z => z] 0 1 = false := by
  decide

end Policy
end ResearchActorInstitution
