# Unit 41. Looking farther does not help: the radius-`d` outrun

**Claim.** Unit 40 showed depth-2 observation of the chain repaired one
pair and was defeated two steps deeper, at two lengths. This module
proves the pattern for every radius. `profileD n i d` is the list of
Unit 40's depth-1 profiles along the window `[i − d, …, i + d]`. Every
point deep enough in the interior (`d < i` and `i + d < n`) has the
constant list of interior profiles (`profileD_deep`), so any two deep
points look alike at radius `d` (`depth_d_outrun`, with no bound on `n`),
and from length `2d + 3` on there are two distinct deep points
(`depth_d_obstruction`). A second group of theorems ties this profile to
Unit 40's: on interior points Genesis's depth-2 record is exactly the
three neighbouring depth-1 profiles (`profile2_interior`), so depth-2
equality and radius-one equality are the same relation on every interior
pair of every chain (`radius_one_agrees_with_sealed_depth2`), and the two
instances of Unit 40 are carried across it. **Status:** derived
(horizon-free in `n` for the outrun; general `n` for the correspondence).
Not in this module: coloured observation, the repair-strategy
consequence, and any statement off the interior. **Lean:**
`lean4/Derivation/SeparationCapacity.lean` lines 42-79 (list lemmas),
84-132 (ball, profile, outrun), 143-236 (correspondence). **Axioms:**
`{propext, Quot.sound}`; `ball_length` `propext`. **Depends on:**
`profile1`, `profile2`, `middle_profile`, `depth2_separates_near_ends_n4`,
`depth2_obstruction_n5` (Unit 40); `reflective_chain_successor_relation`
(Unit 39); `List.range`, `List.map`, `List.filter`.

## Question

Unit 40 left two decided instances and an open conjecture, G2: for every
fixed radius of structural observation, is the chain's deep interior
eventually uniform? And a smaller question underneath it: Genesis's
`profile2` and this module's radius-one profile are written differently.
Are they the same observation?

## What we already possess

- The chain and its three profile classes; `middle_profile` says every
  interior point has profile `(true, true, true)` (Unit 40).
- `profile2`, and the two instances at lengths 4 and 5 (Unit 40).
- The successor relation of the chain as `List.range n` mapped through
  `k ↦ (k, k + 1)` (Unit 39).

## New concept: a ball, a structural profile at radius `d`, and "deep"

The *ball* of radius `d` around `i` is the index list
`[i − d, …, i + d]`, of length `2d + 1`, written as `List.range (2d + 1)`
mapped through `k ↦ i − d + k`. The subtraction is `Nat` subtraction,
which stops at `0`: for `i < d` the window is shifted to start at `0`,
not clipped short. `profileD n i d` maps Genesis's `profile1 (reflState n)`
over that ball: it is the depth-1 view of each point in the window, in
order. The *radius convention*: Genesis's "depth 2" sees `i` and its two
neighbours, which is radius **one** here; "depth `k`" is radius `k − 1`.

A point `i` is *deep* at radius `d` in the chain of length `n` when
`d < i` and `i + d < n`: its whole ball lies strictly inside the
interior, so no window point is the seed or the tip. The threshold
`2d + 3` is the least `n` with two deep points, `d + 1` and `d + 2`.

## Plain-language interpretation

Let the observer with the three-word vocabulary also look `d` steps to
the left and `d` steps to the right. Near the ends that helps: an
element two from the left end sees the seed's unusual description in its
window, and an element two from the right end sees the tip's. But an
element farther than `d` from either end sees only "badge, one in, one
out" in every window position, and so does every other such element.
Once the chain is long enough to hold two of them, which happens at
length `2d + 3`, the observer is defeated again. Looking farther moves
the problem farther in; it does not remove it.

The second half is bookkeeping, but bookkeeping the audit insisted on:
the earlier unit's "depth 2" and this unit's "radius 1" are shown to be
one observation on the interior, for every length, so the earlier
instances are instances of this theorem and not of a lookalike.

