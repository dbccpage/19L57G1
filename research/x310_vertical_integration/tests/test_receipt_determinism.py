"""Cryptographic receipt determinism and tamper-evidence test suite.

Target X310: Vertical Integration Chain
Enforces byte-pinned reproducibility, zero float serialization, and strict
tamper-evidence across all six integrated estate layers.
"""

from __future__ import annotations

import copy
from fractions import Fraction
import json
from typing import Any
import pytest

from pathlib import Path
import sys

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
_CODE_DIR = _REPO_ROOT / "code"
if str(_CODE_DIR) not in sys.path:
    sys.path.insert(0, str(_CODE_DIR))

for _sub in [
    "target_a_execution",
    "g011_finitary_substrate",
    "p200_operational_protocols",
    "g014_observer_descent",
    "x301_formal_semantics",
    "m114_solver_adapter",
    "x302_operational_reasoning",
    "x303_bounded_agency",
]:
    _sub_path = _REPO_ROOT / "research" / _sub
    if str(_sub_path) not in sys.path:
        sys.path.insert(0, str(_sub_path))

import research.target_a_execution.runner as _tar_runner
sys.modules["runner"] = _tar_runner
import research.p200_operational_protocols.protocol as _p200_prot
sys.modules["protocol"] = _p200_prot
import research.p200_operational_protocols.embedded_observer as _p200_emb
sys.modules["embedded_observer"] = _p200_emb

from research.x310_vertical_integration.pipeline import (
    PipelineConfig,
    canonical_grand_receipt_digest,
    canonical_json_dumps,
    run_vertical_pipeline,
)
from research.target_a_execution.control import (
    Controlled,
    State as SubstrateState,
    encode_c,
)
from research.target_a_execution.runner import (
    ProtectionKind,
    ProtectionObligation,
)


def _assert_no_floats(obj: Any, path: str = "") -> None:
    """Recursively certify that zero floating-point numbers exist in receipt structures."""
    if isinstance(obj, float):
        raise AssertionError(f"Found float {obj} at path: {path}")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            _assert_no_floats(v, f"{path}.{k}" if path else str(k))
    elif isinstance(obj, (list, tuple)):
        for i, item in enumerate(obj):
            _assert_no_floats(item, f"{path}[{i}]")


def test_canonical_json_dumps_determinism():
    """Certify that canonical JSON serialization produces deterministic byte-pinned strings."""
    d1 = {"b": 2, "a": 1, "c": [3, 2, 1], "d": {"z": 10, "y": 20}}
    d2 = {"d": {"y": 20, "z": 10}, "c": [3, 2, 1], "a": 1, "b": 2}

    s1 = canonical_json_dumps(d1)
    s2 = canonical_json_dumps(d2)

    assert s1 == s2
    assert s1 == '{"a":1,"b":2,"c":[3,2,1],"d":{"y":20,"z":10}}'


def test_grand_receipt_sha256_reproducibility():
    """Certify that two independent runs with identical config produce bit-for-bit identical receipts."""
    cfg1 = PipelineConfig(run_id="DETERM-01", timestamp_fixed="2026-09-12T00:00:00Z")
    cfg2 = PipelineConfig(run_id="DETERM-01", timestamp_fixed="2026-09-12T00:00:00Z")

    res1 = run_vertical_pipeline(cfg1)
    res2 = run_vertical_pipeline(cfg2)

    assert res1.is_success
    assert res2.is_success
    assert res1.grand_receipt_sha256 == res2.grand_receipt_sha256
    assert res1.grand_receipt["grand_receipt_sha256"] == res2.grand_receipt["grand_receipt_sha256"]

    json1 = canonical_json_dumps(res1.grand_receipt)
    json2 = canonical_json_dumps(res2.grand_receipt)
    assert json1 == json2


