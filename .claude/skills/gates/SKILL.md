---
name: gates
description: Run the six CI gate families locally, in the order CI runs them, with freshness enforcement so a stale input cannot produce a false pass. Use before pushing, before claiming a gate result, or when asked whether the repository is green.
---

# Run the verification contract

**AuthorityEffect: None.** This skill runs commands and reports what they
printed. It approves nothing, merges nothing, registers no claim, and
mutates no artifact. A gate result it reports is evidence only about the
command that produced it. If this file disagrees with
`.github/workflows/verify.yml`, the workflow is correct and this file is
wrong.

## The rule that matters most

**A gate that did not run is not a gate that passed.** Every step below
prints an exit status. If an upstream command fails, its downstream check
may still exit 0 by reading a stale file. Report a gate as passing only
when you have seen its own command succeed in the same session.

This is not hypothetical. `ci/check_coverage.py` reads `coverage.json`,
which is TRACKED IN THE REPOSITORY and absent from `.gitignore`. On a
machine where `coverage` is not on PATH, `coverage run` and `coverage json`
both fail, and `check_coverage.py` then reports the committed file's old
numbers at exit 0. That has happened. It is why step 3 deletes the file
first.

## Order

Run from the repository root. `code/` must be on `PYTHONPATH` for anything
outside pytest.

### 1. Prompt byte-identity

```powershell
python ci/check_prompt_hashes.py
```

`prompt/**` is `-text` in `.gitattributes`. A CRLF conversion breaks this.

### 2. Transport citations

```powershell
python ci/check_transport_citations.py
```

Expect `N verified, 0 unresolved`. The population is enumerated by a
pattern independent of the classifier, on purpose — do not "simplify" that
into one pattern.

### 3. Tests under coverage — delete the stale file FIRST

```powershell
Remove-Item coverage.json -Force -ErrorAction SilentlyContinue
python -m coverage run -m pytest -q
python -m coverage json -q
python ci/check_coverage.py
```

Use `python -m coverage`, not `coverage` — the bare name is not always on
PATH, and that failure is silent in the way described above. Confirm
`coverage.json` did not exist before the generate step and does after.
Both line and branch must reach 95% independently.

### 4. Strict typing

```powershell
python -m mypy
```

Config lives in `pyproject.toml`: `strict = true`, `files = ["code"]`.
`ci/` is deliberately outside this scope.

### 5. Artifact regeneration

The runner census is a glob over the TOP LEVEL of `code/` — not a hand
list, and not recursive.

```powershell
$env:PYTHONPATH = "code"
Get-ChildItem code/run_*.py | ForEach-Object { python $_.FullName --artifacts artifacts2 }
python ci/compare_artifacts.py artifacts artifacts2
```

`artifacts2/` is gitignored. The comparison checks the export sets in both
directions: a committed artifact with no regeneration, and a regenerated
artifact never committed, both fail by name.

### 6. Lean

```powershell
cd lean4
lake build 2>&1 | Tee-Object -FilePath ../lake_build_local.log
cd ..
python ci/check_lean_audit.py lake_build_local.log
python ci/check_axiom_report.py lake_build_local.log
```

Do not read `$LASTEXITCODE` after a pipeline to judge `lake build` — it
reports the last element of the pipeline, not the build. That has produced
a false clean here. Re-run without the pipe if the status matters.

Only `propext` and `Quot.sound` are permitted. `Classical.choice` fails.

## Reporting

State each gate's own result and exit status. State explicitly which gates
you did NOT run and why — an unrun gate is reported as unrun, never
omitted. Numbers are claims: quote what the command printed rather than
what you expected.
