import Chain

/-!
# Observe.Periodic: eventual periodicity, formalised

A tape functional along the whole run on a finite carrier is eventually
periodic.  Every ledger in this family called that "the standard consequence"
and left it unstated; this states it.

Nothing is cited.  The pigeonhole is proved here, constructively: the census of
reliance refuses the standard library's classical lemmas, and this package
consumes no finite-set library.

AuthorityEffect: None.
-/

namespace Observe

open Derivation Translation Execution Control Product Schedule Runner

/-! ## 5. Eventual periodicity, formalised

A tape functional along the whole run (`obs_functional`) on a finite carrier
is eventually periodic.  Every ledger in this family has called that "the
standard consequence" and left it unstated; this states it.

Nothing is cited.  The pigeonhole is proved here, constructively: the census
of reliance refuses the standard library's classical lemmas, and this package
consumes no finite-set library.  The datum sequence is identified with the
orbit of one function on the carrier — the value the runner moves to, with
the datum itself wherever it stops — and the orbit of a function on `n` data
repeats within `n` steps. -/

/-- Whether some `i` at most `m` has `f i = v`.  Decided by recursion rather
than by a bounded-quantifier instance, so the proof term is visible. -/
theorem find_eq : ∀ (m : Nat) (f : Nat → Nat) (v : Nat),
    (∃ i, i ≤ m ∧ f i = v) ∨ (∀ i, i ≤ m → f i ≠ v)
  | 0, f, v => by
      rcases Nat.decEq (f 0) v with hne | heq
      · refine Or.inr (fun i hi => ?_)
        have hi0 : i = 0 := Nat.le_zero.mp hi
        rw [hi0]
        exact hne
      · exact Or.inl ⟨0, Nat.le_refl 0, heq⟩
  | m + 1, f, v => by
      rcases find_eq m f v with ⟨i, hi, he⟩ | hno
      · exact Or.inl ⟨i, Nat.le_succ_of_le hi, he⟩
      · rcases Nat.decEq (f (m + 1)) v with hne | heq
        · refine Or.inr (fun i hi hfi => ?_)
          rcases Nat.lt_or_ge i (m + 1) with hlt | hge
          · exact hno i (by omega) hfi
          · have him : i = m + 1 := by omega
            rw [him] at hfi
            exact hne hfi
        · exact Or.inl ⟨m + 1, Nat.le_refl _, heq⟩

/-- **Pigeonhole.**  `n + 1` values below `n` repeat. -/
theorem pigeon : ∀ (n : Nat) (f : Nat → Nat), (∀ i, i ≤ n → f i < n) →
    ∃ i j, i < j ∧ j ≤ n ∧ f i = f j
  | 0, f, h => absurd (h 0 (Nat.le_refl 0)) (Nat.not_lt_zero _)
  | n + 1, f, h => by
      rcases find_eq n f (f (n + 1)) with ⟨i, hi, he⟩ | hno
      · exact ⟨i, n + 1, by omega, Nat.le_refl _, he⟩
      · have hbound : ∀ i, i ≤ n → (if f i < f (n + 1) then f i else f i - 1) < n := by
          intro i hi
          have hfi : f i < n + 1 := h i (by omega)
          have hne : f i ≠ f (n + 1) := hno i hi
          have hv : f (n + 1) < n + 1 := h (n + 1) (Nat.le_refl _)
          rcases Nat.lt_or_ge (f i) (f (n + 1)) with hlt | hge
          · rw [if_pos hlt]
            omega
          · rw [if_neg (by omega)]
            omega
        obtain ⟨i, j, hij, hjn, hgij⟩ :=
          pigeon n (fun i => if f i < f (n + 1) then f i else f i - 1) hbound
        refine ⟨i, j, hij, by omega, ?_⟩
        have hfi : f i < n + 1 := h i (by omega)
        have hfj : f j < n + 1 := h j (by omega)
        have hnei : f i ≠ f (n + 1) := hno i (by omega)
        have hnej : f j ≠ f (n + 1) := hno j (by omega)
        have hg : (if f i < f (n + 1) then f i else f i - 1)
            = (if f j < f (n + 1) then f j else f j - 1) := hgij
        rcases Nat.lt_or_ge (f i) (f (n + 1)) with hi1 | hi2
        · rcases Nat.lt_or_ge (f j) (f (n + 1)) with hj1 | hj2
          · rw [if_pos hi1, if_pos hj1] at hg
            exact hg
          · rw [if_pos hi1, if_neg (by omega)] at hg
            omega
        · rcases Nat.lt_or_ge (f j) (f (n + 1)) with hj1 | hj2
          · rw [if_neg (by omega), if_pos hj1] at hg
            omega
          · rw [if_neg (by omega), if_neg (by omega)] at hg
            omega

