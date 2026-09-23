"""Explicitly reviewed scope, maps, stages and open obligations. AuthorityEffect: None."""
from __future__ import annotations

import json
from typing import Any

from eg_graph import reviewed_claim, theorem_scope_digest
from eg_sources import HERE, Snapshot, canonical, digest, read_object


def apply_reviews(snapshot: Snapshot, groups: dict[str, list[dict[str, Any]]]) -> None:
    reviews = read_object(HERE / "scope_reviews.json")
    if reviews["source_snapshot"] != snapshot.snapshot:
        raise ValueError("REVIEW_SOURCE_CHANGED")
    theorems = {t["id"]: t for t in groups["theorem"]}
    for review in reviews["reviews"]:
        snapshot.resolve(review["source"])
        expected = review["theorem_scope_digests"]
        if any(key not in theorems for key in expected):
            raise ValueError("REVIEW_THEOREM_MISSING: " + review["id"])
        if expected != {key: theorem_scope_digest(theorems[key]) for key in expected}:
            raise ValueError("REVIEW_THEOREM_SCOPE_CHANGED: " + review["id"])
        existing = next((row for row in groups["claim"] if row["id"] == review["id"]), None)
        if existing is not None and existing["statement"] != review["source"]:
            raise ValueError("REVIEW_STATEMENT_CHANGED: " + review["id"])
        if existing:
            groups["claim"].remove(existing)
        claim = reviewed_claim(snapshot, groups, identifier=review["id"], text=review["scope_statement"],
            source=review["source"], evidence=list(expected), lineage=review["lineage"],
            parents=review["parent_bridge_ids"], public_id=review["public_id"])
        if existing:
            claim["statement"] = existing["statement"]
        for headline in groups["headline"]:
            if headline["source"] != review["source"] or not existing:
                continue
            headline.update(scope_verdict="MATCHED", scope_evidence_ids=list(expected), gap=None,
                review={"scope_statement": review["scope_statement"], "theorem_scope_digests": expected,
                        "computation_scope_digests": {}, "source_span_sha256": review["source"]["span_sha256"]})


