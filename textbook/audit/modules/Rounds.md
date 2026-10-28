# Audit: Rounds

| field | value |
|---|---|
| Path | lean4/Derivation/Rounds.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | f81985bbff91318e |
| Lines | 482 |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.TransitionTransport, Derivation.Counting |
| Declarations | 1 structure (`Round`), 1 inductive (`ClosedRun : Regime → List Round → Regime → Prop`), 25 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 21 lines; axioms seen: none (`filter_none_of_all_false`), propext, propext+Quot.sound. Not in artifact: `nodup_head'`, `nodup_tail'`, `filter_nodup'`, `range_nodup'` |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
Rounds discharges residual R8: Counting proved the abstract laws (a strictly increasing bounded measure has boundedly many states; the requirement language on `n` data has `n(n-1)/2` elements) but their hypotheses had been checked of the transition system only computationally. The module declares the minimal Lean object that represents a run — a list of rounds, each an imposed target plus a response delta, chained by the engine's `respond` under two side conditions (the target is fresh; the response admits no datum) — and proves that under that shape each round raises the requirement count by exactly one over a fixed datum count, requirements stay ordered, bounded and duplicate-free, and hence a closed run from an empty store makes at most `n(n-1)/2` rounds, stated division-free. The counting is done with choice-free `decide`-filter lemmas because the toolchain's `List.nodup_range`/`length_erase` routes pull in `Classical.choice`, which the axiom boundary forbids. What stays computational is narrowed to one fact: that every exported round has the declared syntactic shape.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `Round` | 283 | structure | `target : Nat × Nat`, `response : List Item` | ADMITTED (declared round shape) |
| `ClosedRun r rds t` | 291 | inductive Prop | `nil`; `cons` requires `rd.target ∉ r.reqs`, `newDatum ∉ rd.response`, `respond r i j δ = some mid`, `ClosedRun mid rds t` | ADMITTED (declared policy: freshness and datum fixity are hypotheses of the shape, mirroring engine invariants) |

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `filter_length_split` | 55 | `(l.filter p).length + (l.filter (!p)).length = l.length` | FROZEN | propext, Quot.sound | A |
| `nodup_head'` | 78 | head of a nodup list differs from every tail member | FROZEN | not in artifact | A |
| `nodup_tail'` | 83 | tail of a nodup list is nodup | FROZEN | not in artifact | A |
| `filter_none_of_all_false` | 88 | if `p` is false on all of `l`, `l.filter p = []` | FROZEN | none | A |
| `filter_nodup'` | 99 | filter of a nodup list is nodup | FROZEN | not in artifact | A |
| `nodup_filter_self_length` | 116 | in a nodup list containing `a`, exactly one member equals `a` (`DecidableEq α`) | FROZEN | propext | A |
| `nodup_subset_length` | 145 | a nodup list included in a nodup list is no longer (`DecidableEq α`) | FROZEN | propext, Quot.sound | S |
| `nodup_append_singleton` | 169 | `a ∉ l → l.Nodup → (l ++ [a]).Nodup` | FROZEN | propext | A |
| `allPairs_mem_bound` | 190 | `q ∈ allPairs n → q.1 < q.2 ∧ q.2 < n` | FROZEN | propext, Quot.sound | A |
| `mem_allPairs` | 205 | converse | FROZEN | propext, Quot.sound | A |
| `nodup_map_of_inj` | 222 | map by a function injective on the list preserves nodup | FROZEN | propext, Quot.sound | A |
| `range_nodup'` | 240 | `(List.range n).Nodup`, choice-free | FROZEN | not in artifact | A |
| `nodup_append_disjoint` | 249 | disjoint nodup lists append to nodup | FROZEN | propext | A |
| `allPairs_nodup` | 264 | `(allPairs n).Nodup` | FROZEN | propext, Quot.sound | A |
| `applyItem_data_eq` | 301 | a non-`newDatum` item that applies leaves `data` unchanged | CONDITIONAL: `it ≠ newDatum` | propext | A |
| `applyDelta_data_eq` | 328 | a delta with no `newDatum` that applies leaves `data` unchanged | CONDITIONAL: `newDatum ∉ δ` | propext | A |
| `respond_anatomy` | 355 | `respond r i j δ = some s` implies `i < j`, `j < r.data`, `s.reqs = insertNew r.reqs (i,j)`, and the delta applied to the imposed regime gives `s` | FROZEN | propext | S |
| `round_reqs_succ` | 380 | if `(i,j) ∉ r.reqs` and the round succeeds, `s.reqs.length = r.reqs.length + 1` | CONDITIONAL: freshness `(i,j) ∉ r.reqs` | propext | S |
| `round_data_eq` | 389 | if `newDatum ∉ δ` and the round succeeds, `s.data = r.data` | CONDITIONAL: `newDatum ∉ δ` | propext | S |
| `closedRun_data_eq` | 398 | a closed run fixes `data` | FROZEN (over `ClosedRun`) | propext | A |
| `closedRun_reqs_length` | 405 | `t.reqs.length = r.reqs.length + rds.length` | FROZEN (over `ClosedRun`) | propext, Quot.sound | S |
| `closedRun_reqs_nodup` | 415 | if `r.reqs.Nodup` then `t.reqs.Nodup` | CONDITIONAL: `r.reqs.Nodup` | propext | A |
| `closedRun_reqs_wf` | 425 | if every starting requirement is ordered and bounded by `r.data`, so is every final one by `t.data` | CONDITIONAL: `hwf` | propext | A |
| `closedRun_round_bound` | 452 | under `r.reqs.Nodup` and `hwf`: `2 * (r.reqs.length + rds.length) ≤ r.data * (r.data − 1)` | CONDITIONAL: `r.reqs.Nodup`, `hwf` | propext, Quot.sound | S |
| `closedRun_round_bound_from_empty` | 472 | if `r.reqs = []`, `2 * rds.length ≤ r.data * (r.data − 1)` | CONDITIONAL: `r.reqs = []` (and the `ClosedRun` shape) | propext, Quot.sound | S |

