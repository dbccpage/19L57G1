# Audit: RefusalFrontier

| field | value |
|---|---|
| Path | lean4/Derivation/RefusalFrontier.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | f3bfd62198a86dd8 |
| Lines | 371 |
| Imported by root `Derivation.lean` | yes (line 19) |
| Imports | `Derivation.Refusal`, `Derivation.Bridge`, `Derivation.PrimDiff` |
| Declarations | 2 inductive (`AdmResult`, `MItem`), 3 structure (`JState`, `PState`, `MState`), 11 def (`stepTraced`, `storeSwap`, `stepJ`, `stepP`, `bridgeState`, `swapP`, `stepM`, `minState`, `stepU`, `stepRefl`, `reflState`), 1 instance (derived `DecidableEq`/`Repr` are `deriving`; the inventory counts one explicit instance — none appears in the source text, so "1 instance" in the inventory is the derive handler; not checked further), 20 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 20 lines (every theorem); axioms seen: none / `propext` / `propext, Quot.sound` |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

"Frontier Run 006" asks whether repeated presentation or attempted re-admission of one token can generate two-ness or a witnessed difference without importing a second token, hidden occurrence identity, undeclared order, or an already two-valued result algebra. The module holds the eight "theorem cores" of that run. T1: under silent deduplication any history of re-presentations fixes the state, horizon-free. T2: a traced runner that returns `isNew`/`existing` results has the silent replay as its state projection — results are host data; two histories of different lengths erase to one state. T3: a retained pair of result codes is distinguishable exactly when the codes differ, so two-ness there is imported by the result algebra. T4: the judgment variant grows a judgment store, never the carrier. T5: two declared priced protocols close the bridge in two presentations of one token — `stepP` (reification + tag + automatic relation, not swap-invariant) and `stepM` (receipt reification into a coproduct carrier + automatic relation, no tag store, no result store), the latter being the Python search's unique minimum for the witnessed targets. T6: the facts so produced still do not entail the irreflexivity law. T7: a fully general one-line invariance ceiling — an equivariant construction sends fixed points to fixed points. T8: three declared reflective semantics realize a fixed point, a two-cycle, and a chain whose carrier is `range (n+1)` and whose relation is successor, for every `n`. The header's rule is that fourteen distinctions (token, occurrence, presentation, attempt, result, state transition, datum, judgment, receipt, trace, carrier element, sort, relation instance, relation law, classifier) are never conflated.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `AdmResult` | 56 | inductive | `isNew`, `existing` — host-visible admission results | ADMITTED |
| `stepTraced` | 60 | def | silent step returning its result alongside the state | ADMITTED |
| `storeSwap` | 94 | def | swaps the two components of a `Nat × Nat` receipt store | ADMITTED |
| `JState` | 124 | structure | `data`, `judgments : List Nat` | ADMITTED |
| `stepJ` | 129 | def | re-admission appends a judgment; fresh admission appends a datum | ADMITTED (declared protocol R2) |
| `PState` | 179 | structure | `data`, `tags : List Nat`, `rel : List (Nat × Nat)` | ADMITTED |
| `stepP` | 185 | def | re-admission re-appends the token, tags the new index, asserts `(0, newIndex)`; fresh admission appends | ADMITTED (declared "sufficient, non-minimum" protocol) |
| `bridgeState` | 192 | def | `stepP (stepP ⟨[],[],[]⟩ 0) 0` | ADMITTED (concrete) |
| `swapP` | 203 | def | swaps indices 0/1 in `tags` and in both components of `rel`; `data` untouched | ADMITTED |
| `MItem` | 223 | inductive | `tok n` ⊕ `receipt n` — the coproduct carrier | ADMITTED |
| `MState` | 228 | structure | `data : List MItem`, `rel : List (Nat × Nat)` | ADMITTED |
| `stepM` | 236 | def | re-presentation of a present token appends `receipt (length)` and asserts `(0, length)`; fresh appends `tok t` | ADMITTED (declared minimum protocol) |
| `minState` | 242 | def | `stepM (stepM ⟨[],[]⟩ 0) 0` | ADMITTED (concrete) |
| `stepU` | 292 | def | `fun _ => true` on `Bool` (untyped reflection) | ADMITTED |
| `stepRefl` | 304 | def | appends the current length as a new datum, tags it, links `(len−1, len)` | ADMITTED (declared reflective semantics; ignores any token) |
| `reflState` | 309 | def | `Nat → PState`: `⟨[0],[],[]⟩` then iterate `stepRefl` | ADMITTED (a metatheoretic `Nat`-indexed family) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `silent_repetition_inert` | 29 | for any `h` and `s`, if every admitted token of `h` is already in `s.data`, then `h.foldl (stepR .silent) s = s` | CONDITIONAL:every admission of `h` is of a present token | propext, Quot.sound | S |
| `trace_erasure` | 69 | `(stepTraced s e).2 = stepR .silent s e` | FROZEN | propext, Quot.sound | S |
| `histories_collapse` | 82 | `replayR .silent [admitTok 0, admitTok 0] = replayR .silent [admitTok 0]` | VERIFIED_FINITE | propext, Quot.sound | S |
| `mono_code_swap_invariant` | 96 | `storeSwap (c,c) = (c,c)` | FROZEN (`rfl`) | none | A |
| `distinct_code_not_swap_invariant` | 99 | `c0 ≠ c1 → storeSwap (c0,c1) ≠ (c0,c1)` | FROZEN | none | A |
| `singleton_algebra_monochrome` | 105 | if both components of `p` equal `c` then `p = (c,c)` | FROZEN (trivial) | propext | A |
| `distinction_needs_two_constructors` | 113 | if `p.1 ≠ p.2` then there are two distinct values among `{p.1, p.2}` | FROZEN (trivial restatement; see §11) | none | A |
| `judgment_variant_second_judgment_not_datum` | 133 | three `stepJ 0` from empty give `data = [0]`, `judgments = [0,0]` | VERIFIED_FINITE | propext, Quot.sound | S |
| `judgment_carrier_bound` | 138 | for any `h : List Nat` of zeros and start `s` with `data ∈ {[], [0]}`, the fold keeps `data ∈ {[], [0]}` | CONDITIONAL:`∀ tok ∈ h, tok = 0`, start singleton-or-empty | propext, Quot.sound | S |
| `priced_bridge_closes` | 194 | `bridgeState` has 2 data, `rel = [(0,1)]`, all links off-diagonal, `tags = [1]` | VERIFIED_FINITE | propext, Quot.sound | S |
| `priced_bridge_oriented` | 210 | `swapP bridgeState ≠ bridgeState` | VERIFIED_FINITE | propext, Quot.sound | S |
| `min_witnessed_route_closes` | 249 | `minState.data = [tok 0, receipt 1]`, `minState.rel = [(0,1)]`, all links off-diagonal | VERIFIED_FINITE (one concrete two-step state) | propext | S |
| `bridge_facts_not_law` | 261 | there is `r' : Nat → Nat → Prop` containing every pair of `bridgeState.rel` with `¬ Irrefl r'` (witness: constant `True`) | REFUTED (countermodel to "the bridge's facts entail the law"); the witness does not depend on `bridgeState` | propext, Quot.sound | S |
| `equivariant_output_invariant` | 276 | for any `actS`, `actR`, `F` with `F (actS s) = actR (F s)`: `actS s = s → actR (F s) = F s` | FROZEN (generic over `Type`s) | none | S |
| `untyped_reflect_fixpoint` | 294 | `stepU (stepU s) = stepU s` | VERIFIED_FINITE | none | A |
| `toggle_two_cycle` | 298 | `!(!s) = s ∧ !s ≠ s` on `Bool` | VERIFIED_FINITE | none | A |
| `reflective_chain_growth` | 316 | `∀ n, (reflState n).data.length = n + 1` | FROZEN (∀ n, metatheoretic) | propext | S |
| `reflective_chain_is_initial_segment` | 333 | `∀ n, (reflState n).data = List.range (n+1)` | FROZEN | propext | S |
| `reflective_chain_successor_relation` | 347 | `∀ n, (reflState n).rel = (range n).map (k ↦ (k, k+1))` | FROZEN | propext | S |
| `reflective_chain_irreflexive_facts` | 363 | `∀ n, ∀ p ∈ (reflState n).rel, p.1 ≠ p.2` | FROZEN (follows from the successor shape; `omega`) | propext, Quot.sound | S |

