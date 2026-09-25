"""The finite cross-check for rung four: the first-demand index up to the
implemented isomorphism.

Classification (assumption discipline):

* Everything here is metatheory apparatus layered on the sealed kernel,
  the sealed isomorphism procedure, the track-one sibling
  ``research/second_nofirst/nofirst.py`` and rung three's
  ``research/second_index/index.py``, all imported read-only through their
  public functions and pinned by blob in ``SOURCE_MANIFEST.json``.  No
  sibling source is copied.
* The rectangle, the three bases and the seven stakes are rung three's,
  consumed unchanged.  Nothing here declares an eighth stake.
* A CLASS is the set of regimes the sealed key procedure gives one key.
  The key procedure is cross-checked here, on every regime reached, against
  the sealed brute-force minimum over every bijection pair.
* A RENAMING of a class representative is a presentation of the class,
  formed by the sealed renaming helper.  It is NOT an admitted state: no
  event reaches it and nothing here replays it.  It is read only to ask
  whether carrying a demand is a property of the class.
* A TRAJECTORY of a sequence is the tuple of the classes of all its
  prefixes.  Two sequences with one trajectory are class-matched, in the
  sense the Lean of this rung defines.
* The enumeration is a FINITE COMPUTATION over a declared rectangle, run
  without any sealed pruning lemma.
* Nothing here is a theorem.  The theorems of this rung are in ``lean/``;
  this file checks their content by exhaustion on a rectangle and records
  the numbers the theorems do not give.
"""

from __future__ import annotations

import pathlib
import sys
from dataclasses import dataclass
from itertools import permutations
from typing import Any, Callable, Iterable, Mapping, Optional, Sequence

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
_INDEX_TREE = str(REPO / "research" / "second_index")
if _INDEX_TREE not in sys.path:
    sys.path.insert(0, _INDEX_TREE)

# Rung three's module puts the sealed kernel and the sibling trees on the
# path, and puts its OWN tree at the front.  Each of those trees carries
# modules named `verify_pins`, `check_coverage` and `test_*`.  So this
# tree goes back to the front AFTER the import, or a sibling's module is
# silently loaded in place of this rung's -- the defect rung three found
# live one level down, and recorded.
from index import (  # noqa: E402
    ALPHABET,
    BASE_NAMES,
    EMPTY_BASE,
    Alphabet,
    Observations,
    Rectangle,
    base_genesis,
    build_rectangle,
    declared_stakes,
    first_index_forward,
    history_descriptor,
    regime_shape,
    replay_check,
)
from nofirst import APART, FREE, SAME, Stake  # noqa: E402
from derivation.iso import (  # noqa: E402
    CanonKey,
    automorphisms,
    canonical,
    canonical_bruteforce,
    rename,
    serialize,
)
from derivation.model import (  # noqa: E402
    EMPTY,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Regime,
    Supply,
    replay,
    step,
)
from derivation.observe import profiles  # noqa: E402

if str(HERE) in sys.path:
    sys.path.remove(str(HERE))
sys.path.insert(0, str(HERE))

# The declared orbit bound: every bijection pair on at most five data and
# at most two forms.  Frozen in PREDICTIONS.md before the first run.
ORBIT_BOUND = 240

# The declared token renaming: the five fresh tokens in reverse order, and
# the supply token replaced by a sixth token no base carries.
RENAMED_SUPPLY_TOKEN = "<y>"


# ---------------------------------------------------------------------------
# Classes of regimes, two ways
# ---------------------------------------------------------------------------


