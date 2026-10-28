# Unit 42. Counting without choosing, and how many things a bounded window can tell apart

**Claim.** Two modules. `Pigeonhole` is apparatus: a duplicate-free list
of naturals below `B` has at most `B` entries (`nodup_length_le`), and a
map from `B + 1` indices into `B` values collides (`pigeonhole`), both
proved inside `{propext, Quot.sound}`. The point of the module is *how*:
the usual route through `n == n` at `Nat` carries `Classical.choice` on
this toolchain, so the proof uses `decide (x = B)` and a hand-written
index list instead of `List.range`. `CapacityBound` spends that
pigeonhole on Unit 41's chain. Colour the indices with `k` colours and
let a view `v` depend only on the colours in the radius-`d` window
(`ViewLocal`). Then the window has at most `k^(2d + 1)` distinguishable
colourings, so once `n ≥ k^(2d + 1) + 2d + 2` two deep points have equal
views (`capacity_bound`). The bound `B = k^(2d + 1)` is derived from
locality, not assumed, and does not grow with `n`. Two fixtures show the
theorem has content: one colour collapses everything
(`capacity_at_one_colour`), and at `k = 2, d = 0, n = 3`, below the
threshold 4, a parity view separates every deep pair
(`local_view_can_separate`). **Status:** derived; the Pigeonhole module
is declared metatheory apparatus. Not claimed: tightness of
`k^(2d + 1)`, anything for non-local views, anything about Genesis's own
profile colouring. **Lean:** `lean4/Derivation/Pigeonhole.lean` lines
51-230; `lean4/Derivation/CapacityBound.lean` lines 59-252. **Axioms:**
`{propext, Quot.sound}`; `local_view_blind` and `upto_length` none.
**Depends on:** `ball`, `ball_length` (Unit 41); `List.Nodup` as
`Pairwise`, `List.filter`, `List.map`, `decide`.

## Question

Unit 41 proved that structural observation at any fixed radius is outrun.
But a repair strategy could *colour* the chain, marking elements, and let
the observer read colours in its window. With `k` colours and radius `d`,
how many elements can such an observer tell apart? If the answer is a
number that does not depend on the chain's length, a long enough chain
defeats it. Underneath that: counting requires pigeonhole, and the
repository's audit gate bars `Classical.choice`. Can pigeonhole be proved
without it?

## What we already possess

- The ball `ball i d` and the deep interior `d < i ∧ i + d < n` (Unit 41).
- `List.Nodup` as "pairwise distinct", `List.filter`, `List.map`.
- The audit gate: every `Derivation` constant must use at most `propext`
  and `Quot.sound` (CLAUDE.md, "the axiom boundary").

## New concept: a choice-free count, a local view, and a capacity

*Counting.* Split a duplicate-free list below `B + 1` by the test
`x = B`: the part equal to `B` has at most one entry (no duplicates), the
rest is duplicate-free below `B`; induct. The test must be written
`decide (x = B)`. On Lean 4.33.0, `x == B` at `Nat` goes through the
`ReflBEq Nat` instance, which carries `Classical.choice`; the `decide`
route does not (the book check measures both). The pigeonhole then maps
`B + 1` indices through `f` into values below `B`: if no two collided the
image list would be duplicate-free of length `B + 1` below `B`.

*Locality.* `colourBall colour i d` is the list of colours along the
window. `ViewLocal v colour d` says `v i = g (colourBall colour i d)` for
some `g`: the view reads the window and nothing else, in particular not
the index. A local view cannot separate two points with equal colour
windows (`local_view_blind`).

*Capacity.* A window of length `2d + 1` over `k` colours has at most
`k^(2d + 1)` colourings, and a base-`k` encoding (`encode`) carries each
window to a distinct number below `k^(2d + 1)`. The deep interior of the
chain of length `n` has `n − 2d − 1` points; at `n = k^(2d + 1) + 2d + 2`
it has `B + 1` of them, and pigeonhole gives two with equal windows.

