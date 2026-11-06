# institution_forces

AuthorityEffect: None. Outside the seal. Consumes the sealed `Derivation`
package (the `Compression` namespace, through the two trees below), the
`two_theorems` tree and the `actor_institution` tree, read-only
(`lean/lakefile.toml` requires `../../../lean4`, `../../two_theorems/lean`
and `../../actor_institution/lean`), and changes nothing in any of them.
Every consumed name (`Institution`, `Knows`, `knows_iff_determined`,
`knows_mono`, `knows_comp`, `knows_member`, `pQ`, `pQ_exact`, `SigEq`,
`sigList`, `parity`, `half`, `Inst.Exceeds`, `Inst.sigEq_single`,
`Chain.Corr`, `Chain.agreeQ`, `Chain.agreement_known_of_admitted`) is used
as merged.

Question (the operator's work packages WP0 and the Lean half of WP4, plan of
2026-11-06, approved by the author the same day): fix the finite core
vocabulary used by the plan, prove the lemma that
makes "an actor is a family of presentations" and "an actor is one
presentation" agree (L0), and prove the three results the plan's
institution design rests on: robustness against replaced seats (L1), when a
decision goes stale (L2), and what ballots lose against pooled observations
(L3). Where the plan's wording was wrong, the corrected statement is proved
and the plan's reading is recorded as REFUTED with its witness.

## Vocabulary

The objects are those of `two_theorems` and `actor_institution`; see their
READMEs. This tree adds four.

| Word | Object here | Status |
|---|---|---|
| seat | one position of the list `Q : Institution` | admitted reading: a list position, so a repeated presentation is two seats |
| separation redundancy | `redundancy Q x y`: the number of seats `m` of `Q` with `m x ≠ m y`, by list recursion | derived definition |
| replacement of at most `k` seats | `Robust.Repl k Q Q'`: same length, one constructor per seat, at most `k` of them `swap` (a swapped seat may receive any presentation) | admitted grammar |
| deletion of at most `k` seats | `Robust.Del k Q K` | admitted grammar |
| ballot | `Ballot.ballots fs Q`: seat `m` with map `f` casts `f ∘ m`; NAY `0`, AYE `1`, ABSTAIN `2` | admitted reading of the values; the theorems hold for any values |
| sincere ballot | `Ballot.sincere D q m`: AYE or NAY where `q` is settled on the seat's class, ABSTAIN elsewhere | derived definition |

## Results

**L0 (`Joint.knows_family_iff_joint`).** `Knows D F q ↔ Knows D [pQ D F] q`.
The proof is the one the plan gave: `pQ_exact` makes the one-member family of
the joint presentation merge exactly what `F` merges, and `Knows` depends
only on that (`knows_iff_determined`). The information side,
`classCount D [pQ D Q] = information D Q`, is `two_theorems`'
`institution_is_actor` and is not repeated.

**Redundancy.** `knows_iff_redundancy`: `Q` knows `q` exactly when every
pair `q` separates has at least one separating seat. A duplicated
separating presentation counts twice (`duplicate_counts_twice`) while
knowledge does not change (`duplicate_knows_inert`). So redundancy counts
seats, not sources: if two seats copy one source, a captured source moves
both, and the seat count overstates robustness against that capture
(`IF-15o`).

**L1 (`Robust.robust_iff`).** Every `Q'` obtained from `Q` by replacing at
most `k` seats knows `q` exactly when every pair of `D` that `q` separates has
at least `k + 1` separating seats. Both directions are proved; necessity
replaces each separating seat of the weak pair by the constant `0`
(`blunt`). `deletion_robust_iff` gives the same threshold for deleting at
most `k` seats. `robustB` computes the condition and `robustB_iff` proves it
correct. On four points `[parity, half]` knows the identity with robustness
0; duplicated, with robustness 1 (`robust_parity_half`).

**L2 (`Staleness`).** A decision is `Knows D Q q`.

- (a) adding seats never breaks it (`add_preserves`);
- (b) the kept seats `K` of `K ++ R` know `q` exactly when every
  `q`-separated pair keeps a separating seat in `K` (`removal_iff`); the
  decision survives every replacement of the seats `R`, relabellings
  included, exactly when `K` alone knows `q` (`seat_corruption_iff`,
  `relabel_of_kept`);
- (c) given the decision on `D`, it holds on `D ++ [x]` exactly when `q` is
  constant on the signature class of `x` in `D ++ [x]` (`extension_iff`);
- (d) `Knows` has no target argument, so declaring a target changes nothing;
  admitting the target `t` as a seat never breaks the decision and makes
  agreement with `t` known (`target_member_preserves`), and a decision can
  hold while failing its target (`decision_holds_target_fails`).

