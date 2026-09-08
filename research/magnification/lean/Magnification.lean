import Derivation.PrimitiveCore
import EngineClass

/-!
# Magnification: a primitive difference as a seed, and what context changes

* `induced`: a declared constant map from settings to the demanded seed
  R2L. It ignores all fields and requires no difference witness. Its
  constancy records the definition, not a derived translation.
* `fresh_form_valid`: at any collapsed pair of any `Good` state, admitting a
  fresh form with one instance that mentions the first datum is a valid
  response. The unary mark, binary link and binary self-loop constructions
  remain valid at every distinct admitted pair
  (`bare_round_embeds`).  This generalizes the sealed `mark_progress`.
* `context_changes_minimum`: a state with an existing unary form has a
  one-item minimum at a collapsed pair, while the seed has none below two
  items; the seed's own classes stay valid there but are not minima
  (`bare_mark_not_min_in_context`).  So the tree at a difference in context
  is not the tree at the bare difference: the measure reads the context.

AuthorityEffect: None.
-/

namespace Magnification

open Derivation EngineClass

/-! ## 1. The induced seed -/

/-- A declared constant map to two data and a separation demand. Every
field of the setting is ignored; no witness is required. This definition
does not prove that the setting translates to, or forces, this regime. -/
def induced (_S : PrimitiveCore.Setting) : Regime := ⟨2, [], [], [], [(0, 1)]⟩

theorem induced_eq_R2L (S : PrimitiveCore.Setting) : induced S = R2L := rfl

theorem induced_constant (S T : PrimitiveCore.Setting) : induced S = induced T := rfl

theorem induced_wf (S : PrimitiveCore.Setting) : (induced S).wf := R2L_wf

theorem induced_collapsed (S : PrimitiveCore.Setting) : collapsed (induced S) 0 1 :=
  R2L_collapsed

/-! ## 2. The holed context (retained locally from the now-merged PR #147) -/

def holeAt (d : Nat) (args : List Nat) : List (Option Nat) :=
  args.map (fun a => if a = d then none else some a)

theorem holeAt_length (d : Nat) (args : List Nat) :
    (holeAt d args).length = args.length :=
  List.length_map _

theorem holeAt_getD (d a : Nat) :
    (if a = d then (none : Option Nat) else some a).getD d = a := by
  by_cases h : a = d
  · rw [if_pos h]
    exact h.symm
  · rw [if_neg h]
    rfl

theorem holeAt_map_getD (d : Nat) :
    ∀ args : List Nat, (holeAt d args).map (fun s => s.getD d) = args
  | [] => rfl
  | a :: t => by
      show ((if a = d then (none : Option Nat) else some a).getD d)
          :: (holeAt d t).map (fun s => s.getD d) = a :: t
      rw [holeAt_getD, holeAt_map_getD d t]

theorem plug_holeAt (f d : Nat) (args : List Nat) :
    plug ⟨f, holeAt d args⟩ d = (f, args) := by
  show (f, (holeAt d args).map (fun s => s.getD d)) = (f, args)
  rw [holeAt_map_getD]

/-- Plugging the context holed at `i` with a different datum changes the
argument list wherever `i` occurred. -/
theorem holeAt_plug_other {i j : Nat} (hij : i ≠ j) :
    ∀ args : List Nat, i ∈ args → (holeAt i args).map (fun s => s.getD j) ≠ args
  | [], h => absurd h List.not_mem_nil
  | a :: t, h => by
      intro heq
      have heq' : ((if a = i then (none : Option Nat) else some a).getD j)
          :: (holeAt i t).map (fun s => s.getD j) = a :: t := heq
      injection heq' with hhead htail
      by_cases ha : a = i
      · rw [if_pos ha] at hhead
        exact hij (ha ▸ hhead.symm ▸ rfl)
      · rw [if_neg ha] at hhead
        have hit : i ∈ t := by
          rcases List.mem_cons.mp h with hai | hit
          · exact absurd hai.symm ha
          · exact hit
        exact holeAt_plug_other hij t hit htail