def bridges(snapshot: Snapshot, groups: dict[str, list[dict[str, Any]]]) -> None:
    def native(name: str) -> str:
        return "theorem:lean4::" + name

    erasure = snapshot.reference("lean4/Derivation/Erasure.lean")
    trace = snapshot.reference("lean4/Derivation/TraceAlgebra.lean", 355, 409)
    groups["bridge"].extend([
        {"id": "bridge:token_erasure", "source": erasure,
         "source_carrier": "Derivation.TRegime", "target_carrier": "Derivation.Regime",
         "source_steps": "Derivation.stepT", "target_steps": "Derivation.stepE",
         "supported_domain": "All Lean token-aware regimes and events; Python source is outside this theorem's endpoints.",
         "state_maps": ["Derivation.TRegime.erase"], "event_maps": ["Derivation.eraseEvent, dependent on the pre-state", "Derivation.eraseHistory"],
         "observation_maps": ["State erasure; observational transport requires the separate RegimeExt family."],
         "direction": "forward simulation; no inverse asserted",
         "identity_composition": "Empty histories erase to empty histories; the recursively state-dependent history map satisfies erase_replay. An arbitrary state-independent event map is not claimed.",
         "refusal_guard": "Option.map transports failure and success exactly in erase_step and erase_replay; duplicate datum admission erases to supply.",
         "proof_ids": [native("Derivation.erase_step"), native("Derivation.erase_replay")], "countermodel_ids": [], "gap": None},
        {"id": "bridge:typed_trace_erasure", "source": trace,
         "source_carrier": "TraceAlgebra.TRecord and lists with LegalTrace s tr", "target_carrier": "PrimitivePassage.PState and List PEvent",
         "source_steps": "WFRecord and Aligned bind each record's pre/event/post", "target_steps": "PrimitivePassage.step and replayP",
         "supported_domain": "Aligned traces; LegalTrace additionally includes every well-formed record's guard, effect, delta and profile requirements.",
         "state_maps": ["identity on PState; endState follows the recorded post-states"], "event_maps": ["eraseTrace maps every record to its ev field"],
         "observation_maps": ["WFRecord checks the computed profile; replay equality is equality of full PState"],
         "direction": "typed records to existing native event replay",
         "identity_composition": "The map is List.map on ev: empty lists and concatenation use its list laws. No quotient-completeness or automatic event selection is asserted.",
         "refusal_guard": "LegalTrace includes WFRecord; target step retains its actual refusal and halt semantics. Aligned alone suffices for the narrower replay theorem.",
         "proof_ids": [native("TraceAlgebra.replay_erases"), native("TraceAlgebra.legal_trace_replays")], "countermodel_ids": [], "gap": None},
    ])
    open_rows = [
        ("tower_native", "research/primitive_difference_tower/STATUS.md", "DiffInterface.Stage", "declared finite tower fixture",
         "No source-to-fixture map derives the seed carrier, anchor, naming convention, successor grammar or schedule. The unbounded native successor remains open."),
        ("represented_readback", "research/represented_execution/CLAIMS.md", "Translation.FiniteSetting", "encoded graph and Execution.Config",
         "The lookup and word execution theorems are scoped evidence. A reverse translation for arbitrary represented state, every refusal and every native event is not established by them."),
        ("cells_native", "research/g013_trace_calculus/lean/HigherCell.lean", "G013TraceCalculus.Step and Cell2", "guarded PrimitivePassage steps",
         "No state/event map from this declared cell grammar into native guarded steps is supplied; constructor-level cells do not provide that bridge."),
        ("pipeline_carrier", "research/x310_vertical_integration/CLAIMS.md", "SubstrateState", "the six sibling entry points",
         "The codec and synthetic glue have narrower carriers; the full state, every stage and all protection metadata are not connected by one proved commuting map."),
    ]
    for name, path, src, dst, gap in open_rows:
        groups["bridge"].append({"id": "bridge:" + name, "source": snapshot.reference(path),
            "source_carrier": src, "target_carrier": dst, "source_steps": None, "target_steps": None,
            "supported_domain": None, "state_maps": [], "event_maps": [], "observation_maps": [],
            "direction": None, "identity_composition": None, "refusal_guard": None, "proof_ids": [], "countermodel_ids": [], "gap": gap})
    census_path = "artifacts/completion_dependency_graph.json"
    census = json.loads(snapshot.text(census_path))["graph"]
    available = {row["declaration"]: row["id"] for row in groups["theorem"] if row["id"].startswith("theorem:lean4::")}
    if not census["bridges"] or len(census["bridges"]) != sum(census["statuses"].values()):
        raise ValueError("NATIVE_BRIDGE_SOURCE_POPULATION")
    for declared in census["bridges"]:
        key = "bridge:source_census:" + digest(canonical({k: declared[k] for k in ("source", "relation", "target")}))[:20]
        groups["bridge"].append({"id": key, "source": {"source": snapshot.reference(census_path),
            "declared_relation": declared["relation"], "declared_status": declared["status"],
            "declared_boundary": declared["boundary"], "declared_evidence": declared["evidence"]},
            "source_carrier": declared["source"], "target_carrier": declared["target"],
            "source_steps": None, "target_steps": None, "supported_domain": declared["boundary"],
            "state_maps": [], "event_maps": [], "observation_maps": [], "direction": declared["relation"],
            "identity_composition": None, "refusal_guard": None,
            "proof_ids": [available[name] for name in declared["evidence"] if name in available], "countermodel_ids": [],
            "gap": "This is a row of the declared notion/bridge census, not automatically a transition-map contract. Source status is preserved separately; same-scope semantic review and any actual maps remain required."})


