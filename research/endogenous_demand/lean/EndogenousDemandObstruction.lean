import Derivation.Basic
import Derivation.Inertia
import Derivation.Counting
import Derivation.Rounds

/-!
# Target 8: Constructive Finite Termination Obstruction Theorem (OB-1)

This module formalizes the constructive finite termination obstruction theorem
for endogenous demand generation in the object language.

Under minimum-response selection with no external driving (`Item.newDatum ∉ response`):
1. The carrier size is invariant: `s.data = r.data = N`.
2. Requirement store growth is strictly monotonic: each accepted round adds
   exactly one fresh pair, `s.reqs.length = r.reqs.length + 1`.
3. Separation is preserved and monotonic: no requirement is duplicated, and all
   pairs belong to the finite carrier pair space `allPairs N`.
4. Stated division-free: any endogenous execution trace of length `k` from regime `r` satisfies
   `2 * (r.reqs.length + k) ≤ N * (N - 1)`.
5. In particular, from an empty requirement store, `2 * k ≤ N * (N - 1)`, which means
   `k ≤ Nat.choose N 2 = N * (N - 1) / 2`.
6. Obstruction: no infinite endogenous demand execution without external data growth
   is possible on any finite carrier $N$. Every endogenous trace must terminate
   in at most `binom(N, 2)` steps.

Axioms are strictly audited to be contained in `{propext, Quot.sound}`.
AuthorityEffect: None.
-/

namespace EndogenousDemandObstruction

open Derivation

/-! ## 1. Finite Carrier Pairs and Combinatorial Capacity -/

/-- The canonical list of valid ordered demand pairs on a carrier of size `n`. -/
def carrierPairs (n : Nat) : List (Nat × Nat) := allPairs n

/-- The binomial coefficient `binom(n, 2) = n * (n - 1) / 2`. -/
def binom2 (n : Nat) : Nat := n * (n - 1) / 2

/-- Exact multiplicative capacity of carrier pairs: `2 * |allPairs n| = n * (n - 1)`. -/
theorem carrierPairs_capacity (n : Nat) :
    2 * (carrierPairs n).length = n * (n - 1) :=
  allPairs_length n

/-- Every valid requirement pair on carrier `n` is a member of `carrierPairs n`. -/
theorem mem_carrierPairs_iff (n : Nat) (q : Nat × Nat) :
    q ∈ carrierPairs n ↔ q.1 < q.2 ∧ q.2 < n :=
  ⟨allPairs_mem_bound n q, fun ⟨h1, h2⟩ => mem_allPairs n q h1 h2⟩

/-- Carrier pairs have no duplicate entries. -/
theorem carrierPairs_nodup (n : Nat) : (carrierPairs n).Nodup :=
  allPairs_nodup n

/-! ## 2. Endogenous Transition Steps and Monotonicity -/

/-- An endogenous step: a round that imposes an unfulfilled fresh pair `rd.target ∉ r.reqs`
    and responds with a delta admitting no new data (`Item.newDatum ∉ rd.response`). -/
structure EndogenousStep (r : Regime) (rd : Round) (s : Regime) : Prop where
  fresh : rd.target ∉ r.reqs
  no_grow : Item.newDatum ∉ rd.response
  step : respond r rd.target.1 rd.target.2 rd.response = some s

/-- An endogenous step fixes the carrier size (no external driving). -/
theorem step_data_invariant {r s : Regime} {rd : Round}
    (h : EndogenousStep r rd s) : s.data = r.data :=
  round_data_eq h.no_grow h.step

/-- An endogenous step strictly increments the requirement store count by 1. -/
theorem step_reqs_strict_mono {r s : Regime} {rd : Round}
    (h : EndogenousStep r rd s) : s.reqs.length = r.reqs.length + 1 :=
  round_reqs_succ h.fresh h.step

/-- An endogenous step preserves the absence of duplicate requirements. -/
theorem step_reqs_nodup {r s : Regime} {rd : Round}
    (h : EndogenousStep r rd s) (hn : r.reqs.Nodup) : s.reqs.Nodup := by
  obtain ⟨_, _, hreqs, _⟩ := respond_anatomy h.step
  rw [hreqs, insertNew_of_not_mem h.fresh]
  exact nodup_append_singleton h.fresh hn

/-- An endogenous step preserves requirement well-formedness (boundedness within the carrier). -/
theorem step_reqs_wf {r s : Regime} {rd : Round}
    (h : EndogenousStep r rd s)
    (hwf : ∀ q ∈ r.reqs, q.1 < q.2 ∧ q.2 < r.data) :
    ∀ q ∈ s.reqs, q.1 < q.2 ∧ q.2 < s.data := by
  obtain ⟨h1, h2, hreqs, _⟩ := respond_anatomy h.step
  have hdata : s.data = r.data := step_data_invariant h
  intro q hq
  rw [hreqs] at hq
  rcases mem_insertNew.mp hq with hin | he
  · obtain ⟨ha, hb⟩ := hwf q hin
    exact ⟨ha, hdata ▸ hb⟩
  · subst he
    exact ⟨h1, hdata ▸ h2⟩

/-! ## 3. Endogenous Execution Traces -/

/-- An endogenous trace of length `k` from initial regime `r` to terminal regime `t`. -/
def EndogenousTrace (r : Regime) (k : Nat) (t : Regime) : Prop :=
  ∃ rds : List Round, rds.length = k ∧ ClosedRun r rds t

/-- Zero-step endogenous trace is reflexive. -/
theorem trace_zero (r : Regime) : EndogenousTrace r 0 r :=
  ⟨[], rfl, ClosedRun.nil r⟩

