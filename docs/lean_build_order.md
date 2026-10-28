# Lean build order from a fresh clone

AuthorityEffect: None. A build recipe: not a gate, not a receipt, and not
part of the sealed derivation.

A fresh clone has no Lean build products. The sealed package `lean4/` and
the research Lake packages each have to be built once, and the order
matters. Every research package that requires `lean4` through a path
builds the sealed modules it imports into the shared `lean4/.lake/`,
because Lake builds a path dependency in the dependency's own directory.
Some research packages also require other research packages, so building
one of them builds whatever it requires that is not built yet.

## How this page is made

The block between the two generated markers below is written by
`python ci/lean_build_order.py --write`. It reads every tracked
`lakefile.toml` (its `[[require]]` tables with `name` and `path`) and
`lakefile.lean` (its `require <name> from "<path>"` lines) each time it
runs; nothing in the block is typed by hand. `tests/test_lean_build_order.py`
fails when the block differs from what the lakefiles give, so a change to a
require line cannot leave this page behind. After a rebase or merge that
changes a lakefile, rerun `--write` and commit the result. The prose outside
the markers is edited by hand; the block only through the generator.

Two facts no lakefile states are recorded by hand in the generator and
checked against the tree on every run: which directory is the build entry
when one Lake package is declared in two directories
(`DUPLICATE_PACKAGE_DIRS`), and which packages need a tree script
(`SPECIAL`). A lakefile source directory that holds no tracked file fails
the check until a `SPECIAL` entry names the script that stages it. A require
form the generator does not read, a path that holds no tracked lakefile, a
require name that differs from the required package's name, and a require
cycle each fail it as well, so an edge cannot silently drop out of the page.

**Derived, not replayed.** The order follows from the require graph. The
whole recipe has not been run end to end, on purpose: rebuilding the chained
packages from nothing is what ran out of memory in the audit (see below).
What was run for this page, locally on 2026-09-18 in a fresh worktree at
`827bf983`: `lake build` in `lean4/` (exit 0, 80 jobs, six warnings), then
`lake build` in `research/local_reuse/lean` (exit 0, 19 jobs). No other
command in the block was run for it.

## The order, in words

1. Build `lean4/` alone, first. After that, a dependent build reuses the
   sealed modules instead of compiling them: the `local_reuse` build above
   compiled only its own two libraries, and from the sealed package it only
   replayed the logged warnings of two modules.
2. For each require group, build its packages one at a time in the order
   given: its longest chain, with every other member of the group placed
   after everything it requires. The block names the packages; they come
   from the lakefiles, so a require line removed or added changes them.
3. Then the packages that require only `lean4`, one at a time, in any
   order.
4. The packages that require nothing compile inside their own `.lake/` and
   do not read `lean4/.lake/`. They can go at any point, still one at a
   time.

## Parallelism: order and isolation, not a flag

- `lake --help` and `lake build --help` (Lake 5.0.0-src+d8b1897 with Lean
  4.33.0, run inside `lean4/` on 2026-09-18) list no option that limits the
  number of build jobs.
- `lean --help` lists `-j, --threads` and `-M, --memory`. They apply to a
  single-file `lean` run, such as `lake env lean Inventory.lean`; the
  command line of `lake build` offers no way to pass them to the `lean`
  processes it starts.
- So the controls are order and isolation: one Lake or Lean job on the
  machine at a time, and never two tree verifiers at once.
  `ci/run_gates.py` refuses to start while another run of it holds its
  machine lock; nothing locks a bare `lake build`.

Audit observations, recorded by the audit and not reproduced here:

- `INTERNAL PANIC: out of memory` on seven sealed modules during a fresh
  `lake build` of `research/magnification/lean`, on a 16 GB machine with
  about 3.5 GB free after the failure and other Lean processes resident.
- Read failures on `.olean.private` files while other Lean runs were
  active, which passed when the unchanged command was rerun.

