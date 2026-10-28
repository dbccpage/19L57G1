# Unit 55. The first graph is supplied, its observer is created

**Claim.** In the declared growth driver, supplied events admit occurrences and edges and explicitly attempt a chosen observation column. The guards and round theorems verify the column's execution and resolution. Higher-cell and boundary conventions are separate admissions.

**Status:** FROZEN (the round schema and `graphAt_spec`, horizon-free);
ADMITTED (the driver, the cell calculus, the boundary conventions:
declared content); VERIFIED_FINITE (`k4`, the alternating statistic, the
cut census on carriers 2 to 4, mirrored growth to 15 rounds); OPEN (the
ladder at every dimension as a two-rule statement; see Unit 60).
**Lean:** `lean4/Derivation/HigherStructure.lean` lines 61-815, imports
`PrimitivePassage`. **Axioms:** 37 exported reports; `grow_len`
`propext` only, `round_creation_record` none, the rest `propext,
Quot.sound`. **Depends on:** Unit 54 (`PState`, `step`, `replayP`,
`obstP`, `extension_always_available`, `two_rule`), Unit 03 (replay).

## First pass

Follow one round before considering the whole run. The driver supplies an occurrence and an edge, retains and protects the pair, and supplies the required budget.

The driver also supplies the final `addCol` event. Its funded, licensed execution resolves the obstruction. The induction describes repetitions of this supplied growth pattern; it does not derive the driver, its column choice, or graph edges from the obstruction alone.

## Detailed claim and formal anchors

`HigherStructure` runs Unit 54's round forever and says
exactly what each round creates.

A *growth driver* `growBlock k` feeds
the passage one occurrence, one asserted and retained difference, one
protection and one unit of budget per round; `graphAt_spec` proves by
induction that the state after round `k + 1` is exactly `pathState k`,
the path graph on `k + 2` occurrences with every edge protected and one
observation column per edge.

Inside every round the new pair is
obstructed (`round_obstruction`), the singleton column is proposed
(`round_two_rule`) and executing it lands on the next characterised
state (`round_resolution`); the last event of every round is that
`addCol` (`round_creation_record`); quiescence is restored
(`graphAt_quiescent`); the counts grow by one each
(`graph_growth`).

The *driver* supplies the occurrence, pair-record, protection, budget,
and chosen column events. The obstruction supplies the condition under
which the chosen column qualifies; the step function checks the other
guards and executes the supplied event. It does not choose or issue
`addCol` by itself.

Above dimension
one nothing is forced: a declared cell calculus `cstep` admits a
triangle only over three present edges and a solid cell only over four
present triangles (`ladder_dim2`, `ladder_dim3`), refuses otherwise
(`shell_guard_load_bearing`), and never fills a shell by itself
(`filling_not_forced`); the four-occurrence demonstration `k4` is built
in creation order with its edges equal to the passage's witness store
(`k4_builds`, `k4_skeleton_agrees`); the declared integer boundary
composes to zero on its cells (`d2_zero_triangles`, `d2_zero_tet`), and
so does a second, different convention (`boundary_not_forced`).

## Question

Unit 54 gives a repair-or-extension family under its stated hypotheses,
without selecting a unique response. What happens
when the response is taken and the machine is fed again, and again? What
is created each time, and by whom: the thing that feeds the machine, or
the obstruction itself? And once the first graph is there, is anything
above it, a surface spanning three edges, a solid spanning four
surfaces, forced by the same process?

## What we already possess

- The passage state with its nine stores and the guarded `step`;
  `replayP h genesisP = h.foldl step genesisP` (Unit 54).
- `obstP` and its four gates; `extension_always_available`: at an
  obstruction on an in-range protected pair `(i, j)`, the singleton
  column `[i]` is a proposal; `two_rule` (Unit 54).
- `addCol c` executes only when `colOk`, licensed and funded, and then
  `extension_resolves` (Unit 54).

## New concept: a driver, a characterised stage, a cell calculus

