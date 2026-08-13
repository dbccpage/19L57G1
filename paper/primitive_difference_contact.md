# Primitive Difference: the native characterization and the contact verdict

Run: PR #12 (contact and passage).  Base: `blind-native-base` =
ccd3a53 (merged main after PR #11).  Phase I corrections:
`paper/pr11_correction_ledger.md`.  Everything in this paper is
theorem, countermodel, finite computation, or explicitly tagged OPEN;
sources are `lean4/Derivation/PrimitiveCore.lean`,
`lean4/Derivation/PrimitiveCats.lean`,
`lean4/Derivation/PrimitiveContact.lean`, and the artifacts
`primitive_candidates.json`, `primitive_implication_matrix.json`,
`primitive_contact.json`.

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

## CONTACT VERDICT

**CONTACT_INPUT_ABSENT.**  The declared package
`contact/omega_primdiff/` (manifest, `lean4/`, `prose/`) is absent at
`blind-native-base` and at completion; the runtime check is recorded
in `primitive_contact.json`.  Per protocol the native phases complete
and no contents are invented.  No comparison, no agreement, and no
disagreement with any external development is asserted anywhere in
this run.  `PrimitiveContact.lean` fixes the interface a future
contact must meet (kernel binding, universal status, orientation
fork, branching theorem, 72-cell matrix), so the collision, if it
ever happens, is against a committed target.

Answering Phase V in the absence of a second party: the kernel of
record is the native one — **a pointed witnessed irreflexive
relation, with the two-element oriented realization initial in the
full pointed witnessed category**; carrier data before laws, positive
witness before any observer, orientation as pointing, retention and
protection as separately priced stores, and exact relation to
metatheoretic inequality given by `imp_a_d` / `nimp_w_d` /
`D_iff_ne`.

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