## Pseudocode

```
ball i d     := [i - d, ..., i + d]               -- Nat subtraction; shifted at the left end
profileD n i d := map (profile1 (reflState n)) (ball i d)
deep n i d   := d < i ∧ i + d < n

profileD_deep:   deep n i d  ⟹  profileD n i d = [(T,T,T), ... 2d+1 times]
depth_d_outrun:  deep n i d ∧ deep n j d  ⟹  profileD n i d = profileD n j d
depth_d_obstruction: n ≥ 2d + 3  ⟹  i := d+1, j := d+2 are deep, distinct, and collide

profile2_interior: 0 < i < n ⟹ profile2 (reflState n) i
                                 = (profile1 i, [profile1 (i-1)], [profile1 (i+1)])
profileD_radius_one: 0 < i ⟹ profileD n i 1 = [profile1 (i-1), profile1 i, profile1 (i+1)]
correspondence: interior i, j ⟹ (profile2 i = profile2 j ↔ profileD n i 1 = profileD n j 1)
```

## Python

Genesis has no Python module for this file. The check rebuilds `ball`
and `profileD` from Genesis's `generator.profile1` (Python (book)) and
compares with Genesis's `generator.profile2`.

```python
from derivation.generator import profile1, profile2

def ball(i, d): return [max(i - d, 0) + k for k in range(2 * d + 1)]
def profile_d(n, i, d): return [profile1(n, k) for k in ball(i, d)]
def deep(n, i, d): return d < i and i + d < n

print(ball(2, 1), ball(0, 1))
print(profile_d(7, 3, 2) == profile_d(7, 4, 2), [i for i in range(8) if deep(7, i, 2)])
print(all((profile2(n, i) == profile2(n, j)) == (profile_d(n, i, 1) == profile_d(n, j, 1))
          for n in range(2, 16) for i in range(1, n) for j in range(1, n)))
```

Output:

```text
[1, 2, 3] [0, 1, 2]
True [3, 4]
True
```

The check script's run:

```text
ball 2 1 = [1, 2, 3]; ball 0 1 = [0, 1, 2] (shifted: truncated subtraction starts the window at 0)
every deep point's radius-d profile is the constant interior list (n <= 15, d <= 4): True
radius d: least n with a colliding deep pair; 2d+3; deep points at that n
  0: 3; 3; [1, 2]
  1: 5; 5; [2, 3]
  2: 7; 7; [3, 4]
  3: 9; 9; [4, 5]
  4: 11; 11; [5, 6]
depth-2 equality == radius-one equality on every interior pair (n <= 15): True
  n = 4: profileD 4 1 1 = [(False, False, True), (True, True, True), (True, True, True)], profileD 4 3 1 = [(True, True, True), (True, True, True), (True, True, False)]; deep points at radius 1: [2]
  n = 5: profileD 5 2 1 == profileD 5 3 1: True
  off the interior (n = 5): profileD 0 == profileD 1: True; profile2 0 == profile2 1: False; profile2 of the seed: ((False, False, True), (), ((True, True, True),))
failures: []
```

## Line-by-line Python explanation

`ball(i, d)` uses `max(i - d, 0)` for Lean's truncated subtraction;
`profile_d` maps Genesis's `profile1` over it; `deep` is the two
inequalities. The first block checks, for every length to 15 and radius
to 4, that every deep point's list is the constant interior list: that
is `profileD_deep` on a finite prefix. The second block searches, per
radius, for the least length with two deep points that collide, and finds
`2d + 3` with the deep points `[d + 1, d + 2]`: `depth_d_obstruction`'s
witness, and, on this prefix, the fact that there is no earlier colliding
*deep* pair because there is no earlier deep pair at all. The third block
checks the correspondence on every interior pair to length 15, then
prints the two Unit 40 instances in radius-one form: at length 4 the
window of element 1 begins with the seed's profile and the window of
element 3 ends with the tip's, so they differ, while element 2 is the
only deep point; at length 5 elements 2 and 3 both carry the constant
list.

