# Natural sections at one object: the fixed-pair criterion is an iff

AuthorityEffect: None.  This tree proposes nothing for the sealed
derivation and amends nothing under `prompt/`, `paper/`, `code/`,
`lean4/Derivation/`, or `artifacts/`.

| object | id |
|---|---|
| source snapshot | `a36d34948ffd2a24ee99ec717f903f57141095c7`, tree `603478526a6c06de116c843956da7e76d280c4b6` |
| semantic root | `Derivation.PresentationNaturality` (import closure: 12 sealed modules, all pinned in `SOURCE_MANIFEST.json`) |

## Question

`PresentationNaturality.no_natural_section_of_fixed_point_free` is a
sufficient condition for naturality to FAIL over the one-object family
`autoFamily O F`: if the automorphism fixes no admissible pair, no
natural section exists.  Its contrapositive
`fixed_pair_of_natural_section` is stated.  The sealed module never
states the equivalence, and its non-claims leave every many-object
question open.  Two questions:

1. Is the converse provable -- does a natural section exist whenever the
   automorphism fixes something?
2. What is the necessary and sufficient condition, and is it stated
   anywhere in the repository?

## Results (Lean, `lean/NaturalSections.lean`; 24 reports, every one
"does not depend on any axioms" -- the tree's 48 reports in all are
within `{propext, Quot.sound}`, 41 with no axioms and 7 in `Hop3` on
`propext`, as the fixture sections say)

* **`natural_section_iff_fixed_pair`** -- over `autoFamily O F`, a natural
  section exists **iff** `F` fixes an admissible pair:
  `(∃ s, IsNatural (autoFamily O F) s) ↔ ∃ p : NonZeroPair O, F.mapPair p = p`.
  The forward half is the sealed `fixed_pair_of_natural_section`; the
  backward half is `natural_section_of_fixed_pair`, the constant section.
  `hnatural_section_iff_fixed_pair` is the same statement for the indexed
  `hAutoFamily`, through the sealed bridge `hAuto_iff_auto`.  Over one
  object the whole question is this; the sealed module's own docstring
  calls the negative direction near-definitional, and the equivalence is
  no deeper.  **Proved theorem**, on every carrier and residual type.
* **`fixed_pair_iff_two_fixed_points`** -- `F.mapPair p = p` iff `F`
  fixes both components of `p`.  Since `p` is admissible, the invariant
  is: two fixed carrier points that the observer distinguishes.
  **Proved theorem.**
* **The converse as "has a fixed point" is false**, by two countermodels:
  - `fixed_point_without_natural_section` -- `cycIso` on the sealed
    `card4Obs` fixes `e1` and cycles `e2 e3 e4`.  It has a fixed point;
    its only fixed pair is `(e1, e1)`, inadmissible because
    `DiffObs.zero_refl` is a field; so it fixes no admissible pair
    (`cycIso_fixed_pair_free`) and carries no natural section.
  - `identity_fixes_everything_no_section` -- the identity on the
    one-view observer `blindObs = kernelObs (fun _ => ())` fixes every
    carrier point, and there is no section of any kind because no pair
    is admissible (`blindObs_no_admissible_pair`).
  **Countermodels.**  So "every automorphism has a fixed point" is
  neither the condition nor sufficient; "fixes an admissible pair" is
  the condition at one object.

## The many-object criterion: walks, forests, and the iff (sections 4-5)

Over a declared `HFamily` -- arrows listed with no closure, `HIsNatural`
quantifying over exactly the listed arrows -- the necessary and
sufficient condition is now a theorem, in two forms.

