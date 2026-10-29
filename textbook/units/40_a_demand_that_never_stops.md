# Unit 40. A growing chain keeps equal three-bit profiles

**Claim.** For the declared chain and three-bit observation, every stage
n ≥ 3 contains distinct positions 1 and 2 with equal profiles. A policy
can demand their separation. This is a fact about the indexed chain
states, not a proof that a physical process runs forever.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Put Unit 39's reflective chain under a declared observation
regime of depth 1, which sees of each element only whether it is tagged,
whether some link enters it and whether some link leaves it, and apply
the declared policy demanding separation of distinct admitted positions
with equal profiles. This reuses the pair-separation idea, not the
`Regime` context type of Unit 08. Lean proves the endpoint and interior
profiles; all three classes are inhabited when `n ≥ 2`. For `n ≥ 1` and
distinct admitted positions, equal-profile pairs are *exactly* interior pairs
(`depth1_obstructions_are_exactly_middle_pairs`, an iff). For every stage
`n ≥ 3`, positions 1 and 2 still agree (`generation_never_dries`). The
chain family iterates a declared step in the metatheory; this theorem has
no event runner or object-language demand store. Lean also
proves the fates of three repairs: marking presence changes nothing
(`automark_presence_vacuous`); beyond any fixed finite list of marked
positions there is a larger-stage interior pair with equal base profiles
(`finite_marks_outrun`); marking with the element's own index separates
every pair and so ends generation (`valued_marks_collapse_generation`).
Depth-2 observation repairs the pair (1, 3) at length 4 and is outrun by
(2, 3) at length 5 (two decided instances). That no declared strategy
both fires, repairs and never imports is a computation over five
strategies for 15 rounds.

**Status:** derived (profile classes,
exactness, generation, the three depth-1 fates); derived at two instances
(depth 2); bounded computation in class (the exclusion); OPEN (the
general repair-strategy exclusion; Unit 41 proves the specified radius
profile result and its interior correspondence). **Lean:**
`lean4/Derivation/Generator.lean` lines 35-46, 55-122, 131-172,
183-188, 198-249, 259-271, 277-294. **Axioms:** within
`{propext, Quot.sound}`. **Depends on:** `reflState`, `stepRefl`,
`reflective_chain_growth`, `reflective_chain_successor_relation` (Unit
39); `List.range`, `List.map`, `List.foldr`.

</details>

## First pass

At stage 3 the declared chain has three links and four positions:

```text
0 → 1 → 2 → 3
```

Every position except 0 is tagged. Ask only three Yes/No questions:
“tagged?”, “has an incoming link?”, and “has an outgoing link?”

| Position | Tagged? | Incoming? | Outgoing? |
|---|---|---|---|
| 0 | No | No | Yes |
| 1 | Yes | Yes | Yes |
| 2 | Yes | Yes | Yes |
| 3 | Yes | Yes | No |

Positions 1 and 2 are different places with identical three-bit answers.
The relation itself contains more information than these answers retain:
0 links directly to 1, not to 2. The chosen observation ignores which
other position supplies a link.

**Predict:** if the next stage adds position 4, do positions 1 and 2
become distinguishable by these same three questions?

<details>
<summary>Check your prediction</summary>

No. Both remain tagged and have incoming and outgoing links. The theorem
proves this agreement at every stage n ≥ 3 of the declared family.

</details>

A richer observation can distinguish more. Reading each position's
index separates every pair by definition; it changes the information
supplied to the observer.

## Question

Unit 39 gave a chain state for every finite number of applications of a
declared rule. Its successor shape was supplied by that rule; theorems
proved what its iterations contain. This unit asks a
different question of the same chain: if an observer with a fixed,
finite vocabulary looks at it, does the chain keep producing things the
observer cannot tell apart? If so, the closure policy of Unit 28 keeps
demanding a separation, round after round, with no outside event. And
if the observer tries to pay the demand, what does each way of paying
cost?

## What we already possess

- The chain: `reflState n` has carrier `List.range (n + 1)`, links
  `(k, k + 1)` for `k < n` (Unit 39), and, proved here first, tags
  `[1, …, n]` (`reflective_chain_tags`).
