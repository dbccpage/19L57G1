# Audit: Basic

| field | value |
|---|---|
| Path | lean4/Derivation/Basic.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 1520b392f4061af5 |
| Lines | 217 |
| Imported by root `Derivation.lean` | yes (first import) |
| Imports | none (Lean core only; no Mathlib) |
| Declarations | 1 abbrev, 15 def, 2 structure, 2 inductive, 3 instance, 7 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 1 line (`separable_not_collapsed`: propext); the six other theorems are not in the artifact |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
Basic declares the whole object language of the sealed derivation in its token-erased form. A regime is the admitted state: a count of admitted data (identity is the index), a list of judgment-form arities, admitted instances, forms carrying the uniform all-tuples rule, and imposed separation requirements. It declares what it means for a context (a form with holes) to observe a datum (`plug`), what is derivable (membership in admitted instances, or coverage by an all-tuples rule — nothing else), and the two declared senses that the rest of the programme turns on: observational collapse (no well-formed context tells two data apart) and internal separability (some well-formed context does, carried as a witness). It also declares the admission events, the all-or-nothing replay, the candidate augmentations (items and deltas), the notion of a valid response to a separation requirement, and the two Challenge 3 regimes `R2L` and `R2F`. Its one substantive theorem is that separability contradicts collapse, which is the constructive link between the two declared senses. Everything else in the module is admitted structure, deliberately: the paper's "declared metatheory" lives here.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `Inst` | 21 | abbrev | `Nat × List Nat`: a form index and an argument tuple of datum indices | ADMITTED |
| `insertNew` | 25 | def | deduplicating list insertion (`if a ∈ l then l else l ++ [a]`), modelling set-valued admitted collections | ADMITTED (declared policy: re-admission is idempotent, matching Python) |
| `Regime` | 53 | structure | `data : Nat`, `forms : List Nat`, `insts : List Inst`, `rules : List Nat`, `reqs : List (Nat × Nat)`; derives `DecidableEq` | ADMITTED (the declared state shape, paper C1) |
| `Regime.wf` | 64 | def | instances respect arity and datum bounds, rules name admitted forms, reqs are ordered pairs below `data`, every arity ≥ 1 | ADMITTED (a predicate, NOT enforced by the structure) |
| `Ctx` | 74 | structure | a form index and a slot list where `none` is a hole | ADMITTED |
| `plug` | 80 | def | fill every hole of a context with the same datum | ADMITTED |
| `derivable` | 85 | def | `i ∈ r.insts ∨ i.1 ∈ r.rules`; docstring: "No other inference is admitted" | ADMITTED (declared derivability) |
| instance `Decidable (derivable r i)` | 88 | instance | by unfolding | ADMITTED |
| `slotOk` | 92 | def | hole, or a datum index below `n` | ADMITTED |
| instance `Decidable (slotOk n s)` | 96 | instance | by cases | ADMITTED |
| `wfCtx` | 106 | def | form admitted, slot count = arity, at least one hole, filled slots admitted | ADMITTED (the "at least one hole" clause is a declared choice matching the Python enumeration) |
| instance `Decidable (wfCtx r c)` | 112 | instance | by unfolding | ADMITTED |
| `collapsed` | 117 | def | every well-formed context gives the same derivability for `d` and `d'` | ADMITTED (declared sense of collapse) |
| `separable` | 123 | def | some well-formed context separates `d`, `d'` by derivability (existential, witness-carrying) | ADMITTED (declared sense, paper 3.5) |
| `Event` | 134 | inductive | `supply token`, `admitDatum`, `admitForm`, `admitInst`, `admitRuleAll`, `impose i j` | ADMITTED |
| `stepE` | 145 | def | one admission step; `none` on ill-formed admissions; `supply` returns the regime unchanged | ADMITTED (the declared admission semantics) |
| `replayE` | 166 | def | `foldlM stepE`; one ill-formed event poisons the whole history | ADMITTED |
| `Item` | 171 | inductive | `newDatum`, `newForm`, `newInst`, `newRuleAll` (candidate augmentations) | ADMITTED |
| `applyItem` | 178 | def | same clauses as the four admission events of `stepE` | ADMITTED |
| `applyDelta` | 192 | def | `foldlM applyItem` | ADMITTED |
| `validResponse` | 198 | def | the delta applies, the result separates the target and keeps every previously imposed requirement separated | ADMITTED (declared acceptance criterion) |
| `R2L` | 208 | def | `⟨2, [], [], [], [(0,1)]⟩`, reading L | ADMITTED |
| `R2F` | 209 | def | `⟨3, [], [], [], [(1,2)]⟩`, reading F | ADMITTED |

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `insertNew_nil` | 28 | `insertNew [] a = [a]` (by `rfl`, `@[simp]`) | FROZEN | not in artifact | A |
| `insertNew_of_not_mem` | 31 | if `a ∉ l` then `insertNew l a = l ++ [a]` | FROZEN | not in artifact (probe: propext) | A |
| `insertNew_of_mem` | 35 | if `a ∈ l` then `insertNew l a = l` | FROZEN | not in artifact (probe: propext) | A |
| `mem_insertNew` | 40 | `x ∈ insertNew l a ↔ x ∈ l ∨ x = a` | FROZEN | not in artifact (probe: propext) | A |
| `separable_not_collapsed` | 128 | for any regime and data, `separable r d d' → ¬ collapsed r d d'` | FROZEN | propext | S |
| `R2L_wf` | 211 | `R2L.wf` | VERIFIED_FINITE (simp on a concrete regime) | not in artifact (probe: propext, Quot.sound) | A |
| `R2F_wf` | 214 | `R2F.wf` | VERIFIED_FINITE | not in artifact (probe: propext, Quot.sound) | A |

