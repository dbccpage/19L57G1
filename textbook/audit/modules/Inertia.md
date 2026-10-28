# Audit: Inertia

| field | value |
|---|---|
| Path | lean4/Derivation/Inertia.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | c62615cb3757474d |
| Lines | 94 |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.Basic |
| Declarations | 1 def, 10 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 10 lines; axioms seen: none, propext, propext+Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
Inertia answers Challenges 0–2 of the seed in the declared grammar: nothing follows from the initial inscription, supply is not admission, and before any judgment instance is admitted every pair of data is observationally collapsed. It states the genesis regime, shows a bare supply is literally the identity step, shows nothing is derivable in a regime with no instances and no rules, and proves the key collapse lemma: with no admitted instances derivability depends only on the form, so no context can separate any two data. It then instantiates this at the Challenge 2/3 regimes of both readings, replays the recorded histories to those regimes by computation, exhibits the non-increase countermodel (a real admission that leaves the collapsed pair collapsed), and proves replay is compositional.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `genesis` | 14 | def | `⟨0, [], [], [], []⟩`: nothing admitted | ADMITTED |

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `supply_no_op` | 17 | for every regime and token, `stepE r (.supply t) = some r` (by `rfl`) | FROZEN | propext | S |
| `genesis_underivable` | 21 | no instance is derivable in `genesis` | FROZEN (structural proof; an instance of `underivable_of_empty` on a concrete regime) | none | S |
| `underivable_of_empty` | 30 | if `r.insts = []` and `r.rules = []` then no instance is derivable in `r` | CONDITIONAL: `insts = []`, `rules = []` | none | S |
| `collapsed_of_no_insts` | 40 | if `r.insts = []` then every pair `d d'` is collapsed in `r` (no bound on `d`, `d'`) | CONDITIONAL: `insts = []` | propext | S |
| `R2L_collapsed` | 50 | `collapsed R2L 0 1` | FROZEN (instance of the previous on a concrete regime) | propext | S |
| `R2F_collapsed` | 54 | `collapsed R2F d d'` for all `d d'` | FROZEN (instance) | propext | S |
| `historyL_replays` | 59 | the recorded reading-L history replays from `genesis` to `some R2L` | VERIFIED_FINITE (`decide`) | propext | S |
| `historyF_replays` | 66 | the recorded reading-F history replays from `genesis` to `some R2F` | VERIFIED_FINITE (`decide`) | propext | S |
| `admission_without_expressive_increase` | 76 | there is `s` with `stepE R2L .admitDatum = some s`, `s ≠ R2L`, and `collapsed s 0 1` | REFUTED (countermodel to "a new inscription necessarily increases expressive power"); witness `⟨3,[],[],[],[(0,1)]⟩`, two conjuncts by `decide`, the third by `collapsed_of_no_insts` | propext | S |
| `replayE_append` | 83 | `replayE (h ++ [e]) base = (replayE h base).bind (stepE · e)` | FROZEN | propext, Quot.sound | A (used by replay certification argument) |

## 4. External and admitted assumptions
- Structures/definitions taken from Basic: `stepE`, `replayE`, `derivable`, `collapsed`, `R2L`, `R2F`.
- Recurring hypotheses: `r.insts = []` (and `r.rules = []`) — the "no instances" state of Challenges 0–2.
- Library lemmas doing work: `List.foldlM` unfolding, `Option.bind` simp lemmas (replayE_append). `decide` on `Regime` equality via derived `DecidableEq`.
- Universe/Type parameters: none.
- `Nat → X` as data: none. The `supply` tokens in the replayed histories (`0,1,1,2`) are metatheoretic labels for `<>`, `<a>`, `<a>`, `<ab>`; the Lean discards them.
- Unearned identity / unrestricted universe / unbounded internal function / silent observer / unspecified presentation correspondence / unjustified cost / admitted-as-forced / finite-as-universal: none found. The two `decide` theorems are about the two concrete recorded histories and the paper tags them as such.

