# The price list: the pinned world beside the side-free control

Rendered from `receipts/comparison.json` by `run_comparison.py`.  Every number, name and sentence below is carried by that record; this file adds nothing to it and is regenerated rather than edited.

The price list: what each world can say at the pinned rungs, what each says it costs, and what the admitted primitive bought.  Every row is computed from a pinned receipt or from a carrier; no boundary number is typed in.

Pinned commit `5c43c5ee`.  The blob at the pinned commit when that commit is reachable, and the vendored copy otherwise; both are held to the one declared sha256, so the rows are the same either way.

| challenge | vendored copy | sha256 | bytes |
|---|---|---|---|
| 0 | `pinned/boundary_challenge0.json` | `7441796b5265` | 5553 |
| 1 | `pinned/boundary_challenge1.json` | `de48399f3fe5` | 28363 |
| 2 | `pinned/boundary_challenge2.json` | `ca6a9f935951` | 35499 |
| 3 | `pinned/boundary_challenge3.json` | `e4904075aaa0` | 220518 |

SOURCE_MANIFEST.json, which is one of the three files this tree's source-isolation scan carves for naming the pinned tree. This record cites the local vendored copies instead, so the carve stays exactly three files wide.

A record that carried it would not be the same file in a clone that cannot reach the pinned commit.  run_comparison.py prints the reachability report instead, so it is never silent.

## Gates

| gate | name | passed |
|---|---|---|
| C0 | `pinned_bytes_ok` | true |
| C1 | `declared_values_agree` | true |
| C2 | `receipt_agrees` | true |
| C3 | `minimum_join` | true |
| C4 | `taxonomy_total` | true |

All gates passed: true.

## The rows

A row is in BOUGHT_NOTHING exactly when the control reaches the same value at the same stated price; in BOUGHT_SOMETHING when either differs; and in ABSENT when the notion has no statement in one world, which is evidence for neither bucket.

### genesis

| id | kind | item | unnamed reading | named reading | control | difference vs unnamed | status |
|---|---|---|---|---|---|---|---|
| R01 | what holds | marks admitted at genesis | `0` | `0` | `0` | same | BOUGHT_NOTHING |
| R02 | declared structure | the declared observation vocabulary | `["OnSide", "SideNamed"]` | `["OnSide", "SideNamed"]` | `["Admitted"]` | only pinned `["OnSide", "SideNamed"]`; only control `["Admitted"]` | BOUGHT_SOMETHING |
| R03 | what holds | judgments holding at genesis | `0` | `2` | `0` | same | BOUGHT_NOTHING |
| R04 | declared structure | the serialization key at genesis | `["U", []]` | `["O", []]` | `[0]` | only pinned `["U", []]`; only control `[0]` | BOUGHT_SOMETHING |
| R05 | declared structure | the two sides are collapsed at genesis | `true` | `false` | ABSENT -- the notion names a side, and a world with no sides cannot state it | absent in the control | ABSENT |
| R06 | event discipline | an external presentation leaves admitted state unchanged | `true` | `true` | `true` | same | BOUGHT_NOTHING |
| R07 | event discipline | no event is entailed by admitted state | `true` | `true` | `true` | same | BOUGHT_NOTHING |

* **R03.** The named reading's two judgments hold before any mark is admitted, and the control cannot hold them at any price: a container exists before its contents, an admission order does not.

### one admitted mark

| id | kind | item | unnamed reading | named reading | control | difference vs unnamed | status |
|---|---|---|---|---|---|---|---|
| R08 | declared structure | admissions available from the one supplied token | `2` | `2` | `1` | control minus boundary = -1 | BOUGHT_SOMETHING |
| R09 | declared structure | isomorphism classes of those admissions | `1` | `2` | `1` | same | BOUGHT_NOTHING |
| R10 | what holds | marks after one admission | `1` | `1` | `1` | same | BOUGHT_NOTHING |
| R11 | what holds | judgments holding after one admission | `1` | `3` | `1` | same | BOUGHT_NOTHING |
| R12 | declared structure | the serialization key after one admission | `["U", [0]]` | `["O", [0]]` | `[1]` | only pinned `["U", [0]]`; only control `[1]` | BOUGHT_SOMETHING |
| R13 | event discipline | the state after the supply alone equals genesis | `true` | `true` | `true` | same | BOUGHT_NOTHING |
| R14 | event discipline | an admission that would move an admitted mark is refused | `true` | `true` | ABSENT -- the refusal is REMOVED, not absorbed: with no sides there is nowhere to move a mark to, so the refusal has no side-free statement at all | absent in the control | ABSENT |


