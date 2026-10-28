# Unit 54. From an asserted difference to a response

**Claim.** The declared passage machine keeps assertion, retention, protection, observation, and execution distinct. Under the stated obstruction hypotheses it offers repair or extension proposals. Their execution still depends on the relevant guards.

**Status:** FROZEN; ADMITTED (the convention that gate 4 reads `true`
before any observation is declared, `zeroDeclP`, and the policy
`obst_requires_observation` that an undeclared observation obstructs
nothing: both declared, both priced by `obst_policies_differ`);
VERIFIED_FINITE (the arrow report of `artifacts/primitive_passage.json`,
fourteen executable witnesses). **Lean:**
`lean4/Derivation/PrimitivePassage.lean` lines 77-1298, imports
`PrimitiveCore`, `PrimitiveCats`, `PrimitiveContact`. **Axioms:** 56
exported reports, all `propext, Quot.sound` except `wit_independent_of_obs`
and `quotient_no_recovery` (none). **Depends on:** Unit 51 (`Setting`,
reading A, D), Unit 53 (`nativeKernelWitness`), Unit 03 (replay of a
history by `foldl`), Unit 44 (a zero relation as an equivalence).

## First pass

Assert a pair first; retain it separately; then record protection and declare the observer. These steps have different fields and effects.

If a retained protected pair is still merged by the observer, inspect the response family. A structural repair can still be available. Executing an existing-column refinement needs budget; creating a column also needs the license. Both require the machine not to be halted.

## Detailed claim and formal anchors

`PrimitivePassage` replays a difference through a small
machine and proves, store by store, when it becomes an *obstruction* and
what the machine must then offer.

A state `PState` holds nine stores:
occurrences, asserted pairs, retained pairs, protected pairs, an optional
declared observation, a budget, a licence flag, a refusal record and a
halt flag.

A difference is *obstructed* exactly when four gates hold at
once: retained, protected, an observation declared, and that observation
blind to the pair (`obstP_factors`); no three gates entail the fourth
(`gate_zero_independent`, `gate_declared_independent`,
`gate_protection_independent`, `gate_retention_independent`, witnessed by
five named states).

Assertion is not retention
(`assertion_not_retained`), retention needs an assertion
(`retention_requires_assertion`) and persists (`retention_persists`), and
without protection nothing obstructs (`no_protection_no_obstruction`).

At
an obstruction with an in-bounds protected pair the machine never runs
dry: repair the observation at the same level, or create a column
(`two_rule`, via `extension_always_available`).

Listing a proposal spends no budget. Executing a new-column event needs
a licence and a positive budget (`proposal_not_execution`,
`budget_gates_execution`); an existing-column refinement needs a positive
budget but does not consult the licence flag. Both events are inert after
halt. An executed extension clears the obstruction
(`extension_resolves`); a refusal records and moves nothing
(`refusal_object_inert`) while a halt absorbs everything
(`terminal_absorbing`). With no active protected pair the next family is
empty; an active protected pair contributes a block under the stated
off-diagonal and in-range hypotheses (`nextFamilyP_stop`,
`nextFamilyP_nonempty`). A listed block is not a guarantee that its events
will execute under the current licence and halt settings.

## Question

A difference has been asserted between two occurrences. At what point in
a replayed history does it become something the machine must answer, and
when it does, what is the machine forced to put on the table? And which
of those answers are theorems, and which are conventions the author
chose?

## What we already possess

- A `Setting` with a relation `r`, two points `a`, `b`, a retention
  relation `ret` and a protection relation `prot`; reading A, "`r a b`
  and `r` is irreflexive", and the fact that A gives D, the endpoints
  apart (Unit 51).
- `nativeKernelWitness`, the two-point setting the native side commits
  to before contact (Unit 53).
- A history is a list of events; replaying it is `foldl step genesis`,
  so the state after a history is a function of the list and of nothing
  else (Unit 03).
