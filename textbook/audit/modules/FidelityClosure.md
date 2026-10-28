# Audit: FidelityClosure

| field | value |
|---|---|
| Path | lean4/Derivation/FidelityClosure.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 188743dd2ed84760 |
| Lines | 234 |
| Imported by root `Derivation.lean` | yes (line 59) |
| Imports | Derivation.QuotientRetention (transitively PresentationDescent, PresentationNaturality) |
| Declarations | 3 structures (`TranslationNetwork`, `HolonomyResidual`, `FaithfulNetworkDescent`), 1 inductive (`FidelityPath`), 1 abbrev (`FidelityQuotient`), 9 defs (`FidelityPath.toBij`, `FidelityRel`, `fidelitySetoid`, `classOf`, `NoCoherentPath`, `LoopTrivial`, `AllLoopsTrivial`, `LabelInvariant`, `LabelDescends`), 11 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 11 lines; axioms seen: none (6), `Quot.sound` (3: the label theorems), `propext, Quot.sound` (2: `class_eq_iff_coherent_path`, `no_coherent_path_retains_indices`) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

A *translation network* supplies a type of presentation indices, a carrier for each index, and typed attempted translations between carriers; it does **not** supply an equivalence on indices. The module generates one: a *fidelity path* is built only from attempts whose scoped arrows totalize and whose round trips cohere (PresentationDescent), closed under identity, reversal and composition. Each path composes to an actual carrier bijection. The resulting relation is an equivalence (`fidelitySetoid`), and two indices have the same class exactly when a coherent path joins them; a missing path retains two classes, while one failed direct attempt refutes nothing, since the identity path always exists. Index reachability is weaker than carrier descent: a *holonomy residual* (an admitted loop that moves a carrier point) refutes any faithful network descent, and such a descent forces every loop to act trivially. Finally a label on indices descends to the fidelity quotient exactly when it is invariant along coherent paths, so an inside/outside polarity that flips along a coherent translation is a presentation label, not a property of the descended object.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `TranslationNetwork` | 43 | structure (Type 1) | `Index : Type`, `Carrier : Index → Type`, `Attempt : Index → Index → Type`, `pair : Attempt i j → TranslationAttempt (Carrier i) (Carrier j)`. | ADMITTED (the supplied network; three `Type`-valued fields) |
| `FidelityPath N i j` | 54 | inductive (Type) | `refl`, `step a u h` (an attempt with a totalization and a `RoundTripCoherent` proof), `symm`, `trans`. | ADMITTED (the generating rule for fidelity — a declared admission criterion) |
| `FidelityPath.toBij` | 65 | def | Composes a path to a `Bij (Carrier i) (Carrier j)` using `coherent_to_bij`, `Bij.symm`, `Bij.trans`. | ADMITTED |
| `FidelityRel N i j` | 75 | def | `Nonempty (FidelityPath N i j)`. | ADMITTED |
| `fidelitySetoid N` | 97 | def | The setoid with `r := FidelityRel N`. | ADMITTED (derived from the three theorems below) |
| `FidelityQuotient N` | 104 | abbrev | `Quotient (fidelitySetoid N)`. | ADMITTED |
| `classOf N i` | 106 | def | `Quotient.mk _ i`. | ADMITTED |
| `NoCoherentPath N i j` | 119 | def | `¬ FidelityRel N i j`. | ADMITTED (a proposition, not a decision procedure — header of EndogenousFidelityGenerator says so) |
| `LoopTrivial loop` | 143 | def | `∀ x, loop.toBij.fwd x = x`. | ADMITTED |
| `HolonomyResidual N` | 149 | structure | An index, a loop at it, a carrier point the loop moves. | ADMITTED |
| `FaithfulNetworkDescent N` | 158 | structure (Type 1) | `Carrier : Type`, injective `embed i : N.Carrier i → Carrier` for every `i`, and `embed j (path.toBij.fwd x) = embed i x` for every path. | ADMITTED (declared notion of global descent; `Carrier : Type` is metatheoretic existential output) |
| `AllLoopsTrivial N` | 177 | def | Every loop at every index is `LoopTrivial`. | ADMITTED |
| `LabelInvariant label` | 189 | def | `∀ i j, FidelityRel N i j → label i = label j`. | ADMITTED |
| `LabelDescends label` | 193 | def | `∃ descended : FidelityQuotient N → Y, ∀ i, descended (classOf N i) = label i`. | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `fidelity_refl` | 78 | `FidelityRel N i i`. | FROZEN | none | A |
| `fidelity_symm` | 82 | `FidelityRel N i j → FidelityRel N j i`. | FROZEN | none | A |
| `fidelity_trans` | 87 | Transitivity. | FROZEN | none | A |
| `class_eq_iff_coherent_path` | 109 | `classOf N i = classOf N j ↔ FidelityRel N i j`. | FROZEN | propext, Quot.sound | S |
| `no_coherent_path_retains_indices` | 122 | `NoCoherentPath N i j → classOf N i ≠ classOf N j`. | CONDITIONAL: `NoCoherentPath N i j` | propext, Quot.sound | S |
| `failed_endomorphism_does_not_refute_self_fidelity` | 133 | Given any `CoherenceResidual u` for an attempted endomorphism at `i`, still `FidelityRel N i i`. | FROZEN (the residual hypothesis is unused; the conclusion is `fidelity_refl`) | none | S (as a scope fence) |
| `holonomy_residual_refuses_faithful_network_descent` | 167 | A `HolonomyResidual N` implies `¬ Nonempty (FaithfulNetworkDescent N)`. | CONDITIONAL: a holonomy residual | none | S |
| `faithful_network_descent_forces_trivial_loops` | 180 | Any `FaithfulNetworkDescent N` implies `AllLoopsTrivial N`. | FROZEN | none | S |
| `label_descends_iff_fidelity_invariant` | 198 | `LabelDescends label ↔ LabelInvariant label`. | FROZEN | Quot.sound | S |
| `coherent_disagreement_refuses_label_descent` | 215 | If `FidelityRel N i j` and `label i ≠ label j` then `¬ LabelDescends label`. | CONDITIONAL: the two hypotheses | Quot.sound | A |
| `polarity_flip_is_presentation_relative` | 227 | The previous theorem for `Y := Bool`. | CONDITIONAL: same | Quot.sound | A (restatement) |