Definitions.  `Step D a b`: a declared arrow traversed forward (`fwd h`)
or backward (`bwd h`); `Walk D a b`: a list of steps with chained
endpoints; `Step.transport` / `Walk.transport`: the composite of the
declared transports, `mapPair` forward and `.symm.mapPair` backward;
`Walk.append`, `Walk.reverse`.  `Forest D`: a base object `root a` for
every object and a walk `path a : Walk D (root a) a` -- DATA, declared,
so no choice principle is used anywhere.  `Forest.gen h` for a declared
arrow `h : a → b` is the walk `path a ; fwd h ; (path b).reverse` from
`root a` to `root b`; `Forest.spread p` is the section that transports
the base pair `p (root a)` out along `path a`.

* **`natural_section_iff_generators`** (generator form; NO condition on
  the forest) -- a natural section exists iff some choice of pairs `p`
  satisfies, for every declared arrow `h : a → b`,
  `(T.gen h).transport (p (root a)) = p (root b)`.  Necessity is
  `Walk.transport_of_natural`: a natural section is carried to itself
  along every walk, backward steps included (`Step.transport_of_natural`
  uses the sealed `mapPair_symm_left`).  Sufficiency is the spread: the
  generator equation, after cancelling `(path b).reverse` against
  `path b` (`Walk.transport_reverse_transport`), is exactly naturality at
  `h`.  **Proved theorem**, with no axioms.
* **`natural_section_iff_holonomy`** (holonomy form; bases constant
  along arrows, `hroot : Hom a b → root a = root b`, i.e. one base per
  connected component) -- a natural section exists iff some choice of
  pairs is fixed by every closed walk at its base.  Derived from the
  generator form through `walk_maps_of_closed_fixed`, which turns
  "fixed by every closed walk at `r`" into "carried along any walk from
  `r` to a base equal to `r`" by substituting the equality of bases.
  **Proved theorem**, with no axioms.
* **`one_object_recovered`** -- the general theorem, specialised to
  `hAutoFamily O F` with the trivial forest (`root _ = ()`,
  `path _ = nil`), is the one-object iff of section 1: the single
  generator is `F` itself.  A consistency check, not new content.
  **Proved theorem.**

What the proofs settled about the clauses assessed before they were
written.  (a) Backward traversal: built into `Step.bwd`; the two
cancellation lemmas `Walk.reverse_transport_transport` and
`Walk.transport_reverse_transport` rest on the sealed
`mapPair_symm_left/right` and nothing else.  (b) One base per
component: needed only for the holonomy form (`hroot`); the generator
form holds for ANY assignment of bases and walks, including one that is
not a forest at all.  That is stronger than the assessed statement.  (c)
The fixed pair is common per base: it is `p (root a)`, one value per
base.  (d) The generators suffice: the generator form IS the theorem;
the holonomy form is derived from it, not the other way round.  (e) The
section is determined by its base values: it is `Forest.spread p`, and
the choice of walks changes the construction, not existence.
Existential per-base pairs would need choice to assemble; the theorem
quantifies over a function `p : HSec D` instead, which is the
constructive statement and the one that says the same thing.

Relation to the sealed module.  `no_natural_section_of_endo` is the
length-one-loop case of `Walk.transport_of_natural`; the sealed
non-claims -- multi-object families, naturality under a generating set,
arrows crossing objects with different carriers -- are now covered by
these theorems as far as `HFamily` reaches, and `HFamily` already
allows carriers and residual types to vary with the object.  The
sealed module is not amended; it is imported.

Still open.  A general embedding of the flat `Family` into `HFamily` is
untouched and remains the sealed module's OPEN item.  The hop fixture
below supplies the closed walks of length above one and the finite
holonomy computation that an earlier version of this paragraph listed
as missing.

## Hop fixture: predictions, written before the computation ran

The first fixture with closed walks of length above one.  Two hard-core
particles on a finite site graph.  Declared before running:

* Object: an unordered pair of distinct occupied sites, written sorted
  `{x < y}`.  Objects are UNLABELLED on purpose: with labelled particles
  and identity-on-labels hops, every closed walk is the identity on
  both graphs and the family is the cover, on which a section exists by
  construction.  That would test nothing.
