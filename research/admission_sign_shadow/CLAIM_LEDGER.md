# Claim ledger

`AuthorityEffect: None`.

The classes used here are `PROVED`, `CONDITIONAL`, `IMPORTED`, `REFUTED`, and
`OPEN`. A source-manifest match proves custody only; it never upgrades a claim.

## ASS-01 — local exchange action

- Class: `PROVED`
- Claim: the local two-history carrier is a free two-point exchange action
  with one local erased endpoint and a unique transporter.
- Lean: `histories_distinct`, `same_erased_endpoint`,
  `exchange_involutive`, `exchange_has_no_fixed_point`, `act_identity`,
  `act_composition`, `unique_transporter`.
- Python: `CharacterTests.test_exchange_is_free_involution_with_one_erasure`.
- Scope: local reconstruction only.

## ASS-02 — character classification

- Class: `PROVED`
- Claim: both trivial and sign characters satisfy the laws; these exhaust the
  local character maps, so the laws do not force nontriviality.
- Lean: `character_classification`, `trivial_and_sign_are_characters`,
  `character_laws_do_not_force_nontrivial`.
- Python: `CharacterTests.test_both_characters_exist_and_nontrivial_is_unique`.

## ASS-03 — conditional relative sign

- Class: `CONDITIONAL`
- Claim: if operational nontriviality is supplied, exchange has negative
  polarity uniquely; its declared integer encoding is `-1`. Relative labels
  are unique after a basepoint and otherwise differ by global negation.
- Lean: `nontrivial_exchange_is_negative`, `nontrivial_character_unique`,
  `nontrivial_exchange_toInt`,
  `operational_nontrivial_iff_labels_separate`, `sign_exchange_relative`,
  `sign_global_basepoint_flip`, `relative_label_classification`,
  `relative_label_unique_after_basepoint`, `global_neg_preserves_relative`.
- Python: `CharacterTests.test_global_basepoint_flip_is_relative`.
- Imported premise: operational nontriviality.

## ASS-04 — exact frozen facts and chosen correspondence

- Class: `PROVED` for the observed facts and chosen equivalence; `OPEN` for
  source authorization.
- Claim: the exact frozen histories and token-aware replay endpoints differ,
  while their erased replay endpoints agree. A post-seal chosen bijection to
  local `HistoryClass` commutes with the exchange transported through that
  bijection.
- Lean: `frozen_pair_observed_facts`, `chosen_pair_equivalence`,
  `erased_readout_cannot_separate`.
- Scope: `encode` and `sourceExchange` are metatheoretic definitions. The
  opposite orientation also works. No frozen theorem supplies or authorizes
  an exchange operation, and no unique correspondence is claimed.

## ASS-05 — canonical count no-determination

- Class: `PROVED`
- Claim: no function of the local ordered-deduplicated token list recovers the
  count of token `7` for every valid occurrence presentation.
- Lean: `canonical_forget_same_count_differs`,
  `canonical_data_does_not_determine_count`,
  `separating_weight_does_not_factor`, `zero_weight_factors_through_forget`.
- Python:
  `OccurrenceTests.test_canonical_forget_does_not_determine_count`.

## ASS-06 — declared occurrence algebra

- Class: `PROVED`
- Claim: within the declared occurrence presentation, count is zero on the
  empty list, additive on append, invariant under permutation, and its
  count-equivalence is an equivalence relation. Ordered forget is not a
  quotient of that equivalence.
- Lean: `occurrence_valid_append`, `countToken_nil`, `countToken_append`,
  `countToken_perm`, `occurrence_equivalent_refl`,
  `occurrence_equivalent_symm`, `occurrence_equivalent_trans`,
  `perm_occurrence_equivalent`,
  `count_equivalent_but_ordered_forget_differs`.
- Python: all `OccurrenceTests` reordering, validity, and equivalence cases.
- Scope: the occurrence presentation is declared; Genesis does not supply it.

## ASS-06A — exact retained-trace occurrence projection

- Class: `PROVED`, with a conditional integration boundary.
- Claim: a retained exact `List Derivation.TEvent` deterministically projects
  to occurrence records with consecutive IDs; count and canonical forgetting
  commute with that trace analysis. Injective ID renaming preserves validity,
  count, and forgetting.
