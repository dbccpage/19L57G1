# G1 local finite-alphabet class — claim and attack ledger

Date: 2026-08-26

This ledger is scoped to the class quoted in
`artifacts/g1_class_receipt.json`. It records theorem, computation,
counterexample, and boundary separately. It does not authorize a new
object-language declaration.

## Claims

### G1-LC-CLASS

- **Statement**: `LocalStrategy d` carries a fixed import discipline,
  colouring, repair view, and a proof that the view factors through the
  radius-`d` colour ball. `FiniteDeclaration k S` uses one `k` at every chain
  length.
- **Class**: admitted metatheoretic class definition.
- **Evidence**: exact Lean source quotes in the receipt; executable mirror in
  `code/derivation/local_strategy.py`.
- **Falsifier**: a purported member whose equal colour balls receive unequal
  view values, or whose alphabet bound grows with chain length.
- **Boundary**: index-inspecting views and growing alphabets are outside the
  class, not refuted by definition.

### G1-LC-T5

- **Statement**: on arbitrary interior indices and arbitrary chain length,
  equality of sealed depth-two profiles is equivalent to equality of
  radius-one structural profiles.
- **Class**: theorem.
- **Lean**: `SeparationCapacity.radius_one_agrees_with_sealed_depth2`, with
  its seven constructive shape/filter helpers. The receipt binds all eight
  reports; each lies within `{propext, Quot.sound}`.
- **Falsifier**: interior `n,i,j` for which the two equality relations differ.
- **Boundary**: this is radius one; it is not the G1 class consequence.

### G1-LC-CAPACITY

- **Statement**: every finite declared local strategy collides on a distinct
  deep pair once
  `k ^ (2 * d + 1) + 2 * d + 2 <= n`. The view bound is derived from the
  alphabet and radius; it is not a separate assumption.
- **Class**: theorem consuming `CapacityBound.capacity_bound` directly.
- **Lean**: `LocalFiniteAlphabet.strategy_capacity_collision` and
  `finite_local_not_clears`; axiom reports within
  `{propext, Quot.sound}`.
- **Python**: `artifacts/local_strategy.json` records concrete thresholds
  10, 10, and 516 for the three finite concrete members.
- **Falsifier**: a member satisfying `FiniteDeclaration` and `ViewLocal` that
  separates every deep pair at or above the displayed threshold.

### G1-LC-EXCLUSION

- **Statement**: every fixed-radius finite-alphabet local member fires on the
  inherited reflective family, fails to clear every chain length, and cannot
  satisfy `Fires S and Clears S and not RecurringImport S`.
- **Class**: horizon-free class theorem, not bounded enumeration.
- **Lean**: `LocalFiniteAlphabet.g1_local_finite_alphabet_class`,
  `G1Class.local_strategy_cycle_impossible`, and
  `G1Class.g1_class_exclusion`; axiom reports within
  `{propext, Quot.sound}`.
- **Python**: bounded witnesses and concrete membership rows only; they are
  not the proof.
- **Falsifier**: a quoted-class member satisfying the full cycle.
- **Boundary**: `OB1_UNCHANGED`; unrestricted repair channels are not
  quantified over.

### G1-LC-FIVE

- **Statement**: bare, presence, and depth-two are finite class members that
  fire and fail to clear all lengths; per-pair fresh marking is recurring and
  not finite; valued marking is one-time identity-grade, clears, and is not
  finite. Presence is bare. Depth-two clears the nontrivial length-4 case.
- **Class**: theorem classification plus deterministic bounded mirror.
- **Lean**: the 15 concrete theorems from `bare_finite` through
  `depthTwo_classification`, all bound by the receipt.
- **Python**: `artifacts/local_strategy.json`, five rows, check bound 15.
- **Falsifier**: disagreement between a row and its named Lean proposition,
  or acceptance of the constant-colour identity-view probe as local.

### G1-LC-G3

- **Statement**: G3 is not derived from the present predicates. A one-time
  valued strategy witnesses both `Clears` and `Fires`, because clearing is
  post-repair while firing is the inherited pre-repair demand.
- **Class**: counterexample to the proposed implication; G3 remains a
  conjecture.
