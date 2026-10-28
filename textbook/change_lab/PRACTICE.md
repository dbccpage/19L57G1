# Practice: preserve the right distinctions

[Change lab](README.md) · [Separate answers](ANSWERS.md)

A new passage ledger has three admitted positions K, L, M. All three
pair records were asserted and retained. K/L and K/M are protected.
The only observation column is `[L]`. Budget is one, permission is off,
and the machine is not halted. These are supplied conditions.

1. Write the Yes/No answers to the column on K, L, M. Which protected
   pair is active? Give all four conditions that make it active.
2. Try adding M to the old `[L]` column. Does this preserve the already
   separated protected pair? Can it execute with permission off?
3. Return to the original state and also protect L/M. Reconsider the
   same repair. Identify exactly why it fails now.
4. With all pairs protected, propose a new column `[K]`. Give its
   structural effect. Which remaining gate prevents its execution?
   What happens if permission is on but the budget is zero instead?
5. In the original state, record a refusal of the active pair. Is that
   record evidence that every existing repair failed? Explain using
   your answer to question 2.
6. In the all-protected state, list the two singleton proposals for the
   active pair. Would `[K,L]` also qualify as a new column? Explain why
   it is absent from that singleton proposal family.
7. Someone writes a raw record with K/M protected but not retained.
   Can these passage events construct it from genesis? Give the reason,
   rather than merely pointing to the fact that its fields can be written.
8. Halt the all-protected state. Its proposal generator still lists
   column blocks. Do those lists establish that a later block executes?
   Explain the difference between the generator and the guarded step.

For transfer, invent a recorder task where one old distinction must be
preserved. State a proposed question change, one condition on its
execution, and a measurement that could show the intended correspondence
has failed. This exercise supplies no result about a real recorder.

AuthorityEffect: None. Try these tasks before opening the answers.
