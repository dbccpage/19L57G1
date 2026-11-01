"""Finite map, class, and lookup examples; AuthorityEffect: None."""
from __future__ import annotations

import argparse
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
from derivation import compression as native  # noqa: E402
from textbook.map_lab.native_paths import build_paths, check_paths_population, PINS  # noqa: E402

BLUE = (1, 1, 0, 0)
TRIANGLE = (0, 1, 1, 0)
FAMILIES = ((), (BLUE,), (TRIANGLE,), (BLUE, TRIANGLE))
TARGETS = (BLUE, TRIANGLE, tuple(2*b+t for b, t in zip(BLUE, TRIANGLE)), (1, 1, 1, 1))


def plain(value):
    return json.loads(json.dumps(value))


def domain(mask, reverse=False):
    ids = [i for i in range(4) if mask & (1 << i)]
    return ids[::-1] if reverse else ids


def map_case(mask, family, target, reverse):
    D = domain(mask, reverse)
    Q, q = FAMILIES[family], TARGETS[target]
    # Native p_quotient returns one value PER DOMAIN ENTRY, not a full
    # position-indexed function. Zip first, then extend outside D only as
    # teaching apparatus. No agreement with native pQ off D is claimed.
    aligned = native.p_quotient(D, Q)
    assert len(aligned) == len(D)
    by_position = dict(zip(D, aligned))
    p = tuple(by_position.get(i, 0) for i in range(4))
    assert all(p[x] in D and native.sig_eq(Q, x, p[x]) for x in D)
    groups = []
    for representative in dict.fromkeys(aligned):
        members = [x for x in D if p[x] == representative]
        values = sorted({q[x] for x in members})
        groups.append({"representative": representative, "members": members,
                       "requested_values": values, "conflict": len(values) > 1})
    expected_groups = {frozenset(x for x in D if native.sig_list(Q, x) == native.sig_list(Q, y)) for y in D}
    assert {frozenset(g["members"]) for g in groups} == expected_groups
    assert {frozenset(g) for g in native.partition_of(D, Q)} == expected_groups
    assert len(groups) == native.class_count(D, Q)
    conflicts = [[a, b] for a, b in combinations(D, 2) if p[a] == p[b] and q[a] != q[b]]
    m = 4 if target == 2 else 2
    image_maps = native.valid_factor_maps(D, p, q, m)
    recoverable = not conflicts
    assert recoverable == native.fiber_constant(D, p, q) == bool(image_maps)
    assert recoverable == native.factors_on(D, p, q, m)
    assert len(image_maps) == int(recoverable)
    full = [values for values in product(range(m), repeat=4)
            if all(values[p[x]] == q[x] for x in D)]
    assert len(full) == (m ** (4-len(groups)) if recoverable else 0)
    observed_lookup = [] if not image_maps else [
        {"label": label, "value": value} for label, value in sorted(image_maps[0].items())]
    assert not image_maps or all(image_maps[0][p[x]] == q[x] for x in D)
    if not recoverable:
        assert all(p[a] == p[b] and q[a] != q[b] for a, b in conflicts)
    return plain({"domain_mask": mask, "family": family, "target": target, "reverse": reverse,
                  "domain": D, "questions": Q, "requested": q, "presentation": p,
                  "aligned_representatives": aligned, "signatures": [native.sig_list(Q, x) for x in D],
                  "groups": groups, "class_count": len(groups), "recoverable": recoverable,
                  "blocking_pairs": conflicts, "image_lookup": observed_lookup,
                  "unused_labels": [i for i in range(4) if i not in aligned],
                  "full_label_alphabet": 4, "answer_alphabet": m,
                  "full_lookup_count": len(full), "full_lookup_examples": full[:2]})