- **Lean**: `G1Class.clears_does_not_imply_not_fires`, within
  `{propext, Quot.sound}`.
- **Missing hypothesis**: a state-transition semantics connecting a repair to
  the absence of future demands.
- **Boundary**: no universe-wide conservation law is claimed.

### G1-LC-G4

- **Statement**: **WITHDRAWN** — the former 455-pair computation never passed
  its enumerated chain pair to the engine. It repeated the four fixed
  Challenge-3 catalogs, so no finite chain correspondence was established and
  G4 remains a conjecture. The original Challenge-3 L/F and `mu1`/`mu2`
  minima remain available only in their prior scope.
- **Class**: refuted finite claim; surviving G4 status is conjecture.
- **Python**: `artifacts/challenges.json`, `code/derivation/engine.py`, and
  `tests/test_engine.py` support only the surviving Challenge-3 catalogs.
- **Falsifier**: a declared collapse-preserving chain adapter followed by a
  replayable run in which every counted pair reaches `min_responses`.
- **Boundary**: Challenge-3 minima do not authorize a carrier encoding, a
  reading, or an identification with an object-language generator.

### G1-LC-RECEIPT

- **Statement**: the deterministic receipt binds the base commit, operator
  task hash, toolchains, exact Python lock, prompt hashes, exact class and
  exclusion quotes, 34 new theorem reports, every finite bound, all five
  verdicts, T5/G3 status, the G4 withdrawal, and every OPEN/WITHDRAWN sentence
  introduced by this run.
- **Class**: receipt binding, not mathematical proof.
- **Python**: `code/derivation/g1_class_receipt.py`,
  `tests/test_g1_class_receipt.py`, `artifacts/g1_class_receipt.json`.
- **Falsifier**: lock/hash/source/report drift that nevertheless regenerates
  the same receipt.

## Strategy membership verdicts

| strategy | finite local class | import | fires | clears | identity-grade | disposition |
|---|---:|---|---:|---:|---:|---|
| bare | yes, `k=8,d=0` | one-time | yes | no | no | class member; unrepaired |
| presence | yes, `k=8,d=0` | one-time | yes | no | no | definitionally bare |
| depth-two | yes, `k=8,d=1` | one-time | yes | no globally | no | clears length 4, then outrun |
| per-pair fresh mark | no | recurring | yes | yes | yes | repairs by recurring import |
| valued mark | no | one-time | yes | yes | yes | prevents separation failure after declaration |

## Required adversarial audit

| # | result | record |
|---:|---|---|
| 1 | SURVIVED | The theorem consumes the capacity bound and has no 15-round premise; the bounded artifact is labelled only as witness computation. |
| 2 | SURVIVED | `ViewLocal` is a field. Injection changed the bounded fiber classifier to accept inconsistent views; `test_unconstrained_view_fails_locality_fiber_check` failed with `{(0,): 0} is None`, then passed after reversal. |
| 3 | SURVIVED | The theorem threshold derives `k ^ (2*d+1)` and assumes no independent `B`. |
| 4 | SURVIVED | `valued_not_finite` proves failure for every fixed `k`; the concrete row has no alphabet size. |
| 5 | SURVIVED | `perPair_recurring` and `perPair_not_finite` keep one-item-per-demand growth classified as recurring. |
| 6 | SURVIVED | `presence_eq_bare`, `presence_classification`, and the mirror show presence does not repair. |
| 7 | SURVIVED | `fires_every_strategy` consumes `generation_never_dries`; cycle exclusion separately requires and refutes `Clears`. |
| 8 | SURVIVED | No progress marker is used as a demand source. |
| 9 | SURVIVED | Every terminal surface includes `OB1_UNCHANGED`; the theorem is explicitly class-relative. |
| 10 | SURVIVED | Index inspection is outside `ViewLocal`, not presented as a third in-class way. |
| 11 | SURVIVED | An alphabet growing with chain length fails `FiniteDeclaration`; it is not called endogenous. |
| 12 | WITHDRAWN_AND_REPAIRED | The first general T5 proof shape leaked `Classical.choice` through generic natural-number equality filtering. It was withdrawn; `Generator.profile2` and the filter lemmas now use `decide`, and use-site reports are within the whitelist. |
| 13 | SURVIVED | Names are resolved by Lean and recorded by the generated axiom inventory; no theorem count is inferred from source text. |
| 14 | SURVIVED | `g1_class_exclusion` states and proves the same full conjunction; the exact declaration is quoted in the receipt. |
| 15 | SURVIVED | No forbidden comparison vocabulary from attack 15 was added to a sealed file. |
| 16 | SURVIVED | Both sealed prompt files remain hash-pinned; the receipt recomputes their hashes. |
| 17 | SURVIVED | The axiom artifact was regenerated by `ci/regen_axiom_artifact.py`, not shell redirection. |
| 18 | SURVIVED | No artifact or receipt was regenerated during any live injection. |
| 19 | SURVIVED | No functoriality, initiality, preferred strategy, or object-language generator claim is made. |
| 20 | WITHDRAWN_AND_REPAIRED | G3 has a Lean counterexample and remains conjectural. The former finite G4 success/failure terminals are withdrawn because the loop never passed a chain pair to the engine; the current status is `G4_REMAINS_CONJECTURE`. |

