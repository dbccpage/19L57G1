# research/alpha_engine

AuthorityEffect: None.

Outside the sealed derivation.  Consumes sealed `code/derivation` **by
import** (the six runtime modules named in `SOURCE_MANIFEST.json`).  It
does not copy those modules, does not claim proved equivalence to them,
and does not amend `prompt/`, `paper/`, `code/`, `lean4/Derivation/`, or
`artifacts/`.

This tree is a **local receipt**.  It is **not** gate 11: it is not
listed in `.github/workflows/verify.yml`, and `research/README.md` is
outside this write root.

## Proposal, evaluation, authorization

Proposal, evaluation, and authorization are distinct.

- A `Proposal` is Supply-shaped: recording it changes no admitted state.
- `evaluate` enumerates sealed `min_responses`, quotients with ephemeral
  children, and retains every iso class.  It never admits.  A score is
  not a license.  Grades `Tie` / `UniqueClass` / `UniqueDelta` / `None`
  are not returned and are not licenses.
- A `License` names a granter, a scope, and authorized `CanonKey`s.  It
  is not an `Event`.  There is no revoke API and no integer class
  selector.  A License of a sole class is still an apply.
  *2026-09-25:* a `License` also records the declaration it authorizes
  (source history digest, target, measure, bounds) and applies only
  there; Driver A checks the parent's replay, recomputes the evaluation
  from the sealed kernel and executes the recomputed member, never the
  caller's.  See the closeout audit in `STATUS.md`.

The PEA JSON keys are a record layout, not a proof of temporal
order.  The fold's recorded `compute_order` is evaluate, wrap minima as
a Proposal, present, License, explore.

Driver A explores only licensed keys and expands by sealed `Admit*` /
`Impose` replay onto a **new** `Node`.  Unique minima remain proposals.
Demand generation and OB-1 stay **OPEN**.  Driver B (any lift that would
need a new sealed `Event` kind) is **OPEN** and unimplemented.

## Running

```powershell
cd research/alpha_engine
python verify.py
```

Regenerate the PEA record deliberately, never under a live
injection: `python run.py --write`.  Local Lean about this harness
(License is not Event; SearchPolicy is a subset; uniqueness does not
apply) is `python verify_lean.py --check`.  Those lemmas are not a
proved equivalence to `code/derivation/`.

2026-09-25: `python verify.py` is the one command that verifies the Alpha
reference slice described in `docs/ALPHA_HANDOFF.md`.  It also runs
`python handoff_demo.py --check` (four demonstrations on the
Challenge-3 fixtures, each independently checked; regenerate with
`--write`, never under a live injection) and the sealed kernel's own
tests of the six consumed modules.  The live injections of the
closeout repairs are `python inject_boundary.py`, run on a clean
worktree; `verify.py` never runs them.
