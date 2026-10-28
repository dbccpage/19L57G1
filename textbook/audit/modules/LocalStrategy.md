# Audit: LocalStrategy

| field | value |
|---|---|
| Path | lean4/Derivation/LocalStrategy.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 5802900337ffc9b0 |
| Lines | 262 |
| Imported by root `Derivation.lean` | **no (neither)**: not in the root import list, not named in `lean4/ParkedAudit.lean`. It is imported only by `lean4/Derivation/G1Class.lean` line 1 (`import Derivation.LocalStrategy`), and `G1Class` is imported by the root (line 53), so the module is in the root's transitive closure, is elaborated, and its 23 theorems have `#print axioms LocalFiniteAlphabet.*` lines in the root (lines 1386 ff.). The inventory records `root_import: false`, `parked: false`. |
| Imports | `Derivation.CapacityBound` |
| Declarations | 1 inductive (`ImportDiscipline`), 2 structures (`LocalStrategy`, `BaseObstructed`), 15 defs, 23 theorems, 1 derived instance (`DecidableEq ImportDiscipline`); namespace `LocalFiniteAlphabet` |
| Axiom reports in `artifacts/lean_axioms.txt` | 23 lines (every theorem, under `LocalFiniteAlphabet.*`); `profileCode_lt_eight`: none; `perPair_recurring`, `perPair_identityGrade`, `perPair_not_finite`, `valued_oneTimeIdentity`, `valued_not_finite`: propext; the other 17: propext, Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module declares a class of repair strategies for the reflective chain's standing demand and derives the class-relative form of conjecture G1. A `LocalStrategy d` is an import-discipline tag, a colouring family `colour n : Nat → Nat`, a repair view family `view n : Nat → Nat`, and a proof that at every chain length the view factors through the radius-`d` colour ball (`CapacityBound.ViewLocal`). `FiniteDeclaration k S` says one alphabet bound `k` holds at every length and every index. `Fires` says arbitrarily long chains carry a pre-repair depth-1 obstruction; `Clears` says the view separates every obstructed pair at every length; `IdentityGrade` says it separates every distinct pair. The theorems: every strategy fires (because the chain does); identity grade implies clearing; the capacity bound applied to a finite member gives a deep equal-view pair; hence no finite local member clears, none is identity-grade, and the conjunction "fires, clears, no recurring import" is excluded for the class. Five concrete members (bare, presence, depth-two, per-pair fresh marking, valued) are built and classified, with the boundary facts that depth-two does clear length 4 and that the two identity-grade members are not finite declarations.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `ImportDiscipline` | 21 | inductive | `oneTime | recurring`, a declared tag | ADMITTED (declared label; see §4) |
| `LocalStrategy d` | 28 | structure | import tag, `colour : Nat → Nat → Nat`, `view : Nat → Nat → Nat`, `locality : ∀ n, ViewLocal (view n) (colour n) d` | ADMITTED (the declared class) |
| `FiniteDeclaration k S` | 35 | def | `∀ n x, S.colour n x < k` | ADMITTED |
| `RecurringImport S` | 39 | def | `S.importDiscipline = .recurring` | ADMITTED (reads the tag) |
| `BaseObstructed n i j` | 44 | structure | `i ≤ n`, `j ≤ n`, `i ≠ j`, equal `profile1 (reflState n)` | ADMITTED (the inherited depth-1 obstruction) |
| `Fires S` | 51 | def | `∃ n0, ∀ n ≥ n0, ∃ i j, BaseObstructed n i j` — **does not depend on `S`** (`_S`) | ADMITTED |
| `ClearsOn S n` | 56 | def | every base-obstructed pair at length `n` gets distinct views | ADMITTED |
| `Clears S` | 60 | def | `∀ n, ClearsOn S n` | ADMITTED |
| `IdentityGrade S` | 64 | def | distinct carrier indices get distinct views, every `n` | ADMITTED |
| `OneTimeIdentity S` | 69 | def | one-time tag ∧ `IdentityGrade` | ADMITTED |
| `zeroRadiusStrategy` | 123 | def | radius-0 member with `colour = view = f` | ADMITTED |
| `boolCode`, `profileCode` | 134, 138 | def | the 3-bit depth-1 profile as a number below 8 | ADMITTED |
| `bare` | 147 | def | view = coded depth-1 profile | ADMITTED (concrete member) |
| `presence` | 154 | def | `:= bare` (presence is the first bit of the profile) | ADMITTED |
| `depthTwo` | 158 | def | radius-1 member: colour = coded profile, view = base-8 encoding of the colour ball | ADMITTED |
| `perPairFreshMark` | 169 | def | radius-0, `colour = view = fun _ i => i`, tag `recurring` | ADMITTED |
| `valued` | 174 | def | radius-0, `colour = view = fun _ i => i`, tag `oneTime` — the same functions as `perPairFreshMark` | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `fires_every_strategy` | 72 | `Fires S` for every `S` (witness `n0 = 3`, pair `(1,2)`, from `generation_never_dries`) | FROZEN (trivially in `S`) | propext, Quot.sound | S |
| `identityGrade_implies_clears` | 78 | `IdentityGrade S → Clears S` | FROZEN | propext, Quot.sound | A |
| `strategy_capacity_collision` | 84 | `FiniteDeclaration k S → k^(2d+1)+2d+2 ≤ n → ∃ distinct deep i j, S.view n i = S.view n j` | CONDITIONAL:`FiniteDeclaration k S`, threshold | propext, Quot.sound | S |
| `finite_local_not_clears` | 93 | `FiniteDeclaration k S → ¬ Clears S` | CONDITIONAL:`FiniteDeclaration k S` | propext, Quot.sound | S |
| `finite_local_not_identityGrade` | 104 | `FiniteDeclaration k S → ¬ IdentityGrade S` | CONDITIONAL:`FiniteDeclaration k S` | propext, Quot.sound | S |
| `g1_local_finite_alphabet_class` | 113 | `FiniteDeclaration k S → Fires S ∧ ¬ Clears S ∧ ¬ (Fires S ∧ Clears S ∧ ¬ RecurringImport S)` | CONDITIONAL:`FiniteDeclaration k S` | propext, Quot.sound | S |
| `profileCode_lt_eight` | 141 | `profileCode p < 8` | VERIFIED_FINITE | none | A |
| `bare_finite` | 177 | `FiniteDeclaration 8 bare` | FROZEN | propext, Quot.sound | A |
| `presence_finite` | 181 | `FiniteDeclaration 8 presence` | FROZEN | propext, Quot.sound | A |
| `presence_eq_bare` | 183 | `presence = bare` (rfl) | FROZEN | propext, Quot.sound | A |
| `depthTwo_finite` | 185 | `FiniteDeclaration 8 depthTwo` | FROZEN | propext, Quot.sound | A |
| `depthTwo_clears_n4` | 191 | `ClearsOn depthTwo 4` | VERIFIED_FINITE (case split + `decide`) | propext, Quot.sound | S |
| `perPair_recurring` | 203 | `RecurringImport perPairFreshMark` (rfl on the tag) | FROZEN | propext | A |
| `perPair_identityGrade` | 205 | `IdentityGrade perPairFreshMark` | FROZEN | propext | A |
| `perPair_not_finite` | 209 | `¬ FiniteDeclaration k perPairFreshMark` for every `k` | REFUTED (of finiteness; witness `x = k`) | propext | A |
| `valued_oneTimeIdentity` | 214 | `OneTimeIdentity valued` | FROZEN | propext | A |
| `valued_not_finite` | 220 | `¬ FiniteDeclaration k valued` | REFUTED (of finiteness) | propext | A |
| `valued_clears` | 224 | `Clears valued` | FROZEN | propext, Quot.sound | S |
| `class_nonvacuity` | 227 | `Fires bare ∧ ClearsOn depthTwo 4 ∧ IdentityGrade valued` | FROZEN/VERIFIED_FINITE (conjunction of the above) | propext, Quot.sound | A |
| `bare_not_identityGrade` | 232 | `¬ IdentityGrade bare` (pair `(1,2)` at `n = 3`) | REFUTED | propext, Quot.sound | A |
| `bare_classification` | 241 | finite 8, fires, ¬clears, ¬recurring | FROZEN | propext, Quot.sound | S |
| `presence_classification` | 248 | same for `presence` | FROZEN | propext, Quot.sound | A |
| `depthTwo_classification` | 255 | finite 8, fires, ¬clears, ¬recurring | FROZEN | propext, Quot.sound | S |