- Profiles and separability in Unit 08 used contexts. Here the observation
  is the explicitly defined Boolean triple below. The policy demands a
  response to equal profiles on distinct admitted positions. Units 28 and
  34 bound rounds with fresh recorded demands and no new data; fixed data
  alone do not bound every successful event. Here the data are *not* fixed: the
  chain grows by one element per round.
- The fact/law and realization distinctions of Unit 39.

## New concept: a depth-1 profile, and three fates for a repair

`reflState n` has `n` links and `n + 1` positions, numbered 0 through
`n`. We call `n` its stage. The older output below calls it “length”;
that label counts links, not data. At stage 0 there is just one untagged
position and no links. At stage 1 only seed and tip classes are inhabited;
at stage 2 an interior class first appears.

`profile1 s i` is a triple of booleans: is `i` in `s.tags`; does some
link in `s.rel` end at `i`; does some link start at `i`. The element's
*index* `i` is bookkeeping in the metatheory; the regime never sees it.
Two distinct elements with equal profiles are an *obstruction*: the
closure policy demands they be separated.

A *repair strategy* is a declared response to an obstruction. Five are
declared: do nothing; mint a fresh observable per unseparated pair and
apply it (an external act each time); mark every receipt with a presence
bit; mark every element with its own index as a readable value; raise
the regime to depth 2 (also see the profiles of neighbours). Each branch
runs 15 rounds, one chain step per round, and is classified by three
implemented predicates: did it ever fire; was every firing round
repaired; how many rounds imported. "Fires, repairs every time, never
imports" is the class the frontier question F5 asked for.

## Plain-language interpretation

Line up the chain's elements and describe each one in three words:
badged or not, something points at it or not, it points at something or
not. The first element is "no badge, nothing in, one out". The last is
"badge, one in, nothing out". Every element in between reads "badge, one
in, one out", and from the third round there are at least two of those.
An observer with only these three words can never tell any two middle
elements apart, and each round adds another one. That is a demand that
never runs dry, produced by the chain's own rule.

How can the demand be paid? Give every receipt the same presence badge:
it adds no information to this view, since all receipts are already tagged.
Hand each unseparated pair a new, never-before-used
sticker: the chosen branch repairs its pairs and imports once in each
firing round tested, rounds 3 through 15. The separate finite-mark theorem
finds a pair beyond any fixed finite list of marked positions; it does
not formalize every dynamic marking procedure.
Let the observer read each element's *position number*: every pair is
told apart at once, and no demand ever fires again. But a position
number for every element is an unbounded vocabulary, one word per
element. This is a richer declared observation, `profileV`, whose second
component is the index. Its separation result is true by that definition;
the earlier three-bit observer did not have that input.
Let the observer also look one step along the links: it tells
apart elements near the ends, and is defeated again two steps deeper in.

The paper summarizes the declared branches as “endogenous demands,
exogenous payments.” The exclusion was tested for five strategies and
15 rounds. It is not a theorem about every possible repair procedure or
about what must happen in physical reality.

## Pseudocode

```
profile1 s i := (i ∈ s.tags, ∃ link ending at i, ∃ link starting at i)

for the chain at stage n >= 1 (n links, n+1 positions):
  profile1 0 = (F, F, T)                  -- seed
  profile1 i = (T, T, T)  for 1 ≤ i < n   -- interior
  profile1 n = (T, T, F)                  -- tip
obstructions = { {i, j} : i ≠ j, profile1 i = profile1 j } = interior pairs

one round of a branch (strategy S, round n):
  state := reflState n                    -- the declared step, not an import
  obs   := pairs the regime (under S) cannot separate
  if S = per_pair: while obs ≠ ∅: mint a fresh mark, apply it to the larger
                   element of the first pair; count one import
  record (fired?, repaired?, imports)
classification: fired ∧ repaired every firing round ∧ imports = 0 → endogenous_cycle
```

## Python

```python
from derivation.generator import obstructions, profile1, profile2, run_branch, STRATEGIES

print([profile1(5, i) for i in range(6)])
print([obstructions("none", n, {}) for n in range(1, 5)])
for s in STRATEGIES:
    r = run_branch(s)
    print(s, r.first_fire_round(), r.per_round_import_rounds(), r.classification())
print(profile2(4, 1) != profile2(4, 3), profile2(5, 2) == profile2(5, 3))
```

