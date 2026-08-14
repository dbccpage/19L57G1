# Contact dictionary: supplied development ↔ native corpus

SUPPLIED_INPUT-labeled analysis (2026-08-13, base a5caee2).  This
directory is the only repository location permitted to quote the
supplied development's vocabulary.  The supplied single Lean file
(sha256 `d9cdb350a53c513e3e211e72f17262be6ba85d7da6159f910388c7137e8`
`14a89`, bound by `contact/omega_primdiff/CONTACT_MANIFEST.json`;
prose stage PROSE_INPUT_ABSENT) contains 103 top-level declarations
inside one namespace.  The machine-readable row-per-declaration map,
the countermodel table, and the G1–G20 gap dispositions live in
`contact_countermodels.json`.  Everything below is commentary on
formal statements; comments and doc-strings of the supplied file are
never treated as evidence.

## The core identification

The supplied core structure `PrimitiveDifference` is field-for-field
the native `DiffInterface.DiffObs` (sealed at base a5caee2): a valued
difference map, a zero predicate on values, and three equivalence law
FIELDS.  The differences are spelling (`δ` vs `delta`), binder
implicitness on two law fields, and universe polymorphism — at
`Type 0` the two structures are definitionally interconvertible.
Evidence class FINITE_COMPUTATION: a scratch bridge file (kept
outside the repository; hashes recorded in
`contact_countermodels.json`) compiles both, converts in both
directions, and proves both round trips and the zero-relation match
with axiom-free reports.  **Reproducibility limit:** the vocabulary
firewall forbids committing that file, so this premise is NOT
re-runnable from the repository — no CI job, test, or reviewer can
reproduce it, and the two recorded sha256 values are the whole
record.  Everything resting on it inherits that limitation.

Consequence, recorded exactly: `zeroRel_refl` / `zeroRel_symm` /
`zeroRel_trans` / `zeroRel_equivalence` on the supplied side are
re-exports of ADMITTED fields, while the same laws are PROVED
(equality-grade) at every concrete observer OF THE SEALED CORPUS AT
`a5caee2` — each is a `kernelObs` at a view, where the laws come out
by `rfl`/`.symm`/`.trans` — and at the passage's declared observation
stage (`ContactBridge.declared_zero_as_view`).  **Scope: this is not
a universal claim about native observers.**  Observers added by this
run are not all `kernelObs` — `ObsDescent.intDiffObs` proves its laws
by linear arithmetic, `ObsDescent.collapseAllObs` by `trivial`, and
`ContactBridge.apartObs` (`ContactBridge.lean:224`) discharges
`zero_refl`/`zero_symm`/`zero_trans` by `h.irrefl`/`h.symm`/
`h.cotrans`, i.e. by the three ADMITTED `Apartness.IsApart` fields,
spent one-for-one; at that native observer the three laws are exactly
as admitted as on the supplied side.  The asymmetry is at
the INSTANCE level: the native `DiffObs` signature carries the same
three laws as fields, exactly as the supplied structure does.  The supplied stratum sits at
the native zero-relation stage: an admitted observer, not a
pre-observational witness (H1 verified and sharpened;
`ContactBridge.kernelStage`, `kernel_stage_no_obstruction`).

## The abstract half (items 1–80): reconstructed

The supplied quotient-descent layer — exactness, unary and binary
descent with existence-iff-compatibility, GLOBAL uniqueness,
witness-blocking, pairing, the mod-setoid layer, coarsening
transport, the all-zero countermodel, the tag construction — had no
sealed native counterpart at base.  It is reconstructed this run in
native vocabulary as `ObsDescent` (module doc lists the dictionary),
under the identical axiom budget ⊆ {propext, Quot.sound}.  Naming
dictionary highlights:

| supplied | native |
|---|---|
| `DeltaCongruent` / `deltaFactor` | `ObsDescent.DeltaConstant` / `deltaDescend` |
| `InvariantCongruent` / `invariantFactor` | `ObsDescent.ClassConstant` / `descend` |
| `*_exists_iff_*` | `descend_exists_iff`, `deltaDescend_exists_iff` |
| `*_unique` | `descend_unique`, `deltaDescend_unique` (symmetric two-map form) |
| `*_no_factor_of_*_ne` | `descend_blocked_of_witness`, `deltaDescend_blocked_of_witness` |
| `invariantCongruent_pair_iff` | `classConstant_pair_iff` |
| `localGreenGlobalRed_*` (flagship) | `view_descends_pair_blocked` (slogan branding not imported) |
| `quotientMapOfSetoidImp` | `coarsenMap` |
| `productSetoid` | `pairSetoid` |
| `boolAllZeroNonconstant*` | `collapseAllObs*` |
| the ~28 `*Mod*` declarations | collapsed to the equality layer via `classConstant_comp_mk_iff` (+ `descendMod_exists_iff`, `deltaDescendMod_exists_iff`, `descendMod_exists_of_coarsen`) |

## The tail (items 81–103): subsumed

