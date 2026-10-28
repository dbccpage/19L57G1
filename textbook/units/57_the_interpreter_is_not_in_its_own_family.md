# Unit 57. The interpreter is not in its own family: what a notes-diagonal does and does not show

**Claim.** A notes-diagonal step differs from every member of the finite constitution-code family. Because notes are operationally inert, this does not establish the meaning of an uncoded interpreter role.

**Status:** FROZEN (the thirteen theorems);
VERIFIED_FINITE (the 65-count, the Python diagonal over 64 indices);
ADMITTED (the relation, retention and protection of `boundarySetting`,
inserted by definition); OPEN (the denotational bridge; absolute
self-interpretation). **Lean:** `lean4/Derivation/InterpreterBoundary.lean`
lines 103-394, imports `Constitution`, `PrimitiveCore`. **Axioms:** 13
reports; `propext` and `Quot.sound` for the diagonal and the `rfl`
equations over `interpStep`, none for the five I5 theorems. **Depends
on:** Unit 45 (`World`, `step`, `supp`, `notes_inert`), Unit 48
(`ConstitutionDesc`, `interpStep`, `kernelDesc`, `allDescs`,
`interp_describe`), Unit 25 (`FidelityObstruction`,
`obstruction_under_irrefl`), Unit 51 (`Setting`, A, F).

## First pass

There are 64 constitution descriptors and one fixed interpreter that executes them. A descriptor and the function interpreting descriptors have different types and roles.

The diagonal witness changes notes to differ from every coded step. That proves the stated difference of functions; the operational meaning of an uncoded role remains an open bridge.

## Detailed claim and formal anchors

The sealed constitution (Unit 48) has a 64-member family of
codes `ConstitutionDesc`, one fixed evaluator `interpStep` that runs any
code, and a verified self-description: the all-on code executes to the
sealed step (`interp_describe`).

The evaluator is a function over the
codes and is not one of them. `InterpreterBoundary` studies that
boundary and proves exactly this much. **I1**, `tower_persists`: for any
finite list of codes and any evaluation map into step functions, some
step function differs from every coded one.

The witness is a diagonal
that, at the world whose datum count is the code's index, runs that
code and appends one element to the operationally inert `notes` field.
**I2**, `i2_universal_in_class`: the pair of `allDescs_complete` and
`interp_describe`. **I3**, `evalOpt`: one evaluator on
`Option ConstitutionDesc` that returns `none` for the uncoded input, by
definition. **I4**, `family_missed`: I1 at the sealed family. **I5**: a
`PrimitiveCore.Setting` on the 65-element carrier whose asserted,
retained and protected relation is the single ordered pair (kernel
code, uncoded role); it satisfies A and F (`i5_boundary_is_A`,
`i5_boundary_is_F`) and identifying its two endpoints is obstructed
under irreflexivity (`i5_collapse_obstructed`).

What is *not* proved,
and is recorded as such: that the uncoded role means anything, that the
missed function is "the interpreter", or that the boundary difference
changes any accessible verdict. `arbitrary_uncoded_assignment` proves
that any function at all can be assigned to the uncoded role, so the
existence of such an assignment grounds nothing.

The denotational
bridge is the OPEN label `openDenotationalBridge`; the identification
of the boundary with a primitive difference is the retained conjecture
`frontierConjecture`.

## Question

A machine can carry a description of itself and we can prove the
description runs as the machine does. Does that make the machine its
own interpreter? And if not, what exactly is the gap: a theorem that
says the gap cannot close, a theorem that says it can, or neither?

## What we already possess

- `World` with seven fields, the last of them `notes`, which no guard
  reads; `supp w` drops it; `notes_inert` shows two worlds differing only
  in notes step to support-equal worlds (Unit 45).
- `ConstitutionDesc`, six booleans; `interpStep d` is the sealed `step`
  with each guard consulted only when its bit is on; `kernelDesc` is all
  six on; `allDescs` lists the 64 codes with the first field slowest, so
  `kernelDesc` is last, at index 63; `interp_describe` says
  `interpStep kernelDesc w e = step w e` (Unit 48).