## 4. External and admitted assumptions

- **`Fires` is independent of the strategy.** Its body ignores `_S`; it is a fact about the chain (`generation_never_dries`). Consequently `fires_every_strategy` holds for every `S` including ones that clear, and the "cycle" `Fires S ∧ Clears S ∧ ¬ RecurringImport S` is excluded exactly when `¬ Clears S` or `RecurringImport S`. The module's header says "`Fires` concerns the inherited depth-one obstruction before repair" — consistent, but the textbook must say that `Fires` is not a property of `S`.
- **`ImportDiscipline` is a declared label, not a derived property.** `perPairFreshMark` and `valued` have identical `colour` and `view` (`fun _ i => i`) and differ only in the tag. Nothing in Lean connects the tag to any import, cost or event; the "recurring import" is an admission about how the strategy is to be read. The ledger classifies the class as declared metatheory (`CL-G1-LOCAL-CLASS`) and the five rows as "bounded mirror"; the paper says per-pair "clears by recurring imports". Flag: the cost reading rests on the tag alone.
- `FiniteDeclaration k S` bounds `colour n x` for all `n, x : Nat`, including indices outside the chain. For the identity colouring this is what makes `valued` non-finite (`x = k`); a colouring bounded on the carrier `0..n` but not on all of `Nat` would also be excluded. Scope note.
- `colour : Nat → Nat → Nat`, `view : Nat → Nat → Nat`: total metatheoretic functions over every length and index (finitude flag). The `locality` proof is per length `n` — the factor `g` may depend on `n` (it is existential inside `∀ n`); only the radius and (under `FiniteDeclaration`) the alphabet are uniform. The header's "one fixed radius" is right; "one fixed factor function" (the Python docstring) is stronger than the Lean, where `g` may vary with `n`. Minor.
- Library lemmas doing work: `simp [colourBall, ball]` in `zeroRadiusStrategy.locality` (computes the radius-0 ball to `[i]`), `simpa` on the identity views, `omega`, `decide` on `reflState 3/4`, `CapacityBound.capacity_bound`, `Generator.generation_never_dries`, `middle_profile`, `depth1_obstructions_are_exactly_middle_pairs`.
- Unearned identity: none. Unrestricted external universe: none (all `Nat`). Unbounded function treated as internally available: the strategy families (flagged). Silently assumed observer: the class declares its observers. Unspecified correspondence between presentations: `presence := bare` is a definitional identification, stated (`presence_eq_bare`). Cost function without justification: the import tag (flagged above). Admitted condition later described as forced: none found. Finite computation presented as universal: `depthTwo_clears_n4` is one length and is presented as such.