/-! ## 3. A fresh form with one mentioning instance is always a valid response -/

/-- Derivability of instances on the old forms is unchanged by a fresh form
and one instance on it (generalizes the sealed `derivable_extend`). -/
theorem derivable_fresh {r : Regime} (hwf : r.wf) (a : Nat) (args : List Nat)
    (x : Inst) (hx : x.1 ≠ r.forms.length) :
    derivable ⟨r.data, r.forms ++ [a], r.insts ++ [(r.forms.length, args)], r.rules, r.reqs⟩ x
      ↔ derivable r x := by
  unfold derivable
  constructor
  · intro h
    cases h with
    | inl h =>
        cases List.mem_append.mp h with
        | inl h => exact Or.inl h
        | inr h =>
            exfalso
            have : x = (r.forms.length, args) := List.mem_singleton.mp h
            exact hx (by rw [this])
    | inr h => exact Or.inr h
  · intro h
    cases h with
    | inl h => exact Or.inl (List.mem_append.mpr (Or.inl h))
    | inr h => exact Or.inr h

/-- **At any difference, a fresh form with one instance that mentions the
first datum is a valid response** — for every arity and every argument list
inside the carrier.  The holed context separates the pair; every standing
requirement keeps its witness on the old forms. -/
theorem fresh_form_valid (r : Regime) (hwf : r.wf)
    (hreqs : ∀ q ∈ r.reqs, separable r q.1 q.2)
    (i j : Nat) (hij : i ≠ j)
    (a : Nat) (args : List Nat) (ha : 1 ≤ a) (hlen : args.length = a)
    (hargs : ∀ x ∈ args, x < r.data) (hmem : i ∈ args) :
    validResponse r i j [.newForm a, .newInst r.forms.length args] := by
  have hfresh : ((r.forms.length, args) : Inst) ∉ r.insts := by
    intro hm
    exact Nat.lt_irrefl _ ((hwf.1 _ hm).1)
  have happ : applyDelta r [.newForm a, .newInst r.forms.length args] =
      some ⟨r.data, r.forms ++ [a], r.insts ++ [(r.forms.length, args)], r.rules, r.reqs⟩ := by
    rw [applyDelta_pair]
    have h1 : applyItem r (.newForm a) = some { r with forms := r.forms ++ [a] } := by
      simp only [applyItem]
      rw [if_pos ha]
    have hcond : r.forms.length < (r.forms ++ [a]).length ∧
        args.length = (r.forms ++ [a]).getD r.forms.length 0 ∧
        ∀ x ∈ args, x < r.data := by
      refine ⟨by simp, ?_, hargs⟩
      rw [getD_concat_self]
      exact hlen
    have h2 : applyItem { r with forms := r.forms ++ [a] } (.newInst r.forms.length args) =
        some ⟨r.data, r.forms ++ [a], r.insts ++ [(r.forms.length, args)], r.rules, r.reqs⟩ := by
      simp only [applyItem]
      rw [if_pos hcond]
      simp [insertNew_of_not_mem hfresh]
    rw [h1]
    exact h2
  refine ⟨_, happ, ?_, ?_⟩
  · refine ⟨⟨r.forms.length, holeAt i args⟩, ⟨by simp, ?_, ?_, ?_⟩, ?_⟩
    · show (holeAt i args).length = (r.forms ++ [a]).getD r.forms.length 0
      rw [holeAt_length, getD_concat_self]
      exact hlen
    · exact List.mem_map.mpr ⟨i, hmem, by simp⟩
    · intro s hs
      obtain ⟨x, hx, rfl⟩ := List.mem_map.mp hs
      by_cases h : x = i
      · rw [if_pos h]
        trivial
      · rw [if_neg h]
        exact hargs x hx
    · intro hiff
      have hder_i : derivable
          ⟨r.data, r.forms ++ [a], r.insts ++ [(r.forms.length, args)], r.rules, r.reqs⟩
          (plug ⟨r.forms.length, holeAt i args⟩ i) := by
        rw [plug_holeAt]
        exact Or.inl (List.mem_append.mpr (Or.inr List.mem_cons_self))
      have hder_j := hiff.mp hder_i
      cases hder_j with
      | inl hm =>
          rcases List.mem_append.mp hm with hold | hnew
          · have := (hwf.1 _ hold).1
            exact absurd this (Nat.lt_irrefl _)
          · have heq : plug ⟨r.forms.length, holeAt i args⟩ j = (r.forms.length, args) :=
              List.mem_singleton.mp hnew
            have hargs' : (holeAt i args).map (fun s => s.getD j) = args :=
              congrArg Prod.snd heq
            exact holeAt_plug_other hij args hmem hargs'
      | inr hr =>
          have := hwf.2.1 _ hr
          exact absurd this (Nat.lt_irrefl _)
  · intro q hq
    obtain ⟨c, hwfc, hne⟩ := hreqs q hq
    have hform : c.form ≠ r.forms.length := by
      intro hbad
      exact Nat.lt_irrefl _ (hbad ▸ hwfc.1)
    have hplug : ∀ d, (plug c d).1 ≠ r.forms.length := fun _ => hform
    refine ⟨c, ⟨?_, ?_, hwfc.2.2.1, hwfc.2.2.2⟩, ?_⟩
    · show c.form < (r.forms ++ [a]).length
      have := hwfc.1
      simp
      omega
    · show c.slots.length = (r.forms ++ [a]).getD c.form 0
      rw [getD_append_lt _ _ _ hwfc.1]
      exact hwfc.2.1
    · intro hiff
      apply hne
      constructor
      · intro h
        exact (derivable_fresh hwf a args _ (hplug q.2)).mp
          (hiff.mp ((derivable_fresh hwf a args _ (hplug q.1)).mpr h))
      · intro h
        exact (derivable_fresh hwf a args _ (hplug q.1)).mp
          (hiff.mpr ((derivable_fresh hwf a args _ (hplug q.2)).mpr h))

