# The deletion register

Everything the deletion removed from the pinned carrier, and everything it
narrowed instead, with the reason for each.  This is the closure the design
calls for, and it is checked rather than asserted.

## How the population is fixed

The set of names below is enumerated **independently of the classification**,
from the pinned source at the pinned commit:

* the **direct seed** is every pinned defined name -- module constant,
  function, class, dataclass field or parameter -- whose name carries one of
  the deleted word components: *side*, *sides*, *placement*, *reflect*,
  *reflection*, *reading*, *readings*, *convention*, *conventions*, *near*,
  *far*;
* the **closure** is every pinned top-level definition whose own body reaches
  one of those names.

`tests/test_deletion.py` recomputes that population and requires it to equal
the register exactly, in both directions. It needs the landed pinned commit
and fails if its source is unavailable. Everything else on this page needs
no git at all. Later source definitions are classified as absent here, not
imported as additional control operations; the comparison scope is unchanged.

## How the classification is fixed, and how it is held

The kind of each entry -- DELETED or NARROWED -- is **declared** here.  It was
arrived at by reading this tree's own modules, and it is held in both
directions by tests that do not use the classifier's own pattern:

* every DELETED name must be **absent** from the identifier census of the
  side-free modules;
* every NARROWED name must be **present** in it;
* no identifier of those modules may carry a deleted word component at all,
  outside a declared allowlist of six names, each with its reason.

The census is read from the **syntax tree**, not from the text.  A deleted
word inside a comment or a doc string is how a deletion gets explained, and
must never be mistaken for a use of it.

## What is scanned, and what is not

Scanned: `model.py`, `presentation.py`, `requirement.py`, `candidates.py`,
`enumerate.py` -- the side-free carrier proper and the generic enumerator.

Excluded **by declaration**, and named here rather than left implicit in a
glob: `mirror.py`, which is the side-typed countermodel-domain object, and
`control.py`, which is the comparison driver.  Both must be able to NAME the
deleted structure in order to compare against it.

## The removed refusal

The pinned carrier refuses an admission that would move an already-admitted
mark to the other side.  That refusal is **REMOVED, not absorbed**: it has no
side-free statement at all, because with no sides there is nowhere to move a
mark to.  It is recorded here rather than quietly folded into the no-op, and
its computed consequence -- that a second label-keyed admission of an already
admitted label is exactly a no-op, with nothing hidden inside it -- is
reported in the receipt beside the two identity policies.

## The allowlist

Six identifiers of the side-free modules carry a deleted word component and
are allowed anyway.  Two kinds appear, and no third.

| identifier | why it is allowed |
|---|---|
| `DELETED_FROM_SECOND_READING` | 'reading' in its other pinned sense: a second way of reading the imposed challenge, not the index over the two sides |
| `PINNED_COLLATERAL_FACTS_WITHOUT_A_SIDE_FREE_SUBJECT` | the declared list of pinned facts that have no side-free subject |
| `REQUIREMENT_SECOND_READING` | 'reading' in its other pinned sense: a second way of reading the imposed challenge, not the index over the two sides |
| `SideFreeCarrier` | the name of the control carrier itself |
| `_SIDE_WORD` | the deletion criterion's own pattern; it must spell what it deletes |
| `satisfies_second_reading` | 'reading' in its other pinned sense: a second way of reading the imposed challenge, not the index over the two sides |

## DELETED: 83 names, absent from the side-free modules

