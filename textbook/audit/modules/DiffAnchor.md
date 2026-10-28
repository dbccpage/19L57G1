# Audit: DiffAnchor

| field | value |
|---|---|
| Path | lean4/Derivation/DiffAnchor.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 3241f3e98da28403 |
| Lines | 73 |
| Imported by root `Derivation.lean` | no (parked in `ParkedAudit.lean`, imported at its line 6 and listed in `parkedModules` at line 142; its import-collision probe `DiffAnchorCompat` is parked beside it, line 7 / line 143) |
| Imports | Derivation.ContactBridge, Derivation.ObsDescent (both root-imported) |
| Declarations | 1 def (`colObs`), 3 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 3 lines (`ParkedAudit.lean:265:0`, lines 1490–1492 of the artifact); axioms seen: `propext, Quot.sound` for all three |
| Forbidden tokens (sorry/admit/axiom) | none found (the word "axioms" occurs only in the docstring sentence "axioms within `{propext, Quot.sound}`", not at line start as a declaration) |

## 1. Mathematical purpose

The module supplies the *descent* side of the typed native-difference anchor over a declared observation. The anchor itself is owned by `ContactBridge`: `colView cols` is the per-column membership signature of an occurrence, and `declared_zero_as_view` shows the passage's Boolean zero relation `zeroP cols` is exactly the zero relation of the kernel observer at that view. `DiffAnchor` names that observer (`colObs cols := kernelObs (colView cols)`), re-exports the fidelity as an `↔` with `ZeroRel`, lifts it to an exact identification of quotient points (`ObsQuotient.mk (colObs cols) i = … j ↔ zeroP cols i j = true`), and proves the one new fact: the difference map of `colObs` is constant on zero-classes in both arguments (`DeltaConstant`), so it descends to the observer quotient via `ObsDescent.deltaDescend`. Everything is conditional on a *declared* list of observation columns `cols`; nothing says the columns are forced. The module is parked: not in the root's import closure, audited through `ParkedAudit.lean`.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `colObs cols` | 44 | def | `kernelObs (ContactBridge.colView cols) : DiffObs Nat (List Bool × List Bool)` — a named handle for the observer `observation_stage_realizes_observer` exhibits existentially. | ADMITTED (a name for an existing witness; `cols : List (List Nat)` is declared data) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `colObs_zeroRel_iff_zeroP` | 48 | For all `cols i j`: `ZeroRel (colObs cols) i j ↔ PrimitivePassage.zeroP cols i j = true` (symmetric re-export of `ContactBridge.declared_zero_as_view`). | FROZEN (over all declared `cols`) | propext, Quot.sound | A (re-export) |
| `colObs_quotient_eq_iff_zeroP` | 56 | `ObsQuotient.mk (colObs cols) i = ObsQuotient.mk (colObs cols) j ↔ zeroP cols i j = true` (rewrites with `obsQuotient_mk_eq_iff`). | FROZEN | propext, Quot.sound | S |
| `colObs_deltaConstant` | 64 | `DeltaConstant (colObs cols)`: `ZeroRel x x' → ZeroRel y y' → delta x y = delta x' y'` (the delta is the pair of views). | FROZEN | propext, Quot.sound | S |

## 4. External and admitted assumptions

- From ContactBridge: `colView`, `declared_zero_as_view`; from ObsDescent: `ObsQuotient.mk`, `obsQuotient_mk_eq_iff`, `DeltaConstant`, `deltaDescend` (the last mentioned only in prose); from DiffInterface: `DiffObs`, `kernelObs`, `ZeroRel`; from PrimitivePassage: `zeroP` (`!sepP`, i.e. "no declared column separates").
- **What it anchors, exactly:** the typed difference interface (`DiffObs`) to the passage's declared observation stage. `cols : List (List Nat)` is the declared observation; the docstring (line 28–29) says "`cols` is DECLARED … conditional on a declared observation, not a claim it is forced". The three theorems are universally quantified over every `cols`, so they are FROZEN as Lean statements, but their subject (which columns) is admitted data.
- `colObs cols` is a kernel observer, so `DeltaConstant` is automatic for *every* kernel observer (`delta x y = (view x, view y)`, and `ZeroRel` is view equality); the proof is two rewrites. The "genuinely new content" claim of the docstring (line 24) is new relative to `ContactBridge`, not deep: the same two-line proof works for any `kernelObs view`.
- Finitude rule: `Nat → …` functions (`colView cols : Nat → List Bool`) are ambient; `cols` is a finite list so each view is finitely determined, but the quantification over `i j : Nat` is metatheoretic. The docstrings do not read this as a system capacity.
- Unearned identity / unrestricted universe / unbounded internal function / silently assumed observer (the observer is explicitly named) / unspecified correspondence / cost function / admitted-then-forced ("not a claim it is forced" is stated) / finite-as-universal: none found for each.
- Library lemmas doing real work: `rw` with `obsQuotient_mk_eq_iff` (a `Quotient.exact`/`sound` pair, hence `Quot.sound`); the `propext` comes through `declared_zero_as_view`'s `decide` and `and_congr`.

## 5. Derived consequences