/-- At any `Good` state and any distinct admitted pair, the unary mark,
binary link and binary self-loop constructions are valid responses. This
does not assert an embedding of classes or of whole response trees. -/
theorem bare_round_embeds (r : Regime) (hg : Good r) (i j : Nat)
    (hi : i < r.data) (hj : j < r.data) (hij : i ≠ j) :
    validResponse r i j [.newForm 1, .newInst r.forms.length [i]] ∧
    validResponse r i j [.newForm 2, .newInst r.forms.length [i, j]] ∧
    validResponse r i j [.newForm 2, .newInst r.forms.length [i, i]] := by
  refine ⟨?_, ?_, ?_⟩
  · refine fresh_form_valid r hg.1 hg.2.2 i j hij 1 [i] (Nat.le_refl 1) rfl ?_ List.mem_cons_self
    intro x hx
    have : x = i := List.mem_singleton.mp hx
    subst this
    exact hi
  · refine fresh_form_valid r hg.1 hg.2.2 i j hij 2 [i, j] (by decide) rfl ?_ List.mem_cons_self
    intro x hx
    rcases List.mem_cons.mp hx with rfl | hx
    · exact hi
    · have : x = j := List.mem_singleton.mp hx
      subst this
      exact hj
  · refine fresh_form_valid r hg.1 hg.2.2 i j hij 2 [i, i] (by decide) rfl ?_ List.mem_cons_self
    intro x hx
    rcases List.mem_cons.mp hx with rfl | hx
    · exact hi
    · have : x = i := List.mem_singleton.mp hx
      subst this
      exact hi

/-! ## 4. Context changes the minimum -/

/-- A state with one unary form marking datum 0; data 1 and 2 are collapsed. -/
def ctxRegime : Regime := ⟨3, [1], [(0, [0])], [], []⟩

theorem ctxRegime_good : Good ctxRegime := by
  refine ⟨?_, rfl, ?_⟩
  · refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [ctxRegime]
  · intro q hq
    cases hq

