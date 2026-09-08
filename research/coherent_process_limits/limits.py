"""Coherent finite observations of the represented process, and their limit.

AuthorityEffect: None.  Mirrors ``lean/Limits.lean`` (the abstract inverse
system) and ``lean/Observe.lean`` (the represented process at step scales).

The process observed is the merged control machine of
``research/represented_execution`` — its ``control.step_det`` — and the
artifact that family authored, ``evidence/process.json``.  This family reads
that artifact and never writes it.  The artifact's ``setting_json`` is the
sealed ``Setting.json``, which sorts the operation tables and so loses the
index order the enablements refer to; ``identify_programs`` recovers the
order as the unique one that reproduces every recorded run, and refuses if
none or several do.  That the schema is lossy is recorded as a finding for
the represented execution family.
"""

from __future__ import annotations

from itertools import permutations, product
import json
from pathlib import Path
from typing import Callable, Sequence, cast

import control as ct
import translation as tr

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
ARTIFACT = REPO / "research" / "represented_execution" / "evidence" / "process.json"
Word = tuple[int, ...]
JsonObj = dict[str, object]


class LimitsError(ValueError):
    """A named refusal."""


# ---------------------------------------------------------------------------
# The abstract inverse system on words (the Lean ``Limits``)
# ---------------------------------------------------------------------------


def bond(word: Word) -> Word:
    """Forget the last entry."""
    return word[:-1]


def compatible(family: Sequence[Word]) -> bool:
    """Compatibility at every stage listed: stage ``n`` has length ``n`` and
    is the bonding of stage ``n + 1``."""
    return all(len(family[n]) == n for n in range(len(family))) and all(
        bond(family[n + 1]) == family[n] for n in range(len(family) - 1))


def eventually_compatible(family: Sequence[Word], after: int) -> bool:
    return all(bond(family[n + 1]) == family[n] for n in range(after, len(family) - 1))


def of_seq(seq: Callable[[int], int], upto: int) -> tuple[Word, ...]:
    """The prefixes of a sequence: a compatible family."""
    return tuple(tuple(seq(i) for i in range(n)) for n in range(upto + 1))


def to_seq(family: Sequence[Word], i: int) -> int:
    """Read entry ``i`` at stage ``i + 1``."""
    return family[i + 1][i]


def eventual(upto: int) -> tuple[Word, ...]:
    """The Lean ``eventual``: constant 0 except at stage 1, where it reads 1."""
    return tuple((1,) if n == 1 else (0,) * n for n in range(upto + 1))