def build_packet():
    assert Path(native.__file__).resolve().is_relative_to(ROOT / "code"), "Unexpected source origin"
    original = json.loads((ROOT / "textbook/first_steps/cards.json").read_text(encoding="utf-8"))
    assert [(c["id"], c["color"], c["shape"]) for c in original["cards"]] == [
        ("A", "blue", "circle"), ("B", "blue", "triangle"), ("C", "amber", "triangle")]
    cases = {f"{mask}_{family}_{target}_{int(reverse)}": map_case(mask, family, target, reverse)
             for mask, family, target, reverse in product(range(16), range(4), range(4), (False, True))}
    for mask, family, reverse in product(range(16), range(4), (False, True)):
        prefix = f"{mask}_{family}_"
        blue = cases[prefix + f"0_{int(reverse)}"]["recoverable"]
        triangle = cases[prefix + f"1_{int(reverse)}"]["recoverable"]
        assert cases[prefix + f"2_{int(reverse)}"]["recoverable"] == (blue and triangle)
        assert cases[prefix + f"3_{int(reverse)}"]["recoverable"]
        assert cases[prefix + f"0_0"]["recoverable"] == cases[prefix + f"0_1"]["recoverable"]
    controls = []
    D = list(range(4))
    for label, Q in (("blue only", (BLUE,)), ("duplicate blue", (BLUE, BLUE)),
                     ("blue and its complemented answer", (BLUE, tuple(1-b for b in BLUE))),
                     ("blue and triangle", (BLUE, TRIANGLE))):
        blocks = native.partition_of(D, Q)
        p_aligned = native.p_quotient(D, Q)
        controls.append({"case": label, "groups": blocks, "class_count": len(blocks),
                         "triangle_recoverable": native.fiber_constant(D, p_aligned, TRIANGLE)})
    assert [c["class_count"] for c in controls] == [2, 2, 2, 4]
    assert [c["triangle_recoverable"] for c in controls] == [False, False, False, True]
    # "Some answer agrees" fails transitivity on A/B/C; exact complete
    # signature agreement is the relation used by the quotient cases.
    some_match = lambda a, b: any(q[a] == q[b] for q in (BLUE, TRIANGLE))
    assert some_match(0, 1) and some_match(1, 2) and not some_match(0, 2)
    pins = {name: hashlib.sha256((ROOT / name).read_text(encoding="utf-8").encode("utf-8")).hexdigest()
            for name in ("code/derivation/compression.py", "textbook/first_steps/cards.json", *PINS)}
    return plain({"authority_effect": "None", "classification": "supplied four-card finite map model",
                  "source_text_sha256": pins, "digest_mode": "UTF-8 source text with LF normalization",
                  "cards": ["A", "B", "C", "D"], "blue": BLUE, "triangle": TRIANGLE,
                  "family_names": ["no questions", "blue only", "triangle only", "both questions"],
                  "target_names": ["blue?", "triangle?", "(blue?, triangle?)", "always Yes"],
                  "cases": cases, "controls": controls, "native_paths": build_paths(),
                  "some_agreement_counterexample": [0, 1, 2]})


def check_population():
    # Every four-label presentation and every binary target on four items,
    # on all sixteen selected domains. Independent grouping versus complete
    # Boolean lookup enumeration; source functions are called directly.
    count = 0
    for p, q, mask in product(product(range(4), repeat=4), product(range(2), repeat=4), range(16)):
        D = domain(mask)
        direct = all(q[a] == q[b] for a in D for b in D if p[a] == p[b])
        lookups = [g for g in product(range(2), repeat=4) if all(g[p[x]] == q[x] for x in D)]
        assert direct == bool(lookups) == native.fiber_constant(D, p, q)
        assert direct == native.factors_on(D, p, q, 2)
        count += 1
    assert count == 65536
    return count


def check_recorded(directory=SOURCE):
    packet = build_packet()
    if json.loads((directory / "recorded_lab.json").read_text(encoding="utf-8")) != packet:
        raise ValueError("Recorded map lesson differs from the source-backed computations")
    counts = {"Selected card domains": 16, "Kept-question families": 4, "Requested-answer choices": 4,
              "Representative-order choices": 2, "Recorded map settings": len(packet["cases"]),
              "Four-label-presentation/binary-target/domain cases": 65536}
    rows = re.findall(r"^\| ([^|]+) \| (\d+) \|$", (SOURCE / "SOURCE_MAP.md").read_text(encoding="utf-8"), re.MULTILINE)
    if len(rows) != len(counts) or {k: int(v) for k, v in rows} != counts:
        raise ValueError("Map lesson population table differs from checked cases")
    from textbook.map_lab.figures import render_figures
    for name, svg in render_figures(packet).items():
        path = SOURCE / 'figures' / name
        if not path.is_file() or path.read_text(encoding='utf-8') != svg:
            raise ValueError('Map lesson figure differs from checked cases: ' + name)
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--population", action="store_true")
    args = parser.parse_args()
    if args.write:
        packet = build_packet()
        (SOURCE / "recorded_lab.json").write_text(json.dumps(packet, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        from textbook.map_lab.figures import render_figures
        (SOURCE / 'figures').mkdir(exist_ok=True)
        for name, svg in render_figures(packet).items():
            (SOURCE / 'figures' / name).write_text(svg, encoding='utf-8', newline='\n')
    print(check_recorded())
    if args.population:
        print({"additional_finite_factorization_cases": check_population()})
        print({"two_state_translation_histories": check_paths_population()})