## Plain-language interpretation

Give the observer coloured pens, `k` colours, and let them colour the
chain however they like, then look at a window of `2d + 1` elements and
report what they see. They can see at most `k^(2d + 1)` different
pictures, however long the chain is, because that is how many ways a
window of that size can be coloured. Put more deep elements in the chain
than there are pictures and two of them must show the same picture, and
the observer, who sees only pictures, cannot tell them apart.

The counting fact behind this is pigeonhole: more pigeons than holes,
two share a hole. The module's care is in proving that without a tool
the repository forbids. The forbidden tool hides in an innocent place: a
test for `n == n` on numbers, whose library instance happens to reach for
the axiom of choice. Writing the test as `decide (n = n)` avoids it.

What the theorem does not say: that `k^(2d + 1)` is the true number of
pictures an observer can use (only that it is an upper bound); anything
about an observer who reads the index itself, which is Unit 40's valued
mark and is not local; and anything about the particular colours
Genesis's own profile would paint.

## Pseudocode

```
-- counting
nodup_length_le B l:  l duplicate-free, every x in l below B  ⟹  length l ≤ B
  induction on B; split l by decide (x = B): ≤ 1 equal to B, rest below B
pigeonhole B f:  (∀ p < B+1, f p < B)  ⟹  ∃ p ≠ q < B+1, f p = f q
  else map f over [B, ..., 0] is duplicate-free, length B+1, below B

-- capacity
encode k []       = 0
encode k (x :: t) = x + k * encode k t        -- < k^length; injective at fixed length
colourBall c i d  = map c (ball i d)
ViewLocal v c d   = ∃ g, ∀ i, v i = g (colourBall c i d)
capacity_bound: colours below k, v local at radius d, n ≥ k^(2d+1) + 2d + 2
  ⟹ ∃ deep i ≠ j with v i = v j
  proof: t ↦ encode k (colourBall c (d+1+t) d) maps B+1 indices below B = k^(2d+1);
         pigeonhole; encode injective ⟹ equal windows ⟹ equal views
```

## Python

Genesis has no Python for these modules. The check rebuilds `encode`,
`colourBall` and the deep interior (Python (book)) and searches small
cases exhaustively.

```python
import itertools

def ball(i, d): return [max(i - d, 0) + k for k in range(2 * d + 1)]
def encode(k, l): return 0 if not l else l[0] + k * encode(k, l[1:])
def deep_points(n, d): return [i for i in range(n + 1) if d < i and i + d < n]

k, d = 2, 1
n = k ** (2 * d + 1) + 2 * d + 2
pts = deep_points(n, d)
collide = all(len({encode(k, [c[x] for x in ball(i, d)]) for i in pts}) < len(pts)
              for c in itertools.product(range(k), repeat=n + 1))
print(n, pts, collide)
```

Output:

```text
12 [2, 3, 4, 5, 6, 7, 8, 9, 10] True
```

The check script's run:

```text
duplicate-free lists below 3 have length <= 3: True (16 lists); 4 indices into 3 values collide: [(0, 3)]
encode 2 over the 8 colour lists of length 3: [0, 4, 2, 6, 1, 5, 3, 7]; all below 2^3: True; injective: True
k, d: threshold; deep points there; every colouring of 0..n collides on a deep pair
  1, 0: 3; [1, 2] (2 points, 1 possible balls); True
  1, 1: 5; [2, 3] (2 points, 1 possible balls); True
  2, 0: 4; [1, 2, 3] (3 points, 2 possible balls); True
  2, 1: 12; [2, 3, 4, 5, 6, 7, 8, 9, 10] (9 points, 8 possible balls); True
  3, 0: 5; [1, 2, 3, 4] (4 points, 3 possible balls); True
k, d: n = threshold - 1; a colouring whose radius-d view separates every deep pair
  2, 0: 3; deep [1, 2]; colouring [0, 0, 1, 0]
  2, 1: 11; deep [2, 3, 4, 5, 6, 7, 8, 9]; colouring [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0]
  3, 0: 4; deep [1, 2, 3]; colouring [0, 0, 1, 2, 0]
parity view at n = 3, d = 0: deep points [1, 2], views [1, 0], separated: True
failures: []
```

