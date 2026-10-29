# Reproduce and review the map lab

AuthorityEffect: None. Run from the repository root. No sealed source,
artifact, or research receipt is written by these checks.

```text
python textbook/map_lab/run_lab.py --population
python textbook/checks/u61_map_lab.py
python textbook/checks/u61_map_lab_lean.py
python -m unittest discover -s textbook/map_lab -p test_lab.py
```

The book runner uses the existing compiled native libraries. Build them
with `lake build` in `lean4/` if necessary. The normal textbook job
discovers both check scripts.

```text
uv run --isolated --no-project --python 3.14.7 --with-requirements requirements.txt python ci/run_gates.py --job textbook --receipt artifacts2/map_lab/textbook_gates.json
```

Use a normal writable TEMP/TMP directory on this Windows host if default
sandbox temporary directories have restrictive ACLs. Capture Lean output
as UTF-8 so diagnostic symbols remain readable.

After an intentional reviewed change:

```text
python textbook/map_lab/run_lab.py --write
python textbook/map_lab/build_results.py
```

Review the differences. Never regenerate a record to accept a live defect.
The source map gives exact finite domains and the separate global theorem scope.

```text
python -m http.server 8770 --bind 127.0.0.1 --directory textbook/map_lab
```

Open `http://127.0.0.1:8770/results.html`. The self-contained desk selects
recorded cases, runs no Python, makes no runtime data request, and stores
no reader responses. Wiki generation rewrites its links and mirrors figures.

Review recovery predictions, every selected domain and order, the shortened
domain adapter, paired answers, empty domains, group arrows, unused labels,
complete lookup examples, controls, keyboard reset, and phone layout.
Inject stale record/desk/figure copies and a false book equality, restoring
bytes between checks. Novice explanation and transfer require reader trials.
