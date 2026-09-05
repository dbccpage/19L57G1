# Claim ledger: the side-free control

Every claim this tree makes, with its status, what it rests on, what would
falsify it, and what survives it unanswered.  Identifiers are this tree's own
(`SF-*`); no identifier of any other tree appears here.

Statuses are drawn from the declared twelve: METATHEORY APPARATUS, SUPPLIED
DATUM, IMPOSED CHALLENGE, ADMITTED PRIMITIVE, DERIVED DEFINITION, PROVED
THEOREM, DETERMINISTIC COMPUTATION, COUNTERMODEL, OPTIONAL REALIZATION,
CONJECTURE, OPEN OBSTRUCTION, REFUTED CLAIM.  A claim that is true by
unfolding a declaration is additionally marked **DEFINITION-level** and is
never counted as content.

---

### SF-CARRIER-NOTHING-ADMITTED

* **Statement.**  This tree admits no primitive.  Its carrier is a regime with
  one variable field, the labels of the admitted marks in admission order.
* **Status.**  DERIVED DEFINITION.
* **Depends on.**  Nothing.
* **Assumes.**  That the pinned carrier's placement index space and its mark
  index space are the same set, which the pinned validator enforced by
  refusing any regime whose two tuples differ in length.
* **Python evidence.**  `code/sidefree/model.py`; `tests/test_model.py`.
* **Lean.**  `SideFree.Regime`, `SideFree.genesis`.
* **Axiom report.**  `SideFree.genesis_size` — no axioms.
* **Falsifier.**  A second variable field, or any state change outside an
  admission event.
* **Surviving boundary.**  None.

### SF-SUPPLY-INERT

* **Statement.**  The external presentation event changes no admitted state.
* **Status.**  PROVED THEOREM.
* **Depends on.**  SF-CARRIER-NOTHING-ADMITTED.
* **Assumes.**  Nothing.
* **Python evidence.**  `tests/test_model.py::Events::test_supply_changes_no_state`.
* **Lean.**  `SideFree.supply_no_op`, `SideFree.replay_supply_inert`,
  `SideFree.supply_is_not_an_admission`.
* **Axiom report.**  All three: no axioms.
* **Falsifier.**  A regime that differs after a presentation event.
* **Surviving boundary.**  None.

### SF-ADMISSION-ONLY

* **Statement.**  Admitted state changes only through an admission event, and
  every certified regime is the replay of an explicit history from genesis.
* **Status.**  PROVED THEOREM (Lean) and DETERMINISTIC COMPUTATION (every row).
* **Depends on.**  SF-CARRIER-NOTHING-ADMITTED.
* **Assumes.**  The Lean carrier is total and carries no refusals; every
  refusal of the Python carrier is a declaration about well-formed histories.
  This is stated in the Lean file rather than left for a reader to find.
* **Python evidence.**  Every row's `certified` and `replays_from_genesis`
  fields; `tests/test_control.py::Enumerator::test_every_row_replays_from_genesis_and_agrees_with_its_carrier`.
* **Lean.**  `SideFree.step_changes_only_by_admission`,
  `SideFree.replay_deterministic`, `SideFree.replay_append`,
  `SideFree.retained_replays_from_genesis`,
  `SideFree.retainedPlus_replays_from_genesis`.
* **Axiom report.**  All five: no axioms.
* **Falsifier.**  A row whose regime is not its history's replay.
* **Surviving boundary.**  None.

### SF-REQUIREMENT-INHERITED

* **Statement.**  The requirement and its second reading are the pinned texts
  with one declared phrase deleted each, byte for byte, and neither control
  string names any word the deletion removes.
* **Status.**  IMPOSED CHALLENGE.
* **Depends on.**  The vendored pin (SF-PIN).
* **Assumes.**  That deleting the tower index leaves the same requirement.
  This is a translation claim, and G4 is what checks it mechanically rather
  than by assertion.
* **Python evidence.**  Gate G2; `tests/test_space.py::Requirement`;
  the injection I3 in `MANUAL.md`.
* **Lean.**  None; the requirement is a text, not a theorem.
* **Axiom report.**  Not applicable.
* **Falsifier.**  Either deletion failing byte for byte, or a deleted word
  appearing in a control string.
* **Surviving boundary.**  The premise that a candidate's permitted renamings
  are closed under composition and inverse is inherited as OPEN — SF-OPEN-C.

### SF-TRANSLATION-REPLAYS

