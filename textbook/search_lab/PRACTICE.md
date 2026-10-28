# Practice: make a repair and defend its scope

[Search lab](README.md) · [Separate answers](ANSWERS.md)

Use a fresh ledger with three admitted entries U, V, W, one one-slot form
P, the single recorded instance `P(U)`, and no uniform rules. Both U/V
and U/W are imposed separation requirements. A new demand asks for V/W.

1. Give the current answers to `P(_)`. Does writing the V/W demand change them?
2. Consider recording `P(V)` on the old form. Which pair would lose its
   distinction? Is the instance ill-formed, or is the response invalid?
3. Allow at most one item and forms of at most two slots. Explain why no
   response works. Consider new entries, new forms, existing-form instances,
   and the all-tuples rule separately.
4. Allow two items. Give a working plan using a new one-slot form Q. State
   a witness for V/W and check both old required pairs.
5. Compare your plan's prices under mu1 and mu2 with a plan adding a
   two-slot form R and recording `R(V,V)`. Do both satisfy the requirements?
6. A person reports that the original two-entry example has exactly three
   item-count minimum classes, without giving an arity bound. What must be
   repaired in that statement? Use the recorded arity-three case to give
   a specific counterexample to the unrestricted count.
7. A graph export passes event replay. Its author then claims every price
   annotation is correct and every possible future branch was explored.
   Explain which further checks and scope statements would be needed.

Finally, propose an investigation involving a real recorder. State the
distinctions to preserve, what would be changed, and what observations
would count against your proposed repair. The formal exercise supplies
no empirical answers to that investigation.

AuthorityEffect: None. These are declared finite exercises.
