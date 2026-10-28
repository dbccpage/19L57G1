# Audit: Bridge

| field | value |
|---|---|
| Path | lean4/Derivation/Bridge.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 5dc42aed7ee99c2a |
| Lines | 316 |
| Imported by root `Derivation.lean` | yes (line 17) |
| Imports | `Derivation.Basic`, `Derivation.Erasure`, `Derivation.PrimDiff` |
| Declarations | 4 def (`SingleTok`, `AtMostTok`, `hist01`, `hist10`), 1 `Decidable` instance (for `SingleTok`), 12 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 11 lines; axioms seen: none / `propext, Quot.sound`. `exists_not_of_not_ball` is **not in artifact** (probe: no axioms) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module asks whether the opaque inscription of the regime model (one supplied, then admitted, token) can be elaborated into the witnessed irreflexive datum that `PrimDiff` identified as the strongest primitive-difference candidate, and if not, which of its six ingredients — carrier, two designated occurrences, relation, witness, irreflexivity, orientation — must be admitted from outside. It is the one module that deliberately imports both the token-aware admission model (`TRegime`, `stepT`, `replayT`, `TRegime.erase` from `Erasure`) and the primitive-difference layer. For each ingredient it gives a provenance theorem or countermodel: under the deduplicating admission discipline a single token never yields two admitted data; two-ness needs a datum admission with a second token; forms arise only from form admissions and instances presuppose forms; positive facts never entail the irreflexivity law; a swap-equivariant irreflexive inhabited relation on the two-point carrier is `S2`, never `D2`; and admission order is visible in the token list but erased by token erasure. The header's rule is "no gap is filled silently": wherever the metatheory could supply an ingredient (positions, supply order, token identity) the module states that as a theorem about the metatheory and flags it as invisible to the object language.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `SingleTok t0 e` | 32 | def | every datum admission in `e` carries token `t0` (`∀ tok, e = admitDatum tok → tok = t0`) | ADMITTED |
| `AtMostTok t0 t` | 37 | def | `t.tokens = [] ∨ t.tokens = [t0]` | ADMITTED (invariant) |
| (instance) | 114 | instance | `Decidable (SingleTok t0 e)` by cases on the event | ADMITTED (auxiliary) |
| `hist01` | 289 | def | `[supply 0, admitDatum 0, supply 1, admitDatum 1]` | ADMITTED (concrete history) |
| `hist10` | 293 | def | the same two tokens admitted in the other order | ADMITTED (concrete history) |

