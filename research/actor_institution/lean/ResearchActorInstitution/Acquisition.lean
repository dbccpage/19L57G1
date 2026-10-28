import Derivation.Counting
import Derivation.Represented
import ResearchTwoTheorems.Institution
import ResearchTwoTheorems.Observer
import ResearchTwoTheorems.Sufficiency

/-!
# Acquiring a presentation by probes

The two-theorems tree separated *representing* a distinction (an evaluator
sharp for an actor exists: `sharpObserver_sharp`) from *acquiring* one, and
left the cost of acquisition as the conjecture TT-43o.  This module fixes the
cost model and proves the first conjecture, refutes nothing it stated, and
proves the transcript theorem TT-39o.

**Cost model.**  An actor is a presentation `p : Nat → Nat` on the carrier
`List.range n`.  A *probe* asks whether `p x = p y` and costs one.  A
*protocol* chooses the next probe from the transcript so far, or stops; it
is adaptive.  Acquisition *succeeds* when the evaluator an admission rule
builds from the transcript is sharp for the actor (TT's `Sharp`).  Nothing
here lets the actor or the protocol see `p` except through probes.

* `run`, `Consistent`, `run_consistent`, `run_congr`: the machinery.  Two
  actors that answer every asked probe alike produce the same transcript.
* `lower_bound`: if the identity actor's transcript has fewer than
  `n(n−1)/2` entries, some pair `x < y < n` was never probed, and the actor
  `merge x y` (which identifies exactly that pair) produces the same
  transcript.  `no_acquisition_below_bound`: whatever the admission rule, one
  of the two actors is then not sharply presented.  `no_acquisition_in_fewer_steps`
  states it for a step budget `k < n(n−1)/2`.
* `table_sharp`, `complete_table_acquires`: the complete table of all
  `n(n−1)/2` probes, read into one view per datum, is sharp for every actor.
  So the least worst-case number of probes is exactly `n(n−1)/2`
  (`acquisition_cost_exact`), which is TT-43o (i).
* `log_views`: once acquired, the two-theorems bound on views applies: a
  sharp evaluator with `⌈log₂ k⌉` views, `k` the number of classes, is
  computable from the transcript alone (`pQ` of the table's questions).
* `transcripts_identical_capabilities_differ` (TT-39o): below the bound two
  actors of different capability have identical transcripts.
* `complete_evaluator_for_two`: the retained counterexample — for the fixed
  family `{id, merge 0 1}` on two data, one probe and a two-case rule acquire
  every member.  Completeness relative to a fixed finite family is cheap;
  the bound is about every actor on the carrier.
* `acquires_implies_fixes`: an evaluator sharp for every actor consistent
  with a transcript forces all those actors to share one partition
  (TT-43o (iv), the necessity half).  The constructive converse — an
  evaluator computed from an arbitrary partition-fixing transcript — is left
  OPEN in the ledger.

Quantifiers over `Nat`, lists and functions are metatheory.  A protocol is
not an observer the system admitted; it is the external caller of the seed,
probing.  AuthorityEffect: None.
-/

namespace ResearchActorInstitution
namespace Acquisition

open Compression Represented Derivation ResearchTwoTheorems
open ResearchTwoTheorems.Institution ResearchTwoTheorems.Sufficiency

/-- A transcript: the probed pairs with their answers. -/
abbrev Transcript := List (Nat × Nat × Bool)

/-- A protocol: from the transcript so far, the next pair to probe, or stop. -/
abbrev Protocol := Transcript → Option (Nat × Nat)

/-- The transcript entry recording the actor's answer on a pair. -/
def entry (p : Nat → Nat) (pr : Nat × Nat) : Nat × Nat × Bool :=
  (pr.1, pr.2, decide (p pr.1 = p pr.2))

/-- Run a protocol against an actor for at most `k` steps. -/
def run (π : Protocol) (p : Nat → Nat) : Nat → Transcript
  | 0 => []
  | k + 1 =>
    match π (run π p k) with
    | none => run π p k
    | some pr => run π p k ++ [entry p pr]

theorem run_succ_none {π : Protocol} {p : Nat → Nat} {k : Nat}
    (h : π (run π p k) = none) : run π p (k + 1) = run π p k := by
  simp only [run, h]

theorem run_succ_some {π : Protocol} {p : Nat → Nat} {k : Nat} {pr : Nat × Nat}
    (h : π (run π p k) = some pr) : run π p (k + 1) = run π p k ++ [entry p pr] := by
  simp only [run, h]

theorem run_mono (π : Protocol) (p : Nat → Nat) (k : Nat) (e : Nat × Nat × Bool)
    (he : e ∈ run π p k) : e ∈ run π p (k + 1) := by
  cases hπ : π (run π p k) with
  | none => rw [run_succ_none hπ]; exact he
  | some pr => rw [run_succ_some hπ]; exact List.mem_append_left _ he

/-- A transcript has at most one entry per step. -/
theorem run_length_le (π : Protocol) (p : Nat → Nat) : ∀ k, (run π p k).length ≤ k := by
  intro k
  induction k with
  | zero => exact Nat.le_refl _
  | succ k ih =>
    cases hπ : π (run π p k) with
    | none => rw [run_succ_none hπ]; omega
    | some pr =>
      rw [run_succ_some hπ, List.length_append, List.length_singleton]
      omega

/-- The actor `p` answers every entry of `T` as recorded. -/
def Consistent (T : Transcript) (p : Nat → Nat) : Prop :=
  ∀ e, e ∈ T → decide (p e.1 = p e.2.1) = e.2.2

theorem run_consistent (π : Protocol) (p : Nat → Nat) : ∀ k, Consistent (run π p k) p := by
  intro k
  induction k with
  | zero => intro e he; cases he
  | succ k ih =>
    intro e he
    cases hπ : π (run π p k) with
    | none => rw [run_succ_none hπ] at he; exact ih e he
    | some pr =>
      rw [run_succ_some hπ] at he
      rcases List.mem_append.mp he with he | he
      · exact ih e he
      · rw [List.mem_singleton.mp he]; rfl

/-- **Two actors that answer alike on every asked pair have the same
transcript.**  The protocol cannot see anything else. -/
theorem run_congr (π : Protocol) (p p' : Nat → Nat) :
    ∀ k, (∀ e, e ∈ run π p k → decide (p' e.1 = p' e.2.1) = decide (p e.1 = p e.2.1)) →
      run π p' k = run π p k := by
  intro k
  induction k with
  | zero => intro _; rfl
  | succ k ih =>
    intro h
    have h' : ∀ e, e ∈ run π p k → decide (p' e.1 = p' e.2.1) = decide (p e.1 = p e.2.1) :=
      fun e he => h e (run_mono π p k e he)
    have ih' := ih h'
    cases hπ : π (run π p k) with
    | none =>
      rw [run_succ_none hπ]
      rw [← ih'] at hπ
      rw [run_succ_none hπ, ih']
    | some pr =>
      have hmem : entry p pr ∈ run π p (k + 1) := by
        rw [run_succ_some hπ]; exact List.mem_append_right _ List.mem_cons_self
      have hdec : decide (p' pr.1 = p' pr.2) = decide (p pr.1 = p pr.2) := h _ hmem
      rw [run_succ_some hπ]
      rw [← ih'] at hπ
      rw [run_succ_some hπ, ih']
      show run π p k ++ [(pr.1, pr.2, decide (p' pr.1 = p' pr.2))] =
        run π p k ++ [(pr.1, pr.2, decide (p pr.1 = p pr.2))]
      rw [hdec]

/-! ## The merge adversary -/

/-- The presentation that identifies `y` with `x` and nothing else. -/
def merge (x y : Nat) : Nat → Nat := fun z => if z = y then x else z

/-- Off the merged pair, `merge x y` answers as the identity does. -/
theorem merge_agrees {x y a b : Nat} (hab : ¬ (a = x ∧ b = y)) (hba : ¬ (a = y ∧ b = x)) :
    (merge x y a = merge x y b) ↔ a = b := by
  unfold merge
  cases Nat.decEq a y with
  | isTrue hay =>
    cases Nat.decEq b y with
    | isTrue hby =>
      rw [if_pos hay, if_pos hby]
      constructor
      · intro _; omega
      · intro _; rfl
    | isFalse hby =>
      rw [if_pos hay, if_neg hby]
      have hbx : b ≠ x := fun e => hba ⟨hay, e⟩
      constructor
      · intro e; exact absurd e.symm hbx
      · intro e; omega
  | isFalse hay =>
    cases Nat.decEq b y with
    | isTrue hby =>
      rw [if_neg hay, if_pos hby]
      have hax : a ≠ x := fun e => hab ⟨e, hby⟩
      constructor
      · intro e; exact absurd e hax
      · intro e; omega
    | isFalse hby =>
      rw [if_neg hay, if_neg hby]

/-- The pair `{x, y}` was probed, in either order. -/
def askedB (T : Transcript) (x y : Nat) : Bool :=
  T.any (fun e => (decide (e.1 = x) && decide (e.2.1 = y)) || (decide (e.1 = y) && decide (e.2.1 = x)))

theorem askedB_iff (T : Transcript) (x y : Nat) :
    askedB T x y = true ↔ ∃ e, e ∈ T ∧ ((e.1 = x ∧ e.2.1 = y) ∨ (e.1 = y ∧ e.2.1 = x)) := by
  simp only [askedB, List.any_eq_true, Bool.or_eq_true, Bool.and_eq_true, decide_eq_true_eq]

/-- The unordered pair of an entry. -/
def norm (e : Nat × Nat × Bool) : Nat × Nat := (min e.1 e.2.1, max e.1 e.2.1)

theorem mem_allPairs (i j : Nat) : ∀ n : Nat, (i, j) ∈ allPairs n ↔ i < j ∧ j < n := by
  intro n
  induction n with
  | zero =>
    show (i, j) ∈ ([] : List (Nat × Nat)) ↔ _
    constructor
    · intro h; cases h
    · intro h; exact absurd h.2 (Nat.not_lt_zero j)
  | succ n ih =>
    show (i, j) ∈ allPairs n ++ (List.range n).map (fun a => (a, n)) ↔ _
    rw [List.mem_append, List.mem_map, ih]
    constructor
    · rintro (h | ⟨a, ha, hij⟩)
      · exact ⟨h.1, Nat.lt_succ_of_lt h.2⟩
      · have h1 := (Prod.mk.inj hij).1
        have h2 := (Prod.mk.inj hij).2
        have := List.mem_range.mp ha
        exact ⟨by omega, by omega⟩
    · rintro ⟨hij, hjn⟩
      cases Nat.decEq j n with
      | isTrue h => exact Or.inr ⟨i, List.mem_range.mpr (by omega), by rw [h]⟩
      | isFalse h => exact Or.inl ⟨hij, by omega⟩

/-! ### A constructive count: a duplicate-free list is no longer than any list containing it -/

/-- Remove every occurrence of `a`. -/
def dropAll {α : Type} [DecidableEq α] (a : α) : List α → List α
  | [] => []
  | b :: t => if b = a then dropAll a t else b :: dropAll a t

theorem length_dropAll_le {α : Type} [DecidableEq α] (a : α) :
    ∀ l : List α, (dropAll a l).length ≤ l.length := by
  intro l
  induction l with
  | nil => exact Nat.le_refl _
  | cons b t ih =>
    show (if b = a then dropAll a t else b :: dropAll a t).length ≤ t.length + 1
    cases decEq b a with
    | isTrue e => rw [if_pos e]; omega
    | isFalse ne => rw [if_neg ne]; simp only [List.length_cons]; omega

theorem length_dropAll_lt {α : Type} [DecidableEq α] (a : α) :
    ∀ l : List α, a ∈ l → (dropAll a l).length < l.length := by
  intro l
  induction l with
  | nil => intro h; cases h
  | cons b t ih =>
    intro h
    show (if b = a then dropAll a t else b :: dropAll a t).length < t.length + 1
    cases decEq b a with
    | isTrue e =>
      rw [if_pos e]
      have := length_dropAll_le a t
      omega
    | isFalse ne =>
      rw [if_neg ne]
      have hat : a ∈ t := by
        rcases List.mem_cons.mp h with h | h
        · exact absurd h.symm ne
        · exact h
      simp only [List.length_cons]
      have := ih hat
      omega

theorem mem_dropAll {α : Type} [DecidableEq α] (a z : α) :
    ∀ l : List α, z ∈ l → z ≠ a → z ∈ dropAll a l := by
  intro l
  induction l with
  | nil => intro h; cases h
  | cons b t ih =>
    intro h hz
    show z ∈ (if b = a then dropAll a t else b :: dropAll a t)
    rcases List.mem_cons.mp h with h | h
    · rw [h] at hz ⊢
      rw [if_neg hz]
      exact List.mem_cons_self
    · cases decEq b a with
      | isTrue e => rw [if_pos e]; exact ih h hz
      | isFalse ne => rw [if_neg ne]; exact List.mem_cons_of_mem _ (ih h hz)

theorem nodup_subset_length {α : Type} [DecidableEq α] :
    ∀ (l₁ l₂ : List α), l₁.Nodup → l₁ ⊆ l₂ → l₁.length ≤ l₂.length := by
  intro l₁
  induction l₁ with
  | nil => intro l₂ _ _; exact Nat.zero_le _
  | cons a t ih =>
    intro l₂ hnd hsub
    have hnd' := List.nodup_cons.mp hnd
    have ha : a ∈ l₂ := hsub List.mem_cons_self
    have hsub' : t ⊆ dropAll a l₂ := by
      intro z hz
      apply mem_dropAll a z l₂ (hsub (List.mem_cons_of_mem _ hz))
      intro e
      rw [e] at hz
      exact hnd'.1 hz
    have h1 := ih _ hnd'.2 hsub'
    have h2 := length_dropAll_lt a l₂ ha
    simp only [List.length_cons]
    omega

theorem nodup_range_self : ∀ n : Nat, (List.range n).Nodup := by
  intro n
  induction n with
  | zero => exact List.nodup_nil
  | succ n ih =>
    rw [List.range_succ, List.nodup_append]
    refine ⟨ih, List.nodup_cons.mpr ⟨List.not_mem_nil, List.nodup_nil⟩, ?_⟩
    intro a ha b hb
    rw [List.mem_singleton.mp hb]
    exact Nat.ne_of_lt (List.mem_range.mp ha)

theorem allPairs_nodup : ∀ n : Nat, (allPairs n).Nodup := by
  intro n
  induction n with
  | zero => exact List.nodup_nil
  | succ n ih =>
    show (allPairs n ++ (List.range n).map (fun a => (a, n))).Nodup
    rw [List.nodup_append]
    refine ⟨ih, ?_, ?_⟩
    · show List.Pairwise (fun x y : Nat × Nat => x ≠ y) (List.map (fun a => (a, n)) (List.range n))
      exact List.Pairwise.map _ (fun a b h e => h (Prod.mk.inj e).1) (nodup_range_self n)
    · intro a ha b hb
      obtain ⟨i, _, rfl⟩ := List.mem_map.mp hb
      obtain ⟨x, y⟩ := a
      have hxy := (mem_allPairs x y n).mp ha
      intro e
      have := (Prod.mk.inj e).2
      omega

/-- **A short transcript misses a pair.** -/
theorem uncovered_pair (n : Nat) (T : Transcript) (hshort : T.length < (allPairs n).length) :
    ∃ x y, x < y ∧ y < n ∧ askedB T x y = false := by
  cases hall : (allPairs n).all (fun pr => askedB T pr.1 pr.2) with
  | false =>
    obtain ⟨pr, hpr, hf⟩ := all_false_witness _ _ hall
    obtain ⟨x, y⟩ := pr
    have hxy := (mem_allPairs x y n).mp hpr
    exact ⟨x, y, hxy.1, hxy.2, hf⟩
  | true =>
    exfalso
    rw [List.all_eq_true] at hall
    have hsub : allPairs n ⊆ T.map norm := by
      intro pr hpr
      obtain ⟨x, y⟩ := pr
      have hxy := (mem_allPairs x y n).mp hpr
      obtain ⟨e, he, hcase⟩ := (askedB_iff T x y).mp (hall (x, y) hpr)
      rw [List.mem_map]
      refine ⟨e, he, ?_⟩
      unfold norm
      rcases hcase with ⟨h1, h2⟩ | ⟨h1, h2⟩
      · rw [h1, h2, Nat.min_eq_left (Nat.le_of_lt hxy.1), Nat.max_eq_right (Nat.le_of_lt hxy.1)]
      · rw [h1, h2, Nat.min_eq_right (Nat.le_of_lt hxy.1), Nat.max_eq_left (Nat.le_of_lt hxy.1)]
    have hle := nodup_subset_length _ _ (allPairs_nodup n) hsub
    rw [List.length_map] at hle
    omega

/-- **The merge adversary.**  If the identity actor's transcript is shorter
than `n(n−1)/2`, some `merge x y` with `x < y < n` has the same transcript. -/
theorem lower_bound (n : Nat) (π : Protocol) (k : Nat)
    (hshort : (run π (fun z => z) k).length < (allPairs n).length) :
    ∃ x y, x < y ∧ y < n ∧ run π (merge x y) k = run π (fun z => z) k := by
  obtain ⟨x, y, hxy, hyn, hnot⟩ := uncovered_pair n _ hshort
  refine ⟨x, y, hxy, hyn, ?_⟩
  apply run_congr
  intro e he
  have hne : ¬ ((e.1 = x ∧ e.2.1 = y) ∨ (e.1 = y ∧ e.2.1 = x)) := by
    intro hc
    have := (askedB_iff _ x y).mpr ⟨e, he, hc⟩
    rw [hnot] at this
    cases this
  have hiff := merge_agrees (x := x) (y := y) (a := e.1) (b := e.2.1)
    (fun h => hne (Or.inl h)) (fun h => hne (Or.inr h))
  show decide (merge x y e.1 = merge x y e.2.1) = decide (e.1 = e.2.1)
  exact decide_eq_decide.mpr hiff

/-- **No acquisition below the bound.**  Whatever evaluator an admission rule
builds from a transcript shorter than `n(n−1)/2`, some actor on `range n` is
not sharply presented by it. -/
theorem no_acquisition_below_bound (n : Nat) (π : Protocol) (rule : Transcript → Evaluator)
    (k : Nat) (hshort : (run π (fun z => z) k).length < (allPairs n).length) :
    ∃ p : Nat → Nat, ¬ Sharp (List.range n) (rule (run π p k)) p := by
  obtain ⟨x, y, hxy, hyn, heq⟩ := lower_bound n π k hshort
  have hx : x ∈ List.range n := List.mem_range.mpr (Nat.lt_trans hxy hyn)
  have hy : y ∈ List.range n := List.mem_range.mpr hyn
  cases hv : verdictB (rule (run π (fun z => z) k)) x y with
  | true =>
    refine ⟨merge x y, ?_⟩
    intro hs
    rw [heq] at hs
    have hm : merge x y x = merge x y y := by
      show (if x = y then x else x) = (if y = y then x else y)
      rw [if_neg (Nat.ne_of_lt hxy), if_pos rfl]
    have := (hs x hx y hy).mpr hm
    rw [hv] at this
    cases this
  | false =>
    refine ⟨fun z => z, ?_⟩
    intro hs
    have : x = y := (hs x hx y hy).mp hv
    omega

/-- The same, for a step budget: fewer than `n(n−1)/2` steps never acquire
every actor. -/
theorem no_acquisition_in_fewer_steps (n : Nat) (π : Protocol) (rule : Transcript → Evaluator)
    (k : Nat) (hk : k < (allPairs n).length) :
    ∃ p : Nat → Nat, ¬ Sharp (List.range n) (rule (run π p k)) p :=
  no_acquisition_below_bound n π rule k (Nat.lt_of_le_of_lt (run_length_le π _ k) hk)

/-- In the seed's own count: `2k < n(n−1)` steps never acquire every actor. -/
theorem no_acquisition_below_half_square (n : Nat) (π : Protocol)
    (rule : Transcript → Evaluator) (k : Nat) (hk : 2 * k < n * (n - 1)) :
    ∃ p : Nat → Nat, ¬ Sharp (List.range n) (rule (run π p k)) p := by
  apply no_acquisition_in_fewer_steps n π rule k
  have := allPairs_length n
  omega

/-- **TT-39o.**  Below the bound, two actors of different capability — one
tells `x` from `y`, the other does not — have identical transcripts. -/
theorem transcripts_identical_capabilities_differ (n : Nat) (π : Protocol) (k : Nat)
    (hshort : (run π (fun z => z) k).length < (allPairs n).length) :
    ∃ p p' : Nat → Nat, run π p k = run π p' k ∧
      ∃ x y, x ∈ List.range n ∧ y ∈ List.range n ∧ p x = p y ∧ p' x ≠ p' y := by
  obtain ⟨x, y, hxy, hyn, heq⟩ := lower_bound n π k hshort
  refine ⟨merge x y, fun z => z, heq, x, y, List.mem_range.mpr (Nat.lt_trans hxy hyn),
    List.mem_range.mpr hyn, ?_, Nat.ne_of_lt hxy⟩
  show (if x = y then x else x) = (if y = y then x else y)
  rw [if_neg (Nat.ne_of_lt hxy), if_pos rfl]

/-! ## The retained counterexample: a fixed finite family -/

/-- Probe `(0, 1)`, always. -/
def probe01 : Protocol := fun _ => some (0, 1)

/-- Two cases: if the pair answered "same", present nothing; otherwise one
view separating `0` from `1`. -/
def admit01 (T : Transcript) : Evaluator := if (0, 1, true) ∈ T then [] else [[0]]

/-- **Completeness relative to a fixed family is cheap.**  One probe and a
two-case rule are sharp for both members of `{id, merge 0 1}` on two data.
This does not contradict the bound, which quantifies over every actor. -/
theorem complete_evaluator_for_two :
    Sharp (List.range 2) (admit01 (run probe01 (fun z => z) 1)) (fun z => z) ∧
    Sharp (List.range 2) (admit01 (run probe01 (merge 0 1) 1)) (merge 0 1) := by
  unfold Sharp
  decide

/-- The two transcripts the rule distinguishes. -/
theorem probe01_transcripts :
    run probe01 (fun z => z) 1 = [(0, 1, false)] ∧ run probe01 (merge 0 1) 1 = [(0, 1, true)] := by
  decide

/-! ## The upper bound: the complete table -/

/-- Ask the pairs of a script in order, then stop. -/
def scripted (L : List (Nat × Nat)) : Protocol := fun T =>
  match L.drop T.length with
  | [] => none
  | pr :: _ => some pr

theorem run_scripted (L : List (Nat × Nat)) (p : Nat → Nat) :
    ∀ j, j ≤ L.length → run (scripted L) p j = (L.take j).map (entry p) := by
  intro j
  induction j with
  | zero => intro _; rfl
  | succ j ih =>
    intro hj
    have hlt : j < L.length := hj
    have ih' := ih (Nat.le_of_lt hlt)
    have hlen : (run (scripted L) p j).length = j := by
      rw [ih', List.length_map, List.length_take, Nat.min_eq_left (Nat.le_of_lt hlt)]
    have hstep : scripted L (run (scripted L) p j) = some L[j] := by
      show (match L.drop (run (scripted L) p j).length with
        | [] => none
        | pr :: _ => some pr) = some L[j]
      rw [hlen, List.drop_eq_getElem_cons hlt]
    rw [run_succ_some hstep, ih', ← List.take_append_getElem hlt, List.map_append,
      List.map_cons, List.map_nil]

/-- The complete table of answers on `range n`. -/
def fullT (n : Nat) (p : Nat → Nat) : Transcript := (allPairs n).map (entry p)

theorem run_complete (n : Nat) (p : Nat → Nat) :
    run (scripted (allPairs n)) p (allPairs n).length = fullT n p := by
  rw [run_scripted _ _ _ (Nat.le_refl _), List.take_length]
  rfl

theorem fullT_length (n : Nat) (p : Nat → Nat) :
    2 * (fullT n p).length = n * (n - 1) := by
  unfold fullT
  rw [List.length_map]
  exact allPairs_length n

/-- Read "same class" off a transcript. -/
def sameT (T : Transcript) (a b : Nat) : Bool :=
  decide (a = b) ||
    T.any (fun e =>
      ((decide (e.1 = a) && decide (e.2.1 = b)) || (decide (e.1 = b) && decide (e.2.1 = a))) && e.2.2)

theorem sameT_full (n : Nat) (p : Nat → Nat) (a b : Nat) (ha : a < n) (hb : b < n) :
    sameT (fullT n p) a b = true ↔ p a = p b := by
  unfold sameT fullT
  simp only [Bool.or_eq_true, decide_eq_true_eq, List.any_eq_true, Bool.and_eq_true, List.mem_map]
  constructor
  · rintro (h | ⟨e, ⟨pr, _, rfl⟩, hor, hv⟩)
    · rw [h]
    · have hpp : p pr.1 = p pr.2 := of_decide_eq_true hv
      rcases hor with ⟨h1, h2⟩ | ⟨h1, h2⟩
      · have h1' : pr.1 = a := h1
        have h2' : pr.2 = b := h2
        rw [← h1', ← h2']; exact hpp
      · have h1' : pr.1 = b := h1
        have h2' : pr.2 = a := h2
        rw [← h1', ← h2']; exact hpp.symm
  · intro hpab
    cases Nat.decEq a b with
    | isTrue e => exact Or.inl e
    | isFalse ne =>
      apply Or.inr
      cases Nat.decLt a b with
      | isTrue hab =>
        refine ⟨entry p (a, b), ⟨(a, b), (mem_allPairs a b n).mpr ⟨hab, hb⟩, rfl⟩,
          Or.inl ⟨rfl, rfl⟩, ?_⟩
        exact decide_eq_true hpab
      | isFalse hnab =>
        have hba : b < a := by omega
        refine ⟨entry p (b, a), ⟨(b, a), (mem_allPairs b a n).mpr ⟨hba, ha⟩, rfl⟩,
          Or.inr ⟨rfl, rfl⟩, ?_⟩
        exact decide_eq_true hpab.symm

/-- One view per datum: the data the transcript puts in its class. -/
def tableE (n : Nat) (T : Transcript) : Evaluator :=
  (List.range n).map (fun a => (List.range n).filter (fun b => sameT T a b))

theorem tableE_length (n : Nat) (T : Transcript) : (tableE n T).length = n := by
  unfold tableE
  rw [List.length_map, List.length_range]

/-- **The complete table acquires every actor.** -/
theorem table_sharp (n : Nat) (p : Nat → Nat) : Sharp (List.range n) (tableE n (fullT n p)) p := by
  intro x hx y hy
  have hxn := List.mem_range.mp hx
  have hyn := List.mem_range.mp hy
  rw [verdictB_eq_false_iff]
  constructor
  · intro h
    have hc := h ((List.range n).filter (fun b => sameT (fullT n p) x b))
      (List.mem_map.mpr ⟨x, hx, rfl⟩)
    rw [sepB_eq_false_iff] at hc
    have hxc : x ∈ (List.range n).filter (fun b => sameT (fullT n p) x b) := by
      rw [List.mem_filter]
      exact ⟨hx, (sameT_full n p x x hxn hxn).mpr rfl⟩
    have hyc := hc.mp hxc
    rw [List.mem_filter] at hyc
    exact (sameT_full n p x y hxn hyn).mp hyc.2
  · intro hpxy c hc
    obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hc
    have han := List.mem_range.mp ha
    rw [sepB_eq_false_iff, List.mem_filter, List.mem_filter]
    constructor
    · rintro ⟨_, hs⟩
      refine ⟨hy, ?_⟩
      rw [sameT_full n p a y han hyn, ← hpxy]
      exact (sameT_full n p a x han hxn).mp hs
    · rintro ⟨_, hs⟩
      refine ⟨hx, ?_⟩
      rw [sameT_full n p a x han hxn, hpxy]
      exact (sameT_full n p a y han hyn).mp hs

theorem complete_table_acquires (n : Nat) (p : Nat → Nat) :
    Sharp (List.range n) (tableE n (run (scripted (allPairs n)) p (allPairs n).length)) p := by
  rw [run_complete]
  exact table_sharp n p

/-- **TT-43o (i), both halves.**  Fewer than `n(n−1)/2` steps never acquire
every actor; `n(n−1)/2` steps, spent on the complete table, acquire every
actor. -/
theorem acquisition_cost_exact (n : Nat) :
    (∀ (π : Protocol) (rule : Transcript → Evaluator) (k : Nat), k < (allPairs n).length →
      ∃ p : Nat → Nat, ¬ Sharp (List.range n) (rule (run π p k)) p) ∧
    (∀ p : Nat → Nat,
      Sharp (List.range n) (tableE n (run (scripted (allPairs n)) p (allPairs n).length)) p) :=
  ⟨fun π rule k hk => no_acquisition_in_fewer_steps n π rule k hk,
   fun p => complete_table_acquires n p⟩

/-! ## From the table to the view bound -/

theorem sharp_congr {D : List Nat} {E : Evaluator} {p p' : Nat → Nat} (h : Sharp D E p)
    (hk : ∀ x, x ∈ D → ∀ y, y ∈ D → (p x = p y ↔ p' x = p' y)) : Sharp D E p' :=
  fun x hx y hy => (h x hx y hy).trans (hk x hx y hy)

theorem classCount_congr {D : List Nat} {p p' : Nat → Nat}
    (hk : ∀ x, x ∈ D → ∀ y, y ∈ D → (p x = p y ↔ p' x = p' y)) :
    classCount D [p'] = classCount D [p] := by
  apply Nat.le_antisymm
  · apply count_le_of_determines (sigList [p]) (sigList [p']) D
    intro a ha b hb h
    have h' : p a = p b := (List.cons.inj h).1
    show [p' a] = [p' b]
    rw [(hk a ha b hb).mp h']
  · apply count_le_of_determines (sigList [p']) (sigList [p]) D
    intro a ha b hb h
    have h' : p' a = p' b := (List.cons.inj h).1
    show [p a] = [p b]
    rw [(hk a ha b hb).mpr h']

/-- The presentation the table determines, computed from the transcript. -/
def acquired (n : Nat) (T : Transcript) : Nat → Nat :=
  pQ (List.range n) (questions (tableE n T))

/-- The acquired presentation has the actor's partition on the carrier. -/
theorem acquired_kernel (n : Nat) (p : Nat → Nat) :
    ∀ x, x ∈ List.range n → ∀ y, y ∈ List.range n →
      (acquired n (fullT n p) x = acquired n (fullT n p) y ↔ p x = p y) := by
  intro x hx y hy
  unfold acquired
  rw [pQ_exact _ _ x hx y hy, ← verdictB_false_iff_sigEq]
  exact table_sharp n p x hx y hy

/-- An evaluator with `m` views, computed from the transcript alone. -/
def logE (n : Nat) (T : Transcript) (m : Nat) : Evaluator :=
  sharpObserver (List.range n) (acquired n T) m

theorem logE_length (n : Nat) (T : Transcript) (m : Nat) : (logE n T m).length = m :=
  bitObserver_length _ _ m

/-- **TT-43o (iii), sufficiency, from the transcript.**  If the actor has at
most `2^m` classes, `m` views computed from the complete table are sharp. -/
theorem log_views (n : Nat) (p : Nat → Nat) (m : Nat) (h : classCount (List.range n) [p] ≤ 2 ^ m) :
    Sharp (List.range n) (logE n (fullT n p) m) p := by
  have hk := acquired_kernel n p
  have hc : classCount (List.range n) [acquired n (fullT n p)] ≤ 2 ^ m := by
    rw [classCount_congr (p := p) (p' := acquired n (fullT n p)) (fun x hx y hy => (hk x hx y hy).symm)]
    exact h
  exact sharp_congr (sharpObserver_sharp _ _ m hc) hk

/-! ## Fixing the partition -/

/-- The transcript fixes the partition on `D`: all consistent actors agree on
every pair. -/
def Fixes (D : List Nat) (T : Transcript) : Prop :=
  ∀ p p', Consistent T p → Consistent T p' →
    ∀ x, x ∈ D → ∀ y, y ∈ D → (p x = p y ↔ p' x = p' y)

/-- **TT-43o (iv), necessity.**  An evaluator sharp for every actor consistent
with the transcript forces those actors to share one partition. -/
theorem acquires_implies_fixes (D : List Nat) (T : Transcript) (E : Evaluator)
    (h : ∀ p, Consistent T p → Sharp D E p) : Fixes D T := by
  intro p p' hp hp' x hx y hy
  rw [← (h p hp) x hx y hy, ← (h p' hp') x hx y hy]

/-- A transcript the identity and a merge both answer does not fix the
partition: the empty transcript on two data. -/
theorem empty_transcript_fixes_nothing : ¬ Fixes [0, 1] [] := by
  intro h
  have := (h (fun z => z) (merge 0 1) (fun _ he => by cases he) (fun _ he => by cases he)
    0 (by decide) 1 (by decide)).mpr (by decide)
  exact absurd this (by decide)

/-! ## The promised count: the "exactly `N`" reading of TT-43o (ii), refuted at `n = N` -/

/-- On two points an actor has two classes exactly when it separates them. -/
theorem classCount_two_iff (p : Nat → Nat) : classCount [0, 1] [p] = 2 ↔ p 0 ≠ p 1 := by
  have e1 : classCount [0, 1] [p] = (dedupL [[p 0], [p 1]]).length := rfl
  rw [e1, dedupL_cons, memB_cons]
  cases Nat.decEq (p 0) (p 1) with
  | isTrue h =>
    rw [h, if_pos rfl]
    show (dedupL [[p 1]]).length = 2 ↔ p 1 ≠ p 1
    rw [dedupL_cons]
    show [[p 1]].length = 2 ↔ p 1 ≠ p 1
    rw [List.length_singleton]
    constructor
    · intro e; exact absurd e (by decide)
    · intro ne; exact absurd rfl ne
  | isFalse ne =>
    rw [if_neg (fun e => ne (List.cons.inj e).1)]
    show ([p 0] :: dedupL [[p 1]]).length = 2 ↔ p 0 ≠ p 1
    rw [dedupL_cons]
    show [[p 0], [p 1]].length = 2 ↔ p 0 ≠ p 1
    exact ⟨fun _ => ne, fun _ => rfl⟩

/-- **The "exactly `N`" reading of TT-43o (ii) fails at `n = N = 2`.**  The
proposal's count `N(N−1)/2 + (n−N)(N−1)` is `1` there, but when exactly two
classes are promised on two points, the one-view evaluator `[[0]]` is sharp
for every such actor with no probe at all: the promise already fixes the
partition.  (The same holds at every `n = N`; the finite model checks
`n ≤ 5`.)  Under the "at most `N`" reading the count at `N = n` is part (i). -/
theorem exact_promise_zero_probes_two (p : Nat → Nat) (hN : classCount [0, 1] [p] = 2) :
    Sharp [0, 1] [[0]] p := by
  have hne := (classCount_two_iff p).mp hN
  intro x hx y hy
  have hx' : x = 0 ∨ x = 1 := by
    rcases List.mem_cons.mp hx with h | h
    · exact Or.inl h
    · exact Or.inr (List.mem_singleton.mp h)
  have hy' : y = 0 ∨ y = 1 := by
    rcases List.mem_cons.mp hy with h | h
    · exact Or.inl h
    · exact Or.inr (List.mem_singleton.mp h)
  rcases hx' with rfl | rfl <;> rcases hy' with rfl | rfl
  · exact ⟨fun _ => rfl, fun _ => by decide⟩
  · constructor
    · intro h; exact absurd h (by decide)
    · intro h; exact absurd h hne
  · constructor
    · intro h; exact absurd h (by decide)
    · intro h; exact absurd h.symm hne
  · exact ⟨fun _ => rfl, fun _ => by decide⟩

/-- The proposal's count at `n = N = 2`, for the record. -/
theorem proposal_count_two : 2 * (2 - 1) / 2 + (2 - 2) * (2 - 1) = 1 := by decide

end Acquisition
end ResearchActorInstitution
