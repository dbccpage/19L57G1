---
name: claims-audit
description: Check numbers and claims written in paper/ against what the machine actually produces. Use before freezing the paper, after changing any derivation module or Lean theorem set, or when asked whether the paper is still true.
---

# Audit the paper against the machine

**AuthorityEffect: None.** This skill compares prose to measurement and
reports divergence. It approves nothing, registers no claim, and rewrites
nothing on its own. A divergence it finds is a finding, not a licence to
edit the number quietly — see Repair below.

## The premise

**Every number in `paper/` is a claim.** Test counts, coverage
percentages, node counts, round counts, report counts, tie-class counts.
A number that was true at some earlier freeze and is now stale is a false
statement in the paper, not a historical note — unless it is explicitly
dated and scoped as a snapshot.

This has happened. `paper/paper.md` §12 carried "82 tests passing", "line
coverage 99.77%", "branch coverage 98.75%", and "51 exported reports" long
after the true values had moved into the hundreds and thousands.

## What to check, and against what

Never re-derive a number from prose. Get it from the machine.

**Test count and coverage.** Run the `gates` procedure. Do not read
`coverage.json` without regenerating it first; it is tracked and can be
arbitrarily stale.

**Lean axiom reports.** Count from `artifacts/lean_axioms.txt`, which is
the committed receipt, and confirm it matches a fresh build log via
`ci/check_axiom_report.py`. Count reports by counting lines that carry a
report, not by grepping for `theorem` — a docstring line beginning with
that word has defeated a grep count here twice.

**Ledger-backed claims.** `paper/paper_claim_ledger.md` gives every claim
a stable `CL-*` ID naming its Python evidence (artifact key and/or test
name) and its Lean theorem names. `artifacts/claims.json` holds the
computed values. Compare the ledger's asserted value against the artifact
key it names — that is the cross-check the ledger exists for.

**Node, round, and frontier counts.** These come from the exported
artifacts, not from the paper's own earlier sentences.

**Module and declaration censuses.** `artifacts/elaborated_modules.txt`
for Lean modules. The runner census is a live glob over the top level of
`code/`, with `artifacts/` as its own pin.

## Independence

Enumerate the population by a route that does not share machinery with
the thing being checked. A count taken with the same pattern that
generated the text proves nothing; that exact circularity was a real
defect in the citation checker, where the totality invariant used the
classifier's own regex and silently dropped two citations on both sides
at once.

## Repair

When prose turns out to cover less than it asserted, the established move
is to **weaken the statement and quote the withdrawn wording**, in
`paper/paper_claim_ledger.md` and at the original site, and record the
narrowing in `paper/paper_change_log.md` newest-last. Never keep the
wording and lean on the receipt. `paper/pr11_correction_ledger.md` is a
worked example.

For a stale measurement specifically: either update it to the freshly
measured value and say what produced it, or date and scope it explicitly
as a snapshot of an earlier state. Silently editing a number to match the
machine, with no change-log entry, loses the fact that the paper was
wrong — which is itself part of the record.

## Reporting

List every divergence as `file:line`, the asserted value, the measured
value, and the command that measured it. State which claims you did NOT
check and why. An unchecked claim is reported as unchecked, never assumed
current.
