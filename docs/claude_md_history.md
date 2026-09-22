# CLAUDE.md history (archived 2026-09-21)

**Historical; not binding.** This is the full text of `CLAUDE.md` exactly as
it stood before the 2026-09-21 split (last changed in `4c9b5d8f`,
2026-09-08), kept byte for byte below the rule. It holds the dated history
the current file no longer carries: withdrawn statements and the reasons
for them, incident narratives, superseded counts, and the completed
execution plan. The current rules are in `CLAUDE.md`. The injection record
continues in `docs/injection_record.md`. Where this archive and `CLAUDE.md`
differ, `CLAUDE.md` governs.

---

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
All eight gate families then defined pass at `052e657` (line 99.10%, branch 96.73%, 1314
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

- **Refused grid, recorded (author, 2026-08-31).** An outside
  classification grid — nine single-letter slot names and an
  accompanying phrase — was offered through the operator channel for the
  primitive-difference inventory and refused as vocabulary by the
  author: every letter individually is generic mathematics, so no
  denylist fired, but the pattern of names was an outside architecture's
  grid, and structural smuggling is still smuggling.  The inventory's
  names are repo-native; the offered names are reproduced nowhere in
  this repository, this clause included, because describing without
  naming is the only way to record a refusal without committing the
  smuggle it refuses.  Any future claim of independent convergence
  between this repository's inventory and any external architecture's
  slot grid is false by construction and must cite this clause.  The
  paper's own refusal note is pinned by a digest test so it cannot
  drift out.

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
contract written in `.github/workflows/verify.yml` and `ci/`, and run
locally — see **No hosted CI** immediately below.

## No hosted CI — settled, do not reopen

**This repository does not use hosted GitHub Actions CI, and never will.**
This is a permanent decision by the author (2026-09-08), not a lapse, an
outage, or a billing problem to be fixed. Treat it as closed.

`.github/workflows/verify.yml` is kept as the written contract: it is the
canonical list of the twelve gate families and the order they run in. It
does **not** execute. No push, pull request, or merge triggers a hosted
run, and none is expected to.

What "green" means here: **every gate is run locally by the author (or by
an agent at the author's direction) before a merge, and the pass is a local
receipt.** A receipt in a PR body, a README, or a change-log entry is a
local run unless it explicitly says otherwise. There is no hosted run to
consult, ever.

Consequences, so no one asks again:

- Do **not** propose enabling, restoring, paying for, re-instating, or
  "fixing" hosted CI, and do not open issues or PRs toward that end.
- Do **not** read an absent, dormant, skipped, or failed Actions run as a
  defect, a regression, or a thing to investigate. There is nothing there
  to investigate.
- A merge is authorized on the strength of local receipts alone. The
  author merges; the absence of a hosted check never blocks or gates that.
- Sentences elsewhere in this file that say a gate is "enforced by CI",
  that "CI sees" a merge state, or that describe a hosted rollup, are
  historical wording from when hosted runs were contemplated. Read them as
  "the gate that `verify.yml` defines, run locally." This subsection is the
  authority; where it conflicts with older phrasing, it wins.

The peer file `AGENTS.md` states the same policy in short form for agents
that read it instead of this one.

## Pull-request topology

Every pull request must target `main` directly. Stacked pull requests are
prohibited: do not open a pull request whose base is another unmerged topic
branch. If work depends on an open pull request, merge that dependency first,
then rebase from the new `main`, or combine the work into one pull request.
This keeps review, CI, provenance pins, and merge authority bound to one head
and one base at a time.

## Commands

Run from the repository root. Shell examples are PowerShell (the primary
platform is Windows).

### Tests

```powershell
python -m pytest                      # pinned-lock suite, matching CI
python -m pytest tests/test_iso.py    # one file
python -m pytest tests/test_iso.py::test_tokens_are_forgotten   # one test
python -m pytest -k equivariance      # by keyword
```

`pyproject.toml` puts `code/` on `pythonpath` for pytest only. Anything run
outside pytest (the `run_*.py` entry points) needs `$env:PYTHONPATH = "code"`.

On a machine with at least eight logical CPUs, use eight fixed pytest workers
for the exhaustive local suite instead of the single-worker command. The two
parallel test plugins stay ephemeral because `requirements.txt` is hash-bound
by the G1 receipt; adding them to that file is a separate receipt-repin act.
`pytest-cov` combines all eight workers into the one fresh report consumed by
the independent coverage gate. Keep the fixed bound rather than `-n auto`,
which can oversubscribe smaller machines:

```powershell
$parallelUvCache = Join-Path $env:TEMP "19L57G1-parallel-pytest"
$env:UV_CACHE_DIR = $parallelUvCache
uv run --isolated --with-requirements requirements.txt `
  --with pytest-xdist==3.8.0 --with pytest-cov==7.1.0 `
  python -m pytest -n 8 --dist load --cov=code --cov-branch `
  --cov-report=json:coverage.json --cov-report=term
python ci/check_coverage.py
```

### The twelve gate families CI enforces

`.github/workflows/verify.yml` runs three jobs, `python`, `lean`, and
`research`. Between them they are twelve gate families. Earlier versions of
this line said two jobs and nine, then three jobs and ten, then three jobs
and eleven; all three are WITHDRAWN. The eleventh arrived with the
parked-module axiom census and is numbered 10 below, next to the census pin
it completes; the research job is 11 because it is unlike the others. The
twelfth, the prose watchlist census, runs in the `python` job and is
numbered 12 below: the numbering is a stable reporting census, and the
workflow's step order is what CI actually runs. The local equivalents:

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

# 9. every evidence citation in the claim ledger resolves. Population
#    enumerated independently of the classifier, so an unplaceable token
#    fails totality rather than cancelling out on both sides. It checks
#    that names RESOLVE, never that wording matches proof.
python ci/check_ledger_evidence.py

# 10. every module UNDER `lean4/Derivation/` and outside `Derivation.lean`'s
#     import closure is named in `lean4/ParkedAudit.lean`, which is what
#     emits its axiom reports. The scope clause is load-bearing: a
#     top-level `lean4/*.lean` is outside every census in this repository,
#     including this one, and `ParkedAudit.lean` is itself such a file.
#     Python rather than Lean on purpose: `ParkedAudit` checks its own
#     list against the compiled environment, but a module NOTHING imports
#     is absent from that environment, so Lean cannot see it is missing.
python ci/check_parked_audit.py

# 11. the registered research trees' source pins still match their inputs,
#     and their own tests and strict typing pass. NOT a sealed-derivation gate:
#     it guards `research/`, which is outside the seal. Run from the
#     repository root, then from inside the tree:
python research/primitive_difference_tower/verify_manifest.py
python research/portable_interface/verify_pins.py
python research/blind_restart/verify_pins.py
$env:PYTHONPATH = "$PWD/code"
python research/partial_decide/verify_pins.py
```

```powershell
cd research/primitive_difference_tower
python -m unittest discover -s . -p "test_*.py"
python -m mypy
cd ../..

cd research/portable_interface
python -m unittest discover -s . -p "test_*.py"
python -m mypy
cd ../..

cd research/blind_restart
python -m unittest discover -s . -p "test_*.py"
python -m mypy
cd ../..

cd research/partial_decide
python -m unittest discover -s . -p "test_*.py"
python -m mypy
cd ../..
```

```powershell
# 12. the prose watchlist census matches its pin. Physics-shaped and
#     outside-target words, stored as DIGESTS in `ci/prose_watchlist.json`
#     so the list is not itself the smuggle it watches for; every whole-word
#     hit in tracked prose is pinned per file, and the gate fails in both
#     directions -- a hit above its pin names the file, line, and token, a
#     hit below it names the stale pin. `--probe WORD` says whether a word
#     is watched, `--report` lists every hit, `--add TERM --tag TEXT` watches
#     one more term by digest, `--regen` rewrites the pin deliberately and
#     never under a live injection. It reads PROSE: identifiers with `_` or
#     digits are never split, so those stay with the firewall in
#     `tests/test_primitive_contact.py`. This reads what that cannot.
python ci/check_prose_watchlist.py
```

The partial-Decide computation enumerates candidates and replays each
candidate's `Impose` and admission-event values only into an ephemeral
comparison child used to compute a quotient key. It derives no decision input
from the panel, authorizes no candidate, persistently applies no response,
and commits no event to the declared base. This bounded enumeration is not an
object-language demand generator; no such generator is supplied by that
package. Its corresponding scoped terminals are
`NO_PANEL_DERIVED_INPUT`,
`NO_AUTHORIZED_OR_PERSISTENT_RESPONSE_APPLICATION`, and
`NO_EVENT_COMMITTED_TO_DECLARED_BASE`, alongside the narrower adapter,
authorization, and generator refusals recorded in its receipt.

After the partial-Decide verifier's early custody preflight, receipt rendering
runs in a fresh `-I -B -S` child that installs its audit boundary and explicit
project paths before importing the receipt or derivation modules. That does
not authenticate the already-running verifier/entry point, interpreter,
standard library, Git executable, or parsed pin JSON. Deliberate receipt
writing refuses an existing link, reparse point, directory, or other
non-regular target and atomically replaces a safe target through a flushed,
synchronized, exclusively created same-directory temporary regular file.

The primitive-difference portion of gate 11 is expected to go red on a
legitimate change to one of its protected paths, while the other registered
research checks should remain green unless one of their exact inputs or
contracts moved. A pull request that
edits a module pinned in `research/primitive_difference_tower/SOURCE_MANIFEST.json`
will fail it. That is the signal to repin — not a defect in the pull
request — and that coupling is exactly why this tree was kept out of CI
originally. The job makes drift VISIBLE; whether drift BLOCKS is branch
protection, which is a policy setting rather than a property of this file.

Why it was added: on 2026-08-21, merging #76 and #77 left `main` with five
failing research tests **while the workflow reported SUCCESS**. Neither
pull request could see it — the two changes only interact once both are
present, and no job read the tree. Every gate was green and the repository
was broken. That is an observed instance, not a hypothetical.

What gate 11 does NOT cover: `verify_lean.py`. It builds the research Lake
package, which needs elan and compiles the sealed package as a dependency —
the expense the job exists to avoid. **The research tree's axioms therefore
remain a manual receipt, unchecked by any gate.** An earlier version of this
line called it "a second live residual alongside the parked-module one". The
parked-module one is now closed by `lean4/ParkedAudit.lean`, so this is the
last of the two and that comparison is WITHDRAWN. It is recorded rather than
closed badly.

Repairing a gate-11 failure: `verify_manifest.py --repin`, then revise the
prose it names (`CLAIM_LEDGER.md`, `FINDINGS.md`) — the verifier fails until
the prose matches. Review a repin by diffing the PARSED JSON, not the text:
`--repin` re-serializes with `indent=2` and rewrote 135 lines to change 3
values the one time it has been run. That procedure applies only to the
primitive-difference manifest. The other registered trees have their own
pin policies; partial Decide deliberately provides no automatic repin.

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
BOTH default targets: `lean4/Derivation.lean` for its hand-maintained
`#print axioms` inventory, and `lean4/ParkedAudit.lean` for the twelve modules
the root does not import. If the log comes back with no `#print axioms` lines,
force those roots to rebuild before auditing — touching both is what
regenerates the full report set.

When a theorem is renamed, added, or removed, `artifacts/lean_axioms.txt` is
rewritten by `python ci/regen_axiom_artifact.py <log>`, which writes bytes
explicitly so a shell redirect cannot reintroduce CRLF. It overwrites the
committed artifact, so run it deliberately, then commit the diff. Artifacts
derived from it — the completion receipts and the dependency graph — must be
regenerated *after* it, not before; that ordering is the whole coupling, and
no Python source hard-codes Lean theorem names.

**The axiom boundary, stated exactly.** The audit's reach is the union of two
populations, gathered differently, and the difference matters. The first is
the set of declarations enumerated by the committed `#print axioms` inventory
in `lean4/Derivation.lean` — hand-maintained, so it does not by itself
establish that it names every exported declaration in the root's closure. The
second is every **theorem** of the twelve modules named in
`lean4/ParkedAudit.lean`, enumerated from the compiled environment rather than
by hand.

An earlier version of this paragraph said the second population was "every
non-internal declaration" and that "within those twelve modules it IS
declaration-complete". That is **WITHDRAWN** — it was false, and it was the
worse kind of false, because this is the paragraph a reader quotes instead of
re-deriving. `ParkedAudit.lean` filters on `ConstantInfo.isTheorem`, so
definitions, structures, and generated constructors are not reported, and the
twelve modules carry roughly two dozen such declarations. The narrower
statement 150 lines below was right and this one was not.

The audit certifies that every report in that union lies within
`{propext, Quot.sound}`. Read "axiom-clean" accordingly: **theorems only** in
both halves, complete over the parked twelve's theorems, and a claim about
the enumerated reports only for the root inventory.

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

- **Elaboration is not auditing — CLOSED, and how.** An earlier version of
  this entry said a module the root does not import "contributes no `#print
  axioms` report", that a parked module "could therefore depend on
  `Classical.choice` and no gate would fail", and left the residual OPEN
  because the obvious regex approach was already known to break here. That is
  **WITHDRAWN**. `lean4/ParkedAudit.lean` now emits one report per theorem
  for all twelve modules outside the root's import closure — 48 of them,
  taking the audit from 1424 reports to 1472. All are within the whitelist:
  nothing was hiding, but the hole was real.

  Reach, stated exactly: **theorems**, as Lean classifies them, not
  definitions. That matches what `artifacts/lean_axioms.txt` has always been
  — every one of the 1424 prior reports is a theorem — and keeps one
  `inductive` from adding a dozen generated names to a pinned artifact. What
  it leaves: a *definition* carrying `Classical.choice` that no theorem
  reaches is unreported. Anything a theorem reaches is caught, since
  `collectAxioms` walks the whole graph, so what escapes is dead code.

  The defect was demonstrated live before being closed, not argued about.
  With a `Classical.em` theorem injected into
  `Derivation/IsoCollapseCompat.lean`, the old single-target build reported
  `lean audit clean: 74 sources, 1424 axiom reports, axioms within
  ['Quot.sound', 'propext']`. The same tree with the census enabled reported
  `FAIL: disallowed axioms ['Classical.choice']`, naming the declaration.
  Both states were observed on the same working tree, minutes apart.

  **The census does not read the source.** It reads the compiled environment
  — `Environment.getModuleIdx?` to resolve each module, and
  `ModuleData.constNames` for what that module actually added — so the defect
  that broke two grep counts here, a doc-string line beginning with the word
  `theorem`, cannot move it. Compiler-internal names are skipped via
  `Name.isInternalDetail`, which loses nothing the audit needs:
  `collectAxioms` walks the whole dependency graph, so a theorem reaching
  `Classical.choice` through an internal helper still reports it.

  It is a SECOND `defaultTargets` entry, not an import of the root, and that
  is forced rather than chosen: `DiffAnchorCompat`, `FormTransportCompat`,
  `IsoBridgeCompat`, `IsoCanonCompat`, and `IsoCollapseCompat` each begin with
  `import Derivation`, so the root importing them is a genuine cycle and Lake
  rejects it as one. Being unimportable by the root is what "parked" MEANT for
  those five. Ordering is deterministic because the census transitively
  imports the root and so cannot finish first; the artifact was confirmed to
  regenerate byte-identically across two independent builds.

  That twelve is the RIGHT number is a separate claim, and it is now
  checked too. `ci/check_parked_audit.py` enumerates the modules from the
  source tree, computes the root's transitive import closure, and requires
  the difference to equal the list in `ParkedAudit.lean` — failing in both
  directions. It is Python and not Lean because the blind spot is invisible
  from inside Lean: a module NOTHING imports is absent from the compiled
  environment, so `ParkedAudit`'s own self-check cannot see that it is
  missing. That was confirmed by injection, not assumed — a parked
  `ZzzProbe.lean` left the in-Lean check green and failed the Python one.
- **Line endings are pinned.** `.gitattributes` marks `prompt/**` and
  `artifacts/**` as `-text`. Never let an editor or a CRLF conversion rewrite
  those files — it breaks both the prompt hash gate and byte comparison.
- **The prose watchlist is a census of digests, not a list of words.**
  `ci/prose_watchlist.json` stores SHA-256 digests of the watched terms,
  because the refused-grid clause above records outside names by describing
  and never by naming, and a plaintext list would be the smuggle it watches
  for. `ci/check_prose_watchlist.py` pins every whole-word hit per tracked
  file and fails in both directions. Regenerating the pin is a deliberate
  act; doing it under a live injection adopts the defect as the baseline,
  exactly as with `elaborated_modules.txt`. Its reach is PROSE: identifiers
  containing `_` or digits are never split, so an outside word inside a
  `snake_case` name is the identifier firewall's business. What it cannot
  see: an outside SHAPE carried by native words — a fixture that is an
  outside model in everything but name passes it, and only a reader catches
  that. The term list is the author's to extend or prune; `--probe` answers
  whether a word is on it, and the two read-only seed inputs, the
  `contact/analysis/` quarantine, and the list file itself are out of scope
  by declaration.

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
| Axiom-report pin, new theorem | dropped `collapsed_rename` from `artifacts/lean_axioms.txt` | `FAIL: axiom reports differ between CI build and artifact`, naming the missing report |
| Lean census pin, new module | removed `Derivation.CountTransport` from `elaborated_modules.txt` | census diff named the module and the check exited non-zero |
| Ledger evidence gate | renamed a cited test to `test_supply_is_not_admission_zzz_probe` | `FAIL: ... CL-0-INERTIA [python] ... matches no test, code def, artifact key, artifact text, or source literal` |
| Ledger evidence gate, real case | first real run, no injection | three dead references found and named: two stale tree-export filenames, one renamed theorem surviving only in a rename note |
| Axiom-report parser, primed names | (found live, not injected) four primed theorems absent from `lean_axioms.txt` while the match gate stayed green — both parsers shared the blind `'[^']+'` pattern | audit line count 1417 vs artifact 1413 exposed it; non-greedy capture fixed both, counts agree |
| Parked-audit completeness, unnamed module | added `Derivation/ZzzProbe.lean`, imported by nothing | `FAIL: Derivation.ZzzProbe is outside Derivation.lean's import closure but is not named in lean4/ParkedAudit.lean`; exit 0 after deletion. The in-Lean self-check stayed GREEN throughout — a module nothing imports is absent from the environment, which is why this gate is Python |
| Parked-audit completeness, other direction | added `import Derivation.Composing` to the root | `FAIL: Derivation.Composing is named in lean4/ParkedAudit.lean but IS inside Derivation.lean's import closure`; exit 0 after reversal |
| Research pin drift (gate 11) | restored the stale `PrimitivePassage.lean` hash in `SOURCE_MANIFEST.json` | `FAIL: hash mismatch for lean4/Derivation/PrimitivePassage.lean`, exit 1, naming the module; exit 0 after reversal. The exit status was checked directly, NOT through a pipeline — `$?` after `\| tail` reports tail's status and showed 0 while the script was returning 1 |
| Parked-module axiom census | `Classical.em` theorem added to the parked `Derivation/IsoCollapseCompat.lean` | `FAIL: disallowed axioms ['Classical.choice']`, naming `zzz_probe_choice`; plus the counterfactual on the same tree — reverting `defaultTargets` to `["Derivation"]` made the identical injection report `lean audit clean`, which is the residual itself, observed rather than argued |
| Research pin drift, real case | (found live, not injected) merging #76 and #77 | five research tests failed on `main` at `a1738fa` while the CI rollup reported SUCCESS; no job read the tree, and the two changes only interact once both are present |
| Partial-Decide source pin | changed the first byte of the pinned `model.py` digest | `FAIL: hash mismatch for code/derivation/model.py`, printing wanted, snapshot, and HEAD hashes; exit 1, then 0 after reversal |
| Partial-Decide import authority | added `from derivation.represented import cert_neg` to the production consumer | `FAIL: authorized import mismatch`, naming the extra module and symbol; exit 1, then 0 after reversal |
| Partial-Decide receipt bytes | changed `authority_effect` in the committed receipt | `FAIL: partial_decide_c3.json differs from the deterministic renderer`; exit 1, then 0 after reversal |
| Partial-Decide grade separation | changed the live-tie return to bounded `None` | `test_c3_mu1_retains_all_tied_classes` failed for both L and F and receipt equality failed; exit 1, then 0 after reversal |
| Partial-Decide measure totality | removed `mu2` from one reading at `43b57b9311ba4cacfde58904732b6bd0c1a211e8` | `FAIL: reading L grades keys differ: missing ['mu2'], extra []`; exit 1, then 0 after reversal |
| Partial-Decide dynamic-import refusal | called `builtins.__import__` at `61c172657bcde93d9fc4f9773785807a8ea4f560` | `FAIL: ... uses prohibited dynamic execution/import attribute __import__`; exit 1, then 0 after reversal |
| Partial-Decide source closure | omitted `derivation.observe` at `e24548b0ee503ba249ebae19628ccfd477cef8b6` | `FAIL: derivation.candidates has unpinned derivation dependencies: derivation.observe`; exit 1, then 0 after reversal |
| Partial-Decide conjecture freeze | removed inherited `G4_REMAINS_CONJECTURE` at `ae5d1f651dee47e34a0138df1caf2590e20551b8` | `FAIL: status input required_terminals differ from G3/G4 freeze`; exit 1, then 0 after reversal |
| Partial-Decide module mapping | mapped `derivation.model` to `observe.py` at `3f5fdd16cafbf82304b512e7196c289d16b8d4d6` | `FAIL: module/path mismatch for derivation.model`; exit 1, then 0 after reversal |
| Partial-Decide shadow refusal | registered local `derivation.py` at `12b9f3de4287456a20a2b7b26e34871cb795c18b` | `FAIL: reserved derivation shadow path: research/partial_decide/derivation.py`; exit 1, then 0 after reversal |
| Partial-Decide package-tree pin | replaced the pinned tree with zeroes at `6b30c490aebcc52f80f548a34f3458f65b0b947e` | `FAIL: source package tree mismatch`, naming wanted, snapshot, and HEAD trees; exit 1, then 0 after reversal |
| Partial-Decide refusal-policy pin | replaced the refusal with a totalizing policy at `1f5ee586fd7890fdb8d9cae9b9141886dba761e6` | `FAIL: source policy differs from the exact refusal declaration`; exit 1, then 0 after reversal |
| Partial-Decide exact snapshot | replaced the commit id with `HEAD` at `15c8ab7d57d80bbefdd129f82013881131349d47` | `FAIL: source snapshot commit must be an exact 40-digit lowercase hex id`; exit 1, then 0 after reversal |
| Partial-Decide early custody | dirtied tracked `c3_receipt.py` before preflight | `FAIL: partial-Decide executable package or transport policy has worktree changes before custody preflight`, naming the file; exit 1, then 0 after reversal |
| Partial-Decide package census, first diagnostic | committed an unlisted consumer at `758ec430baaa946177a5948676f4049a4d86333f` | `FAIL: tracked package census differs across declaration, HEAD, and index`; exit 1, then 0 after reversal. It detected divergence but did not name the injected file, so this first probe did not meet the diagnostic standard |
| Partial-Decide package census, repaired diagnostic | repeated the unlisted consumer at `431d172bee890ae37fa7e5fabcadefa5e19f0fda` | `FAIL: ... research/partial_decide/zzz_consumer_probe.py [declaration=no, HEAD=yes, index=yes]`; exit 1, then 0 after reversal |
| Partial-Decide mypy census | added an uncommitted type-invalid consumer | mypy named the incompatible assignment and checked six source files; exit 1, then five clean files and exit 0 after reversal |
| Partial-Decide transport attribute | changed `-text` to `text` at `80ddae268710c4d0a5be671ad254cfa7b4fa6944` | `FAIL: receipt transport attribute must be committed as -text`; exit 1, then 0 after reversal |
| Partial-Decide CRLF refusal | committed CRLF receipt bytes at `5e1eb4b2ac42e06f565272b55130bbe9dd9819b9` | `FAIL: partial_decide_c3.json contains CR bytes`; exit 1, then 0 after reversal |
| Partial-Decide class-key binding | exchanged members between two L/mu1 classes while preserving counts and the exact partition | `test_literal_receipt_contract_binds_members_to_canonical_classes` now reports `canonical key differs`; the pre-repair verifier at `4869cb2` accepted the same mutation |
| Partial-Decide duplicate JSON names | duplicated root `policy` and nested `authority_effect` names with authorization-bearing last values | `test_json_decoder_rejects_root_and_nested_duplicate_keys` reports `duplicate JSON key`; the pre-repair decoder accepted both through last-wins semantics |
| Partial-Decide status namespace | added `statuses.g4_result = G4_HOLDS_UNDER_MU2` | the status mutation test reports `G1 class statuses keys differ`; the pre-repair verifier at `4869cb2` accepted it |
| Ledger conformance, tab heading | `###\tCL-ZZZ-SMUGGLED` appended to the ledger text | `test_injection_tab_heading_is_not_invisible`: the ATX population sees it, the classifier names it, `KNOWN_CLAIM_IDS` fails. A space-only `### ` scan would have dropped it from both sides |
| Ledger conformance, empty fields | `**Statement**: .` (and the other seven keys) | `test_injection_empty_fields_are_missing_not_present`: each required field is missing; a presence-only check stayed green |
| Ledger conformance, rewritten body | CL-0-INERTIA statement replaced with a lie that keeps every key | `test_injection_rewritten_inertia_body_breaks_the_pin`: body pin digest moves; ID ratchets would have stayed green |
| Ledger conformance, match-arm index | synthetic `| exact =>` / comment words `that worth of carrying` | `test_match_arm_and_comment_words_are_not_declarations`: those strings are absent from the declaration index; constructors `| name (` still index |
| Ledger conformance, root wildcard | token `Derivation.*` | `test_root_namespace_wildcard_does_not_resolve`: returns false. `PresentationRelativity.*` still resolves |
| Prose watchlist, new hit | appended one line carrying a watched noun to `research/notes/README.md` | `FAIL: NEW HIT: research/notes/README.md: watched term 1d1d155e7584 appears 1 times, pinned 0 -- line 15 '…'`, exit 1; `prose watchlist clean: 49 watched terms, 153 files with pinned hits, 1886 hits` and exit 0 after `git checkout` of the file |
| Prose watchlist, stale pin | deleted the one line of `research/notes/peirce_semiotics_note.md` carrying a pinned noun | `FAIL: STALE PIN: research/notes/peirce_semiotics_note.md: watched term d4e3fc7b0477 appears 0 times, pinned 1; if the removal is intended, regenerate with --regen`, exit 1; exit 0 after reversal |
| Prose watchlist, real case | (found live, not injected) the gate's own test file used an outside proper name as a tokenization sample | `FAIL: NEW HIT: tests/test_prose_watchlist.py: watched term 5cc10d9143b2 appears 2 times, pinned 0 -- line 48 '…'; line 49 '…'` on the first run over the staged tree; the sample was reworded, the pin was NOT regenerated |
| Prose watchlist, stemmer over-reach | (found live, not injected) the phrase "prose hopes" in `research/convention_price/PROMPT.md` was pinned as a hit on a watched three-letter noun: the `es` strip reached it through a vowel | the strip was narrowed to the English rule (after s, x, z, ch, sh), `test_es_strip_does_not_reach_a_three_letter_stem_through_a_vowel` fixes it, the gate then reported `STALE PIN: research/convention_price/PROMPT.md: … appears 2 times, pinned 3`, and the pin dropped by exactly that one hit on the next deliberate `--regen` |

The Partial-Decide injection commit IDs above are local throwaway objects with
no branch or tag reachability; they may be pruned and are locators rather than
durable evidence. `research/partial_decide/STATUS.md` records the exact
mutation, command, diagnostic, exit, and recovery needed to replay the repaired
package-census probe without relying on its commit object.

What injection does NOT prove: that the population is the right
mathematical object. A perfect pin of the wrong set is still the wrong set.
An earlier version added that it "cannot close the parked-module axiom
residual above — it can only demonstrate that the residual is still live".
That is WITHDRAWN as to the parked-module residual, which is closed, and
injection is exactly how the closure was shown to bite. The general point
survives and still applies to the research-tree axiom receipt above:
injection demonstrates that a residual is live; it does not close one.

### Claim hygiene

`paper/paper_change_log.md` records material changes newest-last, including
withdrawn and repaired claims; `paper/pr11_correction_ledger.md` is a worked
example of narrowing an overclaim. When a proof turns out to cover less than
the prose asserted, the established move in this repository is to weaken the
statement in the ledger and the paper — never to keep the wording and lean on
the receipt.
