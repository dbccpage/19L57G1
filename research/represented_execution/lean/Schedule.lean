import Product

/-!
# Schedule: a two-locus run, and what the record of it shows

`Product` built two loci as a *carrier* and proved the independence square of
the *operations*.  A carrier is not a run.  The consumer family's obligation
asks for the square as a statement about **observations**, and the obstacle it
names is precise: a machine with two loci has to decide which locus moves, and
if the interpreter decides, the schedule is a host choice.  The runner's
existing refusal to select (`Control.stepDet` returns `branch` when two
operations are enabled) is the test any answer has to pass.

The answer here is that **the schedule is data**.  A scheduled setting names,
at each datum, the one operation enabled there; the enablement is represented
in exactly the instances the machine already reads, so the interpreter finds a
singleton and never selects (`enabledAt_scheduled`, `scheduled_no_branch`).
Nothing about the interpreter changes, and nothing is added to the grammar.

On the product carrier that gives a genuine two-locus run, and three results
about its record:

* **One locus moves at a time** (`step_moves_one_locus`).  Whatever the
  schedule, every step leaves one of the two coordinates exactly where it was.
  This is independence as a property of the *run*: not that two moves commute,
  but that the record never shows them happening together.
* **The square holds of the outcome and fails of the observation.**  Two
  schedules that move the loci in opposite orders reach the same datum
  (`square_on_the_outcome`) by different tapes
  (`square_fails_on_the_observation`).  The commutation is real and the
  record still distinguishes the orders, because a tape totally orders events
  that the loci do not.
* **What does lift is the projection.**  Reading the tape at one locus and
  dropping the repeats — the steps that moved the *other* locus — returns
  that locus's own one-locus run exactly (`locus1_is_its_own_run`,
  `locus2_is_its_own_run`).  The destuttering is the whole content of the
  lift, and it is what the observing family can state.

The failure case is kept beside the theorem: an operation that is neither a
left nor a right move changes both loci in one step (`swap_moves_both`), so
`step_moves_one_locus` is a property of the product's operations and not of
the machine that runs them.

AuthorityEffect: None.
-/

namespace Schedule

open Derivation Translation Control Product

/-! ## 1. Filtering a range at one index -/

theorem filter_single_true {p : Nat → Bool} {n : Nat} (h : p n = true) :
    [n].filter p = [n] := by
  show (match p n with | true => n :: List.filter p [] | false => List.filter p []) = [n]
  rw [h]
  rfl

theorem filter_single_false {p : Nat → Bool} {n : Nat} (h : p n = false) :
    [n].filter p = [] := by
  show (match p n with | true => n :: List.filter p [] | false => List.filter p []) = []
  rw [h]
  rfl

theorem filter_range_eq_nil (k : Nat) : ∀ n, n ≤ k →
    (List.range n).filter (fun j => decide (k = j)) = []
  | 0, _ => rfl
  | n + 1, h => by
      have hr : List.range (n + 1) = List.range n ++ [n] := List.range_succ
      rw [hr, List.filter_append, filter_range_eq_nil k n (by omega),
        filter_single_false (p := fun j => decide (k = j)) (decide_eq_false (by omega))]
      rfl

theorem filter_range_eq_single (k : Nat) : ∀ n, k < n →
    (List.range n).filter (fun j => decide (k = j)) = [k]
  | 0, h => absurd h (Nat.not_lt_zero k)
  | n + 1, h => by
      have hr : List.range (n + 1) = List.range n ++ [n] := List.range_succ
      rcases Nat.lt_or_ge k n with hk | hk
      · rw [hr, List.filter_append, filter_range_eq_single k n hk,
          filter_single_false (p := fun j => decide (k = j)) (decide_eq_false (by omega))]
        rfl
      · have hkn : k = n := by omega
        subst hkn
        rw [hr, List.filter_append, filter_range_eq_nil k k (Nat.le_refl k),
          filter_single_true (p := fun j => decide (k = j)) (decide_eq_true rfl)]
        rfl

