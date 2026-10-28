# Audit: StableContent

| field | value |
|---|---|
| Path | lean4/Derivation/StableContent.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | ab6ab867cbed308b |
| Lines | 582 (`wc -l`; inventory.json counts 583) |
| Imported by root `Derivation.lean` | yes (line 40; `#print axioms` inventory present, lines 853 ff.) |
| Imports | `Derivation.PrimitivePassage` |
| Declarations | 11 def (`protSep`, `SepHere`, `TraceStableSep`, `IsTraceExcludedEvent`, `RestrictedTrace`, `RestrictedStableSep`, `sHalt`, `sUnfunded`, `sUnprot`, `openExactStabilityCharacterization`, `quiescentP`), 18 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 18 lines (every theorem); axioms seen: `propext, Quot.sound` only |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

On the passage dynamics (`PrimitivePassage.PState`/`step`/`replayP`, not the regime model of `Basic.lean`) the module asks when a separation of two occurrence positions by the declared observation is *stable*: still present after every replay of the event grammar. It defines that predicate (`TraceStableSep`), a weaker one over a syntactic fragment that omits occurrence admission, budget and license writes (`RestrictedStableSep`), and *protected separation* (`protSep`: the pair is in the protected store and the declared columns separate it). It proves the true direction: protected separation is trace stable, because protection is never lost, new columns only add separators, and an accepted refinement is guarded by exactly the monotone preservation of protected separations. It then refutes the converse with a halted state carrying an unprotected separation (every replay is inert there), gives a live-but-unfunded state where an unprotected separation is stable for the restricted fragment only, and proves that a funded accepted refinement routed through the one separating column destroys an unprotected separation in one step. The exact characterization on live funded states is recorded as an unproved proposition. Separately it proves that on a declared state quiescence (no actively obstructed pair) holds exactly when every retained protected pair is separated, and draws the corollary that such pairs are trace stable. The module header records that an earlier claim "stable content is exactly protected separation" was withdrawn as an overclaim.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `protSep` | 63 | def (Bool) | `(i,j) ∈ prot` and the declared columns separate `(i,j)`; `false` pre-observationally | ADMITTED |
| `SepHere` | 70 | def (Prop) | `∃ cols, s.obs = some cols ∧ sepP cols i j = true` | ADMITTED |
| `TraceStableSep` | 76 | def (Prop) | `∀ h : List PEvent, SepHere (replayP h s) i j` | ADMITTED (metatheoretic universal over all event lists) |
| `IsTraceExcludedEvent` | 83 | def (Bool) | `admitOcc`, `setBudget`, `setLicense` | ADMITTED (declared syntactic fragment, "no ownership claim") |
| `RestrictedTrace` | 91 | def (Prop) | no excluded event in the list | ADMITTED |
| `RestrictedStableSep` | 97 | def (Prop) | `SepHere` after every restricted replay | ADMITTED |
| `sHalt` | 273 | def | halted state, `obs = some [[0]]`, `prot = []`, `occ = [0,1]` | ADMITTED (countermodel state) |
| `sUnfunded` | 410 | def | same but live, `budget = 0` | ADMITTED (countermodel state) |
| `sUnprot` | 465 | def | `occ = [0,1,2]`, `(1,2)` retained+protected, `obs = some [[0]]`, `budget = 1` | ADMITTED (witness state) |
| `openExactStabilityCharacterization` | 495 | def (Prop) | live ∧ funded ∧ `SepHere` ∧ `TraceStableSep` → `protSep = true` | ADMITTED (named OPEN proposition; never proved) |
| `quiescentP` | 502 | def (Prop) | `∀ i j, obstP s i j = false` | ADMITTED (universal over all `Nat` pairs; `obstP` is false off `wit` so the content is finite) |

## 3. Theorems and lemmas

