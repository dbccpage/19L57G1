# Audit: IsoBridge

| field | value |
|---|---|
| Path | lean4/Derivation/IsoBridge.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | e667f5e55a1be362 |
| Lines | 75 |
| Imported by root `Derivation.lean` | no (parked: imported by `lean4/ParkedAudit.lean` line 11, listed in `parkedModules`; default target `ParkedAudit`) |
| Imports | Derivation.IsoCanon |
| Declarations | 1 def (`Iso.of_components`, Type-valued), 0 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 0 lines (the ParkedAudit census reports theorems only; this module has none). Probed: `Iso.of_components` propext, Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
IsoCanon's kernel needs two relabellings to coincide as regimes (as lists). `serialize` sorts instances, rules and requirements, so equal keys give relabellings equal only up to those sorts — equal as membership, not as lists. IsoBridge closes exactly that step: two regimes with the same datum count and the same form-arity list, and equal membership in instances, rules and requirements, are `Iso` via the identity maps, provided both requirement lists are ordered (the identity still sends `q` to `sortPair q`). The remaining list-combinatorial lemma (sorted-list equality ⇒ membership equality) is explicitly left to a key-definition unit.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `Iso.of_components A B hdata hforms hInst hRule hReq hAord hBord` | 37 | def (Type) | `Iso A B` with `dmap = dinv = fmap = finv = id` | ADMITTED (construction); CONDITIONAL on equal data, equal forms, membership-equal insts/rules/reqs, both requirement lists ordered |

## 3. Theorems and lemmas
None. (The def's fields are proofs: bounds by `hdata`/`hforms`, inverses `rfl`, `arity` by `hforms`, memberships by the iffs, `reqs_*` by `sortPair_of_le` plus the iff.) `#check` output recorded in probe2.lean confirms the signature.

## 4. External and admitted assumptions
- `Iso`, `sortPair_of_le` (IsoCanon), `List.mem_range`. Ordered requirements on both sides.
- Universe: none. `Nat → Nat` as data: `id` — metatheory.
- Unearned identity / unrestricted universe / unbounded internal function / silent observer / presentation correspondence (header names the unproved sorted-list lemma) / cost / admitted-as-forced / finite-as-universal: none found.

## 5. Derived consequences
No Lean module uses `of_components` (grep over `lean4/`: only this file and ParkedAudit's import). Paper 11 (line 985) cites "the partial canonical-key bridges of `IsoCanon.lean` and `IsoBridge.lean`".

## 6. Counterexamples and limitations
No countermodels. Not proved: the sorted-list-equality ⇒ membership-equality lemma; the composition with `iso_of_relabel_eq` into a single "equal key ⇒ `Iso`" statement; anything about `serialize` itself.

## 7. Axiom dependencies
`Iso.of_components` propext, Quot.sound (probe2.lean, exit 0). None exceed. Note: because the module has no theorems, the artifact and `ci/check_lean_audit.py` see nothing from it; its axiom footprint is checked only by hand (this probe).

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). Not in the artifact (no theorems). Paper 11 cites the file. Probe: `lake env lean …/probes/A/probe2.lean`, exit 0, `#print axioms Derivation.Iso.of_components` → propext, Quot.sound.

## 9. Related Python implementations
`code/derivation/iso.py::serialize` (the componentwise sorts), `::group_by_canonical`; tests `tests/test_iso.py::test_group_by_canonical_groups_and_preserves_order`.

## 10. Textbook placement proposal
- Prerequisites: IsoCanon.
- Substantive: `Iso.of_components` as the "same components, same regime" step. Auxiliary: none.
- Lesson title: "Order of listing is not structure". Question: why does `Iso` not care in which order instances are listed, and where does that leave the canonical key?
- Omit: nothing; one declaration.

## 11. Interpretation findings
- Header lines 26–27: "Parked module (not imported by `Derivation.lean`); axioms within `{propext, Quot.sound}`, verified by hand, not by the root gate." Accurate: with no theorems it has no artifact line at all, so "by hand" is the only check. none found (the by-hand check is reproduced above).
- Finitude: none found. Vacuity: hypotheses satisfiable with `A = B` and ordered requirements. none found.