## 4. External and admitted assumptions

- The network `N` is supplied in full: which indices exist, which carriers, which attempts. The admission criterion for a step (totalization + `RoundTripCoherent`) is a **declared policy** encoded in the `step` constructor. "Endogenous" in the header means: *given* the network, no further choice selects the equivalence — it is generated by the coherence proofs. It does not mean the network or the criterion arises from inside the regime model (the header, lines 32–34, says exactly this).
- `TranslationNetwork` has three `Type`-valued fields and lives in `Type 1`; `FaithfulNetworkDescent` has a `Carrier : Type` field. Under the finitude rule these are metatheoretic. `FidelityRel N i j := Nonempty (FidelityPath N i j)` is an existential over paths of arbitrary length — a metatheoretic closure, not a search the system performs. `NoCoherentPath` is therefore a negative statement about an unbounded space; the downstream header (EndogenousFidelityGenerator lines 22–23) flags that it "is a proposition, not a claimed decision procedure". Flagged as required; the prose does not overread it.
- Unearned identity: none found (class equalities go through `Quotient.sound`/`exact`; carrier equalities through injectivity of `embed`).
- Unrestricted external universe: the `Type`-valued fields above, declared as supplied data.
- Unbounded function treated as internally available: `label : N.Index → Y` and `polarity : N.Index → Bool` are arbitrary ambient functions; the theorems are about *whether* such a function descends, so this is the intended object, not a smuggled capacity.
- Silently assumed observer: none found; the header says "no observer decides which indices are connected".
- Unspecified correspondence between presentations: none found — each step carries its explicit `Totalization`.
- Cost function: none.
- Admitted condition later described as forced: none found.
- Finite computation presented as universal: none (no finite computation here).
- Library lemmas doing real work: `Quotient.lift`, `Quotient.sound`, `Quotient.exact`; `Function.Injective`; `congrArg`.

## 5. Derived consequences

- `EndogenousFidelityGenerator` imports this module: proves `fidelitySetoid N` is the least equivalence containing admitted steps and compares it with the indiscrete setoid via QuotientRetention.
- `NoOutsideFidelity` imports it but uses only PresentationDescent's notions (`TranslationAttempt`, `Totalization`, `RoundTripCoherent`, `FaithfulCommonDescent`) — no `FidelityPath` is built there (checked).
- Paper: ledger CL-FIDELITY-CLOSURE; `native_derivation_completion.md` §19; `endogenous_generator.md` ~line 253; change log 2026-08-14. Individual theorem names (`holonomy_…`, `polarity_flip_…`, `label_descends_…`) are not cited anywhere in `paper/` (grep: no hits). Not cited in `paper/paper.md`.

## 6. Counterexamples and limitations