class Keys:
    """Class keys of regimes, memoized.  Two procedures are kept apart:
    the sealed key procedure, which refines colours and searches only
    colour-preserving bijections, and the sealed brute-force minimum over
    every bijection pair.  Neither is derived from the other."""

    def __init__(self) -> None:
        self._fast: dict[Regime, CanonKey] = {}
        self._brute: dict[Regime, CanonKey] = {}

    def key(self, regime: Regime) -> CanonKey:
        found = self._fast.get(regime)
        if found is None:
            found = canonical(regime, ORBIT_BOUND)
            self._fast[regime] = found
        return found

    def brute(self, regime: Regime) -> CanonKey:
        found = self._brute.get(regime)
        if found is None:
            found = canonical_bruteforce(regime)
            self._brute[regime] = found
        return found


def partition(
    regimes: Iterable[Regime], key: Callable[[Regime], object]
) -> frozenset[frozenset[Regime]]:
    """The partition of a regime population by a key function."""
    groups: dict[object, set[Regime]] = {}
    for regime in regimes:
        groups.setdefault(key(regime), set()).add(regime)
    return frozenset(frozenset(group) for group in groups.values())


def partition_disagreements(
    regimes: Sequence[Regime], keys: Keys
) -> int:
    """The count of regimes whose class under the sealed key procedure
    differs from their class under the brute-force minimum.  Zero exactly
    when the two partitions coincide."""
    fast = {r: block for block in partition(regimes, keys.key) for r in block}
    brute = {r: block for block in partition(regimes, keys.brute) for r in block}
    return sum(1 for r in regimes if fast[r] != brute[r])


def brute_automorphism_count(regime: Regime) -> int:
    """Every bijection pair whose serialization equals the identity's.
    Written independently of the sealed ``automorphisms``, which searches
    only colour-preserving bijections."""
    n, m = regime.n_data(), len(regime.forms)
    identity = serialize(regime, tuple(range(n)), tuple(range(m)))
    return sum(
        1
        for pi in permutations(range(n))
        for phi in permutations(range(m))
        if serialize(regime, pi, phi) == identity
    )


def automorphism_report(regimes: Sequence[Regime]) -> dict[str, Any]:
    """The automorphism group's size at every regime, two ways."""
    disagreements = 0
    sizes: dict[str, int] = {}
    for regime in regimes:
        sealed = len(automorphisms(regime, ORBIT_BOUND))
        if sealed != brute_automorphism_count(regime):
            disagreements += 1
        sizes[str(sealed)] = sizes.get(str(sealed), 0) + 1
    values = sorted(int(size) for size in sizes)
    return {
        "disagreements": disagreements,
        "size_distribution": dict(sorted(sizes.items(), key=lambda kv: int(kv[0]))),
        "smallest": values[0],
        "largest": values[-1],
    }


# ---------------------------------------------------------------------------
# Carrying a demand, read a second way, for presentations of a class
# ---------------------------------------------------------------------------


def carries_from_profiles(stake: Stake, regime: Regime) -> bool:
    """PROCEDURE TWO for carrying a demand, written independently of the
    sibling's ``demands``: the profiles are computed once, and each held
    pair's label is read against their equality.  Used for the renamings
    of a class representative, where the sibling procedure would recompute
    the profiles once per stake; checked against the sibling procedure on
    every reached regime."""
    profs = profiles(regime)
    n = regime.n_data()
    for j in range(n):
        for i in range(j):
            label = stake.label(i, j)
            if label == FREE:
                continue
            equal = profs[i] == profs[j]
            if label == APART and equal:
                return True
            if label == SAME and not equal:
                return True
    return False


def statuses_from_profiles(
    stakes: Sequence[Stake], regime: Regime
) -> tuple[bool, ...]:
    """Procedure two for every stake at once, from one profile computation."""
    profs = profiles(regime)
    n = regime.n_data()
    out: list[bool] = []
    for stake in stakes:
        found = False
        for j in range(n):
            for i in range(j):
                label = stake.label(i, j)
                if label == FREE:
                    continue
                equal = profs[i] == profs[j]
                if (label == APART and equal) or (label == SAME and not equal):
                    found = True
                    break
            if found:
                break
        out.append(found)
    return tuple(out)