/-- The orbit of a function from a datum. -/
def orbit (g : Nat → Nat) (x : Nat) : Nat → Nat
  | 0 => x
  | t + 1 => g (orbit g x t)

theorem orbit_add (g : Nat → Nat) (x a : Nat) :
    ∀ b, orbit g x (a + b) = orbit g (orbit g x a) b
  | 0 => rfl
  | b + 1 => by
      show g (orbit g x (a + b)) = g (orbit g (orbit g x a) b)
      rw [orbit_add g x a b]

theorem orbit_lt {g : Nat → Nat} {n x : Nat} (hx : x < n) (hg : ∀ y, y < n → g y < n) :
    ∀ t, orbit g x t < n
  | 0 => hx
  | t + 1 => hg _ (orbit_lt hx hg t)

/-- **An orbit on `n` data is eventually periodic**, with preperiod and period
together at most `n`. -/
theorem eventually_periodic {g : Nat → Nat} {n x : Nat} (hx : x < n)
    (hg : ∀ y, y < n → g y < n) :
    ∃ i k, 0 < k ∧ i + k ≤ n ∧ ∀ t, orbit g x (i + k + t) = orbit g x (i + t) := by
  obtain ⟨i, j, hij, hjn, he⟩ := pigeon n (orbit g x) (fun t _ => orbit_lt hx hg t)
  refine ⟨i, j - i, by omega, by omega, fun t => ?_⟩
  have hik : i + (j - i) = j := by omega
  rw [hik, orbit_add g x j t, orbit_add g x i t, he]

/-- The next value read off the program, or the datum where the runner
stops.  A total function on the carrier, which is what an orbit needs. -/
def nextVal (g : List Inst) (nops x : Nat) : Nat := (nextOf g nops x).getD x

theorem nextOf_eq_lookup {g : List Inst} {nops x k : Nat} (he : enabledAt g nops x = [k]) :
    nextOf g nops x = lookup (3 + k) x g := by
  show (match enabledAt g nops x with | [k] => lookup (3 + k) x g | _ => none) = _
  rw [he]