## 4. External and admitted assumptions
- Structures: `Regime`, `Ctx`, `Event`, `Item` are the declared grammar. `Regime` does not carry `wf`; any theorem over "all regimes" ranges over ill-formed ones too unless it takes `wf` as a hypothesis (several downstream modules do).
- Declared policies: deduplicating admission (`insertNew`); the uniform all-tuples rule (`derivable` ignores the argument tuple whenever the form is in `rules`, including tuples of the wrong length); contexts must have at least one hole; replay is all-or-nothing.
- Library lemmas doing work: `List.mem_append`, decidable `∈` on lists (`DecidableEq` instances). No Mathlib.
- Universe/Type parameters: `insertNew` and its lemmas are polymorphic in `α : Type` with `DecidableEq`; only instantiated at `Inst`, `Nat`, `Nat × Nat`.
- Functions `Nat → X` treated as data: none. `data : Nat` is a count (metatheory), and `Event.supply (token : Nat)` carries a label that `stepE` discards.
- Unearned identity: none found (identity of data is by index, declared).
- Unrestricted external universe: none found.
- Unbounded function treated as internally available: none found. `collapsed` quantifies over all `Ctx` (an unbounded Lean type) but restricts by `wfCtx`, which makes the contexts of a regime finite; this is a metatheoretic quantifier, not an internal totality.
- Silently assumed observer: the context is the only observer and it is declared, not assumed.
- Unspecified correspondence between presentations: presentation tokens are absent by design; the token bridge is `Erasure.lean` (audited separately).
- Cost function without justification: none in this module (`mu1`/`mu2` live in Minimality).
- Admitted condition later described as forced: none found in this module.
- Finite computation presented as universal: none found; `R2L_wf`, `R2F_wf` are instance checks and are not cited as general.

## 5. Derived consequences
`insertNew` and `mem_insertNew` are used by Erasure, Ext, Rounds, RuleBridge, TransitionTransport. `separable_not_collapsed` is used by CountTransport, Minimality, MinimalityF and cited by the ledger (CL-3-FAIL-CURRENT). Every other Derivation module builds on the definitions here; `genesis` (Inertia) and `R2L`/`R2F` are the base regimes for Inertia, Minimality, MinimalityF, Refusal and others.

