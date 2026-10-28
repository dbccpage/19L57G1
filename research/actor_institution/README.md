# actor_institution

AuthorityEffect: None. Outside the seal. Consumes the sealed `Derivation`
package (`Derivation.Counting`, `Derivation.Represented`, and through
`two_theorems` the `Compression` namespace) and the `two_theorems` research
tree read-only (`lean/lakefile.toml` requires `../../../lean4` and
`../../two_theorems/lean`) and changes nothing in either. Every name consumed
from `two_theorems` (`Institution`, `pQ`, `Knows`, `classCount`,
`information`, `Sharp`, `sharpObserver`, `residuals`, `knowsB`) is used as
merged in #277, unchanged.

Question (the research brief of 2026-10-28, Parts I to VI): finish what can be
finished of the actor, institution, information, knowledge and wisdom
derivations. In Lean where a general statement holds; by a finite witness
where a conjecture fails; as a precise OPEN obligation where neither is
reached. A definition is not a theorem, and nothing below is declared done
because it has a name.

## Vocabulary, reconciled

| Word in the brief | Object here | Status | What the status rests on |
|---|---|---|---|
| actor, presentation | `p : Nat → Nat`, read on a carrier `D : List Nat` (two_theorems `Presentation`) | admitted | A function is the metatheory's; on `D` it is a finite table (TT-41). Nothing reads `p` off `D`. |
| institution, family | `Q : List (Nat → Nat)` (two_theorems `Institution`): retention is the list, comparison is `SigEq Q x y`, combination is the representative `pQ D Q` | admitted | The three operations are the sealed `Compression` definitions. |
| information | `information D Q = classCount D Q`: the number of signature classes on `D` | derived definition; the *word* is a proposal | Monotone, bounded by `|D|`, raised by exactly one by an unknown question (sealed and TT theorems, listed below). |
| knowledge | `Knows D Q q := FactorsOn D (pQ D Q) q`: `q` factors through the representative | derived definition; the *word* is a proposal | Equivalent to determination (`knows_iff_determined`) and to stationarity (`knows_iff_information_eq`), both TT. |
| witnessed difference | `¬ SigEq Q x y`, with its separator (`Compression.exists_separator_of_not_sigEq`) | derived | A pair is apart only by a member that separates it. |
| observation | a view `c : List Nat` and its verdict `verdictB E x y` (sealed `Represented`); a probe `p x = p y` (`Acquisition.entry`) | admitted grammar | The probe grammar is the admission of this tree; TT-43o left it to be chosen. |
| determination, certified claim | `knowsB D Q s = true`, equivalently `residuals D Q s = []` (TT `knows_iff_knowsB`, `residuals_nil_iff`) | derived | The certificate is the computed Boolean plus the empty residual list. |
| residual, demurral | `residuals D Q s`; `Policy.respond` returns `.demur R` with that list | derived | Each residual is a pair of the carrier the institution merges and the claim separates. |
| outcome of a claim | `Policy.Outcome`: supported, refuted, unresolved, for the pair claims `same x y`, `apart x y` | derived | The brief's UNSUPPORTED is this tree's `unresolved`: not supported and not refuted. |
| authorization | `Policy.Rule := List Nat → Institution → (Nat → Nat) → Bool`; `ScopedSound A := ∀ D Q s, A D Q s = true → Knows D Q s` | admitted | Which rule is in force is a choice. The theorems hold for every `ScopedSound` rule and select none. |
| correspondence, truth | `Chain.Corr D q t := ∀ x ∈ D, q x = t x`, relative to an admitted target `t` | admitted target | No target, no truth: `determination_not_truth`. |
| wisdom | no object claims the word | proposal | `Wise` was refuted as a reading (TT-34): it held of every institution. What is formalized here are components: outcomes, assert/demur, the retained residual, the demurred claim, scoped authorization. |
| intelligence | no object claims the word | proposal | What is formalized: an actor's partition (`classCount D [p]`), sharp presentation (`Sharp`), and what a transcript can and cannot show of it (AI-16, AI-20, AI-21). |

