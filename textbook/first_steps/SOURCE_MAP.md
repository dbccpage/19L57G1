# Source map and assumptions

AuthorityEffect: None. These are pedagogical examples outside the seal.
All source paths below are consumed read-only. The teaching model creates
no new event, theorem, or physical interpretation inside the sealed system.

## What each lesson uses

| Lesson | Supplied teaching operation | Existing definitions and results |
|---|---|---|
| 00 | Rename a display label while holding answer tables fixed | Unit 00's external constructor; `Supply` in `code/derivation/model.py`; token erasure in Unit 07 and `lean4/Derivation/Erasure.lean` |
| 01 | Compare one explicit boolean answer on two listed items | `contexts`, `plug`, `derivable`, `profile`, `separable`, `witness` in `code/derivation/observe.py`; `Ctx`, `wfCtx`, `collapsed`, `separable` in `lean4/Derivation/Basic.lean` |
| 02 | Compare complete patterns on a chosen finite question list | `Compression.sigList`, `SigEq`, `sigEq_iff_sigList`, `pQ_exact` in `lean4/Derivation/Compression.lean` |
| 03 | Append a question, or replace one, in a supplied fixed table | `Compression.enlarge_refines`, `splits_iff_new_separator`; the loss example is a finite book calculation |
| 04 | Recover one supplied question from the recorded pattern | `Compression.FiberConstant`, `FactorsOn`, `factors_iff_fiberConstant`, `descent_witness`; `Institution.knows_iff_determined` in `research/two_theorems/lean/ResearchTwoTheorems/Institution.lean` |

The full formal lessons remain Units 00, 03, 07–09, 19–20, 61 and
Institutions 00–02, 06 and 16. The first-steps route prepares those lessons;
it does not replace their exact hypotheses or scientific scope.

## A declared finite correspondence

The default teaching carrier is the three positions 0, 1, 2. Display names
A, B, C refer to them. Each selected question has one explicit boolean
answer per position. To read the question as a `Nat → Nat` presentation
on that carrier, encode false as 0 and true as 1. Values outside the
three-position carrier are not part of the teaching table.

This gives a list of numerical presentations on a supplied finite domain
of the kind used by `Compression`. The signature definition and the
factorization theorem keep their source meaning: `FactorsOn D p q`
means that **q is recovered from p**, on `D`.

For the unary-form encoding checked by `checks.py`:

1. Admit exactly three distinct datum tokens, in order.
2. For each selected question, admit one form of arity one.
3. Admit its unary instance exactly at positions whose supplied answer
   is true. Admit no uniform rules and no additional facts.
4. Compare all resulting well-formed unary contexts, derivability checks,
   profiles, pair separations, and returned witnesses with the table.

This is an executable finite correspondence for the stated encoding.
It is not a general Python-to-Lean refinement proof. In particular, a
display rename is not replayed as a new sealed event.

## Answers and positive derivability

In the teaching table, both yes and no are supplied answers. In the unary
encoding, yes corresponds to derivability of the supplied positive
instance; no corresponds to absence of derivability under the declared
rule-free ledger. This does not encode a separately proved negative fact.
The encoding's complete answer table is our metatheoretic apparatus.

The well-formed-context restriction is essential. The sealed raw
`derivable` predicate is broader when uniform rules are admitted; the
first-steps encoding admits no such rules and does not change that predicate.

## What was admitted

- The three-position carrier, labels, colors, shapes, and answer tables.
- The list of selectable questions, their order, and the requested answer.
- The operation of retaining an old table while appending a question.
- The finite recovery task: one answer rule must work for every listed item.
- The implementation language, arrays, booleans, and all validation/checking
  apparatus used outside the represented teaching machine.

No observer, container, indefinite supply, physical measuring rule, or
interpretation is inferred from the seed mark. The card appearance is a
supplied visual aid. A real-world application needs a separately tested
correspondence between a device's responses and the target measurement.

## Verification reach

The JavaScript model is checked on the default example and all 64
two-question boolean tables on three items. Recovery is compared with
independent enumeration of all lookup rules on each table's observed
patterns. The Python check compares each of those 64 tables, under all
four selected-question subsets, with the sealed unary encoding.

These checks establish finite computational agreement in the declared
population. Human prediction, explanation, transfer, and delayed retention
remain separate evidence to collect with the reader checks.
