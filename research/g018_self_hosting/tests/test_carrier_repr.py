"""Tests for carrier representation and state graph encoding inside the carrier."""

from __future__ import annotations

import pytest

from carrier_repr import (
    CarrierEncodingError,
    MachineSpec,
    MachineState,
    Transition,
    decode_carrier,
    encode_carrier,
    run_direct,
    step_direct,
)


def test_transition_serialization_roundtrip() -> None:
    t = Transition(curr_state=3, read_sym=1, next_state=7, write_sym=2, move_cursor=-1, halt=False)
    serialized = t.serialize()
    deserialized = Transition.deserialize(serialized)
    assert deserialized == t


def test_transition_validation_refusals() -> None:
    with pytest.raises(CarrierEncodingError, match="curr_state"):
        Transition(curr_state=-1, read_sym=0, next_state=0, write_sym=0, move_cursor=0, halt=False)

    with pytest.raises(CarrierEncodingError, match="read_sym"):
        Transition(curr_state=0, read_sym=-2, next_state=0, write_sym=0, move_cursor=0, halt=False)

    with pytest.raises(CarrierEncodingError, match="move_cursor"):
        Transition(curr_state=0, read_sym=0, next_state=0, write_sym=0, move_cursor=2, halt=False)


def test_machine_spec_determinism_refusal() -> None:
    t1 = Transition(curr_state=0, read_sym=1, next_state=1, write_sym=0, move_cursor=1, halt=False)
    t2 = Transition(curr_state=0, read_sym=1, next_state=2, write_sym=1, move_cursor=0, halt=True)
    with pytest.raises(CarrierEncodingError, match="Non-deterministic"):
        MachineSpec(transitions=(t1, t2))


def test_carrier_encode_decode_roundtrip() -> None:
    spec = MachineSpec(
        transitions=(
            Transition(0, 0, 1, 1, 1, False),
            Transition(1, 0, 2, 2, -1, False),
            Transition(2, 1, 3, 0, 0, True),
        ),
        default_sym=0,
    )
    state = MachineState(state=0, cursor=2, tape=(0, 1, 0, 4), fuel=50, halted=False)

    encoded = encode_carrier(spec, state)
    assert isinstance(encoded, tuple)
    assert all(isinstance(x, int) and x >= 0 for x in encoded)

    dec_spec, dec_state = decode_carrier(encoded)
    assert dec_spec == spec
    assert dec_state == state


def test_carrier_decode_malformed_refusal() -> None:
    # Truncated data
    with pytest.raises(CarrierEncodingError):
        decode_carrier((1001, 0))

    # Corrupt tag
    with pytest.raises(CarrierEncodingError, match="Expected tag"):
        decode_carrier((9999, 0, 0, 1003, 1004, 0, 1005, 0, 1006, 0, 1007, 1008, 0, 1009, 0, 1010))


def test_direct_execution_counter() -> None:
    # A 3-step counter: state 0 -> 1 -> 2 -> halt
    spec = MachineSpec(
        transitions=(
            Transition(0, 0, 1, 1, 1, False),
            Transition(1, 0, 2, 1, 1, False),
            Transition(2, 0, 3, 1, 0, True),
        )
    )
    init_state = MachineState(state=0, cursor=0, tape=(), fuel=10, halted=False)

    s1 = step_direct(spec, init_state)
    assert s1.state == 1
    assert s1.cursor == 1
    assert s1.tape == (1,)
    assert s1.fuel == 9
    assert not s1.halted

    s2 = step_direct(spec, s1)
    assert s2.state == 2
    assert s2.cursor == 2
    assert s2.tape == (1, 1)
    assert s2.fuel == 8
    assert not s2.halted

    s3 = step_direct(spec, s2)
    assert s3.state == 3
    assert s3.cursor == 2
    assert s3.tape == (1, 1, 1)
    assert s3.fuel == 7
    assert s3.halted

    # Stepping a halted machine is an identity
    s4 = step_direct(spec, s3)
    assert s4 == s3


def test_direct_execution_fuel_exhaustion() -> None:
    # Infinite cycler with fuel 5
    spec = MachineSpec(
        transitions=(
            Transition(0, 0, 1, 0, 0, False),
            Transition(1, 0, 0, 0, 0, False),
        )
    )
    init_state = MachineState(state=0, cursor=0, tape=(0,), fuel=5, halted=False)
    final_state = run_direct(spec, init_state)
    assert final_state.fuel == 0
    assert not final_state.halted
