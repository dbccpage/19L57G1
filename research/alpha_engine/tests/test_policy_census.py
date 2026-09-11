"""A silent drop of a retained class fails the census."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

from derivation.candidates import Bounds  # noqa: E402
from derivation.engine import READING_F, READING_L  # noqa: E402
from derivation.model import replay  # noqa: E402

from evaluate import evaluate  # noqa: E402
from search_policy import (  # noqa: E402
    CensusError,
    PolicyCensus,
    declared_explore_first,
    record_census,
)


class PolicyCensusTests(unittest.TestCase):
    def test_silent_drop_of_a_retained_class_fails(self) -> None:
        base = replay(READING_L.genesis)
        result = evaluate(base, READING_L.target, "mu1", Bounds(2, 2))
        retained = tuple(item.key for item in result.retained)
        self.assertGreaterEqual(len(retained), 2)
        with self.assertRaises(CensusError) as ctx:
            record_census(retained, (), (), retained[:-1])
        self.assertIn("silent drop", str(ctx.exception))

    def test_partition_counts_equal_the_tie_set(self) -> None:
        base = replay(READING_F.genesis)
        result = evaluate(base, READING_F.target, "mu1", Bounds(2, 2))
        retained = tuple(item.key for item in result.retained)
        policy = declared_explore_first(retained)
        census = policy.census()
        self.assertEqual(
            len(census.explored) + len(census.pruned) + len(census.open_keys),
            census.tie_set_size,
        )
        self.assertEqual(census.tie_set_size, len(retained))
        self.assertEqual(set(policy.subset()), set(census.explored))
        self.assertTrue(set(census.explored).issubset(set(retained)))

    def test_overlap_fails_the_census(self) -> None:
        base = replay(READING_L.genesis)
        result = evaluate(base, READING_L.target, "mu1", Bounds(2, 2))
        retained = tuple(item.key for item in result.retained)
        key = retained[0]
        rest = retained[1:]
        with self.assertRaises(CensusError):
            record_census(retained, (key,), (key,), rest)

    def test_direct_mismatch_counts_fail(self) -> None:
        with self.assertRaises(CensusError):
            PolicyCensus(explored=(), pruned=(), open_keys=(), tie_set_size=1)

    def test_duplicate_retained_or_bucket_keys_fail(self) -> None:
        base = replay(READING_L.genesis)
        result = evaluate(base, READING_L.target, "mu1", Bounds(2, 2))
        key = result.retained[0].key
        with self.assertRaises(CensusError):
            record_census((key, key), (), (), (key,))
        with self.assertRaises(CensusError):
            record_census((key,), (key, key), (), ())

    def test_declared_explore_first_on_empty_retained(self) -> None:
        policy = declared_explore_first(())
        census = policy.census()
        self.assertEqual(census.tie_set_size, 0)
        self.assertEqual(policy.subset(), ())


if __name__ == "__main__":
    unittest.main()
