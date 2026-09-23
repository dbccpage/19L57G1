import ResearchConservationLadder.Action

/-!
# A worked instance: a central weight and the rotation generator

AuthorityEffect: None.  All data here are supplied, integer, and exact.

* `central c` is the two-point weight
  `(x₁ - x₀)² + (y₁ - y₀)² - c·(x₀² + y₀²)`.
* `rot (x, y) = (-y, x)` is the generator of rotations, used only to first
  order through dual numbers.
* `step c a b = (2 - c)·b - a` componentwise; `solve c a b` is the history
  it generates from the two starting points `a` and `b`.

Proved here:

* `central_invariant`: the weight is invariant under `rot`, for every `c`.
* `central_charge`: its charge is `2·(x₀·y₁ - y₀·x₁)` on the edge
  `((x₀, y₀), (x₁, y₁))`.  That value is not constant on edges
  (`charge_nonconstant`).
* `solve_stationary`, `solve_charge_const`: `solve c a b` is stationary at
  every interior point, so the charge is equal on all of its edges.
* Necessity witnesses, each against one premise:
  - `aniso_not_invariant` and `aniso_charge_moves`: with the potential on
    `x₀` only, `rot` is no longer a symmetry, and along the anisotropic
    weight's own stationary history the charge changes;
  - `nonstationary_charge_moves`: on a history that is not stationary,
    the charge of the central weight changes;
  - `shift_not_invariant`: the constant generator `(1, 0)` is not a
    symmetry of `central 1`, although it is of `central 0`
    (`shift_invariant_free`).
-/

namespace ResearchConservationLadder

open Expr

def x₀ : Expr := var 0
def y₀ : Expr := var 1
def x₁ : Expr := var 2
def y₁ : Expr := var 3

/-- The central two-point weight. -/
def central (c : Int) : Expr :=
  add (add (sq (sub x₁ x₀)) (sq (sub y₁ y₀)))
    (neg (mul (const c) (add (sq x₀) (sq y₀))))

/-- The same kinetic part with the potential on `x₀` only. -/
def aniso : Expr :=
  add (add (sq (sub x₁ x₀)) (sq (sub y₁ y₀))) (neg (sq x₀))

def rot (p : P) : P := (-p.2, p.1)

def shift (_ : P) : P := (1, 0)

theorem D₁_central (c : Int) (a b v : P) :
    D₁ (central c) a b v =
      -2 * ((b.1 - a.1) * v.1 + (b.2 - a.2) * v.2) - 2 * c * (a.1 * v.1 + a.2 * v.2) := by
  simp only [D₁, central, sq, sub, x₀, y₀, x₁, y₁, ddir, eval, slots, first]
  simp only [Int.neg_mul, Int.two_mul, Int.sub_mul, Int.mul_sub, Int.add_mul, Int.mul_add]
  simp only [Int.sub_eq_add_neg, Int.neg_add, Int.neg_neg, Int.mul_neg, Int.neg_mul,
    Int.mul_zero, Int.zero_mul, Int.add_zero, Int.zero_add, Int.mul_one, Int.one_mul,
    Int.mul_comm, Int.mul_left_comm, Int.mul_assoc]
  omega

theorem D₂_central (c : Int) (a b v : P) :
    D₂ (central c) a b v = 2 * ((b.1 - a.1) * v.1 + (b.2 - a.2) * v.2) := by
  simp only [D₂, central, sq, sub, x₀, y₀, x₁, y₁, ddir, eval, slots, second]
  simp only [Int.neg_mul, Int.two_mul, Int.sub_mul, Int.mul_sub, Int.add_mul, Int.mul_add]
  simp only [Int.sub_eq_add_neg, Int.neg_add, Int.neg_neg, Int.mul_neg, Int.neg_mul,
    Int.mul_zero, Int.zero_mul, Int.add_zero, Int.zero_add, Int.mul_one, Int.one_mul,
    Int.mul_comm, Int.mul_left_comm, Int.mul_assoc]
  omega

theorem central_invariant (c : Int) : Invariant (central c) rot := by
  intro a b
  rw [D₁_central, D₂_central]
  simp only [rot]
  simp only [Int.neg_mul, Int.two_mul, Int.sub_mul, Int.mul_sub, Int.add_mul, Int.mul_add]
  simp only [Int.sub_eq_add_neg, Int.neg_add, Int.neg_neg, Int.mul_neg, Int.neg_mul,
    Int.mul_zero, Int.zero_mul, Int.add_zero, Int.zero_add, Int.mul_one, Int.one_mul,
    Int.mul_comm, Int.mul_left_comm, Int.mul_assoc]
  omega

theorem central_charge (c : Int) (a b : P) :
    charge (central c) rot a b = 2 * (a.1 * b.2 - a.2 * b.1) := by
  simp only [charge, D₂_central, rot]
  simp only [Int.neg_mul, Int.two_mul, Int.sub_mul, Int.mul_sub, Int.add_mul, Int.mul_add]
  simp only [Int.sub_eq_add_neg, Int.neg_add, Int.neg_neg, Int.mul_neg, Int.neg_mul,
    Int.mul_zero, Int.zero_mul, Int.add_zero, Int.zero_add, Int.mul_one, Int.one_mul,
    Int.mul_comm, Int.mul_left_comm, Int.mul_assoc]
  omega

