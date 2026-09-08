import EngineClass

/-!
# Restart at any state: the class composes, splits, and transports

* `path_append`, `path_split`, `path_append_iff`, `path_cut_unique`: a path
  through a state is exactly a path to it followed by a path from it, and the
  cut state is determined by the recorded list.  `rooted_restart`: the
  engine's rooted class can be restarted at any state it reaches with
  nothing lost, provided the whole state travels; `rooted_iff_path` is the
  same class as a seed round followed by a path.
* `fire_rename`: a datum renaming carries every firing onto a firing of the
  renamed regime, with the same cost, the renamed response and the renamed
  successor — the relation is invariant under the sealed transport action.
  `fire_auto` specializes it to a datum automorphism: the response family at
  an orbit-related pair is the renamed family, which is what the engine's
  quotient by isomorphism relies on.
* `orbitRep_rootL_01`, `orbitRep_rootF_01`, `not_orbitRep_rootF_12`: the
  reading-L seed target is the orbit demand of its root; the reading-F seed
  target `(1, 2)` is not — the engine's first round there is the declared
  seed round, not an orbit step.

AuthorityEffect: None.
-/

namespace Restart

open Derivation EngineClass

/-! ## 1. Paths through a state -/

theorem path_append {m : Measure} {supply : Bool} {r c t : Regime} {l1 l2 : List Regime}
    (h1 : Path m supply r l1 c) (h2 : Path m supply c l2 t) :
    Path m supply r (l1 ++ l2) t := by
  induction h1 with
  | nil => exact h2
  | cons hstep _ ih => exact Path.cons hstep (ih h2)

theorem path_split {m : Measure} {supply : Bool} {r t : Regime} (l1 l2 : List Regime)
    (h : Path m supply r (l1 ++ l2) t) :
    ∃ c, Path m supply r l1 c ∧ Path m supply c l2 t := by
  induction l1 generalizing r with
  | nil => exact ⟨r, Path.nil r, h⟩
  | cons s rest ih =>
      cases h with
      | cons hstep hpath =>
          obtain ⟨c, h1, h2⟩ := ih hpath
          exact ⟨c, Path.cons hstep h1, h2⟩

/-- **Restart is exact**: a path along the concatenated record is a path to
some cut state followed by a path from it. -/
theorem path_append_iff {m : Measure} {supply : Bool} {r t : Regime} (l1 l2 : List Regime) :
    Path m supply r (l1 ++ l2) t ↔ ∃ c, Path m supply r l1 c ∧ Path m supply c l2 t :=
  ⟨path_split l1 l2, fun ⟨_, h1, h2⟩ => path_append h1 h2⟩

