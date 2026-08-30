# PREFLIGHT -- S9 obligations run, PROMPT.md steps 1-4

AuthorityEffect: None.  This run proposes; it amends nothing sealed.

House rule, from the prompt: nothing happens that is not declared.  A
green test is not a discharged obligation.  A table is not a
computation.  An absent separation is not an equality.

Everything below was declared before any part computed.  The parts P1,
P2, P3 are bound by the bounds in step 4; a part may reach less than a
bound and must say so, and no part raises a bound.  Raising one is an
amendment of this file, recorded as such, never a silent widening.

## Step 1. The prompt's blob id and the snapshot commit

| object | id |
|---|---|
| governing prompt, `research/s9_obligations/PROMPT.md` | Git blob `1642e3f6ac746002678e4997f738e0fabd1248c9` |
| snapshot commit (HEAD when this preflight ran) | `db1d2b225b577d5212780ff02700efd693c8e446` |

Commands used, from the worktree root, with what they printed:

    git rev-parse HEAD
    db1d2b225b577d5212780ff02700efd693c8e446

    git rev-parse HEAD:research/s9_obligations/PROMPT.md
    1642e3f6ac746002678e4997f738e0fabd1248c9

    git show HEAD:research/s9_obligations/PROMPT.md | git hash-object --stdin
    1642e3f6ac746002678e4997f738e0fabd1248c9

The third line re-derives the blob id from the blob bytes rather than
trusting the name lookup; the two agree.  The SHA-256 of the same blob
bytes is `2AA069B18E51F4361FCC32DE935ED79E446FB6FAD9668E4D89ABC942DD99ABE1`
(16026 bytes), recorded here so a reader without Git can check the file.

Every receipt records both ids: `common.receipt_header()` returns
`prompt_path`, `prompt_blob_id`, and `snapshot_commit`, and each part
embeds it.  `verify_pins.py` re-checks the blob id at HEAD and fails on
drift; on drift the run stops (step 1).

## Step 2. Write root and sealed paths

Write root: `research/s9_obligations/`.  The sealed paths, verbatim from
the prompt:

    `prompt/`, `paper/`, `code/`, `lean4/Derivation/`, `artifacts/` are
    read-only here.  Writing any of them fails the run.  Amending the
    seal is the author's act, not this run's.

Also not written by this run: `.github/`, `ci/`, `tests/`, `contact/`,
`CLAUDE.md`, and every other `research/` tree.  Two mechanical guards
carry the rule: `common.assert_inside_tree` refuses any path that does
not resolve under the write root, and every part calls it before
writing; `verify_pins.py` fails when
`git status --porcelain -- prompt paper code lean4/Derivation artifacts`
prints anything (step 35).  Lake build products under
`research/s9_obligations/lean/.lake/` are gitignored build output, not
source writes.

## The numbering convention

S9.1, S9.2, S9.3 are the first three bullets of section S9 of
`paper/primitive_difference.md`, in the order they appear there:

* S9.1 -- the axiom lattice (first bullet);
* S9.2 -- morphism classes and initiality (second bullet);
* S9.3 -- witness types (third bullet).

