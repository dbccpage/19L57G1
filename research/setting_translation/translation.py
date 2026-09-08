"""A finite setting as a regime of the sealed grammar: the translation, its
faithfulness census over the sealed universe of settings, and the sealed
engine restarted from encoded settings.

AuthorityEffect: None.  Nothing here is a new primitive.  Every encoding is
the sealed ``replay`` of an admission history; every derivability question
is the sealed ``derivable``; every separability verdict cross-checked here is
the sealed ``separable``; every restart is the sealed ``build_tree`` certified
by the sealed ``verify_full_export``.

The module mirrors ``lean/Translation.lean``, ``lean/Chains.lean`` and
``lean/Visible.lean``:

* ``FiniteSetting`` / ``events`` / ``encode`` — the carrier as data, one
  binary form per store (0 the difference relation, 1 retention, 2
  protection) and per admitted operation (its graph on form ``3 + k``),
  no rule, no standing requirement.
* ``readings`` — the nine candidate readings decided on the **encoded**
  regime exactly as the Lean transports state them (``W_iff`` … ``F_iff``,
  ``E_iff_noChain``); ``no_chain`` is the bounded word criterion and
  ``no_chain_reach`` its product-state cross-check.
* ``visible`` — the Lean ``Visible`` criterion for binary regimes: some
  form's self-instance, row or column differs at the two data.
* ``restart`` — the sealed engine from an encoded setting, the designated
  pair as the seed target.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterator, Sequence, cast

from derivation import primitive_core as sealed
from derivation.candidates import Bounds
from derivation.engine import Reading, build_tree
from derivation.export import Json, delta_json, dumps_deterministic, regime_sha256, tree_full_json, verify_full_export
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, Event, Regime, certify, replay
from derivation.observe import collapsed_pairs, derivable, separable
import hashlib

JsonDict = dict[str, Json]
Pair = tuple[int, int]
Rel = frozenset[Pair]
Table = tuple[int, ...]
READINGS: tuple[str, ...] = ("W", "A", "Bs", "Bc", "Bl", "C", "D", "E", "F")


class TranslationError(ValueError):
    """A named failure of the translation or of a check against it."""


# ---------------------------------------------------------------------------
# Finite settings and their encoding
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FiniteSetting:
    """The Lean ``FiniteSetting``: carrier ``range(n)``, three stores as pair
    sets, two endpoints, operations as value tables closed on the carrier."""

    n: int
    rel: Rel
    ret: Rel
    prot: Rel
    a: int
    b: int
    ops: tuple[Table, ...]

    def __post_init__(self) -> None:
        if self.n < 1:
            raise TranslationError("the carrier is empty")
        if not (0 <= self.a < self.n and 0 <= self.b < self.n):
            raise TranslationError("an endpoint lies outside the carrier")
        for store in (self.rel, self.ret, self.prot):
            if any(not (0 <= x < self.n and 0 <= y < self.n) for x, y in store):
                raise TranslationError("a store pair lies outside the carrier")
        for g in self.ops:
            if len(g) != self.n or any(not (0 <= v < self.n) for v in g):
                raise TranslationError("an operation is not closed on the carrier")

    def json(self) -> JsonDict:
        return {
            "n": self.n,
            "rel": [list(p) for p in sorted(self.rel)],
            "ret": [list(p) for p in sorted(self.ret)],
            "prot": [list(p) for p in sorted(self.prot)],
            "a": self.a,
            "b": self.b,
            "ops": [list(g) for g in self.ops],
        }


def events(F: FiniteSetting) -> tuple[Event, ...]:
    """The admission history of the encoding: the carrier, one binary form
    per store and per operation, the asserted pairs, the graphs."""
    out: list[Event] = [AdmitDatum(f"x{i}") for i in range(F.n)]
    out.extend(AdmitForm(2) for _ in range(3 + len(F.ops)))
    for form, store in ((0, F.rel), (1, F.ret), (2, F.prot)):
        out.extend(AdmitInst(form, (x, y)) for x, y in sorted(store))
    for k, g in enumerate(F.ops):
        out.extend(AdmitInst(3 + k, (x, g[x])) for x in range(F.n))
    return tuple(out)


def encode(F: FiniteSetting) -> Regime:
    """The Lean ``encode``, as the sealed replay of ``events``."""
    history = events(F)
    r = replay(history)
    if not certify(history, r):
        raise TranslationError("the encoding does not replay from its history")
    return r


def expected_instances(F: FiniteSetting) -> frozenset[tuple[int, Pair]]:
    graph = {(3 + k, (x, g[x])) for k, g in enumerate(F.ops) for x in range(F.n)}
    return frozenset({(0, p) for p in F.rel} | {(1, p) for p in F.ret} | {(2, p) for p in F.prot} | graph)


def faithful(F: FiniteSetting, r: Regime) -> bool:
    """The Lean ``derivable_rel``/``derivable_ret``/``derivable_prot``/
    ``derivable_op`` on one encoding: the derivable binary instances are
    exactly the store pairs and graph edges, the shape is as declared."""
    if r.n_data() != F.n or r.forms != (2,) * (3 + len(F.ops)) or r.rules or r.reqs:
        return False
    expected = expected_instances(F)
    if frozenset(r.insts) != expected:
        return False
    return all(
        derivable(r, (f, (x, y))) == ((f, (x, y)) in expected)
        for f in range(len(r.forms)) for x in range(F.n) for y in range(F.n)
    )


# ---------------------------------------------------------------------------
# Internal visibility (the Lean ``Visible``)
# ---------------------------------------------------------------------------


def visible(r: Regime, x: int, y: int) -> bool:
    """Some binary form's self-instance, row or column differs at ``x`` and
    ``y``.  Declared for binary regimes only, as the Lean criterion is."""
    if any(a != 2 for a in r.forms):
        raise TranslationError("visibility is declared for binary regimes only")
    n = r.n_data()
    for f in range(len(r.forms)):
        if derivable(r, (f, (x, x))) != derivable(r, (f, (y, y))):
            return True
        for z in range(n):
            if derivable(r, (f, (x, z))) != derivable(r, (f, (y, z))):
                return True
            if derivable(r, (f, (z, x))) != derivable(r, (f, (z, y))):
                return True
    return False


def visible_rows_columns(r: Regime, x: int, y: int) -> bool:
    """The criterion without its self-instance clause (the Lean
    ``visible_iff_rows_columns``): a row or a column differs."""
    if any(a != 2 for a in r.forms):
        raise TranslationError("visibility is declared for binary regimes only")
    n = r.n_data()
    return any(
        derivable(r, (f, (x, z))) != derivable(r, (f, (y, z)))
        or derivable(r, (f, (z, x))) != derivable(r, (f, (z, y)))
        for f in range(len(r.forms)) for z in range(n)
    )


# ---------------------------------------------------------------------------
# Chains (the Lean ``run``, ``words``, ``NoChain``)
# ---------------------------------------------------------------------------


def run(F: FiniteSetting, word: Sequence[int], x: int) -> int:
    for k in word:
        x = F.ops[k][x]
    return x


def words(letters: int, max_len: int) -> Iterator[tuple[int, ...]]:
    """All words over ``range(letters)`` of length at most ``max_len``."""
    for length in range(max_len + 1):
        yield from product(range(letters), repeat=length)


def no_chain(F: FiniteSetting) -> bool:
    """The Lean ``NoChain``: no word of length at most ``n * n`` over the
    operation indices runs the two endpoints to the same datum."""
    return all(run(F, w, F.a) != run(F, w, F.b) for w in words(len(F.ops), F.n * F.n))


def no_chain_reach(F: FiniteSetting) -> bool:
    """The same by product-state reachability, the cross-check."""
    seen = {(F.a, F.b)}
    frontier = [(F.a, F.b)]
    while frontier:
        nxt: list[Pair] = []
        for x, y in frontier:
            if x == y:
                return False
            for g in F.ops:
                p = (g[x], g[y])
                if p not in seen:
                    seen.add(p)
                    nxt.append(p)
        frontier = nxt
    return True


# ---------------------------------------------------------------------------
# The nine readings, decided on the encoding
# ---------------------------------------------------------------------------


def readings(F: FiniteSetting) -> dict[str, bool]:
    """The nine candidate readings, each decided on the encoded regime by the
    statement the Lean transport gives it."""
    r = encode(F)
    n = F.n

    def d(f: int, x: int, y: int) -> bool:
        return derivable(r, (f, (x, y)))

    witnessed = d(0, F.a, F.b)
    no_self = all(not d(0, x, x) for x in range(n))
    symmetric = all(d(0, y, x) for x in range(n) for y in range(n) if d(0, x, y))
    splitting = all(
        d(0, x, z) or d(0, z, y)
        for x in range(n) for y in range(n) if d(0, x, y) for z in range(n)
    )
    a = witnessed and no_self
    return {
        "W": witnessed,
        "A": a,
        "Bs": a and symmetric,
        "Bc": a and splitting,
        "Bl": a,
        "C": witnessed and d(2, F.a, F.b),
        "D": F.a != F.b,
        "E": no_chain(F),
        "F": a and d(1, F.a, F.b) and d(2, F.a, F.b),
    }


def from_sealed(s: sealed.Setting) -> FiniteSetting:
    return FiniteSetting(s.n, s.r, s.ret, s.prot, s.a, s.b, tuple(sorted(s.ops)))


def to_sealed(F: FiniteSetting) -> sealed.Setting:
    return sealed.Setting(F.n, F.rel, F.a, F.b, F.ret, F.prot, frozenset(F.ops))


# ---------------------------------------------------------------------------
# The sealed concrete settings and the two-point exhibits
# ---------------------------------------------------------------------------


def _all(n: int) -> Rel:
    return frozenset((x, y) for x in range(n) for y in range(n))


def _const0(n: int) -> Table:
    return tuple(0 for _ in range(n))


NONE: Rel = frozenset()
EDGE: Rel = frozenset({(0, 1)})
BOTH: Rel = frozenset({(0, 1), (1, 0)})

# The thirteen concrete settings of the sealed `PrimitiveCore`, transcribed:
# `Unit` is the one-point carrier, `Bool` the two-point carrier with
# `false = 0`, `true = 1`, `Fin 3` the three-point carrier; the admitted
# merger `fun _ => false` is the constant table to 0.
SEALED_SETTINGS: dict[str, FiniteSetting] = {
    "unitBare": FiniteSetting(1, _all(1), NONE, NONE, 0, 0, ()),
    "unitFull": FiniteSetting(1, _all(1), _all(1), _all(1), 0, 0, ()),
    "d2Bare": FiniteSetting(2, EDGE, NONE, NONE, 0, 1, ()),
    "d2Merged": FiniteSetting(2, EDGE, NONE, NONE, 0, 1, (_const0(2),)),
    "d2Protected": FiniteSetting(2, EDGE, _all(2), _all(2), 0, 1, ()),
    "d2ProtectedMerged": FiniteSetting(2, EDGE, _all(2), _all(2), 0, 1, (_const0(2),)),
    "s2Bare": FiniteSetting(2, BOTH, NONE, NONE, 0, 1, ()),
    "s2Merged": FiniteSetting(2, BOTH, NONE, NONE, 0, 1, (_const0(2),)),
    "tri": FiniteSetting(3, EDGE, NONE, NONE, 0, 1, ()),
    "triProtected": FiniteSetting(3, EDGE, _all(3), _all(3), 0, 1, ()),
    "triSym": FiniteSetting(3, BOTH, NONE, NONE, 0, 1, ()),
    "boolEmpty": FiniteSetting(2, NONE, NONE, NONE, 0, 1, ()),
    "boolEmptyMerged": FiniteSetting(2, NONE, NONE, NONE, 0, 1, (_const0(2),)),
}

# The verdicts the sealed Lean theorems state, by theorem name.
SEALED_VERDICTS: tuple[tuple[str, str, bool, str], ...] = (
    ("unitBare", "W", True, "unitBare_w"),
    ("unitBare", "A", False, "unitBare_not_a"),
    ("unitBare", "C", False, "unitBare_not_c"),
    ("unitBare", "D", False, "unitBare_not_d"),
    ("unitBare", "E", False, "unitBare_not_e"),
    ("unitFull", "C", True, "unitFull_c"),
    ("unitFull", "A", False, "unitFull_not_a"),
    ("unitFull", "D", False, "unitFull_not_d"),
    ("unitFull", "E", False, "unitFull_not_e"),
    ("d2Bare", "A", True, "d2Bare_a"),
    ("d2Bare", "Bs", False, "d2Bare_not_bs"),
    ("d2Bare", "Bc", True, "d2Bare_bc"),
    ("d2Bare", "Bl", True, "d2Bare_bl"),
    ("d2Bare", "C", False, "d2Bare_not_c"),
    ("d2Bare", "F", False, "d2Bare_not_f"),
    ("d2Merged", "A", True, "d2Merged_a"),
    ("d2Merged", "Bc", True, "d2Merged_bc"),
    ("d2Merged", "Bl", True, "d2Merged_bl"),
    ("d2Merged", "E", False, "d2Merged_not_e"),
    ("d2Protected", "F", True, "d2Protected_f"),
    ("d2Protected", "Bs", False, "d2Protected_not_bs"),
    ("d2ProtectedMerged", "F", True, "d2ProtectedMerged_f"),
    ("d2ProtectedMerged", "E", False, "d2ProtectedMerged_not_e"),
    ("s2Bare", "Bs", True, "s2Bare_bs"),
    ("s2Bare", "C", False, "s2Bare_not_c"),
    ("s2Bare", "F", False, "s2Bare_not_f"),
    ("s2Merged", "Bs", True, "s2Merged_bs"),
    ("s2Merged", "E", False, "s2Merged_not_e"),
    ("tri", "A", True, "tri_a"),
    ("tri", "Bl", True, "tri_bl"),
    ("tri", "Bc", False, "tri_not_bc"),
    ("triProtected", "F", True, "triProtected_f"),
    ("triProtected", "Bc", False, "triProtected_not_bc"),
    ("triSym", "Bs", True, "triSym_bs"),
    ("triSym", "Bc", False, "triSym_not_bc"),
    ("boolEmpty", "W", False, "boolEmpty_not_w"),
    ("boolEmpty", "A", False, "boolEmpty_not_a"),
    ("boolEmpty", "C", False, "boolEmpty_not_c"),
    ("boolEmpty", "D", True, "boolEmpty_d"),
    ("boolEmpty", "E", True, "boolEmpty_e"),
    ("boolEmptyMerged", "D", True, "boolEmptyMerged_d"),
    ("boolEmptyMerged", "E", False, "boolEmptyMerged_not_e"),
)

# The two-point exhibits of `lean/Visible.lean` and their proved verdicts.
TWO_POINT: dict[str, tuple[FiniteSetting, bool]] = {
    "selfOnly": (FiniteSetting(2, frozenset({(0, 0)}), NONE, NONE, 0, 1, ()), True),
    "linkOnly": (FiniteSetting(2, EDGE, NONE, NONE, 0, 1, ()), True),
    "selfAndLink": (FiniteSetting(2, frozenset({(0, 0), (0, 1)}), NONE, NONE, 0, 1, ()), True),
    "bothLinks": (FiniteSetting(2, BOTH, NONE, NONE, 0, 1, ()), True),
    "everyPair": (FiniteSetting(2, _all(2), NONE, NONE, 0, 1, ()), False),
    "noPair": (FiniteSetting(2, NONE, NONE, NONE, 0, 1, ()), False),
}


# ---------------------------------------------------------------------------
# The sealed engine restarted from an encoded setting
# ---------------------------------------------------------------------------


def reading_of(name: str, F: FiniteSetting) -> Reading:
    if F.a == F.b:
        raise TranslationError("the seed target needs two distinct endpoints")
    return Reading(
        f"encoded:{name}",
        "the encoded setting as genesis; the designated pair as the seed target",
        events(F),
        (min(F.a, F.b), max(F.a, F.b)),
    )


def restart(name: str, F: FiniteSetting, measure: str, supply: bool,
            max_rounds: int, guard: int) -> JsonDict:
    """The sealed ``build_tree`` from the encoding, certified by the sealed
    ``verify_full_export``; the root round and the tree statistics."""
    reading = reading_of(name, F)
    tree = build_tree(reading, measure, Bounds(2, 2), max_rounds, guard, supply)
    payload = tree_full_json(tree)
    if not verify_full_export(payload):
        raise TranslationError(f"{name}: the sealed certification refused the restart export")
    root = tree.nodes[0]
    root_edges = [e for e in tree.edges if e.parent == 0]
    classes: list[Json] = [
        {
            "label": e.response_label,
            "response": cast(Json, delta_json(e.response)),
            "class_size": e.class_size,
            "tie_classes": e.tie_classes,
            "cost": list(e.cost),
            "kind": e.kind,
        }
        for e in root_edges
    ]
    return {
        "measure": measure,
        "supply": supply,
        "max_rounds": max_rounds,
        "guard": guard,
        "target": list(reading.target),
        "target_collapsed_at_root": reading.target in collapsed_pairs(root.regime),
        "root_regime_sha256": regime_sha256(root.regime),
        "root_round": classes,
        "stats": cast(Json, tree.stats()),
        "export_sha256": hashlib.sha256(dumps_deterministic(cast(Json, payload))).hexdigest(),
    }


# ---------------------------------------------------------------------------
# The census
# ---------------------------------------------------------------------------


def universe_census() -> JsonDict:
    """Every setting of the sealed finite universe: encoded, faithful, the
    nine readings on the encoding against the sealed evaluator, visibility
    against the sealed separability and against its row-column form, the
    chain criterion against reachability; then the tallies the claims
    quote."""
    failures: list[Json] = []
    total = 0
    distinct_pairs = 0
    pair_visible = 0
    by_reading: dict[str, dict[str, int]] = {p: {"holds": 0, "holds_visible": 0, "holds_collapsed": 0}
                                             for p in READINGS}
    by_n: dict[str, int] = {}
    for s in sealed.enumerate_settings():
        total += 1
        F = from_sealed(s)
        r = encode(F)
        by_n[str(F.n)] = by_n.get(str(F.n), 0) + 1
        if not faithful(F, r):
            failures.append({"setting": F.json(), "check": "faithful"})
            continue
        ours = readings(F)
        theirs = sealed.evaluate(s)
        if ours != theirs:
            failures.append({"setting": F.json(), "check": "readings", "encoded": ours, "sealed": theirs})
        if no_chain(F) != no_chain_reach(F):
            failures.append({"setting": F.json(), "check": "chain_reach"})
        for x in range(F.n):
            for y in range(x + 1, F.n):
                if visible(r, x, y) != separable(r, x, y):
                    failures.append({"setting": F.json(), "check": "visible", "pair": [x, y]})
                if visible_rows_columns(r, x, y) != visible(r, x, y):
                    failures.append({"setting": F.json(), "check": "rows_columns", "pair": [x, y]})
        if F.a != F.b:
            distinct_pairs += 1
            vis = visible(r, F.a, F.b)
            pair_visible += int(vis)
            for p in READINGS:
                if ours[p]:
                    by_reading[p]["holds"] += 1
                    by_reading[p]["holds_visible" if vis else "holds_collapsed"] += 1
    return {
        "settings": total,
        "by_carrier_size": by_n,
        "settings_with_distinct_endpoints": distinct_pairs,
        "distinct_endpoints_visible": pair_visible,
        "distinct_endpoints_collapsed": distinct_pairs - pair_visible,
        "by_reading": cast(Json, by_reading),
        "failures": failures,
    }


def sealed_settings_census() -> JsonDict:
    """The thirteen sealed concrete settings: readings on the encoding
    against the sealed theorem verdicts, visibility, and the engine restarted
    at the designated pair under both measures."""
    out: dict[str, Json] = {}
    failures: list[Json] = []
    for name, F in SEALED_SETTINGS.items():
        r = encode(F)
        ours = readings(F)
        checks: list[Json] = []
        for setting, reading, verdict, theorem in SEALED_VERDICTS:
            if setting != name:
                continue
            agree = ours[reading] == verdict
            checks.append({"reading": reading, "theorem": theorem, "verdict": verdict, "agrees": agree})
            if not agree:
                failures.append({"setting": name, "theorem": theorem})
        if ours != sealed.evaluate(to_sealed(F)):
            failures.append({"setting": name, "check": "sealed evaluator"})
        entry: dict[str, Json] = {
            "setting": F.json(),
            "regime_sha256": regime_sha256(r),
            "faithful": faithful(F, r),
            "readings": cast(Json, ours),
            "sealed_theorems": checks,
        }
        if F.a != F.b:
            entry["pair_visible"] = visible(r, F.a, F.b)
            entry["restart"] = {
                m: restart(name, F, m, False, 4, 120) for m in ("mu1", "mu2")
            }
        out[name] = entry
    return {"settings": out, "failures": failures}


def two_point_census() -> JsonDict:
    out: dict[str, Json] = {}
    failures: list[Json] = []
    for name, (F, proved_visible) in TWO_POINT.items():
        r = encode(F)
        vis = visible(r, 0, 1)
        if vis != proved_visible or vis != separable(r, 0, 1):
            failures.append({"exhibit": name, "visible": vis, "proved": proved_visible})
        entry: dict[str, Json] = {
            "setting": F.json(),
            "visible": vis,
            "readings": cast(Json, readings(F)),
            "restart": {
                f"{m}_{'supply' if sup else 'closed'}": restart(name, F, m, sup, 3, 60)
                for m in ("mu1", "mu2") for sup in (False, True)
            },
        }
        out[name] = entry
    return {"exhibits": out, "failures": failures}


def census() -> JsonDict:
    universe = universe_census()
    thirteen = sealed_settings_census()
    two_point = two_point_census()
    failures = (len(cast(list[Json], universe["failures"])) + len(cast(list[Json], thirteen["failures"]))
                + len(cast(list[Json], two_point["failures"])))
    return {
        "schema_version": 1,
        "classification": "deterministic computation through the sealed kernel",
        "authority_effect": "None",
        "universe": universe,
        "sealed_settings": thirteen,
        "two_point": two_point,
        "totals": {"failures": failures, "universe_settings": universe["settings"]},
    }
