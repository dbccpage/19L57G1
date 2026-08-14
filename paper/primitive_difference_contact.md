# Primitive Difference: the native characterization and the contact verdict

Run: PR #12 (contact and passage), extended by the executed collision
of 2026-08-13 (base a5caee2).  Base of the native record:
`blind-native-base` = ccd3a53 (merged main after PR #11).  Phase I
corrections: `paper/pr11_correction_ledger.md`.  Everything in this
paper is theorem, countermodel, finite computation, or explicitly
tagged OPEN; sources are `lean4/Derivation/PrimitiveCore.lean`,
`lean4/Derivation/PrimitiveCats.lean`,
`lean4/Derivation/PrimitiveContact.lean`, the collision modules
`lean4/Derivation/ObsDescent.lean`,
`lean4/Derivation/ContactBridge.lean`,
`lean4/Derivation/ContactKernel.lean`, and the artifacts
`primitive_candidates.json`, `primitive_implication_matrix.json`,
`primitive_contact.json`.  The externally supplied development is
referenced only by neutral description; its vocabulary and the
per-declaration correspondence live exclusively in
`contact/analysis/` (SUPPLIED_INPUT-labeled).

## FORMAL SPINE

### The signature and the nine candidate readings

All candidates are predicates over one signature
(`PrimitiveCore.Setting`): carrier `X`, asserted relation `r`,
designated endpoints `a b`, retention store `ret`, protected-demand
store `prot`, admitted operation family `Ops`.  The signature has no
observation field — that is Phase VI's separate admission.

| Candidate | Reading | Definition |
|---|---|---|
| W | bare witnessed pair | `r a b` |
| A | pointed witnessed irreflexive relation (PD-A) | `r a b ∧ Irrefl r` |
| Bs | symmetric axis (PD-B) | `A ∧ Symm r` |
| Bc | cotransitive axis (PD-B) | `A ∧ Cotrans r` |
| Bl | located axis (PD-B) | `A ∧ Located r` |
| C | witnessed non-identification (PD-C) | `r a b ∧ prot a b` |
| D | non-factorization through the point (PD-D) | `¬∃ p : Unit → X, …` |
| E | irreducibility under `Ops` (PD-E) | `Irred Ops a b` |
| F | protected retained PD (PD-F) | `A ∧ ret a b ∧ prot a b` |

`D_iff_ne`: non-factorization through the point is exactly
metatheoretic endpoint inequality.  `e_empty_iff_d`: over the empty
operation family, irreducibility is exactly D — PD-E is
family-relative all the way down.

### The implication matrix (72 ordered cells, all settled)

17 IMPLIES (each a theorem `imp_*_*`), 51 COUNTERMODEL (each a
compiled concrete finite countermodel `nimp_*_*`, minimum carrier
where claimed), 4 OPEN_LOCATED (`a→bl`, `bs→bl`, `bc→bl`, `f→bl`),
machine-readable in `PrimitiveCore.matrixCells` and cross-verified by
exhaustive Python enumeration (`primitive_implication_matrix.json`,
`expected_equals_computed: true`).

Load-bearing cells:

- **A → D** (`imp_a_d`): an irreflexive witness forces endpoint
  inequality.  **W → D fails** (`nimp_w_d`): the one-point
  self-difference (`Unit`, `r () ()`) is a bare witness with `a = b`.
  Positivity without irreflexivity does not yet separate.
- **A → Bc fails at carrier 3, provably minimally**
  (`nimp_a_bc` + `cotrans_auto_on_two`): cotransitivity is
  *automatic* on the two-element carrier, so no smaller countermodel
  exists.  The cotransitivity axis first becomes real content at
  three occurrences.
- **A → Bs fails at carrier 2** (`nimp_a_bs`, D2), minimal because a
  one-element carrier hosts no A-witness
  (`no_witness_on_subsingleton`).
- **C is not A and not D** (`nimp_c_a`, `nimp_c_d`): a demanded,
  witnessed non-identification on the one-point carrier — demand
  plus fact still does not entail difference without the
  irreflexivity law.
- **E → D** (`imp_e_d`); **D → E fails** with one admitted merger
  (`nimp_d_e`, `merger_erases`); **A → E fails** the same way:
  irreducibility is controller-relative, never primitive.
- **Fidelity is separate** (`prot_not_from_witness`,
  `ret_not_from_witness`): no witness entails its own protection or
  retention.  PD-F adds exactly two declared stores to PD-A
  (`f_ops_irrelevant`: the operation family is invisible to F).

### The OPEN cells, scoped exactly

`Located` (boolean realizability) is not derivable from any
propositional candidate law, and no internal countermodel can exist:
every decidable relation is located (`located_of_decidable`), and
every concrete finite countermodel in this development is decidable.
The four cells from A-entailing sources to Bl are therefore OPEN with
this exact scope: locatedness is admitted as separate data;
underivability is metatheoretic.  In the finite/computable regime the
distinction is invisible (`bl_equals_a_in_finite_universe` in the
artifact).

### Categories and the true universal properties

`PrimitiveCats` defines pointed witnessed relations (`PtdRel`),
morphisms preserving endpoints and edges (`Hom`), proves the category
laws, and settles:

1. **`d2Obj` is initial among ALL pointed witnessed relations**
   (`d2_initial`) — irreflexivity of the target is not needed, so
   this genuine universal property characterizes the bare-witness
   reading W (the free pointed object on one witnessed arrow) and
   restricts to the irreflexive subcategory (`d2_initial_irrefl`).
   Initiality does not select irreflexivity; the independent reason
   for A is `imp_a_d` against `nimp_w_d`.
2. **`s2Obj` is initial exactly in the symmetric subcategory**
   (`s2_initial_sym`) and **not weakly initial in the full category**
   (`s2_no_hom_to_d2`, `s2_not_weakly_initial`).
3. **Initiality is unique only up to isomorphism** (`initials_iso`)
   and **provably not up to presentation identity**
   (`two_initials_not_identical`: the oppositely-pointed `d2SwapObj`
   is also initial and is not the same presentation).
4. **Initiality is not minimum cardinality** (`larger_not_initial`):
   witnessed structures exist on every larger carrier
   (`ptd_on_every_larger_carrier`) and every one of them admits two
   distinct morphisms out — the free third point breaks uniqueness.
5. **Orientation lives in the pointing** (`pointed_rigid` vs
   `s2_swap_isRelAuto`): S2's swap is an automorphism only of the
   unpointed structure.  Neither branch of the orientation fork is
   prior; both are retained.

### The observer branching theorem

For a three-occurrence source, the category of faithful presentations
has **no weakly terminal object** (`no_terminal_pres`): the two
maximal observer cuts (`mergeA`, `mergeB`) are incomparable, and any
common receiver would identify the protected endpoints.  On the
two-point source the cut-branching vanishes, but unrestricted
terminality fails anyway, constructively: the free-point presentation
gives every candidate target two distinct commuting maps
(`no_terminal_pres2` — review-pass closure of the former OPEN cell).
The positive fragment is exactly uniqueness against surjective
presentations (`phom2_unique_of_epi`), where no free point exists.
The observer is
a *choice of maximal faithful collapse*; at three or more occurrences
that choice is essentially non-unique (cut census: 1, 2, 4, 8 for
carriers 2, 3, 4, 5).

## COUNTERMODELS

The 51 matrix countermodels are compiled theorems; the thirteen named
finite models (`unitBare` … `boolEmptyMerged`) are exported for
cross-reference.  Beyond the matrix: `larger_not_initial`
(initiality ≠ minimality), `s2_no_hom_to_d2` (orientation cannot be
recreated by any pointed map), `no_terminal_pres` (observer
non-uniqueness), `two_initials_not_identical` (uniqueness up to iso
only), and the Phase I countermodel pinned in
`Horizon.budget_saturation_noop`.

## THE EXECUTED COLLISION (2026-08-13)

The contact package arrived: one external Lean file (sha256 recorded
in `contact/omega_primdiff/CONTACT_MANIFEST.json`; no prose —
PROSE_INPUT_ABSENT), read under the committed statements-only
discipline against the fixed interface above.

### Formal spine of the collision

1. **The arriving core structure is the native valued observer.**
   Its five fields correspond one-for-one to
   `DiffInterface.DiffObs` (spelling, binder implicitness, and
   universe polymorphism aside).  That correspondence is a
   FINITE_COMPUTATION performed by a scratch compile run OUTSIDE
   this repository: the vocabulary firewall forbids committing the
   check, so only the sha256 of the file and of its log are on
   record (`contact/analysis/contact_countermodels.json`, field
   `scratch_bridge_check`), and no CI job, test, or reviewer can
   re-run it from the repository.  Every claim downstream of this
   premise inherits that limitation.  Its three
   equivalence laws are ADMITTED fields; the native side PROVES the
   same laws, equality-grade, at the declared observation stage of
   the passage (`ContactBridge.declared_zero_as_view`,
   `observation_stage_realizes_observer`) — the arriving stratum is
   an admitted observer at the zero-relation stage, not a
   pre-observational witness (`ContactBridge.kernelStage`,
   `kernel_stage_no_obstruction`).
2. **The arriving quotient-descent layer had no sealed counterpart
   and is reconstructed** in native vocabulary (`ObsDescent`):
   exactness (`obsQuotient_exact`, `obsQuotient_mk_eq_iff`,
   `obsQuotient_mk_surjective`), unary and binary descent with
   existence-iff-compatibility and global uniqueness (`descend_*`,
   `deltaDescend_*`), witness-blocking, pairing
   (`classConstant_pair_iff`, `pair_descend_exists_iff`,
   `view_descends_pair_blocked` — the flagship obstruction shape),
   the mod-setoid layer collapsed to the equality layer
   (`classConstant_comp_mk_iff` + existence forms + `coarsenMap` +
   `pairSetoid`), the all-zero countermodel (`collapseAllObs`
   family), and the integer tail subsumed by `intDiffObs` plus five
   one-line lemmas.  Axiom budget identical: every report ⊆
   {propext, Quot.sound} (`artifacts/lean_axioms.txt`).
3. **The factorization dictionary** (H4), at `Nat` scope: for kernel
   observers on the carrier `Nat` with `Nat`-valued views
   (`p q : Nat → Nat` — the typing forced by the sealed
   `Compression` layer's `D : List Nat`), global quotient descent is
   exactly native list-scoped factorization quantified over every
   represented domain (`descend_iff_factorsOn_all`,
   `classConstant_iff_fiberConstant_all`); per fixed domain the
   native notion is strictly weaker
   (`fiberConstant_fixed_D_not_classConstant`); uniqueness-scope
   difference is exactly projection surjectivity.  Kernel observers
   at other carriers or view types are outside the proved statements.
4. **The common replacement kernel** (`ContactKernel.WitnessedDiff`):
   valued difference presentation, designated endpoints,
   diagonal-zero law, refutation-grade witness — no symmetry, no
   transitivity, no stores.  Realized from native candidate-A
   settings (`ofSetting`, exact under pointwise decidability —
   `ofSetting_exact`; the gap without it recorded OPEN) and from
   observers plus a chosen non-zero pair (`ofDiffObs`; the pair
   proved load-bearing — `pair_choice_load_bearing`); and in the
   reverse direction the kernel *plus the two law declarations* is
   the observer record itself, field-for-field and losslessly
   (`toDiffObs`, `toDiffObs_fields`, `toDiffObs_apart`) — a record
   identity at DEFINITION grade, not a derivation.  It meets the
   sealed pre-contact interface (`toNativeKernel`), inherits the
   initial gateway unconditionally (`kernel_gateway_unique` from the
   sealed `d2_initial`), has provably no terminal collector at the
   induced-apartness morphism grade (`kernel_no_terminal_collector`,
   `kernel_no_terminal`: morphisms of the `apartObj` presentations,
   which discard the value data — terminality in the valued morphism
   category `VHom` is not addressed), carries value grade as
   presentation (`value_presentation_fork`, `vhom_not_unique`)
   rigidified under delta-surjectivity (`vhom_unique_of_onto` —
   sufficiency, with one non-onto countermodel; no equivalence is
   proved), and licenses passage entry pre-retention and
   pre-observation (`kernel_licenses_entry`,
   `entry_pre_observation`) — where the kernel contributes endpoint
   distinctness only: the other two conjuncts of
   `kernel_licenses_entry` (candidate A at the sealed pre-retention
   state; the empty retention store) are sealed constants that do
   not mention the kernel, and no map from an arbitrary kernel into
   the passage state is claimed.
5. **The matrix**: 37 collision cells
   (`ContactKernel.contactCells`, length proved), mirrored in
   `primitive_contact.json` and cross-checked by test.  Machine-
   checked: the count (`contactCells_length = 37`) and byte-level
   agreement between the Lean literal and the artifact mirror.  Each
   row's status and size annotation is a DECLARED LABEL naming the
   theorem that carries it; the named theorem, not the row, is the
   evidence.

### Collision countermodels

Native → arriving-shape representability fails at signature level.
Two of the refutations quantify over the value type: the oriented
two-element witness is no zero-complement over ANY value type
(`ContactBridge.d2_not_obs_complement`, carrier 2), and likewise the
symmetric three-point relation (carrier 3,
`triSym_not_obs_complement`, minimal by `bool_bs_repr`) and endpoint
witnesses over the empty relation (carrier 2,
`d_not_witnessed_repr`).  One does not: bare self-difference at
carrier 1 (`unit_total_not_repr`) refutes `∃ O : DiffObs Unit Prop`
only — the claim there is about PROP-VALUED observers, and no
value-type-general statement is proved for it.  All statements
quantify over `Type` (universe 0), while the arriving structure is
universe-polymorphic.  The crown characterization decides every such
cell at once *for Prop-valued observers*: a relation is the
zero-complement of some `DiffObs X Prop` exactly when its complement
is an equivalence and the relation is stable under double negation
(`obsApart_repr_iff`); at other value types only the forward
direction of that biconditional is available (from `obsApart_stable`
and the sealed `zeroRel_equivalence`).  Protection, retention,
operations, and the
designated pair are never derivable (`kernel_not_c`,
`kernel_not_f`, `kernel_prot_independent`,
`pair_choice_load_bearing`).  The dropped hypotheses are priced —
two of them exactly, as equivalences: the unconditional
cotransitivity schema for observer complements IS the weak law of
excluded middle (`cotrans_schema_iff_wlem`) and the stability schema
IS double-negation elimination (`stability_schema_iff_dne`); the
third one-directionally, the locatedness schema IMPLIES the weak law
(`located_schema_implies_wlem`, converse OPEN).  No internal
countermodel can exist for these schemas, and the residual cells
are recorded OPEN with those prices.

The collision declares **four** OPEN cells, and each is registered
as an open obligation in `artifacts/primitive_completion_receipt.json`
(`open_obligations`, which the collision therefore takes from four
entries to eight): `open_bridge_cotrans` (price: WLEM),
`open_bridge_located` (price: a WLEM-implication, converse OPEN),
`ContactKernel.open_kernel_grade` (price: DNE), and
`ContactKernel.open_kernel_bl` (underivability of Located from the
kernel fields is metatheoretic).  The two conjectures below that the
collision raised are registered in the same file's
`frontier_conjectures`, taking it from three entries to five.

## CONTACT VERDICT

**Sealed history**: the pre-contact terminal
**CONTACT_INPUT_ABSENT** (recorded at `blind-native-base`, preserved
as `history[0]` in `primitive_contact.json` and as
`PrimitiveContact.contactStatus`) fixed the interface this collision
was executed against.  Current status: **CONTACT_PROCESSED_LEAN_ONLY**
(`PrimitiveContact.contactStatusCurrent`).

**Primary: CONTACT_INCOMPARABLE_WITH_COUNTERMODELS.**  The
`WITH_COUNTERMODELS` half of that code covers the native→arriving
direction only; the arriving→native half is an ABSENCE claim about
the sealed corpus (the global quotient-descent layer does not occur
in it), not a refutation — no countermodel stands against that
layer, and its content is in fact derivable natively at the `Nat`
scope of the dictionary (`descend_iff_factorsOn_all`).  With that
said: the two developments are incomparable as supplied, with the
asymmetry proved.  The native→arriving gap is signature-level and
permanent, with finite countermodels exhibited at carrier sizes
1/2/3/2/2/1/2/2/2 across the nine native candidate readings.
CARRIER MINIMALITY is proved for exactly one of the nine — Bs at 3,
by the positive `bool_bs_repr` at carrier 2.  The other sizes are
the least carrier at which the reading can be posed at all (a
reading demanding a distinguished pair cannot be stated below
carrier 2): that is METATHEORY, not a proved minimum, and the
transport analysis records carrier minimality as explicitly
unclaimed for `d_not_witnessed_repr` and `no_kernel_over_allzero`.
Bc, Bl and F carry no separate countermodel at all; they fail
through the A-conjunct models cited in
`contact/analysis/contact_countermodels.json`.  The arriving→native
gap was content-level and is closed this run by the `ObsDescent`
reconstruction under the identical axiom budget.

**COMMON_PRIMITIVE_KERNEL_REPLACES_BOTH**, scoped to the overlap:
entry-level content of both sides is `WitnessedDiff` plus separately
declared additions.  On the arriving side the addition is the two
equivalence-law declarations, and the recomposition is a record
identity carrying a theorem, not prose — `toDiffObs` builds the
observer from a kernel and those two declarations, `toDiffObs_fields`
proves the fields are carried unchanged and the kernel is recovered
from the result, `toDiffObs_apart` proves the relations match;
DEFINITION grade, and the two declarations are separately priced at
carriers two and three (`kernel_not_observer`,
`kernel_zero_not_trans`).  On the native side the additions are the
retention/protection/observation declarations, and the kernel's own
entry-level content is derived (`toSetting_A`, `kernel_to_w`,
`kernel_to_d`, `kernel_to_e_empty`), with the declarations shown
separable (`ofSetting_ret_irrelevant`, `kernel_prot_independent`).
It does not replace native orientation, stores, operations, or
passage dynamics — native-only surplus.

**CONTACT_EQUIVALENT_UNDER_DECIDABLE_ZERO_PLUS_APARTNESS_ADMISSIONS**,
on the relational core only.  The decidability hypothesis is TWO
hypotheses, one per direction, and they are not interchangeable.
Apartness → observer spends pointwise decidability of the ASSERTED
APARTNESS relation (`isApart_repr`, `apartObs_roundtrip`, both
carrying `[∀ x y, Decidable (r x y)]`).  Observer → apartness spends
pointwise decidability of the ZERO relation (`obsApart_isApart`,
`indist_obsApart_iff`, both carrying
`[∀ x y, Decidable (ZeroRel O x y)]`).  Neither discharges the
other: the zero relation of the observer built from an apartness is
that apartness negated, and `Decidable (¬ P)` does not yield
`Decidable P` constructively — the residue is exactly what
`stability_schema_iff_dne` prices at double-negation elimination.
Under both admissions and the three apartness admissions the two
presentations are inter-constructible with matching relations in
both round trips; each dropped hypothesis priced as above.
Sufficiency is what is proved — necessity of either decidability
admission for a fixed observer is not.

**Not issued**, with recorded reasons: CONTACT_STRICTLY_STRONGER
(refuted by the countermodels); NATIVE_STRICTLY_STRONGER (as a
sealed-corpus claim it would launder this run's reconstruction into
the sealed record; the honest sentence is in the artifact's verdict
block).  Carried unchanged: the native characterization, passage
composition, and two-rule terminals — nothing in the arriving file
touches passage dynamics.

Answering Phase V now with a second party present: the kernel of
record remains the native one — **a pointed witnessed irreflexive
relation, with the two-element oriented realization initial in the
full pointed witnessed category** — and the collision sharpened it:
the common kernel both sides realize is that data with the witness at
refutation grade **plus a value layer** — a value type `R` and a
difference map `delta` (`WitnessedDiff`), which is strictly more than
the relation: two kernels can induce the same apartness with
different `delta` (`ContactKernel.value_presentation_fork`), and
morphisms are not determined by the carrier map
(`ContactKernel.vhom_not_unique`).  The value grade is presentation,
not relation.  Everything either side adds beyond that is a
separately priced declaration.

## FRONTIER CONJECTURES

1. The four OPEN located cells cannot be closed internally; a
   metatheoretic independence proof (a model of the ambient type
   theory where A holds and Located fails) would settle them — out
   of scope for this calculus, conjectured true.
2. The cut census `2^(n-2)` is computed for carriers 2–5 and
   conjectured for all `n ≥ 2` (finite computation; the bijection
   with free subsets of the non-designated occurrences is evident
   but not formalized).
3. (Closed in the review pass.)  Unrestricted two-point terminality
   is refuted constructively (`no_terminal_pres2`); the earlier
   selection-principle conjecture is superseded — the failure needs
   no choice analysis, only a free point.
4. (Recorded at the collision; registered in the receipt as
   ENLARGED_CORPUS_CONTAINS_RECONSTRUCTED_SUPPLIED_ABSTRACT_HALF.)
   Post-reconstruction, the enlarged native corpus strictly contains
   the reconstructed image of the arriving abstract half while the
   converse containment remains signature-impossible; any future
   strictly-stronger verdict must be stated relative to the enlarged
   corpus, never the sealed one.  Missing: any formal notion of
   corpus containment inside the calculus — the statement is
   METATHEORY about two corpora, not a proposition of the
   development.
5. (Recorded at the collision; registered in the receipt as
   LOCATEDNESS_SCHEMA_EQUALS_WLEM.)  The converse of
   `located_schema_implies_wlem` is OPEN: it would need a
   function-comprehension principle beyond the weak law; the
   forward price stands as proved.
