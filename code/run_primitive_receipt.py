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


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
        "prompt_sha256": {
            "prompt/prompt.md": sha256_of(REPO / "prompt/prompt.md"),
            "prompt/seed_prompt.md":
                sha256_of(REPO / "prompt/seed_prompt.md"),
            "prompt/prompt_pr12.md":
                sha256_of(REPO / "prompt/prompt_pr12.md"),
        },
        "toolchain": {
            "lean": (REPO / "lean4/lean-toolchain")
                .read_text(encoding="utf-8").strip(),
            "python_requirements_sha256":
                sha256_of(REPO / "requirements.txt"),
        },
        "axiom_report": {
            "sha256": sha256_of(lean_axioms),
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
        },
        "terminals": [
            {"code": "NATIVE_PRIMITIVE_DIFFERENCE_CHARACTERIZED",
             "evidence": ["PrimitiveCore.matrixCells (72 cells)",
                          "PrimitiveCats.d2_initial",
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
             "evidence": ["PrimitivePassage (all fourteen arrows "
                          "with statuses)",
                          "primitive_passage.json"]},
            {"code": "TWO_RULE_SCHEMA_PROVED_UNDER_"
                     "DECLARED_RESPONSE_UNIVERSE_AND_WF_PROTECTED_"
                     "PAIR",
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
            {"code": "INTERPRETER_TOWER_PERSISTS",
             "evidence": ["InterpreterBoundary.tower_persists",
                          "primitive_interpreter.json "
                          "(diagonal_misses_all)"]},
            {"code": "INTERPRETER_BOUNDARY_IS_PRIMITIVE_DIFFERENCE",
             "evidence": ["InterpreterBoundary.i5_boundary_is_A",
                          "InterpreterBoundary.i5_boundary_is_F",
                          "InterpreterBoundary."
                          "i5_collapse_obstructed",
                          "InterpreterBoundary."
                          "i5_difference_grounded"]},
            {"code": "HIGHER_STRUCTURE_OPTIONAL_NOT_FORCED",
             "evidence": ["HigherStructure.filling_not_forced",
                          "HigherStructure.boundary_not_forced",
                          "HigherStructure.ladder_dim2/dim3"]},
        ],
        "open_obligations": [
            "four OPEN located matrix cells (a->bl, bs->bl, bc->bl, "
            "f->bl): no internal countermodel can exist "
            "(located_of_decidable); independence is metatheoretic",
            "PrimitiveCats.openTerminalPres2: two-point observer "
            "terminality is selection-relative; unrestricted form "
            "needs a preimage-selection principle",
            "cut census formula 2^(n-2): computed to carrier 5, "
            "conjectured generally",
            "absolute self-interpretation: the outermost "
            "interpretation relation remains metatheoretic "
            "(inherited OPEN bridge), now POSITIVELY characterized: "
            "the boundary satisfies the native kernel candidates A "
            "and F (Phase VIII) — open as absolute closure, "
            "structured as Primitive Difference",
            "absolute no-outside: not formulable in this calculus; "
            "not claimed (inherited scope)",
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
             "disposition": "BLOCKED: family_missed (the family "
                            "provably misses an interpreter-grade "
                            "function)"},
            {"attack": "self-description sold as "
                       "self-interpretation",
             "disposition": "BLOCKED: interp_describe vs "
                            "family_missed (I4)"},
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
                            "boundary_not_forced; the post-hoc "
                            "table is derivation-inert"},
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
