"""Run every stage and write the receipts deterministically (``--out DIR``):
``receipts/balance_carrier.json`` and ``receipts/tau.yaml``.

The receipt records computations; it proves no theorem (A7).  The Lean
statuses written here are declarations checked by ``verify_lean.py``,
which is the receipt for the Lean package.  AuthorityEffect: None.
"""

from __future__ import annotations

# ruff: noqa: E402 -- bytecode suppression must precede tree-local imports

import sys

sys.dont_write_bytecode = True

import argparse
import hashlib
import json
from pathlib import Path

import growth_checkpoints
import layer_observer
import register
import signed_table
import walk_carrier as wc

HERE = Path(__file__).resolve().parent

ADVERSARIAL: dict[str, str] = {
    "A1": "an identity for the running balance re-expresses the same signed sum; growth stays OPEN (FW-GROWTH)",
    "A2": "the class and the count are declared and the identity is stated in those terms; no outside name is used (FW-NAME)",
    "A3": "agreement at the pinned checkpoints is FINITE_COMPUTATION within bound, not a theorem",
    "A4": "the Lean identity for S1b at every N does not close the growth OPEN; the protected open is unchanged",
    "A5": "every family here has magnitude 1 throughout, so the certificate criterion refuses nothing: LP4 persists and the diverse-magnitude census is priced again",
    "A6": "layer_observer_grades is proved in the declared form (a fresh part carried along a divisor arrow reads its source part count); walks are not graded by any theorem here",
    "A7": "Lean proves; this receipt records",
    "A8": "the run saw only the commitment hash; FW-LEAD is honored by construction and both stage-2 terminals were pre-agreed",
    "A9": "disjoint write roots, frozen shared files, a pin to main at one snapshot; nothing outside research/balance_carrier/ was written",
    "A10": "the menu is declared and finite (90 candidates); it is not a classification of carriers and none is claimed (FW-SET)",
}


def build_report(limit: int) -> dict[str, object]:
    bal = wc.balance_table(limit)
    run = wc.running_balance_table(bal)
    stage1 = layer_observer.report()
    stage2 = wc.report(bal, run)
    search = stage2["search"]
    assert isinstance(search, dict)
    hits = search["hits"]
    assert isinstance(hits, list)
    stage3 = signed_table.report([str(h) for h in hits], bal, run)
    stage4 = growth_checkpoints.report(bal, run)
    stage5 = register.register(search, stage3)
    stage2_terminals = [
        {"menu": label, "terminal": status["status"], "scope": status["scope"]}
        for label, status in register.LEAN_STATUS.items()
        if label in hits
    ]
    terminals = [
        {
            "stage": 1,
            "terminal": "LAYER_OBSERVER_PROVED",
            "scope": "layer_observer_wf, layer_observer_constant, layer_observer_separates, layer_observer_grades in core Lean; verify_lean.py is the receipt",
        },
        *[{"stage": 2, **t} for t in stage2_terminals],
        {
            "stage": 3,
            "terminal": stage3["terminal"],
            "scope": f"N in {stage3['family_sizes']} for every stage-2 hit",
        },
        {
            "stage": 4,
            "terminal": stage4["terminal"],
            "scope": "checkpoint values only; no growth bound in either direction",
        },
        {"stage": 5, "terminal": stage5["terminal"], "scope": "three rows, four leftovers"},
    ]
    return {
        "stage_1_layer_observer": stage1,
        "stage_2_walk_carrier": stage2,
        "stage_3_signed_family_table": stage3,
        "stage_4_growth_checkpoints": stage4,
        "stage_5_register": stage5,
        "terminals": terminals,
        "adversarial": ADVERSARIAL,
        "authority_effect": "None",
    }


