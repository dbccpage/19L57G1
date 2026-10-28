# Audit: SeparationCapacity

| field | value |
|---|---|
| Path | lean4/Derivation/SeparationCapacity.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | f4d2ff5b0948f2c7 |
| Lines | 238 |
| Imported by root `Derivation.lean` | yes (line 21) |
| Imports | `Derivation.Generator` |
| Declarations | 2 def (`ball`, `profileD`), 14 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 14 lines (every theorem); `ball_length`: propext; the other 13: propext, Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The generator module showed that depth-1 observation of the reflective chain is outrun by growth and exhibited two depth-2 instances (`n = 4` separates the near-end pair, `n = 5` has an interior collision). This module generalises the structural half to every fixed graph radius `d`: on the chain `reflState n`, the radius-`d` structural profile of a point is the list of depth-1 profiles along the ball `[i-d, …, i+d]`, and for every point deep enough in the interior (`d < i`, `i + d < n`) that list is the constant interior profile. Hence any two deep points collide (`depth_d_outrun`), and a colliding deep pair exists exactly from `n = 2d + 3` (`depth_d_obstruction`). It also fixes the radius convention — the sealed `profile2` observes a radius-ONE ball — and proves, for every chain length and every interior pair, that sealed depth-2 equality and radius-one `profileD` equality are the same relation (`radius_one_agrees_with_sealed_depth2`, T5), then carries the two sealed instances across that correspondence. The coloured capacity bound and the class-relative repair consequence are in `CapacityBound` and `LocalStrategy`.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `ball` | 84 | def | `(range (2d+1)).map (fun k => i - d + k)` — the unclipped (Nat-subtraction) radius-`d` index ball around `i` | ADMITTED (declared observation window; on the deep interior no clipping occurs) |
| `profileD` | 93 | def | `(ball i d).map (profile1 (reflState n))` — the radius-`d` structural profile, built from the sealed `profile1` | ADMITTED (declared regime) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `filter_range_decide_eq` | 42 | `(range n).filter (· = i) = if i < n then [i] else []` | FROZEN | propext, Quot.sound | A |
| `filter_range_succ_eq` | 62 | for `0 < i ≤ n`: `(range n).filter (·+1 = i) = [i-1]` | CONDITIONAL:`0 < i`, `i ≤ n` | propext, Quot.sound | A |
| `filter_range_eq` | 76 | for `i < n`: `(range n).filter (· = i) = [i]` | CONDITIONAL:`i < n` | propext, Quot.sound | A |
| `ball_length` | 87 | `(ball i d).length = 2d + 1` | FROZEN | propext | A |
| `profileD_deep` | 99 | for `d < i`, `i + d < n`: `profileD n i d` is the constant list of `(true,true,true)` of length `2d+1` | CONDITIONAL:`d < i`, `i + d < n` | propext, Quot.sound | S |
| `depth_d_outrun` | 119 | for deep `i, j` (`d < i, i+d < n, d < j, j+d < n`): `profileD n i d = profileD n j d` | CONDITIONAL:deepness of both points | propext, Quot.sound | S |
| `depth_d_obstruction` | 127 | for `2d + 3 ≤ n`: ∃ distinct deep `i, j` with equal radius-`d` profiles (witness `d+1`, `d+2`) | CONDITIONAL:`2d + 3 ≤ n` | propext, Quot.sound | S |
| `incoming_edges_interior` | 143 | for `0 < i ≤ n`: the in-edges of `i` in `reflState n` are exactly `[(i-1, i)]` | CONDITIONAL:`0 < i`, `i ≤ n` | propext, Quot.sound | A |
| `outgoing_edges_interior` | 151 | for `i < n`: the out-edges of `i` are exactly `[(i, i+1)]` | CONDITIONAL:`i < n` | propext, Quot.sound | A |
| `profile2_interior` | 159 | for `0 < i < n`: `profile2 (reflState n) i = (profile1 i, [profile1 (i-1)], [profile1 (i+1)])` | CONDITIONAL:`0 < i < n` | propext, Quot.sound | A |
| `profileD_radius_one` | 169 | for `0 < i`: `profileD n i 1 = [profile1 (i-1), profile1 i, profile1 (i+1)]` | CONDITIONAL:`0 < i` | propext, Quot.sound | A |
| `radius_one_agrees_with_sealed_depth2` | 181 | for interior `i, j` (`0 < i < n`, `0 < j < n`): `profile2 i = profile2 j ↔ profileD n i 1 = profileD n j 1` | CONDITIONAL:both interior | propext, Quot.sound | S |
| `radius_one_agrees_with_sealed_depth2_n5` | 201 | the iff over interior indices `1..4` of `reflState 5` (by `decide`), and the pair `(2,3)` carried from `Generator.depth2_obstruction_n5` | VERIFIED_FINITE | propext, Quot.sound | S |
| `radius_one_agrees_with_sealed_depth2_n4` | 224 | the iff over interior indices `1..3` of `reflState 4` (by `decide`), `profileD 4 1 1 ≠ profileD 4 3 1` carried from the sealed separation, and the arithmetic fact that `(1,3)` is not a deep pair at radius one | VERIFIED_FINITE (third conjunct: `omega`) | propext, Quot.sound | S |