### two retained marks

| id | kind | item | unnamed reading | named reading | control | difference vs unnamed | status |
|---|---|---|---|---|---|---|---|
| R15 | what holds | marks retained | `2` | `2` | `2` | same | BOUGHT_NOTHING |
| R16 | what holds | judgments holding at the retained regime | `2` | `4` | `2` | same | BOUGHT_NOTHING |
| R17 | what holds | presentation labels at the retained regime | `["a", "a"]` | `["a", "a"]` | `["a", "a"]` | same | BOUGHT_NOTHING |
| R18 | declared structure | state-changing event kinds | `["AdmitMark", "AdmitOccurrence"]` | `["AdmitMark", "AdmitOccurrence"]` | `["AdmitMark", "AdmitOccurrence"]` | same | BOUGHT_NOTHING |
| R19 | verdict | automorphisms of the retained regime | `2` | `1` | `2` | same | BOUGHT_NOTHING |
| R20 | verdict | the two retained marks are internally separable at base | `false` | `true` | `false` | same | BOUGHT_NOTHING |
| R21 | verdict | invariant separating mark properties at base | `[]` | `["on_side_0", "on_side_1"]` | `[]` | same | BOUGHT_NOTHING |
| R22 | what holds | the admission order is internally available | `false` | `false` | `false` | same | BOUGHT_NOTHING |
| R23 | what holds | the presentation label is internally available | `false` | `false` | `false` | same | BOUGHT_NOTHING |
| R24 | declared structure | the serialization key at the retained regime | `["U", [0, 1]]` | `["O", [0, 1]]` | `[2]` | only pinned `["U", [0, 1]]`; only control `[2]` | BOUGHT_SOMETHING |
| R25 | declared structure | the caller's two orders give equal regimes | `false` | `false` | `true` | differs | BOUGHT_SOMETHING |
| R26 | declared structure | the caller's two orders are isomorphic | `true` | `true` | `true` | same | BOUGHT_NOTHING |
| R27 | declared structure | isomorphism classes of the caller's two orders | `1` | `1` | `1` | same | BOUGHT_NOTHING |
| R28 | declared structure | identity policies that admit both retained wholes | `1` | `1` | `1` | same | BOUGHT_NOTHING |
| R29 | event discipline | marks the shared identity policy retains | `0` | `0` | `1` | control minus boundary = 1 | BOUGHT_SOMETHING |

* **R22.** False everywhere, and for the same reason in each world: the two supplies carry one token, so reversing them is not a change to notice.  The order still EXISTS side-free -- it is the mark's internal identity, and it is what the result turns on.
* **R29.** The pinned world REFUSES the second admission and retains none; the control accepts it as a no-op and retains ONE, so the requirement has no subject and the retained-mark check raises by name.  Neither is a false, and neither is a satisfied requirement.

### the imposed requirement