The last line is the audit's third note made concrete. Off the interior
nothing is claimed, and nothing holds: the shifted window of the seed is
`[0, 1, 2]`, the same window as element 1's, so `profileD 5 0 1` equals
`profileD 5 1 1`; but `profile2` of the seed has an empty in-list while
element 1's does not. The hypothesis `0 < i` in the correspondence is
doing work.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/SeparationCapacity.lean lines 84-132
def ball (i d : Nat) : List Nat :=
  (List.range (2 * d + 1)).map (fun k => i - d + k)

theorem ball_length (i d : Nat) : (ball i d).length = 2 * d + 1 := by
  simp [ball]

def profileD (n i d : Nat) : List (Bool × Bool × Bool) :=
  (ball i d).map (profile1 (reflState n))

theorem profileD_deep (n i d : Nat) (hlo : d < i) (hhi : i + d < n) :
    profileD n i d
      = (List.range (2 * d + 1)).map (fun _ => (true, true, true)) := by
  unfold profileD ball
  rw [List.map_map]
  apply List.map_congr_left
  intro k hk
  have hkr := List.mem_range.mp hk
  show profile1 (reflState n) (i - d + k) = (true, true, true)
  apply middle_profile
  · omega
  · omega

theorem depth_d_outrun (n i j d : Nat)
    (hi0 : d < i) (hi1 : i + d < n) (hj0 : d < j) (hj1 : j + d < n) :
    profileD n i d = profileD n j d := by
  rw [profileD_deep n i d hi0 hi1, profileD_deep n j d hj0 hj1]

theorem depth_d_obstruction (d n : Nat) (hn : 2 * d + 3 ≤ n) :
    ∃ i j, i ≠ j ∧ d < i ∧ i + d < n ∧ d < j ∧ j + d < n ∧
      profileD n i d = profileD n j d :=
  ⟨d + 1, d + 2, by omega, by omega, by omega, by omega, by omega,
   depth_d_outrun n (d + 1) (d + 2) d (by omega) (by omega)
     (by omega) (by omega)⟩
```

```lean
-- Lean (Genesis), lean4/Derivation/SeparationCapacity.lean lines 143-192, 201-211
theorem incoming_edges_interior (n i : Nat) (hpos : 0 < i) (hle : i ≤ n) :
    (reflState n).rel.filter (fun p => decide (p.2 = i)) = [(i - 1, i)] := by
  rw [reflective_chain_successor_relation, List.filter_map]
  change List.map (fun k => (k, k + 1))
    ((List.range n).filter (fun k => decide (k + 1 = i))) = [(i - 1, i)]
  rw [filter_range_succ_eq n i hpos hle]
  simp [Nat.sub_add_cancel hpos]

theorem outgoing_edges_interior (n i : Nat) (hlt : i < n) :
    (reflState n).rel.filter (fun p => decide (p.1 = i)) = [(i, i + 1)] := by
  ...

theorem profile2_interior (n i : Nat) (hpos : 0 < i) (hlt : i < n) :
    profile2 (reflState n) i =
      (profile1 (reflState n) i,
       [profile1 (reflState n) (i - 1)],
       [profile1 (reflState n) (i + 1)]) := by
  unfold profile2
  rw [incoming_edges_interior n i hpos (by omega),
      outgoing_edges_interior n i hlt]
  rfl

theorem profileD_radius_one (n i : Nat) (hpos : 0 < i) :
    profileD n i 1 =
      [profile1 (reflState n) (i - 1),
       profile1 (reflState n) i,
       profile1 (reflState n) (i + 1)] := by
  have hcenter : i - 1 + 1 = i := Nat.sub_add_cancel (by omega)
  have hright : i - 1 + 2 = i + 1 := by omega
  simp [profileD, ball, List.range_succ, hcenter, hright]