Abbreviations: **Dec** = `s.obs = some cols`; **Prot** = `(i,j) ∈ s.prot`; **Sep** = `sepP cols i j = true`.

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `sepP_append` | 103 | a separating column list still separates after appending a column | CONDITIONAL:Sep | propext, Quot.sound | A |
| `sepP_refine` | 112 | under Dec, `refineOk s v p`, Prot, Sep: the refined columns still separate `(i,j)` | CONDITIONAL:Dec, `refineOk`, Prot, Sep | propext, Quot.sound | S |
| `prot_mono` | 130 | a protected pair stays protected after every event | CONDITIONAL:Prot | propext, Quot.sound | S |
| `sep_preserved` | 138 | under Dec, Prot, Sep: after any event there are declared columns separating `(i,j)` | CONDITIONAL:Dec, Prot, Sep | propext, Quot.sound | S |
| `protSep_persists` | 245 | `protSep s i j = true → protSep (step s e) i j = true` | CONDITIONAL:`protSep` | propext, Quot.sound | S |
| `protSep_replays` | 264 | the same along every replay | CONDITIONAL:`protSep` | propext, Quot.sound | S |
| `protSep_trace_stable` | 281 | `protSep s i j = true → TraceStableSep s i j` (sufficiency) | CONDITIONAL:`protSep` | propext, Quot.sound | S |
| `trace_stable_restricted_stable` | 300 | `TraceStableSep → RestrictedStableSep` | CONDITIONAL:`TraceStableSep` | propext, Quot.sound | A |
| `replay_halted` | 308 | on a halted state every replay is inert | CONDITIONAL:`s.halted = true` | propext, Quot.sound | A |
| `halted_stable_not_protected` | 283 | `TraceStableSep sHalt 0 1 ∧ protSep sHalt 0 1 = false` | REFUTED (converse of sufficiency, over all `PState`) | propext, Quot.sound | S |
| `restricted_step_inert_unfunded` | 299 | for a non-excluded event, Dec and `budget = 0`: the step keeps `obs = some cols` and `budget = 0` | CONDITIONAL:`IsTraceExcludedEvent e = false`, Dec, `budget = 0` | propext, Quot.sound | S |
| `restricted_replay_inert_unfunded` | 390 | the same along every `RestrictedTrace` | CONDITIONAL:`RestrictedTrace`, Dec, `budget = 0` | propext, Quot.sound | S |
| `unfunded_restricted_stable_not_protected` | 422 | `RestrictedStableSep sUnfunded 0 1`, `protSep = false`, live | VERIFIED_FINITE + CONDITIONAL theorem instance (restricted-fragment example; not a countermodel to the full converse, as the source says) | propext, Quot.sound | S |
| `separation_breakable` | 438 | live, Dec, `refineOk s v p`, `0 < budget`, and the refined columns do not separate `(i,j)` ⇒ `¬ SepHere (step s (refineCol v p)) i j` | CONDITIONAL:the five named witness hypotheses | propext, Quot.sound | S |
| `unprotected_separation_unstable` | 470 | at `sUnprot`: `(0,1)` separated before, refinement `refineCol [0] 1` gives `[[1,0]]`, `(0,1)` no longer separated, `(1,2)` protected and now separated, `protSep sUnprot 0 1 = false` | VERIFIED_FINITE (`decide`) | propext, Quot.sound | S |
| `quiescent_iff_protected_separated` | 507 | under Dec: `quiescentP s ↔ ∀ pr ∈ prot, pr ∈ wit → sepP cols pr.1 pr.2` | CONDITIONAL:Dec | propext, Quot.sound | S |
| `quiescence_is_protected_separation` | 541 | under Dec: `quiescentP s ↔ ∀ pr ∈ prot, pr ∈ wit → protSep s pr.1 pr.2` | CONDITIONAL:Dec | propext, Quot.sound | S |
| `quiescent_retained_protected_trace_stable` | 565 | under Dec and `quiescentP s`: every retained protected pair is trace stable | CONDITIONAL:Dec, `quiescentP` | propext, Quot.sound | S |

## 4. External and admitted assumptions

