---
name: pin
description: Pin the exact object under review before reading or diffing it, and apply the repository's review procedure. Use when reviewing a pull request, diffing a branch, or reporting a result about a specific revision.
---

# Pin the object before reading anything

**AuthorityEffect: None.** This skill fixes what is being talked about and
reports findings. It approves nothing, merges nothing, and registers no
claim. A review produced with it carries no authority: a disposition line
is an opinion on a SHA, not a permission.

## Pin first

```bash
gh pr view N --json headRefOid,baseRefOid,mergeStateStatus
git fetch origin
git merge-base <baseRefOid> <headRefOid>
git diff --stat <mergeBaseSha> <headRefOid>
```

Record **all three SHAs** — base, head, and merge-base — and diff the
pinned SHAs.

**Never diff against a branch name.** `origin/main` is a moving ref: it is
the wrong base for a stacked pull request or a non-main base, it is stale
if the remote was not fetched, and it can move mid-review.

**Diff from the merge-base, not tip to tip.** A tip-to-tip diff reports
commits that are on the base and not on the branch as deletions. That once
produced a false "this pull request deletes 3083 lines" finding here.

If any pinned SHA changes during the review, re-pin and restate rather
than reconciling.

## Establish the verification domain before any claim

Everything downstream is conditional on this.

- For each changed Lean module: is it reached by a build target? Does
  `lean4/Derivation.lean` import it? Distinguish SCANNED from ELABORATED —
  `ci/check_lean_audit.py` reads `.lean` files as text and does not
  typecheck them.
- What does CI actually execute on these files? Read
  `.github/workflows/verify.yml`. Do not assume.
- A green run is evidence only about what it inspected.

## Then read, in this order

Statement, then docstring, then pull request body. Prose read first primes
you.

- Does the STATEMENT mention every structure the name and docstring claim?
- Does the PROOF consume every result the docstring cites?
- What is each cited gate's DOMAIN — what would it fail to see?
- Is any totality invariant computed with the same pattern it is checking?
  A census taken by the parser under test cannot fail.
- `#print axioms F` reports the axioms of `F`'s own proof term, not of
  instances a use site supplies. Check the instantiation.
- Keep UNSATISFIABLE, VACUOUSLY TRUE, and UNFALSIFIABLE apart. They are
  three different things.
- Derive counts by machine resolution, never by grep. A docstring line
  beginning with the word `theorem` has defeated a grep count here twice.

## Check your own tooling

Did any command silently error? A flag that does not exist can make a
search return "no matches", which reads as a clean result. Re-run anything
that returned "nothing found" with a DIFFERENT tool before reporting it as
absence. Both author and reviewer have produced false results this way.

## Required output

- Findings with severity, each naming FILE:LINE and the exact false
  statement.
- A VERIFICATION BOUNDARY: what was run, what was not run, and why. Failed
  or skipped steps are stated as such, never omitted.
- Whether anything was mutated: source, pull request, merge state, or
  claim registration.
- A disposition on the exact head SHA.

## The single question

> If this claim were false, which gate would fail?

If the answer is "none", that is the finding — whether the claim is a
theorem, a name, a count, or a receipt.

`paper/pr_review_template.md` is the long form, including an explicit
statement that it is not a gate and enforces nothing.
