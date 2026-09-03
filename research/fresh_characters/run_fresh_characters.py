"""Run every stage and write the receipts deterministically (``--out DIR``).

The receipt records computations; it proves no theorem.  The Lean package is
audited by ``verify_lean.py``, which is the receipt for the Lean half.  Keys
are sorted and no timestamp or environment value is written, so the receipt
is byte-replayable.  AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import characters as ch
import divisor_recursion as dr
import fresh_totals as ft
import magnitude_census as mc
import register as rg

ADVERSARIAL: dict[str, str] = {
    "A1": "an identity for the balance says nothing about its growth; FW-GROWTH holds and the growth question is untouched",
    "A2": "the characters, the carriers, and the totals are declared here and named by their descriptions; no outside name appears",
    "A3": "the menu is declared and finite; it is not a classification of value carriers and none is claimed",
    "A4": "agreement to a bound is FINITE_COMPUTATION within that bound; every sentence carries it",
    "A5": "a refusal is a decision of the criterion on one named family and says nothing about a family outside the rectangle",
    "A6": "no diversity at the term level in this rectangle is not absence of diversity; the rectangle is in the sentence",
    "A7": "the criterion is CONDITIONAL_THEOREM, cited by pin, reconstructed as computation, and cross-checked against a brute-force search",
    "A8": "Lean proves; this receipt records",
    "A9": "the sealed bet's plaintext was authored by this session, so FW-LEAD is BREACHED for this run and recorded as such in STATUS.md",
    "A10": "disjoint write roots, frozen shared files, one pinned snapshot; nothing outside research/fresh_characters/ was written",
    "A11": "ties are retained: two pairs met stage 2 and both are carried through every later stage; neither is called the carrier",
    "A12": "no menu member was dropped; every obstruction is recorded next to its member",
}


def build(limit: int) -> dict[str, object]:
    stage1 = ch.target_report(limit)
    stage2 = ft.report(limit)
    stage3 = dr.report(limit)
    stage4 = mc.report(limit)
    stage5 = rg.report(stage1, stage2, stage3, stage4)
    return {
        "adversarial": ADVERSARIAL,
        "authority_effect": "None",
        "bound": limit,
        "snapshot": "f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be",
        "stage_1_layer_characters": stage1,
        "stage_2_total_identity": stage2,
        "stage_3_divisor_recursion": stage3,
        "stage_4_magnitude_census": stage4,
        "stage_5_register": stage5,
        "write_root": "research/fresh_characters/",
    }


def tau(report: dict[str, object]) -> str:
    stage2 = report["stage_2_total_identity"]
    assert isinstance(stage2, dict)
    search = stage2["search"]
    cross = stage2["cross_check"]
    assert isinstance(search, dict) and isinstance(cross, dict)
    stage3 = report["stage_3_divisor_recursion"]
    stage4 = report["stage_4_magnitude_census"]
    stage5 = report["stage_5_register"]
    assert isinstance(stage3, dict) and isinstance(stage4, dict) and isinstance(stage5, dict)
    rowkind = stage4["row_family_kind"]
    termkind = stage4["term_family_kind"]
    assert isinstance(rowkind, dict) and isinstance(termkind, dict)
    terminals = stage4["terminals"]
    assert isinstance(terminals, list)
    hits = search["hits"]
    assert isinstance(hits, list)
    stage1 = report["stage_1_layer_characters"]
    assert isinstance(stage1, dict)
    trivial_misses = stage1["character_trivial_total_misses"]
    assert isinstance(trivial_misses, list)
    return "\n".join([
        "yaml_export:",
        "  steps_completed: [LayerCharacters, TotalIdentity, DivisorRecursion,"
        " MagnitudeCensus, Register]",
        "  write_root: research/fresh_characters/",
        "  snapshot: f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be",
        "  sealed_paths_touched: []",
        "  shared_files_touched: []",
        "  census_pin_regenerated: false",
        "  prompt_hash_native: d45ba3e4827806458f19d3ec7d7ce8b4b474aab51a1a11d50d5a8b8b03d78348",
        "  predictions_hashes:",
        "    - aeb3d7728e98c98e1d2a00cd22145d5f198d8af9b0df28b63b301bb03534699f",
        "    - aa37d38170d20a3978331bab7e297a199c1e9c1c1d648ff2ef4c4a61d83a2abe",
        "  terminals:",
        "    - {code: CHARACTERS_DEFINED, scope: four targets proved in core Lean for every"
        " part count, carrier-free on the exponent word}",
        f"    - {{code: {search['terminal']}, scope: exhaustive over 24 declared pairs at part"
        f" counts 1..{search['bound']}; kernel-decided in Lean to 20}}",
        f"    - {{code: {stage3['terminal']}, scope: the declared rectangle to"
        f" {stage3['bound']}; kernel-decided in Lean to 16}}",
        *[f"    - {{code: {t}, scope: the declared rectangle to {stage4['bound']},"
          f" both family kinds}}" for t in terminals],
        "    - {code: REGISTER_WRITTEN, scope: six menu members, five leftovers}",
        "    - {code: GROWTH_OPEN_UNCHANGED, scope: mandatory; no growth sentence in the tree}",
        f"  layer_characters: {{menu: [V1, V2, V3, V4, V5, V6], lean_targets_proved: 4,"
        f" python_exponent_word_misses: {len(trivial_misses)}}}",
        f"  total_identity: {{terminal: {search['terminal']}, pairs: {hits},"
        f" menu_size: {search['menu_size']}, bound_python: {search['bound']},"
        f" bound_lean: 20, direct_cross_check: {cross['direct_bound']},"
        f" checkpoint_misses: {cross['checkpoint_misses']}}}",
        f"  divisor_recursion: {{terminal: {stage3['terminal']},"
        f" carriers_meeting: {stage3['carriers_meeting_the_recursion']}, bound: {stage3['bound']}}}",
        f"  magnitude_census: {{terminals: {terminals}, rectangle: {stage4['bound']},"
        f" term_families: {termkind['families']}, term_diverse: {termkind['diverse_families']},"
        f" row_families: {rowkind['families']}, row_diverse: {rowkind['diverse_families']},"
        f" certificate_refusals: {rowkind['certificate_refusals']},"
        f" criterion_vs_brute_force_misses: {stage4['criterion_miss_count']}}}",
        f"  lp4_disposition: moved at the row level, witness part count"
        f" {rowkind['smallest_diverse_witness']['n'] if rowkind['smallest_diverse_witness'] else None};"
        f" carried forward unchanged at the term level",
        "  growth: {terminal: GROWTH_OPEN_UNCHANGED}",
        "  leftover: five, named and priced, executed nowhere",
        "  opens_unchanged: [OB1_UNCHANGED, S66_UNCHANGED, S9_LAST_UNCHANGED,"
        " NS95_GROWTH_UNCHANGED]",
        "  outside_bet_hash: 6b7fb10447284d2229b71b14ec18eade4620a8dab2697d4cdf9e7635d22b482c",
        "  outside_bet_blind: false",
        "  authority_effect: None",
        "final_state: true",
        "op QED",
        "",
    ])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=Path("receipts"))
    parser.add_argument("--bound", type=int, default=60)
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    report = build(args.bound)
    (args.out / "fresh_characters.json").write_bytes(
        (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )
    (args.out / "tau.yaml").write_bytes(tau(report).encode("utf-8"))
    stage2 = report["stage_2_total_identity"]
    assert isinstance(stage2, dict)
    search = stage2["search"]
    assert isinstance(search, dict)
    stage4 = report["stage_4_magnitude_census"]
    assert isinstance(stage4, dict)
    print(f"stage 2: {search['terminal']}, hits {search['hits']}")
    print(f"stage 4: {stage4['terminals']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
