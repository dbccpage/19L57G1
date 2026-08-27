"""Finite, local reference model for the thinghood construction run.

The module is metatheory for the research packet.  It does not extend the
sealed derivation and it does not import the sealed implementation.  The
candidate universe, its cost, and its isomorphism relation are all declared
here so that the reported minimum is a bounded computation rather than a
narrative identification.

The local predicate ``collapse_fails_law`` is intentionally stricter than a
collision: an admitted asserted pair must be present, the original relation
must satisfy its declared law, and an endomap identifying that pair must make
the pushed relation violate that same law.  A law-free candidate therefore
cannot be a ``thing`` in this run.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
from typing import Iterator, Optional, Sequence

Pair = tuple[int, int]
Relation = frozenset[Pair]
Function = tuple[int, ...]

MAX_CARRIER = 3
MAX_RELATION_EDGES = 3
LAW_NAMES: tuple[str, ...] = (
    "none",
    "irreflexive",
    "asymmetric",
    "symmetric",
    "transitive",
    "irreflexive+transitive",
)
LAW_ATOMS: dict[str, int] = {
    "none": 0,
    "irreflexive": 1,
    "asymmetric": 1,
    "symmetric": 1,
    "transitive": 1,
    "irreflexive+transitive": 2,
}
STORE_NAMES: tuple[str, ...] = ("retained", "protected", "observed")
PASSAGE_STORE_OPTIONS: tuple[tuple[str, ...], ...] = tuple(
    tuple(name for bit, name in enumerate(STORE_NAMES) if mask & (1 << bit))
    for mask in range(1 << len(STORE_NAMES))
)

# This is the hash of the prompt at the start of the run.  It is checked by
# the runner and tests so an accidental edit cannot be silently treated as a
# completed execution.
PROMPT_SHA256 = "ad70e80ec1eb9fd884671cad00881405b4ea4301d1f756472c35e105ebaf8bfc"


@dataclass(frozen=True)
class Bill:
    """The independently priced metatheory bill for one candidate."""

    carrier_points: int
    relation_edges: int
    asserted_admissions: int
    law_atoms: int
    meta_constraints: int
    store_admissions: int
    resource_admissions: int

    @property
    def total(self) -> int:
        return (
            self.carrier_points
            + self.relation_edges
            + self.asserted_admissions
            + self.law_atoms
            + self.meta_constraints
            + self.store_admissions
            + self.resource_admissions
        )

    def json(self) -> dict[str, int]:
        return {
            "carrier_points": self.carrier_points,
            "relation_edges": self.relation_edges,
            "asserted_admissions": self.asserted_admissions,
            "law_atoms": self.law_atoms,
            "meta_constraints": self.meta_constraints,
            "store_admissions": self.store_admissions,
            "resource_admissions": self.resource_admissions,
            "total": self.total,
        }


@dataclass(frozen=True)
class Candidate:
    """A finite pointed structure with optional law and priced stores.

    ``asserted`` is an independent admission of one ordered pair.  The pair
    must also be an edge of ``rel``; charging both fields keeps the admission
    and the carrier structure distinct.  ``meta_inequality`` is the optional
    A3-style metatheoretic constraint and is not an object-language law.
    Budget and license are separate execution resources; they are priced but
    never needed by the Q1 predicate.
    """

    n: int
    rel: Relation
    asserted: Optional[Pair]
    law: str
    meta_inequality: bool = False
    stores: tuple[str, ...] = ()
    designated: Optional[Pair] = None
    budget_admitted: bool = False
    license_admitted: bool = False

    def bill(self) -> Bill:
        return Bill(
            carrier_points=self.n,
            relation_edges=len(self.rel),
            asserted_admissions=int(self.asserted is not None),
            law_atoms=LAW_ATOMS[self.law],
            meta_constraints=int(self.meta_inequality),
            store_admissions=len(self.stores),
            resource_admissions=int(self.budget_admitted) + int(self.license_admitted),
        )

    def json(self) -> dict[str, object]:
        return {
            "carrier_size": self.n,
            "relation": [list(pair) for pair in sorted(self.rel)],
            "asserted_pair": (
                None if self.asserted is None else list(self.asserted)
            ),
            "designated_pair": (
                None if self.designated is None else list(self.designated)
            ),
            "law": self.law,
            "meta_inequality": self.meta_inequality,
            "stores": list(self.stores),
            "budget_admitted": self.budget_admitted,
            "license_admitted": self.license_admitted,
            "bill": self.bill().json(),
        }

    def short_id(self) -> str:
        relation = ",".join(f"{x}{y}" for x, y in sorted(self.rel)) or "-"
        asserted = "-" if self.asserted is None else f"{self.asserted[0]}{self.asserted[1]}"
        stores = ",".join(self.stores) or "-"
        designated = (
            "-" if self.designated is None else f"{self.designated[0]}{self.designated[1]}"
        )
        return (
            f"n{self.n}:r[{relation}]:a[{asserted}]:l[{self.law}]"
            f":m{int(self.meta_inequality)}:d[{designated}]:s[{stores}]"
        )


@dataclass(frozen=True)
class CollapseWitness:
    """A finite witness that a candidate law fails under a collapse."""

    source_pair: Pair
    function: Function
    pushed_relation: Relation

    def json(self) -> dict[str, object]:
        return {
            "source_pair": list(self.source_pair),
            "function": list(self.function),
            "pushed_relation": [list(pair) for pair in sorted(self.pushed_relation)],
        }


def _pairs(n: int) -> tuple[Pair, ...]:
    return tuple((x, y) for x in range(n) for y in range(n))


def _relations(n: int) -> Iterator[Relation]:
    """Enumerate all relations with at most the declared edge bound."""

    pairs = _pairs(n)
    for size in range(MAX_RELATION_EDGES + 1):
        for chosen in combinations(pairs, size):
            yield frozenset(chosen)


def _well_formed(candidate: Candidate) -> bool:
    if not 1 <= candidate.n <= MAX_CARRIER:
        return False
    if candidate.law not in LAW_NAMES:
        return False
    if len(candidate.rel) > MAX_RELATION_EDGES:
        return False
    if any(
        x < 0 or x >= candidate.n or y < 0 or y >= candidate.n
        for x, y in candidate.rel
    ):
        return False
    if candidate.asserted is not None:
        x, y = candidate.asserted
        if not (0 <= x < candidate.n and 0 <= y < candidate.n):
            return False
        if candidate.asserted not in candidate.rel:
            return False
    if candidate.designated is not None:
        x, y = candidate.designated
        if not (0 <= x < candidate.n and 0 <= y < candidate.n):
            return False
    if candidate.asserted is not None and candidate.designated != candidate.asserted:
        return False
    if candidate.meta_inequality:
        if candidate.designated is None:
            return False
        if candidate.designated[0] == candidate.designated[1]:
            return False
    elif candidate.designated is not None and candidate.asserted is None:
        return False
    if candidate.meta_inequality and candidate.asserted is not None:
        if candidate.asserted[0] == candidate.asserted[1]:
            return False
    declared_store_order = tuple(
        name for name in STORE_NAMES if name in candidate.stores
    )
    if declared_store_order != candidate.stores:
        return False
    if any(store not in STORE_NAMES for store in candidate.stores):
        return False
    if len(set(candidate.stores)) != len(candidate.stores):
        return False
    return law_holds(candidate.n, candidate.rel, candidate.law)


@lru_cache(maxsize=1)
def all_candidates() -> tuple[Candidate, ...]:
    """The declared finite candidate space, in deterministic order."""

    out: list[Candidate] = []
    for n in range(1, MAX_CARRIER + 1):
        pairs = _pairs(n)
        for relation in _relations(n):
            asserted_options: tuple[Optional[Pair], ...] = (None,) + tuple(
                pair for pair in pairs if pair in relation
            )
            for asserted in asserted_options:
                for law in LAW_NAMES:
                    for meta_inequality in (False, True):
                        for stores in PASSAGE_STORE_OPTIONS:
                            designated_options: tuple[Optional[Pair], ...]
                            if asserted is not None:
                                designated_options = (asserted,)
                            elif meta_inequality:
                                designated_options = tuple(
                                    pair for pair in pairs if pair[0] != pair[1]
                                )
                            else:
                                designated_options = (None,)
                            for designated in designated_options:
                                for budget_admitted in (False, True):
                                    for license_admitted in (False, True):
                                        candidate = Candidate(
                                            n=n,
                                            rel=relation,
                                            asserted=asserted,
                                            law=law,
                                            meta_inequality=meta_inequality,
                                            stores=stores,
                                            designated=designated,
                                            budget_admitted=budget_admitted,
                                            license_admitted=license_admitted,
                                        )
                                        if _well_formed(candidate):
                                            out.append(candidate)
    return tuple(out)


def law_holds(n: int, relation: Relation, law: str) -> bool:
    """Evaluate one of the explicitly declared finite law predicates."""

    if law == "none":
        return True
    if law in ("irreflexive", "irreflexive+transitive"):
        if any(x == y for x, y in relation):
            return False
    if law == "asymmetric":
        if any((y, x) in relation for x, y in relation):
            return False
    if law in ("symmetric",):
        if any((y, x) not in relation for x, y in relation):
            return False
    if law in ("transitive", "irreflexive+transitive"):
        for x, y in relation:
            for y2, z in relation:
                if y == y2 and (x, z) not in relation:
                    return False
    if law not in LAW_NAMES:
        return False
    # ``n`` is part of the signature even when the current law has no need to
    # inspect isolated points; retaining it makes the predicate explicit.
    return all(0 <= x < n and 0 <= y < n for x, y in relation)


def all_functions(n: int) -> tuple[Function, ...]:
    return tuple(tuple(values) for values in product(range(n), repeat=n))


def pushforward(relation: Relation, function: Function) -> Relation:
    return frozenset((function[x], function[y]) for x, y in relation)


def collapsing_functions(candidate: Candidate) -> Iterator[Function]:
    """Functions identifying the candidate's admitted ordered pair."""

    if candidate.asserted is None:
        return
    x, y = candidate.asserted
    if x == y:
        return
    for function in all_functions(candidate.n):
        if function[x] == function[y]:
            yield function


