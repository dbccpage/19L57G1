# Diagonal identity — covering-miss versus identifying-push

AuthorityEffect: None. Outside the sealed derivation; consumes it read-only.

## Question

Are `PrimDiff.obstruction_under_irrefl` and the covering theorems restated
from `research/unboundedness/lean/Continuum.lean` one obstruction, or two?

## Standing

**Typed split recorded. Identity not proved.** Terminal:
`TYPED_SPLIT_RECORDED_IDENTITY_NOT_PROVED`.

Both families of facts hold. They do not share binders:

- identifying a witnessed pair along a map is `FidelityObstruction Irrefl`;
- a family `Nat → (Nat → Fin c)` misses a sequence obtained by square
  evaluation then a pointwise flip.

A combinator `diagFlip` packages the covering side only. A share-bridge that
would instantiate it at PrimDiff binders `(r, c)` is OPEN.

## Layout

| path | role |
|---|---|
| `lean/DiagonalIdentity/Covering.lean` | restated covering theorems; no `Metric` |
| `lean/DiagonalIdentity/Combinator.lean` | `diagFlip`; definitional equations |
| `lean/DiagonalIdentity/Collapse.lean` | `D2` collapsed to `Unit` |
| `lean/DiagonalIdentity/Split.lean` | inhabited conjunction, not an `Iff` of types |
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