## 4. External and admitted assumptions

- **Every protocol is a declared step function** (`stepTraced`, `stepJ`, `stepP`, `stepM`, `stepRefl`, `stepU`). The module proves what each declaration realizes; it derives none of them. The paper says so repeatedly ("Realization, not derivation").
- **Positions as data.** `stepP`, `stepM` and `stepRefl` use `s.data.length` as the new index/receipt/datum and as a relation endpoint. The chain `reflState n` has `data = range (n+1)`: its elements *are* list positions. Finitude flag: the "numerals" here are the metatheory's `Nat` indices written into a list by a declared constructor; the paper's FR10 says exactly this ("the successor shape is the declaration's content"; "Refusal by itself derives no numerals — that reading is explicitly disclaimed"). The textbook must keep that disclaimer.
- **`reflState : Nat → PState`** is a `Nat`-indexed family of states; "the chain" as a single object (the ordinals below ω in the post-hoc section) is a metatheoretic reading of that family, not a state of any system. Flagged; no prose found treating the totality as object-level.
- **Universe parameters** `{S R : Type}` in `equivariant_output_invariant`: arbitrary external types; the lemma is a triviality about any maps, acknowledged as such ("fully general, one line").
- **Decidability / `decide`:** all concrete facts are `decide` on small lists of `Nat`/`MItem`.
- **Library lemmas doing work:** `List.range_succ`, `List.map_append`, `List.length_append`, `List.mem_map`, `omega`, `simp_all`.
- Unearned identity: none found. Unrestricted external universe: `S R : Type` in T7 only. Unbounded function treated as internally available: `reflState` and `s.data.length` — flagged above; declared in the paper. Silently assumed observer: the tag and the relation are the observers, declared (`stepP`, `stepRefl`). Unspecified correspondence between presentations: none in Lean (the "minimum in the 44-protocol class" correspondence between `stepM` and a Python protocol is a reading, see §11). Cost function without justification: the two cost orders A and B are Python (`cost_a`, `cost_b`), declared, not in Lean. Admitted condition later described as forced: none found. Finite computation presented as universal: see §11 item 1 (minimality is finite-class Python; the Lean verifies closure only).

