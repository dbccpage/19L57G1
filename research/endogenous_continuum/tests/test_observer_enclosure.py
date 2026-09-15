"""Tests for Track 1: Endogenous Observer Enclosure.

AuthorityEffect: None.

Verifies:
1. Localized stepping updates carrier state and appends internal records.
2. Trace invariant verification holds over multi-step paths.
3. Detection and rejection of retrocausal tampering and history rewriting.
4. Exact trace length, step count, and state correspondence.
5. Strict typing, exact integer arithmetic, and absence of floating-point values.
"""

from __future__ import annotations

import pytest

from research.endogenous_continuum.observer_enclosure import (
    AdmissionError,
    EnclosedCarrier,
    InternalTrace,
    LocalAdmitDatum,
    LocalAdmitForm,
    LocalAdmitInst,
    LocalAdmitRuleAll,
    LocalEvalDerivable,
    LocalImpose,
    LocalizedTransition,
    LocalObserveProfile,
    LocalRegisterAdd,
    LocalRegisterWrite,
    LocalSeparabilityCheck,
    ObserverRecord,
    TraceInvariantChecker,
    compute_carrier_digest,
    compute_record_hash,
)


def test_genesis_carrier_initialization() -> None:
    """Verify genesis enclosed carrier initializes with empty trace and zeroed state."""
    carrier = EnclosedCarrier.genesis(num_registers=4)
    assert carrier.step_count == 0
    assert carrier.trace.length == 0
    assert carrier.trace.latest is None
    assert carrier.local_registers == (0, 0, 0, 0)
    assert len(carrier.regime.data) == 0
    assert carrier.trace.is_valid_chain() is True

    digest = carrier.carrier_digest()
    assert isinstance(digest, str)
    assert len(digest) == 64

    with pytest.raises(ValueError, match="non-negative"):
        EnclosedCarrier.genesis(num_registers=-1)


def test_hash_serialization_is_unambiguous_and_empty_path_fails_closed() -> None:
    digest = "0" * 64
    first = compute_record_hash(0, "kind", ("a,b",), (1,), digest, "GENESIS")
    second = compute_record_hash(0, "kind", ("a", "b"), (1,), digest, "GENESIS")
    assert first != second

    empty_result = TraceInvariantChecker.check_carrier_path([])
    assert not empty_result.valid
    assert empty_result.steps_verified == 0


def test_localized_transition_inputs_reject_non_integer_values() -> None:
    with pytest.raises(TypeError, match="must be an int"):
        LocalRegisterWrite(register_index=True, value=1)
    with pytest.raises(TypeError, match="must be an int"):
        LocalRegisterWrite(register_index=0, value=1.5)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="tuple of ints"):
        LocalAdmitInst(form=0, args=(True,))


def test_localized_stepping_updates_carrier_and_appends_record() -> None:
    """Verify localized transitions update carrier and monotonically append internal records."""
    c0 = EnclosedCarrier.genesis()

    # Step 1: Admit datum d0
    t1 = LocalAdmitDatum("d0")
    c1 = c0.step_localized(t1)
    assert c1.step_count == 1
    assert c1.trace.length == 1
    assert c1.regime.data == ("d0",)

    rec1 = c1.trace.latest
    assert rec1 is not None
    assert rec1.step == 0
    assert rec1.transition_kind == "LOCAL_ADMIT_DATUM"
    assert rec1.local_input == ("d0",)
    assert rec1.local_readout == (1,)
    assert rec1.prev_record_hash == "GENESIS"
    assert rec1.verify_integrity() is True
    assert rec1.state_digest == c1.carrier_digest()

    res1 = TraceInvariantChecker.check_step_transition(c0, c1, t1)
    assert res1.valid is True
    assert len(res1.violations) == 0

    # Step 2: Admit datum d1
    t2 = LocalAdmitDatum("d1")
    c2 = c1.step_localized(t2)
    assert c2.step_count == 2
    assert c2.trace.length == 2
    assert c2.regime.data == ("d0", "d1")

    rec2 = c2.trace.latest
    assert rec2 is not None
    assert rec2.step == 1
    assert rec2.prev_record_hash == rec1.record_hash
    assert rec2.verify_integrity() is True
    assert rec2.state_digest == c2.carrier_digest()

    res2 = TraceInvariantChecker.check_step_transition(c1, c2, t2)
    assert res2.valid is True


