# Audit: CountTransport

| field | value |
|---|---|
| Path | lean4/Derivation/CountTransport.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 42834f932042070c |
| Lines | 306 |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.Basic |
| Declarations | 1 structure (`DRen`), 5 def, 13 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 8 lines for this module's theorems (`plug_mapCtx`, `derivable_rename`, `wfCtx_rename`, `collapsed_rename`, `collapsedCount_rename`, `rename_insts_wf`, `cm_separable`, `non_injective_does_not_transport`: all propext, Quot.sound). `DRen.f_inj`, `list_map_inj`, `mapInst_inj`, `mapCtx_f_g`, `cmRegime_wf` not in artifact. (The inventory's match of `Attachment.Renaming.f_inj` to this module is a name collision with another module's theorem.) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
CountTransport discharges residual R6 / claim CL-COUNT-INVARIANCE: observational collapse, and therefore the collapsed-pair count, is invariant under a renaming of the datum indices with the forms held fixed. It declares a datum renaming `DRen n` (a bijection on `Nat` with inverse, mapping the admitted range into itself both ways), an action on instances, contexts and regimes, and proves the chain plugging-commutes → derivability-transports → well-formed-contexts-transport → collapse-transports → the count transports. The module records why the proof is clean: `collapsed` reads only `forms`, `data`, `insts`, `rules` and never `reqs`, so the action can leave requirements alone. It also shows the bijectivity hypothesis is load-bearing with a countermodel: under the constant map the transport iff is false.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `DRen n` | 50 | structure | `f g : Nat → Nat`, `g ∘ f = id`, `f ∘ g = id`, both map `{x < n}` into itself | ADMITTED (a bijection on all of `Nat`, not merely on the admitted range) |
| `DRen.inv` | 68 | def | swaps `f`/`g` and the bounds | ADMITTED |
| `mapInst` | 79 | def | rename the argument tuple of an instance | ADMITTED |
| `mapCtx` | 83 | def | rename filled slots; holes stay holes | ADMITTED |
| `renameRegime` | 90 | def | map `insts` only; `data`, `forms`, `rules`, `reqs` untouched | ADMITTED (declared action; `reqs` deliberately not renamed) |
| `cmRegime` | 286 | def | `⟨2, [1], [(0,[0])], [], []⟩`, the countermodel regime | ADMITTED |

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `DRen.f_inj` | 62 | `σ.f` is injective | FROZEN | not in artifact | A |
| `list_map_inj` | 93 | an injective `f : Nat → Nat` gives an injective `List.map f` | FROZEN | not in artifact | A |
| `mapInst_inj` | 110 | `mapInst f` is injective when `f` is | FROZEN | not in artifact | A |
| `plug_mapCtx` | 125 | `plug (mapCtx f c) (f d) = mapInst f (plug c d)` for any `f` (no injectivity needed) | FROZEN | propext, Quot.sound | S |
| `derivable_rename` | 137 | for injective `f`, `derivable (renameRegime f r) (mapInst f i) ↔ derivable r i` | CONDITIONAL: `f` injective (named hypothesis `hf`) | propext, Quot.sound | S |
| `wfCtx_rename` | 154 | for `σ : DRen n` and `r.data = n`, `wfCtx (renameRegime σ.f r) (mapCtx σ.f c) ↔ wfCtx r c` | CONDITIONAL: `r.data = n` and the bound fields of `σ` | propext, Quot.sound | S |
| `mapCtx_f_g` | 189 | `mapCtx σ.f (mapCtx σ.g c) = c` | FROZEN | not in artifact | A |
| `collapsed_rename` | 204 | for `σ : DRen n`, `r.data = n`: `collapsed (renameRegime σ.f r) (σ.f d) (σ.f d') ↔ collapsed r d d'` (all `d d'`, unbounded) | CONDITIONAL: `σ` a `DRen n` with `r.data = n` (bounds used only through `wfCtx_rename`) | propext, Quot.sound | S |
| `collapsedCount_rename` | 239 | given deciders `p`, `q` proved to track `collapsed` on `r` and on the renamed regime, and ANY list `L` of pairs, `countP q (L.map σ) = countP p L` | CONDITIONAL: `hp`, `hq` (caller-supplied decision procedures), `σ`, `r.data = n` | propext, Quot.sound | S |
| `rename_insts_wf` | 258 | the instance conjunct of `Regime.wf` is preserved by the action | CONDITIONAL: `r.data = n`, the instance conjunct holds for `r` | propext, Quot.sound | A |
| `cmRegime_wf` | 288 | `cmRegime.wf` | VERIFIED_FINITE (simp on a concrete regime) | not in artifact | A |
| `cm_separable` | 292 | `separable cmRegime 0 1`, witness context `⟨0,[none]⟩` | VERIFIED_FINITE (`decide`) | propext, Quot.sound | A |
| `non_injective_does_not_transport` | 300 | the constant map `fun _ => 0` sends `cmRegime` to a regime where `(0,0)` is collapsed, while `cmRegime` does not collapse `0,1` | REFUTED (countermodel to transport without injectivity) | propext, Quot.sound | S |

