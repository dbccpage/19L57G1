"""Never-selects instance reader, and the source scan."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

import reader  # noqa: E402
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, Supply, replay  # noqa: E402


class Lookup(unittest.TestCase):
    def test_unique_edge(self) -> None:
        insts = frozenset({(0, (0, 1)), (0, (1, 2))})
        self.assertEqual(reader.lookup_binary(insts, 0, 0), 1)
        self.assertEqual(reader.lookup_binary(insts, 0, 1), 2)
        self.assertIsNone(reader.lookup_binary(insts, 0, 2))
        self.assertIsNone(reader.lookup_binary(insts, 1, 0))

    def test_multiple_matches_refuse_to_choose(self) -> None:
        insts = frozenset({(0, (0, 1)), (0, (0, 2))})
        self.assertIsNone(reader.lookup_binary(insts, 0, 0))

    def test_non_binary_ignored(self) -> None:
        insts = frozenset({(0, (0,)), (0, (0, 1, 2))})
        self.assertIsNone(reader.lookup_binary(insts, 0, 0))
        self.assertEqual(reader.read_pairs(insts, 0), ())


class ReadPairs(unittest.TestCase):
    def test_drops_reflexive_and_reversed(self) -> None:
        insts = frozenset({(0, (0, 1)), (0, (1, 0)), (0, (2, 2)), (1, (0, 3))})
        self.assertEqual(reader.read_pairs(insts, 0), ((0, 1),))

    def test_regime_wrapper(self) -> None:
        history = (
            Supply("a"), AdmitDatum("a"), Supply("b"), AdmitDatum("b"),
            AdmitForm(2), AdmitInst(0, (0, 1)),
        )
        regime = replay(history)
        self.assertEqual(reader.read_pairs_of_regime(regime, 0), ((0, 1),))
        self.assertEqual(regime.reqs, frozenset())


class NeverSelects(unittest.TestCase):
    def test_committed_source_has_no_forbidden_names(self) -> None:
        self.assertEqual(reader.reader_source_violations(), ())

    def test_injected_reqs_branch_is_named(self) -> None:
        source = (
            "from derivation.model import Regime\n"
            "def bad(regime: Regime):\n"
            "    return sorted(regime.reqs)\n"
        )
        hits = reader.reader_source_violations(source)
        self.assertTrue(any(h.endswith(":reqs") for h in hits), hits)

    def test_injected_collapsed_name_is_named(self) -> None:
        source = "collapsed = True\n"
        hits = reader.reader_source_violations(source)
        self.assertEqual(hits, ("1:collapsed",))

    def test_getattr_on_forbidden_field_is_named(self) -> None:
        # a dynamic accessor with a literal forbidden name is the same host
        # choice as a direct attribute access and must be named too.
        for src in (
            "def bad(regime):\n    return getattr(regime, 'reqs')\n",
            "def bad(regime):\n    return hasattr(regime, 'collapsed_pairs')\n",
        ):
            hits = reader.reader_source_violations(src)
            self.assertTrue(hits, src)
        # a bare string constant that is not an accessor argument is not a hit
        self.assertEqual(reader.reader_source_violations("note = 'reqs'\n"), ())


if __name__ == "__main__":
    unittest.main()