/-- An endogenous trace preserves carrier size throughout execution. -/
theorem trace_data_invariant {r t : Regime} {k : Nat}
    (h : EndogenousTrace r k t) : t.data = r.data := by
  obtain ⟨rds, _, hrun⟩ := h
  exact closedRun_data_eq hrun

/-- The requirement store strictly grows by the number of steps `k` in the trace. -/
theorem trace_reqs_length {r t : Regime} {k : Nat}
    (h : EndogenousTrace r k t) : t.reqs.length = r.reqs.length + k := by
  obtain ⟨rds, rfl, hrun⟩ := h
  exact closedRun_reqs_length hrun

/-- An endogenous trace preserves non-duplication of requirements. -/
theorem trace_reqs_nodup {r t : Regime} {k : Nat}
    (h : EndogenousTrace r k t) (hn : r.reqs.Nodup) : t.reqs.Nodup := by
  obtain ⟨rds, _, hrun⟩ := h
  exact closedRun_reqs_nodup hrun hn

/-- An endogenous trace preserves carrier-boundedness of all requirements. -/
theorem trace_reqs_wf {r t : Regime} {k : Nat}
    (h : EndogenousTrace r k t)
    (hwf : ∀ q ∈ r.reqs, q.1 < q.2 ∧ q.2 < r.data) :
    ∀ q ∈ t.reqs, q.1 < q.2 ∧ q.2 < t.data := by
  obtain ⟨rds, _, hrun⟩ := h
  exact closedRun_reqs_wf hrun hwf

/-- Every requirement accumulated at the end of an endogenous trace belongs to `carrierPairs`. -/
theorem trace_reqs_subset_carrierPairs {r t : Regime} {k : Nat}
    (h : EndogenousTrace r k t)
    (hwf : ∀ q ∈ r.reqs, q.1 < q.2 ∧ q.2 < r.data) :
    ∀ q ∈ t.reqs, q ∈ carrierPairs r.data := by
  intro q hq
  obtain ⟨rds, _, hrun⟩ := h
  have htwf := closedRun_reqs_wf hrun hwf q hq
  have htdata := closedRun_data_eq hrun
  rw [mem_carrierPairs_iff]
  exact ⟨htwf.1, htdata ▸ htwf.2⟩

/-! ## 4. The Constructive Finite Termination Obstruction Theorem (OB-1) -/

/-- **Theorem (Constructive Finite Termination Bound)**:
    Under minimum-response selection with no external data growth, any endogenous trace
    of length `k` on a carrier of size `N = r.data` satisfies:
    `2 * (r.reqs.length + k) ≤ N * (N - 1)`. -/
theorem endogenous_termination_bound {r t : Regime} {k : Nat}
    (h : EndogenousTrace r k t) (hn : r.reqs.Nodup)
    (hwf : ∀ q ∈ r.reqs, q.1 < q.2 ∧ q.2 < r.data) :
    2 * (r.reqs.length + k) ≤ r.data * (r.data - 1) := by
  obtain ⟨rds, rfl, hrun⟩ := h
  exact closedRun_round_bound hrun hn hwf

/-- **Corollary (Termination from Clean Store)**:
    Starting from an empty requirement store (`r.reqs = []`), any endogenous trace
    of length `k` satisfies `2 * k ≤ N * (N - 1)`. -/
theorem endogenous_termination_from_empty {r t : Regime} {k : Nat}
    (h : EndogenousTrace r k t) (he : r.reqs = []) :
    2 * k ≤ r.data * (r.data - 1) := by
  obtain ⟨rds, rfl, hrun⟩ := h
  exact closedRun_round_bound_from_empty hrun he

/-- **Theorem (Obstruction Bound in Binomial Form)**:
    Starting from an empty requirement store, the length `k` of any endogenous trace
    is bounded by `binom(N, 2)`. -/
theorem endogenous_trace_le_binom2 {r t : Regime} {k : Nat}
    (h : EndogenousTrace r k t) (he : r.reqs = []) :
    k ≤ binom2 r.data := by
  have hb := endogenous_termination_from_empty h he
  unfold binom2
  omega

/-- **Theorem (Obstruction to Infinite Generation / OB-1)**:
    No endogenous demand execution without external data growth can exceed
    `binom(N, 2)` steps. Any trace of length `k > binom(N, 2)` is excluded. -/
theorem endogenous_obstruction_no_excess {r t : Regime} {k : Nat}
    (he : r.reqs = []) (h_excess : binom2 r.data < k) :
    ¬ EndogenousTrace r k t := by
  intro h_trace
  have h_le := endogenous_trace_le_binom2 h_trace he
  omega

end EndogenousDemandObstruction

/-! ## 5. Axiom Audit -/

#print axioms EndogenousDemandObstruction.carrierPairs_capacity
#print axioms EndogenousDemandObstruction.step_data_invariant
#print axioms EndogenousDemandObstruction.step_reqs_strict_mono
#print axioms EndogenousDemandObstruction.step_reqs_nodup
#print axioms EndogenousDemandObstruction.step_reqs_wf
#print axioms EndogenousDemandObstruction.trace_data_invariant
#print axioms EndogenousDemandObstruction.trace_reqs_length
#print axioms EndogenousDemandObstruction.trace_reqs_nodup
#print axioms EndogenousDemandObstruction.trace_reqs_wf
#print axioms EndogenousDemandObstruction.trace_reqs_subset_carrierPairs
#print axioms EndogenousDemandObstruction.endogenous_termination_bound
#print axioms EndogenousDemandObstruction.endogenous_termination_from_empty
#print axioms EndogenousDemandObstruction.endogenous_trace_le_binom2
#print axioms EndogenousDemandObstruction.endogenous_obstruction_no_excess
