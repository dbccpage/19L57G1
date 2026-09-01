"""Produce the PR #12 completion receipt deterministically.

Usage: python code/run_primitive_receipt.py [--artifacts DIR]

Writes ``primitive_completion_receipt.json``: the binding record of
the contact-and-passage run — base commit, contact status, prompt
hashes, toolchain and dependency pins, the axiom-report hash, all
declared finite bounds, every terminal claim with its evidence, all
open obligations (including the four OPEN cells the collision
declared, each with its price), the frontier conjectures, and the
adversarial record (twenty-one attacks, each with its
disposition)."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Optional

from derivation.export import Json, write_json
from run_primitive_contact import (
    SCOPE_EQUIVALENT,
    SCOPE_INCOMPARABLE,
    SCOPE_KERNEL,
    VERDICT_PRIMARY,
)

REPO = Path(__file__).resolve().parent.parent


def canonical_sha256(path: Path) -> str:
    """Hash an explicitly CRLF-to-LF-normalized text rendering.

    For every currently declared tracked input the result is tested
    against the corresponding Git blob hash.  That equality is a
    verified property of those inputs and repository attributes, not
    the definition of this function for arbitrary byte strings.
    ``test_mutation_detected`` separately checks content sensitivity.
    """
    crlf = b"\r\n"
    lf = b"\n"
    return hashlib.sha256(
        path.read_bytes().replace(crlf, lf)).hexdigest()


def receipt() -> dict[str, Json]:
    lean_axioms = REPO / "artifacts" / "lean_axioms.txt"
    reports = [ln for ln in
               lean_axioms.read_text(encoding="utf-8").splitlines()
               if "axioms" in ln]
    manifest = (REPO / "contact" / "omega_primdiff"
                / "CONTACT_MANIFEST.json")
    manifest_hash: Json = None
    if manifest.exists():
        manifest_hash = hashlib.sha256(
            manifest.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    return {
        "run": "PR #12 — Primitive Difference contact and passage",
        "blind_native_base": "ccd3a53",
        "contact": {
            "package_present": (REPO / "contact").exists(),
            "manifest_hash": manifest_hash,
            "status": "CONTACT_PROCESSED_LEAN_ONLY",
            "status_history": [
                "CONTACT_INPUT_ABSENT (pre-contact, "
                "blind-native-base ccd3a53)",
                "CONTACT_PROCESSED_LEAN_ONLY (2026-08-13, "
                "base a5caee2)",
            ],
        },
        "prompt_sha256_canonical": {
            "prompt/prompt.md":
                canonical_sha256(REPO / "prompt/prompt.md"),
            "prompt/seed_prompt.md":
                canonical_sha256(REPO / "prompt/seed_prompt.md"),
        },
        "retired_prompt_sha256_canonical": {
            "prompt/prompt_pr12.md":
                "fc1625a46ca19be4d479b8e407f82cc0"
                "d8ba26beb8647437f6895486e67d7403",
            "prompt/ultra_prompt_pr12.md":
                "f73e6c8e7e7d6a826340df0043a56778"
                "9cf52ec14a89247d430d0f096302fa7a",
        },
        "seed_prompt_original_supplied_sha256":
            "ee3ba0583fea2a11f129"
            "4538c912c542b3faee5316355dc226efb92ef64646ab",
        "seed_prompt_provenance":
            "the original supplied working-tree rendering (CRLF) was "
            "hashed at recording time; the repository-canonical blob "
            "is its one-time LF staging normalization, accepted "
            "alongside it by ci/check_prompt_hashes.py since PR #1",
        "toolchain": {
            "lean": (REPO / "lean4/lean-toolchain")
                .read_text(encoding="utf-8").strip(),
            "python_requirements_sha256_canonical":
                canonical_sha256(REPO / "requirements.txt"),
        },
        "axiom_report": {
            "sha256_canonical": canonical_sha256(lean_axioms),
            "theorem_count": len(reports),
            "axioms_within": ["propext", "Quot.sound"],
        },
        "bounds": {
            "growth_rounds": 15,
            "matrix_universe": "carriers 1..3, declared ret/prot/ops "
                               "decorations (see "
                               "primitive_implication_matrix.json)",
            "apartness_exhaustive_carrier": 3,
            "preservation_census_carrier": 4,
            "cut_census_carriers": [2, 3, 4, 5],
            "cell_demonstration_carrier": 4,
            "controller_class": 1024,
            "controller_behavior_basis":
                "6 states x 10 events (recorded in artifact)",
            "interpreter_family": 64,
            "interpreter_basis": "six probe worlds/events",
            "attachment_rounds": 15,
            "attachment_shape_carrier": 4,
            "attachment_orbit_carrier": 3,
            "ladder_general_dims_decided": [2, 3, 4, 5],
            "renaming_symmetric_group": 6,
            "renaming_assoc_triples": 216,
            "genesis_sample_states": 8,
            "genesis_battery_checks": 600,
            "genesis_internal_traces": 11104,
            "boundary_cells_checked": 218,
            "boundary_coefficient_checks": 3124,
            "boundary_dims": [2, 3, 4, 5, 6],
            "weight_carrier": 2,
            "weight_max": 3,
            "weight_coeff_bound": 3,
            "contact_carrier_max": 3,
            "contact_relation_counts": [2, 16, 512],
            "collision_cells": 37,
            "supplied_declarations": 103,
            "denylist_entries_full_census": 111,
            "denylist_entries_working": 102,
            "denylist_definitions":
                "full census = every supplied top-level identifier "
                "plus field names (111); working subtraction file = "
                "census minus 9 identifiers verified native-at-base "
                "or Lean-core (102)",
        },
        "terminals": [
            {"code": "NATIVE_PRIMITIVE_DIFFERENCE_CHARACTERIZED",
             "scope": "within the declared nine-candidate signature, "
                      "A (witnessed irreflexive relation) is the "
                      "weakest studied positive-witness candidate "
                      "forcing endpoint inequality (imp_a_d vs "
                      "nimp_w_d); d2_initial is initiality of the "
                      "free pointed witnessed relation (candidate W) "
                      "and restricts to the irreflexive subcategory "
                      "- initiality does not itself select "
                      "irreflexivity",
             "evidence": ["PrimitiveCore.matrixCells (72 cells: 17 "
                          "implications, 51 finite countermodels "
                          "with minimum carrier proved where cited, "
                          "4 OPEN located cells)",
                          "PrimitiveCats.d2_initial (W-initiality)",
                          "PrimitiveCore.imp_a_d / nimp_w_d",
                          "primitive_implication_matrix.json"]},
            {"code": "NATIVE_PRIMITIVE_DIFFERENCE_BRANCHES",
             "evidence": ["PrimitiveCats.s2_initial_sym",
                          "PrimitiveCats.s2_not_weakly_initial",
                          "PrimitiveCats.no_terminal_pres",
                          "orientation fork and observer cut both "
                          "retained"]},
            {"code": "CONTACT_INPUT_ABSENT",
             "scope": "SEALED HISTORY: the pre-contact terminal of "
                      "the blind-native stage (ccd3a53), preserved as "
                      "history[0]; superseded by "
                      "CONTACT_PROCESSED_LEAN_ONLY at base a5caee2",
             "evidence": ["primitive_contact.json (history)",
                          "PrimitiveContact.contactStatus (sealed)",
                          "PrimitiveContact.contactStatusHistory"]},
            {"code": VERDICT_PRIMARY,
             "scope": SCOPE_INCOMPARABLE,
             "evidence": ["ContactBridge.d2_not_obs_complement",
                          "ContactBridge.obsApart_repr_iff",
                          "ContactBridge.unit_total_not_repr",
                          "ContactBridge.triSym_not_obs_complement",
                          "ContactBridge.d_not_witnessed_repr",
                          "ContactKernel.kernel_from_obs_iff_pair",
                          "ContactKernel.kernel_not_unique_of_pair",
                          "ContactKernel."
                          "kernel_no_witness_from_collapse",
                          "ContactKernel.kernel_not_c",
                          "ContactKernel.kernel_not_f",
                          "ObsDescent (reconstruction corpus)",
                          "primitive_contact.json (verdict, "
                          "collision_cells, enumerations)"]},
            {"code": "COMMON_PRIMITIVE_KERNEL_REPLACES_BOTH",
             "scope": SCOPE_KERNEL,
             "evidence": ["ContactKernel.WitnessedDiff",
                          "ContactKernel.ofSetting",
                          "ContactKernel.ofSetting_exact",
                          "ContactKernel.ofDiffObs",
                          "ContactKernel.toDiffObs (with "
                          "toDiffObs_fields, toDiffObs_apart: the "
                          "observer-side record identity)",
                          "ContactKernel.toNativeKernel",
                          "ContactKernel.kernel_gateway_unique",
                          "ContactKernel."
                          "kernel_no_terminal_collector",
                          "ContactKernel.vhom_unique_of_onto",
                          "ContactKernel.kernel_licenses_entry",
                          "ContactKernel.entry_pre_observation"]},
            {"code": "CONTACT_EQUIVALENT_UNDER_DECIDABLE_ZERO_PLUS_"
                     "APARTNESS_ADMISSIONS",
             "scope": SCOPE_EQUIVALENT,
             "evidence": ["ContactBridge.isApart_repr",
                          "ContactBridge.obsApart_isApart",
                          "ContactBridge.apartObs_roundtrip",
                          "ContactBridge.indist_obsApart_iff",
                          "ContactBridge.cotrans_schema_iff_wlem",
                          "ContactBridge.stability_schema_iff_dne",
                          "ContactBridge."
                          "located_schema_implies_wlem"]},
            {"code": "PRIMITIVE_DIFFERENCE_PASSAGE_COMPOSED",
             "scope": "candidate A transports into the passage as a "
                      "theorem: the asserted store induces a Setting "
                      "satisfying A (assert_transport, "
                      "kernel_enters_preretained) BEFORE retention, "
                      "and retention/protection/observation are "
                      "separate admissions; thirteen arrows, each "
                      "THEOREM or DECLARATION-with-countermodel",
             "evidence": ["PrimitivePassage.assert_transport",
                          "PrimitivePassage.kernel_enters_preretained",
                          "PrimitivePassage.assertion_not_retained",
                          "PrimitivePassage.retention_requires_assertion",
                          "primitive_passage.json"]},
            {"code": "TWO_RULE_SCHEMA_PROVED_UNDER_"
                     "DECLARED_RESPONSE_UNIVERSE_AND_WF_PROTECTED_"
                     "PAIR",
             "scope": "grammar-relative: the declared "
                      "singleton-column extension universe contains "
                      "a separator for every well-formed pair; the "
                      "obstruction identifies a separator already "
                      "available in that declared universe - it does "
                      "not manufacture the constructor; setBudget 1 "
                      "in emitted blocks is a declared self-funding "
                      "policy",
             "evidence": ["PrimitivePassage.two_rule",
                          "PrimitivePassage."
                          "extension_always_available"]},
            {"code": "NONUNIQUE_CONTROLLER_FAMILY",
             "evidence": ["ControllerCategory.live_census",
                          "ControllerCategory.nonrefuse_agree",
                          "ControllerCategory.refuse_distinguishes"]},
            {"code": "INITIALITY_REFUTED_BY_CONSTANT_SIMULATIONS_"
                     "COUNTERMODEL",
             "evidence": ["ControllerCategory.no_initial_ctrl",
                          "ControllerCategory.no_initial_live_ctrl",
                          "ControllerCategory."
                          "strict_agree_on_reachable (orbit-relative "
                          "salvage)"]},
            {"code": "FINITE_CODE_FAMILY_NOT_EXTENSIONALLY_"
                     "COMPLETE",
             "scope": "a finite code list under any evaluation map "
                      "does not enumerate the function type (the "
                      "diagonal differs only at the operationally "
                      "inert notes field); NOT a self-interpretation "
                      "impossibility, NOT 'the evaluator cannot be "
                      "coded', NOT a semantic tower theorem",
             "evidence": ["InterpreterBoundary.tower_persists",
                          "primitive_interpreter.json "
                          "(diagonal_misses_all)"]},
            {"code": "DECLARED_BOUNDARY_MODEL_SATISFIES_A_AND_F",
             "scope": "a DECLARED model of the description/"
                      "interpreter boundary satisfies candidates A "
                      "and F; the relation, retention, and "
                      "protection are inserted by definition, and "
                      "no theorem links the uncoded occurrence to "
                      "the diagonal's missed function",
             "evidence": ["InterpreterBoundary.i5_boundary_is_A",
                          "InterpreterBoundary.i5_boundary_is_F",
                          "InterpreterBoundary."
                          "i5_collapse_obstructed"]},
            {"code": "HIGHER_STRUCTURE_OPTIONAL_NOT_FORCED",
             "evidence": ["HigherStructure.filling_not_forced",
                          "HigherStructure.boundary_not_forced",
                          "HigherStructure.ladder_dim2/dim3"]},
        ],
        "open_obligations": [
            "four OPEN located matrix cells (a->bl, bs->bl, bc->bl, "
            "f->bl): no internal countermodel can exist "
            "(located_of_decidable); independence is metatheoretic",
            "COLLISION OPEN CELL (bridge, cotransitivity; "
            "ContactBridge.open_bridge_cotrans): the cotransitivity "
            "schema for observer complements, quantified over all "
            "observers, is exactly the weak law of excluded middle "
            "(cotrans_schema_iff_wlem) - PRICE: WLEM; pointwise "
            "decidability of the zero relation discharges it "
            "(obsApart_cotrans); no internal countermodel can exist "
            "because the schema is classically true",
            "COLLISION OPEN CELL (bridge, locatedness; "
            "ContactBridge.open_bridge_located): the locatedness "
            "schema implies the weak law of excluded middle "
            "(located_schema_implies_wlem) - PRICE: a WLEM-"
            "implication, forward direction only; the converse is "
            "OPEN and would need a function-comprehension principle "
            "beyond WLEM; pointwise decidability discharges the "
            "schema (obsSetting_bl)",
            "COLLISION OPEN CELL (kernel, read-back grade; "
            "ContactKernel.open_kernel_grade): without pointwise "
            "decidability of the asserted relation the kernel read "
            "back from a candidate-A setting carries the double "
            "negation of that relation - PRICE: double-negation "
            "elimination (ContactBridge.stability_schema_iff_dne); "
            "exact under the explicit Decidable hypothesis "
            "(ofSetting_exact); no internal countermodel can exist",
            "COLLISION OPEN CELL (kernel, locatedness; "
            "ContactKernel.open_kernel_bl): underivability of Located "
            "from the kernel fields alone is METATHEORETIC - no "
            "internal countermodel exists, since every kernel with a "
            "pointwise-decidable zero predicate has a located "
            "apartness (kernel_located_of_decidable); Located remains "
            "separate declared data",
            "cut census formula 2^(n-2): computed to carrier 5, "
            "conjectured generally",
            "absolute self-interpretation: the outermost "
            "interpretation relation remains metatheoretic "
            "(inherited OPEN bridge); a DECLARED model of the "
            "boundary satisfies candidates A and F (Stage VIII), "
            "and the stronger identification is a frontier "
            "conjecture, not a result",
            "absolute no-outside: not formulable in this calculus; "
            "not claimed (inherited scope)",
        ],
        "extensions": [
            {"tag": "D2_MAP_INJECTIVE_INTO_IRREFLEXIVE",
             "status": "THEOREM",
             "evidence": ["PrimitiveCats.d2_map_injective",
                          "PrimitiveCats."
                          "d2_map_not_injective_without_irrefl"]},
            {"tag": "ATTACHMENT_TREES_POLICY_UNIFORM",
             "status": "THEOREM",
             "evidence": ["Attachment.treeAt_spec",
                          "Attachment.attach_residue",
                          "Attachment.parent_lt",
                          "Attachment.parent_unique",
                          "Attachment.parent_exists",
                          "Attachment.all_reach"]},
            {"tag": "GLOBAL_SHAPE_NOT_FORCED",
             "status": "COUNTERMODEL",
             "evidence": ["Attachment.path4_star4_not_isomorphic",
                          "Attachment.tree4_concrete"]},
            {"tag": "UP_FAMILY_REGISTRY_IFF_AND_RENAMING_ACTION",
             "status": "THEOREM",
             "evidence": ["Attachment.up_iff_legal (membership iff "
                          "declared one-edge legality)",
                          "Attachment.up_exec_eq / up_executes "
                          "(every block executes to a strict legal "
                          "extension)",
                          "Attachment.upBlock_transport / "
                          "upFamily_transport / act_up_comm "
                          "(genuine renaming action; replay "
                          "commutes, supply fragment)",
                          "Attachment.upFamily_grammar_uniform "
                          "(carrier-identical uniformity only)",
                          "orbit instances: Attachment."
                          "star_orbit_swap / path_oriented_rigid / "
                          "path_center_separate"]},
            {"tag": "UNIFORM_GUARDED_FILLER",
             "status": "THEOREM",
             "evidence": ["LadderGeneral.uniform_guarded_filler "
                          "(admission + strict extension under the "
                          "repaired well-formed guard, uniform in "
                          "the dimension; NOT a homology claim)",
                          "LadderGeneral.shell_refuses_general",
                          "LadderGeneral.shell_no_self_fill",
                          "LadderGeneral.wf_nreplay (well-formed "
                          "cells are a replayed invariant)",
                          "LadderGeneral.d4_demo",
                          "LadderGeneral.d4_wf",
                          "LadderGeneral.d4_guard_load_bearing"]},
            {"tag": "PR12_REPAIRS",
             "status": "THEOREM + COUNTERMODEL",
             "evidence": ["no clamping: Attachment.LawfulPolicy, "
                          "typed refusal Attachment."
                          "attachChecked_refuses / unlawful_refused; "
                          "countermodel clamp_rewrote_input",
                          "occurrence identity: tokens vs positions "
                          "resolved; Attachment.freshTok_fresh; "
                          "countermodel "
                          "length_not_fresh_countermodel; "
                          "Attachment.freshTok_treeState + "
                          "attachBlock_is_upBlock (coincide on "
                          "canonical tree states)",
                          "presentation invariance repaired: "
                          "countermodel "
                          "equal_size_not_renaming_related (equal "
                          "size, equal family, no relating "
                          "renaming)",
                          "selection never forced: countermodel "
                          "equal_cost_non_isomorphic_extensions",
                          "well-formed cells: countermodel "
                          "LadderGeneral.pseudo_cell_countermodel "
                          "([0,0] admitted by the legacy guard, "
                          "refused now)",
                          "receipt generation is deterministic under "
                          "declared CRLF-to-LF canonicalization and "
                          "fixed inputs; equality with current Git "
                          "blobs and mutation detection are tested"]},
            {"tag": "PROTECTED_SEPARATION_IS_TRACE_STABLE",
             "status": "THEOREM + COUNTERMODEL + RESTRICTED EXAMPLE",
             "evidence": ["SUFFICIENCY ONLY: StableContent."
                          "protSep_trace_stable — protected AND "
                          "separated implies separated after every "
                          "replay (protSep_persists / "
                          "protSep_replays)",
                          "CONVERSE IS FALSE: "
                          "StableContent."
                          "halted_stable_not_protected (absorption "
                          "— every replay inert, unprotected pair "
                          "trace stable).  Separate restricted-fragment "
                          "example: StableContent."
                          "unfunded_restricted_stable_not_protected "
                          "(resource blocking in the explicit "
                          "restricted trace fragment; no ownership "
                          "or full-trace claim)",
                          "instability is witness-borne: "
                          "StableContent.separation_breakable + "
                          "unprotected_separation_unstable",
                          "quiescence: StableContent."
                          "quiescent_iff_protected_separated + "
                          "quiescence_is_protected_separation "
                          "(a statement about protSep, NOT about "
                          "trace stability)"]},
            {"tag": "FINITE_WEIGHT_PROFILE_AND_SIGN_SHADOW",
              "status": "FINITE THEOREMS + SCOPED COUNTERMODELS",
              "evidence": ["on the positive-total domain the profile "
                           "is classified exactly by common positive "
                           "cross-multiples: WeightProfile."
                           "profile_iff_ray, with "
                           "profile_equivalence_positive and "
                           "profile_scale_positive; zero scaling "
                           "exits that domain (zero_scale_boundary)",
                           "carrier-facing lists are duplicate-free; "
                           "raw totals count repetitions with "
                           "multiplicity (CarrierList, total_append)",
                           "what it keeps and forgets: "
                           "profile_support, profile_order, "
                           "profile_forgets_total",
                           "a valid decorated presentation reproduces "
                           "the weight profile: "
                           "presentation_profile_redundant and "
                           "presentations_agree_on_profile",
                           "unsigned square presentations are "
                           "carrierwise determined; separately, two "
                           "valid integer-square presentations in the "
                           "declared two-coordinate fixture differ by "
                           "sign and are split by its declared mixing "
                           "read-out (signed_square_presentations_split)",
                           "descent classification: "
                           "descent_iff_subsingleton_support - a "
                           "two-coordinate integer read-out followed "
                           "by squaring descends through coordinate-"
                           "square fibers exactly when one coefficient "
                           "vanishes",
                           "NO PRICED CLIMB: the former carrier shape "
                           "is trivially inhabited, list additivity is "
                           "proved, and the former uniqueness schema "
                           "is false by the zero read-out "
                           "(claimedReadOutUniqueness_false)"]},
            {"tag": "GENERAL_BOUNDARY_CANCELLATION",
             "status": "THEOREM (general) + COUNTERMODEL",
             "evidence": ["BoundaryCancellation."
                          "d2_zero_unrestricted (every finite cell, "
                          "every face) and d2_zero_general (the "
                          "declared ascending hypotheses, "
                          "discharged from it)",
                          "the proof pairs deletion orders and "
                          "cancels signs: eraseIdx_swap, sgn_cancel, "
                          "dterm_cancel, coeff_rect, rect_zero, "
                          "tri_transpose",
                          "connected to replay: "
                          "BoundaryCancellation.d2_zero_replayed "
                          "(via LadderGeneral.wf_nreplay) and "
                          "d2_zero_d4",
                          "renaming independence for strictly "
                          "monotone renamings: eraseIdx_map, "
                          "ascB_map, d2_zero_renamed, d2_zero_shift",
                          "SIGNS ARE DECLARED, not derived: "
                          "signless_countermodel and "
                          "signless_countermodel_dim3 give nonzero "
                          "composites without them",
                          "ill-formed cells: illformed_countermodel "
                          "- strict ascent is load-bearing for "
                          "DISTINCTNESS of codimension-two faces "
                          "(codim2_distinct, eraseIdx_inj_of_asc), "
                          "NOT for the vanishing",
                          "the filler rule does NOT force the "
                          "coefficients or the signs; this is not "
                          "claimed anywhere"]},
            {"tag": "GRAPH_GROWTH_IS_SUPPLIED_NOT_GENERATED",
             "status": "THEOREM + COUNTERMODEL",
             "evidence": ["negative theorems: "
                          "GraphGenesis.refineCol_only_obs / "
                          "addCol_only_obs (seven fields provably "
                          "unchanged; only obs/budget are outside "
                          "the list)",
                          "GraphGenesis."
                          "extensionProposals_range_over_existing / "
                          "repairFamily_range_over_existing / "
                          "nextFamilyP_block_shape / "
                          "nextFamilyP_range_over_existing (the "
                          "internal family ranges over columns on "
                          "EXISTING occurrences only; no third "
                          "block shape exists)",
                          "GraphGenesis."
                          "internal_family_cannot_grow_carrier "
                          "(occ/asserted/wit/prot fixed along every "
                          "internal trace)",
                          "GraphGenesis.graph_growth_is_supplied "
                          "(the corollary: growth comes from the Up "
                          "grammar, never from the internal "
                          "response family)",
                          "PROPOSAL RECORD (Part 2): complete Up "
                          "membership proof, embedding+retraction, "
                          "fresh-token evidence, preservation of "
                          "asserted/retained/protected/separated "
                          "content, new pair with provenance, "
                          "declared cost, and NO license, execution "
                          "or activation field; "
                          "GraphGenesis.proposal_confers_no_"
                          "execution",
                          "GraphGenesis.proposal_transports + "
                          "proposal_family_retains_ties (transport "
                          "under renaming; equal-cost "
                          "non-isomorphic branches retained, no "
                          "selection)",
                          "PART 3 VERDICT (irreducibility): "
                          "GraphGenesis."
                          "growth_demand_not_obstruction_consequence"
                          " + family_never_grows_carrier + "
                          "obstruction_resolved_in_carrier - an "
                          "active obstruction is answered INSIDE "
                          "the existing carrier, so the "
                          "carrier-changing growth demand is a "
                          "separately declared premise, not an "
                          "obstruction consequence"]},
            {"tag": "UP_IS_EQUIVARIANT_EARNED",
             "status": "THEOREM + COUNTERMODEL",
             "evidence": ["group laws: RenamingStructure.comp_id / "
                          "id_comp / comp_assoc / inv_comp / "
                          "comp_inv / inv_inv, via Renaming.ext",
                          "action laws: RenamingStructure.act_id "
                          "(unconditional) / act_comp (scope "
                          "n <= occ.length) / act_inv",
                          "transport respects the structure: "
                          "upBlock_id / upBlock_comp / upFamily_id / "
                          "upFamily_comp / upFamily_transport_id / "
                          "upFamily_transport_comp",
                          "coherence: act_up_comm_comp + "
                          "act_up_comm_twostep (the naturality "
                          "square closes under composition)",
                          "no selected representative: "
                          "upFamily_orbit_closed / "
                          "star_orbit_both_present / "
                          "upFamily_length",
                          "countermodels supplying NO law: "
                          "collapse_not_a_renaming + "
                          "collapse_pushforward_ill_formed "
                          "(arbitrary non-bijective map), "
                          "equal_size_supplies_no_law, "
                          "equal_cost_supplies_no_law",
                          "the word 'equivariant' is used only in "
                          "RenamingStructure.equivariance_summary, "
                          "after the laws, with its exact scope"]},
            {"tag": "TARGET_RELATIVE_COMPRESSION",
             "status": "THEOREM + COUNTERMODEL",
             "evidence": ["Compression.factors_iff_fiberConstant + "
                          "factor_unique_on_image + "
                          "factor_not_unique_off_image (A)",
                          "Compression.pQ_exact / pQ_adequate / "
                          "pQ_coarsest / pQ_unique_on_image (B: "
                          "coarsest Q-adequate, universal property "
                          "with exact scope)",
                          "Compression.descent_witness (C: every "
                          "merged-but-separated pair is witnessed)",
                          "Compression.enlarge_refines + "
                          "splits_iff_new_separator (D)",
                          "Compression.absolute_adequacy_iff_"
                          "injective (E: absolute adequacy = "
                          "injectivity = no compression)",
                          "Compression.dup_no_refine / "
                          "postcompose_no_refine / "
                          "refine_requires_separator (F: replay and "
                          "digests add no separating question)",
                          "Compression.refine_bounded / "
                          "strict_split_increases / chain_bounded / "
                          "strict_steps_lt (iteration bounded by "
                          "the declared domain)",
                          "countermodels: refinement_not_unique, "
                          "refinement_tie (no unique, no "
                          "unique-minimum refinement)"]},
        ],
        "frontier_conjectures": [
            {"conjecture":
                "INTERPRETER_BOUNDARY_IS_PRIMITIVE_DIFFERENCE",
             "missing_theorem":
                "a denotational bridge connecting code, "
                "interpretation, lawful interpreter behavior, the "
                "uncoded evaluator role, and an OPERATIONALLY "
                "EFFECTIVE non-identification — the current "
                "diagonal differs only at the operationally inert "
                "notes field, and no theorem links the uncoded "
                "occurrence to the missed function "
                "(InterpreterBoundary.arbitrary_uncoded_assignment "
                "proves that a freely chosen interpretation is "
                "vacuous; openDenotationalBridge names the missing "
                "obligation but is not a proposition; the former "
                "i5_difference_grounded was renamed to "
                "i5_family_not_extensionally_complete because its "
                "statement is family_missed and mentions neither "
                "the boundary pair nor the uncoded occurrence)"},
            {"conjecture": "GENERAL_BOUNDARY_COMPOSITE_VANISHING",
             "missing_theorem":
                "SETTLED (Goal 4), and settled more strongly than "
                "conjectured: the coefficientwise composite boundary "
                "vanishes at EVERY target presentation for EVERY "
                "finite list "
                "(BoundaryCancellation.d2_zero_unrestricted), proved "
                "by pairing the two orders for each unordered pair "
                "of deleted positions and cancelling their signs "
                "(eraseIdx_swap, sgn_cancel, dterm_cancel, "
                "rect_zero) - not by computation.  The declared "
                "hypotheses are recorded in d2_zero_general and "
                "discharged from the stronger theorem; strict "
                "ascent turned out NOT to be load-bearing for the "
                "vanishing itself, only for distinctness of the "
                "codimension-two faces (codim2_distinct, "
                "eraseIdx_inj_of_asc).  The signs and integer "
                "coefficients remain DECLARED inputs: "
                "the integer signless_countermodel is nonzero, and "
                "the filler rule does not force the signs.  No claim "
                "is made that the signless countermodel works in "
                "every coefficient system"},
            {"conjecture": "GRAPH_GENESIS_BY_OBSTRUCTION",
             "missing_theorem":
                "SETTLED NEGATIVELY for this calculus (Goal 5): the "
                "internal response family provably cannot create "
                "occurrences, asserted, retained or protected pairs "
                "(GraphGenesis.internal_family_cannot_grow_carrier, "
                "family_never_grows_carrier), and every obstruction "
                "meeting the kernel's own hypotheses is resolved "
                "inside the existing carrier "
                "(obstruction_resolved_in_carrier).  What remains "
                "is therefore not a conjecture about THIS driver "
                "but the OPEN question whether some OTHER declared "
                "response family could request a lawful "
                "carrier-changing proposal.  One explicit sufficient "
                "proposal schema is delivered as "
                "GraphGenesis.ProposalRecord; no minimality or "
                "universal property is proved for that schema, and "
                "growth is not entailed by nextFamilyP"},
            {"conjecture":
                "ENLARGED_CORPUS_CONTAINS_RECONSTRUCTED_SUPPLIED_"
                "ABSTRACT_HALF",
             "missing_theorem":
                "RECORDED AT THE COLLISION (2026-08-13).  "
                "Post-reconstruction, the enlarged native corpus is "
                "conjectured to contain strictly the reconstructed "
                "image of the supplied abstract half, while the "
                "converse containment remains signature-impossible "
                "by the native -> supplied countermodels "
                "(ContactBridge.d2_not_obs_complement and the "
                "nine-reading row).  MISSING: any formal notion of "
                "corpus containment inside the calculus - the "
                "statement is METATHEORY about two corpora, not a "
                "proposition of the development; consequently no "
                "strictly-stronger verdict is issued this run, and "
                "any future one must be stated relative to the "
                "enlarged corpus, never the sealed one"},
            {"conjecture": "LOCATEDNESS_SCHEMA_EQUALS_WLEM",
             "missing_theorem":
                "RECORDED AT THE COLLISION (2026-08-13).  The "
                "forward price is proved "
                "(ContactBridge.located_schema_implies_wlem: the "
                "locatedness schema quantified over all observers "
                "implies the weak law of excluded middle).  MISSING: "
                "the converse.  Deriving the locating boolean for an "
                "arbitrary observer from WLEM alone appears to need "
                "a function-comprehension principle beyond it, so "
                "the equivalence is conjectured to FAIL at WLEM and "
                "to require a stronger principle; the OPEN cell "
                "ContactBridge.open_bridge_located carries the same "
                "obligation, and no internal countermodel can exist "
                "because the schema is classically true"},
        ],
        "adversarial_record": [
            {"attack": "metatheoretic inequality relabeled as "
                       "object-level difference",
             "disposition": "BLOCKED: PrimitiveCore.D_iff_ne, "
                            "nimp_w_d, "
                            "PrimDiff.meta_diff_without_assertion; "
                            "contact update: the supplied "
                            "physics-labeled tail is metatheoretic "
                            "inequality rendered on Int - subsumed "
                            "by five native one-line lemmas "
                            "(ObsDescent.int_sub_ne_zero_iff, "
                            "int_sub_ne_zero_of_gt, "
                            "int_shift_cancel, "
                            "int_two_mul_eq_zero_iff, "
                            "int_add_sub_cancel)"},
            {"attack": "witness relabeled as observer separation",
             "disposition": "BLOCKED: "
                            "Completion.witness_not_separation, "
                            "PrimitivePassage."
                            "wit_independent_of_obs"},
            {"attack": "two-ness relabeled as relation",
             "disposition": "BLOCKED: two-ness forced only under "
                            "irreflexivity "
                            "(no_witness_on_subsingleton); bare "
                            "one-point witness countermodel"},
            {"attack": "finite off-diagonal facts relabeled as an "
                       "irreflexivity law",
             "disposition": "BLOCKED: laws only by admission; "
                            "RefusalFrontier.bridge_facts_not_law "
                            "(sealed); OPEN located cells kept OPEN"},
            {"attack": "orientation imported through ordered "
                       "endpoint names",
             "disposition": "BLOCKED: "
                            "Apartness.orientations_same_apartness "
                            "+ orientations_differ price the "
                            "orientation as retained data; "
                            "PrimitiveCats.pointed_rigid; contact "
                            "update: orientation is not importable "
                            "through a zero-complement over any "
                            "value type "
                            "(ContactBridge.d2_not_obs_complement); "
                            "the value channel carries orientation "
                            "separately and the zero relation "
                            "cannot (ObsDescent."
                            "value_orientation_survives, "
                            "ContactKernel."
                            "value_presentation_fork)"},
            {"attack": "protection silently merged with retention",
             "disposition": "BLOCKED: separate stores throughout; "
                            "matrix cells separate C/F; the sealed "
                            "ofWorld identification is stated"},
            {"attack": "observer imported into Primitive Difference",
             "disposition": "BLOCKED: "
                            "obst_requires_observation (theorem); "
                            "the candidate signature has no "
                            "observation field; contact update: the "
                            "supplied stratum is an ADMITTED "
                            "observer at the zero-relation stage, "
                            "not a pre-observational witness "
                            "(ContactBridge.kernelStage, "
                            "declared_zero_as_view, "
                            "observation_stage_realizes_observer); "
                            "the common kernel carries no observer "
                            "(ContactKernel.kernel_not_observer)"},
            {"attack": "quotient no-recovery applied without a "
                       "protected distinction",
             "disposition": "BLOCKED: quotient_no_recovery takes "
                            "the identification hypothesis; "
                            "no_protection_no_obstruction"},
            {"attack": "repair-family existence sold as execution",
             "disposition": "BLOCKED: proposal_not_execution, "
                            "budget_gates_execution"},
            {"attack": "extension proposal sold as authorization",
             "disposition": "BLOCKED: license and budget gates are "
                            "separate events in every funded block"},
            {"attack": "refusal record sold as terminal",
             "disposition": "BLOCKED: refusal_not_terminal vs "
                            "terminal_absorbing, separately typed"},
            {"attack": "recursive definition sold as internal "
                       "triggering",
             "disposition": "BLOCKED: next-family iteration stated "
                            "metatheoretic; sealed autonomy level 4 "
                            "remains NOT attained"},
            {"attack": "singleton policy family sold as absence of "
                       "policy",
             "disposition": "BLOCKED: the growth policy is a "
                            "declared driver; the closure family is "
                            "non-singleton at obstructions "
                            "(nextFamilyP_complete_*)"},
            {"attack": "probe-compliance uniqueness sold as "
                       "initiality",
             "disposition": "SETTLED AGAINST INITIALITY: Stage VII "
                            "refutation in a genuine category; live "
                            "census 128"},
            {"attack": "one split retract sold as a universal "
                       "property",
             "disposition": "BLOCKED: erase_sim is one morphism; "
                            "initiality refuted; orbit-relative "
                            "agreement is the exact positive scope"},
            {"attack": "fixed interpreter sold as represented "
                       "constitution",
              "disposition": "BLOCKED AT THE DECLARED SCOPE: "
                            "family_missed proves only that the finite "
                            "family does not exhaust the step-function "
                            "type; it does not rule out a coded "
                            "evaluator"},
            {"attack": "self-description sold as "
                       "self-interpretation",
              "disposition": "NOT ESTABLISHED: interp_describe is a "
                            "verified step description; family_missed "
                            "is separate finite non-exhaustion and no "
                            "self-interpretation impossibility follows"},
            {"attack": "finite model enumeration sold as "
                       "unrestricted theorem",
             "disposition": "BLOCKED: every bound declared in this "
                            "receipt; formulas beyond bounds are "
                            "computations or conjectures"},
            {"attack": "contact comments sold as contact Lean "
                       "results",
             "disposition": "EXECUTED AND BLOCKED: contact input "
                            "arrived this run and was read under "
                            "the committed statements-only "
                            "discipline; every comment-vs-content "
                            "gap in the supplied file has a "
                            "recorded disposition (G1-G20 in "
                            "contact/analysis/"
                            "contact_countermodels.json); "
                            "comment-borne physics vocabulary was "
                            "REFUSED transport into the formal "
                            "record - only stated theorems "
                            "collided"},
            {"attack": "proof-theoretic non-derivability asserted "
                       "in comments over undefined predicates "
                       "(the supplied authority-firewall claim)",
             "disposition": "REFUSED TRANSPORT: the comment claims "
                            "a non-derivability between two "
                            "predicates never defined in the file; "
                            "no proof system or derivability "
                            "relation exists there; the actual "
                            "formal content is integer subtraction "
                            "(a difference of two free integers is "
                            "nonzero when they differ) and was "
                            "reconstructed at exactly that "
                            "strength (ObsDescent."
                            "int_sub_ne_zero_iff); the G12 row of "
                            "the analysis file records the gap"},
            {"attack": "graph/cochain realization sold as forced "
                       "ontology",
             "disposition": "BLOCKED: filling_not_forced, "
                            "boundary_not_forced; the driver "
                            "supplies graph data and the "
                            "obstruction creates observation "
                            "columns (stated exactly); the "
                            "post-hoc table is derivation-inert"},
        ],
        "withdrawn_or_repaired_claims": [
            "42a33d9 item 8 cross-language claim: REFUTED and "
            "repaired (C10; Horizon budget saturation pins)",
            "CL-NC-AUTONOMY lawfulness citation: OVERSTATED and "
            "closed upward (C6; Horizon every-horizon theorems)",
        ],
        "graph_scope": "dependency records classify declared "
                       "bridges; no claim exhausts every possible "
                       "bridge (inherited scope)",
    }


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path,
                        default=Path("artifacts"))
    args = parser.parse_args(argv)
    payload = receipt()
    out_path = args.artifacts / "primitive_completion_receipt.json"
    write_json(out_path, payload)
    terminals = payload["terminals"]
    assert isinstance(terminals, list)
    print(f"terminals: {len(terminals)}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
