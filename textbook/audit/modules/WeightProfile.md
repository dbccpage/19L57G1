# Audit: WeightProfile

| field | value |
|---|---|
| Path | lean4/Derivation/WeightProfile.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | f0cc62611e0ad1ad |
| Lines | 522 (`wc -l`; inventory.json counts 523) |
| Imported by root `Derivation.lean` | yes (line 44; `#print axioms` inventory present) |
| Imports | `Derivation.Compression` — no identifier from namespace `Compression` is used in this file (grep: 0 hits for `Compression.`; no `open`). The import appears to serve build ordering only; not checked by removing it. |
| Declarations | 1 abbrev (`Weights`), 14 def (`CarrierList`, `total`, `SameProfile`, `Presents`, `sq`, `sqInt`, `SignedSquarePresents`, `mixSum`, `signedPlus`, `signedSplit`, `unitIntWeights`, `readOut`, `ModulusBlind`, `ClaimedReadOutUniqueness`), 31 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 31 lines (every theorem); axioms seen: `propext, Quot.sound`, `propext`, `none` |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

This module is a self-contained piece of finite `Nat`/`Int` arithmetic; it mentions neither the regime model of `Basic.lean` nor the passage state `PState`. Its object is a *declared* weight assignment — a count per label on a finite label list — and the question is what the normalized profile of such an assignment keeps and forgets, stated without division: two assignments have the same profile when they agree after cross-multiplying by each other's totals. On the positive-total domain this is an equivalence, positive scaling preserves it, and two assignments share a profile exactly when they lie on a common positive cross-multiple ("ray"); the profile keeps support and order and forgets the total. A "decorated presentation" (a declared map `m` and decoration `c` with `m ∘ c = w` on the carrier) adds nothing to the profile. Squaring is injective on naturals, so unsigned square presentations are determined on the carrier; over integers the square forgets a sign, and one declared two-input read-out `(x+y)^2` sees that sign at a two-label fixture. For a two-coordinate integer linear read-out followed by squaring, descent through coordinate-square fibers holds exactly when one coefficient is zero. The closing section audits a previously proposed "priced climb" toward a richer carrier and finds its rungs trivially inhabited, already theorems, or false. The module's own docstring and the write-up `paper/weight_profile_contact.md` insist that none of this derives a vector space, dynamics, or a representation theorem; the arithmetic is metatheory applied to admitted decorations.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `Weights` | 58 | abbrev | `Nat → Nat`, a declared count per label | ADMITTED (an unbounded function treated as a datum; every theorem reads it only on a finite list `l`) |
| `CarrierList` | 63 | def (Prop) | `l.Nodup`: the declared duplicate-free carrier policy | ADMITTED (declared policy) |
| `total` | 69 | def | `foldl (+) 0` of `l.map w` | ADMITTED |
| `SameProfile` | 125 | def (Prop) | `∀ p ∈ l, w p * total l v = v p * total l w` | ADMITTED |
| `Presents` | 273 | def (Prop) | `CarrierList l ∧ ∀ p ∈ l, m (c p) = w p` | ADMITTED (declared presentation) |
| `sq` | 312 | def | `x * x` on `Nat` | ADMITTED (declared modulus) |
| `sqInt` | 341 | def | `x * x` on `Int` | ADMITTED (declared fixture) |
| `SignedSquarePresents` | 344 | def (Prop) | duplicate-free carrier and `sqInt (c p) = w p` | ADMITTED |
| `mixSum` | 350 | def | `(x + y) * (x + y)` on `Int` | ADMITTED ("nothing forces this read-out; it is part of the fixture") |
| `signedPlus`, `signedSplit`, `unitIntWeights` | 352–356 | def | the fixture: `(1,1)`, `(1,-1)`, weights `(1,1)` | ADMITTED (finite witnesses) |
| `readOut` | 395 | def | `a * x + b * y` on `Int` | ADMITTED (declared linear read-out) |
| `ModulusBlind` | 398 | def (Prop) | `x*x = x'*x' ∧ y*y = y'*y'` | ADMITTED |
| `ClaimedReadOutUniqueness` | 480 | def (Prop) | the formerly proposed uniqueness schema, kept only to be refuted | ADMITTED (candidate claim) |

## 3. Theorems and lemmas

