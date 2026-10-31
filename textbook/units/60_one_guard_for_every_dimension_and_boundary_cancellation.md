# Unit 60. One guard for every dimension, and boundary cancellation

**Claim.** For the declared signed boundary construction, taking a boundary twice gives coefficient zero at every target. The unreduced list may remain nonempty. The unsigned construction has counterexamples.

<details>
<summary>Sources and classification (optional)</summary>

**Status:** FROZEN (general filler, invariant, and unrestricted boundary cancellation); CONDITIONAL (`uniform_guarded_filler`, `shell_refuses_general`, `eraseIdx_inj_of_asc`, `codim2_distinct`, `d2_zero_renamed`); VERIFIED_FINITE / REFUTED (`pseudo_cell_countermodel`, `d4_demo`, `d4_guard_load_bearing`, `signless_countermodel`, `illformed_countermodel`); PROOF DEFECT (`d2_zero_dims_2_3_4` conjuncts 1–2 vacuous, superseded by `d2_zero_unrestricted`). **Lean:** `lean4/Derivation/LadderGeneral.lean` lines 51-329 and `lean4/Derivation/BoundaryCancellation.lean` lines 95-661. **Axioms:** 13 reports for `LadderGeneral` (`propext, Quot.sound` for 11, none for 2) and 37 reports for `BoundaryCancellation` (`propext, Quot.sound` for 30, `propext` for 4, none for 3). **Depends on:** Unit 55 (`HigherStructure`, for the dimension-0–3 motivation; neither module uses any declaration from `HigherStructure`).

</details>

## First pass

For the signed-edge pictures, use the [Path lab](../path_lab/README.md).

Draw a triangle with vertices 0, 1, and 2. Its declared **signed
boundary** is a list of edges with plus or minus signs:

`+[1,2] −[0,2] +[0,1]`.

The boundary of an edge `[a,b]` is `+[b] −[a]`. Apply that rule to each
edge, keeping the signs already present:

`+[2] −[1] −[2] +[0] +[1] −[0]`.

Each vertex has total coefficient zero: vertex 2 contributes `1 − 1`,
and the same cancellation occurs for vertices 1 and 0. A **coefficient**
is the sum of the signed contributions to one chosen vertex or face.

**Predict.** Does zero total at every vertex mean the stored list is empty?

<details>
<summary>Check your prediction</summary>

No. The unreduced list still has six terms. Zero here means every target
has coefficient zero. Replacing all signs by plus signs instead gives
coefficient 2 at each vertex. These signs are part of the supplied
construction, not a consequence of drawing a triangle.

</details>

<details>
<summary>Detailed statement and formal anchors (optional)</summary>

## Detailed claim and formal anchors

`LadderGeneral` replaces the hard-coded dimension-0–3 cell calculus of `HigherStructure` (Unit 55) with a dimension-indexed complex `ComplexN` (`cells : Nat → List (List Nat)`) and a single shell guard `shellN C k σ` uniform in `k ≥ 1`: exact vertex count `σ.length = k + 1`, strict ascent `ascB σ = true`, every facet in `facets σ` present in `C.cells (k - 1)`, and `σ` absent from `C.cells k`.

Whenever `shellN C k σ = true`, `stepN C k σ` admits `σ` into dimension `k` and strictly extends `C` (`uniform_guarded_filler`); whenever `shellN C k σ = false`, `stepN C k σ = C` (`shell_refuses_general`).

Without `ascB`, the retired guard `shellNLegacy` admits the repeated-vertex pseudo-cell `[0, 0]` over a single vertex (`pseudo_cell_countermodel`), whereas `stepV` and `stepN` preserve well-formedness (`WFComplex`: every cell in dimension `k` has length `k + 1` and strict ascent) along every event trace from `emptyN` (`wf_nreplay`).

A five-vertex replay (`d4_demo`) builds the 5/10/10/5 boundary of a 4-cell and fills `[0, 1, 2, 3, 4]`, while dropping one 3-cell leaves dimension 4 empty (`d4_guard_load_bearing`).

In `LadderGeneral.d2_zero_dims_2_3_4`, conjunct 3 genuinely checks dimension 4, whereas conjuncts 1 and 2 contain a **proof defect (vacuous statement)**: they query `coeffN e (pushN (bdN t))` at codimension-1 facets `e ∈ facets t` rather than codimension-2 faces, one dimension away from the composite chain's support. `BoundaryCancellation` closes the general question by proving `coeffN τ (pushN (bdN σ)) = 0` for *every* list `σ` and *every* `τ` (`d2_zero_unrestricted`, with `d2_zero_general`, `d2_zero_facets`, `d2_zero_replayed`, `d2_zero_d4` as corollaries): deleting `b` then `a` for `a < b` gives the same face as deleting `a` then `b - 1` (`eraseIdx_swap`) with opposite signs (`sgn_cancel`), so paired terms cancel (`dterm_cancel`) and transposing the upper triangle of the double sum kills the rectangle (`tri_transpose`, `rect_zero`).