## Line-by-line Python explanation

The first block enumerates every duplicate-free list over `{0, 1, 2}` (16
of them, the empty list included) and checks none is longer than 3; then
maps the four indices `0..3` through `t % 3` and finds the collision
`(0, 3)`. The second block lists the eight base-2 encodings of 3-bit
windows: all below 8 and pairwise distinct, the two facts `encode_lt` and
`encode_inj` state in general.

The third block is the bound, brute-forced: for each `(k, d)` it takes
`n` at the threshold, lists the deep points (always `k^(2d + 1) + 1` of
them, one more than the possible windows), and checks that *every*
colouring of `0..n` gives two deep points the same encoded window. The
fourth block goes one below the threshold and finds a colouring whose
windows are all distinct on the deep points, so the threshold is not
slack in these cases. At `k = 2, d = 1` the colouring found along
positions `1..10` is `0, 0, 0, 1, 0, 1, 1, 1, 0, 0`, whose eight 3-windows
are the eight binary words: a de Bruijn sequence. Genesis exhibits only
the `d = 0` witness; this `d = 1` witness is the book's, and the book
Lean below proves it. The last line is Genesis's own fixture, parity at
`n = 3`.

Nothing here is a proof of `capacity_bound`; the searches are finite
instances of a theorem that holds for every `k`, `d`, `n` and every
colouring and local view.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Pigeonhole.lean lines 113-166, 173-175, 215-230
theorem nodup_filter_eq_le_one (B : Nat) :
    ∀ l : List Nat, List.Nodup l →
      (l.filter (fun x => decide (x = B))).length ≤ 1
  | [], _ => Nat.zero_le 1
  | x :: t, hnd => by
      rw [List.filter_cons]
      cases hp : (decide (x = B)) with
      | true =>
          show (x :: t.filter (fun y => decide (y = B))).length ≤ 1
          have hxB : x = B := of_decide_eq_true hp
          have hnone : ∀ y ∈ t, (decide (y = B)) = false := by
            intro y hy
            refine decide_eq_false ?_
            intro hyB
            exact nodup_head hnd y hy (hxB.trans hyB.symm)
          rw [filter_eq_nil_of_none _ t hnone]
          exact Nat.le_refl 1
      | false =>
          show (t.filter (fun y => decide (y = B))).length ≤ 1
          exact nodup_filter_eq_le_one B t (nodup_tail hnd)

theorem nodup_length_le :
    ∀ (B : Nat) (l : List Nat), List.Nodup l → (∀ x ∈ l, x < B) →
      l.length ≤ B
  | 0, l, _, hb => by
      cases l with
      | nil => exact Nat.le_refl 0
      | cons x t =>
          exact absurd (hb x (List.mem_cons_self ..)) (Nat.not_lt_zero x)
  | B + 1, l, hnd, hb => by
      have hsplit := length_filter_split (fun x => decide (x = B)) l
      have h1 : (l.filter (fun x => decide (x = B))).length ≤ 1 :=
        nodup_filter_eq_le_one B l hnd
      have h2 : (l.filter (fun x => !(decide (x = B)))).length ≤ B := by
        refine nodup_length_le B _ (filter_nodup _ l hnd) ?_
        intro x hx
        have hm := List.mem_filter.mp hx
        have hlt : x < B + 1 := hb x hm.1
        have hne : x ≠ B := by
          have hb2 : ((!(decide (x = B))) = true) := hm.2
          cases hd : (decide (x = B)) with
          | false => exact of_decide_eq_false hd
          | true =>
              rw [hd] at hb2
              exact Bool.noConfusion hb2
        omega
      omega

