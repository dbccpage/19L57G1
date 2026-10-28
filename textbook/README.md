# The Genesis Textbook

AuthorityEffect: None. This folder teaches the sealed derivation; it is not
part of it. Nothing here is an input to `prompt/`, `paper/`, `code/`,
`lean4/Derivation/` or `artifacts/`, and nothing here changes them. Where a
unit and the Lean disagree, the Lean wins.

The book is built one small derivation at a time. Each unit takes one
theorem (or one definition), states it, shows it in Lean, shows it in
Python, explains it in plain words, walks the proof step by step, and says
what it does and does not establish.

## Source

Units 00 to 03 were written against `main` at
`23979a46308219b4cc9e7e172e4e32511f8efdb0` (2026-10-24); Units 04 onward
against `main` at `33100245` (2026-10-28, after #283). The sealed files the
units quote are the same at both commits. Lean is quoted from
`lean4/Derivation/`. Axiom reports are read from the committed
`artifacts/lean_axioms.txt` and, for the book's own Lean, from a local
Lean 4.33.0 build of `lean4/`; a unit says so when it did not rebuild Lean.
Part 2 of the book (`textbook/institutions/`, see **Parts**) is written on
draft pull request #284 and is not in `main` at either commit.

## Status marks

| Mark | Meaning |
|---|---|
| **admitted** | A definition, a declared rule, a convention, or a hypothesis. Chosen, not proved. |
| **derived** | Proved in Lean from the admitted definitions, with no extra hypothesis. A countermodel proved in Lean is derived too, and is called one. |
| **verified finite** | Computed exhaustively over a declared finite search space. The unit states the bounds; the result says nothing outside them. |
| **conditional** | Proved in Lean only under an extra admitted hypothesis. The unit names the hypothesis. |
| **open** | Neither proved nor refuted, or a choice with no internal answer. |

The marks follow the paper's classification tags, which keep **[theorem]**
apart from **[finite computation]** and **[bounded theorem]**
(`paper/paper.md`, opening paragraph). A finite check is
never promoted to **derived**, and a sample check (such as Unit 01's) is
weaker still: it illustrates a theorem, it does not verify anything
exhaustively.

**derived** is always relative to the admitted definitions. No theorem in
this book proves that its own definitions were the necessary ones. Each unit
lists, under **What you need first**, the admitted definitions its claim
depends on.

## Kinds of code

| Label | What it is | Trust |
|---|---|---|
| Lean (Genesis) | Copied from `lean4/Derivation/`. | Checked by Lean's kernel when Genesis builds. The authority. |
| Python (Genesis) | Copied from `code/derivation/`. | Tested in Genesis. Tied to the Lean by executable checks, not by proof (ledger entry `CL-TOKEN-ERASURE`). |
| Lean (book) | Written for this book, held in a check script, and kernel-checked against Genesis's compiled `Derivation` library when that script runs. | Checked by Lean's kernel when the script runs; not part of Genesis's build, gates or `artifacts/lean_axioms.txt`. The script prints its own axiom report. |
| Gloss | Pseudocode written for this book. | Unchecked. Read it as a translation aid only. |

A claim proved only in the book's Lean is marked **derived (book Lean)**:
derived from the same admitted definitions, but checked by the book's
script rather than by Genesis's build. The book's Lean lives inside Python
scripts, not `.lean` files, so that it stays out of Genesis's Lean census
and toolchain tests.

Each unit that makes a computational point has a script in `checks/` that
runs Genesis's own Python. Run it from the repository root:

```
python textbook/checks/u01_genesis_underivable.py
```

From Unit 04 on, each unit also has a `checks/uNN_lean.py` holding its
Lean (book) source and the axiom report it expects. These scripts share
the runner `checks/booklean.py`, which writes the source to a temporary
file, runs `lake env lean` inside `lean4/` (or a given Lean binary with
`--lean PATH --lean-path DIR`), prints the `#print axioms` lines, and exits
0 only when every report matches. A unit's Verification table records
what each script found when it was written.

## Notation

The book writes ⟨⟩, ⟨A⟩, ⟨AB⟩ for the seed's `<>`, `<a>`, `<ab>`. Inside
Lean there are no letters, only numbered data (datum 0, datum 1, ...). ⟨AA⟩
is not in Genesis; the book uses it only as an example of a fresh token.
The letter A in ⟨A⟩ is unrelated to the candidate labels `A1`–`A5` in
`PrimDiff.lean`.

⟨ARA⟩ (A related to itself) and ⟨ARB⟩ (A related to B) are informal
inscriptions, not Genesis objects. Written down alone, ⟨ARA⟩ is one more
opaque whole and establishes no internal difference: nothing inside it is
licensed to see two endpoints, an R, or a repeated A. Units 19 and 20 use
two **later formal realizations** of them, each built from extra
admissions. (Units 23 to 25 work with an abstract relation `r` in
`PrimDiff.lean`, not with a regime, and carry their own hypotheses.)

| Inscription | Realization | What the realization admits beyond the inscription |
|---|---|---|
| ⟨ARB⟩ | `Minimality.BL` (binary link) | two data, one binary form, the instance (form 0, [datum 0, datum 1]), and the externally imposed demand that datum 0 and datum 1 be separated |
| ⟨ARA⟩ | `Minimality.BD` (binary self-loop) | two data, one binary form, the instance (form 0, [datum 0, datum 0]), and the same demand |

```lean
-- Lean (Genesis), lean4/Derivation/Minimality.lean lines 42-44
def BL : Regime := ⟨2, [2], [(0, [0, 1])], [], [(0, 1)]⟩
def BD : Regime := ⟨2, [2], [(0, [0, 0])], [], [(0, 1)]⟩
```

So `Minimality.BD_separable` (Unit 20) does not say that writing ⟨ARA⟩
separates anything. It says that in the regime `BD`, the context "form 0
with datum 0 in the second slot" holds when datum 0 fills the hole and fails
when datum 1 does, so the regime distinguishes the two data. Every later
mapping from informal notation to a Genesis structure lists the admissions
it needs, as this table does.

## No imports from nowhere

This is a standing rule of the book (author, 2026-10-28). Nothing enters the
system unless it is derived inside the system or admitted at a stated price.
In particular, the book never brings in from nowhere:

- an **observer**: a viewpoint, reader, measurer or classifier that the
  system has not admitted;
- a **container**: a background space, set, universe or totality in which
  the system's things are supposed to sit;
- a **continuum**, or any **infinity**: an infinite set of data, of
  instances, of presentations, of presentation families, of observers, or an
  unbounded supply of any of them;
- an **empty thing** treated as present: "the empty set", "the space of all
  possibilities", or a limit that has not been reached.

The system is never allowed past where it is. At each step it has exactly
what has been admitted so far: a finite ledger, built by a finite history of
events. What has not been derived or admitted is not "there but unknown"; it
is not there.

**Lean is outside the system.** Lean's types (`Nat`, `List`, `Prop`,
`Type`), its quantifiers (`∀`, `∃`), its equality and its proof checker
belong to the declared metatheory (`paper/paper.md` §2; Unit 00). `Nat` has
no largest element and `List Nat` has no longest list, but that is a fact
about the metatheory's apparatus, not something the system possesses. When
a theorem says "for every instance `i : Inst`", it is a genuine universal
statement, proved once and uniformly for an arbitrary instance; it is not a
collection of separate checks. What matters is where that quantifier lives:
it ranges over a Lean type, so it is a statement the metatheory makes
*about* the system. It puts no collection of instances, and no universal
quantifier, into the system's ledger. Every unit that discusses a universal
theorem keeps those two apart: the theorem's own quantifier, at full
strength, and what the system has admitted.

**A finite ledger does not bound what its definitions reach.** The ledger
stores finitely many admitted items, but an admitted definition can have an
unbounded extension when the metatheory reads it. The uniform rule is the
first case. In the well-formed regime `⟨0, [1], [], [0], []⟩` (one unary
form, the all-instances rule on it, no data, no instances),
`derivable` holds of `(0, [99])`, though datum 99 was never admitted, and
of `(0, [])` and `(0, [1, 2, 3])`, though form 0 has arity 1 (Unit 01;
`checks/u01_rule_extension.py`). Nothing infinite is stored: the rule is one
admitted item, a form number in a list. The unbounded part is the
metatheory's reading of `derivable`, and a unit that uses it says so. If a
later unit needs derivability restricted to admitted data, it introduces a
separate, named predicate outside the seal rather than reading the
restriction into the sealed one.

So every unit has a section **Outside the system** that lists:

1. each Lean type, quantifier or construction the unit uses that is
   metatheory, and what it is used for;
2. what the system itself holds at that point (always a finite ledger),
   and, where a definition's extension read in Lean is unbounded, that it
   is;
3. any admission the unit relies on, with its price (the events or
   hypotheses it needs);
4. any phrase in the unit that would import an observer, container or
   infinity if read as a claim about the system, and how to read it
   instead.

If a later unit needs something unbounded inside the system, it must either
derive it or admit it as a named, priced admission, and the unit must say
which.

## Unit template

1. **Claim**, with its status mark and its Lean name.
2. **What you need first**: the admitted definitions the claim depends on,
   each in Lean, then Python, then gloss. Every unit names them; no theorem
   is stated without them.
3. **The theorem** in Lean.
4. **The proof, step by step**, with no step skipped.
5. **The same fact in Python**, with the check script.
6. **Outside the system**: the metatheory's types and quantifiers the unit
   uses, what the system holds, and the price of every admission (see No
   imports from nowhere).
7. **What it shows and what it does not.**
8. **Sources**: file, theorem, axiom report, ledger entry, test.

Units 00 to 03 follow this eight-part template. From Unit 04 on, by the
author's brief of 2026-10-28, each unit keeps the **Claim** header (status,
Lean name, axioms, dependencies) and then runs through fifteen fixed
sections in this order: Question; What we already possess; New concept;
Plain-language interpretation; Pseudocode; Python; Line-by-line Python
explanation; Lean 4; Line-by-line Lean explanation; What has been proved;
What has not been proved; Outside the system; Student exercise; Answer;
Verification. The two templates carry the same obligations: the admitted
definitions are named before the theorem, no proof step is skipped, the
metatheory is listed under Outside the system, and the Verification table
plays the part of Sources. The sections were not mixed: a unit is written
in one template or the other, and this table says which.

