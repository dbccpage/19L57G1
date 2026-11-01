# Practice: memory, projection and permission

[Start at Lesson 65](65_memory_has_a_horizon.md) · [Answers after your attempt](AGENCY_ANSWERS.md)

Use a fresh two-item notebook, X and Y. Initially only Y is marked.
Each stated action computes a new notebook without changing its input.
The default authorizer is used unless a question supplies another policy.

1. A horizon-3 buffer receives four successful records, named a, b, c, d
   in that order. What remains, oldest first? Was action a undone?
2. Insert a refusal between c and d. Does that refusal occupy a memory
   slot or increment the controller's success count?
3. Give the controller budget 2 and a ceiling of one marked item. Offer
   “mark X” at cost 1. What projection is checked, and why is it refused?
4. In a fresh copy, raise the ceiling to two but supply an authorizer
   that always denies. Does viability by itself cause commitment?
5. At a two-mark ceiling, compare an empty license with a license listing
   the computed key for the “mark X” projection. Use the normal factory
   action with no supplied cached key. Which application is allowed?
6. With budget 1, offer “mark Y” at cost 1. What happens to the marks,
   budget and memory? Is the evaluator's model-change flag true?
7. Give the same no-change action cost zero and budget 1. Must this
   budget eventually be exhausted after repeated successes?
8. In a fresh copy, start with budget zero and offer a zero-cost action.
   What does the controller do before evaluating it?
9. A successful action has `has_empirical_reference=True`. Has a physical
   observation thereby occurred? State exactly what this Python flag compares.
10. Imagine using such a controller with a real labeling device. Identify
    one observation needed to connect a notebook update to a physical
    result, and one permission the model's license does not supply.

AuthorityEffect: None. The cases and budgets are supplied teaching data.
