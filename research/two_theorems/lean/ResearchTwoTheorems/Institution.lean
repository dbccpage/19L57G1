import Derivation.Represented
import Derivation.NoOutside
import Derivation.Compression
import Derivation.PresentationRelativity
import ResearchTwoTheorems.Observer

/-!
# Theorem II — institutional knowledge and wisdom

AuthorityEffect: None.  Outside the seal; consumes the sealed `Derivation`
package read-only.

Vocabulary, each item tagged.

* DECLARED (supplied by the requester, not Genesis): an *institution* is a
  presentation family — in Genesis, a represented question family
  `Q : List (Nat → Nat)`; its *actor* is the joint presentation `pQ D Q`
  (so an institution is a kind of actor); a *fiber* of the actor is a
  signature class.
* DEFINITIONS: `information D Q` (the class count of the family on `D`);
  `Knows D Q q` (the institution knows `q` on `D` when `q` factors through
  the actor); `Wise D Q` (for every question, either knowledge or a
  represented witness of ignorance).
* THEOREMS: knowledge is exactly signature determination
  (`knows_iff_determined`), closed under every computation on known
  answers (`knows_comp`, `knows_join`) and monotone in the family
  (`knows_mono`); knowledge is exactly information stationarity
  (`knows_iff_information_eq`) and ignorance exactly a strict information
  increase (`information_lt_of_not_knows`); a known question, the actor
  included, adds nothing (`known_extension_inert`, `self_inclusion_inert`);
  the institution read as one actor carries the institution's information
  (`institution_is_actor`); a member observes the whole institution
  sharply exactly when it alone knows every member (`member_sharp_iff`),
  and an institution can exceed each of its members
  (`institution_exceeds_members`); an observer is sharp for an institution
  exactly when the two know each other
  (`sharp_institution_iff_mutual_knowledge`); the pooled panel merges
  exactly the panel's joint quotient (Genesis `certNegB`) while unanimous
  separation is strictly stronger than pooled separation
  (`certPos_imp_pooled`, `pooled_not_certPos`); an institution of `m`
  Boolean questions carries at most `2 ^ m` information
  (`information_le_resolution`); every institution on a represented carrier
  is wise at the question level (`wise_of_represented`, by a Boolean
  decision procedure, no excluded middle).

Nothing here says what an institution *should* know; `Knows` is a
factorization fact about represented data.
-/

namespace ResearchTwoTheorems
namespace Institution

open Represented Compression

/-- DECLARED: an institution is a represented question family. -/
abbrev Institution := List (Nat → Nat)

/-- The institution as one actor: Genesis's joint presentation. -/
def actor (D : List Nat) (Q : Institution) : Nat → Nat := pQ D Q

/-- Information of an institution on `D`: how many signature classes it
cuts `D` into (Genesis `classCount`). -/
def information (D : List Nat) (Q : Institution) : Nat := classCount D Q

/-- The institution knows `q` on `D`: `q` factors through its actor. -/
def Knows (D : List Nat) (Q : Institution) (q : Nat → Nat) : Prop :=
  FactorsOn D (pQ D Q) q

/-! ## Knowledge is signature determination -/

