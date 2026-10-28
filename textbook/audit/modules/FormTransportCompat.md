# Audit: FormTransportCompat

| field | value |
|---|---|
| Path | lean4/Derivation/FormTransportCompat.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | e73539b0cddd03f0 |
| Lines | 23 |
| Imported by root `Derivation.lean` | no (parked: imported by `lean4/ParkedAudit.lean` line 9, listed in `parkedModules`; default target `ParkedAudit`). It cannot be root-imported: it begins with `import Derivation`, so the root importing it would be a cycle (lakefile comment, ParkedAudit header) |
| Imports | `Derivation` (the whole root), `Derivation.FormTransport` |
| Declarations | none |
| Axiom reports in `artifacts/lean_axioms.txt` | 0 lines (nothing to report) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
None. This file is an import-compatibility probe: it forces the root target and the parked module `Derivation.FormTransport` into one environment so that a name declared by the parked module that collides with a root declaration fails the per-module census build at the source rather than in some later downstream file. It re-exports (by transitive import) the root and FormTransport (and transitively FormRenaming); it declares nothing.

## 2. Definitions and structures
None.

## 3. Theorems and lemmas
None.

## 4. External and admitted assumptions
None of its own. Its existence presupposes the census policy described in `lean4/ParkedAudit.lean` (every module under `lean4/Derivation/` is elaborated; the twelve parked modules are named explicitly). Why it exists: the file's own header (lines 4–23) records the incident: an earlier `FormTransport` declared `Iso`, colliding with `Minimality.Iso` (root-imported), and the collision surfaced only under `import Derivation; import Derivation.FormTransport`; this file IS those two imports. `git log` at this checkout shows a single commit touching it (`ca30e30 2026-09-20 Merge pull request #225 … finish-c5-parked-trees`); the history before that squash is not available here. The header also notes that `Breaking` and `Composing` are not probed by a compat file (`Breaking` is not in this batch and was not checked; `Composing` indeed has no compat probe at this commit — confirmed against `parkedModules`).

## 5. Derived consequences
None. Nothing imports it except `ParkedAudit.lean`.

## 6. Counterexamples and limitations
None. The probe's scope is exactly the one module it names (and that module's transitive parked imports); it does not probe the other parked modules.

## 7. Axiom dependencies
None (no declarations).

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). Not in the artifact (nothing to report). Not cited by the paper. No probe needed.

## 9. Related Python implementations
none found (`ci/check_parked_audit.py` checks from the source tree that the parked list is complete; that is the nearest Python, and it is a gate, not an implementation).

## 10. Textbook placement proposal
Not textbook material. Mention once, in a note on how the parked modules are kept honest, under the ParkedAudit discussion.

## 11. Interpretation findings
Header: "Parked; no declarations, hence no axiom footprint." Accurate. none found.