def collapse_witness(candidate: Candidate) -> Optional[CollapseWitness]:
    """Return the first deterministic law-violating collapse, if any."""

    if not _well_formed(candidate) or candidate.law == "none":
        return None
    if candidate.asserted is None or candidate.asserted[0] == candidate.asserted[1]:
        return None
    for function in collapsing_functions(candidate):
        pushed = pushforward(candidate.rel, function)
        if not law_holds(candidate.n, pushed, candidate.law):
            return CollapseWitness(candidate.asserted, function, pushed)
    return None


def collapse_fails_law(candidate: Candidate) -> bool:
    """The Q1 predicate: an admitted pair collapses and violates its law."""

    return collapse_witness(candidate) is not None


def is_datum(candidate: Candidate) -> bool:
    return candidate.asserted is not None


def is_difference(candidate: Candidate) -> bool:
    """The local A1i skeleton, not a renaming of the sealed paper object."""

    return (
        is_datum(candidate)
        and candidate.law == "irreflexive"
        and law_holds(candidate.n, candidate.rel, candidate.law)
    )


def is_thing(candidate: Candidate) -> bool:
    return collapse_fails_law(candidate)


def candidate_tags(candidate: Candidate) -> tuple[str, ...]:
    """Tags used to populate the required Phase-I class table."""

    tags: list[str] = []
    if candidate.stores:
        tags.append("sealed_passage_state")
    if (
        candidate.n == 1
        and not candidate.rel
        and candidate.asserted is None
        and candidate.law == "none"
        and not candidate.meta_inequality
    ):
        tags.append("carrier_no_relation_no_law")
    if candidate.law == "none" and candidate.asserted is not None:
        tags.append("a1_bare_asserted_pair")
    if (
        candidate.meta_inequality
        and candidate.asserted is None
        and candidate.designated is not None
        and not candidate.rel
        and candidate.law == "none"
    ):
        tags.append("a3_meta_inequality")
    if candidate.asserted is not None and candidate.law == "irreflexive":
        tags.append("a1i_asserted_pair_irreflexive")
    if candidate.asserted is not None and candidate.law == "symmetric":
        tags.append("a1_asserted_pair_symmetry_only")
    if candidate.asserted is not None and candidate.law not in (
        "none",
        "irreflexive",
        "symmetric",
    ):
        tags.append("richer_law")
    return tuple(tags)


