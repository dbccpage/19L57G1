"""The estate census must notice a verifier disappearing as well as failing."""

from __future__ import annotations

import json

from ci import check_tree_custody


def test_pinned_population_matches_the_research_tree_files() -> None:
    pin = json.loads(check_tree_custody.PIN.read_text(encoding="utf-8"))
    found = {f"{tree}/{name}" for tree, name in check_tree_custody.verifiers()}
    assert set(pin["verifiers"]) == found
    assert len(pin["verifiers"]) == len(found)


def test_removed_passing_verifier_is_not_silent() -> None:
    pin: dict[str, object] = {
        "verifiers": ["green/verify_pins.py", "red/verify_pins.py"],
        "expected_failures": {"red/verify_pins.py": "known failure"},
    }
    outcomes: dict[str, dict[str, object]] = {
        "red/verify_pins.py": {"exit": 1, "line": "known failure"},
    }
    assert check_tree_custody.compare(outcomes, pin) == [
        "MISSING VERIFIER: green/verify_pins.py is pinned but was not run"
    ]


def test_new_passing_verifier_requires_a_pin_update() -> None:
    pin: dict[str, object] = {
        "verifiers": ["known/verify_pins.py"],
        "expected_failures": {},
    }
    outcomes: dict[str, dict[str, object]] = {
        "known/verify_pins.py": {"exit": 0, "line": "ok"},
        "new/verify_pins.py": {"exit": 0, "line": "ok"},
    }
    assert check_tree_custody.compare(outcomes, pin) == [
        "NEW VERIFIER: new/verify_pins.py ran but is not pinned"
    ]
