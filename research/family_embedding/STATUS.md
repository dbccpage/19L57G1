# Family embedding: the flat `Family` into `HFamily`

AuthorityEffect: None.  This tree proposes nothing for the sealed
derivation and amends nothing under `prompt/`, `paper/`, `code/`,
`lean4/Derivation/`, or `artifacts/`.

| object | id |
|---|---|
| source snapshot | `d74945a47b4f64cd92b4da5e061bdb46dddcbe05`, tree `2242ac29d28c0b4bafde877b73a046307de1efd3` |
| semantic root | `Derivation.PresentationNaturality` (import closure: 12 sealed modules, all pinned in `SOURCE_MANIFEST.json`) |

## Question

The sealed module's OPEN item at PresentationNaturality §14: a general
embedding of the flat `Family` (one carrier, arrows as `Arr` with
`src`/`tgt`) into `HFamily` is not proved there.  `hAuto_iff_auto`
bridges the two only at one object.  Construct `H F` with the stated
`Hom` and transported `iso`, and prove the natural-section existence
iff, or stop with `LEAN_NOT_CARRIED`.

## Result

`natural_section_iff_embed` is proved.  For `F : Family X R`,

`(∃ s : Sec F, IsNatural F s) ↔ (∃ s' : HSec (H F), HIsNatural (H F) s')`.

`H F` takes `Obj := F.Obj`, `car _ := X`, `res _ := R`, `obs := F.obs`,
and `Hom a b := { f : F.Arr // F.src f = a ∧ F.tgt f = b }`.  The
isomorphism at such an arrow is `F.iso` recast by `isoAlong` (`▸` on
the two observer equalities).  `mapPair_along` is the transport of
`mapPair` under `▸`; `hnatural_of_natural` rewrites along it after
recasting the section values.  Both directions of the iff keep the
same section.  Sixteen `#print axioms`
reports, every one "does not depend on any axioms", all within
`{propext, Quot.sound}`.  No `LEAN_NOT_CARRIED`.

`one_object_recovers` specialises the iff at `autoFamily O F` and
composes with the sealed `hAuto_iff_auto`, so a natural section of
`H (autoFamily O F)` exists exactly when one exists of `hAutoFamily O F`.
`autoFamily_hom_inhabited` shows that one-object `Hom () ()` is occupied.

## Anti-vacuity fixtures

Two objects (`TwoObj.a`, `TwoObj.b`), observer `boolEqObs` at both,
four arrows so every `Hom` cell is occupied: a loop at each object and
a crossing in each direction.

* **Obstructed.**  Loops are the sealed `negIso` (fixed-point-free on
  the carrier); crossings are `PresIso.refl`.  `obstructed_no_section`
  and `obstructed_H_no_section` (via `no_natural_section_of_endo` at
  the loop, using `obstructed_loopA_is_neg`).  `obstructed_hom_inhabited`
  occupies all four cells.
* **Clean.**  Every arrow is `PresIso.refl`.  `cleanSection` is the
  constant `boolEqPair`; `clean_natural`, `clean_has_section`,
  `clean_H_has_section`.  `clean_hom_inhabited` occupies all four cells.

An empty `Hom` would make the obstructed `H` side vacuously natural and
would make these fail.  The Python receipt uses the same spine (2
objects, 4 arrows, 2 admissible pairs, 4 sections): it groups Arr into
a Hom table and decides H-naturality on that table separately from the
Arr walk.  Emptying Hom while keeping the obstructed arrows makes the
two sides disagree.  Replay is byte-identical.

## Bounds

The Lean iff is the theorem `natural_section_iff_embed`, not a sweep.
The fixture computation is bounded by those two objects, four arrows,
two admissible pairs, and four sections; it does not enumerate larger
families.

## Manual receipt

This tree's axiom reports are a manual receipt.  No CI gate reads them.
Nothing in `.github/workflows` runs `verify_lean.py` or `verify_pins.py`;
a pass is a receipt for the sources present when it ran and implies no
enforcement.

Write root: `research/family_embedding/`.  The Lean package declares
NO Lake dependency.  `verify_lean.py` stages the snapshot blob of each
of the 12 pinned modules into `lean/sealed/` (gitignored) and diffs
repository-wide git status before and after the build.

## Non-claims

* No categorical structure is claimed for `Family` or `HFamily`.
* Nothing here derives `ContactKernel.no_equivariant_pair_valued_map`.
* The heterogeneous crossing-carrier OPEN of PresentationNaturality §14
  is untouched: both fixtures use one carrier.
* The statement of the iff is not weakened.

## Commands (run from the repository root)

| command | exit | key line |
|---|---|---|
| `python research/family_embedding/verify_pins.py` | 0 | `import closure of ['Derivation.PresentationNaturality']: 12 module(s), all pinned`; `sealed prefixes clean` |
| `python research/family_embedding/verify_lean.py` | 0 | `Lean #print axioms declarations: 16 within ['Quot.sound', 'propext']`; every report `no axioms`; `write root respected` |
| `cd research/family_embedding && PYTHONDONTWRITEBYTECODE=1 python run_embedding.py --out receipts` | 0 | obstructed `hom_inhabited True flat False H False`; clean `hom_inhabited True flat True H True` |
| `cd research/family_embedding && PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s . -p "test_*.py"` | 0 | tree tests, including the clean rebuild |
| `cd research/family_embedding && python -m mypy` | 0 | strict, files `.` |