## 5. Derived consequences
`collapsed_of_no_insts` is used by Minimality (`no_insts_no_separation`, `cost1_insufficient_general`), MinimalityF and Refusal. `genesis` is the base regime for Constitution, ControllerCategory, GraphGenesis, Horizon, MinimalityF, NoOutside, NoOutsideFidelity, PrimitivePassage, Represented, TraceAlgebra, TransitionAlphabet. `R2L_collapsed`/`R2F_collapsed` with `separable_not_collapsed` discharge CL-3-FAIL-CURRENT. `replayE_append` is cited by the replay-certification ledger row (line 608) and is not used by another Lean module.

## 6. Counterexamples and limitations
`admission_without_expressive_increase` is the module's countermodel: it refutes the necessity claim "every new external inscription increases internal expressive power". Its Lean conclusion is `collapsed s 0 1` only; the paper's phrasing "the number of observational classes stays 1" is the stronger all-pairs fact, which follows from `collapsed_of_no_insts s` but is not what the theorem states. What the module does not prove: that no transition is internally forced (there is no forcing predicate; the paper's section 4 correctly tags that as a property of the declared grammar). `historyL_replays`/`historyF_replays` certify two specific histories; they say nothing about the general replay/certify algorithm in Python beyond those two instances.

## 7. Axiom dependencies
All within {propext, Quot.sound}: `genesis_underivable`, `underivable_of_empty` axiom-free; `replayE_append` propext + Quot.sound; the rest propext. None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All ten theorems are in the axiom artifact (root inventory lines 74–84). Paper cites all ten (sections 4–6, 10; ledger CL-0-INERTIA, CL-1-SUPPLY-NOT-ADMISSION, CL-2-COLLAPSED, CL-2-NONINCREASE, CL-3-FAIL-CURRENT, replay row at ledger 608; native_derivation_map rows 13–15). No extra probe beyond the artifact.

## 9. Related Python implementations
`code/derivation/model.py` (`step`, `replay`, `certify`, `EMPTY`); `code/derivation/observe.py` (`collapsed_pairs`, `profiles`); `code/derivation/engine.py` Challenge 0–2 construction. Tests: `tests/test_engine.py::test_challenge0_inertia`, `::test_challenge2_collapse_and_no_expressive_increase`, `tests/test_model.py`, `tests/test_export_and_run.py` (replay/certify, tamper detection).

## 10. Textbook placement proposal
- Prerequisites: Basic (regime, derivable, collapsed, stepE/replayE).
- Substantive: `supply_no_op`, `collapsed_of_no_insts`, `R2L_collapsed`/`R2F_collapsed`, `admission_without_expressive_increase`, the two replay checks. Auxiliary: `genesis_underivable`/`underivable_of_empty` (one line each), `replayE_append`.
- Lesson title: "Nothing follows yet". Question: before any judgment form is admitted, can anything inside the regime tell two admitted data apart?
- Omit: `replayE_append` as a displayed theorem (state it in prose as "replay is a fold").

## 11. Interpretation findings
- `admission_without_expressive_increase`. Paper 6: "admitting a fresh datum is a real state change, yet the number of observational classes stays 1". Lean: `collapsed s 0 1` for the one pair. The all-pairs statement is a one-line corollary of `collapsed_of_no_insts s rfl`, not the theorem's conclusion. INTERPRETATION DEFECT (minor; the stronger claim is true and provable from the module).
- Paper 10.2 answers "[theorem] `supply_no_op` plus the structural fact that every state change is an admission event". Only the supply clause is a theorem; the rest is the shape of `stepE` (as section 4 itself says since 2026-09-08). INTERPRETATION DEFECT (minor, already scoped in section 4; see Basic finding).
- Vacuity: `collapsed_of_no_insts` is not vacuous (hypothesis satisfiable); but on `R2L`/`R2F` NO context is well-formed (no forms), so the collapse there holds because the quantifier over well-formed contexts is empty, not because contexts fail to separate. The paper's "no witness context exists" (7.1) is exact. Noted for teaching, not a defect.
- Finitude: none found; the `supply` tokens are metatheoretic labels and `genesis` is finite.