def orbit(regime: Regime) -> Iterable[Regime]:
    """Every renaming of a regime by a bijection pair on its datum and form
    indices, within the declared orbit bound."""
    n, m = regime.n_data(), len(regime.forms)
    count = 0
    for pi in permutations(range(n)):
        for phi in permutations(range(m)):
            count += 1
            if count > ORBIT_BOUND:
                raise ValueError(
                    f"orbit of a regime with {n} data and {m} forms exceeds"
                    f" the declared bound {ORBIT_BOUND}"
                )
            yield rename(regime, pi, phi)


# ---------------------------------------------------------------------------
# The measurements
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Population:
    """Every base's rectangle, the distinct regimes reached, and the class
    of each."""

    rects: tuple[Rectangle, ...]
    regimes: tuple[Regime, ...]
    keys: Keys

    def classes(self) -> dict[CanonKey, list[Regime]]:
        out: dict[CanonKey, list[Regime]] = {}
        for regime in self.regimes:
            out.setdefault(self.keys.key(regime), []).append(regime)
        return out


def regime_order(regime: Regime) -> tuple[object, ...]:
    """A deterministic total order on regimes that reads presentation
    tokens only to break ties, so that a chosen representative is
    reproducible; nothing is compared by it."""
    return (
        regime.n_data(),
        regime.forms,
        tuple(sorted(regime.insts)),
        tuple(sorted(regime.rules)),
        tuple(sorted(regime.reqs)),
        regime.data,
    )


def build_population(alphabet: Alphabet = ALPHABET) -> Population:
    rects = tuple(build_rectangle(base, alphabet) for base in BASE_NAMES)
    seen: set[Regime] = set()
    regimes: list[Regime] = []
    for rect in rects:
        for node in rect.nodes:
            if node.regime not in seen:
                seen.add(node.regime)
                regimes.append(node.regime)
    regimes.sort(key=regime_order)
    return Population(rects, tuple(regimes), Keys())


def first_reaching(population: Population) -> dict[Regime, tuple[str, tuple[str, ...]]]:
    """For each reached regime, the base and the least history descriptor
    reaching it: a replayable witness, chosen deterministically."""
    out: dict[Regime, tuple[str, tuple[str, ...]]] = {}
    for rect in population.rects:
        for node in rect.nodes:
            candidate = (rect.base, history_descriptor(node.history))
            prior = out.get(node.regime)
            if prior is None or candidate < prior:
                out[node.regime] = candidate
    return out


def class_split_report(
    population: Population, stakes: Sequence[Stake], seen: Observations
) -> dict[str, Any]:
    """Per stake: classes whose REACHED members carry a demand and carry
    none, and classes whose full orbit does.  Also the agreement of the two
    demand procedures on every reached regime, and whether every orbit
    contains the status of every reached member of its class."""
    classes = population.classes()
    witnesses = first_reaching(population)
    procedure_disagreements = 0
    reached: dict[str, int] = {s.name: 0 for s in stakes}
    orbital: dict[str, int] = {s.name: 0 for s in stakes}
    orbit_misses_reached = 0
    orbit_size_total = 0
    witness: dict[str, Optional[dict[str, object]]] = {s.name: None for s in stakes}
    for key in sorted(classes, key=lambda k: regime_order(min(classes[k], key=regime_order))):
        members = sorted(classes[key], key=regime_order)
        statuses: dict[Regime, tuple[bool, ...]] = {}
        for regime in members:
            first = tuple(seen.carries(s, regime) for s in stakes)
            second = statuses_from_profiles(stakes, regime)
            if first != second:
                procedure_disagreements += 1
            statuses[regime] = first
        orbit_statuses: set[tuple[bool, ...]] = set()
        for renamed in orbit(members[0]):
            orbit_size_total += 1
            orbit_statuses.add(statuses_from_profiles(stakes, renamed))
        if not set(statuses.values()) <= orbit_statuses:
            orbit_misses_reached += 1
        for index, stake in enumerate(stakes):
            values = {status[index] for status in statuses.values()}
            if len(values) == 2:
                reached[stake.name] += 1
                if witness[stake.name] is None:
                    carrying = next(r for r in members if statuses[r][index])
                    quiet = next(r for r in members if not statuses[r][index])
                    witness[stake.name] = {
                        "carrying": {
                            "base": witnesses[carrying][0],
                            "history": list(witnesses[carrying][1]),
                            "regime": regime_shape(carrying),
                        },
                        "quiet": {
                            "base": witnesses[quiet][0],
                            "history": list(witnesses[quiet][1]),
                            "regime": regime_shape(quiet),
                        },
                    }
            if len({status[index] for status in orbit_statuses}) == 2:
                orbital[stake.name] += 1
    return {
        "classes": len(classes),
        "classes_with_two_reached_members": sum(1 for v in classes.values() if len(v) > 1),
        "demand_procedure_disagreements": procedure_disagreements,
        "orbit_misses_reached_status": orbit_misses_reached,
        "orbit_presentations_formed": orbit_size_total,
        "reached_split_classes": reached,
        "orbit_split_classes": orbital,
        "reached_split_witness": witness,
    }


