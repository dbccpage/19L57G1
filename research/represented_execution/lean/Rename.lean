import Schedule

/-!
# Rename: the machine does not read the names of the data

A datum is a number here only because something had to be written down.  The
question this module answers is whether the machine can tell: if the carrier
is renamed by a permutation, does the run correspond?

A `Renaming` is a map on the carrier with a two-sided inverse there — stated
as four conditions on `Nat → Nat` rather than as a bijection of a subtype, so
that nothing outside the sealed grammar's arithmetic is needed.  It carries a
finite setting to a renamed one (`renameSetting`), a controlled setting to a
renamed one (`renameControlled`), and a state to a renamed one
(`renameState`).

What is proved:

* **The program is renamed, not rebuilt.**  The enablement read at the renamed
  datum is the enablement read at the original (`rename_enabledAt`), and the
  edge leaving it is the renamed edge (`rename_lookup`).
* **One step corresponds** (`rename_stepDet`): the renamed state steps to the
  renamed successor, or stops with the *same* terminal.
* **The whole run corresponds** (`rename_runDet`, `rename_run`): the renamed
  run ends at the same terminal, at the renamed datum, with the renamed tape,
  the same clock and the same fuel.
* **And so the record is the renamed record** (`rename_tape`): presentation
  identity is not internal identity, and the machine reads only the latter.

The failure case is kept beside it: a map that is not a renaming — one whose
inverse misses — carries a run to a run of a *different* program
(`not_a_renaming`).

AuthorityEffect: None.
-/

namespace Rename

open Derivation Translation Execution Control Schedule

/-! ## 1. Renamings, and reading a list at an index -/

/-- A renaming of a carrier of `n` data: a map with a two-sided inverse
there.  Nothing is asked of either map outside the carrier. -/
structure Renaming (n : Nat) where
  fwd : Nat → Nat
  bwd : Nat → Nat
  fwd_lt : ∀ x, x < n → fwd x < n
  bwd_lt : ∀ x, x < n → bwd x < n
  left : ∀ x, x < n → bwd (fwd x) = x
  right : ∀ x, x < n → fwd (bwd x) = x

/-- Reading a mapped list at an index inside it is mapping the reading.  The
defaults are unrelated on purpose: inside the list they are never consulted. -/
theorem getD_map {α β : Type} (f : α → β) (d : α) (e : β) :
    ∀ (l : List α) (k : Nat), k < l.length → (l.map f).getD k e = f (l.getD k d)
  | [], k, hk => absurd hk (Nat.not_lt_zero k)
  | _ :: _, 0, _ => rfl
  | a :: as, k + 1, hk => by
      have hl : (a :: as).length = as.length + 1 := rfl
      have hk' : k < as.length := by omega
      have h1 : ((a :: as).map f).getD (k + 1) e = (as.map f).getD k e := rfl
      have h2 : (a :: as).getD (k + 1) d = as.getD k d := rfl
      rw [h1, h2]
      exact getD_map f d e as k hk'

theorem length_map {α β : Type} (f : α → β) : ∀ (l : List α), (l.map f).length = l.length
  | [] => rfl
  | a :: as => by
      have h : ((a :: as).map f).length = (as.map f).length + 1 := rfl
      have h2 : (a :: as).length = as.length + 1 := rfl
      rw [h, h2, length_map f as]

/-! ## 2. Renaming a setting and a controlled setting -/

/-- The renamed setting: every operation is conjugated by the renaming, every
store is read through its inverse, and the endpoints move. -/
def renameSetting (F : FiniteSetting) (σ : Renaming F.n) : FiniteSetting where
  n := F.n
  rel := fun x y => F.rel (σ.bwd x) (σ.bwd y)
  ret := fun x y => F.ret (σ.bwd x) (σ.bwd y)
  prot := fun x y => F.prot (σ.bwd x) (σ.bwd y)
  a := σ.fwd F.a
  b := σ.fwd F.b
  ops := F.ops.map (fun g x => σ.fwd (g (σ.bwd x)))
  a_lt := σ.fwd_lt _ F.a_lt
  b_lt := σ.fwd_lt _ F.b_lt
  ops_closed := by
    intro h hh x hx
    obtain ⟨g, hg, rfl⟩ := List.mem_map.mp hh
    exact σ.fwd_lt _ (F.ops_closed g hg _ (σ.bwd_lt x hx))

theorem renameSetting_n (F : FiniteSetting) (σ : Renaming F.n) :
    (renameSetting F σ).n = F.n := rfl

theorem renameSetting_ops_length (F : FiniteSetting) (σ : Renaming F.n) :
    (renameSetting F σ).ops.length = F.ops.length := length_map _ F.ops

