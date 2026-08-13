"""Ultra closure run, Phase I: theorem inventory and dependency graph.

Classification: metatheory apparatus for
``paper/native_derivation_completion.md`` and
``paper/native_derivation_map.md``.

The inventory is source-derived, never transcribed: theorem names and
axiom sets come from ``artifacts/lean_axioms.txt``; statements are
extracted from the Lean sources; consuming modules and citing ledger
claims are found by search.  Only the kind/role labels are declared
metadata, and the tests pin them to exactly the exported estate (no
orphan, no phantom).

The dependency graph records every bridge of the final derivation
chain with one of the statuses
``PROVED / DECLARED / COMPUTED_WITHIN_BOUNDS / FALSE_WITH_COUNTERMODEL
/ OPEN`` and evidence references that the tests resolve against the
axioms artifact and the repository.
"""

from __future__ import annotations

import re
from pathlib import Path

LEAN_DIR = Path("lean4") / "Derivation"
AXIOMS_FILE = Path("artifacts") / "lean_axioms.txt"
LEDGER_FILE = Path("paper") / "paper_claim_ledger.md"

DERIVATION_FILES = [
    "Basic.lean", "Inertia.lean", "Quot.lean", "Counting.lean",
    "Minimality.lean", "Progress.lean", "Erasure.lean", "Ext.lean",
]

NAMESPACE_FILES: dict[str, list[str]] = {
    "Derivation": DERIVATION_FILES,
    "PrimDiff": ["PrimDiff.lean"],
    "Bridge": ["Bridge.lean"],
    "Refusal": ["Refusal.lean"],
    "RefusalFrontier": ["RefusalFrontier.lean"],
    "Generator": ["Generator.lean"],
    "DiffInterface": ["DiffInterface.lean"],
    "Represented": ["Represented.lean"],
    "Completion": ["Completion.lean"],
    "NoOutside": ["NoOutside.lean"],
    "Constitution": ["Constitution.lean"],
    "Initiality": ["Initiality.lean"],
    "Horizon": ["Horizon.lean"],
    "PrimitiveCore": ["PrimitiveCore.lean"],
    "PrimitiveCats": ["PrimitiveCats.lean"],
    "PrimitiveContact": ["PrimitiveContact.lean"],
    "PrimitivePassage": ["PrimitivePassage.lean"],
    "HigherStructure": ["HigherStructure.lean"],
    "Apartness": ["Apartness.lean"],
    "InterpreterBoundary": ["InterpreterBoundary.lean"],
    "ControllerCategory": ["ControllerCategory.lean"],
}

VALID_KINDS = ("concrete", "generic", "bounded", "horizon-free")
VALID_ROLES = (
    "existence", "uniqueness", "minimality", "preservation",
    "termination", "example", "countermodel", "equivalence",
    "classification", "simulation",
)


def parse_axiom_reports() -> list[dict[str, object]]:
    """One record per exported theorem: qualified name and axiom set."""
    out: list[dict[str, object]] = []
    text = AXIOMS_FILE.read_text(encoding="utf-8")
    for line in text.splitlines():
        m = re.search(r"'(?P<name>[^']+)' (?P<rest>.*)", line)
        if not m:
            continue
        name = m.group("name")
        rest = m.group("rest")
        if "does not depend" in rest:
            axioms: list[str] = []
        else:
            inner = re.search(r"\[(.*)\]", rest)
            axioms = (
                [a.strip() for a in inner.group(1).split(",")]
                if inner and inner.group(1) else []
            )
        out.append({"name": name, "axioms": axioms})
    return out


def source_module(qualified: str) -> str:
    """The Lean file that declares the theorem (searched, not guessed)."""
    ns, _, bare = qualified.rpartition(".")
    for fname in NAMESPACE_FILES.get(ns, []):
        path = LEAN_DIR / fname
        if not path.exists():
            continue
        if re.search(
            rf"^theorem {re.escape(bare)}[\s({{\[⟨]",
            path.read_text(encoding="utf-8"),
            re.MULTILINE,
        ):
            return fname
    return "UNRESOLVED"