- An observation's zero relation, "the observer cannot tell `x` from
  `y`", and the three laws that make it an equivalence (Unit 44).

## New concept: a store per status, and a gate per store

The machine keeps a difference in *separate stores* according to its
status. A pair that was *asserted* sits in `asserted`. A pair the system
has *retained* as a witness sits in `wit`. A pair on which a *demand* has
been placed, "keep these two apart", sits in `prot`. The observation the
system has *declared* sits in `obs`, which is either `none`, no
observation declared yet, or `some cols`, a list of columns, each column
a list of positions. A column *separates* `i` from `j` when exactly one
of them is in it; the observation is *zero* on `(i, j)` when no column
separates them.

An *obstruction* is the coincidence of four facts about one pair: it is
retained, it is protected, an observation is declared, and that
observation is zero on it. Each fact is one gate, a Boolean function of
the state. The module proves that the obstruction predicate `obstP` is
the conjunction of the four gates, and then, separately, that no three
gates force the fourth over raw state records. This does not say that
every combination is reachable by events: protection requires retention,
which persists. The declared and total-zero gates also share the
observation field and cannot both be false.

A *response* is one of two families: *repair*, which refines an existing
column by one position so that it separates the pair; or *extension*,
which proposes a new column. Proposals are lists; they execute only
through their actual guarded events. A refinement needs budget; adding
a column needs budget and licence; halt blocks both. A *refusal* is
an event that records the pair, with the obstruction as its certificate,
and changes nothing else. A *halt* is an event after which every event is
inert.

## Plain-language interpretation

Think of a filing room with labelled trays. Someone claims two things are
different: the claim goes in the "asserted" tray. Nothing more happens by
itself. Only an explicit act of the system moves a copy to the "retained"
tray, and the act is refused if there was no claim to retain. Another
explicit act places a demand on the retained pair: keep these apart. Then
the system opens its eyes by declaring an observation, which at first
sees nothing at all, an empty list of columns.

Now, and only now, the pair is obstructed: it is retained, a demand sits
on it, an observation is open, and the observation cannot tell the two
apart. Four conditions are required. The module compares raw records
omitting each condition; this is not a demonstration that an event can
remove retention or protection from a state reached from genesis.

Being active does not mean that the existing repair menu is exhausted.
At an active, off-diagonal pair satisfying the source's bounds, the
module supplies the repair-or-extension alternative. The singleton on
the first endpoint qualifies as a new-column proposal; the family can
also retain other singleton proposals. Appending an eligible column
requires an unhalted state, one budget unit, and the licence flag.
Proposing it changes no state. Once the guarded addition executes, the
pair's obstruction is gone on re-evaluation.

Two other answers exist and are kept apart by type. A refusal is a line
in the refusal register that cites the active obstruction; it does not
require repair-menu exhaustion and changes no observation. The active
pair remains until another event resolves it. A halt closes the room: after it, every event,
including a second halt, leaves the state as it is.

