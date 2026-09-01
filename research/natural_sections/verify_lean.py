"""Build this tree's Lean package and audit the axiom reports it prints.

The package under ``lean/`` compiles the sealed import closure of
``Derivation.PresentationNaturality`` as STAGED copies: this script reads
each pinned module's blob at the manifest's snapshot commit, checks its
SHA-256 against ``SOURCE_MANIFEST.json``, and writes those exact bytes to
``lean/sealed/Derivation/<Module>.lean`` (gitignored), which the
``Derivation`` library of ``lakefile.lean`` compiles inside ``lean/.lake/``.
There is no Lake dependency on ``lean4/``: a path dependency is built in
the dependency's own directory and would write ``lean4/.lake/``, outside
this tree's write root.  The build is thereby bound to the pinned
snapshot, not to whatever ``lean4/`` currently holds.

The write-root boundary is checked, not assumed: the repository-wide
``git status --porcelain --untracked-files=all --ignored=matching`` is
taken before staging and again after the build, and any record that is
new and not under ``research/natural_sections/`` fails the run by name.

It then applies the sealed tree's forbidden-token scan to every ``.lean``
file under ``lean/`` outside ``.lake`` and ``sealed``, parses every
``#print axioms`` line with a non-greedy name capture, requires the set
of reported declarations to equal ``AXIOM_REPORT_DECLARATIONS`` below,
and requires every report to lie within ``{propext, Quot.sound}``.

Nothing in ``.github/workflows`` runs this script.  A pass is a manual
receipt for the sources present when it ran.  AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import re
import subprocess
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import verify_pins


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
WRITE_ROOT = "research/natural_sections/"
LEAN_ROOT = HERE / "lean"
STAGED_ROOT = LEAN_ROOT / "sealed"
AXIOM_REPORT_MODULE = "NaturalSections.AxiomReport"
AXIOM_REPORT_SOURCE = "NaturalSections/AxiomReport.lean"

AXIOM_REPORT_DECLARATIONS: tuple[str, ...] = (
    "NaturalSections.natural_section_of_fixed_pair",
    "NaturalSections.natural_section_iff_fixed_pair",
    "NaturalSections.hnatural_section_iff_fixed_pair",
    "NaturalSections.fixed_pair_iff_two_fixed_points",
    "NaturalSections.cyc_cycInv",
    "NaturalSections.cycInv_cyc",
    "NaturalSections.cyc_fixes_e1",
    "NaturalSections.cyc_fixes_only_e1",
    "NaturalSections.cycIso_fixed_pair_free",
    "NaturalSections.fixed_point_without_natural_section",
    "NaturalSections.blindObs_no_admissible_pair",
    "NaturalSections.identity_fixes_everything_no_section",
    # Walks, forests, and the iff (sections 4-5).
    "NaturalSections.Step.inv_transport",
    "NaturalSections.Step.transport_inv",
    "NaturalSections.Walk.transport_append",
    "NaturalSections.Walk.reverse_transport_transport",
    "NaturalSections.Walk.transport_reverse_transport",
    "NaturalSections.Step.transport_of_natural",
    "NaturalSections.Walk.transport_of_natural",
    "NaturalSections.Forest.gen_transport",
    "NaturalSections.natural_section_iff_generators",
    "NaturalSections.walk_maps_of_closed_fixed",
    "NaturalSections.natural_section_iff_holonomy",
    "NaturalSections.one_object_recovered",
    # Hop fixture (NaturalSections/HopFixture.lean): chain, square, star.
    "NaturalSections.Hop.chain_no_hop_flips",
    "NaturalSections.Hop.chain_natural_section",
    "NaturalSections.Hop.chain_has_natural_section",
    "NaturalSections.Hop.sqWalk_transport",
    "NaturalSections.Hop.square_no_natural_section",
    "NaturalSections.Hop.stWalk_transport",
    "NaturalSections.Hop.star_no_natural_section",
    "NaturalSections.Hop.chain_square_star_separation",
    # Three-label fixture (NaturalSections/HopFixture3.lean).
    "NaturalSections.Hop3.raw_lt",
    "NaturalSections.Hop3.hop_inv",
    "NaturalSections.Hop3.pair_ext",
    "NaturalSections.Hop3.c3_no_fixed",
    "NaturalSections.Hop3.c3_is_even",
    "NaturalSections.Hop3.c3_order_three",
    "NaturalSections.Hop3.sq3_comp",
    "NaturalSections.Hop3.sq3_transport_val",
    "NaturalSections.Hop3.sq3_no_fixed_pair",
    "NaturalSections.Hop3.square3_no_natural_section",
    "NaturalSections.Hop3.parity_and_fixed_pair_come_apart",
    "NaturalSections.Hop3.star3_generators",
    "NaturalSections.Hop3.star3_has_natural_section",
    "NaturalSections.Hop3.chain3_natural_section",
    "NaturalSections.Hop3.chain3_has_natural_section",
    "NaturalSections.Hop3.chain3_star3_square3_separation",
    # Four-label fixture (NaturalSections/HopFixture4.lean).
    "NaturalSections.Hop4.swap01_invol",
    "NaturalSections.Hop4.pair_ext",
    "NaturalSections.Hop4.walk_transport_val",
    "NaturalSections.Hop4.walk_moves_pair01",
    "NaturalSections.Hop4.constant23_natural",
    "NaturalSections.Hop4.section_exists",
    "NaturalSections.Hop4.nontrivial_holonomy_with_natural_section",
    # Phase fibre over an arbitrary abelian group (NaturalSections/HopFixturePhase.lean).
    "NaturalSections.HopPhase.AbGroup.neg_zero",
    "NaturalSections.HopPhase.AbGroup.neg_neg",
    "NaturalSections.HopPhase.AbGroup.cancel",
    "NaturalSections.HopPhase.tag_antisymm",
    "NaturalSections.HopPhase.stag_antisymm",
    "NaturalSections.HopPhase.interp_flip",
    "NaturalSections.HopPhase.tr_inv",
    "NaturalSections.HopPhase.walk_transport_val",
    "NaturalSections.HopPhase.comp_label0",
    "NaturalSections.HopPhase.comp_label1",
    "NaturalSections.HopPhase.two_labels",
    "NaturalSections.HopPhase.flux_zero_of_fixed",
    "NaturalSections.HopPhase.no_natural_section_of_flux",
    "NaturalSections.HopPhase.interp_zero_flux",
    "NaturalSections.HopPhase.constant_natural_of_zero_flux",
    "NaturalSections.HopPhase.section_iff_flux_zero",
    "NaturalSections.HopPhase.section_iff_flux_zero_fin4",
    # The weighted layer (NaturalSections/WeightedLayer.lean).
    "NaturalSections.sumList_map_congr",
    "NaturalSections.twisted_of_natural",
    "NaturalSections.unit_weight",
    "NaturalSections.total_unit",
    "NaturalSections.count_le_length",
    "NaturalSections.count_eq_length_iff",
    "NaturalSections.count_lt_of_mover",
    "NaturalSections.Sq.weights_ws3",
    "NaturalSections.Sq.sum_blind_to_obstruction",
    "NaturalSections.Sq.every_value_square",
    "NaturalSections.Ch.every_value_chain",
    "NaturalSections.value_silent_about_class",
    # A2 repaired: conjugation-closed weightings and holonomy orbits.
    "NaturalSections.Walk.conj_transport",
    "NaturalSections.Walk.conj_fixes_iff",
    "NaturalSections.unit_conj_closed",
    "NaturalSections.ite_congr_pair",
    "NaturalSections.twisted_conj_equivariant",
    "NaturalSections.sumList_perm",
    "NaturalSections.twisted_const_of_conj_closed",
    "NaturalSections.Sq.sqWalk_moves_boolEqPair",
    "NaturalSections.Sq.ws2_closure_witness",
    "NaturalSections.Sq.twisted_const_on_square_orbit",
    "NaturalSections.Sq.square_orbit_values",
    "NaturalSections.Sq.signW_not_conj_closed",
    # Pointwise re-presentation (NaturalSections/Represent.lean).
    "NaturalSections.Repres.iso_mapPair",
    "NaturalSections.Repres.push_natural",
    "NaturalSections.Repres.pull_natural",
    "NaturalSections.natural_section_iff_repres",
    "NaturalSections.obstruction_survives_repres",
    "NaturalSections.square_obstruction_survives",
    "NaturalSections.chain_section_survives",
    # The cut theorem and the blindness of counts (NaturalSections/CutAndCounts.lean).
    "NaturalSections.cut_no_hop_flips",
    "NaturalSections.cut_removes_exactly_the_flips",
    "NaturalSections.cut_natural_section",
    "NaturalSections.cut_theorem",
    "NaturalSections.cover_natural_section",
    "NaturalSections.unWalk_reWalk",
    "NaturalSections.reWalk_unWalk",
    "NaturalSections.reWalk_length",
    "NaturalSections.dynamics_blind_to_class",
    # Refinement (NaturalSections/Refinement.lean).
    "NaturalSections.Subdiv.push_natural",
    "NaturalSections.Subdiv.pull_natural",
    "NaturalSections.natural_section_iff_subdiv",
    "NaturalSections.class_refinement_invariant",
    "NaturalSections.square_subdiv_obstructed",
    "NaturalSections.chain_subdiv_section",
    "NaturalSections.Repl.push_natural",
    "NaturalSections.Repl.h0_equation",
    "NaturalSections.Repl.pull_natural",
    "NaturalSections.natural_section_iff_repl",
    "NaturalSections.square_repl_obstructed",
    "NaturalSections.chain_repl_section",
    "NaturalSections.ReplE.push_natural",
    "NaturalSections.ReplE.h0_equation",
    "NaturalSections.ReplE.h0r_equation",
    "NaturalSections.ReplE.pull_natural",
    "NaturalSections.natural_section_iff_replE",
    "NaturalSections.square_replE_obstructed",
    "NaturalSections.chain_replE_section",
    "NaturalSections.replE_square_inhabited",
    "NaturalSections.replE_chain_inhabited",
    "NaturalSections.replE_square_flip_inhabited",
    # Budget closure (NaturalSections/Budgets.lean).
    "NaturalSections.Budgets.linear_polyBounded",
    "NaturalSections.Budgets.polyBounded_mul",
    "NaturalSections.Budgets.polyBounded_comp",
    "NaturalSections.Budgets.gen_linear_polyBounded",
    "NaturalSections.Budgets.gen_congr",
    "NaturalSections.Budgets.pow_in_gen_linear",
    "NaturalSections.Budgets.sq_le_two_pow",
    "NaturalSections.Budgets.self_lt_two_pow",
    "NaturalSections.Budgets.two_pow_escapes",
    "NaturalSections.Budgets.two_pow_not_polyBounded",
    "NaturalSections.Budgets.generators_decide_the_class",
    "NaturalSections.Budgets.dominated_polyBounded",
    "NaturalSections.Budgets.polyBounded_dominated",
    "NaturalSections.Budgets.polyBounded_iff_dominated",
    "NaturalSections.Budgets.linear_mono",
    "NaturalSections.Budgets.gen_linear_mono",
    "NaturalSections.Budgets.parity_polyBounded",
    "NaturalSections.Budgets.parity_not_gen_linear",
    "NaturalSections.Budgets.polyBounded_without_gen_linear",
    # Faces: the chord square (NaturalSections/TwoComplex.lean).
    "NaturalSections.TwoCell.tag_antisymm",
    "NaturalSections.TwoCell.stag_antisymm",
    "NaturalSections.TwoCell.interp_flip",
    "NaturalSections.TwoCell.tr_inv",
    "NaturalSections.TwoCell.outer_flux_eq_add",
    "NaturalSections.TwoCell.wT1_transport_val",
    "NaturalSections.TwoCell.wT2_transport_val",
    "NaturalSections.TwoCell.compT1_label0",
    "NaturalSections.TwoCell.compT1_label1",
    "NaturalSections.TwoCell.compT2_label0",
    "NaturalSections.TwoCell.fluxT1_zero_of_fixed",
    "NaturalSections.TwoCell.fluxT2_zero_of_fixed",
    "NaturalSections.TwoCell.section_fluxes_zero",
    "NaturalSections.TwoCell.eq_of_add_neg_eq_zero",
    "NaturalSections.TwoCell.eq_neg_of_add_eq_zero",
    "NaturalSections.TwoCell.add_neg_cancel_right",
    "NaturalSections.TwoCell.pair_step",
    "NaturalSections.TwoCell.potential_natural",
    "NaturalSections.TwoCell.section_iff_faces_zero",
    "NaturalSections.TwoCell.fill_transfers",
    "NaturalSections.TwoCell.ctr_fluxT1",
    "NaturalSections.TwoCell.ctr_fluxOuter",
    "NaturalSections.TwoCell.outer_zero_but_obstructed",
    "NaturalSections.TwoCell.section_iff_faces_zero_fin4",
    # Repair mass (NaturalSections/QuotientMass.lean).
    "NaturalSections.QMass.neg_of_add_eq_zero",
    "NaturalSections.QMass.neg_add_rev",
    "NaturalSections.QMass.fluxT1_d0",
    "NaturalSections.QMass.fluxT2_d0",
    "NaturalSections.QMass.exact_of_fluxes_zero",
    "NaturalSections.QMass.ind_eq_zero_iff",
    "NaturalSections.QMass.ind_le_one",
    "NaturalSections.QMass.ind_eq_one_of_ne",
    "NaturalSections.QMass.zero_mass_iff",
    "NaturalSections.QMass.suppMass_congr",
    "NaturalSections.QMass.repair_mass_zero_iff_faces_zero",
    "NaturalSections.QMass.repair_mass_zero_iff_section",
    "NaturalSections.QMass.add_add_add",
    "NaturalSections.QMass.neg_add'",
    "NaturalSections.QMass.fluxT1_add",
    "NaturalSections.QMass.fluxT2_add",
    "NaturalSections.QMass.fluxT1_neg",
    "NaturalSections.QMass.fluxT2_neg",
    "NaturalSections.QMass.residual_flux1",
    "NaturalSections.QMass.residual_flux2",
    "NaturalSections.QMass.reaches_of_sameClass",
    "NaturalSections.QMass.single_mass_le_one",
    "NaturalSections.QMass.single_e01_flux1",
    "NaturalSections.QMass.single_e01_flux2",
    "NaturalSections.QMass.single_e32_flux1",
    "NaturalSections.QMass.single_e32_flux2",
    "NaturalSections.QMass.single_e03_flux1",
    "NaturalSections.QMass.single_e03_flux2",
    "NaturalSections.QMass.mass_le_one_axes",
    "NaturalSections.QMass.repair_mass_le_one_iff",
    "NaturalSections.QMass.pairRep_flux1",
    "NaturalSections.QMass.pairRep_flux2",
    "NaturalSections.QMass.pairRep_mass_le_two",
    "NaturalSections.QMass.repair_mass_le_two",
    "NaturalSections.QMass.repair_mass_zero_iff_section_fin4",
    # Aggregation (NaturalSections/Aggregation.lean).
    "NaturalSections.Aggregate.nil_zero",
    "NaturalSections.Aggregate.forced_sum",
    "NaturalSections.Aggregate.forced_weighted_sum",
    "NaturalSections.Aggregate.max_calibrated",
    "NaturalSections.Aggregate.max_not_additive",
    "NaturalSections.Aggregate.max_disagrees_with_sum",
    "NaturalSections.Aggregate.scaled_additive",
    "NaturalSections.Aggregate.scaled_not_calibrated",
    "NaturalSections.Aggregate.suppMass_is_edge_sum",
    "NaturalSections.Aggregate.aggregation_determines_suppMass",
    # The equivariant bridge to the sealed selector theorem
    # (NaturalSections/EquivariantBridge.lean).
    "NaturalSections.EqBridge.pairRetract_table",
    "NaturalSections.EqBridge.pairRetract_fixes_admissible",
    "NaturalSections.EqBridge.pairRetract_equivariant",
    "NaturalSections.EqBridge.sectionOf_natural",
    "NaturalSections.EqBridge.no_equivariant_pair_valued_map_via_sections",
    "NaturalSections.EqBridge.equivariant_iff_sealed_shape",
    "NaturalSections.EqBridge.sealed_selector_content_along_bridge",
    "NaturalSections.EqBridge.bridge_statement_is_the_sealed_statement",
    "NaturalSections.SlotEx.mod_idem",
    "NaturalSections.SlotEx.repAdd_val",
    "NaturalSections.SlotEx.repAdd_rot_zero",
    "NaturalSections.SlotEx.swap_count_one",
    "NaturalSections.SlotEx.swap_count_two",
    "NaturalSections.SlotEx.swap_count_three",
    "NaturalSections.SlotEx.swap_count_four",
    "NaturalSections.SlotEx.swap_count_five",
    "NaturalSections.SlotEx.swap_count_six",
    "NaturalSections.SlotEx.swap_count_seven",
    "NaturalSections.SlotEx.swap_count_eight",
    "NaturalSections.SlotEx.transposeW_transposeW",
    "NaturalSections.SlotEx.oddW_diag_zero",
    "NaturalSections.SlotEx.odd_total_zero",
    "NaturalSections.SlotEx.sym_odd_zero",
    "NaturalSections.SlotEx.irrefl_support_diag_zero",
    "NaturalSections.SlotEx.d2Fam_odd",
    "NaturalSections.SlotEx.d2Fam_supported",
    "NaturalSections.SlotEx.d2Fam_total_zero",
    "NaturalSections.SlotEx.sumList_pair_cancel",
    "NaturalSections.SlotEx.sumList_nonneg",
    "NaturalSections.SlotEx.sum_pairs_residual",
    "NaturalSections.SlotEx.sum_pairs_residual_nonneg",
    "NaturalSections.SlotEx.discard_is_not_cancel",
    "NaturalSections.SlotEx.flip_fixed_zero",
    "NaturalSections.SlotEx.mixed_residual_negative",
    "NaturalSections.Receiver.R_refl",
    "NaturalSections.Receiver.R_symm",
    "NaturalSections.Receiver.int_left_cancel",
    "NaturalSections.Receiver.den_int_ne_zero",
    "NaturalSections.Receiver.R_trans",
    "NaturalSections.Receiver.den_rawAdd",
    "NaturalSections.Receiver.rawAdd_left_congr",
    "NaturalSections.Receiver.rawAdd_right_congr",
    "NaturalSections.Receiver.rawNeg_congr",
    "NaturalSections.Receiver.add_comm",
    "NaturalSections.Receiver.add_assoc",
    "NaturalSections.Receiver.add_zero",
    "NaturalSections.Receiver.add_neg",
    "NaturalSections.Receiver.layer_mul_compat",
    "NaturalSections.Receiver.layer_add",
    "NaturalSections.Receiver.receiver_is_union",
    "NaturalSections.Receiver.half_add_half",
    "NaturalSections.Receiver.half_ne_zero",
    "NaturalSections.Balance.natCast_dvd_down",
    "NaturalSections.Balance.lt_of_mul_left",
    "NaturalSections.Balance.layer_inj",
    "NaturalSections.Balance.fresh_not_below",
    "NaturalSections.Balance.reduce_below",
    "NaturalSections.Balance.fresh_descend",
    "NaturalSections.Balance.fresh_rep_exists",
    "NaturalSections.Balance.fresh_rep_unique",
    "NaturalSections.Balance.mem_divisorsBelow",
    "NaturalSections.Balance.map_congr_mem",
    "NaturalSections.Balance.balanceFuel_stable",
    "NaturalSections.Balance.balance_eq_fuel",
    "NaturalSections.Balance.balance_one",
    "NaturalSections.Balance.sumI_append_single",
    "NaturalSections.Balance.balance_divisor_sum",
    "NaturalSections.Balance.balance_values",
    "NaturalSections.Balance.freshCount_values",
    "NaturalSections.Balance.partition_instances",
    "NaturalSections.Balance.inversion_instances",
    "NaturalSections.Balance.runningBalance_checkpoints",
)

ALLOWED_AXIOMS = frozenset({"propext", "Quot.sound"})
FORBIDDEN_TOKENS = (
    r"\bsorry\b",
    r"\badmit\b",
    r"^\s*axiom\s",
    r"\bunsafe\b",
    r"\bpartial\b",
)

_REPORT_LINE = re.compile(
    r"^'(.+?)' (?:depends on axioms: \[(.*?)\]|does not depend on any axioms)\s*$",
    re.MULTILINE,
)
_PRINT_AXIOMS = re.compile(r"^#print axioms ([A-Za-z_][A-Za-z0-9_.']*)\s*$", re.MULTILINE)


def _run_lake(arguments: Sequence[str]) -> str:
    process = subprocess.run(
        ["lake", *arguments],
        cwd=LEAN_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
    )
    output = process.stdout or ""
    if process.returncode:
        raise RuntimeError(
            f"lake {' '.join(arguments)} failed with exit {process.returncode}:\n{output}"
        )
    return output


def parse_axiom_report(output: str) -> dict[str, frozenset[str]]:
    reports: dict[str, frozenset[str]] = {}
    for match in _REPORT_LINE.finditer(output):
        name = match.group(1)
        raw = match.group(2) or ""
        axioms = frozenset(axiom.strip() for axiom in raw.split(",") if axiom.strip())
        if name in reports:
            raise ValueError(f"duplicate axiom report: {name}")
        reports[name] = axioms
    return reports


def check_axiom_reports(
    reports: Mapping[str, frozenset[str]],
    expected: Sequence[str] = AXIOM_REPORT_DECLARATIONS,
    allowed: frozenset[str] = ALLOWED_AXIOMS,
) -> list[str]:
    missing = sorted(set(expected) - set(reports))
    unexpected = sorted(set(reports) - set(expected))
    if missing or unexpected:
        raise ValueError(
            f"axiom report inventory differs: missing {missing}, unexpected {unexpected}"
        )
    lines: list[str] = []
    for name in expected:
        extra = sorted(reports[name] - allowed)
        if extra:
            raise ValueError(f"{name} depends on disallowed axioms: {extra}")
        lines.append(f"{name}: {sorted(reports[name]) or 'no axioms'}")
    return lines


def declared_report_inventory(source: str) -> tuple[str, ...]:
    return tuple(_PRINT_AXIOMS.findall(source))


def research_lean_sources() -> list[Path]:
    """This tree's own Lean sources: not the build cache, not the staged copies."""

    return sorted(
        path
        for path in LEAN_ROOT.rglob("*.lean")
        if ".lake" not in path.parts and "sealed" not in path.parts
    )


