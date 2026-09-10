"""Declared finite regime space for the CL-ISO-SOUND falsifier hunt.

Classification: declared metatheory (the bound) plus deterministic
enumeration.  Tokens are dummy labels; the implemented isomorphism
forgets them.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
from itertools import combinations, product
from typing import Iterator

from derivation.model import Inst, Pair, Regime

# The declared bound.  Changing any field is a different hunt.
MAX_DATA = 3
MAX_FORMS = 2
MAX_ARITY = 2
MAX_INSTS = 3

BOUNDS: dict[str, int] = {
    "max_data": MAX_DATA,
    "max_forms": MAX_FORMS,
    "max_arity": MAX_ARITY,
    "max_insts": MAX_INSTS,
}


def form_signatures() -> tuple[tuple[int, ...], ...]:
    out: list[tuple[int, ...]] = [()]
    for n_forms in range(1, MAX_FORMS + 1):
        for arities in product(range(1, MAX_ARITY + 1), repeat=n_forms):
            out.append(arities)
    return tuple(out)


def instance_slots(n_data: int, forms: tuple[int, ...]) -> tuple[Inst, ...]:
    slots: list[Inst] = []
    for form_index, arity in enumerate(forms):
        for args in product(range(n_data), repeat=arity):
            slots.append((form_index, args))
    return tuple(slots)


def req_slots(n_data: int) -> tuple[Pair, ...]:
    return tuple(
        (i, j) for i in range(n_data) for j in range(i + 1, n_data)
    )


def masks(n: int) -> range:
    return range(1 << n)


def enumerate_regimes() -> Iterator[Regime]:
    """Every well-formed regime inside the declared bound, in a fixed order."""
    for n_data in range(MAX_DATA + 1):
        tokens = tuple(f"d{i}" for i in range(n_data))
        reqs_all = req_slots(n_data)
        n_req = len(reqs_all)
        for forms in form_signatures():
            slots = instance_slots(n_data, forms)
            n_forms = len(forms)
            max_k = min(MAX_INSTS, len(slots))
            for k in range(max_k + 1):
                for chosen in combinations(slots, k):
                    insts = frozenset(chosen)
                    for rule_mask in masks(n_forms):
                        rules = frozenset(
                            f for f in range(n_forms) if (rule_mask >> f) & 1
                        )
                        for req_mask in masks(n_req):
                            reqs = frozenset(
                                reqs_all[i]
                                for i in range(n_req)
                                if (req_mask >> i) & 1
                            )
                            yield Regime(tokens, forms, insts, rules, reqs)


def regime_record(r: Regime) -> dict[str, object]:
    return {
        "n_data": r.n_data(),
        "forms": list(r.forms),
        "insts": sorted(([f, list(args)] for f, args in r.insts)),
        "rules": sorted(r.rules),
        "reqs": sorted(([i, j] for i, j in r.reqs)),
    }


def count_space() -> int:
    """Closed-form size of the enumeration, used to cross-check the bound.

    Independent of ``form_signatures``/``instance_slots``: the signature set is
    re-derived inline and the slot count is the arithmetic ``sum n_data**arity``,
    so this catches an under-enumeration in those two functions rather than
    sharing their blind spot.  The literal 56020 pinned in the tests is the
    ground-truth anchor.
    """
    total = 0
    for n_data in range(MAX_DATA + 1):
        n_req = n_data * (n_data - 1) // 2
        for n_forms in range(MAX_FORMS + 1):
            for arities in product(range(1, MAX_ARITY + 1), repeat=n_forms):
                n_slots = sum(n_data ** arity for arity in arities)
                max_k = min(MAX_INSTS, n_slots)
                n_inst_sets = sum(math.comb(n_slots, k) for k in range(max_k + 1))
                total += n_inst_sets * (1 << n_forms) * (1 << n_req)
    return total