def test_internal_observation_and_derivability() -> None:
    """Verify localized internal evaluation of derivability without mutating carrier regime."""
    c = EnclosedCarrier.genesis()
    c = c.step_localized(LocalAdmitDatum("x"))
    c = c.step_localized(LocalAdmitDatum("y"))
    c = c.step_localized(LocalAdmitForm(1))
    c = c.step_localized(LocalAdmitInst(form=0, args=(0,)))

    regime_before = c.regime

    # Evaluate derivable instance (0, (0,))
    t_eval_true = LocalEvalDerivable(form=0, args=(0,))
    c_after_true = c.step_localized(t_eval_true)
    assert c_after_true.regime == regime_before
    assert c_after_true.trace.latest is not None
    assert c_after_true.trace.latest.local_readout == (1,)

    # Evaluate non-derivable instance (0, (1,))
    t_eval_false = LocalEvalDerivable(form=0, args=(1,))
    c_after_false = c_after_true.step_localized(t_eval_false)
    assert c_after_false.regime == regime_before
    assert c_after_false.trace.latest is not None
    assert c_after_false.trace.latest.local_readout == (0,)


def test_internal_profile_and_separability_observation() -> None:
    """Verify internal observer computes profiles and separability status locally."""
    c = EnclosedCarrier.genesis()
    c = c.step_localized(LocalAdmitDatum("a"))
    c = c.step_localized(LocalAdmitDatum("b"))
    c = c.step_localized(LocalAdmitForm(1))
    c = c.step_localized(LocalAdmitInst(form=0, args=(0,)))

    # Profile observation for datum 0
    t_prof0 = LocalObserveProfile(datum=0)
    c = c.step_localized(t_prof0)
    prof0_readout = c.trace.latest.local_readout if c.trace.latest else ()

    # Profile observation for datum 1
    t_prof1 = LocalObserveProfile(datum=1)
    c = c.step_localized(t_prof1)
    prof1_readout = c.trace.latest.local_readout if c.trace.latest else ()

    # Profiles must differ because form 0 instance holds for datum 0 but not datum 1
    assert prof0_readout != prof1_readout

    # Separability check between 0 and 1
    t_sep = LocalSeparabilityCheck(i=0, j=1)
    c = c.step_localized(t_sep)
    assert c.trace.latest is not None
    assert c.trace.latest.local_readout == (1,)

    # Separation requirement imposition
    t_imp = LocalImpose(i=0, j=1)
    c = c.step_localized(t_imp)
    assert (0, 1) in c.regime.reqs


def test_internal_registers_exact_arithmetic() -> None:
    """Verify internal register manipulation maintains exact integer arithmetic."""
    c = EnclosedCarrier.genesis(num_registers=4)
    c = c.step_localized(LocalRegisterWrite(register_index=0, value=100))
    assert c.local_registers == (100, 0, 0, 0)

    c = c.step_localized(LocalRegisterWrite(register_index=1, value=25))
    assert c.local_registers == (100, 25, 0, 0)

    c = c.step_localized(LocalRegisterAdd(target_index=0, source_index=1))
    assert c.local_registers == (125, 25, 0, 0)
    assert c.trace.latest is not None
    assert c.trace.latest.local_readout == (0, 125)

    for val in c.local_registers:
        assert isinstance(val, int)
        assert not isinstance(val, float)


def test_trace_invariant_verification_over_multistep_path() -> None:
    """Verify that internal trace invariants hold across a comprehensive multi-step path."""
    transitions: list[LocalizedTransition] = [
        LocalAdmitDatum("d0"),
        LocalAdmitDatum("d1"),
        LocalAdmitDatum("d2"),
        LocalAdmitForm(arity=1),
        LocalAdmitForm(arity=2),
        LocalAdmitInst(form=0, args=(0,)),
        LocalAdmitInst(form=1, args=(0, 1)),
        LocalEvalDerivable(form=0, args=(0,)),
        LocalEvalDerivable(form=0, args=(1,)),
        LocalObserveProfile(datum=0),
        LocalObserveProfile(datum=1),
        LocalSeparabilityCheck(i=0, j=1),
        LocalRegisterWrite(register_index=2, value=7),
        LocalRegisterAdd(target_index=2, source_index=2),
        LocalAdmitRuleAll(form=0),
        LocalEvalDerivable(form=0, args=(1,)),  # now derivable via all-tuples rule
    ]

    path: list[EnclosedCarrier] = [EnclosedCarrier.genesis()]
    for t in transitions:
        path.append(path[-1].step_localized(t))

    assert len(path) == len(transitions) + 1

    # Invariant verification across whole path
    result = TraceInvariantChecker.check_carrier_path(path, transitions)
    assert result.valid is True
    assert result.steps_verified == len(transitions)
    assert len(result.violations) == 0

    # Verify exact length and state correspondence for each carrier in path
    for k, carrier in enumerate(path):
        assert carrier.step_count == k
        assert carrier.trace.length == k
        if k > 0:
            rec = carrier.trace.records[k - 1]
            assert rec.step == k - 1
            assert rec.state_digest == carrier.carrier_digest()