- `FidelityObstruction P r c`: `c` collides a related pair and the
  pushforward of `r` along `c` fails `P`; `obstruction_under_irrefl`:
  identifying any related pair is obstructed under `Irrefl` (Unit 25).
- `PrimitiveCore.Setting` with fields `X r a b ret prot Ops`; candidate
  A is `r a b ∧ Irrefl r`; F is A with `ret a b` and `prot a b` (Unit
  51).

## New concept: a diagonal against a finite code list, and a declared boundary

Given any list of codes `cs` and any way `ev` of reading a code as a
step function, the *diagonal* `diag cs ev` is the step function that,
at a world with `i` data, looks up the code at position `i`, runs it,
and appends `999` to the notes; at a world whose datum count is past
the end of the list it returns its input. At the world with `i` data
the diagonal has one more note than code `i` does, so it is not code
`i`'s function. It differs from each code at one world, a different
world for each code.

An *evaluation map* here is any function `C → World → Event → World`;
`interpStep` is one. A *typed refusal* is an evaluator whose codomain is
`Option World`, so that "no verdict" is a value and not a missing case.

The *declared boundary model* is a `Setting` whose carrier is
`Option ConstitutionDesc`: the 64 codes wrapped in `some`, plus `none`,
read as the interpreter's role. Its relation is the single pair
`(some kernelDesc, none)`, and the same pair is its retention and its
protection. All three are written into the definition.

## Plain-language interpretation

Think of the 64 codes as 64 cards, each saying which of six guards to
switch on. There is one reader, `interpStep`, that takes any card and
behaves accordingly. One card, all six on, makes the reader behave
exactly as the sealed machine (Unit 48). That is a self-description:
the machine's own behaviour appears among the cards, and we have a
proof of it.

The reader itself is not a card. Is that a deep fact or a bookkeeping
fact? The module answers in pieces, and each piece is smaller than it
sounds.

Piece one: no finite deck of cards, read by any reader at all, covers
every possible behaviour. Proof: build a behaviour that disagrees with
card 0 when there is nothing on the table, with card 1 when there is
one thing, and so on. The disagreement is made in the cheapest possible
place, a comment field that no rule reads. So the behaviour the deck
misses is, operationally, indistinguishable from the card it shadows;
only the comment differs. That is why the module calls this
*extensional* incompleteness and refuses the word "tower".

Piece two: the deck is complete as a deck, and the all-on card is the
machine. Nothing new; two Unit 48 theorems restated as one.

Piece three: one can give the reader a 65th input, "no card", and have
it answer "no verdict". That is a construction that compiles. It does
not show the reader had to be partial, or that it could not have been
given something else.

Piece four: piece one applied to the actual deck and the actual reader.

Piece five: write down a setting in which the all-on card and the
"no card" slot are the two named points, declare that they differ,
declare that the difference is retained and protected, and check that
the declared setting satisfies the two candidate readings A and F from
Unit 51 and that gluing the two points together is obstructed. It does.
Of course it does: every clause was written in. The module says so,
in the words "inserted by definition".

What would turn this declared model into a derived one is a theorem
that connects the "no card" slot to the missed behaviour of piece one,
and shows that identifying them changes some verdict a reader can
reach. There is no such theorem. Worse for the easy route: *any*
behaviour can be assigned to the empty slot while the cards keep their
meanings, so the mere existence of an assignment is free and proves
nothing. The module records the missing theorem as an obligation
string and the identification as a conjecture, and that is where the
frozen derivation leaves it.

## Pseudocode

```
diag(cs, ev)(w, e) :=
    i := length(w.data)
    if i < length(cs): out := ev(cs[i])(w, e); out.notes += [999]; return out
    else:              return w

claim I1: for every finite cs and every ev, exists f with f ≠ ev(c) for all c in cs
    witness f := diag(cs, ev); at world(i) its notes are one longer than ev(cs[i])'s

evalOpt(none)(w, e)   := none
evalOpt(some d)(w, e) := some(interpStep(d)(w, e))

boundary: carrier = {some d | d in allDescs} ∪ {none}
          r = ret = prot = {(some kernelDesc, none)}
A: r(a, b) and no r(x, x)        -- true by the definition of r
F: A and ret(a, b) and prot(a, b) -- true by the definition of ret, prot

not proved: any link between none and the f of I1
```

