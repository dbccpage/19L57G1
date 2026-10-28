# Audit: Counting

| field | value |
|---|---|
| Path | lean4/Derivation/Counting.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 6db7f0d5a8528ead |
| Lines | 86 |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.Basic |
| Declarations | 1 def, 4 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 4 lines; axioms seen: propext+Quot.sound (all four) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
Counting states the abstract termination law behind the closed-system (no-supply) variant of pair-separation closure: a measure that strictly increases every round and never exceeds a bound `B` admits at most `B+1` rounds. It instantiates the bound at the number of unordered pairs of `n` data, and defines the requirement language of a regime with `n` data (`allPairs n`, the ordered pairs `i < j < n`) and proves it has exactly `n(n-1)/2` elements, stated division-free. The module is explicit that the law is conditional on the hypotheses about the measure; connecting those hypotheses to the transition system is done later in Rounds (`ClosedRun`), not here.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `allPairs` | 61 | def | `allPairs 0 = []`, `allPairs (n+1) = allPairs n ++ (range n).map (·, n)`: all `(i, j)` with `i < j < n` | ADMITTED (the declared requirement language) |

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `index_le_strict_mono` | 15 | if `f : Nat → Nat` satisfies `f i < f (i+1)` for all `i+1 < L`, then `i ≤ f i` for all `i < L` | CONDITIONAL: `hstrict` (a law about an arbitrary measure) | propext, Quot.sound | A |
| `strict_bounded_length` | 30 | if additionally `f i ≤ B` for all `i < L`, then `L ≤ B + 1` | CONDITIONAL: `hstrict`, `hbound` | propext, Quot.sound | S |
| `no_supply_round_bound` | 53 | same with `B = n*(n-1)/2`: `L ≤ n*(n-1)/2 + 1` | CONDITIONAL: `hstrict`, `hbound` (docstring itself says "Conditional") | propext, Quot.sound | S |
| `allPairs_length` | 69 | `2 * (allPairs n).length = n * (n - 1)` for every `n` | FROZEN | propext, Quot.sound | S |

## 4. External and admitted assumptions
- Hypotheses recurring: strict growth of a `Nat`-valued measure along a run and its boundedness; both are premises, not proved here for the engine.
- `Nat → X` as data: `f : Nat → Nat` is the run's measure sequence, indexed by round. This is metatheory (an auditor's sequence), and the docstring says so ("a Lean theorem connecting the hypotheses to the transition system itself is not proved here"). Not read as internally available.
- Library lemmas: `omega`, `List.length_append`, `List.length_map`, `List.length_range`. No Mathlib.
- Universe parameters: none.
- Unearned identity / unrestricted universe / silent observer / presentation correspondence / cost / admitted-as-forced: none found.
- Finite computation presented as universal: none; the laws are general and the paper tags them "conditional abstract laws".

## 5. Derived consequences
Rounds uses `strict_bounded_length`, `no_supply_round_bound`, `allPairs` and `allPairs_length` to prove `closedRun_round_bound` and `closedRun_round_bound_from_empty` (the discharge of `hstrict`/`hbound` for `ClosedRun`-shaped runs). `allPairs_length` is cited for CL-CLOSURE-FIXPOINT ("the requirement language has exactly n(n-1)/2 elements") and paper 9.6, 10.7, 10.8.

## 6. Counterexamples and limitations
No countermodels. The module does not prove that the engine's rounds satisfy `hstrict`/`hbound`; the docstring of `no_supply_round_bound` says that is "discharged computationally for the exported runs". Rounds later discharges it for a declared syntactic round shape only (see Rounds audit). `allPairs_length` counts the list; that imposed requirements are a duplicate-free subset of `allPairs` is proved in Rounds, not here. Nothing about termination *with* supply is claimed (paper 10.7 keeps unboundedness [unresolved]).

## 7. Axiom dependencies
All four: propext, Quot.sound (from `omega`/`simp`). None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All four in the artifact (root lines 92–95). Paper 9, 10.7, 10.8 and ledger CL-CLOSURE-TERMINATION / CL-CLOSURE-FIXPOINT cite them. Probe: `#check Derivation.no_supply_round_bound` (probes/A/probe1.lean) printed the signature reproduced in section 3.

## 9. Related Python implementations
`code/derivation/engine.py` (closed-system run, `supply=False`), `code/derivation/observe.py::collapsed_pairs` (the pairs language). Tests: `tests/test_engine.py::test_no_supply_variant_terminates_within_pair_bound`, `::test_closure_policy_fixpoint`, `::test_closed_system_terminal_at_round_boundary` (ledger).

## 10. Textbook placement proposal
- Prerequisites: Basic (`reqs`); elementary induction on `Nat`.
- Substantive: `strict_bounded_length` (the law) and `allPairs_length` (the language size). Auxiliary: `index_le_strict_mono`, `no_supply_round_bound` (a specialisation).
- Lesson title: "Why closure without supply must stop". Question: how many separation rounds can a closed regime with `n` data accept?
- Omit: `index_le_strict_mono` as a displayed theorem; present `no_supply_round_bound` as the instance of the law at `B = n(n-1)/2`.

## 11. Interpretation findings
- Paper 10.7: "**[bounded theorem]** without it pair-separation closure terminates within n(n-1)/2 rounds (sections 8.5, 9)". The Lean in this module proves only the abstract law under `hstrict`/`hbound`; the system-level statement is proved in Rounds only for `ClosedRun`-shaped runs, and the ledger (CL-CLOSURE-TERMINATION) says "what remains computational is … that each EXPORTED round has the declared syntactic shape". The paper's "[bounded theorem]" tag and the ledger's scoping agree; the docstring of `no_supply_round_bound` ("a closed-system run … has at most n(n-1)/2+1 states") reads slightly stronger than its statement but immediately says "Conditional". None found beyond this scoping note.
- Finitude: `f : Nat → Nat` is an auditor's measure sequence, not system content; no prose reads it otherwise. None found.
- Vacuity: `hstrict`/`hbound` are jointly satisfiable (e.g. `f = id`, `L = B+1`); conclusions are non-trivial.