| id | kind | item | unnamed reading | named reading | control | difference vs unnamed | status |
|---|---|---|---|---|---|---|---|
| R30 | verdict | the requirement holds at base | `false` | `true` | `false` | same | BOUGHT_NOTHING |
| R31 | price | the minimum cost to meet the requirement, under mu1 | `1` | `0` | `1` | same | BOUGHT_NOTHING |
| R32 | verdict | tied non-isomorphic minima | `3` | `1` | `1` | control minus boundary = -2 | BOUGHT_SOMETHING |
| R33 | verdict | the minimum is unique | `false` | `true` | `true` | differs | BOUGHT_SOMETHING |
| R34 | verdict | the members attaining the minimum, under the declared collapse map | `["extra_mark", "withdraw_mark_permutations", "withdraw_reflection"]` | `["base"]` | `["withdraw_mark_permutations"]` | only pinned `["extra_mark", "withdraw_reflection"]`; only control `[]` | BOUGHT_SOMETHING |
| R35 | declared structure | the declared candidate space | `48` | `48` | `8` | control minus boundary = -40 | BOUGHT_SOMETHING |
| R36 | declared structure | one-step points in that space, under the declared collapse map | `["admit_names", "extra_mark", "keep_labels", "withdraw_mark_permutations", "withdraw_reflection"]` | `["admit_names", "extra_mark", "keep_labels", "withdraw_mark_permutations", "withdraw_reflection"]` | `["extra_mark", "keep_labels", "withdraw_mark_permutations"]` | only pinned `["admit_names", "withdraw_reflection"]`; only control `[]` | BOUGHT_SOMETHING |
| R37 | declared structure | bundles refused at two capabilities or more | `41` | `41` | `4` | control minus boundary = -37 | BOUGHT_SOMETHING |
| R38 | verdict | one-step points that satisfy, under the declared collapse map | `["extra_mark", "withdraw_mark_permutations", "withdraw_reflection"]` | `["admit_names", "extra_mark", "keep_labels", "withdraw_mark_permutations", "withdraw_reflection"]` | `["withdraw_mark_permutations"]` | only pinned `["extra_mark", "withdraw_reflection"]`; only control `[]` | BOUGHT_SOMETHING |
| R39 | declared structure | collateral facts the world declares | `["sides_internally_separable", "order_internally_available", "label_internally_available", "convention_internally_available", "side_names_hold"]` | `["sides_internally_separable", "order_internally_available", "label_internally_available", "convention_internally_available", "side_names_hold"]` | `["order_internally_available", "label_internally_available"]` | only pinned `["sides_internally_separable", "convention_internally_available", "side_names_hold"]`; only control `[]` | BOUGHT_SOMETHING |
| R40 | price | the minimum of the restricted second measure | `0` | `0` | `0` | same | BOUGHT_NOTHING |

* **R32.** Plurality is its own column and is NEVER summed with price: two worlds can pay the same and reach a different number of routes.
* **R34.** The unnamed column is the pinned point list with the declared collapse map applied, so one control point stands against one pinned class and the join is like for like.
* **R36.** The map joins by NAME in both reading columns, but its one-class justification is a fact of the unnamed reading only: there the two pinned further-mark points carry one class key, while under the named reading they carry two different class keys and are two classes.  So the named column shows five names where that reading has six points, and the decision this table reports is taken against the unnamed reading.
* **R38.** As R36: the map joins by name in both columns, its one-class justification holds under the unnamed reading only, and the named column therefore shows five names where that reading has six satisfying points.
* **R39.** The two lists are not the same length, so the second measure counted over them is NOT comparable across the worlds and is never differenced.  The restricted measure below is.
* **R40.** A row whose boundary value cells are not read from a pinned path.  Which rows those are is not asserted here but computed over every row's value and stated-price sources, with each cell's role and path recorded, at `boundary_source_census.rows_whose_boundary_cells_are_not_read_from_a_pinned_path`.  No pinned receipt carries a minimum of the restricted measure, so both are minima computed on THIS TREE'S OWN mirror carrier and read out of this tree's record.  The totality gate over the declared pinned values therefore does not reach them, and never counted them: what holds them instead is the weaker per-point data join, `second_measures.data_join_against_the_pin`, which joins 48 rows per reading against the pin and reports its mismatches.

### the prices each world states

