# 06. Carry the hypotheses with the conclusion

[Previous](05_order_of_questions.md) · [Reasoning lab](README.md) · [Next](07_evidence_for_a_claim.md)

## Predict first

Suppose we claim: “If two cards have the same blue answer, they have
the same round answer.” Which pair could test this claim?

## Read a theorem as a conditional promise

A **hypothesis** is a condition a result requires. A **conclusion** is
what the result establishes when those conditions hold. A **theorem**
is a statement established by a proof in its stated mathematical setting.

For the proposed claim, the hypothesis for a pair is that its blue
answers agree. The conclusion is that its round answers agree. A/B
satisfies the hypothesis but fails the conclusion. That refutes this
claim on our domain.

## One useful result, with its conditions

Suppose the round answer really can be recovered by one function from
the kept answer, for every card in a declared domain. Then cards with
the same kept answer must have the same round answer.

Why? Equal kept answers give the recovering function the same input.
One function gives that input one output. Thus the recovered answers
agree. The source map names the exact factorization definitions and result.

The recovery function and its correctness on every domain member are
hypotheses. Merely saying “recovery” does not supply them. Our A/B
counterexample shows that those hypotheses cannot hold when only blue
is kept and round is requested on all three cards.

## A missing hypothesis leaves a question open

If the result requires a recovering function and none has been supplied,
we cannot use the result yet. This alone does not prove its conclusion
false. A failed implication needs a case with its hypotheses satisfied
and its conclusion false.

## Your turn

For the smaller domain A and C, give a recovery function from blue to
round. Explain why this does not contradict failure on A, B, C.

AuthorityEffect: None. The result is conditional on its declared domain and recovery map.