def even_family(family: Sequence[Word]) -> tuple[Word, ...]:
    """The even-scale subsystem of a family."""
    return tuple(family[2 * n] for n in range(len(family) // 2 + (1 if len(family) % 2 else 0)))


def shift_obs(word: Word, n: int) -> Word:
    """The shifted prefix: the first ``n`` entries after dropping one."""
    return word[1:][:n]


# ---------------------------------------------------------------------------
# The represented process at step scales (the Lean ``Observe``)
# ---------------------------------------------------------------------------


def next_state(s: ct.State) -> ct.State:
    """One step of the deterministic runner; a terminal keeps the state."""
    r = ct.step_det(s)
    return r if isinstance(r, ct.State) else s


def iterate(n: int, s: ct.State) -> ct.State:
    for _ in range(n):
        s = next_state(s)
    return s


def obs(n: int, s: ct.State) -> Word:
    """The observation at scale ``n``: the tape after ``n`` steps."""
    return iterate(n, s).tape


def is_prefix(a: Word, b: Word) -> bool:
    return len(a) <= len(b) and b[: len(a)] == a


# ---------------------------------------------------------------------------
# The artifact of the represented execution family
# ---------------------------------------------------------------------------


def load_artifact(path: Path = ARTIFACT) -> JsonObj:
    record = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        raise LimitsError("the artifact is not an object")
    if record.get("fragment") != "control":
        raise LimitsError(f"the artifact's fragment is {record.get('fragment')!r}, not 'control'")
    if "control_runs" not in record:
        raise LimitsError("the artifact records no controlled runs")
    return cast(JsonObj, record)


def setting_from_json(setting_json: JsonObj, order: Sequence[int]) -> tr.FiniteSetting:
    """A finite setting from the sealed ``Setting.json`` with the operation
    tables taken in the given order (the schema sorts them)."""
    tables = [tuple(int(v) for v in table) for table in cast(list[list[int]], setting_json["ops"])]
    pairs = cast(Callable[[str], frozenset[tuple[int, int]]],
                 lambda key: frozenset((int(p[0]), int(p[1]))
                                       for p in cast(list[list[int]], setting_json[key])))
    return tr.FiniteSetting(int(cast(int, setting_json["n"])), pairs("r"), pairs("ret"), pairs("prot"),
                            int(cast(int, setting_json["a"])), int(cast(int, setting_json["b"])),
                            tuple(tables[k] for k in order))


def identify_programs(record: JsonObj) -> tuple[dict[str, ct.Controlled], JsonObj]:
    """Recover the programs the artifact recorded: the operation order is the
    unique permutation of the sorted tables under which every recorded
    controlled run replays to its recorded tape and terminal.  Refuses when
    none or several orders do."""
    runs = cast(list[JsonObj], record["control_runs"])
    settings = {json.dumps(r["setting_json"], sort_keys=True) for r in runs}
    if len(settings) != 1:
        raise LimitsError("the recorded runs do not share one setting; identification is per setting only")
    setting_json = cast(JsonObj, runs[0]["setting_json"])
    count = len(cast(list[object], setting_json["ops"]))
    consistent: list[tuple[int, ...]] = []
    for order in permutations(range(count)):
        F = setting_from_json(setting_json, order)
        ok = True
        for r in runs:
            enablements = frozenset((int(p[0]), int(p[1])) for p in cast(list[list[int]], r["enablements"]))
            C = ct.Controlled(F, enablements)
            terminal, s = ct.trace(C, int(cast(int, r["start"])), int(cast(int, r["fuel"])))
            if list(s.tape) != r["tape"] or terminal.value != r["terminal"]:
                ok = False
                break
        if ok:
            consistent.append(order)
    if not consistent:
        raise LimitsError("no ordering of the recorded operation tables replays the recorded runs")
    if len(consistent) > 1:
        raise LimitsError(f"the recorded runs leave the operation order ambiguous: {consistent}")
    order = consistent[0]
    F = setting_from_json(setting_json, order)
    programs: dict[str, ct.Controlled] = {}
    for r in runs:
        name = str(r["program"])
        enablements = frozenset((int(p[0]), int(p[1])) for p in cast(list[list[int]], r["enablements"]))
        programs.setdefault(name, ct.Controlled(F, enablements))
    finding: JsonObj = {
        "schema_loses_operation_order": True,
        "recovered_order_of_sorted_tables": list(order),
        "identified_from_recorded_runs": len(runs),
    }
    return programs, finding


# ---------------------------------------------------------------------------
# The readout, the bound, and the connected experiment
# ---------------------------------------------------------------------------


def count_zero(tape: Word) -> int:
    return sum(1 for x in tape if x == 0)


def bound_holds(tape: Word) -> bool:
    """The bound derived at the coarse scale: with one visit of datum 0 per
    period of three, ``L <= 3 * count <= L + 2`` for a tape of length ``L``."""
    L, cnt = len(tape), count_zero(tape)
    return L <= 3 * cnt <= L + 2


SCALES: tuple[int, ...] = (3, 6, 12, 24)


def connected_experiment(forever: ct.Controlled, recorded_tape: Word) -> JsonObj:
    """Run the represented process at four step scales from datum 0; check
    that the observations are compatible (each a prefix of the next), that
    the artifact's own recorded tape is a prefix of every scale at least as
    fine, and that the bound derived at the coarsest scale holds at every
    finer one with the readout unchanged."""
    tapes = {F: ct.trace(forever, 0, F)[1].tape for F in SCALES}
    coarse = tapes[SCALES[0]]
    if not bound_holds(coarse):
        raise LimitsError("the bound does not hold at the coarse scale it was derived from")
    scales: list[JsonObj] = []
    for F in SCALES:
        tape = tapes[F]
        scales.append({
            "scale": F,
            "tape_length": len(tape),
            "count_zero": count_zero(tape),
            "three_count_minus_length": 3 * count_zero(tape) - len(tape),
            "bound_holds": bound_holds(tape),
            "prefix_of_next": F == SCALES[-1] or is_prefix(tape, tapes[SCALES[SCALES.index(F) + 1]]),
            "recorded_tape_is_prefix": is_prefix(recorded_tape, tape) if len(recorded_tape) <= len(tape)
            else is_prefix(tape, recorded_tape),
        })
    for entry in scales:
        if not entry["bound_holds"]:
            raise LimitsError(f"the bound fails at scale {entry['scale']}")
        if not entry["prefix_of_next"]:
            raise LimitsError(f"the observation at scale {entry['scale']} is not a prefix of the next")
        if not entry["recorded_tape_is_prefix"]:
            raise LimitsError(f"the artifact's recorded tape and the scale {entry['scale']} observation are not "
                              "prefix-related")
    return {
        "program": "forever",
        "start": 0,
        "readout": "the number of entries equal to datum 0 in the tape",
        "bound": "L <= 3 * count <= L + 2 for a tape of length L",
        "derived_at_scale": SCALES[0],
        "derived_from": list(coarse),
        "scales": scales,
        "limit": "the frequency count / L lies within 2 / (3 L) of 1 / 3 at every scale; the limiting value "
                 "1 / 3 is the rational the bound isolates, and precision e needs L >= 2 / (3 e)",
    }


# ---------------------------------------------------------------------------
# The three verdicts, and the failures
# ---------------------------------------------------------------------------


def deterministic_programs(F: tr.FiniteSetting) -> list[ct.Controlled]:
    """Every program on the setting with at most one operation enabled at
    each datum."""
    count = len(F.ops)
    out: list[ct.Controlled] = []
    for choice in product(range(-1, count), repeat=F.n):
        enablements = frozenset((x, k) for x, k in enumerate(choice) if k >= 0)
        out.append(ct.Controlled(F, enablements))
    return out


def realized_tapes(F: tr.FiniteSetting, fuel: int) -> set[Word]:
    return {ct.trace(C, x, fuel)[1].tape for C in deterministic_programs(F) for x in range(F.n)}


def functional(tape: Word) -> bool:
    """Equal entries have equal successors."""
    pairs = list(zip(tape, tape[1:]))
    return all(y == y2 for (x, y) in pairs for (x2, y2) in pairs if x == x2)


NOT_REALIZED: Word = (0, 1, 0, 2)


def verdicts(F: tr.FiniteSetting, fuel: int) -> JsonObj:
    tapes = realized_tapes(F, fuel)
    return {
        "class": "every program on the recorded setting with at most one operation enabled per datum, "
                 "from every datum",
        "programs": len(deterministic_programs(F)),
        "fuel": fuel,
        "realized_tapes": len(tapes),
        "injective": "the observation at the scale of a tape's length is the tape itself: injective on tapes",
        "all_realized_tapes_functional": all(functional(t) for t in tapes),
        "not_dense_witness": list(NOT_REALIZED),
        "witness_has_no_realized_extension": not any(is_prefix(NOT_REALIZED, t) for t in tapes),
        "surjective": False,
        "why_not_surjective": "a realized tape is functional (equal entries have equal successors, "
                              "Observe.next_active_det), so no thread with the prefix [0, 1, 0, 2] is "
                              "realized; the full thread space contains it",
    }


def lost_fuel(forever: ct.Controlled) -> JsonObj:
    s0, s1 = ct.init(forever, 0, 0), ct.init(forever, 0, 1)
    return {
        "same_tape": list(s0.tape) == list(s1.tape),
        "tape": list(s0.tape),
        "after_one_step_fuel_0": list(obs(1, s0)),
        "after_one_step_fuel_1": list(obs(1, s1)),
        "lost_information": "fuel",
        "repair": "observe the fuel beside the tape; with the program, the active datum and the fuel the "
                  "next observation is determined (Observe.next_active_det)",
    }


def shift_failure() -> JsonObj:
    a, b = (0, 1, 2), (0, 1, 0)
    return {
        "prefixes": [list(a[:2]), list(b[:2])],
        "shifted": [list(shift_obs(a, 2)), list(shift_obs(b, 2))],
        "meaning": "two words with one prefix of length 2 shift to different words: the entry beyond the "
                   "observed boundary would have to be supplied (Limits.shift_not_local)",
    }
