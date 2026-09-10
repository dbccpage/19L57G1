/-!
# Observe: the represented execution process at finite step scales

Formalizes the step-scale observation of Target A deterministic execution.
At scale `n`, the observer reads the execution tape after `n` deterministic steps:
`obs n s = (iter n s).tape`.

Key constructive theorems:
- Deterministic stepping appends to tape (`next_tape`).
- Prefix compatibility: `obs n s <+: obs (n + 1) s` and `obs m s <+: obs (m + k) s`.
- Fuel independence: `obs n s` is invariant under all fuel amounts ≥ n (`obs_fuel_indep`, `obs_fuel_eq`).
- Determinism of active datum under identical programs (`next_active_det`).
- Lost fuel witness: Tape alone loses fuel; states with fuel 0 and 1 diverge after 1 step (`lost_fuel`).

Axiom boundary: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
AuthorityEffect: None.
-/

namespace Observe

/-! ## 1. Graph representation and state -/

abbrev Inst := Nat × List Nat

def isEdge (f x : Nat) : Inst → Bool
  | (g, [x', _]) => decide (g = f ∧ x' = x)
  | _ => false

def value : Inst → Nat
  | (_, [_, y]) => y
  | _ => 0

def lookup (f x : Nat) (l : List Inst) : Option Nat :=
  (l.find? (isEdge f x)).map value

structure State where
  graph : List Inst
  nops : Nat
  active : Nat
  tape : List Nat
  clock : Nat
  fuel : Nat
deriving Repr

inductive Fired
  | ok (s : State)
  | exhausted
  | noEdge

inductive Terminal
  | halt
  | exhausted
  | refuse
  | branch
deriving DecidableEq, Repr

def enabled (g : List Inst) (nops x k : Nat) : Bool :=
  decide (lookup (3 + nops + k) x g = some x)

def enabledAt (g : List Inst) (nops x : Nat) : List Nat :=
  (List.range nops).filter (fun k => enabled g nops x k)

def fire (s : State) (k : Nat) : Fired :=
  match s.fuel with
  | 0 => .exhausted
  | f + 1 =>
    match lookup (3 + k) s.active s.graph with
    | none => .noEdge
    | some y => .ok ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f⟩

def stepDet (s : State) : Terminal ⊕ State :=
  match enabledAt s.graph s.nops s.active with
  | [] => .inl .halt
  | [k] =>
    match fire s k with
    | .ok s' => .inr s'
    | .exhausted => .inl .exhausted
    | .noEdge => .inl .refuse
  | _ :: _ :: _ => .inl .branch

def next (s : State) : State :=
  match stepDet s with
  | .inr s' => s'
  | .inl _ => s

def iter : Nat → State → State
  | 0, s => s
  | n + 1, s => next (iter n s)

def obs (n : Nat) (s : State) : List Nat := (iter n s).tape

/-! ## 2. Stepping and prefix compatibility -/

theorem fire_exhausted {s : State} {k : Nat} (h : s.fuel = 0) : fire s k = .exhausted := by
  show (match s.fuel with
        | 0 => Fired.exhausted
        | f + 1 => _) = .exhausted
  rw [h]

theorem fire_succ (s : State) (k f : Nat) (hf : s.fuel = f + 1) :
    fire s k = (match lookup (3 + k) s.active s.graph with
                | none => Fired.noEdge
                | some y => Fired.ok ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f⟩) := by
  show (match s.fuel with
        | 0 => Fired.exhausted
        | f' + 1 => _) = _
  rw [hf]

theorem fire_ok {s s' : State} {k : Nat} (h : fire s k = .ok s') :
    lookup (3 + k) s.active s.graph = some s'.active ∧ s'.tape = s.tape ++ [s'.active] ∧
      s'.clock = s.clock + 1 ∧ s.fuel = s'.fuel + 1 ∧ s'.graph = s.graph ∧ s'.nops = s.nops := by
  obtain ⟨f, hf⟩ : ∃ f, s.fuel = f + 1 := by
    cases hfu : s.fuel with
    | zero =>
        rw [fire_exhausted hfu] at h
        cases h
    | succ f => exact ⟨f, rfl⟩
  rw [fire_succ s k f hf] at h
  cases hl : lookup (3 + k) s.active s.graph with
  | none =>
      rw [hl] at h
      cases h
  | some y =>
      rw [hl] at h
      have h' : Fired.ok ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f⟩ = Fired.ok s' := h
      cases h'
      exact ⟨rfl, rfl, rfl, hf, rfl, rfl⟩

theorem stepDet_inr {s s' : State} (h : stepDet s = .inr s') :
    ∃ k, enabledAt s.graph s.nops s.active = [k] ∧ fire s k = .ok s' := by
  revert h
  show (match enabledAt s.graph s.nops s.active with
        | [] => Sum.inl Terminal.halt
        | [k] =>
          match fire s k with
          | .ok s' => Sum.inr s'
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse
        | _ :: _ :: _ => Sum.inl Terminal.branch) = Sum.inr s' → _
  cases he : enabledAt s.graph s.nops s.active with
  | nil =>
      intro h
      cases h
  | cons k rest =>
      cases rest with
      | nil =>
          show (match fire s k with
                | .ok s' => Sum.inr s'
                | .exhausted => Sum.inl Terminal.exhausted
                | .noEdge => Sum.inl Terminal.refuse) = Sum.inr s' → _
          cases hf : fire s k with
          | ok t =>
              intro h
              have h' : Sum.inr t = Sum.inr s' := h
              cases h'
              exact ⟨k, rfl, hf⟩
          | exhausted =>
              intro h
              cases h
          | noEdge =>
              intro h
              cases h
      | cons k' rest' =>
          intro h
          cases h

theorem next_tape (s : State) : s.tape <+: (next s).tape := by
  show s.tape <+: (match stepDet s with | .inr s' => s' | .inl _ => s).tape
  cases hs : stepDet s with
  | inl _ => exact List.prefix_refl _
  | inr s' =>
      obtain ⟨k, -, hf⟩ := stepDet_inr hs
      obtain ⟨-, ht, -, -, -, -⟩ := fire_ok hf
      rw [ht]
      exact List.prefix_append _ _

theorem obs_prefix (n : Nat) (s : State) : obs n s <+: obs (n + 1) s :=
  next_tape (iter n s)

theorem obs_prefix_add (m : Nat) (s : State) : ∀ k, obs m s <+: obs (m + k) s
  | 0 => List.prefix_refl _
  | k + 1 => (obs_prefix_add m s k).trans (obs_prefix (m + k) s)

theorem iter_succ : ∀ (n : Nat) (s : State), iter (n + 1) s = iter n (next s)
  | 0, _ => rfl
  | n + 1, s => by
      show next (iter (n + 1) s) = next (iter n (next s))
      rw [iter_succ n s]

/-! ## 3. Determinism and step cases -/

theorem next_active_det {s t s' t' : State} (hg : s.graph = t.graph) (hn : s.nops = t.nops)
    (ha : s.active = t.active) (hs : stepDet s = .inr s') (ht : stepDet t = .inr t') :
    s'.active = t'.active := by
  obtain ⟨k, hek, hfk⟩ := stepDet_inr hs
  obtain ⟨k', hek', hfk'⟩ := stepDet_inr ht
  rw [hg, hn, ha] at hek
  rw [hek] at hek'
  have hkk : k = k' := List.singleton_inj.mp hek'
  subst hkk
  obtain ⟨hl, -, -, -, -, -⟩ := fire_ok hfk
  obtain ⟨hl', -, -, -, -, -⟩ := fire_ok hfk'
  rw [hg, ha] at hl
  rw [hl] at hl'
  exact Option.some.inj hl'

theorem next_halt {s : State} (he : enabledAt s.graph s.nops s.active = []) : next s = s := by
  have h : stepDet s = Sum.inl Terminal.halt := by
    show (match enabledAt s.graph s.nops s.active with
          | [] => Sum.inl Terminal.halt
          | [k] => _
          | _ :: _ :: _ => Sum.inl Terminal.branch) = Sum.inl Terminal.halt
    rw [he]
  show (match stepDet s with | .inr s' => s' | .inl _ => s) = s
  rw [h]

theorem next_branch {s : State} {a b : Nat} {rest : List Nat}
    (he : enabledAt s.graph s.nops s.active = a :: b :: rest) : next s = s := by
  have h : stepDet s = Sum.inl Terminal.branch := by
    show (match enabledAt s.graph s.nops s.active with
          | [] => Sum.inl Terminal.halt
          | [k] => _
          | _ :: _ :: _ => Sum.inl Terminal.branch) = Sum.inl Terminal.branch
    rw [he]
  show (match stepDet s with | .inr s' => s' | .inl _ => s) = s
  rw [h]

theorem next_exhausted {s : State} {k : Nat} (he : enabledAt s.graph s.nops s.active = [k])
    (hf : s.fuel = 0) : next s = s := by
  have h : stepDet s = Sum.inl Terminal.exhausted := by
    show (match enabledAt s.graph s.nops s.active with
          | [] => Sum.inl Terminal.halt
          | [k] =>
            match fire s k with
            | .ok s' => Sum.inr s'
            | .exhausted => Sum.inl Terminal.exhausted
            | .noEdge => Sum.inl Terminal.refuse
          | _ :: _ :: _ => Sum.inl Terminal.branch) = Sum.inl Terminal.exhausted
    rw [he]
    show (match fire s k with
          | .ok s' => Sum.inr s'
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse) = Sum.inl Terminal.exhausted
    rw [fire_exhausted hf]
  show (match stepDet s with | .inr s' => s' | .inl _ => s) = s
  rw [h]

theorem next_refuse {s : State} {k : Nat} (he : enabledAt s.graph s.nops s.active = [k])
    (hl : lookup (3 + k) s.active s.graph = none) : next s = s := by
  cases hfu : s.fuel with
  | zero => exact next_exhausted he hfu
  | succ f =>
      have h : stepDet s = Sum.inl Terminal.refuse := by
        show (match enabledAt s.graph s.nops s.active with
              | [] => Sum.inl Terminal.halt
              | [k] =>
                match fire s k with
                | .ok s' => Sum.inr s'
                | .exhausted => Sum.inl Terminal.exhausted
                | .noEdge => Sum.inl Terminal.refuse
              | _ :: _ :: _ => Sum.inl Terminal.branch) = Sum.inl Terminal.refuse
        rw [he]
        show (match fire s k with
              | .ok s' => Sum.inr s'
              | .exhausted => Sum.inl Terminal.exhausted
              | .noEdge => Sum.inl Terminal.refuse) = Sum.inl Terminal.refuse
        rw [fire_succ s k f hfu, hl]
      show (match stepDet s with | .inr s' => s' | .inl _ => s) = s
      rw [h]

theorem next_fire {s : State} {k y : Nat} (he : enabledAt s.graph s.nops s.active = [k])
    (hfuel : 0 < s.fuel) (hl : lookup (3 + k) s.active s.graph = some y) :
    next s = ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, s.fuel - 1⟩ := by
  obtain ⟨f, hf⟩ : ∃ f, s.fuel = f + 1 := ⟨s.fuel - 1, by omega⟩
  have h : stepDet s = Sum.inr ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f⟩ := by
    show (match enabledAt s.graph s.nops s.active with
          | [] => Sum.inl Terminal.halt
          | [k] =>
            match fire s k with
            | .ok s' => Sum.inr s'
            | .exhausted => Sum.inl Terminal.exhausted
            | .noEdge => Sum.inl Terminal.refuse
          | _ :: _ :: _ => Sum.inl Terminal.branch) = _
    rw [he]
    show (match fire s k with
          | .ok s' => Sum.inr s'
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse) = _
    rw [fire_succ s k f hf, hl]
  show (match stepDet s with | .inr s' => s' | .inl _ => s) = _
  rw [h]
  have hff : f = s.fuel - 1 := by omega
  rw [hff]

theorem next_fuel (s : State) : s.fuel - 1 ≤ (next s).fuel := by
  show s.fuel - 1 ≤ (match stepDet s with | .inr s' => s' | .inl _ => s).fuel
  cases hs : stepDet s with
  | inl _ => exact Nat.sub_le _ _
  | inr s' =>
      obtain ⟨k, -, hf⟩ := stepDet_inr hs
      obtain ⟨-, -, -, hfuel, -, -⟩ := fire_ok hf
      change s.fuel - 1 ≤ s'.fuel
      omega

/-! ## 4. Fuel independence -/

def Same (s t : State) : Prop :=
  s.graph = t.graph ∧ s.nops = t.nops ∧ s.active = t.active ∧ s.tape = t.tape

theorem same_next {s t : State} (h : Same s t) (hs : 0 < s.fuel) (ht : 0 < t.fuel) :
    Same (next s) (next t) := by
  obtain ⟨hg, hn, ha, htape⟩ := h
  have he : enabledAt t.graph t.nops t.active = enabledAt s.graph s.nops s.active := by
    rw [hg, hn, ha]
  cases hes : enabledAt s.graph s.nops s.active with
  | nil =>
      rw [next_halt hes, next_halt (he.trans hes)]
      exact ⟨hg, hn, ha, htape⟩
  | cons k rest =>
      cases rest with
      | nil =>
          cases hl : lookup (3 + k) s.active s.graph with
          | none =>
              rw [next_refuse hes hl, next_refuse (he.trans hes) (by rw [← hg, ← ha]; exact hl)]
              exact ⟨hg, hn, ha, htape⟩
          | some y =>
              rw [next_fire hes hs hl,
                next_fire (he.trans hes) ht (by rw [← hg, ← ha]; exact hl)]
              exact ⟨hg, hn, rfl, by rw [htape]⟩
      | cons k' rest' =>
          rw [next_branch hes, next_branch (he.trans hes)]
          exact ⟨hg, hn, ha, htape⟩

theorem obs_fuel_indep : ∀ (n : Nat) {s t : State}, Same s t → n ≤ s.fuel → n ≤ t.fuel →
    Same (iter n s) (iter n t)
  | 0, _, _, h, _, _ => h
  | n + 1, s, t, h, hs, ht => by
      rw [iter_succ, iter_succ]
      have hs0 : 0 < s.fuel := by omega
      have ht0 : 0 < t.fuel := by omega
      have hfs : s.fuel - 1 ≤ (next s).fuel := next_fuel s
      have hft : t.fuel - 1 ≤ (next t).fuel := next_fuel t
      have hns : n ≤ (next s).fuel := by omega
      have hnt : n ≤ (next t).fuel := by omega
      exact obs_fuel_indep n (same_next h hs0 ht0) hns hnt

theorem obs_fuel_eq (n : Nat) {s t : State} (h : Same s t) (hs : n ≤ s.fuel) (ht : n ≤ t.fuel) :
    obs n s = obs n t := (obs_fuel_indep n h hs ht).2.2.2

/-! ## 5. Lost fuel witness -/

def cycleGraph : List Inst :=
  [(3, [0, 1]), (3, [1, 2]), (3, [2, 0]),
   (6, [0, 0]), (6, [1, 1]), (6, [2, 2])]

def stateWithFuel (f : Nat) : State :=
  ⟨cycleGraph, 3, 0, [0], 0, f⟩

theorem lost_fuel :
    (stateWithFuel 0).tape = (stateWithFuel 1).tape ∧
      (next (stateWithFuel 0)).tape = [0] ∧
      (next (stateWithFuel 1)).tape = [0, 1] := by
  refine ⟨rfl, ?_, ?_⟩
  · decide
  · decide

end Observe