| id | kind | item | unnamed reading | named reading | control | difference vs unnamed | status |
|---|---|---|---|---|---|---|---|
| R41 | price | the requirement is met with no augmentation | `false` | `true` | `false` | same | BOUGHT_NOTHING |
| R42 | price | nothing new is paid at this rung | `false` | `true` | `false` | same | BOUGHT_NOTHING |
| R43 | price | capabilities newly paid for at this rung | `["extra_mark", "withdraw_mark_permutations", "withdraw_reflection"]` | `[]` | `["withdraw_mark_permutations"]` | only pinned `["extra_mark", "withdraw_reflection"]`; only control `[]` | BOUGHT_SOMETHING |
| R44 | price | capabilities the satisfaction uses | `[]` | `["admitted boundary", "the side exchange is not a permitted renaming", "occurrence identity"]` | `["withdraw_mark_permutations"]` | only pinned `[]`; only control `["withdraw_mark_permutations"]` | BOUGHT_SOMETHING |
| R45 | price | who pays for the satisfaction | the run | the declared reading, and the run at Challenge 2 | the run | same | BOUGHT_NOTHING |
| R46 | price | coordinates the world prices at this rung | `["withdraw_reflection", "withdraw_mark_permutations", "admit_names", "keep_labels", "extra_mark"]` | `["withdraw_reflection", "withdraw_mark_permutations", "admit_names", "keep_labels", "extra_mark"]` | `["withdraw_mark_permutations", "keep_labels", "extra_mark"]` | only pinned `["withdraw_reflection", "admit_names"]`; only control `[]` | BOUGHT_SOMETHING |
| R47 | declared structure | declared values of the further-mark coordinate | `["None", "0", "1"]` | `["None", "0", "1"]` | `["False", "True"]` | only pinned `["None", "0", "1"]`; only control `["False", "True"]` | BOUGHT_SOMETHING |

* **R44.** The pinned world flags this field as declared and not computed, in its own receipt; the control column is the computed member list of its minimum, and the two are not the same kind of thing.
* **R45.** Declared and not computed on the pinned side, by its own flag, and declared and not computed on the control side too: nothing in this carrier computes a payer.  Both columns are declarations, so the agreement is true by unfolding them and is DEFINITION-level, not a measurement.
* **R46.** The control's three are the pinned five minus the two whose pinned capability sentence names a side; the three that transfer carry their pinned sentences byte for byte.
* **R47.** The single value-set change of the whole deletion, read from the pin.  Under the UNNAMED reading the two pinned further-mark points carry one class key and stand as the two members of one retained class; under the NAMED reading they carry two different class keys and are two classes, so the one-class sentence is scoped to the unnamed reading and is not a fact of both.

## What the admitted boundary bought, what it cost, what depends on it

Decided against the unnamed reading.