Strict ascent is not needed for cancellation (`illformed_countermodel` on `[0, 0, 1]`), but is load-bearing for facet and codimension-2 face distinctness (`eraseIdx_inj_of_asc`, `codim2_distinct`) and transports along strictly monotone vertex renamings (`d2_zero_renamed`).

The alternating sign convention `sgn` is load-bearing: with all signs `+1`, the composite on `[0, 1, 2]` has coefficient `2` at every vertex (`signless_countermodel`).

</details>

## Question

What single guard licenses adding a cell at any finite dimension `k ≥ 1` without admitting degenerate repeated-vertex lists? And when we define the alternating-sign boundary operator on vertex lists, why does the boundary of a boundary vanish in every dimension, which declared assumption makes it vanish, and what role does strict vertex ascent actually play?

## What we already possess

- The hard-coded 0–3 cell complex of `HigherStructure` (`shell2`, `shell3`, `cstep`, `filling_not_forced`, `boundary_not_forced`), where cells up to dimension 3 were stored in separate tuple fields and the boundary calculus was written out case by case (Unit 55).
- List operations `List.eraseIdx`, `List.range`, `List.map`, `List.flatMap`, `List.filter` and `List.foldl` from Lean's core library.

## New concept: dimension-indexed complexes, the uniform shell guard, and the deletion-order pairing

A `ComplexN` holds a function `cells : Nat → List (List Nat)`. `emptyN` maps every dimension to `[]`. For a vertex list `σ : List Nat`, `facets σ` is `(List.range σ.length).map σ.eraseIdx`, the list of sublists obtained by dropping one position at a time. `ascB σ` tests whether each entry of `σ` is strictly less than the next (`a < b`).

For `k : Nat` and `σ : List Nat`, the uniform shell guard `shellN C k σ` is the conjunction of five boolean tests:
1. `σ.length = k + 1` (exact arity for a `k`-cell),
2. `1 ≤ k` (positive dimension; vertices at `k = 0` enter via `stepV`),
3. `ascB σ` (strictly ascending vertices),
4. `(facets σ).all (fun τ => decide (τ ∈ C.cells (k - 1)))` (every facet already admitted in dimension `k - 1`), and
5. `!(decide (σ ∈ C.cells k))` (the cell is not yet in dimension `k`).

`stepN C k σ` appends `σ` to `C.cells k` when `shellN C k σ` is `true` and returns `C` otherwise. `WFComplex C` states that for every `k` and every `σ ∈ C.cells k`, `σ.length = k + 1 ∧ ascB σ = true`.

For the boundary calculus, `sgn i : Int` is `1` when `i % 2 = 0` and `-1` when `i % 2 = 1`. The boundary of a cell `σ` is:

$$\text{bdN}(\sigma) = \bigl[\bigl(\text{sgn}(i),\ \sigma.\text{eraseIdx}(i)\bigr) \;\big|\; 0 \le i < |\sigma|\bigr].$$

`pushN ch` applies `bdN` to each cell in a chain `ch : List (Int × List Nat)` and multiplies the integer coefficients (`p.1 * q.1`). `coeffN τ ch` filters `ch` for pairs with `p.2 == τ` and sums their coefficients.

In `BoundaryCancellation`, `dterm σ τ i j` is the signed contribution of deleting index `i` from `σ` and then index `j` from `σ.eraseIdx i`:

$$\text{dterm}(\sigma, \tau, i, j) = \begin{cases} \text{sgn}(i)\cdot\text{sgn}(j) & \text{if } (\sigma.\text{eraseIdx}(i)).\text{eraseIdx}(j) = \tau, \\ 0 & \text{otherwise.} \end{cases}$$

`sumTo f m` sums `f 0 + ⋯ + f (m - 1)` and `sumFrom f a m` sums `f a + ⋯ + f (a + m - 1)`. `rowTri F n` and `colTri F n` sum a two-argument function `F a b` over the strict upper triangle `0 ≤ a < b < n` in row-major and column-major order.

## Plain-language interpretation