Output:

```text
[(False, False, True), (True, True, True), (True, True, True), (True, True, True), (True, True, True), (True, True, False)]
[[], [], [(1, 2)], [(1, 2), (1, 3), (2, 3)]]
none 3 0 fires_unrepaired
per_pair_fresh_mark 3 13 repairs_by_recurring_imports
automark_presence 3 0 fires_unrepaired
automark_valued None 0 generation_dead
depth2 5 0 fires_unrepaired
True True
```

The check script's run, every classification compared with
`artifacts/generator.json`:

```text
depth-1 profiles (tagged, entered, left) of the chain of length 5:
  element 0: (False, False, True)
  element 1: (True, True, True)
  element 2: (True, True, True)
  element 3: (True, True, True)
  element 4: (True, True, True)
  element 5: (True, True, False)
obstructions of the bare chain == interior pairs, lengths 1..15:
  True; length 2: []; length 3: [(1, 2)]
five strategies, 15 rounds: fired, first fire, repaired every round, rounds that imported, classification
  none                   True  3    False  0 fires_unrepaired
  per_pair_fresh_mark    True  3    True  13 repairs_by_recurring_imports
  automark_presence      True  3    False  0 fires_unrepaired
  automark_valued        False None True   0 generation_dead
  depth2                 True  5    False  0 fires_unrepaired
  endogenous cycle found: False (artifact False)
per-pair marking (round, obstructions before, imports, after): [(1, 0, 0, 0), (2, 0, 0, 0), (3, 1, 1, 0), (4, 1, 1, 0), (5, 1, 1, 0)] ... (15, 1, 1, 0)
outrun: marks [1, 2, 3]; at length 6 the unmarked pair (4, 5) has equal profiles: True; presence view of 1 and 2 at length 3 equal: True; valued view: ((True, True, True), 1) vs ((True, True, True), 2)
depth 2: length 4, elements 1 and 3 differ: True; length 5, elements 2 and 3 equal: True; depth-2 obstructions at lengths 4..7: [0, 1, 3, 6]
Lean agreement block: {'depth1_obstructions_are_exactly_middle_pairs': True, 'depth2_separates_near_ends_n4': True, 'depth2_obstruction_n5': True, 'valued_marks_collapse_generation': True} (matches artifact: True)
failures: []
```

## Line-by-line Python explanation

`chain_tags(n)` is the set `{1, …, n}` and `chain_rel(n)` the links
`(k, k + 1)` for `k < n`: the Python chain is written directly from the
Lean theorems of Unit 39 and this unit, not recomputed through
`stepRefl` (`test_chain_matches_lean_shape` checks the shape).
`profile1(n, i)` is the triple. `profile2(n, i)` adds the list of
profiles of the elements linking into `i` and of those `i` links to.

`view(strategy, n, i, marks)` is what the regime sees under each
strategy: at depth 2 the depth-2 profile; otherwise the depth-1 profile
plus, for presence marking, the bit `i >= 1` (true of every receipt, so
equal to the tag bit already present); for valued marking the index `i`
itself; for per-pair marking the set of minted marks applied to `i`.
`obstructions` lists the unordered pairs with equal views.

`repair_per_pair` loops while an obstruction exists: it takes the first
pair, mints a fresh mark, applies it to the larger element, and counts
one repair. Every mint is an import. `run_branch` runs 15 rounds, each
round one chain step, then the demand, then the repair, and records
obstructions before and after, repairs and imports. `classification`
decides among four names by the three predicates. The table shows: bare,
presence and depth-2 fire and never repair; per-pair repairs every
firing round and imports in every one of the 13 firing rounds; valued
never fires. `exclusion_check` reports that no strategy is in the
`endogenous_cycle` class. The per-pair row shows exactly one obstruction
before each round from 3 on: last round's marks separate everything but
the newest interior pair, so one fresh mark per round suffices, and one
is needed.