def _mapped(
    candidate: Candidate, function: Function
) -> tuple[Relation, Optional[Pair], Optional[Pair]]:
    relation = frozenset((function[x], function[y]) for x, y in candidate.rel)
    asserted = (
        None
        if candidate.asserted is None
        else (function[candidate.asserted[0]], function[candidate.asserted[1]])
    )
    designated = (
        None
        if candidate.designated is None
        else (function[candidate.designated[0]], function[candidate.designated[1]])
    )
    return relation, asserted, designated


def candidate_isomorphic(left: Candidate, right: Candidate) -> bool:
    """Isomorphism preserves laws, stores, meta constraints, and the pair."""

    if left.n != right.n:
        return False
    if (
        left.law != right.law
        or left.meta_inequality != right.meta_inequality
        or left.stores != right.stores
        or left.budget_admitted != right.budget_admitted
        or left.license_admitted != right.license_admitted
    ):
        return False
    for permutation_values in permutations(range(left.n)):
        function = tuple(permutation_values)
        relation, asserted, designated = _mapped(left, function)
        if (
            relation == right.rel
            and asserted == right.asserted
            and designated == right.designated
        ):
            return True
    return False


def canonical_key(candidate: Candidate) -> tuple[object, ...]:
    """The lexicographically least representation under carrier relabeling."""

    representations: list[tuple[object, ...]] = []
    for permutation_values in permutations(range(candidate.n)):
        function = tuple(permutation_values)
        relation, asserted, designated = _mapped(candidate, function)
        asserted_key: tuple[int, int] = (-1, -1) if asserted is None else asserted
        designated_key: tuple[int, int] = (
            (-1, -1) if designated is None else designated
        )
        representations.append(
            (
                candidate.law,
                candidate.meta_inequality,
                candidate.stores,
                candidate.budget_admitted,
                candidate.license_admitted,
                tuple(sorted(relation)),
                asserted_key,
                designated_key,
            )
        )
    return min(representations)


