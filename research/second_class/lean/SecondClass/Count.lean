import SecondClass.Kernel
import SecondClass.IsoKernel
import SecondClass.Rounds

/-!
# The five component counts across the sealed isomorphism

Native to rung eight.

The sealed isomorphism structure bundles four maps with two-sided
inverses on the admitted ranges of data and forms, and asks that
instances, uniform rules and requirements be carried forward and back as
MEMBERSHIP.  Membership does not see a repeated entry, and the maps are
constrained only on the admitted ranges.  So:

* `iso_data`, `iso_forms`: the numbers of data and of forms are kept by
  every inhabitant of the structure, with no hypothesis on either regime.
  The maps restricted to the admitted range carry it without a repeated
  value into the other range (`count_le_of_inv`), and the exchanged maps
  (`isoSymm`) carry it back.
* `insts_le`, `rules_le`, `reqs_le`: a list of the source regime without
  a repeated entry, whose entries name only admitted data and forms (the
  sealed well-formedness), is no longer than the matching list of the
  target.  Nothing is assumed of the target.
* `components_iso`, `size_iso`: so two CLEAN regimes -- well formed and
  duplicate-free -- that the structure relates have all five component
  counts equal, and one element count.

`length_le_of_nodup_sub` is the counting lemma: a list without a repeated
entry whose entries all lie in a second list is no longer than it.  The
library proves the same statement inside a classical section, and its
lemmas on removing an entry and on the admitted range having no repeated
index reach `Classical.choice`; so the counting lemma is proved here over
decidable equality with the removal done by hand, and `range_nodup` is
proved again, to keep `Classical.choice` out of the package.

That neither hypothesis can be dropped is in `Counter.lean`.

AuthorityEffect: None.
-/

namespace SecondClass
namespace Count

open Sealed
open Rounds (size)

/-- The sealed isomorphism with its maps exchanged. -/
def isoSymm {r s : Regime} (σ : Iso r s) : Iso s r where
  dmap := σ.dinv
  dinv := σ.dmap
  fmap := σ.finv
  finv := σ.fmap
  dmap_lt := σ.dinv_lt
  dinv_lt := σ.dmap_lt
  dinv_dmap := σ.dmap_dinv
  dmap_dinv := σ.dinv_dmap
  fmap_lt := σ.finv_lt
  finv_lt := σ.fmap_lt
  finv_fmap := σ.fmap_finv
  fmap_finv := σ.finv_fmap
  arity := fun f hf => by
    have h := σ.arity (σ.finv f) (List.mem_range.mpr (σ.finv_lt f hf))
    rw [σ.fmap_finv f hf] at h
    exact h.symm
  insts_fwd := σ.insts_bwd
  insts_bwd := σ.insts_fwd
  rules_fwd := σ.rules_bwd
  rules_bwd := σ.rules_fwd
  reqs_fwd := σ.reqs_bwd
  reqs_bwd := σ.reqs_fwd

/-- The lists of instances, uniform rules and requirements each hold no
entry twice. -/
def Dupfree (r : Regime) : Prop :=
  r.insts.Nodup ∧ r.rules.Nodup ∧ r.reqs.Nodup

/-- Well formed in the sealed sense, and duplicate-free. -/
def Clean (r : Regime) : Prop :=
  r.wf ∧ Dupfree r

/-- A map with a left inverse on a list keeps it free of repeated
entries. -/
theorem nodup_map_of_inv {α β : Type} (f : α → β) (g : β → α) :
    ∀ l : List α, (∀ x ∈ l, g (f x) = x) → l.Nodup → (l.map f).Nodup := by
  intro l
  induction l with
  | nil => intro _ _; exact List.Pairwise.nil
  | cons a t ih =>
    intro hinv hnd
    rw [List.nodup_cons] at hnd
    rw [List.map_cons, List.nodup_cons]
    refine ⟨?_, ih (fun x hx => hinv x (List.mem_cons_of_mem _ hx)) hnd.2⟩
    intro hmem
    rcases List.mem_map.mp hmem with ⟨y, hy, hfy⟩
    have h1 : g (f y) = y := hinv y (List.mem_cons_of_mem _ hy)
    have h2 : g (f a) = a := hinv a List.mem_cons_self
    rw [hfy] at h1
    have hya : y = a := h1.symm.trans h2
    exact hnd.1 (hya ▸ hy)