| what the admitted boundary bought | what it cost | which results depend on its presence |
|---|---|---|
| R02 (declared structure) the declared observation vocabulary: pinned `["OnSide", "SideNamed"]`, control `["Admitted"]` | neither world states a price for this item | R02 at genesis; also `["R04"]` |
| R04 (declared structure) the serialization key at genesis: pinned `["U", []]`, control `[0]` | neither world states a price for this item | R04 at genesis; also `["R02"]` |
| R08 (declared structure) admissions available from the one supplied token: pinned `2`, control `1` | neither world states a price for this item | R08 at one admitted mark; also `["R12"]` |
| R12 (declared structure) the serialization key after one admission: pinned `["U", [0]]`, control `[1]` | neither world states a price for this item | R12 at one admitted mark; also `["R08"]` |
| R24 (declared structure) the serialization key at the retained regime: pinned `["U", [0, 1]]`, control `[2]` | neither world states a price for this item | R24 at two retained marks; also `["R25", "R29"]` |
| R25 (declared structure) the caller's two orders give equal regimes: pinned `false`, control `true` | neither world states a price for this item | R25 at two retained marks; also `["R24", "R29"]` |
| R29 (event discipline) marks the shared identity policy retains: pinned `0`, control `1` | neither world states a price for this item | R29 at two retained marks; also `["R24", "R25"]` |
| R32 (verdict) tied non-isomorphic minima: pinned `3`, control `1` | neither world states a price for this item | R32 at the imposed requirement; also `["R33", "R34", "R35", "R36", "R37", "R38", "R39"]` |
| R33 (verdict) the minimum is unique: pinned `false`, control `true` | neither world states a price for this item | R33 at the imposed requirement; also `["R32", "R34", "R35", "R36", "R37", "R38", "R39"]` |
| R34 (verdict) the members attaining the minimum, under the declared collapse map: pinned `["extra_mark", "withdraw_mark_permutations", "withdraw_reflection"]`, control `["withdraw_mark_permutations"]` | neither world states a price for this item | R34 at the imposed requirement; also `["R32", "R33", "R35", "R36", "R37", "R38", "R39"]` |
| R35 (declared structure) the declared candidate space: pinned `48`, control `8` | neither world states a price for this item | R35 at the imposed requirement; also `["R32", "R33", "R34", "R36", "R37", "R38", "R39"]` |
| R36 (declared structure) one-step points in that space, under the declared collapse map: pinned `["admit_names", "extra_mark", "keep_labels", "withdraw_mark_permutations", "withdraw_reflection"]`, control `["extra_mark", "keep_labels", "withdraw_mark_permutations"]` | neither world states a price for this item | R36 at the imposed requirement; also `["R32", "R33", "R34", "R35", "R37", "R38", "R39"]` |
| R37 (declared structure) bundles refused at two capabilities or more: pinned `41`, control `4` | neither world states a price for this item | R37 at the imposed requirement; also `["R32", "R33", "R34", "R35", "R36", "R38", "R39"]` |
| R38 (verdict) one-step points that satisfy, under the declared collapse map: pinned `["extra_mark", "withdraw_mark_permutations", "withdraw_reflection"]`, control `["withdraw_mark_permutations"]` | neither world states a price for this item | R38 at the imposed requirement; also `["R32", "R33", "R34", "R35", "R36", "R37", "R39"]` |
| R39 (declared structure) collateral facts the world declares: pinned `["sides_internally_separable", "order_internally_available", "label_internally_available", "convention_internally_available", "side_names_hold"]`, control `["order_internally_available", "label_internally_available"]` | neither world states a price for this item | R39 at the imposed requirement; also `["R32", "R33", "R34", "R35", "R36", "R37", "R38"]` |
| R43 (price) capabilities newly paid for at this rung: pinned `["extra_mark", "withdraw_mark_permutations", "withdraw_reflection"]`, control `["withdraw_mark_permutations"]` | the item IS a price statement; what each world states is the row's own three columns | R43 at the prices each world states; also `["R44", "R46", "R47"]` |
| R44 (price) capabilities the satisfaction uses: pinned `[]`, control `["withdraw_mark_permutations"]` | the item IS a price statement; what each world states is the row's own three columns | R44 at the prices each world states; also `["R43", "R46", "R47"]` |
| R46 (price) coordinates the world prices at this rung: pinned `["withdraw_reflection", "withdraw_mark_permutations", "admit_names", "keep_labels", "extra_mark"]`, control `["withdraw_mark_permutations", "keep_labels", "extra_mark"]` | the item IS a price statement; what each world states is the row's own three columns | R46 at the prices each world states; also `["R43", "R44", "R47"]` |
| R47 (declared structure) declared values of the further-mark coordinate: pinned `["None", "0", "1"]`, control `["False", "True"]` | neither world states a price for this item | R47 at the prices each world states; also `["R43", "R44", "R46"]` |

Bought nothing: `["R01", "R03", "R06", "R07", "R09", "R10", "R11", "R13", "R15", "R16", "R17", "R18", "R19", "R20", "R21", "R22", "R23", "R26", "R27", "R28", "R30", "R31", "R40", "R41", "R42", "R45"]`.

Bought something: `["R02", "R04", "R08", "R12", "R24", "R25", "R29", "R32", "R33", "R34", "R35", "R36", "R37", "R38", "R39", "R43", "R44", "R46", "R47"]`.

A difference in a world's own bookkeeping -- the size of its declared space, the tag its serialization key carries -- is not a capability the primitive bought, and the kinds keep the two apart without curating which rows are in which bucket.

Rows whose pinned field the pinned world's own receipt calls declared and not computed: `["R44", "R45"]`.

Rows whose control field this module declares rather than computes: `["R45"]`.  DEFINITION-level, being declared on both sides: `["R45"]`.

A row whose pinned column and control column are BOTH declared and not computed agrees by unfolding two declarations.  That is DEFINITION-level and is not content, so it is named here and the verdict reports its tallies with the declared-field rows and without them.

Rows reading a cell this tree's own endowment ledger flags as declared and not computed, by value column and by price column: `[{"price_columns": ["control"], "row": "R03", "value_columns": []}]`.