def finite_fixture(snapshot: Snapshot, groups: dict[str, list[dict[str, Any]]]) -> None:
    path = "research/primitive_difference_tower/receipts/finite_tower_0_15.json"
    data = json.loads(snapshot.text(path))
    verifier = next(row for row in groups["replay"] if row["tree"] == "primitive_difference_tower" and row["command"][:2] == ["python", "verify_manifest.py"])
    scope = {"horizon": data["horizon"], "stage_min": 0, "stage_max": 15, "initial_carrier": [0, 1],
             "negative_carrier": data["negative_fixture"]["witness"]["carrier"], "pair_orbit_size": 2,
             "candidate_rows": len(data["candidate_grammar"])}
    gap = verifier["gap"] if verifier["result"] != "PASSED" else None
    computation = {"id": "computation:tower_0_15", "source": snapshot.reference("research/primitive_difference_tower/finite_tower.py"),
        "entrypoint": "finite_tower.render_report(15)", "grammar": {"admissions": data["admissions"], "candidates": data["candidate_grammar"]},
        "bounds": scope, "arithmetic": "Exact integers, finite labelled sets and tuples; no approximate numerical inputs.",
        "receipt_sources": [snapshot.reference(path)], "replay_command": verifier["command"], "replay_receipt": verifier["id"],
        "frontier_status": "Complete for the emitted stages and displayed two-choice orbit; native and unbounded continuation remain open.", "gap": gap}
    groups["computation"].append(computation)
    identifier = "claim:scoped:tower_0_15"
    groups["claim"].append({"id": identifier, "public_id": None,
        "statement": {"source": snapshot.reference(path), "text": "Every emitted stage from 0 through 15 replays, retains old edges, and satisfies the six reported checks after the eight explicitly listed admissions."},
        "source_class": "deterministic computation", "status": "VERIFIED_FINITE" if gap is None else "OPEN",
        "lineage": "parallel_construction", "bounds": scope, "assumption_ids": [], "parent_bridge_ids": [],
        "evidence_ids": [computation["id"]], "gap": gap})
    for index, admission in enumerate(data["admissions"]):
        key = f"assumption:tower_input:{index}"
        groups["assumption"].append({"id": key, "statement": {"source": snapshot.reference(path), "text": admission},
                                    "source_class": "supplied object-language datum", "gap": None})
        groups["claim"][-1]["assumption_ids"].append(key)
    claim_id, model_id = "claim:scoped:swap_stable_pair", "countermodel:two_pair_swap"
    groups["claim"].append({"id": claim_id, "public_id": None,
        "statement": {"source": snapshot.reference(path), "text": "The displayed orbit of two disjoint pairs admits a singleton selection fixed by the displayed swap."},
        "source_class": "refuted claim", "status": "REFUTED" if gap is None else "OPEN", "lineage": "parallel_construction",
        "bounds": scope, "assumption_ids": [], "parent_bridge_ids": [], "evidence_ids": [model_id], "gap": gap})
    retained = []
    for field in ("carrier", "pair_orbit", "permutation"):
        key = "assumption:swap_fixture:" + field
        retained.append(key)
        groups["assumption"].append({"id": key, "statement": {"source": snapshot.reference(path), "text": {field: data["negative_fixture"]["witness"][field]}},
                                    "source_class": "supplied object-language datum", "gap": None})
    groups["claim"][-1]["assumption_ids"] = retained
    groups["countermodel"].append({"id": model_id, "source": snapshot.reference(path), "negated_claim_id": claim_id,
        "retained_assumptions": retained,
        "removed_assumption": "No distinguished pair or supplied anchor is allowed to break the displayed swap.",
        "witness": data["negative_fixture"]["witness"], "checker": "finite_tower.symmetric_single_pair_failure through verify_manifest.py",
        "replay_receipt": verifier["id"], "gap": gap})
    groups["edge"].append({"id": "edge:swap_refutation", "kind": "refuted-by", "from": claim_id, "to": model_id,
                            "source": snapshot.reference(path), "gap": None})