* **Statement.**  This tree's own verdict function, applied to the pinned
  world's own recorded automorphism sets, reproduces the pinned world's own
  recorded answers on all fourteen rows the minimum ranges over.
* **Status.**  DETERMINISTIC COMPUTATION.  **This is the load-bearing tie**
  between the two worlds, and it uses no re-declaration of anything.
* **Depends on.**  SF-PIN.
* **Assumes.**  Nothing beyond the pinned bytes.
* **Python evidence.**  Gate G4, 14 rows, 14 agreements;
  `tests/test_control.py::Gates`; the mutation probe in the same class.
* **Lean.**  None.
* **Axiom report.**  Not applicable.
* **Falsifier.**  Any disagreement — which VOIDS the run.
* **Surviving boundary.**  G4 is total over what the minimum is computed FROM,
  not over all 48 points per reading; a defect in a bundle row's recorded
  verdict is invisible to it.

### SF-FORGETFUL-LEMMA

* **Statement.**  Whatever renaming carries a side-typed regime — or its
  exchange — onto itself, the same renaming carries the forgotten regime onto
  itself.  Corollary: side-free separation implies side-typed separation.
* **Status.**  PROVED THEOREM (Lean, unbounded) with a bounded Python census
  as its cross-check.
* **Depends on.**  SF-CARRIER-NOTHING-ADMITTED, SF-MIRROR.
* **Assumes.**  In Lean, that a renaming acts by reading marks at indices; the
  proof needs no permutation property, which is strictly stronger than needed.
* **Python evidence.**  Gate G5: 1344 cells, 2140 automorphisms checked, 0
  violations, 0 corollary violations, 228 non-vacuity cells;
  `tests/test_mirror.py::Forgetting`; injection I6 in `MANUAL.md`.
* **Lean.**  `SideFree.forgetful_lemma_keeping_labels`,
  `SideFree.forgetful_lemma_forgetting_labels`,
  `SideFree.free_separation_implies_sided_separation`,
  `SideFree.free_separation_implies_sided_separation_forgetting_labels`,
  `SideFree.forget_rename`, `SideFree.forget_reflect`,
  `SideFree.reorder_map`, `SideFree.reorder_length_congr`.
* **Axiom report.**  Within `{propext, Quot.sound}`; the two label-forgetting
  statements and `reorder_length_congr` use both, the rest `propext` alone.
* **Falsifier.**  Any violating cell with no injection live.
* **Surviving boundary.**  The lemma is about the two carriers declared here.
  That the mirror is the pinned carrier is not claimed; see SF-MIRROR.

### SF-FAIRNESS-SIGN

* **Statement.**  The instrument cannot return a negative difference: the
  pinned minimum is at most the side-free minimum, so a tie is the strongest
  statement available against the admitted primitive.
* **Status.**  PROVED THEOREM (the corollary of SF-FORGETFUL-LEMMA), together
  with the DETERMINISTIC COMPUTATION that every side-free candidate has a
  side-typed counterpart at the same capability count.
* **Depends on.**  SF-FORGETFUL-LEMMA, SF-CAPABILITY-TEXTS.
* **Assumes.**  The counterpart map is the collapse map declared in
  `pinned/BOUNDARY_PIN.json`.
* **Python evidence.**  The route table's four joined rows; gate G5's
  `sign_consequence` field.
* **Lean.**  The two `free_separation_implies_sided_separation` theorems.
* **Falsifier.**  A negative `delta_vs_unnamed`.
* **Surviving boundary.**  None within the declared space.

### SF-CAPABILITY-TEXTS

* **Statement.**  The three surviving coordinates carry their pinned
  capability sentences byte-identical, their names are string-identical, and
  the partition into surviving and deleted is the mechanical one: a coordinate
  transfers exactly when its pinned sentence contains no whole word *side* or
  *sides*.
* **Status.**  DETERMINISTIC COMPUTATION.
* **Depends on.**  SF-PIN.
* **Assumes.**  That the mechanical criterion is the right criterion.  It is
  declared, not derived; what is checked is that it partitions the pinned five
  with no borderline case and that its partition equals the implemented one.
* **Python evidence.**  Gate G3; `tests/test_space.py::DeletionCriterion`;
  injections I4, I5, I10.
* **Lean.**  None.
* **Falsifier.**  One altered character, one renamed coordinate, or a widened
  criterion — each of which was injected and each of which fired.