Abbreviations: **Pw** = `0 < total l w`; **Pv** = `0 < total l v`.

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `duplicate_list_not_carrier` | 65 | `[0, 0]` is not a `CarrierList` | VERIFIED_FINITE | propext | A |
| `foldl_add_acc` | 72 | `foldl (+) a l = a + foldl (+) 0 l` | FROZEN (metatheory) | propext, Quot.sound | A |
| `total_cons` | 82 | `total (p :: l) w = w p + total l w` | FROZEN | propext, Quot.sound | A |
| `total_append` | 95 | `total (l₁ ++ l₂) w = total l₁ w + total l₂ w` (repetitions counted) | FROZEN | propext, Quot.sound | S |
| `total_scale` | 101 | `total l (a * w) = a * total l w` | FROZEN | propext, Quot.sound | A |
| `total_ray` | 109 | pointwise `a * w p = b * v p` on `l` gives `a * total l w = b * total l v` | CONDITIONAL:pointwise ray on `l` | propext, Quot.sound | A |
| `profile_refl` | 128 | `SameProfile l w w` | FROZEN | none | A |
| `profile_symm` | 131 | symmetry, no positivity needed | FROZEN | none | A |
| `profile_trans` | 136 | transitivity, given `0 < total l v` (middle total) | CONDITIONAL:Pv | propext, Quot.sound | S |
| `profile_scale_raw` | 159 | `SameProfile l (a * w) w` for every `a`, zero included | FROZEN | propext, Quot.sound | A |
| `profile_scale_positive` | 168 | for `0 < a`, Pw: same profile and the scaled total is positive | CONDITIONAL:`0 < a`, Pw | propext, Quot.sound | S |
| `profile_equivalence_positive` | 177 | reflexivity, symmetry, transitivity packaged on the positive-total domain | CONDITIONAL:positive totals (only Pv used in the transitivity leg) | propext, Quot.sound | S |
| `zero_scale_boundary` | 191 | `SameProfile l 0 w`, `total l 0 = 0`, `¬ 0 < total l 0` (hypothesis `_hw : 0 < total l w` is unused) | FROZEN (the named hypothesis is not consumed) | propext, Quot.sound | S |
| `profile_iff_ray` | 206 | under Pw, Pv: `SameProfile l w v ↔ ∃ a b > 0, ∀ p ∈ l, a * w p = b * v p` | CONDITIONAL:Pw, Pv | propext, Quot.sound | S |
| `profile_support` | 236 | under Pw, Pv and same profile: `w p = 0 ↔ v p = 0` for `p ∈ l` | CONDITIONAL:Pw, Pv, SameProfile | propext, Quot.sound | S |
| `profile_order` | 256 | under the same: `w p ≤ w q ↔ v p ≤ v q` for `p, q ∈ l` | CONDITIONAL:Pw, Pv, SameProfile | none | S |
| `profile_forgets_total` | 286 | on `[0,1]`, doubling `(3,1)` keeps the profile and changes the total | VERIFIED_FINITE (witness) | propext, Quot.sound | S |
| `total_congr` | 277 | pointwise equal on `l` ⇒ equal totals | CONDITIONAL:pointwise equality | propext, Quot.sound | A |
| `presentation_profile_redundant` | 289 | `Presents l m c w → SameProfile l (m ∘ c) w` | CONDITIONAL:`Presents` (only its second conjunct is used) | propext, Quot.sound | S |
| `presentations_agree_on_profile` | 298 | two presentations of `w` with Pw have the same profile | CONDITIONAL:two `Presents`, Pw | propext, Quot.sound | S |
| `sq_mono` | 316 | `c < d → sq c < sq d` | CONDITIONAL:`c < d` | propext, Quot.sound | A |
| `sq_injective` | 326 | `sq c = sq d → c = d` on `Nat` | FROZEN | propext, Quot.sound | S |
| `unsigned_decoration_determined` | 334 | two `sq`-presentations of `w` agree pointwise on `l` | CONDITIONAL:two `Presents l sq _ w` (Nodup not used) | propext, Quot.sound | S |
| `signed_square_presentations_split` | 361 | `(1,1)` and `(1,-1)` both `SignedSquarePresents` weights `(1,1)` on `[0,1]`, differ at label 1, and `mixSum` separates them | VERIFIED_FINITE (two-label witness) | propext, Quot.sound | S |
| `presentation_scope` | 383 | packages redundancy, unsigned determination, and the signed split | CONDITIONAL:two `Presents l sq _ w` | propext, Quot.sound | A |
| `sq_mul` | 402 | `(x*y)*(x*y) = (x*x)*(y*y)` in `Int` | FROZEN (metatheory) | propext | A |
| `sq_add_sub` | 408 | `(a+b)² = (a−b)² + 4ab` in `Int` | FROZEN (metatheory) | propext, Quot.sound | A |
| `descent_iff_subsingleton_support` | 423 | `(∀ x y x' y', ModulusBlind → (readOut a b x y)² = (readOut a b x' y')²) ↔ a * b = 0` | FROZEN (over all `a b : Int`) | propext, Quot.sound | S |
| `decoratedCarrierShape_exists` | 465 | `∃ (D : Type) (m : D → Nat) (op), m surjective ∧ m (op d e) = m (op e d)` — inhabited by `Nat`, id, `+` | FROZEN (trivial witness; a `Type` existential in metatheory) | none | S (as audit) |
| `claimedReadOutUniqueness_false` | 489 | `¬ ClaimedReadOutUniqueness` (witness: the zero read-out on `[0]`) | REFUTED | propext, Quot.sound | S |
| `finite_scope_summary` | 503 | packages `profile_iff_ray`, `profile_scale_positive`, `presentation_profile_redundant` | CONDITIONAL:Pw, Pv, `0 < a` | propext, Quot.sound | A |

