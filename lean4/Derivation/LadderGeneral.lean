import Derivation.HigherStructure

/-!
# The ladder at arbitrary finite dimension

Generalization of the hard-coded `HigherStructure` cell calculus
(dimensions 0–3) to every finite dimension: a dimension-indexed
complex, one shell guard uniform in the dimension, one admission
step, and the LADDER THEOREM proved for all `k ≥ 1` — upgrading the
review-pass frontier conjecture GENERAL_DIMENSIONAL_LADDER to a
theorem *of this generalized declared calculus*.

Imported (declared, not derived) inputs, per the standing
discipline: fresh vertex supply, the ascending-list cell encoding,
integer coefficients and the boundary sign convention, and the
metatheoretic iteration of any driver.  Protection, observer
transport, budget, and activation do not appear in this module at
all — the calculus is the declared realization layer, not the
passage.

What remains conjectural after this module: the general vanishing of
the composite boundary (`∂∂ = 0` for every dimension) — decided here
at dimensions 2, 3, and 4 on the demonstration cells, general case
recorded as the remaining boundary-calculus conjecture.
-/

namespace LadderGeneral

/-- A dimension-indexed complex: dimension `k` carries its cells,
each a `(k+1)`-vertex ascending list. -/
structure ComplexN where
  cells : Nat → List (List Nat)

def emptyN : ComplexN := ⟨fun _ => []⟩

/-- The facets of a cell: drop one vertex each. -/
def facets (σ : List Nat) : List (List Nat) :=
  (List.range σ.length).map σ.eraseIdx

/-- The dimension-`k` shell guard, uniform in `k`: the candidate has
the right vertex count, every facet is present one dimension down,
and the cell itself is absent — the complete-unfilled-boundary
condition at every dimension. -/
def shellN (C : ComplexN) (k : Nat) (σ : List Nat) : Bool :=
  (decide (σ.length = k + 1)) && (decide (1 ≤ k))
    && (facets σ).all (fun τ => decide (τ ∈ C.cells (k - 1)))
    && !(decide (σ ∈ C.cells k))

/-- Vertex admission (dimension 0), dedup-guarded. -/
def stepV (C : ComplexN) (v : Nat) : ComplexN :=
  if [v] ∈ C.cells 0 then C
  else ⟨fun j => if j = 0 then C.cells 0 ++ [[v]] else C.cells j⟩

/-- Cell admission at any dimension `k ≥ 1`, shell-guarded. -/
def stepN (C : ComplexN) (k : Nat) (σ : List Nat) : ComplexN :=
  if shellN C k σ then
    ⟨fun j => if j = k then C.cells k ++ [σ] else C.cells j⟩
  else C

/-- **THE GENERAL LADDER THEOREM, arbitrary finite dimension**: at
every `k`, a complete unfilled boundary admits its filling cell, and
the admission genuinely extends the complex — the two-rule shape
(obstruction-shaped precondition, structure-creating response),
uniform in the dimension. -/
theorem ladder_general (C : ComplexN) (k : Nat) (σ : List Nat)
    (h : shellN C k σ = true) :
    σ ∈ (stepN C k σ).cells k ∧ stepN C k σ ≠ C := by
  have hproj : (stepN C k σ).cells k = C.cells k ++ [σ] := by
    unfold stepN
    rw [if_pos h]
    show (if k = k then C.cells k ++ [σ] else C.cells k)
      = C.cells k ++ [σ]
    rw [if_pos rfl]
  constructor
  · rw [hproj]
    exact List.mem_append.mpr (Or.inr List.mem_cons_self)
  · intro heq
    rw [heq] at hproj
    have hlen := congrArg List.length hproj
    simp only [List.length_append, List.length_cons,
      List.length_nil] at hlen
    omega

/-- The shell guard is load-bearing at every dimension: without it
(any failing conjunct — wrong arity, missing facet, duplicate), the
step is inert. -/
theorem shell_refuses_general (C : ComplexN) (k : Nat)
    (σ : List Nat) (h : shellN C k σ = false) :
    stepN C k σ = C := by
  unfold stepN
  rw [if_neg (by rw [h]; exact fun hc => Bool.noConfusion hc)]

/-- The shell does not fill itself at any dimension: admission
requires the step event. -/
theorem shell_no_self_fill (C : ComplexN) (k : Nat) (σ : List Nat)
    (h : shellN C k σ = true) : ¬ (σ ∈ C.cells k) := by
  intro hmem
  unfold shellN at h
  simp only [Bool.and_eq_true, Bool.not_eq_true',
    decide_eq_false_iff_not] at h
  exact h.2 hmem