In Unit 55, adding an edge required 2 vertices, adding a triangle required 3 edges, and adding a tetrahedron required 4 triangles. `LadderGeneral` writes that rule once for all dimensions `k ≥ 1`. A `k`-cell is represented by a list of `k + 1` vertices, and its facets are the `k + 1` lists obtained by deleting one position at a time.

Why must the guard demand `ascB σ` (strictly ascending vertices)? Suppose only vertex `[0]` has been admitted into dimension `0` (`oneVertex`). Consider the candidate 1-cell `[0, 0]`. Its length is `2 = 1 + 1`, its two facets are `[0]` and `[0]`, both of which are in `oneVertex.cells 0`, and `[0, 0]` is not yet in `oneVertex.cells 1`. Without `ascB`, the legacy guard `shellNLegacy` accepts `[0, 0]` as a 1-cell (`pseudo_cell_countermodel`). Adding `ascB σ` forbids repeated vertices and makes `WFComplex` an invariant of every replay from `emptyN` (`wf_nreplay`).

Now consider the composite boundary `pushN (bdN σ)`: take the signed facets of `σ`, and then take the signed facets of each facet. Collecting the coefficient of a target list `τ` sums `dterm σ τ i j` over all pairs `(i, j)` in the `n × (n - 1)` index rectangle `0 ≤ i < n`, `0 ≤ j < n - 1`, where `n = σ.length` (`coeff_rect`).

Why does that rectangle sum vanish for *every* list `σ` and *every* target `τ`? Split each row `i` of the rectangle at the diagonal (`j < i` versus `j ≥ i`). A pair below the diagonal has `a = j < i = b`. A pair on or above the diagonal has `i = a ≤ j`, which we shift by writing `j = b - 1` with `a < b < n`. Now every unordered pair of indices `0 ≤ a < b < n` appears twice:
- once as `(b, a)`: delete position `b` first, then position `a` (which is before `b`, so its index did not shift);
- once as `(a, b - 1)`: delete position `a` first, which shifts every later position down by `1`, then delete position `b - 1` (the new index of the old position `b`).

Both deletion orders leave the exact same sublist (`eraseIdx_swap`), and their signs are `sgn b * sgn a` and `sgn a * sgn (b - 1)`. Because `b` and `b - 1` have opposite parity, `sgn b = -sgn (b - 1)`, so the two signed terms sum to `0` (`sgn_cancel`, `dterm_cancel`). Transposing the upper-triangle sum from row-major to column-major order (`tri_transpose`) pairs `(b, a)` with `(a, b - 1)` for each `a < b` and reduces the entire rectangle sum to `0` (`rect_zero`, `d2_zero_unrestricted`).

Notice two surprises that the Lean proof exposes:
1. **Strict ascent is not used in `d2_zero_unrestricted`.** The cancellation pairs index deletions `(b, a)` and `(a, b - 1)` before ever looking at what vertices sit at those indices. Even on the ill-formed list `[0, 0, 1]`, the four terms that land on `[0]` cancel in two pairs (`illformed_countermodel`). What strict ascent actually buys is *distinctness*: on an ascending list, distinct deleted indices produce distinct facets (`eraseIdx_inj_of_asc`) and distinct pairs `a < b` produce distinct codimension-2 faces (`codim2_distinct`), whereas on `[0, 0, 1]` deleting index `0` or index `1` gives the same facet `[0, 1]` with boundary coefficient `1 + (-1) = 0` (the boundary forgets a facet!).
2. **A proof defect in `LadderGeneral.d2_zero_dims_2_3_4`.** Before `BoundaryCancellation` was written, `LadderGeneral` included a finite `decide` theorem `d2_zero_dims_2_3_4` intended to spot-check composite boundary vanishing at dimensions 2, 3 and 4. Its third conjunct steps down twice from the 4-cell `[0, 1, 2, 3, 4]` (`q ∈ facets [0, 1, 2, 3, 4]`, `t2 ∈ facets q`) and checks `coeffN t2 (pushN (bdN [0, 1, 2, 3, 4])) == 0`, which is a genuine codimension-2 check. Its first two conjuncts, however, step down only *once*: for `t ∈ combs 5 2` (a 3-vertex triangle), conjunct 1 checks `coeffN e (pushN (bdN t)) == 0` for `e ∈ facets t` (a 2-vertex edge). Because `pushN (bdN t)` is supported on 1-vertex lists (`[[2], [1], [2], [0], [1], [0]]`), no 2-vertex list `e` ever matches `p.2 == e`, so `coeffN e _` returns `0` vacuously! In `u60_lean.py`, we verify that conjuncts 1 and 2 still `decide` to `true` when `bdN` is replaced by the signless `bdNoSign`, whereas the repaired two-step check at dimension 2 and conjunct 3 at dimension 4 evaluate to `false` under `bdNoSign` and `true` under `bdN`.

