"""The seven mixed regimes from the sealed iso tests, as a named seed corpus.

Classification: deterministic computation.  These sit inside the declared
bound on size; they are not the exhaustive space.

AuthorityEffect: None.
"""

from __future__ import annotations

from derivation.iso import canonical, canonical_bruteforce
from derivation.model import (
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    Impose,
    Regime,
    replay,
)

from space import MAX_ARITY, MAX_DATA, MAX_FORMS, MAX_INSTS


def _mk(*events: object) -> Regime:
    return replay(list(events))  # type: ignore[arg-type]


def seed_corpus() -> tuple[Regime, ...]:
    """The mixed collection used by ``tests/test_iso.py``."""
    u_a = _mk(
        AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(0, 1),
        AdmitForm(1), AdmitInst(0, (0,)),
    )
    u_b = _mk(
        AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(0, 1),
        AdmitForm(1), AdmitInst(0, (1,)),
    )
    b_link = _mk(
        AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(0, 1),
        AdmitForm(2), AdmitInst(0, (0, 1)),
    )
    b_link_r = _mk(
        AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(0, 1),
        AdmitForm(2), AdmitInst(0, (1, 0)),
    )
    b_diag = _mk(
        AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(0, 1),
        AdmitForm(2), AdmitInst(0, (0, 0)),
    )
    f_out = _mk(
        AdmitDatum("<>"), AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(1, 2),
        AdmitForm(2), AdmitInst(0, (1, 0)),
    )
    f_in = _mk(
        AdmitDatum("<>"), AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(1, 2),
        AdmitForm(2), AdmitInst(0, (0, 1)),
    )
    return (u_a, u_b, b_link, b_link_r, b_diag, f_out, f_in)


def in_bounds(r: Regime) -> bool:
    return (
        r.n_data() <= MAX_DATA
        and len(r.forms) <= MAX_FORMS
        and all(arity <= MAX_ARITY for arity in r.forms)
        and all(arity >= 1 for arity in r.forms)
        and len(r.insts) <= MAX_INSTS
    )


def corpus_agreement() -> dict[str, object]:
    corpus = seed_corpus()
    # Compute each regime's two keys once (O(n)), not once per partner (O(n^2)).
    refined_keys = [canonical(r) for r in corpus]
    brute_keys = [canonical_bruteforce(r) for r in corpus]
    disagree = 0
    for i in range(len(corpus)):
        for j in range(i, len(corpus)):
            refined = refined_keys[i] == refined_keys[j]
            brute = brute_keys[i] == brute_keys[j]
            if refined != brute:
                disagree += 1
    return {
        "size": len(corpus),
        "in_bounds": all(in_bounds(r) for r in corpus),
        "pair_checks": len(corpus) * (len(corpus) + 1) // 2,
        "disagreements": disagree,
        "agreement": disagree == 0,
    }
