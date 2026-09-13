# Claim ledger — covering-miss versus identifying-push

AuthorityEffect: None.

Classifications are exactly one of: proved theorem, finite computation, open.
Identity of the two objects is not a row with class proved theorem.

| ID | statement | class | evidence |
|---|---|---|---|
| DI-01 | For `c ≥ 2`, no family `Nat → (Nat → Fin c)` covers `Nat → Fin c`; no family `Nat → Thread c` covers `Thread c`. Non-enumerability only. | proved theorem | `DiagonalIdentity.Covering.diagonal_bool`, `DiagonalIdentity.Covering.seq_uncountable`, `DiagonalIdentity.Covering.thread_uncountable`, `DiagonalIdentity.Covering.not_surjective_nat_to_thread` |
| DI-02 | `diagBool` and `diagSeq` are `diagFlip` at boolean negation and at `flipFin`, by `rfl`. If `flip` has no fixed point, the combinator differs from every row. | proved theorem | `DiagonalIdentity.Combinator.diagBool_is_diagFlip`, `DiagonalIdentity.Combinator.diagSeq_is_diagFlip`, `DiagonalIdentity.Combinator.diagFlip_ne_row` |
| DI-03 | Identifying the witnessed pair of `D2` along `Bool → Unit` is `FidelityObstruction Irrefl`. The pushforward of a witnessed identifying map is not irreflexive and holds of a self-pair. | proved theorem | `DiagonalIdentity.Collapse.d2_constant_obstructs`, `DiagonalIdentity.Collapse.identifying_push_not_irrefl`, `DiagonalIdentity.Collapse.identifying_push_self_loop`, sealed `PrimDiff.obstruction_under_irrefl` |
| DI-04 | The covering-miss facts and the identifying-push facts hold together. The conjunction does not identify the two theorem types. | proved theorem | `DiagonalIdentity.Split.collapse_yes_covering_no`, `DiagonalIdentity.Split.family_miss_and_identifying_push` |
| DI-05 | Covering definitions `diagBool`, `flipFin`, `diagSeq`, `diagThread` match the formulas in `research/unboundedness/lean/Continuum.lean`. | finite computation | `test_covering_formulas_match_continuum`, `diagonal_identity.formulas_match` |
| DI-06 | Identity of `PrimDiff.obstruction_under_irrefl` with `Covering.seq_uncountable` is not proved. | open | `STATUS.md` terminal `DUAL_NOT_IDENTITY_ON_DECLARED_CARRIERS`; `test_standing_refuses_identity_and_wrong_terminal` |
| DI-07 | On the declared carriers, pair-id at `D2`/`d2Const` is non-injectivity plus `Irrefl` failure of `Push`, and is not a covering family (`Bool ≠ Nat`). Family-miss at `diagSeq` is non-surjectivity of `S : Nat → (Nat → Fin c)`, is not the D2 constant map, and the missed row is `diagFlip`. | proved theorem | `DiagonalIdentity.Dual.dual_on_declared_carriers`, `DiagonalIdentity.Dual.d2Const_not_injective`, `DiagonalIdentity.Dual.d2Const_not_as_covering_family`, `DiagonalIdentity.Dual.family_not_surjective`, `DiagonalIdentity.Dual.family_not_as_d2_const`, `DiagonalIdentity.Dual.covering_miss_witness_is_diagFlip` |
