# Audit: Pigeonhole

| field | value |
|---|---|
| Path | lean4/Derivation/Pigeonhole.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 61edcde0b75aa7bf |
| Lines | 232 |
| Imported by root `Derivation.lean` | yes (line 51) |
| Imports | none |
| Declarations | 1 def (`upto`), 12 theorems (one named `lemma`-style helper is a `theorem`) |
| Axiom reports in `artifacts/lean_axioms.txt` | 8 lines: `nodup_length_le`, `pigeonhole`, `map_nodup_of_inj`, `length_filter_split`, `upto_mem` (propext, Quot.sound); `nodup_filter_eq_le_one`, `filter_nodup` (propext); `upto_length` (none). Not in artifact: `nodup_head`, `nodup_tail`, `filter_eq_nil_of_none` |
| Forbidden tokens (sorry/admit/axiom) | none found (the header discusses the `Classical.choice` axiom in prose; the token scan pattern `^\s*axiom\s` is not triggered — not re-run here) |

## 1. Mathematical purpose

Metatheory apparatus, classified as such by its own header: a choice-free counting lemma (`nodup_length_le`: a duplicate-free list of naturals all below `B` has at most `B` entries) and the pigeonhole derived from it (`pigeonhole`: a map from `B + 1` indices into `B` values collides), both inside the audit gate `{propext, Quot.sound}`. It exists because the separation-capacity bound needed a pigeonhole and the obvious routes through `x == B` on `Nat` (`ReflBEq Nat`), `List.erase` lemmas and `List.nodup_range` pull in `Classical.choice` on this toolchain. It supplies no object-language notion; it licenses the counting step of `CapacityBound.capacity_bound`.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `upto` | 173 | def | the descending list `[n-1, …, 0]`, used in place of `List.range` because `List.nodup_range` is choice-dependent | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `nodup_head` | 51 | `Nodup (x :: t) → ∀ a ∈ t, x ≠ a` | FROZEN | not in artifact | A |
| `nodup_tail` | 56 | `Nodup (x :: t) → Nodup t` | FROZEN | not in artifact | A |
| `length_filter_split` | 63 | `(l.filter p).length + (l.filter (!p ·)).length = l.length` | FROZEN | propext, Quot.sound | A |
| `filter_eq_nil_of_none` | 81 | if `p` is false on every member, `l.filter p = []` | FROZEN | not in artifact | A |
| `filter_nodup` | 92 | filtering preserves `Nodup` | FROZEN | propext | A |
| `nodup_filter_eq_le_one` | 113 | a `Nodup` list of naturals has at most one entry equal to `B` (via `decide (x = B)`) | FROZEN | propext | A |
| `nodup_length_le` | 141 | `Nodup l → (∀ x ∈ l, x < B) → l.length ≤ B` | FROZEN | propext, Quot.sound | S |
| `upto_length` | 177 | `(upto n).length = n` | FROZEN | none | A |
| `upto_mem` | 183 | `x ∈ upto n → x < n` | FROZEN | propext, Quot.sound | A |
| `map_nodup_of_inj` | 193 | if `f` separates distinct indices below `n`, `(upto n).map f` is `Nodup` | FROZEN | propext, Quot.sound | A |
| `pigeonhole` | 215 | `(∀ p < B+1, f p < B) → ∃ p < B+1, ∃ q < B+1, p ≠ q ∧ f p = f q` (guarded binders; proof by `Decidable.byContradiction`) | FROZEN | propext, Quot.sound | S |

## 4. External and admitted assumptions

- Stated for `List Nat` and `f : Nat → Nat` only (header). Generic `α` appears in the list helpers.
- The decidability of the negated existential is what lets `Decidable.byContradiction` avoid choice; the docstring explains why the binders are guarded in that shape. Checked: the statement form at line 217 matches.
- Library lemmas doing work: `List.filter_cons`, `List.mem_filter`, `List.mem_map`, `List.mem_cons`, `List.length_map`, `of_decide_eq_true/false`, `decide_eq_false`, `Bool.noConfusion`, `omega`, `List.Pairwise.cons/nil` (Nodup destructed via `Pairwise`).
- Unearned identity / external universe / unbounded function as internal / silent observer / unspecified correspondence / cost function / admitted-as-forced / finite-as-universal: none found; the module makes no object-language claim.

## 5. Derived consequences

`CapacityBound.capacity_bound` consumes `pigeonhole` (and `upto`-free statement). `Rounds.lean` line 46 cites the module's finding about `List.nodup_range` in a comment. Ledger: `CL-CAP-BOUND` (supporting), and `pigeonhole` is mentioned by `CL-DI-PROPOSAL` and `CL-RP-PROGRESS` (the word, in the `DiffInterface`/represented-progress contexts — those cite `DiffInterface.bool_view_pigeonhole`, not this module; not checked further). `code/derivation/completion.py` classifies `Pigeonhole.pigeonhole` as ("generic", "existence").

## 6. Counterexamples and limitations

None are countermodels. The header's axiom-provenance analysis (`ReflBEq Nat` carries `Classical.choice`) is a toolchain measurement reported in prose; it was not re-measured in this audit (not checked).

## 7. Axiom dependencies

All eight reported theorems within `{propext, Quot.sound}`; `upto_length` uses none. The three unreported helpers are used only by reported theorems whose closures are clean, so they are clean too. None exceed: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). Eight of eleven theorems in the artifact; `CL-CAP-BOUND` cites `pigeonhole`; `contact/analysis/separation_capacity_open.md` §3 (the residual this closes) exists in the tree (content not read). No probe run.

## 9. Related Python implementations

None implement the lemma. `code/derivation/completion.py` lines 599 and `tests/test_completion.py` lines 85, 124 classify the theorem name; `code/derivation/represented.py` line 217 and `tests/test_represented.py::test_pigeonhole_progress_story` concern the `DiffInterface` pigeonhole story, not this module.

## 10. Textbook placement proposal

- Prerequisites: `List.Nodup` as `Pairwise (≠)`; `decide` vs `==`; why `Classical.choice` is barred.
- Substantive: `nodup_length_le`, `pigeonhole` (as the one counting fact the capacity bound rests on). Auxiliary: all others.
- Lesson title: "Counting without choosing." Question answered: how to prove pigeonhole for `Nat` inside `{propext, Quot.sound}`.
- Recommend omitting: everything but the two substantive statements and a one-paragraph note on the `ReflBEq Nat` trap; the module is apparatus.

## 11. Interpretation findings

None found. Vacuity: `pigeonhole` at `B = 0` has hypothesis `∀ p < 1, f p < 0`, unsatisfiable — the theorem is vacuous there and contentful for `B ≥ 1`; no prose reads it otherwise.
