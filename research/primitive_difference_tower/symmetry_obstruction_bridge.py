"""Deterministic report for the finite symmetry--obstruction--repair bridge.

The report is a replayable assessment of one explicitly supplied fixture.  It
does not derive its carrier, swap, repair table, residual, anchor imports, or
continuation grammar from the sealed source interface.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

from bridge_contract import Origin, Provenance, two_coordinate_contract
from continuation_trilemma import (
    AnchoredContinuation,
    Continuation,
    RefusedContinuation,
    RetainedOrbitContinuation,
    declared_continuations,
    is_swap_stable,
)
from equivariant_selection import (
    AnchoredSingletonChoice,
    anchored_singleton_choice,
    is_equivariant_singleton_choice,
    no_equivariant_residual_singleton_choice,
    residual_singleton_choices,
)
from repair_obstruction import certify_declared_repair_obstruction
from verify_lean import BRIDGE_AXIOM_REPORT_DECLARATIONS


REPORT_SCHEMA = "primitive_difference_tower_symmetry_obstruction_bridge/v1"
REPORT_SCOPE = (
    "A deterministic assessment of one declared two-coordinate fixture; "
    "not a native-stage bridge, a general cohomology result, or a physical claim."
)


def displayed_anchor_imports() -> tuple[AnchoredSingletonChoice, ...]:
    """State the two labelled imports used to display tied singleton branches."""

    contract = two_coordinate_contract()
    return (
        anchored_singleton_choice(
            contract,
            (1, 0),
            Provenance("left-coordinate-anchor", Origin.ADMITTED),
        ),
        anchored_singleton_choice(
            contract,
            (0, 1),
            Provenance("right-coordinate-anchor", Origin.ADMITTED),
        ),
    )


def bridge_report() -> dict[str, Any]:
    """Rebuild the complete finite bridge assessment from its declared inputs."""

    contract = two_coordinate_contract()
    anchors = displayed_anchor_imports()
    certificate = certify_declared_repair_obstruction(contract)
    continuations = declared_continuations(
        contract,
        anchors,
        "withhold a free singleton under the declared swap",
    )
    anchored = tuple(
        continuation
        for continuation in continuations
        if isinstance(continuation, AnchoredContinuation)
    )
    singleton_choices = residual_singleton_choices(contract)
    singleton_equivariance = {
        str(list(choice)): is_equivariant_singleton_choice(contract, choice)
        for choice in singleton_choices
    }
    continuation_data = [
        {
            "continuation": continuation.to_data(),
            "selected_singleton": (
                list(continuation.selection.choice)
                if isinstance(continuation, AnchoredContinuation)
                else None
            ),
            "swap_stable": is_swap_stable(contract, continuation),
        }
        for continuation in continuations
    ]
    return {
        "checks": {
            "anchored_branches_are_explicit_imports": all(
                continuation.selection.anchor.origin is Origin.ADMITTED
                for continuation in anchored
            ),
            "declared_repair_obstruction": certificate.excludes_every_declared_potential,
            "full_orbit_is_retained": any(
                isinstance(continuation, RetainedOrbitContinuation)
                and continuation.members == contract.residual_orbit
                and is_swap_stable(contract, continuation)
                for continuation in continuations
            ),
            "no_equivariant_residual_singleton": no_equivariant_residual_singleton_choice(
                contract
            ),
            "refusal_has_no_singleton": any(
                isinstance(continuation, RefusedContinuation)
                and is_swap_stable(contract, continuation)
                for continuation in continuations
            ),
            "tied_anchor_branches_retained": len(anchored) == len(anchors),
        },
        "contract": contract.to_data(),
        "continuations": continuation_data,
        "lean_axiom_inventory": list(BRIDGE_AXIOM_REPORT_DECLARATIONS),
        "repair_obstruction": certificate.to_data(),
        "schema": REPORT_SCHEMA,
        "scope": REPORT_SCOPE,
        "selection": {
            "anchored_imports": [anchor.to_data() for anchor in anchors],
            "residual_singleton_choices": [list(choice) for choice in singleton_choices],
            "singleton_equivariance": singleton_equivariance,
        },
    }


def render_bridge_report() -> bytes:
    """Render the assessment in deterministic UTF-8 bytes with an LF terminator."""

    return (
        json.dumps(bridge_report(), ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def bridge_report_sha256() -> str:
    """Return the uppercase SHA-256 of the deterministic report bytes."""

    return sha256(render_bridge_report()).hexdigest().upper()


def verify_bridge_report(payload: Mapping[str, Any]) -> bool:
    """Accept only the exact report regenerated from the declared fixture."""

    return dict(payload) == bridge_report()


def write_bridge_report(output: Path) -> None:
    """Write the deterministic bridge report, creating its parent if needed."""

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(render_bridge_report())
