# Derivation audit

AuthorityEffect: None. One row per group of declarations: what it depends
on, whether it is admitted or derived, its carrier, which quantifiers and
function types it uses that belong to Lean rather than to the system
("metatheory"), the smallest model that shows its bound or refutes its
negation, and where the Python model reproduces it. The second table lists
every admission the tree makes or inherits, with its price, where one exists.

## Finitude audit

| Declarations | Depends on | Admitted / derived | Carrier | Metatheory used | Smallest model | Python |
|---|---|---|---|---|---|---|
| `Joint.knows_family_iff_joint`, `knows_joint_idem` | `pQ_exact` (sealed), `knows_iff_determined` (TT), `Inst.sigEq_single` (AI) | derived | any `D : List Nat` | `F : List (Nat → Nat)`, `q : Nat → Nat`; a function is read on `D` only (TT-41) | — (an equivalence) | `model.l0_check` |
| `sepCount`, `redundancy` and its lemmas, `knows_iff_redundancy` | `exists_separator_of_not_sigEq` (sealed), `Nat.decEq` | definitions derived (list recursion); lemmas derived | pairs `x y : Nat`, read on `D` in `knows_iff_redundancy` | `Nat → Nat` seats | — | `model.redundancy` |
| `duplicate_counts_twice`, `duplicate_knows_inert` | `knows_mono` (TT) | derived | any `D` | — | one seat listed twice | — |
| `Robust.Repl`, `Del` | — | admitted grammar: replacement and deletion, one constructor per seat | lists of seats | the replacing presentation `m'` ranges over every `Nat → Nat` (metatheory); `k : Nat` is a count | — | positions and Boolean tables in `model.l1_check` |
| `repl_*`, `del_*`, `redundancy_le_repl`, `redundancy_le_del`, `blunt`, `agreeing`, `sigEq_blunt`, `sigEq_agreeing` | `omega` on `Nat` | derived | lists of seats | — | — | — |
| `robust_iff`, `deletion_robust_iff` | the above, `knows_iff_determined` | derived | any `D` | `∀ Q'` and `∀ K` range over all lists of functions: a metatheory quantifier. The necessity direction exhibits one finite family (`blunt` or `agreeing`), built from `Q` and constants | at `k = 0` both are `knows_iff_redundancy` (`repl_zero`) | `model.l1_check` |
| `robustB`, `robustB_iff`, `robust_parity_half` | `List.all_eq_true`, `decide` | derived (closed computation for the witness) | `[0, 1, 2, 3]` for the witness | — | the witness is the four-point family of TT `institution_exceeds_members` | `model.examples` |
| `Staleness.add_preserves`, `knows_congr_mem` | `knows_mono` (TT) | derived | any `D` | `M : Institution` | — | `model.l2_add_and_target_check` |
| `removal_iff`, `seat_corruption_iff`, `relabel_of_kept`, `sigEq_append_consts` | `knows_iff_redundancy`, `redundancy_append`, `List.eq_of_mem_replicate` | derived | any `D` | `∀ R'` over lists of functions and `∀ σ : Nat → Nat`: metatheory; necessity uses one list of constants | `removal_count_not_necessary`: two points, two seats | `model.l2_removal_check` |
| `removal_count_not_necessary`, `relabel_can_be_harmless`, `relabel_can_break`, `swap02`, `swap12` | `decide` | derived (closed computation) | `[0, 1]`, `[0, 1, 2, 3]` | — | the relabelling witnesses use the plan's four-point family; no smaller one is claimed | `model.examples` |
| `extension_iff`, `extension_breaks` | `knows_iff_determined` | derived | `D ++ [x]`; the witness on `[0, 2] ++ [1]` | — | a smaller instance, not proved here: `[0] ++ [1]` with the empty family and the identity question; the witness uses a nonempty seat | `model.l2_extension_check` |
| `target_member_preserves`, `decision_holds_target_fails` | `knows_mono`, `Chain.agreement_known_of_admitted` (AI) | derived | any `D`; `[0, 1]` for the witness | the target `t : Nat → Nat` is metatheory until seated | a smaller instance, not proved here: one point, the constant 0 against the constant target 1 | `model.l2_add_and_target_check` |
| `Ballot.knows_of_known_members`, `ballots`, `mem_ballots`, `ballot_known`, `ballot_compression`, `uniform_ballot_compression` | `knows_comp`, `knows_member` (TT) | `ballots` admitted (pairing in order, stopping at the shorter list); theorems derived | any `D` | ballot maps `fs : List (Nat → Nat)`: metatheory | — | `model.l3_check` (nine maps per seat) |
| `tallyOf`, `tally_known`, `tally_compression` | `knows_iff_sigList` (TT) | definition admitted; theorems derived | any `D` | `List.count` on `Nat` | — | `model.l3_check` (sincere part) |
| `settledAt`, `sincere`, `settledAt_eq`, `settledAt_congr`, `sincere_known`, `sincere_compression` | `List.all_eq_true`, `knows_iff_determined` | `sincere` admitted as the reading of a sincere ballot; theorems derived | any `D` | — | — | `model.sincere`, `model.l3_check` |
| `xorPH`, `ballot_loses_exceeding`, `injective_ballot_keeps` | `decide`, `Inst.Exceeds` (AI) | derived (closed computation) | `[0, 1, 2, 3]` | — | exceeding needs three points (AI-02, AI-03); whether ballots lose it on three points is not checked; the four-point witness is the one the plan names | `model.examples` |

Hidden totalities looked for and not found. Every carrier is a list. Every
`∀` over presentations, families, replacements, relabellings or ballot maps is
a Lean quantifier about tables read on a finite list, and every necessity
proof exhibits one finite family built from the given seats and constants.
Lean's `Nat` is never a carrier. No observer is assumed: the institution is
its list of seats; the "rule that sees only ballots" of L3 is the ballot
family itself, and what it can know is `Knows` of that family. The model is
silent outside its bound: four points, Boolean seats, at most three seats.

## Admissions

| Admission | Where | Priced? |
|---|---|---|
| Seats are list positions: a repeated presentation is two seats | `redundancy`, `Repl`, `Del` | unpriced; the effect is IF-02, and the source-level count it replaces is IF-15o |
| Replacement grammar: at most `k` seats, each replaced by any presentation | `Robust.Repl` | the count `k` is the only cost; no price per seat is attached |
| Deletion grammar | `Robust.Del` | the count `k` only |
| Shared carrier: every seat reads the same datum at the same index | inherited from AI-04 (`correspondence_matters`) | unpriced in both trees |
| Ballot values NAY `0`, AYE `1`, ABSTAIN `2` | `Ballot` | a reading only; no theorem depends on the values |
| The sincere ballot rule | `Ballot.sincere` | unpriced; a definition, not derived from anything |
| A target `t` as a seat | `Staleness.target_member_preserves`; AI-09 | price: one seat, as in AI-09 ("the price of truth is admitting the target") |
| `ScopedSound` (a rule authorizes only known claims) | AI-13, not used here | **unpriced**. Its only price is its name. The plan's WP0 asked that it be priced or recorded as unpriced; it is recorded here as unpriced (IF-17o) |
| The probe grammar of acquisition | AI-16, not used here | 1 per probe (AI) |
| A mandate or jurisdiction grant | not represented in this tree or in AI | — (`CROSSWALK.md`, authorization row) |