STAGES = [
    (0, "prompt/seed_prompt.md", "Opaque inscription is supplied. Its visible glyphs supply no order, pair, boundary, equality or successor structure.", ["claim:scoped:supply_no_op"]),
    (1, "lean4/Derivation/Basic.lean", "Regime fields, event grammar and replay are declarations. Their supply no-op theorem does not derive those declarations from the seed.", ["claim:scoped:supply_no_op", "claim:scoped:token_erasure"]),
    (2, "code/derivation/observe.py", "Contexts and profiles define the stated observation. Candidate grammar, cost orders and demand policies are separate supplied choices.", []),
    (3, "paper/paper_claim_ledger.md", "Item-count minimum and tied classes stay distinct from refined-cost class uniqueness. Neither reading chooses a concrete successor.", ["claim:paper/paper_claim_ledger.md::CL-3-COST1-IMPOSSIBLE"]),
    (4, "lean4/Derivation/DiffInterface.lean", "Witness, irreflexivity, valued difference and orientation are separate interfaces. DiffObs supplies carriers, delta, Zero and each of zero_refl, zero_symm and zero_trans; packaging them does not derive them.", ["claim:scoped:zero_relation"]),
    (5, "lean4/Derivation/PrimitivePassage.lean", "Occurrence, assertion, witness, protection, observer, budget, license, refusal and halt are actual state fields with actual guards. The one-open-edge count belongs only to the declared completion graph.", []),
    (6, "lean4/Derivation/TraceAlgebra.lean", "Typed replay, conditional frames, the two-rule rewrite, cancellation and supplied translations are composites with hypotheses. They imply neither an autonomous event source nor an additional flow.", ["claim:scoped:aligned_replay", "claim:scoped:legal_replay", "claim:scoped:rewrite_sound"]),
]

FRONTIERS = [
    ("second_3", "research/second/SEED.md", "Challenge 3 engine", "Declare engine state and demand sources; retain all minimum ties and refusal outcomes."),
    ("second_4", "research/second/SEED.md", "Challenge 4 forward run", "Run the declared engine under explicit bounds and report every surviving process and terminal."),
    ("second_5", "research/second/SEED.md", "Challenge 5 definability census", "Separate each stage's definitions, realizations, supplied capabilities and forced conclusions."),
    ("demand_channel", "research/endogenous_demand/CLAIMS.md", "Demand and instance channels", "The reqs result is scoped to C_reqs; inspect the distinct instance grammar and its declared InClass/I1Class boundary."),
    ("instance_channel", "research/instance_demand/CLAIMS.md", "Represented instance generation", "Provide a native demand bridge beyond the represented classes before claiming the open general obligation is closed."),
    ("tower_native", "research/primitive_difference_tower/STATUS.md", "Native tower bridge", "Map arbitrary native stages into the admitted fixture without concealing anchor, carrier, naming, grammar or schedule inputs."),
    ("tower_unbounded", "research/primitive_difference_tower/STATUS.md", "Unbounded endogenous successor", "A finite horizon and a universally quantified counter schema do not supply an unbounded native successor source."),
    ("represented_readback", "research/represented_execution/CLAIMS.md", "Represented execution and read-back", "State precisely which finite carriers and words the encode/lookup/run facts cover; construct each additional reverse map and guard law."),
    ("pipeline_carrier", "research/x310_vertical_integration/CLAIMS.md", "Integrated carrier", "Connect every stage on one declared carrier, with full state/protection metadata and actual step commutation."),
    ("driver_b", "research/alpha_engine/STATUS.md", "Driver B", "Provide demand generation and the missing driver without converting proposal, evaluation or uniqueness into a license."),
    ("analytic_limit", "research/endogenous_continuum/CLAIMS.md", "Analytic limit", "Finite carriers, finite covers and checked potentials need a separate analytic construction and limit theorem."),
]


