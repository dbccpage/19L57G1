"""Produce the contact-status artifact deterministically.

Usage: python code/run_primitive_contact.py [--artifacts DIR]

Writes ``primitive_contact.json``: the declared contact protocol, the
three-valued contact status (absent / present-unprocessed /
processed-Lean-only), the manifest binding, the status history
preserving the sealed pre-contact terminal, the executed-collision
verdict with its terminal codes and scopes, the 37-row collision-cell
mirror of ``ContactKernel.contactCells``, and five independent finite
enumeration probes (E1-E5) whose checks the generator enforces by
raising.  All inputs are in-repo: the artifact is byte-identical with
or without the external contact file."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from itertools import product
from pathlib import Path
from typing import Optional

from derivation.export import Json, write_json

STATUS_ABSENT = "CONTACT_INPUT_ABSENT"
STATUS_UNPROCESSED = "CONTACT_PRESENT_UNPROCESSED"
STATUS_PROCESSED = "CONTACT_PROCESSED_LEAN_ONLY"

STATUS_HISTORY: list[str] = [
    "CONTACT_INPUT_ABSENT (pre-contact, blind-native-base ccd3a53)",
    "CONTACT_PROCESSED_LEAN_ONLY (2026-08-13, base a5caee2)",
]

VERDICT_PRIMARY = "CONTACT_INCOMPARABLE_WITH_COUNTERMODELS"

SCOPE_INCOMPARABLE = (
    "Sealed native corpus at a5caee2 versus the supplied single-file "
    "development (sha256 d9cdb350a53c513e3e211e72f17262be6ba85d7da6"
    "159f910388c7137e814a89), Lean content only (manifest: "
    "prose_supplied = false, PROSE_INPUT_ABSENT).  WITH_COUNTERMODELS "
    "covers the native -> supplied direction only; the other "
    "direction is an absence claim, stated as such below.  Native -> "
    "supplied: refuted at signature level - no valued observer's "
    "zero-complement equals the oriented two-element witness over any "
    "value type (ContactBridge.d2_not_obs_complement); for "
    "Prop-valued observers (DiffObs X Prop) the representable class "
    "is exactly the double-negation-stable complements of "
    "equivalences (ContactBridge.obsApart_repr_iff - no claim is made "
    "for observers at other value types, where only the forward "
    "direction is available); each of the nine native candidate "
    "readings fails representability or witness-transport, with "
    "finite countermodels exhibited at carrier sizes "
    "1,2,3,2,2,1,2,2,2.  MINIMALITY of those carriers is proved for "
    "exactly one reading - Bs at 3, by the positive "
    "ContactBridge.bool_bs_repr at carrier 2; the remaining sizes are "
    "the least carrier at which the reading can be posed at all (a "
    "reading demanding a distinguished pair cannot be stated below "
    "carrier 2), which is METATHEORY, not a proved minimum, and "
    "contact/analysis/lean_theorem_transport.md records carrier "
    "minimality as unclaimed for d_not_witnessed_repr and "
    "no_kernel_over_allzero; Bc, Bl and F carry no separate "
    "countermodel and fail through the A-conjunct models cited in "
    "contact/analysis/contact_countermodels.json.  Protection, "
    "retention, operations, and the designated pair are underivable "
    "(ContactKernel.kernel_not_c, ContactKernel.kernel_not_f, "
    "ContactKernel.pair_choice_load_bearing).  Supplied -> native: an "
    "ABSENCE claim about the sealed corpus, NOT a refutation - the "
    "supplied global quotient-descent layer "
    "(existence-iff-compatibility, global uniqueness, mod-setoid "
    "transport) does not occur in the sealed corpus (FINITE_"
    "COMPUTATION over the corpus text plus METATHEORY), whose "
    "image-scoped uniqueness plus off-image countermodel "
    "(Compression.factor_not_unique_off_image) is deliberately weaker "
    "on arbitrary presentations; no countermodel refutes the layer, "
    "and its content is in fact derivable natively for the "
    "Nat-scoped kernel observers of the dictionary "
    "(ObsDescent.descend_iff_factorsOn_all); reconstructed this run "
    "(ObsDescent) in native vocabulary under identical axiom budget "
    "within {propext, Quot.sound}.  The incomparability is asymmetric "
    "in kind: signature-level and permanent against the supplied "
    "side; content-level and closed-this-run against the native side."
)

SCOPE_KERNEL = (
    "The kernel ContactKernel.WitnessedDiff (valued difference "
    "presentation + designated endpoints + diagonal-zero law + "
    "refutation-grade non-zero witness; NO symmetry/transitivity "
    "admissions, NO retention/protection/operations): realized from "
    "native candidate-A settings (ofSetting; exact under pointwise "
    "decidability, double-negation-coarse otherwise - recorded OPEN) "
    "and from valued observers plus a chosen non-zero pair (ofDiffObs; "
    "the pair proved load-bearing); meets the sealed pre-contact "
    "interface (toNativeKernel : WitnessedDiff X R -> "
    "PrimitiveContact.NativeKernel); universal status proved: initial "
    "gateway inherited from sealed d2_initial (kernel_gateway_unique), "
    "no terminal collector AT THE INDUCED-APARTNESS MORPHISM GRADE "
    "(kernel_no_terminal_collector, kernel_no_terminal: morphisms of "
    "the induced pointed-relation presentations apartObj, which "
    "discard the value data; nothing is proved about terminality in "
    "the valued morphism category VHom), value grade is presentation "
    "with off-image non-uniqueness (vhom_not_unique) rigidified UNDER "
    "delta-surjectivity (vhom_unique_of_onto - sufficiency plus one "
    "non-onto countermodel; no equivalence is proved, so necessity is "
    "not claimed); licenses passage entry pre-retention/"
    "pre-observation (kernel_licenses_entry), where the kernel "
    "contributes ENDPOINT DISTINCTNESS ONLY - the other two conjuncts "
    "(candidate A at the sealed pre-retention state, empty retention "
    "store) are sealed constants that do not mention the kernel, and "
    "no map from an arbitrary kernel into the passage state is "
    "claimed (entry_pre_observation).  'Replaces' is scoped to the "
    "OVERLAP: entry-level content of both sides is the kernel + "
    "separately declared additions.  Supplied side, DEFINITION not "
    "derivation: the kernel together with the two law declarations "
    "IS the observer record, field-for-field and losslessly "
    "(toDiffObs, toDiffObs_fields, toDiffObs_apart), and the two "
    "declarations are priced at carriers two and three "
    "(kernel_not_observer, kernel_zero_not_trans).  Native side, "
    "DERIVED_THEOREM: toSetting_A, kernel_to_w, kernel_to_d, "
    "kernel_to_e_empty, with the declarations shown separable "
    "(ofSetting_ret_irrelevant, ContactBridge.kernel_prot_"
    "independent).  It does NOT replace native orientation, "
    "retention/protection, operations, or passage dynamics - "
    "native-only surplus."
)

SCOPE_EQUIVALENT = (
    "On the relational core only.  Premise 1 - the supplied core "
    "structure and the native DiffObs correspond field-for-field at "
    "the observer stratum - is a mechanical scratch check run OUTSIDE "
    "the repository (FINITE_COMPUTATION; file and log sha256 recorded "
    "in contact/analysis/contact_countermodels.json, field "
    "correspondence_map.scratch_bridge_check).  The vocabulary "
    "firewall forbids "
    "committing that check, so it is NOT reproducible from this "
    "repository: no CI job, test, or reviewer re-runs it.  Premise 2 "
    "is TWO decidability admissions, one per direction, and they are "
    "NOT interchangeable.  Apartness -> observer spends pointwise "
    "decidability of the ASSERTED APARTNESS relation "
    "(ContactBridge.isApart_repr, ContactBridge.apartObs_roundtrip: "
    "[forall x y, Decidable (r x y)]).  Observer -> apartness spends "
    "pointwise decidability of the ZERO relation "
    "(ContactBridge.obsApart_isApart, "
    "ContactBridge.indist_obsApart_iff: [forall x y, Decidable "
    "(ZeroRel O x y)]).  The two do not substitute for each other: "
    "the zero relation of the observer built from an apartness is the "
    "negation of that apartness, and Decidable of a negation does not "
    "return Decidable of the statement - that residue is exactly what "
    "stability_schema_iff_dne prices at double-negation elimination.  "
    "Under both admissions and the three IsApart admissions the "
    "native apartness and the supplied-style observer are "
    "inter-constructible with matching relations in both round trips. "
    " Dropping decidability is priced: cotransitivity-schema <-> WLEM "
    "(cotrans_schema_iff_wlem), stability-schema <-> DNE "
    "(stability_schema_iff_dne), locatedness-schema -> WLEM "
    "(located_schema_implies_wlem; forward direction only, converse "
    "OPEN).  Dropping any IsApart admission is refuted at carriers "
    "1/2/3 (sealed countermodels cited).  Statement scope: carriers "
    "and value types range over Type (universe 0), where the supplied "
    "structure is universe-polymorphic; the apartness -> observer "
    "direction produces a Prop-valued observer.  Valuation data, "
    "orientation, and everything dynamic is OUTSIDE this scope (the "
    "other terminal codes govern there)."
)

# The 37-row literal mirror of ``ContactKernel.contactCells``.  A test
# cross-checks this list against the Lean literal row for row.
COLLISION_CELLS: list[tuple[str, str, str]] = [
    ("K_to_W", "IMPLIES", "kernel_to_w"),
    ("W_to_K", "COUNTERMODEL size 1",
     "no_kernel_on_subsingleton (unitBare cited)"),
    ("K_to_A", "IMPLIES", "toSetting_A"),
    ("A_to_K", "EQUIV_UNDER_DEC (asserted relation S.r)",
     "ofSetting, ofSetting_exact, open_kernel_grade"),
    ("K_to_Bs", "COUNTERMODEL size 2", "kernel_not_bs"),
    ("Bs_to_K", "IMPLIES", "ofSetting (Bs within A)"),
    ("K_to_Bc", "COUNTERMODEL size 3", "kernel_not_bc"),
    ("Bc_to_K", "IMPLIES", "ofSetting (Bc within A)"),
    ("K_to_Bl", "CONDITIONAL_DEC + OPEN_PRICED",
     "kernel_located_of_decidable, open_kernel_bl"),
    ("Bl_to_K", "IMPLIES", "ofSetting (Bl within A)"),
    ("K_to_C", "COUNTERMODEL (never derivable, freely declarable)",
     "kernel_not_c, kernel_prot_independent"),
    ("C_to_K", "COUNTERMODEL size 1",
     "no_kernel_on_subsingleton (unitFull cited)"),
    ("K_to_D", "IMPLIES", "kernel_to_d"),
    ("D_to_K", "COUNTERMODEL size 2", "no_kernel_over_allzero"),
    ("K_to_E", "IMPLIES (empty Ops) / COUNTERMODEL (merged)",
     "kernel_to_e_empty, kernel_not_e_merged"),
    ("E_to_K", "COUNTERMODEL size 2",
     "no_kernel_over_allzero (boolEmpty_e cited)"),
    ("K_to_F", "COUNTERMODEL (never derivable)", "kernel_not_f"),
    ("F_to_K", "IMPLIES",
     "ofSetting via imp_f_a, ofSetting_ret_irrelevant"),
    ("Obs_to_Bs", "IMPLIES", "obsSetting_bs"),
    ("Obs_to_Bc", "CONDITIONAL_DEC + OPEN_PRICED",
     "obsApart_cotrans, cotrans_schema_iff_wlem, open_bridge_cotrans"),
    ("Obs_to_Bl", "CONDITIONAL_DEC + OPEN_PRICED",
     "obsSetting_bl, located_schema_implies_wlem, open_bridge_located"),
    ("repr_crown", "CHARACTERIZATION", "obsApart_repr_iff"),
    ("D2_repr (H3)", "COUNTERMODEL size 2", "d2_not_obs_complement"),
    ("Bs_repr", "COUNTERMODEL size 3, positive at 2",
     "triSym_not_obs_complement, bool_bs_repr"),
    ("total_repr (W/C)", "COUNTERMODEL size 1", "unit_total_not_repr"),
    ("witness_repr (D/E)", "COUNTERMODEL size 2",
     "d_not_witnessed_repr"),
    ("meet_roundtrip", "EQUIV_UNDER_DEC (apartness r one way, ZeroRel back)",
     "isApart_repr, obsApart_isApart, apartObs_roundtrip, "
     "indist_obsApart_iff"),
    ("stability_price", "OPEN_PRICED", "stability_schema_iff_dne"),
    ("descent_vs_factorsOn", "SAME_THIRD_NOTION",
     "descend_iff_factorsOn_all, classConstant_iff_fiberConstant_all"),
    ("fixed_D_strict", "COUNTERMODEL (D = [])",
     "fiberConstant_fixed_D_not_classConstant"),
    ("uniqueness_scope", "SAME_THIRD_NOTION",
     "obsQuotient_mk_surjective (+ sealed citations)"),
    ("quot_barrier", "NATIVE_MORE_GENERAL",
     "Derivation.quot_barrier (citation)"),
    ("pairing_dict", "SAME_THIRD_NOTION",
     "classConstant_pair_iff, sigEq_append_iff"),
    ("flagship_vs_obstP", "SAME_THIRD_NOTION (native finer)",
     "pair_blocked_is_collapse_collision (+ obst_conditions_"
     "independent cited)"),
    ("tail_subsumption", "SAME_THIRD_NOTION",
     "intDiffObs, int_sub_ne_zero_iff, int_sub_ne_zero_of_gt, "
     "int_shift_cancel, int_two_mul_eq_zero_iff, int_add_sub_cancel"),
    ("observer_placement (H1)",
     "IMPLIES (native proves what supplied fields declare)",
     "declared_zero_as_view, observation_stage_realizes_observer, "
     "kernelStage, kernel_stage_no_obstruction"),
    ("value_orientation", "INCOMPARABLE_SUBROW",
     "value_orientation_survives, value_presentation_fork"),
]


def _require(cond: bool, message: str) -> None:
    """Generator-level check: a red probe blocks artifact
    regeneration (and therefore the run) by raising."""
    if not cond:
        raise ValueError(f"enumeration check failed: {message}")


def enum_bool_observers() -> dict[str, Json]:
    """E1 (the H3 slice on Bool values): all 16 difference tables x 4
    zero predicates on the two-point carrier; no full observer has the
    oriented table as its zero-complement."""
    pts = (False, True)
    tables = list(product(pts, repeat=4))

    def dval(t: tuple[bool, ...], x: bool, y: bool) -> bool:
        return t[(2 if x else 0) + (1 if y else 0)]

    zpreds = list(product(pts, repeat=2))

    def zmem(z: tuple[bool, ...], v: bool) -> bool:
        return z[1 if v else 0]

    def zrel(t: tuple[bool, ...], z: tuple[bool, ...],
             x: bool, y: bool) -> bool:
        return zmem(z, dval(t, x, y))

    def diag_zero(t: tuple[bool, ...], z: tuple[bool, ...]) -> bool:
        return all(zrel(t, z, x, x) for x in pts)

    def laws(t: tuple[bool, ...], z: tuple[bool, ...]) -> bool:
        refl = diag_zero(t, z)
        symm = all(zrel(t, z, y, x)
                   for x in pts for y in pts if zrel(t, z, x, y))
        trans = all(zrel(t, z, x, w)
                    for x in pts for y in pts for w in pts
                    if zrel(t, z, x, y) and zrel(t, z, y, w))
        return refl and symm and trans

    diag_pairs = sum(1 for t in tables for z in zpreds
                     if diag_zero(t, z))
    law_pairs = sum(1 for t in tables for z in zpreds if laws(t, z))
    kernel_quads = sum(1 for t in tables for z in zpreds
                       for a in pts for b in pts
                       if diag_zero(t, z) and not zrel(t, z, a, b))
    oriented = sum(
        1 for t in tables for z in zpreds
        if laws(t, z) and all(
            (not zrel(t, z, x, y)) == ((not x) and y)
            for x in pts for y in pts))
    _require(oriented == 0,
             "a Bool-valued observer represented the oriented witness")
    return {
        "delta_tables": len(tables),
        "zero_predicates": len(zpreds),
        "diag_zero_pairs": diag_pairs,
        "observer_law_pairs": law_pairs,
        "witnessed_kernel_quadruples": kernel_quads,
        "oriented_complement_observers": oriented,
    }


def enum_settings_kernels() -> dict[str, Json]:
    """E2 (candidate A versus kernels, plus Bell counts): carriers
    1..3, all relations, all endpoint pairs; A-settings biject with
    witnessed exact-apartness kernels; representable relations are
    counted by the Bell numbers; decidable cotransitivity collapses to
    complement-transitivity."""
    bell = [1, 2, 5]
    a_counts: list[int] = []
    kernel_counts: list[int] = []
    repr_counts: list[int] = []
    witnessed_counts: list[int] = []
    rel_counts: list[int] = []
    for n in (1, 2, 3):
        pts = list(range(n))
        rels = list(product((False, True), repeat=n * n))
        rel_counts.append(len(rels))

        def r_at(r: tuple[bool, ...], i: int, j: int) -> bool:
            return r[i * n + j]

        def irrefl(r: tuple[bool, ...]) -> bool:
            return all(not r_at(r, i, i) for i in pts)

        a_counts.append(sum(
            1 for r in rels for a in pts for b in pts
            if irrefl(r) and r_at(r, a, b)))
        # kernel side, computed over value tables with Zero = (== 0)
        vtables = list(product((0, 1), repeat=n * n))
        kernel_counts.append(sum(
            1 for t in vtables for a in pts for b in pts
            if all(t[i * n + i] == 0 for i in pts)
            and t[a * n + b] != 0))

        def symm_comp(r: tuple[bool, ...]) -> bool:
            return all(not r_at(r, j, i)
                       for i in pts for j in pts
                       if not r_at(r, i, j))

        def trans_comp(r: tuple[bool, ...]) -> bool:
            return all(not r_at(r, i, k)
                       for i in pts for j in pts for k in pts
                       if not r_at(r, i, j) and not r_at(r, j, k))

        def representable(r: tuple[bool, ...]) -> bool:
            return irrefl(r) and symm_comp(r) and trans_comp(r)

        repr_counts.append(sum(1 for r in rels if representable(r)))
        wa, wb = 0, (1 if n > 1 else 0)
        witnessed_counts.append(sum(
            1 for r in rels if representable(r) and r_at(r, wa, wb)))

        def cotrans(r: tuple[bool, ...]) -> bool:
            return all(
                r_at(r, i, k) or r_at(r, k, j)
                for i in pts for j in pts for k in pts
                if r_at(r, i, j))

        _require(all(cotrans(r) == trans_comp(r) for r in rels),
                 f"cotransitivity vs complement-transitivity, n={n}")
    _require(kernel_counts == a_counts,
             "A-setting count differs from witnessed-kernel count")
    _require(kernel_counts[0] == 0, "a kernel lived on one point")
    _require(repr_counts == bell,
             "representable relations are not the Bell numbers")
    _require(witnessed_counts == [0, 1, 3],
             "witnessed representable counts moved")
    return {
        "carriers": [1, 2, 3],
        "relation_counts": rel_counts,
        "a_setting_counts": a_counts,
        "witnessed_kernel_counts_matching": kernel_counts,
        "representable_relation_counts": repr_counts,
        "bell_numbers": bell,
        "witnessed_representable_counts": witnessed_counts,
        "cotrans_equals_complement_transitivity": True,
    }


def enum_descent_dictionary() -> dict[str, Json]:
    """E3 (the H4 dictionary): on the three-point carrier with
    two-valued views, descent-existence, class-constancy, and
    fiber-constancy over the full represented domain agree on all 64
    combinations; at the fixed domain [0] the native notion is
    strictly weaker."""
    maps = list(product((0, 1), repeat=3))
    fmaps = list(product((0, 1), repeat=2))
    descend = 0
    diverge = 0
    for p in maps:
        for q in maps:
            cc = all(q[x] == q[y]
                     for x in range(3) for y in range(3)
                     if p[x] == p[y])
            ex = any(all(f[p[x]] == q[x] for x in range(3))
                     for f in fmaps)
            fc_full = all(q[x] == q[y]
                          for x in [0, 1, 2] for y in [0, 1, 2]
                          if p[x] == p[y])
            _require(cc == ex and ex == fc_full,
                     "descent/class-constant/fiber-constant diverged")
            fc_zero = all(q[x] == q[y]
                          for x in [0] for y in [0] if p[x] == p[y])
            if cc:
                descend += 1
            if fc_zero and not cc:
                diverge += 1
    _require(diverge > 0, "no fixed-domain divergence witnessed")
    return {
        "combinations": len(maps) * len(maps),
        "descend_count": descend,
        "fixed_domain_divergence_count": diverge,
    }


def enum_flagship_census() -> dict[str, Json]:
    """E4 (flagship census): triples (view kernel, compatible first
    observable, incompatible second observable) exist in quantity."""
    maps = list(product((0, 1), repeat=3))
    count = 0
    for p in maps:
        for phi in maps:
            cc_phi = all(phi[x] == phi[y]
                         for x in range(3) for y in range(3)
                         if p[x] == p[y])
            if not cc_phi:
                continue
            for psi in maps:
                cc_psi = all(psi[x] == psi[y]
                             for x in range(3) for y in range(3)
                             if p[x] == p[y])
                if not cc_psi:
                    count += 1
    _require(count > 0, "no flagship triple exists")
    return {"triples": count}


def enum_value_fork() -> dict[str, Json]:
    """E5 (value fork): on the two-point carrier with a three-element
    value type, the oriented apartness class contains at least two
    distinct difference presentations."""
    tables = list(product((0, 1, 2), repeat=4))
    oriented = [
        t for t in tables
        if t[0] == 0 and t[3] == 0 and t[1] != 0 and t[2] == 0]
    _require(len(oriented) >= 2,
             "value fork collapsed to one presentation")
    return {
        "value_type_size": 3,
        "tables": len(tables),
        "oriented_class_presentations": len(oriented),
    }


def contact_report(repo_root: Path) -> dict[str, Json]:
    contact_dir = repo_root / "contact" / "omega_primdiff"
    manifest = contact_dir / "CONTACT_MANIFEST.json"
    analysis = (repo_root / "contact" / "analysis"
                / "contact_countermodels.json")
    present = contact_dir.exists()
    if not present:
        status = STATUS_ABSENT
    elif analysis.exists():
        status = STATUS_PROCESSED
    else:
        status = STATUS_UNPROCESSED
    manifest_sha: Json = None
    external_sha: Json = None
    if manifest.exists():
        raw = manifest.read_bytes().replace(b"\r\n", b"\n")
        manifest_sha = hashlib.sha256(raw).hexdigest()
        parsed = json.loads(raw.decode("utf-8"))
        files = parsed["files"]
        external_sha = str(files[0]["sha256"])
    return {
        "protocol": {
            "package_path": "contact/omega_primdiff/",
            "read_order": [
                "lean4/ only after the native characterization "
                "commit (Phase II)",
                "prose/ only after the Lean-only comparison commit "
                "(Phase III)",
            ],
            "manifest_required": "contact/omega_primdiff/"
                                 "CONTACT_MANIFEST.json",
            "absence_rule": "complete the native phases and terminate "
                            "with CONTACT_INPUT_ABSENT; do not invent "
                            "contents",
        },
        "package_present": present,
        "manifest_present": manifest.exists(),
        "status": status,
        "history": list(STATUS_HISTORY),
        "manifest_sha256": manifest_sha,
        "external_file_sha256_per_manifest": external_sha,
        "prose_status": "PROSE_INPUT_ABSENT",
        "native_kernel_interface": {
            "kernel": "PDA_pointed_witnessed_irreflexive",
            "lean_binding": "PrimitiveContact.NativeKernel",
            "witness": "PrimitiveContact.nativeKernelWitness",
            "universal_status":
                "PrimitiveCats.d2_initial (initial among all pointed "
                "witnessed relations)",
            "orientation_fork": [
                "PrimitiveCats.s2_initial_sym",
                "PrimitiveCats.s2_not_weakly_initial",
                "both branches retained",
            ],
            "observer_branching": "PrimitiveCats.no_terminal_pres",
            "implication_matrix":
                "artifacts/primitive_implication_matrix.json "
                "(72 cells, PrimitiveCore.matrixCells)",
        },
        "verdict": {
            "primary": VERDICT_PRIMARY,
            "terminals": [
                {"code": VERDICT_PRIMARY,
                 "scope": SCOPE_INCOMPARABLE},
                {"code": "COMMON_PRIMITIVE_KERNEL_REPLACES_BOTH",
                 "scope": SCOPE_KERNEL},
                {"code": "CONTACT_EQUIVALENT_UNDER_DECIDABLE_ZERO_"
                         "PLUS_APARTNESS_ADMISSIONS",
                 "scope": SCOPE_EQUIVALENT},
            ],
            "carried_unchanged": [
                "NATIVE_PRIMITIVE_DIFFERENCE_CHARACTERIZED",
                "PRIMITIVE_DIFFERENCE_PASSAGE_COMPOSED",
                "TWO_RULE_SCHEMA_PROVED_UNDER_DECLARED_RESPONSE_"
                "UNIVERSE_AND_WF_PROTECTED_PAIR",
            ],
            "not_issued": [
                {"code": "CONTACT_STRICTLY_STRONGER",
                 "reason": "refuted by the native->supplied "
                           "countermodels of the primary bundle"},
                {"code": "NATIVE_STRICTLY_STRONGER",
                 "reason": "as a sealed-corpus claim it would launder "
                           "this run's reconstruction into the sealed "
                           "record - the sealed corpus lacks the "
                           "global quotient-descent layer; recorded "
                           "instead: every supplied abstract-half "
                           "theorem now has a native counterpart "
                           "(ObsDescent) while the converse direction "
                           "retains countermodels; the supplied "
                           "physics-labeled tail adds no content "
                           "beyond five native one-line lemmas"},
                {"code": "CONTACT_INPUT_ABSENT",
                 "reason": "superseded; preserved as sealed history "
                           "(history[0])"},
            ],
            "frontier_conjecture":
                "post-reconstruction, the enlarged native corpus "
                "strictly contains the reconstructed image of the "
                "supplied abstract half while the converse "
                "containment remains signature-impossible; any future "
                "strictly-stronger verdict must be stated relative to "
                "the enlarged corpus",
            "kernel": {
                "structure": "ContactKernel.WitnessedDiff",
                "gateway": "ContactKernel.kernel_gateway_unique "
                           "(inherited from PrimitiveCats.d2_initial)",
                "no_terminal_collector":
                    "ContactKernel.kernel_no_terminal_collector "
                    "(morphism grade: PrimitiveCats.Hom of the "
                    "induced apartObj presentations, value data "
                    "discarded; no terminality claim at VHom grade)",
                "value_rigidity":
                    "ContactKernel.vhom_unique_of_onto (sufficiency "
                    "under delta-surjectivity) with "
                    "ContactKernel.vhom_not_unique (one non-onto "
                    "countermodel); no equivalence proved",
                "observer_side_identity":
                    "ContactKernel.toDiffObs with toDiffObs_fields "
                    "and toDiffObs_apart (record identity: kernel + "
                    "the two law declarations = the observer record; "
                    "DEFINITION, not a derivation)",
                "realized_from_native":
                    "ContactKernel.ofSetting (exact under Decidable: "
                    "ofSetting_exact; open_kernel_grade otherwise)",
                "realized_from_supplied_shape":
                    "ContactKernel.ofDiffObs (chosen non-zero pair; "
                    "ContactKernel.pair_choice_load_bearing)",
                "meets_interface": "ContactKernel.toNativeKernel",
            },
        },
        "collision_cells": [list(row) for row in COLLISION_CELLS],
        "enumerations": {
            "E1_bool_observers": enum_bool_observers(),
            "E2_settings_kernels": enum_settings_kernels(),
            "E3_descent_dictionary": enum_descent_dictionary(),
            "E4_flagship_census": enum_flagship_census(),
            "E5_value_fork": enum_value_fork(),
            "bounds": {
                "carrier_max": 3,
                "bool_delta_tables": 16,
                "relation_counts": [2, 16, 512],
                "descent_combinations": 64,
                "flagship_triples_universe": 512,
                "value_fork_tables": 81,
            },
        },
    }


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path,
                        default=Path("artifacts"))
    args = parser.parse_args(argv)
    repo_root = Path(__file__).resolve().parent.parent
    payload = contact_report(repo_root)
    out_path = args.artifacts / "primitive_contact.json"
    write_json(out_path, payload)
    print(f"contact status: {payload['status']}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