- Nothing imports `DiffAnchor` except `DiffAnchorCompat` (a declaration-free import-collision probe that imports both `Derivation` and `DiffAnchor`) and `ParkedAudit.lean` (which emits the three `#print axioms` lines). No other `lean4/Derivation/*.lean` references `colObs` or `DiffAnchor` (grep: none).
- Paper: not cited in `paper/paper.md`, `paper/paper_claim_ledger.md`, `paper/paper_change_log.md` or any `paper/*.md` (grep for `DiffAnchor`, `colObs`, `BR-0`, "diff anchor": no hits). The only references are `docs/claude_md_history.md` ~line 740 (why the compat shims force a second `defaultTargets` root) and `docs/index/pins.md` lines 318–319 (four research trees pin the file: `coherent_process_limits`, `endogenous_demand`, `represented_execution`, `setting_translation`).
- `code/derivation/completion.py` line 51 lists `"DiffAnchor": ["DiffAnchor.lean"]` in a module map; no theorem-level bindings for it were found (grep `DiffAnchor\.` in completion.py: none beyond the module map).

## 6. Counterexamples and limitations

- No countermodel in this module. The contrasting countermodel lives in `ObsDescent` (`collapseAllObs_not_deltaConstant`: a two-point all-zero observer whose delta does *not* descend), which is what makes `colObs_deltaConstant` a non-trivial property to state, even though for kernel observers it holds by construction.
- The docstring's label "BR-0" is not defined anywhere in `paper/` (grep: none); it appears to be an internal bridge-task label from the period when the module was written. Not resolvable from the available history: `git log -- lean4/Derivation/DiffAnchor.lean` shows a single snapshot commit (`ca30e30`, 2026-09-20), so the "earlier version of this module [that] duplicated them" mentioned at line 13 is not recoverable here.
- Status: parked, meaning (per `ParkedAudit.lean`) outside the root import closure, elaborated by the `lean-census` step and axiom-audited by the second default target. The docstring's "verified by hand, not by the root gate" (line 34) predates the ParkedAudit mechanism, which now does report the three theorems in the artifact.

## 7. Axiom dependencies

All three theorems: `[propext, Quot.sound]`. None exceeds.

## 8. Verification status

- Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0; parked modules are built via `ParkedAudit.lean`, the second default target).
- Its theorems appear in `artifacts/lean_axioms.txt` at `ParkedAudit.lean:265:0` (artifact lines 1490–1492). The paper does not cite them.
- Probe: `textbook/audit/probes/F2/fid_probe.lean`, exit 0: `#print axioms DiffAnchor.colObs_deltaConstant` → `[propext, Quot.sound]`; `#eval PrimitivePassage.zeroP [] 0 1 = true` (with no declared columns everything is zero-related, so `colObs []` collapses all of `Nat` to one class), `zeroP [[0]] 0 1 = false`, `zeroP [[0,1]] 0 1 = true` — confirming the declared-observation dependence.

## 9. Related Python implementations

- `code/derivation/completion.py:51` lists the module in a file map only. The Python passage/observation code (`code/derivation/observe.py`: contexts, profiles, separability) implements the kernel's own observation notion, not `zeroP`/`colView` over declared columns; no Python function named for `colObs`, `DeltaConstant` or `zeroP` was found (grep `colObs|DeltaConstant|delta_constant|zeroP` in `code/`, `tests/`: none).

## 10. Textbook placement proposal

- Prerequisites: `DiffObs`, `kernelObs`, `ZeroRel` (DiffInterface); `ObsQuotient`, `obsQuotient_mk_eq_iff`, `DeltaConstant`, `deltaDescend` and the `collapseAllObs` countermodel (ObsDescent); `colView`, `declared_zero_as_view` (ContactBridge); `zeroP` (PrimitivePassage).
- Substantive: `colObs_quotient_eq_iff_zeroP` (the exact quotient identification) and `colObs_deltaConstant` (the descent of the difference map), taught in one breath with the remark that both are properties of *any* kernel observer and the declared-column observer is one.
- Auxiliary: `colObs` (a name), `colObs_zeroRel_iff_zeroP` (re-export).
- Suggested lesson: "Does the declared observation's difference map survive passage to the quotient?" — answering: yes, because it is a pair of views and the quotient identifies exactly equal views; and this depends on which columns were declared.
- Recommend omitting from the textbook: the module as a separate unit. Its content is a three-line corollary of ContactBridge + ObsDescent; it is parked, uncited by the paper, and labelled with an undefined task code ("BR-0"). Fold the two substantive facts into the ObsDescent/ContactBridge lesson and note that `DiffAnchor` exists as the named handle.

## 11. Interpretation findings

1. **Docstring line 24: "`colObs_deltaConstant` — the genuinely new content".** Lean: the proof is `rw [hx', hy']` on `(view x, view y)`; `DeltaConstant` holds for every `kernelObs view` by the same argument. "New" is true only relative to what `ContactBridge` states; it is not a new mathematical fact. INTERPRETATION DEFECT (minor overstatement in the docstring; no prose outside the module repeats it).
2. **Docstring line 33–34: "Parked module (not imported by `Derivation.lean`); axioms … verified by hand, not by the root gate."** Current state: the parked audit (`ParkedAudit.lean`, second default target) does report the three theorems into `artifacts/lean_axioms.txt`, and `ci/check_parked_audit.py` requires the module to be listed. The sentence is stale, not wrong at the time of writing. INTERPRETATION DEFECT (stale status note).
3. Vacuity: none of the three theorems is vacuous; `cols := []` gives the total collapse (one class), `cols := [[0]]` separates `0` from `1`. Checked by `#eval` (probe).
