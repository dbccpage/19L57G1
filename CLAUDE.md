# CLAUDE.md

This file holds the repository's current rules. Two other files carry what
used to live here:

- `docs/claude_md_history.md`: the dated history. That means withdrawn
  statements and why they were withdrawn, incident narratives, superseded
  counts, and the completed execution plan. It is the full text of this file
  as it stood on 2026-09-21, before the split, kept byte for byte. Nothing
  in it binds.
- `docs/injection_record.md`: the standing record of gate injections.

## Repository boundary

**The blind protocol is scoped to the sealed derivation, not to the whole
repository.** It governs exactly `prompt/`, `paper/`, `code/`,
`lean4/Derivation/` and `artifacts/`. By the author's ruling of 2026-09-18 it
also governs the root file `lean4/Derivation.lean`. The derivation's entire
value is that it was carried out blind. Retiring the boundary retroactively
would destroy the only thing that makes it evidence, so the boundary is
sealed, not amended.

**Stopping-condition status.** The mechanical clauses were re-run on
2026-08-17, and all gate families then defined passed at `052e657`. The
captured output is in `verification_20260817.md`, at the repository root:
`paper/paper.md` cites it at that path. The clauses that require judgement
are not discharged by any gate and remain operator claims:

- every notion carries a source classification;
- every theorem-level claim has Lean evidence or is downgraded;
- tied minima are retained unless eliminated by proof;
- the paper states the strongest defensible terminal result.

**Scoping.** `lean4/` is carved down to `lean4/Derivation/` plus the root
file above. `code/`, `paper/` and `artifacts/` are named whole. So a future
`code/coda/` would fall inside the sealed contract, and inside mypy, coverage
and artifact regeneration. Carve those the same way before putting CODA code
under them.

**No `paper/coda/` carve is in force. Do not write that tree, and do not
invent an exception to this paragraph.** `paper/` is named whole above, so
any subpath of it is inside the seal until an amendment here says otherwise.
Amending this contract is the author's act, not an agent's. The rule was
breached once: pull request #55 landed 30 files under `paper/coda/`, and
they were removed in `6c3d880`.

**External citation is not permitted anywhere in this repository.** `coda/`
and `coda_meta/` moved to the private `dbccpage/CODA` on 2026-08-17, and the
exception they carried left with them.

Within the sealed derivation:

- All work uses only this repository: no network research, no external files,
  no prior project instructions, no plugins, agents, skills or memories, and
  no user guidance during the derivation.
- `prompt/prompt.md` and `prompt/seed_prompt.md` are read-only inputs and must
  remain byte-identical. Their SHA-256 hashes are recorded in the paper.
- Toolchains already installed on this machine are metatheoretic apparatus,
  not inputs: Python 3.14, pytest, coverage, mypy, and Lean 4.33 / Lake 5.0
  via elan.

## Execution plan (completed; historical)

The five-step plan has been carried out:

1. toolchain check;
2. the seed prompt's Challenges 0–3 and its autonomous continuation;
3. the finite reference model in `code/`;
4. the Lean formalization;
5. the paper.

Its full text is in `docs/claude_md_history.md`. The discipline, gates and
stopping conditions below still govern any change inside the seal.

## Assumption discipline

- Every substantive notion is classified as exactly one of: metatheory
  apparatus; supplied object-language datum; externally imposed challenge;
  admitted primitive; derived definition; proved theorem; deterministic
  computation; countermodel; optional realization; conjecture; open
  obstruction; refuted claim.
- The words "forced", "minimal", "free", "canonical", "equivalent",
  "universal" and "complete" are used only with a proof or a precise
  conditional scope.
- Presentation identity, internal identity, observational equivalence,
  behavioral separation and semantic interpretation are kept distinct.
- Supply, mention, admission, current-state designation, retention,
  observation and equality are never conflated.
- Absence of a test is never converted into equality. A model proposal never
  mutates admitted state without a separately defined admission event.
- Receipts (hashes, test passes, parser success) are never treated as proof of
  an unverified mathematical payload.
