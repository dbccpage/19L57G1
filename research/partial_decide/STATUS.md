# Partial decision grade

`STATUS: DETERMINISTIC_METATHEORETIC_COMPUTATION`

`AuthorityEffect: None`

This tree records the result of the existing finite minimum-response
computation as a partial grade:

```text
decide(r, i, j, measure, bounds) : Grade | None

None             no valid response inside the declared finite bounds
Tie(Q)           at least two implemented isomorphism classes remain
UniqueClass(Q)   one class remains, with multiple literal deltas
UniqueDelta(d)   one literal minimum remains
```

`None` is not an invalid-input bucket and is not a global impossibility
theorem. Invalid targets, measures, unsupported candidate bounds,
rule-bearing bases, and isomorphism-budget exhaustion are errors. On otherwise
valid inputs, a grade is returned only when the bounded search and quotient
computation complete.

## Current bounded C3 result

With the already declared Challenge-3 readings, targets,
`Bounds(max_items=2, max_arity=2)`, and permutation budget `100000`:

| reading | measure | raw minima | classes | grade |
|---|---:|---:|---:|---|
| L | mu1 | 6 | 3 | `Tie` |
| F | mu1 | 10 | 5 | `Tie` |
| L | mu2 | 2 | 1 | `UniqueClass` |
| F | mu2 | 2 | 1 | `UniqueClass` |

Thus `UniqueDelta` is absent from these four C3 calls at the displayed bounds
and budget, while the mu2 `UniqueClass` is inhabited by both endpoint-mark
deltas. A separate already-separated fixture returns
`UniqueDelta(())`, witnessing that the constructor is live without falsely
assigning it to C3.

Candidate enumeration is live in these computations. To form quotient keys,
`decide` replays `Impose` and each candidate delta's admission-event values
against the supplied regime into a newly constructed, ephemeral comparison
child. Those children exist only for classification: no child replaces the
declared base, no candidate is authorized, and no response or event is
persistently applied or committed to that base. This bounded candidate
enumeration is distinct from an object-language demand generator; no such
generator is defined here.

The machine-readable record is `partial_decide_c3.json`. Every class member
is retained. No field names a representative, selected delta, authorized
delta, or transition to apply.

## Panel and authorization boundary

The existing `certNeg` and `PanelEquiv` results are panel-relative. Within this
tree and its pinned import surface, their indices are not connected to the
engine's admitted-data indices by a declared carrier/pair correspondence. This
tree therefore records:

```text
NO_AUTHORIZED_OR_PERSISTENT_RESPONSE_APPLICATION
NO_EVENT_COMMITTED_TO_DECLARED_BASE
NO_PANEL_DERIVED_INPUT
NO_PANEL_ENGINE_ADAPTER
NO_RESPONSE_AUTHORIZATION
OBJECT_LANGUAGE_GENERATOR_NOT_IN_SCOPE
PANEL_TO_ENGINE_LINK_NOT_DEFINED
```

A panel may motivate a separately declared request supplied to `decide`, but
this tree derives no decision input from the panel and supplies no adapter by
which the panel chooses the engine regime, pair, reading, measure, bounds,
quotient member, or response. Absence of that correspondence is not encoded
as the function's `None` result. The absence statement is a scoped source
audit: the verifier enforces package custody and import syntax but does not
recognize every possible semantic adapter.

## Explicit scope and nonclaims

- Candidates and their admission-event values are enumerated by the declared
  bounded computation and replayed only into ephemeral comparison children.
- No panel-derived input or candidate authorization is declared; no response
  is authorized or persistently applied, and no event is committed to the
  declared base.
- No object-language demand generator is defined. Candidate enumeration for
  a supplied bounded request is not such a generator.
- No L/F reading, measure, bound, or endpoint is preferred.
- No quotient representative is selected.
- No Map C, chain/local-view correspondence, or G4 adapter is defined.
- `G3_REMAINS_CONJECTURE` and `G4_REMAINS_CONJECTURE` are inherited from the
  mechanically pinned `artifacts/g1_class_receipt.json`; they are not outputs
  of `decide`. The former finite G4 terminals remain withdrawn.
- No object-language `Laugh` or generator is added.
- No Lean theorem or axiom claim is made.
- A source pin, test pass, type check, or byte-identical receipt is not proof
  that the declared candidate measures were forced.

The receipt's `terminals` field contains scoped status labels, not a claim of
engine termination, repository completion, satisfaction of the global
stopping conditions, or authority.

## Provenance and replay

