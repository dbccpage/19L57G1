# Audit: Progress

| field | value |
|---|---|
| Path | lean4/Derivation/Progress.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 9f49ca4646b68a93 |
| Lines | 237 |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.Basic, Derivation.Inertia |
| Declarations | 6 theorem (no definitions) |
| Axiom reports in `artifacts/lean_axioms.txt` | 2 lines (`mark_progress`: propext, Quot.sound; `separable_of_subrules`: propext). The four helpers are not in the artifact |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
Progress proves two things the engine relies on. First, response existence: in any well-formed regime whose imposed requirements are all separated, a supplied demand to separate two distinct admitted data `i`, `j` has a valid response — one fresh unary form plus one mark on `j` — and this response keeps every imposed requirement separated. The docstrings are emphatic that this is response existence only: it proves neither autonomous demand generation nor anything about the length of the process. Second, a pruning fact: a separation witness never inhabits a uniformly ruled form (a ruled form derives both plugs), so shrinking the rule set of a regime preserves every separation.

## 2. Definitions and structures
None.

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `old_inst_form_lt` | 22 | in a `wf` regime every instance's form index is below `forms.length` | CONDITIONAL: `r.wf` | not in artifact | A |
| `getD_concat_self` | 27 | `(l ++ [a]).getD l.length 0 = a` | FROZEN | not in artifact | A |
| `getD_append_lt` | 34 | `(l ++ l').getD i 0 = l.getD i 0` for `i < l.length` | FROZEN | not in artifact (the artifact's `Attachment.getD_append_lt` is a different module's lemma) | A |
| `derivable_extend` | 45 | for `wf` `r`, derivability in the fresh-mark extension agrees with `r` on every instance whose form is not the fresh one | CONDITIONAL: `r.wf`, `x.1 ≠ r.forms.length` | not in artifact | A |
| `mark_progress` | 75 | for `wf` `r`, `i j < r.data`, `i ≠ j`, and every imposed requirement separable in `r`: `[newForm 1, newInst r.forms.length [j]]` is a valid response to `(i,j)` | CONDITIONAL: `r.wf`, `i < data`, `j < data`, `i ≠ j`, `∀ q ∈ r.reqs, separable r q.1 q.2` | propext, Quot.sound | S |
| `separable_of_subrules` | 202 | if `rs' ⊆ s.rules` (as membership) and `separable s d d'`, then the regime with rules `rs'` still separates `d d'` | CONDITIONAL: `hsub` (subset) | propext | S |

## 4. External and admitted assumptions
- Recurring hypotheses: `Regime.wf`; the pre-state "all imposed requirements separated" (the engine's accepted-state invariant); distinct admitted targets.
- `mark_progress` fixes ONE concrete two-item delta; it does not quantify over the candidate grammar (docstring says so) and does not claim minimality.
- Library lemmas: `List.mem_append`, `List.getD` on `++`, `Nat.lt_irrefl`, `omega`. Core only.
- Universe parameters: none. `Nat → X` as data: none.
- Unearned identity / unrestricted universe / unbounded internal function / silent observer / presentation correspondence / cost / admitted-as-forced / finite-as-universal: none found.

## 5. Derived consequences
No other Lean module uses these theorems (RuleBridge re-proves what it needs on `dropRules` and cites `separable_of_subrules` only in prose/ledger). The ledger CL-PROGRESS rests on `mark_progress`; CL-PRUNE-RULE (i) on `separable_of_subrules`, with (ii) the delta-level bridge in RuleBridge. Paper 8.2, 8.3, 9, 10.7 cite `mark_progress`; paper 8.3 and register row R4 cite `separable_of_subrules`.

## 6. Counterexamples and limitations
No countermodels. Not proved: autonomous demand generation (CL-CLOSURE-POLICY says none was derived); any bound or unboundedness of the process; preservation of separations other than the imposed requirements (the preservation conjunct quantifies over `r.reqs` only — narrowed in the paper 2026-08-18); that the fresh-mark response is minimal (it is a two-item response; minimality is Minimality's business on the Challenge 3 base only). The `separable_of_subrules` docstring still says the delta-level bridge "is certified computationally, not proved here" — RuleBridge proved it on 2026-08-18, so the docstring understates (stale in the safe direction).

## 7. Axiom dependencies
`mark_progress` propext, Quot.sound; `separable_of_subrules` propext. Helpers probed (probe2.lean, exit 0): `old_inst_form_lt` propext; `derivable_extend` propext; `getD_append_lt` propext; `getD_concat_self` propext, Quot.sound. None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). Two theorems in the artifact (root lines 122–123). Paper and ledger cite both. No extra probe.

## 9. Related Python implementations
`code/derivation/engine.py` (response search; the engine assertion that no `terminal_no_response` node occurs), `code/derivation/candidates.py::min_responses`, `iter_cost1_items`. Tests: `tests/test_candidates.py::test_min_responses_cost1_path`, `::test_rule_never_appears_in_minimum_responses`.

## 10. Textbook placement proposal
- Prerequisites: Basic (`validResponse`, `wf`), Minimality (the unary mark as the canonical repair).
- Substantive: `mark_progress` (with its exact hypotheses and its "existence only" scope), `separable_of_subrules`. Auxiliary: the four helpers.
- Lesson title: "A demand can always be met". Question: given a well-formed regime that has met all its earlier demands, is there always some repair for the next supplied one — and what does that NOT say about where demands come from?
- Omit: `old_inst_form_lt`, `getD_*` helpers.

## 11. Interpretation findings
- Paper 10.7: "every supplied demand has a response (**[theorem]** `mark_progress`)". Lean requires `r.wf`, `i ≠ j` both admitted, and every imposed requirement already separated. Paper 8.2 and ledger CL-PROGRESS state these; the 10.7 summary drops them. INTERPRETATION DEFECT (minor: hypotheses omitted in a summary sentence; smallest counterexample to the unqualified reading: a regime with an imposed requirement that is NOT separated — the response is still a response to `(i,j)` but `validResponse` fails on that requirement; or `i = j`, where no context separates a datum from itself).
- Paper 8.2: "which moreover keeps every imposed requirement separated (the proved conjunct quantifies over the requirement store, not over all separable pairs …)". Exact.
- `separable_of_subrules` docstring vs RuleBridge: docstring says the delta-level corollary is "not proved here" and computational; it is now proved in RuleBridge (`applyDelta_dropRules`, `rule_item_never_minimal`). Stale understatement, not an overread. Not a defect by the brief's definition; recorded.
- Vacuity: `mark_progress` hypotheses satisfiable (`R2L` after one accepted round, or `U0` with `i=0,j=1`); conclusion is a specific witness. none found.
- Finitude: none found.