The module relies on the imported declared policy `stepT` (`Erasure.lean` 40–59): `admitDatum tok` is a no-op when `tok ∈ t.tokens` (deduplication), `admitForm a` requires `1 ≤ a`, `admitInst f args` requires `f < t.forms.length`, matching arity and in-range arguments, and `supply` is always a no-op.

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `stepT_preserves_atMostTok` | 40 | if `AtMostTok t0 t`, `SingleTok t0 e` and `stepT t e = some t'` then `AtMostTok t0 t'` | CONDITIONAL:`AtMostTok t0 t`, `SingleTok t0 e` (and the dedup `stepT`) | propext, Quot.sound | A |
| `single_token_carrier_bound` | 91 | for any history `h` all of whose datum admissions carry `t0`, any start `t` with `AtMostTok t0 t`, and `replayT h t = some res`: `res.tokens.length ≤ 1` | CONDITIONAL:`∀ e ∈ h, SingleTok t0 e`, `AtMostTok t0 t`; rests on the deduplicating `stepT` | propext, Quot.sound | S |
| `exists_not_of_not_ball` | 128 | for a list `l` and decidable `P`: `¬ (∀ x ∈ l, P x) → ∃ x ∈ l, ¬ P x` | FROZEN (generic list lemma; needs `[DecidablePred P]`) | not in artifact (probe: none) | A |
| `second_token_required` | 149 | for any `t0`, history `h` replayed from the empty token-aware regime to `res` with `2 ≤ res.tokens.length`: some `e ∈ h` is `admitDatum tok` with `tok ≠ t0` | CONDITIONAL:`replayT h ⟨[],[],[],[],[]⟩ = some res`, `2 ≤ res.tokens.length`; rests on dedup `stepT` | propext, Quot.sound | S |
| `no_admitForm_no_forms` | 177 | if no event of `h` is an `admitForm`, `t.forms = []` and `replayT h t = some res`, then `res.forms = []` | CONDITIONAL:`∀ e ∈ h, ∀ a, e ≠ admitForm a`, `t.forms = []` | propext, Quot.sound | S |
| `no_forms_no_witness` | 220 | if `t.forms = []` then `stepT t (admitInst f args) = none` for all `f`, `args` | CONDITIONAL:`t.forms = []` (one step; a property of the declared `stepT` guard) | propext, Quot.sound | S |
| `irrefl_law_not_entailed` | 230 | for any `r : α → α → Prop` and any `a : α` there is `r' ⊇ r` (pointwise) with `¬ Irrefl r'` (witness: `r ∪ {(a,a)}`) | FROZEN (requires an element `a : α`) | none | S |
| `equivariant_witness_is_S2` | 244 | if `S` on `Bool` is swap-invariant, `Irrefl S`, and `S false true ∨ S true false`, then `S x y ↔ S2 x y` for all `x y` | CONDITIONAL:swap-invariance, `Irrefl S`, inhabited off-diagonal | none | S |
| `equivariant_not_D2` | 267 | under the same three hypotheses, `¬ (∀ x y, S x y ↔ D2 x y)` | CONDITIONAL:same | none | S |
| `no_swap_fixed_offdiag_pair` | 281 | `∀ x y : Bool, x ≠ y → (not x, not y) ≠ (x, y)` | VERIFIED_FINITE (`decide`); hypothesis `x ≠ y` unused, see §11 | none | S |
| `order_visible_to_metatheory` | 301 | `replayT hist01 empty ≠ replayT hist10 empty` (token lists `[0,1]` vs `[1,0]`) | VERIFIED_FINITE (`decide`) | propext, Quot.sound | S |
| `order_erased_at_object_level` | 311 | the two replays have equal `TRegime.erase` images | VERIFIED_FINITE (`decide`) | propext, Quot.sound | S |

## 4. External and admitted assumptions

- **Declared policy doing the work:** the deduplicating `stepT` from `Erasure.lean` ("the Python semantics: re-admitting a present token designates the existing datum"). `single_token_carrier_bound` and `second_token_required` are theorems *about that discipline*; the paper records this (`paper/refusal_difference.md` R6: "proved for the dedup discipline; the reifying disciplines escape it by being different declared disciplines") and names the alternative `occurrence` discipline, which reaches carrier 2 from one token at the price of a position import (bridge paper B4, declared not formalised). The textbook must not present "one inscription never gives two" as discipline-independent.
- **Tokens are `Nat`.** Token identity, equality and the ordered token list are metatheoretic data. `order_visible_to_metatheory` says exactly this ("a metatheoretic orientation exists for free") and `order_erased_at_object_level` that erasure removes it. Finitude flag: the "first-admitted / second-admitted" orientation lives in a `List Nat`, not in the object language; the module flags the import rather than using it. No defect.
- **Universe parameter** `{α : Type}` and an arbitrary relation in `irrefl_law_not_entailed`; the theorem needs an inhabitant `a : α` (supplied as an argument). The relation `r` is not assumed finite despite the docstring's "finite facts".
- **Decidability** `[DecidablePred P]` in `exists_not_of_not_ball` and the `Decidable (SingleTok t0 e)` instance: used to avoid `Classical.choice` when producing the witness in `second_token_required`. Admitted condition, harmless (events have `DecidableEq`).
- **Library lemmas doing work:** `Option.some.inj`, `List.mem_cons_of_mem`, `List.mem_cons_self`, `replayT_cons` (Erasure), `of_decide_eq_true/false`, `omega`. `decide` evaluates `replayT` on two concrete four-event histories.
- Unearned identity: none found. Unrestricted external universe: `α` in one theorem, harmless. Unbounded function treated as internally available: none found. Silently assumed observer: none found. Unspecified correspondence between presentations: the `supply`/`admitDatum` pairing is the regime model's own; the module does not assume it beyond `stepT`. Cost function without justification: none in Lean (the paper's "four admissions / five admissions" counts are Python, scoped to the 7-event horizon). Admitted condition later described as forced: see §11 (dedup discipline). Finite computation presented as universal: the paper's "only the self-edge witness is single-token reachable" is Python-only to horizon 7 and is listed as `[unresolved]` in B9; the Lean theorems are horizon-free but weaker. No defect.

