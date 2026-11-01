# 58. Read the score rule

A number between zero and one needs an interpretation. Read
[Number 09](../number_lab/09_equal_pieces.md) if halves are unfamiliar.
We now inspect X301's separate truth-score operations. This is a supplied
mathematical scoring rule, not a measured amount of evidence.

For this example use scores 0, 1/2 and 1. “And” takes the smaller score;
“or” takes the larger. Negation, written “not,” follows this rule:

| Score of the claim | Score of its negation | Larger of the two |
|---|---|---|
| 0 | 1 | 1 |
| 1/2 | 0 | 1/2 |
| 1 | 0 | 1 |

<details><summary>Predict: must a score of 1/2 give its negation a score of 1/2?</summary>

No. The defined negation gives 1 only when the original score is zero;
otherwise it gives zero. It is not the subtraction rule “one minus the score.”

</details>

## Distinguish three questions

“Is the score exactly 1?” differs from “Is it exactly 0?” At 1/2 both
answers are no. A program branch that treats only 1 as true must not
turn every other score into the mathematical claim “score equals zero.”

The score 1/2 also does not mean “one success in two trials.” A chance
model needs its own outcomes, preparation and response rules. A learning
or observation claim needs evidence connecting the score to records.

## Keep the two source implementations separate

X301's Python score type accepts exact rational numbers. Its formula
evaluator starts with binary relation/identity answers and combines those
answers using the declared operations; it does not supply half-valued
atoms. The Lean model instead permits relation values 0, half and 1.
These are different model definitions. Sharing a name does not prove
that either implementation represents the other.

Next, change an input and [compare before with after](59_change_and_compare.md).

AuthorityEffect: None. Supplied truth-score rules; no frequency interpretation.
