# STATUS — diagonal identity

AuthorityEffect: None. Outside the sealed derivation; consumes it read-only.

## Terminal

`DUAL_NOT_IDENTITY_ON_DECLARED_CARRIERS`

Pair-id (non-injectivity of a map on a related pair, plus `Irrefl` failure
of `Push`) and family-miss (non-surjectivity of a `Nat`-indexed family) both
hold on their declared carriers and do not recode each other. The
square-then-flip combinator packages the covering side only. Identity of
`PrimDiff.obstruction_under_irrefl` with `Covering.seq_uncountable` is **not**
proved. A sibling ledger item about that identification remains `[OPEN]`;
this tree does not close it.

## What is proved here

1. Covering-miss, restated without `Metric`: `diagonal_bool`,
   `seq_uncountable`, `thread_uncountable`, `not_surjective_nat_to_thread`.
   Formulas match `research/unboundedness/lean/Continuum.lean` by source
   comparison (`diagBool`, `flipFin`, `diagSeq`, `diagThread`).
2. Combinator packaging: `diagBool f = diagFlip (fun b => !b) f` and
   `diagSeq = diagFlip (flipFin …)` by `rfl`. `diagFlip_ne_row` uses
   `∀ a, flip a ≠ a`.
3. Collapse inhabitant: `d2_constant_obstructs` is
   `obstruction_under_irrefl D2_witness rfl` at `Bool → Unit`.
4. Split conjunctions: `collapse_yes_covering_no` and
   `family_miss_and_identifying_push`. Not an `Iff` of the two theorem types.
5. Dual on declared carriers (`DiagonalIdentity.Dual`):
   - `d2Const` is not injective; `PairIdObstruction D2 d2Const` holds;
     `Push D2 d2Const` has a self-loop.
   - `d2Const` is not a covering family: `IdentifyingMapAsCoveringFamily`
     requires `Bool = Nat`, which `bool_ne_nat` refutes.
   - Every `S : Nat → (Nat → Fin c)` (`c ≥ 2`) is not surjective;
     `FamilyMiss c S (diagSeq c hc S)` holds; the missed row is `diagFlip`.
   - No such `S` is the D2 constant map:
     `CoveringFamilyAsD2Const` requires
     `(Nat → (Nat → Fin c)) = (Bool → Unit)`, refuted.
   - Package: `dual_on_declared_carriers`.

## What is not proved

- A common lemma of which both objects are instances.
- A share-bridge instantiating `diagFlip` at PrimDiff binders `(r, c)`.
- A relation on `Thread` whose collapse recodes covering-miss.
- Cardinality of `Thread c`, or any injection with `Nat → Bool`.

## Import style

Sealed staging, not a Lake path into `lean4/`. `Limits.lean` is staged the
same way. `Continuum.lean` is pinned for formula comparison and is not
compiled.

Snapshot: `0ab0e67037900606159ec2babb2e7cf5b7854f20`.
