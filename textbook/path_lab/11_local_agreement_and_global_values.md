# 11. Local agreement and global values

We now have two precise properties of a cost rule:

| Property | Requirement |
|---|---|
| Exact | One state-to-number potential gives every step cost by subtraction |
| Closed | The two cost totals agree on every commuting square |

**Predict:** if a cost is exact, must it be closed? If it is closed,
must it be exact?

<details><summary>Keep the directions separate</summary>

An exact cost is closed. Both routes of a commuting square have the
same start and end; telescoping therefore gives them equal costs.

The reverse implication fails for this passage. The state-change count
is closed on every commuting square, as proved in the research. Yet its
budget return loop costs 2, so it is not exact. This is a proved
counterexample to that reverse implication under these definitions.

</details>

## Why the square checks do not remove the loop

Exchanging adjacent events keeps the events; it changes only their
order. Our two-event return loop and the empty history do not have the
same event list or even the same length. Agreement on each allowed
exchange does not say that the loop can be erased.

Also distinguish a **closed cost**, a property of a cost rule on all
commuting squares, from a **closed path**, one history returning to its
start. Sharing the word does not make the definitions identical.

**Try a change:** ask for signed budget change instead. Budget itself
supplies its potential. This cost is both exact and closed; it gives
the budget loop total 0.

The desk checks 432 two-event comparisons in a declared twelve-state
slice. Of those, 348 commute. Those finite checks illustrate the
properties. The general closedness claim comes from the actual Lean
proof, not from absence of a failure in that slice.

Continue with [12. Say which path changes are allowed](12_which_path_changes_are_allowed.md).

AuthorityEffect: None. NS-7 proves exact implies closed; NS-8/10 prove
`Closed writes ∧ ¬ Exact writes`. This is not a general claim about
physical work or conservation.
