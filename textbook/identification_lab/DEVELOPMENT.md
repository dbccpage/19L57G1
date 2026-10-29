# Reproduce the Same-record lab

AuthorityEffect: None. Run from the repository root. No command writes
into sealed sources or research receipts.

```powershell
python textbook/identification_lab/run_lab.py
python -m unittest discover -s textbook/identification_lab -p "test_*.py"
python -m unittest discover -s textbook/media -p "test_identification_lab_wiki.py"
python ci/check_textbook.py --python-only
```

The first command recomputes the two selected starting histories, all
24 root probes, two next-demand branches, the explicit outside-bound
reply, and two practice probes. It compares the results with the packet,
source-map counts, and four figures. Use `--write` to regenerate the packet
and figures after an intentional teaching change, then review their
meaning. Do not regenerate native campaign receipts as a lesson update.

The tests inject false costs, equality results, retained promises, side
effects, continuation prices, and stale figures. The Wiki tests corrupt
published assets and remove a page. These check detection of specific
defects, not every possible error in the lesson or research implementation.

The textbook gate discovers `textbook/checks/u20_identification_lab.py`.
This route adds a Python computation check and no book-Lean proof.
The research tree also has no native Lean proof; a passing Python check
must not be reported as one. The full textbook job and the repository's
twelve local gate families have different scopes.

The figures are standalone accessible-title SVGs. Review rendered
previews for text bounds, collisions, and legibility after editing.
This route uses worked static sequences and separate answers. It adds
no custom browser application. Browser interaction review of other
routes remains a separate task. Software checks and figure inspection
do not establish learning or retention.