`SOURCE_PINS.json` binds the static `derivation.*` dependency closure consumed
by this package to canonical Git blobs at the declared source snapshot. It
also pins the complete tracked package population and all controlled local and
sealed imports, plus the inherited G3/G4 status receipt. `verify_pins.py`
checks immutable Git identifiers, snapshot ancestry/tree, hashes at the
snapshot and HEAD, regular Git entry modes, early source/package cleanliness,
exact consumer and local-import censuses, symbol resolution, static transitive
closure, resolved runtime import origins, prohibited dynamic-loader constructs
in the non-verifier consumers, an import audit and origin census through
receipt rendering, the mechanically pinned G3/G4 labels, an independently
literal C3 receipt contract, duplicate-free JSON decoding, a closed inherited
status map, independent replay and canonicalization of every retained class
member after custody/origin checks, receipt transport policy, complete package
custody, and byte-identical receipt regeneration. The documented writer uses
that verified isolated renderer and refuses to write when its custody
preflight fails. If writing is requested, it also refuses an existing target
that is a symlink, reparse point, directory, or other non-regular file. It
writes exact binary LF bytes to an exclusively created same-directory regular
temporary file, flushes and synchronizes that file, rechecks the target,
atomically replaces it with no fallible post-commit step, and cleans the
temporary file after an error. These are
syntactic/provenance/transport checks; they do not recognize every possible
semantic adapter.

Python necessarily starts `verify_pins.py` (or the small writer entry point)
before that file can check its own Git custody. That already-running parent,
the invoking interpreter and standard library, the Git executable, and the
parsed pin JSON are the explicit bootstrap boundary. After the early custody
preflight, receipt rendering starts a fresh `-I -B -S` child, installs the
child's audit boundary and explicit project paths, and only then imports the
receipt and derivation modules. The flags exclude environment/user-site
influence, ordinary `site` initialization, and bytecode writes in that child;
they do not retroactively authenticate the parent bootstrap.

Run from the repository root:

```powershell
$env:PYTHONPATH = "$PWD/code"
python research/partial_decide/verify_pins.py
Push-Location research/partial_decide
python -m unittest discover -s . -p "test_*.py"
python -m mypy
Pop-Location
```

Regenerate the receipt only after inspecting a deliberate semantic change:

```powershell
Push-Location research/partial_decide
python run_receipt.py --write
Pop-Location
```

`--write` delegates to the public `write_receipt_atomic` helper described
above. The helper is deliberately small so its special-target refusal,
temporary-file cleanup, and atomic-replacement behavior can be tested without
regenerating the committed receipt.

Receipt equality witnesses byte-identical regeneration in that invocation;
the repeated-call test separately checks equality for the tested inputs. It
grants no authority and is not a general determinism theorem.

## Injection record

Each probe was reversed before the next one, and the verifier/tests returned
exit zero after reversal. No receipt or source pin was regenerated while a
probe was live.

| probe | observed failure |
|---|---|
| changed the first byte of the pinned `model.py` digest | `hash mismatch for code/derivation/model.py`, with wanted, snapshot, and HEAD hashes; exit 1 |
| added `from derivation.represented import cert_neg` to the production consumer | `authorized import mismatch`, naming `derivation.represented` and `cert_neg`; exit 1 |
| changed one `authority_effect` value in the committed receipt | `partial_decide_c3.json differs from the deterministic renderer`; exit 1 |
| made a live tie return `None` | both L and F failed `test_c3_mu1_retains_all_tied_classes`; receipt equality also failed; exit 1 |

These injections show that the registered checks catch those four defects.
They do not prove that the declared measures, bounds, readings, or target are
the right declarations.

### Exact verifier and custody campaign

The first fourteen probes in this independent campaign were run from detached
worktrees at `a9aef3090d37a79434eaf053168407a46fa7be4e`. Each of their committed
probes has that commit as its parent. Every verifier failure exited one; the
type probe made mypy exit one. The relevant check returned exit zero after
every reversal.

All campaign commits were local throwaway objects and are not reachable from
a branch or tag; they may be pruned and are not the durable evidence. The
tracked mutation descriptions, commands, exact diagnostics, exits, and
recovery results below are the replay record.

| probe | injection commit | observed failure |
|---|---|---|
| removed `mu2` from one reading while duplicating `mu1` | `43b57b9311ba4cacfde58904732b6bd0c1a211e8` | `reading L grades keys differ: missing ['mu2'], extra []` |
| called dynamic `builtins.__import__` in a receipt consumer | `61c172657bcde93d9fc4f9773785807a8ea4f560` | `c3_receipt.py uses prohibited dynamic execution/import attribute __import__` |
| omitted `derivation.observe` from the source closure | `e24548b0ee503ba249ebae19628ccfd477cef8b6` | `derivation.candidates has unpinned derivation dependencies: derivation.observe` |
| removed inherited `G4_REMAINS_CONJECTURE` | `ae5d1f651dee47e34a0138df1caf2590e20551b8` | `status input required_terminals differ from G3/G4 freeze` |
| mapped `derivation.model` to `observe.py` | `3f5fdd16cafbf82304b512e7196c289d16b8d4d6` | `module/path mismatch for derivation.model` |
| registered a local `derivation.py` shadow | `12b9f3de4287456a20a2b7b26e34871cb795c18b` | `reserved derivation shadow path: research/partial_decide/derivation.py` |
| replaced the pinned source-package tree with zeroes | `6b30c490aebcc52f80f548a34f3458f65b0b947e` | `source package tree mismatch`, naming wanted, snapshot, and HEAD trees |
| replaced the exact refusal declaration with a totalizing policy | `1f5ee586fd7890fdb8d9cae9b9141886dba761e6` | `source policy differs from the exact refusal declaration` |
| replaced the source snapshot id with symbolic `HEAD` | `15c8ab7d57d80bbefdd129f82013881131349d47` | `source snapshot commit must be an exact 40-digit lowercase hex id` |
| dirtied tracked `c3_receipt.py` before custody preflight | worktree-only | `partial-Decide executable package or transport policy has worktree changes before custody preflight`, naming the file |
| committed an unlisted consumer before diagnostic repair | `758ec430baaa946177a5948676f4049a4d86333f` | `tracked package census differs across declaration, HEAD, and index`; this detected the divergence but did not name the file, so it did not meet the injection diagnostic standard |
| added an uncommitted type-invalid consumer | worktree-only | mypy reported the incompatible assignment and checked six rather than five source files |
| changed the receipt transport attribute from `-text` to `text` | `80ddae268710c4d0a5be671ad254cfa7b4fa6944` | `receipt transport attribute must be committed as -text` |
| committed the receipt with CRLF bytes under `-text` | `5e1eb4b2ac42e06f565272b55130bbe9dd9819b9` | `partial_decide_c3.json contains CR bytes` |