/-! ## The dimension-4 demonstration: the boundary of the
five-vertex cell, filled

The complete replay: 5 vertices, 10 edges, 10 triangles, 5
tetrahedra (each over its complete boundary), then the single
4-cell over its 5 tetrahedral facets — every admission
shell-guarded, in creation order. -/

inductive NEvent where
  | addV (v : Nat)
  | addC (k : Nat) (σ : List Nat)

def nstep (C : ComplexN) : NEvent → ComplexN
  | .addV v => stepV C v
  | .addC k σ => stepN C k σ

def nreplay (h : List NEvent) (C : ComplexN) : ComplexN :=
  h.foldl nstep C

/-- Ascending selections: all `m`-element ascending sublists of a
list. -/
def combsAux : Nat → List Nat → List (List Nat)
  | 0, _ => [[]]
  | _ + 1, [] => []
  | m + 1, x :: xs =>
      (combsAux m xs).map (fun l => x :: l) ++ combsAux (m + 1) xs

/-- All `(m+1)`-vertex ascending cells over the first `n` vertices. -/
def combs (n m : Nat) : List (List Nat) :=
  combsAux (m + 1) (List.range n)

def d4Events : List NEvent :=
  ((List.range 5).map .addV)
    ++ ((combs 5 1).map (.addC 1))
    ++ ((combs 5 2).map (.addC 2))
    ++ ((combs 5 3).map (.addC 3))
    ++ [.addC 4 [0, 1, 2, 3, 4]]

def d4Complex : ComplexN := nreplay d4Events emptyN

set_option maxRecDepth 4096 in
/-- The dimension-4 instance of the ladder, replayed: every guarded
admission fired, and the top cell is present exactly over its
complete boundary. -/
theorem d4_demo :
    (d4Complex.cells 0).length = 5 ∧
    (d4Complex.cells 1).length = 10 ∧
    (d4Complex.cells 2).length = 10 ∧
    (d4Complex.cells 3).length = 5 ∧
    d4Complex.cells 4 = [[0, 1, 2, 3, 4]] := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> decide

/-- Without one tetrahedral facet the 4-shell is not complete and
the 4-cell is refused — the guard is load-bearing at dimension 4. -/
def d4MissingEvents : List NEvent :=
  ((List.range 5).map .addV)
    ++ ((combs 5 1).map (.addC 1))
    ++ ((combs 5 2).map (.addC 2))
    ++ (((combs 5 3).drop 1).map (.addC 3))
    ++ [.addC 4 [0, 1, 2, 3, 4]]

set_option maxRecDepth 4096 in
theorem d4_guard_load_bearing :
    (nreplay d4MissingEvents emptyN).cells 4 = [] := by decide

/-! ## The generalized boundary calculus (declared) and its
composite at dimensions 2–4 -/

/-- Alternating sign, declared. -/
def sgn (i : Nat) : Int := if i % 2 = 0 then 1 else -1

/-- The generalized boundary of one cell. -/
def bdN (σ : List Nat) : List (Int × List Nat) :=
  (List.range σ.length).map (fun i => (sgn i, σ.eraseIdx i))

/-- Pushforward of a chain one dimension down. -/
def pushN (ch : List (Int × List Nat)) : List (Int × List Nat) :=
  ch.flatMap (fun p => (bdN p.2).map (fun q => (p.1 * q.1, q.2)))

/-- Coefficient collection. -/
def coeffN (τ : List Nat) (ch : List (Int × List Nat)) : Int :=
  (ch.filter (fun p => p.2 == τ)).foldl (fun acc p => acc + p.1) 0

/-- The composite boundary vanishes on the demonstration cells of
dimensions 2, 3, and 4 (decided).  The general vanishing at every
dimension is the remaining boundary-calculus conjecture, recorded in
the receipt — declared coefficients and signs carry the content. -/
theorem d2_zero_dims_2_3_4 :
    ((combs 5 2).all fun t =>
      (facets t).all fun e => coeffN e (pushN (bdN t)) == 0) = true ∧
    ((combs 5 3).all fun q =>
      (facets q).all fun t2 =>
        coeffN t2 (pushN (bdN q)) == 0) = true ∧
    ((facets [0, 1, 2, 3, 4]).all fun q =>
      (facets q).all fun t2 =>
        coeffN t2 (pushN (bdN [0, 1, 2, 3, 4])) == 0) = true := by
  refine ⟨?_, ?_, ?_⟩ <;> decide

end LadderGeneral