## 4. External and admitted assumptions

- **No system model.** Nothing from `PrimitivePassage`, `Basic`, or `Compression` is used. The module is arithmetic over `List Nat`, `Nat → Nat`, `Int`, and the Lean `Type` universe (one existential). It is metatheory about admitted decorations: the docstring says "A weight assignment is a DECLARED datum … Nothing in the passage calculus produces one", and no theorem relates a weight to a regime, context or observation.
- **Declared policies/fixtures.** `CarrierList` (duplicate-free), `sq`/`sqInt` (the modulus), `mixSum` and `readOut` (the read-outs), the signed fixture, the positive-total domain. All named as declared in the source and in `paper/weight_profile_contact.md`.
- **Recurring hypotheses.** `0 < total l w` / `0 < total l v`; `Presents`; `0 < a`.
- **Library lemmas doing real work.** `Nat.eq_of_mul_eq_mul_left`, `Nat.le_of_mul_le_mul_left`, `Nat.mul_eq_zero`, `Int.mul_eq_zero`, `Nat.mul_lt_mul_of_lt_of_le`, `ac_rfl`, `omega` (on `Nat` and `Int` linear goals, including the key step of `descent_iff_subsingleton_support` from `(a+b)² = (a−b)²` to `a*b = 0` via `sq_add_sub`), `List.Nodup` via `simp`, `decide`.
- **Finitude rule.** `Weights := Nat → Nat` is an unbounded function type used as a datum; every statement reads it only at members of a finite list `l`, so no totality over all labels is consumed. `Int` subtraction and squares are metatheoretic arithmetic on admitted integer decorations; the write-up says the word "ray" "abbreviates that displayed cross-multiple relation; it does not introduce a real vector space". `decoratedCarrierShape_exists` quantifies over `D : Type`; its purpose is to show a former existential was too weak, and it is not used as an internal carrier. `ClaimedReadOutUniqueness` quantifies over all `F : List Nat → Weights → Nat`; it is a candidate claim refuted by one witness. No docstring reads any of these as internally available to the system.
- **Admitted condition carried but never consumed.** `CarrierList l` inside `Presents` and `SignedSquarePresents` is not used by any proof (probe below). The write-up says carrier-facing claims "use" it; what is true is that the predicate includes it. Unused hypothesis also in `zero_scale_boundary` (`_hw`).
- Unearned identity: none found. Unrestricted external universe: the `Type` existential (above), labelled trivial by the source. Silently assumed observer: none (the read-outs are explicitly declared). Unspecified correspondence between presentations: none claimed; `presentations_agree_on_profile` is the proved relation. Cost function without justification: none. Admitted condition later described as forced: none found. Finite computation presented as universal: none found; `profile_forgets_total` and the signed split are stated as witnesses.

## 5. Derived consequences

