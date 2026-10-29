# Unit 34. Closed runs bound recorded new demands

**Claim.** With n fixed data and an initially empty demand store, a run that
records a fresh pair each round and admits no new data has at most
n(n−1)/2 rounds. The formal run shape counts recorded demands; it does
not itself require those demands to be met.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Under the declared round shape, one engine round grows the
demand count by exactly one (`round_reqs_succ`) over a fixed datum count
(`round_data_eq`), so a closed run from an empty demand store on `n` data
makes at most `n(n-1)/2` rounds, stated without division as `2 * rounds
≤ n * (n - 1)` (`closedRun_round_bound_from_empty`). The round shape,
`ClosedRun`, is declared: each round imposes a *fresh* target and answers
with a delta admitting *no* fresh datum. That the exported rounds have
this shape is computational.

**Status:** derived under the declared round
shape (R8, discharged 2026-08-18). **Lean:** `Derivation.nodup_subset_length`
(`lean4/Derivation/Rounds.lean` line 145), `mem_allPairs` (205),
`allPairs_nodup` (264), `Round` (283), `ClosedRun` (291-299),
`applyDelta_data_eq` (328), `respond_anatomy` (355-378), `round_reqs_succ`
(380-386), `round_data_eq` (389-395), `closedRun_data_eq` (398),
`closedRun_reqs_length` (405-413), `closedRun_reqs_nodup` (415),
`closedRun_reqs_wf` (425), `closedRun_round_bound` (452-470),
`closedRun_round_bound_from_empty` (472-481). **Axioms:** `propext` for
the round lemmas; `propext, Quot.sound` for the run bounds. **Depends on:**
the impose guard and `insertNew` (Unit 17); `respond` (Unit 31);
`allPairs`, `allPairs_length` and the abstract counting laws (Unit 28).

</details>

## First pass

Three data, A, B, and C, allow three different demands: A/B, A/C,
and B/C. Begin with none recorded. If each round records a previously
absent pair and admits no new datum, the demand count can grow only
through 0, 1, 2, and 3. That is three rounds between four states.

The formal name for this run shape is `ClosedRun`. Its constructor asks
that the pair be fresh, that the response contain no new datum, and that
imposition and replay succeed. It does not ask whether the response
actually separates the pair.

For example, impose A/B on two bare data and apply no items. Replay
succeeds and the demand is recorded. With no forms, A and B remain
collapsed. This is a `ClosedRun` step, but not a valid separation
response.

**Predict:** does the round bound prove that all three possible demands
will be met?

<details>
<summary>Check your prediction</summary>

No. It is an upper bound on this run shape. Runs can stop early, and
meeting demands requires a separate validity check.

</details>

## Question

Unit 28 proved two counting laws about an arbitrary measure, and said
their connection to the engine would come later. Here it is. What is a
"round" as a Lean object, which of its features make the demand count
climb by one and the datum count stand still, and what exactly about the
engine's exported runs is *not* proved by the bound?

## What we already possess

- `stepE r (.impose i j)`: `some { r with reqs := insertNew r.reqs (i, j) }`
  when `i < j ∧ j < r.data`, else `none` (Unit 17). `insertNew l a` is `l`
  if `a ∈ l`, else `l ++ [a]`.
- `respond r i j δ = (stepE r (.impose i j)).bind (applyDelta · δ)`
  (Unit 31).
- `allPairs n`, the ordered pairs below `n`; `2 * (allPairs n).length = n
  * (n - 1)`; `strict_bounded_length` and `no_supply_round_bound` (Unit
  28).