theorem knows_iff_determined (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows D Q q ↔ ∀ x, x ∈ D → ∀ y, y ∈ D → SigEq Q x y → q x = q y := by
  unfold Knows
  rw [factors_iff_fiberConstant]
  unfold FiberConstant
  constructor
  · intro h x hx y hy hs
    exact h x hx y hy ((pQ_exact D Q x hx y hy).mpr hs)
  · intro h x hx y hy hp
    exact h x hx y hy ((pQ_exact D Q x hx y hy).mp hp)

theorem knows_iff_sigList (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows D Q q ↔
      ∀ x, x ∈ D → ∀ y, y ∈ D → sigList Q x = sigList Q y → q x = q y := by
  rw [knows_iff_determined]
  constructor
  · intro h x hx y hy hs
    exact h x hx y hy ((sigEq_iff_sigList Q x y).mpr hs)
  · intro h x hx y hy hs
    exact h x hx y hy ((sigEq_iff_sigList Q x y).mp hs)

/-- Knowledge is decidable on a represented carrier: a list computation,
no choice principle, no excluded middle. -/
instance knowsDecidable (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Decidable (Knows D Q q) :=
  decidable_of_iff _ (knows_iff_sigList D Q q).symm

theorem knows_member {D : List Nat} {Q : Institution} {q : Nat → Nat}
    (hq : q ∈ Q) : Knows D Q q :=
  (knows_iff_determined D Q q).mpr (fun _ _ _ _ hs => hs q hq)

theorem knows_const (D : List Nat) (Q : Institution) (c : Nat) :
    Knows D Q (fun _ => c) :=
  ⟨fun _ => c, fun _ _ => rfl⟩

/-- The institution knows its own actor. -/
theorem knows_actor (D : List Nat) (Q : Institution) : Knows D Q (pQ D Q) :=
  ⟨fun y => y, fun _ _ => rfl⟩

/-- Inference closure: anything computed from a known answer is known. -/
theorem knows_comp {D : List Nat} {Q : Institution} {q : Nat → Nat}
    (g : Nat → Nat) (h : Knows D Q q) : Knows D Q (fun x => g (q x)) := by
  obtain ⟨f, hf⟩ := h
  refine ⟨fun y => g (f y), fun x hx => ?_⟩
  show g (f (pQ D Q x)) = g (q x)
  rw [hf x hx]

/-- Anything computed from two known answers is known. -/
theorem knows_join {D : List Nat} {Q : Institution} {q₁ q₂ : Nat → Nat}
    (g : Nat → Nat → Nat) (h₁ : Knows D Q q₁) (h₂ : Knows D Q q₂) :
    Knows D Q (fun x => g (q₁ x) (q₂ x)) := by
  obtain ⟨f₁, hf₁⟩ := h₁
  obtain ⟨f₂, hf₂⟩ := h₂
  refine ⟨fun y => g (f₁ y) (f₂ y), fun x hx => ?_⟩
  show g (f₁ (pQ D Q x)) (f₂ (pQ D Q x)) = g (q₁ x) (q₂ x)
  rw [hf₁ x hx, hf₂ x hx]

/-- A larger institution knows everything a smaller one knows. -/
theorem knows_mono {D : List Nat} {Q Q' : Institution} {q : Nat → Nat}
    (hsub : ∀ q', q' ∈ Q → q' ∈ Q') (h : Knows D Q q) : Knows D Q' q := by
  rw [knows_iff_determined] at h ⊢
  intro x hx y hy hs
  exact h x hx y hy (enlarge_refines Q Q' hsub x y hs)

/-! ## Information -/

theorem information_le_carrier (D : List Nat) (Q : Institution) :
    information D Q ≤ D.length :=
  refine_bounded D Q

/-- A known question carries no more information than the institution. -/
theorem information_known_le {D : List Nat} {Q : Institution} {q : Nat → Nat}
    (h : Knows D Q q) : classCount D [q] ≤ information D Q := by
  unfold information classCount
  apply count_le_of_determines (sigList Q) (sigList [q]) D
  intro a ha b hb hab
  have := (knows_iff_sigList D Q q).mp h a ha b hb hab
  show [q a] = [q b]
  rw [this]

theorem information_member_le {D : List Nat} {Q : Institution} {q : Nat → Nat}
    (hq : q ∈ Q) : classCount D [q] ≤ information D Q :=
  information_known_le (knows_member hq)

theorem information_mono {D : List Nat} {Q Q' : Institution}
    (hsub : ∀ q, q ∈ Q → q ∈ Q') : information D Q ≤ information D Q' := by
  unfold information classCount
  apply count_le_of_determines (sigList Q') (sigList Q) D
  intro a ha b hb hab
  exact (sigEq_iff_sigList Q a b).mp
    (enlarge_refines Q Q' hsub a b ((sigEq_iff_sigList Q' a b).mpr hab))

theorem sigList_append_eq_of_knows {D : List Nat} {Q : Institution}
    {q : Nat → Nat} (h : Knows D Q q) {a b : Nat} (ha : a ∈ D) (hb : b ∈ D)
    (hab : sigList Q a = sigList Q b) :
    sigList (Q ++ [q]) a = sigList (Q ++ [q]) b := by
  apply (sigEq_iff_sigList _ a b).mp
  intro q' hq'
  rcases List.mem_append.mp hq' with hq' | hq'
  · exact (sigEq_iff_sigList Q a b).mpr hab q' hq'
  · rw [List.mem_singleton.mp hq']
    exact (knows_iff_sigList D Q q).mp h a ha b hb hab

/-- A known question adds no information. -/
theorem information_append_of_knows {D : List Nat} {Q : Institution}
    {q : Nat → Nat} (h : Knows D Q q) :
    information D (Q ++ [q]) = information D Q := by
  apply Nat.le_antisymm
  · unfold information classCount
    exact count_le_of_determines (sigList Q) (sigList (Q ++ [q])) D
      (fun a ha b hb hab => sigList_append_eq_of_knows h ha hb hab)
  · exact information_mono (fun q' hq' => List.mem_append_left _ hq')

/-! ## Know, or witness ignorance: a decision procedure -/

/-- The Boolean knowledge test, a list computation over the represented
carrier. -/
def knowsB (D : List Nat) (Q : Institution) (q : Nat → Nat) : Bool :=
  D.all (fun x => D.all (fun y =>
    (!(decide (sigList Q x = sigList Q y))) || decide (q x = q y)))

/-- A failing `all` has a witness, by list recursion: the constructive
form of the library's classical `List.all_eq_false`. -/
theorem all_false_witness {α : Type} (p : α → Bool) :
    ∀ l : List α, l.all p = false → ∃ x, x ∈ l ∧ p x = false := by
  intro l
  induction l with
  | nil => intro h; exact Bool.noConfusion h
  | cons a t ih =>
    intro h
    rw [List.all_cons] at h
    cases hpa : p a with
    | false => exact ⟨a, List.mem_cons_self, hpa⟩
    | true =>
      rw [hpa, Bool.true_and] at h
      obtain ⟨x, hx, hpx⟩ := ih h
      exact ⟨x, List.mem_cons_of_mem a hx, hpx⟩

/-- **Know or witness.**  For every question the institution either knows
it or exhibits two points of `D` it cannot tell apart on which the
question differs.  Decided by `knowsB`; no excluded middle, no choice. -/
theorem know_or_witness (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows D Q q ∨ ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ SigEq Q x y ∧ q x ≠ q y := by
  cases h : knowsB D Q q with
  | true =>
    left
    rw [knows_iff_sigList]
    intro x hx y hy hs
    unfold knowsB at h
    rw [List.all_eq_true] at h
    have h1 := h x hx
    rw [List.all_eq_true] at h1
    have h2 := h1 y hy
    rw [decide_eq_true hs, Bool.not_true, Bool.false_or] at h2
    exact of_decide_eq_true h2
  | false =>
    right
    unfold knowsB at h
    obtain ⟨x, hx, h1⟩ := all_false_witness _ D h
    obtain ⟨y, hy, h2⟩ := all_false_witness _ D h1
    obtain ⟨h3, h4⟩ := Bool.or_eq_false_iff.mp h2
    have h5 : sigList Q x = sigList Q y := by
      cases hd : decide (sigList Q x = sigList Q y) with
      | true => exact of_decide_eq_true hd
      | false => rw [hd] at h3; exact Bool.noConfusion h3
    exact ⟨x, hx, y, hy, (sigEq_iff_sigList Q x y).mpr h5, of_decide_eq_false h4⟩

theorem not_knows_iff_witness (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    ¬ Knows D Q q ↔ ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ SigEq Q x y ∧ q x ≠ q y := by
  constructor
  · intro hn
    rcases know_or_witness D Q q with h | h
    · exact absurd h hn
    · exact h
  · rintro ⟨x, hx, y, hy, hs, hne⟩ hk
    exact hne ((knows_iff_determined D Q q).mp hk x hx y hy hs)

/-- Ignorance is exactly a split of some class under adjoining the
question (Genesis `SplitsAt`). -/
theorem not_knows_iff_split (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    ¬ Knows D Q q ↔ ∃ x, x ∈ D ∧ SplitsAt D Q (Q ++ [q]) x := by
  rw [not_knows_iff_witness]
  constructor
  · rintro ⟨x, hx, y, hy, hs, hne⟩
    exact ⟨x, hx, y, hy, hs, fun h' =>
      hne (h' q (List.mem_append_right _ (List.mem_singleton_self q)))⟩
  · rintro ⟨x, hx, y, hy, hs, hnot⟩
    refine ⟨x, hx, y, hy, hs, ?_⟩
    intro heq
    apply hnot
    intro q' hq'
    rcases List.mem_append.mp hq' with hq' | hq'
    · exact hs q' hq'
    · rw [List.mem_singleton.mp hq']
      exact heq

/-- Ignorance is exactly a strict information increase on learning. -/
theorem information_lt_of_not_knows {D : List Nat} {Q : Institution}
    {q : Nat → Nat} (hn : ¬ Knows D Q q) :
    information D Q < information D (Q ++ [q]) := by
  obtain ⟨x, hx, hs⟩ := (not_knows_iff_split D Q q).mp hn
  exact strict_split_increases D Q (Q ++ [q])
    (fun q' hq' => List.mem_append_left _ hq') x hx hs

/-- **Knowledge is information stationarity.** -/
theorem knows_iff_information_eq (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows D Q q ↔ information D (Q ++ [q]) = information D Q := by
  constructor
  · exact information_append_of_knows
  · intro heq
    rcases know_or_witness D Q q with h | h
    · exact h
    · exfalso
      have hlt := information_lt_of_not_knows
        ((not_knows_iff_witness D Q q).mpr h)
      rw [heq] at hlt
      exact Nat.lt_irrefl _ hlt

/-! ## Knowledge of knowledge adds nothing -/

/-- Adjoining a known question changes what is known of nothing. -/
theorem known_extension_inert {D : List Nat} {Q : Institution} {q : Nat → Nat}
    (h : Knows D Q q) (q' : Nat → Nat) :
    Knows D (Q ++ [q]) q' ↔ Knows D Q q' := by
  constructor
  · intro h'
    rw [knows_iff_sigList] at h' ⊢
    intro x hx y hy hs
    exact h' x hx y hy (sigList_append_eq_of_knows h hx hy hs)
  · exact knows_mono (fun q'' hq'' => List.mem_append_left _ hq'')

/-- The institution adjoining its own actor as a member knows exactly what
it knew. -/
theorem self_inclusion_inert (D : List Nat) (Q : Institution) (q' : Nat → Nat) :
    Knows D (Q ++ [pQ D Q]) q' ↔ Knows D Q q' :=
  known_extension_inert (knows_actor D Q) q'

theorem self_inclusion_information (D : List Nat) (Q : Institution) :
    information D (Q ++ [pQ D Q]) = information D Q :=
  information_append_of_knows (knows_actor D Q)

/-- **The institution is an actor.**  Read as a single presentation, the
institution's actor carries exactly the institution's information. -/
theorem institution_is_actor (D : List Nat) (Q : Institution) :
    classCount D [pQ D Q] = information D Q := by
  apply Nat.le_antisymm
  · exact information_known_le (knows_actor D Q)
  · unfold information classCount
    apply count_le_of_determines (sigList [pQ D Q]) (sigList Q) D
    intro a ha b hb hab
    have hp : pQ D Q a = pQ D Q b := by
      have h' : [pQ D Q a] = [pQ D Q b] := hab
      injection h'
    exact (sigEq_iff_sigList Q a b).mp ((pQ_exact D Q a ha b hb).mp hp)

/-! ## Members against the institution -/

/-- A member observes the whole institution sharply (fiber identity with
the actor) exactly when it alone knows every member: the institution
adds nothing to that member. -/
theorem member_sharp_iff {D : List Nat} {Q : Institution} {q : Nat → Nat}
    (hq : q ∈ Q) :
    PresentationRelativity.FiberIdentityOn D q (pQ D Q) ↔
      ∀ q', q' ∈ Q → Knows D [q] q' := by
  unfold PresentationRelativity.FiberIdentityOn
  constructor
  · intro h q' hq'
    rw [knows_iff_determined]
    intro x hx y hy hs
    have hqxy : q x = q y := hs q (List.mem_singleton_self q)
    exact (pQ_exact D Q x hx y hy).mp ((h x hx y hy).mp hqxy) q' hq'
  · intro h x hx y hy
    constructor
    · intro hqxy
      apply (pQ_exact D Q x hx y hy).mpr
      intro q' hq'
      exact (knows_iff_determined D [q] q').mp (h q' hq') x hx y hy
        (fun q'' hq'' => by rw [List.mem_singleton.mp hq'']; exact hqxy)
    · intro hp
      exact (pQ_exact D Q x hx y hy).mp hp q hq

def parity (x : Nat) : Nat := x % 2
def half (x : Nat) : Nat := x / 2

/-- An institution can exceed each of its members: two two-valued members
that know nothing of each other jointly know the whole carrier. -/
theorem institution_exceeds_members :
    information [0, 1, 2, 3] [parity, half] = 4 ∧
    classCount [0, 1, 2, 3] [parity] = 2 ∧
    classCount [0, 1, 2, 3] [half] = 2 ∧
    ¬ Knows [0, 1, 2, 3] [parity] half ∧
    ¬ Knows [0, 1, 2, 3] [half] parity ∧
    Knows [0, 1, 2, 3] [parity, half] (fun x => x) := by decide

/-- **Sharp observation of an institution is mutual knowledge.**  An
observer is sharp for the institution's actor exactly when the observer's
questions know every member and the institution knows every view. -/
theorem sharp_institution_iff_mutual_knowledge (D : List Nat) (E : Evaluator)
    (Q : Institution) :
    Sharp D E (pQ D Q) ↔
      (∀ q, q ∈ Q → Knows D (questions E) q) ∧
      (∀ c, c ∈ E → Knows D Q (viewQ c)) := by
  rw [sharp_iff_fiberIdentity]
  unfold PresentationRelativity.FiberIdentityOn
  constructor
  · intro h
    constructor
    · intro q hq
      rw [knows_iff_determined]
      intro x hx y hy hs
      have h1 : pQ D (questions E) x = pQ D (questions E) y :=
        (pQ_exact D _ x hx y hy).mpr hs
      exact (pQ_exact D Q x hx y hy).mp ((h x hx y hy).mp h1) q hq
    · intro c hc
      rw [knows_iff_determined]
      intro x hx y hy hs
      have h2 : pQ D Q x = pQ D Q y := (pQ_exact D Q x hx y hy).mpr hs
      exact (pQ_exact D _ x hx y hy).mp ((h x hx y hy).mpr h2) (viewQ c)
        (List.mem_map.mpr ⟨c, hc, rfl⟩)
  · rintro ⟨h1, h2⟩ x hx y hy
    constructor
    · intro hE
      apply (pQ_exact D Q x hx y hy).mpr
      intro q hq
      exact (knows_iff_determined D _ q).mp (h1 q hq) x hx y hy
        ((pQ_exact D _ x hx y hy).mp hE)
    · intro hQ
      apply (pQ_exact D _ x hx y hy).mpr
      intro q' hq'
      obtain ⟨c, hc, rfl⟩ := List.mem_map.mp hq'
      exact (knows_iff_determined D Q (viewQ c)).mp (h2 c hc) x hx y hy
        ((pQ_exact D Q x hx y hy).mp hQ)

/-! ## Pooled against unanimous: an institution of observers -/

/-- The pooled observer of a panel: every view of every member. -/
def pooled (panel : List Evaluator) : Evaluator := panel.flatten

/-- The pooled observer merges exactly the panel's joint quotient. -/
theorem pooled_merges_iff (panel : List Evaluator) (i j : Nat) :
    verdictB (pooled panel) i j = false ↔ NoOutside.PanelEquiv panel i j := by
  rw [verdictB_eq_false_iff]
  unfold NoOutside.PanelEquiv pooled
  constructor
  · intro h E hE c hc
    exact (sepB_eq_false_iff c i j).mp (h c (List.mem_flatten.mpr ⟨E, hE, hc⟩))
  · intro h c hc
    obtain ⟨E, hE, hcE⟩ := List.mem_flatten.mp hc
    exact (sepB_eq_false_iff c i j).mpr (h E hE c hcE)

/-- Pooled non-separation is Genesis's negative certificate. -/
theorem pooled_merges_iff_certNeg {panel : List Evaluator} (hne : panel ≠ [])
    (i j : Nat) : verdictB (pooled panel) i j = false ↔ certNegB panel i j = true := by
  rw [pooled_merges_iff, NoOutside.certNeg_iff_panelEquiv]
  exact ⟨fun h => ⟨hne, h⟩, fun h => h.2⟩

/-- Unanimous separation (the positive certificate) implies pooled
separation. -/
theorem certPos_imp_pooled {panel : List Evaluator} {i j : Nat}
    (h : certPosB panel i j = true) : verdictB (pooled panel) i j = true := by
  obtain ⟨hne, hall⟩ := (cert_scope panel i j).mp h
  cases panel with
  | nil => exact absurd rfl hne
  | cons E rest =>
    obtain ⟨c, hc, hsep⟩ := hall E List.mem_cons_self
    unfold verdictB pooled
    rw [List.any_eq_true]
    exact ⟨c, List.mem_flatten.mpr ⟨E, List.mem_cons_self, hc⟩, hsep⟩

/-- Pooled separation does not imply unanimous separation: the pool of
Genesis's `cert_panel_relative` panel separates `0` from `1`, the panel
does not certify it. -/
theorem pooled_not_certPos :
    verdictB (pooled [[[0]], [[0, 1]]]) 0 1 = true ∧
      certPosB [[[0]], [[0, 1]]] 0 1 = false := by decide

/-! ## Information is bounded by resolution -/

/-- The class list of a family on `D`. -/
def classes (D : List Nat) (Q : Institution) : List (List Nat) :=
  dedupL (D.map (sigList Q))

theorem classes_length (D : List Nat) (Q : Institution) :
    (classes D Q).length = information D Q := rfl

theorem mem_classes (D : List Nat) (Q : Institution) (s : List Nat) :
    s ∈ classes D Q ↔ ∃ x, x ∈ D ∧ sigList Q x = s := by
  unfold classes
  rw [mem_dedupL, List.mem_map]

/-- An institution of `m` views (Boolean questions) has at most `2 ^ m`
information on any carrier: the information side of Theorem I's
resolution bound. -/
theorem information_le_resolution (D : List Nat) (E : Evaluator) :
    information D (questions E) ≤ 2 ^ E.length := by
  rw [← classes_length]
  apply Nat.le_of_not_lt
  intro hlt
  have hmem : ∀ p, p < (classes D (questions E)).length →
      ∃ x, x ∈ D ∧ (classes D (questions E)).getD p [] = sigList (questions E) x := by
    intro p hp
    obtain ⟨x, hx, hxs⟩ := (mem_classes D (questions E) _).mp (getD_mem [] _ p hp)
    exact ⟨x, hx, hxs.symm⟩
  obtain ⟨s, hs, t, ht, hst, heq⟩ :=
    Pigeonhole.pigeonhole (2 ^ E.length)
      (fun p => CapacityBound.encode 2 ((classes D (questions E)).getD p []))
      (fun p hp => by
        obtain ⟨x, _, hxs⟩ := hmem p (Nat.lt_of_lt_of_le hp hlt)
        show CapacityBound.encode 2 ((classes D (questions E)).getD p []) < 2 ^ E.length
        rw [hxs]
        exact sigCode_lt E x)
  apply hst
  apply nodup_getD_inj [] (classes D (questions E)) (dedupL_nodup _) s t
    (Nat.lt_of_lt_of_le hs hlt) (Nat.lt_of_lt_of_le ht hlt)
  obtain ⟨x, _, hxs⟩ := hmem s (Nat.lt_of_lt_of_le hs hlt)
  obtain ⟨y, _, hys⟩ := hmem t (Nat.lt_of_lt_of_le ht hlt)
  have heq' : CapacityBound.encode 2 (sigList (questions E) x) =
      CapacityBound.encode 2 (sigList (questions E) y) := by
    have h0 := heq
    simp only [hxs, hys] at h0
    exact h0
  rw [hxs, hys]
  exact CapacityBound.encode_inj 2 _ _
    (by rw [sigList_questions_length, sigList_questions_length])
    (sigList_questions_bounded E x) (sigList_questions_bounded E y) heq'

/-! ## Wisdom at the question level -/

/-- DECLARED reading of wisdom: for every question, the institution either
knows it or holds a represented witness of its ignorance. -/
def Wise (D : List Nat) (Q : Institution) : Prop :=
  ∀ q : Nat → Nat,
    Knows D Q q ∨ ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ SigEq Q x y ∧ q x ≠ q y

/-- Every institution on a represented carrier is wise at the question
level, by the decision procedure `knowsB`. -/
theorem wise_of_represented (D : List Nat) (Q : Institution) : Wise D Q :=
  fun q => know_or_witness D Q q

end Institution
end ResearchTwoTheorems