def _candidate_with_tags(tag: str, *, stores: Optional[tuple[str, ...]] = None) -> Optional[Candidate]:
    for candidate in all_candidates():
        if tag in candidate_tags(candidate) and (
            stores is None or candidate.stores == stores
        ):
            return candidate
    return None


def _candidate_json(candidate: Optional[Candidate]) -> Optional[dict[str, object]]:
    return None if candidate is None else candidate.json()


def _witness_json(candidate: Optional[Candidate]) -> Optional[dict[str, object]]:
    if candidate is None:
        return None
    witness = collapse_witness(candidate)
    return None if witness is None else witness.json()


@lru_cache(maxsize=1)
def minimality_report() -> dict[str, object]:
    candidates = all_candidates()
    survivors = [candidate for candidate in candidates if is_thing(candidate)]
    minimum_cost = min(candidate.bill().total for candidate in survivors)
    raw_minima = [
        candidate for candidate in survivors if candidate.bill().total == minimum_cost
    ]
    representatives: dict[tuple[object, ...], Candidate] = {}
    for candidate in raw_minima:
        representatives.setdefault(canonical_key(candidate), candidate)
    below = [candidate for candidate in candidates if candidate.bill().total < minimum_cost]
    below_survivors = [candidate for candidate in below if is_thing(candidate)]
    assert not below_survivors
    assert raw_minima
    assert all(is_thing(candidate) for candidate in raw_minima)
    return {
        "candidate_count": len(candidates),
        "survivor_count": len(survivors),
        "minimum_cost": minimum_cost,
        "cost_measure": (
            "mu_additive_atoms: one unit per carrier point, relation edge, "
            "asserted admission, law atom, metatheoretic inequality, passage "
            "store admission, budget admission, and license admission"
        ),
        "below_minimum_count": len(below),
        "below_minimum_survivor_count": len(below_survivors),
        "every_below_minimum_fails": not below_survivors,
        "every_minimum_satisfies": all(is_thing(candidate) for candidate in raw_minima),
        "raw_minimum_count": len(raw_minima),
        "minimum_isomorphism_class_count": len(representatives),
        "non_unique_first_answer": len(representatives) > 1,
        "minimum_representatives": [
            {
                **candidate.json(),
                "collapse_witness": _witness_json(candidate),
            }
            for _, candidate in sorted(representatives.items(), key=lambda item: item[0])
        ],
    }