def trajectories(
    population: Population,
) -> list[tuple[str, tuple[Event, ...], tuple[CanonKey, ...]]]:
    """Every sequence of every base with its trajectory: the classes of all
    its prefixes, the count zero included."""
    out: list[tuple[str, tuple[Event, ...], tuple[CanonKey, ...]]] = []
    for rect in population.rects:
        traj: dict[tuple[Event, ...], tuple[CanonKey, ...]] = {}
        for node in sorted(rect.nodes, key=lambda n: len(n.history)):
            parent = traj.get(node.history[:-1], ()) if node.history else ()
            traj[node.history] = parent + (population.keys.key(node.regime),)
            out.append((rect.base, node.history, traj[node.history]))
    return out


def index_table(
    population: Population, stakes: Sequence[Stake], seen: Observations
) -> dict[tuple[str, tuple[Event, ...]], tuple[Optional[int], ...]]:
    """The first count of every sequence under every stake, by rung three's
    forward procedure."""
    out: dict[tuple[str, tuple[Event, ...]], tuple[Optional[int], ...]] = {}
    for rect in population.rects:
        for node in rect.nodes:
            out[(rect.base, node.history)] = tuple(
                first_index_forward(rect.regime, node.history, s, seen) for s in stakes
            )
    return out


def varying_classes(
    groups: Sequence[list[tuple[Optional[int], ...]]],
    stakes: Sequence[Stake],
    *,
    ignore_absent: bool,
) -> dict[str, int]:
    """Per stake, the count of groups on which the first count varies.
    With ``ignore_absent``, a sequence with no first count is left out, so
    only two different numbers count as variation."""
    out: dict[str, int] = {}
    for index, stake in enumerate(stakes):
        count = 0
        for rows in groups:
            values = {row[index] for row in rows}
            if ignore_absent:
                values.discard(None)
            if len(values) > 1:
                count += 1
        out[stake.name] = count
    return out


def trajectory_report(
    population: Population,
    table: Mapping[tuple[str, tuple[Event, ...]], tuple[Optional[int], ...]],
    stakes: Sequence[Stake],
) -> dict[str, Any]:
    """The sequences quotiented by their trajectory, and by the class of the
    regime the whole sequence reaches."""
    by_trajectory: dict[tuple[CanonKey, ...], list[tuple[Optional[int], ...]]] = {}
    by_final: dict[CanonKey, list[tuple[Optional[int], ...]]] = {}
    for base, history, traj in trajectories(population):
        row = table[(base, history)]
        by_trajectory.setdefault(traj, []).append(row)
        by_final.setdefault(traj[-1], []).append(row)
    return {
        "sequences": sum(len(v) for v in by_trajectory.values()),
        "trajectory_classes": len(by_trajectory),
        "trajectory_classes_with_two_members": sum(
            1 for v in by_trajectory.values() if len(v) > 1
        ),
        "largest_trajectory_class": max(len(v) for v in by_trajectory.values()),
        "trajectory_classes_with_varying_count": varying_classes(
            list(by_trajectory.values()), stakes, ignore_absent=False
        ),
        "final_classes": len(by_final),
        "final_classes_with_two_counts": varying_classes(
            list(by_final.values()), stakes, ignore_absent=True
        ),
    }