* Carrier at every object: `Bool`, index `false` the smaller site,
  `true` the larger; observer `boolEqObs`; admissible pairs
  `(false, true)` and `(true, false)`, the two orientations.
* Arrow: a hop -- one particle moves to an adjacent site not occupied
  by the other.  Its transport is the identity when the mover stays on
  its side of the stayer and the swap `negIso` when it ends on the far
  side.  That flip bit is the whole modeling input; it is computed from
  the sorted positions, never tabulated by hand.
* Forest: breadth-first from the base object `{0, 1}` in the sorted
  order of objects; the criterion is `natural_section_iff_generators`
  (Lean) and, in Python, the same generator check: parity potential
  along the tree, every non-tree hop's generator must have even flip
  parity.

Predictions:

| site graph | prediction | why |
|---|---|---|
| open chain `P_n` | section exists | the particles cannot pass, so no hop flips and every closed walk is the identity |
| `2 x 2` square, `2 x 3` ladder | no section | the particles can trade places around the cycle, so some closed walk is the swap, which fixes no admissible pair |
| star `K_{1,3}` (a tree) | no section | the particles can trade places through the hub, so the swap appears without any cycle in the site graph |

Reading of the outcomes, agreed in advance.  If both the chain and the
square come out as predicted, the criterion reproduces
one-dimensional-versus-not from the hop graph alone -- and the star says
what "not" means: exchangeability, not dimension.  If the chain comes
out obstructed, the arrow set carries an identity the model should not
have (a flip where nothing passed).  If the square comes out clean, it
is missing one it should have (a pass counted as no flip).  If the star
comes out clean while the square is obstructed, the flip rule is wrong
in the branching case, not the graph.  Nothing in these fixtures names
a physical system; they are hop graphs and a parity, and stay that way.

### Results, written after the run (`holonomy_fixture.py`, receipt
`receipts/holonomy_fixture.json`; Lean `lean/NaturalSections/HopFixture.lean`)

Every prediction held.  Finite computation, then the Lean half:

| fixture | objects | hops | odd generators | verdict | as predicted |
|---|---|---|---|---|---|
| chain `P2` .. `P6` | 1, 3, 6, 10, 15 | 0, 4, 12, 24, 40 | 0 | section exists | yes |
| square `2 x 2` | 6 | 16 | 4 | no section; witness `{0,1} → {0,3} → {0,2} → {1,2} → {0,1}`, one flip | yes |
| ladder `2 x 3` | 15 | 56 | 8 | no section | yes |
| star `K_{1,3}` | 6 | 12 | 2 | no section; witness of six hops through the hub, three flips | yes |
| triangle `C_3` | 3 | 6 | 2 | no section | (not predicted; consistent) |

Lean carries three of them on the same six objects `Pair4`, differing
only in the adjacency function, with the transport rule `flipB` computed
from sorted positions and never tabulated (8 reports, no axioms):
`chain_has_natural_section` (the constant orientation is natural because
`chain_no_hop_flips`, decided over all 36 object pairs),
`square_no_natural_section` and `star_no_natural_section` (the Python's
witness walks, `sqWalk_transport` and `stWalk_transport` showing each
closed walk is the swap, then the sealed `negIso_fixed_point_free`
through `Walk.transport_of_natural`), and
`chain_square_star_separation` stating all three together.  These are the
first uses of the walk machinery on closed walks of length four and six
with nontrivial transport; NS-12 is closed by them.

Two negative controls in `test_holonomy_fixture.py`, each the failure
mode named above exhibited on purpose: with the flip bit forced to
`false` on every hop (the cover), the square comes out with a section;
with a spurious flip on ONE hop lying on a cycle of the configuration
graph (`{0,2} <-> {0,3}` on the chain `0-1-2-3`, whose objects
`{0,2}, {0,3}, {1,3}, {1,2}` form a 4-cycle), the chain comes out
obstructed.  So the flip bit is what carries the obstruction, in both
directions.