| Units | Template |
|---|---|
| 00–03 | eight parts, above |
| 04 onward | Claim header plus the fifteen sections |

## Contents

| Unit | Claim | Lean | Status | Written |
|---|---|---|---|---|
| 00 | The mark and the external constructor | (none; seed §1, paper §2) | admitted | yes |
| 01 | Nothing is derivable at genesis | `Inertia.genesis_underivable` | derived | yes |
| 02 | Nothing is derivable without instances or rules (and one admitted rule makes unadmitted instances derivable) | `Inertia.underivable_of_empty` | derived | yes |
| 03 | Supplying a token changes nothing | `Inertia.supply_no_op` | derived | yes |
| 04 | No successor is internally forced (by the declared grammar) | (none; paper §4) | admitted | yes |
| 05 | Is ⟨⟩ admitted? Readings L and F | `Inertia.historyL_replays`, `historyF_replays` | open | yes |
| 06 | Re-admitting a token designates, it does not add | `Erasure.stepT` | admitted | yes |
| 07 | Forgetting tokens loses nothing the room can use | `Erasure.erase_replay` | derived | yes |
| 08 | Contexts, plugging, collapsed, separable | `Basic.collapsed`, `Basic.separable` | admitted | yes |
| 09 | Separable and collapsed exclude each other | `Basic.separable_not_collapsed` | derived | yes |
| 10 | With no instances, every pair is collapsed | `Inertia.collapsed_of_no_insts` | derived | yes |
| 11 | One token gives at most one datum | `Bridge.single_token_carrier_bound` | derived | yes |
| 12 | A fresh datum adds no power | `Inertia.admission_without_expressive_increase`, `Mention.collapsed_fresh_datum` | derived | yes |
| 13 | Two data need a second, different token | `Bridge.second_token_required` | derived | yes |
| 14 | Factoring through a point is equality | `PrimDiff.factors_through_point_iff` | derived | yes |
| 15 | An outside difference is not an asserted one | `PrimDiff.meta_diff_without_assertion` | derived | yes |
| 16 | ⟨A⟩ and ⟨AB⟩ are collapsed | `Inertia.R2L_collapsed`, `R2F_collapsed` | derived | yes |
| 17 | Demands are irreflexive by guard | `Basic.stepE` (impose) | admitted | yes |
| 18 | One item never answers the demand | `Minimality.cost1_insufficient_general` | derived | yes |
| 19 | The link regime `BL` (realizing ⟨ARB⟩) separates | `Minimality.BL_separable` | derived | yes |
| 20 | The self-loop regime `BD` (realizing ⟨ARA⟩) separates | `Minimality.BD_separable` | derived | yes |
| 21 | The cheapest answer is not unique under mu1 | `Minimality.mu1_minimum_not_unique` | derived | yes |
| 22 | It is unique under mu2 | `Minimality.mu2_unique` | derived | yes |
| 23 | A related pair r a b alone does not give a ≠ b (countermodel) | `PrimDiff.selfdiff_consistent` | derived | yes |
| 24 | Under irreflexivity, r a b gives a ≠ b | `PrimDiff.irrefl_witness_ne` | conditional | yes |
| 25 | Under irreflexivity, collapsing a related pair is obstructed | `PrimDiff.obstruction_under_irrefl` | conditional | yes |
| 26 | Facts never entail the irreflexivity law | `Bridge.irrefl_law_not_entailed` | derived | yes |
| 27 | An abstraction cannot see what it identifies | `Quot.quot_barrier`, `Quot.barrier_R2L` | derived | yes |
| 28 | Closure over fixed data must stop within n(n-1)/2 rounds | `Counting.strict_bounded_length`, `Counting.allPairs_length`, `Counting.no_supply_round_bound` | derived / conditional | yes |
| 29 | Renaming the data changes nothing a context can see | `CountTransport.collapsed_rename`, `CountTransport.non_injective_does_not_transport` | derived | yes |
| 30 | A context that reaches outside the regime separates nothing | `Mention.collapsed_append_unmentioning`, `Mention.collapsed_fresh_form` | derived | yes |
| 31 | Renaming carries every transition; index-least selection is not congruent | `TransitionTransport.transStep_rename_fwd`, `TransitionTransport.least_pair_selection_not_congruent` | derived | yes |
| 32 | The same proof with one more datum | `MinimalityF.mu2_unique_F`, `MinimalityF.genesis_mark_not_separable` | derived | yes |
| 33 | A rule never pays for itself | `RuleBridge.applyDelta_dropRules`, `RuleBridge.rule_item_never_minimal` | derived | yes |
| 34 | How many demands can a closed system meet? | `Rounds.round_reqs_succ`, `Rounds.closedRun_round_bound_from_empty` | derived under the declared round shape | yes |

The order follows the derivation. Units 27-34 follow the root import order
of `lean4/Derivation.lean` (Quot, Counting, CountTransport, Mention,
TransitionTransport, MinimalityF, RuleBridge, Rounds); units after 34
continue with Progress, Ext and ObserverInventory.

## Parts

| Part | Folder | Teaches |
|---|---|---|
| 1 | `textbook/units/` | the sealed derivation, from the mark forward (the contents table above) |
| 2 | `textbook/institutions/` | actors, institutions, information, knowledge, authorization and acquisition: the research trees `two_theorems` and `actor_institution`, outside the seal, with their own README and contents table |
