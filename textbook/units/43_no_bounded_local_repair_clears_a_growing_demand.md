# Unit 43. Fixed colour bounds and local windows cannot clear every chain stage

**Claim.** A strategy with one fixed radius and one finite colour bound
cannot separate every inherited obstructed pair at every chain stage.
This excludes the stated family of views. It does not prove failure of
every repair procedure or describe how repairs change a running state.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** `LocalStrategy` declares a class of repairs for Unit 40's
standing demand: a strategy has a radius `d`, a colouring of the chain at
each length, a view at each length, and a proof that the view reads only
the radius-`d` colour window (Unit 42's `ViewLocal`). `FiniteDeclaration k
S` adds one alphabet bound `k` for every length and index. Three
predicates are kept apart: `Fires` (the chain carries a depth-1
obstruction from length 3 on; it does not mention the strategy),
`Clears` (the view separates every obstructed pair at every length) and
`IdentityGrade` (the view separates every distinct pair). The theorem:
for a finite member, Unit 42's capacity bound gives two deep points with
equal views, and deep points share the depth-1 profile, so no finite
local member clears (`finite_local_not_clears`); hence
`g1_local_finite_alphabet_class`, renamed `G1Class.g1_class_exclusion`:
`Fires S ∧ ¬ Clears S ∧ ¬ (Fires S ∧ Clears S ∧ ¬ RecurringImport S)`.
Five members are classified: bare, presence (which *is* bare), depth-two
(finite; clears length 4, not all lengths), per-pair fresh marking and
valued marking (both identity-grade and clearing, both outside
`FiniteDeclaration`, differing only in a declared tag). `G1Class` also
records that `Clears` does not imply `¬ Fires` (the valued member has
both), so conjecture G3 needs a state-transition hypothesis the class
lacks.

**Status:** derived, conditional on `FiniteDeclaration k S`;
class-relative only. The paper's words "the member fires" and "the
fire/clear/no-import cycle is impossible" overread the Lean, whose
content is `¬ Clears S`; see "What has been proved". **Lean:**
`lean4/Derivation/LocalStrategy.lean` lines 21-260;
`lean4/Derivation/G1Class.lean` lines 22-43. **Axioms:**
`{propext, Quot.sound}` throughout; `profileCode_lt_eight` none.
**Depends on:** `capacity_bound`, `ViewLocal`, `encode` (Unit 42);
`generation_never_dries`, `middle_profile`,
`depth1_obstructions_are_exactly_middle_pairs`, `profile1` (Unit 40).

</details>

## First pass

Use two colours, alternating by position, and read just the centre's
colour. In the base three-bit observation, all interior positions agree.
Try the new colour view as a proposed repair:

| Chain stage | Interior positions | New colour answers | All separated? |
|---|---|---|---|
| 3 | 1, 2 | 1, 0 | Yes |
| 4 | 1, 2, 3 | 1, 0, 1 | No: 1 and 3 agree |

A success at one stage has not established success at every stage.
The theorem generalizes this counting argument to every colouring with
the stated fixed palette and window radius, even when the colouring and
reporting functions change between stages.

The formal class stores families of proposed views, not a process that
applies repairs to a changing state. Its `Fires` predicate describes
unrepaired base-chain profiles and ignores which strategy was supplied.

**Predict:** if a strategy has the label `recurring`, has the theorem
measured repeated resource use?

<details>
<summary>Check your prediction</summary>

No. That field is a declared label. The mathematical exclusion follows
from the finite colour bound and locality; it does not measure a runtime
or infer costs from the label.

</details>

## Question

Unit 40 left a demand that never stops and five repair strategies tried
for 15 rounds. Unit 42 bounded what any local, finitely coloured view can
distinguish. Put the two together: is there any repair, inside a class we
can state exactly, that separates every obstructed pair at every chain
length with a fixed radius and a fixed alphabet? If not, what exactly is
excluded, what escapes, and does the exclusion say anything about
whether repairing stops the demand (conjecture G3)?

## What we already possess

- The chain `reflState n`, its depth-1 profile `profile1`, and the fact
  that the middle elements `1..n−1` share one profile (Unit 40,
  `middle_profile`); the depth-1 obstructions are exactly the middle pairs
  (`depth1_obstructions_are_exactly_middle_pairs`); the demand fires from
  length 3 on (`generation_never_dries`).
- Colour windows, local views and the capacity bound at threshold
  `k^(2d + 1) + 2d + 2` (Unit 42).
- The five strategies and their 15-round fates (Unit 40, `artifacts/generator.json`).

## New concept: a declared strategy class and three separate predicates

A `LocalStrategy d` is four things: a tag `importDiscipline ∈ {oneTime,
recurring}`, a colour family `colour : Nat → Nat → Nat` (length, index),
a view family `view : Nat → Nat → Nat`, and a proof `locality : ∀ n,
ViewLocal (view n) (colour n) d`. Nothing else: no state, no rounds, no
transition. `FiniteDeclaration k S` is `∀ n x, S.colour n x < k`.

Here `n` counts chain steps/links, with `n+1` positions. The older output
uses “length” for that stage parameter. The colour and view families can
change with `n`; locality supplies a factor separately at each stage.
The colouring rule itself need not be local or cheap. The bound limits
the number of colours and the readout window, not the computation that
assigns colours or the magnitude of the numerical view values.

`BaseObstructed n i j`: two indices of the chain of length `n`,
distinct, with equal depth-1 profiles. `Fires S` is `∃ n0, ∀ n ≥ n0, ∃ i
j, BaseObstructed n i j`; the binder for `S` is written `_S` and the
body never uses it. `ClearsOn S n`: every base-obstructed pair at length
`n` gets distinct views. `Clears S`: at every `n`. `IdentityGrade S`:
every distinct pair of indices `≤ n` gets distinct views, at every `n`.
`RecurringImport S` reads the tag.

The exclusion is one application of Unit 42. A finite member has a
collision of deep views at the threshold; deep points of the chain are
middle points, so they are base-obstructed; so the member fails to clear
that length.

## Plain-language interpretation

Imagine every possible repair that works like this: colour the chain
with at most `k` colours, look at a window of fixed width, and announce
what you see. The class is everything of that shape, whatever the
colouring rule and whatever the announcing rule, as long as the width and
the number of colours are fixed before the chain grows. Unit 42 says a
long enough chain has two deep elements with the same window, and Unit
40 says deep elements already look the same before repair. So the repair
has not told them apart. That is the whole theorem.

What escapes: a view that reads the index itself (per-pair marking,
valued marking) is identity-grade and clears every length, but it is not
a finite declaration: its "colours" are the indices, unbounded. These
are members of `LocalStrategy`; they lie outside the subclass satisfying
one fixed `FiniteDeclaration k`. Thus locality alone is not what excludes
them, and the theorem does not refute their clearing behavior.

What the theorem does not do: it does not model repair *over time*.
`Fires` is a fact about the chain, true for every strategy, including the
ones that clear. So "clearing does not stop the firing" is not a
discovery about the valued rule; it is what the definitions say. A
theorem that related repairing to the demand ceasing (G3) would need a
state that changes when a repair is applied. The class has no such state,
and the paper says G3 remains a conjecture.

## Pseudocode

```
LocalStrategy d = (tag, colour : n ↦ (x ↦ Nat), view : n ↦ (x ↦ Nat), proof: view n reads colourBall (colour n) · d)
FiniteDeclaration k S = ∀ n x, colour n x < k
BaseObstructed n i j = i ≤ n ∧ j ≤ n ∧ i ≠ j ∧ profile1 (chain n) i = profile1 (chain n) j
Fires _          = ∃ n0, ∀ n ≥ n0, ∃ i j, BaseObstructed n i j        -- no strategy in the body
Clears S         = ∀ n i j, BaseObstructed n i j → view n i ≠ view n j
IdentityGrade S  = ∀ n i j ≤ n, i ≠ j → view n i ≠ view n j

finite_local_not_clears S k:
  n := k^(2d+1) + 2d + 2
  (i, j) := capacity_bound (colour n) (view n) k d n        -- deep, distinct, equal views
  profile1 (chain n) i = profile1 (chain n) j               -- both middle (middle_profile)
  so Clears S at n is contradicted
g1_class_exclusion S k = (Fires S, ¬ Clears S, ¬ (Fires S ∧ Clears S ∧ ¬ RecurringImport S))
  -- third conjunct from the second
clears_does_not_imply_not_fires = (valued, valued_clears, fires_every_strategy valued)
```

## Python

Genesis's mirror is `code/derivation/local_strategy.py`; its artifact is
`artifacts/local_strategy.json`. The class is a dataclass whose `view`
is *built* from a factor applied to the colour ball, so locality holds
by construction; the predicates are checked through a declared bound.

```python
from derivation.local_strategy import (BARE, DEPTH_TWO, VALUED, STRATEGIES,
    base_obstructions, capacity_collision, capacity_threshold, classification, clears_within)

print(base_obstructions(3))                                  # ((1, 2),)
print([classification(s, 15) for s in STRATEGIES])
print(capacity_threshold(BARE), capacity_collision(BARE))     # 10 (1, 2)
print(capacity_threshold(DEPTH_TWO), capacity_collision(DEPTH_TWO))   # 516 (2, 3)
print(capacity_threshold(VALUED))                            # None: no alphabet
print(clears_within(DEPTH_TWO, 4), clears_within(DEPTH_TWO, 5))       # True False
```

The check script's run:

```text
five members through chain length 15 (name: radius, alphabet, tag -> classification; artifact agrees):
  none: 0, 8, one_time -> fires_unrepaired; True
  per_pair_fresh_mark: 0, None, recurring -> repairs_by_recurring_imports; True
  automark_presence: 0, 8, one_time -> fires_unrepaired; True
  automark_valued: 0, None, one_time -> generation_dead; True
  depth2: 1, 8, one_time -> fires_unrepaired; True
Fires ignores the strategy: base obstructions at length 3 are ((1, 2),) ; fires_within(S, 3) for every S: [True, True, True, True, True]
per-pair and valued: same colour and view through 15: True; tags recurring / one_time; classifications repairs_by_recurring_imports / generation_dead
thresholds k^(2d+1)+2d+2: {'none': 10, 'per_pair_fresh_mark': None, 'automark_presence': 10, 'automark_valued': None, 'depth2': 516}
collisions at the threshold (deep pair with equal views): {'none': (1, 2), 'per_pair_fresh_mark': None, 'automark_presence': (1, 2), 'automark_valued': None, 'depth2': (2, 3)}
depth-two views at length 4: [508, 508, 511, 255, 31]; clears length 4: True
depth-two views at length 5: [508, 508, 511, 511, 255, 31]; base pairs ((1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)); clears through 5: False
bare views at length 3: [4, 7, 7, 3]; identity grade through 3: False; presence is bare: True
negative locality probe (constant colour, identity view, radius 0): factor table None; artifact: {'constant_colour_identity_view_accepted': False, 'reason': 'same radius-zero colour ball receives two view values'}
book member parity (2 colours, radius 0): threshold 4, collision (1, 3), clears length 3: True, clears through 4: False, classification fires_unrepaired
failures: []
```

## Line-by-line Python explanation

`base_obstructions(n)` lists the pairs `i < j ≤ n` with equal `profile1`:
at length 3 only `(1, 2)`. `fires_within(S, b)` ignores `S` (the module
writes `_ = strategy`) and asks whether any length up to `b` has an
obstruction; it is the bounded mirror of `Fires` and is true for every
strategy from `b = 3`. `clears_within(S, b)` checks every obstructed pair
at every length up to `b` for distinct views; `identity_grade_within`
checks every pair; `finite_declaration_within` checks the declared
alphabet on the carrier, and returns `False` when no alphabet is declared
(`alphabet_size is None`). `classification` reads these four with the
tag: recurring and clearing gives `repairs_by_recurring_imports`;
one-time and identity-grade gives `generation_dead`; firing and not
clearing gives `fires_unrepaired`. The five rows match the artifact.

`capacity_threshold(S)` is `k^(2d + 1) + 2d + 2` when an alphabet is
declared, else `None`; `capacity_collision(S)` walks the deep points at
that length and returns the first repeated view: `(1, 2)` for bare at
length 10, `(2, 3)` for depth-two at length 516. The collisions are
concrete instances of `strategy_capacity_collision`.

The depth-two lines show the non-vacuity witness and its limit: at
length 4 the three deep views 508, 511, 255 are distinct; at length 5
indices 2 and 3 both read 511 (the window `[7, 7, 7]` in base 8), and
`(2, 3)` is base-obstructed. The bare line shows why bare is not
identity-grade: indices 1 and 2 both read 7 at length 3.

The negative locality probe is the module's test that locality is doing
work: a constant colouring with the identity view has no factor table at
radius 0, because one colour window would need two view values. The
Python class cannot express such a view; the Lean class cannot either,
because `locality` is a proof obligation.

The parity member is the book's: two colours, radius 0, threshold 4; it
clears every length up to 3 and fails at 4 on `(1, 3)`. Python's
`clears_within(parity, 3)` quantifies over all lengths up to 3.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/LocalStrategy.lean lines 21-65, 72-119
inductive ImportDiscipline where
  | oneTime
  | recurring
  deriving DecidableEq

structure LocalStrategy (d : Nat) where
  importDiscipline : ImportDiscipline
  colour : Nat → Nat → Nat
  view : Nat → Nat → Nat
  locality : ∀ n, ViewLocal (view n) (colour n) d

def FiniteDeclaration {d : Nat} (k : Nat) (S : LocalStrategy d) : Prop :=
  ∀ n x, S.colour n x < k

def RecurringImport {d : Nat} (S : LocalStrategy d) : Prop :=
  S.importDiscipline = .recurring

structure BaseObstructed (n i j : Nat) : Prop where
  left_mem : i ≤ n
  right_mem : j ≤ n
  distinct : i ≠ j
  same_profile : profile1 (reflState n) i = profile1 (reflState n) j

def Fires {d : Nat} (_S : LocalStrategy d) : Prop :=
  ∃ n0, ∀ n, n0 ≤ n → ∃ i j, BaseObstructed n i j

def ClearsOn {d : Nat} (S : LocalStrategy d) (n : Nat) : Prop :=
  ∀ i j, BaseObstructed n i j → S.view n i ≠ S.view n j

def Clears {d : Nat} (S : LocalStrategy d) : Prop :=
  ∀ n, ClearsOn S n

def IdentityGrade {d : Nat} (S : LocalStrategy d) : Prop :=
  ∀ n i j, i ≤ n → j ≤ n → i ≠ j → S.view n i ≠ S.view n j

theorem fires_every_strategy {d : Nat} (S : LocalStrategy d) : Fires S := by
  refine ⟨3, ?_⟩
  intro n hn
  have hgenerated := generation_never_dries n hn
  exact ⟨1, 2, ⟨by omega, by omega, hgenerated.1, hgenerated.2⟩⟩

theorem identityGrade_implies_clears {d : Nat} {S : LocalStrategy d}
    (h : IdentityGrade S) : Clears S := by
  intro n i j hij
  exact h n i j hij.left_mem hij.right_mem hij.distinct

theorem strategy_capacity_collision {d : Nat} (S : LocalStrategy d) (k n : Nat)
    (hfinite : FiniteDeclaration k S)
    (hn : k ^ (2 * d + 1) + 2 * d + 2 ≤ n) :
    ∃ i j, i ≠ j ∧ d < i ∧ i + d < n ∧ d < j ∧ j + d < n ∧
      S.view n i = S.view n j :=
  capacity_bound (S.colour n) (S.view n) k d n (hfinite n) (S.locality n) hn

theorem finite_local_not_clears {d : Nat} (S : LocalStrategy d) (k : Nat)
    (hfinite : FiniteDeclaration k S) : ¬ Clears S := by
  intro hclears
  let n := k ^ (2 * d + 1) + 2 * d + 2
  obtain ⟨i, j, hij, hi0, hi1, hj0, hj1, hview⟩ :=
    strategy_capacity_collision S k n hfinite (by simp [n])
  have hprofile : profile1 (reflState n) i = profile1 (reflState n) j := by
    rw [middle_profile n i (by omega) (by omega),
        middle_profile n j (by omega) (by omega)]
  exact (hclears n i j ⟨by omega, by omega, hij, hprofile⟩) hview

theorem g1_local_finite_alphabet_class {d : Nat} (S : LocalStrategy d) (k : Nat)
    (hfinite : FiniteDeclaration k S) :
    Fires S ∧ ¬ Clears S ∧
      ¬ (Fires S ∧ Clears S ∧ ¬ RecurringImport S) := by
  have hfires := fires_every_strategy S
  have hnot := finite_local_not_clears S k hfinite
  exact ⟨hfires, hnot, fun hcycle => hnot hcycle.2.1⟩
```

```lean
-- Lean (Genesis), lean4/Derivation/LocalStrategy.lean lines 123-132, 147-175, 191-201, 220-225
def zeroRadiusStrategy (discipline : ImportDiscipline)
    (f : Nat → Nat → Nat) : LocalStrategy 0 where
  importDiscipline := discipline
  colour := f
  view := f
  locality := by
    intro n
    refine ⟨fun xs => xs.headD 0, ?_⟩
    intro i
    simp [colourBall, ball]

def bare : LocalStrategy 0 :=
  zeroRadiusStrategy .oneTime
    (fun n i => profileCode (profile1 (reflState n) i))

def presence : LocalStrategy 0 := bare

def depthTwo : LocalStrategy 1 where
  importDiscipline := .oneTime
  colour := fun n i => profileCode (profile1 (reflState n) i)
  view := fun n i =>
    encode 8 (colourBall (fun x => profileCode (profile1 (reflState n) x)) i 1)
  locality := by
    intro n
    exact ⟨encode 8, fun _ => rfl⟩

def perPairFreshMark : LocalStrategy 0 :=
  zeroRadiusStrategy .recurring (fun _ i => i)

def valued : LocalStrategy 0 :=
  zeroRadiusStrategy .oneTime (fun _ i => i)

theorem depthTwo_clears_n4 : ClearsOn depthTwo 4 := by
  intro i j hij
  rcases hij with ⟨hi, hj, hne, hprofile⟩
  have hinterior :=
    (depth1_obstructions_are_exactly_middle_pairs 4 i j
      (by omega) hi hj hne).mp hprofile
  have hiCases : i = 1 ∨ i = 2 ∨ i = 3 := by omega
  have hjCases : j = 1 ∨ j = 2 ∨ j = 3 := by omega
  rcases hiCases with (rfl | rfl | rfl) <;>
    rcases hjCases with (rfl | rfl | rfl) <;>
      first | contradiction | decide

theorem valued_not_finite (k : Nat) : ¬ FiniteDeclaration k valued := by
  intro h
  exact (Nat.lt_irrefl k) (h 0 k)

theorem valued_clears : Clears valued :=
  identityGrade_implies_clears valued_oneTimeIdentity.2
```

```lean
-- Lean (Genesis), lean4/Derivation/G1Class.lean lines 22-43
theorem local_strategy_cycle_impossible {d : Nat} (S : LocalStrategy d)
    (k : Nat) (hfinite : FiniteDeclaration k S) :
    ¬ (Fires S ∧ Clears S ∧ ¬ RecurringImport S) := by
  intro hcycle
  exact (finite_local_not_clears S k hfinite) hcycle.2.1

theorem g1_class_exclusion {d : Nat} (S : LocalStrategy d) (k : Nat)
    (hfinite : FiniteDeclaration k S) :
    Fires S ∧ ¬ Clears S ∧
      ¬ (Fires S ∧ Clears S ∧ ¬ RecurringImport S) :=
  g1_local_finite_alphabet_class S k hfinite

theorem clears_does_not_imply_not_fires :
    ∃ S : LocalStrategy 0, Clears S ∧ Fires S :=
  ⟨valued, valued_clears, fires_every_strategy valued⟩
```

The book's Lean makes the flagged facts into kernel-checked statements:
`Fires` is the same proposition for two strategies; per-pair and valued
are the same functions under different tags; the third conjunct follows
from the second; the G3 counterexample holds for any clearing member; the
bare and depth-two views have the values the Python printed; a two-colour
member built in the book is excluded at threshold 4 after clearing
length 3; and a member whose factor depends on the length is accepted by
the class.

```lean
-- Lean (book), textbook/checks/u43_lean.py
theorem fires_ignores_strategy : Fires bare = Fires valued := rfl

theorem base_obstructed_three : BaseObstructed 3 1 2 :=
  ⟨by omega, by omega, by omega, by decide⟩

theorem perPair_valued_same_functions :
    perPairFreshMark.colour = valued.colour ∧ perPairFreshMark.view = valued.view :=
  ⟨rfl, rfl⟩

theorem perPair_valued_tags_differ :
    perPairFreshMark.importDiscipline ≠ valued.importDiscipline := by
  decide

theorem cycle_from_not_clears {d : Nat} (S : LocalStrategy d) (h : ¬ Clears S) :
    ¬ (Fires S ∧ Clears S ∧ ¬ RecurringImport S) :=
  fun c => h c.2.1

theorem any_clearing_member_fires {d : Nat} (S : LocalStrategy d) (h : Clears S) :
    Clears S ∧ Fires S :=
  ⟨h, fires_every_strategy S⟩

theorem bare_views_three :
    bare.view 3 0 = 4 ∧ bare.view 3 1 = 7 ∧ bare.view 3 2 = 7 ∧ bare.view 3 3 = 3 := by
  decide

theorem depthTwo_views_four :
    depthTwo.view 4 1 = 508 ∧ depthTwo.view 4 2 = 511 ∧ depthTwo.view 4 3 = 255 := by
  decide

theorem depthTwo_fails_at_five : ¬ ClearsOn depthTwo 5 :=
  fun h => h 2 3 ⟨by omega, by omega, by omega, by decide⟩ (by decide)

def parity : LocalStrategy 0 := zeroRadiusStrategy .oneTime (fun _ i => i % 2)

theorem parity_finite : FiniteDeclaration 2 parity :=
  fun _ x => Nat.mod_lt x (by decide)

theorem parity_not_clears : ¬ Clears parity :=
  finite_local_not_clears parity 2 parity_finite

theorem parity_threshold : 2 ^ (2 * 0 + 1) + 2 * 0 + 2 = 4 := rfl

theorem parity_collision_four :
    ∃ i j, i ≠ j ∧ 0 < i ∧ i + 0 < 4 ∧ 0 < j ∧ j + 0 < 4 ∧ parity.view 4 i = parity.view 4 j :=
  strategy_capacity_collision parity 2 4 parity_finite (by decide)

theorem parity_fails_at_four : ¬ ClearsOn parity 4 :=
  fun h => h 1 3 ⟨by omega, by omega, by omega, by decide⟩ (by decide)

theorem parity_clears_three : ClearsOn parity 3 := by
  intro i j hij
  rcases hij with ⟨hi, hj, hne, hprofile⟩
  have hint := (depth1_obstructions_are_exactly_middle_pairs 3 i j (by omega) hi hj hne).mp hprofile
  have hi' : i = 1 ∨ i = 2 := by omega
  have hj' : j = 1 ∨ j = 2 := by omega
  rcases hi' with rfl | rfl <;> rcases hj' with rfl | rfl <;> first | contradiction | decide

def shifting : LocalStrategy 0 where
  importDiscipline := .oneTime
  colour := fun _ i => i % 2
  view := fun n i => n + i % 2
  locality := fun n => ⟨fun xs => n + xs.headD 0, fun _ => rfl⟩

theorem shifting_finite : FiniteDeclaration 2 shifting :=
  fun _ x => Nat.mod_lt x (by decide)

theorem shifting_not_clears : ¬ Clears shifting :=
  finite_local_not_clears shifting 2 shifting_finite
```

## Line-by-line Lean explanation

**The class (LocalStrategy 21-32).** `ImportDiscipline` has two
constructors and nothing else; `deriving DecidableEq` lets `decide`
compare tags. `LocalStrategy d` is a structure whose last field is a
proof, so a value of the type carries its locality; one cannot build a
member whose view reads outside the window. The factor `g` lives inside
`ViewLocal` under `∀ n`, so it may differ from one length to the next
(the book's `shifting` has `g = (n + ·)`); the Python docstring's "one
fixed factor function" describes a narrower class. The audit records this
as a minor interpretation defect; the Lean exclusion covers the wider
class, so nothing is lost.

**The predicates (35-70).** `FiniteDeclaration` bounds `colour n x` for
*every* `x : Nat`, not only `x ≤ n`; that is what makes the identity
colouring fail it at `x = k`. `BaseObstructed` is a `Prop`-valued
structure with four fields. `Fires` binds `_S` and never uses it: the
book's `fires_ignores_strategy` proves `Fires bare = Fires valued` by
`rfl`, because after unfolding both sides are the same term. `ClearsOn`,
`Clears`, `IdentityGrade` quantify over the view. `RecurringImport` is an
equation on the tag; the Lean never connects it to an import, a cost or
an event.

**`fires_every_strategy` (72-76).** `n0 = 3`; for `n ≥ 3`,
`generation_never_dries n hn` gives `1 ≠ 2` and equal profiles at 1 and
2 (Unit 40); the two bounds `1 ≤ n`, `2 ≤ n` are `omega`. The strategy
`S` appears only in the statement.

**`identityGrade_implies_clears` (78-81).** A base-obstructed pair is in
particular a distinct pair within the carrier, so identity grade gives
distinct views.

**`strategy_capacity_collision` (84-89).** One application of Unit 42's
`capacity_bound` to `colour n`, `view n`, the alphabet bound `hfinite n`
and the member's own `locality n`. Nothing is added; the threshold is
Unit 42's.

**`finite_local_not_clears` (93-102).** Suppose `Clears S`. Take `n` at
the threshold (`by simp [n]` discharges `n ≤ n` after the `let`). The
collision gives deep `i ≠ j` with equal views. Deep means `0 < i < n`
and `0 < j < n` after the `omega`s, so `middle_profile` rewrites both
profiles to the middle value: `BaseObstructed n i j`. `Clears` then
demands distinct views, contradicting `hview`.

**`finite_local_not_identityGrade` (104-107)** is the composite with
`identityGrade_implies_clears`.

**`g1_local_finite_alphabet_class` (113-119) and `g1_class_exclusion`
(G1Class 30-34).** The three conjuncts are `fires_every_strategy`,
`finite_local_not_clears`, and `fun hcycle => hnot hcycle.2.1`: the third
is the second applied to the middle component of the hypothesis. The
book's `cycle_from_not_clears` states that step on its own, with no
finiteness hypothesis. So the theorem's content is `¬ Clears S`; the
first conjunct is true of every strategy and the third is a rewording of
the second. The word "cycle" in the docstring and the paper names a
conjunction of three static predicates; no sequence of rounds is
modelled. `local_strategy_cycle_impossible` (G1Class 22-26) is the third
conjunct alone.

**The members (123-175).** `zeroRadiusStrategy` builds a radius-0 member
whose view is its colouring; the locality factor is `headD 0` on the
one-element window, discharged by `simp [colourBall, ball]`. `bare`
colours by the 3-bit depth-1 profile code (`profileCode`: presence bit,
incoming bit times 2, outgoing bit times 4, all below 8 by
`profileCode_lt_eight`). `presence := bare`: the definitional
identification is stated as `presence_eq_bare`. `depthTwo` colours the
same way and views the radius-1 window in base 8. `perPairFreshMark` and
`valued` are `zeroRadiusStrategy` on the identity with the two tags; the
book's `perPair_valued_same_functions` (two `rfl`s) and
`perPair_valued_tags_differ` (`decide`) record that they differ in the
tag and nowhere else.

**`depthTwo_clears_n4` (191-201).** A base-obstructed pair at length 4
is a middle pair by `depth1_obstructions_are_exactly_middle_pairs`, so
`i, j ∈ {1, 2, 3}`; nine cases, the diagonal by `contradiction` with
`hne`, the rest by `decide` on the views 508, 511, 255 (the book's
`depthTwo_views_four`). At length 5 the pair `(2, 3)` both read 511, the
book's `depthTwo_fails_at_five`: one length clearing is not clearing.

**`perPair_not_finite`, `valued_not_finite` (209-222).** At `n = 0`,
`x = k`, the colour is `k`, not below `k`. The two identity-grade members
are not refuted; they are placed outside the hypothesis.

**`valued_clears` (224-225)** is identity grade (`simpa` on `i ≠ j`)
through `identityGrade_implies_clears`. **`class_nonvacuity` (227-230)**
bundles a firing member, the length-4 clearance and an identity-grade
member. **`bare_not_identityGrade` (232-239)**: the pair `(1, 2)` at
length 3 has equal codes (the book's `bare_views_three`: 7 and 7).

**`clears_does_not_imply_not_fires` (G1Class 41-43).** The witness is
`valued` with `valued_clears` and `fires_every_strategy valued`. The
book's `any_clearing_member_fires` shows the second component is
available for any member whatsoever: the counterexample says that the
predicates, as defined, cannot express a repair stopping the demand. The
ledger's conclusion, that G3 needs a state-transition hypothesis, is the
right reading; "a discovery about the valued rule" is not.

**The book's `parity` and `shifting`.** `parity` is a two-colour member:
finite (`Nat.mod_lt`), hence not clearing by the Genesis theorem;
threshold 4; a collision at length 4 from `strategy_capacity_collision`;
`(1, 3)` concretely; and `ClearsOn parity 3` by the same case analysis as
Genesis's length-4 proof. `shifting` has view `n + i % 2`: the factor
`fun xs => n + xs.headD 0` depends on `n`, and the locality proof is
`rfl` because `ball i 0` reduces to `[i − 0 + 0]`. The class admits it
and the exclusion applies to it.

## What has been proved

- Inside the declared class, every member with a fixed alphabet bound
  fails to clear some chain length, the length being computable from `k`
  and `d` (Genesis, `finite_local_not_clears`).
- Hence no such member is identity-grade, and the conjunction
  `Fires ∧ Clears ∧ ¬ RecurringImport` is excluded for it (Genesis).
- The five members have the stated classifications; depth-two clears
  length 4 and not length 5; per-pair and valued are identity-grade,
  clearing, and not finite declarations (Genesis; Python through 15).
- `Clears` does not imply `¬ Fires` (Genesis), and this holds for any
  clearing member because `Fires` ignores its argument (book).
- A two-colour radius-0 member is excluded at length 4 after clearing
  length 3; a length-dependent factor is admitted by the class (book).

## What has not been proved

- Unrestricted G1: anything about a repair that is not a fixed-radius,
  fixed-alphabet local view (an alphabet growing with `n`; a view
  reading the index). The ledger: outside the class, not disproved.
- Anything dynamic: no state changes when a repair is applied, so no
  theorem says what a repair does to later demands. G3 and G4 remain
  conjectures by the paper's own terminal block (`G3_REMAINS_CONJECTURE`,
  `G4_REMAINS_CONJECTURE`; the earlier "455 pairs run through the
  engine" claim is withdrawn there).
- Any relation between the tag `recurring` and an actual import or cost.
  The paper's "clears by recurring imports" reads the tag as a derived
  property; the ledger classes the tag as declared metatheory.
- That the member "fires": `Fires S` is a fact about the chain. The
  phrase in the paper and ledger (`CL-G1-CLASS-EXCLUSION`) overreads a
  correct theorem.
- Closure-policy obligation OB1: unchanged by this module, as its header
  says.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `colour`, `view : Nat → Nat → Nat` | the strategy families | total metatheoretic functions over every length and index; the finitude rule flags them as supplied, not derived |
| `ImportDiscipline` | the tag | declared label; uninterpreted in Lean |
| `FiniteDeclaration` | the hypothesis | admitted; impossible at `k = 0`, making the conditional exclusion vacuous there; inhabited at `k = 8` by bare and depth-two |
| `capacity_bound`, `generation_never_dries`, `middle_profile` | the proof | Units 42 and 40 |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** The chain and its profiles (Unit 40). The
class is declared from outside and the theorem says what happens to
anything of that shape. The honest statement of the result is the
ledger's: the class-relative exclusion is proved; the class was not
derived; the repair channel outside it is not addressed.

**Phrases to read with care.**

- "Every member fires": every chain of length at least 3 has an
  obstruction; the member is not involved.
- "The fire/clear/no-recurring-import cycle is impossible": a
  conjunction of three predicates at one time, not a cycle of events; and
  it is impossible because `Clears` is.
- "Per-pair clears by recurring imports": per-pair and valued are the
  same view; the difference is a declared tag.
- "The depth-two member really clears": one length, 4; it fails at 5.

## Student exercise

Build, in words, a member of the class with three colours and radius 1.
Give the length at which the theorem guarantees a failure, and explain
why the length-4 success of depth-two does not contradict the theorem for
your member either.

## Answer

<details>
<summary>Worked answer</summary>

Any colouring `colour n x < 3` and any view reading the three-colour
window, for instance `view n i = encode 3 (colourBall (colour n) i 1)`,
with `locality` given by `encode 3`. `FiniteDeclaration 3` holds, so by
`finite_local_not_clears` the member does not clear. The guaranteed
length is `3^(2·1 + 1) + 2·1 + 2 = 31`. At that length the deep points
are those `i` with `1 < i` and `i + 1 < 31`, that is `2..29`, twenty-eight
of them, while a radius-1 window over three colours has `3^3 = 27`
possible colourings; Unit 42's pigeonhole gives two deep points with the
same window, hence the same view, and both are middle points with the
same profile. The failure is guaranteed at length 31 (and at every
greater length), not at length 4; depth-two's clearing of length 4 is one
`ClearsOn`, and `Clears` quantifies over all lengths. The theorem never
says a finite member fails at every length, only that it fails at one.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/LocalStrategy.lean` lines 21-70 (class and predicates), 72-119 (the exclusion), 123-175 (members), 177-260 (member facts and classifications); `lean4/Derivation/G1Class.lean` lines 22-43 |
| Axiom report | `artifacts/lean_axioms.txt` lines 1262-1287: all within `{propext, Quot.sound}`; `profileCode_lt_eight` none; five member facts `propext` only |
| Paper | `paper/endogenous_generator.md` "2026-08-26 — local finite-alphabet class theorem" (current terminal block, the class and the exclusion, five strategies, T5/G3/G4); `paper/paper_claim_ledger.md` `CL-G1-LOCAL-CLASS`, `CL-G1-CAPACITY-APPLICATION`, `CL-G1-CLASS-EXCLUSION`, `CL-G1-FIVE-STRATEGIES`, `CL-G1-G3-COUNTEREXAMPLE`, `CL-G1-G4-FINITE` (withdrawn) |
| Python | `code/derivation/local_strategy.py`, `artifacts/local_strategy.json`, `tests/test_local_strategy.py`; `code/derivation/g1_class_receipt.py` binds the 26 axiom reports |
| Check (Python) | `python textbook/checks/u43_local_strategy.py`: five rows against the artifact; `Fires` ignores the strategy; per-pair and valued identical; thresholds 10, 10, 516 and their collisions; depth-two at 4 and 5; bare at 3; the negative locality probe; the parity member |
| Check (book Lean) | `python textbook/checks/u43_lean.py`: seventeen book declarations plus nine Genesis theorems kernel-checked, Lean 4.33.0 |