def renamed_token(token: str, alphabet: Alphabet) -> str:
    """The declared token renaming: the fresh tokens reversed, the supply
    token replaced, every other token left alone."""
    fresh = alphabet.fresh_tokens
    if token in fresh:
        return fresh[len(fresh) - 1 - fresh.index(token)]
    if token == alphabet.supply_token:
        return RENAMED_SUPPLY_TOKEN
    return token


def rename_history(history: Sequence[Event], alphabet: Alphabet) -> tuple[Event, ...]:
    out: list[Event] = []
    for event in history:
        if isinstance(event, Supply):
            out.append(Supply(renamed_token(event.token, alphabet)))
        elif isinstance(event, AdmitDatum):
            out.append(AdmitDatum(renamed_token(event.token, alphabet)))
        else:
            out.append(event)
    return tuple(out)


def token_report(
    population: Population,
    table: Mapping[tuple[str, tuple[Event, ...]], tuple[Optional[int], ...]],
    stakes: Sequence[Stake],
    seen: Observations,
    alphabet: Alphabet = ALPHABET,
) -> dict[str, Any]:
    """Replay every sequence with its tokens renamed; compare first counts
    and the class of every prefix."""
    moved_counts = 0
    moved_classes = 0
    changed_presentations = 0
    for rect in population.rects:
        genesis = base_genesis(rect.base)
        for node in rect.nodes:
            renamed = rename_history(node.history, alphabet)
            regime = rect.regime
            renamed_regime = rect.regime
            for original_event, renamed_event in zip(node.history, renamed):
                regime = step(regime, original_event)
                renamed_regime = step(renamed_regime, renamed_event)
                if population.keys.key(regime) != population.keys.key(renamed_regime):
                    moved_classes += 1
                    break
            if replay(genesis + renamed, EMPTY) != renamed_regime:
                raise RuntimeError("a renamed sequence does not replay from genesis")
            if renamed_regime != node.regime:
                changed_presentations += 1
            counts = tuple(
                first_index_forward(rect.regime, renamed, s, seen) for s in stakes
            )
            if counts != table[(rect.base, node.history)]:
                moved_counts += 1
    return {
        "renamed_supply_token": RENAMED_SUPPLY_TOKEN,
        "fresh_tokens_reversed": True,
        "sequences_with_a_moved_count": moved_counts,
        "sequences_with_a_moved_class": moved_classes,
        "sequences_whose_presentation_changed": changed_presentations,
    }


# ---------------------------------------------------------------------------
# The exhibited class-matched histories, replayed in Python
# ---------------------------------------------------------------------------

_FRESH = ALPHABET.fresh_tokens


def exhibited_histories() -> dict[str, tuple[Event, ...]]:
    """The four histories the Lean countermodels name, with declared
    tokens.  The Lean datum admission carries no token; the tokens here
    are presentation only."""
    prefix_p: tuple[Event, ...] = (
        AdmitForm(1),
        AdmitForm(1),
        AdmitDatum(_FRESH[0]),
        AdmitInst(0, (0,)),
        AdmitDatum(_FRESH[1]),
        AdmitInst(1, (1,)),
    )
    prefix_q: tuple[Event, ...] = (
        AdmitForm(1),
        AdmitForm(1),
        AdmitForm(1),
        AdmitDatum(_FRESH[0]),
        AdmitInst(0, (0,)),
        AdmitDatum(_FRESH[1]),
        AdmitInst(1, (1,)),
        AdmitDatum(_FRESH[2]),
        AdmitInst(2, (2,)),
    )
    return {
        "P1": prefix_p + (AdmitRuleAll(0), AdmitDatum(_FRESH[2])),
        "P2": prefix_p + (AdmitRuleAll(1), AdmitDatum(_FRESH[2])),
        "Q1": prefix_q + (AdmitRuleAll(0), AdmitDatum(_FRESH[3])),
        "Q2": prefix_q + (AdmitRuleAll(1), AdmitDatum(_FRESH[3])),
    }


