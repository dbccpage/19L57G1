# Claim ledger — closed_family

One evidence class per row. Lean names live in `lean/ClosedFamily/`; the
reconstruction bindings are in `SOURCE_MANIFEST.json` and are checked by
`verify_pins.py`. `AuthorityEffect: None.`

| ID | class | statement | evidence |
|---|---|---|---|
| CF-1 | CONDITIONAL_THEOREM | The pinned observer, its zero relation, explicit bijections, presentation isomorphisms with identity, inverse and composition, the transported pair bundle, declared families, sections, naturality, and the four bundle-coherence lemmas, all reconstructed verbatim. | `lean/ClosedFamily/Base.lean`, eight source projections checked exact |
| CF-2 | DEFINITION | A word from one object to another: each step a declared arrow taken forwards or backwards, indexed by its endpoints. | `Closure.Path` |
| CF-3 | DEFINITION | A word is interpreted by the pinned `refl`, `symm`, and `trans`, and by nothing else. | `Closure.pathIso` |
| CF-4 | DEFINITION | The closure of a declared family: the same objects and observers, every word an arrow. | `Closure.closure` |
| CF-5 | PROVED_THEOREM | Sections of the closure are sections of the family — the same type, by `rfl`. | `Closure.sec_closure_eq` |
| CF-6 | DERIVED_DEFINITION | The closure explicitly represents the formal inverse of every declared arrow and the composite of any composable words. This supplies operations the declared family need not list; it does not assert strict growth for every family. | `Closure.closure_contains_inverse`, `Closure.closure_contains_composite` |
| CF-7 | PROVED_THEOREM | Identity law on the transported bundle. | `Closure.mapPair_nil` |
| CF-8 | PROVED_THEOREM | Composition law on the transported bundle: interpreting a concatenation is interpreting the parts in order. | `Closure.mapPair_comp` |
| CF-9 | PROVED_THEOREM | Both inverse laws on the transported bundle: a word followed by its reversal returns the pair unchanged. | `Closure.mapPair_inv` |
| CF-10 | PROVED_THEOREM | Concatenation is associative; the empty word is a left unit by `rfl` and a right unit by induction. | `Closure.comp_assoc`, `Closure.nil_comp`, `Closure.comp_nil` |
| CF-11 | PROVED_THEOREM | Naturality runs backwards along a declared arrow. The pinned `IsNatural` states one direction; the closure demands the other, and it follows from the pinned `mapPair_symm_left`. | `Closure.natural_symm` |
| CF-12 | PROVED_THEOREM | Naturality along an arbitrary word follows from naturality on the declared arrows alone. | `Closure.natural_on_path` |
| CF-13 | PROVED_THEOREM | **A section is natural for the closure exactly when it is natural for the declared family.** Closing under composition and inverses imposes no new obligation on a section. | `Closure.natural_iff_natural_closure` |
| CF-14 | PROVED_THEOREM | A declared family carries a natural section exactly when its closure does: the obstruction is unchanged by closing. | `Closure.has_natural_section_iff` |
| CF-15 | PROVED_THEOREM | Closing a closure imposes nothing further. | `Closure.natural_closure_closure` |
| CF-16 | FINITE_COMPUTATION | 21 axiom reports, every one axiom-free — no `propext`, no `Quot.sound`. | `verify_lean.py`, `lean/ClosedFamily/AxiomReport.lean` |
| CF-17 | METATHEORY | The operation laws are proved on the transported bundle map, which is the only thing naturality reads. They are not equalities of `PresIso` records. | declared reading 2 in `STATUS.md` |
| CF-18 | OPEN | Record-level laws; families with declared relations among their arrows; the heterogeneous case; and whether the pinned fixed-point obstruction's witness data is invariant under closing. | `STATUS.md` leftovers |
| CF-19 | REFUSED | That the closure is a structure of any named outside kind. It is the closure of a declared family under the operations the pinned isomorphisms already carry, and it is named that. | FW-NAME |