theorem charge_nonconstant (c : Int) :
    charge (central c) rot (0, 0) (1, 1) ≠ charge (central c) rot (1, 0) (0, 1) := by
  rw [central_charge, central_charge]
  decide

/-- The recurrence of the central weight's stationarity equation. -/
def next (c : Int) (a b : P) : P :=
  ((2 - c) * b.1 - a.1, (2 - c) * b.2 - a.2)

/-- The history generated from two starting points. -/
def pairs (c : Int) (a b : P) : Nat → P × P
  | 0 => (a, b)
  | n + 1 => ((pairs c a b n).2, next c (pairs c a b n).1 (pairs c a b n).2)

def solve (c : Int) (a b : P) (n : Nat) : P := (pairs c a b n).1

theorem solve_succ (c : Int) (a b : P) (n : Nat) :
    solve c a b (n + 1) = (pairs c a b n).2 := rfl

theorem solve_succ_succ (c : Int) (a b : P) (n : Nat) :
    solve c a b (n + 2) = next c (solve c a b n) (solve c a b (n + 1)) := rfl

theorem solve_stationary (c : Int) (a b : P) (k : Nat) (hk : 1 ≤ k) :
    Stationary (central c) (solve c a b) k := by
  intro v
  obtain ⟨m, rfl⟩ : ∃ m, k = m + 1 := ⟨k - 1, by omega⟩
  rw [D₂_central, D₁_central, Nat.add_sub_cancel]
  show 2 * (((solve c a b (m + 1)).1 - (solve c a b m).1) * v.1 +
      ((solve c a b (m + 1)).2 - (solve c a b m).2) * v.2) +
    (-2 * (((solve c a b (m + 2)).1 - (solve c a b (m + 1)).1) * v.1 +
      ((solve c a b (m + 2)).2 - (solve c a b (m + 1)).2) * v.2) -
     2 * c * ((solve c a b (m + 1)).1 * v.1 + (solve c a b (m + 1)).2 * v.2)) = 0
  rw [solve_succ_succ]
  simp only [next]
  generalize (solve c a b m).1 = p₁
  generalize (solve c a b m).2 = p₂
  generalize (solve c a b (m + 1)).1 = r₁
  generalize (solve c a b (m + 1)).2 = r₂
  simp only [Int.neg_mul, Int.two_mul, Int.sub_mul, Int.mul_sub, Int.add_mul, Int.mul_add]
  simp only [Int.sub_eq_add_neg, Int.neg_add, Int.neg_neg, Int.mul_neg, Int.neg_mul,
    Int.mul_zero, Int.zero_mul, Int.add_zero, Int.zero_add, Int.mul_one, Int.one_mul,
    Int.mul_comm, Int.mul_left_comm, Int.mul_assoc]
  omega

/-- **The charge is constant along every generated history.** -/
theorem solve_charge_const (c : Int) (a b : P) (k : Nat) :
    charge (central c) rot (solve c a b k) (solve c a b (k + 1)) =
      charge (central c) rot a b :=
  charge_const (central c) rot (central_invariant c) (solve c a b)
    (fun k hk => solve_stationary c a b k hk) k

/-! ## Necessity witnesses -/

theorem aniso_not_invariant : ¬ Invariant aniso rot := by
  intro h
  have := h (1, 1) (0, 0)
  simp [D₁, D₂, aniso, sq, sub, x₀, y₀, x₁, y₁, ddir, eval, slots, first, second, rot] at this

/-- The anisotropic weight's stationary recurrence. -/
def anisoNext (a b : P) : P := (b.1 - a.1, 2 * b.2 - a.2)

theorem aniso_charge_moves :
    charge aniso rot (1, 0) (1, 1) ≠ charge aniso rot (1, 1) (anisoNext (1, 0) (1, 1)) := by
  decide

theorem aniso_next_stationary (a b : P) :
    ∀ v : P, D₂ aniso a b v + D₁ aniso b (anisoNext a b) v = 0 := by
  intro v
  simp only [D₁, D₂, aniso, sq, sub, x₀, y₀, x₁, y₁, ddir, eval, slots, first, second,
    anisoNext]
  simp only [Int.neg_mul, Int.two_mul, Int.sub_mul, Int.mul_sub, Int.add_mul, Int.mul_add]
  simp only [Int.sub_eq_add_neg, Int.neg_add, Int.neg_neg, Int.mul_neg, Int.neg_mul,
    Int.mul_zero, Int.zero_mul, Int.add_zero, Int.zero_add, Int.mul_one, Int.one_mul,
    Int.mul_comm, Int.mul_left_comm, Int.mul_assoc]
  omega

theorem nonstationary_charge_moves :
    charge (central 0) rot (0, 0) (1, 0) ≠ charge (central 0) rot (1, 0) (1, 1) := by
  rw [central_charge, central_charge]
  decide

theorem shift_not_invariant : ¬ Invariant (central 1) shift := by
  intro h
  have := h (1, 0) (1, 0)
  rw [D₁_central, D₂_central] at this
  simp [shift] at this

theorem shift_invariant_free : Invariant (central 0) shift := by
  intro a b
  rw [D₁_central, D₂_central]
  simp only [shift]
  omega

end ResearchConservationLadder
