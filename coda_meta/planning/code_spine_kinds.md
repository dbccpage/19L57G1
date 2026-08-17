# code_spine_kinds — OES domain ontology (plan)

**AuthorityEffect:** None. Plan only. This is the required
ontology document for code / skills / tests before any
production spine extract on those surfaces. It does not
extract a spine, stand up an index, or write
AuthorityEffect.

Parent: `oes.md`. Paper kinds stay in `oes.md`. Do not reuse
them here.

Illustrations are drawn from the Residual monoid / typed-error
discipline already present on the product surface. They are
examples, not a claim that a file named `colored_operad.py`
exists in this vault.

## Conversion-quality analogue (gate, not a number we invent)

Before extract: named AST parser, two rates on a fixed
sample — (1) parse success, (2) public-name / test-name
retention. Threshold ~80 %, same rule as the paper
conversion gate in `oes.md`. Below threshold, refuse
extraction. No invented baseline.

## Allowed kinds

| Kind | What counts | Stable ID |
| --- | --- | --- |
| `FunctionSig` | Exported or publicly named function/method the source treats as a commitment | `module:qualname` or `module:qualname:sig-hash` |
| `TypeDecl` | Class, dataclass, TypedDict, named type later referenced | `module:ClassName` |
| `ErrorType` | Named exception with semantic weight | `module:ExceptionName` |
| `TestCase` | Named test that asserts a property or residual movement | test name + assertion text-hash |
| `Invariant` / `Property` | Assert, contract, or documented property treated as a claim | statement hash or named property |
| `ResidualCertificate` | Residual / cost / obligation already sealed in `domain/` | certificate id or content hash |
| `ConfigGauge` | Config or gauge that changes ambient behavior, treated as structural | key + value hash |
| `SkillCardClaim` | Explicit “this skill/agent can X” | skill-id + claim text-hash |
| `AuthorityEffectRecord` | Explicit AuthorityEffect annotation or sealed effect object | record id / content hash |
| `PR-Decision` | Rare. Named in `oes.md`. No example here. | not allocated |

Files, packages, and sections are containers via `appears_in`
/ containment. They are not primary vertices.

## Observational edges (script only)

- `references_by_name` — import or call of a stable name
- `shares_identifier` — exact token / skill-id / residual-id
  in local scope
- `appears_in` — unit in file / package / skill-bundle
- `sequential_in_source` — definition order; low weight
- `tested_by_link` — only when the test *literally* names the
  unit (string or AST name). Indirect calls do not license
  this edge

**Forbidden for any script** (human or sealed admit +
replayable witness): `implements`, `satisfies`,
`depends_for_correctness`, `repairs`, `dualizes`,
`authorized_by`, `fills_lock`.

## Worked miniature (extractor view)

Units a script may see on a Residual-style surface:

```
Residual                  ResidualCertificate   colored_operad:Residual
Residual.absorb           FunctionSig           colored_operad:Residual.absorb
Residual.discharge        FunctionSig           colored_operad:Residual.discharge
Residual.is_empty         FunctionSig           colored_operad:Residual.is_empty
ColorMismatch             ErrorType             colored_operad:ColorMismatch
ArityMismatch             ErrorType             colored_operad:ArityMismatch
compose                   FunctionSig           colored_operad:compose
```

Licensed edges: methods `references_by_name` Residual;
`compose` `shares_identifier` Residual; errors `appears_in`
the module; sequential edges among Residual methods (low
weight). No “compose implements the residual monoid” edge.

## Pre-declared lock (example, not live)

**L-Residual-1** (must exist *before* search): any composition
path that produces a non-empty Residual must call `discharge`
on every obligation or raise a typed error. Silent residual
loss is forbidden.

Candidate: a `compose` change that adds an explicit
`residual.discharge(...)` and shares observational structure
with the ResidualCertificate.

Jewel only when a replayable witness appears: the certificate
shows the residual became empty, or a typed error was raised.
That is machine-checkable residual movement. It must not reuse
the channel extractor that produced the candidate.

## Thin-spine diff (example)

```
v1: Residual, Residual.absorb, compose
v2: + Residual.discharge
    + observational edge  compose --references_by_name--> Residual.discharge
```

No semantic `repairs` / `implements` edge. The diff is an
op-read artifact, not a jewel.

## Op-read (example)

Query: which units nearly fill L-Residual-1 under licensed
ρ\* “insert explicit discharge call”?

Result: candidate = `compose` plus the new observational
edge. Jewel status is not granted until the residual-movement
witness is re-run. Never write AuthorityEffect.