* **Surviving boundary.**  Whether the criterion is the right one is a
  judgement about words, not a computation.

### SF-MINIMUM

* **Statement.**  Within the three declared coordinates, at the pinned
  requirement and prices, at the retained two-mark configuration, under
  `mu1`: the side-free minimum is **1**, attained by exactly **one**
  non-isomorphic class, `{withdraw_mark_permutations}`.
* **Status.**  DETERMINISTIC COMPUTATION.
* **Depends on.**  SF-CARRIER-NOTHING-ADMITTED, SF-REQUIREMENT-INHERITED,
  SF-CAPABILITY-TEXTS.
* **Assumes.**  The declared exhaustiveness scope, inherited from the pinned
  world and widened by one clause: no augmentation admitting a new per-mark
  datum is enumerated.
* **Python evidence.**  `receipts/side_free.json`, `decided.side_free_minimum`
  and `decided.side_free_classes`; `control.minima_by_mu1`.
* **Lean.**  `SideFree.base_exchange_is_an_automorphism`,
  `SideFree.exchange_moves_zero_to_one`,
  `SideFree.keep_labels_exchange_is_an_automorphism`,
  `SideFree.extra_mark_exchange_is_an_automorphism`,
  `SideFree.withdrawal_does_not_move_zero_to_one` — the four rows, at the
  retained regime, in Lean.
* **Axiom report.**  `propext` for each of the five.
* **Falsifier.**  Any other one-step candidate satisfying, or that one
  failing, or a class count above 1.
* **Surviving boundary.**  The minimum is attained **by unfolding** — see
  SF-DEFINITION-LEVEL — and the scope is these three coordinates and no wider.

### SF-DEFINITION-LEVEL

* **Statement.**  `withdraw_mark_permutations` satisfies the requirement by
  unfolding the declaration: with no permitted renaming that moves an index,
  no renaming carries one mark to another.
* **Status.**  DERIVED DEFINITION, marked **DEFINITION-level**, never counted
  as content.
* **Depends on.**  SF-MINIMUM.
* **Assumes.**  Nothing.
* **Python evidence.**  The COMPUTED field
  `no_permitted_renaming_moves_an_index`, reported beside the verdict rather
  than asserted; the route census, 4 of 4.
* **Lean.**  `SideFree.withdrawal_moves_no_index`,
  `SideFree.exchange_is_not_the_identity` (which shows the withdrawal is a
  real restriction and not a vacuous one).
* **Falsifier.**  The flag computing false while the row satisfies.
* **Surviving boundary.**  Whether the requirement should have been declared
  so as to exclude such a route is SF-OPEN-D.

### SF-DIFFERENCE

* **Statement.**  `delta_vs_unnamed = 0` and `delta_vs_named = +1`.  The
  admitted primitive reduced the price of the required separation by ZERO
  under the unnamed reading and by ONE under the named reading.
* **Status.**  DETERMINISTIC COMPUTATION.
* **Depends on.**  SF-MINIMUM, SF-TRANSLATION-REPLAYS, SF-FAIRNESS-SIGN,
  SF-MIRROR.
* **Assumes.**  The cross-world join by string equality on the coordinate
  names, and the declared collapse map for the two pinned further-mark points.
* **Python evidence.**  `decided.delta_vs_unnamed`, `decided.delta_vs_named`,
  `decided.what_the_admitted_primitive_bought = NOTHING_IN_COST`.
* **Lean.**  None; the difference is a computation over two enumerations.
* **Falsifier.**  Either delta differing; a disagreeing route table cell other
  than `extra_mark`.
* **Surviving boundary.**  Scoped to these three coordinates, this
  requirement, this configuration and this measure.  It is **not** the claim
  that the admitted primitive bought nothing — see SF-TERMINAL.

### SF-ROUTES

* **Statement.**  What the admitted primitive bought under the unnamed reading
  is **two additional routes at the same price**: `withdraw_reflection` and
  `extra_mark`, both mediated by the sides.
* **Status.**  DETERMINISTIC COMPUTATION.
* **Depends on.**  SF-DIFFERENCE.
* **Assumes.**  The collapse map.
* **Python evidence.**  `decided.routes_the_admitted_primitive_bought`,
  `decided.routes_bought_count`.
* **Falsifier.**  Any other member set.
* **Surviving boundary.**  Routes and price are separate columns and are never
  summed; a test asserts no receipt field combines them.