- **Base model.** `PState`, `step`, `replayP`, `sepP`, `refineOk`, `colOk`, `obstP`, `step_halted`, `obst_agrees_when_declared` from `PrimitivePassage` (whose station names were an externally imposed challenge; this module adds no state).
- **Declared.** The restricted fragment `IsTraceExcludedEvent` (explicitly "a syntactic classification only … generated repair blocks may contain `setBudget`", repaired after `TransitionAlphabet.internal_family_emits_budget_write`); the OPEN proposition; the three witness states.
- **Recurring hypotheses.** A declared observation `s.obs = some cols` (pre-observational states have no separation to stabilize, as the header says); `(i,j) ∈ s.prot`; `sepP cols i j = true`.
- **Library lemmas doing real work.** `List.any_append`, `List.all_eq_true`, `List.mem_append`, `Option.some.inj`, `omega` (budget), `decide`; `repeat' split` over the `step` `if`/`match` tree.
- **Finitude rule.** `TraceStableSep` quantifies over all `h : List PEvent` ("after EVERY replay") and `quiescentP` over all `i j : Nat`; both are metatheoretic universals, read in the docstrings as "every replay of the declared grammar" and "no pair is actively obstructed" — the second is finite in content because `obstP` requires membership in `wit`. No docstring treats a totality of traces as something the system holds. `openExactStabilityCharacterization` is a `Prop` over all `PState`, not a theorem.
- Unearned identity: none found. Unrestricted external universe: none. Unbounded function treated as internally available: none. Silently assumed observer: none — every stability statement names `s.obs = some cols`. Unspecified correspondence between presentations: none claimed. Cost function without justification: none. Admitted condition later described as forced: none found. Finite computation presented as universal: none found in Lean; the Python battery (carrier 3, depth 2, breadth 24) is reported as computation in the ledger.

## 5. Derived consequences

- No other Lean module imports `StableContent` (grep of `lean4/`; the dependency graph lists no consumers). The root prints axioms for all 18 theorems.
- Ledger CL-PD2-TRACE-STABILITY (which supersedes the withdrawn CL-PD2-STABLE-CONTENT) cites 17 theorems plus the OPEN proposition; `paper/primitive_difference_map.md` (line 311 ff.) summarizes the same; `paper/paper_change_log.md` records the withdrawal ("Audit repair gate", 2026-08-13), the renaming `stableSep → protSep`, the narrowing of (iii) on 2026-08-18, and the note that "the prose of `StableContent.lean` was not re-checked against the narrowed (iii)".
- Internally: `prot_mono` + `sep_preserved` ⇒ `protSep_persists` ⇒ `protSep_replays` ⇒ `protSep_trace_stable` ⇒ `quiescent_retained_protected_trace_stable`.

## 6. Counterexamples and limitations

| theorem | what it refutes | witness |
|---|---|---|
| `halted_stable_not_protected` | "trace stability implies protected separation" (over all `PState`) | `sHalt`: halted, `obs = some [[0]]`, `prot = []`, pair `(0,1)` |
| `unfunded_restricted_stable_not_protected` | "restricted stability implies protected separation" | `sUnfunded`: live, `budget = 0`, same observation |
| `unprotected_separation_unstable` | "an unprotected separation persists" | `sUnprot`, `refineCol [0] 1` |

Limitations:
- **The chosen converse witnesses are not genesis-reachable.** Both `sHalt` and `sUnfunded` have `prot = []` with a nonempty column `[0]`. Column creation (`colOk`) and refinement (`refineOk`) each require some protected obstructed pair, and `prot` is append-only (`prot_mono`), so no replay from `genesisP` reaches a state with a nonempty column and empty `prot` (reasoning from the guards; not checked in Lean). The refutation is of the converse over all `PState`, which is what the ledger states. A genesis-reachable halted witness does exist and was checked by probe (§8): after `admitOcc 0,1,2; assertWit 1 2; admitWit 1 2; protect 1 2; declareObs; setBudget 1; addCol [1]; halt`, the pair `(0,1)` is separated by `[1]`, unprotected, and trace stable by `replay_halted`. So the converse also fails on reachable states; the module simply did not use that witness.
- `separation_breakable` is one-directional: given the witness, the separation is destroyed. Nothing in the module proves that every destruction of an unprotected separation needs such a witness (see §11.1).
- `quiescent_iff_protected_separated` is a statement about `obstP` on a declared state; it is not a stability claim (the source says so).
- Not proved: `openExactStabilityCharacterization`; any reachability-restricted version of the converse; that restricted stability differs from full stability at any reachable state.

