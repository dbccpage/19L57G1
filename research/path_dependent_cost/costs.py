"""The candidate costs, each declared with the reading that motivates it.

`FW-TUNED` binds this file: every candidate below is written down with its
native reading **before** its circulation is computed, and one that turns
out to be exact is reported as exact rather than quietly dropped.  Three of
the eight are here precisely because they are expected to telescope; a
search that only lists the answers is not a search.

Every candidate is a weighting of single-item moves.  By the
characterisation proved in `lean/PathDependentCost/Cochain.lean` that is not
a restriction: an additive cost IS such a weighting, extended by summation,
so this file ranges over the whole space of additive costs that anyone
could have proposed.

AuthorityEffect: None.
"""

from __future__ import annotations

import pathlib
import sys
from collections.abc import Callable

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
_CODE = str(REPO / "code")
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)

from derivation.candidates import (  # noqa: E402
    Item,
    NewDatum,
    NewForm,
    NewInst,
    NewRuleAll,
    apply_delta,
)
from derivation.model import Regime  # noqa: E402
from derivation.observe import contexts, profiles  # noqa: E402

Weight = Callable[[Regime, Item], int]

__all__ = ["CANDIDATES", "READINGS", "Weight"]


def _after(base: Regime, it: Item) -> Regime:
    return apply_delta(base, (it,))


def profile_size(r: Regime) -> int:
    """Total observable content: derivable pluggings, summed over the data.

    Restated from the sealed `profiles`, not imported from a sibling: the
    two trees that declared it are unmerged.  `SOURCE_MANIFEST.json` says
    so."""

    return sum(len(p) for p in profiles(r))


# --------------------------------------------------------------------------
# The candidates
# --------------------------------------------------------------------------


def reach(base: Regime, it: Item) -> int:
    """Pluggings the move makes newly derivable."""

    return profile_size(_after(base, it)) - profile_size(base)


def context_opening(base: Regime, it: Item) -> int:
    """Contexts the move newly opens, derivable or not."""

    return len(contexts(_after(base, it))) - len(contexts(base))


def item_count(base: Regime, it: Item) -> int:
    """The sealed count: one per item, whatever it does."""

    return 1


def redundancy(base: Regime, it: Item) -> int:
    """One when the move leaves the state exactly as it found it."""

    return 1 if _after(base, it) == base else 0


def empty_admission(base: Regime, it: Item) -> int:
    """One when the move changes the state but not what is derivable.

    Distinct from `redundancy`: admitting an instance whose form already
    carries a uniform rule enlarges the record and adds no observable
    content."""

    after = _after(base, it)
    if after == base:
        return 0
    return 1 if profile_size(after) == profile_size(base) else 0


def arity_debt(base: Regime, it: Item) -> int:
    """A form costs its arity; everything else is free.  Base-free, listed
    to check that base-freeness and exactness are different properties."""

    return it.arity if isinstance(it, NewForm) else 0


def width_at_admission(base: Regime, it: Item) -> int:
    """A form costs the number of data standing when it is declared; a
    datum costs nothing.

    The reading: a form is an obligation over everything present and a datum
    is not an obligation at all, so the two are not symmetric.  A cost that
    prices them symmetrically is the one making an assumption."""

    return base.n_data() if isinstance(it, NewForm) else 0


def rule_span(base: Regime, it: Item) -> int:
    """A uniform rule costs the number of pluggings of its form at the
    moment it is admitted; every other move is free.

    The reading, and the one this tree was written for: a rule is a
    commitment over **all** pluggings of its form.  How far that commitment
    reaches is not a property of the rule -- it is a property of the state
    the rule is made in.  Commit early and the commitment is narrow; commit
    late and the same commitment ranges over everything that arrived
    meanwhile."""

    if not isinstance(it, NewRuleAll):
        return 0
    arity: int = base.forms[it.form]
    return int(base.n_data() ** arity)


def mention_deficit(base: Regime, it: Item) -> int:
    """An instance costs the number of standing data it does NOT mention.

    The reading: an instance that ignores most of the state is a narrower
    act than one that touches it, and the price should say so."""

    if not isinstance(it, NewInst):
        return 0
    return base.n_data() - len(set(it.args))


CANDIDATES: dict[str, Weight] = {
    "arity_debt": arity_debt,
    "context_opening": context_opening,
    "empty_admission": empty_admission,
    "item_count": item_count,
    "mention_deficit": mention_deficit,
    "reach": reach,
    "redundancy": redundancy,
    "rule_span": rule_span,
    "width_at_admission": width_at_admission,
}

READINGS: dict[str, str] = {
    "arity_debt": "a form costs its arity; base-free, listed to separate base-freeness from exactness",
    "context_opening": "contexts newly opened, derivable or not",
    "empty_admission": "one when the record grows and the observable content does not",
    "item_count": "the sealed count, one per item",
    "mention_deficit": "an instance costs the standing data it does not mention",
    "reach": "pluggings newly made derivable",
    "redundancy": "one when the move leaves the state as it found it",
    "rule_span": "a commitment costs what it ranges over at the moment it is made",
    "width_at_admission": "a form costs the state it must range over; a datum is not an obligation",
}

assert set(CANDIDATES) == set(READINGS)


def reads_the_base(name: str, samples: list[tuple[Regime, Item]]) -> bool:
    """Whether the candidate ever gives one item two prices.

    Decided against the supplied moves, never asserted: `width_at_admission`
    and `rule_span` are base-relative by construction, but `item_count` is
    not, and the table should say which is which from evidence."""

    weight = CANDIDATES[name]
    by_item: dict[Item, set[int]] = {}
    for base, it in samples:
        by_item.setdefault(it, set()).add(weight(base, it))
    return any(len(v) > 1 for v in by_item.values())
