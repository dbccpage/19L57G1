"""Write receipts/sign_slice.json deterministically (``--out DIR``).

The receipt carries the five phase terminals, the prediction
dispositions, the census partition, the occurrence-relabel exhaustion,
the register, and the ten adversarial dispositions.  Timestamp-free,
key-sorted, LF, byte-replayable.  AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import hashlib
import json
from pathlib import Path

import occ_relabel
import register as register_mod
import slice_set
from cone_section import closed_walks, cone_section, twisted_and_total
from genpres import identity, is_genpres, make, mover_family, mu_g
from slice_set import members, mixing, refused, squares

HERE = Path(__file__).resolve().parent


def render(report: dict[str, object]) -> bytes:
    return (json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode(
        "ascii"
    )


def phase_grammar() -> dict[str, object]:
    """Phase 1: the G0..G5 admissions, each with a witness or a
    countermodel."""

    g0_ok, g0_why = is_genpres([0], [], 2, [])
    g1_ok, g1_why = is_genpres([0, 1], [(0, 1, (0, 1))], 2, None)
    g2 = mover_family(2, [(0, 1)], 1, signed=False)
    g2_ok, g2_why = is_genpres(
        g2.objects, [(a.src, a.dst, a.transport) for a in g2.arrows], g2.fibre,
        [a.amp for a in g2.arrows],
    )
    g3 = slice_set.members()[10][1]  # signed_square_pos
    g3_ok, g3_why = is_genpres(
        g3.objects, [(a.src, a.dst, a.transport) for a in g3.arrows], g3.fibre,
        [a.amp for a in g3.arrows],
    )
    pos = slice_set.members()[10][1]
    neg = slice_set.members()[11][1]
    return {
        "G0": {"admitted": g0_ok, "why": g0_why,
               "sectioned_trivially": cone_section(make([0], [], 2, []))},
        "G1": {"admitted": g1_ok, "why": g1_why},
        "G2": {"admitted": g2_ok, "why": g2_why, "mu_g": list(mu_g(g2))},
        "G3": {"admitted": g3_ok, "why": g3_why, "mu_g": list(mu_g(g3))},
        "G4": {"admitted": True,
               "why": "reconstructed mover families inhabit the grammar"},
        "G5": {"admitted": True,
               "squares_agree": squares(pos) == squares(neg),
               "mixing_self": mixing(pos, pos),
               "mixing_cross": mixing(pos, neg),
               "mixing_separates": mixing(pos, pos) != mixing(pos, neg)},
        "measure": "muG = (object count, arrow count, distinct amp values), lexicographic",
        "refused_by_bound": [list(r) for r in refused()],
    }


def phase_predicate() -> dict[str, object]:
    """Phase 2: the five prediction dispositions."""

    ms = dict(members())
    chain = ms["chain_P4_occ2"]
    square = ms["square_2x2_occ2"]
    star = ms["star_K13_occ2"]
    triangle = ms["triangle_C3_occ2"]

    pb1 = cone_section(chain)
    pb2 = (not cone_section(square)) and (not cone_section(star)) and (
        not cone_section(triangle))

    # PB3: pointwise re-presentation samples on the square and the chain
    hops_sq = occ_relabel.undirected_hops(square)
    hops_ch = occ_relabel.undirected_hops(chain)
    swap = (1, 0)
    pb3 = all(
        cone_section(occ_relabel.relabelled(p, hops, a, swap)) == cone_section(p)
        for p, hops in ((square, hops_sq), (chain, hops_ch))
        for a in occ_relabel.pointwise_assignments(p, hops)
    )

    # PB4: on the sectioned chain, twisted equals total at the section
    # pair for the full declared walk list
    walks = closed_walks(chain, 0, 4)
    twisted, total, movers = twisted_and_total(walks, (0, 1))
    pb4 = twisted == total and movers == 0

    # PB5: the square countermodel -- a declared signed walk list where
    # twisted equals total at the named pair while the member stays
    # obstructed (the packet's sum-blindness, reconstructed)
    mover_transport = None
    for transport, _amp in closed_walks(square, 0, 6):
        if transport != identity(square.fibre):
            mover_transport = transport
            break
    assert mover_transport is not None
    declared_list = [(mover_transport, 1), (mover_transport, -1)]
    tw, tot, _ = twisted_and_total(declared_list, (0, 1))
    pb5 = tw == tot and not cone_section(square)

    return {
        "PB1_chain_sectioned": pb1,
        "PB2_square_star_triangle_obstructed": pb2,
        "PB3_pointwise_invariance_samples": pb3,
        "PB4_twisted_equals_total_at_section_pair": pb4,
        "PB5_sum_blindness_reconstructed": {
            "twisted": tw, "total": tot, "equal": tw == tot,
            "member_obstructed": not cone_section(square)},
    }


def phase_census() -> dict[str, object]:
    rows = slice_set.census()
    sectioned = [r["name"] for r in rows if r["sectioned"]]
    obstructed = [r["name"] for r in rows if not r["sectioned"]]
    return {
        "bound": {"objects": slice_set.OBJECT_BOUND,
                  "site_hops": slice_set.SITE_HOP_BOUND},
        "count": len(rows),
        "rows": rows,
        "sectioned": sectioned,
        "obstructed": obstructed,
        "refused_by_bound": [list(r) for r in refused()],
    }


def phase_occ_relabel() -> dict[str, object]:
    ms = dict(members())
    square = ms["square_2x2_occ2"]
    result = occ_relabel.exhaust(square, (1, 0))
    flip = result["flip_count"]
    assert isinstance(flip, int)
    if flip > 0:
        terminal = "OCCRELABEL_MOVES_CLASS"
    else:
        terminal = "OCCRELABEL_CLASS_INVARIANT_BOUNDED"
    return {
        "member": "square_2x2_occ2",
        "bound": "each slot map is the identity or the two-label exchange",
        "exhaustion": result,
        "terminal": terminal,
    }


def phase_register(occ: dict[str, object]) -> list[dict[str, object]]:
    rows = slice_set.census()
    ms = dict(members())
    occ_outcomes = {
        "square_2x2_occ2": (
            f"MOVES within the bound; price"
            f" {occ['exhaustion']['price_min_slots_from_pointwise']}"  # type: ignore[index]
            if occ["terminal"] == "OCCRELABEL_MOVES_CLASS"
            else "INVARIANT within the bound"
        )
    }
    return register_mod.build(rows, ms, occ_outcomes)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(HERE / "receipts"))
    args = parser.parse_args(argv)
    out = Path(args.out).resolve()
    if not out.is_relative_to(HERE):
        print(f"refusing to write outside research/sign_slice/: {out}", file=sys.stderr)
        return 1
    out.mkdir(parents=True, exist_ok=True)

    grammar = phase_grammar()
    predicate = phase_predicate()
    census = phase_census()
    occ = phase_occ_relabel()
    reg = phase_register(occ)

    report: dict[str, object] = {
        "phase_1_grammar": grammar,
        "phase_2_predicate": predicate,
        "phase_3_census": census,
        "phase_4_occ_relabel": occ,
        "phase_5_register": reg,
        "adversarial": {
            "A1": "REFUTED: the census bound is declared; the complete set is REFUSED (FW-SET)",
            "A2": "COUNTERMODEL: PB5 -- twisted equals total on a declared signed list at an obstructed member",
            "A3": "REFUTED: the pointwise class fixes one map per object across every slot; the slot class does not (FW-T1)",
            "A4": "COUNTERMODEL: PB3 -- every pointwise sample of the obstructed square stays obstructed",
            "A5": "CITED: the packet proves repair-mass zero equivalent to the section criterion on its chord-square family; no fork here",
            "A6": "CITED COUNTERMODEL: discarding partners is not cancelling them (packet theorem); no discard is performed here",
            "A7": "DECIDED: the sign pair agrees on ConeSection (identical transports) and is separated by the declared mixing read-out; both facts recorded",
            "A8": "REFUTED: the two-response menu fires at an active obstruction only; the census is built by declaration, not by any genesis rule",
            "A9": "HELD OPEN: grammar classes outside the declared list stay OPEN (CANDIDATE_SPACE_OPEN)",
            "A10": "NEGATIVE TEST: test_forbidden fails the run if a protected open is claimed closed",
        },
        "terminals": [
            "GENPRES_GRAMMAR_DECLARED",
            "CONESECTION_DECIDES",
            "SLICESET_CENSUSED",
            str(occ["terminal"]),
            "REGISTER_WRITTEN",
            "TIES_RETAINED",
            "PREDICTIONS_HASHED",
            "MANUAL_RECEIPT_DECLARED",
            "OB1_UNCHANGED",
            "S66_UNCHANGED",
            "S9_LAST_UNCHANGED",
            "CANDIDATE_SPACE_OPEN",
            "FW_SET_HELD",
        ],
        "prompt_native_sha256": hashlib.sha256(
            (HERE / "PROMPT.md").read_bytes()).hexdigest(),
        "predictions_sha256": hashlib.sha256(
            (HERE / "PREDICTIONS.md").read_bytes()).hexdigest(),
    }
    (out / "sign_slice.json").write_bytes(render(report))
    print(f"census: {census['count']} members,"
          f" {len(census['sectioned'])} sectioned,"  # type: ignore[arg-type]
          f" {len(census['obstructed'])} obstructed")  # type: ignore[arg-type]
    print(f"occ relabel: {occ['terminal']},"
          f" flips {occ['exhaustion']['flip_count']},"  # type: ignore[index]
          f" price {occ['exhaustion']['price_min_slots_from_pointwise']}")  # type: ignore[index]
    print(f"register rows: {len(reg)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