| name | reason |
|---|---|
| `CONVENTIONS` | direct: the name carries the deleted component conventions |
| `DECLARED_CONVENTION` | direct: the name carries the deleted component convention |
| `DeepRegime` | via: its pinned definition reaches READINGS, reading, side |
| `Renamings` | via: its pinned definition reaches reflection |
| `_read_nested` | via: its pinned definition reaches _split_sides |
| `_split_sides` | direct: the name carries the deleted component sides |
| `configurations_isomorphic` | via: its pinned definition reaches reading |
| `deep_genesis` | via: its pinned definition reaches reading |
| `deep_is_isomorphic` | via: its pinned definition reaches reading |
| `deep_rename_marks` | via: its pinned definition reaches reading |
| `deep_serialize` | via: its pinned definition reaches reading |
| `deep_step` | via: its pinned definition reaches reading, side |
| `exchange_level` | via: its pinned definition reaches reading, side |
| `flatten_deep` | via: its pinned definition reaches reading |
| `pair_marks` | via: its pinned definition reaches admitted_side, convention |
| `permitted_configuration_images` | via: its pinned definition reaches reflection |
| `OTHER_CONVENTION` | direct: the name carries the deleted component convention |
| `OnSide` | direct: the name carries the deleted component side |
| `PRESENTED_SIDES` | direct: the name carries the deleted component sides |
| `READINGS` | direct: the name carries the deleted component readings |
| `READING_O` | direct: the name carries the deleted component reading |
| `READING_O_BUNDLE` | direct: the name carries the deleted component reading |
| `READING_U` | direct: the name carries the deleted component reading |
| `REQUIREMENT_READINGS_AGREE_BECAUSE` | direct: the name carries the deleted component readings |
| `SIDE_NAMES` | direct: the name carries the deleted component side |
| `SideNamed` | direct: the name carries the deleted component side |
| `admitted_side` | direct: the name carries the deleted component side |
| `convention` | direct: the name carries the deleted component convention |
| `convention_facts` | direct: the name carries the deleted component convention |
| `different_sides_census` | direct: the name carries the deleted component sides |
| `expected_placement` | direct: the name carries the deleted component placement |
| `is_automorphism_reflection` | direct: the name carries the deleted component reflection |
| `mark_side` | direct: the name carries the deleted component side |
| `marks_on_different_sides` | direct: the name carries the deleted component sides |
| `on_side_0` | direct: the name carries the deleted component side |
| `on_side_1` | direct: the name carries the deleted component side |
| `other_convention` | direct: the name carries the deleted component convention |
| `placement` | direct: the name carries the deleted component placement |
| `presented_side` | direct: the name carries the deleted component side |
| `reading` | direct: the name carries the deleted component reading |
| `reading_facts` | direct: the name carries the deleted component reading |
| `reflect` | direct: the name carries the deleted component reflect |
| `reflection` | direct: the name carries the deleted component reflection |
| `reflection_permitted` | direct: the name carries the deleted component reflection |
| `refused_under_every_convention` | direct: the name carries the deleted component convention |
| `side` | direct: the name carries the deleted component side |
| `side_exchange` | direct: the name carries the deleted component side |
| `side_exchanging_automorphism` | direct: the name carries the deleted component side |
| `side_exchanging_automorphism_under` | direct: the name carries the deleted component side |
| `side_profile` | direct: the name carries the deleted component side |
| `sides_collapsed` | direct: the name carries the deleted component sides |
| `sides_fact_agrees_with_the_requirement` | direct: the name carries the deleted component sides |
| `withdraw_reflection` | direct: the name carries the deleted component reflection |
| `automorphism_facts` | via: its pinned definition reaches reflect, side_exchange, side_exchanging_automorphism |
| `build` | via: its pinned definition reaches READING_O, READING_U, REQUIREMENT_READINGS_AGREE_BECAUSE |
| `canonical` | via: its pinned definition reaches READING_U, reading, reflect |
| `class_key` | via: its pinned definition reaches reading |
| `contents` | via: its pinned definition reaches placement, side |
| `counterfactual_square` | via: its pinned definition reaches _convention, reading, reflection_permitted |
| `fixed_up_to_mark_renaming` | via: its pinned definition reaches reflect |
| `identity_policy_facts` | via: its pinned definition reaches CONVENTIONS, convention, refused_under_every_convention |
| `isomorphism_witness` | via: its pinned definition reaches reading |
| `label_facts` | via: its pinned definition reaches placement, reading |
| `later_event_facts` | via: its pinned definition reaches OnSide, mark_side |
| `mark_form_invariant` | via: its pinned definition reaches OnSide, side |
| `name_observations` | via: its pinned definition reaches READING_U, SIDE_NAMES, SideNamed |
| `names_admitted` | via: its pinned definition reaches READING_O, reading |
| `one_step_detail` | via: its pinned definition reaches DECLARED_CONVENTION, SIDE_NAMES, _convention |
| `orbit_property_separates` | via: its pinned definition reaches _reflection, reading |
| `order_facts` | via: its pinned definition reaches DECLARED_CONVENTION, placement |
| `permitted_images` | via: its pinned definition reaches READING_U, reading, reflect |
| `point_row` | via: its pinned definition reaches _convention, reading |
| `policy_event` | via: its pinned definition reaches side |
| `policy_facts` | via: its pinned definition reaches convention, placement |
| `price_facts` | via: its pinned definition reaches READING_O, reading |
| `process_admission_facts` | via: its pinned definition reaches DECLARED_CONVENTION, reading |
| `regime_domain` | via: its pinned definition reaches placement, reading |
| `requirement_met` | via: its pinned definition reaches reading |
| `retained_facts` | via: its pinned definition reaches DECLARED_CONVENTION, marks_on_different_sides, placement |
| `score` | via: its pinned definition reaches SIDE_NAMES, withdraw_reflection |
| `score_c1x` | via: its pinned definition reaches SIDE_NAMES |
| `separating_mark_forms` | via: its pinned definition reaches OnSide, side |
| `separation_facts` | via: its pinned definition reaches READING_O, SIDE_NAMES, mark_side |