- **Vocabulary ruling (author, 2026-09-23).** No external theory,
  architecture, or project terminology may be introduced as an input to the
  sealed derivation. The read-only seed prompt remains an immutable supplied
  input. Research outside the seal may use explicitly classified supplied
  vocabulary; such vocabulary supplies neither a native derivation nor a
  proved bridge. The six already fenced post-hoc comparison sections
  identified in paper section 13 are preserved as historical records in
  their existing positions. They are not derivational inputs, theorem
  evidence, or authorization to extend comparison inside the seal. External
  citations remain prohibited throughout the repository. The identifier
  firewall and prose watchlist retain their current populations; changing
  either population requires a separate deliberate author decision. The
  vocabulary firewall in `tests/test_primitive_contact.py` walks the whole
  tree via `git ls-files` and bars the 102 working-denylist identifiers
  outside `contact/analysis/`. This ruling supersedes the repository-wide
  vocabulary prohibition; `docs/claude_md_history.md` records the change.
- **Refused grid, recorded (author, 2026-08-31).**
  - *What was offered:* an outside classification grid, nine single-letter
    slot names and an accompanying phrase, offered through the operator
    channel for the primitive-difference inventory.
  - *Why it was refused:* the author refused it as vocabulary. Each letter
    on its own is generic mathematics, so no denylist fired. But the pattern
    of names was an outside architecture's grid, and structural smuggling is
    still smuggling.
  - *How it is recorded:* the inventory's names are repository-native. The
    offered names are reproduced nowhere in this repository, this clause
    included. Describing without naming is the only way to record a refusal
    without committing the smuggle it refuses.
  - *What follows:* any future claim of independent convergence between
    this repository's inventory and any external architecture's slot grid is
    false by construction, and must cite this clause.
  - *How it is held in place:* a digest test pins the paper's own refusal
    note, so it cannot drift out.

## Proof gates

- Every theorem-level claim used by the paper has a Lean 4 proof, or is
  explicitly downgraded to computation, conjecture, countermodel or OPEN.
- `lake build` passes with no `sorry`, `admit`, user-declared `axiom`,
  `unsafe` or `partial`.
- Every exported theorem cited by the paper has a `#print axioms` report, and
  any library axiom reliance is recorded in the claim ledger.
- Failed theorem targets remain counterexamples or OPEN, never prose proofs.
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
- Equality, minimality, isomorphism, survivor counts and proof status are
  decided only by implemented algorithms, never by judgment calls outside the
  code.

## Stopping conditions

A branch stops in either of two cases:

- no next challenge or no justified response exists;
- the declared resource bound is reached: fifteen accepted augmentation
  rounds per finite branch, with the deterministic node, arity and cost
  bounds stated in the paper.

Either way, the exact frontier is exported, together with a proof of what is
complete within the bound.

The task stops only when all of the following hold:

- every introduced notion has a source classification;
- every state change has a replayable admission history;
- every theorem-level claim has Lean evidence or is downgraded;
- every computational claim has deterministic Python evidence;
- all tied minimum branches are retained unless eliminated by proof;
- both coverage thresholds are met;
- Lean builds without forbidden escapes;
- the working tree is clean, with all intentional artifacts committed;
- `prompt/prompt.md` is byte-identical to the initial file;
- the paper states the strongest defensible terminal result, including
  termination or failure, without targeting a predetermined conclusion.

---

# Operating manual

Everything below is metatheoretic apparatus: how to drive the toolchain, and
where things live. The verification contract is written in
`.github/workflows/verify.yml` and `ci/`, and it runs locally.

## No hosted CI — settled, do not reopen

**This repository does not use hosted GitHub Actions CI, and never will.**
This is a permanent decision by the author (2026-09-08), not a lapse, an
outage, or a billing problem to be fixed.

`.github/workflows/verify.yml` is kept as the written contract: the canonical
list of the gate families and the order they run in. It does **not** execute.
No push, pull request or merge triggers a hosted run, and none is expected
to. "Green" means every gate was run locally, by the author or by an agent
at the author's direction. That pass is a local receipt. A receipt in a PR
body, a README or a change-log entry is a local run unless it explicitly
says otherwise.

- Do **not** propose enabling, restoring, paying for, re-instating or
  "fixing" hosted CI, and do not open issues or PRs toward that end.
- Do **not** read an absent, dormant, skipped or failed Actions run as a
  defect, a regression, or a thing to investigate.
- A merge rests on local receipts alone. The author merges; the absence of a
  hosted check never blocks or gates that.
- Wherever this repository says a gate is "enforced by CI", read "the gate
  that `verify.yml` defines, run locally". A local run sees the branch head,
  not a merge result. Two branches that are each green can still break
  `main` once both land, so re-run after merging a pair that interacts.

`AGENTS.md` states the same policy in short form.