Two things in this story are conventions, not theorems, and the module
says so. Before any observation is declared, gate 4 ("the observation is
zero on the pair") is set to read `true`. And a state with no observation
declared is not obstructed, whatever its other trays hold. The rival
policy, reading "no observation yet" as "an empty observation", would
obstruct the same state; `obst_policies_differ` exhibits the one state on
which the two policies disagree. The author chose, and priced the choice.

## Pseudocode

```
state := (occ, asserted, wit, prot, obs, budget, licensed, refusals, halted)

obstructed(state, i, j) :=
    (i,j) in wit  and  (i,j) in prot
    and obs is some cols  and  no column of cols separates i from j

step(state, event) :=
    if event is halt: set halted
    if halted: return state unchanged
    admitOcc t:    append t to occ unless present
    assertWit i j: append (i,j) to asserted if i≠j, both in range, not present
    admitWit i j:  append (i,j) to wit if asserted and not present
    protect i j:   append (i,j) to prot if retained and not present
    declareObs:    obs := some [] if obs was none
    refineCol v p: if refineOk and budget>0: add p to column v, budget-1
    addCol c:      if colOk and licensed and budget>0: append c, budget-1
    refuse i j:    append (i,j) to refusals if obstructed and not present
    setBudget n / setLicense b: set the field

replay(history) := fold step over history from genesis

nextFamily(state) :=
    for each protected pair (i,j) that is obstructed:
        [refineCol v p]            for each repair (v,p) of (i,j)
        [setBudget 1, addCol c]    for each extension c of (i,j)
```

## Python

Genesis's mirror is `code/derivation/primitive_passage.py`. The
obstruction predicate and the retention and protection guards of the step
function, as written there:

```python
def obst_p(s: PS, i: int, j: int) -> bool:
    """Active obstruction: retained, protected, observation DECLARED,
    observer-zero — the four-condition conjunction."""
    if s.obs is None:
        return False
    return ((i, j) in s.wit and (i, j) in s.prot
            and zero_p(s.obs, i, j))
```

```python
    if kind == "admitWit":
        i, j = e[1], e[2]
        assert isinstance(i, int) and isinstance(j, int)
        if (wf_pair(s, i, j) and (i, j) in s.asserted
                and (i, j) not in s.wit):
            return replace(s, wit=s.wit + ((i, j),))
        return s
    if kind == "protect":
        i, j = e[1], e[2]
        assert isinstance(i, int) and isinstance(j, int)
        if (i, j) in s.wit and (i, j) not in s.prot:
            return replace(s, prot=s.prot + ((i, j),))
        return s
```

The book's check, `textbook/checks/u54_primitive_passage.py`, replays the
witnesses through these functions. Its core, the five gate witnesses and
the two-rule at the all-gates state:

```python
BASE = dict(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),), prot=((0, 1),),
            budget=0, licensed=True, refusals=(), halted=False)
GATE_NO_ZERO = PS(obs=((0,),), **BASE)
GATE_NO_DECLARATION = PS(obs=None, **BASE)
GATE_NO_PROTECTION = replace(PS(obs=(), **BASE), prot=())
GATE_NO_RETENTION = replace(PS(obs=(), **BASE), wit=())
GATE_ALL = PS(obs=(), **BASE)


def gates(s: PS, i: int, j: int) -> tuple[bool, bool, bool, bool]:
    return ((i, j) in s.wit, (i, j) in s.prot, s.obs is not None,
            True if s.obs is None else zero_p(s.obs, i, j))

    for s in (GATE_NO_ZERO, GATE_NO_DECLARATION, GATE_NO_PROTECTION,
              GATE_NO_RETENTION, GATE_ALL):
        if obst_p(s, 0, 1) != all(gates(s, 0, 1)):
            failures.append("obstP_factors")

    rep = repair_family_p(GATE_ALL, 0, 1)
    ext = extension_proposals(GATE_ALL, 0, 1)
    nxt = next_family_p(GATE_ALL)
    expected_next = [(("setBudget", 1), ("addCol", (0,))),
                     (("setBudget", 1), ("addCol", (1,)))]
    if rep != [] or ext != [(0,), (1,)] or nxt != expected_next:
        failures.append("two_rule / nextFamilyP at gateWitnessAll")
```

## Line-by-line Python explanation

- `if s.obs is None: return False`: the declared policy. With no
  observation there is no obstruction, whatever `wit` and `prot` hold.
  This line is the Python form of Lean's `obst_requires_observation`.
- `(i, j) in s.wit and (i, j) in s.prot and zero_p(s.obs, i, j)`: the
  other three gates. `zero_p` is "no column separates", the negation of
  `sep_p`, which is `any(sep_col(c, i, j) for c in cols)`; `sep_col` is
  `(i in c) != (j in c)`, exactly one endpoint in the column.
- `admitWit`: three conditions in the guard. `wf_pair` says the two
  positions differ and are in range of `occ`; `in s.asserted` says there
  is a claim to retain; `not in s.wit` prevents a duplicate. If any
  fails, `return s`: the event is inert, not an error.
- `protect`: the guard asks for `(i, j) in s.wit`, so a demand can only
  be placed on a retained pair. There is no check against `asserted`
  here; retention already implied it.
- `BASE` and the five states: the Lean witnesses `gateWitnessNoZero`,
  `gateWitnessNoDeclaration`, `gateWitnessNoProtection`,
  `gateWitnessNoRetention`, `gateWitnessAll`, field for field. Only
  `obs`, `prot` and `wit` vary. `obs=((0,),)` is one column holding
  position 0, which separates 0 from 1, so gate 4 fails there.
- `gates`: the four gates as a tuple. The fourth entry writes the
  convention out: `True if s.obs is None`. Comparing `obst_p` with
  `all(gates(...))` at the five states is an instance of
  `obstP_factors`, not a proof of it; the Lean proves it for all states.
- `repair_family_p(GATE_ALL, 0, 1) == []`: the declared observation is
  the empty list of columns, so there is nothing to refine.
- `extension_proposals(GATE_ALL, 0, 1) == [(0,), (1,)]`: the candidates
  are the singleton columns over the admitted positions, `[0]` and
  `[1]`; both are new, in range, and separate 0 from 1. Lean's
  `extension_always_available` promises only `[i]`, here `[0]`; the
  Python shows the whole list.
- `next_family_p(GATE_ALL)`: one block per proposal, each block the
  two-event list `setBudget 1, addCol c`. The budget event is inside the
  block because `GATE_ALL` has budget 0 and `addCol` would otherwise be
  inert; the family *represents* a funded execution, it does not perform
  one.

## Lean 4

The state, the obstruction predicate and its factorisation
(`lean4/Derivation/PrimitivePassage.lean` lines 77-88, 147-151,
218-226):

```lean
structure PState where
  occ : List Nat
  asserted : List (Nat × Nat)
  wit : List (Nat × Nat)
  prot : List (Nat × Nat)
  obs : Option (List (List Nat))
  budget : Nat
  licensed : Bool
  refusals : List (Nat × Nat)
  halted : Bool
deriving Repr, DecidableEq

def obstP (s : PState) (i j : Nat) : Bool :=
  (decide ((i, j) ∈ s.wit)) && (decide ((i, j) ∈ s.prot))
    && (match s.obs with
        | none => false
        | some cols => zeroP cols i j)
```

The gate on which the convention lives (lines 184-187):

```lean
def zeroDeclP (s : PState) (i j : Nat) : Bool :=
  match s.obs with
  | none => true
  | some cols => zeroP cols i j
```

Two guards of the step function (lines 631-641):

```lean
  | .admitWit i j =>
      if s.halted then s
      else if wfPair s i j && (decide ((i, j) ∈ s.asserted))
          && !(decide ((i, j) ∈ s.wit)) then
        { s with wit := s.wit ++ [(i, j)] }
      else s
  | .protect i j =>
      if s.halted then s
      else if (decide ((i, j) ∈ s.wit))
          && !(decide ((i, j) ∈ s.prot)) then
        { s with prot := s.prot ++ [(i, j)] }
      else s
```

The two-rule and the represented next family (lines 1082-1094,
1227-1232):

```lean
theorem two_rule (s : PState) (i j : Nat)
    (hobst : obstP s i j = true) (hij : i ≠ j)
    (hi : i < s.occ.length) (hprot : (i, j) ∈ s.prot) :
    repairFamily s i j ≠ [] ∨
      (repairFamily s i j = [] ∧ extensionProposals s i j ≠ []) := by
  cases hrep : repairFamily s i j with
  | cons m rest => exact Or.inl (by simp)
  | nil =>
      refine Or.inr ⟨rfl, ?_⟩
      intro hempty
      have := extension_always_available s i j hobst hij hi hprot
      rw [hempty] at this
      cases this

def nextFamilyP (s : PState) : List (List PEvent) :=
  (obstructedPairs s).flatMap fun r =>
    (repairFamily s r.1 r.2).map
        (fun m => [PEvent.refineCol m.1 m.2])
      ++ (extensionProposals s r.1 r.2).map
          (fun c => [PEvent.setBudget 1, PEvent.addCol c])
```

Lean (book), from `textbook/checks/u54_lean.py`: the convention made
visible, the two-rule instantiated, and the resolving block replayed.

```lean
theorem convention_before_declaration :
    zeroDeclP gateWitnessNoDeclaration 0 1 = true ∧
    zeroStrictP gateWitnessNoDeclaration 0 1 = false ∧
    obstP gateWitnessNoDeclaration 0 1 = false := by
  decide

theorem two_rule_at_all :
    repairFamily gateWitnessAll 0 1 ≠ [] ∨
      (repairFamily gateWitnessAll 0 1 = [] ∧
        extensionProposals gateWitnessAll 0 1 ≠ []) :=
  two_rule gateWitnessAll 0 1 (by decide) (by decide) (by decide) (by decide)

theorem families_at_all :
    repairFamily gateWitnessAll 0 1 = [] ∧
    extensionProposals gateWitnessAll 0 1 = [[0], [1]] ∧
    nextFamilyP gateWitnessAll =
      [[.setBudget 1, .addCol [0]], [.setBudget 1, .addCol [1]]] := by
  decide

theorem block_resolves :
    obstP (replayP [.setBudget 1, .addCol [0]] gateWitnessAll) 0 1 = false ∧
    nextFamilyP (replayP [.setBudget 1, .addCol [0]] gateWitnessAll) = [] := by
  decide
```

## Line-by-line Lean explanation

- `structure PState where … deriving Repr, DecidableEq`: nine fields, all
  finite lists, Booleans or a number. `DecidableEq` is what lets `decide`
  compare two whole states, which the book's `early_retention_inert`
  uses.
- `obs : Option (List (List Nat))`: `none` means "no observation
  declared". It is not an empty observation; the empty observation is
  `some []`. The distinction is the whole subject of the convention
  below.
- `def obstP … (decide ((i, j) ∈ s.wit)) && …`: `decide` turns a
  decidable proposition into a `Bool`, so the three conjuncts are
  Booleans. `match s.obs with | none => false` is the policy: no
  observation, no obstruction. `| some cols => zeroP cols i j` is the
  fourth gate when an observation exists.
- `def zeroDeclP … | none => true`: gate 4 as a *total* Boolean. On an
  undeclared observation it reads `true`, so that the product of the four
  gates still equals `obstP`: gate 3, `declaredP`, is the one that
  reads `false` there. The alternative, `zeroStrictP`, reads `false`;
  the module declares it only to state the comparison as a theorem.
- `| .admitWit i j => if s.halted then s else if wfPair s i j && … then
  { s with wit := s.wit ++ [(i, j)] } else s`: every branch of `step`
  begins with the halt test. Then the guard; then `{ s with … }`, the
  state with one field replaced. A failing guard returns `s`, so an
  unlicensed event is a non-event, not a crash.
- `| .protect i j => … (decide ((i, j) ∈ s.wit))`: a demand needs a
  retained pair. The asymmetry with `admitWit` is deliberate: retention
  looks at `asserted`, protection looks at `wit`, and nothing looks two
  stores back.
- `theorem two_rule … (hobst : obstP s i j = true) (hij : i ≠ j) (hi :
  i < s.occ.length) (hprot : (i, j) ∈ s.prot)`: four hypotheses, named
  so that nothing is hidden. `hij` and `hi` say the pair is well formed;
  they are *not* consequences of `hobst`, because `prot` can hold a pair
  that was never checked, which is why they are hypotheses.
- `cases hrep : repairFamily s i j with | cons m rest => … | nil => …`:
  the proof splits on whether the repair list is empty. If it has a head
  `m`, the left disjunct holds by `simp`. If it is empty, the right
  disjunct needs the extension list nonempty.
- `have := extension_always_available s i j hobst hij hi hprot; rw
  [hempty] at this; cases this`: that lemma says `[i] ∈
  extensionProposals s i j`; if the list were `[]`, membership in `[]`
  has no constructor, and `cases` closes the goal. So the two-rule rests
  on one fact: the singleton column `[i]` is always a fresh, in-range,
  separating column at an obstruction.
- `def nextFamilyP … flatMap … map … ++ … map`: for each obstructed
  protected pair, the repair blocks then the extension blocks. Each
  element is a *list of events*, a block, not a state: the family is a
  record of what could be replayed, and the module leaves iterating it
  to the reader.
- Book `convention_before_declaration`: the three values at
  `gateWitnessNoDeclaration`, by computation. Gate 4 reads `true` under
  the declared convention, `false` under the strict one, and `obstP` is
  `false` either way because gate 3 fails.
- Book `two_rule_at_all`: Genesis's theorem with its four hypotheses
  discharged by `decide` at `gateWitnessAll`. This is the vacuity check
  of the audit made into a declaration: the hypotheses are jointly
  satisfiable.
- Book `families_at_all`: what the two-rule leaves abstract, computed.
  The repair list is empty and the extension list is `[[0], [1]]`, so
  the two-rule's right disjunct is the one in force here.
- Book `block_resolves`: replaying the first block from the all-gates
  state clears the obstruction and empties the next family, which is
  `nextFamilyP_stop` and `extension_resolves` seen on one state.

## What has been proved

- `obstP_factors` (line 218): for every state and pair, `obstP s i j =
  (retainedP && protectedP && declaredP && zeroDeclP)`. Near-definitional,
  and to be cited together with the next item.
- `gate_zero_independent`, `gate_declared_independent`,
  `gate_protection_independent`, `gate_retention_independent` (lines
  521-585): each is a pair of `¬ ∀` statements. No three gates entail the
  fourth, and no three entail `obstP`. The five witness states (lines
  425-462) carry the proofs; `obst_conditions_independent` (line 476)
  collects them.
- `obs_gates_not_both_false` (line 281): gates 3 and 4 both read `obs`,
  so they are independent but not jointly free: at most one of them is
  `false` at a time. The module says this itself.
- `obst_requires_observation` (line 326): `obs = none` gives `obstP =
  false`. This is the declared policy stated as a theorem about the
  definition. `obst_policies_differ` (line 408) shows the rival policy
  `obstEmptyObs` disagrees at `preRetainedObstructed`, and
  `obst_policies_agree_when_declared` (line 390) shows the two agree
  wherever an observation exists.
- `assertion_not_retained` (line 692), `retention_not_free` (702),
  `retention_requires_assertion` (711), `retention_persists` (725),
  `assertion_persists` (734), `retention_completes` (864): the four
  stores fill in order and only in order.
- `witness_no_protection` (870), `no_protection_no_obstruction` (878):
  retention never creates protection, and without protection `obstP` is
  `false`.
- `asserted_offdiag` (787), `retained_sub_asserted` (821),
  `assert_transport` (838), `kernel_enters_preretained` (855): the
  asserted store is off-diagonal, retained pairs were asserted, and the
  induced `Setting` of a state with one asserted pair satisfies reading
  A, so Unit 53's witness enters the pre-retention state.
- `zero_refl`, `zero_symm`, `zero_trans` (907-953): for every list of
  columns, "no column separates" is an equivalence. The book's check
  confirms the three laws on every observation with at most two columns
  over three points.
- `menu_complete` (982), `extension_always_available` (1006), `two_rule`
  (1082): the response universe is complete over declared columns and
  in-range points; the singleton column `[i]` is always a proposal at an
  obstruction; repair or extension, never neither.
- `proposal_not_execution` (1098), `budget_gates_execution` (1112):
  `addCol` is inert without a licence, and without a budget.
- `refusal_object_inert` (1130), `refusal_not_terminal` (1141),
  `terminal_absorbing` (1156): a refusal moves no store but `refusals`
  and does not halt; after a halt every event is inert.
- `replay_append` (1175): replaying `h1 ++ h2` is replaying `h2` from the
  state after `h1`.
- `extension_resolves` (1185): after a funded, licensed, acceptable
  `addCol c` with `c` separating the pair, `obstP` is `false`.
- `nextFamilyP_stop` (1236), `nextFamilyP_nonempty` (1255),
  `nextFamilyP_complete_repair` (1273), `nextFamilyP_complete_ext`
  (1286): the family is empty exactly when nothing is obstructed, and it
  contains every repair and every extension block.

## What has not been proved

- That the declared convention was forced. `zeroDeclP` reading `true`
  before a declaration, and `obstP` reading `false` there, are choices.
  The module prices them (`obst_policies_differ`) and the ledger entry
  `CL-PD2-PACKET-05R` records that the choice is declared. The book's
  `convention_before_declaration` shows the three values side by side so
  that the reader sees a convention, not a derivation.
- That the chain terminates. `nextFamilyP` is a list of blocks; nothing
  in the module iterates it, and the module says so ("iteration of the
  family remains metatheoretic"). The fifteen-round growth driver of
  `code/derivation/primitive_passage.py` is a computation outside the
  Lean, taught with `HigherStructure` in Unit 55.
- Audit finding 1. `no_outside_operational` (line 1166) and
  `replay_deterministic` (1171) are `congrArg`: equal inputs give equal
  outputs because `step` and `replayP` are functions. They are true and
  carry no content beyond that; the paper's arrow 10 lists them as
  theorems beside `replay_append`, which is the only member of that row
  with content. This unit teaches determinism as "`step` is a
  function", as the audit proposes.
- Audit finding 2. `quotient_no_recovery` (line 897) says: if `q a = q
  b` then `g (q a) (q b) ↔ g (q a) (q a)`, a one-line rewrite. The
  paper's reading, "recovery data must be retained outside the quotient;
  that is what retention is *for*", is commentary: the theorem mentions
  no presentation, no faithfulness and no `wit`. The book's
  `collapse_cannot_see` instantiates it at a constant map to show what
  it does say.
- Audit finding 3. Arrow 5 of the paper's table, "observer zero → guarded
  collapse", carries the status THEOREM but names no theorem; it is the
  definition of `obstP`. It should read DEFINITION. The sealed paper is
  not edited; the correction lives here and in the audit record.
- Audit finding 4, a finitude flag. `inducedSetting` (line 755) uses
  `X := Nat` as carrier, with `r x y := (x, y) ∈ s.asserted`. The
  system's content is the finite list `s.occ`; `Nat` is the
  metatheory's container, and irreflexivity holds off the asserted store
  vacuously over all of `Nat`. "The two-element kernel enters the
  passage" is right about the relation, one off-diagonal pair, and wrong
  if read as "the setting has two elements". The book's
  `induced_reading` reads the three relations at `0`, `1` and nothing
  else.
- `obst_diverges_when_undeclared` is omitted here, as the ledger keeps it
  only as a historical witness and its first conjunct is a statement
  about written-out lists rather than about any state.

## Outside the system

- The positions `Nat`, the `Option` type, and the quantifier over every
  `cols : List (List Nat)` in the zero laws are metatheory. The system
  possesses finite lists at each state; it does not possess the type of
  all lists.
- The budget and licence are numbers and flags set by events
  (`setBudget`, `setLicense`) that have no guard but the halt. Who sets
  them is not modelled: the machine records funding for either column
  change and permission for a new column, without identifying their
  supplier. Existing-column refinement has no licence gate. This is where the derivation's authority
  boundary sits in this module.
- Column *meaning* is outside. A column is a list of positions; that it
  "observes" anything is the reader's gloss. The module uses only
  membership.
- The paper's arrow 2, "retained witness → faithful presentation", is a
  declaration with no theorem in this module; it cites
  `PrimDiff.const_presentation_unfaithful` from Unit 15. Faithfulness is
  demanded, never proved here.

## Student exercise

Start from `gateWitnessAll` but with `obs := some [[0, 1]]`: one column
holding both positions. Decide, by hand, each of the four gates for the
pair `(0, 1)`, then `obstP`. Then list the extension proposals and the
repair family, and say which disjunct of `two_rule` is in force, or
whether its hypotheses hold at all.

## Answer

The column `[0, 1]` contains both positions, so it separates nothing:
`sepCol [0, 1] 0 1 = (true != true) = false`, hence `zeroP [[0, 1]] 0 1 =
true`. The four gates read retained `true`, protected `true`, declared
`true`, zero `true`, so `obstP = true`: the pair is obstructed even though
a column exists, because the column does not split it.

The two-rule's hypotheses hold: `obstP` is `true`, `0 ≠ 1`, `0 < 2`, and
`(0, 1) ∈ prot`. Extension proposals: the candidates are `[0]` and `[1]`;
each is in range, not already a column, and separates the pair, and
`colOk` also asks that some obstructed protected pair is separated, which
`(0, 1)` is. So both are proposed. Repair family: the menu is `([0, 1],
0)` and `([0, 1], 1)`; `refineOk` requires `p ∉ v`, and both positions
are already in the column, so the family is empty. The right disjunct is
in force: repair empty, extension nonempty. Running
`[setBudget 1, addCol [0]]` yields `obs = some [[0, 1], [0]]`, and `[0]`
separates the pair, so `obstP` becomes `false`.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/PrimitivePassage.lean` lines 77-105 (`PState`, `genesisP`, `PEvent`), 110-124 (`sepCol`, `sepP`, `zeroP`), 147-151 (`obstP`), 168-197 (the four gates and the strict variant), 202-226 (the two factorisations), 281 (`obs_gates_not_both_false`), 326-331 (`obst_requires_observation`), 382-410 (`obstEmptyObs`, the policies), 425-476 (the five witnesses), 521-585 (independence), 592-678 (`wfPair`, `refineOk`, `colOk`, `step`, `replayP`), 692-883 (assertion, retention, protection, transport), 897-899 (`quotient_no_recovery`), 907-953 (zero laws), 961-1012 (menu, repair, extension), 1082-1094 (`two_rule`), 1098-1158 (licence, budget, refusal, terminal), 1166-1177 (replay), 1185-1222 (`extension_resolves`), 1224-1298 (`nextFamilyP` and its four theorems) |
| Axiom report | `artifacts/lean_axioms.txt` lines 459-514 |
| Paper | `paper/primitive_difference_passage.md` "The chain, arrow by arrow" and "P-theorems"; `paper/paper_claim_ledger.md` `CL-PD2-PASSAGE`, `CL-PD2-PACKET-05P`, `CL-PD2-PACKET-05R` |
| Python | `code/derivation/primitive_passage.py` (`PS`, `obst_p`, `pstep`, `preplay`, `repair_family_p`, `extension_proposals`, `next_family_p`, `arrow_report`), `tests/test_primitive_passage.py`, `artifacts/primitive_passage.json` (`arrows`) |
| Audit | `textbook/audit/modules/PrimitivePassage.md` findings 1-8 |
| Check (Python) | `python textbook/checks/u54_primitive_passage.py`: the store order, the four gates at the five witnesses, the two policies, the two-rule and next family at `gateWitnessAll`, licence and budget, refusal, the absorbing halt, replay, the zero laws on 1 971 cases, and `arrow_report()` against the artifact |
| Check (book Lean) | `python textbook/checks/u54_lean.py`: twenty-one book declarations plus twenty-two Genesis theorems kernel-checked, Lean 4.33.0 |