/-- **An operation of the renamed setting is the renamed operation.** -/
theorem rename_op (F : FiniteSetting) (σ : Renaming F.n) {k x : Nat}
    (hk : k < F.ops.length) (hx : x < F.n) :
    (renameSetting F σ).ops.getD k id (σ.fwd x) = σ.fwd (F.ops.getD k id x) := by
  have hg : (renameSetting F σ).ops.getD k id
      = (fun g x => σ.fwd (g (σ.bwd x))) (F.ops.getD k id) :=
    getD_map _ id id F.ops k hk
  rw [hg]
  show σ.fwd (F.ops.getD k id (σ.bwd (σ.fwd x))) = σ.fwd (F.ops.getD k id x)
  rw [σ.left x hx]

/-- The renamed controlled setting: the renamed carrier, and the enablement
read through the inverse. -/
def renameControlled (C : Controlled) (σ : Renaming C.F.n) : Controlled :=
  ⟨renameSetting C.F σ, fun x k => C.ctrl (σ.bwd x) k⟩

theorem renameControlled_nops (C : Controlled) (σ : Renaming C.F.n) :
    (renameControlled C σ).F.ops.length = C.F.ops.length := renameSetting_ops_length C.F σ

/-! ## 3. The program is renamed, not rebuilt -/