A finding from a failed first version of the second control, recorded
rather than hidden: flipping EVERY hop leaves every chain clean, and
the square too once its real flips are discarded.  A hop changes
`x + y` by one, so the configuration graph is bipartite, every closed
walk has even length, and a uniform flip contributes even parity to
every cycle -- a uniform relabelling of the fibre is a gauge, absorbed
by a section.  Only a flip that changes the parity of some cycle
obstructs, and the position-computed flip does exactly that on the
square and the star and never on a chain
(`test_a_uniform_spurious_flip_is_a_gauge_not_an_obstruction`).  "A
flip where nothing passed" therefore obstructs only when it is
non-uniform; the prediction table's reading of a chain failure stands,
with that qualification.

What this does and does not show.  It shows that the criterion, with
the declared hop rule, separates the open chain from every graph on
which two hard-core particles can trade places -- and the star shows
that "can trade places" is the invariant, not the presence of a cycle
in the site graph.  It shows nothing about weights, phases, or any
cancellation; the fibre is two-element and the holonomy is a parity.
That was the boundary stated before the run and it is unchanged by it.

## Three-label fixture: the generality check and the predictions, written before the computation ran

Generality check, done before anything was changed.  Sections 4-5 of
`NaturalSections.lean` mention no `Bool`, no `negIso`, no `boolEqObs`:
`Step`, `Walk`, `transport`, `Forest`, `natural_section_iff_generators`
and `natural_section_iff_holonomy` quantify over an `HFamily` whose
carriers are arbitrary types and whose arrows are arbitrary `PresIso`
bijections.  The invariant they prove is "some admissible pair is
carried by every generator" / "fixed by every closed walk", and
`fixed_pair_iff_two_fixed_points` unfolds it to "two distinct carrier
points, distinguished by the observer, fixed by the holonomy".  The
two-element case lives entirely in the fixture layer (`Hop.family`,
`car _ := Bool`, the sealed `negIso_fixed_point_free`).  The theorems
are not changed.

What the fibre is.  With `n` labels the carrier has `n` points and the
admissible pairs are the `n (n - 1)` ordered pairs of distinct labels.
The symmetric group is what ACTS; the fibre is the pair set.  The
theorem's invariant is therefore: the holonomy group has at least two
common fixed points.  At `n = 3` a non-identity permutation fixes at
most one point, so "no common fixed pair" and "holonomy nontrivial"
coincide, and parity is the invariant that can disagree -- a 3-cycle is
even and fixes nothing.  At `n = 4` "nontrivial" and "no fixed pair"
come apart too (a lone transposition fixes the other two labels); that
is the next test, not this one.

The model, `k` particles on a site graph: object = sorted `k`-subset of
occupied sites; carrier `Fin k`, index `i` the `i`-th smallest occupied
site; observer the kernel of the identity, so the admissible pairs are
the ordered pairs of distinct indices; arrow = one particle hops to an
adjacent empty site; transport = the induced permutation of sorted
indices, computed from positions.  At `k = 2` this is the flip bit of
the previous fixture, and the general code is checked against that
receipt on all nine graphs before anything at `k = 3` is believed.
Holonomy group at a base = closure of the forest generators; reported
per fixture: its order, whether every element is even, its common fixed
points, whether a fixed pair exists (the theorem's criterion), and
whether the group is trivial.

Predictions at `k = 3`:

| site graph | prediction | why |
|---|---|---|
| chain `P2` | vacuous: no object | three particles do not fit on two sites |
| chain `P3`, triangle `C3` | section exists, frozen | one object, no hop |
| chain `P4`, `P5`, `P6` | section exists, group trivial | order is preserved; every transport is the identity |
| square `2 x 2` | **no section, group of order 3, every element even** | one hole circulating the 4-cycle cyclically shifts the three particles: a 3-cycle, even, fixing no label -- parity says clean, the fixed-pair criterion says obstructed; this is the separating case |
| ladder `2 x 3` | no section, group the full symmetric group | with three holes both transpositions and 3-cycles arise; parity fails too, so not separating |
| star `K_{1,3}` | **section exists, group trivial** | one hole on a tree cannot circulate; the reverse of the `k = 2` verdict, because exchange needs room, not because of the fibre |

Reading, agreed in advance.  If the square comes out with an
even-only nontrivial group and no section, the invariant the theorem
proves is the fixed pair and not parity, and the `k = 2` agreement of
the two was a coincidence of the fibre size.  If the square comes out
with a section, the transport rule is wrong.  If the star comes out
obstructed at `k = 3`, the hop rule is admitting a move through an
occupied site.

### Results at `k = 3`, written after the run (`holonomy_group.py`,
receipt `receipts/holonomy_group.json`; Lean `lean/NaturalSections/HopFixture3.lean`)