## 5. Derived consequences

`Generator` opens this namespace and builds on `stepRefl`, `reflState`, `PState`, `reflective_chain_growth`, `reflective_chain_is_initial_segment`, `reflective_chain_successor_relation` (its `reflective_chain_tags`, `chain_tagged_iff`, `chain_hasIn_iff`, `chain_hasOut_iff`, the profile theorems and the depth-2 results all rest on them); `SeparationCapacity`, `CapacityBound`, `LocalStrategy`, `G1Class` inherit through `Generator`. Paper: `paper/refusal_as_difference.md` FR3–FR10 (owner); `paper/native_derivation_map.md` rows "admission ⇒ two-ness PROVED (`min_witnessed_route_closes`, `reifyUntagged_eq_occurrence`)", "two-ness ⇒ orientation FALSE (`equivariant_output_invariant`)", "irreflexivity fact ⇒ law FALSE (`bridge_facts_not_law`)". Ledger: `CL-FR6-T1-INERTIA` (`silent_repetition_inert`), `CL-NO-UNIVERSAL-PROPERTY` (names the file), `CL-G-DIRECT-SWAP` (contrast with `equivariant_output_invariant`); ledger line 873 records the 44-protocol, 6-event scope of the computed parts. No ledger entry lists `min_witnessed_route_closes` or the T8 chain theorems by name (grep of `RefusalFrontier.` in the ledger: two hits only) — "not checked" whether they are listed under short names elsewhere in the ledger.

## 6. Counterexamples and limitations