def stage_frontier_rows(snapshot: Snapshot, groups: dict[str, list[dict[str, Any]]]) -> None:
    for number, path, boundary, claim_ids in STAGES:
        groups["stage"].append({"id": f"stage:{number}", "stage": number, "source": snapshot.reference(path),
            "claim_ids": list(claim_ids), "boundary": boundary, "gap": None})
    core = "claim:paper/paper_claim_ledger.md::"
    by_stage = {row["stage"]: row for row in groups["stage"]}
    by_stage[0]["claim_ids"] += [core + "CL-0-INERTIA"]
    by_stage[3]["claim_ids"] += [core + name for name in ("CL-3-MIN-TWO", "CL-3-NONUNIQUE-MU1", "CL-3-TIE-CLASSES", "CL-3-INFINITE-TIES", "CL-3-UNIQUE-MU2-L", "CL-3-UNIQUE-MU2-F")]
    by_stage[5]["claim_ids"] += [core + "CL-PD2-PASSAGE"]
    by_stage[6]["claim_ids"] += [core + name for name in ("CL-PD2-BOUNDARY-CANCELLATION", "CL-FIDELITY-DESCENT", "CL-TOKEN-ERASURE", "CL-PD2-TRACE-ALGEBRA")]
    # Law-bearing structure fields are supplied separately, even when they are
    # packaged in one non-propositional binder in the compiled theorem type.
    zero = next(row for row in groups["claim"] if row["id"] == "claim:scoped:zero_relation")
    for name, start, stop in (("carriers", 33, 33), ("delta", 34, 34), ("Zero", 35, 35),
                             ("zero_refl", 36, 36), ("zero_symm", 37, 37), ("zero_trans", 38, 39)):
        key = "assumption:zero_interface:" + name
        source = snapshot.reference("lean4/Derivation/DiffInterface.lean", start, stop)
        groups["assumption"].append({"id": key, "statement": source, "source_class": "supplied object-language datum", "gap": None})
        zero["assumption_ids"].append(key)
        groups["edge"].append({"id": "edge:" + key, "kind": "uses-assumption", "from": zero["id"], "to": key, "source": source, "gap": None})
    for name, path, disposition, requirement in FRONTIERS:
        candidates = [row["id"] for row in groups["claim"] if row["statement"].get("path") == path]
        groups["frontier"].append({"id": "frontier:" + name, "source": snapshot.reference(path), "claim_ids": candidates,
            "disposition": "OPEN: " + disposition, "required_evidence": requirement, "gap": requirement})
    precedents = [
        ("additive_cost", "research/g013_trace_calculus/lean/Price.lean", "Exact trace-price addition; branch-price equality is an explicit premise of its invariance result."),
        ("budget_accounting", "lean4/Derivation/PrimitivePassage.lean", "Represented exact budget fields and guards; no charge generated by a symmetry action follows."),
        ("signed_boundary", "lean4/Derivation/BoundaryCancellation.lean", "Signed deletion coefficients and cancellation for the declared finite-list grammar; scope is the compiled coefficient statement."),
        ("finite_form_matrices", "research/p209b_clifford_symplectic/lean/CliffordSymplectic.lean", "Six explicitly displayed two-element-field matrices preserve the declared form; no arbitrary-field result follows."),
        ("path_cost", "research/path_dependent_cost/CLAIM_LEDGER.md", "Abstract exactness implications have supplied action/cost hypotheses; finite route prices have a declared depth-three grammar."),
    ]
    for name, path, scope in precedents:
        groups["frontier"].append({"id": "precedent:" + name, "source": snapshot.reference(path), "claim_ids": [],
            "disposition": "SCOPED_PRECEDENT", "required_evidence": scope,
            "gap": "This precedent does not establish a symmetry-generated conserved quantity for native evolution."})
