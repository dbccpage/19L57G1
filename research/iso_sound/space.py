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

DEEP_BOUNDS: dict[str, int] = {
    "max_data": 3,
    "max_forms": 1,
    "max_arity": 3,
    "max_insts": 4,
}


def form_signatures(
    max_forms: int = MAX_FORMS,
    max_arity: int = MAX_ARITY,
) -> tuple[tuple[int, ...], ...]:
    out: list[tuple[int, ...]] = [()]
    for n_forms in range(1, max_forms + 1):
        for arities in product(range(1, max_arity + 1), repeat=n_forms):
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


def enumerate_regimes(
    max_data: int = MAX_DATA,
    max_forms: int = MAX_FORMS,
    max_arity: int = MAX_ARITY,
    max_insts: int = MAX_INSTS,
) -> Iterator[Regime]:
    """Every well-formed regime inside the declared bound, in a fixed order."""
    for n_data in range(max_data + 1):
        tokens = tuple(f"d{i}" for i in range(n_data))
        reqs_all = req_slots(n_data)
        n_req = len(reqs_all)
        for forms in form_signatures(max_forms=max_forms, max_arity=max_arity):
            slots = instance_slots(n_data, forms)
            n_forms = len(forms)
            max_k = min(max_insts, len(slots))
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


def sample_regimes(
    max_data: int = 3,
    max_forms: int = 2,
    max_arity: int = 3,
    max_insts: int = 4,
    sample_count: int = 1000,
    seed: int = 42,
    require_ternary: bool = True,
) -> Iterator[Regime]:
    """Deterministic pseudo-random sample of regimes for high-density sweeps."""
    import random
    rng = random.Random(seed)
    all_sigs = [
        sig for sig in form_signatures(max_forms=max_forms, max_arity=max_arity)
        if (not require_ternary or any(a >= 3 for a in sig))
    ]
    if not all_sigs:
        all_sigs = list(form_signatures(max_forms=max_forms, max_arity=max_arity))

    for _ in range(sample_count):
        n_data = rng.randint(1, max_data)
        tokens = tuple(f"d{i}" for i in range(n_data))
        reqs_all = req_slots(n_data)
        n_req = len(reqs_all)
        forms = rng.choice(all_sigs)
        n_forms = len(forms)
        slots = instance_slots(n_data, forms)
        if not slots:
            chosen: tuple[Inst, ...] = ()
        else:
            max_k = min(max_insts, len(slots))
            k = rng.randint(0, max_k)
            chosen = tuple(rng.sample(slots, k))
        insts = frozenset(chosen)
        rule_mask = rng.randrange(1 << n_forms) if n_forms > 0 else 0
        rules = frozenset(f for f in range(n_forms) if (rule_mask >> f) & 1)
        req_mask = rng.randrange(1 << n_req) if n_req > 0 else 0
        reqs = frozenset(reqs_all[i] for i in range(n_req) if (req_mask >> i) & 1)
        yield Regime(tokens, forms, insts, rules, reqs)


def regime_record(r: Regime) -> dict[str, object]:
    return {
        "n_data": r.n_data(),
        "forms": list(r.forms),
        "insts": sorted(([f, list(args)] for f, args in r.insts)),
        "rules": sorted(r.rules),
        "reqs": sorted(([i, j] for i, j in r.reqs)),
    }


def count_space(
    max_data: int = MAX_DATA,
    max_forms: int = MAX_FORMS,
    max_arity: int = MAX_ARITY,
    max_insts: int = MAX_INSTS,
) -> int:
    """Closed-form size of the enumeration, used to cross-check the bound.

    Independent of ``form_signatures``/``instance_slots``: the signature set is
    re-derived inline and the slot count is the arithmetic ``sum n_data**arity``,
    so this catches an under-enumeration in those two functions rather than
    sharing their blind spot.  The literal 56020 pinned in the tests is the
    ground-truth anchor.
    """
    total = 0
    for n_data in range(max_data + 1):
        n_req = n_data * (n_data - 1) // 2
        for n_forms in range(max_forms + 1):
            for arities in product(range(1, max_arity + 1), repeat=n_forms):
                n_slots = sum(n_data ** arity for arity in arities)
                max_k = min(max_insts, n_slots)
                n_inst_sets = sum(math.comb(n_slots, k) for k in range(max_k + 1))
                total += n_inst_sets * (1 << n_forms) * (1 << n_req)
    return total