The general code at `k = 2` agrees with the flip-bit receipt on all
nine graphs (`k2_agrees_with_flip_bit_receipt`), and at `k = 2` parity
and the fixed pair never come apart (`test_at_k2_parity_and_fixed_pair_never_come_apart`).
At `k = 3` every prediction held:

| fixture | objects | holonomy group | every element even | common fixed points | section (theorem) | parity says |
|---|---|---|---|---|---|---|
| chain `P2` | 0 | -- | -- | -- | exists (vacuous) | clean |
| chain `P3`, triangle `C3` | 1 | trivial | yes | all three | exists | clean |
| chain `P4`, `P5`, `P6` | 4, 10, 20 | trivial | yes | all three | exists | clean |
| **square `2 x 2`** | 4 | **order 3** | **yes** | **none** | **NO** | **clean** |
| ladder `2 x 3` | 20 | order 6 | no | none | NO | obstructed |
| star `K_{1,3}` | 4 | trivial | yes | all three | exists | clean |

The square is the separating case.  Its holonomy group is generated by
the 3-cycle `(1, 2, 0)` -- the hole circulating `{0,1,2} → {0,2,3} →
{1,2,3} → {0,1,3} → {0,1,2}` shifts the three particles cyclically --
which is EVEN and fixes no label.  Parity would call the square clean;
the criterion of `natural_section_iff_holonomy` calls it obstructed,
because no admissible pair is fixed.  **The invariant the theorems
prove is the fixed pair, not parity, and their agreement at `k = 2` was
a coincidence of the fibre size** (at two labels every non-identity
permutation is odd).

Lean carries it (`HopFixture3.lean`, 16 reports, 48 in the tree; nine
of the sixteen with no axioms, seven -- the ones decided through
`if`-defined maps and hop-by-hop case splits: `c3_is_even`,
`star3_generators`, `chain3_natural_section` and what is built from
them -- on `propext` alone, within the whitelist; the audit line
names each).
`hopPerm` computes each hop's permutation of sorted indices from the
hole positions by the formula `rank h' (if s = h'.site then h.site else s)`
with `s = occ h i`, for every pair of hole positions (`raw_lt`, `hop_inv`
decided over all of them); the same formula serves the square, the
star and the chain, which differ only in adjacency.
`parity_and_fixed_pair_come_apart` states, in one theorem: the
holonomy of the square's closed walk is `c3 = swap01 ∘ swap12` (a
composite of two transpositions, so even; `c3_is_even`), it fixes no
admissible pair (`sq3_no_fixed_pair`, from `c3_no_fixed`), and the
square has no natural section (`square3_no_natural_section`, through
the sealed-free `Walk.transport_of_natural`).  `star3_has_natural_section`
is the spread of the base pair along the forest with base the hole at
the hub, by `natural_section_iff_generators` with every generator
decided (`star3_generators`); `chain3_has_natural_section` is the
constant orientation.  `chain3_star3_square3_separation` states all
three.

