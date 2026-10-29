# Answers: change the table

1. P gives yes on X and dash on Y. Q works in the opposite direction.
   Either question witnesses the unequal profiles.
2. Add P(Y) and Q(X), for two items. Doing nothing leaves two mismatches.
   One instance can repair only one. One uniform rule can repair one
   column, leaving the other mismatch. A fresh datum alone cannot change
   an old unary answer, and a fresh form alone adds no positive answer.
3. There are four minimum replies under the full declared two-item
   grammar. “Rule P” means the uniform all-cards rule for P.

   | Reply | X | Y | Z |
   |---|---|---|---|
   | P(Y) and Q(X) | yes, yes | yes, yes | —, — |
   | Rule P and Q(X) | yes, yes | yes, yes | yes, — |
   | P(Y) and Rule Q | yes, yes | yes, yes | —, yes |
   | Rule P and Rule Q | yes, yes | yes, yes | yes, yes |

   Only the instance-only reply leaves Z's profile unchanged. All four
   cost two items. The two mixed replies are related by an allowed
   renaming exchanging X/Y and P/Q; the complete state comparison groups
   the four replies into three classes. Matching printed rows alone is
   not that state comparison.
4. The first three replies preserve the two added separation promises.
   The last makes all three profiles equal and violates both promises.
5. You would need an argument covering larger budgets too, under the
   specified rules. Exhausting only the two-item candidates supplies
   no such argument. Lesson 03 explicitly exhibits the difference.
6. Inspect the admitted data positions. They still contain X, Y, and Z.
   Matching rows changes neither their count nor X's and Y's distinct
   internal indices. No merge operation has been supplied.

The finite check in `run_lab.py` reconstructs this supplied table through
admission events, enumerates the two-item candidates, retains all four
replies, compares profiles, and checks the promised-pair variant.
These results are computational evidence for this finite practice, not
a proof about arbitrary records.