Treat both as resource exhaustion: stop the other Lean jobs and rerun that
one package alone. Neither shows a defect in the sources.

## Toolchain

Run `lake` from inside the package directory, as the block does. elan picks
the toolchain from the `lean-toolchain` file of the working directory or its
nearest parent. The repository root has none, so from there elan falls back
to its default: on this machine `lean --version` at the root reported Lean
4.34.0, while the build directories pin the toolchain listed in the block
(both read on 2026-09-18).

## Windows: `PYTHONUTF8`

Set `$env:PYTHONUTF8 = '1'` before running a research verifier directly.
The block does, and `ci/run_gates.py` does for every step it runs. Many
research scripts call `lake` or `lean` with `text=True` and no `encoding`;
under the Windows default code page, Lean output that the code page cannot
decode raises a decode error in Python, and that error hides the Lean error
behind it.

## Expected warnings from sealed modules

The fresh `lake build` in `lean4/` above printed six warnings, all in sealed
modules, which are not edited:

| location | warning |
|---|---|
| `Derivation/Erasure.lean:96:33` | a `simp` argument is unused |
| `Derivation/Progress.lean:31:20` | `simp` suggested instead of `simpa` |
| `Derivation/Progress.lean:45:39` | variable `hwf` is not referenced |
| `Derivation/Progress.lean:76:5` | variable `hi` is not referenced |
| `Derivation/Apartness.lean:172:16` | variable `x` is not referenced |
| `Derivation/Apartness.lean:172:18` | variable `y` is not referenced |

A dependent build replays the warnings of whichever of these modules its
imports reach: the `local_reuse` build replayed the `Erasure` and
`Progress` ones. They are expected output, not a regression.

## One module name, many packages

Several packages in one require closure supply a root module named
`Inventory`; the last table of the block lists every closure where a root
module is supplied more than once. In those packages, compile a census
module by file path, as `lake env lean Inventory.lean` from the package
directory or `lake build` of the package's own target, never through
`import Inventory`, which leaves the search path to decide whose module it
gets. The block's table reads library roots only; the census over every
tracked module is `tests/test_research_module_names.py`, which pins each
such collision and fails when a research verifier feeds `import Inventory`
to Lean inside a closure with more than one `Inventory`.

## Script steps

The last column of the build-entry table names the packages whose build
needs a tree script, and says whether the script runs instead of
`lake build` or after it. The scripts compute their own paths, so the
directory they run in does not matter to them; the block runs each one in
its tree directory. For `admission_sign_shadow`, the audit observed a direct
build of the three modules the script compiles stop at
`unknown module prefix 'Derivation'`. That is by design: the package does
not require `lean4`, and the script supplies a frozen copy of the sealed
package instead.

## What this page does not claim

- That every command in the block succeeds: only the two builds named above
  were run for it.
- Anything about time or memory beyond those two builds and the audit
  observations above.
- That the hand-recorded entries are complete beyond what the generator
  checks. An untracked lakefile source directory is caught; a script step
  a package needs for some other reason is not.

<!-- generated by ci/lean_build_order.py: begin -->

### Build sequence

100 build entries: 4 base, 16 in 3 require group(s), 13 requiring only a base package, 67 requiring nothing.  Run the block from the repository root.  Each command throws when it fails, so a run of the block saved as a script stops at the first failure.

