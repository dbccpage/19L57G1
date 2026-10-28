# Reproduce and review the change lab

AuthorityEffect: None. The packet and the book's temporary Lean source
are explanatory apparatus outside the sealed paths.

From the repository root:

```text
python textbook/change_lab/run_lab.py
python textbook/checks/u54_passage_lab.py
python textbook/checks/u54_passage_lab_lean.py
```

The first two commands recompute the passage packet through the actual
sealed Python functions and compare it with `recorded_lab.json`.
The third imports the compiled `Derivation.PrimitivePassage` library and
checks the book's finite agreements and general store invariant. Run
`lake build` in `lean4/` first if its libraries have not been built.
The existing textbook gate automatically discovers both new check scripts.

The pinned local job can be run with the existing Python 3.14.7 runtime:

```text
uv run --isolated --no-project --python 3.14.7 --with-requirements requirements.txt python ci/run_gates.py --job textbook --receipt artifacts2/change_lab/textbook_gates.json
```

Regenerate teaching data only after reviewing an intentional source change:

```text
python textbook/change_lab/run_lab.py --write
python textbook/change_lab/build_results.py
```

Inspect the difference; do not regenerate a record merely to accept a
disagreement. The source map names the finite populations and proof scope.

Preview the self-contained passage desk:

```text
python -m http.server 8767 --bind 127.0.0.1 --directory textbook/change_lab
```

Open `http://127.0.0.1:8767/results.html`. Controls select recorded cases.
No Python runs in the page, no reader response is stored, and no runtime
data requests are needed. The Wiki version rewrites reading/download links
to the published pages and packet.

Review prediction gating, the event timeline, all 24 operational settings
for both events, refusal/recovery versus halt, the column-family scope,
keyboard controls, and narrow layout. Test stale packet/desk refusal and
an intentionally false book-Lean expected equality before release.

Reader comprehension, new-example transfer, and delayed retention remain
separate evidence. No learning-time guarantee is claimed.