Two things the run settled that the predictions did not state.  The
star's verdict REVERSES between `k = 2` (obstructed) and `k = 3`
(clean): with one hole on a tree the hole cannot circulate, so exchange
needs room, not a cycle -- density enters through the arrow set, not
the fibre.  And at `k = 3` "no common fixed pair" coincides with
"holonomy nontrivial", so this run cannot tell those two apart; the
`k = 4` case (a lone transposition fixes the other two labels and the
theorem then predicts a section despite nontrivial holonomy) is the
test that would, and it is the next one.

## Boundary and write root

Write root: `research/natural_sections/`.  The Lean package declares
NO Lake dependency: a path dependency on `../../../lean4` is built in
`lean4/.lake/`, outside the write root (a reviewer showed this on the
sibling S9-obligations tree).  Instead `verify_lean.py` stages the
snapshot blob of each of the 12 pinned modules, SHA-256-checked against
the manifest, into `lean/sealed/` (gitignored), and the `Derivation`
library of `lakefile.lean` compiles them inside `lean/.lake/`.  The
verifier diffs a repository-wide `git status --ignored` before and after
the build and fails by name on any new record outside the write root;
`test_clean_build_leaves_lean4_untouched_and_stays_inside_the_root`
rebuilds from nothing and asserts `lean4/.lake` is as present or absent
as before.  Verified on a checkout with no `lean4/.lake`: exit 0, and
none afterwards.

`SOURCE_MANIFEST.json` follows the primitive-difference tower's shape;
`verify_pins.py` resolves the snapshot, requires it to be an ancestor of
HEAD with the recorded tree, hashes every module at the snapshot and at
HEAD, requires the module list to equal the import closure of the root
in both directions, and refuses any modified, untracked, or
ignored-but-present file under a sealed prefix.

## Manual receipt

This tree's axiom reports are a manual receipt.  No CI gate reads them.
Nothing in `.github/workflows` runs `verify_lean.py` or `verify_pins.py`;
a pass is a receipt for the sources present when it ran and implies no
enforcement.  The registration diff that would add the Python checks to
the research job (not `verify_lean.py`, for the sibling trees' reason)
is the same shape as the sibling steps; it is not applied here.

## Non-claims

* No categorical structure is claimed for `Family`, `HFamily`, `Step`,
  `Walk`, or `Forest`; a walk is a list, "holonomy" names the transport
  along a closed walk, and no groupoid, fundamental group, or covering
  is asserted.
* A `Forest` is any assignment of bases and walks; nothing here proves
  that a spanning forest exists for a given family, and the theorems do
  not need one to.
* Nothing here derives `ContactKernel.no_equivariant_pair_valued_map`
  or touches the OPEN items the sealed module records.
* The countermodels separate the fixed-point reading from the
  fixed-pair reading; they say nothing about which automorphisms arise
  from any presentation theory.

## Commands (run from the repository root)

| command | exit | key line |
|---|---|---|
| `python research/natural_sections/verify_pins.py` | 0 | `import closure of ['Derivation.PresentationNaturality']: 12 module(s), all pinned`; `sealed prefixes clean` |
| `python research/natural_sections/verify_lean.py` | 0 | `Lean #print axioms declarations: 48 within ['Quot.sound', 'propext']`; 41 reports `no axioms`, 7 (all in `Hop3`) `['propext']`; `write root respected` |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python run_holonomy_fixture.py --out receipts` | 0 | five chains `section exists`; square, ladder, star, triangle `NO natural section` |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python run_holonomy_group.py --out receipts` | 0 | `k=3 square_2x2: NO natural section; parity says clean; ... group order(s) 3`; `k=3 star_K13: section exists` |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s . -p "test_*.py"` | 0 | `Ran 52 tests`, `OK` (the clean rebuild included) |
| `cd research/natural_sections && python -m mypy` | 0 | strict, 9 source files |