### SF-REFUTED-DEPENDENCE

* **Statement.**  The pinned clause that *every* separation result of that
  rung requires the admitted primitive is **REFUTED** — within the scope of
  this declared carrier, these three coordinates and this eight-point
  enumeration, and nowhere wider.
* **Status.**  REFUTED CLAIM.
* **Depends on.**  SF-MINIMUM, SF-CAPABILITY-TEXTS.
* **Assumes.**  That `withdraw_mark_permutations` is one of that rung's
  separation results, which the pinned receipt shows by retaining it as one of
  its three tied minima.
* **Python evidence.**  The control's `withdraw_mark_permutations` row, which
  is formulated after removing the admitted primitive, costs the same, and
  satisfies the same requirement; `withdrawal_port.same_cost`.
* **Falsifier.**  That coordinate failing side-free, or costing more.
* **Surviving boundary.**  The refutation is of one clause at one rung.  The
  clause's other conjuncts — the side exchange, the two side mark properties,
  the counterfactual square — are untouched, and this tree does not price
  them.

### SF-MIRROR

* **Statement.**  The mirror is this tree's own re-declaration of a side-typed
  carrier, used only as the domain of the lemma and the censuses, and it
  reproduces the pinned vector on all 48 rows per reading.
* **Status.**  COUNTERMODEL — specifically a countermodel-domain object.
* **Depends on.**  SF-PIN.
* **Assumes.**  Nothing; a divergence VOIDS the run rather than adjusting it.
* **Python evidence.**  Gate G6, 96 rows compared;
  `tests/test_mirror.py::MirrorAgainstThePin`.
* **Falsifier.**  Any divergence on any row, minimum or class.
* **Surviving boundary.**  **It is never claimed to be the pinned carrier.**
  The load-bearing tie is SF-TRANSLATION-REPLAYS, which uses no
  re-declaration.

### SF-PIN

* **Statement.**  `pinned/boundary_challenge3.json` is the pinned receipt's
  bytes: sha256 `e4904075aaa07dd05a2f9d0cba313e77b6eb965a44efecb5cff51864f70a64ab`,
  git blob `dbb4cce3cdd49d15d0784c2a73bf7afeab9de7a0`, 220518 bytes, no CR,
  committed `-text`.
* **Status.**  METATHEORY APPARATUS.
* **Depends on.**  Nothing; the three digests need no git.
* **Assumes.**  For the fourth, conditional check: that the pinned commit is
  reachable.
* **Python evidence.**  Gate G1; `verify_pins.py`; injections I1 and I14.
* **Falsifier.**  Any digest, the byte count, a CR byte, or a blob at the
  pinned commit differing.
* **Surviving boundary.**  **Live residual.**  The pinned commit is on an
  unmerged branch; in CI the conditional check is a reported SKIP and the
  bytes are held by their digests alone.  Re-take the pin when that branch
  merges.

### SF-OBSERVATION-INERT

* **Statement.**  The one positive judgment form, `Admitted`, separates the
  two retained marks at no cell of the control's route census.
* **Status.**  DETERMINISTIC COMPUTATION.
* **Depends on.**  SF-CARRIER-NOTHING-ADMITTED.
* **Assumes.**  That `Admitted` is the honest residue of the pinned side
  judgment, which the pinned source bears out: that judgment is literally the
  conjunction of "the mark is admitted" and a placement test.
* **Python evidence.**  `observation_grammar.inert`;
  `tests/test_space.py::MarkProperties`.
* **Lean.**  `SideFree.no_judgment_at_genesis`, `SideFree.retained_judgments`.
* **Falsifier.**  Any census cell at which it separates.
* **Surviving boundary.**  Inertness is over the declared census, not over
  every conceivable regime.

### SF-SUBJECT-REFUSED

* **Statement.**  Under the pinned shared identity policy the control retains
  ONE mark, so the requirement has no subject and the retained-mark check
  raises by name.  This is a refusal of the subject, never a false and never a
  satisfied requirement.
* **Status.**  DETERMINISTIC COMPUTATION.
* **Depends on.**  SF-CARRIER-NOTHING-ADMITTED.
* **Assumes.**  Occurrence identity is inherited already paid, exactly as the
  pinned world pays it one rung earlier.
* **Python evidence.**  `identity_policies.shared_policy`;
  `tests/test_control.py::Policies`.
