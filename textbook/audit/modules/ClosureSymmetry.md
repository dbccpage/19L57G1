# Audit: ClosureSymmetry

| field | value |
|---|---|
| Path | lean4/Derivation/ClosureSymmetry.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | f1fcba4787d9b409 |
| Lines | 166 |
| Imported by root `Derivation.lean` | yes (line 55) |
| Imports | Derivation.PresentationRelativity |
| Declarations | 1 structure (`InternalSymmetryBreak`), 3 defs (`transpose`, `residual_to_internal_symmetry_break`, `internal_symmetry_break_to_residual`), 7 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 7 lines; axioms seen: `propext` (4 transposition lemmas, `residual_nonempty_iff_…`), `Quot.sound` (`residual_refutes_factorization`), `propext, Quot.sound` (`closure_failure_iff_internal_symmetry_break`) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module re-reads a factorization failure between two internal faces `p, q : Nat → Nat` of one attempted closure on a represented finite domain `D` as a loss of invariance under an internal symmetry. A directional residual (a represented pair identified by `p` and separated by `q`, from PresentationRelativity) generates the transposition of its two points; that involution preserves `D` and leaves `p` invariant, but `q` is not invariant under it at the residual's left point. Conversely any represented involution preserving `D` and `p` but moving `q` at some represented point reconstructs a residual. Hence "`q` does not factor through `p` on `D`", "a residual exists" and "an internal symmetry of `p` breaks `q`" are one statement. No evaluator, observer or preferred repair is introduced: the symmetry is built from the failed fiber itself.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `transpose a b x` | 31 | def | Swap `a` and `b`, fix everything else (on `Nat`). | ADMITTED |
| `InternalSymmetryBreak D p q` | 73 | structure (Type) | A map `symmetry : Nat → Nat`, involutive, preserving `D` and `p` on `D`, plus a `point ∈ D` with `q (symmetry point) ≠ q point`. | ADMITTED (declared form of "internal symmetry break"; its `symmetry` is any ambient `Nat → Nat` satisfying the laws, not only a transposition) |
| `residual_to_internal_symmetry_break r` | 87 | def | From a `DirectionalResidual D p q` build the break with `symmetry := transpose r.left r.right`, `point := r.left`. | ADMITTED (construction; content is in the field proofs) |
| `internal_symmetry_break_to_residual b` | 122 | def | From a break build the residual `(b.point, b.symmetry b.point)`. | ADMITTED (construction) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `transpose_left` | 35 | `transpose a b a = b`. | FROZEN | propext | A |
| `transpose_right` | 39 | `transpose a b b = a` (case `a = b` handled). | FROZEN | propext | A |
| `transpose_fixed` | 46 | `x ≠ a → x ≠ b → transpose a b x = x`. | FROZEN | propext | A |
| `transpose_involutive` | 50 | `transpose a b (transpose a b x) = x` for all `x`. | FROZEN | propext | A |
| `residual_nonempty_iff_internal_symmetry_break_nonempty` | 134 | `Nonempty (DirectionalResidual D p q) ↔ Nonempty (InternalSymmetryBreak D p q)`. | FROZEN | propext | S |
| `residual_refutes_factorization` | 146 | A `DirectionalResidual D p q` implies `¬ FactorsOn D p q`. | FROZEN | Quot.sound | A (duplicate in substance of `PresentationRelativity.directionalResidual_refutes_identity`'s first half) |
| `closure_failure_iff_internal_symmetry_break` | 158 | `¬ FactorsOn D p q ↔ Nonempty (InternalSymmetryBreak D p q)`. | FROZEN | propext, Quot.sound | S |

## 4. External and admitted assumptions

- From PresentationRelativity: `DirectionalResidual`, `directionalResidual_of_factorization_failure` (which supplies the forward direction via a `decide` over the list-bounded existential); from Compression: `FactorsOn`, `factors_iff_fiberConstant`.
- `p q : Nat → Nat` and `symmetry : Nat → Nat` are ambient functions (finitude rule); all conditions are restricted to `x ∈ D`, so the content is finite. The docstrings say "represented domain", "represented involutive symmetry"; the `symmetry` field itself is unrestricted off `D` (e.g. `transpose a b` acts on all of `Nat`). Flagged: nothing in the prose reads the symmetry as a system-internal operation beyond `D`.
- Unearned identity: none found.
- Unrestricted external universe: none found (no `Type` fields).
- Unbounded function treated as internally available: the `symmetry : Nat → Nat` field (above) — a reading hazard only; the equivalence theorem shows a transposition always suffices.
- Silently assumed observer: none found; the header insists none is primitive.
- Unspecified correspondence between presentations: none found.
- Cost function: none.
- Admitted condition later described as forced: none found.
- Finite computation presented as universal: none found.
- Library lemmas doing real work: `simp [transpose]` with `if` reduction (source of `propext`); `by_cases` on `Nat` equality (decidable); `Ne.symm`.

## 5. Derived consequences

- `ResidualClosure` imports this module and uses `InternalSymmetryBreak`, `residual_refutes_factorization`, `closure_failure_iff_internal_symmetry_break`.
- No other module under `lean4/Derivation/` references `InternalSymmetryBreak`, `ClosureSymmetry.`, or `InvariantUnderOn` (grep; the word `transpose` in `BoundaryCancellation`, `ContactKernel`, `ObserverInventory` refers to their own local definitions).
- Paper: ledger CL-CLOSURE-SYMMETRY; `native_derivation_completion.md` ~lines 365–375; `endogenous_generator.md` ~lines 241–247; change log 2026-08-14 "Closure failure as loss of internal symmetry invariance". Not cited in `paper/paper.md`.

## 6. Counterexamples and limitations

- `residual_refutes_factorization` is the countermodel-shaped direction: a residual witnesses non-factorization.
- The equivalence is on a finite common carrier `List Nat` only; no heterogeneous or infinite-domain version (ledger non-claim).
- `InternalSymmetryBreak` admits symmetries other than transpositions; the module proves only that *some* break exists iff a residual does, not that every break is a transposition (probe: a transposition-based break on `D = [0,1,2]`, `p` constant, `q = id` typechecks; a 3-cycle would not be involutive, but a product of two disjoint transpositions would qualify — not checked).
- Nothing selects a repair or a preferred face; the symmetry is relative to the supplied `p`, `q`, `D`.

## 7. Axiom dependencies

All within {propext, Quot.sound}: `propext` from `simp`/`if`, `Quot.sound` inherited from `factors_iff_fiberConstant`. None exceeds.

## 8. Verification status

- Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0).
- All seven theorems are in `artifacts/lean_axioms.txt`; the ledger cites "the seven `ClosureSymmetry.*` theorem reports".
- Probe: `textbook/audit/probes/F2/cs_qr_probe.lean`, exit 0: `closure_failure_iff_internal_symmetry_break` depends on `[propext, Quot.sound]`; a concrete `InternalSymmetryBreak [0,1,2] (fun _ => 0) id` with `symmetry := transpose 0 1`, `point := 0` was constructed; and `r.left ≠ r.right` for every `DirectionalResidual` was checked (so the generated transposition is never the identity).

