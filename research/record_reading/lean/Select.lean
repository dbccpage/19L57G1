import Record

/-!
# Select: a class of laws and a discriminating input

The observed family named its next obstacle: the model-selection and
measurement burden.  This module states what the tape observation of the
represented process can and cannot identify.

* **What the observation identifies.**  One step of the merged runner is
  fixed by the *next value* at the active datum — the value of the one
  enabled operation, or none (`nextValue`, `stepDet_spec`).  Two states with
  the same next-value function, active datum, record and fuel have the same
  observation at every scale (`obs_bisim`).  So the tape identifies a law
  only up to its next-value function: which operation carried the datum
  is not observed.
* **A genuine ambiguity in the class.**  On the observed family's setting,
  the program that enables the cycle everywhere and the program that
  enables the climb at datum 0 instead differ as programs
  (`forever_differ`) and are indistinguishable from every start, at every
  fuel and every scale (`forever_indistinguishable`): both carry 0 to 1.
  No start datum and no scale separates them; a different observable
  would be needed.  That is the missing axiom, exhibited.
* **A discriminating input.**  A record-reading program that agrees with
  the lifted cycle-everywhere program from datum 0 up to scale 3
  (`turncoat_agrees`) is separated at scale 4 (`turncoat_differs_scale`)
  and from start datum 2 at scale 2 (`turncoat_differs_start`): the
  observation that was seen does not select the law; a further input does.
* **The finest scale suffices.**  The observation at a scale is the prefix
  of the observation at any finer one (`obs_take`), so a class is searched
  by its finest observation alone.

AuthorityEffect: None.
-/

namespace Select

open Derivation Translation Execution Control Observe

/-! ## 1. What one step reads -/

/-- The value the runner moves to at datum `x` on program `g`: the value of
the one enabled operation, or none when none, two, or no edge. -/
def nextValue (g : List Inst) (nops x : Nat) : Option Nat :=
  match enabledAt g nops x with
  | [k] => lookup (3 + k) x g
  | _ => none

/-- **One step, by the next value.**  Either the runner stops — no fuel or no
next value — or it moves to the next value, appending it to the record. -/
theorem stepDet_spec (s : State) :
    ((s.fuel = 0 ∨ nextValue s.graph s.nops s.active = none) ∧ ∃ t, stepDet s = .inl t) ∨
      ∃ f y, s.fuel = f + 1 ∧ nextValue s.graph s.nops s.active = some y ∧
        stepDet s = .inr ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f⟩ := by
  have hstep : stepDet s = (match enabledAt s.graph s.nops s.active with
        | [] => Sum.inl Terminal.halt
        | [k] =>
          match fire s k with
          | .ok s' => Sum.inr s'
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse
        | _ :: _ :: _ => Sum.inl Terminal.branch) := rfl
  have hval : nextValue s.graph s.nops s.active = (match enabledAt s.graph s.nops s.active with
        | [k] => lookup (3 + k) s.active s.graph
        | _ => none) := rfl
  rw [hstep, hval]
  cases enabledAt s.graph s.nops s.active with
  | nil => exact Or.inl ⟨Or.inr rfl, Terminal.halt, rfl⟩
  | cons k rest =>
      cases rest with
      | nil =>
          show ((s.fuel = 0 ∨ lookup (3 + k) s.active s.graph = none) ∧
                ∃ t, (match fire s k with
                      | .ok s' => Sum.inr s'
                      | .exhausted => Sum.inl Terminal.exhausted
                      | .noEdge => Sum.inl Terminal.refuse) = Sum.inl t) ∨
              ∃ f y, s.fuel = f + 1 ∧ lookup (3 + k) s.active s.graph = some y ∧
                (match fire s k with
                 | .ok s' => Sum.inr s'
                 | .exhausted => Sum.inl Terminal.exhausted
                 | .noEdge => Sum.inl Terminal.refuse) =
                  Sum.inr ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f⟩
          cases hfu : s.fuel with
          | zero =>
              rw [fire_exhausted hfu]
              exact Or.inl ⟨Or.inl rfl, Terminal.exhausted, rfl⟩
          | succ f =>
              rw [fire_succ s k f hfu]
              cases lookup (3 + k) s.active s.graph with
              | none => exact Or.inl ⟨Or.inr rfl, Terminal.refuse, rfl⟩
              | some y => exact Or.inr ⟨f, y, rfl, rfl, rfl⟩
      | cons k' rest' => exact Or.inl ⟨Or.inr rfl, Terminal.branch, rfl⟩