- No Lean module imports `WeightProfile` (grep of `lean4/`; dependency graph lists no consumers). The root prints axioms for all 31 theorems.
- Ledger CL-PD2-WEIGHT-PROFILE ("corrected contact ceiling") cites 21 names; `paper/weight_profile_contact.md` is the write-up; `paper/paper.md` does not name the module; `paper/paper_change_log.md` records the renaming of "the forgotten total" to "total weight" and the removal of outside vocabulary (2026-08 entry near line 2470).
- Internally: `total_cons`/`total_congr`/`total_scale`/`total_ray` feed the profile theorems; `profile_trans` feeds `presentations_agree_on_profile`; `sq_add_sub` is the whole content of the forward direction of the descent classification.

## 6. Counterexamples and limitations

| theorem | what it refutes | witness |
|---|---|---|
| `duplicate_list_not_carrier` | "every list is a carrier" | `[0, 0]` |
| `zero_scale_boundary` | "scaling by zero is a positive-ray action" | the zero assignment |
| `profile_forgets_total` | "the profile determines the total" | `(6,2)` vs `(3,1)` on `[0,1]` |
| `signed_square_presentations_split` | "square presentations are determined" over `Int` | `(1,1)` vs `(1,-1)`, read-out `(x+y)²`: 4 vs 0 |
| `descent_iff_subsingleton_support` (→) | "every linear read-out descends through squares" | `ModulusBlind 1 1 1 (-1)` |
| `claimedReadOutUniqueness_false` | the proposed read-out uniqueness schema | `F = 0`, `l = [0]`, `w = 1` |

Not proved (and the source says so): any vector-space, inner-product, probability, dynamics or representation statement; that the sign is observable by any read-out other than `mixSum`; descent for more than two coordinates or non-linear read-outs; anything about where weights come from. The `CarrierList` policy has no theorem-level consequence in this module (see probe). `unsigned_decoration_determined` is pointwise agreement on `l`, not equality of the functions `c`, `d` off the carrier.

## 7. Axiom dependencies

All 31 artifact lines lie within `{propext, Quot.sound}`; `profile_refl`, `profile_symm`, `profile_order`, `decoratedCarrierShape_exists` report `none`. Probe re-confirmed `descent_iff_subsingleton_support`, `claimedReadOutUniqueness_false`, `profile_iff_ray` at `[propext, Quot.sound]`. None exceed the boundary.

## 8. Verification status

- Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0).
- Axiom artifact: 31/31 present.
- Ledger CL-PD2-WEIGHT-PROFILE cites `CarrierList`, `duplicate_list_not_carrier`, `total_append`, `profile_equivalence_positive`, `profile_scale_positive`, `zero_scale_boundary`, `profile_iff_ray`, `profile_support`, `profile_order`, `profile_forgets_total`, `presentation_profile_redundant`, `presentations_agree_on_profile`, `sq_injective`, `unsigned_decoration_determined`, `signed_square_presentations_split`, `presentation_scope`, `sq_add_sub`, `descent_iff_subsingleton_support`, `decoratedCarrierShape_exists`, `claimedReadOutUniqueness_false`, `finite_scope_summary`.
- Probe (`textbook/audit/probes/F1/wp_carrier_unused.lean`, run with `lake env lean` inside `lean4/`, exit 0): (a) the redundancy identity and unsigned determination re-prove by the same one-line proofs on the duplicated carrier `[0, 0]` with the `CarrierList` conjunct dropped — the Nodup policy is not load-bearing; (b) `zero_scale_boundary`'s first two conjuncts hold without its `_hw` hypothesis; (c) the three `#print axioms` above.

## 9. Related Python implementations

- `code/derivation/weight_profile.py`: `carrier_list`, `total`, `same_profile`, `scale`, `same_ray`, `all_weights`, `profile_report` (exhaustive check of equivalence/ray/support/order on carrier 2, weights to 3), `sq`, `presents`, `mix_sum`, `unsigned_decoration_determined`, `signed_mixing_separates`, `presentation_report`, `read_out`, `descends`, `descent_report` (coefficients to 3, inputs to 2), `climb_report`, `weight_profile_report`.
- `code/run_weight_profile.py` → `artifacts/weight_profile.json`.
- `tests/test_weight_profile.py`: `test_profile_algebra_exhaustive`, `test_profile_primitives`, `test_unsigned_square_determined_and_signed_fixture_scoped`, `test_descent_classification`, `test_climb_overclaims_are_classified`, `test_report_shape_and_bounds`, `test_runner_byte_stable`.

## 10. Textbook placement proposal