## Python

Genesis's mirror, `code/derivation/interpreter_boundary.py`:

```python
def index_world(i: int) -> World:
    """The world whose carrier length encodes the index ``i``."""
    return World(data=tuple(range(i)))


def diag(cs: Sequence[Desc], w: World, e: Event) -> World:
    idx = len(w.data)
    if idx < len(cs):
        w2 = interp_step(cs[idx], w, e)
        return World(
            data=w2.data, views=w2.views, reqs=w2.reqs,
            refusals=w2.refusals, budget=w2.budget,
            aug_licensed=w2.aug_licensed, notes=w2.notes + (999,),
        )
    return w


def diagonal_misses_all(
    f: Callable[[World, Event], World], cs: Sequence[Desc]
) -> bool:
    return all(
        f(index_world(i), NOTE_EVENT)
        != interp_step(cs[i], index_world(i), NOTE_EVENT)
        for i in range(len(cs))
    )


def eval_opt(c: Optional[Desc], w: World, e: Event) -> Optional[World]:
    if c is None:
        return None
    return interp_step(c, w, e)


def boundary_rel(x: Optional[Desc], y: Optional[Desc]) -> bool:
    return x == KERNEL_DESC and y is None
```

The book's check, `textbook/checks/u57_interpreter_boundary.py`, adds
Python (book):

```python
def supp(w: World) -> tuple:
    return (w.data, w.views, w.reqs, w.refusals, w.budget, w.aug_licensed)

    supp_agree = all(
        supp(f(index_world(i), NOTE_EVENT))
        == supp(interp_step(descs[i], index_world(i), NOTE_EVENT))
        for i in range(64)
    )

    def assign(fn):
        return lambda c, w, e: fn(w, e) if c is None else interp_step(c, w, e)
    i1 = assign(lambda w, e: w)
    i2 = assign(f)
```

## Line-by-line Python explanation

- `index_world(i)`: data `(0, …, i-1)`, everything else at its default.
  Only the length is used; the module says "only the length is
  load-bearing".
- `diag`: `idx` is the datum count. Inside the list, run the code at
  that index and copy every field of the result except `notes`, which
  gets `999` appended. Outside the list, return `w` untouched. The
  Python check confirms both branches: at index 63 the kernel's notes
  are `(0,)` and the diagonal's `(0, 999)`; at 64 data the diagonal
  returns its input.
- `diagonal_misses_all(f, cs)`: for each index, compare `f` with code
  `i` at `index_world(i)` under the note event. It is `True` for the
  diagonal and `False` for a function that copies member 5, which
  agrees with itself at index 5. This is the finite mirror of
  `tower_persists`, over the 64 indices only.
- `eval_opt`: `None` returns `None`; a code returns the plain
  `interp_step`. The two Lean equations are these two lines.
- `boundary_rel`: the one ordered pair. `candidate_a` and `candidate_f`
  in the module test it on all 65 carrier elements and the artifact
  records both `True`.
- Python (book) `supp`: drop `notes`. `supp_agree` is `True` at all 64
  indices: on the support the diagonal *is* the code it shadows. This
  is the scope the module and paper state in prose, made a number.
- Python (book) `assign`: complete the carrier with any `fn` at `None`.
  Two different choices both cover the family and disagree at `None`.
  Nothing selected either.

## Lean 4

The diagonal and I1 (`lean4/Derivation/InterpreterBoundary.lean` lines
114-178, abridged):

