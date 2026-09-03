# closed_family — the native run charter

`AuthorityEffect: None.`

## What this rung was asked to do

Direct author instruction, 2026-09-03, in the operator channel: *close the
family under composition and prove `Sec` against it.*

The occasion was a reading of the estate against outside vocabulary, done
outside this repository. That reading found that the pinned `Family` of
`lean4/Derivation/PresentationNaturality.lean` declares of itself, in the
span pinned in `SOURCE_MANIFEST.json`:

> "Nothing is assumed about closure under composition or inverses; the
> family is exactly what it lists."

so a section natural for a declared family is natural for a *list* of
isomorphisms, while `PresIso` already carries `refl`, `symm`, and `trans`.
This rung builds the closure and measures what it costs a section.

## Write root and seal

Write root: `research/closed_family/` only. Sealed and frozen: `prompt/`,
`paper/`, `code/`, `lean4/Derivation/`, `artifacts/`, `CLAUDE.md`, `ci/`,
`.github/`, root `tests/`, `pyproject.toml`, `requirements.txt`, every
sibling research tree, and the census pin `ci/prose_watchlist.json`.

Snapshot: `f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be` of `main`. Every pull
request targets `main` directly; `CLAUDE.md` prohibits stacked pull
requests.

## Carrier

Reconstructed verbatim in `lean/ClosedFamily/Base.lean` from three pinned
sealed sources, in eight blocks, each bound to an exact source slice by
`SOURCE_MANIFEST.json` and checked by `verify_pins.py`:

- `DiffInterface`: `DiffObs`, `ZeroRel`, `zeroRel_equivalence`
- `ContactKernel`: `NonZeroPair`
- `PresentationNaturality`: `Bij` and its laws; `PresIso` and
  `zeroRel_transport`; `refl`/`symm`/`trans` with their component laws;
  `mapPair`; `Family`, `Sec`, `IsNatural`; the four bundle-coherence lemmas
  of its section 11

## Refusals in force

`FW-SEAL` no path outside the write root is written.
`FW-NAME` no outside theory, programme, or person name, in prose or in an
identifier. In particular: the construction below is a closure of a declared
family and is named that; no outside word for the resulting structure is
used anywhere in this tree.
`FW-SCOPE` the operation laws are proved on the transported bundle map, and
no sentence upgrades them to equalities of `PresIso` records.
`FW-SET` no statement about all families beyond what is quantified in Lean.
`FW-CHAIN` sealed statements are consumed by verbatim reconstruction under
pin, never by import.
`FW-PIN` the census pin is not regenerated; the write root carries no
watched prose word.

## Terminals, pre-agreed

`CLOSURE_BUILT`, `OBLIGATION_UNCHANGED`, `OBLIGATION_ENLARGED`,
`OPEN_AT_NAMED_TARGET`.

The second and third are the two branches of the substantive question and
both were agreed before the proof was attempted: closing might impose new
obligations on a section, or might impose none. This charter states which
one holds nowhere.
