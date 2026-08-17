# CLAUDE.md — Execution Plan

## Repository boundary

**The blind protocol is scoped to the sealed derivation, not to the whole
repository.** It governs exactly `prompt/`, `paper/`, `code/`,
`lean4/Derivation/`, and `artifacts/`. The derivation's entire value is that
it was carried out blind; retiring the boundary retroactively would destroy
the only thing that makes it evidence. So it is sealed, not amended.

Its stopping conditions were run and reported met on 2026-08-16. **No gate
consumes that report**, and this scoping change is not its source — treat it
as an operator claim to be re-run, not a receipt.

Re-run on 2026-08-17 with output captured in `verification_20260817.md`.
All eight gate families pass at `052e657` (line 99.10%, branch 96.73%, 1314
axiom reports within `{propext, Quot.sound}`, artifacts byte-identical,
prompt hashes matching). **That discharges the mechanical clauses only.**
The clauses requiring judgement — that every notion carries a source
classification, that every theorem-level claim has Lean evidence or is
downgraded, that tied minima are retained unless eliminated by proof, and
that the paper states the strongest defensible terminal result — are **not**
discharged by any gate and remain operator claims. The 2026-08-16 sentence
above is therefore narrowed, not withdrawn: what was unverified about it is
still unverified, and now says so precisely.

Scoping note: `lean4/` is carved to `lean4/Derivation/`, but `code/`,
`paper/`, and `artifacts/` are named whole. A future `code/coda/` would
therefore fall inside the sealed contract, and inside mypy, coverage, and
artifact regeneration. Carve those the same way before putting CODA code
under them.

**No `paper/coda/` carve is in force. Do not write that tree, and do not
invent an exception to this paragraph.** `paper/` is named whole above, so a
subpath of it is inside the seal until an amendment here says otherwise —
and amending this contract is the author's act, not an agent's. This is
stated explicitly because it was breached: pull request #55 landed 30 files
under `paper/coda/` and they were removed in `6c3d880`. The rule previously
lived only in `coda_meta/LONG_HORIZON_PROMPT.md` and
`coda_meta/inter_repo_horizon_workflow.md`, both of which moved out of this
repository in `fd7e392` — so it is restated here, in the file that is always
loaded, rather than in a card that can leave.

