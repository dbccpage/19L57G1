"""Book finite search over native contexts; AuthorityEffect: None."""
SOURCE = r'''
namespace Textbook.ContextSearch
open Derivation

def slotChoices (n : Nat) : List (Option Nat) :=
  none :: (List.range n).map some

theorem mem_slotChoices (n : Nat) (s : Option Nat) :
    s ∈ slotChoices n ↔ slotOk n s := by
  cases s <;> simp [slotChoices, slotOk]

def slotLists (n : Nat) : Nat → List (List (Option Nat))
  | 0 => [[]]
  | a+1 => (slotChoices n).flatMap fun s => (slotLists n a).map (s :: ·)

theorem mem_slotLists (n a : Nat) (xs : List (Option Nat)) :
    xs ∈ slotLists n a ↔ xs.length = a ∧ ∀ s ∈ xs, slotOk n s := by
  induction a generalizing xs with
  | zero =>
    cases xs with
    | nil =>
      constructor
      · intro _
        refine ⟨rfl, ?_⟩
        intro s hs; cases hs
      · intro _; exact List.mem_cons_self
    | cons s ss =>
      constructor
      · intro h
        have heq := List.mem_singleton.mp h
        cases heq
      · intro h; exact False.elim (Nat.noConfusion h.1)
  | succ a ih =>
    cases xs with
    | nil =>
      constructor
      · intro h
        obtain ⟨s, _, hmap⟩ := List.mem_flatMap.mp h
        obtain ⟨ys, _, heq⟩ := List.mem_map.mp hmap
        cases heq
      · intro h; exact False.elim (Nat.noConfusion h.1)
    | cons s ss =>
      simp only [slotLists, List.mem_flatMap, List.mem_map]
      constructor
      · rintro ⟨t, ht, ys, hys, heq⟩
        cases heq
        have hi := (ih ss).mp hys
        constructor
        · exact congrArg Nat.succ hi.1
        · intro z hz
          rcases List.mem_cons.mp hz with hz | hz
          · subst z; exact (mem_slotChoices n s).mp ht
          · exact hi.2 z hz
      · rintro ⟨hlen, hok⟩
        refine ⟨s, (mem_slotChoices n s).mpr (hok s List.mem_cons_self), ss, ?_, rfl⟩
        apply (ih ss).mpr
        constructor
        · exact Nat.succ.inj hlen
        · intro z hz; exact hok z (List.mem_cons_of_mem s hz)

def candidates (r : Regime) : List Ctx :=
  (List.range r.forms.length).flatMap fun f =>
    (slotLists r.data (r.forms.getD f 0)).map fun slots => ⟨f, slots⟩

def allContexts (r : Regime) : List Ctx :=
  (candidates r).filter fun c => decide (wfCtx r c)

theorem allContexts_sound (r : Regime) (c : Ctx) (h : c ∈ allContexts r) :
    wfCtx r c := by
  exact of_decide_eq_true (List.mem_filter.mp h).2

theorem allContexts_complete (r : Regime) (c : Ctx) (h : wfCtx r c) :
    c ∈ allContexts r := by
  apply List.mem_filter.mpr
  constructor
  · apply List.mem_flatMap.mpr
    refine ⟨c.form, List.mem_range.mpr h.1, ?_⟩
    apply List.mem_map.mpr
    exact ⟨c.slots, (mem_slotLists _ _ _).mpr ⟨h.2.1, h.2.2.2⟩, rfl⟩
  · exact decide_eq_true h

def scan (r : Regime) (d e : Nat) : List Ctx → Option Ctx
  | [] => none
  | c :: cs => if derivable r (plug c d) ↔ derivable r (plug c e)
               then scan r d e cs else some c

theorem scan_none_iff (r : Regime) (d e : Nat) (cs : List Ctx) :
    scan r d e cs = none ↔
      ∀ c ∈ cs, (derivable r (plug c d) ↔ derivable r (plug c e)) := by
  induction cs with
  | nil => simp [scan]
  | cons c cs ih =>
    by_cases h : derivable r (plug c d) ↔ derivable r (plug c e)
    · simp [scan, h, ih]
    · simp [scan, h]

theorem scan_some_sound (r : Regime) (d e : Nat) (cs : List Ctx) (c : Ctx)
    (h : scan r d e cs = some c) :
    c ∈ cs ∧ ¬ (derivable r (plug c d) ↔ derivable r (plug c e)) := by
  induction cs with
  | nil => simp [scan] at h
  | cons a cs ih =>
    by_cases ha : derivable r (plug a d) ↔ derivable r (plug a e)
    · simp only [scan, if_pos ha] at h
      have hi := ih h
      exact ⟨List.mem_cons_of_mem a hi.1, hi.2⟩
    · simp only [scan, if_neg ha, Option.some.injEq] at h
      subst c
      exact ⟨List.mem_cons_self, ha⟩

def firstWitness (r : Regime) (d e : Nat) : Option Ctx :=
  scan r d e (allContexts r)

theorem firstWitness_none_iff_collapsed (r : Regime) (d e : Nat) :
    firstWitness r d e = none ↔ collapsed r d e := by
  constructor
  · intro h c hwf
    exact (scan_none_iff r d e _).mp h c (allContexts_complete r c hwf)
  · intro h
    apply (scan_none_iff r d e _).mpr
    intro c hc
    exact h c (allContexts_sound r c hc)

theorem firstWitness_some_sound (r : Regime) (d e : Nat) (c : Ctx)
    (h : firstWitness r d e = some c) :
    wfCtx r c ∧ ¬ (derivable r (plug c d) ↔ derivable r (plug c e)) := by
  have hs := scan_some_sound r d e _ c h
  exact ⟨allContexts_sound r c hs.1, hs.2⟩

theorem separable_of_not_collapsed (r : Regime) (d e : Nat)
    (h : ¬ collapsed r d e) : separable r d e := by
  cases hs : firstWitness r d e with
  | none => exact False.elim (h ((firstWitness_none_iff_collapsed r d e).mp hs))
  | some c => exact ⟨c, firstWitness_some_sound r d e c hs⟩

end Textbook.ContextSearch
'''
NAMES = ('mem_slotChoices', 'mem_slotLists', 'allContexts_sound', 'allContexts_complete',
         'scan_none_iff', 'scan_some_sound', 'firstWitness_none_iff_collapsed',
         'firstWitness_some_sound', 'separable_of_not_collapsed')
SOURCE += '\n' + '\n'.join('#print axioms Textbook.ContextSearch.' + n for n in NAMES) + '\n'
REPORTS = {'Textbook.ContextSearch.' + n: 'depends on axioms: [propext, Quot.sound]' for n in NAMES}
