# Observer visibility: passivity, kernel cover, necessity of joint-kernel triviality

AuthorityEffect: None.  This tree proposes nothing for the sealed
derivation and amends nothing under `prompt/`, `paper/`, `code/`,
`lean4/Derivation/`, or `artifacts/`.

| object | id |
|---|---|
| source snapshot | `df7a1136da1783b2890d8104e594e8e2aee70292`, tree `f9338344c48d6923ee39a415876b8ab361ef5e4c` |
| semantic root | `Derivation.PresentationNaturality` (import closure: 12 sealed modules, pinned and staged for write-root binding, not imported, not a Lake target) |

Mathematics is defined natively in this tree.  The gauge takes values in
the nonnegative integers (a decidable subsemiring of the rationals).
The general real-valued gauge is OPEN: Lean 4 core here has no real
field, and that is the blocker.

## Predictions (registered before computation)

These lines were written before any Python receipt was generated and
before the Lean package was built.

* **OV1.**  For any observer, `J ≤ I`, and `I = 0` forces `J = 0`.
  Reason: each watcher is nu-contractive, so each observed term is at
  most the coboundary mass on that edge; unwatched edges only add to `I`.
* **OV2.**  All-Green (`J^a = 0` for every observer) iff `D(s)_e` lies
  in the joint watcher kernel `K_e` for every edge.  Unwatched edges
  have `K_e` the whole carrier.
* **OV3.**  Three patches, three overlap objects, six covering edges
  (Čech nerve of three pairwise overlaps), identity restrictions,
  rank-1 coordinate projections as watchers, section `(0,1)` on
  overlaps and `0` on patches: All-Green, full coverage, `I(s) = 6`.
  Corollary: no recovery modulus `f` with `I(s) ≤ f(max J^a(s))` on
  this family, because `max J = 0` and `I = 6`.
* **OV4.**  Full coverage and `K_e = {0}` for every edge implies
  All-Green forces `I(s) = 0`.
* **OV5.**  The family is sound (All-Green implies `I = 0` for every
  section) iff `im(D) ∩ prod_e K_e = {0}`, under faithful `nu`.  This
  is the necessity of joint-kernel triviality on the coboundary image,
  not of `K_e = {0}` on unreached coboundaries.  A decision procedure
  over rational vectors will return a minimal-support-then-minimal-mass
  witness when unsound, and `SOUND` when the intersection is trivial.
  Predicted on the OV3 family: unsound, witness mass 6.  Predicted on
  OV3 plus one extra watcher killing the remaining kernel: `SOUND`.
  Predicted: brute force on 20 seeded small diagrams agrees with the
  linear decision.
* **OV6.**  On the chord square (four objects, five edges, two faces),
  the gauge orbit of a cochain is finite when the fibre is a finite
  group.  `Phi(w) = 0` iff both face fluxes vanish.  For `Z_N` with
  `N in {2,3,4}`, `Phi` is determined by the two fluxes; the formula
  is computed on the finite group and recorded, not claimed for every
  gauge.
* **OV7.**  `I - max J^a = edge_loss + fragment` with both terms
  nonnegative.  A zero-map watcher fixture makes edge_loss the whole
  gap.  A split-observer fixture makes fragment the whole gap.
* **OV8.**  A dual vector that annihilates every All-Green coboundary
  and is bounded by `nu` lower-bounds `I` on All-Green sections.  The
  Python certificate is checkable by that theorem, not trusted as a
  solver receipt.

## Results

Written after the Lean build and the Python receipts.  The first
results paragraph named `sound_iff_intersection_trivial`,
`orbit_eq_of_gauge`, `gap_add`, `fragment_nonneg`, and
`dual_lower_bounds_mass`.  Those names did not match the obligations
and are withdrawn.  The statements below are the replacements.

* **OV1.**  `passivity_term`, `j_le_i`, `j_le_i_unwatched`,
  `jobs_zero_of_i_zero`, `i_zero_forces_every_j_zero`.  An observer is
  a list of optional contractions; unwatched slots add only to `I`.
  `J ≤ I` for any such observer, and `I = 0` forces every listed
  observer's `J` to vanish.