## Injection receipts

1. **Locality fiber classifier**: inconsistent equal-ball views were
   deliberately accepted. The negative-locality test failed by name and
   displayed the wrongly accepted table. Reversal restored one passing test.
2. **Historical G4 mark classifier (deleted at `38fca668`)**: before deletion,
   an instance using an argument outside the target pair was deliberately
   labelled pair-only. The shape test failed by name; the reading-F count test
   also changed from two outside-target classes to zero. Reversal restored both
   passing tests. This records the former test surface only and supplies no
   current G4 artifact, terminal, or chain correspondence.
3. **Receipt axiom resolver**: the report for
   `G1Class.g1_class_exclusion` was deleted temporarily. Receipt construction
   failed with `missing axiom report: G1Class.g1_class_exclusion`. Reversal
   restored the passing receipt test.

## Full-gate integration finding

The first full completion-inventory run failed by name at
`LocalFiniteAlphabet.profileCode_lt_eight`: the new namespaces were absent
from the source-module map, so all 26 LocalFiniteAlphabet/G1Class reports were
`UNRESOLVED`. This was a real live defect, not an injection. The repair adds
both exact module mappings and individual kind/role classifications for all
34 new reports, including the eight T5 reports in the otherwise unclassified
SeparationCapacity namespace. `test_g1_local_inventory_surface_is_exact`
pins the complete set. The inventory test then recovered with 1,506 resolved
records. The expanded axiom bytes required ordered regeneration of
`completion_dependency_graph.json`, `completion_receipt.json`, and
`primitive_completion_receipt.json`; the all-runner comparison named exactly
those three before regeneration.

The subsequent full suite exposed the ledger's independent schema gate: all
eight new `CL-G1-*` entries were unpinned and lacked required explicit fields.
The repair did not add them to any legacy-gap ratchet. Instead every entry now
states dependencies and assumptions, uses the closed Class vocabulary, and
has nonvacuous Python, Lean, axiom, and falsifier fields as applicable. The
heading census and generated claim-body pin were extended to 135 entries.
All 26 conformance tests then passed.

## OPEN

- OB-1 / CL-CLOSURE-POLICY remains OPEN outside the declared
  `LocalStrategy` class.
- G3 remains a CONJECTURE because no state-transition hypothesis connects
  post-repair clearing to absence of future pre-repair demands.
- G4 remains a CONJECTURE because no collapse-preserving chain-pair-to-engine
  adapter is defined or authorized.
- Strategies outside the fixed-radius finite-alphabet class remain OPEN.
- F4 chain initiality remains carried and OPEN.
- The definition-level axiom residual remains OPEN.
- The comparison-heading conflict remains OPEN for an author act.

## WITHDRAWN

- The previous three-line generator TERMINAL block is WITHDRAWN as the current
  complete terminal; its generation theorem remains supported.
- The two old sentences saying T5 and the class consequence remained OPEN are
  WITHDRAWN.
- The first T5 proof shape with a choice-dependent equality filter is
  WITHDRAWN and replaced by the constructive `decide` form.
- The former finite G4 split, including its success and failure terminals, is
  WITHDRAWN because no chain correspondence was computed. G4 remains a
  CONJECTURE.