```lean
def indexWorld (i : Nat) : World :=
  ⟨List.range i, [], [], [], 0, true, []⟩

def diag {C : Type} (cs : List C) (ev : C → World → Event → World)
    (w : World) (e : Event) : World :=
  (cs[w.data.length]?).elim w
    (fun c => { ev c w e with notes := (ev c w e).notes ++ [999] })

theorem tower_persists {C : Type} (cs : List C)
    (ev : C → World → Event → World) :
    ∃ f : World → Event → World, ∀ c ∈ cs, f ≠ ev c := by
  refine ⟨diag cs ev, ?_⟩
  intro c hc hEq
  obtain ⟨i, hi⟩ := List.getElem?_of_mem hc
  have hidx : cs[(indexWorld i).data.length]? = some c := by
    rw [indexWorld_len]
    exact hi
  have happ : diag cs ev (indexWorld i) (.note 0) =
      ev c (indexWorld i) (.note 0) :=
    congrFun (congrFun hEq (indexWorld i)) (Event.note 0)
  rw [diag_hit ev hidx (Event.note 0)] at happ
  have hlen : ((ev c (indexWorld i) (.note 0)).notes ++ [999]).length =
      (ev c (indexWorld i) (.note 0)).notes.length :=
    congrArg (fun w : World => w.notes.length) happ
  simp only [List.length_append, List.length_cons,
    List.length_nil] at hlen
  omega
```

I3 and I5 (lines 233-249, 286-327, abridged):

```lean
def evalOpt (c : Option ConstitutionDesc) (w : World) (e : Event) :
    Option World :=
  match c with
  | some d => some (interpStep d w e)
  | none => none

def boundarySetting : PrimitiveCore.Setting where
  X := Option ConstitutionDesc
  r := fun x y => x = some kernelDesc ∧ y = none
  a := some kernelDesc
  b := none
  ret := fun x y => x = some kernelDesc ∧ y = none
  prot := fun x y => x = some kernelDesc ∧ y = none
  Ops := fun _ => False

theorem i5_boundary_is_A : PrimitiveCore.A boundarySetting :=
  ⟨⟨rfl, rfl⟩, fun _x h => nomatch h.1.symm.trans h.2⟩

theorem i5_boundary_is_F : PrimitiveCore.F boundarySetting :=
  ⟨i5_boundary_is_A, ⟨rfl, rfl⟩, ⟨rfl, rfl⟩⟩

theorem i5_collapse_obstructed {β : Type}
    (q : Option ConstitutionDesc → β)
    (hq : q (some kernelDesc) = q none) :
    PrimDiff.FidelityObstruction PrimDiff.Irrefl
      boundarySetting.r q :=
  PrimDiff.obstruction_under_irrefl ⟨rfl, rfl⟩ hq
```

The vacuity proof and the two labels (lines 356-394, abridged):

```lean
theorem arbitrary_uncoded_assignment
    (f : World → Event → World) :
    ∃ I : Option ConstitutionDesc → (World → Event → World),
      I none = f ∧ ∀ d, I (some d) = interpStep d := by
  refine ⟨fun c => match c with
    | none => f
    | some d => interpStep d, rfl, ?_⟩
  intro d
  rfl

def openDenotationalBridge : String :=
  "OPEN: independently specify lawful meaning for the uncoded role " ++
  "and prove an accessible behavioral non-identification; a freely " ++
  "chosen assignment is vacuous"

def frontierConjecture : String :=
  "INTERPRETER_BOUNDARY_IS_PRIMITIVE_DIFFERENCE (conjecture; " ++
  "missing: denotational/operational grounding theorem)"
```

Lean (book), from `textbook/checks/u57_lean.py`: the diagonal at the
kernel's index, its agreement on the support, two assignments at once,
and a reversed declared setting.