def prefix_regimes(history: Sequence[Event]) -> list[Regime]:
    regimes = [EMPTY]
    for event in history:
        regimes.append(step(regimes[-1], event))
    return regimes


def stake_named(name: str) -> Stake:
    for stake in declared_stakes():
        if stake.name == name:
            return stake
    raise KeyError(name)


def exhibited_report(seen: Observations, keys: Keys) -> dict[str, Any]:
    """The exhibited pairs: length, data and forms, whether every prefix
    pair is in one class, and the first counts under the stakes each pair
    is for."""
    histories = exhibited_histories()
    out: dict[str, object] = {}
    for pair, stakes in (("P", ("parity", "chain")), ("Q", ("residue_three",))):
        one, two = histories[pair + "1"], histories[pair + "2"]
        first_regimes = prefix_regimes(one)
        second_regimes = prefix_regimes(two)
        split_prefixes = sum(
            1
            for a, b in zip(first_regimes, second_regimes)
            if keys.key(a) != keys.key(b)
        )
        final = first_regimes[-1]
        out[pair] = {
            "length": len(one),
            "data": final.n_data(),
            "forms": len(final.forms),
            "prefix_pairs_in_two_classes": split_prefixes,
            "first_counts": {
                name: {
                    pair + "1": first_index_forward(EMPTY, one, stake_named(name), seen),
                    pair + "2": first_index_forward(EMPTY, two, stake_named(name), seen),
                }
                for name in stakes
            },
        }
    return out


def all_reports(alphabet: Alphabet = ALPHABET) -> dict[str, Any]:
    """Everything this rung measures."""
    population = build_population(alphabet)
    stakes = declared_stakes()
    seen = Observations()
    table = index_table(population, stakes, seen)
    return {
        "bases": {
            rect.base: {
                "nodes": len(rect.nodes),
                "distinct_regimes": len({node.regime for node in rect.nodes}),
                "replay_mismatches": replay_check(rect),
            }
            for rect in population.rects
        },
        "distinct_regimes": len(population.regimes),
        "key_partition_disagreements": partition_disagreements(
            population.regimes, population.keys
        ),
        "automorphisms": automorphism_report(population.regimes),
        "class_split": class_split_report(population, stakes, seen),
        "trajectory": trajectory_report(population, table, stakes),
        "tokens": token_report(population, table, stakes, seen, alphabet),
        "exhibited": exhibited_report(seen, population.keys),
    }


__all__ = [
    "ALPHABET",
    "BASE_NAMES",
    "base_genesis",
    "declared_stakes",
    "first_index_forward",
    "EMPTY_BASE",
    "Keys",
    "ORBIT_BOUND",
    "Population",
    "RENAMED_SUPPLY_TOKEN",
    "all_reports",
    "automorphism_report",
    "brute_automorphism_count",
    "build_population",
    "carries_from_profiles",
    "class_split_report",
    "exhibited_histories",
    "exhibited_report",
    "first_reaching",
    "index_table",
    "orbit",
    "partition",
    "partition_disagreements",
    "prefix_regimes",
    "regime_order",
    "rename_history",
    "renamed_token",
    "stake_named",
    "statuses_from_profiles",
    "token_report",
    "trajectories",
    "trajectory_report",
    "varying_classes",
]