## Pull-request topology

Every pull request must target `main` directly. Stacked pull requests are
prohibited: do not open a pull request whose base is another unmerged topic
branch. If work depends on an open pull request, do one of two things:

- merge that dependency first, then rebase onto the new `main`; or
- combine the work into one pull request.

This keeps review, provenance pins and merge authority bound to one head and
one base at a time.

## Running the gates

Run from the repository root. Shell examples are PowerShell, since the
primary platform is Windows.

`python ci/run_gates.py` runs the jobs of `.github/workflows/verify.yml`
locally, in the workflow's order, and prints a pass/fail table. This is the
documented way to run the gates.

```powershell
python ci/run_gates.py                      # every job: python, lean, research
python ci/run_gates.py --job python         # one job (repeatable)
python ci/run_gates.py --fast               # only single-command python-job checks
python ci/run_gates.py --step "stake"       # only steps whose name matches a regex
python ci/run_gates.py --list               # show the selected steps, run nothing
python ci/run_gates.py --keep-going --workers 8 --receipt run.json
```

What the runner guarantees:

- It refuses any workflow construct it does not implement.
- Before a run, it deletes stale outputs: `coverage.json`, `lake_build.log`
  and `artifacts_ci/`.
- It fails any step that rewrites a tracked file under `artifacts/`.
- Two runs cannot overlap on one machine; a lock prevents it.

### Tests

```powershell
python -m pytest                      # pinned-lock suite
python -m pytest tests/test_iso.py    # one file
python -m pytest tests/test_iso.py::test_tokens_are_forgotten   # one test
python -m pytest -k equivariance      # by keyword
```

`pyproject.toml` puts `code/` on `pythonpath` for pytest only. Anything run
outside pytest, such as the `run_*.py` entry points, needs
`$env:PYTHONPATH = "code"`.

On a machine with at least eight logical CPUs, run the exhaustive local
suite with eight fixed pytest workers. The two parallel test plugins stay
ephemeral: `requirements.txt` is hash-bound by the G1 receipt, and adding
them there would be a separate repin act.

```powershell
$parallelUvCache = Join-Path $env:TEMP "19L57G1-parallel-pytest"
$env:UV_CACHE_DIR = $parallelUvCache
uv run --isolated --with-requirements requirements.txt `
  --with pytest-xdist==3.8.0 --with pytest-cov==7.1.0 `
  python -m pytest -n 8 --dist load --cov=code --cov-branch `
  --cov-report=json:coverage.json --cov-report=term