theorem ctx_collapsed_12 : collapsed ctxRegime 1 2 := by
  intro c hc
  rw [one_unary_form_ctx_char ctxRegime rfl c] at hc
  subst hc
  decide

/-- A one-item response: the existing form marks datum 2. -/
theorem ctx_one_item_valid : validResponse ctxRegime 1 2 [.newInst 0 [2]] := by
  refine ⟨⟨3, [1], [(0, [0]), (0, [2])], [], []⟩, by decide, ?_, ?_⟩
  · exact ⟨⟨0, [none]⟩, by decide, by decide⟩
  · intro q hq
    cases hq

theorem ctx_empty_invalid : ¬ validResponse ctxRegime 1 2 [] := by
  rintro ⟨s, hs, hsep, _⟩
  have : s = ctxRegime := (Option.some.inj hs).symm
  subst this
  exact separable_not_collapsed hsep ctx_collapsed_12

/-- In context the minimum costs one item. -/
theorem ctx_min1 : IsMin .mu1 ctxRegime 1 2 [.newInst 0 [2]] := by
  refine ⟨⟨by decide, ?_⟩, ctx_one_item_valid, ?_⟩
  · intro a ha
    rcases List.mem_cons.mp ha with h | h
    · cases h
    · cases h
  · intro δ' _ hv
    cases δ' with
    | nil => exact absurd hv ctx_empty_invalid
    | cons it rest =>
        show 1 < (it :: rest).length ∨ (1 = (it :: rest).length ∧ 0 ≤ 0)
        cases rest with
        | nil => exact Or.inr ⟨rfl, Nat.le_refl 0⟩
        | cons it2 rest2 =>
            left
            show 1 < rest2.length + 1 + 1
            exact Nat.succ_lt_succ (Nat.succ_pos _)

/-- **Context changes the minimum**: at the bare difference no response of at
most one item is valid (sealed), while at the same difference inside
`ctxRegime` a one-item response is the minimum. -/
theorem context_changes_minimum :
    (∀ δ, δ.length ≤ 1 → ¬ validResponse R2L 0 1 δ) ∧
      IsMin .mu1 ctxRegime 1 2 [.newInst 0 [2]] :=
  ⟨cost1_insufficient, ctx_min1⟩

/-- The seed's mark stays valid in context but is no longer a minimum. -/
theorem bare_mark_not_min_in_context :
    validResponse ctxRegime 1 2 [.newForm 1, .newInst 1 [1]] ∧
      ¬ IsMin .mu1 ctxRegime 1 2 [.newForm 1, .newInst 1 [1]] := by
  refine ⟨(bare_round_embeds ctxRegime ctxRegime_good 1 2 (by decide) (by decide) (by decide)).1, ?_⟩
  intro hmin
  have hle := hmin.2.2 [.newInst 0 [2]] ⟨by decide, fun a ha => by
    rcases List.mem_cons.mp ha with h | h
    · cases h
    · cases h⟩ ctx_one_item_valid
  revert hle
  show ¬ (2 < 1 ∨ (2 = 1 ∧ 0 ≤ 0))
  decide

end Magnification

#print axioms Magnification.induced_eq_R2L
#print axioms Magnification.induced_constant
#print axioms Magnification.induced_wf
#print axioms Magnification.induced_collapsed
#print axioms Magnification.holeAt_length
#print axioms Magnification.holeAt_getD
#print axioms Magnification.holeAt_map_getD
#print axioms Magnification.plug_holeAt
#print axioms Magnification.holeAt_plug_other
#print axioms Magnification.derivable_fresh
#print axioms Magnification.fresh_form_valid
#print axioms Magnification.bare_round_embeds
#print axioms Magnification.ctxRegime_good
#print axioms Magnification.ctx_collapsed_12
#print axioms Magnification.ctx_one_item_valid
#print axioms Magnification.ctx_empty_invalid
#print axioms Magnification.ctx_min1
#print axioms Magnification.context_changes_minimum
#print axioms Magnification.bare_mark_not_min_in_context
