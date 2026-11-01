"""Unit 19 check: the binary link separates the two data.

Runs Genesis's own Python model. This is sample computation, not a proof;
the proof is Derivation.BL_separable. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u19_link.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.candidates import (  # noqa: E402
    Bounds,
    NewForm,
    NewInst,
    NewRuleAll,
    NodeView,
    apply_delta,
    response_valid_fast,
    response_valid_naive,
)
from derivation.engine import GENESIS_L  # noqa: E402
from derivation.model import AdmitDatum, AdmitRuleAll, Impose, replay, step  # noqa: E402
from derivation.observe import (  # noqa: E402
    contexts,
    derivable,
    plug,
    profile,
    satisfies,
    separable,
    witness,
)


def main() -> int:
    failures: list[object] = []
    base = replay(GENESIS_L)
    delta = (NewForm(2), NewInst(0, (0, 1)))
    bl = apply_delta(base, delta)
    print(f"BL: forms={bl.forms} insts={sorted(bl.insts)} data={bl.data}")

    # 1. The five contexts of a binary form over two data, and what each
    # plugging derives.
    ctxs = contexts(bl)
    print(f"contexts: {len(ctxs)}")
    for c in ctxs:
        d0, d1 = derivable(bl, plug(c, 0)), derivable(bl, plug(c, 1))
        print(f"  {c}: plug 0 -> {plug(c, 0)} {d0}; plug 1 -> {plug(c, 1)} {d1}"
              f"{'  <- witness' if d0 != d1 else ''}")
    witnesses = [c for c in ctxs
                 if derivable(bl, plug(c, 0)) != derivable(bl, plug(c, 1))]
    print(f"witnesses: {witnesses}; first (Genesis's witness()): "
          f"{witness(bl, 0, 1)}")
    if (len(ctxs) != 5 or witnesses != [(0, (None, 1)), (0, (0, None))]
            or witness(bl, 0, 1) != (0, (None, 1))):
        failures.append("contexts")

    # 2. Profiles differ; the demand is met.
    p0, p1 = profile(bl, 0), profile(bl, 1)
    print(f"profile(0)={sorted(p0)} profile(1)={sorted(p1)} "
          f"separable={separable(bl, 0, 1)}")
    demanded = step(bl, Impose(0, 1))
    print(f"satisfies after Impose(0, 1): {satisfies(demanded)}")
    if not separable(bl, 0, 1) or not satisfies(demanded):
        failures.append("separable")

    # 3. The delta is a valid response, and so is its mirror image.
    view = NodeView.of(base)
    for d in (delta, (NewForm(2), NewInst(0, (1, 0)))):
        ok = response_valid_fast(view, (0, 1), d)
        print(f"valid response {d}: {ok}")
        if not ok:
            failures.append(("valid", d))

    # 4. A form of arity 2 with no instance does not separate (Unit 18).
    form_only = apply_delta(base, (NewForm(2),))
    print(f"form alone: contexts={len(contexts(form_only))}, "
          f"separable={separable(form_only, 0, 1)}")
    if separable(form_only, 0, 1):
        failures.append("form-only")

    uniform = step(bl, AdmitRuleAll(0))
    still_valid = response_valid_naive(demanded, (0, 1), (NewRuleAll(0),))
    print(f"uniform rule retains link={uniform.insts == bl.insts}; "
          f"separable={separable(uniform, 0, 1)}; valid response={still_valid}")
    if uniform.insts != bl.insts or separable(uniform, 0, 1) or still_valid:
        failures.append("uniform rule counterexample")

    # A separate three-datum example: validity must meet both stored requests.
    pending = replay([AdmitDatum(t) for t in ("A", "B", "C")]
                     + [Impose(0, 1), Impose(1, 2)])
    for marked, expected in ((0, (True, False)), (1, (True, True))):
        plan = (NewForm(1), NewInst(0, (marked,)))
        result = apply_delta(pending, plan)
        pairs = (separable(result, 0, 1), separable(result, 1, 2))
        slow = response_valid_naive(pending, (0, 1), plan)
        fast = response_valid_fast(NodeView.of(pending), (0, 1), plan)
        if pairs != expected or slow != all(expected) or fast != slow:
            failures.append(("all stored requests", marked, pairs, slow, fast))
        print(f"three-data mark {marked}: pair answers {pairs}, valid={slow}, "
              f"requests retained={result.reqs == pending.reqs}")
        if result.reqs != pending.reqs:
            failures.append("repair changed the request set")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