def test_receipt_tamper_evidence_stage_mutation():
    """Certify that altering any bit in any stage receipt alters the computed grand receipt digest."""
    cfg = PipelineConfig(run_id="TAMPER-01", timestamp_fixed="2026-09-12T00:00:00Z")
    res = run_vertical_pipeline(cfg)

    original_digest = res.grand_receipt_sha256
    receipt_copy = copy.deepcopy(res.grand_receipt)

    # 1. Mutate Stage 1 receipt
    receipt_copy["stage_receipts"]["stage_1_substrate"]["fuel_remaining"] += 1
    mutated_digest_1 = canonical_grand_receipt_digest(receipt_copy)
    assert mutated_digest_1 != original_digest

    # Reset
    receipt_copy = copy.deepcopy(res.grand_receipt)

    # 2. Mutate Stage 4 solver receipt
    receipt_copy["stage_receipts"]["stage_4_solver"]["status"] = "INFEASIBLE_MUTATED"
    mutated_digest_4 = canonical_grand_receipt_digest(receipt_copy)
    assert mutated_digest_4 != original_digest

    # Reset
    receipt_copy = copy.deepcopy(res.grand_receipt)

    # 3. Mutate Stage 6 agency receipt
    receipt_copy["stage_receipts"]["stage_6_agency"]["selected_action"] = "tampered_action"
    mutated_digest_6 = canonical_grand_receipt_digest(receipt_copy)
    assert mutated_digest_6 != original_digest


def test_receipt_tamper_evidence_commutation_audit():
    """Certify that tampering with commutation audit outcomes invalidates the grand receipt."""
    cfg = PipelineConfig(run_id="TAMPER-02", timestamp_fixed="2026-09-12T00:00:00Z")
    res = run_vertical_pipeline(cfg)

    receipt_copy = copy.deepcopy(res.grand_receipt)
    receipt_copy["commutation_audit"]["readout_step_commutation"] = False
    mutated_digest = canonical_grand_receipt_digest(receipt_copy)

    assert mutated_digest != res.grand_receipt_sha256


def test_receipt_tamper_evidence_carrier_hash():
    """Certify that modifying initial or final carrier hash invalidates the grand receipt."""
    cfg = PipelineConfig(run_id="TAMPER-03", timestamp_fixed="2026-09-12T00:00:00Z")
    res = run_vertical_pipeline(cfg)

    receipt_copy = copy.deepcopy(res.grand_receipt)
    receipt_copy["initial_carrier_hash"] = "0" * 64
    mutated_digest = canonical_grand_receipt_digest(receipt_copy)

    assert mutated_digest != res.grand_receipt_sha256


def test_schema_conformity_and_zero_floats():
    """Certify schema keys conformity and strict absence of floating-point numbers."""
    cfg = PipelineConfig(run_id="SCHEMA-01", timestamp_fixed="2026-09-12T00:00:00Z")
    res = run_vertical_pipeline(cfg)

    gr = res.grand_receipt
    required_keys = {
        "schema",
        "receipt_version",
        "timestamp_utc",
        "pipeline_run_id",
        "initial_carrier_hash",
        "stage_receipts",
        "commutation_audit",
        "final_carrier_hash",
        "grand_receipt_sha256",
    }
    assert required_keys.issubset(gr.keys())
    assert gr["schema"] == "x310-vertical-integration-v1"
    assert gr["receipt_version"] == "1.0.0"

    # Strict zero float certification across entire nested receipt
    _assert_no_floats(gr)


def test_refusal_receipt_determinism_and_preservation():
    """Certify deterministic receipt and unmutated carrier hashes under refusal."""
    ctrl = frozenset({(0, 0), (1, 0)})
    c = Controlled(n=2, ops=((0, 0),), ctrl=ctrl)
    g = encode_c(c)
    obl = ProtectionObligation(kind=ProtectionKind.SEPARATED, u=0, v=1)
    s0 = SubstrateState(
        graph=g,
        nops=1,
        active=0,
        tape=(0,),
        clock=0,
        fuel=10,
        protection_obligations=(obl,),
    )

    cfg1 = PipelineConfig(run_id="REF-DET-01", timestamp_fixed="2026-09-12T00:00:00Z")
    cfg2 = PipelineConfig(run_id="REF-DET-01", timestamp_fixed="2026-09-12T00:00:00Z")

    res1 = run_vertical_pipeline(cfg1, controlled=c, initial_substrate=s0, op_index=0)
    res2 = run_vertical_pipeline(cfg2, controlled=c, initial_substrate=s0, op_index=0)

    assert res1.is_refusal
    assert res2.is_refusal
    assert res1.grand_receipt_sha256 == res2.grand_receipt_sha256

    gr = res1.grand_receipt
    assert gr["initial_carrier_hash"] == gr["final_carrier_hash"]
    _assert_no_floats(gr)
