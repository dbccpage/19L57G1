"""Admitted regimes, the four sealed admission events, and replay.

Classification: metatheory apparatus.

Re-implemented in this tree against the pinned sealed source
``code/derivation/model.py``.  This tree imports nothing across trees; the
re-implementation is asserted equal to the sealed original, on the whole
enumerated space, by ``tests/test_kernel_agreement.py``, which refuses to run
against unpinned sealed bytes.

State changes only through an admission event.  ``Supply`` is an external
presentation event and provably does not change the admitted state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Union

Args = tuple[int, ...]
Inst = tuple[int, Args]
Pair = tuple[int, int]


class AdmissionRefused(ValueError):
    """An event is ill-formed relative to the current regime."""


@dataclass(frozen=True)
class Regime:
    """Admitted state.

    ``data`` are presentation tokens in admission order; internal identity is
    the index.  ``forms`` maps a form index to its arity.  ``rules`` holds the
    forms carrying the uniform all-tuples rule.  ``reqs`` holds externally
    imposed persistent separation requirements.
    """

    data: tuple[str, ...]
    forms: tuple[int, ...]
    insts: frozenset[Inst]
    rules: frozenset[int]
    reqs: frozenset[Pair]

    def n_data(self) -> int:
        return len(self.data)


EMPTY = Regime((), (), frozenset(), frozenset(), frozenset())


@dataclass(frozen=True)
class Supply:
    """External presentation of a token.  Not an admission."""

    token: str


@dataclass(frozen=True)
class AdmitDatum:
    token: str


@dataclass(frozen=True)
class AdmitForm:
    arity: int


@dataclass(frozen=True)
class AdmitInst:
    form: int
    args: Args


@dataclass(frozen=True)
class AdmitRuleAll:
    form: int


@dataclass(frozen=True)
class Impose:
    """External requirement that ``i`` and ``j`` be internally separable."""

    i: int
    j: int


Event = Union[Supply, AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, Impose]


def step(r: Regime, e: Event) -> Regime:
    """Apply one event.  Deterministic; refuses ill-formed admissions."""
    if isinstance(e, Supply):
        return r
    if isinstance(e, AdmitDatum):
        if e.token in r.data:
            return r
        return Regime(r.data + (e.token,), r.forms, r.insts, r.rules, r.reqs)
    if isinstance(e, AdmitForm):
        if e.arity < 1:
            raise AdmissionRefused(f"form arity must be >= 1, got {e.arity}")
        return Regime(r.data, r.forms + (e.arity,), r.insts, r.rules, r.reqs)
    if isinstance(e, AdmitInst):
        if not 0 <= e.form < len(r.forms):
            raise AdmissionRefused(f"unknown form {e.form}")
        if len(e.args) != r.forms[e.form]:
            raise AdmissionRefused(
                f"form {e.form} has arity {r.forms[e.form]}, "
                f"got {len(e.args)} arguments"
            )
        if not all(0 <= a < len(r.data) for a in e.args):
            raise AdmissionRefused(f"instance arguments out of range: {e.args}")
        return Regime(
            r.data, r.forms, r.insts | {(e.form, e.args)}, r.rules, r.reqs
        )
    if isinstance(e, AdmitRuleAll):
        if not 0 <= e.form < len(r.forms):
            raise AdmissionRefused(f"unknown form {e.form}")
        return Regime(r.data, r.forms, r.insts, r.rules | {e.form}, r.reqs)
    if not 0 <= e.i < e.j < len(r.data):
        raise AdmissionRefused(f"requirement out of range: ({e.i}, {e.j})")
    return Regime(r.data, r.forms, r.insts, r.rules, r.reqs | {(e.i, e.j)})


def replay(history: Sequence[Event], base: Regime = EMPTY) -> Regime:
    """Replay a history from ``base``.  Every certified state equals the
    replay of its recorded history."""
    r = base
    for e in history:
        r = step(r, e)
    return r


# The two sealed genesis histories, transcribed from the pinned
# ``code/derivation/engine.py``.  Reading L retains only what is explicitly
# retained; reading F admits the initial inscription at genesis.
GENESIS_L: tuple[Event, ...] = (
    Supply("<>"),
    Supply("<a>"),
    Supply("<a>"),
    Supply("<ab>"),
    AdmitDatum("<a>"),
    AdmitDatum("<ab>"),
)
GENESIS_F: tuple[Event, ...] = (
    Supply("<>"),
    AdmitDatum("<>"),
    Supply("<a>"),
    Supply("<a>"),
    Supply("<ab>"),
    AdmitDatum("<a>"),
    AdmitDatum("<ab>"),
)
READING_TARGET: dict[str, Pair] = {"L": (0, 1), "F": (1, 2)}


def genesis(reading: str) -> Regime:
    """The sealed Challenge-3 base of a reading."""
    if reading == "L":
        return replay(GENESIS_L)
    if reading == "F":
        return replay(GENESIS_F)
    raise ValueError(f"unknown reading: {reading}")