**`coda/` and `coda_meta/` are gone from this repository.** They were
added on 2026-08-16 under their own rules and moved to
[`dbccpage/CODA`](https://github.com/dbccpage/CODA) on 2026-08-17 —
`coda_meta/` in `fd7e392`, `coda/` here. Every file was confirmed present
at the destination before removal: the 21 planning documents, and all 40
files under `coda/`, checked path by path against
`a83e4872f6a6ef7a78101af660274c08fb719dfd` rather than assumed.

An earlier version of this paragraph read: *"`coda/` and `coda_meta/` are
governed by their own rules, declared in their respective READMEs.
External citation is permitted there and nowhere else."* **WITHDRAWN** —
those READMEs no longer exist here, so the sentence pointed at nothing.

The permission it granted is withdrawn with it. **External citation is
not permitted anywhere in this repository.** With the CODA trees gone,
what remains is the sealed derivation alone, and the blind protocol
governs all of it. That is a narrowing, not a loosening: the exception
existed only for directories that have left.

The record of what moved, and the withdrawal that came with it, is kept
here rather than in the repository a reader may not be able to open —
`dbccpage/CODA` is **private**. `coda_meta/README.md` carried this note,
which concerns *this* repository and so survives its own file:
*"An earlier draft said the FOC/FDA `paper/coda` skeletons were bound.
That was false. Commit `5b6a9d9` and PR #52 contain no `paper/coda`
files."*

- Within the sealed derivation: all work uses only this repository. No
  network research, no external files, no prior project instructions, no
  plugins/agents/skills/memories, no user guidance during the derivation.
- `prompt/prompt.md` and `prompt/seed_prompt.md` are read-only inputs and must
  remain byte-identical (SHA-256 recorded in the paper).
- Toolchains already installed on this machine (Python 3.14, pytest, coverage,
  mypy, Lean 4.33 / Lake 5.0 via elan) are metatheoretic apparatus, not inputs.

## Execution plan

1. Verify Python and Lean toolchains compile a trivial file (primary
   directives 1–2). No object-language content in this step.
2. Execute `prompt/seed_prompt.md`:
   - Challenge 0: analyze the initial inscription `<>` with no object-language
     operations; prove exactly what follows and what does not.
   - Challenge 1: analyze the supply of `<a>`; separate supply, mention,
     admission, current-state designation, retention, observation, equality.
   - Challenge 2: analyze the retained pair `<a>`, `<ab>`; prove what changed
     by admission and what remains internally unavailable.
   - Challenge 3: declare a precise meaning of internal separability, prove
     the current regime fails it, enumerate all minimum one-step augmentations
     under a declared candidate space and declared cost measures, count every
     capability each candidate uses, retain all tied non-isomorphic minima.
   - Autonomous continuation: for each surviving branch, define the weakest
     deterministic challenge generator justified by that branch alone; attempt
     fifteen accepted augmentation rounds per finite branch; quotient branches
     only under an implemented isomorphism relation; replay every certified
     result from genesis; export the exact frontier under declared resource
     bounds and prove what is complete within those bounds.
3. Implement the finite reference model in `code/` with tests in `tests/`.
4. Formalize theorem-level claims and countermodels in `lean4/`.
5. Write `paper/paper.md`, `paper/paper_change_log.md`,
   `paper/paper_claim_ledger.md`. Known mathematics appears only in the final
   post-hoc comparison section.

## Assumption discipline

- Every substantive notion is classified as exactly one of: metatheory
  apparatus; supplied object-language datum; externally imposed challenge;
  admitted primitive; derived definition; proved theorem; deterministic
  computation; countermodel; optional realization; conjecture; open
  obstruction; refuted claim.
- The words "forced", "minimal", "free", "canonical", "equivalent",
  "universal", "complete" are used only with a proof or a precise conditional
  scope.
- Presentation identity, internal identity, observational equivalence,
  behavioral separation, and semantic interpretation are kept distinct.
- Supply, mention, admission, current-state designation, retention,
  observation, and equality are never conflated.
- Absence of a test is never converted into equality. A model proposal never
  mutates admitted state without a separately defined admission event.
- Receipts (hashes, test passes, parser success) are never treated as proof of
  an unverified mathematical payload.
- No known theory is targeted or named during the derivation.  The
  post-hoc comparison originally allowed in the paper's final section was
  withheld by caller correction (2026-08-11): no external architecture,
  theory, or project terminology appears **anywhere in this repository**
  outside the read-only seed prompt.

  That is the clause's original wording, and it holds again without
  exception.  Between 2026-08-16 and 2026-08-17 it was scoped to "the
  sealed derivation" rather than the repository, because `coda/` and
  `coda_meta/` had been added under separate rules permitting external
  citation.  Those directories have moved to `dbccpage/CODA`, so the
  exception has no subject and the unscoped statement is restored.  This
  is a return to the stronger claim, not a new one — recorded because a
  reader comparing revisions would otherwise see the clause widen and
  reasonably suspect it of being quietly strengthened.

  The vocabulary firewall in `tests/test_primitive_contact.py` is
  unaffected and still walks the whole tree via `git ls-files`: the 102
  working-denylist identifiers remain barred outside
  `contact/analysis/`.

## Proof gates

- Every theorem-level claim used by the paper has a Lean 4 proof, or is
  explicitly downgraded to computation, conjecture, countermodel, or OPEN.
- `lake build` passes with no `sorry`, `admit`, user-declared `axiom`,
  `unsafe`, or `partial`.
- Every exported theorem cited by the paper has a `#print axioms` report, and
  any library axiom reliance is recorded in the claim ledger.
- Failed theorem targets remain counterexamples or OPEN — never prose proofs.
- Minimality and necessity claims are proved by exhaustive enumeration over a
  declared finite candidate space, or downgraded to conditional scope.

## Test gates

- Python code in `code/` is deterministic and fully type-annotated; mypy
  passes in strict mode.
- All tests pass; line coverage ≥ 95% and branch coverage ≥ 95% over project
  Python code.
- Negative tests exist for every smuggling or false-minimality failure
  discovered during the derivation.
- Every certified result is replayed from genesis by an implemented replay
  rule; machine-readable branch/level/assumption/claim data is exported.
- Equality, minimality, isomorphism, survivor counts, and proof status are
  decided only by implemented algorithms, never by judgment calls outside the
  code.

## Stopping conditions

- A branch stops when no next challenge or no justified response exists, or at
  the declared resource bound (fifteen accepted augmentation rounds per finite
  branch; deterministic node/arity/cost bounds stated in the paper), with the
  exact frontier exported and a proof of what is complete within the bound.
- The task stops only when: every introduced notion has a source
  classification; every state change has a replayable admission history; every
  theorem-level claim has Lean evidence or is downgraded; every computational
  claim has deterministic Python evidence; all tied minimum branches are
  retained unless eliminated by proof; both coverage thresholds are met; Lean
  builds without forbidden escapes; the working tree is clean with all
  intentional artifacts committed; `prompt/prompt.md` is byte-identical to the
  initial file; and the paper states the strongest defensible terminal result,
  including termination or failure, without targeting a predetermined
  conclusion.

---

# Operating manual

Everything below is metatheoretic apparatus (how to drive the toolchain and
where things live), not object-language input. It records the verification
contract already enforced by `.github/workflows/verify.yml` and `ci/`.

## Commands

Run from the repository root. Shell examples are PowerShell (the primary
platform is Windows).

### Tests

```powershell
python -m pytest                      # whole suite (pyproject sets testpaths=tests, pythonpath=code)
python -m pytest tests/test_iso.py    # one file
python -m pytest tests/test_iso.py::test_tokens_are_forgotten   # one test
python -m pytest -k equivariance      # by keyword
```

`pyproject.toml` puts `code/` on `pythonpath` for pytest only. Anything run
outside pytest (the `run_*.py` entry points) needs `$env:PYTHONPATH = "code"`.

### The eight gate families CI enforces

`.github/workflows/verify.yml` runs two jobs, `python` and `lean`. Between
them they are eight gate families. The local equivalents:

```powershell
# 1. prompt byte-identity (read-only inputs)
python ci/check_prompt_hashes.py

# 2. transport document citations bound to Lean sources
python ci/check_transport_citations.py

# 3. tests under coverage, then the independent dual 95% gate.
#    Use `python -m coverage`, never bare `coverage` -- the bare name is
#    not always on PATH, and that failure used to be silent.
python -m coverage run -m pytest -q; python -m coverage json -q
python ci/check_coverage.py           # line AND branch must each reach 95%

# 4. strict typing (config in pyproject: strict = true, files = ["code"])
python -m mypy

# 5. artifact regeneration must be byte-identical (see below)

# 6. Lean build, forbidden-token/axiom audit, and byte-identical
#    regeneration of the axiom artifact (see below)

# 7. skills are well formed and declare no authority
python ci/check_skills.py

# 8. every paper/*.md path cited inside paper/ resolves
python ci/check_paper_citations.py
```

`ci/check_coverage.py` lives outside `code/` on purpose so it is not part of
the measured source. It reads `coverage.json`, so generate that first — and
it now refuses to believe a report it cannot date. `coverage.json` is
**untracked** (it was tracked, which meant a fresh clone shipped a report and
a branch switch silently restored it over a fresh one — that happened, and
reverted a just-measured report to a two-day-old one). The gate fails by name
if the report is missing, if its file set differs from `code/**/*.py`, or if
any measured source has been modified since `meta.timestamp`. The file-set
check alone is not enough: across that branch-switch swap the file set was
identical, so only the timestamp check catches it. The timestamp check errs
conservatively — touching a source without changing it fails until you
regenerate, which is the safe direction.

`ci/check_transport_citations.py` enumerates the citation population of
`contact/analysis/lean_theorem_transport.md` *independently of the parser
that classifies it* — every backticked token ending in a colon and digits —
so a citation the classifier cannot see fails the totality check instead of
cancelling out on both sides of it. Path-prefixed citations count, and
`--fix` preserves those prefixes when it regenerates line anchors. A
totality invariant computed with the classifier's own pattern proves
nothing; that was a real defect, not a hypothetical one.

### Artifacts

Every `code/run_*.py` writes deterministic JSON into `--artifacts DIR`
(default `artifacts`). To check that the committed artifacts still match
what the code produces:

```powershell
$env:PYTHONPATH = "code"
Get-ChildItem code/run_*.py | ForEach-Object { python $_.FullName --artifacts artifacts2 }
python ci/compare_artifacts.py artifacts artifacts2
```

`artifacts2/` is gitignored, so it is the scratch directory for this check.
To intentionally update the committed artifacts, rerun with
`--artifacts artifacts` and commit the diff.

### Lean

```powershell
cd lean4
lake build 2>&1 | Tee-Object -FilePath ../lake_build_local.log
cd ..
python ci/check_lean_audit.py lake_build_local.log     # forbidden tokens + axiom whitelist
python ci/check_axiom_report.py lake_build_local.log   # log must match artifacts/lean_axioms.txt
```

`lake_build_*.log` is gitignored. The axiom report is produced by compiling
`lean4/Derivation.lean`; if the log comes back with no `#print axioms` lines,
force that root module to rebuild before auditing.

When a theorem is renamed, added, or removed, `artifacts/lean_axioms.txt` is
rewritten by `python ci/regen_axiom_artifact.py <log>`, which writes bytes
explicitly so a shell redirect cannot reintroduce CRLF. It overwrites the
committed artifact, so run it deliberately, then commit the diff. Artifacts
derived from it — the completion receipts and the dependency graph — must be
regenerated *after* it, not before; that ordering is the whole coupling, and
no Python source hard-codes Lean theorem names.

**The axiom boundary, stated exactly.** The audit's reach is the set of
declarations enumerated by the committed `#print axioms` inventory in
`lean4/Derivation.lean`. It certifies that every report in that inventory
lies within `{propext, Quot.sound}`. It does not by itself establish that the
inventory names every exported declaration, nor that every report is present.
Read "axiom-clean" as a claim about the enumerated reports only, unless
declaration completeness or report completeness is independently proved.

## Architecture

### The one pattern to know: a topic is a five-file family

Almost every subject in this repository appears five times under the same
stem, and changing one member usually obliges the others:

| role | path |
|---|---|
| computation | `code/derivation/<topic>.py` |
| artifact writer | `code/run_<topic>.py` |
| tests | `tests/test_<topic>.py` |
| proofs | `lean4/Derivation/<Topic>.lean` |
| output | `artifacts/<topic>.json` |

Prose lives in `paper/`, but not one-per-topic: `paper/paper.md` is the
spine, and the other `paper/*.md` files are per-investigation write-ups.
Every claim carries a stable `CL-*` ID in `paper/paper_claim_ledger.md`,
which names its Python evidence (artifact key and/or test name) and its Lean
theorem names. `artifacts/claims.json` holds the computed values for the
ledger IDs, so ledger prose and machine output are cross-checkable.

### The kernel, read in this order

The first six modules are the whole object language; the ~25 other modules in
`code/derivation/` are studies layered on top of them. This is the
*computational* object language only — the Python side. It is not a reading
order for `lean4/`, whose contact and passage modules are entered through
`paper/paper_claim_ledger.md`, not through this sequence.

1. `model.py` — `Regime` (frozen: `data`, `forms`, `insts`, `rules`, `reqs`)
   plus the event types. State changes *only* through admission events
   (`AdmitDatum/Form/Inst/RuleAll`) or `Impose`; `Supply` is an external
   presentation event that provably does not change state. `replay` rebuilds
   a regime from an event list — this is what makes every result replayable
   from genesis.
2. `observe.py` — contexts (a form plus a slot tuple with holes), profiles
   (which pluggings are derivable), and the declared sense of *internally
   separable*: two data are separable exactly when their profiles differ.
3. `candidates.py` — the declared candidate space of one-step augmentations
   (deltas) and the two declared cost measures `mu1`/`mu2`, plus
   `min_responses`. The cost-2 enumeration is pruned by four named lemmas,
   each with an unpruned cross-check test.
4. `iso.py` — the implemented isomorphism relation and `canonical` keys.
   Presentation tokens are deliberately forgotten. This is the *only*
   sanctioned way to quotient branches, and it is cross-checked against a
   brute-force minimum over all bijection pairs.
5. `engine.py` — Challenges 0–3 and the branch tree. Carries two admission
   *readings* (L and F) as separate genesis histories, and separates the
   declared pair-separation closure policy from the external supply policy
   (`supply=False` runs are the closed-system baseline).
6. `export.py` — deterministic JSON, normalized DAG tree exports, and
   `verify_full_export`, which replays every node and checks its regime hash.

### Invariants that break CI if you miss them

- **Byte-determinism.** Exports carry no timestamps and no environment data,
  keys are sorted, and `.json.gz` uses a fixed mtime and compression level.
  Any change to a derivation module means regenerating and committing the
  affected artifacts, or gate 4 fails.
- **The CI runner census is a glob, and `artifacts/` is its own pin.**
  `.github/workflows/verify.yml` enumerates `code/run_*.py` at the TOP LEVEL
  of `code/` instead of naming each entry point, so a new runner is
  regeneration-checked without anyone remembering to register it. An earlier
  version of this line said the list was hand-enumerated and that a new entry
  point went unchecked until added there; that is WITHDRAWN as of the census
  change. Drift is caught in both directions by `ci/compare_artifacts.py`: a
  committed artifact with no regeneration fails, and a regenerated artifact
  that was never committed fails. No separate census artifact is needed for
  the runners, because the committed export set already plays that role — the
  Lean module census needs `artifacts/elaborated_modules.txt` precisely
  because elaboration leaves no committed output behind to compare. A runner
  placed in a SUBDIRECTORY of `code/` is outside the census.
- **Skills hold no authority, and the declaration is enforced.** Skills
  live in `.claude/skills/<name>/SKILL.md`, are tracked, and each must
  carry the literal line `AuthorityEffect: None`. `ci/check_skills.py`
  checks that, plus frontmatter shape and that the declared `name` matches
  its directory, so an invoked skill and the tracked file cannot diverge.
  The mechanical check exists because prose drifts: without it a skill
  could acquire authority by rewording its own description. What the gate
  does NOT do is judge whether a procedure is correct or was followed — a
  skill is prose plus commands, and no CI step can check that a human or a
  model obeyed it. Read a pass as "well formed and claiming no authority",
  never as "the skills are right".
- **A cited paper path must resolve.** `ci/check_paper_citations.py` walks
  every `paper/<name>.md` token appearing inside `paper/` and requires the
  file to exist. A page citing a sibling that lives only on a branch is a
  dead link on `main`; that shipped once and a reviewer, not a gate, caught
  it. On a `pull_request` event `actions/checkout` checks out the merge
  commit, so the tree CI sees is the state that would land, and plain
  existence therefore has merge-result semantics. The gate cannot tell a
  live citation from a prose mention of a deliberately dead path — an
  incident narrative, a withdrawal notice — so prose must not write a
  `paper/<name>.md` path it does not want a reader to follow, and should
  name such documents descriptively instead.
- **Lean may only use `propext` and `Quot.sound`.** `ci/check_lean_audit.py`
  rejects anything else, so `Classical.choice` is out — decidability has to
  be constructive.
- **The forbidden-token scan is plain text over whole `.lean` files.** It
  matches `sorry`, `admit`, `unsafe`, `partial` and leading `axiom` anywhere,
  including inside comments and doc strings. Phrase Lean prose around those
  words — and mind line WRAPPING: the pattern is `^\s*axiom\s`, so a prose
  line that happens to wrap onto the word `axiom` fails the gate even though
  the sentence is innocuous. This has happened; so has a docstring line
  wrapping onto `theorem` and defeating a grep-based theorem count.
- **Each exported theorem the paper cites needs a `#print axioms` line** in
  `lean4/Derivation.lean`, and `artifacts/lean_axioms.txt` must match the
  fresh build log.
- **Every module elaborates, whether or not the root imports it.** `lake
  build` only builds `defaultTargets`, so a module absent from
  `lean4/Derivation.lean`'s imports was never typechecked by CI — the
  forbidden-token scan reads `.lean` files as text and does not elaborate
  them, so a type error in such a module used to merge green. The `lean` job
  now builds every `lean4/Derivation/**/*.lean` as its own Lake target, from
  a recursive census matching `ci/check_lean_audit.py`'s `rglob`, so a module
  in a subdirectory cannot escape it either. An
  earlier version of this line claimed the root "imports every module"; that
  became false when the first parked modules landed, nothing detected it, and
  the claim is WITHDRAWN in favour of the enforced one above.
- **The census is pinned, not merely computed.** It is diffed against
  `artifacts/elaborated_modules.txt`, so adding or removing a module fails
  the `lean` job until that artifact is regenerated. An empty-census guard
  catches an enumeration that finds *nothing*; only the diff catches one that
  finds *some*. Regenerate from the repository root with:

  ```powershell
  cd lean4
  $m = Get-ChildItem -Recurse -Filter *.lean -Path Derivation | ForEach-Object {
    $rel = $_.FullName.Substring($_.FullName.IndexOf("Derivation"))
    ($rel -replace "\.lean$","") -replace "\\","."
  }
  $s = [System.Collections.Generic.List[string]]$m
  $s.Sort([System.StringComparer]::Ordinal)   # ordinal, to match LC_ALL=C sort
  [System.IO.File]::WriteAllText("$PWD\..\artifacts\elaborated_modules.txt",
    ($s -join "`n") + "`n")                    # LF only; artifacts/** is -text
  ```

- **Elaboration is not auditing — the open residual.** A module the root does
  not import is now typechecked, but it still contributes no `#print axioms`
  report, so `ci/check_lean_audit.py`'s axiom whitelist never sees it. A
  parked module could therefore depend on `Classical.choice` and no gate
  would fail. The forbidden-token scan still reads it, and it still must
  compile; its *axioms* are unchecked. Do not read "every module elaborates"
  as "every module is audited". Closing this needs a declaration census for
  parked modules, and the obvious regex approach is the one already known to
  break here — a docstring line beginning with the word `theorem` defeated a
  grep count twice — so it is left OPEN rather than closed badly.
- **Line endings are pinned.** `.gitattributes` marks `prompt/**` and
  `artifacts/**` as `-text`. Never let an editor or a CRLF conversion rewrite
  those files — it breaks both the prompt hash gate and byte comparison.

### Proving a gate: the injection record

A gate is not proved by being green. It is proved by failing on the exact
defect it exists to catch, with the failure naming the injected object, and
by recovering when the injection is reversed. Green before and after, with
nothing in between, shows only that the gate is quiet.

Injections are minimal and reversible, and receipts are NEVER regenerated
while one is live — regenerating `elaborated_modules.txt` or
`lean_axioms.txt` under an injection adopts the defect as the new baseline
and destroys the test.

What has actually been injected, and what failed:

| Gate | Injection | Observed failure |
|---|---|---|
| Lean census pin | added `Derivation/PinProbe.lean` | `diff` against `elaborated_modules.txt` |
| Per-module elaboration | type error in a parked module | root `lake build` stayed green; the per-module loop failed |
| Runner census | new unregistered `code/run_zzz_probe.py` | census went 24 → 25 with no registration, then `FAIL: regenerated but not committed: zzz_probe.json` |
| Regeneration, committed side | deleted one regenerated `*.json` | `FAIL: missing regeneration: apartness.json` |
| Regeneration, other side | stray `*.json` in the regenerated dir only | `FAIL: regenerated but not committed` |
| Empty-census guard | census pointed at a directory with no matches | guard fired before the pin was consulted |
| Skill authority | probe skill with no `AuthorityEffect: None` line | `FAIL: ... does not declare 'AuthorityEffect: None'` |
| Skill identity | frontmatter `name` ≠ directory name | `FAIL: ... frontmatter name 'wrong_name' does not match directory` |
| Skill shape | directory with no `SKILL.md`; body with no frontmatter | both named individually |
| Paper cross-reference | citation to a sibling that exists on no branch | `FAIL: … cites paper/zzz_probe_absent.md, which does not exist` |
| Paper cross-reference, real case | the original dead link re-injected verbatim | `FAIL: … cites paper/representative_selection.md, which does not exist` |

What injection does NOT prove: that the population is the right
mathematical object. A perfect pin of the wrong set is still the wrong set.
It also cannot close the parked-module axiom residual above — it can only
demonstrate that the residual is still live.

### Claim hygiene

`paper/paper_change_log.md` records material changes newest-last, including
withdrawn and repaired claims; `paper/pr11_correction_ledger.md` is a worked
example of narrowing an overclaim. When a proof turns out to cover less than
the prose asserted, the established move in this repository is to weaken the
statement in the ledger and the paper — never to keep the wording and lean on
the receipt.