## 4. External and admitted assumptions

- Inherits `reflState`, `profile1`, `profile2`, `middle_profile`, `reflective_chain_successor_relation` from `Generator`/`RefusalFrontier`; everything is about the sealed chain, not a private mirror (docstring, and the definitions confirm it).
- **Radius convention is declared** in the header: `d` is graph radius; sealed "depth k" is radius `k−1`. This is a reading, made into a typed correspondence only at radius one (`radius_one_agrees_with_sealed_depth2`); no general "depth k ↔ radius k−1" theorem exists for `k > 2`, and none is claimed.
- **`ball` uses truncated subtraction.** Near the left end (`i < d`) the ball is clipped silently to start at 0 with repeated… no: `i - d + k` with `i - d = 0` gives `[0, …, 2d]`, a *shifted* window, not a clipped one. All theorems guard with `d < i` (or `0 < i` at radius one), so nothing is asserted about the shifted case. Flag for the textbook: `profileD` off the guarded range is not the ball one would draw.
- **Quantification** over `n, i, j, d : Nat` is metatheoretic. "Horizon-free" (docstring) means the statement has no bound on `n` beyond deepness; it does not make the family of chains a system-held totality.
- Library lemmas doing work: `List.range_succ`, `List.filter_append`, `List.filter_map`, `List.map_map`, `List.map_congr_left`, `List.mem_range`, `Nat.sub_add_cancel`, `Nat.lt_trichotomy`, `omega`, `funext` (in `filter_range_succ_eq`, to rewrite the predicate), `decide` on `reflState 4/5`.
- Unearned identity: none found. Unrestricted external universe: none. Unbounded function treated as internally available: `profileD : Nat → Nat → Nat → List …` is metatheoretic bookkeeping over the chain (flag only). Silently assumed observer: the regime is declared. Unspecified correspondence between presentations: the radius-one correspondence is proved; higher radii are left as a stated reading. Cost function: none. Admitted condition described as forced: none found — the threshold `2d + 3` is derived (docstring says so, and the proof shows it as the least `n` with two deep points). Finite computation presented as universal: the two `_n4`/`_n5` theorems are finite and labelled as such; the general theorem is separate. No defect.

## 5. Derived consequences

`CapacityBound` opens this module (`ball`, `ball_length` for `colourBall`); `LocalStrategy` opens it (uses `middle_profile`, `depth1_obstructions_are_exactly_middle_pairs` via `Generator`; `profileD` not used directly); `G1Class` through `LocalStrategy`. `Rounds.lean` only mentions `Pigeonhole.lean` in a comment. Ledger: `CL-G1-T5-GENERAL` (owner of `radius_one_agrees_with_sealed_depth2` and the seven helpers); `depth_d_outrun`/`depth_d_obstruction` have no `CL-` entry naming them (not checked: whether `CL-CAP-BOUND`'s deps or `paper/endogenous_generator.md` §G2 cite them by name — the paper's T5 section does). Python receipt `code/derivation/g1_class_receipt.py` pins `SeparationCapacity.profileD_radius_one` and the T5 reports; `code/derivation/completion.py` classifies `profileD_radius_one`.