A *driver* is a function from a round number to a block of events. It is
declared, not derived: it says what the environment supplies each round.
`growHist k` is the concatenation of the first `k + 1` blocks, and
`graphAt k` replays it from genesis.

A *characterised stage* is a state written out in closed form,
`pathState k`, against which the replayed state is proved equal. The
proof is an induction on `k`: the base case is `decide` on a small
state, the step case walks the six events of `growBlock (m + 2)` through
named intermediate states `g1 m`, `gA m`, `g2 m`, `g3 m`, `preCol m`,
each with its guard discharged.

A *cell calculus* is a second machine with its own state `Complex`, four
lists `c0, c1, c2, c3`, and its own step `cstep`. Its guards are the
*shells*: `shell1` needs both endpoints present and the edge absent;
`shell2` needs all three edges present and the triangle absent; `shell3`
needs all four triangles present and the solid cell absent. A shell is
a complete unfilled boundary. It is deliberately not a boundary with one
face missing; the ledger says so, and the book's checks show that a
boundary one face short is refused.

A *boundary convention* is a declared assignment of signed faces to each
cell, `bd1`, `bd2`, `bd3`, with `push1`, `push2` applying it to a signed
list of cells. "The composite vanishes" means that pushing a cell's
boundary down twice gives coefficient zero at every vertex or edge.

## Plain-language interpretation

Imagine a clerk who every morning brings one new item, declares it
different from yesterday's, insists the difference be kept, and leaves
one budget unit in the state. The new
pair is retained, protected, and the observation it already has cannot
tell the new item from yesterday's, so the pair is obstructed. The
chosen singleton qualifies as a fresh-column proposal. The driver
explicitly supplies its column event, the budget funds it, the column is
added under the guards, and the obstruction is gone. The theorem
`graphAt_spec` says that after `k + 1` mornings the room holds exactly:
items `0` to `k + 1`, a kept difference between each item and the next,
a demand on each, and one column per difference. That is a path, drawn
as a graph: items are points, kept differences are edges.

The provenance matters. The clerk brought the points and the edges. The
guarded execution admitted the driver's chosen columns. The paper uses
the shorthand:
driver creates graph structure, the obstruction creates observation
structure. Here that shorthand means guarded execution of a column event
that the driver explicitly supplies; an obstruction does not choose or
execute that event by itself. Nothing in the machine conjures an edge; a driver in which
edges themselves arise from obstructions is recorded as a conjecture,
not a result (Unit 63).

Above the graph, the module changes machines. A second calculus admits a
triangle only when its three edges are all present and the triangle is
not, and a solid cell only when its four triangles are present. The four
items `0` to `3`, with all six edges fed through the passage, give a
graph whose edges are exactly what the cell calculus then fills, in
order: four triangles, then one solid cell. Two things are proved about
this. First, when the shell is there the admission really adds the cell
and really changes the complex. Second, the shell does not fill itself:
after the four triangles, the solid cell's shell is complete and the
solid list is empty, until someone declares the fill. Higher structure
is admitted, not forced.

The last part is a declared bookkeeping of signs. Each edge is read as
"end minus start", each triangle as a signed sum of its three edges,
each solid cell as a signed sum of its four triangles. With these signs,
boundary of boundary is zero on every cell of the demonstration. The
module also shows a second sign convention with the same property. So
the vanishing is a fact about the declared signs, not something the
graph forced.

## Pseudocode