def _class_result(
    tag: str,
    preferred: Optional[Candidate] = None,
) -> dict[str, object]:
    members = [candidate for candidate in all_candidates() if tag in candidate_tags(candidate)]
    survivors = [candidate for candidate in members if is_thing(candidate)]
    representative = preferred if preferred is not None else (members[0] if members else None)
    witness_candidate = survivors[0] if survivors else None
    return {
        "member_count": len(members),
        "can_fail_law": bool(survivors),
        "representative": _candidate_json(representative),
        "witness_candidate": _candidate_json(witness_candidate),
        "witness": _witness_json(witness_candidate),
        "countermodel": (
            None
            if witness_candidate is not None or representative is None
            else {
                "candidate": representative.json(),
                "reason": (
                    "No candidate in this class satisfies the collapse-fails-law "
                    "predicate within the declared finite space."
                ),
            }
        ),
    }


@lru_cache(maxsize=1)
def class_results() -> dict[str, object]:
    symmetric_example = next(
        (
            candidate
            for candidate in all_candidates()
            if "a1_asserted_pair_symmetry_only" in candidate_tags(candidate)
            and candidate.n == 2
            and candidate.rel == frozenset({(0, 1), (1, 0)})
            and candidate.asserted == (0, 1)
            and not candidate.meta_inequality
            and not candidate.stores
        ),
        None,
    )
    required = {
        "carrier_no_relation_no_law": _class_result("carrier_no_relation_no_law"),
        "a1_bare_asserted_pair": _class_result("a1_bare_asserted_pair"),
        "a3_meta_inequality": _class_result("a3_meta_inequality"),
        "a1i_asserted_pair_irreflexive": _class_result(
            "a1i_asserted_pair_irreflexive"
        ),
        "a1_asserted_pair_symmetry_only": _class_result(
            "a1_asserted_pair_symmetry_only", symmetric_example
        ),
        "richer_law": _class_result("richer_law"),
    }
    richer_by_law: dict[str, object] = {}
    for law in LAW_NAMES:
        if law in ("none", "irreflexive", "symmetric"):
            continue
        members = [
            candidate
            for candidate in all_candidates()
            if candidate.asserted is not None and candidate.law == law
        ]
        survivors = [candidate for candidate in members if is_thing(candidate)]
        richer_by_law[law] = {
            "member_count": len(members),
            "can_fail_law": bool(survivors),
            "witness_candidate": _candidate_json(survivors[0] if survivors else None),
            "witness": _witness_json(survivors[0] if survivors else None),
            "countermodel": (
                None
                if survivors
                else {
                    "candidate": _candidate_json(members[0] if members else None),
                    "reason": "All bounded collapses preserve this law in this class.",
                }
            ),
        }
    passage_options: dict[str, object] = {}
    for stores in PASSAGE_STORE_OPTIONS:
        # Use the same smallest law-bearing structure for every store choice.
        # This isolates the store price instead of accidentally selecting a
        # cheaper store-only object with no asserted pair or law.
        representative = next(
            (
                candidate
                for candidate in all_candidates()
                if candidate.stores == stores
                and candidate.n == 2
                and candidate.rel == frozenset({(0, 1)})
                and candidate.asserted == (0, 1)
                and candidate.designated == (0, 1)
                and candidate.law == "irreflexive"
                and not candidate.meta_inequality
                and not candidate.budget_admitted
                and not candidate.license_admitted
            ),
            None,
        )
        passage_options["not_admitted" if not stores else "+".join(stores)] = {
            "store_admissions": len(stores),
            "candidate": _candidate_json(representative),
            "can_fail_law": (
                False if representative is None else is_thing(representative)
            ),
            "witness": (
                None
                if representative is None
                else (
                    None
                    if collapse_witness(representative) is None
                    else collapse_witness(representative).json()
                )
            ),
            "note": (
                "not_admitted is the zero-store baseline and is not a distinct "
                "free observer; every nonempty store is charged independently"
            ),
        }
    required["sealed_passage_state"] = {
        "member_count": sum(
            1 for candidate in all_candidates() if candidate.stores
        ),
        "can_fail_law": True,
        "options": passage_options,
    }
    return {
        "required_classes": required,
        "richer_laws": richer_by_law,
    }


