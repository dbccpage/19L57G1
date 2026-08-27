# Partial decision-grade claim ledger

`AuthorityEffect: None`

## PD-GRADE-1 — Partial bounded grade

- **Class:** deterministic metatheoretic computation
- **Statement:** For a valid declared rule-free engine regime, ordered target,
  measure, candidate bounds with at most two items, and positive isomorphism
  budget on which canonicalization completes, `decide` returns `None` exactly
  when `min_responses` returns `None`; otherwise it returns `UniqueDelta`,
  `UniqueClass`, or `Tie` according to the raw-minimum and quotient-class
  counts. Isomorphism-budget exhaustion propagates as `IsoBudgetError`, never
  as `None`.
- **Evidence:** `partial_decide.py`; `test_partial_decide.py`.
- **Assumptions:** The supplied regime, target, measure, candidate bounds, and
  permutation budget are declared metatheory. The existing candidate grammar,
  measures, and isomorphism relation are imported pinned inputs.
- **Falsifier:** A valid input for which the returned tag disagrees with the
  retained raw/class counts, or a bounded absence represented by any tag other
  than `None`, or budget exhaustion represented as `None`.
- **Nonclaim:** No input is derived from the panel. Candidate admission-event
  values are replayed only into ephemeral comparison children for quotienting;
  no candidate is authorized and no response or event is persistently applied
  or committed to the declared base.

## PD-GRADE-2 — Challenge-3 grades

- **Class:** deterministic bounded computation
- **Statement:** At the pinned source snapshot and declared C3 bounds, L/mu1
  has six raw minima in three classes, F/mu1 has ten in five classes, and both
  mu2 cases have two raw minima in one class. Hence C3 has no `UniqueDelta`,
  while its mu2 `UniqueClass` is inhabited. After source custody and runtime-
  origin checks, the verifier independently replays every retained member and
  requires its computed canonical key to equal the class key recorded beside
  it.
- **Evidence:** `partial_decide_c3.json`; `verify_pins.py`;
  `test_partial_decide.py`.
- **Assumptions:** The sealed engine's retained L/F readings and targets, the
  declared mu1/mu2 measures, `Bounds(2, 2)`, and permutation budget 100000.
- **Falsifier:** Receipt regeneration or direct computation produces different
  counts/tags, loses a member, or introduces a C3 `UniqueDelta`.
- **Nonclaim:** One isomorphism class is not one literal delta and authorizes
  no endpoint choice.

## PD-GRADE-3 — Panel boundary

- **Class:** open interface boundary
- **Statement:** Within `research/partial_decide` and its exact pinned import
  surface, no declared correspondence connects panel indices from
  `certNeg`/`PanelEquiv` to an engine `Regime` and ordered target. This claim is
  not a repository-wide negative.
- **Evidence:** the scoped source audit recorded in `STATUS.md`; tracked-package
  and import censuses in `SOURCE_PINS.json` and `verify_pins.py`.
- **Assumptions:** The exact tracked package and pinned source/import census
  checked by `verify_pins.py`.
- **Falsifier:** A consumer import or local definition constructs a panel-to-
  engine carrier/pair link, or a panel certificate chooses any decision input
  or quotient member.
- **Nonclaim:** `None` does not encode absence of a panel adapter. The verifier
  enforces syntax, imports, and custody; it does not recognize every possible
  semantic adapter.

## Scoped status labels

These labels are scope-qualified receipt statuses at the pinned source
snapshot, displayed bounds, and permutation budget. They are not engine
termination, repository completion, satisfaction of the global stopping
conditions, or authority. The two C3 labels are computed here; the panel,
authorization, persistent-application, declared-base-event, and generator
labels are refusal/interface boundaries. Candidate enumeration and
admission-event replay into ephemeral comparison children are live; they are
not an authorization, persistent base mutation, or object-language demand
generator. The G3/G4 labels are inherited from the mechanically pinned
`artifacts/g1_class_receipt.json`, not produced by `decide`.

```text
C3_UNIQUE_DELTA_EMPTY
C3_MU2_UNIQUE_CLASS_INHABITED
G3_REMAINS_CONJECTURE
G4_REMAINS_CONJECTURE
NO_AUTHORIZED_OR_PERSISTENT_RESPONSE_APPLICATION
NO_EVENT_COMMITTED_TO_DECLARED_BASE
NO_PANEL_DERIVED_INPUT
NO_PANEL_ENGINE_ADAPTER
NO_RESPONSE_AUTHORIZATION
OBJECT_LANGUAGE_GENERATOR_NOT_IN_SCOPE
PANEL_TO_ENGINE_LINK_NOT_DEFINED
```