```
growBlock(0)   := [admitOcc 0]
growBlock(1)   := [admitOcc 1, assertWit 0 1, admitWit 0 1, protect 0 1,
                   declareObs, setBudget 1, addCol [0]]
growBlock(k+2) := [admitOcc (k+2), assertWit (k+1) (k+2), admitWit (k+1) (k+2),
                   protect (k+1) (k+2), setBudget 1, addCol [k+1]]
graphAt(k) := replay(growBlock(0) ++ ... ++ growBlock(k))

pathState(k) := occ 0..k+1; asserted = wit = prot = [(i, i+1) for i ≤ k];
                obs = [[i] for i ≤ k]; budget 0; licensed; no refusals; live

claim: graphAt(k+1) = pathState(k)        for every k      (induction)

cstep(C, addE i j)     := if shell1 C i j     then C with edge (i,j)     else C
cstep(C, addT i j k)   := if shell2 C i j k   then C with triangle       else C
cstep(C, addQ i j k l) := if shell3 C i j k l then C with solid cell     else C
shell2 C i j k := edges (i,j), (j,k), (i,k) all in C and (i,j,k) not in C
```

## Python

Genesis's mirror of the driver, `code/derivation/primitive_passage.py`:

```python
def grow_block(k: int) -> list[PEvent]:
    if k == 0:
        return [("admitOcc", 0)]
    if k == 1:
        return [("admitOcc", 1), ("assertWit", 0, 1),
                ("admitWit", 0, 1), ("protect", 0, 1),
                ("declareObs",), ("setBudget", 1), ("addCol", (0,))]
    return [("admitOcc", k), ("assertWit", k - 1, k),
            ("admitWit", k - 1, k), ("protect", k - 1, k),
            ("setBudget", 1), ("addCol", (k - 1,))]


def graph_at(k: int) -> PS:
    return preplay(grow_hist(k), GENESIS_P)
```

The cell calculus, `code/derivation/higher_structure.py`:

```python
def shell2(cx: Complex, i: int, j: int, k: int) -> bool:
    return ((i, j) in cx.c1 and (j, k) in cx.c1 and (i, k) in cx.c1
            and (i, j, k) not in cx.c2)
```

The book's check, `textbook/checks/u55_higher_structure.py`, round by
round:

```python
    for k in range(ROUNDS):
        g = graph_at(k + 1)
        spec = path_state(k)
        pre = preplay(grow_block(k + 2)[:5], spec)  # up to setBudget 1
        obstructed = obst_p(pre, k + 1, k + 2)
        ext = (k + 1,) in extension_proposals(pre, k + 1, k + 2)
        lands = pstep(pre, ("addCol", (k + 1,))) == path_state(k + 1)
        quiet = all(not obst_p(g, r[0], r[1]) for r in g.prot)
```

and, Python (book), the one-face-short boundaries:

```python
    horn1 = Complex(c0=(0,))                       # one endpoint absent
    horn2 = Complex(c0=(0, 1, 2), c1=((0, 1), (1, 2)))  # edge (0,2) absent
    horn3 = creplay(k4_events()[:13], EMPTY_COMPLEX)  # triangle (1,2,3) absent
    refused = (cstep(horn1, ("addE", 0, 1)) == horn1
               and cstep(horn2, ("addT", 0, 1, 2)) == horn2
               and cstep(horn3, ("addQ", 0, 1, 2, 3)) == horn3)
```

## Line-by-line Python explanation

- `grow_block(0)`: one event, the first occurrence. There is nothing to
  assert yet.
- `grow_block(1)`: the second occurrence, the first assertion `(0, 1)`,
  its retention, its protection, the declaration of an observation
  (`some []`, empty), one coin, and the first column `[0]`. This is the
  only block with `declareObs`; after it the observation exists for
  good.
- `grow_block(k)` for `k ≥ 2`: the same pattern on the pair `(k - 1,
  k)`, with no declaration. The column added is `(k - 1,)`, the
  singleton on the earlier endpoint, which is what Unit 54's
  `extension_always_available` promises for the pair `(k - 1, k)`.
- `graph_at(k)`: replay of all blocks up to `k` from genesis.
- `shell2`: three memberships and one non-membership. The triple must
  be oriented as the three edges `(i, j)`, `(j, k)`, `(i, k)` are
  stored; `(k, i)` would not do. Nothing here consults the passage
  state: the two machines share nothing but the lists a reader copies
  from one to the other.