* **Lean.**  `SideFree.shared_policy_retains_one_mark`.
* **Axiom report.**  No axioms.
* **Falsifier.**  Two marks under the shared policy, or a `false` reported
  where a refusal is due.
* **Surviving boundary.**  None.

### SF-REMOVED-REFUSAL

* **Statement.**  The pinned refusal of an admission that would move a mark to
  the other side is REMOVED, not absorbed: it has no side-free statement, and
  what is left in its place is exactly a no-op with nothing hidden inside it.
* **Status.**  METATHEORY APPARATUS (a recorded deletion).
* **Depends on.**  SF-CARRIER-NOTHING-ADMITTED.
* **Python evidence.**  `identity_policies.removed_refusal` and its computed
  consequence; `DELETED.md`.
* **Falsifier.**  The refusal firing, or the no-op changing state.
* **Surviving boundary.**  None.

### SF-DELETION-TOTAL

* **Statement.**  The deletion register's population is the mechanical closure
  over the pinned source's own names — 105 entries, 69 deleted and 36 narrowed
  — no deleted name survives in the side-free modules, and no narrowed name is
  absent from them.
* **Status.**  DETERMINISTIC COMPUTATION, with one judgement inside it.
* **Depends on.**  SF-PIN.
* **Assumes.**  The declared word stems.  Whether they are the right stems is
  a judgement about words, not a computation, and is recorded as such.
* **Python evidence.**  `deletion_register.totality`;
  `tests/test_deletion.py`; injection I7.  The population check is conditional
  on the pinned commit and SKIPS with its reason when unreachable.
* **Falsifier.**  A surviving deleted name, an absent narrowed one, or a stem
  leak outside the six-name allowlist.
* **Surviving boundary.**  `mirror.py` and `control.py` are excluded from the
  scan **by declaration**, because both must be able to name the deleted
  structure in order to compare against it.

### SF-SECONDARY

* **Statement.**  Excluding every candidate that separates at every cell of
  its own world's route census, the control has NO satisfying candidate while
  the unnamed reading still has three at price one in two classes.  The answer
  flips.
* **Status.**  DETERMINISTIC COMPUTATION, declared in advance and **never
  deciding**.
* **Depends on.**  SF-MINIMUM, SF-DEFINITION-LEVEL.
* **Assumes.**  The route census domain declared in `DESIGN.md` §9.
* **Python evidence.**  `secondary.decided`; prediction P25.
* **Falsifier.**  The control retaining a satisfying candidate under the
  exclusion, or the unnamed reading losing one.
* **Surviving boundary.**  The primary counts the vacuous route, because
  excluding it in the control while it stands in the pinned world would itself
  be the rigging.  Both numbers are frozen precisely because the answer flips.

### SF-TERMINAL

* **Statement.**  The admitted primitive bought **no price that the admission
  order could not buy at the same price**, within the declared scope.
* **Status.**  DETERMINISTIC COMPUTATION, scoped.
* **Depends on.**  SF-DIFFERENCE, SF-DEFINITION-LEVEL, SF-SECONDARY.
* **Assumes.**  Nothing further.
* **Python evidence.**  `terminal.sentence`,
  `terminal.sentence_is_the_scoped_one`.
* **Falsifier.**  The unscoped sentence — "the admitted primitive bought
  nothing" — being written anywhere as this tree's result.
* **Surviving boundary.**  SF-OPEN-A: whether an order is itself a container.

---

## Open obstructions

### SF-OPEN-A — is the admission order a container?

What pays for separation in a world with no container is the admission order.
This control prices that route; it does not decide what kind of thing an order
is.  **OPEN OBSTRUCTION.**

### SF-OPEN-B — the price of re-purchasing a per-mark two-valued datum

Outside the pinned candidate space, therefore priced in neither world.
Allowing it would price a route the pinned world was never charged for either,
and it answers a different question: the PRICE of rebuilding the admitted
primitive, not the WORTH of having it free.  **OPEN OBSTRUCTION.**

### SF-OPEN-C — closure of the permitted renamings

The pinned premise that a candidate's permitted renamings are closed under
composition and inverse is inherited, stated, and checked by nothing.  It is
not treated as discharged by the renaming set having shrunk.
**OPEN OBSTRUCTION.**

### SF-OPEN-D — should the requirement have excluded a vacuous route?

The pinned tree retains a route that satisfies its requirement without reading
anything, and records this question as OPEN.  This control inherits it.
**OPEN OBSTRUCTION.**