Each force that can break a decision does so on a small witness:
`actor_institution`'s `consensus_after_loss` (removal), `relabel_can_break`
and `actor_institution`'s `correspondence_matters` (relabelling),
`extension_breaks` (carrier extension), `decision_holds_target_fails`
(target). So a decision record needs re-review on removal, relabelling,
carrier extension and a newly admitted target, and never on an added seat
alone.

**L3 (`Ballot`).** `ballot_compression`: with one ballot map per seat, what
the ballots know the seats know. `uniform_ballot_compression` is the case of
one map for all seats; `tally_compression` says a rule that sees one tally
knows at most what the ballots know; `sincere_compression` covers sincere
ballots, which `sincere_known` shows are ballots of their seats. The
converse fails (`ballot_loses_exceeding`): on four points `[parity, half]`
knows `xorPH` (parity of `parity + half`) while neither seat does; both
sincere ballots on `xorPH` are ABSTAIN everywhere, and the ballots know only
the constants. An injective ballot map loses nothing there
(`injective_ballot_keeps`), so the loss comes from what a sincere ballot
reports, not from the number of ballot values. In the finite model every
case in which sincere ballots lose a Boolean question the seats know is a
case in which no single seat knows it (IF-13c).

## Statement corrections against the plan

1. **L2 (b), relabelling.** The plan says relabelling a seat (F3) preserves a
   decision "iff the L1 condition holds for the members affected". For the
   worst case over all relabellings this is `seat_corruption_iff` (the kept
   seats alone must know `q`). For one particular relabelling it is false:
   `relabel_can_be_harmless` relabels `parity` by the swap of 0 and 2, a
   bijection; the decision on the identity survives although `half` alone
   does not know it. `relabel_can_break` relabels by the swap of 1 and 2 and
   the decision fails. Recorded as IF-08r, REFUTED.
2. **L2 (b), removal.** "L1 with `k` set to the affected members", that is,
   at least `|R| + 1` separating seats per pair, is sufficient for every
   removal of `|R|` seats and necessary only when every such removal is
   quantified over (`deletion_robust_iff`). For a particular removal the
   exact condition is `removal_iff`; `removal_count_not_necessary` is a
   two-point witness. Recorded in IF-07.
3. **L3, the witness.** The plan says "any ballot map that is constant on a
   member's classes loses exceeding knowledge". Every ballot `f ∘ m` is
   constant on the classes of `m`, and `injective_ballot_keeps` is one that
   loses nothing, so the sentence is false as written. The proved witness is
   the sincere ballot on `xorPH`. Recorded as IF-13r, REFUTED.
4. **L2 (d).** "Admitting a truth target never changes `Knows`" holds for a
   target that is declared and not seated, by the definition of `Knows`, which
   has no target argument; that is a remark, not a theorem. Admitted as a
   seat, the target can change what is known, only upward
   (`target_member_preserves`).

The plan's L0 and L1 hold as stated and are proved as stated. The plan's
section 3.3 says its paper proofs are complete; for L1 and L0 they are, and
the Lean proofs follow them.

## Outside the system

Everything in Lean here is metatheory about finite tables, as in the two
consumed trees. `Nat → Nat`, the quantifiers `∀ Q'`, `∀ K`, `∀ R'`, `∀ σ`
and `∀ fs` over lists of functions, and the index `k` are the metatheory's;
the system at any point holds a finite carrier, a finite list of seats, and
the tables of the seats on the carrier. The replacements in L1 and L2 range
over every presentation in Lean and over the 16 Boolean tables in the model;
the necessity proofs use only constants. `AUDIT.md` lists every admission
and whether it carries a price.

## Layout and how to run

```
research/institution_forces/
  README.md  CLAIMS.md  AUDIT.md  RECEIPT.md
  TREE_CONTRACT.json  SOURCE_MANIFEST.json  input.json
  model.py  tests/test_model.py  verify.py
  lean/lakefile.toml  lean/lean-toolchain  lean/lake-manifest.json
  lean/ResearchInstitutionForces.lean
  lean/ResearchInstitutionForces/{Joint,Robust,Staleness,Ballot,AxiomReport}.lean
```

From this directory, with Lean 4.33.0 on the path:

```
python verify.py --check        # pins, pytest, mypy --strict, forbidden tokens,
                                # lake build, the axiom report against the contract
python verify.py --write-pins   # after an intentional change to input.json
python model.py                 # every finite check, as JSON (about 25 s)
```

`verify.py` is the canonical scaffold copy. `RECEIPT.md` records one run.
The tree is registered as a local receipt only: no workflow step runs it.