## 5. Derived consequences

`G1Class` restates `g1_local_finite_alphabet_class` as `g1_class_exclusion`, derives `local_strategy_cycle_impossible` from `finite_local_not_clears`, and uses `valued`, `valued_clears`, `fires_every_strategy` for `clears_does_not_imply_not_fires`. Ledger: `CL-G1-LOCAL-CLASS` (definitions), `CL-G1-CAPACITY-APPLICATION` (`strategy_capacity_collision`), `CL-G1-CLASS-EXCLUSION`, `CL-G1-FIVE-STRATEGIES`, `CL-G1-G3-COUNTEREXAMPLE`, `CL-G1-TERMINAL-20260826`. Paper: `paper/endogenous_generator.md` §"The class and the exclusion" (2026-08-26). Receipt: `artifacts/g1_class_receipt.json` via `code/derivation/g1_class_receipt.py` (quotes the definitions and binds the 23+ axiom reports).

## 6. Counterexamples and limitations

- `perPair_not_finite`, `valued_not_finite`: the two identity-grade members are outside the finite class (so the exclusion does not touch them — by hypothesis, not by proof of anything about them). `bare_not_identityGrade`: the bare view merges `(1,2)` at length 3. `depthTwo_clears_n4` + `depthTwo_classification`: a member can clear one length and still not clear all.
- Not proved: anything about strategies whose view does not factor through a fixed-radius ball, or whose alphabet grows with `n` (the ledger says "outside the class, not disproved"); unrestricted G1; any dynamic statement about repair over rounds (no state transition is modelled; the 15-round trajectories are Python only); any relation between the import tag and an actual cost.

## 7. Axiom dependencies