theorem radius_one_agrees_with_sealed_depth2 (n i j : Nat)
    (hi0 : 0 < i) (hi1 : i < n) (hj0 : 0 < j) (hj1 : j < n) :
    (profile2 (reflState n) i = profile2 (reflState n) j ↔
      profileD n i 1 = profileD n j 1) := by
  rw [profile2_interior n i hi0 hi1, profile2_interior n j hj0 hj1,
      profileD_radius_one n i hi0, profileD_radius_one n j hj0]
  simp only [Prod.mk.injEq, List.cons.injEq, and_true]
  constructor
  · rintro ⟨hcenter, hleft, hright⟩
    exact ⟨hleft, hcenter, hright⟩
  · rintro ⟨hleft, hcenter, hright⟩
    exact ⟨hcenter, hleft, hright⟩

theorem radius_one_agrees_with_sealed_depth2_n5 :
    (∀ i ∈ [1, 2, 3, 4], ∀ j ∈ [1, 2, 3, 4],
        (profile2 (reflState 5) i = profile2 (reflState 5) j ↔
          profileD 5 i 1 = profileD 5 j 1))
      ∧ profileD 5 2 1 = profileD 5 3 1 ∧ (2 : Nat) ≠ 3 :=
  have corr : ∀ i ∈ [1, 2, 3, 4], ∀ j ∈ [1, 2, 3, 4],
      (profile2 (reflState 5) i = profile2 (reflState 5) j ↔
        profileD 5 i 1 = profileD 5 j 1) := by decide
  ⟨corr,
   (corr 2 (by decide) 3 (by decide)).mp depth2_obstruction_n5.1,
   depth2_obstruction_n5.2⟩
```

The book's Lean evaluates the ball and the profile at small values,
applies the outrun at radius 2 and at every radius's threshold, shows
there is no deep pair below the threshold, instantiates the
correspondence at length 10, reads the two carried instances off the
Genesis theorems, and shows the correspondence fail at the seed.

```lean
-- Lean (book), textbook/checks/u41_lean.py
theorem ball_values : ball 2 1 = [1, 2, 3] ∧ ball 0 1 = [0, 1, 2] ∧ ball 5 2 = [3, 4, 5, 6, 7] := by
  decide

theorem profileD_values :
    profileD 4 1 1 = [(false, false, true), (true, true, true), (true, true, true)] ∧
    profileD 4 3 1 = [(true, true, true), (true, true, true), (true, true, false)] ∧
    profileD 5 2 1 = [(true, true, true), (true, true, true), (true, true, true)] := by
  decide

theorem deep_profile_nine : profileD 9 4 3 = (List.range 7).map (fun _ => (true, true, true)) :=
  profileD_deep 9 4 3 (by omega) (by omega)

theorem outrun_radius_two : profileD 7 3 2 = profileD 7 4 2 :=
  depth_d_outrun 7 3 4 2 (by omega) (by omega) (by omega) (by omega)

theorem threshold_every_radius (d : Nat) :
    profileD (2 * d + 3) (d + 1) d = profileD (2 * d + 3) (d + 2) d :=
  depth_d_outrun _ _ _ _ (by omega) (by omega) (by omega) (by omega)

theorem no_deep_pair_at_four :
    ¬ ∃ i j : Nat, i ≠ j ∧ 1 < i ∧ i + 1 < 4 ∧ 1 < j ∧ j + 1 < 4 := by
  rintro ⟨i, j, hne, hi0, hi1, hj0, hj1⟩
  omega

theorem depth2_is_three_profiles :
    profile2 (reflState 5) 2 =
      (profile1 (reflState 5) 2, [profile1 (reflState 5) 1], [profile1 (reflState 5) 3]) :=
  profile2_interior 5 2 (by omega) (by omega)