## 5. Derived consequences

Downstream Lean references are citations in docstrings only: `RefusalFrontier.lean` lines 259 and 272 cite `irrefl_law_not_entailed` and `equivariant_witness_is_S2`; `ContactKernel.lean` lines 494–495 cite `no_swap_fixed_offdiag_pair` and `equivariant_not_D2` as the "already native" obstruction transported to the observer side. No theorem of `Bridge` is used as a term in another module (grep of `Bridge.` across `lean4/Derivation`). Paper: `paper/bridge_provenance.md` B2–B8 (owner), `paper/native_derivation_map.md` rows "seed ⇒ two-ness FALSE", "two-ness ⇒ witnessed relation FALSE", "irreflexivity fact ⇒ law FALSE", `paper/refusal_as_difference.md` 296, `paper/refusal_difference.md` 161. Ledger: `CL-PD2-PACKET-02R` cites `no_swap_fixed_offdiag_pair` and `equivariant_not_D2`; the dependency graph lists no citing claim for the other ten theorems (they are owned by the bridge paper, which has no `CL-` entry of its own that I found — "not checked" beyond grep of the ledger for `Bridge.` and `bridge_provenance`).

## 6. Counterexamples and limitations

- `irrefl_law_not_entailed`: witness `r' = r ∪ {(a,a)}`; refutes "an irreflexive fact set entails the irreflexivity law" in the sense that the law is not preserved by extension in the bare signature.
- `second_token_required`: contrapositive of the carrier bound; its conclusion is "some admitted token differs from `t0`" for an arbitrary `t0`, which is slightly stronger than "a second token different from the first admitted".
- `order_visible_to_metatheory` / `order_erased_at_object_level`: the pair `hist01`, `hist10`.
- `equivariant_not_D2`: `D2` fails swap-invariance.
- Not proved: that the self-edge is the only single-token-reachable witness (Python to horizon 7; `[unresolved]` B9); anything about the `occurrence` discipline (not modelled in Lean); any statement about automorphism groups beyond the swap on `Bool`; that a weaker external act than a second token could purchase two-ness (alphabet does not contain such acts).
- `no_forms_no_witness` is one step only; combined with `no_admitForm_no_forms` it covers histories, but the paper's "no witness ever exists" is the two theorems together plus the fact that `insts` grow only through `admitInst` (true of `stepT`, not separately stated here).

## 7. Axiom dependencies

All 12 within `{propext, Quot.sound}` (11 in the artifact; `exists_not_of_not_ball` probed: no axioms). None exceed: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). Eleven theorems are in `artifacts/lean_axioms.txt` and in the root inventory; `exists_not_of_not_ball` is not (it is an unnamed helper in the paper). Paper cites all eleven. Probe `textbook/audit/probes/B/p2.lean` (`lake env lean`, exit 0): `example : ∀ x y : Bool, (Bool.not x, Bool.not y) ≠ (x, y) := by decide` succeeds (the off-diagonal hypothesis is unnecessary); `#print axioms Bridge.exists_not_of_not_ball` → none; `#check` of `second_token_required` confirms the universal `t0`; `#eval replayT hist01/hist10 empty` → `tokens := [0, 1]` and `tokens := [1, 0]` respectively.

## 9. Related Python implementations

`code/derivation/bridge.py`: `event_alphabet`, `occurrence_step`, `StateClass`, `classify`, `reachable_states`, `scenario_report` (scenarios `single_dedup`, `two_dedup`, `occurrence`, 7-event horizon), `equivariant_scan`, `provenance_table`; artifact `artifacts/bridge.json`. Tests `tests/test_bridge.py`: `test_single_token_never_reaches_two_or_witnessed_pair`, `test_second_token_unlocks_the_target`, `test_occurrence_discipline_matches_two_token_milestones`, `test_equivariant_scan_unique_winner_is_symmetric`, `test_provenance_table_covers_all_ingredients`, and others. The token-aware step itself is `code/derivation/model.py` (dedup admission).