```lean
theorem kernel_index : allDescs[63]? = some kernelDesc := by decide

theorem diag_notes_at_kernel :
    (diag allDescs interpStep (indexWorld 63) (.note 0)).notes = [0, 999] ∧
    (interpStep kernelDesc (indexWorld 63) (.note 0)).notes = [0] := by
  constructor <;> rfl

theorem diag_supp_agrees_at_kernel :
    supp (diag allDescs interpStep (indexWorld 63) (.note 0)) =
      supp (interpStep kernelDesc (indexWorld 63) (.note 0)) := rfl

theorem two_assignments :
    ∃ I₁ I₂ : Option ConstitutionDesc → (World → Event → World),
      (∀ d, I₁ (some d) = interpStep d) ∧ (∀ d, I₂ (some d) = interpStep d) ∧
      I₁ none ≠ I₂ none := by
  obtain ⟨I₁, h₁, c₁⟩ := arbitrary_uncoded_assignment (fun w _ => w)
  obtain ⟨I₂, h₂, c₂⟩ :=
    arbitrary_uncoded_assignment (fun w _ => { w with notes := w.notes ++ [1] })
  refine ⟨I₁, I₂, c₁, c₂, ?_⟩
  intro h
  have := congrArg (fun g => (g genesis (.note 0)).notes) (h₁ ▸ h₂ ▸ h)
  exact absurd this (by decide)

def reversedSetting : PrimitiveCore.Setting where
  X := Option ConstitutionDesc
  r := fun x y => x = none ∧ y = some kernelDesc
  a := none
  b := some kernelDesc
  ret := fun x y => x = none ∧ y = some kernelDesc
  prot := fun x y => x = none ∧ y = some kernelDesc
  Ops := fun _ => False

theorem reversed_is_F : PrimitiveCore.F reversedSetting :=
  ⟨⟨⟨rfl, rfl⟩, fun _x h => nomatch h.1.symm.trans h.2⟩, ⟨rfl, rfl⟩, ⟨rfl, rfl⟩⟩
```

## Line-by-line Lean explanation

- `indexWorld i := ⟨List.range i, …⟩`: the data field is `[0, …, i-1]`,
  so `indexWorld_len` says its length is `i`. This is how a natural
  number is smuggled into a world: as a count of data.
- `diag … := (cs[w.data.length]?).elim w (fun c => …)`: `cs[k]?` is
  the optional lookup; `.elim w g` returns `w` on `none` and `g c` on
  `some c`. The `some` branch copies `ev c w e` and extends `notes`.
- `tower_persists`: the witness is the diagonal. Suppose it equals
  `ev c` for some `c` in the list. `List.getElem?_of_mem` gives the
  index `i` where `c` sits. `hidx` rewrites that index as the length of
  `indexWorld i`'s data. `happ` applies the supposed equality at that
  world and the note event; `diag_hit` unfolds the diagonal there, so
  the two sides are the extended notes and the original notes. `hlen`
  takes lengths; `simp` makes it `n + 1 = n`; `omega` closes. Nothing
  about guards, budgets or verdicts appears anywhere in this proof: the
  disagreement is a list length.
- `evalOpt`: a match with two arms. Both I3 theorems are `rfl`, and
  the axiom report shows `propext, Quot.sound` for them only because
  `interpStep` is unfolded.
- `boundarySetting`: seven fields. The same two-clause predicate is
  written three times, as `r`, `ret` and `prot`. `Ops` is empty.
- `i5_boundary_is_A := ⟨⟨rfl, rfl⟩, fun _x h => nomatch …⟩`: `r a b`
  is `some kernelDesc = some kernelDesc ∧ none = none`, two `rfl`s.
  Irreflexivity: a self-pair `r x x` would give `x = some kernelDesc`
  and `x = none`, and chaining them is `some kernelDesc = none`, which
  has no constructor match. No axiom is used because nothing is
  computed; the five I5 reports read "does not depend on any axioms".
- `i5_boundary_is_F`: A, then `ret a b` and `prot a b`, each the same
  two `rfl`s. This is what "inserted by definition" means at the proof
  term.
- `i5_collapse_obstructed`: Unit 25's theorem at the pair, with
  `⟨rfl, rfl⟩` as the proof that the pair is related and `hq` as the
  collision. It needs `hq`; for a `q` that keeps the endpoints apart
  there is no hypothesis, and the theorem says nothing. Book
  `isSome_keeps_apart` exhibits such a `q`.
