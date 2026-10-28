"""Unit 57 check: the interpreter boundary, mirrored finitely.

Runs Genesis's mirror of `InterpreterBoundary` (the 64-member family,
the notes-diagonal, the typed-refusal top, the declared boundary
setting) and adds two Python (book) observations: the diagonal agrees
with every member on the operational support (`supp`), and the
"arbitrary uncoded assignment" is satisfied by any two different
functions at once. Compares the report with
`artifacts/primitive_interpreter.json`.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u57_interpreter_boundary.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.interpreter_boundary import (  # noqa: E402
    BASIS,
    DUP_WORLD,
    KERNEL_DESC,
    NOTE_EVENT,
    all_descs,
    candidate_a,
    candidate_f,
    carrier,
    collapse_obstructed,
    diag,
    diagonal_misses_all,
    distinct_on_basis,
    eval_opt,
    index_world,
    interp_step,
    interpreter_report,
    self_description_on_basis,
)
from derivation.represented import World, step  # noqa: E402


def supp(w: World) -> tuple:
    """Python (book): the operational support, every field but notes
    (mirror of `Represented.supp`)."""
    return (w.data, w.views, w.reqs, w.refusals, w.budget, w.aug_licensed)


def main() -> int:
    failures: list[str] = []
    descs = all_descs()
    print(f"family size {len(descs)}; kernel index {descs.index(KERNEL_DESC)}")
    if len(descs) != 64 or descs.index(KERNEL_DESC) != 63:
        failures.append("family")

    sd = self_description_on_basis()
    dist = distinct_on_basis()
    print(f"kernel code executes to the sealed step on the basis: {sd}; "
          f"distinct behaviours on the basis: {dist}")
    if not sd or dist != 64:
        failures.append("basis")
    # Python (book): the same six probes, stated event by event
    eventwise = all(interp_step(KERNEL_DESC, w, e) == step(w, e) for (_, w, e) in BASIS)
    print(f"  eventwise equality on all six probes: {eventwise}")
    if not eventwise:
        failures.append("eventwise")

    # the diagonal
    f = lambda w, e: diag(descs, w, e)  # noqa: E731
    misses = diagonal_misses_all(f, descs)
    fake = diagonal_misses_all(lambda w, e: interp_step(descs[5], w, e), descs)
    print(f"diagonal misses all 64 at their indexed worlds: {misses}; "
          f"a copy of member 5 misses all: {fake}")
    if not misses or fake:
        failures.append("diagonal")
    w63 = index_world(63)
    d_out, k_out = f(w63, NOTE_EVENT), interp_step(KERNEL_DESC, w63, NOTE_EVENT)
    print(f"  at index 63 (the kernel): diagonal notes {d_out.notes}, kernel notes {k_out.notes}")
    if d_out.notes != (0, 999) or k_out.notes != (0,):
        failures.append("notes")
    # Python (book): on the support the two agree, at every index
    supp_agree = all(
        supp(f(index_world(i), NOTE_EVENT)) == supp(interp_step(descs[i], index_world(i), NOTE_EVENT))
        for i in range(64)
    )
    print(f"  Python (book): diagonal and member agree on supp at all 64 indices: {supp_agree}")
    if not supp_agree:
        failures.append("supp")
    off = f(index_world(64), NOTE_EVENT)
    print(f"  off the index range (64 data) the diagonal returns its input: {off == index_world(64)}")
    if off != index_world(64):
        failures.append("off-range")

    # the typed-refusal top
    top = eval_opt(None, DUP_WORLD, NOTE_EVENT)
    coded = eval_opt(KERNEL_DESC, DUP_WORLD, NOTE_EVENT)
    print(f"evalOpt none -> {top}; evalOpt kernel == interpStep kernel: "
          f"{coded == interp_step(KERNEL_DESC, DUP_WORLD, NOTE_EVENT)}")
    if top is not None or coded != interp_step(KERNEL_DESC, DUP_WORLD, NOTE_EVENT):
        failures.append("evalOpt")

    # the declared boundary setting
    ca, cf = candidate_a(), candidate_f()
    constant = collapse_obstructed(lambda _x: 0)
    is_some = collapse_obstructed(lambda x: 0 if x is None else 1)
    print(f"carrier {len(carrier())}; A {ca}; F {cf}; collapse by a constant obstructed: "
          f"{constant}; by isSome (endpoints kept apart): {is_some}")
    if len(carrier()) != 65 or not (ca and cf and constant) or is_some:
        failures.append("boundary")

    # Python (book): two different functions both complete the carrier
    def assign(fn):
        return lambda c, w, e: fn(w, e) if c is None else interp_step(c, w, e)
    i1 = assign(lambda w, e: w)
    i2 = assign(f)
    both = (
        all(i1(d, w63, NOTE_EVENT) == interp_step(d, w63, NOTE_EVENT) for d in descs)
        and all(i2(d, w63, NOTE_EVENT) == interp_step(d, w63, NOTE_EVENT) for d in descs)
        and i1(None, w63, NOTE_EVENT) != i2(None, w63, NOTE_EVENT)
    )
    print(f"  Python (book): two assignments to the uncoded role, both covering the "
          f"family, disagreeing at none: {both}")
    if not both:
        failures.append("assignment")

    art = json.loads((ROOT / "artifacts" / "primitive_interpreter.json").read_text())
    rep = interpreter_report()
    print(f"report equals artifact: {rep == art}; terminals {rep['terminals']}")
    if rep != art:
        failures.append("artifact")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
