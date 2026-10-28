# Audit: LadderGeneral

| field | value |
|---|---|
| Path | lean4/Derivation/LadderGeneral.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 04d5ea0690ff6c5b |
| Lines | 329 (inventory counts 330) |
| Imported by root `Derivation.lean` | yes (line 38) |
| Imports | Derivation.HigherStructure (import only; no declaration of `HigherStructure` is used in this file) |
| Declarations | 1 structure (`ComplexN`), 1 inductive (`NEvent`), 20 def, 13 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 13 lines (all 13 theorems); axioms seen: none, {propext, Quot.sound} |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module generalizes the hard-coded dimension-0–3 cell calculus of `HigherStructure` to a dimension-indexed complex (`ComplexN`, one cell list per dimension) with one shell guard `shellN` uniform in the dimension `k ≥ 1`: exact arity `k+1`, strict ascent of the vertex list (well-formedness), every facet present one dimension down, and the cell itself absent. The main theorem, `uniform_guarded_filler`, says that whenever this guard holds the guarded step admits the cell and strictly extends the complex. The module records the repair that introduced the ascent conjunct: the retired guard `shellNLegacy` accepted the repeated-vertex pseudo-cell `[0,0]` (`pseudo_cell_countermodel`), and well-formedness (`WFComplex`) is proved to be an invariant of every replay from the empty complex (`wf_nreplay`). A five-vertex demonstration replays the full boundary of a 4-simplex and its filler (`d4_demo`, 5/10/10/5/1) and shows the guard refuses the 4-cell when one tetrahedron is missing. A declared signed boundary calculus (`sgn`, `bdN`, `pushN`, `coeffN`) is spot-checked at dimensions 2–4 (`d2_zero_dims_2_3_4`); the general vanishing lives in `BoundaryCancellation`. The docstring is explicit that this is a theorem about a declared guarded step, "NOT a homology claim", and that the passage notions (protection, observer, budget) do not appear here.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `ComplexN` | 51 | structure | `cells : Nat → List (List Nat)`: a list of cells for every dimension. | ADMITTED (a `Nat`-indexed function treated as data; see §4) |
| `emptyN` | 54 | def | All dimensions empty. | ADMITTED |
| `facets` | 57 | def | `(range σ.length).map σ.eraseIdx`: drop each vertex once. | ADMITTED |
| `ascB` | 62 | def | Strict ascent of a `List Nat`. | ADMITTED |
| `shellN` | 71 | def | Arity `k+1`, `1 ≤ k`, ascent, all facets in `cells (k−1)`, cell absent from `cells k`. | ADMITTED (declared guard / policy) |
| `shellNLegacy` | 78 | def | `shellN` without the ascent conjunct; kept as the countermodel's exhibit. | ADMITTED (retired policy) |
| `stepV` | 84 | def | Dedup-guarded vertex admission into dimension 0. | ADMITTED |
| `stepN` | 89 | def | Shell-guarded admission into dimension `k`; inert otherwise. | ADMITTED (declared policy) |
| `oneVertex` | 140 | def | `stepV emptyN 0`. | ADMITTED |
| `WFComplex` | 155 | def (Prop) | Every cell in dimension `k` has length `k+1` and is ascending. | ADMITTED (named invariant) |
| `NEvent` | 212 | inductive | `addV v`, `addC k σ`. | ADMITTED |
| `nstep` | 216 | def | Dispatch to `stepV` / `stepN`. | ADMITTED |
| `nreplay` | 220 | def | `foldl nstep`. | ADMITTED |
| `combsAux`, `combs` | 246, 253 | def | All `(m+1)`-element ascending sublists of `range n`. | ADMITTED (metatheoretic enumeration) |
| `d4Events` | 256 | def | 5 vertices, then all 1-, 2-, 3-cells over them, then `[0,1,2,3,4]`. | ADMITTED |
| `d4Complex` | 263 | def | `nreplay d4Events emptyN`. | ADMITTED |
| `d4MissingEvents` | 284 | def | As `d4Events` with the first tetrahedron dropped. | ADMITTED |
| `sgn` | 299 | def | `+1` on even index, `−1` on odd. | ADMITTED (declared sign convention) |
| `bdN` | 302 | def | Signed facets of a cell. | ADMITTED (declared) |
| `pushN` | 306 | def | Pushforward of a chain through `bdN`. | ADMITTED |
| `coeffN` | 310 | def | Coefficient of a face in a chain. | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `uniform_guarded_filler` | 100 | For every `C`, `k`, `σ` with `shellN C k σ = true`: `σ ∈ (stepN C k σ).cells k` and `stepN C k σ ≠ C`. | CONDITIONAL: `shellN C k σ = true` (over all `C`, `k`, `σ`) | propext, Quot.sound | S |
| `shell_refuses_general` | 122 | If `shellN C k σ = false` then `stepN C k σ = C`. | CONDITIONAL: `shellN = false` | propext, Quot.sound | S |
| `shell_no_self_fill` | 130 | If `shellN C k σ = true` then `σ ∉ C.cells k`. | CONDITIONAL: `shellN = true` (near-definitional: the last conjunct of the guard) | propext, Quot.sound | A |
| `pseudo_cell_countermodel` | 146 | On `oneVertex`, `shellNLegacy … [0,0] = true`, `shellN … [0,0] = false`, and `stepN` is inert on `[0,0]`. | VERIFIED_FINITE / REFUTED (refutes "the legacy guard admits only well-formed cells") | propext, Quot.sound | S |
| `wf_empty` | 158 | `emptyN` is well-formed. | FROZEN | none | A |
| `wf_stepV` | 162 | `stepV` preserves `WFComplex`. | FROZEN | propext, Quot.sound | A |
| `wf_stepN` | 182 | `stepN` preserves `WFComplex` (the guard's arity and ascent conjuncts supply the new cell's well-formedness). | FROZEN | propext, Quot.sound | A |
| `wf_nstep` | 223 | `nstep` preserves `WFComplex`. | FROZEN | propext, Quot.sound | A |
| `wf_nreplay` | 233 | For every event list and every well-formed `C`, `nreplay h C` is well-formed. | FROZEN | propext, Quot.sound | S |
| `d4_demo` | 269 | `d4Complex` has 5, 10, 10, 5 cells in dimensions 0–3 and `cells 4 = [[0,1,2,3,4]]`. | VERIFIED_FINITE | propext, Quot.sound | S |
| `d4_wf` | 279 | `d4Complex` is well-formed (instance of `wf_nreplay`). | FROZEN-derived instance | propext, Quot.sound | A |
| `d4_guard_load_bearing` | 292 | With one tetrahedron missing, `cells 4 = []`. | VERIFIED_FINITE / REFUTED (refutes "an incomplete 4-shell fills") | propext, Quot.sound | S |
| `d2_zero_dims_2_3_4` | 318 | Three `decide`d conjuncts; see §11: conjuncts 1 and 2 are vacuous, conjunct 3 is the genuine check that the composite boundary of `[0,1,2,3,4]` has coefficient 0 on every codimension-two face. | VERIFIED_FINITE (conjunct 3 only; conjuncts 1–2 vacuous) | none | S (as spot-check) |