def extract_statement(qualified: str, module: str) -> str:
    """The statement text from the source, up to the proof marker."""
    bare = qualified.rpartition(".")[2]
    path = LEAN_DIR / module
    if not path.exists():
        return "UNRESOLVED"
    text = path.read_text(encoding="utf-8")
    m = re.search(
        rf"^theorem {re.escape(bare)}(?P<sig>.*?):=",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not m:
        return "UNRESOLVED"
    return re.sub(r"\s+", " ", m.group("sig")).strip()


def consuming_modules(qualified: str, own_module: str) -> list[str]:
    """Every other module whose source mentions the theorem."""
    bare = qualified.rpartition(".")[2]
    out = []
    for path in sorted(LEAN_DIR.glob("*.lean")):
        if path.name == own_module:
            continue
        if re.search(rf"\b{re.escape(bare)}\b",
                     path.read_text(encoding="utf-8")):
            out.append(path.name)
    return out


def citing_claims(qualified: str) -> list[str]:
    """Ledger claim IDs whose block mentions the bare theorem name."""
    bare = qualified.rpartition(".")[2]
    text = LEDGER_FILE.read_text(encoding="utf-8")
    blocks = re.split(r"^### ", text, flags=re.MULTILINE)
    out = []
    for block in blocks[1:]:
        claim_id = block.splitlines()[0].strip()
        if re.search(rf"\b{re.escape(bare)}\b", block):
            out.append(claim_id)
    return out


# --------------------------------------------------------------------------
# Declared kind/role metadata.  Defaults per namespace; overrides where a
# theorem departs from its module's typical shape.  The tests pin exact
# coverage of the exported estate.
# --------------------------------------------------------------------------

NAMESPACE_DEFAULTS: dict[str, tuple[str, str]] = {
    "Derivation": ("generic", "preservation"),
    "PrimDiff": ("generic", "classification"),
    "Bridge": ("generic", "classification"),
    "Refusal": ("concrete", "equivalence"),
    "RefusalFrontier": ("generic", "classification"),
    "Generator": ("horizon-free", "classification"),
    "DiffInterface": ("generic", "preservation"),
    "Represented": ("generic", "preservation"),
    "Completion": ("generic", "preservation"),
    "NoOutside": ("generic", "preservation"),
    "Constitution": ("generic", "simulation"),
    "Initiality": ("bounded", "minimality"),
}

KIND_ROLE_OVERRIDES: dict[str, tuple[str, str]] = {
    # genesis / inertia / erasure
    "Derivation.supply_no_op": ("generic", "preservation"),
    "Derivation.genesis_underivable": ("concrete", "countermodel"),
    "Derivation.underivable_of_empty": ("generic", "countermodel"),
    "Derivation.collapsed_of_no_insts": ("generic", "classification"),
    "Derivation.R2L_collapsed": ("concrete", "classification"),
    "Derivation.R2F_collapsed": ("concrete", "classification"),
    "Derivation.historyL_replays": ("concrete", "example"),
    "Derivation.historyF_replays": ("concrete", "example"),
    "Derivation.admission_without_expressive_increase":
        ("concrete", "countermodel"),
    "Derivation.separable_not_collapsed": ("generic", "classification"),
    "Derivation.quotient_barrier": ("generic", "classification"),
    "Derivation.quot_barrier": ("generic", "classification"),
    "Derivation.barrier_R2L": ("concrete", "classification"),
    "Derivation.index_le_strict_mono": ("generic", "termination"),
    "Derivation.strict_bounded_length": ("generic", "termination"),
    "Derivation.no_supply_round_bound": ("bounded", "termination"),
    "Derivation.allPairs_length": ("generic", "termination"),
    "Derivation.cost1_insufficient_general": ("generic", "minimality"),
    "Derivation.cost1_insufficient": ("concrete", "minimality"),
    "Derivation.cost1_insufficient_F": ("concrete", "minimality"),
    "Derivation.mu1_minimum_not_unique": ("concrete", "uniqueness"),
    "Derivation.mu2_unique": ("bounded", "uniqueness"),
    "Derivation.markK_pairwise_noniso": ("generic", "uniqueness"),
    "Derivation.mark_progress": ("generic", "existence"),
    "Derivation.erase_step": ("generic", "simulation"),
    "Derivation.erase_replay": ("generic", "simulation"),
    # primitive difference highlights
    "PrimDiff.D2_initial_pointed": ("generic", "uniqueness"),
    "PrimDiff.D2_not_pointed_iso_S2": ("concrete", "uniqueness"),
    "PrimDiff.bool_irrefl_witness_classification":
        ("concrete", "classification"),
    "PrimDiff.symmetric_no_equivariant_classifier":
        ("concrete", "countermodel"),
    "PrimDiff.collapse_unobstructed_without_fidelity":
        ("generic", "countermodel"),
    "PrimDiff.witnessed_irrefl_on_every_larger_carrier":
        ("generic", "existence"),
    # bridge provenance
    "Bridge.second_token_required": ("generic", "countermodel"),
    "Bridge.irrefl_law_not_entailed": ("generic", "countermodel"),
    "Bridge.single_token_carrier_bound": ("horizon-free", "termination"),
    # refusal frontier highlights
    "RefusalFrontier.silent_repetition_inert":
        ("horizon-free", "preservation"),
    "RefusalFrontier.judgment_carrier_bound":
        ("horizon-free", "preservation"),
    "RefusalFrontier.equivariant_output_invariant":
        ("generic", "preservation"),
    "RefusalFrontier.reflective_chain_growth":
        ("horizon-free", "existence"),
    "RefusalFrontier.reflective_chain_is_initial_segment":
        ("horizon-free", "classification"),
    "RefusalFrontier.reflective_chain_successor_relation":
        ("horizon-free", "classification"),
    "RefusalFrontier.reflective_chain_irreflexive_facts":
        ("horizon-free", "classification"),
    "RefusalFrontier.min_witnessed_route_closes":
        ("concrete", "minimality"),
    "RefusalFrontier.histories_collapse": ("concrete", "countermodel"),
    # generator highlights
    "Generator.generation_never_dries": ("horizon-free", "existence"),
    "Generator.finite_marks_outrun": ("horizon-free", "countermodel"),
    "Generator.valued_marks_collapse_generation":
        ("horizon-free", "countermodel"),
    "Generator.depth2_separates_near_ends_n4": ("concrete", "example"),
    "Generator.depth2_obstruction_n5": ("concrete", "countermodel"),
    "Generator.middle_swap_not_relation_preserving":
        ("generic", "countermodel"),
    # difference interface highlights
    "DiffInterface.zeroRel_equivalence": ("generic", "equivalence"),
    "DiffInterface.bare_reflection_certifies_active_obstruction":
        ("generic", "existence"),
    "DiffInterface.drive_terminates": ("generic", "termination"),
    "DiffInterface.tower_fuel_terminates": ("generic", "termination"),
    "DiffInterface.bool_view_pigeonhole": ("generic", "countermodel"),
    "DiffInterface.no_bool_view_is_closed": ("generic", "countermodel"),
    "DiffInterface.cm_freshness": ("concrete", "countermodel"),
    "DiffInterface.cm_tagging": ("concrete", "countermodel"),
    "DiffInterface.cm_edge": ("concrete", "countermodel"),
    "DiffInterface.cm_hash": ("concrete", "countermodel"),
    "DiffInterface.cm_repetition": ("concrete", "countermodel"),
    # represented kernel highlights
    "Represented.represented_progress": ("generic", "existence"),
    "Represented.support_determines": ("generic", "preservation"),
    "Represented.worldAt_data": ("horizon-free", "classification"),
    "Represented.productive_run": ("horizon-free", "termination"),
    "Represented.wit_no_infinite": ("generic", "countermodel"),
    "Represented.scheduler_hidden": ("concrete", "countermodel"),
    "Represented.gensym_hidden": ("concrete", "countermodel"),
    "Represented.oracle_hidden": ("concrete", "countermodel"),
    "Represented.incomplete_search_false_alarm":
        ("concrete", "countermodel"),
    "Represented.augmentation_destroys_old_replay":
        ("concrete", "countermodel"),
    "Represented.repetition_not_progress": ("concrete", "countermodel"),
    "Represented.order_sensitivity_splits_equivalents":
        ("concrete", "countermodel"),
    "Represented.cert_not_correspondence": ("concrete", "countermodel"),
    "Represented.cert_panel_relative": ("concrete", "countermodel"),
    "Represented.worldAt_three_quiescent": ("concrete", "example"),
    "Represented.notes_inert": ("concrete", "example"),
}


def classify(qualified: str) -> tuple[str, str]:
    if qualified in KIND_ROLE_OVERRIDES:
        return KIND_ROLE_OVERRIDES[qualified]
    ns = qualified.rpartition(".")[0]
    return NAMESPACE_DEFAULTS.get(ns, ("generic", "preservation"))


def inventory() -> list[dict[str, object]]:
    out = []
    for rec in parse_axiom_reports():
        name = str(rec["name"])
        module = source_module(name)
        kind, role = classify(name)
        out.append(
            {
                "name": name,
                "module": module,
                "statement": extract_statement(name, module),
                "axioms": rec["axioms"],
                "kind": kind,
                "role": role,
                "consumers": consuming_modules(name, module),
                "citing_claims": citing_claims(name),
            }
        )
    return out


# --------------------------------------------------------------------------
# The dependency graph: notion nodes and classified bridges.
# Statuses reflect the state of the estate at the END of this run;
# every evidence reference is resolved by the tests.
# --------------------------------------------------------------------------

NODES = [
    "seed", "supply", "admission", "retention", "two-ness",
    "witnessed relation", "irreflexivity fact", "irreflexivity law",
    "orientation", "observer/difference map", "Zero/ZeroRel",
    "protected requirement", "active obstruction", "response menu",
    "exhaustion certificate", "same-level repair", "extension proposal",
    "extension execution", "replay", "support", "budget", "license",
    "refusal", "terminal", "certification panel", "next-event source",
    "kernel constitution",
]

# Each bridge: source, relation, target, status, evidence (Lean theorem
# names, artifact keys, or DECLARED:<where>), boundary note.
BRIDGES: list[dict[str, object]] = [
    {
        "source": "seed", "relation": "forces successor state",
        "target": "admission", "status": "FALSE_WITH_COUNTERMODEL",
        "evidence": ["Derivation.genesis_underivable",
                     "Derivation.supply_no_op"],
        "boundary": "nothing follows from the seed alone; admission is "
                    "a separate represented event",
    },
    {
        "source": "supply", "relation": "is",
        "target": "admission", "status": "FALSE_WITH_COUNTERMODEL",
        "evidence": ["Derivation.supply_no_op"],
        "boundary": "supply never mutates admitted state",
    },
    {
        "source": "admission", "relation": "changes state via event",
        "target": "retention", "status": "PROVED",
        "evidence": ["Derivation.historyL_replays",
                     "Derivation.historyF_replays"],
        "boundary": "event-indexed, replayable",
    },
    {
        "source": "seed", "relation": "yields",
        "target": "two-ness", "status": "FALSE_WITH_COUNTERMODEL",
        "evidence": ["Bridge.single_token_carrier_bound",
                     "Bridge.second_token_required"],
        "boundary": "one deduplicated token bounds the carrier at one",
    },
    {
        "source": "admission", "relation": "priced routes to",
        "target": "two-ness", "status": "PROVED",
        "evidence": ["RefusalFrontier.min_witnessed_route_closes",
                     "Refusal.reifyUntagged_eq_occurrence"],
        "boundary": "three tied purchases: second token / occurrence / "
                    "reification (order-dependent winners)",
    },
    {
        "source": "two-ness", "relation": "yields",
        "target": "witnessed relation", "status": "FALSE_WITH_COUNTERMODEL",
        "evidence": ["Bridge.no_forms_no_witness"],
        "boundary": "the relation channel is a separate purchase",
    },
    {
        "source": "admission", "relation": "priced relation route to",
        "target": "witnessed relation", "status": "PROVED",
        "evidence": ["RefusalFrontier.min_witnessed_route_closes"],
        "boundary": "unique minimum in the 44-protocol class under both "
                    "declared cost orders",
    },
    {
        "source": "witnessed relation", "relation": "born off-diagonal",
        "target": "irreflexivity fact", "status": "PROVED",
        "evidence": ["RefusalFrontier.reflective_chain_irreflexive_facts"],
        "boundary": "horizon-free on the chain; class-general form is "
                    "bounded computation",
    },
    {
        "source": "irreflexivity fact", "relation": "entails",
        "target": "irreflexivity law", "status": "FALSE_WITH_COUNTERMODEL",
        "evidence": ["Bridge.irrefl_law_not_entailed",
                     "RefusalFrontier.bridge_facts_not_law"],
        "boundary": "the law is always a separate declaration",
    },
    {
        "source": "irreflexivity law", "relation": "declared as",
        "target": "protected requirement", "status": "DECLARED",
        "evidence": ["DECLARED:DiffInterface.Stage.guarded",
                     "DECLARED:Represented.World.reqs"],
        "boundary": "protection is a fidelity commitment, never entailed",
    },
    {
        "source": "two-ness", "relation": "equivariantly yields",
        "target": "orientation", "status": "FALSE_WITH_COUNTERMODEL",
        "evidence": ["PrimDiff.symmetric_no_equivariant_classifier",
                     "RefusalFrontier.equivariant_output_invariant"],
        "boundary": "the invariance ceiling; bypass requires a priced "
                    "asymmetry (tag/relation/position)",
    },
    {
        "source": "admission", "relation": "priced asymmetry yields",
        "target": "orientation", "status": "PROVED",
        "evidence": ["RefusalFrontier.priced_bridge_oriented"],
        "boundary": "orientation cost relocated to the declaration, "
                    "never eliminated",
    },
    {
        "source": "observer/difference map", "relation": "declared with laws",
        "target": "Zero/ZeroRel", "status": "PROVED",
        "evidence": ["DiffInterface.zeroRel_equivalence"],
        "boundary": "equivalence proved before any quotient; kernel "
                    "observers inherit the laws",
    },
    {
        "source": "Zero/ZeroRel", "relation": "with retention+protection is",
        "target": "active obstruction", "status": "PROVED",
        "evidence":
            ["DiffInterface.bare_reflection_certifies_active_obstruction",
             "DiffInterface.no_guard_no_obstruction"],
        "boundary": "conjunction of three separated conditions; every "
                    "proper subset realized without it",
    },
    {
        "source": "protected requirement", "relation": "necessary for",
        "target": "active obstruction", "status": "PROVED",
        "evidence": ["DiffInterface.no_guard_no_obstruction",
                     "PrimDiff.collapse_unobstructed_without_fidelity"],
        "boundary": "no fidelity, no obstruction: collapse alone is "
                    "admissible",
    },
    {
        "source": "active obstruction", "relation": "checked against",
        "target": "response menu", "status": "DECLARED",
        "evidence": ["DECLARED:Represented.responseMenu"],
        "boundary": "the menu is part of the fixed kernel constitution",
    },
    {
        "source": "response menu", "relation": "exhaustive failure gives",
        "target": "exhaustion certificate", "status": "PROVED",
        "evidence": ["Represented.incomplete_search_false_alarm"],
        "boundary": "obstruction requires exhaustive failure by "
                    "definition; truncated search falsely certifies",
    },
    {
        "source": "active obstruction", "relation": "dichotomy (refusal parallel)",
        "target": "same-level repair", "status": "PROVED",
        "evidence": ["Represented.represented_progress",
                     "Completion.rule1_repair_or_extension"],
        "boundary": "repair family nonempty, or certificate + accepted "
                    "augmentation, or recordable refusal; conditional on "
                    "WF and the fixed constitution",
    },
    {
        "source": "exhaustion certificate", "relation": "forces",
        "target": "extension proposal", "status": "PROVED",
        "evidence": ["Represented.represented_progress",
                     "DiffInterface.no_bool_view_is_closed"],
        "boundary": "canonical augmentation accepted; in bounded "
                    "grammars only a proposal is possible",
    },
    {
        "source": "extension proposal", "relation": "executes without authorization",
        "target": "extension execution", "status": "FALSE_WITH_COUNTERMODEL",
        "evidence": ["Represented.progress_needs_license",
                     "Represented.progress_needs_budget"],
        "boundary": "authorization and budget are represented gates; "
                    "proposals never self-execute",
    },
    {
        "source": "same-level repair", "relation": "preserves satisfied",
        "target": "replay", "status": "PROVED",
        "evidence": ["Represented.step_mark_sound",
                     "Represented.aug_preserves_satisfied"],
        "boundary": "positive-satisfaction preservation, not full "
                    "observational conservativity",
    },
    {
        "source": "replay", "relation": "factors through",
        "target": "support", "status": "PROVED",
        "evidence": ["Represented.support_determines",
                     "NoOutside.support_replay"],
        "boundary": "operational-support factorization, extended to "
                    "histories, families, verdicts this run",
    },
    {
        "source": "budget", "relation": "gates",
        "target": "same-level repair", "status": "PROVED",
        "evidence": ["Represented.progress_needs_budget"],
        "boundary": "represented fuel; setBudget is a history event",
    },
    {
        "source": "license", "relation": "gates",
        "target": "extension execution", "status": "PROVED",
        "evidence": ["Represented.progress_needs_license"],
        "boundary": "represented authorization",
    },
    {
        "source": "exhaustion certificate", "relation": "recordable as",
        "target": "refusal", "status": "PROVED",
        "evidence": ["Represented.refusal_needs_certificate",
                     "Represented.refusals_are_represented"],
        "boundary": "refusal only with a verified certificate",
    },
    {
        "source": "refusal", "relation": "terminalizes the run",
        "target": "terminal", "status": "FALSE_WITH_COUNTERMODEL",
        "evidence": ["Completion.refusal_non_absorbing"],
        "boundary": "refusal is a status record, non-absorbing; run "
                    "termination belongs to the history producer",
    },
    {
        "source": "certification panel", "relation": "certifies up to",
        "target": "Zero/ZeroRel", "status": "PROVED",
        "evidence": ["Represented.cert_scope",
                     "Represented.cert_not_correspondence",
                     "NoOutside.panel_equiv"],
        "boundary": "panel-relative warrant = joint quotient closure; "
                    "never correspondence; panel now replay-integrable",
    },
    {
        "source": "next-event source", "relation": "internalized as policy",
        "target": "replay", "status": "PROVED",
        "evidence": ["Constitution.driver_reproduces_tower",
                     "Constitution.nextFamily_complete"],
        "boundary": "relative to a fixed interpreter; the policy and its "
                    "outputs are represented, the interpreter is "
                    "constitution",
    },
    {
        "source": "kernel constitution", "relation": "represented as data",
        "target": "next-event source", "status": "PROVED",
        "evidence": ["Constitution.interp_describe"],
        "boundary": "a declared constitution family is describable and "
                    "executable relative to the fixed family "
                    "interpreter; the outermost interpreter remains "
                    "metatheory",
    },
    {
        "source": "kernel constitution", "relation": "interprets itself absolutely",
        "target": "kernel constitution", "status": "OPEN",
        "evidence": ["DECLARED:Constitution stratification boundary"],
        "boundary": "the named irreducible obligation: the family "
                    "interpreter is not a member of its own described "
                    "family; absolute self-interpretation unformulated",
    },
]

VALID_STATUSES = (
    "PROVED", "DECLARED", "COMPUTED_WITHIN_BOUNDS",
    "FALSE_WITH_COUNTERMODEL", "OPEN",
)


def dependency_graph() -> dict[str, object]:
    return {
        "nodes": NODES,
        "bridges": BRIDGES,
        "statuses": {
            s: sum(1 for b in BRIDGES if b["status"] == s)
            for s in VALID_STATUSES
        },
    }


# --------------------------------------------------------------------------
# Phase V mirror: represented scheduler, driver, constitution family
# --------------------------------------------------------------------------

from dataclasses import replace as _replace  # noqa: E402

from derivation.represented import (  # noqa: E402
    GENESIS,
    Event,
    World,
    aug_apply,
    aug_ok,
    hist_up_to,
    mark_apply,
    mark_ok,
    obstructed,
    quiescent,
    repair_family,
    replay,
    req_ok,
    step,
    viol,
    wf,
)


def fresh_name(w: World) -> int:
    """Canonical numeral: a priced import of arithmetic and ordering."""
    return len(w.data)


def tower_block(w: World) -> list[Event]:
    k = fresh_name(w)
    return [("setBudget", 1), ("admit", k), ("require", 0, k),
            ("addView", (k,))]


def aug_family(w: World, r: tuple[int, int]) -> list[tuple[int, ...]]:
    return [c for c in [(r[0],), (r[1],)] if aug_ok(w, c)]


def close_blocks(w: World) -> list[list[Event]]:
    out: list[list[Event]] = []
    for r in w.reqs:
        if viol(w, r):
            for (v, p) in repair_family(w, r):
                out.append([("mark", v, p)])
            for c in aug_family(w, r):
                out.append([("addView", c)])
    return out


def next_family(w: World, policy: str) -> list[list[Event]]:
    if policy == "idle":
        return []
    if policy == "tower":
        return [tower_block(w)]
    assert policy == "close"
    return close_blocks(w)


def tower_gen(k: int) -> list[Event]:
    h: list[Event] = [("admit", 0)]
    for _ in range(k):
        h.extend(tower_block(replay(h)))
    return h


PIGEON: list[Event] = [
    ("setBudget", 9), ("admit", 10), ("admit", 20), ("admit", 30),
    ("require", 0, 1), ("require", 0, 2), ("require", 1, 2),
    ("addView", (0,)),
]


def protocols_report(rounds: int = 15) -> dict[str, object]:
    """G0-G2: the driver reproduces the previously supplied stream;
    families are complete and tie-retained; the stop outcome is the
    empty family."""
    reproduces = all(
        tower_gen(k) == hist_up_to(k) for k in range(rounds + 1)
    )
    accepted = []
    for k in range(rounds + 1):
        w = GENESIS
        ok = True
        for e in tower_gen(k):
            w2 = step(w, e)
            if w2 == w:
                ok = False
            w = w2
        accepted.append(ok and quiescent(w) and wf(w))
    pigeon = replay(PIGEON)
    blocks = close_blocks(pigeon)
    both_orientations = (
        [("addView", (1,))] in blocks and [("addView", (2,))] in blocks
    )
    quiet = replay(hist_up_to(4))
    return {
        "G0_supplied_stream": "hist_up_to (metatheoretic producer)",
        "G1_family_singleton_per_stage": True,
        "G2_driver_reproduces_supplied_stream": reproduces,
        "G2_all_stages_accepted_quiescent_wf": all(accepted),
        "close_family_retains_both_orientations": both_orientations,
        "close_family_size_on_pigeonhole": len(blocks),
        "stop_outcome_empty_family": next_family(quiet, "close") == [],
        "fresh_name_source": "canonical numeral (arithmetic/ordering "
                             "import, recorded)",
        "fresh_name_fresh_along_run": all(
            fresh_name(replay(tower_gen(k)))
            not in replay(tower_gen(k)).data
            for k in range(rounds + 1)
        ),
        "generation_scope": "state-derived, prefix-compatible "
                            "generation under metatheoretic iteration "
                            "and a fixed interpreter",
    }


# --------------------------------------------------------------------------
# Constitution family and the fixed family interpreter (mirror)
# --------------------------------------------------------------------------

Desc = tuple[bool, bool, bool, bool, bool, bool]
KERNEL_DESC: Desc = (True, True, True, True, True, True)
DESC_FIELDS = ("dedupAdmit", "guardRequire", "guardAccept",
               "gateBudget", "gateLicense", "certRefusal")


def all_descs() -> list[Desc]:
    out: list[Desc] = []
    for n in range(64):
        bits = (bool(n & 1), bool(n & 2), bool(n & 4),
                bool(n & 8), bool(n & 16), bool(n & 32))
        out.append(bits)
    return out


def interp_step(d: Desc, w: World, e: Event) -> World:
    """Nat-domain guards are unconditional: a disabled guard toggle
    never licenses a negative state, matching the Lean carrier (where
    negatives are unrepresentable) for every constitution descriptor.
    Budget decrements saturate at zero (``max(0, budget - 1)``),
    matching Lean ``Nat`` subtraction exactly — the gateBudget toggle
    only controls whether a zero budget blocks the event, never
    whether the decrement may underflow (PR #12 correction C10)."""
    dedup, greq, gacc, gbud, glic, gcert = d
    kind = e[0]
    if kind == "admit":
        t = e[1]
        assert isinstance(t, int)
        if t < 0 or (dedup and t in w.data):
            return w
        return _replace(w, data=w.data + (t,))
    if kind == "require":
        i, j = e[1], e[2]
        assert isinstance(i, int) and isinstance(j, int)
        if i < 0 or j < 0:
            return w
        if (not greq) or req_ok(w, i, j):
            return _replace(w, reqs=w.reqs + ((i, j),))
        return w
    if kind == "mark":
        v, p = e[1], e[2]
        assert isinstance(v, tuple) and isinstance(p, int)
        if p < 0 or any(x < 0 for x in v):
            return w
        if ((not gacc) or mark_ok(w, v, p)) and (
                (not gbud) or w.budget > 0):
            return _replace(mark_apply(w, v, p),
                            budget=max(0, w.budget - 1))
        return w
    if kind == "addView":
        c = e[1]
        assert isinstance(c, tuple)
        if any(x < 0 for x in c):
            return w
        if (((not gacc) or aug_ok(w, c))
                and ((not glic) or w.aug_licensed)
                and ((not gbud) or w.budget > 0)):
            return _replace(aug_apply(w, c),
                            budget=max(0, w.budget - 1))
        return w
    if kind == "refuse":
        i, j = e[1], e[2]
        assert isinstance(i, int) and isinstance(j, int)
        if i < 0 or j < 0:
            return w
        if ((not gcert) or obstructed(w, (i, j))) and (
                (i, j) not in w.refusals):
            return _replace(w, refusals=w.refusals + ((i, j),))
        return w
    return step(w, e)


DUP_WORLD = World(data=(5,), budget=9)
SAT_WORLD = World(data=(10, 20), views=((0,),), reqs=((0, 1),), budget=9)
BROKE_WORLD = World(data=(10, 20), views=((),), reqs=((0, 1),), budget=0)
UNLIC_WORLD = World(data=(10, 20), views=((),), reqs=((0, 1),),
                    budget=9, aug_licensed=False)

PROBES: list[tuple[str, World, Event]] = [
    ("dedup", DUP_WORLD, ("admit", 5)),
    ("require_guard", DUP_WORLD, ("require", 0, 0)),
    ("accept_guard", SAT_WORLD, ("mark", (0,), 1)),
    ("budget_gate", BROKE_WORLD, ("mark", (), 0)),
    ("license_gate", UNLIC_WORLD, ("addView", (0,))),
    ("refusal_certificate", SAT_WORLD, ("refuse", 0, 1)),
]


def probe_results(d: Desc) -> dict[str, bool]:
    return {
        name: interp_step(d, w, e) == w for (name, w, e) in PROBES
    }


def compliant(d: Desc) -> bool:
    return all(probe_results(d).values())


def cost_capabilities(d: Desc) -> int:
    return sum(1 for b in d if b)


def cost_lex(d: Desc) -> tuple[int, int]:
    return (sum(1 for b in d[:3] if b), sum(1 for b in d[3:] if b))


def minimality_report() -> dict[str, object]:
    descs = all_descs()
    table = [
        {
            "desc": dict(zip(DESC_FIELDS, d)),
            "probes": probe_results(d),
            "compliant": compliant(d),
        }
        for d in descs
    ]
    comp = [d for d in descs if compliant(d)]
    min_cap = (min(cost_capabilities(d) for d in comp) if comp else None)
    min_lex = min((cost_lex(d) for d in comp), default=None)
    interp_matches_kernel = all(
        interp_step(KERNEL_DESC, w, e) == step(w, e)
        for (_, w, e) in PROBES
    ) and interp_step(KERNEL_DESC, SAT_WORLD, ("addView", (1,))) == \
        step(SAT_WORLD, ("addView", (1,)))
    return {
        "class_size": len(descs),
        "compliant": [dict(zip(DESC_FIELDS, d)) for d in comp],
        "unique_compliant_is_kernel": comp == [KERNEL_DESC],
        "orders_agree_on_singleton": (
            len(comp) == 1
            and min_cap == cost_capabilities(KERNEL_DESC)
            and min_lex == cost_lex(KERNEL_DESC)
        ),
        "interp_of_kernel_desc_matches_step": interp_matches_kernel,
        "table": table,
    }


def countermodels_report() -> dict[str, object]:
    """The failed-bridge countermodels of the dependency graph, plus
    the run-level separations, with their evidence handles."""
    failed = [
        {
            "bridge": f"{b['source']} -> {b['target']}",
            "relation": b["relation"],
            "evidence": b["evidence"],
            "boundary": b["boundary"],
        }
        for b in BRIDGES if b["status"] == "FALSE_WITH_COUNTERMODEL"
    ]
    return {
        "failed_bridges": failed,
        "run_level_separations": [
            "witness_not_separation (Completion)",
            "separation_not_witness (Completion)",
            "meta_distinctness_inert (Completion)",
            "retraction_breaks_preservation (Completion)",
            "refusal terminalization refuted: refusal_non_absorbing",
            "guard separations: six load-bearing probes (Initiality)",
        ],
    }
