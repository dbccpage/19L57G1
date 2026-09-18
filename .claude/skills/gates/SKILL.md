---
name: gates
description: Run the twelve CI gate families locally with freshness enforcement so a stale input cannot produce a false pass. Use before pushing, before claiming a gate result, or when asked whether the repository is green.
---

# Run the verification contract

**AuthorityEffect: None.** This skill runs commands and reports what they
printed. It approves nothing, merges nothing, and registers no claim. It
writes ignored logs and scratch exports; the Lean freshness check temporarily
rewrites one tracked artifact and restores its original bytes in a `finally`
block. A gate result it reports is evidence only about the command that
produced it. If this file disagrees with
`.github/workflows/verify.yml`, the workflow is correct and this file is
wrong.

## The rule that matters most

**A gate that did not run is not a gate that passed.** Every command has an
exit status; capture and check it. If an upstream command fails, its downstream check
may still exit 0 by reading a stale file. Report a gate as passing only
when you have seen its own command succeed in the same session.

This is not hypothetical. `ci/check_coverage.py` reads the untracked,
gitignored `coverage.json`. An old local copy can survive a failed generation
command. On a machine where `coverage` is not on PATH, `coverage run` and
`coverage json` can both fail while a later check reads that old file. That
has happened. It is why step 3 deletes the file first.

## Families

Run from the repository root. `code/` must be on `PYTHONPATH` for anything
outside pytest. The numbered families are the stable reporting census; the
workflow's job/step order is authoritative when reproducing CI exactly.

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
$coveragePath = Join-Path (Resolve-Path -LiteralPath ".").Path "coverage.json"
if (Test-Path -LiteralPath $coveragePath) {
  Remove-Item -LiteralPath $coveragePath -Force -ErrorAction Stop
}
if (Test-Path -LiteralPath $coveragePath) { throw "stale coverage report remains" }
python -m coverage run -m pytest -q
if ($LASTEXITCODE -ne 0) { throw "coverage test run failed" }
python -m coverage json -q
if ($LASTEXITCODE -ne 0) { throw "coverage JSON generation failed" }
if (-not (Test-Path -LiteralPath $coveragePath)) { throw "coverage report missing" }
python ci/check_coverage.py
if ($LASTEXITCODE -ne 0) { throw "coverage threshold/freshness check failed" }
```

Use `python -m coverage`, not `coverage` — the bare name is not always on
PATH, and that failure is silent in the way described above. Confirm
`coverage.json` did not exist before the generate step and does after.
Both line and branch must reach 95% independently.

For an operator machine with at least eight logical CPUs, the same full-suite
coverage can be accelerated without changing the hash-bound Python lock. Use
ephemeral, versioned plugins and a fixed worker count; `pytest-cov` combines
the eight workers into the one JSON consumed by the independent gate:

```powershell
$parallelUvCache = Join-Path $env:TEMP "19L57G1-parallel-pytest"
$env:UV_CACHE_DIR = $parallelUvCache
uv run --isolated --with-requirements requirements.txt `
  --with pytest-xdist==3.8.0 --with pytest-cov==7.1.0 `
  python -m pytest -n 8 --dist load --cov=code --cov-branch `
  --cov-report=json:coverage.json --cov-report=term
if ($LASTEXITCODE -ne 0) { throw "parallel coverage test run failed" }
python ci/check_coverage.py
if ($LASTEXITCODE -ne 0) { throw "coverage threshold/freshness check failed" }
```

Do not substitute `-n auto`: it can oversubscribe smaller machines. Adding
these plugins to `requirements.txt` is not a convenience edit; that file is
bound by the G1 receipt and requires a deliberate receipt repin.

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
$repoRoot = (Resolve-Path -LiteralPath ".").Path
$artifactScratch = [IO.Path]::GetFullPath((Join-Path $repoRoot "artifacts2"))
$insideRoot = $artifactScratch.StartsWith(
  $repoRoot.TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar,
  [StringComparison]::OrdinalIgnoreCase)
