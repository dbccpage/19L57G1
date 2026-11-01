"""Recompute the small cell-and-boundary laboratory; AuthorityEffect: None."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "code"))
from derivation import attachment_ladder as cells, boundary_cancellation as boundary  # noqa: E402
from textbook.path_lab.costs import build_costs, check_cost_population, PINS  # noqa: E402

VERTICES = (0, 1, 2, 3)
EDGES = ((0, 1), (1, 2), (0, 2), (2, 3), (0, 3))
FACES = ((0, 1, 2), (0, 2, 3))
WALKS = ((0, 1, 2), (0, 1, 2, 0), (0, 1, 2, 3, 0), (0, 1, 0), (0, 1, 3), (0,))


def plain(value):
    return json.loads(json.dumps(value))


def coefficient_rows(chain, candidates):
    return [{"cell": list(cell), "coefficient": boundary.coeff_n(cell, chain)} for cell in candidates]


def normalized(chain):
    totals = Counter()
    for coefficient, cell in chain:
        totals[cell] += coefficient
    return [(totals[cell], cell) for cell in sorted(totals) if totals[cell]]


def edge_state(mask):
    state = {}
    for vertex in VERTICES:
        state = cells.step_v(state, vertex)
    for i, edge in enumerate(EDGES):
        if mask & (1 << i):
            before = state
            state = cells.step_n(state, 1, edge)
            assert state != before
    assert cells.wf_complex(state)
    return state


def face_case(mask, requests, second_coefficient):
    state = edge_state(mask)
    before = plain(state)
    attempts = []
    for index, face in enumerate(FACES):
        if requests & (1 << index):
            permitted = cells.shell_n(state, 2, face)
            required = tuple(combinations(face, 2))
            independent = all(edge in state.get(1, []) for edge in required) and face not in state.get(2, [])
            assert permitted == independent
            missing = [edge for edge in required if edge not in state.get(1, [])]
            after = cells.step_n(state, 2, face)
            assert (after != state) == permitted
            assert after.get(0, []) == state.get(0, []) and after.get(1, []) == state.get(1, [])
            attempts.append({"face": face, "guard": permitted, "missing_facets": missing,
                             "before_faces": state.get(2, []), "after_faces": after.get(2, [])})
            state = after
    admitted = state.get(2, [])
    face_chain = [(second_coefficient if f == FACES[1] else 1, f) for f in admitted]
    first = boundary.push_n(face_chain)
    second = boundary.push_n(first)
    # Independently expand each triangle's prescribed AB + BC - AC.
    direct = []
    for coefficient, (a, b, c) in face_chain:
        direct += [(coefficient, (a, b)), (coefficient, (b, c)), (-coefficient, (a, c))]
    assert normalized(first) == normalized(direct)
    for vertex in VERTICES:
        direct_endpoint = sum(coefficient * (int(edge[1] == vertex) - int(edge[0] == vertex))
                              for coefficient, edge in direct)
        assert boundary.coeff_n((vertex,), second) == direct_endpoint == 0
    repeats = []
    for face in admitted:
        assert not cells.shell_n(state, 2, face)
        assert cells.step_n(state, 2, face) == state
        repeats.append(face)
    assert cells.wf_complex(state)
    return plain({"edge_mask": mask, "request_mask": requests, "second_coefficient": second_coefficient,
                  "before": before, "after": state, "attempts": attempts, "admitted_faces": admitted,
                  "face_chain": face_chain, "first_boundary": first, "second_boundary": second,
                  "edge_coefficients": coefficient_rows(first, EDGES),
                  "vertex_coefficients": coefficient_rows(second, [(i,) for i in VERTICES]),
                  "repeated_requests_inert": repeats})


def walk_case(mask, sequence):
    if not sequence or any(type(v) is not int or v not in VERTICES for v in sequence):
        raise ValueError("The walk must be a nonempty sequence of declared natural-number vertices")
    state = edge_state(mask)
    steps = list(zip(sequence, sequence[1:]))
    missing = [(a, b) for a, b in steps if tuple(sorted((a, b))) not in state.get(1, [])]
    valid = not missing
    chain = [(1 if a < b else -1, tuple(sorted((a, b)))) for a, b in steps] if valid else None
    endpoints = boundary.push_n(chain) if valid else None
    direct = [sum(int(b == i) - int(a == i) for a, b in steps) for i in VERTICES] if valid else None
    if valid:
        assert direct == [int(sequence[-1] == i) - int(sequence[0] == i) for i in VERTICES]
        assert direct == [boundary.coeff_n((i,), endpoints) for i in VERTICES]
    return plain({"edge_mask": mask, "vertices": sequence, "steps": steps, "missing_steps": missing,
                  "valid": valid, "kind": "invalid" if not valid else "closed" if sequence[0] == sequence[-1] else "open",
                  "step_count": len(steps), "edge_chain": chain, "endpoint_terms": endpoints, "endpoint_counts": direct})


def build_packet():
    for module in (cells, boundary):
        assert Path(module.__file__).resolve().is_relative_to(ROOT / "code"), "Unexpected source origin"
    faces = {f"{mask}_{request}_{coefficient}": face_case(mask, request, coefficient)
             for mask, request, coefficient in product(range(32), range(4), (1, -1))}
    walks = {f"{mask}_{index}": walk_case(mask, walk)
             for mask, (index, walk) in product(range(32), enumerate(WALKS))}
    triangle = FACES[0]
    signed = boundary.push_n(boundary.bd_n(triangle))
    unsigned = boundary.push_no_sign(boundary.bd_no_sign(triangle))
    repeated = (0, 0, 1)
    all_edges = edge_state(31)
    raw = boundary.push_n(boundary.bd_n(repeated))
    comparisons = {"triangle_signed": coefficient_rows(signed, [(i,) for i in range(3)]),
                   "triangle_all_positive": coefficient_rows(unsigned, [(i,) for i in range(3)]),
                   "repeated_list": repeated, "repeated_ascending": boundary.asc(repeated),
                   "repeated_shell_guard": cells.shell_n(all_edges, 2, repeated),
                   "repeated_second_boundary": coefficient_rows(raw, [(i,) for i in VERTICES])}
    assert [r["coefficient"] for r in comparisons["triangle_signed"]] == [0, 0, 0]
    assert [r["coefficient"] for r in comparisons["triangle_all_positive"]] == [2, 2, 2]
    assert not comparisons["repeated_shell_guard"] and not comparisons["repeated_ascending"]
    # Check boundary pairing on every raw word of length 0..4 over four labels.
    raw_words = 0
    for length in range(5):
        for word in product(VERTICES, repeat=length):
            first = boundary.bd_n(word)
            second = boundary.push_n(first)
            assert first == cells.bd_n(word) and second == cells.push_n(cells.bd_n(word))
            assert all(boundary.coeff_n(face, second) == 0 for _, face in second)
            raw_words += 1
    assert raw_words == 341
    # New practice case: the shared edge has equal default signs.
    practice = [(1, (0, 1, 2)), (1, (1, 2, 3))]
    opposite = [(1, (0, 1, 2)), (-1, (1, 2, 3))]
    assert boundary.coeff_n((1, 2), boundary.push_n(practice)) == 2
    assert boundary.coeff_n((1, 2), boundary.push_n(opposite)) == 0
    assert normalized(boundary.push_n(opposite)) == [(1, (0, 1)), (-1, (0, 2)), (1, (1, 3)), (-1, (2, 3))]
    pins = {name: hashlib.sha256((ROOT / name).read_text(encoding="utf-8").encode("utf-8")).hexdigest()
            for name in ("code/derivation/attachment_ladder.py", "code/derivation/boundary_cancellation.py", *PINS)}
    return plain({"authority_effect": "None", "classification": "supplied teaching graph and cell calculus",
                  "source_text_sha256": pins, "digest_mode": "UTF-8 source text with LF normalization",
                  "vertices": ["A", "B", "C", "D"], "edges": EDGES, "faces": FACES, "walks": WALKS,
                  "face_cases": faces, "walk_cases": walks, "comparisons": comparisons,
                  "raw_boundary_words": raw_words, "costs":build_costs(), "practice_same_sign": boundary.push_n(practice),
                  "practice_opposite_sign": boundary.push_n(opposite)})


def check_recorded(directory=SOURCE):
    packet = build_packet()
    if json.loads((directory / "recorded_lab.json").read_text(encoding="utf-8")) != packet:
        raise ValueError("Recorded path lesson differs from the recomputed source-backed cases")
    counts = {"Edge subsets on the five declared edges": 32, "Face-request subsets": 4,
              "Second-face coefficient choices": 2, "Recorded face/boundary settings": len(packet["face_cases"]),
              "Recorded edge-subset/walk settings": len(packet["walk_cases"]),
              "Raw vertex words of length zero through four": packet["raw_boundary_words"]}
    rows = re.findall(r"^\| ([^|]+) \| (\d+) \|$", (SOURCE / "SOURCE_MAP.md").read_text(encoding="utf-8"), re.MULTILINE)
    if len(rows) != len(counts) or {label: int(n) for label, n in rows} != counts:
        raise ValueError("Path lesson population table differs from the checked cases")
    from textbook.path_lab.figures import render_figures
    for name, svg in render_figures(packet).items():
        path = SOURCE / "figures" / name
        if not path.is_file() or path.read_text(encoding="utf-8") != svg:
            raise ValueError("Path lesson figure differs from the checked case: " + name)
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--population", action="store_true")
    args = parser.parse_args()
    if args.write:
        packet = build_packet()
        (SOURCE / "recorded_lab.json").write_text(json.dumps(packet, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        from textbook.path_lab.figures import render_figures
        (SOURCE / "figures").mkdir(exist_ok=True)
        for name, svg in render_figures(packet).items():
            (SOURCE / "figures" / name).write_text(svg, encoding="utf-8", newline="\n")
    print(check_recorded())
    if args.population:
        print({'bounded_native_cost_histories':check_cost_population()})
