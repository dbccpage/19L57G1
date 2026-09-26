"""Continuation one: the declared engine class and its capability census.

Classification (assumption discipline):

* Everything here is metatheory apparatus layered on the sealed kernel,
  rung two's rule class (``research/second_stake/rules.py``), its
  observables and its dynamic no-regress validity and minimum responses
  (``generation.py``), rung one's no-op filter and delta order
  (``research/second_stream/stream.py``) and the two-sided tree's honour
  relation (``research/two_sided_commitment/two_sided.py``), all imported
  read-only through their public functions and pinned by blob in
  ``SOURCE_MANIFEST.json``.  No sibling source is copied.
* An ENGINE is a DECLARATION of four parts, and this module declares the
  finite class of them that ``PROMPT.md`` names.  Its members are
  declarations, not results: that the class holds a member says nothing
  of what the member does.
* A CAPABILITY is one named element of a declaration, from the list in
  ``PROMPT.md``.  The count of an engine is a count of its declaration.
* A DEMAND is read off the state by the generator; no event emits it.
  A RESPONSE is a model proposal until the admission events of its delta
  are replayed, which the probe (``engine_probe.py``) does.
* The two modes read one stake rule: in flipped mode apart and same are
  exchanged and free is kept.  The flipped rule is built from rung two's
  public rule, never by editing it.
* Nothing here is a theorem.  The theorems of this tree are in ``lean/``.
"""

from __future__ import annotations

import pathlib
import sys
from dataclasses import dataclass
from typing import Literal, Optional, Sequence, Union, cast

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
_SIBLINGS = [
    str(REPO / "research" / "second_stake"),
    str(REPO / "research" / "second_stream"),
    str(REPO / "code"),
]
sys.path[:] = _SIBLINGS + [entry for entry in sys.path if entry not in _SIBLINGS]

# Rung two's and rung one's modules put the sealed kernel and three sibling
# trees on the path.  Those trees carry modules named `verify_pins`,
# `check_coverage` and `test_*`, so this tree goes back to the front AFTER
# the imports, or a sibling's module is silently loaded in place of this
# tree's -- the defect rung three found live and later rungs recorded.
from rules import (  # noqa: E402
    APART,
    FREE,
    MENU,
    SAME,
    Label,
    StakeRule,
    demands as stake_demands,
    honoured_labelled_pairs,
    label_of,
)
from generation import response_valid as rung_two_response_valid  # noqa: E402
from stream import delta_order_key, has_noop_item  # noqa: E402
from two_sided import honoured  # noqa: E402
from derivation.candidates import (  # noqa: E402
    Bounds,
    Delta,
    apply_delta,
    delta_events,
    iter_full_deltas,
    mu2,
)
from derivation.model import (  # noqa: E402
    AdmitDatum,
    Event,
    Pair,
    Regime,
    Supply,
    replay,
)

sys.path[:] = [str(HERE)] + [entry for entry in sys.path if entry != str(HERE)]

__all__ = [
    "BOUNDS",
    "BundleRefused",
    "CONTINUATIONS",
    "EState",
    "Engine",
    "EngineEvent",
    "FLIPPED",
    "MAX_DATA",
    "MEASURES",
    "Minima",
    "PLAIN",
    "RULE_NAMES",
    "SKELETON",
    "SwitchMarker",
    "Target",
    "VALIDITY",
    "check_declaration_label",
    "count_minimal",
    "engine_class",
    "engine_named",
    "engine_replay",
    "growth_events",
    "honoured_before",
    "inclusion_minimal",
    "initial_members",
    "input_tally",
    "introduced_clause",
    "least_responses",
    "literal_class",
    "moded_rule",
    "response_events",
    "shared_capability_pairs",
    "state_demands",
]

# ---------------------------------------------------------------------------
# Declared bounds and names
# ---------------------------------------------------------------------------

BOUNDS = Bounds(max_items=2, max_arity=2)
MAX_DATA = 4
MEASURES: tuple[str, ...] = ("mu1", "mu2")
VALIDITY: tuple[str, ...] = ("V1", "V2")
RULE_NAMES: tuple[str, ...] = tuple(rule.name for rule in MENU)
CONTINUATIONS: tuple[tuple[bool, bool], ...] = (
    (False, False),
    (True, False),
    (False, True),
    (True, True),
)
SKELETON: tuple[str, ...] = ("demand_read", "least_response", "replay")
PLAIN = "plain"
FLIPPED = "flipped"
Mode = Literal["plain", "flipped"]
Target = tuple[Label, Pair]


def _continuation_name(growth: bool, switch: bool) -> str:
    if growth and switch:
        return "growth+switch"
    if growth:
        return "growth"
    if switch:
        return "switch"
    return "halt"