## 4. External and admitted assumptions
- `ClosedRun` is a DECLARED shape, not derived from the closure policy: freshness of the imposed target and absence of `newDatum` in the response are constructor hypotheses. The docstring and the paper say so and name what would be needed to derive them (formalising collapsed-pair selection and acceptance). That the exported runs have this shape is a Python receipt (`test_no_supply_variant_terminates_within_pair_bound`, `claims.json:CL-CLOSURE-TERMINATION`).
- `respond` (TransitionTransport), `allPairs`, `allPairs_length` (Counting), `insertNew_of_not_mem`, `mem_insertNew` (Basic).
- Library lemmas doing real work: `List.filter_cons_of_pos/neg`, `List.mem_filter`, `List.mem_map`, `List.mem_range`, `List.range_succ`, `List.Pairwise.cons`, `decide_eq_true/false`, `omega`. `DecidableEq α` instance in the two counting lemmas (used via `decide (x = a)`); on `Nat × Nat` it is the core structural instance. No `Classical`.
- Universe parameters: `{α : Type}` (Type 0 only) in the list lemmas — metatheory.
- `Nat → X` as data: `g : Nat → α` in `nodup_map_of_inj` (metatheory, instantiated at `fun i => (i, m)`).
- Unearned identity: none found. Unrestricted universe: none. Unbounded function as internal: none. Silent observer: none. Presentation correspondence: the correspondence between `ClosedRun` and the engine's actual run objects is declared (docstring "the engine's exact event sequence (`respond`)") and checked only computationally — recorded, not a defect. Cost function: none. Admitted condition later described as forced: none found (the paper tags the theorem "[theorem, under the declared round shape]"). Finite computation as universal: none found.