python ci/check_coverage.py
```

### The twelve gate families

The numbers are a stable census for reporting. The workflow's step order is
what actually runs.

1. **Prompt byte-identity:** `python ci/check_prompt_hashes.py`.
2. **Transport-document citations bound to Lean sources:**
   `python ci/check_transport_citations.py`. It enumerates its citation
   population independently of the parser that classifies it, so a citation
   the classifier cannot see fails the totality check instead of cancelling
   out on both sides of it.
3. **Tests under coverage, then the independent 95% line and branch gate:**
   `python -m coverage run -m pytest -q; python -m coverage json -q; python ci/check_coverage.py`.
   Use `python -m coverage`, never bare `coverage`. `coverage.json` is
   untracked, and the gate fails by name in three cases:
   - the report is missing;
   - its file set differs from `code/**/*.py`;
   - any measured source was modified after the report's `meta.timestamp`.
4. **Strict typing:** `python -m mypy`. The config is in `pyproject.toml`.
5. **Artifact regeneration must be byte-identical.** See Artifacts.
6. **Lean.** The build, the forbidden-token and axiom audit, the axiom
   artifact regenerating byte-identically, the declaration-level axiom
   census, and every module elaborating. See Lean.
7. **Skills are well formed and declare no authority:**
   `python ci/check_skills.py`.
8. **Every `paper/*.md` path cited inside `paper/` resolves:**
   `python ci/check_paper_citations.py`.
9. **Every evidence citation in the claim ledger resolves:**
   `python ci/check_ledger_evidence.py`. The population is enumerated
   independently of the classifier. The gate checks that names **resolve**,
   never that wording matches proof.
10. **Parked-module audit:** `python ci/check_parked_audit.py`. Every module
    under `lean4/Derivation/` that lies outside `Derivation.lean`'s import
    closure must be named in `lean4/ParkedAudit.lean`, which emits their
    axiom reports. Two facts about scope:
    - A top-level `lean4/*.lean` file is outside this census, and
      `ParkedAudit.lean` is itself such a file.
    - The check is Python rather than Lean because a module that nothing
      imports is absent from the compiled environment, so Lean cannot see
      that it is missing.
11. **Registered research trees:** their pins, tests, strict typing and
    receipts. This is not a sealed-derivation gate.
    - *Which trees:* the registered set is the workflow's `research` job,
      plus the research Lean audits in its `lean` job: `second_nofirst`,
      `second_index` (author, 2026-09-24), `typed_translation`,
      (author, 2026-09-23) the four foundations trees `native_bridge`,
      `native_structure`, `conservation_ladder` and `domain_adapters`,
      whose receipt checks run in the `research` job, and (author,
      2026-09-24) seven older trees whose Lean was a manual receipt:
      `natural_sections`, `balance_carrier`, `closed_family`,
      `convention_price`, `coherent_process_limits`, `boundary_seed` and
      `endogenous_continuum`. Also by the author's ruling of 2026-09-24,
      the `research` job holds the test counts of `p208a_path_interference`,
      `p208b_contextuality_nonlocality`, `p208c_commutator_tomography` and
      `p209c_stabilizer_codes` to a minimum, and the `lean` job regenerates
      their receipts, which carry each tree's Lean axiom census.
      `research/README.md` marks each tree's `research`-job registration
      only, so a tree whose Lean alone is gated still shows there as a
      local receipt. `python ci/run_gates.py --job research` runs the
      `research` job, and `--job lean` the Lean audits.
    - *What it does not cover:* every other tree's `verify_lean.py` stays a
      manual receipt, unchecked by any gate. So does every check of a tree
      outside the registered set. Such a check can be red on `main` while
      every gate is green.
    - *Expected reds:* the primitive-difference step is expected to go red
      on a legitimate change to a path it protects. That is the signal to
      repin, not a defect. Repair it with `verify_manifest.py --repin`, then
      revise the prose it names. Review a repin by diffing the parsed JSON,
      not the text. Other registered trees have their own pin policies, and
      partial Decide deliberately provides no automatic repin.
    - *The estate census:* the job ends with
      `python ci/check_tree_custody.py`, which runs every research tree's own
      custody verifier, including the unregistered ones, and compares the
      outcome set with `ci/tree_custody_pin.json`. It fails on a new red and
      on a stale pin, both named, and judges no verifier's logic. Run it on a
      clean worktree; rewrite the pin with `--write`, deliberately.
    - *Second-derivation rungs:* the seed at `research/second/SEED.md`
      limits a rung's writes to `research/second/` and its own
      `research/second_<rung>/`, and its section 10 adds registration in
      the workflow's research job. By the author's ruling of 2026-09-23,
      that registration also covers the generated views of a new tree.
      After committing its tree and its registration in
      `.github/workflows/verify.yml`, a rung runs
      `python ci/research_index.py --write`,
      `python ci/lookup_indexes.py --write`,
      `python ci/lean_build_order.py --write` and
      `python ci/check_tree_custody.py --write`, and commits their output.
      The custody pin may gain the rung's verifier, never an entry under
      `expected_failures`: a rung whose verifier fails is not registered
      until it passes. By the author's ruling of 2026-09-25, the rung
      also adds its own registered gate scripts to
      `.claude/skills/gates/SKILL.md`, which
      `tests/test_gates_skill_matches_workflow.py` requires to name every
      workflow gate script. Apart from the workflow registration and
      those skill lines, the rung hand-edits nothing outside its write
      root, and it regenerates nothing while an injection is live.
    - *"Named first" in the next-rung rule:* by the author's ruling of
      2026-09-25, when the seed's rule breaks a tie by the leftover
      "named first", that means first in the list of leftovers as the
      applying rung writes it. It never means earliest in time: these
      systems have no time.
    - *Second-derivation continuation (author, 2026-09-25):* the ruling
      below is recorded verbatim. `research/second/SEED.md` is unchanged;
      this is a protocol intervention by the author, disclosed in
      `research/second/MANUAL.md` and, at closeout, in the run's paper and
      ledger.

      ```text
      AUTHOR RULING — SECOND DERIVATION CONTINUATION

      1. Census eligibility
      Resolving an unresolved FORCED classification counts as extending
      the Challenge 5 census. A proved negative decision counts as well
      as a proved positive decision. Merely recording OPEN does not
      constitute an evidential resolution.

      A named prerequisite necessary to attempt an eligible census
      question is eligible. Its costs and dependencies must be stated.
      X-5 is eligible on this basis.

      2. Original budget
      The twelve-rung limit is counted by distinct research attempts,
      not by ordinal labels. The two separately scoped rung-two tracks
      count separately. The twelve recorded attempts exhaust the
      original budget. Historical labels and receipts are unchanged.

      3. Authorized continuation
      Authorize at most two additional research attempts in an explicitly
      identified continuation: first Challenge 3, then Challenge 4 with
      its engine-dependent census evaluations.

      The first attempt closes before the second opens. Each retains
      its declared bounds and may terminate OPEN. No additional attempt
      is authorized automatically. No scientific outcome is prescribed.

      The original SEED.md remains byte-identical. The continuation and
      this intervention are disclosed in the manual, paper, and ledger.

      4. Closeout responsibility
      A designated closeout session creates and reconciles:
      research/second/paper.md
      research/second/change_log.md
      research/second/claim_ledger.md

      Reporting and replay do not consume a research attempt. New
      substantive research is not permitted under the label of closeout.
      The author approves the final snapshot.

      5. Completion and freeze
      The paper distinguishes original-phase results, continuation
      results, protocol deviations, and unresolved obstructions.

      Budget exhaustion is not reported as completion-gate satisfaction.
      Every completion condition receives its own evidence or explicit
      unmet status, including the input-count floor.

      The final report and supporting files are frozen before comparison.
      The comparison is written only in the companion repository.
      ```
12. **Prose watchlist:** `python ci/check_prose_watchlist.py`. The census
    matches its pin. See Invariants.

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
python ci/check_declaration_axioms.py                  # every compiled Derivation constant
```

`lake_build_*.log` is gitignored.

- **The axiom report comes from both default targets:**
  `lean4/Derivation.lean`, with its hand-maintained `#print axioms`
  inventory, and `lean4/ParkedAudit.lean`, for the parked modules the root
  does not import. If the log comes back with no `#print axioms` lines,
  force those roots to rebuild before auditing.
- **When a theorem is renamed, added or removed:** rewrite
  `artifacts/lean_axioms.txt` with `python ci/regen_axiom_artifact.py <log>`.
  It writes bytes explicitly, so a shell redirect cannot reintroduce CRLF.
  Then regenerate the artifacts derived from it, the completion receipts and
  the dependency graph. The order matters: derived artifacts come after the
  axiom artifact, never before. No Python source hard-codes Lean theorem
  names.

**The axiom boundary, stated exactly.** Two checks cover it.

- **`ci/check_lean_audit.py`** certifies that every `#print axioms` report in
  the build log lies within `{propext, Quot.sound}`. Its population is the
  union of two sets:
  - the root's hand-maintained inventory, which by itself does not establish
    that it names every declaration in the root's closure;
  - every **theorem** of the parked modules, enumerated from the compiled
    environment. The enumeration filters on `ConstantInfo.isTheorem`, so
    definitions, structures and generated constructors are not reported
    there.
- **`ci/check_declaration_axioms.py`**, registered in the `lean` job since
  2026-09-19, closes the rest for `Derivation` modules. It reads the
  compiled environment, and it fails naming any constant of any kind whose
  axioms leave `{propext, Quot.sound}`. "Any kind" means theorems,
  definitions, instances, and generated or internal constants alike.

`lean4/ParkedAudit.lean` is outside that census by module. It is top-level
apparatus, not a `Derivation` module, and its own definitions are printed
as an informational witness line, not as a failure.

"Axiom-clean" therefore means every constant of every `Derivation` module,
plus every report the audit reads. The rule "Lean may only use `propext`
and `Quot.sound`" is enforced over exactly that population. `Classical.choice`
is out, so decidability has to be constructive.

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

Not every stem has all five members; `docs/index/topics.md` is the generated
map. Prose lives in `paper/`, but not one file per topic: `paper/paper.md`
is the spine, and the other `paper/*.md` files are per-investigation
write-ups.

Every claim carries a stable `CL-*` ID in `paper/paper_claim_ledger.md`,
which names its Python evidence (artifact key and/or test name) and its Lean
theorem names. `artifacts/claims.json` holds the computed values for the
ledger IDs, so ledger prose and machine output are cross-checkable.

### The kernel, read in this order

The first six modules are the whole object language. The other modules in
`code/derivation/` are studies layered on top of them. This is the
*computational* object language only, the Python side. It is not a reading
order for `lean4/`, whose contact and passage modules are entered through
`paper/paper_claim_ledger.md`.

1. `model.py`: `Regime` (frozen: `data`, `forms`, `insts`, `rules`, `reqs`)
   plus the event types. State changes *only* through admission events
   (`AdmitDatum/Form/Inst/RuleAll`) or `Impose`. `Supply` is an external
   presentation event that provably does not change state. `replay` rebuilds
   a regime from an event list, which is what makes every result replayable
   from genesis.
2. `observe.py`: contexts (a form plus a slot tuple with holes), profiles
   (which pluggings are derivable), and the declared sense of *internally
   separable*: two data are separable exactly when their profiles differ.
3. `candidates.py`: the declared candidate space of one-step augmentations
   (deltas) and the two declared cost measures `mu1`/`mu2`, plus
   `min_responses`. The cost-2 enumeration is pruned by four named lemmas,
   each with an unpruned cross-check test.
4. `iso.py`: the implemented isomorphism relation and `canonical` keys.
   Presentation tokens are deliberately forgotten. This is the *only*
   sanctioned way to quotient branches, and it is cross-checked against a
   brute-force minimum over all bijection pairs.
5. `engine.py`: Challenges 0–3 and the branch tree. It carries two admission
   *readings* (L and F) as separate genesis histories. It also separates the
   declared pair-separation closure policy from the external supply policy;
   `supply=False` runs are the closed-system baseline.
6. `export.py`: deterministic JSON, normalized DAG tree exports, and
   `verify_full_export`, which replays every node and checks its regime hash.

### Invariants that break a gate if you miss them

- **Byte-determinism.** Exports carry no timestamps and no environment data,
  keys are sorted, and `.json.gz` uses a fixed mtime and compression level.
  Any change to a derivation module means regenerating and committing the
  affected artifacts, or gate 5 fails.
- **The runner census is a glob, and `artifacts/` is its own pin.** The
  workflow enumerates `code/run_*.py` at the top level of `code/`, so a new
  runner is regeneration-checked without anyone registering it. A runner
  placed in a subdirectory of `code/` is outside the census.
  `ci/compare_artifacts.py` catches drift in both directions:
  - a committed artifact with no regeneration fails;
  - a regenerated artifact that was never committed fails.
- **Skills hold no authority, and the declaration is enforced.** Skills
  live in `.claude/skills/<name>/SKILL.md` and are tracked. Each must carry
  the literal line `AuthorityEffect: None`. `ci/check_skills.py` checks
  that, plus the frontmatter shape and that the declared `name` matches its
  directory. A pass means "well formed and claiming no authority", never
  "the skills are right".
- **A cited paper path must resolve.** Gate 8 requires every
  `paper/<name>.md` token inside `paper/` to name an existing file. It
  cannot tell a live citation from a prose mention of a deliberately dead
  path. So prose must not write a `paper/<name>.md` path it does not want a
  reader to follow; name such documents descriptively instead.
- **The forbidden-token scan is plain text over whole `.lean` files.** It
  matches `sorry`, `admit`, `unsafe`, `partial`, and a leading `axiom`
  anywhere, including inside comments and doc strings. Phrase Lean prose
  around those words, and mind line **wrapping**. The pattern is
  `^\s*axiom\s`, so a prose line that happens to wrap onto the word `axiom`
  fails the gate even though the sentence is innocuous. A docstring line
  wrapping onto `theorem` has also defeated a grep-based theorem count.
- **Each exported theorem the paper cites needs a `#print axioms` line** in
  `lean4/Derivation.lean`. `artifacts/lean_axioms.txt` must match the fresh
  build log.
- **Every module elaborates, whether or not the root imports it.**
  `lake build` builds only `defaultTargets`, so a module the root does not
  import would otherwise never be typechecked. The forbidden-token scan
  reads text; it does not elaborate. So the `lean` job's last step,
  `python ../ci/gate_support.py lean-census` run from `lean4/`, builds every
  `lean4/Derivation/**/*.lean` module in one `lake build` call.
  - The census is recursive, so a subdirectory module cannot escape it.
  - The two top-level roots, `Derivation.lean` and `ParkedAudit.lean`, are
    covered by being default targets, not by the census.
- **The census is pinned, not merely computed.** It is diffed against
  `artifacts/elaborated_modules.txt`, so adding or removing a module fails
  the `lean` job until that artifact is regenerated. An empty-census guard
  catches an enumeration that finds *nothing*; only the diff catches one
  that finds *some*. Regenerate it from the repository root:

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

- **Parked modules are audited.** `lean4/ParkedAudit.lean` emits one axiom
  report per theorem for every module outside the root's import closure.
  It is a second `defaultTargets` entry, not an import of the root. That
  much is forced: several parked modules begin with `import Derivation`, so
  the root importing them would be a cycle. Gate 10 checks from the source
  tree that the parked list is complete, failing in both directions.
- **A research tree's pins certify its snapshot, not the present.** A
  custody verifier fails when a pinned source differs at the snapshot the
  tree was derived against. Whether that source has MOVED since is reported
  as `DRIFT:` lines with a count, and does not fail; `--require-current`
  restores the strict behaviour.
  - *Why:* the snapshot blob is fixed history. Once the author legitimately
    edits a sealed or contract file, no repin can satisfy both the snapshot
    and HEAD, so a verifier that demands both is permanently red and stops
    carrying information. Eleven trees were red that way, some for months,
    until the author's ruling of 2026-09-22.
  - *The exception:* a file inside the tree's own write root, which nothing
    outside the tree can move. `research/s9_obligations` keeps failing on
    drift of its own governing `PROMPT.md`, because its step 1 says so.
  - *New trees:* the `research/_scaffold` template pins only the tree's own
    input files, so it carries no snapshot-and-HEAD check to inherit. A new
    tree that pins sealed sources follows this rule; the scaffold README
    says so.
- **Line endings are pinned.** `.gitattributes` marks `prompt/**` and
  `artifacts/**` as `-text`. Never let an editor or a CRLF conversion
  rewrite those files; it breaks both the prompt hash gate and byte
  comparison. This machine checks files out with `core.autocrlf=true`, so
  write files as bytes with LF.
- **The prose watchlist is a census of digests, not a list of words.**
  - *What it stores:* `ci/prose_watchlist.json` holds SHA-256 digests of the
    watched terms, because a plaintext list would be the smuggle it watches
    for. `ci/check_prose_watchlist.py` pins every whole-word hit per tracked
    file.
  - *How it fails:* in both directions. A hit above its pin names the file,
    line and token; a hit below it names the stale pin.
  - *Options:* `--probe WORD` says whether a word is watched; `--report`
    lists every hit; `--add TERM --tag TEXT` watches one more term by
    digest; `--regen` rewrites the pin.
  - *Regenerating the pin* is a deliberate act. Never do it under a live
    injection.
  - *Its reach is prose.* Identifiers containing `_` or digits are never
    split, so an outside word inside a `snake_case` name is the business of
    the identifier firewall in `tests/test_primitive_contact.py`.
  - *What it cannot see:* an outside **shape** carried by native words. Only
    a reader catches that.
  - *Who owns the list:* the author extends or prunes it. The two read-only
    seed inputs, the `contact/analysis/` quarantine and the list file itself
    are out of scope by declaration.

### Proving a gate

A gate is not proved by being green. It is proved by failing on the exact
defect it exists to catch, with the failure naming the injected object, and
by recovering when the injection is reversed. Green before and after, with
nothing in between, shows only that the gate is quiet.

- **Keep injections minimal and reversible.** Never regenerate a receipt
  while one is live. Regenerating `elaborated_modules.txt`,
  `lean_axioms.txt` or the watchlist pin under an injection adopts the
  defect as the new baseline and destroys the test.
- **Record every injection.** Put it in the pull request body, and add a row
  to `docs/injection_record.md`.
- **Know what injection does not prove:** that the population is the right
  mathematical object. A perfect pin of the wrong set is still the wrong
  set. Injection demonstrates that a residual is live; it does not close
  one.

### Claim hygiene

`paper/paper_change_log.md` records material changes, newest last,
including withdrawn and repaired claims. `paper/pr11_correction_ledger.md` is
a worked example of narrowing an overclaim. When a proof turns out to cover
less than the prose asserted, the established move in this repository is to
weaken the statement in the ledger and the paper. Never keep the wording and
lean on the receipt.

Outside the paper, the same rule applies to this file and to research trees.
Withdraw a false statement with a dated note, and never silently rewrite a
recorded one. This file's own withdrawn statements are preserved in
`docs/claude_md_history.md`.