- The check's loop: `pre` is the state five events into block `k + 2`,
  after the coin and before the column, which is Lean's `preCol k`.
  Three facts are evaluated there, obstruction, proposal, landing, and
  two at the end of the round, equality with the spec and quiescence.
  Fifteen rounds are run because the artifact records fifteen; the
  Lean theorem has no such bound.
- `horn1`, `horn2`, `horn3`: for each dimension, a boundary with one
  face missing. The step returns the complex unchanged in each case.
  This is what "shell, not horn" means operationally, and it is Python
  (book): Genesis proves only `shell_guard_load_bearing`, the
  dimension-2 case over one edge.

## Lean 4

The driver and the characterised stage
(`lean4/Derivation/HigherStructure.lean` lines 72-97):

```lean
def growBlock : Nat → List PEvent
  | 0 => [.admitOcc 0]
  | 1 => [.admitOcc 1, .assertWit 0 1, .admitWit 0 1, .protect 0 1,
          .declareObs, .setBudget 1, .addCol [0]]
  | k + 2 => [.admitOcc (k + 2), .assertWit (k + 1) (k + 2),
              .admitWit (k + 1) (k + 2), .protect (k + 1) (k + 2),
              .setBudget 1, .addCol [k + 1]]

def growHist : Nat → List PEvent
  | 0 => growBlock 0
  | k + 1 => growHist k ++ growBlock (k + 1)

def graphAt (k : Nat) : PState := replayP (growHist k) genesisP

def pathState (k : Nat) : PState :=
  { occ := List.range (k + 2),
    asserted := (List.range (k + 1)).map (fun i => (i, i + 1)),
    wit := (List.range (k + 1)).map (fun i => (i, i + 1)),
    prot := (List.range (k + 1)).map (fun i => (i, i + 1)),
    obs := some ((List.range (k + 1)).map (fun i => [i])),
    budget := 0, licensed := true, refusals := [], halted := false }
```

The round, as three theorems (lines 381-420, abridged), and the
induction (476-479):

```lean
theorem round_obstruction (m : Nat) :
    obstP (preCol m) (m + 1) (m + 2) = true := by
  rw [obst_agrees_when_declared (preCol m)
      ((List.range (m + 1)).map (fun i => [i])) rfl]
  simp only [preCol, Bool.and_eq_true]
  exact ⟨⟨decide_eq_true
      (List.mem_append.mpr (Or.inr List.mem_cons_self)),
    decide_eq_true
      (List.mem_append.mpr (Or.inr List.mem_cons_self))⟩,
    grow_zero m⟩

theorem round_two_rule (m : Nat) :
    [m + 1] ∈ extensionProposals (preCol m) (m + 1) (m + 2) := by
  apply extension_always_available (preCol m) (m + 1) (m + 2)
    (round_obstruction m) (by omega)
  · show m + 1 < (List.range (m + 2) ++ [m + 2]).length
    rw [grow_len]
    omega
  · exact List.mem_append.mpr (Or.inr List.mem_cons_self)

theorem round_resolution (m : Nat) :
    step (preCol m) (.addCol [m + 1]) = pathState (m + 1) := by
  have hcolok : colOk (preCol m) [m + 1] = true := by
    ...

theorem graphAt_spec (k : Nat) : graphAt (k + 1) = pathState k := by
  induction k with
  | zero => decide
  | succ m ih =>
      show replayP (growHist (m + 1) ++ growBlock (m + 2)) genesisP
        = pathState (m + 1)
      ...
```

The cell calculus and the ladder at dimension 2 (lines 574-607, 616-633):