Depth 2's obstruction counts `[0, 1, 3, 6]` at lengths 4 to 7 are the
interior-minus-ends pairs `C(n − 3, 2)`: depth 2 separates the two
elements adjacent to the ends and nothing deeper. `lean_agreement`
recomputes the four Lean facts that are decidable by computation and
the artifact records them as true.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Generator.lean lines 55-58, 97-98, 105-106, 115-116
def profile1 (s : PState) (i : Nat) : Bool × Bool × Bool :=
  (decide (i ∈ s.tags),
   decide (∃ p ∈ s.rel, p.2 = i),
   decide (∃ p ∈ s.rel, p.1 = i))

theorem middle_profile (n i : Nat) (h1 : 1 ≤ i) (h2 : i < n) :
    profile1 (reflState n) i = (true, true, true) := by
  have ht := (chain_tagged_iff n i).mpr ⟨h1, by omega⟩
  have hin := (chain_hasIn_iff n i).mpr ⟨h1, by omega⟩
  have hout := (chain_hasOut_iff n i).mpr h2
  simp only [profile1, decide_eq_true ht, decide_eq_true hin,
             decide_eq_true hout]

theorem endpoint0_profile (n : Nat) (h : 1 ≤ n) :
    profile1 (reflState n) 0 = (false, false, true) := by
  ...
theorem endpointN_profile (n : Nat) (h : 1 ≤ n) :
    profile1 (reflState n) n = (true, true, false) := by
  ...
```

```lean
-- Lean (Genesis), lean4/Derivation/Generator.lean lines 131-134, 183-188, 198-202, 221-235, 243-249, 259-263, 277-294
theorem depth1_obstructions_are_exactly_middle_pairs
    (n i j : Nat) (hn : 1 ≤ n) (hi : i ≤ n) (hj : j ≤ n) (hne : i ≠ j) :
    (profile1 (reflState n) i = profile1 (reflState n) j) ↔
      (1 ≤ i ∧ i < n ∧ 1 ≤ j ∧ j < n) := by
  ...   -- trichotomy seed / tip / interior for each of i, j; nine cases

theorem generation_never_dries (n : Nat) (h : 3 ≤ n) :
    (1 : Nat) ≠ 2 ∧
      profile1 (reflState n) 1 = profile1 (reflState n) 2 := by
  refine ⟨by omega, ?_⟩
  rw [middle_profile n 1 (by omega) (by omega),
      middle_profile n 2 (by omega) (by omega)]

theorem automark_presence_vacuous (n : Nat) (h : 3 ≤ n) :
    (∀ i, 1 ≤ i → i ≤ n → i ∈ (reflState n).tags) ∧
      profile1 (reflState n) 1 = profile1 (reflState n) 2 :=
  ⟨fun i h1 h2 => (chain_tagged_iff n i).mpr ⟨h1, h2⟩,
   (generation_never_dries n h).2⟩

theorem finite_marks_outrun (marks : List Nat) :
    ∃ n i j, 1 ≤ i ∧ i < n ∧ 1 ≤ j ∧ j < n ∧ i ≠ j ∧
      i ∉ marks ∧ j ∉ marks ∧
      profile1 (reflState n) i = profile1 (reflState n) j := by
  refine ⟨marks.foldr max 0 + 3, marks.foldr max 0 + 1,
          marks.foldr max 0 + 2,
          by omega, by omega, by omega, by omega, by omega, ?_, ?_, ?_⟩
  · intro hmem
    have := le_foldr_max marks _ hmem
    omega
  · intro hmem
    have := le_foldr_max marks _ hmem
    omega
  · rw [middle_profile _ _ (by omega) (by omega),
        middle_profile _ _ (by omega) (by omega)]

def profileV (s : PState) (i : Nat) : (Bool × Bool × Bool) × Nat :=
  (profile1 s i, i)

theorem valued_marks_collapse_generation (n i j : Nat) (h : i ≠ j) :
    profileV (reflState n) i ≠ profileV (reflState n) j := by
  intro he
  exact h (congrArg Prod.snd he)

def swap12 (k : Nat) : Nat := if k = 1 then 2 else if k = 2 then 1 else k

theorem middle_swap_not_relation_preserving (n : Nat) (h : 2 ≤ n) :
    (0, 1) ∈ (reflState n).rel ∧
      ((swap12 0, swap12 1) ∉ (reflState n).rel) := by
  ...

