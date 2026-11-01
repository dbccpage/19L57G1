# First four Units: try another example

Attempt these after [Unit 03](units/03_supply_no_op.md), before the
[separate answers](core_start_answers.md). Use the two-lookup rule:
an instance is derivable when it is admitted individually **or** its
form has the all-instances rule. A derivability answer alone is not a
check of whether its form and arguments are well formed.

1. A mark looks like two brackets with a space between them. Does that
   appearance supply the model with two objects or a rule for pairing?
   Where would a chosen pairing rule have to be declared?
2. Both lookup lists are empty. For the candidate “form 0 holds of
   datum 0,” does either lookup succeed? Does the result say that every
   statement about the outside world is false?
3. Admit two data, one unary form numbered 0, and a demand to distinguish
   the data. Admit no instance and no rule. Is “form 0 holds of datum 1”
   derivable? Which of the five ledger fields decides the answer?
4. Start two copies of Question 3's ledger. In the first, admit only
   instance (0, [0]). In the second, admit only the all-instances rule
   for form 0. For each copy, compare the answers to (0, [0]) and
   (0, [1]). Which premise of Unit 02 has changed in each copy?
5. In the token-aware Python model, start empty and record these five
   events: supply “m”; admit datum “m”; supply “n”; admit datum “n”;
   admit datum “m” again. List the admitted token strings after each
   event. Does the last admission append a third datum? Does this show
   that token-erased Lean `admitDatum` sometimes leaves its count fixed?
6. Remove the supply events from Question 5's history. Compare the final
   ledgers and the two event histories. Does equality of the final
   ledgers establish equality of the histories?

AuthorityEffect: None. Six changed tasks about supplied definitions and
recorded model calculations. No learner score or observation is recorded.
