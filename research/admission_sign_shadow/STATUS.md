# Status

`AuthorityEffect: None`.

## Terminal verdict

`BRIDGE_PRODUCERS_PROVED_END_TO_END_OPEN`

All three bridge lanes now compile against the exact frozen interfaces in an
ephemeral build. Exact frozen facts, a chosen two-point equivalence,
retained-trace occurrence projection, actual adapter signature, and the
negative results below are machine checked. The end-to-end connector remains
open because source authorization, operational nontriviality, integer unit
calibration, adapter fields, and retained-trace integration are not derived.

## Exact custody

- Post-seal source base commit: `be7476868e496e06d5dec6599fa4346394c512bd`
- Post-seal source base tree: `0821fc9bc55fa551e0dd4752542221e109d3e36c`
- Publication base commit: `470eec30505ede6ed4b1ec16c689e00d91cc735d`
- Publication base tree: `34d77a4c9be4f7670fe03484f61de3bfb5c76da0`
- Frozen annotated tag object: `e147f01cfed1d17410c55a1e78367fdadc63a5ae`
- Frozen peeled commit: `3100c4ed5ce70d2b6cff6d2ccd3b0251cf918d0a`
- Frozen tree: `d015d9085217267f5cf895935aad13236f1bb6b5`
- Write root: `research/admission_sign_shadow/`

`SOURCE_MANIFEST.json` records exact blob hashes and toolchain text. That is a
custody result, not a semantic correspondence theorem.

## What is proved

- exact classification of the local two-point exchange characters;
- conditional uniqueness of negative exchange after supplied nontriviality;
- relative-label uniqueness after a supplied basepoint;
- failure of canonical ordered deduplication to determine occurrence count;
- occurrence count and calibrated integer laws in a declared presentation;
- conditional coordinate-square agreement and mixer separation;
- collapse, endpoint, trivial-character, flat-mixer, and larger-carrier
  falsifiers;
- two-way non-determination between the local section types.
- exact frozen history and endpoint distinction with exact erased-endpoint
  equality;
- a chosen post-seal equivalence between the exact frozen pair and local
  `HistoryClass`, explicitly without source authorization or uniqueness;
- deterministic occurrence history, count, validity, and ID-renaming laws
  from a retained exact `List Derivation.TEvent`;
- impossibility of recovering occurrence history or count from the
  deduplicated endpoint;
- impossibility of selecting an integer unit from zero and additivity alone;
- an adapter kernel stated against the exact `Family`, `Sec`, `IsNatural`,
  and `PresIso.mapPair` types, plus an exact fixed-point-free no-kernel case.

## What remains imported, declared, or open

- `FROZEN_PAIR_OBSERVED_FACTS = PROVED`
- `CHOSEN_PAIR_EQUIVALENCE = PROVED_POST_SEAL_CHOICE`
- `FROZEN_EXCHANGE_AUTHORIZATION = OPEN`
- `OPERATIONAL_NONTRIVIALITY = REFUTED_AS_FORCED_AND_IMPORTED_FOR_SIGN`
- `OCCURRENCE_HISTORY_FROM_RETAINED_TRACE = PROVED`
- `OCCURRENCE_HISTORY_FROM_ENDPOINT = REFUTED`
- `RETAINED_TRACE_CONNECTOR_INTEGRATION = OPEN`
- `COUNT_UNIT_CALIBRATION = REFUTED_AS_FORCED_AND_IMPORTED_FOR_INTEGER_OUTPUT`
- `POLARITY_INTEGER_CALIBRATION = DECLARED_INPUT`
- `MIXING_MAP = DECLARED_INPUT`
- `ACTUAL_SECTION_ADAPTER_TYPE = PROVED_CONDITIONAL`
- `ACTUAL_SECTION_ADAPTER_FIELDS = OPEN`
- `END_TO_END_CONNECTOR = OPEN`

The declared occurrence model now has an exact producer from a retained frozen
event trace. That removes a separate occurrence-history input only after the
downstream connector accepts that trace. The other forcing claims are either
refuted or remain explicit inputs.

## Verification record

The deterministic records under `receipts/` bind the source manifest,
connector payload, Lean source hashes, promoted-theorem axiom reports, command
exit codes, and tool versions. The final machine receipt is authoritative for
which commands ran successfully in the same replay.

`receipts/frozen_compatibility.json` additionally binds every selected local
bridge source, the complete expected declaration census, the exact frozen
commit/tree and pinned blobs, and the absence of persistent exact frozen
source copies. Identical `lean-toolchain` text is listed separately as
metatheoretic apparatus.

## Source pin change (2026-09-21)

By the author's ruling on 2026-09-21, `CLAUDE.md` is no longer a pinned
source. It had been pinned as a `base` source, so `source_manifest.py
--check` required its blob at HEAD to equal the blob at the fixed base
`be7476868e496e06d5dec6599fa4346394c512bd`. The file changed on
2026-09-08, so the check had failed since then with `base source changed
at HEAD: CLAUDE.md`, and no regeneration could repair it. Nothing in this
tree computes from `CLAUDE.md`. The manifest now pins eight sources, all
at the frozen tag. The frozen identities, the base and publication-base
ancestry checks, and every other pin are unchanged. The machine receipt was
regenerated with `build_receipt.py --write`, and every command in it passed.
