# Independent replay

AuthorityEffect: None.

Use the repository's pinned Python dependencies and Lean toolchain. This
packet's Python tests use `pytest-xdist==3.8.0` for eight workers. Run from the
repository root:

```powershell
python -m pip install -r requirements.txt pytest-xdist==3.8.0
$env:PYTHONPATH = "$PWD\code"
$env:PYTHONDONTWRITEBYTECODE = "1"
Set-Location research/local_reuse
python verify_sources.py --check
python -m pytest -n 8 -q tests -p no:cacheprovider --basetemp "$env:TEMP/local-reuse-tests"
python -m mypy --config-file pyproject.toml
python run.py --check
python verify_lean.py --check
```

Use a fresh writable test temporary directory on Windows. `run.py --check`
regenerates every computation in memory and compares the committed bytes.
`verify_lean.py --check` explicitly builds both local modules, directly
elaborates the theorem source again, and compares its axiom reports plus the
generated helper reports with the independently enumerated environment census.
It rejects missing/extra/duplicate reports, disallowed reliance, missing source
objects, altered local proof sources, and changed sealed inputs.

The Lean package imports the existing source by a local Lake path dependency.
Compilation writes only ignored `.lake` caches, not source or sealed evidence.
The two `--write` modes deliberately create records during development; CI
never uses them. They must not be run while a mutation is present.

The dedicated `local-reuse.yml` workflow runs these checks. The original
verification workflow remains unchanged. This packet's results do not stand
in for a fresh execution of every original research package or every sealed
gate family.