def scan_forbidden_tokens(paths: Iterable[Path]) -> list[str]:
    failures: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_TOKENS:
            for match in re.finditer(pattern, text, flags=re.MULTILINE):
                failures.append(f"{path.name}: forbidden token {match.group(0).strip()!r}")
    return failures


def stage_sealed_sources(manifest: Mapping[str, object] | None = None) -> list[str]:
    """Write the pinned snapshot blob of every manifest module under ``lean/sealed``."""

    if manifest is None:
        manifest = verify_pins.read_manifest()
    block = manifest.get("source_snapshot")
    if not isinstance(block, dict):
        raise ValueError("manifest must carry a 'source_snapshot' object")
    snapshot = block.get("commit")
    if not isinstance(snapshot, str) or not re.fullmatch(r"[0-9a-f]{40}", snapshot):
        raise ValueError("manifest snapshot commit must be an exact 40-digit lowercase hex id")
    modules = manifest.get("modules")
    if not isinstance(modules, list) or not modules:
        raise ValueError("manifest must list modules")
    lines: list[str] = []
    for item in modules:
        if not isinstance(item, dict):
            raise ValueError("each module entry must be an object")
        module = item.get("module")
        wanted = item.get("sha256")
        if not isinstance(module, str) or not isinstance(wanted, str):
            raise ValueError("each module entry needs 'module' and 'sha256'")
        repo_path = verify_pins.module_path(module)
        blob = verify_pins._git_bytes("show", f"{snapshot}:{repo_path}")
        actual = verify_pins._sha256(blob)
        if actual != wanted:
            raise ValueError(
                f"staged module {module} at {snapshot} hashes to {actual}, manifest pins {wanted}"
            )
        target = (STAGED_ROOT / module.replace(".", "/")).with_suffix(".lean").resolve()
        if not target.is_relative_to(LEAN_ROOT.resolve()):
            raise ValueError(f"staged path escapes the tree: {module}")
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.read_bytes() != blob:
            target.write_bytes(blob)
        lines.append(f"staged: {module} at {snapshot[:12]} {actual}")
    return lines