/-- **The enablement read at the renamed datum is the one read at the
original.** -/
theorem rename_enabledAt (C : Controlled) (σ : Renaming C.F.n) {x : Nat} (hx : x < C.F.n) :
    enabledAt (program (renameControlled C σ)) C.F.ops.length (σ.fwd x)
      = enabledAt (program C) C.F.ops.length x := by
  have hlen := renameControlled_nops C σ
  have hfx : σ.fwd x < C.F.n := σ.fwd_lt x hx
  have hcongr : ∀ k ∈ List.range C.F.ops.length,
      enabled (program (renameControlled C σ)) C.F.ops.length (σ.fwd x) k
        = enabled (program C) C.F.ops.length x k := by
    intro k hk
    have hk' : k < C.F.ops.length := List.mem_range.mp hk
    have hleft : enabled (program (renameControlled C σ)) C.F.ops.length (σ.fwd x) k = true
        ↔ C.ctrl (σ.bwd (σ.fwd x)) k = true := by
      rw [← hlen]
      exact enabled_program (renameControlled C σ) (by rw [hlen]; exact hk') hfx
    rw [σ.left x hx] at hleft
    exact bool_of_iff (hleft.trans (enabled_program C hk' hx).symm)
  show (List.range C.F.ops.length).filter
      (fun k => enabled (program (renameControlled C σ)) C.F.ops.length (σ.fwd x) k)
      = (List.range C.F.ops.length).filter
        (fun k => enabled (program C) C.F.ops.length x k)
  exact filter_congr_mem
    (p := fun k => enabled (program (renameControlled C σ)) C.F.ops.length (σ.fwd x) k)
    (q := fun k => enabled (program C) C.F.ops.length x k) (List.range C.F.ops.length) hcongr

/-- **The edge leaving the renamed datum is the renamed edge.** -/
theorem rename_lookup (C : Controlled) (σ : Renaming C.F.n) {k x : Nat}
    (hk : k < C.F.ops.length) (hx : x < C.F.n) :
    lookup (3 + k) (σ.fwd x) (program (renameControlled C σ))
      = some (σ.fwd (C.F.ops.getD k id x)) := by
  have hlen := renameControlled_nops C σ
  have hk' : k < (renameControlled C σ).F.ops.length := by rw [hlen]; exact hk
  have hx' : σ.fwd x < (renameControlled C σ).F.n := σ.fwd_lt x hx
  rw [lookup_program_op (renameControlled C σ) hk' hx']
  show some ((renameSetting C.F σ).ops.getD k id (σ.fwd x)) = _
  rw [rename_op C.F σ hk hx]

/-! ## 4. The state, the step, and the run -/

/-- The renamed state: the renamed program, the renamed datum, the renamed
record.  The clock and the fuel are counts and do not move. -/
def renameState (C : Controlled) (σ : Renaming C.F.n) (s : State) : State :=
  ⟨program (renameControlled C σ), s.nops, σ.fwd s.active, s.tape.map σ.fwd, s.clock, s.fuel⟩

/-- The class of states this transport speaks about: the ones carrying the
program at an admitted datum. -/
def Carried (C : Controlled) (s : State) : Prop :=
  s.graph = program C ∧ s.nops = C.F.ops.length ∧ s.active < C.F.n

theorem carried_init (C : Controlled) {x : Nat} (hx : x < C.F.n) (fuel : Nat) :
    Carried C (Control.init C x fuel) := ⟨rfl, rfl, hx⟩

/-- Firing is renamed: the same operation fires, and the state it reaches is
the renamed state. -/
theorem rename_fire (C : Controlled) (σ : Renaming C.F.n) {s s' : State} {k : Nat}
    (hc : Carried C s) (hk : k < C.F.ops.length) (h : fire s k = .ok s') :
    fire (renameState C σ s) k = .ok (renameState C σ s') ∧ Carried C s' := by
  obtain ⟨hg, hn, hx⟩ := hc
  obtain ⟨hl, htape, hclock, hfuel, hgraph, hnops⟩ := fire_ok h
  rw [hg, lookup_program_op C hk hx] at hl
  have hval : s'.active = C.F.ops.getD k id s.active := (Option.some.inj hl).symm
  have hlt : s'.active < C.F.n := by
    rw [hval]
    exact C.F.ops_closed _ (getD_mem hk) _ hx
  obtain ⟨f, hf⟩ : ∃ f, s.fuel = f + 1 := ⟨s'.fuel, by omega⟩
  have hrf : (renameState C σ s).fuel = f + 1 := hf
  refine ⟨?_, hgraph.trans hg, hnops.trans hn, hlt⟩
  rw [fire_succ (renameState C σ s) k f hrf]
  show (match lookup (3 + k) (σ.fwd s.active) (program (renameControlled C σ)) with
        | none => Fired.noEdge
        | some y => Fired.ok ⟨program (renameControlled C σ), s.nops, y,
            s.tape.map σ.fwd ++ [y], s.clock + 1, f⟩) = .ok (renameState C σ s')
  rw [rename_lookup C σ hk hx, ← hval]
  show Fired.ok ⟨program (renameControlled C σ), s.nops, σ.fwd s'.active,
      s.tape.map σ.fwd ++ [σ.fwd s'.active], s.clock + 1, f⟩ = .ok (renameState C σ s')
  have hst : s'.tape.map σ.fwd = s.tape.map σ.fwd ++ [σ.fwd s'.active] := by
    rw [htape, List.map_append]
    rfl
  show Fired.ok _ = Fired.ok ⟨program (renameControlled C σ), s'.nops, σ.fwd s'.active,
      s'.tape.map σ.fwd, s'.clock, s'.fuel⟩
  have hff : s'.fuel = f := by omega
  rw [hst, hnops, hclock, hff]

/-- **One step corresponds.**  The renamed state steps to the renamed
successor, or stops with the same terminal. -/
theorem rename_stepDet (C : Controlled) (σ : Renaming C.F.n) {s : State} (hc : Carried C s) :
    (∀ t : Terminal, stepDet s = .inl t → stepDet (renameState C σ s) = .inl t) ∧
      (∀ s' : State, stepDet s = .inr s' →
        stepDet (renameState C σ s) = .inr (renameState C σ s') ∧ Carried C s') := by
  obtain ⟨hg, hn, hx⟩ := hc
  have hen : enabledAt (renameState C σ s).graph (renameState C σ s).nops
      (renameState C σ s).active = enabledAt s.graph s.nops s.active := by
    show enabledAt (program (renameControlled C σ)) s.nops (σ.fwd s.active) = _
    rw [hg, hn]
    exact rename_enabledAt C σ hx
  have hstep : stepDet (renameState C σ s) =
      (match enabledAt s.graph s.nops s.active with
        | [] => Sum.inl Terminal.halt
        | [k] =>
          match fire (renameState C σ s) k with
          | .ok t => Sum.inr t
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse
        | _ :: _ :: _ => Sum.inl Terminal.branch) := by
    show (match enabledAt (renameState C σ s).graph (renameState C σ s).nops
            (renameState C σ s).active with
          | [] => Sum.inl Terminal.halt
          | [k] =>
            match fire (renameState C σ s) k with
            | .ok t => Sum.inr t
            | .exhausted => Sum.inl Terminal.exhausted
            | .noEdge => Sum.inl Terminal.refuse
          | _ :: _ :: _ => Sum.inl Terminal.branch) = _
    rw [hen]
  have hplain : stepDet s =
      (match enabledAt s.graph s.nops s.active with
        | [] => Sum.inl Terminal.halt
        | [k] =>
          match fire s k with
          | .ok t => Sum.inr t
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse
        | _ :: _ :: _ => Sum.inl Terminal.branch) := rfl
  cases hes : enabledAt s.graph s.nops s.active with
  | nil =>
      rw [hes] at hstep hplain
      refine ⟨fun t ht => ?_, fun s' hs' => ?_⟩
      · rw [hstep, ← hplain, ht]
      · rw [hplain] at hs'
        cases hs'
  | cons k rest =>
      cases rest with
      | nil =>
          have hk : k < C.F.ops.length := by
            have hkm : k ∈ enabledAt s.graph s.nops s.active := by
              rw [hes]
              exact List.Mem.head []
            rw [hn] at hkm
            exact (mem_enabledAt.mp hkm).1
          rw [hes] at hstep hplain
          have hplain2 : stepDet s = (match fire s k with
                | .ok t => Sum.inr t
                | .exhausted => Sum.inl Terminal.exhausted
                | .noEdge => Sum.inl Terminal.refuse) := hplain
          have hstep2 : stepDet (renameState C σ s) = (match fire (renameState C σ s) k with
                | .ok t => Sum.inr t
                | .exhausted => Sum.inl Terminal.exhausted
                | .noEdge => Sum.inl Terminal.refuse) := hstep
          have hlk : lookup (3 + k) s.active s.graph = some (C.F.ops.getD k id s.active) := by
            rw [hg]
            exact lookup_program_op C hk hx
          cases hfi : fire s k with
          | exhausted =>
              have h0 : s.fuel = 0 := by
                cases hfu : s.fuel with
                | zero => rfl
                | succ f =>
                    rw [fire_succ s k f hfu, hlk] at hfi
                    cases hfi
              have hrf : fire (renameState C σ s) k = .exhausted := fire_exhausted h0
              rw [hfi] at hplain2
              rw [hrf] at hstep2
              refine ⟨fun t ht => ?_, fun s' hs' => ?_⟩
              · rw [hstep2, ← hplain2, ht]
              · rw [hplain2] at hs'
                cases hs'
          | noEdge =>
              cases hfu : s.fuel with
              | zero =>
                  rw [fire_exhausted hfu] at hfi
                  cases hfi
              | succ f =>
                  rw [fire_succ s k f hfu, hlk] at hfi
                  cases hfi
          | ok t =>
              obtain ⟨hrf, hct⟩ := rename_fire C σ ⟨hg, hn, hx⟩ hk hfi
              rw [hfi] at hplain2
              rw [hrf] at hstep2
              refine ⟨fun u hu => ?_, fun s' hs' => ?_⟩
              · rw [hplain2] at hu
                cases hu
              · rw [hplain2] at hs'
                have hts : t = s' := by
                  have h' : Sum.inr t = (Sum.inr s' : Terminal ⊕ State) := hs'
                  injection h'
                subst hts
                exact ⟨hstep2, hct⟩
      | cons k' rest' =>
          rw [hes] at hstep hplain
          refine ⟨fun t ht => ?_, fun s' hs' => ?_⟩
          · rw [hstep, ← hplain, ht]
          · rw [hplain] at hs'
            cases hs'

/-- **The whole run corresponds.** -/
theorem rename_runDet (C : Controlled) (σ : Renaming C.F.n) :
    ∀ (b : Nat) (s : State), Carried C s →
      runDet b (renameState C σ s) = ((runDet b s).1, renameState C σ (runDet b s).2)
  | 0, s, hc => by
      have hone := rename_stepDet C σ hc
      cases hs : stepDet s with
      | inl t =>
          have hr := hone.1 t hs
          show (match stepDet (renameState C σ s) with
                | .inl u => (u, renameState C σ s)
                | .inr _ => (Terminal.exhausted, renameState C σ s)) = _
          rw [hr]
          show (t, renameState C σ s) = ((match stepDet s with
                | .inl u => (u, s)
                | .inr _ => (Terminal.exhausted, s)).1,
              renameState C σ (match stepDet s with
                | .inl u => (u, s)
                | .inr _ => (Terminal.exhausted, s)).2)
          rw [hs]
      | inr s' =>
          obtain ⟨hr, -⟩ := hone.2 s' hs
          show (match stepDet (renameState C σ s) with
                | .inl u => (u, renameState C σ s)
                | .inr _ => (Terminal.exhausted, renameState C σ s)) = _
          rw [hr]
          show (Terminal.exhausted, renameState C σ s) = ((match stepDet s with
                | .inl u => (u, s)
                | .inr _ => (Terminal.exhausted, s)).1,
              renameState C σ (match stepDet s with
                | .inl u => (u, s)
                | .inr _ => (Terminal.exhausted, s)).2)
          rw [hs]
  | b + 1, s, hc => by
      have hone := rename_stepDet C σ hc
      cases hs : stepDet s with
      | inl t =>
          have hr := hone.1 t hs
          show (match stepDet (renameState C σ s) with
                | .inl u => (u, renameState C σ s)
                | .inr t' => runDet b t') = _
          rw [hr]
          show (t, renameState C σ s) = ((match stepDet s with
                | .inl u => (u, s)
                | .inr t' => runDet b t').1,
              renameState C σ (match stepDet s with
                | .inl u => (u, s)
                | .inr t' => runDet b t').2)
          rw [hs]
      | inr s' =>
          obtain ⟨hr, hcs⟩ := hone.2 s' hs
          show (match stepDet (renameState C σ s) with
                | .inl u => (u, renameState C σ s)
                | .inr t' => runDet b t') = _
          rw [hr]
          show runDet b (renameState C σ s') = ((match stepDet s with
                | .inl u => (u, s)
                | .inr t' => runDet b t').1,
              renameState C σ (match stepDet s with
                | .inl u => (u, s)
                | .inr t' => runDet b t').2)
          rw [hs]
          exact rename_runDet C σ b s' hcs

/-- **The renamed run of the renamed program is the renamed run.**  Same
terminal, same clock, same fuel; the datum and the record are renamed and
nothing else is. -/
theorem rename_run (C : Controlled) (σ : Renaming C.F.n) {x : Nat} (hx : x < C.F.n) (fuel : Nat) :
    Control.run (Control.init (renameControlled C σ) (σ.fwd x) fuel)
      = ((Control.run (Control.init C x fuel)).1,
        renameState C σ (Control.run (Control.init C x fuel)).2) := by
  have hinit : Control.init (renameControlled C σ) (σ.fwd x) fuel
      = renameState C σ (Control.init C x fuel) := by
    show (⟨program (renameControlled C σ), (renameControlled C σ).F.ops.length, σ.fwd x,
        [σ.fwd x], 0, fuel⟩ : State) = _
    rw [renameControlled_nops C σ]
    rfl
  show runDet (Control.init (renameControlled C σ) (σ.fwd x) fuel).fuel _ = _
  rw [hinit]
  exact rename_runDet C σ fuel (Control.init C x fuel) (carried_init C hx fuel)

/-- **The record is the renamed record.** -/
theorem rename_tape (C : Controlled) (σ : Renaming C.F.n) {x : Nat} (hx : x < C.F.n) (fuel : Nat) :
    (Control.run (Control.init (renameControlled C σ) (σ.fwd x) fuel)).2.tape
      = (Control.run (Control.init C x fuel)).2.tape.map σ.fwd := by
  rw [rename_run C σ hx fuel]
  rfl

/-! ## 5. The failure case: a map that is not a renaming -/

/-- The collapse of the two-point carrier onto `0`: it is not a renaming,
because its inverse misses. -/
def collapse : Nat → Nat := fun _ => 0

/-- **The inverse is what does the work.**  No map is a two-sided inverse of
the collapse on two data: whatever it answers at `0`, one of the two data is
not returned. -/
theorem not_a_renaming (bwd : Nat → Nat) : ¬ (∀ x, x < 2 → bwd (collapse x) = x) := by
  intro h
  have h0 : bwd 0 = 0 := h 0 (by decide)
  have h1 : bwd 0 = 1 := h 1 (by decide)
  rw [h0] at h1
  cases h1

/-- And the transport genuinely needs it: `rename_run` is stated for a
`Renaming`, and the two-point flip is one. -/
def flipRenaming : Renaming 2 where
  fwd := Product.flip
  bwd := Product.flip
  fwd_lt := fun x _ => flip_lt x
  bwd_lt := fun x _ => flip_lt x
  left := by decide
  right := by decide

theorem flip_renames_the_solo_run :
    (Control.run (Control.init (renameControlled solo flipRenaming) 1 2)).2.tape
      = (Control.run (Control.init solo 0 2)).2.tape.map Product.flip :=
  rename_tape solo flipRenaming (x := 0) (by decide) 2

end Rename

#print axioms Rename.getD_map
#print axioms Rename.length_map
#print axioms Rename.renameSetting_n
#print axioms Rename.renameSetting_ops_length
#print axioms Rename.rename_op
#print axioms Rename.renameControlled_nops
#print axioms Rename.rename_enabledAt
#print axioms Rename.rename_lookup
#print axioms Rename.carried_init
#print axioms Rename.rename_fire
#print axioms Rename.rename_stepDet
#print axioms Rename.rename_runDet
#print axioms Rename.rename_run
#print axioms Rename.rename_tape
#print axioms Rename.not_a_renaming
#print axioms Rename.flip_renames_the_solo_run