```powershell
$env:PYTHONUTF8 = '1'
function Invoke-InDir([string]$Dir, [string]$Exe, [string[]]$Arguments) {
  if (-not (Test-Path -LiteralPath $Dir -PathType Container)) { throw "no directory: ${Dir}" }
  Push-Location -LiteralPath $Dir -ErrorAction Stop
  try {
    & $Exe @Arguments
    if ($LASTEXITCODE -ne 0) { throw "failed in ${Dir}: $Exe $Arguments" }
  } finally {
    Pop-Location
  }
}
# Base package(s), alone, before anything that requires them.
Invoke-InDir 'lean4' 'lake' @('build')
Invoke-InDir 'research/g011_finitary_substrate/lean' 'lake' @('build')
Invoke-InDir 'research/g013_trace_calculus/lean' 'lake' @('build')
Invoke-InDir 'research/p209b_clifford_symplectic/lean' 'lake' @('build')
# Require group 1: its longest chain, one at a time: local_reuse -> ignition -> magnification -> setting_translation -> represented_execution -> coherent_process_limits -> record_reading.
# Require group 1: other members sit after what each one requires.
Invoke-InDir 'research/local_reuse/lean' 'lake' @('build')
Invoke-InDir 'research/ignition/lean' 'lake' @('build')
Invoke-InDir 'research/magnification/lean' 'lake' @('build')
Invoke-InDir 'research/setting_translation/lean' 'lake' @('build')
Invoke-InDir 'research/represented_execution/lean' 'lake' @('build')
Invoke-InDir 'research/coherent_process_limits/lean' 'lake' @('build')
Invoke-InDir 'research/record_reading/lean' 'lake' @('build')
Invoke-InDir 'research/uncollapse/lean' 'lake' @('build')
Invoke-InDir 'research/instance_demand/lean' 'lake' @('build')
Invoke-InDir 'research/unboundedness/lean' 'lake' @('build')
# Require group 2: its longest chain, one at a time: native_bridge -> conservation_ladder -> domain_adapters.
# Require group 2: other members sit after what each one requires.
Invoke-InDir 'research/native_bridge/lean' 'lake' @('build')
Invoke-InDir 'research/conservation_ladder/lean' 'lake' @('build')
Invoke-InDir 'research/domain_adapters/lean' 'lake' @('build')
Invoke-InDir 'research/native_structure/lean' 'lake' @('build')
# Require group 3: its longest chain, one at a time: two_theorems -> qm_bridge.
Invoke-InDir 'research/two_theorems/lean' 'lake' @('build')
Invoke-InDir 'research/qm_bridge/lean' 'lake' @('build')
# Packages that require only a base package, one at a time, any order.
Invoke-InDir 'research/alpha_engine/lean' 'lake' @('build')
Invoke-InDir 'research/endogenous_continuum/lean' 'lake' @('build')
Invoke-InDir 'research/endogenous_demand/lean' 'lake' @('build')
Invoke-InDir 'research/f_class_distinctness/lean' 'lake' @('build')
Invoke-InDir 'research/g010_primitive_removal/lean' 'lake' @('build')
Invoke-InDir 'research/g012_typed_translation/lean' 'lake' @('build')
Invoke-InDir 'research/interpreter_verdict/lean' 'lake' @('build')
Invoke-InDir 'research/iso_sound/lean' 'lake' @('build')
Invoke-InDir 'research/m105_number_tower/lean' 'lake' @('build')
Invoke-InDir 'research/primitive_difference_tower/lean' 'lake' @('build')
Invoke-InDir 'research/reachable/lean' 'lake' @('build')
Invoke-InDir 'research/reading_f_iso' 'lake' @('build')
Invoke-InDir 'research/target_a_execution/lean' 'lake' @('build')
# Packages that require nothing; they do not read lean4/.lake/.
Invoke-InDir 'research/admission_sign_shadow/lean' 'lake' @('build')
Invoke-InDir 'research/admission_sign_shadow' 'python' @('verify_frozen_compatibility.py', '--check')
Invoke-InDir 'research/balance_carrier/lean' 'lake' @('build')
Invoke-InDir 'research/boundary_seed/lean' 'lake' @('build')
Invoke-InDir 'research/closed_family/lean' 'lake' @('build')
Invoke-InDir 'research/concurrency/lean' 'lake' @('build')
Invoke-InDir 'research/convention_price/lean' 'lake' @('build')
Invoke-InDir 'research/described_replay/lean' 'lake' @('build')
Invoke-InDir 'research/diagonal_identity' 'python' @('verify_lean.py')
Invoke-InDir 'research/evidence_graph/lean' 'lake' @('build')
Invoke-InDir 'research/exchange_coefficients' 'python' @('verify.py')
Invoke-InDir 'research/family_embedding' 'python' @('verify_lean.py')
Invoke-InDir 'research/fresh_characters/lean' 'lake' @('build')
Invoke-InDir 'research/g001_target_charter/lean' 'lake' @('build')
Invoke-InDir 'research/g014_observer_descent/lean' 'lake' @('build')
Invoke-InDir 'research/g015_autonomous_stepping/lean' 'lake' @('build')
Invoke-InDir 'research/g018_self_hosting/lean' 'lake' @('build')
Invoke-InDir 'research/higher_order_diagonalization/lean' 'lake' @('build')
Invoke-InDir 'research/internal_syntax_logic/lean' 'lake' @('build')
Invoke-InDir 'research/iso_sound_lean/lean' 'lake' @('build')
Invoke-InDir 'research/limit_and_observer/lean' 'lake' @('build')
Invoke-InDir 'research/m104_equality_order/lean' 'lake' @('build')
Invoke-InDir 'research/m108_internal_algebra/lean' 'lake' @('build')
Invoke-InDir 'research/m109_obstruction_homology/lean' 'lake' @('build')
Invoke-InDir 'research/m114_solver_adapter/lean' 'lake' @('build')
Invoke-InDir 'research/multi_depth/lean' 'lake' @('build')
Invoke-InDir 'research/natural_sections' 'python' @('verify_lean.py')
Invoke-InDir 'research/observer_visibility/lean' 'lake' @('build')
Invoke-InDir 'research/oriented_boundary/lean' 'lake' @('build')
Invoke-InDir 'research/p200_operational_protocols/lean' 'lake' @('build')
Invoke-InDir 'research/p201_relational_spacetime/lean' 'lake' @('build')
Invoke-InDir 'research/p203_composite_systems/lean' 'lake' @('build')
Invoke-InDir 'research/p204_operational_valuations/lean' 'lake' @('build')
Invoke-InDir 'research/p208a_path_interference/lean' 'lake' @('build')
Invoke-InDir 'research/p208b_contextuality_nonlocality/lean' 'lake' @('build')
Invoke-InDir 'research/p208c_commutator_tomography/lean' 'lake' @('build')
Invoke-InDir 'research/p209a_wigner_phase_space/lean' 'lake' @('build')
Invoke-InDir 'research/p209c_stabilizer_codes/lean' 'lake' @('build')
Invoke-InDir 'research/p209d_nonclassical_horizons/lean' 'lake' @('build')
Invoke-InDir 'research/path_dependent_cost/lean' 'lake' @('build')
Invoke-InDir 'research/reach_additivity/lean' 'lake' @('build')
Invoke-InDir 'research/reach_measure/lean' 'lake' @('build')
Invoke-InDir 'research/redheffer' 'lake' @('build')
Invoke-InDir 'research/s9_obligations' 'python' @('verify_lean.py')
Invoke-InDir 'research/second_class/lean' 'lake' @('build')
Invoke-InDir 'research/second_duration/lean' 'lake' @('build')
Invoke-InDir 'research/second_engine/lean' 'lake' @('build')
Invoke-InDir 'research/second_index/lean' 'lake' @('build')
Invoke-InDir 'research/second_iso/lean' 'lake' @('build')
Invoke-InDir 'research/second_nofirst/lean' 'lake' @('build')
Invoke-InDir 'research/second_profile/lean' 'lake' @('build')
Invoke-InDir 'research/second_response/lean' 'lake' @('build')
Invoke-InDir 'research/second_run/lean' 'lake' @('build')
Invoke-InDir 'research/second_succession/lean' 'lake' @('build')
Invoke-InDir 'research/second_symmetry/lean' 'lake' @('build')
Invoke-InDir 'research/self_interpreter' 'lake' @('build')
Invoke-InDir 'research/seventh_constructor/lean' 'lake' @('build')
Invoke-InDir 'research/side_free/lean' 'lake' @('build')
Invoke-InDir 'research/sign_tower/lean' 'lake' @('build')
Invoke-InDir 'research/standing_commitment/lean' 'lake' @('build')
Invoke-InDir 'research/target_b_dynamics/lean' 'lake' @('build')
Invoke-InDir 'research/twin_pricing/lean' 'lake' @('build')
Invoke-InDir 'research/typed_translation/lean' 'lake' @('build')
Invoke-InDir 'research/x300_observer_information/lean' 'lake' @('build')
Invoke-InDir 'research/x301_formal_semantics/lean' 'lake' @('build')
Invoke-InDir 'research/x302_operational_reasoning/lean' 'lake' @('build')
Invoke-InDir 'research/x303_bounded_agency/lean' 'lake' @('build')
Invoke-InDir 'research/x310_vertical_integration/lean' 'lake' @('build')
# Directories with a lean-toolchain and no lakefile: one file at a time.
Invoke-InDir 'research/symmetry_floor/lean' 'lean' @('SymmetryFloor.lean')
```

