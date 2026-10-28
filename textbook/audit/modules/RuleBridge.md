# Audit: RuleBridge

| field | value |
|---|---|
| Path | lean4/Derivation/RuleBridge.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 909ac832299f4b2f |
| Lines | 268 |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.Progress, Derivation.TransitionTransport, Derivation.Minimality |
| Declarations | 1 def (`dropRules`), 8 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 8 lines, all propext |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
RuleBridge closes residual R4: the enumeration prunes every delta containing a uniform-rule item, and Progress had only proved witness transfer under a shrunken final rule set, leaving the step from delta items to rule sets to a Python test. The module observes that no guard of `applyItem` reads the rule store and only `newRuleAll` writes it, so dropping the rule items of a delta yields a delta that applies over any replacement rule field and produces the same regime except for `rules`. Combined with rule monotonicity (admission never removes a rule) and `separable_of_subrules`, a valid response stays valid after the drop, strictly shorter and with the same new-form arity sum. Hence a rule item never occurs in a minimum under `mu1` or `mu2`.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `dropRules` | 40 | def | remove every `newRuleAll` item from a delta, keeping order | ADMITTED |

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `applyItem_rules_mono` | 46 | if `applyItem r it = some s` then every rule of `r` is a rule of `s` | FROZEN | propext | A |
| `applyDelta_rules_mono` | 75 | same for `applyDelta r δ = some s` | FROZEN | propext | A |
| `applyDelta_dropRules` | 100 | if `applyDelta r δ = some s` then for ANY rule list `rs`, applying `dropRules δ` to `r` with rules `rs` gives `s` with rules `rs` | FROZEN | propext | S |
| `dropRules_length_le` | 183 | `(dropRules δ).length ≤ δ.length` | FROZEN | propext | A |
| `dropRules_length_lt` | 195 | if some `newRuleAll f ∈ δ` then the drop is strictly shorter | CONDITIONAL: `newRuleAll f ∈ δ` | propext | A |
| `aritySum_dropRules` | 225 | `aritySum (dropRules δ) = aritySum δ` | FROZEN | propext | A |
| `validResponse_dropRules` | 245 | `validResponse r i j δ → validResponse r i j (dropRules δ)` (uses the bridge at `rs := r.rules`, monotonicity for the subset, then `separable_of_subrules` for the target and each imposed requirement) | FROZEN | propext | S |
| `rule_item_never_minimal` | 259 | if `newRuleAll f ∈ δ` and `δ` is a valid response, then its drop is valid, strictly shorter, with equal `aritySum` | CONDITIONAL: `newRuleAll f ∈ δ` (the premise is the claim's scope) | propext | S |

## 4. External and admitted assumptions
- Takes the definitions of `applyItem`/`applyDelta` (Basic) and `aritySum` (Minimality) and the theorem `separable_of_subrules` (Progress). The inference "shorter with equal arity sum ⇒ smaller under `mu1` and under lexicographic `mu2`" is made in the docstring, not in Lean (no `mu1`/`mu2` are defined in Lean; they are the declared Python measures).
- Hypotheses: a rule item in the delta; a successful application.
- Library lemmas: `List.mem_cons`, `Nat.*` order lemmas, `mem_insertNew` (Basic). Core only.
- Universe parameters: none. `Nat → X` as data: none.
- Unearned identity / unrestricted universe / unbounded internal function / silent observer / presentation correspondence / cost (the measures are declared elsewhere; here only length and arity sum are compared) / admitted-as-forced / finite-as-universal: none found.

## 5. Derived consequences
No other Lean module uses these names (grep: only RuleBridge itself). Ledger CL-PRUNE-RULE (ii) and paper 8.3 / register row R4 ("DISCHARGED 2026-08-18") rest on `rule_item_never_minimal`; `paper/representative_selection.md` cites it as the proved pruning licence.

## 6. Counterexamples and limitations
No countermodels. Not proved: that the Python enumeration actually applies this prune correctly (that is `test_rule_never_appears_in_minimum_responses`); the lexicographic `mu2` comparison itself (prose). The result says nothing about rule items in NON-minimal responses (they are valid; only their minimality is excluded). The docstring's "under either declared measure" is correct for `mu1` and `mu2` as declared; no other measure is covered.

## 7. Axiom dependencies
All eight propext. None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All eight in the artifact. Paper 8.3, register R4, ledger CL-PRUNE-RULE cite them. No extra probe.

## 9. Related Python implementations
`code/derivation/candidates.py` (`iter_cost2_deltas` prunes `NewRuleAll`; `min_responses`); tests `tests/test_candidates.py::test_rule_never_appears_in_minimum_responses`, `::test_pruned_cost2_contains_every_valid_full_delta`.

## 10. Textbook placement proposal
- Prerequisites: Basic (`applyItem`, `validResponse`), Progress (`separable_of_subrules`), the declared measures.
- Substantive: `applyDelta_dropRules`, `validResponse_dropRules`, `rule_item_never_minimal`. Auxiliary: the monotonicity and length/arity lemmas.
- Lesson title: "A rule never pays for itself". Question: can the enumeration skip every delta that imposes a uniform rule without missing a minimum?
- Omit: nothing; the auxiliary lemmas are one line each.

## 11. Interpretation findings
- Paper 8.3 / ledger CL-PRUNE-RULE (ii): "a delta containing a uniform-rule item is never a minimum valid response under either declared measure". Lean gives: valid drop, strictly shorter, equal `aritySum`. The step to "never a minimum under `mu2`" needs that `mu2` is lexicographic (length first), which is the Python definition; it is not formalised. INTERPRETATION DEFECT (minor: the measure comparison is prose over a declared measure, not a Lean conclusion; no counterexample, since `mu2 = (len, aritySum)` is indeed lexicographic in `candidates.py`).
- Progress's `separable_of_subrules` docstring ("certified computationally, not proved here") is superseded by this module; recorded under Progress.
- Vacuity: `rule_item_never_minimal`'s hypotheses are satisfiable (e.g. `deltaU0 ++ [newRuleAll 0]` on `R2L` after the form exists — not checked by probe; the existence of SOME valid delta with a rule item follows from `applyItem_rules_mono` plus `mark_progress`'s delta extended by a rule on a form that exists, which requires the form index guard `f < forms.length`; not verified in Lean here). Stated as "not checked" for a concrete witness.
- Finitude: none found.
