# Claim ledger -- natural sections at one object

Each row names its evidence: a Lean theorem in `lean/NaturalSections.lean`
(every one in `verify_lean.py`'s inventory, reported with no axioms) or a
test in `test_natural_sections.py`.  Classifications are exactly one of
proved theorem, countermodel, finite computation, open.

| ID | statement | class | evidence |
|---|---|---|---|
| NS-01 | Over `autoFamily O F`, for every carrier `X` and residual `R`: a natural section exists iff `F` fixes an admissible pair. | proved theorem | `NaturalSections.natural_section_iff_fixed_pair`, `NaturalSections.natural_section_of_fixed_pair`, sealed `PresentationNaturality.fixed_pair_of_natural_section` |
| NS-02 | The same equivalence over the indexed one-object family `hAutoFamily O F`. | proved theorem | `NaturalSections.hnatural_section_iff_fixed_pair`, sealed `PresentationNaturality.hAuto_iff_auto` |
| NS-03 | `F.mapPair p = p` iff `F.car.fwd` fixes both components of `p`; with admissibility, the invariant is two fixed carrier points the observer distinguishes. | proved theorem | `NaturalSections.fixed_pair_iff_two_fixed_points` |
| NS-04 | "The automorphism has a fixed point" does not give a natural section: `cycIso` on the sealed `card4Obs` fixes `e1`, fixes no admissible pair, and carries no natural section. | countermodel | `NaturalSections.fixed_point_without_natural_section`, `NaturalSections.cycIso_fixed_pair_free`, `NaturalSections.cyc_fixes_only_e1` |
| NS-05 | The identity on the one-view observer fixes every carrier point and carries no section at all, because no pair is admissible. | countermodel | `NaturalSections.identity_fixes_everything_no_section`, `NaturalSections.blindObs_no_admissible_pair` |
| NS-06 | Over a declared `HFamily` with a declared forest `T` (bases and walks as data, no condition), a natural section exists iff some `p : HSec D` satisfies `(T.gen h).transport (p (root a)) = p (root b)` for every declared arrow `h : a → b`; the section is `T.spread p`. | proved theorem | `NaturalSections.natural_section_iff_generators`, `NaturalSections.Walk.transport_of_natural`, `NaturalSections.Forest.gen_transport`, `NaturalSections.Walk.transport_reverse_transport` |
| NS-09 | With bases constant along arrows, a natural section exists iff some `p : HSec D` is fixed by every closed walk at its base (the holonomy form). | proved theorem | `NaturalSections.natural_section_iff_holonomy`, `NaturalSections.walk_maps_of_closed_fixed` |
| NS-10 | Transport along a walk is a bijection on admissible pairs: the reverse walk undoes it in both orders, on the sealed `mapPair_symm_left/right` alone. | proved theorem | `NaturalSections.Walk.reverse_transport_transport`, `NaturalSections.Walk.transport_reverse_transport`, `NaturalSections.Step.inv_transport`, `NaturalSections.Step.transport_inv`, `NaturalSections.Walk.transport_append` |
| NS-11 | The general iff specialised to `hAutoFamily O F` with the trivial forest is the one-object iff NS-02. | proved theorem | `NaturalSections.one_object_recovered` |
| NS-12 | No fixture exercises a closed walk of length above one with nontrivial transport, and no finite computation of holonomy classes exists. | open | none -- named in `STATUS.md` under "Still open" |
| NS-07 | The 12 sealed modules the package compiles are exactly the import closure of `Derivation.PresentationNaturality`, pinned by blob hash at the snapshot and at HEAD. | finite computation | `test_manifest_resolves_and_is_the_import_closure`, `test_unpinned_closure_member_is_refused`, `test_pinned_but_unreachable_module_is_refused` |
| NS-08 | A clean build writes nothing outside `research/natural_sections/`; in particular `lean4/.lake` is not created. | finite computation | `test_clean_build_leaves_lean4_untouched_and_stays_inside_the_root`, `test_writes_outside_root_names_a_new_lean4_build_product`, `test_staged_sources_are_the_pinned_snapshot_blobs` |