@lru_cache(maxsize=1)
def implication_lattice() -> dict[str, object]:
    predicates = {
        "datum": is_datum,
        "difference": is_difference,
        "thing": is_thing,
    }
    edges: dict[str, object] = {}
    names = tuple(predicates)
    for left in names:
        for right in names:
            if left == right:
                continue
            countermodel: Optional[Candidate] = None
            for candidate in all_candidates():
                if predicates[left](candidate) and not predicates[right](candidate):
                    countermodel = candidate
                    break
            key = f"{left}->{right}"
            edges[key] = {
                "holds_in_declared_space": countermodel is None,
                "countermodel": _candidate_json(countermodel),
            }
    return {
        "definitions": {
            "datum": "an admitted asserted pair",
            "difference": "the local A1i law-bearing candidate predicate",
            "thing": "collapse_fails_law",
        },
        "edges": edges,
        "all_arrows_checked_over": "all candidates in the declared finite space",
        "identification_status": (
            "REFUSED: the local A1i minimum is not renamed in the sealed papers; "
            "a tied asymmetric minimum remains a distinct law-bearing class"
        ),
    }


@lru_cache(maxsize=1)
def law_order_report() -> dict[str, object]:
    """Check the strict law-order fact used by the tied-minimum label."""

    asymmetry_implies_irreflexivity = True
    reverse_countermodel: Optional[dict[str, object]] = None
    checked = 0
    for n in range(1, MAX_CARRIER + 1):
        for relation in _relations(n):
            checked += 1
            if law_holds(n, relation, "asymmetric") and not law_holds(
                n, relation, "irreflexive"
            ):
                asymmetry_implies_irreflexivity = False
            if (
                reverse_countermodel is None
                and law_holds(n, relation, "irreflexive")
                and not law_holds(n, relation, "asymmetric")
            ):
                reverse_countermodel = {
                    "carrier_size": n,
                    "relation": [list(pair) for pair in sorted(relation)],
                    "law": "irreflexive",
                    "violates": "asymmetric",
                }
    assert asymmetry_implies_irreflexivity
    assert reverse_countermodel is not None
    return {
        "relations_checked": checked,
        "asymmetric_implies_irreflexive": asymmetry_implies_irreflexivity,
        "irreflexive_not_implies_asymmetric": True,
        "strictly_richer_in_declared_law_order": True,
        "reverse_countermodel": reverse_countermodel,
    }


def _dynamics_countermodel() -> dict[str, object]:
    return {
        "state": "genesisP",
        "stores": {
            "retained": False,
            "protected": False,
            "observation_declared": False,
            "observer_zero": False,
        },
        "obstP": False,
        "why": (
            "A collapsed-pair story supplies no retained, protected, declared, "
            "zero-gate certificate; two_rule is therefore inapplicable."
        ),
    }