def upto : Nat → List Nat
  | 0 => []
  | n + 1 => n :: upto n

theorem pigeonhole (B : Nat) (f : Nat → Nat)
    (hf : ∀ p, p < B + 1 → f p < B) :
    ∃ p, p < B + 1 ∧ ∃ q, q < B + 1 ∧ p ≠ q ∧ f p = f q := by
  refine Decidable.byContradiction ?_
  intro hcon
  have hinj : ∀ p, p < B + 1 → ∀ q, q < B + 1 → p ≠ q → f p ≠ f q :=
    fun p hp q hq hpq hfe => hcon ⟨p, hp, q, hq, hpq, hfe⟩
  have hnd : List.Nodup ((upto (B + 1)).map f) :=
    map_nodup_of_inj f (B + 1) hinj
  have hall : ∀ y ∈ (upto (B + 1)).map f, y < B := by
    intro y hy
    obtain ⟨x, hx, rfl⟩ := List.mem_map.mp hy
    exact hf x (upto_mem (B + 1) x hx)
  have hle := nodup_length_le B ((upto (B + 1)).map f) hnd hall
  rw [List.length_map, upto_length] at hle
  omega
```

```lean
-- Lean (Genesis), lean4/Derivation/CapacityBound.lean lines 59-61, 70-71, 90-93, 131-132, 151-161, 178-200, 227-235
def encode (k : Nat) : List Nat → Nat
  | [] => 0
  | x :: t => x + k * encode k t

theorem encode_lt (k : Nat) :
    ∀ l : List Nat, (∀ x ∈ l, x < k) → encode k l < k ^ l.length
  ...
theorem encode_inj (k : Nat) :
    ∀ l m : List Nat, l.length = m.length →
      (∀ x ∈ l, x < k) → (∀ x ∈ m, x < k) →
      encode k l = encode k m → l = m
  ...

def colourBall (colour : Nat → Nat) (i d : Nat) : List Nat :=
  (ball i d).map colour

def ViewLocal (v : Nat → Nat) (colour : Nat → Nat) (d : Nat) : Prop :=
  ∃ g : List Nat → Nat, ∀ i, v i = g (colourBall colour i d)

theorem local_view_blind {v colour : Nat → Nat} {d : Nat}
    (hloc : ViewLocal v colour d) {i j : Nat}
    (hball : colourBall colour i d = colourBall colour j d) :
    v i = v j := by
  obtain ⟨g, hg⟩ := hloc
  rw [hg i, hg j, hball]

theorem capacity_bound (colour v : Nat → Nat) (k d n : Nat)
    (hk : ∀ x, colour x < k)
    (hloc : ViewLocal v colour d)
    (hn : k ^ (2 * d + 1) + 2 * d + 2 ≤ n) :
    ∃ i j, i ≠ j ∧ d < i ∧ i + d < n ∧ d < j ∧ j + d < n ∧ v i = v j := by
  have hcode : ∀ t : Nat, t < k ^ (2 * d + 1) + 1 →
      encode k (colourBall colour (d + 1 + t) d) < k ^ (2 * d + 1) := by
    intro t _
    have hlen := colourBall_length colour (d + 1 + t) d
    have hbd := colourBall_bounded colour k hk (d + 1 + t) d
    have hlt := encode_lt k (colourBall colour (d + 1 + t) d) hbd
    rw [hlen] at hlt
    exact hlt
  obtain ⟨p, hp, q, hq, hpq, heq⟩ :=
    pigeonhole (k ^ (2 * d + 1))
      (fun t => encode k (colourBall colour (d + 1 + t) d)) hcode
  refine ⟨d + 1 + p, d + 1 + q, by omega, by omega, by omega, by omega,
    by omega, ?_⟩
  refine local_view_blind hloc ?_
  refine encode_inj k _ _ ?_ ?_ ?_ heq
  · rw [colourBall_length, colourBall_length]
  · exact colourBall_bounded colour k hk _ _
  · exact colourBall_bounded colour k hk _ _