- The closed baselines of the engine, `supply=False`, with their trees of
  4 and 20 nodes (Unit 28's check).

## New concept: a declared shape, and a bound through a language

`Round` is a target pair and a response delta. `ClosedRun r rds t` is an
inductive relation: the empty run from `r` to `r`, and the step that
prepends a round whose target is not already in `r.reqs`, whose response
contains no `newDatum`, and whose `respond` succeeds, to a run from the
outcome. The two side conditions are *constructor hypotheses*. They are
not derived from the closure policy; they are the engine's asserted
invariants, written down so that the theorems can use them.

There is another distinction: this constructor does not require a
collapsed target, `validResponse`, or a met demand store. `respond`
checks imposition and item application, not separation. Even imposing
`(0,1)` on two bare data and answering with an empty delta builds a
one-round `ClosedRun`, although the demand remains unmet. The book
checks this example. The counting bound therefore concerns recorded
fresh demands; it does not prove they were successfully met. The engine
uses further validity checks for its exported creation edges.

The bound is proved through the requirement *language*: every demand of
the final regime is ordered and bounded by `t.data`, which equals
`r.data`, so it lies in `allPairs r.data`; the demands are duplicate-free
(fresh insertion keeps them so); a duplicate-free list inside a
duplicate-free list is no longer (`nodup_subset_length`); and
`allPairs_length` turns the length into `n(n-1)/2`. The counting is done
with the `decide`-filter technique rather than the library's `Nodup`
lemmas, because on this toolchain those carry `Classical.choice`.

## Plain-language interpretation

A closed room has a fixed set of objects. Each round of the game puts one
new "tell these two apart" demand on the table and replays a response
without bringing in a new object. With three objects there are three
pairs, so there can be at most three rounds of this shape. Whether the
responses actually distinguish the pairs is a separate validity question.
The counting needs two things
pinned down: that each round really adds one new pair (the target was
not already demanded) and that nobody sneaks in an object (the answer
admits no datum). Those two are what "closed" and "fresh" mean, and the
engine asserts them; the theorem takes them as given and does the rest.

What the theorem does not do is read the engine. That every round the
engine actually exported has this shape is checked by running the engine
and looking, not by proof.

## Pseudocode

```
# Gloss
Round = (target, response)
ClosedRun r [] r
ClosedRun r (rd :: rest) t  if  rd.target not in r.reqs,
                                newDatum not in rd.response,
                                respond r rd.target rd.response = some mid,
                                ClosedRun mid rest t

one round:  reqs(mid) = reqs(r) ++ [target]   (fresh insertion)
            data(mid) = data(r)                (no datum item)
a run:      length(reqs t) = length(reqs r) + rounds
            data t = data r
            reqs t ordered, below data r, no duplicates
            so reqs t  ⊆  allPairs (data r), both nodup
            so rounds + length(reqs r) <= n(n-1)/2
from empty: 2 * rounds <= n * (n - 1)
```

## Python

```python
from derivation.candidates import Bounds, NewDatum, NewForm, NewInst, delta_events
from derivation.engine import READING_F, build_tree
from derivation.model import AdmitDatum, Impose, replay

def respond(r, i, j, delta):
    return replay((Impose(i, j),) + delta_events(r, delta), r)

bare2 = replay([AdmitDatum("a"), AdmitDatum("b")])
u0 = respond(bare2, 0, 1, (NewForm(1), NewInst(0, (0,))))
print(sorted(u0.reqs), u0.n_data(), respond(bare2, 0, 1, (NewDatum(), NewForm(1), NewInst(0, (0,)))).n_data())

t = build_tree(READING_F, "mu1", Bounds(2, 2), max_rounds=15, pre_expansion_node_guard=200, supply=False)
ok = all(len(t.nodes[e.child].regime.reqs) == len(t.nodes[e.parent].regime.reqs) + 1
         and t.nodes[e.child].regime.n_data() == t.nodes[e.parent].regime.n_data()
         and not any(isinstance(it, NewDatum) for it in e.response)
         for e in t.edges if e.kind == "creation")
print(ok, t.stats()["max_depth"])
```

Output:

```text
[(0, 1)] 2 3
True 3
```

## Line-by-line Python explanation

`respond` is Lean's `respond` built from the Python events: impose, then
the delta's admission events, replayed on `r`.

`bare2` has two data and no demand. One round at `(0, 1)` with the mark
gives demands `[(0, 1)]` and still 2 data: Lean's `U0`, and the anatomy
of `respond_anatomy` read off. The third number, `3`, is a round whose
response begins with `NewDatum`: the datum count moved. Such a round is
not a `ClosedRun` round, by the constructor's second hypothesis; the
Python will happily perform it, which is why the shape is declared rather
than derived.

`build_tree(..., supply=False)` is the closed baseline of reading F. For
every creation edge the check tests the three facts the constructor
asks for: the child has one more demand than the parent, the same datum
count, and the response contains no `NewDatum`. `True`: all 19 edges
have the declared shape (the check script also verifies the new demand
is fresh, and that demands stay ordered, bounded and duplicate-free).
The deepest round is 3, and `2 * 3 ≤ 3 * 2`: the bound holds with
equality in reading F, as it does in reading L (`2 * 1 ≤ 2 * 1`).

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Rounds.lean lines 283-299
structure Round where
  target : Nat × Nat
  response : List Item

inductive ClosedRun : Regime → List Round → Regime → Prop where
  | nil : ∀ r, ClosedRun r [] r
  | cons : ∀ (r : Regime) (rd : Round) (mid t : Regime)
      (rds : List Round),
      rd.target ∉ r.reqs →
      Item.newDatum ∉ rd.response →
      respond r rd.target.1 rd.target.2 rd.response = some mid →
      ClosedRun mid rds t →
      ClosedRun r (rd :: rds) t
```

```lean
-- Lean (Genesis), lean4/Derivation/Rounds.lean lines 380-395
theorem round_reqs_succ {r s : Regime} {i j : Nat} {δ : List Item}
    (hfresh : (i, j) ∉ r.reqs) (h : respond r i j δ = some s) :
    s.reqs.length = r.reqs.length + 1 := by
  obtain ⟨_, _, hreqs, _⟩ := respond_anatomy h
  rw [hreqs, insertNew_of_not_mem hfresh, List.length_append]
  rfl

theorem round_data_eq {r s : Regime} {i j : Nat} {δ : List Item}
    (hnd : Item.newDatum ∉ δ) (h : respond r i j δ = some s) :
    s.data = r.data := by
  obtain ⟨_, _, _, happ⟩ := respond_anatomy h
  exact applyDelta_data_eq
    (r := { r with reqs := insertNew r.reqs (i, j) }) hnd happ
```

```lean
-- Lean (Genesis), lean4/Derivation/Rounds.lean lines 452-481
theorem closedRun_round_bound {r t : Regime} {rds : List Round}
    (h : ClosedRun r rds t) (hn : r.reqs.Nodup)
    (hwf : ∀ q ∈ r.reqs, q.1 < q.2 ∧ q.2 < r.data) :
    2 * (r.reqs.length + rds.length) ≤ r.data * (r.data - 1) := by
  have hlen := closedRun_reqs_length h
  have hdata := closedRun_data_eq h
  have hnod := closedRun_reqs_nodup h hn
  have htwf := closedRun_reqs_wf h hwf
  have hsub : ∀ q ∈ t.reqs, q ∈ allPairs r.data := by
    intro q hq
    obtain ⟨h1, h2⟩ := htwf q hq
    exact mem_allPairs r.data q h1 (hdata ▸ h2)
  have hcount : t.reqs.length ≤ (allPairs r.data).length :=
    nodup_subset_length t.reqs (allPairs r.data) hnod
      (allPairs_nodup r.data) hsub
  have hAP := allPairs_length r.data
  omega

theorem closedRun_round_bound_from_empty {r t : Regime}
    {rds : List Round} (h : ClosedRun r rds t) (he : r.reqs = []) :
    2 * rds.length ≤ r.data * (r.data - 1) := by
  have hb := closedRun_round_bound h
    (he ▸ List.Pairwise.nil)
    (fun q hq => absurd hq (he ▸ fun h => nomatch h))
  rw [he] at hb
  simp only [List.length_nil, Nat.zero_add] at hb
  exact hb
```

The book's Lean builds a one-round closed run from two bare data, reads
Genesis's theorems off it, derives the round caps for two and three data,
and shows the two side conditions doing work.

```lean
-- Lean (book), textbook/checks/u34_lean.py
def bare2 : Regime := ⟨2, [], [], [], []⟩

theorem one_round : respond bare2 0 1 deltaU0 = some U0 := by decide
theorem one_round_fresh : (0, 1) ∉ bare2.reqs := by decide
theorem one_round_no_datum : Item.newDatum ∉ deltaU0 := by decide

theorem run1 : ClosedRun bare2 [⟨(0, 1), deltaU0⟩] U0 :=
  ClosedRun.cons bare2 ⟨(0, 1), deltaU0⟩ U0 U0 [] one_round_fresh one_round_no_datum
    one_round (ClosedRun.nil U0)

theorem one_round_grows : U0.reqs.length = bare2.reqs.length + 1 :=
  round_reqs_succ one_round_fresh one_round

theorem two_data_one_round {rds : List Round} {t : Regime}
    (h : ClosedRun bare2 rds t) : rds.length ≤ 1 := by
  have hb := closedRun_round_bound_from_empty h rfl
  have h2 : bare2.data = 2 := rfl
  rw [h2] at hb
  omega

theorem three_data_three_rounds {rds : List Round} {t : Regime}
    (h : ClosedRun ⟨3, [], [], [], []⟩ rds t) : rds.length ≤ 3 := by
  have hb := closedRun_round_bound_from_empty h rfl
  have h3 : (⟨3, [], [], [], []⟩ : Regime).data = 3 := rfl
  rw [h3] at hb
  omega

theorem R2L_target_not_fresh : (0, 1) ∈ R2L.reqs := by decide

theorem datum_round_moves_data :
    respond bare2 0 1 [.newDatum, .newForm 1, .newInst 0 [0]]
      = some ⟨3, [1], [(0, [0])], [], [(0, 1)]⟩ := by decide
```

## Line-by-line Lean explanation

**`ClosedRun`.** Two constructors. `nil`: any regime is the end of the
empty run from itself. `cons`: given a regime, a round, the regime after
the round (`mid`), the final regime and the rest of the rounds, four
facts build a run: the target is not among the standing demands; the
response has no `newDatum`; `respond` succeeds and lands on `mid`; and
`mid` runs on to `t`. The first two are the declared shape.

**`respond_anatomy`** (lines 355-378, not reproduced): from `respond r i j
δ = some s` it extracts `i < j`, `j < r.data`, `s.reqs = insertNew r.reqs
(i, j)` and the application of `δ` to the imposed regime. Its proof
splits on the impose guard: if the guard holds, `stepE` is the record
update and `applyDelta_reqs` says a delta never touches `reqs`; if not,
`respond` is `none`, contradiction.

**`round_reqs_succ`.** Take the third fact of the anatomy, `hreqs`.
Rewrite `insertNew r.reqs (i, j)` with `insertNew_of_not_mem hfresh`: the
target is new, so the insertion is an append; `List.length_append` and
`rfl` finish. Without freshness, `insertNew` returns the list unchanged
and the count does not grow; that is why the hypothesis is there.

**`round_data_eq`.** Take the fourth fact, the application to the
imposed regime, and feed it to `applyDelta_data_eq`, which by induction
on the delta shows that items other than `newDatum` leave `data` alone
(`applyItem_data_eq` reads each constructor's update). The imposition
itself does not change `data`.

**`closedRun_round_bound`.** Four run-level facts, each by induction on
the run: the final demand count is the start's plus the number of rounds
(`closedRun_reqs_length`, from `round_reqs_succ`); the datum count is the
start's (`closedRun_data_eq`, from `round_data_eq`); duplicate-freeness
is kept (fresh insertion appends a new element); every final demand is
ordered and below the datum count (`closedRun_reqs_wf`, using the
anatomy's `i < j < data` for the new demand). Then: every final demand is
in `allPairs r.data` (`mem_allPairs`, the converse of the bound lemma);
`nodup_subset_length` bounds the length by the length of `allPairs`;
`allPairs_length` is `2 * length = n * (n - 1)`; `omega` assembles the
inequality.

**`closedRun_round_bound_from_empty`.** The paper's form. With `r.reqs =
[]`, the nodup and wf hypotheses hold vacuously (`List.Pairwise.nil`, and
no `q` is a member), the demand count at the start is 0, and the
statement is `2 * rounds ≤ n * (n - 1)`.

**The book's `run1`.** `respond bare2 0 1 deltaU0` is decided to be
`some U0`: imposing `(0, 1)` on the bare regime and admitting the mark
gives exactly Unit 21's `U0`, demand included. The two side conditions
are decided on the concrete lists. `ClosedRun.cons` with `mid := U0`, `t
:= U0` and the empty rest is a run of one round. `one_round_grows` is
Genesis's theorem at it: `1 = 0 + 1`.

**`two_data_one_round`, `three_data_three_rounds`.** Genesis's bound at a
concrete start, with the datum count rewritten to its value and `omega`
reading `2 * len ≤ 2` and `2 * len ≤ 6`. These are the caps Unit 28's
check saw as the deepest rounds of the two closed baselines, 1 and 3.

**`R2L_target_not_fresh`, `datum_round_moves_data`.** The two side
conditions failing. `R2L` already carries `(0, 1)` (Challenge 3 is
imposed in it), so a round at `(0, 1)` from `R2L` is not fresh: its
`insertNew` would be the identity and the count would not grow. And a
response that begins by admitting a datum lands on a regime with 3 data:
`respond` performs it, and it is not a closed round.

**Axioms.** `respond_anatomy`, `round_reqs_succ`, `round_data_eq` report
`propext`: rewrites and case splits. The run bounds report `propext,
Quot.sound`, through `omega` and the list lemmas. The book's decided
instances follow the same split.

## What has been proved

- One round, under freshness, grows the demand count by exactly one
  (Genesis, derived).
- One round, under no fresh datum, keeps the datum count (Genesis,
  derived).
- A closed run from an ordered, bounded, duplicate-free demand store
  preserves those properties. From an empty store it makes at most
  `n(n-1)/2` rounds (Genesis, derived over `ClosedRun`). The general bound
  also counts the demands already present at the start.
- The counting goes through `allPairs` with choice-free list lemmas
  (Genesis; the whole module avoids `Classical.choice`).
- A concrete one-round closed run on two data, and the caps 1 and 3 for
  two and three data (book Lean). A second example satisfies `ClosedRun`
  while leaving its demand unmet: validity is not a constructor field.

## What has not been proved

- That the engine's rounds have the declared shape. `ClosedRun`'s two
  side conditions are hypotheses. The module header says what deriving
  them would take: formalizing collapsed-pair selection and acceptance.
  The check and `test_no_supply_variant_terminates_within_pair_bound`
  verify the shape on the exported runs; `claims.json:CL-CLOSURE-TERMINATION`
  records `within_bound = true`.
- A bound for runs admitting new data. Their possible demand pairs can
  grow beyond the initial ceiling. The paper's main trees with supply run
  to the declared cap of 15; that finite observation does not prove an
  infinite execution.
- That the bound is attained. It is attained in both baselines (1 of 1,
  3 of 3), but `ClosedRun` admits runs that stop early, and the theorem
  is an upper bound only.
- Existence of a run of every length allowed by the bound. The empty run
  and `run1` are explicit inhabitants; the theorem is an upper bound, not
  an existence or maximal-length theorem.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `inductive ClosedRun … : Prop` | the run shape | metatheory; a declared relation |
| `List.Nodup`, `List.Pairwise`, `List.filter` | the counting | metatheory; the choice-free routes |
| `omega` | assembling the inequality | metatheory arithmetic |
| `decide` on `respond` | the book run | metatheory; derived `DecidableEq` |
| `propext`, `Quot.sound` | inherited | inside the declared boundary |

**What the system holds.** The regime at each round; after a round, one
more demand. A "run" is a metatheoretic list of rounds; the regime has no
memory of how many rounds it has been through except through its demand
list, which is why the count is readable from the demands.

**Phrases to read with care.**

- "The engine terminates" is proved for the closed system *under the
  declared shape*, and observed for the exported runs. With supply, no
  such theorem exists.
- "Each round adds one demand" is true when the target is fresh. The
  engine asserts it; `insertNew` would silently absorb a repeat.
- "n(n-1)/2" is written `2 * rounds ≤ n * (n - 1)` to avoid division in
  the proof. Unit 28 derives the divided form from the exact multiplicative
  count; a separately supplied parity theorem is not compulsory.

## Student exercise

`round_reqs_succ` uses `insertNew_of_not_mem`, and `closedRun_reqs_nodup`
keeps the demands duplicate-free. Suppose the freshness hypothesis were
dropped from `ClosedRun.cons`. Which of the four run-level facts
(`closedRun_reqs_length`, `closedRun_data_eq`, `closedRun_reqs_nodup`,
`closedRun_reqs_wf`) would survive, and would the final bound still be
true?

## Answer

<details>
<summary>Worked answer</summary>

`closedRun_data_eq` and `closedRun_reqs_wf` would survive: the datum
count never depended on freshness, and a repeated demand is still
ordered and bounded. `closedRun_reqs_nodup` would survive too, for a
different reason: `insertNew` never inserts a duplicate, so the list
stays duplicate-free whether or not the target was fresh. What fails is
`closedRun_reqs_length`: a repeated target adds no demand, so the final
count is at most, not exactly, the start's plus the rounds. The
inequality `2 * rounds ≤ n(n-1)` would then be *false*, because a run
could repeat the same target forever without the demand list growing.
Freshness is what turns "the demands are bounded" into "the rounds are
bounded".

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Rounds.lean` lines 145-167, 190-220, 264-281, 283-299, 301-354, 355-395, 398-450, 452-481 |
| Axiom report | `artifacts/lean_axioms.txt`: `respond_anatomy`, `round_reqs_succ`, `round_data_eq`, `closedRun_data_eq`, `closedRun_reqs_nodup`, `closedRun_reqs_wf` `[propext]`; `closedRun_reqs_length`, `closedRun_round_bound`, `closedRun_round_bound_from_empty`, `nodup_subset_length`, `allPairs_nodup` `[propext, Quot.sound]` |
| Paper | `paper/paper.md` §9 (**[theorem, under the declared round shape]**, with the **[finite computation]** residual named) and §12 residual R8 (discharged 2026-08-18); ledger `CL-CLOSURE-TERMINATION` |
| Artifact | `artifacts/claims.json`, `CL-CLOSURE-TERMINATION.{L,F}`: `pair_bound` 1 and 3, `rounds_used` 1 and 3, `within_bound = true` |
| Tests | `tests/test_engine.py::test_no_supply_variant_terminates_within_pair_bound`, `::test_closed_system_terminal_at_round_boundary` |
| Check (Python) | `python textbook/checks/u34_rounds.py`: the one-round anatomy on two bare data; a datum-admitting response moves the count; every creation edge of both closed baselines (3 and 19) is fresh, datum-fixed, ordered and duplicate-free; deepest rounds 1 and 3 within `n(n-1)/2` |
| Check (book Lean) | `python textbook/checks/u34_lean.py`: thirteen book theorems plus four Genesis theorems kernel-checked, Lean 4.33.0 |