/-- A list without a repeated entry, every entry of which lies in a
second list, is no longer than the second list. -/
theorem length_le_of_nodup_sub {α : Type} [DecidableEq α] :
    ∀ l₁ l₂ : List α, l₁.Nodup → (∀ x ∈ l₁, x ∈ l₂) →
      l₁.length ≤ l₂.length := by
  intro l₁
  induction l₁ with
  | nil => intro l₂ _ _; exact Nat.zero_le _
  | cons a t ih =>
    intro l₂ hnd hsub
    rw [List.nodup_cons] at hnd
    -- Removing one occurrence of `a`, by hand: the library's removal
    -- lemmas reach `Classical.choice`.
    have hrm : ∀ l : List α, a ∈ l → ∃ l' : List α,
        l'.length + 1 = l.length ∧ ∀ x ∈ l, x ≠ a → x ∈ l' := by
      intro l
      induction l with
      | nil => intro h; cases h
      | cons y ys ihl =>
        intro h
        by_cases hy : y = a
        · refine ⟨ys, rfl, fun x hx hxa => ?_⟩
          cases hx with
          | head => exact absurd hy hxa
          | tail _ hx => exact hx
        · have hys : a ∈ ys := by
            cases h with
            | head => exact absurd rfl hy
            | tail _ h => exact h
          obtain ⟨l', hl, hmem⟩ := ihl hys
          refine ⟨y :: l', ?_, fun x hx hxa => ?_⟩
          · show l'.length + 1 + 1 = ys.length + 1
            rw [hl]
          · cases hx with
            | head => exact List.Mem.head _
            | tail _ hx => exact List.Mem.tail _ (hmem x hx hxa)
    obtain ⟨l', hl, hmem⟩ := hrm l₂ (hsub a List.mem_cons_self)
    have ht : ∀ x ∈ t, x ∈ l' := by
      intro x hx
      have hxa : x ≠ a := fun h => hnd.1 (h ▸ hx)
      exact hmem x (hsub x (List.mem_cons_of_mem _ hx)) hxa
    have h1 := ih l' hnd.2 ht
    show t.length + 1 ≤ l₂.length
    omega

/-- A list without a repeated entry, carried into a second list by a map
with a left inverse on it, is no longer than the second list. -/
theorem count_le_of_inv {α : Type} [DecidableEq α] (f g : α → α)
    (l₁ l₂ : List α) (hnd : l₁.Nodup) (hinv : ∀ x ∈ l₁, g (f x) = x)
    (hmap : ∀ x ∈ l₁, f x ∈ l₂) : l₁.length ≤ l₂.length := by
  have h := length_le_of_nodup_sub (l₁.map f) l₂ (nodup_map_of_inv f g l₁ hinv hnd)
    (fun y hy => by
      rcases List.mem_map.mp hy with ⟨x, hx, hxy⟩
      rw [← hxy]
      exact hmap x hx)
  rw [List.length_map] at h
  exact h

/-- The admitted range holds no index twice.  The library's statement of
this reaches `Classical.choice`, so it is proved again here. -/
theorem range_nodup (n : Nat) : (List.range n).Nodup := by
  induction n with
  | zero => exact List.Pairwise.nil
  | succ k ih =>
    rw [List.range_succ, List.nodup_append]
    refine ⟨ih, List.Pairwise.cons (fun _ h => nomatch h) List.Pairwise.nil, ?_⟩
    intro x hx y hy hxy
    rw [List.mem_singleton] at hy
    have hlt : x < k := List.mem_range.mp hx
    omega

theorem data_le {r s : Regime} (σ : Iso r s) : r.data ≤ s.data := by
  have h := count_le_of_inv σ.dmap σ.dinv (List.range r.data) (List.range s.data)
    (range_nodup r.data) σ.dinv_dmap
    (fun d hd => List.mem_range.mpr (σ.dmap_lt d hd))
  rw [List.length_range, List.length_range] at h
  exact h

theorem forms_le {r s : Regime} (σ : Iso r s) :
    r.forms.length ≤ s.forms.length := by
  have h := count_le_of_inv σ.fmap σ.finv (List.range r.forms.length)
    (List.range s.forms.length) (range_nodup r.forms.length) σ.finv_fmap
    (fun f hf => List.mem_range.mpr (σ.fmap_lt f hf))
  rw [List.length_range, List.length_range] at h
  exact h

/-- The number of data is kept, with no hypothesis on either regime. -/
theorem iso_data {r s : Regime} (σ : Iso r s) : r.data = s.data :=
  Nat.le_antisymm (data_le σ) (data_le (isoSymm σ))

/-- The number of forms is kept, with no hypothesis on either regime. -/
theorem iso_forms {r s : Regime} (σ : Iso r s) :
    r.forms.length = s.forms.length :=
  Nat.le_antisymm (forms_le σ) (forms_le (isoSymm σ))

theorem sortPair_of_le {p : Nat × Nat} (h : p.1 ≤ p.2) : sortPair p = p :=
  if_pos h

