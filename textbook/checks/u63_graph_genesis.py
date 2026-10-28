"""Check script for Unit 63: Where new occurrences come from (GraphGenesis).

Recomputes and verifies:
  1. Event partition (4 supply + 4 internal + 3 control = 11 constructors;
     response events = internal + setBudget).
  2. Field invariance battery, internal trace carrier invariance, and nextFamilyP
     block shape / graph-store fixation across the 8 sample states.
  3. ProposalRecord obligations, no-authority check, S_3 renaming transport,
     and equal-cost non-isomorphic tie retention on tri = tree_at(path_pol, 2).
  4. Part-3 demand separation and student exercise on blind_pair().
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.attachment_ladder import up_block  # noqa: E402
from derivation.graph_genesis import (  # noqa: E402
    ALL_KINDS,
    CONTROL_KINDS,
    INTERNAL_KINDS,
    SUPPLY_KINDS,
    blind_pair,
    family_report,
    field_invariance_report,
    graph_stores_fixed,
    internal_fragment_report,
    part3_report,
    proposal_report,
    tie_report,
    transport_report,
)
from derivation.primitive_passage import (  # noqa: E402
    next_family_p,
    obst_p,
    preplay,
)


def main() -> int:
    failures: list[str] = []

    # 1. Partition check
    if len(SUPPLY_KINDS) != 4 or len(INTERNAL_KINDS) != 4 or len(CONTROL_KINDS) != 3:
        failures.append("unexpected kind tuple sizes")
    if len(ALL_KINDS) != 11:
        failures.append(f"expected 11 ALL_KINDS, got {len(ALL_KINDS)}")

    # 2. Field invariance, internal fragment, and family reports
    fields = field_invariance_report(probe=1)
    if not (
        fields["refineCol_only_obs"]
        and fields["addCol_only_obs"]
        and fields["internal_events_fix_graph_stores"]
        and fields["response_events_fix_graph_stores"]
        and fields["graph_fields_move_only_under_supply"]
        and fields["every_supply_kind_moves_a_graph_store"]
    ):
        failures.append(f"field_invariance_report failed: {fields}")

    frag = internal_fragment_report(max_len=2, probe=1)
    if not frag["all_graph_stores_fixed"]:
        failures.append("internal_fragment_report reported graph store mutation")

    fam = family_report()
    if not (
        fam["every_block_has_a_declared_shape"]
        and fam["family_ranges_over_existing_carrier"]
        and fam["family_blocks_are_response_events"]
        and fam["family_blocks_fix_graph_stores"]
    ):
        failures.append(f"family_report failed: {fam}")

    # 3. ProposalRecord, transport, and tie reports
    props = proposal_report()
    if not (
        props["carries_no_authority_field"]
        and props["all_obligations_discharged"]
        and props["execution_is_separately_gated"]
    ):
        failures.append("proposal_report failed")

    trans = transport_report(carrier=3)
    if not (
        trans["act_up_comm_all_perms"]
        and trans["transported_block_is_complete_member"]
        and trans["cost_invariant_under_renaming"]
        and trans["transported_obligations_discharged"]
    ):
        failures.append("transport_report failed")

    ties = tie_report()
    if not (
        ties["equal_cost"]
        and ties["blocks_differ"]
        and ties["both_complete_members"]
        and ties["executions_non_isomorphic"]
        and ties["cost"] == 4
    ):
        failures.append(f"tie_report failed: {ties}")

    # 4. Part 3 and student exercise on blind_pair
    part3 = part3_report()
    if not (
        part3["family_nonempty"]
        and part3["every_response_resolves"]
        and part3["every_response_fixes_graph_stores"]
        and part3["no_response_grows_the_carrier"]
        and part3["every_obstruction_resolved_in_carrier"]
    ):
        failures.append("part3_report failed")

    bp = blind_pair()
    if not obst_p(bp, 0, 1):
        failures.append("expected obst_p(blind_pair, 0, 1) == True")
    nf_bp = next_family_p(bp)
    if len(nf_bp) != 2:
        failures.append(f"expected 2 blocks in next_family_p(blind_pair), got {len(nf_bp)}")
    b0 = nf_bp[0]
    after_b0 = preplay(b0, bp)
    if after_b0.occ != (0, 1) or after_b0.obs != ((0,),) or obst_p(after_b0, 0, 1):
        failures.append(f"unexpected replay of head block on blind_pair: {after_b0}")
    if not graph_stores_fixed(bp, after_b0):
        failures.append("head block on blind_pair mutated a graph store")
    after_up = preplay(up_block(bp, 0), bp)
    if after_up.occ != (0, 1, 2) or after_up.obs != ():
        failures.append(f"unexpected replay of up_block(blind_pair, 0): {after_up}")

    result = {
        "unit": 63,
        "module": "GraphGenesis",
        "field_invariance_checks": fields["total_checks"],
        "internal_traces_checked": frag["traces_checked"],
        "transport_checks": trans["checks"],
        "tie_cost": ties["cost"],
        "blind_pair_blocks": len(nf_bp),
        "failures": failures,
    }
    print(json.dumps(result, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
