# Reproduce and review the path lab

AuthorityEffect: None. Run from the repository root. The checks do not
write sealed sources, derivation artifacts, or research receipts.

```text
python textbook/path_lab/run_lab.py --population
python textbook/checks/u60_path_lab.py
python textbook/checks/u60_path_lab_lean.py
python -m unittest discover -s textbook/path_lab -p test_lab.py
```

The book-Lean check imports the existing compiled cell/boundary libraries
through `textbook/checks/booklean.py`. Run `lake build` in `lean4/` first
if needed. The normal textbook job discovers both new check scripts.

```text
uv run --isolated --no-project --python 3.14.7 --with-requirements requirements.txt python ci/run_gates.py --job textbook --receipt artifacts2/path_lab/textbook_gates.json
```

On this Windows host, give TEMP and TMP a normal writable workspace
directory if the sandbox's default temporary directories have restrictive ACLs.
Set subprocess text output to UTF-8 when capturing Lean diagnostics.

After an intentional, reviewed teaching-input change:

```text
python textbook/path_lab/run_lab.py --write
python textbook/path_lab/build_results.py
```

Inspect the difference. Do not regenerate a record to adopt a live defect.
The source map states which finite populations and general source results
are actually used.

Preview the self-contained desk:

```text
python -m http.server 8769 --bind 127.0.0.1 --directory textbook/path_lab
```

Open `http://127.0.0.1:8769/results.html`. The page selects recorded cases,
runs no Python, makes no runtime data fetch, and stores no learner responses.
Wiki generation rewrites its reading/download links.

Review missing-edge walks, zero-step and returning walks, face prediction
and guard reasons, repeated requests, opposite versus equal shared-edge
signs, all-zero second boundaries, the all-positive control, raw repeated
lists, keyboard controls, and phone layout. Check stale published copies
and a false generated Lean equality, restoring original bytes between
injections. Reader testing remains separate from software validation.

The same commands now include the selected native cost continuation:
84 history records, 432 ordered event comparisons, 27 three-point cost
tables, and 3,108 additional histories. The existing Lean wrapper
re-elaborates three exact research bodies and checks twenty added reports,
giving 184 reports overall. `costs_axioms.json` pins the expected sets.
Never change those sets to accept an unexpected axiom or a failed proof.

`node textbook/path_lab/test_cost_controls.mjs` executes the actual new
handlers in a minimal DOM across 168 history/cost selections and 432
square selections. It checks both prediction gates, incorrect feedback,
and reset of both panels when their shared start changes. It does not
check browser layout, keyboard input or accessibility.

In a browser, compare both costs, inert repeats, the empty history,
the two budget-loop totals, both halt/license orders from live and halted
starts, and a noncommuting square with a zero signed-budget difference.
Check narrow tables, Tab focus and arrow-key scrolling. Inspect the
budget-loop diagram at its intrinsic size. Keep raw event order and
the selected cost question visible; do not silently change the premise.