## Pseudocode

```
facets(sigma)        := [eraseIdx(sigma, i) for i in 0 .. |sigma| - 1]
ascB(sigma)          := all(sigma[i] < sigma[i+1] for i in 0 .. |sigma| - 2)
shellN(C, k, sigma)  := (|sigma| == k + 1) and (1 <= k) and ascB(sigma)
                        and all(tau in C.cells(k - 1) for tau in facets(sigma))
                        and (sigma not in C.cells(k))
stepN(C, k, sigma)   := C with sigma appended to C.cells(k) if shellN(C, k, sigma) else C

sgn(i)               := +1 if i % 2 == 0 else -1
bdN(sigma)           := [(sgn(i), eraseIdx(sigma, i)) for i in 0 .. |sigma| - 1]
pushN(ch)            := [(c * d, tau) for (c, s) in ch for (d, tau) in bdN(s)]
coeffN(tau, ch)      := sum(c for (c, t) in ch if t == tau)

-- Deletion-order pairing for 0 <= a < b < |sigma|:
eraseIdx(eraseIdx(sigma, b), a) == eraseIdx(eraseIdx(sigma, a), b - 1)
sgn(b) * sgn(a) + sgn(a) * sgn(b - 1) == 0
=> dterm(sigma, tau, b, a) + dterm(sigma, tau, a, b - 1) == 0
=> coeffN(tau, pushN(bdN(sigma))) == 0   for ALL lists sigma, tau
```

## Python

Genesis's mirrors, `code/derivation/attachment_ladder.py` and `code/derivation/boundary_cancellation.py`:

```python
def shell_n(cells: CellsN, k: int, sigma: tuple[int, ...]) -> bool:
    return (len(sigma) == k + 1 and k >= 1 and asc(sigma)
            and all(tau in cells.get(k - 1, [])
                    for tau in facets(sigma))
            and sigma not in cells.get(k, []))


def dterm(sigma: Cell, tau: Cell, i: int, j: int) -> int:
    if erase_idx(erase_idx(sigma, i), j) == tau:
        return sgn(i) * sgn(j)
    return 0


def swap_pair(i: int, j: int) -> tuple[int, int]:
    if j < i:
        return (j, i - 1)
    return (j + 1, i)


def pairs_cancel(sigma: Cell, tau: Cell) -> bool:
    n = len(sigma)
    return all(dterm(sigma, tau, b, a) + dterm(sigma, tau, a, b - 1) == 0
               for b in range(n) for a in range(b))
```

The book's check, `textbook/checks/u60_ladder_boundary.py`, adds Python (book):

```python
    conj1_signless_vacuous = all(
        coeff_n(e, push_no_sign(bd_no_sign(t))) == 0
        for t in combs(5, 2) for e in facets(t)
    )
    repaired_dim2_signless = all(
        coeff_n(v, push_no_sign(bd_no_sign(t))) == 0
        for t in combs(5, 2) for e in facets(t) for v in facets(e)
    )
    repaired_dim2_signed = all(
        coeff_n(v, push_n(bd_n(t))) == 0
        for t in combs(5, 2) for e in facets(t) for v in facets(e)
    )
```

## Line-by-line Python explanation

- `shell_n`: checks arity `k + 1`, `k >= 1`, `asc(sigma)`, presence of every facet in `cells.get(k - 1, [])`, and absence of `sigma` in `cells.get(k, [])`.
- `dterm`: returns `sgn(i) * sgn(j)` when the two-step deletion `erase_idx(erase_idx(sigma, i), j)` equals `tau`, and `0` otherwise.
- `swap_pair`: the fixed-point-free involution on the `n × (n - 1)` index rectangle that sends `(b, a)` (with `a < b`) to `(a, b - 1)` and `(a, b - 1)` back to `(b, a)`.
- `pairs_cancel`: checks `dterm(sigma, tau, b, a) + dterm(sigma, tau, a, b - 1) == 0` for every `0 <= a < b < len(sigma)`.
- Python (book) `conj1_signless_vacuous` vs `repaired_dim2_signless`: shows that querying `coeff_n` at 1-step facets `e in facets(t)` returns `0` even for the signless boundary operator (`True`), whereas stepping down twice to `v in facets(e)` refutes the signless boundary (`False`) and confirms the signed boundary (`True`). Note that Genesis's own Python function `d2_zero_dim` in `attachment_ladder.py` tests `{t for (_, t) in ch}` (the actual support of the composite chain), so the Python mirror was never vacuous.