```lean
def shell2 (C : Complex) (i j k : Nat) : Bool :=
  edgeIn C i j && edgeIn C j k && edgeIn C i k
    && !(decide ((i, j, k) ∈ C.c2))

def cstep (C : Complex) : CEvent → Complex
  | .addV v => if v ∈ C.c0 then C else { C with c0 := C.c0 ++ [v] }
  | .addE i j =>
      if shell1 C i j then { C with c1 := C.c1 ++ [(i, j)] } else C
  | .addT i j k =>
      if shell2 C i j k then { C with c2 := C.c2 ++ [(i, j, k)] }
      else C
  | .addQ i j k l =>
      if shell3 C i j k l then
        { C with c3 := C.c3 ++ [(i, j, k, l)] }
      else C

theorem ladder_dim2 (C : Complex) (i j k : Nat)
    (h : shell2 C i j k = true) :
    (i, j, k) ∈ (cstep C (.addT i j k)).c2 ∧
      cstep C (.addT i j k) ≠ C := by
  have hstep : cstep C (.addT i j k)
      = { C with c2 := C.c2 ++ [(i, j, k)] } := by
    simp only [cstep]
    rw [if_pos h]
  rw [hstep]
  constructor
  · exact List.mem_append.mpr (Or.inr List.mem_cons_self)
  · intro heq
    have hlen := congrArg (fun D => D.c2.length) heq
    simp only [List.length_append, List.length_cons,
      List.length_nil] at hlen
    omega
```

Lean (book), from `textbook/checks/u55_lean.py`: round 3 by schema and
by value, the shell one face short, and audit finding 1 made visible.

```lean
theorem round_three_values :
    obstP (preCol 1) 2 3 = true ∧
    extensionProposals (preCol 1) 2 3 = [[2], [3]] ∧
    step (preCol 1) (.addCol [2]) = pathState 2 := by
  decide

theorem budget_gates_round :
    obstP (g3 1) 2 3 = true ∧ step (g3 1) (.addCol [2]) = g3 1 := by
  decide

theorem horn_two_refused :
    cstep ⟨[0, 1, 2], [(0, 1), (1, 2)], [], []⟩ (.addT 0 1 2)
      = ⟨[0, 1, 2], [(0, 1), (1, 2)], [], []⟩ := by
  decide

theorem altNum_not_invariant :
    altNum (creplay (k4Events.take 4) emptyComplex) ≠ altNum (creplay (k4Events.take 10) emptyComplex) ∧
    altNum (cstep k4 (.addV 4)) = 2 := by
  decide
```

## Line-by-line Lean explanation

- `def growBlock : Nat → List PEvent | 0 => … | 1 => … | k + 2 => …`:
  a function by cases on the round number. The three cases are not
  symmetric: round 0 has one event, round 1 seven, every later round
  six. The asymmetry is the one-time declaration of the observation.
- `def growHist … | k + 1 => growHist k ++ growBlock (k + 1)`: the
  history is built by appending; `replay_append` from Unit 54 is what
  lets the induction step replay one block from the previous stage.
- `def pathState (k : Nat) : PState := { occ := List.range (k + 2), …
  }`: `List.range n` is `[0, …, n - 1]`; the four pair-lists are the
  same list of consecutive pairs, mapped from `List.range (k + 1)`; the
  observation is one singleton column per edge; budget `0` because the
  coin of each round was spent.
- `theorem round_obstruction … rw [obst_agrees_when_declared …]`: the
  proof first replaces `obstP` by the rival policy `obstEmptyObs` of
  Unit 54, which is allowed because an observation is declared
  (`rfl` for the `some` hypothesis), and which has a simpler shape to
  split. Then `simp only [preCol, Bool.and_eq_true]` turns the Boolean
  conjunction into a conjunction of propositions.
- `exact ⟨⟨decide_eq_true (List.mem_append.mpr (Or.inr
  List.mem_cons_self)), …⟩, grow_zero m⟩`: the pair `(m + 1, m + 2)`
  is in `wit` and in `prot` because each is `… ++ [(m + 1, m + 2)]`,
  membership in the right summand, head of a singleton. `grow_zero m`
  is the lemma that the `m + 1` singleton columns `[0], …, [m]` do not
  separate `m + 1` from `m + 2`: neither position is in any of them.