/-- The cut state is determined by the recorded list. -/
theorem path_cut_unique {m : Measure} {supply : Bool} {r c c' : Regime} {l : List Regime}
    (h : Path m supply r l c) (h' : Path m supply r l c') : c = c' := by
  induction h generalizing c' with
  | nil =>
      cases h' with
      | nil => rfl
  | cons _ _ ih =>
      cases h' with
      | cons _ hpath' => exact ih hpath'

/-- A rooted state, restarted with any further engine path, is rooted. -/
theorem rooted_restart {m : Measure} {supply : Bool} {root c t : Regime} {tgt : Nat × Nat}
    {l : List Regime} (hc : Rooted m supply root tgt c) (h : Path m supply c l t) :
    Rooted m supply root tgt t := by
  induction h with
  | nil => exact hc
  | cons hstep _ ih => exact ih (Rooted.step hc hstep)

/-- The rooted class is the seed round followed by a path. -/
theorem rooted_iff_path {m : Measure} {supply : Bool} {root t : Regime} {tgt : Nat × Nat} :
    Rooted m supply root tgt t ↔
      ∃ s δ l, Fire m root tgt.1 tgt.2 δ s ∧ Path m supply s l t := by
  constructor
  · intro h
    induction h with
    | seed hfire => exact ⟨_, _, [], hfire, Path.nil _⟩
    | step _ hstep ih =>
        obtain ⟨s, δ, l, hfire, hpath⟩ := ih
        exact ⟨s, δ, l ++ [_], hfire, path_append hpath (Path.cons hstep (Path.nil _))⟩
  · rintro ⟨s, δ, l, hfire, hpath⟩
    exact rooted_restart (Rooted.seed hfire) hpath

/-! ## 2. Transport of firings along the sealed renaming action -/

theorem newForm_mem_map {f : Nat → Nat} {δ : List Item} {a : Nat} :
    Item.newForm a ∈ δ.map (mapItem f) ↔ Item.newForm a ∈ δ := by
  constructor
  · intro h
    obtain ⟨it, hit, heq⟩ := List.mem_map.mp h
    cases it with
    | newForm b =>
        simp only [mapItem] at heq
        injection heq with hba
        subst hba
        exact hit
    | newDatum => simp only [mapItem] at heq; cases heq
    | newInst g args => simp only [mapItem] at heq; cases heq
    | newRuleAll g => simp only [mapItem] at heq; cases heq
  · intro h
    exact List.mem_map.mpr ⟨Item.newForm a, h, rfl⟩

theorem inBounds_map (f : Nat → Nat) {δ : List Item} :
    InBounds (δ.map (mapItem f)) ↔ InBounds δ := by
  unfold InBounds
  rw [mapItem_length]
  constructor
  · rintro ⟨h1, h2⟩
    exact ⟨h1, fun a ha => h2 a (newForm_mem_map.mpr ha)⟩
  · rintro ⟨h1, h2⟩
    exact ⟨h1, fun a ha => h2 a (newForm_mem_map.mp ha)⟩

theorem aritySum_map (f : Nat → Nat) :
    ∀ δ : List Item, aritySum (δ.map (mapItem f)) = aritySum δ
  | [] => rfl
  | .newForm a :: rest => by
      show a + aritySum (rest.map (mapItem f)) = a + aritySum rest
      rw [aritySum_map f rest]
  | .newDatum :: rest => aritySum_map f rest
  | .newInst g args :: rest => aritySum_map f rest
  | .newRuleAll g :: rest => aritySum_map f rest

theorem cost_map (m : Measure) (f : Nat → Nat) (δ : List Item) :
    cost m (δ.map (mapItem f)) = cost m δ := by
  cases m with
  | mu1 =>
      show ((δ.map (mapItem f)).length, 0) = (δ.length, 0)
      rw [mapItem_length]
  | mu2 =>
      show ((δ.map (mapItem f)).length, aritySum (δ.map (mapItem f))) = (δ.length, aritySum δ)
      rw [mapItem_length, aritySum_map]

theorem map_pad_f_g {n : Nat} (σ : DRen n) (δ : List Item) :
    (δ.map (mapItem (padF n σ.g))).map (mapItem (padF n σ.f)) = δ := by
  rw [List.map_map]
  have hcomp : (mapItem (padF n σ.f) ∘ mapItem (padF n σ.g)) = fun it => it :=
    funext (mapItem_pad_f_g σ)
  rw [hcomp, List.map_id']

/-- **A datum renaming carries every firing onto a firing**: the renamed
regime, at the renamed pair, has the renamed response as a minimum of the
same cost, landing on the renamed successor.  The transition part is the
sealed `transStep_rename_fwd`; minimality transports because validity does
(`validResponse_rename`) and the cost is renaming-invariant. -/
theorem fire_rename {n : Nat} (σ : DRen n) {m : Measure} {r t : Regime}
    (hn : r.data = n) (hg : Good r) {i j : Nat} {δ : List Item}
    (h : Fire m r i j δ t) :
    Fire m (renameRegimeR σ.f r) (mapReq σ.f (i, j)).1 (mapReq σ.f (i, j)).2
      (δ.map (mapItem (padF n σ.f))) (renameRegimeR (padF n σ.f) t) := by
  have hinst : ∀ p ∈ r.insts, ∀ a ∈ p.2, a < r.data := fun p hp => (hg.1.1 p hp).2.2
  have hreq : ∀ q ∈ r.reqs, q.1 < q.2 ∧ q.2 < r.data := hg.1.2.2.1
  have hts := transStep_rename_fwd σ r hn hinst hreq (fire_transStep h)
  obtain ⟨hij', hj', hcol', hval', hresp'⟩ := hts
  refine ⟨hij', hj', hcol', ⟨(inBounds_map _).mpr h.2.2.2.1.1, hval', ?_⟩, hresp'⟩
  intro δ' hb' hv'
  have hi : i < r.data := Nat.lt_trans h.1 h.2.1
  have hj : j < r.data := h.2.1
  have hb'' : InBounds (δ'.map (mapItem (padF n σ.g))) := (inBounds_map _).mpr hb'
  have hv2 : validResponse (renameRegimeR σ.f r) (mapReq σ.f (i, j)).1 (mapReq σ.f (i, j)).2
      ((δ'.map (mapItem (padF n σ.g))).map (mapItem (padF n σ.f))) := by
    rw [map_pad_f_g]
    exact hv'
  have hv'' : validResponse r i j (δ'.map (mapItem (padF n σ.g))) := by
    rcases mapReq_cases σ.f (i, j) with hc | hc <;> rw [hc] at hv2
    · exact (validResponse_rename σ r hn hinst hreq hi hj _).mp hv2
    · exact (validResponse_rename σ r hn hinst hreq hi hj _).mp
        ((validResponse_symm _ _ _ _).mp hv2)
  have hle := h.2.2.2.1.2.2 _ hb'' hv''
  have hc1 : cost m (δ'.map (mapItem (padF n σ.g))) = cost m δ' := by
    rw [← cost_map m (padF n σ.f), map_pad_f_g]
  rw [cost_map, ← hc1]
  exact hle

/-- **Equivariance at an automorphism**: when the renaming fixes the regime,
the response family at the image pair is the renamed family and the children
are the renamed children.  This is the relation-level fact the engine's
orbit selection rests on; the selection of the least pair is itself not
congruent (sealed `least_pair_selection_not_congruent`). -/
theorem fire_auto {n : Nat} (σ : DRen n) {m : Measure} {r t : Regime}
    (hn : r.data = n) (hg : Good r) (hauto : renameRegimeR σ.f r = r)
    {i j : Nat} {δ : List Item} (h : Fire m r i j δ t) :
    Fire m r (mapReq σ.f (i, j)).1 (mapReq σ.f (i, j)).2
      (δ.map (mapItem (padF n σ.f))) (renameRegimeR (padF n σ.f) t) := by
  have := fire_rename σ hn hg h
  rw [hauto] at this
  exact this

/-! ## 3. The roots -/

def rootL : Regime := ⟨2, [], [], [], []⟩
def rootF : Regime := ⟨3, [], [], [], []⟩

theorem lexLE_zero_one (q : Nat × Nat) (hq : q.1 < q.2) : lexLE (0, 1) q := by
  show 0 < q.1 ∨ (0 = q.1 ∧ 1 ≤ q.2)
  rcases Nat.eq_zero_or_pos q.1 with h0 | hpos
  · right
    refine ⟨h0.symm, ?_⟩
    rw [h0] at hq
    exact Nat.succ_le_of_lt hq
  · left
    exact hpos

theorem orbitRep_rootL_01 : OrbitRep rootL 0 1 := by
  refine ⟨Nat.zero_lt_one, by decide, collapsed_of_no_insts rootL rfl 0 1, ?_⟩
  intro π _ _
  exact lexLE_zero_one _ (mapReq_ordered π.f_inj Nat.zero_lt_one)

theorem orbitRep_rootF_01 : OrbitRep rootF 0 1 := by
  refine ⟨Nat.zero_lt_one, by decide, collapsed_of_no_insts rootF rfl 0 1, ?_⟩
  intro π _ _
  exact lexLE_zero_one _ (mapReq_ordered π.f_inj Nat.zero_lt_one)

/-- The transposition of the first two data. -/
def sw : Nat → Nat
  | 0 => 1
  | 1 => 0
  | x + 2 => x + 2

theorem sw_invol : ∀ x, sw (sw x) = x
  | 0 => rfl
  | 1 => rfl
  | _ + 2 => rfl

theorem sw_bound : ∀ x, x < 3 → sw x < 3
  | 0, _ => by decide
  | 1, _ => by decide
  | 2, _ => by decide
  | y + 3, h => absurd h (by omega)

def swap01F : DRen 3 := ⟨sw, sw, sw_invol, sw_invol, sw_bound, sw_bound⟩

def idForms0 : DRen 0 := ⟨id, id, fun _ => rfl, fun _ => rfl, fun _ h => h, fun _ h => h⟩

theorem swap01F_auto : IsAuto rootF swap01F idForms0 := by
  show RegimeExt (relab rootF sw id id) rootF
  have h : relab rootF sw id id = rootF := by decide
  rw [h]
  exact RegimeExt.refl' rootF

/-- **The reading-F seed target is not the orbit demand of its root**: the
transposition of the first two data fixes the root and carries `(1, 2)` to
`(0, 2)`, which is lexicographically smaller.  The engine's first round on
reading F is the declared seed round; every later round is an orbit step. -/
theorem not_orbitRep_rootF_12 : ¬ OrbitRep rootF 1 2 := by
  intro h
  have hle := h.2.2.2 swap01F idForms0 swap01F_auto
  revert hle
  decide

end Restart

#print axioms Restart.path_append
#print axioms Restart.path_split
#print axioms Restart.path_append_iff
#print axioms Restart.path_cut_unique
#print axioms Restart.rooted_restart
#print axioms Restart.rooted_iff_path
#print axioms Restart.newForm_mem_map
#print axioms Restart.inBounds_map
#print axioms Restart.aritySum_map
#print axioms Restart.cost_map
#print axioms Restart.map_pad_f_g
#print axioms Restart.fire_rename
#print axioms Restart.fire_auto
#print axioms Restart.lexLE_zero_one
#print axioms Restart.orbitRep_rootL_01
#print axioms Restart.orbitRep_rootF_01
#print axioms Restart.sw_invol
#print axioms Restart.sw_bound
#print axioms Restart.swap01F_auto
#print axioms Restart.not_orbitRep_rootF_12