# ---------------------------------------------------------------------------
# The declared class
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Engine:
    """One member of the declared class: a generator (one stake rule), a
    responder (one measure and one validity member), a continuation (a set
    of continuation rules) and the replay rule, which every member shares.
    """

    rule: str
    measure: str
    validity: str
    growth: bool
    switch: bool

    def __post_init__(self) -> None:
        if self.rule not in RULE_NAMES:
            raise ValueError(f"not a rule of the class: {self.rule!r}")
        if self.measure not in MEASURES:
            raise ValueError(f"not a measure of the class: {self.measure!r}")
        if self.validity not in VALIDITY:
            raise ValueError(f"not a validity member of the class: {self.validity!r}")

    @property
    def continuation(self) -> str:
        return _continuation_name(self.growth, self.switch)

    @property
    def name(self) -> str:
        return f"{self.rule}/{self.measure}/{self.validity}/{self.continuation}"

    @property
    def literal(self) -> bool:
        """A member of the seed-literal subclass: at least one rule."""
        return self.growth or self.switch

    def stake(self) -> StakeRule:
        return moded_rule(self.rule, PLAIN)

    def capabilities(self) -> tuple[str, ...]:
        """The capability set of the declaration, sorted."""
        caps: set[str] = set(SKELETON)
        caps.update(self.stake().observables)
        caps.add(self.measure)
        caps.add("no_regress")
        if self.validity == "V2":
            caps.add("introduced_honoured")
        if self.growth:
            caps.add("growth")
        if self.switch:
            caps.add("switch")
        return tuple(sorted(caps))

    def count(self, growth_weight: int = 1) -> int:
        """The capability count; ``growth_weight`` two is the second
        declared reading, growth counted as a trigger and an admission."""
        if growth_weight not in (1, 2):
            raise ValueError(f"growth is read as one or two, not {growth_weight}")
        extra = growth_weight - 1 if self.growth else 0
        return len(self.capabilities()) + extra


def engine_class() -> tuple[Engine, ...]:
    """Every member, in a fixed order: rule, measure, validity, then the
    continuation subsets in the order HALT, growth, switch, both."""
    return tuple(
        Engine(rule, measure, validity, growth, switch)
        for rule in RULE_NAMES
        for measure in MEASURES
        for validity in VALIDITY
        for growth, switch in CONTINUATIONS
    )


def literal_class() -> tuple[Engine, ...]:
    return tuple(engine for engine in engine_class() if engine.literal)


def engine_named(name: str) -> Engine:
    for engine in engine_class():
        if engine.name == name:
            return engine
    raise KeyError(name)


def count_minimal(members: Sequence[Engine], growth_weight: int = 1) -> tuple[Engine, ...]:
    """Every member of least count, every tie retained."""
    if not members:
        return ()
    least = min(engine.count(growth_weight) for engine in members)
    return tuple(engine for engine in members if engine.count(growth_weight) == least)


def inclusion_minimal(members: Sequence[Engine]) -> tuple[Engine, ...]:
    """Every member no other member's capability set lies strictly inside."""
    sets = [(engine, frozenset(engine.capabilities())) for engine in members]
    return tuple(
        engine
        for engine, caps in sets
        if not any(other < caps for _, other in sets)
    )


def initial_members(members: Sequence[Engine]) -> tuple[Engine, ...]:
    """Every member whose capability set lies inside every member's: the
    initial members under the declared morphisms, inclusions of
    declarations."""
    sets = [(engine, frozenset(engine.capabilities())) for engine in members]
    return tuple(
        engine for engine, caps in sets if all(caps <= other for _, other in sets)
    )


def shared_capability_pairs(members: Sequence[Engine]) -> tuple[tuple[str, str], ...]:
    """Every unordered pair of distinct members with one capability set."""
    out: list[tuple[str, str]] = []
    for index, left in enumerate(members):
        for right in members[index + 1 :]:
            if left.capabilities() == right.capabilities():
                out.append((left.name, right.name))
    return tuple(out)


class BundleRefused(ValueError):
    """A label calls an engine one declaration while it declares several."""


def check_declaration_label(engine: Engine, claimed: int) -> None:
    """Refuse any label that gives an engine fewer capabilities than its
    declaration holds -- in particular any label calling it one
    declaration.  The refusal names the engine and every capability."""
    actual = engine.count()
    if claimed < actual:
        raise BundleRefused(
            f"{engine.name} is called {claimed} declaration(s) but declares "
            f"{actual} capabilities: {', '.join(engine.capabilities())}"
        )


def input_tally(engine: Engine) -> dict[str, bool]:
    """Which of the seed's two named inputs the declaration carries."""
    return {"stake": True, "stream": engine.growth}


# ---------------------------------------------------------------------------
# The generator: one stake rule read in the state's mode
# ---------------------------------------------------------------------------


def _flip(label: Label) -> Label:
    if label == APART:
        return cast(Label, SAME)
    if label == SAME:
        return cast(Label, APART)
    return label


_MODED: dict[tuple[str, str], StakeRule] = {}


