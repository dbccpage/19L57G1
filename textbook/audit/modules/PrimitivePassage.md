# Audit: PrimitivePassage

| field | value |
|---|---|
| Path | lean4/Derivation/PrimitivePassage.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | e14ca1a035e90e2d |
| Lines | 1298 |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.PrimDiff, Derivation.PrimitiveCore |
| Declarations | 1 structure (`PState`), 1 inductive (`PEvent`), 29 defs, 58 theorems. (The inventory's "lemma: 1 / `restates`" is a false positive from the docstring at line 320, "This lemma restates that branch"; there is no declaration named `restates`.) |
| Axiom reports in `artifacts/lean_axioms.txt` | 56 lines; axioms seen: none (2: `wit_independent_of_obs`, `quotient_no_recovery`) and propext+Quot.sound (54). Not in artifact: `asserted_offdiag_step`, `retained_sub_asserted_step` (probe: propext, Quot.sound). |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module is the executable dynamics of the "passage" through primitive difference: a small state machine whose state separates every notion the programme keeps apart — admitted occurrences, an *asserted* witness store, a *retained* witness store, a *protected-demand* store, an optional *declared observation* (a list of columns, each a list of occurrence positions; `none` is pre-observational), a budget, a licence flag, a refusal record and an absorbing terminal flag. Events admit occurrences, assert and then retain a witness, protect it, declare an observation, refine or add a column, refuse, set budget or licence, and halt. On this state it defines the zero relation of a declared observation (no column separates the pair), proves it is an equivalence before any quotient is taken (P4), defines *active obstruction* as "retained, protected, observation declared, and observer-zero on the pair", proves that this three-factor predicate equals the conjunction of four total gates and that no gate follows from the other three (P5), prices the pre-observational `none ⇒ not obstructed` branch as a declared policy against a named rival reading, proves the two-rule theorem (at an in-bounds active obstruction the repair family is nonempty or certified empty with the extension family nonempty, P7), shows that proposal is not execution (licence and budget gate column creation), that refusal is an inert record and the terminal absorbs, that replay is append-transparent, that an executed separating column resolves the obstruction on re-evaluation, and that the represented next-event family is empty exactly at quiescence and complete on both the repair and the extension side. It also transports `PrimitiveCore` candidate A into the passage: every replayed state's asserted store is off-diagonal, so an asserted pair induces a `Setting` satisfying A before anything is retained. The header records that the thirteen station names were supplied as an external challenge, not derived.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `PState` | 77 | structure | `occ`, `asserted`, `wit`, `prot`, `obs : Option (List (List Nat))`, `budget`, `licensed`, `refusals`, `halted`; `DecidableEq` | ADMITTED (the passage state; nine declared separate fields) |
| `genesisP` | 89 | def | empty state, `obs := none`, `licensed := true`, `budget := 0` | ADMITTED |
| `PEvent` | 93 | inductive | 11 event constructors | ADMITTED (declared event alphabet) |
| `sepCol` | 110 | def | one column separates `i`,`j` (membership xor) | ADMITTED |
| `sepP` | 115 | def | some declared column separates | ADMITTED |
| `zeroP` | 121 | def | `!sepP`; the zero relation of a declared observation | ADMITTED |
| `obstP` | 147 | def | retained ∧ protected ∧ (`none ⇒ false` / `some cols ⇒ zeroP cols`) | ADMITTED; the `none ⇒ false` branch is a DECLARED POLICY (docstring, ledger CL-PD2-PACKET-05P) |
| `retainedP` | 168 | def | gate 1 | ADMITTED |
| `protectedP` | 172 | def | gate 2 | ADMITTED |
| `declaredP` | 176 | def | gate 3 | ADMITTED |
| `zeroDeclP` | 184 | def | gate 4, `none ⇒ true` | ADMITTED; DECLARED CONVENTION (vacuous truth) |
| `zeroStrictP` | 195 | def | rival gate 4, `none ⇒ false` | ADMITTED (named only for `strict_gate_entails_declared`) |
| `obstEmptyObs` | 382 | def | rival policy: `none` read as the empty observation | ADMITTED (named rival policy) |
| `preRetainedObstructed` | 397 | def | state: two occurrences, (0,1) asserted, retained, protected, `obs = none` | ADMITTED (witness) |
| `gateWitnessNoZero` | 425 | def | as above with `obs = some [[0]]` | ADMITTED (witness) |
| `gateWitnessNoDeclaration` | 433 | def | `obs = none` (identical data to `preRetainedObstructed`) | ADMITTED (witness) |
| `gateWitnessNoProtection` | 441 | def | `prot = []`, `obs = some []` | ADMITTED (witness) |
| `gateWitnessNoRetention` | 449 | def | `wit = []`, `obs = some []` | ADMITTED (witness) |
| `gateWitnessAll` | 456 | def | all four gates, `obs = some []` | ADMITTED (witness) |
| `wfPair` | 592 | def | `i ≠ j`, both `< occ.length` | ADMITTED |
| `refineOk` | 599 | def | same-level acceptance guard | ADMITTED (declared policy) |
| `colOk` | 614 | def | column-creation acceptance guard | ADMITTED (declared policy) |
| `step` | 622 | def | the transition function | ADMITTED (the declared kernel) |
| `replayP` | 678 | def | `foldl step` | ADMITTED |
| `inducedSetting` | 755 | def | `Setting` with `X := Nat`, `r` = membership in `asserted`, stores from `wit`/`prot`, `Ops` empty | ADMITTED (note `X := Nat`, see §4) |
| `preRetained` | 848 | def | replay of admit 0, admit 1, assert (0,1) | ADMITTED |
| `responseMenu` | 961 | def | declared columns × in-bounds points | ADMITTED (declared response universe) |
| `repairFamily` | 970 | def | menu filtered by `refineOk` and separation | ADMITTED |
| `extensionProposals` | 997 | def | singleton columns over admitted positions, `colOk` and separating | ADMITTED (declared extension universe) |
| `obstructedPairs` | 1224 | def | protected pairs that are obstructed | ADMITTED |
| `nextFamilyP` | 1227 | def | repair blocks and funded extension blocks per obstructed pair | ADMITTED (declared interpreter; `setBudget 1` is a declared self-funding policy) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `zeroP_cons` | 124 | `zeroP (c :: rest) i j = (!sepCol c i j && zeroP rest i j)` | FROZEN | propext, Quot.sound | A |
| `obstP_strict_factors` | 202 | `obstP = retainedP && protectedP && zeroStrictP` (`rfl`) | FROZEN (definitional) | p,Q | A |
| `obstP_factors` | 218 | `obstP s i j = retainedP && protectedP && declaredP && zeroDeclP`, all `s`, `i`, `j` | FROZEN (near-definitional, as its docstring says) | p,Q | S |
| `obst_of_gates` | 227 | four gates true ⇒ `obstP = true` | FROZEN | p,Q | A |
| `gates_of_obst` | 237 | `obstP = true` ⇒ four gates true | FROZEN | p,Q | A |
| `obstP_reads_three_stores` | 253 | states agreeing on `wit`, `prot`, `obs` have the same `obstP` | FROZEN | p,Q | A |
| `undeclared_gates` | 264 | `obs = none` ⇒ `declaredP = false ∧ zeroDeclP = true` | CONDITIONAL:`s.obs = none` | p,Q | A |
| `obs_gates_not_both_false` | 281 | `declaredP s || zeroDeclP s i j = true` always | FROZEN | p,Q | S |
| `strict_gate_entails_declared` | 292 | `zeroStrictP = true ⇒ declaredP = true` | FROZEN | p,Q | A |
| `wit_independent_of_obs` | 309 | replacing `obs` leaves membership in `wit` unchanged (`Iff.rfl`) | FROZEN (definitional) | none | A |
| `obst_requires_observation` | 326 | `obs = none ⇒ obstP = false` | CONDITIONAL:`s.obs = none`; unfolds a DECLARED POLICY | p,Q | S |
| `obst_agrees_when_declared` | 338 | `obs = some cols ⇒ obstP = retained && protected && zeroP cols` | CONDITIONAL:`s.obs = some cols` | p,Q | A |
| `obst_diverges_when_undeclared` | 361 | a closed Bool expression is `true` ∧ `obstP` of a named `none`-state is `false` | VERIFIED_FINITE (first conjunct is a closed truth not about the state — module and ledger say so) | p,Q | A |
| `obst_policies_agree_when_declared` | 390 | `obs = some cols ⇒ obstP = obstEmptyObs` | CONDITIONAL:`s.obs = some cols` | p,Q | S |
| `obst_policies_differ` | 408 | at `preRetainedObstructed`, `obstEmptyObs = true ∧ obstP = false` | VERIFIED_FINITE (`decide`) | p,Q | S |
| `obst_conditions_independent` | 476 | five concrete states with all four gate values and the `obstP` verdict stated | VERIFIED_FINITE (`decide`) | p,Q | S |
| `gate_zero_independent` | 521 | ¬(∀ s i j, gates 1–3 ⇒ gate 4) ∧ ¬(∀ s i j, gates 1–3 ⇒ obstP) | REFUTED (entailment), witness `gateWitnessNoZero` | p,Q | S |
| `gate_declared_independent` | 539 | same with gate 3 omitted; witness `gateWitnessNoDeclaration` | REFUTED | p,Q | S |
| `gate_protection_independent` | 555 | gate 2 omitted; witness `gateWitnessNoProtection` | REFUTED | p,Q | S |
| `gate_retention_independent` | 571 | gate 1 omitted; witness `gateWitnessNoRetention` | REFUTED | p,Q | S |
| `assertion_not_retained` | 692 | after admit 7, admit 8, assert (0,1): `asserted = [(0,1)]`, `wit = []` | VERIFIED_FINITE | p,Q | S |
| `retention_not_free` | 702 | after two admissions both stores are empty | VERIFIED_FINITE | p,Q | A |
| `retention_requires_assertion` | 711 | live state, pair unasserted ⇒ `admitWit` is inert | CONDITIONAL:`halted = false`, `(i,j) ∉ asserted` | p,Q | S |
| `retention_persists` | 725 | `wit` is append-only under every event | FROZEN | p,Q | S |
| `assertion_persists` | 734 | `asserted` is append-only under every event | FROZEN | p,Q | A |
| `asserted_offdiag_step` | 766 | one step preserves "asserted store off-diagonal" | FROZEN | not in artifact (probe: p,Q) | A |
| `asserted_offdiag` | 787 | every replay from genesis has an off-diagonal asserted store | FROZEN | p,Q | S |
| `retained_sub_asserted_step` | 800 | one step preserves `wit ⊆ asserted` | FROZEN | not in artifact (probe: p,Q) | A |
| `retained_sub_asserted` | 821 | from genesis, `wit ⊆ asserted` | FROZEN | p,Q | S |
| `assert_transport` | 838 | `(a,b) ∈ asserted` of a replayed state ⇒ `PrimitiveCore.A (inducedSetting … a b)` | CONDITIONAL:`(a,b) ∈ (replayP h genesisP).asserted` | p,Q | S |
| `kernel_enters_preretained` | 855 | `A (inducedSetting preRetained 0 1) ∧ preRetained.wit = []` | VERIFIED_FINITE (via `assert_transport` + `decide`) | p,Q | S |
| `retention_completes` | 864 | `step preRetained (admitWit 0 1)` has `wit = [(0,1)]` | VERIFIED_FINITE | p,Q | A |
| `witness_no_protection` | 870 | `admitWit` never changes `prot` | FROZEN | p,Q | S |
| `no_protection_no_obstruction` | 878 | a retained, collapsed, unprotected pair is not obstructed (concrete) | VERIFIED_FINITE | p,Q | S |
| `quotient_no_recovery` | 897 | `q a = q b ⇒ (g (q a) (q b) ↔ g (q a) (q a))` for every `g` | FROZEN (trivial by rewriting; see §11) | none | A |
| `sepCol_irrefl` | 907 | `sepCol c i i = false` | FROZEN | p,Q | A |
| `sepCol_symm` | 912 | `sepCol c i j = sepCol c j i` | FROZEN | p,Q | A |
| `sepCol_trans` | 917 | non-separation by one column is transitive | FROZEN | p,Q | A |
| `zero_refl` | 925 | `zeroP cols i i = true` for every column list | FROZEN | p,Q | S |
| `zero_symm` | 934 | `zeroP cols i j = zeroP cols j i` | FROZEN | p,Q | S |
| `zero_trans` | 944 | `zeroP` transitive | FROZEN | p,Q | S |
| `menu_complete` | 982 | `obs = some cols`, `v ∈ cols`, `p < occ.length` ⇒ `(v,p) ∈ responseMenu` | CONDITIONAL:`s.obs = some cols` | p,Q | S |
| `extension_always_available` | 1006 | `obstP = true`, `i ≠ j`, `i < occ.length`, `(i,j) ∈ prot` ⇒ `[i] ∈ extensionProposals s i j` | CONDITIONAL:`obstP`, `i ≠ j`, in-bounds, protected (`hprot` is derivable from `hobst`; probe) | p,Q | S |
| `two_rule` | 1082 | same hypotheses ⇒ repair family nonempty ∨ (empty ∧ extension proposals nonempty) | CONDITIONAL: as above | p,Q | S |
| `proposal_not_execution` | 1098 | `licensed = false`, live ⇒ `addCol` inert | CONDITIONAL:`licensed = false`, `halted = false` | p,Q | S |
| `budget_gates_execution` | 1112 | `budget = 0`, live ⇒ `addCol` inert | CONDITIONAL:`budget = 0`, `halted = false` | p,Q | S |
| `refusal_object_inert` | 1130 | `refuse` leaves `occ`, `wit`, `prot`, `obs`, `budget` unchanged | FROZEN | p,Q | S |
| `refusal_not_terminal` | 1141 | `refuse` leaves `halted` unchanged | FROZEN | p,Q | A |
| `step_halted` | 1148 | `halted = true ⇒ step t e = t` | CONDITIONAL:`halted = true` | p,Q | A |
| `terminal_absorbing` | 1156 | `step (step s halt) e = step s halt` | FROZEN | p,Q | S |
| `no_outside_operational` | 1166 | `s = t ⇒ step s e = step t e` | FROZEN (trivial congruence; see §11) | p,Q | A |
| `replay_deterministic` | 1171 | `h1 = h2 ⇒ replayP h1 genesisP = replayP h2 genesisP` | FROZEN (trivial congruence; see §11) | p,Q | A |
| `replay_append` | 1175 | `replayP (h1 ++ h2) s = replayP h2 (replayP h1 s)` | FROZEN | p,Q | S |
| `extension_resolves` | 1185 | declared, `colOk c`, `sepCol c i j`, licensed, budget > 0, live ⇒ after `addCol c`, `obstP = false` | CONDITIONAL: six named hypotheses | p,Q | S |
| `nextFamilyP_stop` | 1236 | no protected pair obstructed ⇒ `nextFamilyP s = []` | CONDITIONAL:`∀ r ∈ prot, obstP = false` | p,Q | S |
| `nextFamilyP_nonempty` | 1255 | at an in-bounds protected obstruction the funded block for `[i]` is in the family | CONDITIONAL: as `two_rule` | p,Q | S |
| `nextFamilyP_complete_repair` | 1273 | every member of `repairFamily` at an obstructed protected pair appears as a block | CONDITIONAL:`obstP`, protected, `m ∈ repairFamily` | p,Q | S |
| `nextFamilyP_complete_ext` | 1286 | every extension proposal appears as a funded block | CONDITIONAL:`obstP`, protected, `c ∈ extensionProposals` | p,Q | S |

(`p,Q` = propext, Quot.sound.)

## 4. External and admitted assumptions

- Structures/policies: `PState` and `PEvent` are the declared machine; `step`, `refineOk`, `colOk`, `responseMenu`, `extensionProposals`, `nextFamilyP` are declared policies (the header and the ledger say so; the singleton-column extension universe and `setBudget 1` self-funding are explicitly declared). The `none ⇒ false` branch of `obstP` and the `none ⇒ true` convention of `zeroDeclP` are declared, named, and priced against rivals.
- Recurring hypotheses: `halted = false` (inertness theorems), `obs = some cols` / `obs = none`, the four-part obstruction package (`obstP`, `i ≠ j`, in-bounds, protected) for the two-rule family.
- Library lemmas doing real work: `List.foldl_append` (`replay_append`), `List.mem_flatMap`/`mem_map`/`mem_filter`/`mem_range`/`any_eq_true`, `decide` on concrete `PState` values (needs `DecidableEq` deriving), `Bool.and_eq_true`, `simp_all` in `sepCol_trans`. Many proofs use `propext`/`Quot.sound` only through `simp`.
- Universe/Type parameters: `quotient_no_recovery {X Q : Type}`. Functions treated as data: none (all stores are finite `List`s; positions are `Nat` indices into `occ`).
- Unearned identity: none found. Unrestricted external universe: `inducedSetting` sets `X := Nat` — the carrier of the induced `Setting` is all of `Nat`, not the finite occurrence list; irreflexivity over `Nat` holds because the asserted store is off-diagonal, but the Setting's carrier is a metatheoretic stand-in, and endpoints are in-bounds only because `wfPair` guards assertion (see §11). Unbounded function treated as internally available: none found. Silently assumed observer: none — observation is an explicit `Option` field with an explicit event, and the pre-observational state is `none`. Unspecified correspondence between presentations: none found. Cost function without justification: `budget : Nat` is a declared counter, decremented by execution; no cost model is claimed. Admitted condition later described as forced: the module and ledger explicitly refuse to call the `none ⇒ false` branch forced (CL-PD2-PACKET-05P withdrew a prior "not a convention" claim). Finite computation presented as universal: `obst_conditions_independent` is a table and is labelled as such; the quantified independence is in the four `gate_*_independent` theorems, which are genuine `¬ ∀` refutations. None found beyond that.

## 5. Derived consequences

- Imported by 12 modules. Heaviest downstream uses: `preRetained` (7), `zeroP` (6), `kernel_enters_preretained` (4), `obst_requires_observation` (3) — in `ContactBridge` (`declared_zero_as_view`, `observation_stage_realizes_observer`, `kernelStage`, `kernel_stage_no_obstruction`), `ContactKernel` (`kernel_licenses_entry`, `entry_pre_observation`, `passage_gateway_unique`), `HigherStructure` (the growth driver `graphAt_spec`, `round_two_rule`), `Attachment`, `ControllerCategory`, `DiffAnchor`, `GraphGenesis`, `RenamingStructure`, `StableContent`, `TraceAlgebra`, `TransitionAlphabet`.
- `zero_refl/symm/trans` are the native proof of the three laws that the arriving observer admits as fields (scope note in `paper/native_derivation_map.md`).
- Paper: `CL-PD2-PASSAGE`, `CL-PD2-PACKET-05R`, `CL-PD2-PACKET-05P` (ledger), `paper/primitive_difference_passage.md` (arrow table and P1–P8), `paper/observer_inventory.md`, `paper/primitive_difference_map.md`.

## 6. Counterexamples and limitations

- Countermodels: the four `gate_*_independent` theorems (witnesses `gateWitnessNoZero` etc.), `obst_policies_differ` (the two pre-observational policies disagree at `preRetainedObstructed`), `no_protection_no_obstruction`, `assertion_not_retained`/`retention_not_free` (assertion and retention are separate), `obs_gates_not_both_false` (refutes joint freedom of the four gates).
- Not proved: that the `none ⇒ false` policy is forced (explicitly disclaimed); a characterization of all states where the two policies differ (OPEN by declaration); that the machine's iteration terminates or that the driver's closure is anything but metatheoretic (stated); that the extension universe (singleton columns) is the only or a canonical one (declared); the "absolute" no-outside principle (declared not formulable). Arrow 5 of the passage table ("observer zero → guarded collapse", status THEOREM) has no named theorem — it is the definition of `obstP`.
- `two_rule`'s first disjunct is bare non-emptiness of `repairFamily`; which repair is chosen is not addressed. `extension_always_available` needs `i ≠ j` and `i < occ.length` as separate hypotheses because `obstP` on an arbitrary (non-replayed) state does not supply them.

## 7. Axiom dependencies

All 56 artifact reports and the two probed helpers ⊆ {propext, Quot.sound}. None exceed the budget.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). 56 of 58 theorems are in the axiom artifact; the two `*_step` helpers are not. The ledger cites 24 of them by name (CL-PD2-PASSAGE) plus the gate package (CL-PD2-PACKET-05R/05P). Probe run: `lake env lean probes/D/passage_probe.lean` (exit 0) — `#print axioms` of the two helpers; `(inducedSetting preRetained 0 1).X = Nat` by `rfl`; `no_outside_operational` and `replay_deterministic` re-proved as `congrArg`; `quotient_no_recovery` re-proved by `rw`; `(i,j) ∈ s.prot` derived from `obstP s i j = true`.

