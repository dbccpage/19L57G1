# Thinghood research packet -- status

A packet that supplies an agent prompt for one construction run.  It
does not itself answer the questions.  It records the boundary under
which an agent may begin building.

## Repository boundary

This tree is an explicitly non-sealed research surface.  It must not
modify or regenerate anything under `prompt/`, `paper/`, `code/`,
`lean4/Derivation/`, or `artifacts/`.

It follows the precedent of the sibling trees
`research/primitive_difference_tower/`, `research/portable_interface/`,
`research/blind_restart/`, `research/partial_decide/`, and
`research/genesis_continuation/`.  Vocabulary is taken from
`research/genesis_continuation/native_terms.md` plus the native names
already fixed in `lean4/Derivation/PrimDiff.lean` and
`lean4/Derivation/PrimitivePassage.lean`.  The prompt introduces the
caller-supplied word **thing** as an externally imposed challenge, not
as a derived object.

Nothing external is named here.

## What is here

- `PROMPT.md` -- the whole of what a solver is given.  Demands,
  refusals, and a reply format.  No winning candidate is tabulated.
- `STATUS.md` -- this boundary note

## What is not here yet

No Python, no Lean, no receipt, no claim ledger.  Those are the run's
outputs, written under this directory only.  This tree is **not** named
by `.github/workflows/verify.yml`'s research job.  Until an executable
surface exists and is separately registered, receipts here go stale
silently.

## How to run

Paste `PROMPT.md` into a solver that can write this repository.  The
solver works only under `research/thinghood/`.  It does not amend
`CLAUDE.md`, does not touch sealed prompt bytes, and does not close
`OB-1`.

## Nonclaims

- Supplying the prompt is not a derivation of a thing.
- Restating `FidelityObstruction` is not an answer to "what is a thing?".
- `two_rule` is not a dynamical law of the inscription.  The prompt
  forbids treating it as one.  That prohibition is a run rule, not a
  new theorem.
- `OB-1` remains open.  This packet does not change it.
