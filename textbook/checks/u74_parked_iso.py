from __future__ import annotations

import json
import pathlib
import sys
from dataclasses import dataclass

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code"))

from derivation.iso import (  # noqa: E402
    IsoBudgetError,
    canonical,
    canonical_bruteforce,
    find_iso,
    isomorphic,
    rename,
    serialize,
)
from derivation.model import Inst, Pair, Regime  # noqa: E402
from derivation.observe import profile  # noqa: E402


@dataclass(frozen=True)
class LeanRegime:
    """List-backed mirror of Lean's Derivation.Regime (where insts, rules, reqs are Lists)."""

    data: int
    forms: tuple[int, ...]
    insts: tuple[Inst, ...]
    rules: tuple[int, ...]
    reqs: tuple[Pair, ...]


def sort_pair(i: int, j: int) -> Pair:
    return (i, j) if i <= j else (j, i)


def lean_relabel(
    r: LeanRegime, f: tuple[int, ...], g: tuple[int, ...], fg: tuple[int, ...]
) -> LeanRegime:
    """Direct mirror of Lean's IsoCanon.relabel (f, fg, g)."""
    m = len(r.forms)
    forms_out = tuple(r.forms[fg[j]] if fg[j] < m else 0 for j in range(m))
    insts_out = tuple((g[ins[0]], tuple(f[x] for x in ins[1])) for ins in r.insts)
    rules_out = tuple(g[ru] for ru in r.rules)
    reqs_out = tuple(sort_pair(f[q[0]], f[q[1]]) for q in r.reqs)
    return LeanRegime(r.data, forms_out, insts_out, rules_out, reqs_out)


def lean_iso_holds(
    r: LeanRegime, s: LeanRegime, f: tuple[int, ...], g: tuple[int, ...]
) -> bool:
    """Direct mirror of Lean's Minimality.Iso membership-iff conditions."""
    if r.data != s.data or len(r.forms) != len(s.forms):
        return False
    for k in range(len(r.forms)):
        if g[k] >= len(s.forms) or s.forms[g[k]] != r.forms[k]:
            return False
    mapped_insts = {(g[ins[0]], tuple(f[x] for x in ins[1])) for ins in r.insts}
    if set(s.insts) != mapped_insts:
        return False
    mapped_rules = {g[ru] for ru in r.rules}
    if set(s.rules) != mapped_rules:
        return False
    mapped_reqs = {sort_pair(f[q[0]], f[q[1]]) for q in r.reqs}
    if set(s.reqs) != mapped_reqs:
        return False
    return True


PARKED_12 = [
    "Derivation.Composing",
    "Derivation.DiffAnchor",
    "Derivation.DiffAnchorCompat",
    "Derivation.FormRenaming",
    "Derivation.FormTransport",
    "Derivation.FormTransportCompat",
    "Derivation.IsoBridge",
    "Derivation.IsoBridgeCompat",
    "Derivation.IsoCanon",
    "Derivation.IsoCanonCompat",
    "Derivation.IsoCollapse",
    "Derivation.IsoCollapseCompat",
]

COMPAT_5 = [
    "DiffAnchorCompat",
    "FormTransportCompat",
    "IsoBridgeCompat",
    "IsoCanonCompat",
    "IsoCollapseCompat",
]

PARKED_THEOREM_GROUPS = {
    "Composing": {
        "Composing.composite_may_be_nonunique",
        "Composing.composition_may_fail",
        "Composing.noneCompose_no_identity",
        "Composing.relAssocLeft_of_relAssoc",
        "Composing.selection_is_possible",
        "Composing.skew_not_relAssoc",
        "Composing.skew_not_relAssocLeft",
    },
    "DiffAnchor": {
        "DiffAnchor.colObs_deltaConstant",
        "DiffAnchor.colObs_quotient_eq_iff_zeroP",
        "DiffAnchor.colObs_zeroRel_iff_zeroP",
    },
    "FormRenaming": {
        "Derivation.Regime.ext'",
        "Derivation.mapInstForm_gf",
        "Derivation.permForms_getD",
        "Derivation.permForms_length",
        "Derivation.renameForms_arity",
        "Derivation.renameForms_data",
        "Derivation.renameForms_forms_length",
        "Derivation.renameForms_gf",
        "Derivation.renameForms_reqs",
    },
    "FormTransport": {
        "Derivation.collapsed_congr",
        "Derivation.collapsed_renameDataForm",
        "Derivation.collapsed_renameForms",
        "Derivation.derivable_renameForms",
        "Derivation.mapCtxForm_f_g",
        "Derivation.mapInstForm_inj",
        "Derivation.plug_mapCtxForm",
        "Derivation.renameForms_forms",
        "Derivation.renameForms_insts",
        "Derivation.renameForms_rules",
        "Derivation.wfCtx_renameForms",
    },
    "IsoCanon": {
        "Derivation.mapReq_eq_sortPair",
        "Derivation.relabel_data",
        "Derivation.relabel_forms",
        "Derivation.relabel_insts",
        "Derivation.relabel_reqs",
        "Derivation.relabel_rules",
        "Derivation.sortPair_comm",
        "Derivation.sortPair_eq_minmax",
        "Derivation.sortPair_map_sortPair",
        "Derivation.sortPair_of_le",
    },
    "IsoCollapse": {
        "Derivation.Iso.collapsed_fwd",
        "Derivation.Iso.collapsed_transport",
        "Derivation.Iso.derivable_imap",
        "Derivation.Iso.plug_cmap",
        "Derivation.Iso.symm_dmap",
        "Derivation.Iso.wfCtx_cmap",
        "Derivation.map_eq_self_of_mem",
        "Derivation.plug_args_lt",
    },
    "IsoBridge": set(),
}