### Every build entry

| step | directory | Lake name | requires | depth | builds into `lean4/.lake/` | script step |
|---|---|---|---|---|---|---|
| 1 | `lean4` | `derivation` | none | 0 | yes | none |
| 2 | `research/g011_finitary_substrate/lean` | `g011_finitary_substrate` | none | 0 | no | none |
| 3 | `research/g013_trace_calculus/lean` | `g013_trace_calculus` | none | 0 | no | none |
| 4 | `research/p209b_clifford_symplectic/lean` | `p209b_clifford_symplectic` | none | 0 | no | none |
| 5 | `research/local_reuse/lean` | `local_reuse` | `derivation` | 1 | yes | none |
| 6 | `research/ignition/lean` | `ignition` | `derivation`, `local_reuse` | 2 | yes | none |
| 7 | `research/magnification/lean` | `magnification` | `derivation`, `local_reuse`, `ignition` | 3 | yes | none |
| 8 | `research/setting_translation/lean` | `setting_translation` | `derivation`, `local_reuse`, `magnification` | 4 | yes | none |
| 9 | `research/represented_execution/lean` | `represented_execution` | `derivation`, `setting_translation` | 5 | yes | none |
| 10 | `research/coherent_process_limits/lean` | `coherent_process_limits` | `derivation`, `represented_execution` | 6 | yes | none |
| 11 | `research/record_reading/lean` | `record_reading` | `derivation`, `coherent_process_limits` | 7 | yes | none |
| 12 | `research/uncollapse/lean` | `uncollapse` | `derivation`, `ignition` | 3 | yes | none |
| 13 | `research/instance_demand/lean` | `instance_demand` | `derivation`, `represented_execution` | 6 | yes | none |
| 14 | `research/unboundedness/lean` | `unboundedness` | `derivation`, `local_reuse`, `ignition`, `represented_execution`, `coherent_process_limits` | 7 | yes | none |
| 15 | `research/native_bridge/lean` | `native_bridge` | `derivation`, `g013_trace_calculus` | 1 | yes | none |
| 16 | `research/conservation_ladder/lean` | `conservation_ladder` | `derivation`, `native_bridge` | 2 | yes | none |
| 17 | `research/domain_adapters/lean` | `domain_adapters` | `derivation`, `native_bridge`, `conservation_ladder`, `p209b_clifford_symplectic` | 3 | yes | none |
| 18 | `research/native_structure/lean` | `native_structure` | `derivation`, `native_bridge` | 2 | yes | none |
| 19 | `research/two_theorems/lean` | `two_theorems` | `derivation` | 1 | yes | none |
| 20 | `research/qm_bridge/lean` | `qm_bridge` | `derivation`, `two_theorems` | 2 | yes | none |
| 21 | `research/alpha_engine/lean` | `harness` | `derivation` | 1 | yes | none |
| 22 | `research/endogenous_continuum/lean` | `endogenous_continuum` | `derivation` | 1 | yes | none |
| 23 | `research/endogenous_demand/lean` | `endogenous_demand` | `derivation` | 1 | yes | none |
| 24 | `research/f_class_distinctness/lean` | `f_class_distinctness` | `derivation` | 1 | yes | none |
| 25 | `research/g010_primitive_removal/lean` | `g010_primitive_removal` | `derivation` | 1 | yes | none |
| 26 | `research/g012_typed_translation/lean` | `g012_typed_translation` | `derivation` | 1 | yes | none |
| 27 | `research/interpreter_verdict/lean` | `interpreter_verdict` | `derivation` | 1 | yes | none |
| 28 | `research/iso_sound/lean` | `iso_sound` | `derivation` | 1 | yes | none |
| 29 | `research/m105_number_tower/lean` | `m105_number_tower` | `g011_finitary_substrate` | 1 | no | none |
| 30 | `research/primitive_difference_tower/lean` | `primitive_difference_tower` | `derivation` | 1 | yes | none |
| 31 | `research/reachable/lean` | `reachable` | `derivation` | 1 | yes | none |
| 32 | `research/reading_f_iso` | `reading_f_iso` | `derivation` | 1 | yes | none |
| 33 | `research/target_a_execution/lean` | `target_a_execution` | `derivation` | 1 | yes | none |
| 34 | `research/admission_sign_shadow/lean` | `admission_sign_shadow` | none | 0 | no | `python verify_frozen_compatibility.py --check` in `research/admission_sign_shadow`, after `lake build`: `lake build` compiles only the two roots and what they import; the three modules named here compile only through this script, against a frozen copy of the sealed package that it builds in a temporary directory (`AdmissionSignShadow.FrozenPairBridge`, `AdmissionSignShadow.ReplayOccurrence`, `AdmissionSignShadow.ActualSectionAdapter`) |
| 35 | `research/balance_carrier/lean` | `balance_carrier` | none | 0 | no | none |
| 36 | `research/boundary_seed/lean` | `boundaryseed` | none | 0 | no | none |
| 37 | `research/closed_family/lean` | `closed_family` | none | 0 | no | none |
| 38 | `research/concurrency/lean` | `concurrency` | none | 0 | no | none |
| 39 | `research/convention_price/lean` | `convention_price` | none | 0 | no | none |
| 40 | `research/described_replay/lean` | `described_replay` | none | 0 | no | none |
| 41 | `research/diagonal_identity/lean` | `diagonal_identity` | none | 0 | no | `python verify_lean.py` in `research/diagonal_identity`, instead of `lake build`: stages the gitignored `lean/sealed/` from pinned blobs, then runs `lake build`; a fresh clone has no `lean/sealed/`, so a bare `lake build` has no source for it |
| 42 | `research/evidence_graph/lean` | `evidence_graph` | none | 0 | no | none |
| 43 | `research/exchange_coefficients/lean` | `exchange_coefficients` | none | 0 | no | `python verify.py` in `research/exchange_coefficients`, instead of `lake build`: stages the gitignored `lean/pinned/` from pinned blobs, then runs `lake build`; it also rewrites the tree's tracked `evidence/` files, so check `git status` after it |
| 44 | `research/family_embedding/lean` | `family_embedding` | none | 0 | no | `python verify_lean.py` in `research/family_embedding`, instead of `lake build`: stages the gitignored `lean/sealed/` from pinned blobs, then runs `lake build`; a fresh clone has no `lean/sealed/`, so a bare `lake build` has no source for it |
| 45 | `research/fresh_characters/lean` | `fresh_characters` | none | 0 | no | none |
| 46 | `research/g001_target_charter/lean` | `g001_target_charter` | none | 0 | no | none |
| 47 | `research/g014_observer_descent/lean` | `g014_observer_descent` | none | 0 | no | none |
| 48 | `research/g015_autonomous_stepping/lean` | `g015_autonomous_stepping` | none | 0 | no | none |
| 49 | `research/g018_self_hosting/lean` | `g018_self_hosting` | none | 0 | no | none |
| 50 | `research/higher_order_diagonalization/lean` | `higher_order_diagonalization` | none | 0 | no | none |
| 51 | `research/internal_syntax_logic/lean` | `internal_syntax_logic` | none | 0 | no | none |
| 52 | `research/iso_sound_lean/lean` | `iso_sound_lean` | none | 0 | no | none |
| 53 | `research/limit_and_observer/lean` | `limit_observer` | none | 0 | no | none |
| 54 | `research/m104_equality_order/lean` | `m104_equality_order` | none | 0 | no | none |
| 55 | `research/m108_internal_algebra/lean` | `m108_internal_algebra` | none | 0 | no | none |
| 56 | `research/m109_obstruction_homology/lean` | `m109_obstruction_homology` | none | 0 | no | none |
| 57 | `research/m114_solver_adapter/lean` | `m114_solver_adapter` | none | 0 | no | none |
| 58 | `research/multi_depth/lean` | `multi_depth` | none | 0 | no | none |
| 59 | `research/natural_sections/lean` | `natural_sections` | none | 0 | no | `python verify_lean.py` in `research/natural_sections`, instead of `lake build`: stages the gitignored `lean/sealed/` from pinned blobs, then runs `lake build`; a fresh clone has no `lean/sealed/`, so a bare `lake build` has no source for it |
| 60 | `research/observer_visibility/lean` | `observer_visibility` | none | 0 | no | none |
| 61 | `research/oriented_boundary/lean` | `orientedboundary` | none | 0 | no | none |
| 62 | `research/p200_operational_protocols/lean` | `p200_operational_protocols` | none | 0 | no | none |
| 63 | `research/p201_relational_spacetime/lean` | `p201_relational_spacetime` | none | 0 | no | none |
| 64 | `research/p203_composite_systems/lean` | `p203_composite_systems` | none | 0 | no | none |
| 65 | `research/p204_operational_valuations/lean` | `p204_operational_valuations` | none | 0 | no | none |
| 66 | `research/p208a_path_interference/lean` | `p208a_path_interference` | none | 0 | no | none |
| 67 | `research/p208b_contextuality_nonlocality/lean` | `p208b_contextuality_nonlocality` | none | 0 | no | none |
| 68 | `research/p208c_commutator_tomography/lean` | `p208c_commutator_tomography` | none | 0 | no | none |
| 69 | `research/p209a_wigner_phase_space/lean` | `p209a_wigner_phase_space` | none | 0 | no | none |
| 70 | `research/p209c_stabilizer_codes/lean` | `p209c_stabilizer_codes` | none | 0 | no | none |
| 71 | `research/p209d_nonclassical_horizons/lean` | `p209d_nonclassical_horizons` | none | 0 | no | none |
| 72 | `research/path_dependent_cost/lean` | `path_dependent_cost` | none | 0 | no | none |
| 73 | `research/reach_additivity/lean` | `reach_additivity` | none | 0 | no | none |
| 74 | `research/reach_measure/lean` | `reach_measure` | none | 0 | no | none |
| 75 | `research/redheffer` | `redheffer` | none | 0 | no | none |
| 76 | `research/s9_obligations/lean` | `s9_obligations` | none | 0 | no | `python verify_lean.py` in `research/s9_obligations`, instead of `lake build`: stages the gitignored `lean/sealed/` from pinned blobs, then runs `lake build`; a fresh clone has no `lean/sealed/`, so a bare `lake build` has no source for it |
| 77 | `research/second_class/lean` | `second_class` | none | 0 | no | none |
| 78 | `research/second_duration/lean` | `second_duration` | none | 0 | no | none |
| 79 | `research/second_engine/lean` | `second_engine` | none | 0 | no | none |
| 80 | `research/second_index/lean` | `second_index` | none | 0 | no | none |
| 81 | `research/second_iso/lean` | `second_iso` | none | 0 | no | none |
| 82 | `research/second_nofirst/lean` | `second_nofirst` | none | 0 | no | none |
| 83 | `research/second_profile/lean` | `second_profile` | none | 0 | no | none |
| 84 | `research/second_response/lean` | `second_response` | none | 0 | no | none |
| 85 | `research/second_run/lean` | `second_run` | none | 0 | no | none |
| 86 | `research/second_succession/lean` | `second_succession` | none | 0 | no | none |
| 87 | `research/second_symmetry/lean` | `second_symmetry` | none | 0 | no | none |
| 88 | `research/self_interpreter` | `self_interpreter` | none | 0 | no | none |
| 89 | `research/seventh_constructor/lean` | `seventh_constructor` | none | 0 | no | none |
| 90 | `research/side_free/lean` | `sidefree` | none | 0 | no | none |
| 91 | `research/sign_tower/lean` | `sign_tower` | none | 0 | no | none |
| 92 | `research/standing_commitment/lean` | `standing_commitment` | none | 0 | no | none |
| 93 | `research/target_b_dynamics/lean` | `target_b_dynamics` | none | 0 | no | none |
| 94 | `research/twin_pricing/lean` | `twin_pricing` | none | 0 | no | none |
| 95 | `research/typed_translation/lean` | `typedtranslation` | none | 0 | no | none |
| 96 | `research/x300_observer_information/lean` | `x300_observer_information` | none | 0 | no | none |
| 97 | `research/x301_formal_semantics/lean` | `x301_formal_semantics` | none | 0 | no | none |
| 98 | `research/x302_operational_reasoning/lean` | `x302_operational_reasoning` | none | 0 | no | none |
| 99 | `research/x303_bounded_agency/lean` | `x303_bounded_agency` | none | 0 | no | none |
| 100 | `research/x310_vertical_integration/lean` | `x310_vertical_integration` | none | 0 | no | none |

