# 56. A claim needs an interpretation

Use Reasoning 00–07 first. This optional route supplies an X301 research
model; the induction and instrument routes are not prerequisites.

Keep the three cards: A is blue and round, B is blue and triangular,
C is amber and triangular. In our model, positions 0, 1 and 2 name them.
The relation **blue** contains positions 0 and 1. These are supplied facts
in a mathematical example, not measurements made by the program.

Read **blue(x)** as “the card assigned to x is blue.” The expression is
a **formula**: a structured claim we can evaluate. The letter x leaves
one place to fill. An **assignment** tells us which position fills it.

| Formula | Assignment | Model answer |
|---|---|---|
| blue(x) | x names A | 1 |
| blue(x) | x names B | 1 |
| blue(x) | x names C | 0 |

<details><summary>Predict: does the written formula alone choose one of these answers?</summary>

No. Keep both the supplied relation and the assignment. With x naming C,
changing the model so that C belongs to blue changes the answer to 1.

</details>

## Read the answer with its conditions

Here 1 means that the formula meets the model's truth condition; 0 means
that it does not. **Semantics** names the interpretation that gives the
expression this meaning. Another interpretation requires another stated rule.

A stored message saying “A is blue” is another item of data. It can remain
unchanged while the relation changes. Listing the message does not establish
agreement between message and model, or between model and a physical card.
Those are separate comparisons.

Change x to B and change the claim to “x is round.” Explain why the answer
changes although the assignment still names B. Next, specify
[which cards a claim ranges over](57_name_the_domain.md).

AuthorityEffect: None. Supplied model interpretation; no physical observation.