theorem filter_congr_mem {p q : Nat → Bool} : ∀ (l : List Nat), (∀ a ∈ l, p a = q a) →
    l.filter p = l.filter q
  | [], _ => rfl
  | a :: as, h => by
      have ha : p a = q a := h a (List.Mem.head as)
      have ih : as.filter p = as.filter q :=
        filter_congr_mem as (fun b hb => h b (List.Mem.tail a hb))
      show (match p a with | true => a :: as.filter p | false => as.filter p)
          = (match q a with | true => a :: as.filter q | false => as.filter q)
      rw [ha, ih]

theorem bool_of_iff {a b : Bool} (h : a = true ↔ b = true) : a = b := by
  cases a <;> cases b
  · rfl
  · exact h.mpr rfl
  · exact absurd (h.mp rfl) (by decide)
  · rfl

/-! ## 2. A schedule carried in the data -/

/-- A **scheduled** controlled setting: at each datum the program names the
one operation that fires there.  `sched` is a function of the datum, so it is
carried by the enablement instances the machine already reads.  The
interpreter is told nothing it was not told before. -/
def scheduled (F : FiniteSetting) (sched : Nat → Nat) : Controlled :=
  ⟨F, fun x k => decide (sched x = k)⟩

/-- **A schedule in the data leaves the interpreter nothing to choose.**  At
every admitted datum exactly one operation is enabled: the one the schedule
names.  The list is a singleton, and it is a singleton because of the
program's instances, not because of a rule inside the runner. -/
theorem enabledAt_scheduled (F : FiniteSetting) (sched : Nat → Nat) {x : Nat}
    (hx : x < F.n) (hs : sched x < F.ops.length) :
    enabledAt (program (scheduled F sched)) F.ops.length x = [sched x] := by
  have hcongr : ∀ k ∈ List.range F.ops.length,
      enabled (program (scheduled F sched)) F.ops.length x k = decide (sched x = k) := by
    intro k hk
    exact bool_of_iff (enabled_program (scheduled F sched) (List.mem_range.mp hk) hx)
  show (List.range F.ops.length).filter
      (fun k => enabled (program (scheduled F sched)) F.ops.length x k) = [sched x]
  rw [filter_congr_mem (p := fun k => enabled (program (scheduled F sched)) F.ops.length x k)
        (q := fun k => decide (sched x = k)) (List.range F.ops.length) hcongr,
    filter_range_eq_single (sched x) F.ops.length hs]

/-- **The runner never selects, and never has to.**  A scheduled program
cannot make the deterministic step return `branch`.  The refusal that would
stop a two-locus run from being driven by the host is exactly what a schedule
carried in the data does not trigger. -/
theorem scheduled_no_branch (F : FiniteSetting) (sched : Nat → Nat) {s : State}
    (hg : s.graph = program (scheduled F sched)) (hn : s.nops = F.ops.length)
    (hx : s.active < F.n) (hs : sched s.active < F.ops.length) :
    stepDet s ≠ .inl .branch := by
  intro h
  have hlen := stepDet_branch h
  rw [hg, hn, enabledAt_scheduled F sched hx hs] at hlen
  have hone : (2 : Nat) ≤ 1 := hlen
  omega

/-! ## 3. The two-locus setting -/

/-- The two-locus controlled setting: the product carrier, `F`'s operations at
the first locus and `G`'s at the second, and a schedule naming which one
fires at each datum. -/
def twoLocus (F G : FiniteSetting) (sched : Nat → Nat) : Controlled :=
  scheduled (prodSetting F G) sched