## 10. Textbook placement proposal

- Prerequisites: the regime model's events and the token-aware replay (`Erasure`: `TRegime`, `stepT`, `replayT`, `erase`); `PrimDiff`'s `Irrefl`, `D2`, `S2`; the idea of a declared admission discipline.
- Substantive: `single_token_carrier_bound` with `second_token_required` (two-ness is purchased), `no_admitForm_no_forms` + `no_forms_no_witness` (the relation channel is a separate purchase), `irrefl_law_not_entailed` (law vs fact), `equivariant_witness_is_S2` + `equivariant_not_D2` (orientation cannot be introduced equivariantly), the order pair `order_visible_to_metatheory` / `order_erased_at_object_level`. Auxiliary: `stepT_preserves_atMostTok`, `exists_not_of_not_ball`, `no_swap_fixed_offdiag_pair` (fold into the equivariance discussion).
- Lesson title: "What one inscription cannot buy." Question answered: which of the six ingredients of a witnessed irreflexive oriented pair can be reached from a single admitted token under the deduplicating discipline, and which are external admissions or declarations.
- Recommend omitting: `no_swap_fixed_offdiag_pair` as a named result (its content is "the swap on `Bool × Bool` has no fixed point", the off-diagonal qualifier does nothing; teach it as a remark inside `equivariant_not_D2`); `exists_not_of_not_ball` (library-grade helper).

## 11. Interpretation findings

1. `no_swap_fixed_offdiag_pair` — docstring/paper B4: "No ordered off-diagonal pair on the two-element carrier is fixed by the swap: an equivariant *designation* of an ordered pair does not exist. Unordered two-ness is swap-invariant; orientation is not." Lean: `∀ x y : Bool, x ≠ y → (not x, not y) ≠ (x, y)`. The hypothesis `x ≠ y` is unused — `(not x, not y) ≠ (x, y)` holds for every pair, diagonal included (probe §8). So the theorem does not single out off-diagonal pairs, and the contrasting clause "unordered two-ness is swap-invariant" is not stated anywhere in Lean. The statement proved is correct; the prose attributes to it a contrast it does not make. Classification: INTERPRETATION DEFECT (minor).
2. `single_token_carrier_bound` / `second_token_required` — bridge paper B7 table: "carrier (size 2): **not derivable** from one inscription"; `native_derivation_map.md`: "seed ⇒ two-ness FALSE". Lean: proved for histories replayed by the deduplicating `stepT`, whose `admitDatum` of a present token is a no-op. The paper itself scopes this (B1 scenarios; `refusal_difference.md` R6 "proved for the dedup discipline"), and the B7 table lists "declared occurrence discipline importing metatheoretic position" as the alternative. No defect, but a textbook sentence "a second token is required" must carry "under deduplicating admission". Recorded as a scope condition, not a defect.
3. `irrefl_law_not_entailed` — docstring: "Any irreflexive fact set has a bare-signature extension with a self-edge: finite facts never entail the irreflexivity law." Lean: for *any* relation `r` (irreflexive or not, finite or not) on an inhabited `α`, some superset relation has a self-edge. The theorem is more general than the prose and its "entailment" is extension-closure in the bare signature, not a proof-theoretic entailment. Not a defect; the paper's B5 reading ("the law is a declaration, never a derivation") is a gloss on this. Noted.
4. `no_forms_no_witness` — docstring: "no witness ever exists". Lean: one failed `admitInst` step from a state with empty form table. "Ever" is earned only together with `no_admitForm_no_forms` and the fact that `stepT` never adds forms except on `admitForm` (true, visible in `Erasure.lean`, but not a stated lemma). Classification: INTERPRETATION DEFECT (minor; the docstring's temporal universal is the conjunction of two theorems plus an unstated property of `stepT`).
5. Vacuity: `second_token_required` with `t0` arbitrary is satisfiable and non-trivial; `equivariant_witness_is_S2`'s three hypotheses are jointly satisfiable (by `S2`); nothing vacuous found.
6. Finitude: tokens as `Nat` and histories as `List TEvent` are metatheory; the module says so itself ("flagged as invisible to the object language"). No defect.