- `theorem round_two_rule … apply extension_always_available … (by
  omega)`: Unit 54's lemma needs `i ≠ j`, `i < occ.length` and `(i, j)
  ∈ prot`. `omega` proves `m + 1 ≠ m + 2`; the length goal is rewritten
  with `grow_len`, which says the occurrence list has length `m + 3`,
  and `omega` again; the protection goal is the same membership as
  before. So the round's proposal is Unit 54's theorem with its
  hypotheses discharged, nothing more.
- `theorem round_resolution … have hcolok : colOk (preCol m) [m + 1] =
  true`: the body (lines 406-467) discharges `colOk` by showing `[m +
  1]` is in range, not yet a column, and separates an obstructed
  protected pair; then the `step` guard holds and the resulting record
  is `pathState (m + 1)` field by field. It is long because every
  `decide` on a symbolic `m` has to be replaced by a lemma.
- `theorem graphAt_spec … induction k with | zero => decide | succ m ih
  => …`: the base case is a closed computation on stage 1. The step
  case rewrites `growHist (m + 2)` as `growHist (m + 1) ++ growBlock (m
  + 2)`, uses `ih` to replace the replay of the first part by `pathState
  m`, and walks the six events through `g1`, `gA`, `g2`, `g3`,
  `preCol` and `round_resolution`.
- `def cstep … | .addT i j k => if shell2 C i j k then { C with c2 :=
  … } else C`: the guard is the whole content. The `else C` branch is
  `shell_guard_load_bearing` and the book's `horn_two_refused`.
- `theorem ladder_dim2 … (h : shell2 C i j k = true)`: one hypothesis,
  the shell. `have hstep … rw [if_pos h]` evaluates the `if`. The first
  conjunct is membership at the end of the appended list; the second,
  `cstep C … ≠ C`, is proved by comparing lengths: if the complexes were
  equal their `c2` lengths would be, but one is the other plus one,
  which `omega` refuses. This is all the theorem says: under the shell,
  the step appends the cell and the complex is strictly larger.
- Book `round_three_values`: the schema at `m = 1`, as values. The
  extension list is `[[2], [3]]`, both singletons over the new pair;
  Genesis's `round_two_rule` names only `[2]`.
- Book `budget_gates_round`: at `g3 1`, before the coin, the pair is
  already obstructed and `addCol [2]` is inert. The budget gates the
  resolution; it is not one of the obstruction's four gates.
- Book `altNum_not_invariant`: the alternating count differs between
  two stages of one growth, and admitting a fifth vertex to the
  finished `k4` moves it from `1` to `2`. This is audit finding 1 as a
  declaration: the docstring's "stage-invariant" is not a theorem.

## What has been proved

- `graphAt_spec` (line 476): for every `k`, `graphAt (k + 1) = pathState
  k`. Horizon-free: the quantifier over `k` is the metatheory's, each
  stage a finite state.
- `round_obstruction` (381), `round_two_rule` (395), `round_resolution`
  (406), `round_creation_record` (469): inside every round `m + 2`, the
  pair `(m + 1, m + 2)` is obstructed at `preCol m`, `[m + 1]` is
  proposed, executing it lands on `pathState (m + 1)`, and the block's
  last event is that `addCol`.
- `graph_growth` (495): `k + 2` occurrences and `k + 1` edges at stage
  `k + 1`. `graphAt_quiescent` (510): no protected pair is obstructed
  at any stage. `path_connectivity_residue` (536): occurrences minus
  edges is `1`.
- The guard lemmas `grow_fresh`, `grow_wit_not_mem`, `grow_col_not_mem`,
  `grow_cols_blind`, `grow_col_separates`, `grow_pair_separated`,
  `grow_zero` (101-183) and `pstep_*`, `colOk_some`, `*_guard`,
  `reach_preCol` (187-379): the facts the induction step needs, each
  about one guard of one event.
- `ladder_dim2` (616), `ladder_dim3` (635): under a complete unfilled
  boundary the admission appends the filling cell and strictly extends
  the complex. `shell_guard_load_bearing` (654): over one edge of
  three, `addT` is inert. `filling_not_forced` (714): at `k4Boundary`
  the solid cell's shell is complete and `c3` is empty.
- `k4_skeleton_from_passage` (672), `k4_builds` (699),
  `k4_skeleton_agrees` (708): the passage accepts the six edges of the
  four-occurrence graph, all protected, all separated; the declared log
  builds exactly the listed cells; the complex's edges are the passage's
  witness store.
- `altNum_stages` (730): the values `4, -2, 2, 1` at the four stages.
  `cut_census_growth` (752): `1, 2, 4` on carriers `2, 3, 4`.
- `d2_zero_triangles` (796), `d2_zero_tet` (801), `boundary_not_forced`
  (808): with the declared signs the composite boundary has coefficient
  zero at every vertex of every triangle and at every edge of the solid
  cell; `bd2'` differs from `bd2` and has the same property.

