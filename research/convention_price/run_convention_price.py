"""The convention_price run: phases 2-5 computed, receipts written.

Deterministic and byte-replayable: no timestamps, sorted keys, LF
bytes.  Phase 1 and the Lean half of phase 2 are proved in `lean/` and
audited by `verify_lean.py`; this runner computes everything else and
records every pinned prediction's disposition next to its value.

Run from this directory: `python run_convention_price.py --out receipts`.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
# This tree FIRST, the pinned tree second: both carry a `register`
# module, and the pinned one must not shadow this one (observed: the
# reversed order called the pinned build() and crashed).
sys.path.insert(0, str(HERE.parent / "sign_slice"))
sys.path.insert(0, str(HERE))

import argparse
import hashlib
import json

from cone_section import cone_section
from genpres import GenPres
from slice_set import members

from channels import row as channel_row
from channels import separation_verdict, signed_variant, weight_list
from promotion import cure_verified, exhaust_consumed_classes, exhaust_slots
from register import build as build_register
from sixlabel import binary_crosscheck, exhaust as sixlabel_exhaust, member as sixlabel_member


def dispose(condition: bool, value: object) -> str:
    return f"CONFIRMED: {value}" if condition else f"MISS: {value}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="receipts")
    args = parser.parse_args()
    out_dir = HERE / str(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    pinned = json.loads(
        (HERE.parent / "sign_slice" / "receipts" / "sign_slice.json").read_text(
            "ascii"
        )
    )

    # Census reproduction (PS4, FW-CHAIN: the pinned receipt is the
    # comparison object).
    census: list[dict[str, object]] = []
    presentations: dict[str, GenPres] = {}
    for name, p in members():
        presentations[name] = p
        census.append(
            {
                "name": name,
                "fibre": p.fibre,
                "sectioned": cone_section(p),
            }
        )
    pinned_rows = {
        str(r["name"]): bool(r["sectioned"])
        for r in pinned["phase_3_census"]["rows"]
    }
    census_agrees = all(
        pinned_rows[str(r["name"])] == bool(r["sectioned"]) for r in census
    ) and len(pinned_rows) == len(census)
    obstructed = [r for r in census if not bool(r["sectioned"])]

    # Phase 2: the seven two-label obstructed members.
    two_label = [str(r["name"]) for r in obstructed if int(str(r["fibre"])) == 2]
    phase2: dict[str, dict[str, object]] = {}
    cures: dict[str, dict[str, object]] = {}
    classes: dict[str, dict[str, object]] = {}
    for name in two_label:
        p = presentations[name]
        cures[name] = cure_verified(p)
        phase2[name] = exhaust_slots(p)
        classes[name] = exhaust_consumed_classes(p)
    route_agreement = {
        name: phase2[name]["flip_count"] == classes[name]["flip_count_from_classes"]
        and phase2[name]["price_min_slots_from_pointwise"]
        == classes[name]["price_from_classes"]
        for name in two_label
    }
    square = phase2["square_2x2_occ2"]
    pinned_occ = pinned["phase_4_occ_relabel"]
    pm3_ok = (
        square["flip_count"] == pinned_occ["exhaustion"]["flip_count"]
        and square["price_min_slots_from_pointwise"]
        == pinned_occ["exhaustion"]["price_min_slots_from_pointwise"]
        and square["pointwise_moves"] == 0
        and square["pointwise_assignments"] == 64
    )
    pm6_keys = ("flip_count", "price_min_slots_from_pointwise", "pointwise_moves")
    pm6_ok = all(
        phase2[n][k] == square[k] for n in ("signed_square_pos", "signed_square_neg")
        for k in pm6_keys
    )
    pm1_ok = all(bool(cures[n]["cured_sectioned"]) for n in two_label)
    pm2_ok = all("refused" not in phase2[n] for n in two_label)

    phase_2 = {
        "two_label_members": two_label,
        "cure_witnesses": cures,
        "exhaustions": phase2,
        "consumed_class_route": classes,
        "route_agreement": route_agreement,
        "predictions": {
            "PM1": dispose(pm1_ok, "every concretized cure witness sections"),
            "PM2": dispose(pm2_ok, "all seven members within the slot bound"),
            "PM3": dispose(
                pm3_ok,
                {
                    "flip_count": square["flip_count"],
                    "price": square["price_min_slots_from_pointwise"],
                },
            ),
            "PM4": "recorded, not predicted: "
            + json.dumps(
                {
                    n: phase2[n]["price_min_slots_from_pointwise"]
                    for n in two_label
                },
                sort_keys=True,
            ),
            "PM5": "held: the closed form stays CONJECTURE; support is the"
            " two-route agreement map",
            "PM6": dispose(pm6_ok, "signed pair agrees with the square"),
        },
    }

    # Phase 3: the six-label experiment.
    crosscheck = binary_crosscheck(sixlabel_member())
    six = sixlabel_exhaust()
    phase_3 = {
        "binary_crosscheck": crosscheck,
        "exhaustion": six,
        "predictions": {
            "PS1": dispose(
                int(str(six["assignments"])) == 65536, six["assignments"]
            ),
            "PS2": f"decided by the exhaustion alone: {six['terminal']}",
            "PS3": dispose(int(str(crosscheck["misses"])) == 0, crosscheck),
            "PS4": dispose(
                not bool(six["base_sectioned"]) and census_agrees,
                "base obstructed; census reproduced",
            ),
        },
    }

    # Phase 4: the channel table.
    rows: list[dict[str, object]] = []
    for name in ("signed_square_pos", "signed_square_neg"):
        verdict = (
            "CURABLE_WITHIN_BOUND"
            if int(str(phase2[name]["flip_count"])) > 0
            else "NOT_CURABLE_WITHIN_BOUND"
        )
        rows.append(channel_row(name, presentations[name], verdict, "phase_2"))
    for entry in obstructed:
        name = str(entry["name"])
        p = signed_variant(presentations[name])
        if int(str(entry["fibre"])) == 2:
            verdict = (
                "CURABLE_WITHIN_BOUND"
                if int(str(phase2[name]["flip_count"])) > 0
                else "NOT_CURABLE_WITHIN_BOUND"
            )
            source = "phase_2"
        elif name == "square_2x2_occ3":
            verdict = (
                "CURABLE_WITHIN_BOUND"
                if six["terminal"] == "SIXLABEL_MOVES"
                else "NOT_CURABLE_WITHIN_BOUND"
            )
            source = "phase_3"
        else:
            verdict = "NOT_COVERED_BY_BOUND"
            source = "none"
        rows.append(channel_row(f"signed_variant_of_{name}", p, verdict, source))
    separation = separation_verdict(rows)
    pt5_ok = signed_variant(presentations["square_2x2_occ2"]) == presentations[
        "signed_square_pos"
    ]
    unit_single_signed = {
        str(e["name"]): all(v > 0 for v in weight_list(presentations[str(e["name"])]))
        for e in obstructed
    }
    phase_4 = {
        "rows": rows,
        "separation": separation,
        "predictions": {
            "PT1": dispose(len(rows) == 11, f"{len(rows)} rows, none discarded"),
            "PT2": "held: NOT_COVERED_BY_BOUND recorded, distinct from a no",
            "PT3": "held: counting characterization reconstructed; sides per row",
            "PT4": f"decided by the table alone: {separation['terminal']};"
            f" magnitude degeneracy {separation['magnitude_degeneracy']}",
            "PT5": dispose(pt5_ok, "signed_square_pos is the square's variant"),
        },
        "unit_weight_lists_single_signed": unit_single_signed,
    }

    # Phase 5: the register.
    reg = build_register(
        obstructed,
        phase2,
        six,
        rows,
        bool(separation["magnitude_degeneracy"]),
    )
    phase_5 = {
        "rows": reg,
        "predictions": {
            "PR1": dispose(len(reg) == len(obstructed), len(reg)),
            "PR2": dispose(all(bool(r["leftovers"]) for r in reg), "every row"),
            "PR3": "held: see terminals and STATUS.md",
            "PR4": "held: price tie counts recorded in phase 2 and phase 3",
        },
    }

    adversarial = {
        "A1": "refuted: different groups -- pointwise_parity_blind IS the"
        " invariance at parity level; slot_group_sections quantifies over"
        " the strictly larger per-slot group",
        "A2": "refuted by FW-SCOPE and FW-SET: two labels, declared"
        " bounds, a slice -- the supplied challenge is not answered",
        "A3": "refuted: one member, one bound, computed; no analogy",
        "A4": "decided per member; the price map is in phase 2; no"
        " extrapolation",
        "A5": f"decided by the table: {separation['terminal']}; the"
        " magnitude degeneracy is named next to it",
        "A6": "refuted: unit-weight members' walk lists are single-signed;"
        " recorded per member in phase 4",
        "A7": "refuted: phase 3 is computation; its leftover stays OPEN"
        " where the terminal leaves one",
        "A8": "refuted by FW-SET: the census is a declared slice",
        "A9": "partial only: the two-label half of SS-09 closes with"
        " slot_group_sections; the larger-fibre half stays OPEN",
        "A10": "refuted: Lean proves; receipts record runs; neither is"
        " the other",
    }

    terminals = [
        {"code": "PARITY_LAWS_PROVED", "scope": "the abstract two-label parity"
         " model; three targets plus the cycle-invariance corollary; axiom"
         " reports within the whitelist"},
        {"code": "PROMOTION_PROVED", "scope": "two-label only: the Lean cure"
         " theorem, plus price floors decided by exhaustion at all seven"
         " obstructed two-label members under the declared slot bound"},
        {"code": str(six["terminal"]), "scope": str(six["bound"])},
        {"code": str(separation["terminal"]), "scope": "the declared 11-row"
         " signed census at walk bound 6; decided rows only; the magnitude"
         " degeneracy is recorded next to it"},
        {"code": "TABLE_WRITTEN", "scope": "11 rows, cells computed"},
        {"code": "REGISTER_WRITTEN", "scope": f"{len(reg)} rows"},
        {"code": "TIES_RETAINED", "scope": "price ties recorded as counts"},
        {"code": "PREDICTIONS_HASHED", "scope": "two freezes, hashes in"
         " SOURCE_MANIFEST.json"},
        {"code": "MANUAL_RECEIPT_DECLARED", "scope": "no CI gate reads this"
         " tree's receipts, scans, or Lean audit"},
        {"code": "SS09_PARTIALLY_CLOSED", "scope": "the two-label half closes"
         " with slot_group_sections; the larger-fibre half stays OPEN"},
        {"code": "OB1_UNCHANGED", "scope": "untouched"},
        {"code": "S66_UNCHANGED", "scope": "untouched"},
        {"code": "S9_LAST_UNCHANGED", "scope": "untouched"},
        {"code": "FW_SET_HELD", "scope": "no completed-classification"
         " sentence anywhere in this tree"},
    ]

    receipt = {
        "authority_effect": "None",
        "census_reproduced": census_agrees,
        "phase_2_promotion": phase_2,
        "phase_3_sixlabel": phase_3,
        "phase_4_channels": phase_4,
        "phase_5_register": phase_5,
        "adversarial": adversarial,
        "terminals": terminals,
        "prompt_native_sha256": hashlib.sha256(
            (HERE / "PROMPT.md").read_bytes()
        ).hexdigest(),
        "predictions_sha256": hashlib.sha256(
            (HERE / "PREDICTIONS.md").read_bytes()
        ).hexdigest(),
    }
    payload = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("ascii")
    (out_dir / "convention_price.json").write_bytes(payload)

    print(f"census reproduced: {census_agrees}")
    for name in two_label:
        print(
            f"{name}: flips {phase2[name]['flip_count']},"
            f" price {phase2[name]['price_min_slots_from_pointwise']},"
            f" ties {phase2[name]['price_tie_count']},"
            f" routes agree {route_agreement[name]}"
        )
    print(f"sixlabel: {six['terminal']}, flips {six['flip_count']},"
          f" price {six['price_min_slots_from_pointwise']}")
    print(f"channels: {separation['terminal']}, cells {separation['cells']}")
    print(f"register rows: {len(reg)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