## NARROWED: 36 names, present under a narrowed meaning

| name | reason |
|---|---|
| `REQUIREMENT_SECOND_READING` | direct: the name carries the deleted component reading |
| `AdmitMark` | via: its pinned definition reaches side |
| `AdmitOccurrence` | via: its pinned definition reaches side |
| `Augmentation` | via: its pinned definition reaches withdraw_reflection |
| `DECLARED_MARK_PROPERTIES` | via: its pinned definition reaches on_side_0, on_side_1 |
| `OBSERVATION_TYPES` | via: its pinned definition reaches OnSide, SideNamed |
| `Observation` | via: its pinned definition reaches OnSide, SideNamed |
| `Regime` | via: its pinned definition reaches READINGS, placement, reading |
| `Whole` | via: its pinned definition reaches PRESENTED_SIDES, presented_side |
| `admission_event` | via: its pinned definition reaches admitted_side, convention, presented_side |
| `automorphisms_under` | via: its pinned definition reaches reflection |
| `caller_history` | via: its pinned definition reaches admitted_side, convention, presented_side |
| `candidate_history` | via: its pinned definition reaches convention |
| `canonical_under` | via: its pinned definition reaches reflection |
| `changed_coordinates` | via: its pinned definition reaches withdraw_reflection |
| `collateral_facts` | via: its pinned definition reaches other_convention, reading, side_exchanging_automorphism_under |
| `comparison_regimes` | via: its pinned definition reaches DECLARED_CONVENTION, OTHER_CONVENTION, other_convention |
| `domain_images` | via: its pinned definition reaches reflection |
| `effective_structure` | via: its pinned definition reaches reading, reflection_permitted |
| `event_json` | via: its pinned definition reaches side |
| `flags` | via: its pinned definition reaches reading, reflection_permitted |
| `genesis` | via: its pinned definition reaches reading |
| `is_isomorphic_under` | via: its pinned definition reaches reading, reflection |
| `mark_automorphism_to_under` | via: its pinned definition reaches reflection |
| `mark_observations` | via: its pinned definition reaches OnSide, placement |
| `mark_orbit_under` | via: its pinned definition reaches reflection |
| `mark_profile` | via: its pinned definition reaches OnSide |
| `marks_separable_under` | via: its pinned definition reaches reflection |
| `observation_holds` | via: its pinned definition reaches OnSide, READING_O, SIDE_NAMES |
| `permitted_images_under` | via: its pinned definition reaches reflect, reflection |
| `property_domain` | via: its pinned definition reaches placement, reading |
| `relabelled` | via: its pinned definition reaches placement, reading |
| `rename_marks` | via: its pinned definition reaches placement, reading |
| `serialize` | via: its pinned definition reaches placement, reading |
| `serialize_keeping_labels` | via: its pinned definition reaches placement, reading |
| `step` | via: its pinned definition reaches placement, reading, side |
