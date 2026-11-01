# Answers: supports and withdrawal

[Practice](REVISION_PRACTICE.md) · [Reasoning lab](README.md)

1. Each fixed rule has empty hypothesis support. Q and R each have
   support a. Both fixed rules remain assumptions in the derivation;
   empty hypothesis support does not remove them.
2. The conflict support is a/b. Withdrawing a and withdrawing b are the
   two tied minimum candidates. The default selector chooses a by name order.
3. The a/P record, its Q record and its R record become inactive. The b
   record and both fixed rules remain. Withdrawing P supplies no proof
   of not-P; losing a derivation of Q supplies no proof of not-Q.
4. Withdraw b: the candidates remove one name each, and b has lower cost.
   The cost is supplied policy, not evidence about the lamp reports.
5. The supports are a/b and b/c. Removing a leaves the b/c conflict.
   Withdrawing b alone hits both; withdrawing a and c also hits both
   but removes two names. The only one-name solution is b.
6. Withdraw a. One name precedes two names in the comparison, even
   though its assigned cost 9 exceeds their combined cost 2.
7. No. The Python scan compares recorded claims; it does not automatically
   infer Q from the recorded rule and P. Once that inference is recorded,
   Q and not-Q give a detected conflict. An unrecorded consequence was
   not disproved by the earlier empty scan.
8. No. The conflict has empty hypothesis support. There is no hypothesis
   name to hit. The source reports a foundational-inconsistency error;
   revising the fixed setup is outside this operation.
9. No. The a-supported record becomes inactive, while the c-supported
   record remains. Their common sentence does not give them common support.
10. For example, the notebook may contain a mistaken “lamp lit” report
    without any contrary entry. A fresh inspection of the identified
    lamp at the specified time could challenge that report, provided
    its procedure, raw reading and interpretation are documented.
    Another valid answer could investigate a mistaken fixed rule.

Questions 1–9 have executable book controls. Question 10 asks for application
reasoning; no physical trial or reader result is recorded here.

Return to the [reading path](../learning_path.md).

AuthorityEffect: None. Answers concern the supplied notebooks.