## 4. External and admitted assumptions
- `DRen n` demands a bijection on ALL of `Nat` with inverse functions `Nat → Nat`. This is metatheory (an auditor's relabelling); the system never possesses `σ.f` as an internal map. Only the bounds on `{x < n}` reach the regime. The docstrings say so.
- Recurring hypotheses: `r.data = n` (ties the renaming's range to the regime), injectivity of `f`.
- Caller-supplied deciders `p q : Nat × Nat → Bool` with tracking proofs `hp hq`; the module explicitly does not decide `collapsed` (quantifier over the unbounded type `Ctx`). This is an honest "Python decides, Lean states what the decision means" split, stated in the docstring and the ledger.
- Library lemmas: `List.mem_map`, `List.map_map`, `List.countP_cons`, `List.length_map`, `Bool.eq_iff_iff`. No Mathlib.
- Universe parameters: none.
- Unearned identity: none. Unrestricted external universe: none. Unbounded function treated as internal: `σ.f : Nat → Nat` is a metatheoretic relabelling, not internal (flag noted; prose does not overread it). Silent observer: none. Unspecified presentation correspondence: token renaming is outside the Lean model (paper 10.8 says so). Cost: none. Admitted-as-forced: none. Finite-as-universal: none — `cmRegime` results are used only as a countermodel.

## 5. Derived consequences
`DRen`, `mapInst`, `mapCtx`, `renameRegime`, `plug_mapCtx`, `derivable_rename`, `wfCtx_rename`, `collapsed_rename`, `collapsedCount_rename`, `rename_insts_wf`, `mapInst_inj` are reused by TransitionTransport (the transition-level equivariance) and by FormRenaming, FormTransport, IsoCollapse, IsoCanon (the two-bijection transports). The ledger reclassified CL-COUNT-INVARIANCE from [finite computation] to [theorem] on the strength of `collapsed_rename`/`collapsedCount_rename` (2026-08-17), with scope stated 2026-09-08. `cmRegime`/`non_injective_does_not_transport` are cited nowhere else in Lean or the paper (grep: artifact and dependency graph only).

## 6. Counterexamples and limitations
`non_injective_does_not_transport`: for `f = fun _ => 0`, the renamed regime collapses `(f 0, f 1) = (0, 0)` trivially (`Iff.rfl`), and `cmRegime` separates `0,1` by the one-hole context. This refutes "collapse transports under any map"; it does not test any non-injective map other than a constant one, nor a non-surjective injective map (`DRen` requires both). Not proved: transport of the `reqs` conjunct of `wf` (explicitly disclaimed); transport under form bijections (FormTransport); any decision procedure for `collapsed`; that the Python's candidate list `range(data)²` is the right list (the theorem holds for any `L`, so this is not needed for the count statement but is needed to read the count as "the collapsed-pair count of the regime").

## 7. Axiom dependencies
All artifact lines propext, Quot.sound; none exceed. The five theorems absent from the artifact are not in the root inventory (not cited by the paper); not probed, but each is a short structural proof using only `simp`/`cases`/`rfl`.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). Eight theorems in the artifact; paper 10.8, 12 (R6 row) and ledger CL-COUNT-INVARIANCE, CL-ISO-RESIDUALS (line 3913) cite `collapsed_rename`, `collapsedCount_rename`, `plug_mapCtx`, `derivable_rename`, `wfCtx_rename`. No probe run beyond the build.

## 9. Related Python implementations
`code/derivation/iso.py::rename(r, pi, phi)` (acts on data AND forms, including `reqs` — wider than `renameRegime`), `canonical`, `isomorphic`; `code/derivation/observe.py::collapsed_pairs`. Tests: `tests/test_iso.py::test_canonical_invariant_under_rename`, `tests/test_engine.py::test_closure_policy_is_token_blind`, `tests/test_equivariance.py::test_regression_canonical_equal_under_rename`.

## 10. Textbook placement proposal
- Prerequisites: Basic (`collapsed`, `wfCtx`, `plug`); the idea of a relabelling.
- Substantive: `DRen`, `renameRegime`, `plug_mapCtx`, `collapsed_rename`, `collapsedCount_rename`, `non_injective_does_not_transport`. Auxiliary: injectivity lemmas, `mapCtx_f_g`, `rename_insts_wf`, `cmRegime_wf`, `cm_separable`.
- Lesson title: "Renaming data changes nothing a context can see". Question: why is the collapsed-pair count the same after the data are relabelled, and why must the relabelling be a bijection?
- Omit: `list_map_inj`, `mapInst_inj` (standard); keep the countermodel.

## 11. Interpretation findings
- Paper 12 R6 row (line 787): "DISCHARGED 2026-08-17 (full-isomorphism collapse transport: `collapsed_transport`, `collapsed_renameDataForm`; the executable count and pair …)". The Lean of THIS module transports data indices with forms fixed; the paper's own scope paragraph (line 759) and the ledger say so and point to IsoCollapse/FormTransport for the two-bijection case. Consistent; none found.
- `collapsedCount_rename` docstring: "**R6, as the paper states it.** The collapsed-pair count is invariant under renaming." The theorem is about ANY list `L` and caller-supplied deciders; it becomes "the collapsed-pair count" only when `L` enumerates the admitted pairs and `p`/`q` are correct deciders, neither of which Lean supplies. The ledger's "Scope, exactly" paragraph states this. INTERPRETATION DEFECT (minor; docstring headline reads stronger than the parameterised statement, scope stated two sentences later).
- Vacuity: `collapsed_rename` is non-vacuous (`DRen n` is inhabited by the identity; `collapsed` holds on `R2L`). `collapsedCount_rename` is non-vacuous (deciders exist for finite `data` since `wfCtx` is decidable and contexts are finitely many, though Lean does not construct them here).
- Finitude: `σ.f : Nat → Nat` and the whole-`Nat` bijection are metatheory; the docstring ("a bijection on `Nat`") does not attribute it to the system. None found beyond the flag.
