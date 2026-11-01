# First four Units: answers and reasons

Try the [questions](core_start_practice.md) before reading this page.

1. No. The opaque inscription supplies neither that division nor a
   pairing operation. A constructor would declare a representation and
   its rules outside the object language. Choosing definitions is
   different from executing an admission event inside those definitions.
2. Neither lookup succeeds, so the candidate is not derivable under
   this rule. That is a conclusion about the supplied procedure.
   It is not a claim that every outside-world statement is false.
3. No. The individual-instance and all-instances-rule fields are both
   empty. The datum count, form arities and demand field do not supply
   either lookup entry. The demand asks for separation without meeting it.
4. The individually admitted instance makes (0, [0]) derivable and leaves
   (0, [1]) underivable. Its no-instances premise fails. The rule-only
   copy makes both derivable; its no-rules premise fails. Each copy keeps
   the other lookup list empty. Both queried instances here are well formed.
5. The admitted lists are: empty; [“m”]; [“m”]; [“m”, “n”]; [“m”, “n”].
   The fifth event recognizes an already admitted token and leaves the
   Python ledger fixed. Lean's token-erased `admitDatum` has no token
   argument and always increases its count. These are different event
   definitions; Unit 07's Lean erasure treats a repeated token-aware admission
   as a supply, rather than naively erasing its token argument.
6. Both final Python ledgers contain [“m”, “n”] and have the same other
   fields. One history has five events, the other three. Equal final
   ledgers need not retain the history that produced them. Removing
   supplies preserves this replay result, not the original event list.

Revisit [Unit 00](units/00_mark_and_constructor.md) for definitions versus
events, [Unit 02](units/02_underivable_of_empty.md) for its two premises,
or [Unit 03](units/03_supply_no_op.md) for the two admission models.
Continue to [Unit 04](units/04_no_forced_successor.md) when you can explain
why a demand, a successful lookup and an executed event answer different
questions.

AuthorityEffect: None. Model answer guide; no measured beginner outcome.