* **OV2.**  `allGreen_iff_in_joint_ker`.
* **OV3.**  Lean section mass 6, All-Green, six edges.
  `no_recovery_modulus`: every `f` with `f 0 = 0` fails `I ≤ f 0`.
* **OV4.**  `trivial_ker_allGreen_implies_sound`: a watcher with
  trivial kernel, plus All-Green for that watcher, implies `I = 0`.
  Instantiated as `id_allGreen_implies_I_zero`.  The coboundary-mass
  lemma `trivial_kers_imply_sound` is the inner step, not the OV4
  statement.
* **OV5.**  Instance: integer plane, identity restrictions,
  first-coordinate watcher.  `allGreenS_iff_inK` is `Iff.rfl`, so
  `sound_iff_imD_cap_K` is `Iof_zero_iff` (faithful `nu`).  Self-loop
  `(0,0)`: `loop_sound` and `coord_ker_nontrivial` — the family is
  sound while the first-coordinate kernel is not `{0}`.  Linear
  decision is the Q-nullspace of `W ∘ D`, independent of brute force.
  Unsound witness is min over RREF generators, not over the integer
  kernel; on the OV3 box `[-1,1]^12` a separate scan certifies that
  this generator is globally minimal (support 1, mass 2).
  Both-coordinate watch: SOUND.  Unwatched self-loop: SOUND.
  Seed `20260830`, twenty two-object diagrams, decide vs brute agree.
* **OV6.**  `cob_along_path`.  Full `C^1 = Z_N^5` tables for
  `N in {2,3,4}`: `Phi = 0` iff both face fluxes vanish.  Real-valued
  infimum remains OPEN.  This independently reconfirms the same
  vanishing-on-zero-fluxes fact on a chord square whose labels and
  snapshot predate the later pricing tree on `main`.
* **OV7.**  `nat_gap` / `gap_splits` / `disjoint_fragment`.  OV3
  section at `max J = 0`: gap 6 = edge_loss 6 + fragment 0.  Split
  observers on two first-coordinate edges: gap 1 = edge_loss 0 +
  fragment 1, with `max J` taken over that observer family.
* **OV8.**  `dual_pair_le_mass`: `|y| ≤ 1` implies
  `|sum y_e d_e.2| ≤ I`.  Dual `y_e = -1` pairs to 6 on the Lean
  section.

Thirty-three `#print axioms` reports, all within `{propext, Quot.sound}`.

The OV3 scaling corollary `I(s_λ) = 6λ` on the All-Green fibre was
not taken: `no_recovery_modulus` is the `f 0 = 0` failure at the
fixed section.

## Manual receipt

This tree's axiom reports are a manual receipt.  No CI gate reads them.
Nothing in `.github/workflows` runs `verify_lean.py` or `verify_pins.py`;
a pass is a receipt for the sources present when it ran and implies no
enforcement.

Write root: `research/observer_visibility/`.  The Lean package declares
NO Lake dependency and does not compile Derivation.  `verify_lean.py`
stages the snapshot blob of each of the 12 pinned modules into
`lean/sealed/` (gitignored) for pin and write-root binding, then diffs
repository-wide git status before and after the build.

## Non-claims

* No categorical structure is claimed for the diagram or the coboundary.
* Joint-kernel triviality on `im(D)` is not the same as `K_e = {0}` for
  every edge.  The self-loop fixture is the exhibit: sound, with
  first-coordinate kernel containing `(0, 1)`.
* The integer-valued gauge is not the general real-valued gauge (OPEN,
  blocker: no real field in this Lean core package).
* No external names or citations.

## Commands (run from the repository root)

| command | exit | key line |
|---|---|---|
| `python research/observer_visibility/verify_pins.py` | 0 | `sealed prefixes clean` |
| `python research/observer_visibility/verify_lean.py` | 0 | `#print axioms` inventory, write root respected |
| `cd research/observer_visibility && PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s . -p "test_*.py"` | 0 | tree tests |
| `cd research/observer_visibility && python -m mypy` | 0 | strict, files `.` |