## 6. Counterexamples and limitations
No countermodels in this module. What it does not prove: that `stepE` rejects *every* ill-formed admission in some external sense (it rejects exactly the clauses written into it; the ledger's CL-0-NO-PROPOSAL-MUTATION cites "`stepE` totality with `Option` rejection", which is a property of the definition, not a theorem). `Regime.wf` is never shown to be preserved by `stepE`/`applyItem` in this module (preservation lemmas appear in TransitionTransport and Rounds under hypotheses).

## 7. Axiom dependencies
All within {propext, Quot.sound}. Artifact: `separable_not_collapsed` propext. Probe (this session): `R2L_wf`, `R2F_wf` propext + Quot.sound; the three `insertNew` lemmas propext; `insertNew_nil` is `rfl`. None exceed the whitelist.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). In the artifact: only `separable_not_collapsed`. Paper cites `separable_not_collapsed` (ledger CL-3-FAIL-CURRENT) and the `insertNew` lemmas (ledger line 570, token-erasure row). Probe run: `lake env lean probes/A/probe1.lean` with `#print axioms` on `R2L_wf`, `R2F_wf`, `mem_insertNew`, `insertNew_of_mem`; exit 0, outputs recorded above.

## 9. Related Python implementations
`code/derivation/model.py` (`Regime`, `Supply`, `AdmitDatum`, `AdmitForm`, `AdmitInst`, `AdmitRuleAll`, `Impose`, `step`, `replay`, `certify`); `code/derivation/observe.py` (`contexts`, `plug`, `derivable`, `profile`, `separable`, `witness`, `collapsed_pairs`); `code/derivation/candidates.py` (`NewDatum`…`NewRuleAll`, `apply_delta`, `response_valid_naive`/`response_valid_fast`). Tests: `tests/test_model.py`, `tests/test_observe.py`, `tests/test_candidates.py`.

## 10. Textbook placement proposal
- Prerequisites: none beyond lists and indices; this is lesson one of the formal track.
- Substantive: `Regime`, `derivable`, `Ctx`/`plug`/`wfCtx`, `collapsed`, `separable`, `separable_not_collapsed`, `stepE`/`replayE`, `Item`/`applyDelta`/`validResponse`, `R2L`/`R2F`. Auxiliary: `insertNew` and its four lemmas, `slotOk`, the `Decidable` instances, `R2L_wf`/`R2F_wf`.
- Lesson title: "What a regime can see". Question: what does it take, in this grammar, for two admitted data to be told apart?
- Omit from the textbook: the `insertNew` lemmas as theorems (explain dedup in one sentence); the `Decidable` instances.

## 11. Interpretation findings
- Vacuity check: `separable_not_collapsed` is non-vacuous (`separable` is satisfiable, e.g. Minimality's `U0_separable`). `collapsed` is satisfiable (Inertia). `wfCtx` is satisfiable only when some form has arity ≥ 1 and a hole is present; on `R2L`/`R2F` no context is well-formed, so `collapsed R2L d d'` holds vacuously for ALL `d d'` including indices ≥ `data` — the paper's reading "every pair of admitted data is collapsed" is correct but the Lean statement is strictly wider (no bound `d < r.data`). Not a defect; noted for lessons.
- Ledger CL-0-NO-PROPOSAL-MUTATION, class "theorem (model-scoped)", **Lean**: "`stepE` totality with `Option` rejection; `supply_no_op`". The Lean evidence for the rejection half is a definition (`stepE` returns `none` on its written ill-formed clauses); no theorem states it. The paper's section 4 already downgrades the forcing clause to [definition] (2026-09-08), but paper 10.2 still answers "[theorem] `supply_no_op` plus the structural fact". INTERPRETATION DEFECT (minor, scope stated elsewhere in the same paper).
- Finitude: `data : Nat` and `Event.supply (token : Nat)` are metatheoretic counts/labels; no docstring reads them as an internal infinity. None found otherwise.