The 23 physics-labeled declarations never instantiate the file's own
core structure; each is integer subtraction with renamed variables.
All are subsumed by `ObsDescent.intDiffObs` plus five one-line
lemmas (`int_sub_ne_zero_iff`, `int_sub_ne_zero_of_gt`,
`int_shift_cancel`, `int_two_mul_eq_zero_iff`,
`int_add_sub_cancel`) — per-name rows in the coverage map.
`intDiffObs` also closes the gap the supplied file leaves open: it IS
an instance of the core structure with all three laws proved.
Comment-borne physics vocabulary (norms, channels, holonomy,
decoherence, thresholds, and the G12 derivability claim) is REFUSED
transport; dispositions G1–G20 are recorded per row.

## The other direction: signature-level countermodels

No supplied-shape structure represents: the oriented two-element
witness over any value type (`ContactBridge.d2_not_obs_complement` —
H3 as a theorem), bare self-difference for Prop-valued observers
(`unit_total_not_repr`, which refutes `∃ O : DiffObs Unit Prop`
only), the symmetric three-point relation over any value type
(`triSym_not_obs_complement`, minimal by `bool_bs_repr` — the ONE
carrier minimality proved in this run), or a witness over the empty
relation, over any value type (`d_not_witnessed_repr`; carrier
minimality unclaimed, see §4 of `lean_theorem_transport.md`).  The
crown characterization, for Prop-valued observers: a relation is the
zero-complement of some `DiffObs X Prop` exactly when its complement
is an equivalence and it is ¬¬-stable (`obsApart_repr_iff`; at other
value types only the forward direction is available).  All statements
quantify over `Type` (universe 0).  Protection, retention,
operations are never derivable, and the observer alone neither
guarantees a non-zero pair nor determines a same-data kernel
presentation (`kernel_not_c`, `kernel_not_f`,
`kernel_from_obs_iff_pair`, `kernel_no_witness_from_collapse`,
`kernel_not_unique_of_pair`).

## Scoped equivalence and prices

The decidability premise is TWO admissions, one per direction, and
they are not interchangeable.  Apartness → observer spends pointwise
decidability of the ASSERTED APARTNESS relation (`isApart_repr`,
`apartObs_roundtrip`, both under `[∀ x y, Decidable (r x y)]`).
Observer → apartness spends pointwise decidability of the ZERO
relation (`obsApart_isApart`, `indist_obsApart_iff`, both under
`[∀ x y, Decidable (ZeroRel O x y)]`).  Neither returns the other:
the zero relation of `apartObs r h` is `¬ r`, and `Decidable (¬ P)`
does not yield `Decidable P` constructively — the residue is exactly
what `stability_schema_iff_dne` prices at DNE.  Under both admissions
plus the three apartness admissions, the native apartness stratum and
the supplied-style observer are inter-constructible with matching
relations in both round trips.  Dropping decidability is priced:
cotransitivity-schema ↔ WLEM, stability-schema ↔ DNE,
locatedness-schema → WLEM (forward only; converse OPEN with its exact
note).  Sufficiency is what is proved; necessity of either
decidability admission for a fixed observer is not.

## METATHEORY scope notes (honesty rows)

1. **Uniqueness scope.**  Supplied uniqueness is global because
   quotient projections are epi by induction
   (`obsQuotient_mk_surjective`); native presentation uniqueness is
   image-scoped (`factor_unique_on_image` /
   `factor_not_unique_off_image` / `phom2_unique_of_epi`).  The
   difference is exactly codomain coverage by the projection; the
   kernel echo is `vhom_unique_of_onto` against `vhom_not_unique`.
2. **Selection discipline.**  The native factorization layer prices
   representedness and first-match selection where the supplied layer
   prices `Quot.sound` gluing — the same third notion
   (`descend_iff_factorsOn_all`, stated for kernel observers on the
   carrier `Nat` with `Nat`-valued views, `p q : Nat → Nat`, the
   typing forced by the sealed `Compression` layer's `D : List Nat`;
   other carriers and view types are outside the statement), two
   priced realizations; per fixed domain the native notion is
   strictly weaker (`fiberConstant_fixed_D_not_classConstant`).
3. **Flagship vs branching.**  The supplied flagship obstruction is a
   fixed-quotient descent failure; the sealed `no_terminal_pres` /
   `no_terminal_pres2` are non-existence of universal presentations.
   These are NOT identified; the honest bridge is
   `pair_blocked_is_collapse_collision` with its converse
   `collapse_collision_is_pair_blocked` (packaged as
   `pair_blocked_iff_collapse_collision`), which licenses "one event
   in two vocabularies" at THAT grade only, and the sealed
   four-condition passage obstruction is strictly finer
   (`obst_conditions_independent` cited).
4. **Raw-quotient barrier.**  `Derivation.quot_barrier` is strictly
   more general than anything the supplied SETOID-BASED machinery can
   state — the supplied layer requires the setoid.  METATHEORY,
   citation-only cell: no transport theorem is written in either
   direction and none is claimed.
5. **No Phase VII claim.**  Nothing here touches constitution-class
   minimality; gateway uniqueness is inherited initiality, up to
   isomorphism only (`initials_iso`,
   `kernel_gateways_not_identical`).
