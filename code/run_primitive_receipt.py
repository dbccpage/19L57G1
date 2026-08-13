"""Produce the PR #12 completion receipt deterministically.

Usage: python code/run_primitive_receipt.py [--artifacts DIR]

Writes ``primitive_completion_receipt.json``: the binding record of
the contact-and-passage run — base commit, contact status, prompt
hashes, toolchain and dependency pins, the axiom-report hash, all
declared finite bounds, every terminal claim with its evidence, all
open obligations, and the adversarial record (twenty attacks, each
with its disposition)."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Optional

from derivation.export import Json, write_json

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
    return {
        "run": "PR #12 — Primitive Difference contact and passage",
        "blind_native_base": "ccd3a53",
        "contact": {
            "package_present": (REPO / "contact").exists(),
            "manifest_hash": None,
            "status": "CONTACT_INPUT_ABSENT",
        },
        "prompt_sha256_canonical": {
            "prompt/prompt.md":
                canonical_sha256(REPO / "prompt/prompt.md"),
            "prompt/seed_prompt.md":
                canonical_sha256(REPO / "prompt/seed_prompt.md"),
            "prompt/prompt_pr12.md":
                canonical_sha256(REPO / "prompt/prompt_pr12.md"),
            "prompt/ultra_prompt_pr12.md":
                canonical_sha256(REPO / "prompt/ultra_prompt_pr12.md"),
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
             "evidence": ["primitive_contact.json",
                          "PrimitiveContact.contactStatus"]},
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
            "cut census formula 2^(n-2): computed to carrier 5, "
            "conjectured generally",
            "absolute self-interpretation: the outermost "
            "interpretation relation remains metatheoretic "
            "(inherited OPEN bridge); a DECLARED model of the "
            "boundary satisfies candidates A and F (Phase VIII), "
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
                "the guarded filler is a theorem at every dimension "
                "(LadderGeneral.uniform_guarded_filler, narrowed "
                "scope: admission + strict extension, not "
                "homology); what remains is the "
                "general vanishing of the composite boundary for "
                "every dimension — decided at dimensions 2–5, "
                "general case open"},
            {"conjecture": "GRAPH_GENESIS_BY_OBSTRUCTION",
             "missing_theorem":
                "a driver in which graph vertices and edges are "
                "themselves extension proposals generated by "
                "obstructions; in this run the driver SUPPLIES the "
                "graph data and the obstruction creates observation "
                "structure (a later experiment, out of scope here)"},
        ],
        "adversarial_record": [
            {"attack": "metatheoretic inequality relabeled as "
                       "object-level difference",
             "disposition": "BLOCKED: PrimitiveCore.D_iff_ne, "
                            "nimp_w_d, "
                            "PrimDiff.meta_diff_without_assertion"},
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
                            "PrimitiveCats.pointed_rigid"},
            {"attack": "protection silently merged with retention",
             "disposition": "BLOCKED: separate stores throughout; "
                            "matrix cells separate C/F; the sealed "
                            "ofWorld identification is stated"},
            {"attack": "observer imported into Primitive Difference",
             "disposition": "BLOCKED: "
                            "obst_requires_observation (theorem); "
                            "the candidate signature has no "
                            "observation field"},
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
             "disposition": "SETTLED AGAINST INITIALITY: Phase VII "
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
             "disposition": "MOOT AND GUARDED: no contact input "
                            "exists; the committed protocol reads "
                            "statements only"},
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