- `arbitrary_uncoded_assignment`: define `I` by cases; both equations
  are `rfl`. The theorem is true for every `f` because it asks for
  nothing of `f`.
- Book `kernel_index`: `decide` walks the 64-element list. Book
  `diag_notes_at_kernel` and `diag_supp_agrees_at_kernel` are both
  `rfl`: at the kernel's index the diagonal's notes are `[0, 999]`
  against `[0]`, and the supports are identical. Together they are the
  exact content of `family_missed` at one index: different, and
  different nowhere a guard can see.
- Book `two_assignments`: `arbitrary_uncoded_assignment` twice, with the
  identity-on-worlds and with a note-appending function. The two `I`s
  agree on every code and differ at `none`; the difference is read off
  at `genesis` under one note event. The theorem admits both, so it
  picks neither.
- Book `reversedSetting` and `reversed_is_F`: the same carrier with
  the pair written the other way round satisfies F by the same proof
  term. The orientation of the declared difference came from the
  author, not from interpretation.

## What has been proved

- `indexWorld_len` (117), `diag_hit` (132), `tower_persists` (156):
  every finite code list under every evaluation map is missed by a
  step function of the same type.
- `i2_universal_in_class` (199): `allDescs_complete` and
  `interp_describe`, paired.
- `i3_refusal_code_returns_none` (241), `i3_coded_member_returns_some`
  (246): the two defining equations of `evalOpt`.
- `family_missed` (264): `tower_persists` at `allDescs`, `interpStep`.
- `i5_carrier_occurrences` (297): the carrier list has 65 entries.
- `i5_boundary_is_A` (306), `i5_boundary_is_F` (314): the declared
  setting satisfies A and F.
- `i5_collapse_obstructed` (322): identifying the two endpoints is
  obstructed under `Irrefl`.
- `i5_family_not_extensionally_complete` (349): `family_missed` again,
  under the name the 2026-08-13 audit repair gave it.
- `arbitrary_uncoded_assignment` (356): any step function can be
  assigned to `none` with the codes unchanged.

## What has not been proved

- That no self-interpreter exists, that the evaluator cannot be coded,
  or that self-evaluation is impossible. `tower_persists` says only
  that a finite list does not exhaust a function type, and its witness
  differs from each code at the inert field alone
  (`diag_supp_agrees_at_kernel`, and the Python check at all 64
  indices). Audit finding 1: the identifier `tower_persists` and the
  phrase "every finite closure has a new top" promise a tower; the
  statement delivers extensional incompleteness. The paper and the
  ledger scope it exactly in prose; the name stays. Teach the
  statement, not the name.
- That `interpStep` has a code in the family it runs, or that running
  such a code would reproduce `interpStep` on itself. Not formulated.
- That the uncoded occurrence `none` means anything. `evalOpt none` is
  a refusal; `arbitrary_uncoded_assignment` shows a free assignment is
  vacuous; `two_assignments` shows two incompatible ones at once.
- That the boundary difference is a primitive difference in the
  operational sense. The declared setting satisfies A and F because
  its relation, retention and protection are definitions (audit
  finding 2; `reversed_is_F` shows the mirror-image declaration passes
  too). No theorem derives the relation from behaviour, and no verdict
  changes when the endpoints are identified, since the only proved
  difference is in `notes`.
- Audit finding 3: `i2_universal_in_class` proves "the list is complete
  and the kernel is in it"; no universality property beyond the
  definition of `interpStep` is stated. "Universal" is a name.
- Audit finding 4: `{C : Type}` and `∃ f : World → Event → World` are
  metatheory. The system holds no object "the type of step functions";
  "uniform in the level" and "apply again to the 65-member family" are
  iterations the reader performs over Lean lists, not a tower the
  system builds. Under the finitude rule this is a flag, not a defect,
  because the paper's "and nothing more" clause bounds it.
- The denotational bridge is OPEN. The frozen derivation says so in a
  string, `openDenotationalBridge`, and in the ledger entry
  `CL-PD2-INTERPRETER`, and this book teaches it as OPEN. A merged
  research tree outside the seal, `research/interpreter_verdict/`, has
  since recorded a post-freeze verdict on a restricted form of this
  obligation; Part V of this book teaches it under its own status, and
  nothing in it changes the status of any theorem on this page.