## 9. Related Python implementations

`code/derivation/primitive_passage.py` (`PS`, `sep_col`, `sep_p`, `zero_p`, `obst_p`, `wf_pair`, `refine_ok`, `col_ok`, `pstep`, `preplay`, `response_menu`, `repair_family_p`, `extension_proposals`, `obstructed_pairs`, `next_family_p`, `growth_report`, `arrow_report`); tests `tests/test_primitive_passage.py` (`test_observation_semantics`, `test_obstruction_four_conditions`, `test_step_guards_and_dedup`, `test_refusal_certificate_and_record`, `test_terminal_absorbing`, `test_gates_and_resolution`, `test_two_rule_and_next_family`, `test_reports_and_replay_determinism`). Artifact `primitive_passage.json`.

## 10. Textbook placement proposal

- Prerequisites: `PrimitiveCore.Setting` and candidate A; the idea of a replayable event history (`foldl`); the distinction between an asserted fact, a retained fact and a demand; what an observation column is.
- Substantive: `PState`/`PEvent`/`step`; `zeroP` with `zero_refl/symm/trans` (the native equivalence laws); `obstP` with `obstP_factors` **cited together with** the four `gate_*_independent` theorems and `obs_gates_not_both_false`; `obst_requires_observation` as a declared policy with `obstEmptyObs`/`obst_policies_differ`; `assertion_not_retained`, `retention_requires_assertion`, `retention_persists`, `asserted_offdiag`, `assert_transport`, `kernel_enters_preretained`; `witness_no_protection`/`no_protection_no_obstruction`; `menu_complete`, `extension_always_available`, `two_rule`; `proposal_not_execution`, `budget_gates_execution`; `refusal_object_inert` vs `terminal_absorbing`; `replay_append`; `extension_resolves`; the `nextFamilyP_*` quartet.
- Auxiliary: `zeroP_cons`, `sepCol_*`, `obstP_strict_factors`, `obst_of_gates`/`gates_of_obst`, `obstP_reads_three_stores`, `undeclared_gates`, `strict_gate_entails_declared`, `wit_independent_of_obs`, `obst_agrees_when_declared`, `obst_diverges_when_undeclared`, `retention_not_free`, `*_step` helpers, `retention_completes`, `step_halted`, `refusal_not_terminal`, `no_outside_operational`, `replay_deterministic`, `quotient_no_recovery`.
- Lesson title: "From an asserted difference to a response". Question answered: at what point in a replayed history a protected, retained difference becomes an obstruction, and what the machine is then forced to offer.
- Omit: `obst_diverges_when_undeclared` (retained only as a historical witness, per the ledger); `no_outside_operational` and `replay_deterministic` as separate results (they are congruences; teach determinism as "`step` is a function").