## 7. Axiom dependencies

All 18 artifact lines report exactly `propext, Quot.sound`. None exceed the boundary. Probe re-confirmed `halted_stable_not_protected` at `[propext, Quot.sound]`.

## 8. Verification status

- Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0).
- Axiom artifact: 18/18 present.
- Ledger CL-PD2-TRACE-STABILITY cites `protSep_trace_stable`, `protSep_persists`, `protSep_replays`, `trace_stable_restricted_stable`, `sep_preserved`, `prot_mono`, `sepP_refine`, `replay_halted`, `halted_stable_not_protected`, `restricted_step_inert_unfunded`, `restricted_replay_inert_unfunded`, `unfunded_restricted_stable_not_protected`, `separation_breakable`, `unprotected_separation_unstable`, `quiescent_iff_protected_separated`, `quiescence_is_protected_separation`, `quiescent_retained_protected_trace_stable`, and the OPEN `openExactStabilityCharacterization`. `sepP_append` is uncited (auxiliary).
- Probe (`textbook/audit/probes/F1/sc_reachable_witness.lean`, `lake env lean` inside `lean4/`): the two `example`s for the reachable halted witness (`(replayP hist genesisP).obs = some [[1]]`, `prot = [(1,2)]`, `halted = true`, `protSep … 0 1 = false`, `sepP [[1]] 0 1 = true` by `decide`; `TraceStableSep` via `replay_halted`) elaborated without error; `#eval sHalt.prot` printed `[]`, `#eval sHalt.obs` printed `some [[0]]`; `#print axioms StableContent.halted_stable_not_protected` gave `[propext, Quot.sound]`. The file's two trailing `#print axioms` for other modules failed only because they were not imported (reported in the probe output as unknown constants); they are covered by the committed artifact.

## 9. Related Python implementations

- `code/derivation/stable_content.py`: `prot_sep`, `quiescent_p`, `event_battery`, `sample_states`, `is_trace_excluded_event`, `persistence_check`, `replay_persistence_check`, `halted_countermodel`, `unfunded_countermodel`, `unprotected_unstable`, `quiescence_check`, `stable_content_report` (section `stable_content` of `artifacts/primitive_passage.json`; bounds carrier 3, trace depth 2, breadth 24).
- `tests/test_stable_content.py`: `test_prot_sep_basics`, `test_sufficiency_single_step_and_traces`, `test_converse_is_false_absorbed`, `test_converse_is_false_unfunded`, `test_instability_needs_witness` (its docstring reads "with a funded accepted refinement … the unprotected separation dies" — the sufficiency direction), `test_report_records_the_open_gap`, `test_quiescence_battery`, `test_battery_covers_every_kind`, `test_runner_includes_repaired_section`.

## 10. Textbook placement proposal

