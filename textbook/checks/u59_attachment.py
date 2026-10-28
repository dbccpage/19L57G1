"""Unit 59 check: one-edge attachment, tree policies, shape non-forcing,
and the renaming structure around Up.

Runs Genesis's mirrors `code/derivation/attachment_ladder.py` (sections 1-4)
and `code/derivation/renaming_structure.py`, adds Python (book) checks for
the `WFStores` hypothesis of `up_executes` and the `n <= len(s.occ)` scope
hypothesis of `act`, and compares against `artifacts/attachment_ladder.json`
and `artifacts/renaming_structure.json`.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u59_attachment.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.attachment_ladder import (  # noqa: E402
    act,
    attach_checked,
    clamp_countermodel,
    fresh_tok,
    is_tree,
    isomorphic_undirected,
    length_not_fresh_countermodel,
    parent_orbits,
    path_pol,
    renaming_report as attach_renaming_report,
    shape_report,
    star_pol,
    store_automorphisms,
    tree_at,
    tree_report,
    up_block,
    up_family,
    up_report,
    zigzag_pol,
)
from derivation.primitive_passage import PS, preplay  # noqa: E402
from derivation.renaming_structure import (  # noqa: E402
    action_laws,
    coherence,
    comp_ren,
    equal_cost_countermodel,
    equal_size_countermodel,
    group_laws,
    id_ren,
    inv_ren,
    non_bijective_countermodel,
    orbit_no_selection,
    renaming_report as ren_structure_report,
    transport_laws,
)


def main() -> int:
    failures: list[str] = []

    clamp = clamp_countermodel()
    len_cm = length_not_fresh_countermodel()
    print(f"clamp rewrote input: {clamp['rewritten_input_is_not_lawful']}; "
          f"length-as-token fails on (1,2): {len_cm['old_block_fails_to_extend']}, "
          f"fresh_tok(s12)={len_cm['canonical_fresh_token']}, "
          f"repaired extends: {len_cm['repaired_block_extends']}")
    if not (clamp["rewritten_input_is_not_lawful"]
            and len_cm["old_block_fails_to_extend"]
            and len_cm["canonical_fresh_token"] == 3
            and len_cm["repaired_block_extends"]):
        failures.append("countermodels_1_2")

    up_rep = up_report()
    print(f"up_family iff legal: {up_rep['every_member_is_legal'] and up_rep['every_legal_is_member']}; "
          f"typed refusal: {up_rep['typed_refusal']}; "
          f"star3 orbits: {up_rep['star3_parent_orbits']}; "
          f"path3 orbits: {up_rep['path3_parent_orbits']}")
    if not (up_rep["every_member_is_legal"] and up_rep["every_legal_is_member"]
            and up_rep["out_of_registry_absent"]
            and up_rep["star_leaves_one_orbit"]
            and up_rep["oriented_path_rigid"]):
        failures.append("up_report")

    # Python (book): on an ill-formed live state where (0, 2) is already in
    # the three stores before position 2 exists, attach_checked returns
    # "attached" because 0 < 2 and live, yet the assert/wit/prot guards fail
    # on the duplicate pair and none of the relational stores grows
    # (showing WFStores in up_executes is load-bearing).
    s_ill = PS(occ=(1, 2), asserted=((0, 2),), wit=((0, 2),), prot=((0, 2),))
    ill_out = attach_checked(s_ill, 0)
    s_halted = PS(occ=(1, 2), halted=True)
    halted_out = attach_checked(s_halted, 0)
    print(f"Python (book): ill-formed attach_checked outcome={ill_out['outcome']}, "
          f"occ_len={ill_out['occ_len']}, wit_len={ill_out['wit_len']} (unchanged from 1); "
          f"halted attach_checked outcome={halted_out['outcome']}")
    if ill_out != {"outcome": "attached", "occ_len": 3, "wit_len": 1}:
        failures.append("wf_load_bearing")
    if halted_out["outcome"] != "refusedParent":
        failures.append("halted_refused")

    trees = tree_report(15)
    for name, pi in (("path", path_pol), ("star", star_pol), ("zigzag", zigzag_pol)):
        sub = trees[name]
        assert isinstance(sub, dict)
        print(f"  policy {name}: lawful={sub['lawful_to_rounds']}, "
              f"spec={sub['all_spec_match']}, V-E=1={sub['all_residue_one']}, "
              f"trees={sub['all_trees']}, up_blocks={sub['all_blocks_are_up_blocks']}")
        if not (sub["lawful_to_rounds"] and sub["all_spec_match"]
                and sub["all_residue_one"] and sub["all_trees"]
                and sub["all_blocks_are_up_blocks"]):
            failures.append(f"tree_{name}")

    sh = shape_report()
    print(f"shape report: path4={sh['path4']}, star4={sh['star4']}, "
          f"isomorphic_undirected={sh['isomorphic_undirected']}")
    if sh["isomorphic_undirected"] or not sh["trees_but_shapes_differ"]:
        failures.append("shape")

    gl = group_laws(3)
    al = action_laws(3)
    tl = transport_laws(3)
    coh = coherence(3)
    orb = orbit_no_selection(3)
    nb_cm = non_bijective_countermodel()
    es_cm = equal_size_countermodel()
    ec_cm = equal_cost_countermodel()
    print(f"Renaming(3): order={gl['group_order']}, "
          f"group_laws={all(gl[k] for k in ('comp_id', 'id_comp', 'comp_assoc', 'inv_comp', 'comp_inv', 'inv_inv'))}, "
          f"action_laws={all(al.values())}, transport={all(tl.values())}, "
          f"coherence={all(coh.values())}, orbit={all(orb.values())}")
    print(f"countermodels: non_bijective no_inv={nb_cm['no_left_inverse']} "
          f"self_pairs={nb_cm['pushforward_all_self_pairs']}; "
          f"equal_size no_ren={es_cm['no_renaming_relates']}; "
          f"equal_cost non_iso={ec_cm['executions_non_isomorphic']}")
    if not (all(gl[k] for k in ("comp_id", "id_comp", "comp_assoc", "inv_comp", "comp_inv", "inv_inv"))
            and all(al.values()) and all(tl.values())
            and all(coh.values()) and all(orb.values())
            and nb_cm["no_left_inverse"] and nb_cm["pushforward_all_self_pairs"]
            and es_cm["same_carrier"] and es_cm["families_literally_equal"]
            and es_cm["no_renaming_relates"]
            and ec_cm["both_in_family"] and ec_cm["equal_cost"]
            and ec_cm["executions_non_isomorphic"]):
        failures.append("renaming_structure")

    # Compare against committed artifacts
    art_al = json.loads((ROOT / "artifacts" / "attachment_ladder.json").read_text())
    art_rs = json.loads((ROOT / "artifacts" / "renaming_structure.json").read_text())
    al_match = (art_al["trees"] == trees and art_al["shape"] == sh
                and art_al["up"] == up_rep
                and art_al["renaming"] == attach_renaming_report())
    rs_match = (art_rs == ren_structure_report(3))
    print(f"attachment_ladder sections match artifact: {al_match}; "
          f"renaming_structure report matches artifact: {rs_match}")
    if not (al_match and rs_match):
        failures.append("artifact")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
