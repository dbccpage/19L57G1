# Reproduce the growth route

AuthorityEffect: None. Run from the repository root.

```text
python textbook/growth_lab/run_lab.py --population
python textbook/checks/u62_growth_lab.py
python textbook/checks/u62_growth_lab_lean.py
python -m unittest discover -s textbook/growth_lab -p test_lab.py
```

The Lean check re-elaborates the actual research sources in a temporary
file. It writes no research library or receipt. The normal textbook job
discovers both check scripts.

```text
uv run --isolated --no-project --python 3.14.7 --with-requirements requirements.txt python ci/run_gates.py --job textbook --receipt artifacts2/growth_lab/textbook_gates.json
```

On this Windows host, use a normal writable TEMP/TMP directory and UTF-8
subprocess output. Source, research, and sealed artifacts remain unchanged.

After an intentional reviewed change:

```text
python textbook/growth_lab/run_lab.py --write
python textbook/growth_lab/build_results.py
python -m http.server 8771 --bind 127.0.0.1 --directory textbook/growth_lab
```

Review `http://127.0.0.1:8771/results.html` for predictions, reset after
scope changes, quiet and empty controls, old/new pair tables, per-round
service, final versus peak backlog, finite thresholds, keyboard use,
and narrow-screen layout. Verify static SVGs and Wiki links. Inject stale
record/desk/figure copies and a false Lean count, restoring bytes between
checks. Never regenerate a record to bless a live defect.

Software checks establish consistency. Comprehension, unfamiliar-example
transfer, reading time, and delayed retention require reader evidence.
