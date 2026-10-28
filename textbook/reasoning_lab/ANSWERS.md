# Worked answers

[Practice](PRACTICE.md) · [Reasoning lab](README.md)

1. On K, L, M, red implies sealed: the only red-Yes row, K, is sealed-Yes.
   The reverse fails at L: sealed Yes, red No.
2. No. Both red-to-sealed and sealed-to-red must pass. L breaks the latter.
3. Yes: numbered and not-red both read No, Yes, Yes. This checks the
   three supplied rows; it does not establish a rule for unlisted packets.
4. No. K and L both give sealed Yes but their red answers differ. A
   recovering function would need two outputs on the same input Yes.
5. Yes. On K and M, return Yes for sealed Yes and No for sealed No.
   Adding L would invalidate that rule. The domain is part of the claim.
6. K witnesses “some.” L or M refutes “every.” On the empty domain,
   “some” has no witness and is false; “every” has no counterexample
   and is true under the declared convention. This establishes no red
   packet's existence.
7. K/L: red separates; K/M: red or sealed separates; L/M: sealed
   separates. Each pair has a witness. Red fails on L/M and sealed
   fails on K/L, so neither is one common witness for all pairs.
8. There are no pairs of different packets, so the each-pair condition
   has no counterexample. There is also no available question; the
   common-witness existence condition is false. Empty pair and empty
   question domains play different roles.
9. No. Not yet supplying the hypothesis leaves this use of the theorem
   unavailable. It does not establish that its conclusion is false.
   A specific blocking pair can establish impossibility of this recovery
   task, as K/L did for the whole list.
10. A new packet N with red Yes and sealed No is a counterexample on
    the enlarged list. A device test would additionally need specified
    procedures for both labels, a domain, actual readings, and a way
    to handle missing or inconsistent responses. The printed row alone
    is no measurement of a physical packet.

AuthorityEffect: None. The conclusions retain the stated finite domains.