## Lean 4

From `lean4/Derivation/LadderGeneral.lean` (lines 71-327, abridged):

```lean
def shellN (C : ComplexN) (k : Nat) (σ : List Nat) : Bool :=
  (decide (σ.length = k + 1)) && (decide (1 ≤ k)) && ascB σ
    && (facets σ).all (fun τ => decide (τ ∈ C.cells (k - 1)))
    && !(decide (σ ∈ C.cells k))

theorem uniform_guarded_filler (C : ComplexN) (k : Nat)
    (σ : List Nat) (h : shellN C k σ = true) :
    σ ∈ (stepN C k σ).cells k ∧ stepN C k σ ≠ C := by ...

theorem shell_refuses_general (C : ComplexN) (k : Nat)
    (σ : List Nat) (h : shellN C k σ = false) :
    stepN C k σ = C := by
  unfold stepN
  rw [if_neg (by rw [h]; exact fun hc => Bool.noConfusion hc)]

theorem pseudo_cell_countermodel :
    shellNLegacy oneVertex 1 [0, 0] = true ∧
    shellN oneVertex 1 [0, 0] = false ∧
    stepN oneVertex 1 [0, 0] = oneVertex := by
  refine ⟨by decide, by decide,
    shell_refuses_general oneVertex 1 [0, 0] (by decide)⟩

theorem wf_nreplay (h : List NEvent) :
    ∀ C, WFComplex C → WFComplex (nreplay h C) := by ...
```

From `lean4/Derivation/BoundaryCancellation.lean` (lines 207-659, abridged):

```lean
theorem eraseIdx_swap (l : List Nat) (a b : Nat) (h : a < b) :
    (l.eraseIdx b).eraseIdx a = (l.eraseIdx a).eraseIdx (b - 1) := by
  obtain ⟨c, rfl⟩ : ∃ c, b = c + 1 := ⟨b - 1, by omega⟩
  rw [show c + 1 - 1 = c from by omega]
  exact eraseIdx_eraseIdx_succ l a c (by omega)

theorem sgn_cancel (a b : Nat) (h : 0 < b) :
    sgn b * sgn a + sgn a * sgn (b - 1) = 0 := by ...

theorem dterm_cancel (σ τ : List Nat) (a b : Nat) (h : a < b) :
    dterm σ τ b a + dterm σ τ a (b - 1) = 0 := by
  unfold dterm
  rw [eraseIdx_swap σ a b h]
  exact ite_pair_cancel _ _ _ (sgn_cancel a b (by omega))

theorem rect_zero (σ τ : List Nat) :
    sumTo (fun i => sumTo (dterm σ τ i) (σ.length - 1)) σ.length = 0 := by ...

theorem d2_zero_unrestricted (σ τ : List Nat) :
    coeffN τ (pushN (bdN σ)) = 0 := by
  rw [coeff_rect]
  exact rect_zero σ τ

theorem eraseIdx_inj_of_asc :
    ∀ (l : List Nat), ascB l = true → ∀ i j, i < l.length →
      j < l.length → l.eraseIdx i = l.eraseIdx j → i = j := by ...

theorem codim2_distinct :
    ∀ (l : List Nat), ascB l = true → ∀ a b c d, a < b → c < d →
      b < l.length → d < l.length →
      (l.eraseIdx b).eraseIdx a = (l.eraseIdx d).eraseIdx c →
      a = c ∧ b = d := by ...

theorem signless_countermodel :
    ascB [0, 1, 2] = true ∧
    coeffN [0] (pushNoSign (bdNoSign [0, 1, 2])) = 2 ∧
    coeffN [1] (pushNoSign (bdNoSign [0, 1, 2])) = 2 ∧
    coeffN [2] (pushNoSign (bdNoSign [0, 1, 2])) = 2 ∧
    coeffN [0] (pushN (bdN [0, 1, 2])) = 0 ∧
    coeffN [1] (pushN (bdN [0, 1, 2])) = 0 ∧
    coeffN [2] (pushN (bdN [0, 1, 2])) = 0 := by ...

theorem illformed_countermodel :
    ascB [0, 0, 1] = false ∧
    ([0, 0, 1] : List Nat).eraseIdx 0
      = ([0, 0, 1] : List Nat).eraseIdx 1 ∧
    [0, 1] ∈ facets [0, 0, 1] ∧
    coeffN [0, 1] (bdN [0, 0, 1]) = 0 ∧
    ((pushN (bdN [0, 0, 1])).filter (fun p => p.2 == [0])).length = 4 ∧
    ((pushN (bdN [0, 1, 2])).filter (fun p => p.2 == [0])).length = 2 ∧
    coeffN [0] (pushN (bdN [0, 0, 1])) = 0 ∧
    coeffN [1] (pushN (bdN [0, 0, 1])) = 0 := by ...
```