def dynamics_report() -> dict[str, object]:
    """Return the five exact-hypothesis conditional dynamic claims."""

    claims: list[dict[str, object]] = [
        {
            "id": "TH-Q2-01",
            "status": "CONDITIONAL_THEOREM",
            "statement": "The inscription alone forces no object-language successor.",
            "hypotheses": ["Challenge 0 / initial inscription", "no extra object-language admission"],
            "evidence": ["paper/paper.md:175", "paper/paper.md:488-492"],
            "machine_check": False,
        },
        {
            "id": "TH-Q2-02",
            "status": "CONDITIONAL_THEOREM",
            "statement": "A collapsed pair is not an active obstruction by itself.",
            "hypotheses": [
                "obstP requires retained, protected, declared-observation, and observer-zero gates",
                "no gate is supplied by collision alone",
            ],
            "evidence": [
                "lean4/Derivation/PrimitivePassage.lean:326-328",
                "lean4/Derivation/PrimitivePassage.lean:476-518",
            ],
            "countermodel": _dynamics_countermodel(),
            "machine_check": False,
        },
        {
            "id": "TH-Q2-03",
            "status": "CONDITIONAL_THEOREM",
            "statement": "obstP has four independent gates in its declared reading.",
            "hypotheses": [
                "the repository's obstP definition and declared observation policy",
                "the four named independence witnesses",
            ],
            "evidence": [
                "obstP_factors",
                "obst_conditions_independent",
                "gate_zero_independent",
                "gate_declared_independent",
                "gate_protection_independent",
                "gate_retention_independent",
            ],
            "machine_check": False,
        },
        {
            "id": "TH-Q2-04",
            "status": "CONDITIONAL_THEOREM",
            "statement": "two_rule is applicable only at an active, in-bounds protected obstruction.",
            "hypotheses": [
                "hobst : obstP s i j = true",
                "hij : i != j",
                "hi : i is in bounds",
                "hprot : (i,j) is protected",
            ],
            "evidence": ["two_rule", "proposal_not_execution", "extension_always_available"],
            "countermodel": _dynamics_countermodel(),
            "machine_check": False,
        },
        {
            "id": "TH-Q2-05",
            "status": "CONDITIONAL_THEOREM",
            "statement": "two_rule is a response menu at an active obstruction, not a law of the inscription.",
            "hypotheses": [
                "TH-Q2-01 through TH-Q2-04",
                "the response grammar is declared metatheory",
            ],
            "evidence": [
                "two_rule",
                "paper/paper.md:488-492",
                "research/genesis_continuation/continuation_plan.md:86-90",
            ],
            "machine_check": False,
        },
    ]
    assert all(claim["machine_check"] is False for claim in claims)
    return {
        "claims": claims,
        "machine_check_status": "NOT_RUN",
        "machine_check_reason": (
            "This unregistered research tree does not elaborate or resolve the "
            "sealed theorem names; CONDITIONAL_THEOREM is the explicit downgrade."
        ),
        "terminal": "NO_FORCED_DYNAMICAL_LAW",
        "terminal_scope": (
            "the five conditional claims above; Q2 only; no claim that Q1 has "
            "a unique survivor"
        ),
        "open_terminals": [
            "OB1_UNCHANGED",
            "S66_UNCHANGED",
            "S9_LAST_UNCHANGED",
        ],
        "forbidden_closures": {
            "S6_item_6": True,
            "S9_last_bullet": True,
            "OB-1": True,
        },
    }


def adversarial_attacks() -> dict[str, object]:
    """The eight required attack dispositions, kept machine-readable."""

    bare = _candidate_with_tags("a1_bare_asserted_pair")
    asym = next(
        (
            candidate
            for candidate in all_candidates()
            if candidate.law == "asymmetric"
            and candidate.asserted is not None
            and candidate.bill().total == minimality_report()["minimum_cost"]
            and is_thing(candidate)
        ),
        None,
    )
    return {
        "1_datum_is_thing": {
            "status": "COUNTERMODEL",
            "disposition": "REFUSED",
            "countermodel": _candidate_json(bare),
            "reason": "The bare admitted pair has no law and is not a thing.",
        },
        "2_bare_asserted_pair_is_thing": {
            "status": "COUNTERMODEL",
            "disposition": "REFUSED",
            "countermodel": _candidate_json(bare),
            "sealed_evidence": ["selfdiff_consistent", "bare_collapse_admissible"],
        },
        "3_collapse_is_the_law": {
            "status": "REFUSED",
            "disposition": "A collapse is a map; failure is not P(Push r c).",
            "machine_check": "law=none candidates never satisfy collapse_fails_law",
        },
        "4_primitive_difference_is_definitionally_the_thing": {
            "status": "REFUSED",
            "disposition": "The local A1i member is retained without renaming; the tied asymmetric member prevents uniqueness.",
            "countermodel": _candidate_json(asym),
        },
        "5_two_rule_forces_structure_from_seed": {
            "status": "COUNTERMODEL",
            "disposition": "REFUSED",
            "countermodel": _dynamics_countermodel(),
            "sealed_evidence": ["two_rule", "paper/paper.md:175"],
        },
        "6_active_obstruction_follows_from_inscription": {
            "status": "COUNTERMODEL",
            "disposition": "REFUSED",
            "countermodel": _dynamics_countermodel(),
            "sealed_evidence": ["obst_requires_observation", "obst_conditions_independent"],
        },
        "7_cheapest_thing_includes_observer": {
            "status": "FINITE_COMPUTATION",
            "disposition": "Observer stores are independently priced; the no-store A1i minimum is cheaper than every nonempty passage state.",
            "machine_check": True,
        },
        "8_candidate_list_is_closed_by_narrative": {
            "status": "OPEN",
            "disposition": "The result is complete only for the declared finite grammar; any unlisted law or store remains open.",
            "machine_check": True,
        },
    }