if (-not $insideRoot) { throw "artifact scratch escaped repository root" }
if (Test-Path -LiteralPath $artifactScratch) {
  Remove-Item -LiteralPath $artifactScratch -Recurse -Force -ErrorAction Stop
}
New-Item -ItemType Directory -Path $artifactScratch -ErrorAction Stop | Out-Null
$runners = @(Get-ChildItem -LiteralPath (Join-Path $repoRoot "code") `
  -Filter "run_*.py" -File | Sort-Object Name)
if ($runners.Count -eq 0) { throw "runner census enumerated no entry points" }
$env:PYTHONPATH = "code"
foreach ($runner in $runners) {
  python $runner.FullName --artifacts $artifactScratch
  if ($LASTEXITCODE -ne 0) { throw "runner failed: $($runner.Name)" }
}
python ci/compare_artifacts.py artifacts $artifactScratch
if ($LASTEXITCODE -ne 0) { throw "artifact comparison failed" }
```

`artifacts2/` is gitignored, but it is deleted only after its resolved path is
proved to be inside the repository. The reset prevents a removed or failed
runner from borrowing stale output. The nonempty guard proves the census ran.
The comparison then checks export sets in both directions: a committed artifact
with no regeneration, and a regenerated artifact never committed, both fail by
name.

### 6. Lean

```powershell
$repoRoot = (Resolve-Path -LiteralPath ".").Path
Push-Location lean4
try {
  lake clean
  if ($LASTEXITCODE -ne 0) { throw "lake clean failed" }
  lake build *> ../lake_build_local.log
  $buildExit = $LASTEXITCODE
} finally {
  Pop-Location
}
if ($buildExit -ne 0) {
  Get-Content lake_build_local.log -ErrorAction Stop
  throw "default Lean build failed"
}
Write-Host "default Lean build: PASS (full output in lake_build_local.log)"
python ci/check_lean_audit.py lake_build_local.log
if ($LASTEXITCODE -ne 0) { throw "Lean audit failed" }
python ci/check_axiom_report.py lake_build_local.log
if ($LASTEXITCODE -ne 0) { throw "axiom report comparison failed" }

$axiomPath = (Resolve-Path -LiteralPath "artifacts/lean_axioms.txt").Path
$originalAxiomBytes = [IO.File]::ReadAllBytes($axiomPath)
$originalAxiomHash = (Get-FileHash -LiteralPath $axiomPath -Algorithm SHA256).Hash
try {
  python ci/regen_axiom_artifact.py lake_build_local.log
  if ($LASTEXITCODE -ne 0) { throw "axiom regeneration failed" }
  $regeneratedAxiomHash = (Get-FileHash -LiteralPath $axiomPath -Algorithm SHA256).Hash
  $regeneratedHasCr = [IO.File]::ReadAllBytes($axiomPath) -contains 13
} finally {
  [IO.File]::WriteAllBytes($axiomPath, $originalAxiomBytes)
}
if ($regeneratedAxiomHash -cne $originalAxiomHash) {
  throw "regenerated axiom artifact is not byte-identical"
}
if ($regeneratedHasCr) { throw "regenerated axiom artifact contains CR bytes" }
Write-Host "axiom artifact regeneration: PASS (byte-identical, LF-only)"

Push-Location lean4
try {
  $modules = Get-ChildItem -Recurse -Filter *.lean -Path Derivation -File |
    ForEach-Object {
      $relative = $_.FullName.Substring($_.FullName.IndexOf("Derivation"))
      ($relative -replace "\.lean$", "") -replace "\\", "."
    }
  $census = [Collections.Generic.List[string]]$modules
  $census.Sort([StringComparer]::Ordinal)
  if ($census.Count -eq 0) { throw "Lean census enumerated no modules" }
  $censusText = ([string]::Join("`n", $census)) + "`n"
  $pinnedText = [IO.File]::ReadAllText(
    (Join-Path $repoRoot "artifacts/elaborated_modules.txt"))
  if ($censusText -cne $pinnedText) { throw "Lean census differs from its pin" }
  foreach ($module in $census) {
    $moduleOutput = & lake build $module 2>&1
    $moduleExit = $LASTEXITCODE
    if ($moduleExit -ne 0) {
      $moduleOutput | Write-Output
      throw "Lean target failed: $module"
    }
  }
  Write-Host "per-module elaboration: PASS ($($census.Count) pinned targets)"
} finally {
  Pop-Location
}
```

The default build writes its log by redirection rather than a pipeline, so the
captured exit code belongs to `lake build`. `lake clean` ensures the two default
roots actually emit fresh axiom reports. The regeneration is byte-compared and
LF-checked, then the original artifact bytes are restored even on failure. The
recursive census is nonempty, matches its committed pin, and every enumerated
module is built as its own target.

The written Lean job also rebuilds two research packages and audits their
axioms; run them after the per-module loop:

```powershell
python research/second_nofirst/verify_lean.py
if ($LASTEXITCODE -ne 0) { throw "second_nofirst Lean audit failed" }
python research/typed_translation/verify_lean.py
if ($LASTEXITCODE -ne 0) { throw "typed_translation Lean audit failed" }
```

Only `propext` and `Quot.sound` are permitted. `Classical.choice` fails.

### 7. Skills are well formed and declare no authority

```powershell
python ci/check_skills.py
```

Checks frontmatter shape, that each declared `name` matches its directory,
and the literal `AuthorityEffect: None`. It never inspects whether a
procedure is correct or was followed.

### 8. Every cited paper path resolves

```powershell
python ci/check_paper_citations.py
```

One `extract` function serves both the walk and the self-check, so a
pattern cannot pass the self-check and behave differently in production.
Traversal segments are refused and the resolved target must stay under
`paper/`. Prose must not write a `paper/<name>.md` path it does not want a
reader to follow — the gate cannot tell a live citation from a narrative
mention of a dead one.

### 9. Every ledger evidence citation resolves

```powershell
python ci/check_ledger_evidence.py
```

Every backticked token in the `**Python**` / `**Lean**` fields of every
`CL-*` entry must resolve: Lean names against `artifacts/lean_axioms.txt`,
tests against `tests/`, artifact keys against the committed exports. The
citation population is enumerated INDEPENDENTLY of the classifier, so a
token the classifier cannot place fails totality instead of cancelling out
on both sides.

What it does NOT do: judge wording. `Class: theorem` with `Lean: --`
passes. It cannot discharge "every theorem-level claim has Lean evidence";
that clause stays an operator claim, and the gate's own header says so.

### 10. Every parked Lean module is named for audit

```powershell
python ci/check_parked_audit.py
```

This independently computes the recursive module census and the transitive
import closure of `lean4/Derivation.lean`, then requires their difference to
equal `ParkedAudit.parkedModules`. A pass proves census/list agreement and
default-target wiring; it does not turn definitions into reported theorems.

### 11. Registered research provenance, tests, and typing

```powershell
python research/primitive_difference_tower/verify_manifest.py
if ($LASTEXITCODE -ne 0) { throw "primitive-difference manifest verification failed" }
Push-Location research/primitive_difference_tower
try {
  python -m unittest discover -s . -p "test_*.py"
  if ($LASTEXITCODE -ne 0) { throw "primitive-difference tests failed" }
  python -m mypy
  if ($LASTEXITCODE -ne 0) { throw "primitive-difference typing failed" }
}
finally {
  Pop-Location
}

python research/portable_interface/verify_pins.py
if ($LASTEXITCODE -ne 0) { throw "portable-interface pin verification failed" }
Push-Location research/portable_interface
try {
  python -m unittest discover -s . -p "test_*.py"
  if ($LASTEXITCODE -ne 0) { throw "portable-interface tests failed" }
  python -m mypy
  if ($LASTEXITCODE -ne 0) { throw "portable-interface typing failed" }
}
finally {
  Pop-Location
}

python research/blind_restart/verify_pins.py
if ($LASTEXITCODE -ne 0) { throw "blind-restart pin verification failed" }
Push-Location research/blind_restart
try {
  python -m unittest discover -s . -p "test_*.py"
  if ($LASTEXITCODE -ne 0) { throw "blind-restart tests failed" }
  python -m mypy
  if ($LASTEXITCODE -ne 0) { throw "blind-restart typing failed" }
}
finally {
  Pop-Location
}

$partialDecideOldPythonPath = $env:PYTHONPATH
$partialDecideCode = (Resolve-Path code).Path
try {
  $env:PYTHONPATH = $partialDecideCode
  python research/partial_decide/verify_pins.py
  if ($LASTEXITCODE -ne 0) { throw "partial-Decide pin/receipt verification failed" }
  Push-Location research/partial_decide
  try {
    python -m unittest discover -s . -p "test_*.py"
    if ($LASTEXITCODE -ne 0) { throw "partial-Decide tests failed" }
    python -m mypy
    if ($LASTEXITCODE -ne 0) { throw "partial-Decide typing failed" }
  }
  finally {
    Pop-Location
  }
}
finally {
  if ($null -eq $partialDecideOldPythonPath) {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  }
  else {
    $env:PYTHONPATH = $partialDecideOldPythonPath
  }
}
```

The manifest verifier requires full Git history. A protected-history failure
is the signal for an explicit provenance decision, not permission to run
`--repin` automatically. `research/primitive_difference_tower/verify_lean.py`
remains a separate manual Lean/axiom receipt and is not part of CI.
The partial-Decide verifier has no automatic repin: its sealed source snapshot
and import authority list move only by an inspected provenance edit.

The workflow enumerates nine more registered trees by the same shape
(pin verifier, then the tree's tests and typing from inside it):
`research/boundary_seed/verify_pins.py`,
`research/limit_and_observer/verify_pins.py`,
`research/second_inheritance/verify_pins.py`,
`research/second_nofirst/verify_pins.py`,
`research/second_stake/verify_pins.py`,
`research/second_stream/verify_pins.py`,
`research/side_free/verify_pins.py`,
`research/typed_translation/verify_pins.py`, and the four blocks above.
`tests/test_gates_skill_matches_workflow.py` fails by path when the workflow
runs a gate script this skill does not name; `research/README.md` lists the
trees the workflow does not enumerate at all.

### 12. Prose watchlist census

```powershell
python ci/check_prose_watchlist.py
```

Runs in the `python` job, before the tests. Every whole-word hit of a
digest-stored term list in tracked prose is pinned per file in
`ci/prose_watchlist.json`; a hit above its pin fails naming file, line, and
token, and a hit below it fails as a stale pin. `--report` lists every hit,
`--probe WORD` says whether a word is watched, `--add TERM --tag TEXT`
watches one more term by digest, and `--regen` rewrites the pin. Never
regenerate under a live injection: that adopts the defect as the baseline.
This gate reads prose only; identifiers stay with the firewall in
`tests/test_primitive_contact.py`. Expect `prose watchlist clean: N watched
terms, M files with pinned hits, K hits, census matches its pin`.

## This file can drift, and nothing checks it

Steps 7 and 8 were missing for as long as those gates existed, step 9 was
missing from the moment the ledger gate landed, and steps 10–11 later existed
in the workflow without appearing here. Those are historical examples of why
the workflow, not this prose, is authoritative.

No gate compares this file with `.github/workflows/verify.yml`. When they
disagree the workflow is right. Before trusting a count here, read the
workflow's step list and confirm it matches.

## Reporting

State each gate's own result and exit status. State explicitly which gates
you did NOT run and why — an unrun gate is reported as unrun, never
omitted. Numbers are claims: quote what the command printed rather than
what you expected.
