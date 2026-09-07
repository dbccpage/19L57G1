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
The two `--write` modes deliberately create records during development; no
automatic check uses them. They must not be run while a mutation is present.

## Where these checks run

**Locally, by hand, and nowhere else.** This project does not use GitHub
Actions. An earlier draft of this packet added `.github/workflows/local-reuse.yml`
and this paragraph said that workflow ran the checks; both were removed,
because a file that never executes is not enforcement and saying otherwise
told a reader the packet was covered when it was not.

The packet is therefore not yet registered in any live enumeration. The
gate-11 command block in the root `CLAUDE.md` lists four research trees and
does not list this one. Adding it there is the author's act, not this
packet's; until it happens, the four commands at the top of this file are the
whole verification story and someone has to run them.

This packet's results do not stand in for a fresh execution of every original
research package or every sealed gate family.