def profile2 (s : PState) (i : Nat) :
    (Bool × Bool × Bool) × List (Bool × Bool × Bool) ×
      List (Bool × Bool × Bool) :=
  (profile1 s i,
   (s.rel.filter (fun p => decide (p.2 = i))).map (fun p => profile1 s p.1),
   (s.rel.filter (fun p => decide (p.1 = i))).map (fun p => profile1 s p.2))

theorem depth2_separates_near_ends_n4 :
    profile2 (reflState 4) 1 ≠ profile2 (reflState 4) 3 := by decide

theorem depth2_obstruction_n5 :
    profile2 (reflState 5) 2 = profile2 (reflState 5) 3 ∧
      (2 : Nat) ≠ 3 := by decide
```

The book's Lean checks the stage-0 singleton, writes the profile table out, locates the threshold
(length 2 does not fire, length 3 does), instantiates the exactness iff
and the outrun theorem, shows what the valued profile separates by, and
writes the depth-2 profiles out at lengths 4, 5 and 6.

```lean
-- Lean (book), textbook/checks/u40_lean.py
theorem tags_three : (reflState 3).tags = [1, 2, 3] := by
  rw [reflective_chain_tags]; rfl

theorem profile_table_four :
    profile1 (reflState 4) 0 = (false, false, true) ∧
    profile1 (reflState 4) 1 = (true, true, true) ∧
    profile1 (reflState 4) 2 = (true, true, true) ∧
    profile1 (reflState 4) 3 = (true, true, true) ∧
    profile1 (reflState 4) 4 = (true, true, false) := by decide

theorem profile_table_four_by_classes :
    profile1 (reflState 4) 0 = (false, false, true) ∧
    profile1 (reflState 4) 2 = (true, true, true) ∧
    profile1 (reflState 4) 4 = (true, true, false) :=
  ⟨endpoint0_profile 4 (by omega), middle_profile 4 2 (by omega) (by omega),
   endpointN_profile 4 (by omega)⟩

theorem no_fire_at_two : profile1 (reflState 2) 1 ≠ profile1 (reflState 2) 2 := by
  decide

theorem fires_at_three : profile1 (reflState 3) 1 = profile1 (reflState 3) 2 :=
  (generation_never_dries 3 (by omega)).2

theorem obstructions_of_one_at_four :
    ¬ profile1 (reflState 4) 1 = profile1 (reflState 4) 0 ∧
    profile1 (reflState 4) 1 = profile1 (reflState 4) 3 ∧
    ¬ profile1 (reflState 4) 1 = profile1 (reflState 4) 4 := by
  refine ⟨?_, ?_, ?_⟩
  · intro h
    have := (depth1_obstructions_are_exactly_middle_pairs 4 1 0 (by omega) (by omega)
      (by omega) (by omega)).mp h
    omega
  · exact (depth1_obstructions_are_exactly_middle_pairs 4 1 3 (by omega) (by omega)
      (by omega) (by omega)).mpr ⟨by omega, by omega, by omega, by omega⟩
  · intro h
    have := (depth1_obstructions_are_exactly_middle_pairs 4 1 4 (by omega) (by omega)
      (by omega) (by omega)).mp h
    omega

theorem outrun_instance :
    profile1 (reflState 6) 4 = profile1 (reflState 6) 5 ∧ 4 ∉ [1, 2, 3] ∧ 5 ∉ [1, 2, 3] := by
  refine ⟨?_, by decide, by decide⟩
  rw [middle_profile 6 4 (by omega) (by omega), middle_profile 6 5 (by omega) (by omega)]

theorem valued_separates_by_index_only :
    profileV (reflState 3) 1 ≠ profileV (reflState 3) 2 ∧
    (profileV (reflState 3) 1).1 = (profileV (reflState 3) 2).1 :=
  ⟨valued_marks_collapse_generation 3 1 2 (by omega), fires_at_three⟩

theorem depth2_values_four :
    profile2 (reflState 4) 1 =
      ((true, true, true), [(false, false, true)], [(true, true, true)]) ∧
    profile2 (reflState 4) 3 =
      ((true, true, true), [(true, true, true)], [(true, true, false)]) := by decide

