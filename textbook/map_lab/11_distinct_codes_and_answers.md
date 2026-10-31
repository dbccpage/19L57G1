# 11. Distinct codes can hide a distinction

The [budget translation](10_translate_each_step.md) correctly keeps two
different target states: one has budget 0 and the other budget 1.

An encoding is **injective** when different source states get different
target states. You can also say “no two source states share a code.”
Our two codes have that property.

**Predict:** does this guarantee that every target observation can tell
which source state was encoded?

<details><summary>Keep the observation in the question</summary>

No. A reader allowed to inspect budget can distinguish 0 from 1. A reader
that never inspects budget may give the same answer for both states.
Distinct stored records and distinct answers to one question are
different requirements.

</details>

## The passage's specified native observation

This research uses one particular observation of the passage. It reads
the declared tests' agreement relation, the unresolved protected pairs,
and the refusal record. It does not read budget or license.

In both encoded states no test has been declared, there are no unresolved
protected pairs, and there are no refusals. The observation is identical.

| Source | Target budget | Specified native observation |
|---|---|---|
| 0 | 0 | undeclared tests; no active obstruction; no refusals |
| 1 | 1 | undeclared tests; no active obstruction; no refusals |

“Undeclared tests” is kept separate from a declared empty test family.
No observation has been silently added by choosing different budgets.

**Try a change:** let a new target reader inspect budget. It can recover
this switch state. That is a valid change of the question, and it must be
named; it is not the native observation specified above.

The step squares and distinct codes both pass. The stronger claim that
this native observation preserves the switch's own state-answer fails.
The counterexample identifies exactly what the weaker checks omitted.

Continue with [12. Preserve the requested observation](12_preserve_the_requested_observation.md).

AuthorityEffect: None. NB-9 refutes the stronger structural conclusion
from step agreement and injective encoding alone. NB-16 defines the
specified native observation and proves the stronger observation results.