That numbering is the prompt's, not the paper's: the paper's S9 is an
unnumbered bullet list.  The paper's fourth bullet (finite-search
results exhaustive only for carrier at most 3), fifth bullet (the
finite-scope matrix's exhaustiveness lives in Python only), and sixth
bullet (the inscription bridge) are not S9.1-S9.3.  The sixth is the
"S9 last bullet" of step 36 and, with OB-1 and S6.6, is out of scope:
this run does not claim it closed, narrowed, or priced.

## Step 3. Pins

`SOURCE_PINS.json` (schema `s9_obligations_source_pins/v1`) pins:

* the snapshot commit, as the exact 40-digit id above, never `HEAD`;
* the prompt, under the key `prompt`, by its Git blob id;
* under `sealed_inputs`, every sealed file this run reads, by the
  uppercase SHA-256 of `git show HEAD:<path>` -- the blob bytes, so the
  pin is independent of checkout line endings (this checkout has
  `core.autocrlf=true` and shows CRLF in files whose blobs are LF):

  | path | sha256 of the blob |
  |---|---|
  | `lean4/Derivation/PrimDiff.lean` | `69AC9CA08179680D28D74ECE54BC90F94854DB98F3D113DF17D0ABBCA86E23B6` |
  | `code/derivation/primdiff.py` | `A7FE540B4C0D766C9701631449A6AC3D1661C850B9F694B1B01E9D47E83E2ADA` |
  | `code/run_primdiff.py` | `4369DA516F4096882E25F435B5C65A786E9FBA034848838DFBE50ED74C8F1E4C` |
  | `artifacts/primdiff.json` | `D6991342399160B9B6AD7F3D3E1460E4D2472A03EC975BD097581614549B860C` |
  | `paper/primitive_difference.md` | `F69DA9978691945D588C8F7A9283AC50C2FA3F53ADFD1A2CABA90F912ECC0BEC` |

The shape follows `research/blind_restart/SOURCE_PINS.json` (schema,
note, snapshot commit, a list of `{path, sha256}` entries).  The one
declared difference: the list key is `sealed_inputs` rather than
`artifacts`, because the paper and the Lean module are not artifacts,
and the `prompt` entry is separate because it is pinned by blob id, not
by SHA-256.  The prompt asks for `SOURCE_MANIFEST.json`; the sibling
shape it also asks this tree to follow is named `SOURCE_PINS.json`, and
the brief for this run named the file that way.  The name follows the
shape; the content is the manifest the prompt describes.

`verify_pins.py` re-checks, against HEAD: every sealed hash; the prompt
blob id; that the snapshot commit is 40 lowercase hex digits (so `HEAD`
is refused); that every pinned path is relative, has no `..`, no
backslash, no drive letter, and lies under a sealed prefix; and that the
sealed prefixes carry no worktree change.  It exits non-zero on the first
failure.  `--repin` rewrites the hashes from HEAD and verifies nothing.

What it does not check: that the pinned set is the right set (a pin on
the wrong file is still a pin), the interpreter, Git, or itself.
`test_verify_pins.py` exercises every refusal in-process on a tampered
copy of the loaded pins (the JSON is never written), and the sealed-prefix
refusal on a synthetic porcelain line `?? paper/x.md`, so no sealed path
is touched to prove the check bites.

## Step 4. Declared resource bounds

Declared before any part ran.  N is a carrier size; "required" means
the part must reach it, "attempted" means the part reports whether it
completed inside the bound, "refused by name" means no computation at
that size is attempted in this run, for any reason.

### P1 -- S9.1, the axiom lattice

* Carrier bound: N = 3 required (carriers 1, 2, 3; the relation census
  is 2^1 + 2^4 + 2^9 = 530 relations, arithmetic from the declaration --
  P1 prints the count it enumerates).  N = 4 attempted (adds 2^16 =
  65536 relations, census 66066); "completed inside the bound" means
  every clause extent and the closure below were computed over all
  66066 relations with the closure bound not hit.  N = 5 is refused by
  name.
* Clause space (step 5): 4 atoms, head one atom or falsum (5 options),
  body any subset of the atoms (16 options), so 5 x 16 = 80 raw clauses
  before the swap quotient.  That 80 is arithmetic; P1 prints the
  enumerated count before and after quotienting by the swap of x and y,
  and states which count it uses downstream.
* Closure-size bound for the extent lattice (step 9): 65536 = 2^16
  distinct extents.  The meet-closure of the single-clause extents stops
  when 65536 distinct extents have been produced.  If the bound is hit,
  P1 reports `S9_1_LATTICE_BOUNDED` with the partial closure, marked
  truncated; a truncated closure is not reported as the lattice.
* The `EQ_BEARING` fragment (step 6) is enumerated separately under the
  same bounds and is never merged into the pure fragment's results
  without saying so in the same sentence.

### P2 -- S9.2, morphism classes and initiality

* Object carrier bound: objects Y range over pointed structures with an
  asserted pair on carriers of size 1..N.  N = 3 required, N = 4
  attempted, N = 5 refused by name.  The candidate initial objects O
  have carrier exactly 2.  Whether irreflexivity is imposed on objects,
  and whether the asserted pair may be diagonal, are P2's declarations
  under step 15, not bounds; P2 states them before enumerating.
* Menu size bound: at most 8 morphism conditions (so at most 2^8 = 256
  classes); the prompt's five are the required minimum.
* Any class or cell not completed at N = 4 is reported at N = 3, and the
  whole classification is marked `S9_2_CLASSES_BOUNDED` at the carrier
  reached (step 19); initiality quantifies over all objects and the
  sweep reaches only N.

### P3 -- S9.3, proof-relevant witness types

* Carrier bound: N = 2 required, N = 3 attempted, N = 4 refused by name.
* Token-domain size bound T: T = 2 required, T = 3 attempted, T = 4
  refused by name.
* Assignment-count bound: at most 2^20 = 1048576 witness assignments are
  enumerated per (N, T) cell.  A cell whose declared assignment space
  exceeds 2^20 is not enumerated; it is reported as bounded with the
  cells that finished, each named by its (N, T).
* The vocabularies V0, V1, V2 (step 22) are declared by P3 as explicit
  finite question sets with their counts, before any pair is searched.

### What happens when a bound is hit

Report the terminal's bounded form with the partial result -- the cells
that completed, each named -- and never extrapolate.  The word "bounded"
goes in the same sentence as the result, naming the bound reached.  A
carrier-general claim without a Lean theorem naming the general case is
forbidden (step 37); the permitted wording is "finite computation,
bounded by N = ...".

Receipt convention for bounds: every part receipt carries
`declared_bounds` (copied from this section) and `bounds_reached`, and
every result object that depends on a bound carries `bounded` (true or
false) and `bound_reached`.

## The Lake package skeleton (step 27) and its build receipt

`research/s9_obligations/lean/` is modeled on
`research/primitive_difference_tower/lean/`: package `s9_obligations`,
library `S9Obligations` with roots `S9Obligations` and
`S9Obligations.AxiomReport`, `require derivation from "../../../lean4"`,
a `lake-manifest.json` with the same path-dependency shape, `.gitignore`
holding `.lake/`, and `lean-toolchain` byte-identical to the blob
`HEAD:lean4/lean-toolchain` (`leanprover/lean4:v4.33.0` plus LF; checked
by comparing bytes with `git show`).  The root imports
`Derivation.PrimDiff` and nothing else yet; it adds no module under
`lean4/Derivation/`.  `S9Obligations/AxiomReport.lean` imports the root
and holds the report inventory, appended per part.

Build receipt: `cd research/s9_obligations/lean && lake build` exited 0;
last line `Build completed successfully (6 jobs).`  The sealed package
was consumed from its existing build under `lean4/.lake/`; nothing under
`lean4/` was written.

## Manual receipt (step 29)

This tree's axiom reports are a manual receipt.  No CI gate reads them.
Nothing in `.github/workflows` runs `verify_lean.py` or `verify_pins.py`;
a pass is a receipt for the sources present when it ran.  `STATUS.md`,
written last by the synthesis pass, must say so in those words.

`verify_lean.py` builds the package, applies the sealed tree's
forbidden-token scan (`sorry`, `admit`, `unsafe`, `partial`, and a line
beginning with the axiom keyword) to every `.lean` file under `lean/`
outside `.lake`, runs `lake env lean S9Obligations/AxiomReport.lean`,
parses every report line with a non-greedy name capture, requires the
reported set to equal `AXIOM_REPORT_DECLARATIONS` (initially empty), and
requires every report to lie within `{propext, Quot.sound}`.  With an
empty inventory it passes only when nothing is reported; a report it
does not list is an unaudited declaration and fails.

Proved live, not argued, each reversed before the next:

| injection | observed |
|---|---|
| `#print axioms PrimDiff.D2_initial_pointed` added to `AxiomReport.lean` AND listed in the inventory | pass; printed `PrimDiff.D2_initial_pointed: no axioms` -- the parser reads real `lake env lean` output |
| same source line, removed from the inventory | `FAIL: S9Obligations/AxiomReport.lean names ['PrimDiff.D2_initial_pointed'], but this script expects []`, exit 1 |
| a comment line carrying the first forbidden token added to `S9Obligations.lean` | `FAIL: forbidden tokens in research Lean sources: S9Obligations.lean: forbidden token 'sorry'`, exit 1 |
| both reversed | pass, 0 declarations reported, exit 0 |

The unlisted-report refusal is also a unit test
(`test_empty_inventory_passes_only_with_no_reports`).

## Shared conventions for the parts

* Receipts: JSON under `research/s9_obligations/receipts/`, written by
  `run_<part>.py --out DIR` through `common.write_receipt` --
  `json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=True)` plus one
  trailing LF, `newline="\n"`.  No timestamps, no paths, no environment
  data.  Step 33: each part generates twice into two directories and
  compares bytes, and reports that it did.
* Every count the prose states is a value under a named receipt key;
  every cited key exists.
* `common.render_relation` renders a relation given as pairs as a
  sorted list of `[x, y]` without duplicates.
* Tests: `unittest`, files `test_*.py`, run from inside the tree with
  `PYTHONPATH=../../code PYTHONUTF8=1 python -m unittest discover -s .
  -p "test_*.py"`.  Typing: `python -m mypy` from inside the tree
  (`pyproject.toml`: strict, `mypy_path = "../../code"`, `files = ["."]`).
  No per-module override is configured: mypy rejects a `test_*` glob as
  a module pattern, so a part that needs `disallow_untyped_decorators =
  false` adds an override naming its own test module.
* Sealed code is imported read-only as `from derivation.primdiff import
  ...`; nothing re-derives what `PrimDiff.lean` or `primdiff.py` already
  state.
* Vocabulary firewall (step 39): the 102-identifier working denylist was
  loaded from `contact/analysis/contact_countermodels.json` and grepped
  as identifier tokens over the 13 text files of this tree at preflight:
  0 leaks.  Parts re-run that scan over their own files before reporting.

## Preflight receipts, in order

    python research/s9_obligations/verify_pins.py                    exit 0
    cd research/s9_obligations && PYTHONPATH=../../code PYTHONUTF8=1 \
      python -m unittest discover -s . -p "test_*.py"                exit 0 (20 tests)
    cd research/s9_obligations && python -m mypy                     exit 0 (4 source files)
    python research/s9_obligations/verify_lean.py                    exit 0 (0 declarations)
    git status --porcelain -- prompt paper code lean4/Derivation artifacts   (empty)

## What this preflight does not do

It computes no result about S9.1, S9.2, or S9.3; it declares the space
the parts compute in.  It proposes no Lean theorem.  It does not touch
OB-1, S6.6, or the S9 last bullet.  It does not register this tree in
any CI gate, and does not edit `.github/workflows/verify.yml`; the
registration diff belongs to `STATUS.md` as text (step 31).
