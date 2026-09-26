"""Closeout audit (2026-09-25) of the real admission boundary.

Each hypothesis of ``docs/GENESIS_CLOSEOUT.md`` section 4 and the items of
the audit are tested through the real public path (``evaluate`` ->
``make_license`` -> ``apply_licensed`` / ``explore``), each paired with a
positive control that admits a legitimate transition.  The positive
controls are checked independently of the harness's own verdict: by sealed
replay from genesis and by a fresh recomputation from the sealed kernel
(``min_responses`` / ``canonical``), not by ``evaluate``.

When a repair is reverted (a live injection, see ``inject_boundary.py``),
the adversarial test fails with a message that names the defect.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Callable
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

from derivation.candidates import (  # noqa: E402
    Bounds,
    Delta,
    delta_events,
    min_responses,
)
from derivation.engine import READING_F, READING_L  # noqa: E402
from derivation.iso import CanonKey, canonical  # noqa: E402
from derivation.model import (  # noqa: E402
    EMPTY,
    AdmitDatum,
    Event,
    Impose,
    Pair,
    Regime,
    Supply,
    replay,
)
from derivation.observe import satisfies  # noqa: E402

from driver_a import apply_licensed, explore  # noqa: E402
from evaluate import evaluate  # noqa: E402
from harness import (  # noqa: E402
    EvalResult,
    ForgedEvaluationError,
    License,
    LicenseBindingError,
    Node,
    NodeIntegrityError,
    Proposal,
    RetainedClass,
    SeventhEventError,
    SubstitutedMemberError,
    UniqueDeltaAutoApplyError,
    apply_unique_delta,
    check_node_integrity,
    history_digest,
    make_license,
    present,
)
from search_policy import (  # noqa: E402
    CensusError,
    FabricatedClassError,
    PolicyCensus,
    declared_explore_first,
    record_census,
)

B22 = Bounds(2, 2)


def fresh_classes(
    regime: Regime, target: Pair, measure: str, bounds: Bounds
) -> dict[CanonKey, tuple[Delta, ...]]:
    """Independent sealed recomputation: min_responses grouped by canonical."""
    minima = min_responses(regime, target, measure, bounds)
    grouped: dict[CanonKey, list[Delta]] = {}
    if minima is None:
        return {}
    for delta in minima.deltas:
        child = replay(
            (Impose(target[0], target[1]),) + delta_events(regime, delta), regime
        )
        grouped.setdefault(canonical(child), []).append(delta)
    return {key: tuple(members) for key, members in grouped.items()}


def node_of(history: tuple[Event, ...]) -> Node:
    return Node(history=history, regime=replay(history), license=None)


def license_at(
    node: Node,
    target: Pair,
    authorized: tuple[CanonKey, ...],
    measure: str = "mu1",
    bounds: Bounds = B22,
) -> License:
    return make_license(
        granter="host",
        scope="closeout-audit",
        authorized=tuple(sorted(authorized)),
        source=node,
        target=target,
        measure=measure,
        bounds=bounds,
    )


def with_members(
    result: EvalResult, index: int, members: tuple[Delta, ...]
) -> EvalResult:
    """A forged copy of ``result`` whose class ``index`` claims ``members``."""
    retained = list(result.retained)
    retained[index] = RetainedClass(retained[index].key, members)
    return EvalResult(
        measure=result.measure,
        cost=result.cost,
        raw_minima=result.raw_minima,
        retained=tuple(retained),
        found=result.found,
        max_items=result.max_items,
        max_arity=result.max_arity,
    )


@dataclass(frozen=True)
class ExtraEvent:
    token: str


class Boundary(unittest.TestCase):
    def assert_refused(
        self,
        error: type[BaseException],
        call: Callable[[], object],
        defect: str,
    ) -> BaseException:
        """``call`` must raise ``error``; if it returns, fail naming ``defect``."""
        try:
            out = call()
        except error as exc:
            return exc
        self.fail(f"{defect}: the call returned {out!r}")

    def assert_legitimate_child(
        self, parent: Node, child: Node | None, target: Pair, key: CanonKey,
        measure: str = "mu1", bounds: Bounds = B22,
    ) -> Node:
        """Independent checks: sealed replay and fresh sealed recomputation."""
        self.assertIsNotNone(child)
        assert child is not None
        self.assertEqual(replay(child.history), child.regime)
        self.assertEqual(child.history[: len(parent.history)], parent.history)
        self.assertEqual(canonical(child.regime), key)
        self.assertTrue(satisfies(child.regime))
        classes = fresh_classes(parent.regime, target, measure, bounds)
        tail = child.history[len(parent.history):]
        self.assertEqual(tail[0], Impose(target[0], target[1]))
        executed = [
            member for member in classes[key]
            if delta_events(parent.regime, member) == tail[1:]
        ]
        self.assertEqual(len(executed), 1, "executed delta is not a fresh class member")
        return child


class B1SubstitutedMember(Boundary):
    """M1: authorized admission executes only a checked member."""

    def setUp(self) -> None:
        self.node = node_of(READING_L.genesis)
        self.target = READING_L.target
        self.result = evaluate(self.node.regime, self.target, "mu1", B22)
        self.keys = tuple(item.key for item in self.result.retained)
        self.license = license_at(self.node, self.target, (self.keys[0],))

    def test_b1_control_admits_the_fresh_class_member(self) -> None:
        child = apply_licensed(
            self.node, self.result, self.license, self.keys[0], self.target
        )
        self.assert_legitimate_child(self.node, child, self.target, self.keys[0])

    def test_b1_empty_member_under_an_authorized_key_is_refused(self) -> None:
        forged = with_members(self.result, 0, ((),))
        self.assert_refused(
            SubstitutedMemberError,
            lambda: apply_licensed(
                self.node, forged, self.license, self.keys[0], self.target
            ),
            "B1 REPRODUCED: apply_licensed executed an empty substituted member "
            "of an authorized key",
        )

    def test_b1_other_class_member_under_an_authorized_key_is_refused(self) -> None:
        forged = with_members(self.result, 0, self.result.retained[2].members)
        self.assert_refused(
            SubstitutedMemberError,
            lambda: apply_licensed(
                self.node, forged, self.license, self.keys[0], self.target
            ),
            "B1 REPRODUCED: apply_licensed executed a member of an unauthorized "
            "class under an authorized key",
        )

    def test_b1_explore_refuses_a_substituted_member(self) -> None:
        forged = with_members(self.result, 0, ((),))
        census = record_census(self.keys, (self.keys[0],), (), self.keys[1:])
        self.assert_refused(
            SubstitutedMemberError,
            lambda: explore(
                self.node, forged, self.license, census, self.target
            ),
            "B1 REPRODUCED: explore executed an empty substituted member of an "
            "authorized key",
        )

    def test_b1_other_forged_evidence_is_refused(self) -> None:
        forged = EvalResult(
            measure=self.result.measure,
            cost=(1, -1),
            raw_minima=self.result.raw_minima,
            retained=self.result.retained,
            found=True,
            max_items=self.result.max_items,
            max_arity=self.result.max_arity,
        )
        self.assert_refused(
            ForgedEvaluationError,
            lambda: apply_licensed(
                self.node, forged, self.license, self.keys[0], self.target
            ),
            "B1 REPRODUCED: apply_licensed accepted evidence with a forged cost",
        )


class B2NodeIntegrity(Boundary):
    """M2: an admission step refuses a parent that does not replay."""

    def setUp(self) -> None:
        self.target = READING_L.target
        self.regime = replay(READING_L.genesis)
        self.result = evaluate(self.regime, self.target, "mu1", B22)
        self.keys = tuple(item.key for item in self.result.retained)
        self.bad = Node(history=READING_F.genesis, regime=self.regime, license=None)

    def test_b2_control_integral_parent_admits(self) -> None:
        node = node_of(READING_L.genesis)
        license = license_at(node, self.target, (self.keys[0],))
        child = apply_licensed(node, self.result, license, self.keys[0], self.target)
        self.assert_legitimate_child(node, child, self.target, self.keys[0])

    def test_b2_parent_whose_history_replays_elsewhere_is_refused(self) -> None:
        license = license_at(self.bad, self.target, (self.keys[0],))
        self.assert_refused(
            NodeIntegrityError,
            lambda: apply_licensed(
                self.bad, self.result, license, self.keys[0], self.target
            ),
            "B2 REPRODUCED: apply_licensed accepted a parent whose history "
            "does not replay to its stated regime",
        )

    def test_b2_explore_refuses_a_parent_that_does_not_replay(self) -> None:
        license = license_at(self.bad, self.target, (self.keys[0],))
        census = record_census(self.keys, (self.keys[0],), (), self.keys[1:])
        self.assert_refused(
            NodeIntegrityError,
            lambda: explore(self.bad, self.result, license, census, self.target),
            "B2 REPRODUCED: explore accepted a parent whose history does not "
            "replay to its stated regime",
        )

    def test_b2_unreplayable_and_foreign_histories_are_refused(self) -> None:
        with self.assertRaises(NodeIntegrityError) as ctx:
            check_node_integrity(
                Node(history=(Impose(0, 1),), regime=EMPTY, license=None)
            )
        self.assertIn("does not replay", str(ctx.exception))
        foreign = (ExtraEvent("x"),)
        with self.assertRaises(NodeIntegrityError) as ctx:
            check_node_integrity(
                Node(history=foreign, regime=EMPTY, license=None)  # type: ignore[arg-type]
            )
        self.assertIn("non-sealed constructor", str(ctx.exception))
        check_node_integrity(node_of(READING_L.genesis))


class B3LicenseBinding(Boundary):
    """M3: an authorization is bound to source, target, measure and bounds."""

    def setUp(self) -> None:
        self.node = node_of(READING_L.genesis)
        self.target = READING_L.target
        self.result = evaluate(self.node.regime, self.target, "mu1", B22)
        self.keys = tuple(item.key for item in self.result.retained)
        self.license = license_at(self.node, self.target, (self.keys[0],))

    def test_b3_control_license_at_its_declaration_admits(self) -> None:
        child = apply_licensed(
            self.node, self.result, self.license, self.keys[0], self.target
        )
        self.assert_legitimate_child(self.node, child, self.target, self.keys[0])

    def test_b3_license_at_a_relabelled_source_is_refused(self) -> None:
        # Same canonical keys, different presentation: datum 0 is <ab> here.
        other = node_of((AdmitDatum("<ab>"), AdmitDatum("<a>")))
        self.assertEqual(canonical(other.regime), canonical(self.node.regime))
        result = evaluate(other.regime, self.target, "mu1", B22)
        self.assertEqual(result.retained, self.result.retained)
        exc = self.assert_refused(
            LicenseBindingError,
            lambda: apply_licensed(
                other, result, self.license, self.keys[0], self.target
            ),
            "B3 REPRODUCED: a License granted at one source node was accepted "
            "at a relabelled source",
        )
        self.assertIn("source", str(exc))

    def test_b3_license_at_same_regime_other_history_is_refused(self) -> None:
        other = node_of(READING_L.genesis + (Supply("<c>"),))
        self.assertEqual(other.regime, self.node.regime)
        exc = self.assert_refused(
            LicenseBindingError,
            lambda: apply_licensed(
                other, self.result, self.license, self.keys[0], self.target
            ),
            "B3 REPRODUCED: a License granted at one history was accepted at "
            "another history",
        )
        self.assertIn("source", str(exc))

    def test_b3_license_for_another_target_is_refused(self) -> None:
        node = node_of(READING_F.genesis)
        granted = evaluate(node.regime, (1, 2), "mu1", B22)
        used = evaluate(node.regime, (0, 1), "mu1", B22)
        keys = tuple(item.key for item in granted.retained)
        self.assertEqual(keys, tuple(item.key for item in used.retained))
        license = license_at(node, (1, 2), (keys[0],))
        exc = self.assert_refused(
            LicenseBindingError,
            lambda: apply_licensed(node, used, license, keys[0], (0, 1)),
            "B3 REPRODUCED: a License granted for target (1, 2) was accepted "
            "for target (0, 1)",
        )
        self.assertIn("target", str(exc))

    def test_b3_license_for_another_measure_is_refused(self) -> None:
        used = evaluate(self.node.regime, self.target, "mu2", B22)
        self.assertEqual(tuple(item.key for item in used.retained), (self.keys[0],))
        exc = self.assert_refused(
            LicenseBindingError,
            lambda: apply_licensed(
                self.node, used, self.license, self.keys[0], self.target
            ),
            "B3 REPRODUCED: a License granted for mu1 was accepted for mu2",
        )
        self.assertIn("measure", str(exc))

    def test_b3_license_for_other_bounds_is_refused(self) -> None:
        for bounds in (Bounds(2, 3), Bounds(2, 1)):
            with self.subTest(bounds=bounds):
                used = evaluate(self.node.regime, self.target, "mu1", bounds)
                self.assertIn(self.keys[0], {item.key for item in used.retained})
                exc = self.assert_refused(
                    LicenseBindingError,
                    lambda: apply_licensed(
                        self.node, used, self.license, self.keys[0], self.target
                    ),
                    f"B3 REPRODUCED: a License granted under Bounds(2, 2) was "
                    f"accepted under {bounds}",
                )
                self.assertIn("bounds", str(exc))

    def test_b3_explore_refuses_a_rebound_license(self) -> None:
        used = evaluate(self.node.regime, self.target, "mu1", Bounds(2, 3))
        keys = tuple(item.key for item in used.retained)
        census = record_census(keys, (self.keys[0],), (), keys[1:])
        self.assert_refused(
            LicenseBindingError,
            lambda: explore(self.node, used, self.license, census, self.target),
            "B3 REPRODUCED: explore accepted a License granted under other bounds",
        )

    def test_b3_declaration_fields_are_validated(self) -> None:
        digest = history_digest(READING_L.genesis)
        self.assertEqual(digest, history_digest(READING_L.genesis))
        self.assertNotEqual(digest, history_digest(READING_F.genesis))
        self.assertEqual(len(digest), 64)
        with self.assertRaises(SeventhEventError):
            history_digest((ExtraEvent("x"),))  # type: ignore[arg-type]
        for kwargs in (
            {"target": (0, 1), "measure": "mu3", "bounds": B22},
            {"target": (1, 1), "measure": "mu1", "bounds": B22},
            {"target": (0, 1), "measure": "mu1", "bounds": Bounds(-1, 2)},
            {"target": (0, 1), "measure": "mu1", "bounds": Bounds(2, -1)},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    make_license(
                        granter="host",
                        scope="s",
                        authorized=(),
                        source=self.node,
                        **kwargs,  # type: ignore[arg-type]
                    )


class H4UniquenessIsNotAuthorization(Boundary):
    """M4: no path admits without an applicable authorization."""

    def setUp(self) -> None:
        self.node = node_of(READING_L.genesis)
        self.target = READING_L.target
        self.unique = evaluate(self.node.regime, self.target, "mu2", B22)
        self.assertEqual(len(self.unique.retained), 1)
        self.key = self.unique.retained[0].key

    def test_h4_control_licensed_sole_class_admits(self) -> None:
        license = license_at(self.node, self.target, (self.key,), measure="mu2")
        census = record_census((self.key,), (self.key,), (), ())
        out = explore(self.node, self.unique, license, census, self.target)
        self.assertEqual(len(out.children), 1)
        self.assert_legitimate_child(
            self.node, out.children[0], self.target, self.key, measure="mu2"
        )

    def test_h4_unique_class_without_a_license_admits_nothing(self) -> None:
        with self.assertRaises(UniqueDeltaAutoApplyError):
            apply_unique_delta(self.node, self.unique)
        empty = license_at(self.node, self.target, (), measure="mu2")
        self.assertIsNone(
            apply_licensed(self.node, self.unique, empty, self.key, self.target)
        )
        census = record_census((self.key,), (), (), (self.key,))
        out = explore(self.node, self.unique, empty, census, self.target)
        self.assertEqual(out.children, ())
        self.assertEqual(out.census.open_keys, (self.key,))

    def test_h4_unique_class_under_an_inapplicable_license_is_refused(self) -> None:
        mu1_license = license_at(self.node, self.target, (self.key,), measure="mu1")
        census = record_census((self.key,), (self.key,), (), ())
        self.assert_refused(
            LicenseBindingError,
            lambda: explore(self.node, self.unique, mu1_license, census, self.target),
            "H4 REPRODUCED: a unique mu2 class was admitted under a License "
            "granted for mu1",
        )


class H5Dispositions(Boundary):
    """M5: every retained class receives an explicit disposition."""

    def setUp(self) -> None:
        self.node = node_of(READING_L.genesis)
        self.target = READING_L.target
        self.result = evaluate(self.node.regime, self.target, "mu1", B22)
        self.keys = tuple(item.key for item in self.result.retained)
        self.license = license_at(self.node, self.target, (self.keys[0],))

    def test_h5_control_every_fresh_class_has_one_disposition(self) -> None:
        policy = declared_explore_first(self.keys)
        out = explore(
            self.node, self.result, self.license, policy.census(), self.target
        )
        fresh = set(fresh_classes(self.node.regime, self.target, "mu1", B22))
        disposed = (
            list(out.census.explored)
            + list(out.census.pruned)
            + list(out.census.open_keys)
        )
        self.assertEqual(sorted(disposed), sorted(fresh))
        self.assertEqual(len(disposed), len(set(disposed)))
        self.assertEqual(len(out.children), len(out.census.explored))

    def test_h5_census_that_drops_a_class_is_refused(self) -> None:
        dropped = PolicyCensus(
            explored=(self.keys[0],), pruned=(), open_keys=(self.keys[1],),
            tie_set_size=2,
        )
        self.assert_refused(
            CensusError,
            lambda: explore(
                self.node, self.result, self.license, dropped, self.target
            ),
            "H5 REPRODUCED: explore accepted a census that drops a retained class",
        )

    def test_h5_explore_evidence_omitting_a_class_is_refused(self) -> None:
        omitted = EvalResult(
            self.result.measure, self.result.cost, self.result.raw_minima,
            self.result.retained[:1], True, 2, 2,
        )
        census = record_census((self.keys[0],), (self.keys[0],), (), ())
        self.assert_refused(
            FabricatedClassError,
            lambda: explore(
                self.node, omitted, self.license, census, self.target
            ),
            "H5 REPRODUCED: explore accepted evidence omitting retained classes",
        )

    def test_h5_apply_evidence_omitting_a_class_is_refused(self) -> None:
        omitted = EvalResult(
            self.result.measure, self.result.cost, self.result.raw_minima,
            self.result.retained[:1], True, 2, 2,
        )
        self.assert_refused(
            ForgedEvaluationError,
            lambda: apply_licensed(
                self.node, omitted, self.license, self.keys[0], self.target
            ),
            "H5 REPRODUCED: apply_licensed accepted evidence from which two "
            "retained classes had disappeared",
        )


class H6InertAndTypedStops(Boundary):
    """M6: inert proposal and evaluation; a bound stop is not a success."""

    def test_h6_proposal_and_evaluation_leave_admitted_state(self) -> None:
        node = node_of(READING_L.genesis)
        before = replay(READING_L.genesis)
        result = evaluate(node.regime, READING_L.target, "mu1", B22)
        after = present(node.regime, Proposal("offer", result.raw_minima))
        self.assertEqual(after, before)
        self.assertEqual(node.regime, before)
        check_node_integrity(node)

    def test_h6_unfound_evaluation_is_a_typed_stop_not_a_success(self) -> None:
        node = node_of(READING_L.genesis)
        target = READING_L.target
        bound = Bounds(1, 2)
        result = evaluate(node.regime, target, "mu1", bound)
        self.assertFalse(result.found)
        self.assertIsNone(result.cost)
        self.assertEqual((result.raw_minima, result.retained), ((), ()))
        self.assertIsNone(min_responses(node.regime, target, "mu1", bound))
        self.assertIsNotNone(min_responses(node.regime, target, "mu1", B22))
        found_key = evaluate(node.regime, target, "mu1", B22).retained[0].key
        license = license_at(node, target, (found_key,), bounds=bound)
        self.assert_refused(
            FabricatedClassError,
            lambda: apply_licensed(node, result, license, found_key, target),
            "H6 REPRODUCED: an unfound evaluation was admitted",
        )
        empty = license_at(node, target, (), bounds=bound)
        out = explore(node, result, empty, record_census((), (), (), ()), target)
        self.assertEqual(out.children, ())
        self.assertEqual(out.census.tie_set_size, 0)
        self.assertEqual(node.regime, replay(READING_L.genesis))


if __name__ == "__main__":
    unittest.main()
