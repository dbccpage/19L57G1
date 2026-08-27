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

The machine-readable record is `partial_decide_c3.json`. Every class member
is retained. No field names a representative, selected delta, authorized
delta, or transition to apply.

## Panel and authorization boundary

The existing `certNeg` and `PanelEquiv` results are panel-relative. Within this
tree and its pinned import surface, their indices are not connected to the
engine's admitted-data indices by a declared carrier/pair correspondence. This
tree therefore records:

```text
PANEL_TO_ENGINE_LINK_NOT_DEFINED
NO_PANEL_ENGINE_ADAPTER
NO_DECISION_INPUT_SELECTION
NO_RESPONSE_AUTHORIZATION
NO_RESPONSE_APPLICATION
NO_OBJECT_LANGUAGE_EVENT
```

A panel may motivate a separately declared request supplied to `decide`; it
cannot choose the engine regime, pair, reading, measure, bounds, quotient
member, or response. Absence of that correspondence is not encoded as the
function's `None` result. The absence statement is a scoped source audit: the
verifier enforces package custody and import syntax but does not recognize
every possible semantic adapter.

## Explicit nonclaims

- No candidate or demand is generated.
- No new requirement or admission event is derived.
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
literal C3 receipt contract, receipt transport policy, complete package
custody, and byte-identical receipt regeneration. The documented writer uses
that verified isolated renderer and refuses to write when its custody
preflight fails. These are syntactic/provenance checks; they do not recognize
every possible semantic adapter.

Python necessarily starts `verify_pins.py` (or the small writer entry point)
before that file can check its own Git custody. No partial-Decide consumer or
derivation module is parsed or executed until the verifier's early custody
preflight succeeds; the running verifier, standard library, Git executable,
and parsed pin JSON are the explicit bootstrap boundary.

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

The following independent campaign was run from detached worktrees at
`a9aef3090d37a79434eaf053168407a46fa7be4e`. Each committed probe has that
commit as its parent. Every named verifier failure exited one; the type probe
made mypy exit one. The relevant check returned exit zero after every reversal.

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
| committed an unlisted consumer | `758ec430baaa946177a5948676f4049a4d86333f` | `tracked package census differs across declaration, HEAD, and index` |
| added an uncommitted type-invalid consumer | worktree-only | mypy reported the incompatible assignment and checked six rather than five source files |
| changed the receipt transport attribute from `-text` to `text` | `80ddae268710c4d0a5be671ad254cfa7b4fa6944` | `receipt transport attribute must be committed as -text` |
| committed the receipt with CRLF bytes under `-text` | `5e1eb4b2ac42e06f565272b55130bbe9dd9819b9` | `partial_decide_c3.json contains CR bytes` |

All three campaign worktrees ended clean at the exact baseline. The final
verifier and mypy runs exited zero, the receipt remained `i/lf w/lf attr/-text`,
and its SHA-256 remained
`87D2F5E8885B64797CDED3F6A2BF2688B7CED973760F7A881B0B5CA94D3FB127`.
No receipt or source pin was regenerated while any probe was live.