## Outside the system

- The reading of `none` as "the interpreter's role" is a reading. The
  Lean carrier has 65 elements; which one is "the interpreter" is a
  label in the docstring and the artifact's `witness` field.
- The I0 status, the five tag strings, `conclusionTags`,
  `openDenotationalBridge` and `frontierConjecture` are `String` and
  `List String` values. They prove nothing, and `#print axioms` would
  show no axioms for them only because they are not theorems. They are
  receipt text; the book cites them as such.
- The six-way vocabulary the audit record fixes, with Lean referents:
  a *represented transition* is `step w e`; a *coded interpreter* is
  `interpStep d`; a *behavioural distinction* is a probe on which two
  codes disagree (Unit 49's six probes, `distinct_on_basis = 64` in the
  artifact); a *denotational interpretation* would be a relation from
  codes and the uncoded role to step functions, constrained by
  behaviour, and none is defined; a *self-description* is
  `interp_describe`; an *absolute self-interpreter* would be a code `c`
  with `ev c = ev`, or an interpreter in the family of what it
  interprets, and it is neither constructed nor refuted.

## Student exercise

The diagonal appends `999` to `notes`. Suppose instead it appended the
code's index to `data`: at `indexWorld i` it ran code `i` and then added
the datum `i` to the result. Does the proof of `tower_persists` still go
through as written? And does `diag_supp_agrees_at_kernel` still hold?
Say what each answer means for the word "extensional".

## Answer

The proof as written breaks at `hlen`: it compares `notes` lengths, and
the modified diagonal leaves `notes` alone. A proof could be repaired by
comparing `data` lengths instead, since `(ev c (indexWorld i) (.note 0)).data`
has length `i` (a note event adds no datum) and the modified diagonal's
has length `i + 1`; the structure of the argument is the same. So I1
survives the change. But `diag_supp_agrees_at_kernel` fails: `data` is
part of `supp`, so the modified diagonal and the kernel disagree on the
support at index 63. That change would make the missed function differ
from the code it shadows in a field a guard reads, and a later `require`
or `mark` event could reach a different verdict from the two worlds.
The frozen module chose the inert field deliberately, and the paper
says why: it wants the theorem to carry *only* extensional content and
to make no operational claim it has not earned. The exercise shows the
choice is a choice; an operational version of I1 would need to be
stated and proved separately, and the module does not do that.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/InterpreterBoundary.lean` lines 103-110 (I0 string), 114-178 (I1), 199-218 (I2 and tags), 233-249 (I3), 264-266 (I4), 286-352 (I5), 356-394 (vacuity, labels) |
| Axiom report | `artifacts/lean_axioms.txt` lines 580-592 |
| Paper | `paper/primitive_interpreter_boundary.md` (I0-I5, the audit repair of 2026-08-13); `paper/paper_claim_ledger.md` `CL-PD2-INTERPRETER`; `paper/paper_change_log.md` lines 760-780 (the rename); `paper/native_derivation_map.md` last row (OPEN, "the named irreducible obligation") |
| Python | `code/derivation/interpreter_boundary.py`, `code/run_interpreter_boundary.py`, `tests/test_interpreter_boundary.py`, `artifacts/primitive_interpreter.json` |
| Audit | `textbook/audit/modules/InterpreterBoundary.md` findings 1-5 and section 6 |
| Check (Python) | `python textbook/checks/u57_interpreter_boundary.py`: family and kernel index, the six probes, the diagonal over 64 indices and a fake that fails, notes at index 63, support agreement at all 64 indices (Python (book)), the off-range branch, `evalOpt`, the boundary candidates and two collapses, two assignments (Python (book)), report against artifact |
| Check (book Lean) | `python textbook/checks/u57_lean.py`: thirteen book declarations plus thirteen Genesis theorems kernel-checked, Lean 4.33.0 |