def render(report: dict[str, object]) -> bytes:
    return (json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode(
        "ascii"
    )


def yaml_list(items: list[str], indent: str) -> str:
    return "".join(f"{indent}- {item}\n" for item in items)


def render_tau(report: dict[str, object]) -> bytes:
    manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text("ascii"))
    prompt_hash = hashlib.sha256((HERE / "PROMPT.md").read_bytes()).hexdigest()
    stage2 = report["stage_2_walk_carrier"]
    stage3 = report["stage_3_signed_family_table"]
    stage4 = report["stage_4_growth_checkpoints"]
    assert isinstance(stage2, dict) and isinstance(stage3, dict) and isinstance(stage4, dict)
    search = stage2["search"]
    assert isinstance(search, dict)
    hits = search["hits"]
    assert isinstance(hits, list)
    terminals = report["terminals"]
    assert isinstance(terminals, list)
    rows = stage3["rows"]
    assert isinstance(rows, list)
    mags: set[int] = set()
    for r in rows:
        if isinstance(r, dict) and r["N"] == 12:
            multiset = r["magnitude_multiset"]
            assert isinstance(multiset, list)
            for pair in multiset:
                assert isinstance(pair, list)
                mags.add(int(pair[0]))
    mags_at_12 = sorted(mags)
    checkpoints = stage4["checkpoints"]
    assert isinstance(checkpoints, list)
    ratios = "".join(
        f"      {c['N']}: {c['ratio_decimal']}\n" for c in checkpoints if isinstance(c, dict)
    )
    misses = stage4["checkpoint_misses"]
    assert isinstance(misses, list)
    identity_lines = "".join(
        f"    - {{menu: {t['menu']}, terminal: {t['terminal']}}}\n"
        for t in terminals
        if isinstance(t, dict) and t.get("stage") == 2
    )
    terminal_lines = "".join(
        f"    - {{stage: {t['stage']}, code: {t['terminal']}}}\n"
        for t in terminals
        if isinstance(t, dict)
    )
    text = (
        "yaml_export:\n"
        "  steps_completed: [LayerObserver, WalkCarrier, SignedFamilyTable, GrowthCheckpoints, Register]\n"
        "  write_root: research/balance_carrier/\n"
        "  sealed_paths_touched: []\n"
        "  shared_files_touched: []\n"
        "  census_pin_regenerated: false\n"
        f"  prompt_hash_native: {prompt_hash}\n"
        "  predictions_hashes:\n"
        + yaml_list([str(h) for h in manifest["predictions_freezes"]], "    ")
        + "  terminals:\n"
        + terminal_lines
        + "  layer_observer:\n"
        "    proved: [layer_observer_wf, layer_observer_constant, layer_observer_separates, layer_observer_grades]\n"
        "    open: []\n"
        "  walk_carrier:\n"
        f"    menu_size: {search['menu_size']}\n"
        "    bound_python: 12\n"
        f"    bound_lean: {stage3['lean_instance_bound']}\n"
        "    identities:\n"
        + identity_lines
        + "  signed_family_table:\n"
        f"    terminal: {stage3['terminal']}\n"
        f"    magnitudes_at_12: {mags_at_12}\n"
        "  growth:\n"
        f"    terminal: {stage4['terminal']}\n"
        f"    checkpoints_agree: {str(len(misses) == 0).lower()}\n"
        "    ratios:\n"
        + ratios
        + "  lp4_disposition: persists on every family produced here; the diverse-magnitude census is priced again\n"
        "  leftover: the general table identity (CONJECTURE), the enlarged menu, LP4, and the next rung (fresh character totals), named and priced, executed nowhere\n"
        "  opens_unchanged: [OB1_UNCHANGED, S66_UNCHANGED, S9_LAST_UNCHANGED, NS95_GROWTH_UNCHANGED]\n"
        f"  outside_bet_hash: {manifest['outside_bet_sha256']}\n"
        "  authority_effect: None\n"
        f"final_state: {'T' if len(misses) == 0 and len(hits) > 0 else 'F'}\n"
        "op QED\n"
    )
    return text.encode("ascii")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(HERE / "receipts"))
    parser.add_argument("--limit", type=int, default=wc.CHECKPOINTS[-1])
    args = parser.parse_args(argv)
    out = Path(args.out).resolve()
    if not out.is_relative_to(HERE):
        print(f"refusing to write outside research/balance_carrier/: {out}", file=sys.stderr)
        return 1
    out.mkdir(parents=True, exist_ok=True)
    report = build_report(args.limit)
    (out / "balance_carrier.json").write_bytes(render(report))
    (out / "tau.yaml").write_bytes(render_tau(report))
    search = report["stage_2_walk_carrier"]
    assert isinstance(search, dict)
    found = search["search"]
    assert isinstance(found, dict)
    print(f"stage 2: menu {found['menu_size']}, hits {found['hits']}")
    stage3 = report["stage_3_signed_family_table"]
    assert isinstance(stage3, dict)
    print(f"stage 3: {stage3['terminal']}")
    stage4 = report["stage_4_growth_checkpoints"]
    assert isinstance(stage4, dict)
    print(
        f"stage 4: {stage4['terminal']}, checkpoint misses {stage4['checkpoint_misses']},"
        f" running maximum {stage4['running_maximum']}"
    )
    terminals = report["terminals"]
    assert isinstance(terminals, list)
    for t in terminals:
        print("terminal:", t)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