theorem next_of_inl {s : State} {t : Terminal} (h : stepDet s = .inl t) : next s = s := by
  show (match stepDet s with | .inr s' => s' | .inl _ => s) = s
  rw [h]

theorem next_of_inr {s s' : State} (h : stepDet s = .inr s') : next s = s' := by
  show (match stepDet s with | .inr s' => s' | .inl _ => s) = s'
  rw [h]

/-! ## 2. The observation identifies the next-value function, and no more -/

/-- Two states that agree on the next-value function, the active datum, the
record and the fuel. -/
def Rel (s t : State) : Prop :=
  (∀ x, nextValue s.graph s.nops x = nextValue t.graph t.nops x) ∧
    s.active = t.active ∧ s.tape = t.tape ∧ s.fuel = t.fuel

theorem rel_next {s t : State} (h : Rel s t) : Rel (next s) (next t) := by
  obtain ⟨hv, ha, htape, hf⟩ := h
  have hvt : nextValue t.graph t.nops t.active = nextValue s.graph s.nops s.active := by
    rw [hv s.active, ha]
  rcases stepDet_spec s with ⟨hs0, ts, hs⟩ | ⟨f, y, hsf, hsv, hs⟩ <;>
    rcases stepDet_spec t with ⟨ht0, tt, ht⟩ | ⟨f', y', htf, htv, ht⟩
  · rw [next_of_inl hs, next_of_inl ht]
    exact ⟨hv, ha, htape, hf⟩
  · exfalso
    rcases hs0 with hs0 | hs0
    · omega
    · rw [hvt, hs0] at htv
      cases htv
  · exfalso
    rcases ht0 with ht0 | ht0
    · omega
    · rw [hvt, hsv] at ht0
      cases ht0
  · rw [next_of_inr hs, next_of_inr ht]
    have hff : f = f' := by omega
    have hyy : y = y' := by
      rw [hvt, hsv] at htv
      exact Option.some.inj htv
    subst hff
    subst hyy
    exact ⟨hv, rfl, by rw [htape], rfl⟩

theorem rel_iter {s t : State} (h : Rel s t) : ∀ n, Rel (iter n s) (iter n t)
  | 0 => h
  | n + 1 => rel_next (rel_iter h n)

/-- **Bisimulation.**  Same next-value function, active datum, record and
fuel: same observation at every scale. -/
theorem obs_bisim {s t : State} (h : Rel s t) (n : Nat) : obs n s = obs n t :=
  (rel_iter h n).2.2.1

/-- The finest scale suffices: a coarser observation is the prefix of a
finer one, of its own length. -/
theorem obs_take (m k : Nat) (s : State) : obs m s = (obs (m + k) s).take (obs m s).length :=
  List.prefix_iff_eq_take.mp (obs_prefix_add m s k)

/-! ## 3. The ambiguity: which operation carried the datum is not observed -/