theorem correspondence_at_ten :
    profile2 (reflState 10) 4 = profile2 (reflState 10) 6 ↔ profileD 10 4 1 = profileD 10 6 1 :=
  radius_one_agrees_with_sealed_depth2 10 4 6 (by omega) (by omega) (by omega) (by omega)

theorem carried_instances : profileD 5 2 1 = profileD 5 3 1 ∧ profileD 4 1 1 ≠ profileD 4 3 1 :=
  ⟨radius_one_agrees_with_sealed_depth2_n5.2.1, radius_one_agrees_with_sealed_depth2_n4.2.1⟩

theorem seed_breaks_correspondence :
    profileD 5 0 1 = profileD 5 1 1 ∧ profile2 (reflState 5) 0 ≠ profile2 (reflState 5) 1 ∧
    profile2 (reflState 5) 0 = ((false, false, true), [], [(true, true, true)]) := by
  decide
```

## Line-by-line Lean explanation

**`ball`, `ball_length`, `profileD` (lines 84-94).** `ball i d` maps
`k ↦ i − d + k` over `List.range (2d + 1)`; its length is the range's,
by `simp`. `profileD` maps `profile1 (reflState n)` over the ball. The
module header insists this is Genesis's own `profile1` on Genesis's own
chain, "not a private mirror": every theorem below is about the sealed
chain. The book's `ball_values` shows the window at `2`, the shifted
window at `0`, and a radius-2 window.

**`profileD_deep` (lines 99-110).** Unfold both definitions and merge
the two maps (`List.map_map`). `List.map_congr_left` reduces the
equality of two mapped lists to equality of the functions on members of
`List.range (2d + 1)`. For a member `k < 2d + 1`, the window point
`i − d + k` is interior: from `d < i` the subtraction is honest, so the
point is at least `i − d ≥ 1`, and from `i + d < n` it is at most
`i + d < n`. `middle_profile` closes each with two `omega` calls. The
book's `deep_profile_nine` is the case `n = 9, i = 4, d = 3`, a window of
seven.

**`depth_d_outrun` (lines 119-122).** Both deep profiles are the same
constant list; rewrite both. There is no hypothesis on `n` beyond
deepness of the two points, which is what "horizon-free" means here.
Scope, from the docstring: this is the structural profile; a regime that
also colours the carrier is not covered. Unit 42 takes up colours.

**`depth_d_obstruction` (lines 127-132).** Given `2d + 3 ≤ n`, take
`i = d + 1`, `j = d + 2`. Five `omega` goals: distinct, and both deep
(`d < d + 1`; `d + 1 + d < n` from the hypothesis; likewise for `d + 2`).
Then the outrun. The docstring says the threshold "is exactly the least
`n` at which the deep interior holds two distinct points"; the audit
notes this is a remark about the count of deep points, not a proved
minimality of collision length (no theorem here says that below `2d + 3`
no *non-deep* pair collides; at radius 0, which is Unit 40's depth 1,
the threshold 3 is sharp by Unit 40's exactness theorem). The book's
`no_deep_pair_at_four` gives the arithmetic at radius 1: the deep points
of length 4 are the single point 2, so the separated pair `(1, 3)` is not
a counterexample to the outrun.

**The list lemmas (lines 42-79).** `filter_range_decide_eq`: filtering
`List.range n` for `k = i` leaves `[i]` if `i < n`, else `[]`, by
induction on `n` with `List.range_succ` and a trichotomy on `i` against
`n`. `filter_range_succ_eq` rewrites the predicate `k + 1 = i` to
`k = i − 1` (function extensionality on a decidable predicate, with
`Nat.sub_add_cancel` to restore `i`) and applies the first lemma. These
are the constructive `decide` filters the change log mentions: an
earlier proof shape used a generic equality filter whose use-site axiom
report fell outside `{propext, Quot.sound}` and was withdrawn.

**`incoming_edges_interior`, `outgoing_edges_interior` (lines 143-157).**
The chain's relation is `List.range n` mapped through `k ↦ (k, k + 1)`
(Unit 39). `List.filter_map` moves the filter inside the map; the
in-edges of `i` are the `k` with `k + 1 = i`, hence `[(i − 1, i)]` for
`0 < i ≤ n`; the out-edges the `k = i`, hence `[(i, i + 1)]` for `i < n`.

**`profile2_interior`, `profileD_radius_one` (lines 159-176).** Unfold
`profile2`, rewrite the two filters, and the two neighbour lists are
singletons: the depth-2 record of an interior point is the triple
(centre, `[left]`, `[right]`). The radius-one list is
`[left, centre, right]`, after `simp` unfolds the three-element range and
`i − 1 + 1 = i`, `i − 1 + 2 = i + 1` put the indices in order. The book's
`depth2_is_three_profiles` is the first at `n = 5, i = 2`.

**`radius_one_agrees_with_sealed_depth2` (lines 181-192).** Rewrite all
four records by the two lemmas. `Prod.mk.injEq` and `List.cons.injEq`
split each equality into three component equalities, in the orders
(centre, left, right) and (left, centre, right); the two directions
permute the conjuncts. This is the general-`n` statement the paper's T5
section calls closed and whose earlier "only lengths 4 and 5" sentences
it withdraws. The book's `correspondence_at_ten` instantiates it.

**The two carried instances (lines 201-236).** Each first decides the
equivalence over the interior indices of one concrete chain (`corr`),
then applies the *Genesis* theorem of Unit 40 through it: at length 5,
`depth2_obstruction_n5.1` gives the depth-2 collision of `(2, 3)`, and
`corr` turns it into the radius-one collision; at length 4,
`depth2_separates_near_ends_n4` refutes the radius-one equality of
`(1, 3)` by the converse direction. The third conjunct at length 4 is
the arithmetic that only `i = 2` is deep. The change log records why
these replaced two earlier theorems: the earlier `sealed_depth2_is_radius_one`
never mentioned `profile2` and re-instantiated this module's own
obstruction theorem, and `deep_interior_singleton_at_four` was pure
arithmetic under a geometric name. The replacements' statements mention
both profiles and their proofs consume the sealed instances. The book's
`carried_instances` reads the two conjuncts off.

**Off the interior (book, `seed_breaks_correspondence`).** With `i = 0`
the shifted window `[0, 1, 2]` coincides with element 1's, so
`profileD 5 0 1 = profileD 5 1 1`; `profile2` of the seed has an empty
in-list and differs from element 1's. The hypotheses `0 < i`, `0 < j` of
the correspondence are therefore necessary, not decorative, and the
audit's warning against reading `profileD n 0 d` on its own is exact.

## What has been proved

- Every deep point's radius-`d` profile is the constant interior list;
  any two deep points share it; from length `2d + 3` two distinct deep
  points exist (Genesis, for every `n`, `d`).
- On interior points Genesis's depth-2 record is the three neighbouring
  depth-1 profiles, and depth-2 equality coincides with radius-one
  equality on every interior pair of every chain (Genesis).
- The two Unit 40 instances, transported to radius one by the Genesis
  theorems themselves (Genesis).
- Below the threshold there is no deep pair at radius 1 and length 4
  (Genesis conjunct, book restatement); the correspondence fails at the
  seed (book).

## What has not been proved

- Anything about *coloured* observation: a regime that also reads marks
  on the carrier. The capacity bound for that is Unit 42
  (`Pigeonhole`, `CapacityBound`), and the repair-strategy consequence
  Unit 43 (`LocalStrategy`, `G1Class`).
- That `2d + 3` is the least length at which *any* two points collide at
  radius `d`; only that it is the least length with two deep points,
  and that deep points collide.
- Anything off the interior: the correspondence has `0 < i < n` as
  hypotheses, and the book shows it false without them.
- Anything about "absolute interior" or "no outside" (the header's own
  list of what lies outside its statement language).

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `Nat` subtraction in `ball` | the window | metatheory; truncation guarded by `d < i` in every theorem |
| `List.range`, `List.map`, `List.filter`, `List.map_congr_left` | profiles, edge lists | metatheory |
| the radius convention ("depth `k`" is radius `k − 1`) | reading Unit 40's instances | declared; made a theorem by the correspondence |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** The chain and the per-point three-word
description, as in Unit 40; a window of them, now. Nothing new is
admitted: the radius is a parameter of the observer, and the theorem
says the observer with any fixed radius is outrun.

**Phrases to read with care.**

- "Horizon-free" here means no bound on `n` in the outrun; the obstruction
  form does carry a threshold, derived.
- "The least `n`" in the obstruction docstring is about the number of
  deep points, not about collision length in general.
- "Recovered" and "reconciled" for the radius convention were withdrawn
  from the module docstring; what stands is the typed correspondence.
- The paper's conjecture list (G2) still contains a sentence saying the
  general-`n` correspondence is OPEN and only `n = 4, 5` are transported,
  while its later T5 section proves the general statement and withdraws
  that sentence. The ledger entry `CL-G1-T5-GENERAL` is the one to
  trust; the stale G2 sentence is a documentation inconsistency, not a
  defect in any theorem (recorded in the audit note added with this
  unit).

## Student exercise

At radius 2, write `ball 1 2` and `profileD 6 1 2`, and say why
`depth_d_outrun` does not apply to the pair `(1, 4)` at length 6 even
though both points are interior. Then give the least length at which
radius 2 is outrun, with the colliding pair.

## Answer

`ball 1 2` is `[1 − 2 + k]` for `k = 0, …, 4` with truncated
subtraction, so `[0, 1, 2, 3, 4]`: the window is shifted to begin at the
seed. Hence `profileD 6 1 2 = [(F, F, T), (T, T, T), (T, T, T), (T, T, T), (T, T, T)]`,
which begins with the seed's profile. The point `1` is not deep at
radius 2 (`2 < 1` fails), so `depth_d_outrun` has nothing to say about
`(1, 4)`; indeed `profileD 6 4 2` ends with the tip's profile
`(T, T, F)`, so the two differ. The least length with two deep points at
radius 2 is `2·2 + 3 = 7`, with the pair `(3, 4)`, both of whose windows
`[1, …, 5]` and `[2, …, 6]` lie in the interior of `[0, …, 7]`; the check
reports `2: 7; 7; [3, 4]` and the book's `outrun_radius_two` proves the
collision.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/SeparationCapacity.lean` lines 42-79 (list lemmas), 84-94 (ball, profile), 99-132 (deep, outrun, obstruction), 143-176 (edge lists, two shapes), 181-192 (correspondence), 201-236 (carried instances) |
| Axiom report | `artifacts/lean_axioms.txt` lines 1203-1216: `ball_length` `propext`; the other thirteen `propext, Quot.sound` |
| Paper | `paper/endogenous_generator.md` TERMINAL (last paragraph), frontier conjecture G2 (structural half closed; stale OPEN sentence noted above), section "T5, G3, and G4" (T5 proved at general length; withdrawals); `paper/paper_change_log.md` items on `SeparationCapacity` (the radius convention; the two replaced theorems; the withdrawn proof shape); ledger `CL-G1-T5-GENERAL` |
| Python | none in Genesis for this module; `code/derivation/g1_class_receipt.py` binds the eight axiom reports; `artifacts/g1_class_receipt.json` |
| Check (Python, book) | `python textbook/checks/u41_separation_capacity.py`: `ball` and `profileD` rebuilt from `generator.profile1`; deep uniformity to length 15 and radius 4; thresholds `2d + 3` with their deep points; the correspondence on every interior pair to length 15; the two instances; the seed |
| Check (book Lean) | `python textbook/checks/u41_lean.py`: eleven book theorems plus seven Genesis theorems kernel-checked, Lean 4.33.0 |
