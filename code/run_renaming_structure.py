"""Produce the renaming-structure artifact deterministically.

Usage: python code/run_renaming_structure.py [--artifacts DIR]
       [--carrier N]

Writes ``renaming_structure.json``: the group laws for identity,
inverse and composition of renamings (exhaustive over the whole
symmetric group at the declared carrier); the action laws (identity
unconditional, composition and inversion on the well-formed scope);
transport of blocks and of the complete Up family respecting identity
and composition; coherence of replay commutation under composed
renamings; orbit closure with no selected representative; and the
three countermodels — equal carrier size, equal cost, and an
arbitrary non-bijective map — each supplying none of the laws."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import Json, write_json
from derivation.renaming_structure import renaming_report


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path,
                        default=Path("artifacts"))
    parser.add_argument("--carrier", type=int, default=3)
    args = parser.parse_args(argv)
    payload: dict[str, Json] = renaming_report(args.carrier)
    out_path = args.artifacts / "renaming_structure.json"
    write_json(out_path, payload)
    laws = payload["group_laws"]
    assert isinstance(laws, dict)
    print(f"group laws: assoc={laws['comp_assoc']} "
          f"inv={laws['inv_comp']}/{laws['comp_inv']}")
    act = payload["action_laws"]
    assert isinstance(act, dict)
    print(f"action: id={act['act_id']} comp={act['act_comp']} "
          f"inv={act['act_inv']}")
    coh = payload["coherence"]
    assert isinstance(coh, dict)
    print(f"coherence: composed={coh['act_up_comm_composed']} "
          f"twostep={coh['act_up_comm_twostep_agrees']}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
