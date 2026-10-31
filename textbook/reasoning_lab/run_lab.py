"""Finite reasoning examples; AuthorityEffect: None. Sealed sources are read-only."""
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
from textbook.first_steps.checks import check_encoding, model, observe  # noqa: E402
from textbook.reasoning_lab.evidence import build_evidence_packet, check_evidence_population  # noqa: E402

NAMES = ("A", "B", "C")
QUESTIONS = ("blue?", "round?", "triangle?")
ROWS = ((True, True, False), (True, False, False), (False, True, True))
DOMAINS = tuple(tuple(i for i in range(3) if mask & (1 << i)) for mask in range(8))


def claim(rows, domain, left, right, negate=False, kind="if"):
    if kind not in ("if", "iff"):
        raise ValueError("Unknown teaching claim kind")
    cases = []
    for card in domain:
        p, q = rows[left][card], rows[right][card] != negate
        forward_break = p and not q
        reverse_break = q and not p
        cases.append({"card": card, "p": p, "q": q, "forward_break": forward_break,
                      "reverse_break": reverse_break,
                      "breaks": forward_break or (kind == "iff" and reverse_break)})
    return {"domain": list(domain), "left": left, "right": right, "negate": negate,
            "kind": kind, "rows": cases, "holds": not any(r["breaks"] for r in cases),
            "first_true_count": sum(r["p"] for r in cases),
            "some_first": any(r["p"] for r in cases), "every_first": all(r["p"] for r in cases)}


def witnesses(rows, domain, questions):
    pairs = [{"pair": [a, b], "questions": [q for q in questions if rows[q][a] != rows[q][b]]}
             for a, b in combinations(domain, 2)]
    common = [q for q in questions if all(rows[q][a] != rows[q][b] for a, b in combinations(domain, 2))]
    return {"domain": list(domain), "available": list(questions), "pairs": pairs,
            "each_pair_has_some": all(row["questions"] for row in pairs),
            "one_question_for_all": bool(common), "common_questions": common}


def recovery(rows, domain, kept, requested):
    # Enumerate every Boolean lookup function, including unobserved inputs.
    maps = [list(outputs) for outputs in product((False, True), repeat=2)
            if all(outputs[int(rows[kept][i])] == rows[requested][i] for i in domain)]
    blocks = [[a, b] for a, b in combinations(domain, 2)
              if rows[kept][a] == rows[kept][b] and rows[requested][a] != rows[requested][b]]
    assert bool(maps) == (not blocks)
    return {"maps": maps, "blocking_pairs": blocks}