Lean (book), from `textbook/checks/u60_lean.py`:

```lean
theorem support_dim2_is_1verts :
    (pushN (bdN [0, 1, 2])).map (·.2) = [[2], [1], [2], [0], [1], [0]] := by
  decide

theorem conj1_vacuous_signless :
    ((combs 5 2).all fun t =>
      (facets t).all fun e => coeffN e (pushNoSign (bdNoSign t)) == 0) = true := by
  decide

theorem conj2_vacuous_signless :
    ((combs 5 3).all fun q =>
      (facets q).all fun t2 => coeffN t2 (pushNoSign (bdNoSign q)) == 0) = true := by
  decide

theorem repaired_dim2_signless_fails :
    ((combs 5 2).all fun t =>
      (facets t).all fun e => (facets e).all fun v =>
        coeffN v (pushNoSign (bdNoSign t)) == 0) = false := by
  decide

theorem repaired_dim2_signed_holds :
    ((combs 5 2).all fun t =>
      (facets t).all fun e => (facets e).all fun v =>
        coeffN v (pushN (bdN t)) == 0) = true := by
  decide
```

## Line-by-line Lean explanation

- `uniform_guarded_filler`: unfolds `stepN` under `if_pos h`, projects `(stepN C k σ).cells k = C.cells k ++ [σ]`, gets membership from `List.mem_cons_self`, and gets `stepN C k σ ≠ C` because the length of `cells k` increased by `1`.
- `wf_nreplay`: induction on the event list `h`, using `wf_stepV` (which checks `[v].length = 1` and `ascB [v] = true`) and `wf_stepN` (which extracts `σ.length = k + 1` and `ascB σ = true` from `shellN C k σ = true`).
- `eraseIdx_swap`: writes `b = c + 1` for `a ≤ c` and calls `eraseIdx_eraseIdx_succ`, which inducts on the list `l` and index `a`.
- `sgn_cancel`: writes `b = c + 1`, applies `sgn_succ : sgn (c + 1) = -sgn c`, and uses `Int.neg_mul`, `Int.neg_neg` and `Int.mul_comm`.
- `coeff_rect`: rewrites `coeffN τ (pushN (bdN σ))` via `coeff_push_bd` into a double `sumTo` with inner bound `(σ.eraseIdx i).length`, then replaces that inner bound by `σ.length - 1` using `List.length_eraseIdx_of_lt` inside `sumTo_congr`.
- `rect_zero`: splits each row `i` at `i` via `sumTo_split` into the lower triangle `sumTo (dterm σ τ i) i` and the upper triangle `sumFrom (dterm σ τ i) i (σ.length - 1 - i)`; shifts the upper index by `sumFrom_shift` to form `rowTri (fun a b => dterm σ τ a (b - 1)) σ.length`; applies `tri_transpose` to convert `rowTri` into `colTri`; and folds the two sums together into `sumTo (fun b => sumTo (fun a => dterm σ τ b a + dterm σ τ a (b - 1)) b) σ.length`, where every inner term vanishes by `dterm_cancel`.
- `eraseIdx_inj_of_asc` and `codim2_distinct`: induct on `l : List Nat`. For `x :: y :: t` with `x < y` and `ascB (y :: t)`, `ascB_head_lt` proves `x` is strictly below every element of `y :: t`. If deleting index `0` (`y :: t`) agreed with deleting index `j + 1` (`x :: (y :: t).eraseIdx j`), their heads would give `y = x`, contradicting `x < y`. For `codim2_distinct`, if `a = 0` and `c > 0`, `x` would appear as the head of `(l.eraseIdx d).eraseIdx c` and also lie in `(y :: t).eraseIdx b'`, contradicting `x < z` for all `z ∈ y :: t`.
- Book `conj1_vacuous_signless`, `conj2_vacuous_signless`, `repaired_dim2_signless_fails`, `repaired_dim2_signed_holds`: kernel-checked proof of the audit's vacuity finding on `d2_zero_dims_2_3_4`.

## What has been proved