EXPECTED_PARKED_COUNTS = {k: len(v) for k, v in PARKED_THEOREM_GROUPS.items()}


def main() -> int:
    failures: list[str] = []

    # 1. Isomorphic regimes under simultaneous datum + form renaming,
    #    collapse transport, and canonical key agreement with canonical_bruteforce.
    r1 = Regime(
        data=("d0", "d1", "d2"),
        forms=(1, 2),
        insts=frozenset({(0, (0,)), (1, (0, 1)), (1, (0, 2))}),
        rules=frozenset(),
        reqs=frozenset({(1, 2)}),
    )
    # Note: d1 and d2 are observationally collapsed in r1 (both only appear in (1, (0, d)))
    if profile(r1, 1) != profile(r1, 2):
        failures.append("d1 and d2 should be observationally collapsed in r1")

    pi = (2, 1, 0)
    phi = (1, 0)
    r2 = rename(r1, pi, phi)

    if not isomorphic(r1, r2):
        failures.append("r1 and r2 = rename(r1, pi, phi) must be isomorphic")
    if find_iso(r1, r2) is None:
        failures.append("find_iso(r1, r2) returned None")
    if canonical(r1) != canonical(r2):
        failures.append("canonical(r1) != canonical(r2)")
    if canonical(r1) != canonical_bruteforce(r1) or canonical(r2) != canonical_bruteforce(r2):
        failures.append("canonical disagreed with canonical_bruteforce")
    # Transport of observational collapse across isomorphism (Iso.collapsed_transport / collapsed_renameDataForm):
    # pi maps 1 -> 1 and 2 -> 0, so in r2 data 1 and 0 must be observationally collapsed:
    if profile(r2, pi[1]) != profile(r2, pi[2]):
        failures.append("collapsed_transport failed: profile(r2, pi[1]) != profile(r2, pi[2])")

    # 2. Gap 1 (IsoCanon.relabel literal list order vs. iso.serialize sorted tuples):
    lr1 = LeanRegime(
        data=3,
        forms=(1, 2),
        insts=((0, (0,)), (1, (0, 1))),
        rules=(0,),
        reqs=((0, 2),),
    )
    lr_reordered = LeanRegime(
        data=3,
        forms=(1, 2),
        insts=((1, (0, 1)), (0, (0,))),
        rules=(0,),
        reqs=((0, 2),),
    )
    id_f = (0, 1, 2)
    id_g = (0, 1)
    if lean_relabel(lr1, id_f, id_g, id_g) == lean_relabel(lr_reordered, id_f, id_g, id_g):
        failures.append("lean_relabel should preserve list order and distinguish lr1 from lr_reordered")
    if not lean_iso_holds(lr1, lr_reordered, id_f, id_g):
        failures.append("Minimality.Iso (set membership) should hold between lr1 and lr_reordered")

    # 3. Gap 2 (Minimality.Iso set-membership semantics vs. duplicate list entries):
    lr_dup = LeanRegime(
        data=3,
        forms=(1, 2),
        insts=((0, (0,)), (0, (0,)), (1, (0, 1))),
        rules=(0,),
        reqs=((0, 2),),
    )
    if not lean_iso_holds(lr1, lr_dup, id_f, id_g):
        failures.append("Minimality.Iso should equate [p, q] and [p, p, q] by membership iff")
    if len(lr1.insts) == len(lr_dup.insts):
        failures.append("lr1 and lr_dup should differ in list length")

    # 4. Gap 3 (IsoBudgetError when candidate permutations exceed perm_budget):
    budget_raised = False
    try:
        canonical(r1, perm_budget=0)
    except IsoBudgetError:
        budget_raised = True
    if not budget_raised:
        failures.append("canonical(r1, perm_budget=0) should raise IsoBudgetError")

    # 5. Gap 4 (Unordered requirement pair (2, 0) changed to (0, 2) by sortPair under id):
    lr_unordered = LeanRegime(
        data=3,
        forms=(1,),
        insts=((0, (0,)),),
        rules=(),
        reqs=((2, 0),),
    )
    if lean_relabel(lr_unordered, id_f, (0,), (0,)).reqs != ((0, 2),):
        failures.append("lean_relabel under identity should sort unordered req (2, 0) to (0, 2)")
    if lean_iso_holds(lr_unordered, lr_unordered, id_f, (0,)):
        failures.append("isoRefl should fail when reqs has unordered pair (2, 0) not matching sortPair (0, 2)")

    # 6. Action (renameRegime leaves reqs untouched) vs. Iso (maps reqs via sortPair):
    #    Under f = (1, 0, 2), renameRegime keeps reqs = ((0, 2),), whereas sortPair(f(0), f(2)) = (1, 2).
    lr_action_img = LeanRegime(
        data=3,
        forms=(1, 2),
        insts=lean_relabel(lr1, (1, 0, 2), id_g, id_g).insts,
        rules=lr1.rules,
        reqs=lr1.reqs,  # renameRegime leaves reqs untouched!
    )
    if lean_iso_holds(lr1, lr_action_img, (1, 0, 2), id_g):
        failures.append("renameRegime should not be an Iso via f=(1,0,2) when f moves req (0, 2) to (1, 2)")

    # 7. Audit architecture census on disk and in artifacts/lean_axioms.txt
    lean_dir = REPO_ROOT / "lean4"
    derivation_files = sorted((lean_dir / "Derivation").glob("*.lean"))
    if len(derivation_files) != 75:
        failures.append(f"expected 75 .lean files in lean4/Derivation/, got {len(derivation_files)}")

    elaborated = [
        line.strip()
        for line in (REPO_ROOT / "artifacts" / "elaborated_modules.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(elaborated) != 75:
        failures.append(f"expected 75 modules in elaborated_modules.txt, got {len(elaborated)}")

    for compat_name in COMPAT_5:
        compat_text = (lean_dir / "Derivation" / f"{compat_name}.lean").read_text(encoding="utf-8")
        base_name = compat_name.removesuffix("Compat")
        if "import Derivation\n" not in compat_text or f"import Derivation.{base_name}" not in compat_text:
            failures.append(f"{compat_name}.lean missing expected two-import compatibility header")

    axiom_lines = [
        line.strip()
        for line in (REPO_ROOT / "artifacts" / "lean_axioms.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(axiom_lines) != 1530:
        failures.append(f"expected 1530 lines in artifacts/lean_axioms.txt, got {len(axiom_lines)}")

    root_lines = [line for line in axiom_lines if line.startswith("Derivation.lean:")]
    parked_lines = [line for line in axiom_lines if line.startswith("ParkedAudit.lean:")]
    if len(root_lines) != 1482 or len(parked_lines) != 48:
        failures.append(
            f"expected 1482 Derivation.lean + 48 ParkedAudit.lean lines, got {len(root_lines)} + {len(parked_lines)}"
        )

    counts = {k: 0 for k in EXPECTED_PARKED_COUNTS}
    for line in parked_lines:
        name = line[line.index("'") + 1 : line.rindex("'")]
        for mod_key, names_set in PARKED_THEOREM_GROUPS.items():
            if name in names_set:
                counts[mod_key] += 1
    if counts != EXPECTED_PARKED_COUNTS:
        failures.append(f"unexpected parked module counts: {counts} != {EXPECTED_PARKED_COUNTS}")

    result = {
        "unit": 74,
        "total_derivation_modules": len(derivation_files),
        "root_imported_modules": len(derivation_files) - len(PARKED_12),
        "parked_modules": len(PARKED_12),
        "root_axiom_reports": len(root_lines),
        "parked_axiom_reports": len(parked_lines),
        "parked_module_breakdown": counts,
        "failures": failures,
    }
    print(json.dumps(result, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
