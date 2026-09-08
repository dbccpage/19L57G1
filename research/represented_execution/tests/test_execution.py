"""The configuration machine against the operations it represents, and the
named refusals.  The expected values come from the merged ``translation.run``
— the fold that reads the operation tables — which the *tests* may consult
to state what the machine should compute; the machine itself never does."""

from __future__ import annotations

from itertools import islice, product
from pathlib import Path
import sys
import unittest

# Dependencies first, this tree last, so this tree wins name collisions with
# the merged sibling (``run``, ``verify_sources``).
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "setting_translation"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import execution as ex  # noqa: E402
import translation as tr  # noqa: E402
from derivation import primitive_core as sealed  # noqa: E402

TWO_OPS = tr.FiniteSetting(3, tr.NONE, tr.NONE, tr.NONE, 0, 1, ((1, 2, 0), (0, 0, 0)))
UNIVERSE_SLICE = 400
MAX_WORD = 3


def words(letters: int, max_len: int) -> list[tuple[int, ...]]:
    return [w for length in range(max_len + 1) for w in product(range(letters), repeat=length)]


class Correspondence(unittest.TestCase):
    """``run_encode``: on every sampled setting, every well-formed word from
    every datum halts with the word consumed and the active datum the
    operations compute; ``run_evalWord``: the machine agrees with the
    graph-reading fold."""

    def check(self, F: tr.FiniteSetting) -> None:
        graph = frozenset(tr.encode(F).insts)
        for w in words(len(F.ops), MAX_WORD):
            for x in range(F.n):
                c = ex.run(ex.init(F, w, x))
                self.assertIsNotNone(c, (F, w, x))
                assert c is not None
                self.assertEqual(c.word, ())
                self.assertEqual(c.active, tr.run(F, w, x), (F, w, x))
                self.assertEqual(c.active, ex.eval_word(graph, w, x))
                self.assertEqual(len(c.output), len(w))
                self.assertLess(c.active, F.n)

    def test_sealed_settings(self) -> None:
        for F in tr.SEALED_SETTINGS.values():
            self.check(F)

    def test_two_point_exhibits(self) -> None:
        for F, _ in tr.TWO_POINT.values():
            self.check(F)

    def test_universe_slice(self) -> None:
        count = 0
        for s in islice(sealed.enumerate_settings(), UNIVERSE_SLICE):
            self.check(tr.from_sealed(s))
            count += 1
        self.assertEqual(count, UNIVERSE_SLICE)

    def test_two_operation_setting(self) -> None:
        self.check(TWO_OPS)


class WordBridgeTests(unittest.TestCase):
    """The executable tests the brief names, on a setting with two distinct
    operations so that reading the letter and reading the graph both matter."""

    def test_graph_mutation_changes_the_output(self) -> None:
        c0 = ex.init(TWO_OPS, (0, 0), 0)
        before = ex.run(c0)
        assert before is not None
        mutated = ex.replace_edge(c0.graph, 3, 1, 1)  # op 0 at datum 1: 2 -> 1
        after = ex.run(ex.Config(mutated, c0.word, c0.active, c0.output))
        assert after is not None
        self.assertEqual(before.active, 2)
        self.assertEqual(after.active, 1)
        self.assertNotEqual(before.active, after.active)

    def test_mid_run_edit_diverges(self) -> None:
        c0 = ex.init(TWO_OPS, (0, 0, 0), 0)
        unflipped = ex.run(c0)
        mid = ex.iterate(1, c0)
        assert unflipped is not None and mid is not None
        self.assertEqual(mid.active, 1)
        self.assertEqual(mid.word, (0, 0))
        edited = ex.Config(ex.replace_edge(mid.graph, 3, 1, 1), mid.word, mid.active, mid.output)
        continued = ex.run(edited)
        assert continued is not None
        self.assertEqual(unflipped.active, 0)
        self.assertEqual(continued.active, 1)
        self.assertNotEqual(continued.output, unflipped.output)

    def test_two_graphs_one_word(self) -> None:
        G = tr.FiniteSetting(3, tr.NONE, tr.NONE, tr.NONE, 0, 1, ((1, 0, 0), (0, 0, 0)))
        word = (0, 0)
        a = ex.run(ex.init(TWO_OPS, word, 0))
        b = ex.run(ex.init(G, word, 0))
        assert a is not None and b is not None
        self.assertNotEqual(a.active, b.active)

    def test_a_letter_names_an_operation(self) -> None:
        c0 = ex.run(ex.init(TWO_OPS, (0,), 0))
        c1 = ex.run(ex.init(TWO_OPS, (1,), 0))
        assert c0 is not None and c1 is not None
        self.assertEqual(c0.active, 1)
        self.assertEqual(c1.active, 0)

    def test_concatenate(self) -> None:
        for F in (TWO_OPS, tr.SEALED_SETTINGS["d2Merged"]):
            for u in words(len(F.ops), 2):
                for v in words(len(F.ops), 2):
                    for x in range(F.n):
                        whole = ex.run(ex.init(F, u + v, x))
                        first = ex.run(ex.init(F, u, x))
                        assert whole is not None and first is not None
                        rest = ex.resume(first, v)
                        assert rest is not None
                        self.assertEqual(whole.active, rest.active, (F, u, v, x))
                        self.assertEqual(whole.output, rest.output, (F, u, v, x))

    def test_empty_word_is_the_unit(self) -> None:
        for F in tr.SEALED_SETTINGS.values():
            for x in range(F.n):
                c = ex.init(F, (), x)
                self.assertIsNone(ex.step(c))
                self.assertEqual(ex.run(c), c)
                self.assertEqual(c.output, ())

    def test_iterate_add(self) -> None:
        c0 = ex.init(TWO_OPS, (0, 1, 0, 0), 0)
        for a in range(5):
            for b in range(5 - a):
                left = ex.iterate(a + b, c0)
                mid = ex.iterate(a, c0)
                right = None if mid is None else ex.iterate(b, mid)
                self.assertEqual(left, right, (a, b))


class Refusals(unittest.TestCase):
    def test_missing_edge_refuses_without_writing(self) -> None:
        c0 = ex.init(TWO_OPS, (0, 0), 0)
        torn = ex.Config(ex.remove_edge(c0.graph, 3, 1), c0.word, c0.active, c0.output)
        self.assertIsNone(ex.run(torn))
        mid = ex.iterate(1, torn)
        assert mid is not None
        self.assertEqual(mid.active, 1)
        self.assertIsNone(ex.step(mid))

    def test_two_edges_on_one_form_are_refused_by_name(self) -> None:
        c0 = ex.init(TWO_OPS, (0,), 1)
        doubled = c0.graph | {(3, (1, 0))}
        with self.assertRaises(ex.ExecutionError):
            ex.run(ex.Config(doubled, c0.word, c0.active, c0.output))

    def test_start_outside_the_carrier_is_refused(self) -> None:
        with self.assertRaises(ex.ExecutionError):
            ex.init(TWO_OPS, (), 3)

    def test_an_unknown_letter_refuses(self) -> None:
        self.assertIsNone(ex.run(ex.init(TWO_OPS, (2,), 0)))


if __name__ == "__main__":
    unittest.main()
