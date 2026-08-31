"""Write receipts/decide.json deterministically."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
import random
from pathlib import Path

import decide
from diagram import PATCH3_EDGES, all_green, mass, patch3_scale_section, patch3_section

HERE = Path(__file__).resolve().parent
SEED = 20260830


def assert_inside_tree(path: Path) -> Path:
    target = path.resolve()
    if not target.is_relative_to(HERE):
        raise ValueError(f"refusing to write outside research/observer_visibility/: {path}")
    return target


def random_diagrams(n: int) -> list[dict[str, object]]:
    rng = random.Random(SEED)
    out: list[dict[str, object]] = []
    for i in range(n):
        n_obj = 2
        edges = [(0, 1)]
        if rng.randrange(2) == 1:
            edges.append((1, 0))
        both = rng.randrange(3) == 0
        watch: decide.Watch = {e: (True, True) if both else (True, False) for e in edges}
        d = decide.decide(n_obj, edges, watch, bound=1)
        b = decide.brute(n_obj, edges, watch, bound=1)
        out.append(
            {
                "i": i,
                "edges": edges,
                "both": both,
                "decide": d["verdict"],
                "brute": b,
                "agree": d["verdict"] == b,
            }
        )
    return out


def report() -> dict[str, object]:
    s = patch3_section()
    watch = decide.patch3_watch()
    p3 = decide.decide(6, PATCH3_EDGES, watch, bound=1)
    box = decide.min_unsound_on_box(6, PATCH3_EDGES, watch, bound=1)
    killed = decide.decide_trivial_kernels(6, PATCH3_EDGES, bound=1)
    loop_edges = ((0, 0),)
    loop_watch: decide.Watch = {(0, 0): (False, False)}
    loop = decide.decide(1, loop_edges, loop_watch, bound=1)
    seeded = random_diagrams(20)
    return {
        "schema": "observer_visibility_decide/v1",
        "seed": SEED,
        "patch3_lean_section_mass": mass(s, PATCH3_EDGES),
        "patch3_scale_masses": [
            mass(patch3_scale_section(k), PATCH3_EDGES) for k in range(1, 6)
        ],
        "patch3_scale_all_green": all(
            all_green(patch3_scale_section(k), PATCH3_EDGES) for k in range(1, 6)
        ),
        "patch3_decision": p3,
        "patch3_box_min": box,
        "patch3_generator_matches_box_min": (
            p3["verdict"] == box["verdict"]
            and p3["mass"] == box["mass"]
            and p3["support"] == box["support"]
        ),
        "trivial_kernels": killed,
        "loop_unwatched": loop,
        "seeded": seeded,
        "seeded_agree": all(bool(row["agree"]) for row in seeded),
    }


def render() -> bytes:
    return (json.dumps(report(), indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode(
        "ascii"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(HERE / "receipts"))
    args = parser.parse_args(argv)
    try:
        out = assert_inside_tree(Path(args.out).resolve())
        out.mkdir(parents=True, exist_ok=True)
        (out / "decide.json").write_bytes(render())
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    r = report()
    print("patch3", r["patch3_decision"])
    killed = r["trivial_kernels"]
    assert isinstance(killed, dict)
    print("trivial", killed["verdict"])
    print("loop", r["loop_unwatched"])
    print("generator_matches_box", r["patch3_generator_matches_box_min"])
    print("scale_masses", r["patch3_scale_masses"])
    print("seeded_agree", r["seeded_agree"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