/-- Sorting a pair before mapping both entries and sorting again is the
same as mapping and sorting. -/
theorem sortPair_map (g : Nat → Nat) (p : Nat × Nat) :
    sortPair (g (sortPair p).1, g (sortPair p).2) = sortPair (g p.1, g p.2) := by
  obtain ⟨a, b⟩ := p
  by_cases h : a ≤ b
  · have hs : sortPair (a, b) = (a, b) := if_pos h
    rw [hs]
  · have hs : sortPair (a, b) = (b, a) := if_neg h
    rw [hs]
    show (if g b ≤ g a then (g b, g a) else (g a, g b)) =
      (if g a ≤ g b then (g a, g b) else (g b, g a))
    by_cases h1 : g b ≤ g a
    · by_cases h2 : g a ≤ g b
      · rw [if_pos h1, if_pos h2, Nat.le_antisymm h1 h2]
      · rw [if_pos h1, if_neg h2]
    · by_cases h2 : g a ≤ g b
      · rw [if_neg h1, if_pos h2]
      · exact absurd (by omega : g b ≤ g a) h1

theorem insts_le {r s : Regime} (hwf : r.wf) (hnd : r.insts.Nodup)
    (σ : Iso r s) : r.insts.length ≤ s.insts.length :=
  count_le_of_inv (fun p => (σ.fmap p.1, p.2.map σ.dmap))
    (fun p => (σ.finv p.1, p.2.map σ.dinv)) r.insts s.insts hnd
    (fun p hp => by
      show (σ.finv (σ.fmap p.1), (p.2.map σ.dmap).map σ.dinv) = p
      rw [σ.finv_fmap p.1 (List.mem_range.mpr (hwf.1 p hp).1), List.map_map]
      have hargs : p.2.map (σ.dinv ∘ σ.dmap) = p.2.map id :=
        List.map_congr_left (fun a ha =>
          σ.dinv_dmap a (List.mem_range.mpr ((hwf.1 p hp).2.2 a ha)))
      rw [hargs, List.map_id])
    σ.insts_fwd

theorem rules_le {r s : Regime} (hwf : r.wf) (hnd : r.rules.Nodup)
    (σ : Iso r s) : r.rules.length ≤ s.rules.length :=
  count_le_of_inv σ.fmap σ.finv r.rules s.rules hnd
    (fun f hf => σ.finv_fmap f (List.mem_range.mpr (hwf.2.1 f hf)))
    σ.rules_fwd

theorem reqs_le {r s : Regime} (hwf : r.wf) (hnd : r.reqs.Nodup)
    (σ : Iso r s) : r.reqs.length ≤ s.reqs.length :=
  count_le_of_inv (fun q => sortPair (σ.dmap q.1, σ.dmap q.2))
    (fun q => sortPair (σ.dinv q.1, σ.dinv q.2)) r.reqs s.reqs hnd
    (fun q hq => by
      show sortPair (σ.dinv (sortPair (σ.dmap q.1, σ.dmap q.2)).1,
          σ.dinv (sortPair (σ.dmap q.1, σ.dmap q.2)).2) = q
      rw [sortPair_map σ.dinv (σ.dmap q.1, σ.dmap q.2)]
      have h1 := (hwf.2.2.1 q hq).1
      have h2 := (hwf.2.2.1 q hq).2
      show sortPair (σ.dinv (σ.dmap q.1), σ.dinv (σ.dmap q.2)) = q
      rw [σ.dinv_dmap q.1 (List.mem_range.mpr (Nat.lt_trans h1 h2)),
        σ.dinv_dmap q.2 (List.mem_range.mpr h2)]
      exact sortPair_of_le (Nat.le_of_lt h1))
    σ.reqs_fwd

/-- Two clean regimes the sealed structure relates have all five
component counts equal. -/
theorem components_iso {r s : Regime} (hr : Clean r) (hs : Clean s)
    (σ : Iso r s) :
    r.data = s.data ∧ r.forms.length = s.forms.length ∧
      r.insts.length = s.insts.length ∧ r.rules.length = s.rules.length ∧
      r.reqs.length = s.reqs.length :=
  ⟨iso_data σ, iso_forms σ,
    Nat.le_antisymm (insts_le hr.1 hr.2.1 σ) (insts_le hs.1 hs.2.1 (isoSymm σ)),
    Nat.le_antisymm (rules_le hr.1 hr.2.2.1 σ) (rules_le hs.1 hs.2.2.1 (isoSymm σ)),
    Nat.le_antisymm (reqs_le hr.1 hr.2.2.2 σ) (reqs_le hs.1 hs.2.2.2 (isoSymm σ))⟩

/-- Two clean regimes the sealed structure relates have one element
count. -/
theorem size_iso {r s : Regime} (hr : Clean r) (hs : Clean s)
    (σ : Iso r s) : size r = size s := by
  obtain ⟨h1, h2, h3, h4, h5⟩ := components_iso hr hs σ
  unfold size
  omega

end Count
end SecondClass
