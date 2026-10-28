# Audit: CapacityBound

| field | value |
|---|---|
| Path | lean4/Derivation/CapacityBound.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 77c09cd79990c67a |
| Lines | 254 |
| Imported by root `Derivation.lean` | yes (line 52) |
| Imports | `Derivation.SeparationCapacity`, `Derivation.Pigeonhole` |
| Declarations | 3 def (`encode`, `colourBall`, `ViewLocal`), 10 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 8 lines: `encode_lt`, `encode_inj`, `colourBall_bounded`, `capacity_bound`, `capacity_at_one_colour`, `local_view_can_separate` (propext, Quot.sound); `colourBall_length` (propext); `local_view_blind` (none). Not in artifact: `encode_nil`, `encode_cons` |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The coloured separation-capacity bound. A colouring assigns to each index a colour below `k`; a view is *local* at radius `d` when its value at `i` is a function of the colours along the radius-`d` ball at `i` and of nothing else (`ViewLocal`). Then the number of distinguishable balls is at most `k^(2d+1)` — a function of radius and alphabet, not of chain length — and once the deep interior of a chain of length `n ≥ k^(2d+1) + 2d + 2` holds `B + 1` points, two distinct deep points have the same ball and so the same view (`capacity_bound`). The bound is derived by base-`k` encoding of the ball (injective at fixed length) and the choice-free pigeonhole. Two boundary fixtures keep the statement falsifiable: the one-colour degenerate end, and a two-colour radius-0 parity view at `n = 3`, below the threshold `4`, that separates every deep pair. The module answers the residual recorded in `contact/analysis/separation_capacity_open.md` §2–§4, including the trap that without locality the radius is inert and the result is ordinary pigeonhole.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `encode` | 59 | def | little-endian base-`k` encoding of a list of naturals | ADMITTED |
| `colourBall` | 131 | def | `(ball i d).map colour` — the colours along the radius-`d` index ball | ADMITTED |
| `ViewLocal` | 151 | def | `∃ g, ∀ i, v i = g (colourBall colour i d)` — the locality hypothesis | ADMITTED (declared hypothesis; load-bearing) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `encode_nil` | 63 | `encode k [] = 0` | FROZEN (rfl) | not in artifact | A |
| `encode_cons` | 65 | `encode k (x :: t) = x + k * encode k t` | FROZEN (rfl) | not in artifact | A |
| `encode_lt` | 70 | entries below `k` ⇒ `encode k l < k ^ l.length` | FROZEN | propext, Quot.sound | A |
| `encode_inj` | 90 | equal length, entries below `k`, equal encodings ⇒ equal lists | FROZEN | propext, Quot.sound | A |
| `colourBall_length` | 134 | `(colourBall colour i d).length = 2d + 1` | FROZEN | propext | A |
| `colourBall_bounded` | 139 | `(∀ x, colour x < k) → ∀ z ∈ colourBall colour i d, z < k` | CONDITIONAL:`∀ x, colour x < k` | propext, Quot.sound | A |
| `local_view_blind` | 156 | `ViewLocal v colour d → colourBall i = colourBall j → v i = v j` | CONDITIONAL:`ViewLocal` | none | S |
| `capacity_bound` | 178 | `(∀ x, colour x < k) → ViewLocal v colour d → k^(2d+1) + 2d + 2 ≤ n → ∃ i ≠ j, both deep (`d < i, i+d < n, d < j, j+d < n`), v i = v j` | CONDITIONAL:bounded colouring, `ViewLocal`, the threshold | propext, Quot.sound | S |
| `capacity_at_one_colour` | 212 | for `2d + 3 ≤ n`: ∃ distinct deep `i, j` with `(fun _ => 0) i = (fun _ => 0) j` | CONDITIONAL:`2d + 3 ≤ n` (conclusion's equality is trivial; the content is the deep pair) | propext, Quot.sound | A |
| `local_view_can_separate` | 227 | ∃ two-colour colouring and radius-0 local view with `1, 2` deep at `n = 3`, `3 < 4` (the threshold), `v 1 ≠ v 2`, and `v` separating every distinct deep pair | VERIFIED_FINITE (witness `x % 2`; `decide`/case split) | propext, Quot.sound | S |

## 4. External and admitted assumptions

- **The chain is nominal.** `capacity_bound`'s statement mentions neither `reflState` nor any chain structure: it is a statement about an arbitrary colouring `colour : Nat → Nat`, an index-local view, and the index range `d < i`, `i + d < n`. The docstring and ledger phrase the conclusion as "the deep interior of `reflState n` holds two distinct points"; that is a reading of the index range as the chain's carrier, correct because the chain's carrier is `0..n`, but the theorem would hold for any carrier indexed that way. See §11.
- **`ViewLocal` is existential over `g : List Nat → Nat`** and ranges over all of `Nat`; both `colour` and `v` are total functions on `Nat`, i.e. metatheoretic data (finitude flag: the "view" is a `Nat → Nat` function the system does not hold; the theorem is about such functions).
- `hk : ∀ x, colour x < k` bounds the colour at *every* natural, not just indices in the chain. Satisfiable for every `k ≥ 1`; at `k = 0` unsatisfiable, so the theorem is vacuous there (no prose reads it at `k = 0`).
- Library lemmas doing work: `Nat.mul_le_mul_left`, `Nat.mul_succ`, `Nat.pow_succ`, `Nat.one_pow`, `Nat.lt_trichotomy`, `Nat.mod_lt`, `List.mem_map`, `List.length_map`, `omega`, `decide`; `Pigeonhole.pigeonhole`; `SeparationCapacity.ball_length`.
- Unearned identity: none. Unrestricted external universe: none (all `Nat`). Unbounded function treated as internally available: `colour`, `v` (flagged above; the module's own header is explicit that these are arbitrary). Silently assumed observer: none — the locality hypothesis *is* the declared observer. Unspecified correspondence between presentations: none; the header disclaims any relation to `Generator.profile2`. Cost function: none. Admitted condition described as forced: none found — the header says locality is "what turns `B` from an ASSUMPTION into a CONSEQUENCE", which is accurate (the bound `k^(2d+1)` is computed, the locality is assumed). Finite computation presented as universal: none; the two fixtures are labelled.

## 5. Derived consequences

`LocalStrategy` opens this module: `ViewLocal` is the `locality` field of `LocalStrategy`, `colourBall`/`encode` build the `depthTwo` member, `capacity_bound` yields `strategy_capacity_collision` → `finite_local_not_clears` → `g1_local_finite_alphabet_class`; `G1Class` restates. Ledger owner: `CL-CAP-BOUND` (statement, non-claims, both fixtures). `CL-G1-T5-GENERAL` lists it as a dep. `code/derivation/completion.py` classifies `capacity_bound` as ("horizon-free", "countermodel") and `colourBall_length` as ("generic", "classification").

## 6. Counterexamples and limitations

- `local_view_can_separate` is the witness that the threshold does work: below it a local view can separate every deep pair (parity, `k = 2`, `d = 0`, `n = 3`).
- Not proved (and disclaimed in the header and ledger): tightness of `k^(2d+1)`; anything about non-local views; anything about `Generator.profile2`'s colouring specifically (that link is made only in `LocalStrategy.depthTwo`, where `profile1` is encoded as an 8-colour alphabet); a lower bound on the collision length.
- The header's last non-claim, "Nothing here bears on `LocalStrategy`, repair strategies, or absolute interior, none of which exist in this repository", is stale: `lean4/Derivation/LocalStrategy.lean` now exists and imports this module. The theorem content is unaffected. See §11.

## 7. Axiom dependencies

All eight reported theorems within `{propext, Quot.sound}` (`local_view_blind` uses none). None exceed: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). Eight of ten theorems in the artifact (the two `rfl` lemmas are not); `CL-CAP-BOUND` cites `capacity_bound`, `encode*`, `colourBall*`, `local_view_blind`, both fixtures. No probe run.

## 9. Related Python implementations

`code/derivation/local_strategy.py`: `ball`, `encode` ("the little-endian positional encoding from `CapacityBound`"), `LocalStrategy.colour_ball`, `LocalStrategy.view`, `capacity_threshold`, `capacity_collision` (bounded checks of the threshold and a collision pair); tests `tests/test_local_strategy.py`. `code/derivation/completion.py` / `tests/test_completion.py` classify the theorem names.

## 10. Textbook placement proposal

- Prerequisites: SeparationCapacity (`ball`, the deep interior); Pigeonhole (`pigeonhole`); positional encoding.
- Substantive: `ViewLocal` (as the definition of a bounded local observer), `local_view_blind`, `capacity_bound`, `local_view_can_separate` (as the falsifiability witness). Auxiliary: `encode*`, `colourBall_*`, `capacity_at_one_colour`.
- Lesson title: "How many things can a bounded window tell apart?" Question answered: with `k` colours and radius `d`, at most `k^(2d+1)`; so a long enough chain always has two deep points a local view cannot separate.
- Recommend omitting: `encode_nil`/`encode_cons` (definitional), `capacity_at_one_colour` (degenerate; one sentence suffices).

## 11. Interpretation findings

1. `capacity_bound` — docstring and `CL-CAP-BOUND`: "the deep interior of `reflState n` holds two distinct points that `v` does not separate". Lean: the statement contains no `reflState`; it quantifies over an arbitrary `colour : Nat → Nat` and index-local `v`, and concludes a collision among indices in `(d, n−d)`. The chain enters only as the name of the index range. Correct as applied (the chain's carrier is that range), but a student should be told the theorem is a fact about index-local functions on `Nat`, not about the successor relation. Classification: INTERPRETATION DEFECT (minor; the prose names an object the statement does not mention).
2. Header line 45–46: "Nothing here bears on `LocalStrategy`, repair strategies, or absolute interior, none of which exist in this repository." `LocalStrategy.lean` exists at this commit and consumes `capacity_bound`. Stale docstring; no theorem affected. Classification: INTERPRETATION DEFECT (minor, stale non-claim).
3. `capacity_at_one_colour` — conclusion `(fun _ => 0) i = (fun _ => 0) j` is trivially true; the theorem's only content is the existence of a deep pair, already `SeparationCapacity.depth_d_obstruction`'s. Docstring says "degenerate end … exhibited rather than assumed"; vacuity acknowledged. Not a defect.
4. Vacuity: `capacity_bound` at `k = 0` is vacuous (`∀ x, colour x < 0`); for `k ≥ 1` all hypotheses are jointly satisfiable (`local_view_can_separate` and `capacity_at_one_colour` exhibit instances). None found otherwise.