theorem local_view_can_separate :
    ∃ (colour v : Nat → Nat),
      (∀ x, colour x < 2) ∧
      ViewLocal v colour 0 ∧
      0 < 1 ∧ 1 + 0 < 3 ∧ 0 < 2 ∧ 2 + 0 < 3 ∧
      3 < 2 ^ (2 * 0 + 1) + 2 * 0 + 2 ∧
      v 1 ≠ v 2 ∧
      (∀ i j, 0 < i → i + 0 < 3 → 0 < j → j + 0 < 3 →
        i ≠ j → v i ≠ v j) := by
  ...
```

The book's Lean measures the trap, instantiates the counting lemma and
the pigeonhole, computes encodings and a colour window, exhibits a local
view with its `g`, applies the bound at `k = 2, d = 0, n = 4`, and proves
the `d = 1` below-threshold witness that Genesis does not have.

```lean
-- Lean (book), textbook/checks/u42_lean.py
theorem beq_trap (n : Nat) : (n == n) = true := beq_self_eq_true n
theorem decide_route (n : Nat) : decide (n = n) = true := decide_eq_true rfl

theorem upto_three : upto 3 = [2, 1, 0] := rfl

theorem counting_instance : ([0, 2, 1] : List Nat).length ≤ 3 :=
  nodup_length_le 3 _ (by decide) (by decide)

theorem four_into_three :
    ∃ p, p < 4 ∧ ∃ q, q < 4 ∧ p ≠ q ∧ (fun t => t % 3) p = (fun t => t % 3) q :=
  pigeonhole 3 (fun t => t % 3) (fun p _ => Nat.mod_lt p (by decide))

theorem encode_examples : encode 2 [1, 0, 1] = 5 ∧ encode 2 [1, 1, 1] = 7 ∧ encode 3 [2, 2] = 8 := by
  decide

theorem parity_ball : colourBall (fun x => x % 2) 2 1 = [1, 0, 1] := by decide

theorem parity_view_local :
    ViewLocal (fun i => encode 2 (colourBall (fun x => x % 2) i 1)) (fun x => x % 2) 1 :=
  ⟨encode 2, fun _ => rfl⟩

theorem parity_blind_two_four :
    (fun i => encode 2 (colourBall (fun x => x % 2) i 1)) 2 =
    (fun i => encode 2 (colourBall (fun x => x % 2) i 1)) 4 :=
  local_view_blind parity_view_local (by decide)

theorem threshold_values :
    2 ^ (2 * 0 + 1) + 2 * 0 + 2 = 4 ∧ 2 ^ (2 * 1 + 1) + 2 * 1 + 2 = 12 ∧
    3 ^ (2 * 1 + 1) + 2 * 1 + 2 = 31 := by decide

theorem capacity_two_zero_four :
    ∃ i j, i ≠ j ∧ 0 < i ∧ i + 0 < 4 ∧ 0 < j ∧ j + 0 < 4 ∧
      (fun x => x % 2) i = (fun x => x % 2) j :=
  capacity_bound (fun x => x % 2) (fun x => x % 2) 2 0 4
    (fun x => Nat.mod_lt x (by decide)) ⟨fun l => l.headD 0, fun _ => rfl⟩ (by decide)

def deBruijn : Nat → Nat := fun i => [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0].getD i 0

theorem deBruijn_windows :
    (List.range 8).map (fun t => encode 2 (colourBall deBruijn (t + 2) 1)) =
      [0, 4, 2, 5, 6, 7, 3, 1] := by
  decide