## 4. External and admitted assumptions

- Structures: `ComplexN` with `cells : Nat → List (List Nat)`. This is a function on all of `Nat`; every complex reached from `emptyN` has finite support, but the type itself admits complexes with cells in infinitely many dimensions, and `WFComplex` quantifies over all `k`. Finitude flag: the "arbitrary finite dimension" of the title is the metatheory's ∀`k`; no system state holds more than finitely many dimensions, and nothing in the module claims otherwise.
- Declared conventions, named as such in the docstring (lines 38–44): fresh vertex supply, the ascending-list cell encoding, integer coefficients, the sign convention `sgn`, and the metatheoretic iteration of the driver.
- Hypotheses recurring: `shellN C k σ = true/false`; `WFComplex C`.
- Library lemmas doing work: `List.mem_append`, `List.mem_singleton`, `List.length_append`, `decide`, `omega`; `Bool.and_eq_true`.
- Unearned identity: none found.
- Unrestricted external universe: `combs 5 m` enumerates a declared finite set; `facets` uses `List.eraseIdx`. None beyond `ComplexN.cells : Nat → _`.
- Unbounded function treated as internally available: `cells : Nat → List (List Nat)` (flagged above).
- Silently assumed observer: none; the module states protection, observer, budget "do not appear in this module at all".
- Unspecified correspondence between presentations: none (no map to `PState`; the file does not use `HigherStructure`).
- Cost function without justification: none.
- Admitted condition later described as forced: none found — the docstring and the ledger (CL-PD2-LADDER-GENERAL) both state the theorem was "NARROWED" to guarded admission and is "NOT a homology claim".
- Finite computation presented as universal: `d2_zero_dims_2_3_4` is labelled a spot-check and the general theorem is cited as `BoundaryCancellation.d2_zero_unrestricted`. Correctly scoped in prose; but two of its three conjuncts are vacuous (§11).

