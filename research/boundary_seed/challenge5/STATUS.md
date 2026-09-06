# Challenge 5 — status

`AuthorityEffect: None`.  Session of 2026-09-05, branch
`research/boundary-run`, opened with Challenge 4 in its review-repair state
(`75b7ed1a`: 303 tests, line and branch 100%, 139 Lean reports).  One rung
closed: the caller supplies and retains `<<a|>|>`, a whole within a side.

## Order of the work, as committed

1. `67d3e320` `challenge5/PREDICTIONS.md` frozen, sha256
   `b3aab18d8e5a0700e563862ef7a884248badefbc7c653df0e00097044e3d99de`,
   committed alone before any Challenge 5 code or proof.  The existing
   `challenge*/PREDICTIONS.md -text` attribute already covered it
   (`git check-attr` reports `text: unset`), so no attributes change was
   needed.
2. The rung commit: kernel, Lean, receipt, tests, prose, registration, and
   the injections below.

This history proves “committed before” only.  It cannot prove when any
untracked or off-tree code or proof was written, and it is not evidence of
insight.

## Provenance ceiling

Inherited unchanged: `SOURCE_ISOLATED_WITH_DECLARED_PRIOR_EXPOSURE`.  This
session read nothing outside the write root and the seed, but the harness
loads the repository contract file **whole**, operating manual included, which
is wider than the five sections the seed's isolation clause names; and the
session is an instrument of the same kind as the one that declared prior
exposure.  The per-rung adversarial review channel, disclosed in the paper's
section 0, supplied this rung's advisory list; it supplied no definition,
policy, or result.

## Results

Receipt `receipts/challenge5.json` (128086 bytes after the second review
repair); full tables in `paper.md` sections 5.17 to 5.20.