A column that reads a cell this tree's own endowment ledger flags in its declared_columns is reading a DECLARATION of this tree and not a measurement taken off a carrier.  It is named for the reason the pinned world's own declared fields are named: so that a typed-in value is not read as something either world measured.

| kind | bought nothing | bought something | absent |
|---|---|---|---|
| declared structure | `["R09", "R18", "R26", "R27", "R28"]` | `["R02", "R04", "R08", "R12", "R24", "R25", "R35", "R36", "R37", "R39", "R47"]` | `["R05"]` |
| event discipline | `["R06", "R07", "R13"]` | `["R29"]` | `["R14"]` |
| price | `["R31", "R40", "R41", "R42", "R45"]` | `["R43", "R44", "R46"]` | `[]` |
| verdict | `["R19", "R20", "R21", "R30"]` | `["R32", "R33", "R34", "R38"]` | `[]` |
| what holds | `["R01", "R03", "R10", "R11", "R15", "R16", "R17", "R22", "R23"]` | `[]` | `[]` |

Absent, and therefore evidence for neither bucket:

* **R05** the two sides are collapsed at genesis -- the notion names a side, and a world with no sides cannot state it.
* **R14** an admission that would move an admitted mark is refused -- the refusal is REMOVED, not absorbed: with no sides there is nowhere to move a mark to, so the refusal has no side-free statement at all.

What the naming alone bought, over the unnamed reading:

* **R03** judgments holding at genesis: named `2`, control `0`.
* **R09** isomorphism classes of those admissions: named `2`, control `1`.
* **R11** judgments holding after one admission: named `3`, control `1`.
* **R16** judgments holding at the retained regime: named `4`, control `2`.
* **R19** automorphisms of the retained regime: named `1`, control `2`.
* **R20** the two retained marks are internally separable at base: named `true`, control `false`.
* **R21** invariant separating mark properties at base: named `["on_side_0", "on_side_1"]`, control `[]`.
* **R30** the requirement holds at base: named `true`, control `false`.
* **R31** the minimum cost to meet the requirement, under mu1: named `0`, control `1`.
* **R41** the requirement is met with no augmentation: named `true`, control `false`.
* **R42** nothing new is paid at this rung: named `true`, control `false`.
* **R45** who pays for the satisfaction: named the declared reading, and the run at Challenge 2, control the run.

## Which minima read a side

By name: a pinned coordinate transfers exactly when its pinned capability sentence contains no whole word 'side' or 'sides'

By behaviour: a candidate READS the placement when its separation verdict is not constant across the placements of one label configuration in its own route-census domain, and does not read it when the verdict is constant in every such group.

The first column says whose minimum a row is and NOT where its verdicts were taken.  The pinned rows' point names and capability sentences are read from the pinned receipts, so the by-name verdict is computed over pinned text.  The by-behaviour verdict is computed for every row on a carrier of THIS TREE -- the mirror for the pinned rows, the control for its own -- over that carrier's own route-census domain.  No pinned path carries a placement verdict and the pinned world's kernel is not run here, so no cell of the last column is a reading off the pinned world.

| whose minimum | reading | minimum | names a side, over pinned text | reads the placement, computed on a carrier of this tree |
|---|---|---|---|---|
| the pinned world | U | `extra_mark_0` | false | true |
| the pinned world | U | `extra_mark_1` | false | true |
| the pinned world | U | `withdraw_mark_permutations` | false | false |
| the pinned world | U | `withdraw_reflection` | true | true |
| the pinned world | O | `base` | false | true |
| the control | `null` | `withdraw_mark_permutations` | false | false |

The two criteria disagree on: `["base", "extra_mark_0", "extra_mark_1"]`.

## The pinned world's own dependence claims, read

The pinned world's own claims about which of its results need the admitted primitive, hand written in its four challenge modules and filed by its own ledger as computed by nothing.  A test there pins each dictionary against its own module constant, so its bytes are held while nothing adjudicates its claims.

Entries: 20.  By class: `{"DEPENDENT": 5, "INDEPENDENT": 14, "MIXED": 1, "UNCLASSIFIED": 0}`.

Classification: by the sentence's own opening words: 'does not depend' is INDEPENDENT, or MIXED when the same sentence also says something requires the primitive; 'require' is DEPENDENT.