## What has not been proved

- That the graph was forced. The driver supplies every occurrence,
  assertion, retention, protection, budget, and chosen column event by
  declaration. The obstruction establishes eligibility of an extension
  under the stated hypotheses; it does not select a unique column or
  cause an event to occur. The paper's line "the driver creates graph
  structure; the obstruction creates observation structure" is shorthand
  for the declared driver and its guarded execution, not an autonomy theorem.
- Audit finding 1. The module docstring calls `altNum` "a
  stage-invariant of the growth" which "the declared boundary calculus
  turns into" an invariant. No theorem relates `altNum` to the boundary
  calculus, and its values along the stages are `4, -2, 2, 1`. The
  ledger entry `CL-PD2-LADDER` already corrects this to "a statistic,
  not an invariant". The book's `altNum_not_invariant` shows the values
  differ and that admitting one vertex moves it.
- Audit finding 2. `ladder_dim2` and `ladder_dim3` are statements about
  the declared `cstep`: under the shell, the `if` takes its `then`
  branch. The docstring reads the shell as "the dimension-2 obstruction"
  and the step as "the two-rule shape, one dimension up". No theorem
  connects `shell2` to `obstP`, `prot`, or any passage store; the
  analogy is declared. The paper's map (section 5) now says the same:
  what is proved at every dimension, in Unit 60's `LadderGeneral`, is
  the uniform guarded filler, "a statement about the declared guarded
  step and nothing more".
- Audit finding 3, a finitude flag. "The first graph grows without
  bound" (`graph_growth`) is `∀ k, …` over `Nat`. The system never holds
  the family of stages; each `graphAt k` is one finite state, and the
  quantifier is the reader's.
- Audit finding 4. `cut_census_growth` states three values. The
  docstring's "the branching is real and grows with the carrier" is a
  reading of three numbers; the ledger scopes it to carriers 2 to 4 and
  the artifact adds carrier 5. The book's `cut_census_five` states the
  fourth value; no growth law is proved.
- Audit finding 5. "A witnessed binary relation *is* a directed graph
  presentation, identity rather than force" (docstring, paper section
  3) has no Lean statement. It is a reading of the field `wit : List
  (Nat × Nat)` as an edge list. The lesson uses that reading in prose
  and marks it as a reading.
- `path_connectivity_residue` is a corollary of `graph_growth` and proves
  neither connectedness nor acyclicity. The book's `residue_blind` shows
  two edge lists on four occurrences with the same residue, one a
  triangle with an isolated point and one the same triangle with one
  edge reversed; the residue sees neither the isolated point nor the
  orientation.
- The ladder at every dimension as a two-rule statement remains OPEN;
  the ledger calls it a frontier conjecture.

## Outside the system

- The two machines, passage and cell calculus, share no state. The
  equality `k4.c1 = (replayP k4PassageHist genesisP).wit` is checked by
  `decide` on two lists that were written to agree; it is the reader's
  transcription of one into the other, verified, not a map the system
  possesses.