A `SkillCardClaim` “can repair non-identity channels” is a
legitimate vertex. An observational edge to a
ResidualCertificate is allowed only if the skill card
literally names that residual. “This skill implements …”
stays human-admit + witness.

## Illustration (typed; not production code)

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Tuple, TypeAlias

@dataclass(frozen=True)
class Residual:
    """ResidualCertificate. absorb is associative; EMPTY is the unit."""

    obligations: Tuple[str, ...] = ()
    risk: float = 0.0

    def absorb(self, other: Residual) -> Residual:
        # FunctionSig: Residual.absorb
        if other.is_empty:
            return self
        if self.is_empty:
            return other
        return Residual(
            obligations=self.obligations + other.obligations,
            risk=max(self.risk, other.risk),
        )

    def discharge(self, obligation: str, evidence: str) -> Residual:
        # FunctionSig: Residual.discharge
        remaining: Tuple[str, ...] = tuple(
            o for o in self.obligations if o != obligation
        )
        if len(remaining) == len(self.obligations):
            return self
        return Residual(
            obligations=remaining + (f"discharged:{obligation}:{evidence}",),
            risk=0.0 if not remaining else self.risk,
        )

    @property
    def is_empty(self) -> bool:
        # FunctionSig: Residual.is_empty
        return not self.obligations and self.risk == 0.0


EMPTY: Residual = Residual()


class OperadError(Exception):
    """Base error — not usually a primary claim unit."""


class ArityMismatch(OperadError):
    # ErrorType: ArityMismatch
    def __init__(self, expected: int, got: int, context: str) -> None:
        super().__init__(
            f"Arity mismatch in {context}: expected {expected}, got {got}"
        )
        self.expected: int = expected
        self.got: int = got


class ColorMismatch(OperadError):
    # ErrorType: ColorMismatch
    def __init__(
        self,
        slot: int,
        expected: str,
        got: str,
        outer: str,
        inner: str,
    ) -> None:
        super().__init__(
            f"Color mismatch at slot {slot} of {outer!r}: "
            f"expected {expected!r}, got {got!r} from {inner!r}"
        )
        self.slot: int = slot
        self.expected: str = expected
        self.got: str = got
        self.outer: str = outer
        self.inner: str = inner


Color: TypeAlias = str
BodyFn: TypeAlias = Callable[[Tuple[Any, ...]], Tuple[Any, Residual]]


@dataclass(frozen=True)
class ColoredOp:
    name: str
    source_colors: Tuple[Color, ...]
    target_color: Color
    body: BodyFn = field(repr=False, compare=False)
    residual: Residual = EMPTY

    @property
    def arity(self) -> int:
        return len(self.source_colors)

    def compose(self, *args: ColoredOp) -> ColoredOp:
        # FunctionSig: ColoredOp.compose
        # Observational: shares_identifier Residual; references_by_name
        # Residual.absorb and ArityMismatch. No "implements monoid" edge.
        if len(args) != self.arity:
            raise ArityMismatch(self.arity, len(args), self.name)

        def new_body(values: Tuple[Any, ...]) -> Tuple[Any, Residual]:
            result, dynamic = self.body(values)
            total: Residual = self.residual.absorb(dynamic)
            return result, total

        return ColoredOp(
            name=f"compose({self.name})",
            source_colors=self.source_colors,
            target_color=self.target_color,
            body=new_body,
            residual=EMPTY,
        )


def test_residual_discharge_moves_cost() -> None:
    """TestCase. Literal names license tested_by_link."""
    r: Residual = Residual(obligations=("obligation-A",), risk=1.0)
    assert not r.is_empty
    r2: Residual = r.discharge("obligation-A", evidence="unit-test-proof")
    assert r2.is_empty
    assert "discharged:obligation-A:unit-test-proof" in r2.obligations


AUTHORITY_EFFECT: Optional[str] = None  # ConfigGauge; never auto-promoted


@dataclass(frozen=True)
class AuthorityEffectRecord:
    effect: Optional[str]
    provenance: str
    timestamp: str


def assert_no_silent_residual_loss(
    before: Residual,
    after: Residual,
    path: str,
) -> None:
    """Machine-checkable witness helper. Independent of the channel extractor."""
    if not before.is_empty and after.is_empty:
        return
    if not after.is_empty and "discharged:" not in str(after.obligations):
        raise AssertionError(
            f"silent residual loss on path {path}: {before} → {after}"
        )
```

`test_residual_discharge_moves_cost` may emit `tested_by_link`
to `Residual.discharge` and `Residual.is_empty` because it
literally contains those identifiers. Re-running it is
witness material for jewel status. It is not itself a jewel.

`AuthorityEffect: None.`