- In `LadderGeneral`: `uniform_guarded_filler` (100), `shell_refuses_general` (122), `shell_no_self_fill` (130), `pseudo_cell_countermodel` (146), `wf_empty` (158), `wf_stepV` (162), `wf_stepN` (182), `wf_nstep` (223), `wf_nreplay` (233), `d4_demo` (269), `d4_wf` (279), `d4_guard_load_bearing` (292), `d2_zero_dims_2_3_4` (318, conjunct 3 non-vacuous; conjuncts 1–2 vacuous).
- In `BoundaryCancellation`: `sumTo_const_zero` (104), `sumTo_congr` (111), `sumTo_add` (119), `sumTo_split` (129), `sumFrom_shift` (139), `tri_transpose` (159), `eraseIdx_eraseIdx_succ` (193), `eraseIdx_swap` (207), `sgn_succ` (215), `sgn_cancel` (222), `coeffN_nil` (233), `foldl_acc` (235), `coeffN_append` (245), `coeffN_singleton` (253), `coeffN_map_range` (262), `coeffN_flatMap_range` (277), `coeff_push_bd` (296), `coeff_rect` (313), `ite_pair_cancel` (323), `dterm_cancel` (333), `rect_zero` (339), `d2_zero_unrestricted` (377), `d2_zero_general` (387), `d2_zero_facets` (395), `d2_zero_replayed` (406), `d2_zero_d4` (415), `ascB_tail` (423), `ascB_head_lt` (428), `eraseIdx_inj_of_asc` (442), `codim2_distinct` (485), `eraseIdx_map` (534), `ascB_map` (545), `d2_zero_renamed` (568), `d2_zero_shift` (580), `signless_countermodel` (607), `signless_countermodel_dim3` (622), `illformed_countermodel` (648).

## What has not been proved

- **Proof defect in `LadderGeneral.d2_zero_dims_2_3_4` (audit finding 1 of `LadderGeneral.md`).** Conjuncts 1 and 2 of `d2_zero_dims_2_3_4` test `coeffN e (pushN (bdN t)) == 0` for `e ∈ facets t` (codimension 1) instead of stepping down twice to codimension 2. Because `pushN (bdN t)` has cells of length `t.length - 2` while `e` has length `t.length - 1`, `p.2 == e` is always `false` and both conjuncts are vacuously `true` (even for the signless calculus, as proved in `u60_lean.py`). Conjunct 3 at dimension 4 is non-vacuous, and `BoundaryCancellation.d2_zero_unrestricted` (together with `repaired_dim2_signed_holds` and `repaired_dim3_signed_holds` in `u60_lean.py`) closes the evidential gap completely.
- Any connection between `shellN` and the passage's obstruction predicate `obstP`. Audit finding 2 of `LadderGeneral.md`: the docstring phrase "the two-rule shape (obstruction-shaped precondition, structure-creating response)" at line 97 of `LadderGeneral.lean` is an analogy. `LadderGeneral` and `BoundaryCancellation` operate on `ComplexN` and `List Nat`; no passage state, protection store, or observation column appears in either module.
- Any homology claim (cycles, boundaries, or quotient groups). What is proved is the guarded admission step (`uniform_guarded_filler`) and the coefficientwise vanishing of `pushN (bdN σ)` (`d2_zero_unrestricted`).
- That the hypotheses `_hasc : ascB σ = true` and `_hlen : 2 ≤ σ.length` in `d2_zero_general`, `d2_zero_facets`, `d2_zero_replayed` and `d2_zero_d4` are used in the vanishing proof. They are recorded to match the posed statements and discharged immediately by `d2_zero_unrestricted` (`BoundaryCancellation.md` §11).
- In Lean, the quantitative count that every codimension-2 face of an ascending cell collects *exactly two* ordered deletion pairs. `BoundaryCancellation` proves injectivity of unordered deletion pairs on codimension-2 faces (`codim2_distinct`) and decides the slot counts `2` (for `[0, 1, 2]`) and `4` (for `[0, 0, 1]`) in `illformed_countermodel`; the exhaustive multiplicity-2 check over dimensions 2–6 (`218` cells) is in Python (`perfect_matching`).

## Outside the system

- `ComplexN.cells : Nat → List (List Nat)` is a metatheoretic function over all `Nat`, and `WFComplex` quantifies over `∀ k`. Every complex replayed from `emptyN` by a finite event list `h : List NEvent` has finite support (for instance `d4Complex` has cells only in dimensions 0–4).
- `sumTo`, `sumFrom`, `rowTri` and `colTri` take functions `Nat → Int` and `Nat → Nat → Int` as metatheoretic summation apparatus; every sum evaluated in `coeff_rect` and `rect_zero` is bounded by `σ.length`.
- Integer coefficients (`Int`), the alternating sign `sgn i = (-1)^i`, and the ascending-list cell encoding are admitted conventions of the realization layer. `signless_countermodel` proves that `uniform_guarded_filler` does not force the sign convention.