/-- Outside the carrier nothing is enabled. -/
theorem enabledAt_ge (C : Controlled) {x : Nat} (hx : C.F.n ≤ x) :
    enabledAt (program C) C.F.ops.length x = [] := by
  cases he : enabledAt (program C) C.F.ops.length x with
  | nil => rfl
  | cons k rest =>
      exfalso
      have hk : k ∈ enabledAt (program C) C.F.ops.length x := by
        rw [he]
        exact List.mem_cons.mpr (Or.inl rfl)
      obtain ⟨-, hen⟩ := mem_enabledAt.mp hk
      have hmem := lookup_mem (enabled_iff.mp hen)
      rcases mem_program.mp hmem with ⟨_, _, x', hx', h⟩ | ⟨_, _, x', hx', _, h⟩
      · injection h with _ h2
        obtain ⟨rfl, _⟩ := list_two_inj h2
        omega
      · injection h with _ h2
        obtain ⟨rfl, _⟩ := list_two_inj h2
        omega

theorem nextValue_ge (C : Controlled) {x : Nat} (hx : C.F.n ≤ x) :
    nextValue (program C) C.F.ops.length x = none := by
  show (match enabledAt (program C) C.F.ops.length x with
        | [k] => lookup (3 + k) x (program C)
        | _ => none) = none
  rw [enabledAt_ge C hx]

/-- The climb at datum 0 and the cycle at 1 and 2. -/
def climbFirst : Controlled :=
  ⟨base, fun x k => decide ((x = 0 ∧ k = 2) ∨ (x ≠ 0 ∧ k = 0))⟩

/-- The two programs differ. -/
theorem forever_differ : program forever ≠ program climbFirst := by decide

/-- And have the same next value at every datum: both carry 0 to 1. -/
theorem forever_ambiguous : ∀ x, nextValue (program forever) 3 x = nextValue (program climbFirst) 3 x := by
  intro x
  cases Nat.lt_or_ge x 3 with
  | inl hx =>
      revert x
      decide
  | inr hx =>
      show nextValue (program forever) forever.F.ops.length x =
        nextValue (program climbFirst) climbFirst.F.ops.length x
      rw [nextValue_ge forever hx, nextValue_ge climbFirst hx]

/-- **The missing axiom, exhibited.**  From every start datum, at every fuel
and every scale, the two programs have the same observation: the tape does
not say which operation carried the datum. -/
theorem forever_indistinguishable (x fuel n : Nat) :
    obs n (Control.init forever x fuel) = obs n (Control.init climbFirst x fuel) :=
  obs_bisim (s := Control.init forever x fuel) (t := Control.init climbFirst x fuel)
    ⟨fun y => forever_ambiguous y, rfl, rfl, rfl⟩ n

/-! ## 4. A discriminating input -/

/-- The cycle everywhere, except after 2 at datum 0, where the constant map
fires: agrees with the lifted `forever` until the record shows `2, 0`. -/
def turncoat : Record.Recorded :=
  ⟨base, fun p x k => decide (if p = 2 ∧ x = 0 then k = 1 else k = 0)⟩

theorem turncoat_agrees :
    Record.robs 3 (Record.rinit turncoat 0 6) = Record.robs 3 (Record.rinit (Record.lift forever) 0 6) := by
  decide

theorem turncoat_differs_scale :
    Record.robs 4 (Record.rinit turncoat 0 6) ≠ Record.robs 4 (Record.rinit (Record.lift forever) 0 6) := by
  decide

theorem turncoat_differs_start :
    Record.robs 2 (Record.rinit turncoat 2 6) ≠ Record.robs 2 (Record.rinit (Record.lift forever) 2 6) := by
  decide

end Select

#print axioms Select.stepDet_spec
#print axioms Select.next_of_inl
#print axioms Select.next_of_inr
#print axioms Select.rel_next
#print axioms Select.rel_iter
#print axioms Select.obs_bisim
#print axioms Select.obs_take
#print axioms Select.enabledAt_ge
#print axioms Select.nextValue_ge
#print axioms Select.forever_differ
#print axioms Select.forever_ambiguous
#print axioms Select.forever_indistinguishable
#print axioms Select.turncoat_agrees
#print axioms Select.turncoat_differs_scale
#print axioms Select.turncoat_differs_start