- `histories_collapse`: two histories, one state. `bridge_facts_not_law`: the total relation. `priced_bridge_oriented`: the bridge state is moved by the swap. `toggle_two_cycle`: a two-cycle exists under a declared semantics.
- **Scope of `min_witnessed_route_closes` (the brief's question).** The Lean proves, by `decide`, that one concrete declared protocol (`stepM`) applied twice to one token from the empty `MState` yields `data = [tok 0, receipt 1]`, `rel = [(0,1)]`, off-diagonal. It proves nothing about minimality, uniqueness, cost orders, or any other protocol. "The unique minimum witnessed route" and "the same under both cost orders" are findings of the Python search over the declared 44-protocol class (`enumerate_protocols`, `minimum_table`, `cost_a`, `cost_b`) at the 6-event horizon with carrier cap 4 (paper FR1, FR6; ledger line 873). That `stepM` *is* the protocol the search selected (datum retention + autorel, no tag, singleton algebra, one token) is a correspondence stated in prose, not a Lean fact — `MState`/`stepM` are hand-written to have "no tag store and no result store", which is the structural shadow of that correspondence. The 44-protocol class is itself a declared search space (algebra ∈ {1,2 constructors} × retention ∈ {none, judgment, occurrence, datum} × tag × reflection × autorel × tokens, with constraints), "not a curated list" per FR1.
- **Scope of `reflective_chain_irreflexive_facts`.** For every `n`, every link of `reflState n` is off-diagonal. This is a consequence of `reflective_chain_successor_relation` (links are `(k, k+1)`); it says nothing about the irreflexivity *law* (T6 keeps that separate) and nothing about any other reflective semantics. The chain never takes a token as input: `stepRefl` reads only `s.data.length`, and `reflState 0 = ⟨[0],[],[]⟩` is given, so "one token generates a chain" (docstring line 302) means "the declared constructor iterated from a one-element state".
- Not proved: the nine-notion implication matrix (Python); the target-relative dependency normal form (Python, FR8 `[unresolved]` for a Lean form); any classification of invariant substructures beyond `Bool` (FR9 open); initiality of the chain (F4 open); that the stratification `history < state < carrier < separable < witnessed < law` is a single theorem (it is assembled from separate facts and Python rows).
- `distinction_needs_two_constructors` and `singleton_algebra_monochrome` are immediate from their hypotheses; the "dependency theorem" reading in FR4 is carried by the Python checks (`normal_form_check`), not by these lines.

## 7. Axiom dependencies

All 20 within `{propext, Quot.sound}`; 7 use none. None exceed: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 20 theorems are in `artifacts/lean_axioms.txt` and the root inventory; the paper cites all 20 (FR3–FR10 and the TERMINAL block). No probe run: every concrete theorem is `decide` on a two- or three-step state and the four chain theorems are inductions read in full.

## 9. Related Python implementations

`code/derivation/refusal_frontier.py`: `Proto`, `enumerate_protocols` (44), `FState`, `_refuse`, `step_f`, `events_of`, `reachable_f`, `notions`, `swap_first_two`, `oriented_two`, `protocol_report`, `cost_a`, `cost_b`, `minimum_table`, `normal_form_check`, `notion_matrix`; artifact `artifacts/refusal_frontier.json`. Tests `tests/test_refusal_frontier.py`: `test_protocol_space_size_and_validity`, `test_silent_protocol_is_inert`, `test_relation_route_reaches_witnessed_irreflexive`, `test_judgment_protocol_two_states_only`, `test_reflection_grows_to_cap`, `test_refusal_links_are_born_irreflexive_in_class`, `test_minimum_table_ties_and_disagreement`, `test_witnessed_minimum_unique_under_both_orders`, `test_normal_form_holds`, and others.

## 10. Textbook placement proposal

- Prerequisites: Refusal (the five modes, `stepR`, `replayR`), Bridge (`irrefl_law_not_entailed`, `equivariant_witness_is_S2`), PrimDiff (`Irrefl`), `List.range`.
- Substantive: `silent_repetition_inert`, `trace_erasure` + `histories_collapse`, `judgment_carrier_bound`, `priced_bridge_closes` + `priced_bridge_oriented`, `min_witnessed_route_closes` (taught *with* its scope: closure of one declared protocol; minimality is the finite search), `bridge_facts_not_law`, `equivariant_output_invariant`, the four `reflective_chain_*` theorems (taught with the "realization, not derivation" disclaimer). Auxiliary: the T3 quartet (`mono_code_swap_invariant`, `distinct_code_not_swap_invariant`, `singleton_algebra_monochrome`, `distinction_needs_two_constructors`), `judgment_variant_second_judgment_not_datum`, `untyped_reflect_fixpoint`, `toggle_two_cycle`.
- Lesson title: "Refusal routes and their prices." Question answered: which declared ways of recording a refused re-presentation of one token reach a witnessed, oriented pair, and what each imports.
- Recommend omitting: `distinction_needs_two_constructors` and `singleton_algebra_monochrome` (restatements of their hypotheses; the FR4 content lives in the Python normal-form checks), `mono_code_swap_invariant` (`rfl`).

## 11. Interpretation findings

1. `min_witnessed_route_closes` — paper TERMINAL: "The witnessed milestones have a **unique minimum bridge** ... now also verified in Lean (`min_witnessed_route_closes`)"; FR6: "**[theorem]** (`min_witnessed_route_closes`) The *unique minimum* witnessed route — the same single protocol under **both** cost orders ... verified in Lean". Lean: `minState.data = [tok 0, receipt 1] ∧ minState.rel = [(0,1)] ∧ ∀ p ∈ minState.rel, p.1 ≠ p.2`, by `decide` on one concrete state. Uniqueness, minimality and cost-order independence are not in the statement; they are Python results over the declared 44-protocol class at horizon 6 (the paper's own "Computed only within bounds" bullet says this). The sentence "now also verified in Lean" is true of *closure* only. Classification: INTERPRETATION DEFECT (the `[theorem]` tag in FR6 is attached to a sentence most of whose content is `[finite computation]`; the Lean verifies the route closes, not that it is minimum or unique).
2. `reflective_chain_*` — docstring line 302: "One token generates a chain"; FR10 and the post-hoc section: "realizing the ordinals below omega". Lean: `reflState : Nat → PState` with `stepRefl` reading only `s.data.length`; the start state `⟨[0],[],[]⟩` is given, no token event occurs. The paper disclaims derivation ("Refusal by itself derives no numerals"), so no false claim; but the phrase "one token generates" and "horizon-free chain growth" should be read as "a declared constructor iterated in the metatheory for every `n`". Finitude rule: the chain as a completed object is a `Nat`-indexed metatheoretic family. Classification: INTERPRETATION DEFECT (minor; docstring wording) and a finitude flag.
3. `distinction_needs_two_constructors` — docstring: "The dependency theorem (finite core): a distinguishable retained pair yields two distinct constructor codes occurring in the store — the distinction was purchased with the result algebra." Lean: from `p.1 ≠ p.2` conclude `∃ a b, a ≠ b ∧ a ∈ {p.1,p.2} ∧ b ∈ {p.1,p.2}` with `a := p.1`, `b := p.2`. The statement is the hypothesis rephrased; nothing about result algebras, stores or purchase occurs. Vacuity check: not vacuous, but content-free relative to its name. Classification: INTERPRETATION DEFECT (minor; the dependency claim is carried by Python `normal_form_check`).
4. `bridge_facts_not_law` — FR7: "The priced bridge's facts do not entail the law: a superset relation with a self-edge extends them." Lean: the witness is the constant-`True` relation, which extends *every* relation; the theorem does not inspect `bridgeState`. Correct and trivially so; the general form is `Bridge.irrefl_law_not_entailed`. Not a defect; noted as trivial.
5. The stratification `history < state < carrier two-ness < carrier separability < witnessed relation < law` (TERMINAL) is attributed to five separate items, two of which (`two_carrier ↛ separable_pair`, `separable_pair ↛ witnessed_relation`) are Python matrix cells, not Lean theorems; the paper labels them with backticked keys rather than theorem names, so this is correctly signposted. No defect.
6. Vacuity: `silent_repetition_inert`'s hypothesis is satisfiable (e.g. empty history); `judgment_carrier_bound` likewise. None vacuous.