def moded_rule(rule_name: str, mode: str) -> StakeRule:
    """Rung two's rule read in a mode.  The flipped rule is built once, from
    the public rule's labeller, so rung two's label cache sees one stable
    object per rule and mode."""
    key = (rule_name, mode)
    if key in _MODED:
        return _MODED[key]
    base = next((rule for rule in MENU if rule.name == rule_name), None)
    if base is None:
        raise KeyError(rule_name)
    if mode == PLAIN:
        _MODED[key] = base
        return base
    if mode != FLIPPED:
        raise ValueError(f"not a mode: {mode!r}")
    inner = base.labeler

    def flipped(regime: Regime, i: int, j: int) -> Label:
        return _flip(inner(regime, i, j))

    moded = StakeRule(f"{base.name}~", base.observables, flipped, "menu")
    _MODED[key] = moded
    return moded


@dataclass(frozen=True)
class EState:
    """A sealed regime and a mode."""

    regime: Regime
    mode: str


@dataclass(frozen=True)
class SwitchMarker:
    """The engine's switch marker: flips the mode and changes nothing else.
    No requirement is retracted, because an engine imposes none."""


EngineEvent = Union[Event, SwitchMarker]


def engine_replay(history: Sequence[EngineEvent]) -> EState:
    """The engine's replay rule: the sealed replay over the sealed events,
    and the mode flipped once per switch marker."""
    sealed: list[Event] = []
    mode = PLAIN
    for event in history:
        if isinstance(event, SwitchMarker):
            mode = FLIPPED if mode == PLAIN else PLAIN
        else:
            sealed.append(event)
    return EState(replay(sealed), mode)


def state_demands(rule_name: str, state: EState) -> tuple[Target, ...]:
    """Every labelled pair not honoured, read in the state's mode, through
    rung two's public demand reading."""
    return stake_demands(state.regime, moded_rule(rule_name, state.mode))


def honoured_before(rule_name: str, state: EState) -> frozenset[Target]:
    return frozenset(honoured_labelled_pairs(state.regime, moded_rule(rule_name, state.mode)))


def growth_events(regime: Regime) -> tuple[Supply, AdmitDatum]:
    """The stream: the supply and admission of one fresh token."""
    stem = f"engine_g{regime.n_data()}"
    token = stem
    suffix = 0
    while token in regime.data:
        suffix += 1
        token = f"{stem}_{suffix}"
    return (Supply(token), AdmitDatum(token))


# ---------------------------------------------------------------------------
# The responder
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Minima:
    """The tied minima of one demand under one measure and one member."""

    measure: str
    validity: str
    item_count: int
    cost: tuple[int, ...]
    deltas: tuple[Delta, ...]


def introduced_clause(regime: Regime, rule: StakeRule, delta: Delta) -> bool:
    """The clause member two adds: every labelled pair involving a datum
    the delta introduces is honoured afterwards, its label read afterwards
    in the same mode."""
    after = apply_delta(regime, delta)
    for k in range(regime.n_data(), after.n_data()):
        for i in range(k):
            label = label_of(rule, after, i, k)
            if label != FREE and not honoured(after, label, (i, k)):
                return False
    return True


_VALID_MEMO: dict[tuple[Regime, str, str, Target, int], tuple[Delta, ...]] = {}


def _valid_at(
    regime: Regime,
    rule: StakeRule,
    target: Target,
    validity: str,
    item_count: int,
    memo: bool,
) -> tuple[Delta, ...]:
    key = (regime, rule.name, validity, target, item_count)
    if memo and key in _VALID_MEMO:
        return _VALID_MEMO[key]
    seen: set[Delta] = set()
    valid: list[Delta] = []
    for delta in iter_full_deltas(regime, item_count, BOUNDS):
        if delta in seen or has_noop_item(regime, delta):
            continue
        seen.add(delta)
        if not rung_two_response_valid(regime, rule, target, delta):
            continue
        if validity == "V2" and not introduced_clause(regime, rule, delta):
            continue
        valid.append(delta)
    out = tuple(sorted(valid, key=delta_order_key))
    if memo:
        _VALID_MEMO[key] = out
    return out


def least_responses(
    regime: Regime,
    rule: StakeRule,
    target: Target,
    validity: str,
    *,
    memo: bool = True,
) -> Optional[dict[str, Minima]]:
    """The minima under both measures, or ``None`` when the demand is
    refused within the sealed bounds.  The least item count with an
    accepted delta is found first; under ``mu2`` the least cost among its
    accepted deltas is then kept.  Every tie is retained."""
    if validity not in VALIDITY:
        raise ValueError(f"not a validity member: {validity!r}")
    for item_count in range(BOUNDS.max_items + 1):
        valid = _valid_at(regime, rule, target, validity, item_count, memo)
        if not valid:
            continue
        best = min(mu2(delta) for delta in valid)
        return {
            "mu1": Minima("mu1", validity, item_count, (item_count,), valid),
            "mu2": Minima(
                "mu2",
                validity,
                item_count,
                best,
                tuple(delta for delta in valid if mu2(delta) == best),
            ),
        }
    return None


def response_events(regime: Regime, delta: Delta) -> tuple[Event, ...]:
    return tuple(delta_events(regime, delta))