## 5. Derived consequences

- `BoundaryCancellation` imports this module and uses `facets`, `ascB`, `sgn`, `bdN`, `pushN`, `coeffN`, `ComplexN`, `emptyN`, `nreplay`, `WFComplex`, `wf_nreplay`, `d4Events`, `d4Complex` (e.g. `d2_zero_replayed` via `wf_nreplay`; `d2_zero_d4` on `d4Complex`; the docstring at BoundaryCancellation.lean lines 8, 392, 404, 605, 647 names `d2_zero_dims_2_3_4`, `uniform_guarded_filler`, `wf_nreplay`, `pseudo_cell_countermodel`).
- Ledger: CL-PD2-LADDER-GENERAL cites all 13 theorems except `wf_empty`, `wf_stepV`, `wf_stepN`, `wf_nstep` (helpers). CL-PD2-BOUNDARY-CANCELLATION cites `wf_nreplay`. `paper/primitive_difference_map.md` lines 179, 274 and `paper/paper_change_log.md` items 5–8 of the PR #12 repair pass record the renaming/narrowing from `ladder_general`.

## 6. Counterexamples and limitations

- Countermodels: `pseudo_cell_countermodel` (the legacy guard admits `[0,0]`); `d4_guard_load_bearing` (missing facet ⇒ no 4-cell); `shell_refuses_general` as the general form of guard load-bearing.
- Not proved: any homology statement (said explicitly); any connection between `shellN` and the passage's `obstP` (the "two-rule shape" in the docstring of `uniform_guarded_filler`, line 97, is an analogy; the module uses nothing from the passage); that the filler is unique or forced (it is admitted by an `addC` event); the general composite vanishing (delegated to `BoundaryCancellation`).
- `shellN` requires `1 ≤ k`, so `stepN C 0 σ` is always inert; vertices enter only through `stepV`. The "uniform in dimension" statement is for `k ≥ 1`.
- `uniform_guarded_filler` is one `if_pos` unfolding plus a length argument; its content is that the declared step does what its guard says. Its value is the dimension-uniform statement, not depth.

## 7. Axiom dependencies

All 13 theorems in the artifact; axioms within {propext, Quot.sound}; `wf_empty` and `d2_zero_dims_2_3_4` report none. None exceed the whitelist.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 13 theorems appear in the axiom artifact. The ledger cites nine by name. Probe run (file `textbook/audit/probes/E/lg_vacuity.lean`, command `lake env lean <file>` inside `lean4/`, exit 0): with the sign function replaced by the constant `1` (a signless, wrong calculus) the first two conjuncts of `d2_zero_dims_2_3_4` still `decide` to `true`, while the genuine codimension-two check at dimension 2 and the third conjunct at dimension 4 `decide` to `false`; and `(pushN (bdN [0,1,2])).map (·.2) = [[2],[1],[2],[0],[1],[0]]` (the composite chain of a triangle is supported on 1-element lists, so coefficients on 2-element facets are trivially 0).

## 9. Related Python implementations

- `code/derivation/attachment_ladder.py` §5 "The generalized ladder (mirror of LadderGeneral), repaired": `facets`, `asc`, `shell_n`, `shell_n_legacy`, `step_n`, `sgn`, `bd_n`, `push_n`, `coeff_n`, `d2_zero_dim` (which checks coefficients over the actual support of the composite chain, `{t for (_, t) in ch}`, so the Python spot-check is not vacuous), `ladder_report`.
- `code/derivation/boundary_cancellation.py` §1 "The declared calculus (mirror of LadderGeneral)": `asc`, `facets`, `ascending_cells`.
- Tests: `tests/test_attachment_ladder.py::test_generalized_ladder_repaired` (asserts `all_d2_zero`, dimension-5 spot check via `d2_zero_dim((0,1,2,3,4,5))`).

