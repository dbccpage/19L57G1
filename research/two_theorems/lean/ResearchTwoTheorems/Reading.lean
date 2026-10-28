import ResearchTwoTheorems.Observer
import ResearchTwoTheorems.Institution

/-!
# Reading the author's statements of 2026-10-28

AuthorityEffect: None.

The author's brief was cut off before its theorem statements.  On
2026-10-28 he stated, in prose, what the two theorems are to say.  This
module reads those statements against the tree and adds the small theorems
each needs; every reading is declared in `CLAIMS.md` and marked as a
reading, not as his statement.  Everything here is relative to a finite
carrier `D` and finite families; nothing ranges over an infinite object
except where a universal over the metatheory's function type is explicitly
reduced to a finite one (`knows_iff_knows_pQ`).

1. **Knowledge gain requires refinement.**
   `knowledge_gain_requires_refinement` (named `extension_forced` until
   2026-10-28; renamed after review, since it compels nothing): a family
   that does not know a question can come to know it only by a strictly
   more informative family; `finder_separates`: whatever finds the pattern
   separates two data the family merges.  Whether a family *must* extend
   is not decided here; it may hold the residual (item 3).
2. **An observer cannot read another's resolution.**
   `observer_cannot_read_resolution`: wherever an observer merges two data,
   two actors agree with every separation it reports, one merging the pair
   and one splitting it.
3. **Held residuals.**  `residuals`: the pairs a family cannot tell apart on
   which a question differs; empty exactly when the question is known; only
   ever shrunk by listening.
4. **Nesting.**  `nest_inert`, `nest_information`: a sub-family nested as one
   member (its joint presentation, a compressed presentation) is the same
   institution; `participation_collapse`: a family whose members add nothing
   to one member has that member's information.
5. **Finitude.**  `knows_congr`, `knows_member_congr`: only values on `D`
   matter; `pQ_mem`, `knows_iff_knows_pQ`: knowledge of a question is
   knowledge of its representative, a table `D → D`, so the question space
   that matters is finite.
6. **Grounded reports.**  `Grounded D Q s := Knows D Q s`: a self-report
   that claims no distinction the questions cannot make.  This is the tree's
   provisional reading of the author's "not deceiving oneself"; it was named
   `Honest` until 2026-10-28 and renamed after review, since it says nothing
   of truth beyond the admitted questions.  Silence is grounded, the actor's
   own presentation is grounded and every grounded report factors through
   it, listening never makes a grounded report ungrounded, a larger carrier
   can (`grounded_here_not_there`), and the same report is grounded for one
   institution and ungrounded for another (`reports_do_not_certify`).
7. **A guess and who sees it.**  `Guess D p s := ¬ Knows D [p] s`: a report
   not determined by the member's own question.  The member never locates it
   (`own_guess_invisible`); the family locates it exactly when another member
   separates the pair (`guess_visible_iff`); a family that merges the pair
   and endorses the report holds an ungrounded report too (`shared_guess`).
-/

namespace ResearchTwoTheorems
namespace Reading

open Represented Compression PresentationRelativity Institution

/-! ## 1. Knowledge gain requires refinement -/