The unnamed census diagnostic was repaired at
`a1368cc48f64491ca1141b5b66d6239284140066` and the same defect was injected
again at `431d172bee890ae37fa7e5fabcadefa5e19f0fda`. The verifier then exited one
with:

```text
FAIL: tracked package census differs across declaration, HEAD, and index: research/partial_decide/zzz_consumer_probe.py [declaration=no, HEAD=yes, index=yes]
```

The exact replay, from repository root with a clean detached
`a1368cc48f64491ca1141b5b66d6239284140066`, is independent of that now-
unreachable commit object. `apply_patch` added this exact file:

```diff
*** Begin Patch
*** Add File: research/partial_decide/zzz_consumer_probe.py
+"""INJECTION: unlisted partial-Decide consumer for census diagnostics."""
*** End Patch
```

The remaining commands were:

```powershell
git add -- research/partial_decide/zzz_consumer_probe.py
git diff --cached --check
git commit -m "INJECTION: add unlisted partial decision consumer"
$env:PYTHONPATH = "<worktree>\code"
uv run --isolated --no-managed-python `
  --python C:\Users\a343o\AppData\Local\Python\pythoncore-3.14-64\python.exe `
  --with-requirements requirements.txt `
  python research/partial_decide/verify_pins.py
```

The commit command produced
`431d172bee890ae37fa7e5fabcadefa5e19f0fda`; the verifier command exited one
and printed exactly the `FAIL:` line above. Reversal and recovery used:

```powershell
git switch --detach a1368cc48f64491ca1141b5b66d6239284140066
# Repeat the identical PYTHONPATH and uv verifier command above.
```

The recovery verifier exited zero and printed receipt SHA-256
`87D2F5E8885B64797CDED3F6A2BF2688B7CED973760F7A881B0B5CA94D3FB127`
and `AuthorityEffect: None`.

After reversal, the custody worktree was clean at `a1368cc`, and its verifier
returned exit zero. The other two campaign worktrees ended clean at the
original exact baseline. The receipt remained `i/lf w/lf attr/-text`, and its
SHA-256 remained
`87D2F5E8885B64797CDED3F6A2BF2688B7CED973760F7A881B0B5CA94D3FB127`.
No receipt or source pin was regenerated while any probe was live.

### Integrated hardening review

At exact pre-repair head
`4869cb2c52f17e79813c79bd78828a8aaa07fe0e`, an independent detached review
found three accepted mutations in the then-current verifier: exchanging one
member between two L/mu1 classes, adding duplicate JSON names whose last value
carried an authorization claim, and adding
`statuses.g4_result = G4_HOLDS_UNDER_MU2`. The first preserved every count,
key shape, raw minimum, and disjoint-partition check; the other two crossed
otherwise closed schemas through Python's last-wins decoder or an open status
namespace.

The repaired gate now:

- independently replays and canonicalizes every retained member using only
  the already pinned derivation modules, after the production verifier has
  completed custody and runtime-origin checks;
- refuses duplicate object names at every external JSON decode, including
  nested names; and
- requires the exact inherited status-key set and exact G3/G4 values before
  checking the G3/G4 terminals and finite-G4 withdrawal. Other inherited
  status values are not reclassified as claims of this package.

The corresponding in-memory mutation tests are
`test_literal_receipt_contract_binds_members_to_canonical_classes`,
`test_json_decoder_rejects_root_and_nested_duplicate_keys`, and the status-
namespace arm of
`test_g3_g4_status_contract_rejects_drift_and_competing_terminals`. The tests
invoke small validators directly as injection checks; that direct invocation
is not a custody claim. Production semantic recomputation occurs in
`_verify` only after the custody/import/origin boundary. The receipt was not
regenerated and remains byte-identical.