def repository_records() -> frozenset[str]:
    output = verify_pins._git_bytes(
        "status", "--porcelain=v1", "--untracked-files=all", "--ignored=matching"
    ).decode("utf-8")
    return frozenset(line for line in output.splitlines() if line.strip())


def writes_outside_root(
    before: Iterable[str], after: Iterable[str], root: str = WRITE_ROOT
) -> list[str]:
    """Records new in ``after`` whose path is not under ``root``; pure."""

    violations: list[str] = []
    for line in sorted(set(after) - set(before)):
        if len(line) < 4 or line[2] != " ":
            raise ValueError(f"malformed git status record: {line!r}")
        paths = [part.strip().strip('"') for part in line[3:].split(" -> ")]
        if any(not path.startswith(root) for path in paths):
            violations.append(line)
    return violations


def verify_axiom_report() -> list[str]:
    inventory = declared_report_inventory(
        (LEAN_ROOT / AXIOM_REPORT_SOURCE).read_text(encoding="utf-8")
    )
    if inventory != AXIOM_REPORT_DECLARATIONS:
        raise ValueError(
            f"{AXIOM_REPORT_SOURCE} names {list(inventory)}, "
            f"but this script expects {list(AXIOM_REPORT_DECLARATIONS)}"
        )
    sources = research_lean_sources()
    if not sources:
        raise ValueError(f"no Lean sources found under {LEAN_ROOT}")
    failures = scan_forbidden_tokens(sources)
    if failures:
        raise ValueError("forbidden tokens in research Lean sources:\n" + "\n".join(failures))
    before = repository_records()
    staged = stage_sealed_sources()
    _run_lake(("build",))
    output = _run_lake(("env", "lean", AXIOM_REPORT_SOURCE))
    escaped = writes_outside_root(before, repository_records())
    if escaped:
        raise ValueError(
            f"the Lean build wrote outside the write root {WRITE_ROOT}:\n  "
            + "\n  ".join(escaped)
        )
    report_lines = check_axiom_reports(parse_axiom_report(output))
    return [
        f"Lean sources scanned for forbidden tokens: {len(sources)}",
        *staged,
        "Lean package built: lake build (exit 0)",
        f"write root respected: no new file outside {WRITE_ROOT}",
        f"Lean axiom-report target: {AXIOM_REPORT_MODULE}",
        f"Lean #print axioms declarations: {len(report_lines)} within {sorted(ALLOWED_AXIOMS)}",
        *report_lines,
        "manual receipt: nothing in .github/workflows runs this script",
    ]


def main() -> int:
    try:
        print("\n".join(verify_axiom_report()))
    except (OSError, RuntimeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