- Prerequisites: none from the system model; natural-number cross-multiplication, lists, and the programme's rule that declared data (weights, read-outs) are admitted, not derived.
- Substantive: `SameProfile` with `profile_trans` (why positivity is needed), `profile_iff_ray`, `profile_scale_positive` + `zero_scale_boundary`, `profile_support`/`profile_order`/`profile_forgets_total` (what the profile keeps and forgets), `presentation_profile_redundant`, `sq_injective` + `unsigned_decoration_determined` vs `signed_square_presentations_split` (the sign shadow), `descent_iff_subsingleton_support` with `sq_add_sub`, and `claimedReadOutUniqueness_false` as a worked refutation.
- Auxiliary: `foldl_add_acc`, `total_cons`, `total_scale`, `total_ray`, `total_congr`, `profile_refl/symm`, `profile_scale_raw`, `sq_mono`, `sq_mul`, `presentation_scope`, `finite_scope_summary`, `duplicate_list_not_carrier`.
- Suggested lesson: **"A profile without division"** — the one question: *what survives when a declared weight assignment is read only up to positive scale, and what does a square forget?* (Answer: support and order survive, the total does not; a natural square forgets nothing, an integer square forgets a sign that one mixing read-out can see.)
- Recommend omitting: `decoratedCarrierShape_exists` (its only content is that an earlier proposal was vacuous; mention in one sentence); `ClaimedReadOutUniqueness` as a definition (state the refutation directly); the import of `Compression` (unused). If the textbook keeps a "where this sits" note, it must say the module is arithmetic on admitted decorations with no bridge to regimes, contexts or observers.

## 11. Interpretation findings

1. **`paper/weight_profile_contact.md` §1 and `Presents` docstring** — "Carrier-facing claims use `CarrierList l := l.Nodup`"; "The duplicate-free carrier policy is part of the predicate." The policy is part of the predicate, but no theorem's proof consumes it (probe §8(a)): `presentation_profile_redundant`, `presentations_agree_on_profile`, `unsigned_decoration_determined`, `presentation_scope` all hold verbatim on duplicated carriers. Classification: INTERPRETATION DEFECT (minor): "use" suggests the policy does work; it is an admitted condition with no consequence in this module. The paper's own §1 sentence "they are never silently quotient-deduplicated" is correct.
2. **`zero_scale_boundary`** carries an unused hypothesis `_hw : 0 < total l w`; its docstring "exits the positive-total domain whenever the source total is positive" suggests the hypothesis matters. The conclusion is unconditional (probe §8(b)). Not a proof defect; recorded as a vacuous-hypothesis note.
3. **Docstring word "determined" (`unsigned_decoration_determined`, module header item 4: "an unsigned square presentation is determined on the declared carrier")** — the Lean quantifies: two `sq`-presentations of the same `w` agree at every `p ∈ l`. "On the declared carrier" matches; nothing is claimed off `l`. No defect.
4. **"EXACTLY" in `profile_iff_ray` and `descent_iff_subsingleton_support`** — both are biconditionals with the stated hypotheses (positive totals; `a b : Int` arbitrary). Checked; no overreading found.
5. **Ledger CL-PD2-WEIGHT-PROFILE**: "Unsigned square presentations of the same weights are carrierwise equal" — matches `unsigned_decoration_determined`. "two valid integer-square presentations `(1, 1)` and `(1, -1)` of weights `(1, 1)` are distinguished by the declared two-input read-out `(x+y)^2`" — matches the witness (values 4 and 0). "descent through coordinate-square fibers holds exactly when one coefficient vanishes" — matches. None found overreading.
6. **Vacuity check.** Positive-total hypotheses are satisfiable (`[0]`, `w = 1`); `Presents` is inhabited (`m = id`, `c = w`); `ModulusBlind` is reflexive so the descent universal is not vacuous. `claimedReadOutUniqueness_false` refutes a schema that is false already at the zero read-out, which the source states; the refutation is honest about being an inconsistency of the proposed schema rather than a deep result.
7. **Finitude flags.** `Weights : Nat → Nat` and `F : List Nat → Weights → Nat` in `ClaimedReadOutUniqueness` are unbounded function types; the docstrings treat them as declared data and as a candidate schema respectively, never as something the system holds. `decoratedCarrierShape_exists` ranges over `Type`; the docstring says it "says nothing about a distinguished representation". No defect; recorded under the standing rule.