- `failed_endomorphism_does_not_refute_self_fidelity` is the module's explicit smallest counterexample to "one failed round trip proves two indices distinct": its residual hypothesis is discarded and `refl` is returned. It is a scope fence, not a theorem with content.
- `holonomy_residual_refuses_faithful_network_descent` refutes global descent from one moving loop; no concrete network with a nontrivial loop is constructed in this module (none found in the batch either).
- Not proved: that `FidelityRel` is decidable or computable; that any particular network has a nontrivial fidelity class; that parallel paths agree (the header says they may not); anything about the first presentation or the admissibility of attempts.
- Probe (see §8) shows both extremes are inhabited: a two-index network with one coherent identity step has `FidelityRel false true`; a network with no attempts has `NoCoherentPath false true`. So `no_coherent_path_retains_indices` is not vacuous.

## 7. Axiom dependencies

All within {propext, Quot.sound}; six theorems are axiom-free. None exceeds.

## 8. Verification status

- Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0).
- All eleven theorems in `artifacts/lean_axioms.txt` (ledger: "the eleven `FidelityClosure.*` theorem reports").
- Probe: `/tmp/claude-0/-home-claude/47be43b5-43cb-5429-bc31-b53a81ca595d/scratchpad/probes/F2/fid_probe.lean`, exit 0: `holonomy_residual_refuses_faithful_network_descent` axiom-free; `#check TranslationNetwork : Type 1`, `FaithfulNetworkDescent N : Type 1`; a two-index network `twoNet` (indices `Bool`, carriers `Bool`, one attempt `false → true` with identity arrows) has `FidelityRel twoNet false true`; a network `emptyNet` with `Attempt := Empty` has `NoCoherentPath emptyNet false true` (proved by structural recursion on paths).

## 9. Related Python implementations

- `code/derivation/completion.py` lines 797–814: tag bindings for the eleven names; `tests/test_completion.py`. No Python implements translation networks, fidelity paths or holonomy: none found (grep `fidelity|holonomy|FidelityPath|TranslationNetwork` in `code/`, `tests/`: only the bindings).

## 10. Textbook placement proposal

- Prerequisites: PresentationDescent (`Totalization`, `RoundTripCoherent`, `coherent_to_bij`); `Bij` (PresentationNaturality); quotients by a setoid; the distinction between an index relation and a carrier map.
- Substantive: `FidelityPath` as the generating rule; `class_eq_iff_coherent_path`; `no_coherent_path_retains_indices`; `failed_endomorphism_does_not_refute_self_fidelity` (taught as the warning it is); `holonomy_residual_refuses_faithful_network_descent` with `faithful_network_descent_forces_trivial_loops`; `label_descends_iff_fidelity_invariant`.
- Auxiliary: `fidelity_refl/symm/trans`, `FidelityPath.toBij`, `coherent_disagreement_refuses_label_descent`, `polarity_flip_is_presentation_relative`.
- Suggested lesson: "Which presentation indices can be identified without an observer choosing?" — answering: exactly those joined by a chain of coherent translations; reachability of indices still does not make the carriers one.
- Recommend omitting: `polarity_flip_is_presentation_relative` (pure restatement with `Y := Bool`), unless the lesson wants the inside/outside vocabulary made explicit.

## 11. Interpretation findings

1. **Header line 16: "no observer decides which indices are connected. Coherence proofs generate the relation."** Lean: given a supplied `N`, `FidelityRel` is generated by `FidelityPath`; but which attempts exist, and the admission criterion itself, are supplied. The header's lines 32–34 say so. The word "endogenous" in the title must be read as *relative to the supplied network*. INTERPRETATION hazard; the module self-corrects. No defect.
2. **Ledger CL-FIDELITY-CLOSURE: "Its induced setoid identifies exactly path-connected indices."** Lean: `class_eq_iff_coherent_path`. Accurate.
3. **`failed_endomorphism_does_not_refute_self_fidelity`** has an unused hypothesis; its conclusion is `fidelity_refl`. This is by design (docstring: "deliberately not enough"). A textbook citing it as a theorem would be overreading; it is a recorded non-inference. Not a defect, but it should be tagged "scope fence" rather than "theorem".
4. **`native_derivation_completion.md` §19: "Holonomy and label disagreement are separate residuals: either prevents the corresponding global descent without introducing an evaluator."** Lean: holonomy refutes `FaithfulNetworkDescent`; label disagreement refutes `LabelDescends` — two different "descents". The prose says "the corresponding", which is correct. None found.
5. Vacuity: `FaithfulNetworkDescent N` is inhabited for `emptyNet`-like networks (every path is `refl`-generated; take `Carrier := Σ i, N.Carrier i` with `embed := Sigma.mk` — not machine-checked), so `faithful_network_descent_forces_trivial_loops` is not vacuous. `HolonomyResidual` requires a nontrivial loop; none exhibited in the sealed modules (not checked outside the batch).