## Reconciled inventory

**Already proved before this tree, used as is, not repeated.**

- Sealed `Compression`: `pQ_exact` (the representative separates exactly the
  signatures), `exists_separator_of_not_sigEq`, `count_le_of_determines`
  (a coarser map has at most as many classes), `classCount_pos`,
  `sigEq_iff_sigList`.
- Sealed `Counting`: `allPairs`, `allPairs_length` (`2·|allPairs n| = n(n−1)`).
- Sealed `Represented`: views, `sepB`, `verdictB`.
- two_theorems (#277): `knows_iff_determined`, `knows_mono`, `knows_const`,
  `information_mono`, `information_le_carrier`,
  `information_append_of_knows`, `information_lt_of_not_knows`,
  `knows_iff_information_eq`, `known_extension_inert`, `not_knows_iff_witness`,
  `residuals_nil_iff`, `residual_removed_iff`, `knows_iff_knowsB`,
  `verdictB_false_iff_sigEq`, `Sharp`, `bitObserver_sharp`,
  `sharpObserver_sharp`, `sharpObserver_congr`, `sharp_fixes_partition`,
  `sharp_iff_sufficient_and_consistent`; the refutation of `Wise` (TT-34);
  the four-point example of a family knowing what no member knows.
- #278 (interpreter verdict) and #279 (no imports from nowhere) set the
  reading of the Lean quantifiers used below; see Outside the system.

**Proved here.** The ledger `CLAIMS.md` has one row per result; the names are
in `lean/ResearchActorInstitution/{Institution,Chain,Policy,Acquisition}.lean`.

- Institution: the exact condition for a family to know what no member knows,
  with the minimal counts (three data, two members) attained on three points;
  correspondence as an admission; renaming invariance; three degradation
  theorems (aggregates inert, essential members, loss of provenance and
  consensus after loss).
- Chain: TT-35o closed (a chain longer than the carrier has a stationary
  step, at which nothing new is known); information without determination;
  determination is not truth, truth is a further question, and the price of
  truth is admitting the target.
- Policy: assert/demur with the residual retained, the demurred claim always
  known, evidence never a digest, scoped authorization refusing every
  residual, authorization distinct from correctness, outcomes of pair claims
  with their persistence, identity never established absolutely.
- Acquisition: TT-43o (i) in both directions (`n(n−1)/2` probes, exactly),
  (iii) from the transcript, (iv) necessity; TT-39o; the fixed-family
  counterexample; and the refutation of the "exactly `N`" reading of (ii).

**Refuted.** TT-43o (ii) under the reading that the actor's class count is
promised exactly (AI-19, in Lean at `n = N = 2`, in the model at every
`n = N ≤ 6`). Earlier: `Wise` as a reading of wisdom (TT-34).

**Open.** Listed under Remaining obligations.

## Results

### Institution: what a family knows that no member knows

`Exceeds D Q q` says the family `Q` knows `q` and no member alone does.
`exceeds_iff` characterizes it: every pair `q` separates is separated by some
member, and every member merges some pair `q` separates. Consequences: a
nonempty exceeding family has two members disagreeing on a pair one of them
merges, and three distinct data; a single member never exceeds; nothing
exceeds on two points. The empty family exceeds exactly on the constants,
vacuously (`exceeds_nil_iff`), so the minima are stated for nonempty
families. The minimum is attained on `[0, 1, 2]` by `[p1, p2]` and `q3`, each
member and `q3` with two classes and the family with three
(`exceeds_three_two_resolution`): the family's advantage is one class of
information, and `q3` is known because that class is where `q3` changes.

Correspondence is an admission. The same two members know `q3`, and with
datum 0 and datum 1 swapped inside one member they do not
(`correspondence_matters`). What the family compares is the index, and the
index is presentation; a rewriting carried through every member and the claim
changes nothing (`knows_rename`). Nothing here identifies datum 0 of one
member with datum 0 of another beyond the admission that the list shares its
indices, which is the same admission `research/uncollapse` made explicit for
regime families.

Degradation. Members the family already knows add no information and no
knowledge (`aggregates_inert`, `aggregates_inert_knows`): a hierarchy of
digests of what is already known is inert. A member is essential exactly when
the rest do not know it (`essential_iff`). Compressing a family to its joint
representative keeps the knowledge and erases the structure: on four points
`[parity, half]` knows the identity while neither member does, their joint
representative is the identity, and the one-member family of that digest does
not exceed (`aggregate_hides_exceeding`). After losing a member the survivor
merges a pair the family separated and no longer knows `q3`
(`consensus_after_loss`): agreement after loss is not agreement.

### Chain: long chains go stationary; determination is not truth

An extension chain of institutions (`Extends Q Q'`: every member of `Q` is in
`Q'`) that is longer than a nonempty carrier has a stationary step
(`long_chain_stationary`), because information is monotone along it and
bounded by `|D|`. At a stationary step every member of the later institution
was already known by the earlier (`stationary_step_known`) and nothing new is
known (`stationary_step_inert`). This closes TT-35o: the author's "crash by
compression" is, inside Genesis's objects, this stationary step; whether it is
what happens to institutions in the world is TT-36o and stays open. The bound
is tight (model: a chain of three on three points with no stationary step).

`[parity]` on four points has information 2 and does not know `half`
(`information_without_determination`): information is a count of classes,
determination is a factoring, and the first does not give the second.

Every institution knows the constants 0 and 1 on any nonempty carrier, and the
two do not correspond (`determination_not_truth`). "Functional determination"
is `Knows`; "established truth" needs a target `t` and is `Corr D q t`, which
no institution carries. Whether a known claim agrees with a target is itself a
question (`agreeQ q t`), and the institution may not know it
(`truth_is_a_further_question`). The price of truth is admitting the target:
when `t ∈ Q`, correspondence with `t` gives knowledge
(`truth_from_admitted_target`) and agreement with `t` is known
(`agreement_known_of_admitted`).

### Policy: assert, demur, retain, authorize

`respond D Q s` asserts when `knowsB D Q s` and otherwise demurs with
`residuals D Q s`. A demurral carries a witness pair with equal signatures and
unequal claim values (`demur_carries_witness`); each residual is answerable by
one more question, the indicator of its first point (`residual_answerable`),
which is the brief's REQUEST_MORE_EVIDENCE made precise: the residual names
the question. A separating question is never a function of the signature
(`evidence_is_not_a_digest`): evidence is not what the institution already
computes.

The demurred claim marks every unsettled point 0 and shifts the rest; the
institution that demurred knows it (`demurred_known`), and it is total exactly
when the original claim is known (`demurred_total_iff`). Demurring is
therefore a grounded act: what the institution asserts after demurring is
something it knows.

A rule authorizes a claim by returning `true`. `ScopedSound A` is the
admission that `A` authorizes only known claims; under it no rule authorizes a
claim with a residual (`scoped_sound_refuses_residual`), `knowsB` is the
largest such rule (`knowsB_scoped_sound`, `scoped_sound_le_knowsB`). This is
the brief's theorem that a properly constituted institution never authorizes a
claim as established while its observations admit an unresolved relevant
distinction, with "properly constituted" read as `ScopedSound`. The brief
foresaw the split: authorization relative to the certificate is proved;
correctness relative to a target is not entailed (`authorization_not_correctness`:
`knowsB` authorizes both constants).

Pair claims `same x y` and `apart x y` have three outcomes. `same` is never
supported and `apart` is never refuted: an institution can show two data apart
and can never show them the same beyond its current questions. Supported
`apart` and refuted `same` persist under extension; for distinct data some
extension refutes `same` (`same_never_established`), and `same` survives every
extension exactly when the data are equal (`established_iff_eq`). Identity is
scoped: `sameRel [] 0 1` holds and `sameRel [id] 0 1` fails.

### Acquisition: what probes can and cannot buy

TT-43o asked for the cost of acquiring a partition under an admitted grammar.
The grammar admitted here: a probe `x y` is answered by `decide (p x = p y)`
at cost 1; a protocol is a function from the transcript so far to the next
pair or a stop; an admission rule is a function from the transcript to an
evaluator; the protocol *acquires* the actor when that evaluator is sharp for
it. The actor is reached through probes only (`run_congr`: two actors that
answer every asked probe alike have the same transcript).

(i) Exactly `n(n−1)/2`. If the identity's transcript is shorter than
`|allPairs n|`, some pair `x < y < n` was never probed (`uncovered_pair`, with
a constructive count of duplicate-free lists, since core's lemma uses
`Classical.choice`), and the actor `merge x y` that identifies exactly that pair
has the same transcript (`lower_bound`). Whatever evaluator the rule builds
from it, it is not sharp for one of the two (`no_acquisition_below_bound`). The
complete table of all pairs, read into one view per datum, is sharp for every
actor (`table_sharp`, `complete_table_acquires`). Both halves are
`acquisition_cost_exact`; the model's exact minimax over every adaptive
protocol agrees for `n ≤ 6`.

(ii) The promised count, `N(N−1)/2 + (n−N)(N−1)`, is refuted under the
reading "exactly `N` classes": on two points with two classes promised, no
probe is needed (`exact_promise_zero_probes_two`), while the count says one;
the same at every `n = N ≤ 6`. Under "at most `N` classes" the count matches
the exact value for every `N ≤ n ≤ 6`, and under "exactly `N`" for every
`N < n ≤ 6`. The general statement is OPEN (AI-19o).

(iii) From the complete table alone, `acquired n T = pQ (range n) (questions
(tableE n T))` has the actor's partition (`acquired_kernel`), and `m` views
computed from it are sharp when the actor has at most `2^m` classes
(`log_views`). The views are computed from the transcript, which is the
point: the two_theorems observer was built from the actor's partition, this
one from the record of probes.

(iv) An evaluator sharp for every actor consistent with the transcript forces
them all to one partition (`acquires_implies_fixes`). The converse, an
evaluator computed from any fixing transcript, holds in the model for every
transcript on `n ≤ 5` points by the closure of the "same" answers; in Lean it
is OPEN (AI-18o).

TT-39o. Below the bound two actors of different capability, one merging a pair
the other separates, have identical transcripts (`transcripts_identical_capabilities_differ`).
What a transcript shows of another actor is bounded by what was probed; "how
intelligent another is" is, inside this grammar, a statement about the
transcript, and the transcript is silent on every unprobed pair.

Retained counterexample. For the fixed family `{id, merge 0 1}` on two points,
one probe and a two-case rule acquire both members
(`complete_evaluator_for_two`). A complete finite evaluator for a fixed finite
actor family is cheap; the bound is about every actor on the carrier.

## The chain

The brief's chain, witnessed difference → observation → information →
determination → certified claim → authorization, is five links, not one
theorem (AI-22):

1. A witnessed difference is a separating question (`exists_separator_of_not_sigEq`,
   sealed): without a member that separates `x` from `y`, nothing witnesses
   their difference.
2. A question not yet known raises information strictly, by at least one class
   (`information_lt_of_not_knows`, `knows_iff_information_eq`, TT).
3. Information does not give determination (`information_without_determination`).
   The step from a count to a factoring is a further fact about the claim.
4. Determination is the certificate: `knowsB = true`, equivalently an empty
   residual list (`knows_iff_knowsB`, `residuals_nil_iff`), which `respond`
   turns into an assertion (`respond_assert_iff`).
5. The certificate licenses authorization only under `ScopedSound`, an
   admission; and authorization is never correctness (`authorization_not_correctness`).

The sixth arrow the brief hoped for, from authorization to truth, does not
exist here. Truth is relative to an admitted target and costs its admission
(`truth_from_admitted_target`).

## What information, knowledge and wisdom mean here

**Information** is `classCount D Q`, the number of distinguishable classes the
institution's questions cut the carrier into. The theorems about it
(monotone, bounded, raised by an unknown question, inert under known
members, stationary along long chains) are derived. That this number is what
"information" should mean is a proposal; TT-41 shows it is the same number
whether the questions are functions or tables.

**Knowledge** of a claim is factoring through the representative, `Knows`;
equivalently the claim is determined by the signature; equivalently adding
the claim is stationary. Derived. It is knowledge of the institution, not of
a member: a family can know what no member knows, and the exact condition
and minimal counts are AI-01 to AI-03. It is not truth: AI-09.

**Wisdom** has no definition here. `Wise` was refuted (TT-34) because it held
of every institution. What is proved are the acts the brief listed: an
outcome for a claim (supported, refuted, unresolved), the response to assert
or to demur with the residual retained, the demurred claim that is always
grounded, the request for evidence that names its question, and authorization
that, when constituted as `ScopedSound`, refuses every residual. A reader may
call the policy that performs those acts "wisdom"; the tree does not, because
a word attached to a definition that any institution satisfies names nothing,
and because which rule authorizes is an admission the tree cannot derive.

**Intelligence** has no definition here either. What is proved is what an
actor's partition costs to acquire and what a transcript can show of it.

## Remaining obligations

- AI-18o: TT-43o (iv) sufficiency in Lean (the closure evaluator).
- AI-19o: TT-43o (ii) in general, under the "at most `N`" reading, and the
  "exactly `N`" reading for `N < n`.
- The authority rule: `ScopedSound` is the admission. Any stronger reading of
  "properly constituted" (which residuals count as relevant, what else a rule
  may refuse) is a further admission with its own theorem.
- TT-36o, TT-37o, TT-38o remain open as stated in two_theorems; nothing here
  touches them.
- The brief's Part V hoped for an arrow from authorization to truth; AI-09 and
  AI-14 show there is none without an admitted target. That is a result, not
  an obligation, but the reader who wanted the arrow should know it was
  looked for.

## Outside the system

Everything in Lean here is metatheory about finite tables. `Nat → Nat`,
`List Nat`, `Protocol`, the quantifiers `∀ p` and `∃ p`, and the game over
"every actor" are the metatheory's; the system at any point holds a finite
carrier `D`, a finite list of questions, and a finite transcript. No infinite
family, continuum or observer is admitted. The protocol `π` and the admission
rule `rule` in Acquisition are external functions: they stand for the caller
of the seed probing an actor, not for an observer inside the system. The
"adversary" of the lower bound is a proof device: it is the actor `merge x y`,
one finite table, exhibited. The model enumerates partitions of `range n` for
`n ≤ 6`; the Lean theorems quantify over every `p : Nat → Nat` and read it on
`range n` only. Where a definition's extension read in Lean is unbounded
(`Knows D Q q` for `q` off `D`), the theorem says nothing off `D`.

## Layout and how to run

```
research/actor_institution/
  README.md  CLAIMS.md  AUDIT.md  RECEIPT.md
  TREE_CONTRACT.json  SOURCE_MANIFEST.json  input.json
  model.py  tests/test_model.py  verify.py
  lean/lakefile.toml  lean/lean-toolchain  lean/lake-manifest.json
  lean/ResearchActorInstitution.lean
  lean/ResearchActorInstitution/{Institution,Chain,Policy,Acquisition,AxiomReport}.lean
```

From this directory, with Lean 4.33.0 on the path:

```
python verify.py --check        # pins, pytest, mypy --strict, forbidden tokens,
                                # lake build, the axiom report against the contract
python verify.py --write-pins   # after an intentional change to input.json
python model.py                 # the finite model's summary as JSON (n ≤ 5)
python model.py 6               # the same with the game to six points (~11 s)
```

`verify.py --check` is the tree's own receipt; `RECEIPT.md` records one run.
The repository suite (`python -m pytest` at the root) holds the gates that see
this tree from outside: the research-tree contract, the generated index pages
and the identifier firewall.