| | reading U | reading O |
|---|---|---|
| the Challenge 1 and Challenge 4 readers on `<<a|>|>` | both refuse by name (COMPUTED; each bound is its own rung's DEFINITION) | same |
| the third reader bound, and the second widening of the run's reader | one declaration of this rung, paid by the run; depth bound two, deeper refused by name (DEFINITION).  Three bounds, two widenings: the Challenge 1 bound was declared and not widened | same |
| the declared policy space | four policies over three capabilities, at counts `0, 1, 1, 2`; with the naming coordinate, eight points (DEFINITION) | same |
| **one step, and the coordinate count** | one step is capability count one; the two counts **part** at this rung, the recording policy moving one coordinate and using two capabilities (COMPUTED against the declared rule) | same |
| policies that admit the caller's inscription | three of four (COMPUTED) | same |
| what the two one-step policies retain from `<<a|>|>` | one mark, address `(0,)`, isomorphic to what `<a|>` retains — and under the discarding policy **equal** to it (COMPUTED; PROVED that the flattened states coincide) | same |
| **so the object language cannot see a boundary within a side at any one-step policy** | **yes, under both readings** (COMPUTED; PROVED, and proved more generally that flattening is blind to every inner exchange) | same |
| the two one-step policies are the same policy | **no**: they part at 95 of the 144 declared inscriptions, and at none of them is it the caller's own (COMPUTED census) | same |
| the minimum capability count among admitting points | **1** (COMPUTED) | **1** (COMPUTED) |
| the minimum is unique | **no**, two tied classes, both retained; uniqueness refuted — where at Challenge 4 it was not refuted under U (COMPUTED) | **no**, two tied classes, both retained (COMPUTED) |
| the second measure at the minima | 0 at the discarding policy, 1 at the opaque one (COMPUTED) | 1 and 2 (COMPUTED) |
| **the two measures select the same minima** | **no**; the second measure picks the discarding policy alone (COMPUTED).  The first rung at which they part under BOTH readings: at Challenge 3 they parted under O alone and at Challenge 4 they agreed under both | **no**, the same (COMPUTED) |
| bundles refused | 4 of the 8 points (COMPUTED from the declared count) | same |
| what the caller's own demand costs | **2**: the recording policy, refused as a bundle.  WHICH policy the demand names is COMPUTED, by the probe below; that it costs 2 is the declared capability count (DEFINITION) | same |
| the inner whole is a second initial datum | **no**, under no policy (COMPUTED at every point; PROVED that no deep history moves the datum) | same |
| the inner whole is a side | **no**, under no policy: sides come with a boundary and are never admitted (DEFINITION) | same |
| what the inner whole IS | a MARK under the opaque policy; NOTHING under the discarding one; a second BOUNDARY under the recording one (declared classification; the receipt computes what each retains) | same |
| a further mark may be admitted inside the inner whole | under the recording policy alone (COMPUTED: the deciding fact is the deepest place the policy's own admissions name over the declared domain, one at each one-step policy and two at the recording one, and not the policy's name; the deep grammar is policy-agnostic and records the requested address at every admitting point, which the receipt reports beside it) | same |
| depth at every one-step policy | every retained mark is one boundary in; depth separates nothing (COMPUTED over the declared domain) | same |
| **depth as an internally available count**, sense one | under the recording policy: invariant under every permitted renaming, and determined by the key at every point of the space (PROVED that no LEVEL EXCHANGE moves a mark's depth, COMPUTED at one two-mark state that no MARK PERMUTATION does either; the key-determination is DEFINITION-level under the declared serialization) | same |
| **depth as an internally available count**, sense two | **not expressible**: no form of the closed observation grammar reads it, and this rung adds none (COMPUTED census over the declared vocabulary; DEFINITION-level, the grammar being a declared sum of two forms) | same |
| the naming coordinate — whether the reading's naming reaches the inner boundary | **collapses at every policy**: U names nothing at any level, so both values declare the same renamings and the same key (COMPUTED quotient) | **collapses at three of four**, and not at the recording policy (COMPUTED quotient) |
| the retained mark's address orbit, under the recording policy | **4** (COMPUTED); at the two one-step policies the same key reads **2** | **2** without the naming reaching inward, **1** with it (COMPUTED); at the two one-step policies it reads **1** |
| which side of the OUTER boundary the mark lies on | not internally available (COMPUTED) | internally available (COMPUTED) |
| which side of the INNER boundary the mark lies on | not internally available (COMPUTED; PROVED that nothing invariant under the inner exchange separates the two) | **not internally available either**, without the further naming declaration; available with it (COMPUTED; PROVED, with the countermodel that keeps the theorem non-vacuous) |
| the within-whole order at every level | moves the state at 116 of 144 inscriptions and no state's class (COMPUTED for the first; DEFINITION-level for the second, the mark permutations being permitted at every point) | same |
| the outside of the outermost boundary | not formulable: an address is a sequence of sides crossed inward and the declared alphabet has no value for it; **OPEN**, named rather than answered | same |
| initial datum, reading, event-follows relation | unchanged, empty on every probe of both grammars at every point (DEFINITION for one event; PROVED for histories) | same |
| new event kind | `AdmitAt`, available only under the recording policy; no rule withdrawn | same |

Boundary dependence: the identity of the policy space, the capability counts,
the one-step rule, the refusal of bundles, and the two senses of an available
depth do not require the admitted boundary.  The notion of depth, the address,
the crossing, every level exchange, the invisibility of the nesting, and the
reader's own bound require it and are not formulated after removing it.  The
outside of the outermost boundary requires it to be formulated at all, and is
not formulated.

**The seed's questions, answered.**  *Can the object language see a boundary
within a side?*  Not at any policy of capability count one, under either
reading: what `<<a|>|>` retains there is isomorphic to what `<a|>` retains, and
under the discarding policy equal to it.  It can under the recording policy,
which costs two capabilities and is refused as a one-step augmentation.  *Is a
whole on a side a datum, a side, or something needing a new definition?*  Not a
datum — the regime carries exactly one and no admission event makes another —
and not a side, sides coming with a boundary and never being admitted.  Under
the opaque policy it is a mark; under the discarding policy it is nothing at
all; under the recording policy it is a second boundary, which is a new
definition.  *What does “within” mean at depth two under each reading?*  It
means an address: a sequence of sides crossed, outermost first.  Under U
neither level's sides are named and both exchanges are permitted, so the
address is carried to all four of its values.  Under O the outer sides are
named and the inner are not, unless a further declaration says the naming
reaches inward — a declaration the seed's one exception does not make.  So
reading O alone does not settle what “within” means at depth two, and the
rung's sharpest single fact is that the U-versus-O question reappears one level
down and has to be declared again.  *Is depth an internally available count?*
In one sense yes under the recording policy — no permitted renaming moves it
and the key determines it — and in another sense no at every point, no form of
the closed grammar reading it and no counting form being added.  The two senses
are kept apart and neither is unconditional.  *What admission is needed to
treat the inner whole as the outer whole was treated?*  Exactly the recording
policy: its two sides are places at which a further mark may be admitted, which
the probe computes, and no cheaper policy offers that.

## Predictions scored

| id | label | status | note |
|---|---|---|---|
| C4-X | NOT FORCED | **PARTIAL** | seven clauses hit: this rung's reader refuses the nested whole by name and the widening is priced and paid by the run; its ordinal, “a second” widening, holds — the run has three reader bounds and two widenings; depth is available at no policy of capability count one and the boundary within a side is visible at none either, so it is not visible without a new declaration; the inner whole is a second initial datum under no policy; and the decision takes the form of a declared finite policy space.  **MISSED**, recorded next to its value: “a declared finite space of policies with exactly one member letting the caller retain the inscription”.  **Three** of the four declared policies admit the caller's inscription; exactly one retains it so that the retained state tells it from the flat inscription.  The clause is scored on the first count, which is what its own words say, and the second is reported beside it.  The frozen file is untouched |
| C5-1 the readers, and the widening (the frozen file titles it “the third widening”) | FORCED | **PARTIAL**, DEFINITION-level | both refusals are earlier rungs' declared bounds replayed, and the new bound is this rung's declaration; not counted as content.  **MISSED**, recorded next to its value: the ordinal.  The frozen clause says the bound “must be widened a third”, and the census of the run's own readers gives **three bounds and two widenings** — the Challenge 1 bound was declared and not widened.  That is the ordinal the frozen C4-X gives the same event, and it is scored HIT there; scoring one and not the other would leave the run counting one event two ways.  The frozen file is untouched |
| C5-2 the declared policy space and its prices | NOT FORCED | HIT, DEFINITION-level | the four policies, the three capabilities, and the counts are declarations; not counted as content |
| C5-3 the nesting is invisible at every one-step policy | FORCED | HIT | content: an isomorphism-witness search at each candidate's own renamings, with both values attained in the space |
| C5-4 the two one-step policies are two, and both retained | FORCED | HIT | content: a census over 144 declared inscriptions with the parting members named, and the implemented quotient |
| C5-5 what the inner whole is, under each policy | NOT FORCED | HIT | content: the datum clause is a replay at every point and the inner-place clause a probe whose deciding fact is the deepest place each policy's own admissions name over the declared domain, with both values attained; the classification itself is declared and reported as such |
| C5-6 depth, in two senses kept apart | FORCED | HIT | content: the depths census, `[1]` at every one-step policy against `[1, 2]` at the recording one; that the key determines depth and that no form of the closed grammar reads it are both DEFINITION-level and reported separately |
| C5-7 each reading splits at depth two, and only U's split collapses | FORCED | HIT | content: the implemented quotient over the whole domain, and the three orbit sizes read off the unpruned enumeration |
| C5-8 inertia, and the outside | FORCED | HIT | content: certification and replay at every point with both values of the admission predicate attained; the empty event-follows relation is DEFINITION-level |
| C5-X | NOT FORCED | PENDING | scored by the autonomous continuation |

Seven of eight scored predictions hit and one is PARTIAL: six hit as content
(C5-3 to C5-8), one by construction (C5-2), and C5-1 is PARTIAL by
construction — its readers clause holds and its ordinal does not — by the
criterion Challenge 1 declared and this rung reuses unchanged.  The counts are
the receipt's `tally`, computed from the statuses and a declared list, and the
negative direction of every one is tested.

**A near sweep is the weakest kind of evidence this run produces, and this
one is the weakest yet.**  The predictions were written by an instrument that
had already reasoned the rung through — the policy space, the invisibility, the
orbit sizes, and the U/O split at depth two were all worked out by hand before
the file was frozen — so the hits show the ORDER of the work and not
foresight.  The informative number is again the previous rung's extrapolation,
written before this rung existed: PARTIAL, and missed on a count it could have
got right, having asserted “exactly one” where the enumeration finds three.
Two things this rung found were *not* predicted anywhere: that the two cost
measures would select different minima under both readings, which no earlier
rung does, and that one step and the coordinate count would part.  Both are
recorded as results, not as hits.  The single PARTIAL is an ordinal the rung
wrote wrongly into its own frozen file and did not read until review; no result
moved with it.

## Advisories carried from the review of Challenge 4

The rule, inherited: an advisory is **actioned** when the repair lies in a
living document of this rung or in apparatus; one that would require
regenerating a closed rung's receipt, or editing a previous rung's
`STATUS.md`, is **carried** with its reason.  Every advisory is listed;
`change_log.md` carries each repair with its reason.

Actioned:

1. `paper.md:1339`, the cited Lean theorem covering one of the two inseparable
   pairs.  This was actioned inside Challenge 4's own review repair, which
   added `crossRetained_other_marks_share_a_side` and cites both; the advisory
   arrived describing the pre-repair state.  Confirmed rather than repeated:
   both theorems are cited at the three prose sites and in the two ledger
   entries, and the paper's section 7.5 row names both.
2. `paper.md:2112`, section 9's bare “which is proved” attached to a
   conjunction whose first half is COMPUTED only.  Section 9 now says which
   half is computed and which is proved, in the same words the repaired 5.13
   sentence uses.
3. `claim_ledger.md:1853`, “the two marks that share a side” as a definite
   description that does not uniquely denote.  Both ledger entries now name the
   marks and cite both theorems, so the description denotes.
4. `paper.md:1392`, “a complete invariant” as an undefined technical term in a
   section heading.  The heading and the sentence under it now say “an
   invariant that separates the four marks”, with the scope stated; the
   reserved word is gone from both.
5. `paper.md:1430`, the boundary's price table counting collateral facts that
   no receipt key carries.  The count is dropped from the row, which now says
   only what the receipt says.
6. `claim_ledger.md:2041`, B4-TWO-SENSES asserting the grouping-with-names
   point is a parting point under both readings.  The clause is scoped to U,
   with the O behaviour named.
7. `paper.md:1343` (carried `should_fix` from an earlier round), the 5.13 U
   cell saying the side exchange is a permitted automorphism.  The cell now
   says what the receipt computes: a side-exchanging automorphism exists and is
   the side exchange composed with the mark permutation `[1, 0, 3, 2]`.
8. `claim_ledger.md:1823` (carried `should_fix`), three theorems given PROVED
   in the ledger and DEFINITION-level in the paper's section 7.5.  Resolved the
   way the advisory's own analysis points: the paper's classification was the
   error, since the structurally identical Challenge 2 theorem is listed as
   content, and the three are removed from section 7.5's DEFINITION-level list.
   One theorem, one label, in both places.
9. `research/boundary_seed/MANUAL.md:147`, an injection row recording no gate
   failure.  That row is the coverage-gate row, whose recovery line was
   withdrawn in place without a replacement failure being written; it now
   records the failure that was observed, `FAIL: coverage.json missing`, and
   says that the withdrawn recovery line is the one below it.

Carried, with reasons:

10. `code/boundary/challenge4.py:118`, the whole-property domain's label
    alphabet; `:1943`, the receipt's account of “mention”; `:706`, a docstring
    miscount; `:1751`, `side_properties_invariant_by_reading` reading only the
    first of the two properties; `:320`, C4-1's DEFINITION-level tally against
    its isomorphism-search clause; `:1518`, two of the eight C3-X clause
    statuses equal by construction.  All six lie in `code/boundary/challenge4.py`
    and would regenerate a closed rung's receipt.  None can change that rung's
    recorded statuses.  **The last of them is answered rather than repaired**:
    this rung computes, and reports in `readings.*.collateral_facts_agreeing_everywhere`,
    exactly which pairs of its own declared facts take the same value at every
    point, so that a reader knows where its second measure counts one thing
    twice.  That is the general form of the advisory, made into a receipt key.
11. `challenge4/STATUS.md:222`, a reserved word without a stated scope;
    `:191`, a dropped negation in a carried advisory; `:313`, the injection
    tally splitting ten rows as six injected and four found live where seven
    record an injection; `:109`, the predictions table describing C4-8's basis
    in pre-repair terms; `:253`, “the run's first uniqueness statement”.  A
    previous rung's `STATUS.md` is not edited.  Three of them are answered here
    instead: this status states its own tally as **six injected and three
    found live**, counts the one row that is both exactly once, and names the
    overlap rather than leaving a reader to reconcile it; the uniqueness point is settled by this rung's own result,
    which refutes uniqueness under both readings and so retires the earlier
    superlative; and the reserved words in this document all carry a scope or a
    proof.
12. `paper.md:1339`'s sibling items and the Challenge 1 to Challenge 3 carried
    items 15 to 17 of the Challenge 4 status survive unchanged: they lie in
    `challenge1.py`, `challenge2.py`, `challenge3.py`, or a frozen `STATUS.md`.

A dedicated repair session for Challenges 1 to 4 would clear items 10 to 12 in
one deliberate regeneration.  That is not this rung's work.

## Where the run reached for a remembered result (declared reading 0)

- **The vocabulary is standard mathematics and is not derived here.**
  “Address”, “depth”, “power set”, “orbit”, “invariant”, and the recursive
  reading of a bracketed text are known to this instrument.  They are declared
  as definitions 59 to 71 and used.
- **The recursive-descent reader is a remembered technique.**  Splitting a
  body at the bar of nesting level zero, and refusing beyond a declared depth,
  is ordinary parsing and is not a result of this run.  What is not inherited
  is what an admission then does with what is read: that is the declared policy
  space, and the run wrote it to answer the seed's question.
- **The shape of the rung follows Challenges 2 and 4**, which this session
  read: a declared finite space, a capability count per member, a one-step
  rule, an implemented quotient, two measures, and a scorer.  The one place the
  shape had to be changed rather than reused is the class key, and the change
  was forced by a computed fact — the two one-step policies retain isomorphic
  states at the caller's own inscription — and not by taste.
- **The Lean file's shape** — a concrete state, an obstruction, a general
  theorem over an arbitrary property, a countermodel, a continuation induction
  — follows Challenges 1 to 4, which the session read.
- **What was derived, and in this order.**  That both inherited readers refuse
  the inscription; that an admission meeting an item that is a whole has
  exactly four alternatives and that they cost 0, 1, 1, 2; that the two cheap
  ones make the nesting invisible and are nevertheless two policies; that what
  the caller actually asks for costs two and is therefore refused as a bundle;
  that depth splits into two senses; and that reading O does not settle the
  inner side.  All of those were worked out by hand before the predictions were
  frozen and then confirmed by the code, which is why the sweep is weak
  evidence.
- **Nothing in the numbers was remembered.**  144, 95, 116, orbit sizes 4, 2
  and 1, four bundles of eight, 406 tests, 177 axiom reports: all the code's.
  The two findings the predictions do not contain — the measures parting, and
  one step parting from the coordinate count — are the code's as well.

## Leftovers, for the autonomous continuation and later

- Score C5-X: whether the generator's first challenge from a surviving branch
  is a further mark rather than deeper nesting, whether it imports no
  undeclared structure, and whether the stage exports a frontier under a
  declared bound short of fifteen rounds.
- **The minimality is scoped to the declared policy space and to nothing
  wider.**  A policy that admitted the inner whole AND its items as separate
  marks, that admitted the inner boundary as a datum of its own, that read a
  different convention at each level, or that grouped marks by anything but the
  crossing, is not enumerated and no claim is made about it.
- **The domain is a declaration.**  Two policies are the same policy exactly
  when they retain isomorphic states at every one of its 144 members; a wider
  alphabet or a deeper bound is available and might separate policies this
  domain identifies.  Nothing here rules that out, and the class key would move
  with it.
- **The depth bound of two is the reader's declaration, not a limit.**  The
  same reader at a wider bound reads deeper wholes, which a test shows.  What
  happens at depth three — in particular whether the naming coordinate becomes
  a coordinate per level and the space grows with the depth — is not computed.
- The eight collateral facts are not eight independent facts, and the receipt
  says which pairs agree everywhere rather than re-weighting the measure.
  Whether the measure should count classes of facts rather than facts is OPEN.
- The correspondence between the Lean `exchangeLevel` and the Python
  `exchange_level` is prose, as `List.Perm` against `rename_marks` was at
  Challenge 3 and `exchangeWholes` against the configuration renaming at
  Challenge 4.
- Lean does not close the policy space, the capability counts, the class
  counts, the two measures, or the domain census.
- The outside of the outermost boundary is OPEN, and this rung names it rather
  than answering it: an address is inward-facing by declaration.
- Challenge 0 to Challenge 4 leftovers survive: no Lean statement of the
  class-count closed forms; no unbounded canonical-key theorem; the closure
  premise under the orbit witnesses is still checked by nothing; the freeze
  manifest protocol remains OPEN.

## Repairs and live failures during the rung

- **The reader's depth allowance was off by one on its first run**, refusing
  the caller's own inscription: the recursion decremented the allowance before
  testing the item rather than after. Found by a probe, not by a gate, and
  repaired before any receipt existed; `test_the_widened_reader_reads_a_whole_within_a_side`
  and the domain round-trip test fix it.
- **The declared domain was nine members on its first run and should have been
  144**, the enumeration passing the outer whole's own depth as the items'
  allowance.  Found by a probe.  `test_the_domain_is_the_declared_product`
  rebuilds the domain from the declared alphabet independently and fixes it.
- **The receipt byte-identity test fired during the rung**, when the order
  census was restructured to report the structural difference beside the
  class-level one and the committed receipt was left stale.  Row in
  `MANUAL.md`; `run_challenge5.py` regenerated it deliberately with no
  injection live.
- **A `git checkout` of the root Lean module during an injection reversal
  dropped the whole rung's audit lines again**, exactly as at Challenge 4, and
  the audit-totality check named all 38 theorems.  Recorded as a found-live row
  rather than quietly repaired: it is the SECOND time this reversal has done
  it, which says the hazard is in the reversal procedure and not in one
  session's carelessness.  The repair rebuilt the audit lines from the source
  text rather than by hand, and the log was not regenerated at any point while
  an injection was live.
- **A decision procedure was offered a goal carrying the reading as a free
  variable**, for the third rung running.  Two projection lemmas fix it, as at
  Challenges 2, 3 and 4.
- Every gate this rung added or touched has an injection row in `MANUAL.md`.

## Review repair of this rung

The review of Challenge 5 returned eleven surviving findings, one `blocking`
and ten `should_fix`, two of the ten being the same defect seen from two
sides.  The frozen `challenge5/PREDICTIONS.md` was not touched.  **One
prediction changed status**, C5-1, from HIT to PARTIAL, on an ordinal the
frozen file gets wrong; no computed result of the rung moved.  Each repair is
a line in `change_log.md` with its reason.  Nothing here was reached for from
memory: every corrected number is read off this tree's own receipts, code, or
Lean log, and the two comparisons with earlier rungs are read off
`receipts/challenge3.json` and `receipts/challenge4.json`.  Declined: nothing.

Actioned:

1. **The `blocking` one.**  The rung claimed the two cost measures select
   different minima "for the first time in the run", in the paper's sections
   5.18 and 9, in B5-MEASURES-PART, in this status, and in a test comment.
   Challenge 3's own receipt says otherwise: `readings.O.measures_agree_on_minima`
   is false there, and B3-TWO-MEASURES states it in words.  The claim is
   narrowed everywhere to what the three receipts support — the first rung at
   which they part under **both** readings, Challenge 3 having parted under O
   alone and Challenge 4 having agreed under both.
2. Three rows of the paper's section 7.6 gave "none" for theorems the axiom log
   reports as depending on `propext`: `nestedRetained_depth`,
   `flatRetained_depth`, and `flattenAddress_exchangeAt_succ`.  The log is the
   authority and the cells now match it; the other thirty-five rows already
   did, which was checked mechanically against `lean/axioms.txt` rather than by
   eye.
3. Section 9 and the 5.17 evidence cell attached "which is proved" to depth
   invariance under **every** permitted renaming, while the cited Lean theorem
   covers level exchanges only and the mark-permutation half is a bounded
   Python check at one two-mark state.  Both now say which half is proved and
   which computed, in the words B5-DEPTH-TWO-SENSES already used, and the 5.17
   cell cites the test.  The proof is not stretched; the prose is weakened.
4. The address-orbit row gave 4 / 2 / 1 with no scope, and those are the
   recording policy's numbers: at the two one-step policies the same key reads
   2 under U and 1 under O.  The paper's row, section 9's sentence, this
   status's row, and B5-NAMING now name the policy.
5. Section 5.17 said the U-versus-O price "is one capability per level", which
   sections 5.19 and 10 of the same paper record as not computed.  It is scoped
   to the two declared levels.
6. The event-acceptance probe decided its answer with the conjunct
   `point.policy == POLICY_ADDRESS` — the policy's own name — while its
   `because` text denied a length-two address the same object reported.  The
   probe now reads a census: the deepest place each policy's own admissions
   name over the declared 144-member domain, one at the two one-step policies
   and two at the recording one.  The refusal is that number, the recorded
   address is reported beside it, and the text no longer contradicts it.  The
   answer is unchanged; what changed is that it is now computed.  With it, the
   demand-cost row is relabelled: which policy the demand names is COMPUTED,
   what it costs is the declared count, and both declared price fields are
   listed in `price.fields_declared_not_computed`.
7. The receipt's declared text for the second measure called all eight
   collateral facts facts about the caller's retained whole, which definition
   70 contradicts: four are, two are censuses over the domain, one is about the
   grammar, one about the reading.  The constant and its comment now say what
   definition 70 says.  No measure value moves.
8. The declared presentation token for an opaquely admitted whole had no number
   and no ledger entry, while being the ONE collateral fact that separates the
   two tied minima and so the thing the rung's unpredicted result rests on.  It
   is now definition 71, cited from definition 61, and recorded as an
   assumption of B5-POLICY-SPACE and of B5-MEASURES-PART, which names it as the
   parting fact.
9. **The ordinal.**  The paper, this status, `challenge5.py` and
   `presentation.py` called this rung's reader bound the third *widening*.  The
   run has three reader bounds and two widenings: the Challenge 1 bound was
   declared, not widened, and `challenge4/STATUS.md`, the frozen C4-X, the
   ledger's B5-READER and the change log all say "second".  The prose is
   corrected, the receipt now carries the census
   (`reader.reader_bounds_declared`, `reader.widenings_of_the_reader_bound`),
   and **both** frozen ordinals are scored against it rather than one being
   left unread: C4-X's "a second" HITS and C5-1's "a third" MISSES, which is
   why C5-1 is PARTIAL.
10. B4-X was still carried OPEN with "none yet" evidence after this rung scored
    it PARTIAL with a clause MISSED.  It now reads SCORED at Challenge 5, names
    the clauses that hit — six at this repair, seven after the second repair
    below scored the visibility clause — and the one that missed with its
    value, and cites `scores.C4-X` and the tests, in the shape B1-X uses.

Carried: the Challenge 1 to Challenge 4 items already carried above are
unchanged; nothing new is carried.

## Second review repair of this rung

The second review of Challenge 5 returned eight surviving findings, one
`blocking` and seven `should_fix`.  The frozen `challenge5/PREDICTIONS.md` was
not touched.  **No prediction changed status** and no computed result of the
rung moved: one clause of the frozen C4-X that was computed and reported
without a verdict is now scored, and it HITS, so the C4-X count rises from six
clauses to seven while C4-X stays PARTIAL.  Each repair is a line in
`change_log.md` with its reason.  Nothing here was reached for from memory:
every corrected label is read off this tree's own receipt, code, or Lean log,
and the one comparison with earlier rungs is now recorded as a reading of their
code rather than as a computed fact.  Declined: nothing.

Actioned:

1. **The `blocking` one.**  Definition 59 still opened "The third and last
   widening of this run's reader" — the single site the previous repair's own
   account said it had corrected, while the receipt census, section 5.17's own
   bolded lead, B5-READER and this status all say three bounds and two
   widenings, and
   `scores.C5-1` scores the frozen "a third" MISSED on that wording.  The
   definition now names the third reader bound and the second widening.  **"and
   last" is dropped too**: no result of the rung says a later widening cannot
   happen, and the same definition calls the bound "a declaration too and not a
   limit".
2. The `NestedWhole` docstring in `presentation.py` was the second surviving
   site of the same ordinal, five lines below a module docstring that already
   read "the second widening".  It now names the run's third declared reader
   bound and its second widening, and "and last" is dropped from the module
   docstring for the reason above.
3. B5-CLASS-KEY folded a superlative about the run's own history — "the first
   quotient the run takes over a FUNCTION rather than over a state" — into a
   COMPUTED status with no receipt key, census, or test behind it.  It is now
   recorded as a reading of the earlier rungs' own class keys, each pairing a
   declared structure with the canonical key of ONE retained state, and kept
   out of the COMPUTED status; definition 69 and the inheritance paragraph
   below say the same.
4. The frozen C4-X carries eight clauses and only seven were given a status:
   "and the boundary within a side will not be visible without a new
   declaration" was reported as a bare fact that no verdict consulted.  It is
   now `nesting_not_visible_without_a_declaration_clause_status`, computed from
   the same census — the nesting is internally visible at no point of
   capability count one, under either reading — and folded into the verdict.
   The clause HITS, so no miss was hidden and no status moved; the scoring was
   simply not total.
5. B5-INERTIA gave PROVED to "any deep history keeps the reading and the datum"
   while naming four theorems, none of them the one covering the datum half.
   `BoundarySeed.deepReplay_initialDatum` is added to the entry with its axiom
   report, so every conjunct of the PROVED status names its theorem there.
6. `depth_determined_by_the_key` was COMPUTED and counted as C5-6's content
   with a falsifier that cannot fire.  It is true by unfolding the declared
   serialization — every permitted renaming keeps each address its length, so
   equal keys force equal depth signatures — and the receipt bears it out at
   all eight points of each reading, the refusing base included, so it never
   enters the second measure.  It is now DEFINITION-level and reported apart,
   as the grammar clause of the same prediction already was; C5-6's content is
   the depths a policy can hold, `[1]` at every one-step policy against
   `[1, 2]` at the recording one.  The un-fireable falsifier is dropped with
   its reason, and the paper's 5.17 row stops attributing the key to the
   recording policy.
7. `flatten_nested_eq_flat` and `flatten_nested_eq_admitted` carried three
   labels between them: DEFINITION-level in one paragraph of the paper's
   section 7.6, absent from that section's DEFINITION-level list, and PROVED in
   B5-NESTING-INVISIBLE.  Both are `rfl`.  They are now in the list and the
   ledger clause moves to DEFINITION-level, leaving the two blindness theorems
   as the entry's PROVED content.  One theorem, one label, in both places.
8. The receipt's own C5-7 evidence string still gave the address orbit as 4 / 1
   / 2 with no policy scope — the recording policy's numbers — which is the
   defect the previous repair scoped out of every prose site and missed in the
   one document the paper calls the authority.  The string now names the
   recording policy and reports what the same key reads at the two one-step
   policies beside it.  No value moves.

Carried: the Challenge 1 to Challenge 4 items already carried above are
unchanged; nothing new is carried.

## Gates run in this session

| gate | result |
|---|---|
| `verify_pins.py` | `pins ok: seed ba30bcd600d8 and 6 frozen prediction file(s)` |
| `unittest discover -s tests` | `Ran 400 tests`, OK in the rung; `Ran 405 tests`, OK after the review repair; `Ran 406 tests`, OK after the second review repair |
| `mypy` (strict, tree pyproject) | `Success: no issues found in 30 source files` |
| `coverage` + `check_coverage.py` | `line 100.00% branch 100.00% over 9 files` |
| `run_challenge0.py` … `run_challenge5.py` | `unchanged` for the first five receipts: 5553, 28363, 35499, 220518, 795960 bytes; `receipts/challenge5.json` was regenerated deliberately in the review repair, 123522 to 127455 bytes, and again in the second review repair, 127455 to 128086 bytes, with no injection live either time |
| `git diff --exit-code -- receipts` | clean |
| `verify_lean.py` | `lean ok: 177 axiom reports within ['Quot.sound', 'propext'], matching lean/axioms.txt`; the log was regenerated deliberately once, 139 to 177, with no injection live, and not at all in the review repair — no theorem was added, removed, or reproved |
| `ci/check_prose_watchlist.py` | `prose watchlist clean: 49 watched terms, 130 files with pinned hits, 1826 hits, census matches its pin`; no pin regenerated |
| `tests/test_primitive_contact.py` | firewall passes |
| `ci/check_paper_citations.py` | `paper cross-references resolve: 62 citation(s) across 29 document(s)` |
| injections | thirteen rows in `MANUAL.md` for this rung: **six injected and three found live** in the rung itself, two from the review repair and two from the second review repair — each of those four being a stale-receipt failure and a test-count grep.  One of the three found live, the audit-line loss during an injection reversal, also happened while an injection was live; it is counted once, under found-live, because no one planned it, and the overlap is named here rather than counted twice |

## Next session

The mandatory challenge sequence is finished.  The next stage is the seed's
section 4, the **autonomous continuation**, and it opens fresh: read the
handoff, the seed, `PLAN.md`, `MANUAL.md`, and this file; write and commit
`continuation/PREDICTIONS.md` with its own extrapolation before any code;
score C5-X.

The state the continuation inherits.  **Nothing was admitted at Challenge 5
beyond what a policy would admit, and no policy is taken.**  Under each reading
the current configuration is still the replay of the Challenge 4 caller history
— four marks, placement `(0, 1, 0, 1)`, labels `("a", "b", "b", "a")`, grouping
`(0, 0, 1, 1)` read off that history and carried by no regime.  Every minimum
of Challenges 3, 4 and 5 is a retained candidate, priced, and none is taken:
the permitted renamings, the judgment grammar, the serialization, and the
placement are exactly as Challenge 2 left them, and the state type is still one
side per mark.  A stage that wants a deep state must take the recording policy
and pay two capabilities.

What Challenge 5 adds to the inheritance: the third reader bound with its
declared depth; the four-member policy space with its three capabilities and
the naming coordinate beside them; the deep state type with its address, its
level exchanges and its flattening, which is the first state type this run has
declared beside the regime; the one-step rule stated in capabilities rather
than coordinates, with Challenge 4's identity of the two counts narrowed to
that rung's space; the declared 144-member domain of inscriptions and the
policy-sameness relation over it, a quotient over a FUNCTION rather than over a
state — that it is the run's first such is a reading of the earlier rungs' own
class keys and is computed by nothing here; and the Lean flattening and
continuation theorems.

For the continuation the seed asks, for each surviving branch under each
reading: its admitted data, operations, judgments, transition rules, historical
state and metatheoretic assumptions declared; the weakest deterministic finite
procedure that generates the next challenge from that branch alone, with a
proof that it imports no undeclared object-language structure; every minimum
response enumerated and ties preserved as branches; unresolved requirements
tracked; every branch replayed from its recorded history before certification;
and a branch stopped when no next challenge or no justified response exists.
Fifteen accepted rounds per finite branch is the bound; if the tree grows,
declare a smaller deterministic bound, export the exact frontier, and prove
what is complete within it.  Do not fabricate a linear sequence.  If the
generator proposes deeper nesting, it is priced under this rung's definitions
and is never free.  Freeze the predictions before looking.
