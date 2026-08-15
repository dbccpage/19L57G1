# Pull request review template

Classification: metatheory apparatus. This document describes how to
review a change to this repository. It introduces no object-language
notion and licenses no claim.

Every section below corresponds to a defect that reached `main` or
survived a review round. It is not a general code-review checklist; it
is the specific set of things that have actually failed here.

---

## Disposition line, required, first

`approve` / `changes requested` / `blocking` on exact head, full
forty-character SHA.

---

## 0. Pin the object before reading anything

```bash
gh pr view N --json headRefOid,baseRefName,mergeStateStatus
git merge-base origin/main <head>
git diff --stat origin/main...<head>     # THREE dots
```

Use three-dot diffs. A two-dot diff compares tips, so unrelated commits
on `main` appear as deletions in the branch — that once produced a
false "this pull request deletes 3083 lines" finding. If `main` moves
during the review, re-pin and restate rather than reconciling.

---

## 1. Establish the verification domain — before any claim

Do this FIRST. Everything downstream is conditional on it.

- For each changed Lean module: is it reached by a build target? Does
  `lean4/Derivation.lean` import it? Does a `lean_lib` root name it?
- What does CI actually execute on these files? Read
  `.github/workflows/verify.yml`. Do not assume.
- Distinguish SCANNED from ELABORATED. `ci/check_lean_audit.py` reads
  `.lean` files as text for forbidden tokens; it does not typecheck
  them.

A green run is evidence only about what it inspected. This repository
has merged Lean modules that `lake build` never elaborated, on three
consecutive pull requests, each reported as "CI green".

---

## 2. Statement versus prose

For every theorem the change relies on:

- Does the STATEMENT mention every structure the name and the docstring
  claim? A theorem named for a bridge between two things, whose
  statement mentions only one of them, is a finding.
- Does the PROOF consume every result the docstring cites?
  Re-instantiating a local lemma while claiming to transport a sealed
  one is a finding.
- Read in this order: statement, then docstring, then pull request
  body. The prose primes you if you read it first.

---

## 3. Gate domains

For each gate or receipt the change cites:

- What is its DOMAIN? What would it fail to see?
- Is any totality or coverage invariant computed with the same pattern
  it is checking? A census taken by the parser under test cannot fail.
- Enumerate the population INDEPENDENTLY and compare counts.

---

## 4. Weight grading

- Which results are near-definitional once the definitions are fixed?
- If a headline theorem's proof is one line, say so, and check the
  claim is cited WITH its substance rather than alone.

---

## 5. Non-vacuity and boundaries

- Is there a POSITIVE case, or does the structure admit only refusals?
  A theorem that cannot be satisfied by anything is unfalsifiable.
- Does the obstruction require an inhabitant? Does the carrier admit
  empty models, or larger ones than the prose claims?
- Is every advertised ceiling a PREDICATE WITH A PROOF, or is some of
  it prose?

---

## 6. Axioms at the use site

`#print axioms F` reports the axioms of `F`'s own proof term, NOT of
the instances a use site supplies. Check the instantiation, not the
general lemma.

A `Classical.choice` dependency here lived in the `ReflBEq Nat`
instance, invisible to every lemma-level check, while `LawfulBEq Nat`
was clean. A prior analysis listed fifteen lemmas as "checked directly
and clean" and none of them was the carrier.

Also: a bare `simp` can pull classical lemmas from the default simp
set. Prefer `simp only` with named lemmas, or explicit terms.

---

## 7. Counts and receipts

- Derive counts by MACHINE RESOLUTION — have Lean resolve the names —
  never by grep. A docstring line beginning with the word `theorem`
  once defeated a grep count, twice, in the same review.
- Any number in a commit message or pull request body is a claim.
  Verify it or ask for its removal.

---

## 8. Check your own tooling

- Did any command silently error? A flag that does not exist can make a
  search return "no matches", which reads as a clean result.
- Re-run anything that returned "nothing found" with a different tool
  before reporting it as absence.

Both the author and the reviewer produced false results from broken
commands during the review rounds that produced this document. The
template must survive its own operator.

---

## 9. Required output

- Findings with severity, each naming FILE:LINE and the exact false
  statement.
- VERIFICATION BOUNDARY: what was run, what was not run, and why.
  Failed, skipped, or unavailable steps are stated as such, never
  omitted.
- An explicit statement of whether anything was mutated: source, pull
  request, merge state, or claim registration.

---

## The single question

> If this claim were false, which gate would fail?

If the answer is "none", that is the finding — whether the claim is a
theorem, a name, a count, or a receipt.

---

## Repair convention

When a claim turns out to cover less than its prose asserted, the
established move here is to weaken the statement in
`paper/paper_claim_ledger.md` and at the original site, quoting the
withdrawn wording rather than silently replacing it, and to record the
narrowing in `paper/paper_change_log.md` newest-last. Never keep the
wording and lean on the receipt. `paper/pr11_correction_ledger.md` is a
worked example.