def test_rejection_of_retrocausal_tampering() -> None:
    """Verify that any retroactive mutation of past trace entries breaks invariant checks."""
    c = EnclosedCarrier.genesis()
    c = c.step_localized(LocalAdmitDatum("token0"))
    c = c.step_localized(LocalAdmitDatum("token1"))
    c = c.step_localized(LocalAdmitForm(1))
    c = c.step_localized(LocalAdmitInst(0, (0,)))

    assert c.trace.length == 4
    assert c.trace.is_valid_chain() is True

    # Tampering Attack 1: Modify past record readout without changing hash
    orig_rec1 = c.trace.records[1]
    tampered_rec1 = ObserverRecord(
        step=orig_rec1.step,
        transition_kind=orig_rec1.transition_kind,
        local_input=orig_rec1.local_input,
        local_readout=(999,),  # altered readout
        state_digest=orig_rec1.state_digest,
        prev_record_hash=orig_rec1.prev_record_hash,
        record_hash=orig_rec1.record_hash,
    )
    tampered_records = list(c.trace.records)
    tampered_records[1] = tampered_rec1
    tampered_trace = InternalTrace(tuple(tampered_records))

    assert tampered_trace.is_valid_chain() is False
    check_res = TraceInvariantChecker.check_trace_integrity(tampered_trace)
    assert check_res.valid is False

    # Tampering Attack 2: Modify past record and update its record_hash
    rehashed_rec1 = ObserverRecord.create(
        step=orig_rec1.step,
        transition_kind=orig_rec1.transition_kind,
        local_input=orig_rec1.local_input,
        local_readout=(999,),
        state_digest=orig_rec1.state_digest,
        prev_record_hash=orig_rec1.prev_record_hash,
    )
    tampered_records2 = list(c.trace.records)
    tampered_records2[1] = rehashed_rec1
    tampered_trace2 = InternalTrace(tuple(tampered_records2))

    # The chain breaks at record 2 because record 2's prev_record_hash does not match
    assert tampered_trace2.is_valid_chain() is False

    # Tampering Attack 3: Truncating history
    truncated_trace = InternalTrace(c.trace.records[:2])
    assert c.trace.is_monotone_extension_of(truncated_trace) is True
    # Truncated trace is not a valid extension of c.trace
    assert truncated_trace.is_monotone_extension_of(c.trace) is False


def test_rejection_of_external_history_rewriting() -> None:
    """Verify that forged carrier state digests are rejected by step verification."""
    c0 = EnclosedCarrier.genesis()
    t = LocalAdmitDatum("alpha")
    c1 = c0.step_localized(t)

    # Construct carrier with mismatched state digest in record
    bad_record = ObserverRecord.create(
        step=0,
        transition_kind=t.action_type,
        local_input=t.parameters_repr(),
        local_readout=(1,),
        state_digest="0000000000000000000000000000000000000000000000000000000000000000",
        prev_record_hash="GENESIS",
    )
    c1_tampered = EnclosedCarrier(
        regime=c1.regime,
        trace=InternalTrace((bad_record,)),
        local_registers=c1.local_registers,
        step_count=c1.step_count,
    )

    res = TraceInvariantChecker.check_step_transition(c0, c1_tampered, t)
    assert res.valid is False
    assert any("digest" in v for v in res.violations)


def test_absence_of_external_prefix_inspection() -> None:
    """Verify that localized rewrite evaluation depends strictly on current carrier state."""
    # Path A: admit d0, admit d1, write reg 0 = 5
    cA = EnclosedCarrier.genesis()
    cA = cA.step_localized(LocalAdmitDatum("d0"))
    cA = cA.step_localized(LocalAdmitDatum("d1"))
    cA = cA.step_localized(LocalRegisterWrite(0, 5))

    # Path B: admit d1, admit d0, write reg 0 = 5 (reaches same data set and register)
    cB = EnclosedCarrier.genesis()
    cB = cB.step_localized(LocalAdmitDatum("d1"))
    cB = cB.step_localized(LocalAdmitDatum("d0"))
    cB = cB.step_localized(LocalRegisterWrite(0, 5))

    # Both carriers have identical data set and register values (order of admission tokens differs)
    # Testing a localized transition that checks derivability of a new form
    t_form = LocalAdmitForm(arity=1)
    next_cA = cA.step_localized(t_form)
    next_cB = cB.step_localized(t_form)

    # Local readout must be identical for both paths
    assert next_cA.trace.latest is not None
    assert next_cB.trace.latest is not None
    assert next_cA.trace.latest.local_readout == next_cB.trace.latest.local_readout


def test_invalid_transitions_raise_admission_error() -> None:
    """Verify that invalid transitions raise proper errors without altering carrier state."""
    c = EnclosedCarrier.genesis()

    # Form arity < 1
    with pytest.raises(AdmissionError):
        c.step_localized(LocalAdmitForm(0))

    # Instance with unknown form
    with pytest.raises(AdmissionError):
        c.step_localized(LocalAdmitInst(form=99, args=(0,)))

    # Register index out of range
    with pytest.raises(IndexError):
        c.step_localized(LocalRegisterWrite(register_index=99, value=1))

    # Trace remains untouched
    assert c.trace.length == 0
    assert c.step_count == 0
