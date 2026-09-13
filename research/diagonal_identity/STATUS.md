# STATUS — diagonal identity

AuthorityEffect: None. Outside the sealed derivation; consumes it read-only.

## Terminal

`TYPED_SPLIT_RECORDED_IDENTITY_NOT_PROVED`

Identity of `PrimDiff.obstruction_under_irrefl` with `Covering.seq_uncountable`
(or `Covering.thread_uncountable`) is **not** proved. The two objects, as
typed, are a split. A sibling ledger item about that identification remains
`[OPEN]`; this tree does not close it.

## What is proved here

1. Covering-miss, restated without `Metric`: `diagonal_bool`,
   `seq_uncountable`, `thread_uncountable`, `not_surjective_nat_to_thread`.
   Formulas match `research/unboundedness/lean/Continuum.lean` by source
   comparison (`diagBool`, `flipFin`, `diagSeq`, `diagThread`).
2. Combinator packaging: `diagBool f = diagFlip (fun b => !b) f` and
   `diagSeq = diagFlip (flipFin …)` by `rfl`. `diagFlip_ne_row` uses
   `∀ a, flip a ≠ a`. This does not give PrimDiff binders `(r, c)`.
3. Collapse inhabitant: `d2_constant_obstructs` is
   `obstruction_under_irrefl D2_witness rfl` at `Bool → Unit`.
4. Split: `collapse_yes_covering_no` and `family_miss_and_identifying_push`
   are inhabited conjunctions. They are not an `Iff` of the two theorem types.

## What is not proved

- A common lemma of which both objects are instances.
- A share-bridge instantiating `diagFlip` at `(r, c)`.
- A relation on `Thread` whose collapse recodes covering-miss.
- Cardinality of `Thread c`, or any injection with `Nat → Bool`.
- That `Continuum.lean` lives under `research/coherent_process_limits/lean/`
  — that path is absent; the live file is under `research/unboundedness/lean/`.

## Import style

Sealed staging, not a Lake path into `lean4/`. `Limits.lean` is staged the
same way. `Continuum.lean` is pinned for formula comparison and is not
compiled (it imports `Metric`, which pulls `Periodic` and the rest of that
family).

Snapshot: `0ab0e67037900606159ec2babb2e7cf5b7854f20`.
