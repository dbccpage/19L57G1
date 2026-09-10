"""Tests for bounded specialization recovering historical 1,459-history prefix case.

Verifies that the generalized typed translation framework recovers the exact
1,459 valid history prefixes from research/typed_translation/, tests refusal
preservation on invalid historical replay events, and asserts commutation.

AuthorityEffect: None.
"""

from __future__ import annotations

import pytest

from specialization import (
    EVENT_ORDER,
    HistoricalEvent,
    accepts,
    enumerate_specialized_histories,
    initial_replay,
    step_replay,
    verify_specialization_recovery,
)


def test_specialization_recovers_exact_1459_histories() -> None:
    """Bounded specialization yields exactly 1,459 valid prefix histories."""
    metrics = verify_specialization_recovery()

    assert metrics["histories_count"] == 1459
    assert metrics["unique_structures_count"] == 22
    assert metrics["step_commutations_tested"] == 1396
    assert metrics["roundtrip_all_passed"] is True


def test_specialization_matches_historical_census() -> None:
    """Specialized prefix histories match the historical implementation from research/typed_translation/."""
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent.parent.parent
    code_path = root / "research" / "typed_translation" / "code"
    if str(code_path) not in sys.path:
        sys.path.insert(0, str(code_path))
    try:
        from typed_translation.enumerate import (
            enumerate_histories as historical_enumerate,
        )
    except ImportError:
        pytest.skip("Historical typed_translation module not importable")

    hist_histories = historical_enumerate()
    spec_histories = enumerate_specialized_histories()

    assert len(spec_histories) == len(hist_histories)
    assert len(spec_histories) == 1459

    # Check that each history matches event-for-event by value
    for h_spec, h_hist in zip(spec_histories, hist_histories):
        spec_vals = tuple(e.value for e in h_spec)
        hist_vals = tuple(e.value for e in h_hist)
        assert spec_vals == hist_vals


def test_specialization_refusal_guards() -> None:
    """Specialized replay machine properly refuses illegal transitions."""
    replay = initial_replay()

    # Cannot admit without supply
    assert not accepts(replay, HistoricalEvent.ADMIT_D0)
    assert not accepts(replay, HistoricalEvent.ADMIT_D1)

    # Cannot admit instance without form
    assert not accepts(replay, HistoricalEvent.ADMIT_INST0)
    assert not accepts(replay, HistoricalEvent.ADMIT_INST1)

    # Cannot admit rule without form
    assert not accepts(replay, HistoricalEvent.ADMIT_RULE)

    # Supply D0
    r1 = step_replay(replay, HistoricalEvent.SUPPLY_D0)
    # Cannot supply D0 again
    assert not accepts(r1, HistoricalEvent.SUPPLY_D0)
    with pytest.raises(ValueError):
        step_replay(r1, HistoricalEvent.SUPPLY_D0)

    # Admit D0
    r2 = step_replay(r1, HistoricalEvent.ADMIT_D0)
    # Still cannot admit inst0 because form is not admitted
    assert not accepts(r2, HistoricalEvent.ADMIT_INST0)

    # Admit Form
    r3 = step_replay(r2, HistoricalEvent.ADMIT_FORM)
    # Now inst0 is admissible
    assert accepts(r3, HistoricalEvent.ADMIT_INST0)
    # But inst1 is not admissible (d1 not admitted yet)
    assert not accepts(r3, HistoricalEvent.ADMIT_INST1)
