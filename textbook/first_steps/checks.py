"""Finite teaching-model correspondence with sealed unary-context replay.

AuthorityEffect: None. No source files or derivation artifacts are written.
"""
from __future__ import annotations

from itertools import combinations, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "code"
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

from derivation import model, observe  # noqa: E402


def check_encoding(rows: tuple[tuple[bool, ...], ...], selected: tuple[int, ...]) -> int:
    events: list[model.Event] = [model.AdmitDatum(name) for name in ("A", "B", "C")]
    for form, question in enumerate(selected):
        events.append(model.AdmitForm(1))
        events.extend(model.AdmitInst(form, (card,)) for card, yes in enumerate(rows[question]) if yes)
    regime = model.replay(events)
    contexts = tuple((form, (None,)) for form in range(len(selected)))
    assert observe.contexts(regime) == contexts
    assert not regime.rules
    for card in range(3):
        expected_profile = frozenset(contexts[f] for f, question in enumerate(selected) if rows[question][card])
        assert observe.profile(regime, card) == expected_profile
        for form, question in enumerate(selected):
            assert observe.derivable(regime, observe.plug(contexts[form], card)) == rows[question][card]
    for left, right in combinations(range(3), 2):
        different = any(rows[q][left] != rows[q][right] for q in selected)
        assert observe.separable(regime, left, right) == different
        witness = observe.witness(regime, left, right)
        assert (witness is not None) == different
        if witness is not None:
            assert witness in contexts
            assert observe.derivable(regime, observe.plug(witness, left)) != observe.derivable(regime, observe.plug(witness, right))
    return 3


def check() -> dict[str, int]:
    for module in (model, observe):
        assert Path(module.__file__).resolve().is_relative_to(CODE), "Unexpected source origin"
    data = json.loads((Path(__file__).parent / "cards.json").read_text(encoding="utf-8"))
    assert [(c["id"], c["color"], c["shape"]) for c in data["cards"]] == [
        ("A", "blue", "circle"), ("B", "blue", "triangle"), ("C", "amber", "triangle")]
    rows = {q["id"]: tuple(q["answers"]) for q in data["questions"]}
    assert rows == {"blue": (True, True, False), "triangle": (False, True, True), "listed": (True, True, True)}
    subsets = ((), (0,), (1,), (0, 1))
    pair_checks = 0
    for bits in product((False, True), repeat=6):
        table = (bits[:3], bits[3:])
        for selected in subsets:
            pair_checks += check_encoding(table, selected)
    return {"three_item_two_question_tables": 64, "replayed_histories": 256, "pair_comparisons": pair_checks}


if __name__ == "__main__":
    print(json.dumps(check(), sort_keys=True))