/-- **The next value keeps the carrier.**  Where the runner moves it moves
along an operation edge, and where it stops it stays. -/
theorem nextVal_lt (C : Controlled) {y : Nat} (hy : y < C.F.n) :
    nextVal (program C) C.F.ops.length y < C.F.n := by
  have hu : nextVal (program C) C.F.ops.length y =
      (nextOf (program C) C.F.ops.length y).getD y := rfl
  cases hv : nextOf (program C) C.F.ops.length y with
  | none =>
      rw [hu, hv]
      exact hy
  | some z =>
      rw [hu, hv]
      show z < C.F.n
      obtain ⟨k, he, hl⟩ := nextOf_some hv
      have hkmem : k ∈ enabledAt (program C) C.F.ops.length y := by
        rw [he]
        exact List.Mem.head []
      have hk : k < C.F.ops.length := (mem_enabledAt.mp hkmem).1
      have hmem : ((3 + k : Nat), [y, z]) ∈ program C := lookup_mem hl
      rcases mem_program.mp hmem with ⟨k', hk', y', hy', heq⟩ | ⟨k', -, y', -, -, heq⟩
      · injection heq with h1 h2
        have hkk : k' = k := by omega
        subst hkk
        obtain ⟨hyy, hzz⟩ := list_two_inj h2
        subst hyy
        subst hzz
        exact C.F.ops_closed _ (getD_mem hk') _ hy'
      · injection heq with h1 _
        omega

/-- One step with fuel moves the datum to the next value. -/
theorem next_active (s : State) (hf : 0 < s.fuel) :
    (next s).active = nextVal s.graph s.nops s.active := by
  have hu : nextVal s.graph s.nops s.active =
      (nextOf s.graph s.nops s.active).getD s.active := rfl
  cases hes : enabledAt s.graph s.nops s.active with
  | nil =>
      have hn : nextOf s.graph s.nops s.active = none := by
        show (match enabledAt s.graph s.nops s.active with
              | [k] => lookup (3 + k) s.active s.graph | _ => none) = none
        rw [hes]
      rw [next_halt hes, hu, hn]
      rfl
  | cons k rest =>
      cases rest with
      | nil =>
          cases hl : lookup (3 + k) s.active s.graph with
          | none =>
              rw [next_refuse hes hl, hu, nextOf_eq_lookup hes, hl]
              rfl
          | some y =>
              rw [next_fire hes hf hl, hu, nextOf_eq_lookup hes, hl]
              rfl
      | cons k' rest' =>
          have hn : nextOf s.graph s.nops s.active = none := by
            show (match enabledAt s.graph s.nops s.active with
                  | [k] => lookup (3 + k) s.active s.graph | _ => none) = none
            rw [hes]
          rw [next_branch hes, hu, hn]
          rfl

/-- **The datum after `n` steps is the orbit at `n`**, while the fuel lasts. -/
theorem iter_active : ∀ (n : Nat) (s : State), n ≤ s.fuel →
    (iter n s).active = orbit (nextVal s.graph s.nops) s.active n
  | 0, _, _ => rfl
  | n + 1, s, hn => by
      rw [iter_succ]
      have hf : 0 < s.fuel := by omega
      obtain ⟨hg, hnn⟩ := next_graph s
      have hspare := next_fuel s
      have hfuel : n ≤ (next s).fuel := by omega
      have hshift : orbit (nextVal s.graph s.nops) (nextVal s.graph s.nops s.active) n
          = orbit (nextVal s.graph s.nops) s.active (n + 1) := by
        have h1 : orbit (nextVal s.graph s.nops) s.active (1 + n)
            = orbit (nextVal s.graph s.nops) (orbit (nextVal s.graph s.nops) s.active 1) n :=
          orbit_add _ _ 1 n
        rw [Nat.add_comm 1 n] at h1
        exact h1.symm
      rw [iter_active n (next s) hfuel, hg, hnn, next_active s hf, hshift]

/-- **Eventual periodicity of a run.**  On a finite carrier the datum a run is
at repeats: there are a preperiod and a positive period, together at most the
carrier size, after which every later step revisits the datum a period
earlier.  This is the consequence the family's ledgers called standard and
left unstated. -/
theorem eventually_periodic_run (C : Controlled) (x fuel : Nat) (hx : x < C.F.n) :
    ∃ i k, 0 < k ∧ i + k ≤ C.F.n ∧ ∀ t, i + k + t ≤ fuel →
      (iter (i + k + t) (Control.init C x fuel)).active
        = (iter (i + t) (Control.init C x fuel)).active := by
  obtain ⟨i, k, hk, hik, hper⟩ :=
    eventually_periodic (g := nextVal (program C) C.F.ops.length) hx
      (fun y hy => nextVal_lt C hy)
  refine ⟨i, k, hk, hik, fun t ht => ?_⟩
  have hfu : (Control.init C x fuel).fuel = fuel := rfl
  rw [iter_active (i + k + t) (Control.init C x fuel) (by omega),
    iter_active (i + t) (Control.init C x fuel) (by omega)]
  exact hper t

/-- And the observation ends on that datum, so the two tapes end on the same
entry: the periodicity is visible in the record and not only in the state. -/
theorem obs_last_repeats (C : Controlled) (x fuel : Nat) (hx : x < C.F.n) :
    ∃ i k, 0 < k ∧ i + k ≤ C.F.n ∧ ∀ t, i + k + t ≤ fuel →
      (obs (i + k + t) (Control.init C x fuel)).getLast?
        = (obs (i + t) (Control.init C x fuel)).getLast? := by
  obtain ⟨i, k, hk, hik, hper⟩ := eventually_periodic_run C x fuel hx
  refine ⟨i, k, hk, hik, fun t ht => ?_⟩
  have hstart := init_chain C x fuel
  have hone := (iter_chain (i + k + t) (Control.init C x fuel) hstart.1 hstart.2).2
  have htwo := (iter_chain (i + t) (Control.init C x fuel) hstart.1 hstart.2).2
  show (iter (i + k + t) (Control.init C x fuel)).tape.getLast? =
      (iter (i + t) (Control.init C x fuel)).tape.getLast?
  rw [hone, htwo, hper t ht]

end Observe

#print axioms Observe.eventually_periodic
#print axioms Observe.eventually_periodic_run
#print axioms Observe.find_eq
#print axioms Observe.iter_active
#print axioms Observe.nextOf_eq_lookup
#print axioms Observe.nextVal_lt
#print axioms Observe.next_active
#print axioms Observe.obs_last_repeats
#print axioms Observe.orbit_add
#print axioms Observe.orbit_lt
#print axioms Observe.pigeon