## 9. Related Python implementations

- `code/derivation/completion.py` lines 740–749: tag bindings for the seven theorem names; `tests/test_completion.py` pins them. No Python computes transpositions or symmetry breaks for this notion.

## 10. Textbook placement proposal

- Prerequisites: `FactorsOn`, `DirectionalResidual`, `forced_split_of_factorization_failure` (PresentationRelativity); involutions on `Nat`.
- Substantive: `closure_failure_iff_internal_symmetry_break` and `residual_nonempty_iff_internal_symmetry_break_nonempty`, taught with the explicit construction `residual_to_internal_symmetry_break` (the transposition of the failed pair).
- Auxiliary: the four `transpose_*` lemmas, `residual_refutes_factorization`, `internal_symmetry_break_to_residual`.
- Suggested lesson: "What does a failed comparison look like from inside?" — answering: it is a swap of two represented points that one face cannot see and the other can.
- Recommend omitting: `residual_refutes_factorization` as a separate item (it restates `PresentationRelativity.directionalResidual_refutes_identity`'s content for `FactorsOn`).

## 11. Interpretation findings

1. Ledger CL-CLOSURE-SYMMETRY: "failure of `FactorsOn D p q` is equivalent to the existence of a represented involution σ that preserves `D` and `p` but under which `q` is not invariant at a represented point." Lean: exactly `closure_failure_iff_internal_symmetry_break`; σ is any `Nat → Nat` with those four laws, not required to be a transposition. The ledger's second sentence ("constructs σ as the transposition") describes the forward witness correctly. None found.
2. Change log line ~1664 "identifies failed factorization, represented residual, and symmetry loss": the three-way identification is `closure_failure_iff…` plus `residual_nonempty_iff…`; the second `↔` is between `Nonempty` types, so it identifies *existence*, not the data (several residuals can give one break and vice versa). The header line 16 says "contain the same represented obstruction data" — slightly stronger than a `Nonempty ↔ Nonempty`, since no bijection of witnesses is proved. INTERPRETATION DEFECT (minor wording in the module header; the ledger says "identifies the residual and symmetry-break forms", which is accurate at the level of existence).
3. Vacuity: hypotheses satisfiable (probe instance); on `D = []` both sides of `closure_failure_iff…` are false, consistent. None found.