- Prerequisites: `PrimitivePassage` (`PState`, `step`, `replayP`, `sepP`/`sepCol`, `obstP`, `refineOk`/`colOk`, `step_halted`, `obst_agrees_when_declared`); the difference between separation, protection and obstruction; what a replay is.
- Substantive: `protSep`, `TraceStableSep`, `sep_preserved` (the case analysis that is the whole mechanism), `protSep_trace_stable`, `halted_stable_not_protected`, `separation_breakable` + `unprotected_separation_unstable`, `openExactStabilityCharacterization` (taught as an open question), `quiescent_iff_protected_separated`.
- Auxiliary: `sepP_append`, `sepP_refine`, `prot_mono`, `protSep_persists`, `protSep_replays`, `trace_stable_restricted_stable`, `replay_halted`, `restricted_*_inert_unfunded`, `quiescence_is_protected_separation`, `quiescent_retained_protected_trace_stable`.
- Suggested lesson: **"What protection buys"** — the one question: *is a separation that the observer currently draws guaranteed to survive the dynamics, and what guarantees it?* (Answer: protection suffices; it is not necessary, as a halted state shows; a funded refinement through the separating column breaks an unprotected one; the exact boundary on live funded states is open.)
- Recommend omitting or demoting: the restricted fragment (`IsTraceExcludedEvent`, `RestrictedStableSep`, `sUnfunded`) to a remark — the source itself says it is "not a second countermodel to full trace stability" and the fragment is a syntactic choice with no ownership meaning; if kept, use a reachable witness (the probe's history, with the final `halt` dropped and the budget spent to 0 by `addCol [1]`) rather than `sUnfunded`.

## 11. Interpretation findings

1. **Module docstring item 4 (lines 29–33) and the docstring of `separation_breakable` (lines 432–436) vs the Lean** — docstring: "an unprotected separation is destroyed **only when** a concrete breaking witness exists" and "destroyed **exactly when** a concrete accepted refinement exists that routes through the separating column". The Lean: given live, Dec, `refineOk`, funding and a non-separating refined column, `¬ SepHere (step s (refineCol v p)) i j` — the *sufficiency* of the witness only. No theorem proves the necessity direction ("only when"); it is exactly the content of `openExactStabilityCharacterization`. The ledger (iii) was narrowed to sufficiency on 2026-08-18 and `paper/paper_change_log.md` records: "the prose of `StableContent.lean` was not re-checked against the narrowed (iii) of CL-PD2-TRACE-STABILITY". Classification: INTERPRETATION DEFECT (docstring overreads a correct theorem; known and dated in the change log; the ledger is already correct). Smallest illustration of the gap: `TraceStableSep` fails at `sUnprot` by this one witness, but the module gives no theorem of the form "¬ TraceStableSep → ∃ witness".
2. **Ledger (ii) "one full-trace countermodel"** — `halted_stable_not_protected` refutes the converse over all `PState`; its witness `sHalt` is not genesis-reachable (§6). The ledger does not claim reachability, and the module header says "no reachability restriction is built into the open proposition", so this is not an overclaim; recorded because a reader may assume the countermodel is a state the dynamics can produce. A reachable halted witness exists (probe §8). Classification: no defect; limitation recorded.
3. **Module header item 5 / `quiescent_iff_protected_separated` docstring** — "no pair is actively obstructed exactly when every retained protected pair is separated" — matches the Lean biconditional under `s.obs = some cols`. The docstring's "on a declared state" names the hypothesis. No defect.
4. **Words "exactly" / "OPEN"** — the only remaining "exactly" claims are the two quiescence biconditionals (checked) and the `separation_breakable` docstring (item 1). The OPEN item is a `def … : Prop` with no proof anywhere in `lean4/` (grep: the name occurs only at its definition and in the ledger/change log).
5. **Vacuity check.** `protSep s i j = true` forces `s.obs = some _`, so `protSep_trace_stable` is not vacuous and its hypotheses are satisfiable (`sUnprot` for `(1,2)` after refinement; `wObstructed`-style states in `TransitionAlphabet` with a separating column). `separation_breakable`'s five hypotheses are jointly satisfied by `sUnprot`, `cols = [[0]]`, `v = [0]`, `p = 1`, `(i,j) = (0,1)` (that is `unprotected_separation_unstable`). `quiescentP` holds at every pre-observational state trivially (`obstP` is `false` there), but the quiescence theorems assume `s.obs = some cols`, so they are not trivially true. No vacuous theorem found.
6. **Finitude.** `TraceStableSep` ("after EVERY replay") and `quiescentP` ("no pair") are metatheoretic universals; neither docstring nor ledger reads them as a totality the system possesses. No defect.