def prompt_hash() -> str:
    path = Path(__file__).with_name("PROMPT.md")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_receipt() -> dict[str, object]:
    actual_prompt_sha = prompt_hash()
    if actual_prompt_sha != PROMPT_SHA256:
        raise ValueError(
            "PROMPT.md changed during the run: "
            f"expected {PROMPT_SHA256}, got {actual_prompt_sha}"
        )
    minimum = minimality_report()
    return {
        "schema": "thinghood-v1",
        "AuthorityEffect": "None",
        "authority_effect": "None",
        "prompt_sha256": actual_prompt_sha,
        "scope": {
            "write_root": "research/thinghood/",
            "sealed_paths": [
                "prompt/",
                "paper/",
                "code/",
                "lean4/Derivation/",
                "artifacts/",
                "CLAUDE.md",
                ".github/workflows/verify.yml",
                "sibling research trees",
            ],
            "external_citations": False,
        },
        "apparatus_ethics": {
            "withdrawals_remain_withdrawals": True,
            "counts_without_min_response_witness_are_not_claims": True,
            "authority_effect": "None",
        },
        "candidate_space": {
            "carrier_sizes": list(range(1, MAX_CARRIER + 1)),
            "maximum_relation_edges": MAX_RELATION_EDGES,
            "laws": list(LAW_NAMES),
            "passage_store_options": [list(option) for option in PASSAGE_STORE_OPTIONS],
            "resource_options": {
                "budget_admitted": [False, True],
                "license_admitted": [False, True],
            },
            "candidate_count": len(all_candidates()),
            "predicate": "collapse_fails_law",
        },
        "minimality": minimum,
        "class_results": class_results(),
        "thing_difference_datum_lattice": implication_lattice(),
        "law_order": law_order_report(),
        "limit_scope": {
            "status": "CONDITIONAL_THEOREM",
            "evidence": ["generation_never_dries", "g1_class_exclusion"],
            "scope": "LocalStrategy + FiniteDeclaration",
            "unbounded_extension_claim": False,
        },
        "dynamics": dynamics_report(),
        "adversarial_attacks": adversarial_attacks(),
        "terminals": [
            "THINGHOOD_CHARACTERIZED",
            "THING_COINCIDES_WITH_A1I",
            "THING_STRICTLY_RICHER_THAN_A1I",
            "NO_FORCED_DYNAMICAL_LAW",
            "OB1_UNCHANGED",
            "S66_UNCHANGED",
            "S9_LAST_UNCHANGED",
            "CANDIDATE_SPACE_OPEN",
            "REFUSED",
        ],
        "terminal_scopes": {
            "THINGHOOD_CHARACTERIZED": "all candidates in the declared finite grammar",
            "THING_COINCIDES_WITH_A1I": "one minimum isomorphism class is the local A1i law-bearing class",
            "THING_STRICTLY_RICHER_THAN_A1I": "a tied minimum uses the strictly stronger asymmetric law; this is not a unique delta",
            "NO_FORCED_DYNAMICAL_LAW": "Q2 only, under the five conditional claims in dynamics",
            "OB1_UNCHANGED": "object-language endogenous demand generation remains open",
            "S66_UNCHANGED": "the static difference object does not gain a derived successor law",
            "S9_LAST_UNCHANGED": "carrier, occurrences, relation, witness, irreflexivity, and orientation remain un-derived",
            "CANDIDATE_SPACE_OPEN": "unlisted axioms and stores are not silently exhausted",
        },
    }


__all__ = [
    "Candidate",
    "Bill",
    "CollapseWitness",
    "LAW_NAMES",
    "PASSAGE_STORE_OPTIONS",
    "PROMPT_SHA256",
    "all_candidates",
    "adversarial_attacks",
    "build_receipt",
    "candidate_isomorphic",
    "candidate_tags",
    "canonical_key",
    "class_results",
    "collapse_fails_law",
    "collapse_witness",
    "dynamics_report",
    "implication_lattice",
    "is_datum",
    "is_difference",
    "is_thing",
    "law_holds",
    "minimality_report",
    "prompt_hash",
]