- The coin. `setBudget 1` in every block is the declared self-funding
  of the driver. Who funds is outside; that the resolution needs the
  coin is inside (`budget_gates_round`).
- The signs. Integer coefficients, `bd1`, `bd2`, `bd3` and the second
  convention `bd2'` are declarations. The module proves things about
  them; it does not derive them from the graph, and `boundary_not_forced`
  is the record of that.
- `Int` in `altNum` and the boundary calculus is the metatheory's
  integers, used only for finite signed counts.

## Student exercise

Write out `preCol 0` field by field from its definition (line 271 with
`m = 0`), decide which pair is obstructed there and why, list the
extension proposals for that pair, and state what `step (preCol 0)
(.addCol [1])` is. Then say which Genesis theorem each of your three
answers instantiates.

## Answer

`preCol 0`: `occ = [0, 1] ++ [2] = [0, 1, 2]`; `asserted = wit = prot =
[(0, 1)] ++ [(1, 2)] = [(0, 1), (1, 2)]`; `obs = some [[0]]`; `budget =
1`; licensed; no refusals; live.

The pair `(1, 2)` is obstructed: it is retained and protected, an
observation is declared, and the only column `[0]` contains neither
`1` nor `2`, so it does not separate them (`grow_zero 0`). The pair
`(0, 1)` is not obstructed: `[0]` contains `0` and not `1`. This is
`round_obstruction 0`.

Extension proposals for `(1, 2)`: the candidates are `[0]`, `[1]`,
`[2]`. `[0]` is already a column, so `colOk` fails. `[1]` and `[2]` are
in range, new, and each separates `(1, 2)`, an obstructed protected
pair. So the list is `[[1], [2]]`, and `round_two_rule 0` says `[1]` is
in it.

`step (preCol 0) (.addCol [1])`: `colOk` holds, licensed, budget `1 >
0`, so the column is appended and the budget drops: `obs = some [[0],
[1]]`, `budget = 0`, everything else unchanged. That is `pathState 1`,
which is `round_resolution 0`; and `graphAt_spec 1` says the same state
is `graphAt 2`.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/HigherStructure.lean` lines 72-97 (driver, `graphAt`, `pathState`), 101-183 (growth guard facts), 187-243 (step helpers), 248-379 (the stages and their guards), 381-469 (the round), 476-540 (`graphAt_spec`, `graph_growth`, `graphAt_quiescent`, residue), 555-614 (`Complex`, shells, `cstep`, `creplay`), 616-656 (ladder, guard), 664-716 (`k4`), 722-754 (`altNum`, `cutCensus`), 765-813 (boundary calculus) |
| Axiom report | `artifacts/lean_axioms.txt` lines 515-551 |
| Paper | `paper/primitive_difference_map.md` sections 3-6; `paper/paper_claim_ledger.md` `CL-PD2-GROWTH`, `CL-PD2-LADDER` |
| Python | `code/derivation/primitive_passage.py` (`grow_block`, `grow_hist`, `graph_at`, `path_state`, `k4_passage_hist`, `growth_report`), `code/derivation/higher_structure.py` (`Complex`, `shell1/2/3`, `cstep`, `creplay`, `k4_events`, `alt_num`, `cut_census`, `bd1/2/3`, `push1/2`), `code/run_primitive_passage.py` (`cells_report`), `artifacts/primitive_passage.json` (`growth`, `cells`) |
| Audit | `textbook/audit/modules/HigherStructure.md` findings 1-6 |
| Check (Python) | `python textbook/checks/u55_higher_structure.py`: fifteen rounds against `path_state`, the round triple, the K4 skeleton, the cell log, the ladder instances, the one-face-short refusals (Python (book)), the statistic, the census, the boundary calculus, and both reports against the artifact |
| Check (book Lean) | `python textbook/checks/u55_lean.py`: twenty-one book declarations plus twenty Genesis theorems kernel-checked, Lean 4.33.0 |
