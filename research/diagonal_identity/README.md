# Diagonal identity — covering-miss versus identifying-push

AuthorityEffect: None. Outside the sealed derivation; consumes it read-only.

## Question

Are `PrimDiff.obstruction_under_irrefl` and the covering theorems restated
from `research/unboundedness/lean/Continuum.lean` one obstruction, or two?

## Standing

**Dual shapes on declared carriers. Identity not proved.** Terminal:
`DUAL_NOT_IDENTITY_ON_DECLARED_CARRIERS`.

- Pair-id: `d2Const : Bool → Unit` is not injective; `Push D2 d2Const`
  violates `Irrefl`. This map is not a covering family (`Bool ≠ Nat`).
- Family-miss: no `S : Nat → (Nat → Fin c)` (`c ≥ 2`) is surjective. The
  missed row is `diagFlip` at `flipFin`. `S` is not the D2 constant map.

They are not instances of each other on those carriers. `diagFlip` packages
the covering side only. Identity of `obstruction_under_irrefl` with
`seq_uncountable` is not proved.

## Layout

| path | role |
|---|---|
| `lean/DiagonalIdentity/Covering.lean` | restated covering theorems; no `Metric` |
| `lean/DiagonalIdentity/Combinator.lean` | `diagFlip`; definitional equations |
| `lean/DiagonalIdentity/Collapse.lean` | `D2` collapsed to `Unit` |
| `lean/DiagonalIdentity/Split.lean` | inhabited conjunction, not an `Iff` of types |
| `lean/DiagonalIdentity/Dual.lean` | dual shapes; not-instance on declared carriers |
| `SOURCE_MANIFEST.json` | pins `PrimDiff`, `Limits.lean`, `Continuum.lean` |

Sealed staging copies `research/s9_obligations`: `verify_lean.py` writes
pinned blobs into `lean/sealed/` (gitignored). The lakefile has no `require`.

## Commands

```powershell
cd research/diagonal_identity
python -m unittest discover -s tests -p "test_*.py"
python verify_pins.py
python verify_lean.py
python run.py --check
```
