# Endogenous demand: the reqs channel

AuthorityEffect: None.  Outside the sealed derivation; consumes it read-only.
Not registered in `.github/workflows/verify.yml`.

**Outcome B** for class `C_reqs`, with an explicit **OPEN** remainder on the
instance channel.

A demand in the sealed machine is a member of `Regime.reqs`.  The event
language is the six constructors of `Event`.  Lean proves that a pair
enters `reqs` if and only if a successful `impose` of that pair occurs in
the replayed history (`replay_reqs_iff_impose`), and therefore that E2 of
the brief — a new requirement with no supplying `impose` at that step —
is unsatisfiable on this class (`e2_on_C_reqs_unsat`).  Responses
(`applyDelta`) never write `reqs`.  Both sealed Challenge-3 histories
(readings L and F) write `reqs` by `impose`, not by admission.

This is not a claim that nothing can ever be owed.  It is a claim about
the sealed `reqs` channel as E2 writes it.  A never-selects reader of
admitted instances (the represented-execution analogue) can return a pair
that is not in `reqs`; that is candidate I1, **OPEN**, and outside
`C_reqs`.  Closing it would need a grammar production of instances, or a
weakened E2 the brief does not state.

The word *endogenous* is the brief's word for E1 ∧ E2 ∧ E3 ∧ E4.  No row
of the candidate census is labelled that way.  Standing growth
(`SC-8`, `CL-IG-02`), declared closure (`CL-CLOSURE-POLICY`), and the
reflective generator (`generation_never_dries`) remain what those trees
said: not an object-language demand on this channel.  Dynamics
(sustained vs terminating) are not applicable inside `C_reqs`: there is
no generator there.

## Class `C_reqs`

Constructs whose demand is specified to be a member of `reqs` produced by
sealed `step` / `stepE`.  That is the class E2 writes down.  It is
inhabited by the obvious candidates a reader would try (C1–C9); each is
defeated by a named clause.  C10 (a new Event constructor) is outside
the sealed grammar and is not claimed as a member.

## Running

```powershell
cd research/endogenous_demand
python verify.py
```

Regenerate records deliberately, never under a live injection:
`python run.py --write`, `python verify_lean.py --write`.

## Pins

Baseline `cea346d7f3603fd8da374947e76c9b3cd426d122` (`origin/main` at
produce).  Consumed trees: `code/derivation`, `lean4/Derivation`.
`prompt/` and `paper/` are not pinned.

## Not claimed

* Outcome A: no generator on `C_reqs` is exhibited.
* Impossibility of every conceivable instance-encoded read (I1 remains OPEN).
* Second-stake E4 invariance (leftover of that tree; a host `Labeler` even if checked).
* Any sealed-path amendment, any `mathlib` import, any CI registration.