## 6. Counterexamples and limitations

- `depth_d_obstruction` refutes "radius-`d` observation repairs the chain" for every fixed `d` (structural, uncoloured). `radius_one_agrees_with_sealed_depth2_n4`'s third conjunct explains why the separated pair `(1,3)` at `n = 4` is not a counterexample to `depth_d_outrun`: it is not deep.
- Not proved: anything about coloured views (`CapacityBound`); any statement for a ball that is not deep; tightness of `2d + 3` as the least colliding length for every regime (it is the least `n` with two deep points, and the proof exhibits a collision there — so for the structural profile the threshold is attained; a *lower* bound "no collision below" is not stated); the correspondence between sealed depth `k` and radius `k−1` for `k > 2` (no sealed `profile3` exists).
- The paper's earlier sentence that the general-`n` correspondence remained OPEN is WITHDRAWN by `CL-G1-T5-GENERAL` (and in `g1_class_receipt.py`). The `Generator` record (§6, §11 item 5) was written from the generator write-up, which still carries that residual in its G2 paragraph; the withdrawal is in the later T5 section of the same file. Both are recorded here.

## 7. Axiom dependencies

All 14 within `{propext, Quot.sound}`. None exceed: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 14 theorems are in `artifacts/lean_axioms.txt`; `CL-G1-T5-GENERAL` cites eight by name and `paper/endogenous_generator.md` (T5 section, 2026-08-26) cites the correspondence; `depth_d_outrun`/`depth_d_obstruction` are cited in the generator write-up's G2 paragraph. No probe run.

## 9. Related Python implementations

`code/derivation/local_strategy.py`: `ball` (docstring: "Lean's fixed-length natural-number ball `i - d + k`"; note the Python clips with `max(0, i - radius)`, which equals Lean's truncated subtraction), `profile_code`, `_depth_two_factor`; `code/derivation/g1_class_receipt.py` binds the T5 axiom reports; `code/derivation/completion.py` classifies `profileD_radius_one`; tests `tests/test_local_strategy.py`, `tests/test_g1_class_receipt.py`, `tests/test_completion.py` (classification). No Python mirror of `depth_d_outrun` for general `d` found beyond the strategy ball code.

## 10. Textbook placement proposal

- Prerequisites: Generator FG2–FG3 (the three profile classes, `middle_profile`); the notion of a radius ball and a structural profile; truncated subtraction on `Nat`.
- Substantive: `profileD_deep`, `depth_d_outrun`, `depth_d_obstruction`, `radius_one_agrees_with_sealed_depth2`, and the two carried instances (as the bridge from the sealed depth-2 facts). Auxiliary: the three `filter_range_*` lemmas, `ball_length`, the two edge lemmas, `profile2_interior`, `profileD_radius_one`.
- Lesson title: "Looking farther does not help: the radius-`d` outrun." Question answered: can any fixed radius of structural observation keep up with the growing chain? No — from length `2d + 3` two deep points look identical.
- Recommend omitting: the three `filter_range_*` lemmas and `profile2_interior`/`profileD_radius_one` as separate items (fold into one sentence: "on an interior point the depth-2 record is exactly the three neighbouring depth-1 profiles").

## 11. Interpretation findings

1. `depth_d_obstruction` — docstring: "The threshold is derived, not assumed — it is exactly the least `n` at which the deep interior holds two distinct points." Lean: `2d + 3 ≤ n → ∃ colliding deep pair`. The docstring's "least" is a remark about the deep-interior count, not a proved minimality of the collision length; no theorem states that below `2d + 3` there is no colliding pair for the structural profile (there cannot be a *deep* pair, but non-deep pairs are outside the statement). Not a defect; a scope note.
2. Header: "Identity-grade observation outside that declared class, absolute interior, and 'no outside' remain outside this module's statement language." Accurate; recorded.
3. The `ball` shift near the left end (truncated subtraction) is never visible because every theorem guards it; a reader of `profileD` alone could misread `profileD n 0 d`. Not a defect.
4. Vacuity: all hypotheses satisfiable (e.g. `d = 1, i = 2, n = 5`); none vacuous. None found beyond the notes above.
