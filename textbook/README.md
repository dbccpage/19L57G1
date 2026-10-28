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

Every unit is written against `main` at
`23979a46308219b4cc9e7e172e4e32511f8efdb0` (2026-10-24). Lean is quoted from
`lean4/Derivation/`. Axiom reports are read from the committed
`artifacts/lean_axioms.txt`; a unit says so when it did not rebuild Lean.

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

## Three kinds of code

| Label | What it is | Trust |
|---|---|---|
| Lean (Genesis) | Copied from `lean4/Derivation/`. | Checked by Lean's kernel when Genesis builds. The authority. |
| Python (Genesis) | Copied from `code/derivation/`. | Tested in Genesis. Tied to the Lean by executable checks, not by proof (ledger entry `CL-TOKEN-ERASURE`). |
| Gloss | Pseudocode written for this book. | Unchecked. Read it as a translation aid only. |

Each unit that makes a computational point has a script in `checks/` that
runs Genesis's own Python. Run it from the repository root:

```
python textbook/checks/u01_genesis_underivable.py
```

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

## Unit template

1. **Claim**, with its status mark and its Lean name.
2. **What you need first**: the admitted definitions the claim depends on,
   each in Lean, then Python, then gloss. Every unit names them; no theorem
   is stated without them.
3. **The theorem** in Lean.
4. **The proof, step by step**, with no step skipped.
5. **The same fact in Python**, with the check script.
6. **What it shows and what it does not.**
7. **Sources**: file, theorem, axiom report, ledger entry, test.

## Contents

| Unit | Claim | Lean | Status | Written |
|---|---|---|---|---|
| 00 | The mark and the external constructor | (none; seed §1, paper §2) | admitted | yes |
| 01 | Nothing is derivable at genesis | `Inertia.genesis_underivable` | derived | yes |
| 02 | Nothing is derivable without instances or rules | `Inertia.underivable_of_empty` | derived | |
| 03 | Supplying a token changes nothing | `Inertia.supply_no_op` | derived | |
| 04 | No successor is internally forced (by the declared grammar) | (none; paper §4) | admitted | |
| 05 | Is ⟨⟩ admitted? Readings L and F | `Inertia.historyL_replays`, `historyF_replays` | open | |
| 06 | Re-admitting a token designates, it does not add | `Erasure.stepT` | admitted | |
| 07 | Forgetting tokens loses nothing the room can use | `Erasure.erase_replay` | derived | |
| 08 | Contexts, plugging, collapsed, separable | `Basic.collapsed`, `Basic.separable` | admitted | |
| 09 | Separable and collapsed exclude each other | `Basic.separable_not_collapsed` | derived | |
| 10 | With no instances, every pair is collapsed | `Inertia.collapsed_of_no_insts` | derived | |
| 11 | One token gives at most one datum | `Bridge.single_token_carrier_bound` | derived | |
| 12 | A fresh datum adds no power | `Inertia.admission_without_expressive_increase`, `Mention.collapsed_fresh_datum` | derived | |
| 13 | Two data need a second, different token | `Bridge.second_token_required` | derived | |
| 14 | Factoring through a point is equality | `PrimDiff.factors_through_point_iff` | derived | |
| 15 | An outside difference is not an asserted one | `PrimDiff.meta_diff_without_assertion` | derived | |
| 16 | ⟨A⟩ and ⟨AB⟩ are collapsed | `Inertia.R2L_collapsed`, `R2F_collapsed` | derived | |
| 17 | Demands are irreflexive by guard | `Basic.stepE` (impose) | admitted | |
| 18 | One item never answers the demand | `Minimality.cost1_insufficient_general` | derived | |
| 19 | The link regime `BL` (realizing ⟨ARB⟩) separates | `Minimality.BL_separable` | derived | |
| 20 | The self-loop regime `BD` (realizing ⟨ARA⟩) separates | `Minimality.BD_separable` | derived | |
| 21 | The cheapest answer is not unique under mu1 | `Minimality.mu1_minimum_not_unique` | derived | |
| 22 | It is unique under mu2 | `Minimality.mu2_unique` | derived | |
| 23 | A related pair r a b alone does not give a ≠ b (countermodel) | `PrimDiff.selfdiff_consistent` | derived | |
| 24 | Under irreflexivity, r a b gives a ≠ b | `PrimDiff.irrefl_witness_ne` | conditional | |
| 25 | Under irreflexivity, collapsing a related pair is obstructed | `PrimDiff.obstruction_under_irrefl` | conditional | |
| 26 | Facts never entail the irreflexivity law | `Bridge.irrefl_law_not_entailed` | derived | |

The order follows the derivation. Units after 26 continue with the map of
Genesis from the mention lemma onward.
