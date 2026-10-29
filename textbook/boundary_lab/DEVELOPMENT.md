# Reproduce the boundary and swap route

AuthorityEffect: None. All writes below are textbook or local receipt files.
Research source, frozen designs, ledgers, predictions, and receipts remain
read-only. Do not regenerate a packet while an injected defect is live.

From the repository root:

```powershell
python textbook/boundary_lab/run_lab.py
python textbook/boundary_lab/build_results.py
python -m unittest discover -s textbook/boundary_lab -p test_lab.py
python textbook/checks/u37_boundary_lab.py
python textbook/checks/u37_boundary_lab_lean.py
```

After an intentional teaching-model/source update, regenerate the packet
and four figures with `python textbook/boundary_lab/run_lab.py --write`,
then rebuild the desk. Review the resulting data diff and source digests.
This does not repin or validate the research trees' own receipts.

The HTML bundle contains the recorded JSON and makes no runtime fetch.
Serve it locally for browser checking, or open the generated standalone
file. The Wiki mirror uses its own page/asset destinations. Verify each
report subset, all eight control candidates, and changed-label settings;
test keyboard controls, hidden/revealed answers, and a narrow viewport.

Current interaction status: the recorded values and all 120 JavaScript
lookups pass their checks. Browser rendering, keyboard flow, and narrow
layout remain unverified after a localhost timeout and rejection of the
generated browser error page by URL policy. Both preview servers were
stopped. Static figures have separate PNG/geometry review; that does not
validate browser interaction. The detailed scope is recorded in
`REVIEW_2026-10-28.md`.

The ordinary textbook job discovers the two `u37_boundary_lab` scripts.
The full twelve-family local contract is separate and remains required
before requesting a merge. Software checks cannot establish novice learning.
