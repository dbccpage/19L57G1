# Occurrence lane report

`AuthorityEffect: None`.

## Terminal

`TRACE_PROJECTION_PROVED_CONNECTOR_INTEGRATION_OPEN`

The exact frozen token-aware replay trace determines an occurrence projection.
The deduplicated replay endpoint does not determine that projection or its
count.  Consequently, `OCCURRENCE_HISTORY` can be removed as a separate input
only from a connector that already retains and supplies the exact
`List Derivation.TEvent` trace.  It is not removed from an endpoint-only
connector.  `COUNT_UNIT_CALIBRATION` is not removed.

## Exact imports and custody

- Direct Lean import: `Derivation.Erasure`.
- Exact frozen commit: `3100c4ed5ce70d2b6cff6d2ccd3b0251cf918d0a`.
- Exact `lean4/Derivation/Erasure.lean` blob:
  `b855d58a7196c13591b6d43c3dac68adb58f146c`.
- Local support import: `AdmissionSignShadow.Core`.
- `verify_frozen_compatibility.py` materializes the exact frozen tree in an
  ephemeral directory, checks every pinned frozen source blob, and requires
  the exact nine-declaration axiom-report population for this lane.
- No shared root import, ledger, manifest, receipt, or sealed source was
  changed.

## Symbol disposition

| Symbol | Status | Exact evidence or obligation |
|---|---|---|
| replay-derived occurrence projection | `PROVED` | `occurrenceReplay_valid`, `occurrenceReplay_count`, and `replayT_tokens` operate on exact `Derivation.TEvent` histories |
| forget/replay commutation | `PROVED` | `forget_occurrenceReplay_commutes`, under successful `Derivation.replayT` from the empty token-aware regime |
| deterministic IDs and count | `PROVED` | `ids_withIdsFrom`, `occurrenceReplay_count`; IDs are consecutive datum-admission positions |
| duplicate-admission endpoint collision | `PROVED` | `duplicate_admission_endpoint_collision` uses actual `replayT`; one and two admissions of token 7 have the same endpoint and counts 1 and 2 |
| ID-renaming invariance | `PROVED` | `countToken_renameIds`, `forgetOccurrences_renameIds`; `occurrenceValid_renameIds` requires injectivity |
| endpoint determines occurrence history | `REFUTED` | `endpoint_does_not_determine_occurrence_history` |
| endpoint determines occurrence count | `REFUTED` | `endpoint_does_not_determine_occurrence_count` |
| additive laws select an integer unit | `REFUTED` | `additive_laws_do_not_select_integer_unit`; every integer scale supplies an additive encoding |
| unit-calibrated encoding is standard count | `CONDITIONAL` | `unit_calibration_is_conditional` additionally assumes `encode 1 = 1` |
| retained-trace connector integration | `OPEN` | the exact projection exists, but the current connector does not consume `List TEvent` |
| endpoint determines retained event trace | `OPEN` | no such recovery is supplied, and the duplicate-admission collision prevents recovery in general |

The machine-readable version is `SYMBOL_PACKET.json`.  Its only status values
are `PROVED`, `CONDITIONAL`, `REFUTED`, and `OPEN`.

## Remaining obligations and nonclaims

1. The connector interface must actually carry the retained `List TEvent`.
   `replayT` accepting a history proves that the trace is a valid input type;
   it does not prove every downstream endpoint report retains that trace.
2. Consecutive occurrence IDs are a deterministic analysis convention.  The
   proved injective-renaming invariance shows that numeric ID names carry no
   count or endpoint content.
3. Forget/replay commutation has the successful-replay premise.  An ill-formed
   trace yields `none` and has no endpoint to compare.
4. No theorem recovers an occurrence history from `TRegime.tokens`, from
   `TRegime.erase`, or from a canonical endpoint.
5. Additivity and zero determine an integer encoding only relative to its
   freely chosen value at one.  The premise `encode 1 = 1` remains a
   calibration, not a Genesis theorem.
6. This isolated lane does not modify the shared connector, so it does not by
   itself change the repository-wide import ledger or terminal.

## Verification

The shared compatibility receipt records the frozen commit/tree, the exact
Erasure blob, the local source hashes, an empty frozen-source-copy census,
Lean exit zero, and exact equality between expected and observed theorem
reports.

The printed Lean dependency reports contain only `propext` and, for the
list-fold/equality results, `Quot.sound`.

Python replay and mutation suite:

```text
Ran 11 tests in 0.001s
OK
```

The tests cover exact packet replay, supply inertness, event filtering,
deterministic IDs, forget/replay agreement, the duplicate endpoint collision,
injective and non-injective ID renaming, multiple additive integer scales, and
the conditional unit calibration.
