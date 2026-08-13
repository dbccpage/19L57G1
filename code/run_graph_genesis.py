"""Produce the graph-genesis artifact deterministically.

Usage: python code/run_graph_genesis.py [--artifacts DIR]
       [--trace-len N] [--carrier C] [--probe P]

Writes ``graph_genesis.json``: the exhaustive field-invariance
battery on the declared sample states (the two response events move
only the observation and the budget; the four graph stores move only
under supply events); the internal fragment's carrier invariance
over every trace up to the declared length; the represented
next-event family's block shapes, range over the existing carrier
and graph-store invariance; the proposal record with every
obligation discharged as a computable check and no authority field;
transport of the proposal family over the FULL permutation group on
the declared carrier; the equal-cost non-isomorphic tie the family
retains; and the Part-3 witness with the irreducibility verdict —
an active obstruction never requests the carrier-changing lift, so
the growth demand is a separately declared premise."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import Json, write_json
from derivation.graph_genesis import (
    ALL_KINDS,
    field_invariance_report,
    family_report,
    internal_fragment_report,
    part3_report,
    proposal_report,
    sample_states,
    tie_report,
    transport_report,
)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path,
                        default=Path("artifacts"))
    parser.add_argument("--trace-len", type=int, default=2)
    parser.add_argument("--carrier", type=int, default=3)
    parser.add_argument("--probe", type=int, default=1)
    args = parser.parse_args(argv)
    fields = field_invariance_report(args.probe)
    frag = internal_fragment_report(args.trace_len, args.probe)
    props = proposal_report()
    trans = transport_report(args.carrier)
    ties = tie_report()
    lift = part3_report()
    payload: dict[str, Json] = {
        "bounds": {
            "sample_states": len(sample_states()),
            "sample_state_names": [n for n, _ in sample_states()],
            "event_kinds": list(ALL_KINDS),
            "probe_past_carrier": args.probe,
            "internal_trace_length": args.trace_len,
            "transport_carrier": args.carrier,
            "tie_carrier": 4,
            "column_size_bound": 2,
        },
        "imported_inputs": [
            "fresh occurrence supply (canonical next numeral)",
            "protection", "budget/activation (declared, never "
            "carried by a proposal record)",
            "the declared one-edge grammar",
            "metatheoretic driver iteration",
        ],
        "field_invariance": fields,
        "internal_fragment": frag,
        "family": family_report(),
        "proposals": props,
        "transport": trans,
        "ties": ties,
        "obstruction_lift": lift,
    }
    out_path = args.artifacts / "graph_genesis.json"
    write_json(out_path, payload)
    print(f"field invariance ({fields['total_checks']} checks): "
          f"refine={fields['refineCol_only_obs']} "
          f"addCol={fields['addCol_only_obs']} "
          f"supply-only={fields['graph_fields_move_only_under_supply']}")
    print(f"internal traces {frag['traces_checked']}: "
          f"graph fixed={frag['all_graph_stores_fixed']}")
    print(f"proposals: obligations="
          f"{props['all_obligations_discharged']} "
          f"no-authority={props['carries_no_authority_field']}")
    print(f"transport over {trans['permutation_group_size']} "
          f"renamings: comm={trans['act_up_comm_all_perms']} "
          f"cost={trans['cost_invariant_under_renaming']}")
    print(f"tie retained: equal_cost={ties['equal_cost']} "
          f"non_isomorphic={ties['executions_non_isomorphic']}")
    print(f"obstruction lift: resolves="
          f"{lift['every_response_resolves']} "
          f"no_growth={lift['no_response_grows_the_carrier']}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
