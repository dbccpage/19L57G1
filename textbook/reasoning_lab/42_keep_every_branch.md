# 42. Keep every branch

An A procedure has two branches. If A=0, their chances are 1/4 and 3/4.
If A=1, their chances are 3/4 and 1/4.

**Predict:** at each fixed A value, what is the sum of the two branch
chances? Must each branch's weights across different A values sum to one?

<details><summary>Check your prediction</summary>

At each A value, the two branches sum to one. That is the required
condition. A branch is an effect, so its cross-outcome sum has no such
requirement. For example, a certain branch has weights 1,1 and its
impossible complement has weights 0,0.

</details>

Effects whose weights sum to one at every input form a **partition of the
unit effect**. They account for every branch of the stated procedure.
When evaluating a joint A/B preparation, adding all A-branch contributions
uses that full sum, one, at each A value. The result agrees with using
the A unit effect while keeping the same B response.

This is an algebraic identity for the supplied joint table and effects.
The code defines no state-changing measurement update here. It therefore
does not establish the behavior of every physical intervention at A.

**Change one thing:** keep only the first branch with weights 1/4,3/4,
and call it the entire partition. Does the original sum identity apply?

<details><summary>Check the changed example</summary>

No. Its weight is below one at both inputs. The native verifier refuses
this incomplete partition; it does not silently renormalize the branch.
Keeping only one result asks a different question.

</details>

Next: [sum out A before reading B](43_sum_out_a_before_reading_b.md).

AuthorityEffect: None. Full-branch valuation identity, not a dynamics theorem.