Selector: the entries that are DEPENDENT and whose subject carries the whole word 'every', so the claim is universal over its rung.

Selected: `["the side exchange, its withdrawal, the two side mark properties, the counterfactual square, and every separation result of the rung"]`.

Evidence: `{"capability_sentence_is_byte_identical": true, "control_cost": 1, "control_satisfies": true, "coordinate": "withdraw_mark_permutations", "it_is_one_of_the_pinned_minima": true, "pinned_cost": 1, "pinned_satisfies": true, "same_cost": true}`.

Verdict: **CONTRADICTED within the declared scope**.  The selector is declared; the evidence under it is computed, and the contradiction is of one universal clause at one rung and of nothing else in the dictionary.

## The verdict

Over 47 compared items at the pinned rungs, the control reaches the unnamed reading's value at the unnamed reading's price in 26 of them and differs in 19, with 2 items that have no statement in one world and are therefore evidence for neither. Restricted to the items that are verdicts or prices, it reaches the same value at the same price in 9 and differs in 7. Of the 47 items, 2 read a field one world or the other DECLARES rather than computes -- R44, R45 -- and the subset declared on BOTH sides, which agrees by unfolding and is DEFINITION-level rather than content, is R45. Setting all 2 aside, the control reaches the same value at the same price in 25 items and differs in 18, and restricted to verdicts and prices in 8 and 6. At the imposed requirement the minimum cost differs by 0 from the unnamed reading and by 1 from the named reading, and what the admitted primitive bought under the unnamed reading is 2 additional routes at the same price.

Decided value: `NOTHING_IN_COST`.

**Scope.** Challenges 0 to 3 of the pinned world at 5c43c5ee, and their analogues in this carrier: the three declared coordinates, the pinned requirement and prices, the retained two-mark configuration, and the measure mu1.  Nothing wider.

**It does not speak for** the rungs not yet run in the pinned world, nor for whether the requirement was the right one to impose, nor for what the admitted primitive would buy at a rung this comparison does not price.

**It may not be read as** the sentence that the admitted primitive bought nothing.  What pays for separation in a world with no container is the ADMISSION ORDER, and whether an order is itself a container is not answered here.

## Open, and not closed

* **SF-OPEN-A** (inherited) Whether the admission order is itself a container.  What pays for separation in a world with no container is that order; this comparison prices the route and does not decide what kind of thing an order is.
* **SF-OPEN-B** (inherited) The price of re-purchasing a per-mark two-valued datum.  It lies outside the pinned candidate space and is therefore priced in neither world.
* **SF-OPEN-C** (inherited) The pinned premise that a candidate's permitted renamings are closed under composition and inverse is inherited, stated, and checked by nothing.
* **SF-OPEN-D** (inherited) Whether the requirement should have been declared so as to exclude a route that satisfies it by unfolding.
* **SF-OPEN-E** (opened here) OPENED BY THIS COMPARISON.  The record itself is not repaired; the CI step that could not survive it is.  The sibling record receipts/side_free.json carries the pinned commit's reachability inside its own bytes, at gates.G1.commit_check, so it is not the same file in a clone that cannot reach that commit.  Observed, not argued: with the commit replaced in a temporary manifest by an unreachable one, a fresh computation differs from the committed record in exactly two lines -- status PASS becomes SKIPPED, and the reason line changes.  No byte count is quoted for that fresh record, because its length depends on the substituted id and on git's own message.  The pinned branch is carried by no remote, so a checkout that fetches only remote refs is exactly that clone.  The record is NOT repaired, because the frozen design declares that conditional check to be part of it, and the frozen files are not edited to fit a later finding.  The CI step IS repaired: it required no diff after a fresh run, which reddens that clone on a defect that is not in the code, and it now takes the same reachability split the pin verifier takes -- the byte comparison is hard where the pinned commit is reachable, and where it is not the diff is PRINTED under a named SKIP.  Residual, recorded and not closed: in that clone drift in that record is visible in the log and is gated by nothing.  THIS record is built the other way: its rows are held by sha256 alone and the reachability report is printed by the runner, so it is the same file in both clones.