All 23 within `{propext, Quot.sound}`. None exceed: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 23 theorems in the artifact under `LocalFiniteAlphabet.*`; the root's `#print axioms` inventory lists them although the root does not import the module directly (it reaches it through `G1Class`). The ledger cites every theorem across the `CL-G1-*` entries. No probe run.

## 9. Related Python implementations

`code/derivation/local_strategy.py`: `ball`, `encode`, `profile_code`, `LocalStrategy` (dataclass with `radius`, `import_discipline`, `colour`, `factor`; `colour_ball`, `view`), `base_obstructions`, `fires_within`, `clears_within`, `identity_grade_within`, `finite_declaration_within`, `finite_factor_table`, `capacity_threshold`, `capacity_collision`, `classification`, `artifact_payload`; artifact `artifacts/local_strategy.json`; tests `tests/test_local_strategy.py` (`test_ball_and_encoding_match_lean_conventions`, `test_five_strategies_have_the_declared_classification`, `test_finite_local_members_have_capacity_collisions`, `test_identity_and_import_boundaries_are_nonvacuous`, `test_unconstrained_view_fails_locality_fiber_check`, …); `code/derivation/g1_class_receipt.py` / `tests/test_g1_class_receipt.py`.

## 10. Textbook placement proposal

- Prerequisites: Generator FG3–FG4 (`generation_never_dries`), CapacityBound (`ViewLocal`, `capacity_bound`), the distinction between a pre-repair obstruction and a post-repair view.
- Substantive: the class definition (`LocalStrategy`, `FiniteDeclaration`, `Fires`, `Clears`, `IdentityGrade`), `strategy_capacity_collision`, `finite_local_not_clears`, `g1_local_finite_alphabet_class`, `depthTwo_clears_n4` (as the non-vacuity witness), `valued_clears` + `valued_not_finite` (the escape is paying for identity). Auxiliary: the codes, the per-member finiteness facts, `presence_eq_bare`, `class_nonvacuity`, the three `*_classification` bundles.
- Lesson title: "No bounded local repair clears a growing demand." Question answered: inside the declared class, can a fixed-radius, fixed-alphabet repair view ever separate every obstructed pair at every length? No; and the two views that can are not finite declarations.
- Recommend omitting: `presence` as a separate member (it is `bare`); `class_nonvacuity` (a restatement); the `ImportDiscipline` tag from theorem statements — teach it as a label the Lean does not interpret.

## 11. Interpretation findings

1. `g1_local_finite_alphabet_class` / `CL-G1-CLASS-EXCLUSION` — ledger: "every finite declared local member fires on the inherited reflective family, fails to clear every chain length, and cannot satisfy `Fires S and Clears S and not RecurringImport S`"; paper: "the fire/clear/no-recurring-import cycle is impossible". Lean: `Fires S` is a constant predicate (its body does not mention `S`), so "fires on the inherited family" says nothing about the member, and the third conjunct is a one-line consequence of the second. No "cycle" (a sequence of rounds) is modelled; the conjunction is of three static predicates. Classification: INTERPRETATION DEFECT (minor-to-moderate: the word "cycle" and the phrase "member fires" overread a correct theorem whose content is `¬ Clears S`).
2. `ImportDiscipline` / `perPair_recurring` — paper FG5 and the five-strategy table: per-pair marking "clears by recurring imports", valued is "one declared identity-grade value rule". Lean: `perPairFreshMark` and `valued` are the same colouring and view; `RecurringImport` is `rfl` on a declared tag. The Lean proves nothing about imports; the cost reading is an admitted label. The ledger's `CL-G1-LOCAL-CLASS` does classify the class as declared metatheory. Classification: INTERPRETATION DEFECT (minor; the tag is honest in the ledger but the paper prose reads it as a derived property).
3. Python docstring (`local_strategy.py`): "its view is obtained by applying one fixed factor function to one fixed-radius colour ball". Lean: `locality : ∀ n, ∃ g, …` — the factor may depend on `n`. Classification: INTERPRETATION DEFECT (minor; the Python class is narrower than the Lean class, so Python witnesses are valid Lean members, but the Lean exclusion is stronger than the Python description suggests, not weaker).
4. Vacuity: `FiniteDeclaration k S` at `k = 0` is unsatisfiable (every theorem conditional on it is vacuous there); for `k = 8` it is inhabited by `bare`, `depthTwo`. `BaseObstructed` is inhabited (`n = 3`, `(1,2)`). None vacuous as used.
