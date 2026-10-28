# Audit: Quot

| field | value |
|---|---|
| Path | lean4/Derivation/Quot.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 0d1df5e6ef985f48 |
| Lines | 37 |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.Basic, Derivation.Inertia |
| Declarations | 1 def, 3 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 3 lines; axioms seen: Quot.sound; propext+Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
Quot answers the seed's required question 5: if the current abstraction identifies two cases, can an operation defined only on that abstraction recover the distinction? The module says no, in the only sense Lean can state it: any function out of a quotient takes equal values on related elements. It states this for `Quotient` of a setoid and for `Quot` of an arbitrary relation, and instantiates it at the Challenge 2 collapse relation on `R2L`: any function on the collapse classes gives equal outputs on the two admitted data. The content is the barrier itself; the Genesis-specific input is only `R2L_collapsed`.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `collapseRel` | 125 | def | `collapseRel r d d' := collapsed r d d'`, the relation to quotient by | ADMITTED (no `Setoid` instance is built; `Quot` is used, so no equivalence proof is needed) |

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `quotient_barrier` | 111 | for any setoid `s` on `α : Sort u`, any `f : Quotient s → β` and `a ≈ b`, `f ⟦a⟧ = f ⟦b⟧` | FROZEN (a general Lean fact: `congrArg f (Quotient.sound h)`) | Quot.sound | S |
| `quot_barrier` | 117 | same for `Quot rel` and any relation `rel` with `rel a b` | FROZEN | Quot.sound | S |
| `barrier_R2L` | 127 | for any `f : Quot (collapseRel R2L) → β`, `f (mk 0) = f (mk 1)` | FROZEN (instance at a concrete regime, via `R2L_collapsed`) | propext, Quot.sound | S |

## 4. External and admitted assumptions
- Structures: Lean's `Quot`/`Quotient` and `Quot.sound`. These are metatheory: the system has no quotient object; the quotient is the auditor's formalisation of "an abstraction that identifies two cases".
- Universe/Type parameters: `α : Sort u`, `β : Sort v` — an unrestricted external universe of codomains. The theorem is stronger for it (holds for every `β`), and nothing reads `β` as internally available.
- `Nat → X` as data: none.
- Unearned identity: none. Unrestricted external universe: present as parameters (`Sort u`, `Sort v`) but used only to quantify the barrier, not to supply the system with anything. Unbounded internal function: none. Silent observer: none. Presentation correspondence: none. Cost: none. Admitted-as-forced: none. Finite-as-universal: none.
- The sole Genesis-specific hypothesis is `R2L_collapsed` (from Inertia; itself holding because `R2L` has no well-formed contexts).

## 5. Derived consequences
`quot_barrier` is reused by ContactKernel (grep hit); the ledger (lines 2669–2706) and `paper/primitive_difference_map.md` line 491 contrast it with the later `obstP`/`phom2_unique_of_epi` machinery as the weaker, setoid-based statement. `quotient_barrier` and `barrier_R2L` are cited only by the paper/ledger (CL-QUOT-BARRIER).

## 6. Counterexamples and limitations
No countermodels. The module does not show that the *system* cannot recover a distinction: Challenge 3 recovers it by augmentation (changing the regime, hence the abstraction). It shows only that functions whose domain is the quotient are constant on a class — true of every quotient in every setting, i.e. the result carries no information about Genesis beyond the fact that 0 and 1 are collapsed in `R2L`. The ledger's falsifier row says exactly this ("recovering the distinction requires changing the abstraction").

## 7. Axiom dependencies
Within the whitelist: `quotient_barrier`, `quot_barrier` Quot.sound; `barrier_R2L` propext + Quot.sound (propext inherited via `collapsed_of_no_insts`). None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All three in the artifact (root lines 87–89). Paper 10.5 and ledger CL-QUOT-BARRIER cite them. Probe: `#check` of both barriers (probes/A/probe1.lean, exit 0) confirms the universe-polymorphic signatures printed above.

## 9. Related Python implementations
none found (ledger: "Python: n/a (purely logical)").

## 10. Textbook placement proposal
- Prerequisites: Inertia (`R2L_collapsed`); a one-paragraph note on what a quotient is.
- Substantive: `quot_barrier` and `barrier_R2L` (the answer to question 5). Auxiliary: `quotient_barrier` (same statement for setoids), `collapseRel`.
- Lesson title: "The abstraction barrier". Question: once a regime identifies two data, can anything defined on the identification alone tell them apart?
- Omit: `quotient_barrier` (duplicate of `quot_barrier`); teach the point that the theorem is a general fact about quotients and that the Genesis content is entirely in `R2L_collapsed`.

## 11. Interpretation findings
- Paper 10.5 tags the answer "[theorem] (`quotient_barrier`, `quot_barrier`, `barrier_R2L`): every function out of the quotient is constant on identified elements". The Lean statement is exactly that. But the question asks about "any operation defined only on that abstraction" within the system; the Lean quantifies over Lean functions out of a Lean quotient, which is metatheory (Finitude rule: `Quot`, `Sort u`, `Sort v` are not objects the regime possesses). Not false; the theorem's bearing on the system is by the auditor's identification of "abstraction" with "quotient", which the paper does not state as a step. INTERPRETATION DEFECT (minor: the unstated identification; no missing hypothesis).
- Vacuity check: `barrier_R2L` is non-vacuous (functions out of `Quot` exist, e.g. constants, and `Quot.lift` of any `collapseRel`-respecting function); its conclusion is forced by `Quot.sound`, so the theorem is a tautology of quotients, as section 6 says. Not a proof defect.