def build_packet():
    for module in (model, observe):
        assert Path(module.__file__).resolve().is_relative_to(ROOT / "code"), "Unexpected source origin"
    cards = json.loads((ROOT / "textbook/first_steps/cards.json").read_text(encoding="utf-8"))
    assert [(c["id"], c["color"], c["shape"]) for c in cards["cards"]] == [
        ("A", "blue", "circle"), ("B", "blue", "triangle"), ("C", "amber", "triangle")]
    original = {q["id"]: tuple(q["answers"]) for q in cards["questions"]}
    assert original["blue"] == ROWS[0] and original["triangle"] == ROWS[2]
    assert ROWS[1] == tuple(c["shape"] == "circle" for c in cards["cards"])
    claims = {}
    families = {}
    for mask, domain in enumerate(DOMAINS):
        for left, right, negate, kind in product(range(3), range(3), (False, True), ("if", "iff")):
            key = f"{mask}_{left}_{right}_{int(negate)}_{kind}"
            claims[key] = claim(ROWS, domain, left, right, negate, kind)
        for qmask, questions in enumerate(DOMAINS):
            families[f"{mask}_{qmask}"] = witnesses(ROWS, domain, questions)
    assert claims["7_1_0_0_if"]["holds"]
    assert not claims["7_0_1_0_if"]["holds"]
    assert claims["7_2_1_1_iff"]["holds"]
    assert families["7_5"]["each_pair_has_some"] and not families["7_5"]["one_question_for_all"]
    assert families["0_0"]["each_pair_has_some"] and not families["0_0"]["one_question_for_all"]
    pins = {}
    for name in ("textbook/first_steps/cards.json", "textbook/first_steps/checks.py",
                 "code/derivation/model.py", "code/derivation/observe.py", "textbook/reasoning_lab/evidence.py"):
        pins[name] = hashlib.sha256((ROOT / name).read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    return {"authority_effect": "None", "classification": "supplied teaching logic and finite calculations",
            "source_text_sha256": pins, "digest_mode": "UTF-8 source text with LF normalization",
            "cards": list(NAMES), "questions": list(QUESTIONS), "answers": ROWS,
            "evidence": build_evidence_packet(),
            "claims": claims, "families": families,
            "recovery_blue_to_round": {str(mask): recovery(ROWS, domain, 0, 1) for mask, domain in enumerate(DOMAINS)}}


def plain(value):
    return json.loads(json.dumps(value))


def check_recorded(directory=SOURCE):
    if json.loads((directory / "recorded_lab.json").read_text(encoding="utf-8")) != plain(build_packet()):
        raise ValueError("Recorded reasoning lesson differs from the recomputed examples")
    return {"claim_cases": 288, "question_family_cases": 64, "recovery_domains": 8}


def check_population():
    counts = {"three_question_tables": 0, "claim_cases": 0, "question_family_cases": 0,
              "recovery_cases": 0, "sealed_encoding_histories": 0}
    for bits in product((False, True), repeat=9):
        rows = (bits[:3], bits[3:6], bits[6:])
        counts["three_question_tables"] += 1
        for domain in DOMAINS:
            for left, right, negate, kind in product(range(3), range(3), (False, True), ("if", "iff")):
                result = claim(rows, domain, left, right, negate, kind)
                # Independent set inclusion/equality, rather than the row guard.
                positive_p = {i for i in domain if rows[left][i]}
                positive_q = {i for i in domain if rows[right][i] != negate}
                wanted = positive_p <= positive_q if kind == "if" else positive_p == positive_q
                assert result["holds"] == wanted
                assert result["some_first"] == bool(positive_p)
                assert result["every_first"] == (positive_p == set(domain))
                counts["claim_cases"] += 1
            for questions in DOMAINS:
                result = witnesses(rows, domain, questions)
                signatures = [tuple(rows[q][i] for q in questions) for i in domain]
                assert result["each_pair_has_some"] == (len(signatures) == len(set(signatures)))
                expected_common = any(len({rows[q][i] for i in domain}) == len(domain) for q in questions)
                assert result["one_question_for_all"] == expected_common
                assert not result["one_question_for_all"] or result["each_pair_has_some"]
                counts["question_family_cases"] += 1
            for p, q in product(range(3), repeat=2):
                recovery(rows, domain, p, q)
                counts["recovery_cases"] += 1
        for questions in DOMAINS:
            check_encoding(rows, questions)
            counts["sealed_encoding_histories"] += 1
    assert counts == {"three_question_tables": 512, "claim_cases": 147456,
                      "question_family_cases": 32768, "recovery_cases": 36864,
                      "sealed_encoding_histories": 4096}
    lesson_rows = re.findall(r"^\| ([^|]+) \| (\d+) \|$", (SOURCE / "SOURCE_MAP.md").read_text(encoding="utf-8"), re.MULTILINE)
    expected_rows = {
        "Recorded default-table conditional comparisons": 288,
        "Recorded default-table pair/question-family comparisons": 64,
        "Recorded default-table recovery domains": 8,
        "Arbitrary Boolean tables: three questions on three positions": counts["three_question_tables"],
        "Conditional comparisons across all those tables and domains": counts["claim_cases"],
        "Pair/question-family comparisons across those tables and domains": counts["question_family_cases"],
        "Recovery tasks across those tables and domains": counts["recovery_cases"],
        "Sealed unary-encoding replay histories": counts["sealed_encoding_histories"],
    }
    if len(lesson_rows) != 8 or {label: int(n) for label, n in lesson_rows} != expected_rows:
        raise ValueError("Reasoning source-map population table differs from checked cases")
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--population", action="store_true")
    args = parser.parse_args()
    if args.write:
        (SOURCE / "recorded_lab.json").write_text(json.dumps(build_packet(), indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(check_recorded())
    print(check_evidence_population())
    if args.population:
        print(check_population())