/-- **Knowledge gain requires refinement.**  If the family does not know
`q`, every larger family that knows `q` splits a pair the first merged, so
its information is strictly larger.  Learning the hidden pattern is never
free and never internal to the family that missed it.  The theorem compels
nothing: it assumes the larger family and prices it; it does not say the
family must extend. -/
theorem knowledge_gain_requires_refinement {D : List Nat} {Q Q' : Institution} {q : Nat → Nat}
    (hsub : ∀ p, p ∈ Q → p ∈ Q') (hn : ¬ Knows D Q q) (hk : Knows D Q' q) :
    information D Q < information D Q' := by
  obtain ⟨x, hx, y, hy, hs, hne⟩ := (not_knows_iff_witness D Q q).mp hn
  have hns : ¬ SigEq Q' x y := fun hs' =>
    hne ((knows_iff_determined D Q' q).mp hk x hx y hy hs')
  show classCount D Q < classCount D Q'
  exact strict_split_increases D Q Q' hsub x hx ⟨y, hy, hs, hns⟩

/-- What the family does not know, no member knows. -/
theorem member_ignorant_of_family {D : List Nat} {Q : Institution}
    {q : Nat → Nat} (hn : ¬ Knows D Q q) {p : Nat → Nat} (hp : p ∈ Q) :
    ¬ Knows D [p] q :=
  fun h => hn (knows_mono (fun p' hp' => by
    rw [List.mem_singleton.mp hp']; exact hp) h)

/-- Whatever knows the pattern the family misses separates two data the
family merges: the finder sees past the family. -/
theorem finder_separates {D : List Nat} {Q : Institution} {q f : Nat → Nat}
    (hn : ¬ Knows D Q q) (hf : Knows D [f] q) :
    ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ SigEq Q x y ∧ f x ≠ f y := by
  obtain ⟨x, hx, y, hy, hs, hne⟩ := (not_knows_iff_witness D Q q).mp hn
  refine ⟨x, hx, y, hy, hs, fun hfe => hne ?_⟩
  exact (knows_iff_determined D [f] q).mp hf x hx y hy
    (fun p hp => by rw [List.mem_singleton.mp hp]; exact hfe)

/-! ## 2. An observer cannot read another's resolution -/

/-- An observer agrees with an actor when every separation it reports is a
separation of the actor: it claims no distinction the actor lacks. -/
def Consistent (D : List Nat) (E : Evaluator) (p : Nat → Nat) : Prop :=
  ∀ x, x ∈ D → ∀ y, y ∈ D → verdictB E x y = true → p x ≠ p y

/-- The observer's own joint presentation agrees with it. -/
theorem actor_consistent (D : List Nat) (E : Evaluator) :
    Consistent D E (pQ D (questions E)) := by
  intro x hx y hy hv hp
  have hs := (pQ_exact D (questions E) x hx y hy).mp hp
  have hf := (verdictB_false_iff_sigEq E x y).mpr hs
  rw [hf] at hv
  exact Bool.noConfusion hv

/-- A sharply observed actor agrees with its observer. -/
theorem sharp_consistent {D : List Nat} {E : Evaluator} {p : Nat → Nat}
    (h : Sharp D E p) : Consistent D E p := by
  intro x hx y hy hv hp
  have hf := (h x hx y hy).mpr hp
  rw [hf] at hv
  exact Bool.noConfusion hv

/-- `p` with one point marked: the fibers of `p` with the fiber of `x`
split off. -/
def markOne (p : Nat → Nat) (x : Nat) : Nat → Nat :=
  fun z => 2 * p z + (if z = x then 1 else 0)

theorem markOne_eq {p : Nat → Nat} {x a b : Nat}
    (h : markOne p x a = markOne p x b) : p a = p b := by
  unfold markOne at h
  by_cases ha : a = x <;> by_cases hb : b = x
  · rw [if_pos ha, if_pos hb] at h; omega
  · rw [if_pos ha, if_neg hb] at h; omega
  · rw [if_neg ha, if_pos hb] at h; omega
  · rw [if_neg ha, if_neg hb] at h; omega

theorem markOne_separates {p : Nat → Nat} {x y : Nat} (hxy : x ≠ y)
    (hp : p x = p y) : markOne p x x ≠ markOne p x y := by
  unfold markOne
  rw [if_pos rfl, if_neg (Ne.symm hxy)]
  omega

theorem markOne_consistent (D : List Nat) (E : Evaluator) (x : Nat) :
    Consistent D E (markOne (pQ D (questions E)) x) :=
  fun a ha b hb hv h => actor_consistent D E a ha b hb hv (markOne_eq h)

/-- **An observer cannot read an actor's resolution.**  Wherever the
observer merges two distinct data, two actors agree with every separation it
reports, one merging the pair and one splitting it; its verdicts cannot tell
which one it is watching. -/
theorem observer_cannot_read_resolution (D : List Nat) (E : Evaluator)
    {x y : Nat} (hx : x ∈ D) (hy : y ∈ D) (hxy : x ≠ y)
    (hv : verdictB E x y = false) :
    ∃ p₀ p₁ : Nat → Nat, Consistent D E p₀ ∧ Consistent D E p₁ ∧
      p₀ x = p₀ y ∧ p₁ x ≠ p₁ y := by
  have hm : pQ D (questions E) x = pQ D (questions E) y :=
    (pQ_exact D (questions E) x hx y hy).mpr
      ((verdictB_false_iff_sigEq E x y).mp hv)
  exact ⟨pQ D (questions E), markOne (pQ D (questions E)) x,
    actor_consistent D E, markOne_consistent D E x, hm, markOne_separates hxy hm⟩

/-! ## 3. Held residuals -/

/-- All ordered pairs drawn from two lists, by recursion. -/
def pairs : List Nat → List Nat → List (Nat × Nat)
  | [], _ => []
  | x :: t, ys => ys.map (fun y => (x, y)) ++ pairs t ys

theorem mem_pairs (xs ys : List Nat) (x y : Nat) :
    (x, y) ∈ pairs xs ys ↔ x ∈ xs ∧ y ∈ ys := by
  induction xs with
  | nil => exact ⟨(fun h => nomatch h), (fun h => nomatch h.1)⟩
  | cons a t ih =>
    unfold pairs
    rw [List.mem_append, List.mem_map, ih, List.mem_cons]
    constructor
    · rintro (⟨y', hy', hpair⟩ | ⟨hx, hy⟩)
      · have h1 : a = x := congrArg Prod.fst hpair
        have h2 : y' = y := congrArg Prod.snd hpair
        exact ⟨Or.inl h1.symm, h2 ▸ hy'⟩
      · exact ⟨Or.inr hx, hy⟩
    · rintro ⟨hx | hx, hy⟩
      · exact Or.inl ⟨y, hy, by rw [hx]⟩
      · exact Or.inr ⟨hx, hy⟩

/-- The residuals of a question: the pairs of `D` the family cannot tell
apart on which the question differs.  A record kept, not a verdict. -/
def residuals (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    List (Nat × Nat) :=
  (pairs D D).filter (fun xy =>
    decide (sigList Q xy.1 = sigList Q xy.2) && decide (q xy.1 ≠ q xy.2))

theorem mem_residuals (D : List Nat) (Q : Institution) (q : Nat → Nat)
    (x y : Nat) :
    (x, y) ∈ residuals D Q q ↔ x ∈ D ∧ y ∈ D ∧ SigEq Q x y ∧ q x ≠ q y := by
  unfold residuals
  rw [List.mem_filter, mem_pairs]
  simp only [Bool.and_eq_true, decide_eq_true_eq]
  rw [sigEq_iff_sigList]
  constructor
  · rintro ⟨⟨hx, hy⟩, hs, hne⟩; exact ⟨hx, hy, hs, hne⟩
  · rintro ⟨hx, hy, hs, hne⟩; exact ⟨⟨hx, hy⟩, hs, hne⟩

/-- **Held residuals are empty exactly when the question is known.** -/
theorem residuals_nil_iff (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    residuals D Q q = [] ↔ Knows D Q q := by
  rw [knows_iff_determined]
  constructor
  · intro h x hx y hy hs
    cases Nat.decEq (q x) (q y) with
    | isTrue he => exact he
    | isFalse hne =>
      exfalso
      have hm : (x, y) ∈ residuals D Q q :=
        (mem_residuals D Q q x y).mpr ⟨hx, hy, hs, hne⟩
      rw [h] at hm
      exact nomatch hm
  · intro h
    cases hr : residuals D Q q with
    | nil => rfl
    | cons xy t =>
      exfalso
      have hm : xy ∈ residuals D Q q := by
        rw [hr]; exact List.mem_cons_self
      obtain ⟨hx, hy, hs, hne⟩ := (mem_residuals D Q q xy.1 xy.2).mp hm
      exact hne (h xy.1 hx xy.2 hy hs)

/-- **Listening only shrinks the residuals.**  A larger family holds no
residual the smaller one did not. -/
theorem residuals_antitone {D : List Nat} {Q Q' : Institution}
    (hsub : ∀ p, p ∈ Q → p ∈ Q') (q : Nat → Nat) :
    ∀ xy, xy ∈ residuals D Q' q → xy ∈ residuals D Q q := by
  rintro ⟨x, y⟩ h
  rw [mem_residuals] at h ⊢
  obtain ⟨hx, hy, hs, hne⟩ := h
  exact ⟨hx, hy, enlarge_refines Q Q' hsub x y hs, hne⟩

/-- A residual leaves exactly when some question splits its pair; no verdict
removes it. -/
theorem residual_removed_iff {D : List Nat} {Q Q' : Institution}
    {q : Nat → Nat} {x y : Nat} (h : (x, y) ∈ residuals D Q q) :
    (x, y) ∉ residuals D Q' q ↔ ¬ SigEq Q' x y := by
  rw [mem_residuals] at h ⊢
  obtain ⟨hx, hy, _, hne⟩ := h
  constructor
  · intro hn hs'; exact hn ⟨hx, hy, hs', hne⟩
  · rintro hns ⟨_, _, hs', _⟩; exact hns hs'

/-! ## 4. Nesting -/

theorem nest_sigEq (D : List Nat) (Q' Q : Institution) {x y : Nat}
    (hx : x ∈ D) (hy : y ∈ D) :
    SigEq (pQ D Q' :: Q) x y ↔ SigEq (Q' ++ Q) x y := by
  constructor
  · intro h p hp
    rcases List.mem_append.mp hp with hp | hp
    · exact (pQ_exact D Q' x hx y hy).mp (h (pQ D Q') List.mem_cons_self) p hp
    · exact h p (List.mem_cons_of_mem _ hp)
  · intro h p hp
    rcases List.mem_cons.mp hp with hp | hp
    · rw [hp]
      exact (pQ_exact D Q' x hx y hy).mpr
        (fun p' hp' => h p' (List.mem_append_left _ hp'))
    · exact h p (List.mem_append_right _ hp)

/-- **A family nested as one member is the same institution.**  The joint
presentation of a sub-family, nested as a single member (a compressed
presentation), knows exactly what the flat family knows. -/
theorem nest_inert (D : List Nat) (Q' Q : Institution) (q : Nat → Nat) :
    Knows D (pQ D Q' :: Q) q ↔ Knows D (Q' ++ Q) q := by
  rw [knows_iff_determined, knows_iff_determined]
  constructor
  · intro h x hx y hy hs; exact h x hx y hy ((nest_sigEq D Q' Q hx hy).mpr hs)
  · intro h x hx y hy hs; exact h x hx y hy ((nest_sigEq D Q' Q hx hy).mp hs)

theorem nest_information (D : List Nat) (Q' Q : Institution) :
    information D (pQ D Q' :: Q) = information D (Q' ++ Q) := by
  apply Nat.le_antisymm
  · unfold information classCount
    apply count_le_of_determines (sigList (Q' ++ Q)) (sigList (pQ D Q' :: Q)) D
    intro a ha b hb hab
    exact (sigEq_iff_sigList _ a b).mp
      ((nest_sigEq D Q' Q ha hb).mpr ((sigEq_iff_sigList _ a b).mpr hab))
  · unfold information classCount
    apply count_le_of_determines (sigList (pQ D Q' :: Q)) (sigList (Q' ++ Q)) D
    intro a ha b hb hab
    exact (sigEq_iff_sigList _ a b).mp
      ((nest_sigEq D Q' Q ha hb).mp ((sigEq_iff_sigList _ a b).mpr hab))

/-- **Participation collapse.**  When one member knows every member, the
family's information is that member's: the others contribute nothing. -/
theorem participation_collapse {D : List Nat} {Q : Institution}
    {p : Nat → Nat} (hp : p ∈ Q) (h : ∀ q, q ∈ Q → Knows D [p] q) :
    information D Q = classCount D [p] := by
  apply Nat.le_antisymm
  · unfold information classCount
    apply count_le_of_determines (sigList [p]) (sigList Q) D
    intro a ha b hb hab
    apply (sigEq_iff_sigList Q a b).mp
    intro q hq
    exact (knows_iff_sigList D [p] q).mp (h q hq) a ha b hb hab
  · exact information_member_le hp

/-! ## 5. Finitude: only values on `D` matter, and the question space is
finite -/

theorem knows_congr {D : List Nat} {Q : Institution} {q q' : Nat → Nat}
    (h : ∀ x, x ∈ D → q x = q' x) : Knows D Q q ↔ Knows D Q q' := by
  rw [knows_iff_determined, knows_iff_determined]
  constructor
  · intro hk x hx y hy hs; rw [← h x hx, ← h y hy]; exact hk x hx y hy hs
  · intro hk x hx y hy hs; rw [h x hx, h y hy]; exact hk x hx y hy hs

theorem knows_member_congr {D : List Nat} {Q : Institution} {p p' : Nat → Nat}
    (h : ∀ x, x ∈ D → p x = p' x) (q : Nat → Nat) :
    Knows D (p :: Q) q ↔ Knows D (p' :: Q) q := by
  rw [knows_iff_determined, knows_iff_determined]
  have key : ∀ x, x ∈ D → ∀ y, y ∈ D →
      (SigEq (p :: Q) x y ↔ SigEq (p' :: Q) x y) := by
    intro x hx y hy
    constructor
    · intro hs r hr
      rcases List.mem_cons.mp hr with hr | hr
      · rw [hr, ← h x hx, ← h y hy]; exact hs p List.mem_cons_self
      · exact hs r (List.mem_cons_of_mem _ hr)
    · intro hs r hr
      rcases List.mem_cons.mp hr with hr | hr
      · rw [hr, h x hx, h y hy]; exact hs p' List.mem_cons_self
      · exact hs r (List.mem_cons_of_mem _ hr)
  constructor
  · intro hk x hx y hy hs; exact hk x hx y hy ((key x hx y hy).mpr hs)
  · intro hk x hx y hy hs; exact hk x hx y hy ((key x hx y hy).mp hs)

/-- The representative of a question on `D` takes its values in `D`. -/
theorem pQ_mem (D : List Nat) (Q : Institution) {x : Nat} (hx : x ∈ D) :
    pQ D Q x ∈ D :=
  (pQ_spec D Q x hx).1

/-- **The question space is finite.**  Knowledge of `q` is knowledge of its
representative `pQ D [q]`, a table from `D` into `D`; there are finitely many
such tables, so quantifying over all questions quantifies over them. -/
theorem knows_iff_knows_pQ (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows D Q q ↔ Knows D Q (pQ D [q]) := by
  rw [knows_iff_determined, knows_iff_determined]
  constructor
  · intro h x hx y hy hs
    exact (pQ_exact D [q] x hx y hy).mpr
      (fun r hr => by rw [List.mem_singleton.mp hr]; exact h x hx y hy hs)
  · intro h x hx y hy hs
    exact (pQ_exact D [q] x hx y hy).mp (h x hx y hy hs) q
      (List.mem_singleton_self q)

/-! ## 6. Grounded reports -/

/-- A self-report `s` of the institution is **grounded** when the
institution knows it: the report claims no distinction the questions cannot
make.  Under-claiming (merging what the questions separate) is permitted:
that is demurral.  Grounding is relative to the admitted questions and the
carrier; it is not truth, honesty or wisdom (provisional vocabulary). -/
def Grounded (D : List Nat) (Q : Institution) (s : Nat → Nat) : Prop :=
  Knows D Q s

theorem grounded_iff_no_overclaim (D : List Nat) (Q : Institution)
    (s : Nat → Nat) :
    Grounded D Q s ↔
      ∀ x, x ∈ D → ∀ y, y ∈ D → s x ≠ s y → ¬ SigEq Q x y := by
  unfold Grounded
  rw [knows_iff_determined]
  constructor
  · intro h x hx y hy hne hs; exact hne (h x hx y hy hs)
  · intro h x hx y hy hs
    cases Nat.decEq (s x) (s y) with
    | isTrue he => exact he
    | isFalse hne => exact absurd hs (h x hx y hy hne)

/-- **An ungrounded report has a witness**: two data the questions cannot
tell apart on which the report differs. -/
theorem ungrounded_iff_witness (D : List Nat) (Q : Institution)
    (s : Nat → Nat) :
    ¬ Grounded D Q s ↔ ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ SigEq Q x y ∧ s x ≠ s y :=
  not_knows_iff_witness D Q s

/-- Silence is grounded: a report that claims nothing over-claims nothing. -/
theorem silence_grounded (D : List Nat) (Q : Institution) (c : Nat) :
    Grounded D Q (fun _ => c) :=
  knows_const D Q c

/-- Reporting one's own presentation is grounded; by definition every
grounded report factors through it. -/
theorem self_report_grounded (D : List Nat) (Q : Institution) :
    Grounded D Q (pQ D Q) :=
  knows_actor D Q

/-- Reporting a member's answers is grounded. -/
theorem member_report_grounded {D : List Nat} {Q : Institution} {p : Nat → Nat}
    (hp : p ∈ Q) : Grounded D Q p :=
  knows_member hp

/-- Listening more never makes a grounded report ungrounded. -/
theorem grounded_mono {D : List Nat} {Q Q' : Institution} {s : Nat → Nat}
    (hsub : ∀ p, p ∈ Q → p ∈ Q') (h : Grounded D Q s) : Grounded D Q' s :=
  knows_mono hsub h

/-- Grounded on a larger carrier, grounded on a smaller one; not conversely
(`grounded_here_not_there`). -/
theorem grounded_antitone_carrier {D D' : List Nat} {Q : Institution}
    {s : Nat → Nat} (hsub : ∀ x, x ∈ D → x ∈ D') (h : Grounded D' Q s) :
    Grounded D Q s := by
  unfold Grounded at h ⊢
  rw [knows_iff_determined] at h ⊢
  intro x hx y hy hs
  exact h x (hsub x hx) y (hsub y hy) hs

/-- The Boolean knowledge test decides knowledge. -/
theorem knows_iff_knowsB (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows D Q q ↔ knowsB D Q q = true := by
  constructor
  · intro hk
    cases h : knowsB D Q q with
    | true => rfl
    | false =>
      exfalso
      unfold knowsB at h
      obtain ⟨x, hx, h1⟩ := all_false_witness _ D h
      obtain ⟨y, hy, h2⟩ := all_false_witness _ D h1
      obtain ⟨h3, h4⟩ := Bool.or_eq_false_iff.mp h2
      have h5 : sigList Q x = sigList Q y := by
        cases hd : decide (sigList Q x = sigList Q y) with
        | true => exact of_decide_eq_true hd
        | false => rw [hd] at h3; exact Bool.noConfusion h3
      exact of_decide_eq_false h4
        ((knows_iff_sigList D Q q).mp hk x hx y hy h5)
  · intro h
    rw [knows_iff_sigList]
    intro x hx y hy hs
    unfold knowsB at h
    rw [List.all_eq_true] at h
    have h1 := h x hx
    rw [List.all_eq_true] at h1
    have h2 := h1 y hy
    rw [decide_eq_true hs, Bool.not_true, Bool.false_or] at h2
    exact of_decide_eq_true h2

/-- Grounding of a given report is decided from the questions and the
report, by a list computation: an auditor holding both can certify it. -/
def groundedB (D : List Nat) (Q : Institution) (s : Nat → Nat) : Bool :=
  knowsB D Q s

theorem grounded_iff_groundedB (D : List Nat) (Q : Institution) (s : Nat → Nat) :
    Grounded D Q s ↔ groundedB D Q s = true :=
  knows_iff_knowsB D Q s

/-- For every question a grounded answer exists: report it, or demur with
the witness pair. -/
theorem grounded_or_demur (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Grounded D Q q ∨ ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ SigEq Q x y ∧ q x ≠ q y :=
  know_or_witness D Q q

/-- **Reports alone certify nothing.**  The same report is grounded for one
institution and ungrounded for another; certification is relative to the
presented questions. -/
theorem reports_do_not_certify :
    Grounded [0, 1] [fun x => x] (fun x => x) ∧
    ¬ Grounded [0, 1] [] (fun x => x) := by
  unfold Grounded
  decide

/-- **Grounding is never certified ahead of the carrier.**  A report
grounded on `[0, 1]` is ungrounded once `2` is admitted. -/
theorem grounded_here_not_there :
    Grounded [0, 1] [fun x => x % 2] (fun x => x) ∧
    ¬ Grounded [0, 1, 2] [fun x => x % 2] (fun x => x) := by
  unfold Grounded
  decide

/-! ## 7. A guess, and who sees it -/

/-- A member's report that its own question does not determine: a guess.
The report carries what the member did not observe. -/
def Guess (D : List Nat) (p s : Nat → Nat) : Prop := ¬ Knows D [p] s

theorem guess_iff_witness (D : List Nat) (p s : Nat → Nat) :
    Guess D p s ↔ ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ p x = p y ∧ s x ≠ s y := by
  unfold Guess
  rw [not_knows_iff_witness]
  constructor
  · rintro ⟨x, hx, y, hy, hs, hne⟩
    exact ⟨x, hx, y, hy, hs p (List.mem_singleton_self p), hne⟩
  · rintro ⟨x, hx, y, hy, hp, hne⟩
    exact ⟨x, hx, y, hy,
      fun r hr => by rw [List.mem_singleton.mp hr]; exact hp, hne⟩

/-- **The member never locates its own guess.**  Whatever it computes from
its own question agrees on the pair the guess splits. -/
theorem own_guess_invisible {D : List Nat} {p : Nat → Nat} {x y : Nat}
    (hx : x ∈ D) (hy : y ∈ D) (hp : p x = p y) (e : Nat → Nat)
    (he : Knows D [p] e) : e x = e y :=
  (knows_iff_determined D [p] e).mp he x hx y hy
    (fun r hr => by rw [List.mem_singleton.mp hr]; exact hp)

/-- A family that does not agree on a pair has a member that splits it, by
list computation. -/
theorem not_sigEq_witness {Q : Institution} {x y : Nat} (h : ¬ SigEq Q x y) :
    ∃ r, r ∈ Q ∧ r x ≠ r y := by
  cases hall : Q.all (fun r => decide (r x = r y)) with
  | true =>
    exfalso
    apply h
    intro r hr
    rw [List.all_eq_true] at hall
    exact of_decide_eq_true (hall r hr)
  | false =>
    obtain ⟨r, hr, hd⟩ := all_false_witness _ Q hall
    exact ⟨r, hr, of_decide_eq_false hd⟩

/-- **The family locates a member's guess exactly when another member splits
the pair.**  Stepping back needs a second presentation. -/
theorem guess_visible_iff {Q : Institution} {p : Nat → Nat} {x y : Nat}
    (hpxy : p x = p y) :
    ¬ SigEq Q x y ↔ ∃ r, r ∈ Q ∧ r ≠ p ∧ r x ≠ r y := by
  constructor
  · intro h
    obtain ⟨r, hr, hne⟩ := not_sigEq_witness h
    exact ⟨r, hr, fun hrp => hne (by rw [hrp]; exact hpxy), hne⟩
  · rintro ⟨r, hr, _, hne⟩ hs
    exact hne (hs r hr)

/-- **A shared guess.**  If no member splits the pair, a family endorsing the
report is ungrounded too: nobody steps back. -/
theorem shared_guess {D : List Nat} {Q : Institution} {s : Nat → Nat}
    {x y : Nat} (hx : x ∈ D) (hy : y ∈ D) (hs : SigEq Q x y)
    (hne : s x ≠ s y) : ¬ Grounded D Q s :=
  (ungrounded_iff_witness D Q s).mpr ⟨x, hx, y, hy, hs, hne⟩

/-- Witness on four points: `half` guesses the identity, the family with
`parity` checks it and holds it grounded, the family of `half` alone shares
the guess. -/
theorem guess_witness :
    Guess [0, 1, 2, 3] half (fun x => x) ∧
    Grounded [0, 1, 2, 3] [half, parity] (fun x => x) ∧
    ¬ Grounded [0, 1, 2, 3] [half] (fun x => x) := by
  unfold Guess Grounded
  decide

end Reading
end ResearchTwoTheorems
