# Worked practice answers

[Questions](PRACTICE.md) · [Change lab](README.md)

1. K: No; L: Yes; M: No. K/M is active: its pair record is retained,
   it is protected, an observation is declared, and the observation
   does not distinguish K from M. K/L is already separated.
2. The column becomes `[M,L]`, with answers No, Yes, Yes. K/M separates
   and K/L stays separated. The event is a structural repair and can
   execute with the supplied budget one and no halt. Permission does
   not gate an existing-column refinement in this kernel.
3. L/M was separated by the old column but both now answer Yes. The
   repair would destroy a protected separation, so the structural guard
   fails. Turning on permission would not fix that failure.
4. Appending `[K]` keeps the old `[L]` answers and distinguishes K/M.
   It meets the column guard, but permission is off. With permission
   on and budget zero, the budget gate still prevents execution.
5. The refusal is recordable because K/M is active. This kernel does
   not demand an exhausted repair menu for refusal. Question 2 exhibits
   an existing repair, so the stronger interpretation is false here.
6. `[K]` and `[M]` are the singleton proposals. `[K,L]` also separates
   K/M and can be appended under the structural column guard. It is
   not a singleton, so it is outside that declared proposal family.
7. No. Protection is added only for a retained pair, and retained pairs
   never leave the store. The book's Lean invariant establishes this
   for all histories of the declared passage events, starting at genesis.
8. No. The generator reads the outstanding active pairs and can list
   proposals after halt. The step function first checks the halt flag
   for these events and leaves the state unchanged. A listed block is
   different from successful execution of the block.

A transfer example might involve a parcel sensor replacement that must
preserve destination distinctions. Its installation needs a declared
resource and authorization process. A differently destined pair receiving
the same recorded pattern would challenge the proposed measurement
correspondence. Actual sensor behavior, error rates, and authority are
not established by the passage's supplied columns or Boolean switch.

AuthorityEffect: None. These answers concern the stated exercise.