## 5. Derived consequences
No other Lean module uses these names (grep). The ledger row CL-CLOSURE-TERMINATION (Lean bullet) and paper 9 ("[theorem, under the declared round shape]") and register row R8 ("DISCHARGED 2026-08-18") rest on `round_reqs_succ`, `round_data_eq`, `closedRun_round_bound_from_empty`, `nodup_subset_length`.

## 6. Counterexamples and limitations
No countermodels. Not proved: that the closure policy produces only fresh targets; that any response omits `newDatum` (the open-system engine with `supply=True` admits data — the bound is for the closed baseline only); termination of the ENGINE (the theorem bounds the length of any `ClosedRun`, which is a bound on rounds given the shape, not a proof that the engine's search reaches the all-pairs fixpoint — that is the `[bounded theorem]` "closed-system termination" in paper 9, computational); that the bound is attained. The division-free form `2·rounds ≤ n(n−1)` is exactly what is proved; the paper's "at most n(n−1)/2 rounds" is its integer reading.

## 7. Axiom dependencies
All 21 artifact lines within {propext, Quot.sound}; `filter_none_of_all_false` none. Three of the four helpers not in the artifact were probed (probe2.lean, exit 0): `nodup_head'` none; `filter_nodup'` propext; `range_nodup'` propext, Quot.sound (choice-free, as the docstring claims). `nodup_tail'` not probed (same shape as `nodup_head'`). None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). 21 of 25 theorems in the artifact (root inventory). Paper 9, register R8, ledger CL-CLOSURE-TERMINATION, change log 1867–1870 cite them. No extra probe.

## 9. Related Python implementations
`code/derivation/engine.py` (closed baseline `supply=False`; the round loop; the assertion that imposed targets are disjoint from standing requirements), `code/derivation/export.py` (branch reports, `every_maximal_branch_terminates`, `within_bound`). Tests: `tests/test_engine.py::test_no_supply_variant_terminates_within_pair_bound`, `::test_closed_system_terminal_at_round_boundary` (named in the ledger; location not checked), `::test_closure_policy_fixpoint`.

## 10. Textbook placement proposal
- Prerequisites: Basic (`respond`-level transitions via TransitionTransport), Counting (`allPairs`, `allPairs_length`, `no_supply_round_bound`), the notion of a closed system (no supply).
- Substantive: `ClosedRun` (and why its two side conditions are declared), `respond_anatomy`, `round_reqs_succ`, `round_data_eq`, `closedRun_reqs_length`, `closedRun_round_bound(_from_empty)`, `nodup_subset_length` (as the counting tool). Auxiliary: all list lemmas and the `*_data_eq`, `*_nodup`, `*_wf` propagations.
- Lesson title: "How many demands can a closed system meet?". Question: given `n` data and no supply, why can there be at most `n(n−1)/2` accepted rounds, and what about the engine is NOT proved by that bound?
- Omit: the choice-free list toolkit (`filter_*`, `nodup_*`, `range_nodup'`) from the main text; keep as an appendix note on the axiom boundary.

## 11. Interpretation findings
- Paper 9 / ledger: "under the declared round shape (a fresh imposed target, a response admitting no fresh datum) each round grows the requirement count by exactly one over a fixed datum count, and a closed run from an empty store makes at most n(n−1)/2 rounds". Lean: exactly that, with `ClosedRun`'s hypotheses. Match; the paper also names the computational residual. none found.
- Register row R8 header: "Counting-law hypotheses connected to the transition system — DISCHARGED" with the parenthesis "(under the declared round shape; that exported rounds have that shape stays computational)". Exact.
- Finitude: `allPairs n` over Lean `Nat` is metatheory; the paper reads it as the requirement language of a regime with `n` admitted data — a bounded finite object per regime. none found.
- Vacuity: `ClosedRun` is inhabited (the `nil` constructor; and a one-round run from `R2L`-shaped regimes exists via `mark_progress`-type deltas — not checked by probe); `closedRun_round_bound_from_empty` with `rds = []` is trivially `0 ≤ …`, the non-trivial content is for `rds ≠ []`, which exists computationally (the exported runs). none found.