theorem depth2_values_five :
    profile2 (reflState 5) 2 = ((true, true, true), [(true, true, true)], [(true, true, true)]) ∧
    profile2 (reflState 5) 3 = profile2 (reflState 5) 2 ∧
    profile2 (reflState 6) 2 = profile2 (reflState 6) 4 := by decide
```

## Line-by-line Lean explanation

**`reflective_chain_tags` (lines 35-46).** Induction on `n`, as for the
carrier in Unit 39: the tag appended at step `m + 1` is `m + 1` (the
carrier length, by `reflective_chain_growth`), and `List.range (m + 1)`
mapped through `(· + 1)` ends in `m + 1` (`List.range_succ`,
`List.map_append`). So the seed `0` is never tagged and every receipt
is. The book's `tags_three` reads `[1, 2, 3]` off it.

**`profile1` and the three `chain_*_iff` (lines 55-91).** Each
component of the profile is a `decide` of a membership statement. The
three lemmas turn those statements into arithmetic on `i` and `n`:
tagged iff `1 ≤ i ≤ n`; entered iff `1 ≤ i ≤ n` (the link `(i − 1, i)`,
with `Nat.sub_add_cancel` to put `i − 1 + 1 = i` back together); left
iff `i < n` (the link `(i, i + 1)`). All three rewrite the chain's
structure theorems from Unit 39 and then unfold `List.mem_map` and
`List.mem_range`.

**The three classes (lines 97-122).** `middle_profile`: for
`1 ≤ i < n` all three arithmetic conditions hold, so after
`decide_eq_true` on each the profile is `(true, true, true)`.
`endpoint0_profile`: at `0`, tagged and entered are refuted by the iffs
(`omega` on `1 ≤ 0`) and left holds since `0 < n`. `endpointN_profile`:
at `n`, tagged and entered hold and left is refuted by
`Nat.lt_irrefl`. The book's `profile_table_four_by_classes` is three
applications; `profile_table_four` gets the same table by `decide`,
which evaluates `reflState 4` outright.

**`depth1_obstructions_are_exactly_middle_pairs` (lines 131-172).** The
local `tri` says every `m ≤ n` is `0`, `n`, or interior. Applied to `i`
and to `j` that gives nine cases. Three are ruled out by `hne` (both
`0`, both `n`) or give the conclusion (both interior). The other six
rewrite both profiles by the class theorems and refute the equality of
two different concrete triples by `decide`. The converse direction
rewrites both profiles to `(true, true, true)`. This is why the lesson
can say "exactly": the obstruction set is the interior pairs by an iff,
not by inspection of a table. The book's `obstructions_of_one_at_four`
instantiates both directions at length 4.

**`generation_never_dries` (lines 183-188).** For `n ≥ 3`, elements `1`
and `2` are both interior, so both profiles are `(true, true, true)`.
Two lines, after the class theorem. The hypothesis `3 ≤ n` is exact: the
book's `no_fire_at_two` shows that at length 2 element `2` is the tip,
so nothing fires. The paper's phrase "the only event consumed is the
internally enabled reflection” describes the supplied iteration:
`reflState n` is built by `stepRefl` alone. The theorem itself states a
profile equality for each `n`; it does not execute events or establish
that any runtime continues indefinitely.

**`automark_presence_vacuous` (lines 198-202).** A pair of facts already
proved: every receipt is tagged, and `1`, `2` still collide. The repair
"mark presence" adds a bit the regime already sees.

**`finite_marks_outrun` (lines 204-235).** `le_foldr_max` is the
library-grade fact that `foldr max 0` bounds every member of a list. Let
`M` be that bound. The witnesses are length `M + 3` and the pair
`(M + 1, M + 2)`: both interior (`1 ≤ M + 1`, `M + 2 < M + 3`), both
unmarked (a member would be `≤ M`), and equal by `middle_profile`. The
book's `outrun_instance` is the case `marks = [1, 2, 3]`, where the
theorem's witness is length 6 and the pair `(4, 5)`; `outrun_general`
is the same theorem applied. **Read with care:** the theorem is static.
It says no *fixed* finite marking is final. The dynamic claim in its
docstring, that a strategy which keeps minting marks imports at every
firing round, is the Python per-pair trajectory (13 of 15 rounds), not
this statement. The audit records that gap as a minor interpretation
defect of the docstring.

**`valued_marks_collapse_generation` (lines 243-249).** `profileV`
pairs the profile with the index. Two `profileV` values with distinct
indices are distinct: `congrArg Prod.snd` on an equality of pairs gives
an equality of second components, contradicting `h`. The theorem is
true by construction and the paper says so ("identity-grade
observation"). The book's `valued_separates_by_index_only` makes the
point sharper: at length 3 the first components of `profileV 1` and
`profileV 2` are equal (that is `fires_at_three`), so the separation
comes from the added index component rather than the original three-bit
component. The richer observer is still a defined observation; it has
different inputs from `profile1`.

**`middle_swap_not_relation_preserving` (lines 259-271).** `swap12`
exchanges `1` and `2`. The link `(0, 1)` is in the chain; its image
`(0, 2)` is not, since every link is `(k, k + 1)`. So the transposition
of the two colliding interior elements is not a symmetry of the chain,
unlike the swap of Unit 39's bridge. The ledger states the nonclaim: this
is one transposition, not a theorem about all automorphisms, and not a
proof that the directed chain is rigid.

**Depth 2 (lines 277-294).** `profile2` adds the lists of profiles of
in-neighbours and out-neighbours. At length 4, element `1`'s in-neighbour
is the seed `(false, false, true)` and element `3`'s out-neighbour is the
tip `(true, true, false)`: the book's `depth2_values_four` shows the two
triples in full, and they differ in both lists. At length 5, elements `2`
and `3` each have an interior neighbour on both sides, so their depth-2
profiles are equal (`depth2_values_five`, which also shows `(2, 4)` at
length 6). Both Genesis theorems are `decide` on one length each. The
general statement is proved for the specified radius-`d` profile in
`SeparationCapacity` (Unit 41), with threshold stage `2d + 3`. That module
also proves correspondence between `profile2` and radius 1 on interior
pairs for every stage. The older OPEN note is stale. There is no blanket
theorem identifying an unspecified depth hierarchy with every radius.

## What has been proved

- The chain's tags are `[1, …, n]`. For `n ≥ 1`, admitted positions have
  the stated seed, tip, or interior profile, with three distinct possible
  values; the interior is nonempty only for `n ≥ 2` (Genesis; the book
  checks stage 0 separately).
- At depth 1 the obstructions are exactly the interior pairs, as an iff
  for all `n ≥ 1` and all distinct `i, j ≤ n` (Genesis).
- For every `n ≥ 3` the pair `(1, 2)` is an obstruction, so the closure
  demand fires at every length from 3 on with no event but the chain's
  declared step (Genesis, horizon-free); not at length 2 (book).
- Presence marking leaves the obstruction in place; every finite marking
  is outrun at a larger length; valued marking separates every pair
  (Genesis, each horizon-free).
- Depth 2 separates `(1, 3)` at length 4 and collides `(2, 3)` at length
  5 (Genesis, two instances); and `(2, 4)` at length 6 (book).
- Within five strategies and 15 rounds, no strategy fires, repairs and
  never imports (computation, exhaustive in class).

## What has not been proved

- That *no* repair strategy at all is endogenous: the exclusion is over
  five declared strategies and 15 rounds. The paper's residual G1 asks
  for a repair channel that separates the interior of an unbounded chain
  without identity-grade marks, or a proof that none exists.
- A general theorem about every meaning of observation depth. Unit 41
  proves the structural radius-`d` result and the radius-one/depth-2
  correspondence on interior pairs. That correspondence is no longer OPEN.
- That the chain is rigid, or that no automorphism exchanges interior
  elements: only the direct transposition `swap12` is refuted.
- That generation is minimal or unique: the paper and the Lean header
  both disclaim it.
- Anything about an object-language demand generator: the terminal says
  `OBJECT_LANGUAGE_GENERATOR_NOT_IN_SCOPE`. This is demand persistence for
  one declared chain under one declared policy.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `reflState`, `stepRefl` | the chain | a declared rule iterated in the metatheory (Unit 39's finitude flag) |
| depth-1 regime `profile1` | the demand | declared observation regime |
| the element index `i` | bookkeeping; the valued mark | metatheoretic; made observable only by `profileV` |
| the five strategies, 15 rounds | the exclusion | declared class and bound |
| `List.range`, `List.map`, `List.foldr max` | tags; the outrun witness | metatheory |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** One chain, grown by a declared rule, and the
three-word description of each element. The demand is produced by that
chain and that vocabulary. The repairs that work (per-pair marks; the
index) are supplied from outside: the first at every firing round, the
second once, as an unbounded vocabulary.

**Phrases to read with care.**

- "Forever" and "at every round" are `∀ n` in the metatheory over a
  `Nat`-indexed family of states. Nothing inside any one state holds the
  totality.
- "Never becomes endogenous" (the outrun docstring) is proved for fixed
  finite markings and computed for the minting strategy.
- "The generator dies of success": the valued regime prevents every
  demand; it does not repair one that fired.
- "The first horizon-free challenge generator": a comparison within this
  development, with no minimality or uniqueness claim.

## Student exercise

Under depth 1, how many obstructions does the chain of length `n` have,
and which single pair does the per-pair strategy repair at round `n ≥ 4`
after all earlier rounds' marks are in place? Then say, with the
exactness theorem in hand, why depth-1 obstructions at length `n` never
include the seed or the tip.

## Answer

<details>
<summary>Worked answer</summary>

The obstructions are the interior pairs, so there are `C(n − 1, 2)` of
them: `0, 0, 1, 3, 6, …` for `n = 1, 2, 3, 4, 5`, matching the check's
list at length 4. At round `n ≥ 4` the one unseparated pair is `(1, n − 1)`.
The repair always marks the *larger* element of the first pair, so
element `1` is never marked; each of `2, …, n − 2` received its own
fresh mark in the round it became interior, and those marks are
pairwise distinct; the new interior element `n − 1` carries none, so it
and `1` are the two interior elements with an empty mark set. The
check's per-pair row `(n, 1, 1, 0)` confirms one obstruction and one
import per round from round 3, and `run_branch` records the first pair
as `(1, 2), (1, 3), (1, 4), …`. The seed and the tip are never
obstructions because the iff's right-hand side requires `1 ≤ i < n` of
both elements, and `0` fails the first inequality while `n` fails the
second: their profiles `(false, false, true)` and `(true, true, false)`
differ from the interior's and from each other.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Generator.lean` lines 35-46 (tags), 55-91 (regime), 97-122 (classes), 131-172 (exactness), 183-188 (generation), 198-249 (three repairs), 259-271 (swap), 277-294 (depth 2) |
| Axiom report | `artifacts/lean_axioms.txt` lines 160-175: `reflective_chain_tags` `propext`; the rest `propext, Quot.sound` |
| Paper | `paper/endogenous_generator.md` TERMINAL (four lines), FG2-FG4 (regime, classes, generation), FG5-FG6 (strategies, exclusion), FG7 (swap), FG8 ("endogenous demands, exogenous payments"), frontier conjecture G1; ledger `CL-G-TERMINAL`, `CL-G-GENERATION`, `CL-G-OBSTRUCTIONS-EXACT`, `CL-G-REPAIR-FATES`, `CL-G-DEPTH2`, `CL-G-DIRECT-SWAP`, `CL-G-EXCLUSION` |
| Python | `code/derivation/generator.py`; `artifacts/generator.json` (`bounds`, `exclusion`, `lean_agreement`); `tests/test_generator.py` (`test_generation_never_dries_within_bound`, `test_per_pair_repairs_but_imports_every_firing_round`, `test_exclusion_no_endogenous_cycle_in_class`, `test_lean_agreement_all_hold`) |
| Check (Python) | `python textbook/checks/u40_generator.py`: profile table; exactness on lengths 1-15; five classifications against the artifact; the per-pair import row; the outrun, presence and valued views; depth-2 instances and counts; the Lean-agreement block |
| Check (book Lean) | `python textbook/checks/u40_lean.py`: fourteen book theorems plus eight Genesis theorems kernel-checked, Lean 4.33.0 |
