# Reproduce and review the path lab

AuthorityEffect: None. Run from the repository root. The checks do not
write sealed sources, derivation artifacts, or research receipts.

```text
python textbook/path_lab/run_lab.py
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