/-- **One locus moves at a time.**  Whatever the schedule, every step of a
two-locus run leaves one of the two coordinates exactly where it was.  This is
the independence square as a statement about the run rather than about the
operations: the record never shows the two loci moving together. -/
theorem step_moves_one_locus (F G : FiniteSetting) (sched : Nat → Nat) {s s' : State}
    (hg : s.graph = program (twoLocus F G sched))
    (hn : s.nops = (prodSetting F G).ops.length)
    (hx : s.active < (prodSetting F G).n)
    (h : s' ∈ successors s) :
    fstOf G.n s'.active = fstOf G.n s.active ∨ sndOf G.n s'.active = sndOf G.n s.active := by
  obtain ⟨k, hk, -, hy⟩ := successors_sound (twoLocus F G sched) hg hn hx h
  have hmem : (prodSetting F G).ops.getD k id ∈
      F.ops.map (leftOp G.n) ++ G.ops.map (rightOp G.n) := getD_mem hk
  rcases List.mem_append.mp hmem with hl | hr
  · refine Or.inr ?_
    rw [hy]
    exact prod_left_local F G hl s.active
  · refine Or.inl ?_
    rw [hy]
    exact prod_right_local G hr s.active

/-! ## 4. A run of two loci -/

theorem flip_lt (b : Nat) : Product.flip b < 2 := by
  show (if b = 0 then 1 else 0) < 2
  rcases Nat.decEq b 0 with h | h
  · rw [if_neg h]
    decide
  · rw [if_pos h]
    decide

/-- One locus: two data and the flip. -/
def two : FiniteSetting where
  n := 2
  rel := fun _ _ => false
  ret := fun _ _ => false
  prot := fun _ _ => false
  a := 0
  b := 1
  ops := [Product.flip]
  a_lt := by decide
  b_lt := by decide
  ops_closed := by
    intro g hg x _
    have hgf : g = Product.flip := List.mem_singleton.mp hg
    subst hgf
    exact flip_lt x

/-- The alternating schedule: move the first locus when the two loci agree,
the second when they differ.  It is a function of the datum alone, and it
reads both coordinates — which is what a schedule is allowed to do and an
*operation* is not (`Product.coupling_breaks_the_square`). -/
def alt (x : Nat) : Nat := if fstOf 2 x = sndOf 2 x then 0 else 1

/-- The mirror schedule: the same alternation begun at the other locus. -/
def alt' (x : Nat) : Nat := if fstOf 2 x = sndOf 2 x then 1 else 0

def pair : Controlled := twoLocus two two alt

def pairSwapped : Controlled := twoLocus two two alt'

/-- One locus on its own, always firing. -/
def solo : Controlled := scheduled two (fun _ => 0)

/-- **A two-locus run.**  From `(0,0)` the machine visits `(1,0)`, `(1,1)`,
`(0,1)` and returns.  Four steps, alternating loci, driven entirely by the
enablement instances. -/
theorem pair_run : (Control.run (Control.init pair 0 4)).2.tape = [0, 2, 3, 1, 0] := by decide

/-- It ends by spending its fuel, not by branching: the runner never had two
operations to choose between. -/
theorem pair_terminal : (Control.run (Control.init pair 0 4)).1 = Terminal.exhausted := by decide

/-- The mirror run visits the same data in the other order. -/
theorem pairSwapped_run :
    (Control.run (Control.init pairSwapped 0 4)).2.tape = [0, 1, 3, 2, 0] := by decide

/-! ## 5. The square, of the outcome and of the observation -/

/-- **The square holds of the outcome.**  Moving the first locus and then the
second reaches the datum that moving the second and then the first reaches. -/
theorem square_on_the_outcome :
    (Control.run (Control.init pair 0 2)).2.active
      = (Control.run (Control.init pairSwapped 0 2)).2.active := by decide

/-- **And fails of the observation.**  The two runs record different tapes.
The commutation is real, and the record still distinguishes the orders: a
tape totally orders events that the loci do not. -/
theorem square_fails_on_the_observation :
    (Control.run (Control.init pair 0 2)).2.tape
      ≠ (Control.run (Control.init pairSwapped 0 2)).2.tape := by decide

/-! ## 6. What does lift: the projection to one locus -/

/-- The first locus, read off a tape. -/
def locus1 (m : Nat) (l : List Nat) : List Nat := l.map (fstOf m)

/-- The second locus, read off a tape. -/
def locus2 (m : Nat) (l : List Nat) : List Nat := l.map (sndOf m)

/-- Adjacent repeats dropped: what one locus's reading of the tape looks like
once the steps that moved the *other* locus are forgotten. -/
def destutter : List Nat → List Nat
  | [] => []
  | [x] => [x]
  | x :: y :: rest => if x = y then destutter (y :: rest) else x :: destutter (y :: rest)

/-- The one-locus run this family's second locus is compared against. -/
theorem solo_run : (Control.run (Control.init solo 0 2)).2.tape = [0, 1, 0] := by decide

/-- **The lift, first locus.**  Reading the two-locus tape at the first locus
and dropping the repeats returns that locus's own run, exactly. -/
theorem locus1_is_its_own_run :
    destutter (locus1 2 (Control.run (Control.init pair 0 4)).2.tape)
      = (Control.run (Control.init solo 0 2)).2.tape := by decide

/-- **The lift, second locus.** -/
theorem locus2_is_its_own_run :
    destutter (locus2 2 (Control.run (Control.init pair 0 4)).2.tape)
      = (Control.run (Control.init solo 0 2)).2.tape := by decide

/-- The repeats are not an artefact of the destuttering: the raw projections
carry them, and they are exactly the steps at the other locus. -/
theorem locus1_stutters :
    locus1 2 (Control.run (Control.init pair 0 4)).2.tape = [0, 1, 1, 0, 0] := by decide

theorem locus2_stutters :
    locus2 2 (Control.run (Control.init pair 0 4)).2.tape = [0, 0, 1, 1, 0] := by decide

/-! ## 7. The failure case, kept beside the theorem -/

/-- A move that is neither at the first locus nor at the second. -/
def swapOp (m x : Nat) : Nat := pack m (sndOf m x) (fstOf m x)

/-- **One locus at a time is a property of the product's operations.**  An
operation outside the two local families changes both coordinates in a single
step, so `step_moves_one_locus` is bought by `prodSetting`'s operations and
not by the machine that runs them. -/
theorem swap_moves_both :
    fstOf 2 (swapOp 2 1) ≠ fstOf 2 1 ∧ sndOf 2 (swapOp 2 1) ≠ sndOf 2 1 := by decide

/-- And `swapOp` is not one of them. -/
theorem swap_not_local :
    (∃ x, sndOf 2 (swapOp 2 x) ≠ sndOf 2 x) ∧ (∃ x, fstOf 2 (swapOp 2 x) ≠ fstOf 2 x) :=
  ⟨⟨1, swap_moves_both.2⟩, ⟨1, swap_moves_both.1⟩⟩

end Schedule

#print axioms Schedule.filter_single_true
#print axioms Schedule.filter_single_false
#print axioms Schedule.filter_range_eq_nil
#print axioms Schedule.filter_range_eq_single
#print axioms Schedule.filter_congr_mem
#print axioms Schedule.bool_of_iff
#print axioms Schedule.enabledAt_scheduled
#print axioms Schedule.scheduled_no_branch
#print axioms Schedule.step_moves_one_locus
#print axioms Schedule.flip_lt
#print axioms Schedule.pair_run
#print axioms Schedule.pair_terminal
#print axioms Schedule.pairSwapped_run
#print axioms Schedule.square_on_the_outcome
#print axioms Schedule.square_fails_on_the_observation
#print axioms Schedule.solo_run
#print axioms Schedule.locus1_is_its_own_run
#print axioms Schedule.locus2_is_its_own_run
#print axioms Schedule.locus1_stutters
#print axioms Schedule.locus2_stutters
#print axioms Schedule.swap_moves_both
#print axioms Schedule.swap_not_local
