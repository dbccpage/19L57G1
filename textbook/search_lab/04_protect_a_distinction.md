# 04. Protect a distinction

[Previous](03_keep_the_ties.md) · [Search lab](README.md) · [Next: stopping](05_why_the_search_stopped.md)

## Keep one small ledger while changing its requirements

Keep the one-slot mark on A and the required separation A/B. Admit a third
entry C. The old form now has these derivability answers:

| Entry | F(_) |
|---|---|
| A | Yes |
| B | No |
| C | No |

Now impose a new demand: **separate B from C**. Predict which repairs work.

## First repair: also mark B on the old form

The answers become Yes, Yes, No. B/C is separated, but A/B collapses.
The repair fails the already imposed A/B requirement.

Its instance is well-formed: the form and entry exist. The search's
**response-validity filter** rejects it. The raw admission function checks
well-formedness and can produce this unsatisfactory state; it does not by
itself enforce every separation requirement.

## Second repair: also mark C on the old form

The answers become Yes, No, Yes. A/B remains separated, and B/C becomes
separated. This is a valid one-item response when A/B is the only old demand.

But A/C, previously separated, now collapses. That pair was not protected
by a requirement. Preserving all imposed demands is weaker than preserving
every distinction that happened to be available.

## Change only the protection

Return to the original table. Add the requirement that A/C must remain
separated as well. The second repair now fails. With at most one item,
the declared search finds no valid response.

Permit two items. Admit a new one-slot form H and record `H(B)`.

| Entry | F(_) | H(_) |
|---|---|---|
| A | Yes | No |
| B | No | Yes |
| C | No | No |

All three pairs are separated. The new test preserves the old F answers.
The packet records all ten minimum raw plans under item-count pricing
for this protected case; H(B) is one worked representative, not the only repair.

## Your turn

Identify separately what changed when we protected A/C and what changed
when we raised the item budget. Neither action alone records H(B).

**Connection to First steps:** adding a question while retaining old
answers preserved old distinctions there. Adding an instance to an old
form can change its answers here. The operations have different hypotheses.

AuthorityEffect: None. Protection here means imposed pair-separation demands.
It is not a license or authorization mechanism from another formal setting.
