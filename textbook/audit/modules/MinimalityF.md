# Audit: MinimalityF

| field | value |
|---|---|
| Path | lean4/Derivation/MinimalityF.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 04ce2ef3fb6b036f |
| Lines | 197 |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.Minimality, Derivation.Mention |
| Declarations | 4 def (`U0F`, `U2F`, `swap12`, `isoU2F_U0F`), 2 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 2 lines (`genesis_mark_not_separable`, `mu2_unique_F`: propext, Quot.sound) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
MinimalityF discharges residual R5: grammar-wide uniqueness of the `mu2` minimum up to isomorphism for reading F, where reading L already had `mu2_unique`. The L case analysis transfers because it uses only that the base regime is form-less and instance-less with a singleton requirement list; the datum bound rises from 2 to 3, so one new terminal case appears — the unary mark on the genesis datum `0`, which lies outside the required pair `(1,2)`. That case is killed by the mention lemma: the mark mentions neither required datum, so the pair stays collapsed and validity fails. The two marks on the required data are one class under the transposition `swap12`. With `cost1_insufficient_F` (floor) and `deltaU0F_valid` (existence) from Minimality, this gives reading F the same package as reading L.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `U0F` | 37 | def | `⟨3,[1],[(0,[1])],[],[(1,2)]⟩`: unary mark on the first required datum | ADMITTED |
| `U2F` | 40 | def | mark on the second required datum | ADMITTED |
| `swap12` | 43 | def | transposition of data 1, 2 fixing 0 | ADMITTED |
| `isoU2F_U0F` | 47 | def (Type-valued) | `Iso U2F U0F` via `swap12`, all fields by `decide` | ADMITTED (VERIFIED_FINITE fields) |

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `genesis_mark_not_separable` | 72 | `¬ separable ⟨3,[1],[(0,[0])],[],[(1,2)]⟩ 1 2` | FROZEN (instance: `collapsed_of_no_insts` + `collapsed_append_unmentioning`, non-mention side conditions by `decide`) | propext, Quot.sound | S |
| `mu2_unique_F` | 86 | for any items `a b`, if `[a,b]` is a valid response on `R2F` to `(1,2)` with `aritySum [a,b] ≤ 1`, then `applyDelta R2F [a,b] = some s` with `Nonempty (Iso s U0F)` | FROZEN (general over the item grammar; hypotheses `hval`, `har` are the claim's scope) | propext, Quot.sound | S |

## 4. External and admitted assumptions
- Inherits Minimality's declared measures and `Iso`; uses Mention's R3 lemma.
- Hypotheses: validity on `R2F` and `aritySum ≤ 1` (the `mu2` scope).
- Library lemmas: as Minimality (`Option.some.inj`, `omega`, `simp`, `decide`).
- Universe parameters: none. `Nat → Nat` as data: `swap12` and the `Iso` fields (metatheory).
- Unearned identity / unrestricted universe / unbounded internal function / silent observer / presentation correspondence / cost (inherited, declared) / admitted-as-forced / finite-as-universal: none found.

## 5. Derived consequences
No other Lean module uses these. The paper (7.4, 10.6, register row R5) and ledger CL-3-UNIQUE-MU2-F rest on `mu2_unique_F`; `representative_selection.md` cites it with `mu2_unique` to refute "no invariant rule can break the Challenge-3 tie".

## 6. Counterexamples and limitations
No countermodels (the genesis-mark case is a dead branch, not a refutation of a claim). Not proved: anything about reading F under `mu1` (the five tie classes remain bounded enumeration; ledger CL-3-TIE-CLASSES); a one-theorem "the `mu2` minimum is unique" statement (assembled in prose as for reading L).

## 7. Axiom dependencies
Both propext, Quot.sound; the def `isoU2F_U0F` probed: propext, Quot.sound (probe2.lean, exit 0). None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). Both theorems in the artifact (root inventory). Paper 7.4, 12 (R5) and ledger CL-3-UNIQUE-MU2-F cite them. No extra probe.

## 9. Related Python implementations
`code/derivation/candidates.py::min_responses` with `mu2` on the reading-F base; tests `tests/test_engine.py::test_challenge3_reading_f_has_five_classes` (mu1 classes), `tests/test_independent_oracles.py::test_c3_mu2_minimum_is_exactly_the_two_unary_marks`.

## 10. Textbook placement proposal
- Prerequisites: Minimality (`mu2_unique`), Mention (R3).
- Substantive: `mu2_unique_F` and the one new case (`genesis_mark_not_separable`). Auxiliary: `U2F`, `swap12`, `isoU2F_U0F`.
- Lesson title: "The same proof with one more datum". Question: does admitting the opaque genesis datum change which cheapest repair is forced under `mu2`?
- Omit: nothing beyond folding the definitions into one sentence.

## 11. Interpretation findings
- Paper 7.4: "Reading F: exactly one mu2 class, grammar-wide — the unary mark on either required datum". Lean: every valid `(2, ≤1)` response is isomorphic to `U0F`; `isoU2F_U0F` makes the two marks one class. Match. none found.
- Paper register row R5 (line 786): "`genesis_mark_not_separable` closing the one new case via the R3 mention lemma". Exact.
- Vacuity: `mu2_unique_F`'s hypotheses are satisfiable (`deltaU0F_valid`). none found.
- Finitude: none found.