- Lean: `occurrenceReplay_valid`, `occurrenceReplay_count`,
  `forget_occurrenceReplay_commutes`, `occurrenceValid_renameIds`,
  `duplicate_admission_endpoint_collision`.
- Python: all `ReplayOccurrenceTests`.
- Refuted stronger claim: `endpoint_does_not_determine_occurrence_count` and
  `endpoint_does_not_determine_occurrence_history` prove that the deduplicated
  endpoint cannot recover the trace projection.
- Integration boundary: the current connector does not yet consume the exact
  retained trace, so repository-wide import removal remains conditional.

## ASS-07 — count calibration

- Class: `CONDITIONAL`
- Claim: an integer encoding satisfying zero, addition, and unit laws equals
  the nonnegative integer embedding; calibrated occurrence weight therefore
  equals calibrated count.
- Lean: `count_calibration_unique`, `calibrated_occurrence_weight`,
  `occurrenceWeight_zero`, `occurrenceWeight_append`.
- Python: `OccurrenceTests.test_integer_map_is_an_explicit_argument`.
- Imported premise: the unit calibration laws.
- Negative closure: `additive_laws_do_not_select_integer_unit` exhibits the
  family of additive integer scales; `unit_calibration_is_conditional` proves
  uniqueness only after `encode 1 = 1` is supplied.

## ASS-08 — conditional finite contact

- Class: `CONDITIONAL`
- Claim: given an imported eligible exchange pair, operational
  nontriviality, the declared polarity calibration, and a separating mixer,
  the induced presentations have equal coordinate squares and different
  mixed readouts.
- Lean: `induced_coordinate_squares_equal`,
  `conditional_mixing_separation`, `square_mixing_separates`,
  `square_mixing_contact`.
- Python: `ConditionalContactTests.test_conditional_contact`.
- Imported or declared inputs: pair correspondence, nontriviality,
  calibration, mixer.

## ASS-09 — contact falsifiers

- Class: `PROVED`
- Claim: collapse and unequal endpoints invalidate pair eligibility; the
  trivial character produces no changed pair; a flat mixer does not separate;
  no fixed-point-free involution exists on the declared three-element carrier;
  two retained coordinates do not determine a third coordinate.
- Lean: `collapsed_pair_rejected`, `unequal_endpoints_rejected`,
  `trivial_character_rejected`, `trivial_character_no_pair_change`,
  `coordinate_data_does_not_force_mixing`, `three_cycle_is_not_involution`,
  `three_involution_has_fixed_point`, `no_free_three_involution`,
  `two_coordinates_do_not_determine_third`.
- Python: `ConditionalContactTests.test_required_mutations`.

## ASS-10 — section-type mismatch

- Class: `REFUTED`
- Claim refuted: either local section type determines the other without
  additional adapter data.
- Lean: `flip_family_has_no_natural_choice`,
  `report_section_does_not_determine_natural_choice`,
  `flip_family_has_no_adapter_kernel`, `empty_report_has_no_section`,
  `natural_choice_does_not_determine_report_section`.
- Python: `ConditionalContactTests.test_type_firewall_countermodel`.

## ASS-10A — exact actual-section adapter boundary

- Class: `CONDITIONAL` for adapter construction and `REFUTED` for derivation
  from a bare report section.
- Claim: `ActualSectionAdapter.Kernel` states the minimal `query`, report-fibre
  `pairOf`, and exact `PresIso.mapPair` commutation needed to produce the
  frozen `PresentationNaturality.Sec` and `IsNatural` types.
- Lean: `Kernel.toSec_isNatural`, `no_kernel_of_no_actual_section`,
  `report_section_does_not_determine_actual_section`,
  `fixed_point_free_family_has_no_kernel`.
- Open inputs: no existing source constructs `query`, `pairOf`, or
  `commutes`.

## ASS-11 — end-to-end connector

- Class: `OPEN`
- Produced: exact frozen observed facts, a chosen pair equivalence, an exact
  retained-trace occurrence projection, and the exact conditional adapter
  signature.
- Refuted as forced: operational nontriviality, endpoint recovery of
  occurrences, additive selection of the integer unit, and bare report-section
  production of an actual natural section.
- Required remaining composition: a source-authorized exchange/nontrivial
  sign, retained-trace connector input, supplied integer unit if integer
  output is required, and actual adapter fields.
- Terminal: `BRIDGE_PRODUCERS_PROVED_END_TO_END_OPEN`.