## 11. Interpretation findings

1. **P8 / arrow 10 — `no_outside_operational`, `replay_deterministic` (INTERPRETATION DEFECT, minor).** Paper (`primitive_difference_passage.md`, arrow 10, status THEOREM): "`replay_deterministic`, `replay_append`: state is a function of represented history"; P8: "operational no-outside: `no_outside_operational`, `replay_deterministic`". Lean: `(h : s = t) : step s e = step t e` and `(heq : h1 = h2) : replayP h1 genesisP = replayP h2 genesisP` — both are `congrArg` (probe). They are true but carry no content beyond `step`/`replayP` being Lean functions; the docstring's "the step is a function of represented data alone" is a statement about the definition, not a theorem outcome. `replay_append` is the only non-trivial member of arrow 10. The module itself flags that the absolute form is not claimed.
2. **P3 — `quotient_no_recovery` (INTERPRETATION DEFECT, minor).** Paper: "once a presentation identifies the endpoints, no function of the quotient alone separates their images; recovery data must be retained outside the quotient. That is what retention is *for*." Lean: for `q a = q b` and any `g`, `g (q a) (q b) ↔ g (q a) (q a)` — a one-line rewrite with no hypothesis about presentations, faithfulness or retention. The "barrier" reading and the "that is what retention is for" conclusion are commentary; nothing in the theorem mentions `wit`.
3. **Arrow 5 of the passage table (INTERPRETATION DEFECT, minor).** `primitive_difference_passage.md` row 5: "observer zero → guarded collapse | THEOREM (conditional on protection) | zero on a protected retained pair is exactly the collapse in force". No theorem is named; this is the definition of `obstP`. Should read DEFINITION.
4. **`inducedSetting` carrier (finitude flag).** `assert_transport` and `kernel_enters_preretained` realize candidate A on a `Setting` with `X := Nat` and `r x y := (x, y) ∈ s.asserted`. The occurrence set is the finite list `s.occ`; `Nat` is a metatheoretic container. The claim "the two-element kernel enters the passage" is accurate about the relation (one asserted pair, off-diagonal) but the Setting is not two-element; `D`/`a ≠ b` hold, and irreflexivity holds over all of `Nat` vacuously off the asserted store. Not a defect in the Lean; a reader should not take `inducedSetting` as a finite-carrier object.
5. **`obstP_factors` (correctly scoped).** The module, the ledger (CL-PD2-PACKET-05R) and the docstring all say it is near-definitional and must be cited with the independence theorems. Recorded here as checked and consistent; the earlier overclaim is documented as withdrawn in the ledger.
6. **`obst_diverges_when_undeclared` (already flagged by the module).** First conjunct is a closed truth about written-out lists, not about the state. The ledger says it is "not evidence of divergence". Consistent.
7. **Finitude flags.** `PState.occ : List Nat` with `Nat` positions, `obs : Option (List (List Nat))`: all system content is finite lists; the `Nat` index type is metatheoretic. `zero_refl/symm/trans` quantify over every `cols : List (List Nat)` — a metatheoretic ∀ over finite data, not an observer the system possesses. `nextFamilyP` iteration is explicitly left metatheoretic.
8. **Vacuity check.** `extension_always_available`/`two_rule`/`nextFamilyP_nonempty` hypotheses are jointly satisfiable (`gateWitnessAll` with occurrences `[0,1]`: `obstP = true`, `0 ≠ 1`, `0 < 2`, `(0,1) ∈ prot`). `extension_resolves` hypotheses are satisfiable (same state with `budget := 9`, `c := [0]`). `nextFamilyP_stop` hypothesis holds at `genesisP`. None found vacuous; the three trivial theorems above are true, not vacuous.