## Student exercise

In `BoundaryCancellation.d2_zero_renamed`, the hypothesis `hr : ∀ x y, x < y → r x < r y` (strict monotonicity of `r : Nat → Nat`) is assumed, and four conjuncts are proved for `σ.map r`:
1. `ascB (σ.map r) = true`,
2. `(σ.map r).length = σ.length`,
3. `∀ i, (σ.map r).eraseIdx i = (σ.eraseIdx i).map r`, and
4. `∀ τ, coeffN τ (pushN (bdN (σ.map r))) = 0`.

Which of the four conjuncts actually depend on `hr` and `hasc : ascB σ = true`, and what happens to all four conjuncts when `σ = [0, 1, 2]` and `r` is the non-monotone bijection `0 ↦ 2, 1 ↦ 0, 2 ↦ 1`?

<details>
<summary>Student exercise answer</summary>

Only conjunct 1 (`ascB (σ.map r) = true`, proved by `ascB_map r hr σ hasc`) uses `hr` or `hasc`. Conjunct 2 is `List.length_map`, which holds for any function `r` and any list `σ`. Conjunct 3 is `eraseIdx_map`, proved by structural induction on `σ` and `i` for any function `r`. Conjunct 4 holds for *every* list `σ.map r` and *every* `τ` by `d2_zero_unrestricted (σ.map r) τ`, without needing `hr`, `hasc` or `hlen`. When `σ = [0, 1, 2]` and `r` sends `0 ↦ 2, 1 ↦ 0, 2 ↦ 1`, the mapped list is `[2, 0, 1]`: conjunct 1 fails (`ascB [2, 0, 1] = false` because `2 < 0` is false), while conjuncts 2, 3 and 4 all still hold (`scrambled_triangle_cancels` in `u60_lean.py`).

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/LadderGeneral.lean` lines 51-93 (`ComplexN`, `shellN`, `stepN`), 100-137 (`uniform_guarded_filler`, `shell_refuses_general`), 140-243 (`pseudo_cell_countermodel`, `WFComplex`, `wf_nreplay`), 246-294 (`d4_demo`, `d4_guard_load_bearing`), 299-329 (boundary definitions, `d2_zero_dims_2_3_4`); `lean4/Derivation/BoundaryCancellation.lean` lines 95-188 (`sumTo`, `tri_transpose`), 193-230 (`eraseIdx_swap`, `sgn_cancel`), 233-370 (`coeff_rect`, `dterm_cancel`, `rect_zero`), 377-420 (`d2_zero_unrestricted`, `d2_zero_replayed`), 423-531 (`eraseIdx_inj_of_asc`, `codim2_distinct`), 534-588 (`d2_zero_renamed`), 592-661 (`signless_countermodel`, `illformed_countermodel`) |
| Axiom report | `artifacts/lean_axioms.txt` lines 710-722 (`LadderGeneral`, 13 reports) and lines 821-857 (`BoundaryCancellation`, 37 reports) |
| Paper | `paper/primitive_difference_map.md` §8; `paper/paper_claim_ledger.md` `CL-PD2-LADDER-GENERAL`, `CL-PD2-BOUNDARY-CANCELLATION` |
| Python | `code/derivation/attachment_ladder.py` (section 5), `code/derivation/boundary_cancellation.py`, `code/run_attachment_ladder.py`, `code/run_boundary_cancellation.py`, `tests/test_attachment_ladder.py`, `tests/test_boundary_cancellation.py`, `artifacts/attachment_ladder.json`, `artifacts/boundary_cancellation.json` |
| Audit | `textbook/audit/modules/LadderGeneral.md`, `textbook/audit/modules/BoundaryCancellation.md`, `textbook/audit/probes/E/lg_vacuity.lean` |
| Check (Python) | `python textbook/checks/u60_ladder_boundary.py`: `ladder_report(5)`, `pseudo_cell_countermodel`, Python (book) vacuity probe on `d2_zero_dims_2_3_4` conjuncts 1–2, `cancellation_report` (218 cells, 3124 checks), `renaming_report`, `signless_countermodel`, `illformed_countermodel`, artifact comparison |
| Check (book Lean) | `python textbook/checks/u60_lean.py`: ten book theorems (including the vacuity proofs `conj1_vacuous_signless`, `conj2_vacuous_signless` and the repaired dimension-2/3 checks) plus twenty-five Genesis theorems kernel-checked, Lean 4.33.0 |