theorem deBruijn_separates_deep :
    ∀ i ∈ [2, 3, 4, 5, 6, 7, 8, 9], ∀ j ∈ [2, 3, 4, 5, 6, 7, 8, 9], i ≠ j →
      encode 2 (colourBall deBruijn i 1) ≠ encode 2 (colourBall deBruijn j 1) := by
  decide
```

The check asserts the axiom report of `beq_trap` is
`[propext, Classical.choice, Quot.sound]` and that of `decide_route` is
empty: a measurement of the toolchain, not a Genesis result.

## Line-by-line Lean explanation

**`nodup_head`, `nodup_tail` (Pigeonhole 51-59).** `List.Nodup` is
`Pairwise (· ≠ ·)`; `cases` on its `cons` constructor yields the head's
inequalities against the tail and the tail's own `Nodup`. The module
destructs the constructor directly rather than through a library lemma,
keeping the axiom trail short.

**`length_filter_split`, `filter_eq_nil_of_none`, `filter_nodup`
(63-106).** Structural recursion on the list. Filtering by `p` and by
`not p` splits the length additively (`List.filter_cons`, then `omega`
in each branch of `p x`); a test false everywhere filters to `[]`;
filtering keeps `Nodup` (the kept head is still distinct from every kept
tail element, by `List.mem_filter`).

**`nodup_filter_eq_le_one` (113-132).** Filter a duplicate-free list for
`decide (x = B)`. If the head passes, `x = B` by `of_decide_eq_true`,
and every tail element fails the test because it differs from `x`
(`nodup_head`), so the filtered tail is `[]` and the length is 1. If the
head fails, recurse. The `decide` is the whole point: `of_decide_eq_true`
and `decide_eq_false` are choice-free, where the `BEq` lemmas at `Nat`
are not (module header; measured by the book's `beq_trap`).

**`nodup_length_le` (141-166).** Induction on `B`. At `B = 0` the list
must be empty, since no natural is below 0. At `B + 1`, split by
`decide (x = B)`: the equal part has length at most 1, the rest is
duplicate-free (`filter_nodup`) and below `B` (an element is `< B + 1`
and `≠ B`, the latter read off the negated `decide` by cases on its
value), so by induction at most `B`; `omega` adds. The book's
`counting_instance` is the case `B = 3, l = [0, 2, 1]`.

**`upto`, `upto_length`, `upto_mem`, `map_nodup_of_inj` (173-205).**
`upto n` is `[n − 1, …, 0]`, defined by recursion because
`List.nodup_range` is choice-dependent on this toolchain. Its length is
`n`, its members are below `n`, and mapping an injective-on-`[0, n)`
function over it gives a duplicate-free list (head `f n` differs from
every `f x` with `x < n`; tail by induction). The book's `upto_three`
is `[2, 1, 0]`.

**`pigeonhole` (215-230).** By contradiction (decidable: the
existential is written with each bound immediately guarding its binder,
the docstring explains why). If no two indices collide, `f` is
injective on `[0, B + 1)`, so its image list over `upto (B + 1)` is
duplicate-free, of length `B + 1`, and below `B`: contradicting
`nodup_length_le`. The audit notes that at `B = 0` the hypothesis
`∀ p < 1, f p < 0` is unsatisfiable, so the theorem is vacuous there and
contentful from `B = 1`. The book's `four_into_three` is `B = 3`.

**`encode`, `encode_lt`, `encode_inj` (CapacityBound 59-126).** Base-`k`
positional encoding, least digit first. `encode_lt`: for a list of
digits below `k`, the value is below `k^length`, by recursion with
`Nat.mul_le_mul_left` and `Nat.pow_succ`. `encode_inj`: two digit lists
of equal length with equal encodings are equal; the proof compares tails
by trichotomy (if the tails' encodings differed by at least 1, the
values would differ by at least `k`, more than the heads can make up),
then reads the heads off, then recurses. The book's `encode_examples`
and `encode_bound_instance` are instances.

**`colourBall`, `ViewLocal`, `local_view_blind` (131-161).** The window
of colours; locality as factoring through it; and the one-line
consequence that equal windows give equal views (rewrite both by `g`,
then by the window equality). `local_view_blind` uses no axioms. The
book's `parity_view_local` exhibits `g = encode 2` for the radius-1
parity view, and `parity_blind_two_four` applies blindness to the equal
windows `[1, 0, 1]` at 2 and at 4.

**`capacity_bound` (178-200).** Set `B = k^(2d + 1)`. The map
`t ↦ encode k (colourBall colour (d + 1 + t) d)` sends each
`t ≤ B` to a value below `B` (`hcode`: the window has length `2d + 1`
and digits below `k`, so `encode_lt`). Pigeonhole gives `p ≠ q ≤ B` with
equal encodings. The points `d + 1 + p` and `d + 1 + q` are deep when
`n ≥ B + 2d + 2` (five `omega` goals), and their windows are equal by
`encode_inj` (same length, digits bounded), so their views are equal by
`local_view_blind`. The audit's note: the statement never mentions
`reflState`; it is a fact about index-local functions on `Nat`, and the
chain enters as the name of the index range `(d, n − d)`. That is why it
applies to any colouring of the chain, and why it says nothing about the
successor relation. The book's `capacity_two_zero_four` is the smallest
instance with content, `k = 2, d = 0, n = 4`: three deep points, two
colours.

**The fixtures (212-252).** `capacity_at_one_colour` is the bound at
`k = 1`, whose conclusion `0 = 0` is trivial; its content is the deep
pair, which is already Unit 41's. `local_view_can_separate` is the
falsifiability witness: at `k = 2, d = 0, n = 3`, strictly below the
threshold 4, the parity view is local (`g = headD 0` on the one-element
window) and separates the two deep points, so the theorem's conclusion
is false there and the threshold is doing work. The book's de Bruijn
pair extends the witness to radius 1: with the colouring
`0, 0, 0, 1, 0, 1, 1, 1, 0, 0` along `1..10`, the eight deep points of
the chain of length 11 (threshold 12) have the eight distinct encoded
windows `[0, 4, 2, 5, 6, 7, 3, 1]`. Neither witness proves tightness in
general; the module claims none.

**The stale non-claim.** The module header says nothing here bears on
`LocalStrategy`, "none of which exist in this repository". `LocalStrategy`
exists and consumes `capacity_bound`; the audit records the line as a
stale docstring. Unit 43 teaches that module.

## What has been proved

- The counting lemma and the pigeonhole for `Nat`, inside
  `{propext, Quot.sound}` (Genesis).
- `encode` is bounded by `k^length` and injective at fixed length
  (Genesis).
- A local view cannot separate equal colour windows (Genesis, no
  axioms).
- For every bounded colouring and local view, a deep collision from
  `n ≥ k^(2d + 1) + 2d + 2` (Genesis).
- Below the threshold a separating local view exists at `k = 2, d = 0`
  (Genesis) and at `k = 2, d = 1` (book).
- On Lean 4.33.0, `n == n` at `Nat` carries `Classical.choice` and
  `decide (n = n)` does not (book measurement).

## What has not been proved

- That `k^(2d + 1)` is tight: no lower bound on distinguishable windows
  is proved, and the module says so. The exhaustive searches show the
  threshold is attained at five small `(k, d)` pairs, nothing more.
- Anything for a view that is not local: for an index-reading view
  (Unit 40's valued mark) the radius is inert and the theorem is silent.
- Anything about Genesis's own profile as a colouring: `colour` is
  arbitrary, and no theorem relates `profile1` to it.
- The repair-strategy consequence (what the bound says about strategies
  that colour and repair): Unit 43.
- Absolute interior, "no outside", identity-grade observation: outside
  the statement language, by the ledger's own list.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `List.Nodup`, `List.filter`, `List.map` | counting | metatheory |
| `decide (x = B)` in place of `x == B` | the choice-free route | toolchain fact, measured |
| `upto` in place of `List.range` | the index list | metatheory, defined to avoid a choice-dependent lemma |
| `Nat` exponentiation, `encode` | the capacity `k^(2d + 1)` | metatheory |
| `colour : Nat → Nat`, `v : Nat → Nat` | the observer | arbitrary functions in the metatheory; `ViewLocal` is the only constraint |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** Nothing new: the Pigeonhole module declares
itself apparatus, and the capacity bound is a theorem about functions on
indices. Its force for Genesis is through Unit 41's chain: any observer
who colours it with finitely many colours and reads a bounded window is
outrun, and the length at which that happens is computed from the
observer's own declaration.

**Phrases to read with care.**

- "The deep interior of `reflState n` holds two points that `v` does not
  separate": true as applied; the theorem's statement has no `reflState`.
- "`B` is derived, not assumed": `B = k^(2d + 1)` follows from
  `ViewLocal`; without locality the radius plays no role and the result
  is ordinary pigeonhole.
- "Choice-free": a property of the enumerated axiom reports on this
  toolchain, which the book check re-measures.

## Student exercise

With three colours and radius 0, how many deep points does the chain
need before two must share a view, and what is the threshold `n`? Give a
colouring of `0..4` whose radius-0 view separates all deep points of the
chain of length 4, and say why no colouring of `0..5` does so at
length 5.

## Answer

At radius 0 the window is the point itself, so there are `3^1 = 3`
possible views; four deep points force a collision. The deep interior at
radius 0 is `1..n − 1`, with `n − 1` points, so four deep points first
occur at `n = 5`, which is the threshold `3^1 + 0 + 2 = 5`. At length 4
the deep points are `1, 2, 3`; colour them `0, 1, 2` (the check found
`[0, 0, 1, 2, 0]`, the colours of `0` and `4` being irrelevant), and the
three views are distinct. At length 5 the deep points `1, 2, 3, 4` take
only three colours, so by `pigeonhole 3` two of them are coloured alike
and, the view being local at radius 0 (it reads the one colour), equal.
The check's row `3, 0: 5; [1, 2, 3, 4] (4 points, 3 possible balls); True`
confirms every one of the `3^6` colourings collides.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Pigeonhole.lean` lines 51-106 (list lemmas), 113-166 (counting), 173-205 (`upto`, injective maps), 215-230 (pigeonhole); `lean4/Derivation/CapacityBound.lean` lines 59-126 (`encode`), 131-161 (windows, locality, blindness), 178-200 (the bound), 212-252 (fixtures) |
| Axiom report | `artifacts/lean_axioms.txt` lines 1246-1261: all within `{propext, Quot.sound}`; `upto_length`, `local_view_blind` none; `nodup_filter_eq_le_one`, `filter_nodup`, `colourBall_length` `propext` |
| Paper | `paper/paper_claim_ledger.md` `CL-CAP-BOUND` (statement, why it is a capacity statement, the exact non-claims, falsifier); `paper/paper_change_log.md` entries on the `ReflBEq Nat` measurement and the `decide`-filter technique; `contact/analysis/separation_capacity_open.md` (the residual document the modules close; its "general `n` OPEN" wording predates Unit 41's correspondence) |
| Python | none in Genesis; `code/derivation/g1_class_receipt.py` binds the axiom reports |
| Check (Python, book) | `python textbook/checks/u42_capacity_bound.py`: counting and pigeonhole instances; `encode` bounded and injective; exhaustive collision at the threshold for five `(k, d)`; separating colourings one below; Genesis's parity fixture |
| Check (book Lean) | `python textbook/checks/u42_lean.py`: fourteen book declarations (the two toolchain measurements included) plus seven Genesis theorems kernel-checked, Lean 4.33.0 |