## 10. Textbook placement proposal

- Prerequisites: the dimension-0–3 calculus of `HigherStructure` (`shell2`, `cstep`, `filling_not_forced`); lists as cells; the notion of a replayed invariant.
- Substantive: `uniform_guarded_filler`, `shell_refuses_general`, `pseudo_cell_countermodel`, `wf_nreplay`, `d4_demo`, `d4_guard_load_bearing`.
- Auxiliary: `shell_no_self_fill`, `wf_empty`, `wf_stepV`, `wf_stepN`, `wf_nstep`, `d4_wf`.
- Lesson title: "One guard for every dimension: admission over a complete, well-formed, unfilled boundary." Question answered: what single condition licenses adding a cell in any dimension, and what goes wrong (the `[0,0]` pseudo-cell) without strict ascent?
- Recommend omitting: `d2_zero_dims_2_3_4` — its first two conjuncts are vacuous (§11) and the general theorem `BoundaryCancellation.d2_zero_unrestricted` supersedes it; if mentioned, present only its third conjunct as a dimension-4 spot check. Do not present the guard as "the obstruction one dimension up" without saying it is an analogy to `obstP`, not a proved bridge.

## 11. Interpretation findings

1. **`d2_zero_dims_2_3_4` — PROOF DEFECT (vacuous statement, conjuncts 1 and 2).** Docstring (lines 313–317): "The composite boundary vanishes on the demonstration cells of dimensions 2, 3, and 4 (decided)." Ledger CL-PD2-LADDER-GENERAL: "the older dimension-2–5 computations are retained as spot-checks." Lean, conjunct 1: `(combs 5 2).all fun t => (facets t).all fun e => coeffN e (pushN (bdN t)) == 0`. For a 3-vertex `t`, `pushN (bdN t)` is a chain supported on 1-vertex lists, while `e` ranges over the 2-vertex facets of `t`; `coeffN e _` filters on `p.2 == e` and is therefore `0` for every chain whatsoever. Conjunct 2 has the same mismatch one dimension up (4-vertex `q`, 3-vertex `t2`, composite supported on 2-vertex lists). Only conjunct 3 (5-vertex top cell, 4-vertex facets `q`, 3-vertex faces `t2`, composite supported on 3-vertex lists) tests the right dimension. Probe (see §8): the first two conjuncts remain `true` with all signs replaced by `+1`; the correct codim-2 test at dimension 2 and conjunct 3 become `false`. The proof is kernel-correct; the statement's dimension-2 and dimension-3 parts are vacuous and provide no evidence. The claim "dimensions 2, 3, and 4" is thus supported in Lean only at dimension 4 by this theorem. The evidential gap is already closed elsewhere: `HigherStructure.d2_zero_triangles` and `d2_zero_tet` test the right dimensions on `k4`, and `BoundaryCancellation.d2_zero_unrestricted` / `d2_zero_facets` prove the general statement. The Python mirror `d2_zero_dim` is not vacuous. Recommendation for the textbook: cite `BoundaryCancellation` and do not cite this theorem for dimensions 2–3.
2. **`uniform_guarded_filler` — INTERPRETATION note (docstring analogy).** Docstring line 97–98: "the two-rule shape (obstruction-shaped precondition, structure-creating response), uniform in the dimension." Lean: a theorem about `stepN` under `shellN = true`; no passage notion (`obstP`, `prot`, `obs`) appears, and the module imports `HigherStructure` without using it. The ledger and docstring correctly say "a theorem about the declared guarded step, not a homology claim"; the textbook should also say "not a theorem about the passage's obstruction". Not a defect in the ledger wording.
3. **Finitude flag.** `ComplexN.cells : Nat → List (List Nat)` and "arbitrary finite dimension" (`∀ k`) are metatheoretic; no replayed complex has cells beyond finitely many dimensions (`d4Complex` has none above 4). No prose reads this as a system-internal totality; flagged for the matrix only.
4. Vacuity check of the remaining theorems: `shellN` is satisfiable (`d4_demo` fires every guard), so `uniform_guarded_filler` and `shell_no_self_fill` are non-vacuous; `shell_refuses_general` is non-vacuous (`pseudo_cell_countermodel`). None found beyond item 1.
