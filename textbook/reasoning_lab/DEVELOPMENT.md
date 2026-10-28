# Reproduce and review the reasoning route

AuthorityEffect: None. Run these from the repository root. No sealed
source or research receipt is written by this route.

```text
python textbook/reasoning_lab/run_lab.py --population
python textbook/checks/u00_reasoning_lab.py
python textbook/checks/u00_reasoning_lab_lean.py
python -m unittest discover -s textbook/reasoning_lab -p test_lab.py
```

The Lean command uses the existing built `Derivation.Compression` library
through the shared book-Lean runner. Build it with `lake build` in
`lean4/` if needed. The normal textbook job discovers the two check scripts.

The pinned local job uses Python 3.14.7 and `requirements.txt`:

```text
uv run --isolated --no-project --python 3.14.7 --with-requirements requirements.txt python ci/run_gates.py --job textbook --receipt artifacts2/reasoning_lab/textbook_gates.json
```

On this Windows host, set TEMP and TMP to a normal writable workspace
directory if sandbox-created temporary directories have restrictive ACLs.
This is an execution environment setting, not a test or source repair.

After an intentional, reviewed change to the teaching inputs:

```text
python textbook/reasoning_lab/run_lab.py --write
python textbook/reasoning_lab/build_results.py
```

Inspect the changes. Do not regenerate a record to hide a live disagreement.
The source map states exactly which finite populations and book proofs run.

Preview the self-contained desk:

```text
python -m http.server 8768 --bind 127.0.0.1 --directory textbook/reasoning_lab
```

Open `http://127.0.0.1:8768/results.html`. The desk selects recorded cases,
performs no Python execution or runtime data fetch, and stores no reader
responses. The Wiki build rewrites reading/download links.

Review all 288 conditional settings and 128 selected witness demands,
prediction gating and reset after scope changes, empty domains, negative
second answers, keyboard controls, narrow layout, and the rendered lessons.
Check stale packet/desk rejection with byte restoration and rejection of
an intentionally false book proof. Reader evidence remains a separate task.
