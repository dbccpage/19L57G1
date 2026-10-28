"""Unit 60 check: the dimension-uniform guarded filler, the vacuity probe on
`d2_zero_dims_2_3_4`, and general boundary cancellation.

Runs Genesis's mirrors `code/derivation/attachment_ladder.py` (section 5)
and `code/derivation/boundary_cancellation.py`, adds the Python (book)
vacuity demonstration on `d2_zero_dims_2_3_4` conjuncts 1 and 2, and
compares against `artifacts/attachment_ladder.json` and
`artifacts/boundary_cancellation.json`.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u60_ladder_boundary.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.attachment_ladder import (  # noqa: E402
    combs,
    ladder_report,
    pseudo_cell_countermodel,
)
from derivation.boundary_cancellation import (  # noqa: E402
    bd_n,
    bd_no_sign,
    cancellation_report,
    coeff_n,
    facets,
    illformed_countermodel,
    involution_report,
    push_n,
    push_no_sign,
    renaming_report,
    signless_countermodel,
    support,
)


def main() -> int:
    failures: list[str] = []

    lad = ladder_report(5)
    pcm = pseudo_cell_countermodel()
    print(f"ladder dims {lad['dims_checked']}: fire={lad['all_ladders_fire']}, "
          f"guards={lad['all_guards_load_bearing']}, wf={lad['all_wf']}, "
          f"d2_zero={lad['all_d2_zero']}; pseudo_cell={pcm}")
    if not (lad["all_ladders_fire"] and lad["all_guards_load_bearing"]
            and lad["all_wf"] and lad["all_d2_zero"]
            and pcm["legacy_admits_pseudo_cell"]
            and pcm["repaired_refuses"]
            and pcm["repaired_step_inert"]):
        failures.append("ladder")

    # Python (book): demonstrate why conjuncts 1 and 2 of Lean's
    # `LadderGeneral.d2_zero_dims_2_3_4` are vacuous (testing 1-step
    # facets `e in facets(t)` instead of 2-step faces `v in facets(e)`),
    # whereas conjunct 3 (and Python's `d2_zero_dim`) tests codimension-2 faces.
    conj1_signless_vacuous = all(
        coeff_n(e, push_no_sign(bd_no_sign(t))) == 0
        for t in combs(5, 2) for e in facets(t)
    )
    conj2_signless_vacuous = all(
        coeff_n(t2, push_no_sign(bd_no_sign(q))) == 0
        for q in combs(5, 3) for t2 in facets(q)
    )
    repaired_dim2_signless = all(
        coeff_n(v, push_no_sign(bd_no_sign(t))) == 0
        for t in combs(5, 2) for e in facets(t) for v in facets(e)
    )
    repaired_dim2_signed = all(
        coeff_n(v, push_n(bd_n(t))) == 0
        for t in combs(5, 2) for e in facets(t) for v in facets(e)
    )
    conj3_signless = all(
        coeff_n(t2, push_no_sign(bd_no_sign((0, 1, 2, 3, 4)))) == 0
        for q in facets((0, 1, 2, 3, 4)) for t2 in facets(q)
    )
    print(f"Python (book) vacuity check: "
          f"conj1_signless_vacuous={conj1_signless_vacuous}, "
          f"conj2_signless_vacuous={conj2_signless_vacuous}, "
          f"repaired_dim2_signless={repaired_dim2_signless}, "
          f"repaired_dim2_signed={repaired_dim2_signed}, "
          f"conj3_signless={conj3_signless}")
    if not (conj1_signless_vacuous and conj2_signless_vacuous
            and not repaired_dim2_signless and repaired_dim2_signed
            and not conj3_signless):
        failures.append("vacuity_probe")

    canc = cancellation_report()
    ren = renaming_report()
    sl_cm = signless_countermodel()
    ill_cm = illformed_countermodel()
    inv5 = involution_report(5)
    bnds = canc["bounds"]
    assert isinstance(bnds, dict)
    print(f"boundary cancellation: cells={bnds['cells_checked']}, "
          f"coeff_checks={bnds['coefficient_checks']}, "
          f"all_cancel={canc['all_cancel']}, all_distinct={canc['all_distinct']}, "
          f"inv5_bijection={inv5['is_bijection'] and inv5['sign_reversing']}")
    print(f"renaming: monotone_ascent={ren['monotone_preserves_ascent']}, "
          f"non_monotone_breaks_ascent={ren['non_monotone_breaks_ascent']}, "
          f"non_monotone_still_cancels={ren['non_monotone_still_cancels']}")
    print(f"countermodels: signless_nonzero={sl_cm['all_signless_nonzero']}; "
          f"illformed erase_inj={ill_cm['erase_injective']}, "
          f"slot_mult={ill_cm['slot_multiplicity_pseudo']} vs {ill_cm['slot_multiplicity_well_formed']}, "
          f"still_vanishes={ill_cm['composite_still_vanishes']}")
    if not (canc["all_cancel"] and canc["all_distinct"]
            and canc["sgn_alternates"] and canc["sgn_cancel_pairs"]
            and ren["monotone_preserves_ascent"]
            and ren["non_monotone_breaks_ascent"]
            and ren["non_monotone_still_cancels"]
            and sl_cm["all_signless_nonzero"] and sl_cm["all_signed_zero"]
            and not ill_cm["erase_injective"]
            and ill_cm["two_positions_one_facet"]
            and ill_cm["boundary_forgets_a_facet"]
            and ill_cm["slot_multiplicity_pseudo"] == 4
            and ill_cm["slot_multiplicity_well_formed"] == 2
            and ill_cm["composite_still_vanishes"]):
        failures.append("boundary_cancellation")

    art_al = json.loads((ROOT / "artifacts" / "attachment_ladder.json").read_text())
    art_bc = json.loads((ROOT / "artifacts" / "boundary_cancellation.json").read_text())
    al_ok = art_al["ladder"] == lad
    bc_ok = (art_bc["cancellation"] == canc and art_bc["renaming"] == ren
             and art_bc["countermodels"] == {"signless": sl_cm, "illformed": ill_cm})
    print(f"ladder matches attachment_ladder.json: {al_ok}; "
          f"boundary_cancellation matches artifact: {bc_ok}")
    if not (al_ok and bc_ok):
        failures.append("artifact")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