### Toolchain pins

- `leanprover/lean4:v4.33.0`: 101 build directories.

### Root modules supplied more than once in one require closure

| directory | module | supplied by |
|---|---|---|
| `research/ignition/lean` | `Inventory` | `ignition`, `local_reuse` |
| `research/magnification/lean` | `Inventory` | `ignition`, `local_reuse`, `magnification` |
| `research/setting_translation/lean` | `Inventory` | `ignition`, `local_reuse`, `magnification`, `setting_translation` |
| `research/represented_execution/lean` | `Inventory` | `ignition`, `local_reuse`, `magnification`, `represented_execution`, `setting_translation` |
| `research/coherent_process_limits/lean` | `Inventory` | `coherent_process_limits`, `ignition`, `local_reuse`, `magnification`, `represented_execution`, `setting_translation` |
| `research/record_reading/lean` | `Inventory` | `coherent_process_limits`, `ignition`, `local_reuse`, `magnification`, `record_reading`, `represented_execution`, `setting_translation` |
| `research/uncollapse/lean` | `Inventory` | `ignition`, `local_reuse` |
| `research/instance_demand/lean` | `Inventory` | `ignition`, `instance_demand`, `local_reuse`, `magnification`, `represented_execution`, `setting_translation` |
| `research/unboundedness/lean` | `Inventory` | `coherent_process_limits`, `ignition`, `local_reuse`, `magnification`, `represented_execution`, `setting_translation`, `unboundedness` |
| `research/domain_adapters/lean` | `Inventory` | `g013_trace_calculus`, `p209b_clifford_symplectic` |
| `research/m105_number_tower/lean` | `Inventory` | `g011_finitary_substrate`, `m105_number_tower` |

<!-- generated by ci/lean_build_order.py: end -->
