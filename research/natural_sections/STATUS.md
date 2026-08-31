# Natural sections: the fixed-pair criterion, its fixtures, and its layers

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
"does not depend on any axioms".  The TREE's totals grew with each
later section and are recorded in ONE place, the commands table at the
end of this file; per-section counts below are historical and correct
for their own sections.  An earlier version of this heading carried a
tree total that went stale twice, and a repaired version still repeated
the table's numbers here -- both caught by a reviewer.  This heading now
carries no number at all.)

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

## Four-label fixture: predictions, written before the computation ran

The question (NS-25): does "the holonomy group is nontrivial" come
apart from "no common fixed pair"?  At `k = 4` a lone transposition
fixes the other two labels, so the theorem predicts a natural section
DESPITE nontrivial holonomy wherever exactly two particles can trade
places while two others are frozen.  On the nine graphs that situation
does not arise -- four particles on at most four sites are frozen or
do not fit -- so a tenth site graph is declared for it: the square
`0-1, 0-2, 1-3, 2-3` plus a DISJOINT edge `4-5`.  Particles cannot
cross between site-graph components, so the configuration graph splits
by how many particles sit on the edge, and each configuration component
is judged on its own (the holonomy form has one base per component).

Predictions at `k = 4`:

| site graph | prediction |
|---|---|
| chain `P2`, `P3`, triangle | vacuous: no object |
| chain `P4`, square, star | frozen: one object, section exists |
| chain `P5`, `P6` | trivial holonomy, section exists |
| ladder `2 x 3` (two holes) | nontrivial, no common fixed point, odd elements present: no section, parity obstructed; the group is expected to be large (3-cycles from a block with one hole, transpositions from a block with two) |
| square + edge, component with 4 on the square | frozen: section |
| square + edge, component with 3 on the square and 1 on the edge | group of order 3 (the `k = 3` square 3-cycle), even, one common fixed point (the edge particle, index 3): no fixed PAIR, no section, parity clean -- the `k = 3` separation again |
| **square + edge, component with 2 on the square and 2 on the edge** | **group of order 2 generated by the transposition `(0 1)` (the `k = 2` square exchange), odd, common fixed points `{2, 3}` (the frozen edge particles): a natural section EXISTS -- the constant pair `(2, 3)` -- although the holonomy is nontrivial and parity says obstructed** |

Reading, agreed in advance.  If the two-on-the-square component comes
out with a section and a nontrivial group, then "nontrivial holonomy"
is not the invariant either: the theorem is about a fixed pair, finer
than parity (the `k = 3` result) and coarser than triviality (this
one).  If it comes out obstructed, the transport is moving an index it
should not (the frozen particles' ranks must never change, since their
sites are the largest).  The Lean half carries that component: the
constant pair `(2, 3)` is natural, and the `k = 2` witness walk moves
`(0, 1)`.

### Results at `k = 4`, written after the run (`holonomy_group.py`,
receipt `receipts/holonomy_group.json` key `runs.k4`; Lean
`lean/NaturalSections/HopFixture4.lean`)

Every prediction held, including the designed one:

| fixture / component | objects | group | even | common fixed | fixed pair | section | parity says |
|---|---|---|---|---|---|---|---|
| chain `P2`, `P3`, triangle | 0 | -- | -- | -- | -- | vacuous | clean |
| chain `P4`, square, star | 1 | trivial | yes | all | yes | exists | clean |
| chain `P5`, `P6` | 5, 15 | trivial | yes | all | yes | exists | clean |
| ladder `2 x 3` | 15 | order 24 | no | none | no | NO | obstructed |
| square + edge, 4 on the square | 1 | trivial | yes | all | yes | exists | clean |
| square + edge, 3 on the square | 8 | order 3 | yes | `{3}` | no | NO | clean |
| **square + edge, 2 on the square** | 6 | **order 2** | **no** | **`{2, 3}`** | **yes** | **EXISTS** | **obstructed** |

The two-on-the-square component is the separating case: its holonomy
group is generated by the transposition `(1, 0, 2, 3)` (the two-label
square exchange), nontrivial and odd, yet indices `2` and `3` -- the
frozen edge particles -- are fixed by everything, so the pair `(2, 3)`
is admissible and fixed and a natural section exists.  With the `k = 3`
square (even holonomy, no fixed pair, no section) this pins the
invariant from both sides: **the theorem's criterion is a fixed
admissible pair -- finer than parity, coarser than trivial holonomy --
and neither of those two proxies is what was proved.**

Lean carries the separating component (`HopFixture4.lean`, 7 reports,
55 in the tree): objects `Hop.Pair4`, carrier `Fin 4`, the two-label
flip bit acting as the transposition `swap01Iso` of indices `0` and
`1`.  `walk_moves_pair01`: the two-label witness walk carries `(0, 1)`
to `(1, 0)`, so the holonomy is nontrivial; `constant23_natural`: the
constant pair `(2, 3)` commutes with every hop, decided hop by hop;
`nontrivial_holonomy_with_natural_section` states both together.

Not carried in Lean: the three-on-the-square component (the `k = 3`
square again, already carried there) and the ladder's order-24 group
(finite computation; the witness is a transposition `(0, 2, 1, 3)` and
the closure is decided in Python only).  `test_frozen_edge_particles_never_move_index`
checks the modeling assumption the Lean family encodes: in the
two-on-the-square component all sixteen hops fix indices `2` and `3`.

## Phase fibre: what is admitted, what is refused, and the predictions, written before the computation ran

Refused by name: a continuous phase.  It is neither finite nor
decidable, and every claim in this tree is decided by `decide` over
finite types.  `holonomy_phase.refuse_continuous_phase` raises when
asked for it.  Admitted instead: phases in `Z_N` with `N` declared
(`N = 4` primary; periodicity in `N` checked at `N = 2, 3, 6`).  That
is the whole of what a finite, decidable phase can be here, and the
results below are results about `Z_N`, never about the circle.

The extension is a change of carrier, not of theorem.  Carrier at every
object: `label x Fin N`, a phase register per particle.  Observer: the
kernel of the label projection, so two points are zero-related when
they carry the same label -- phases are INVISIBLE to distinctness and
the admissible pairs are, as before, the ordered pairs of distinct
labels, now each carrying a phase.  Arrow: a hop; its transport is
`(l, phi) -> (sigma l, phi + theta_l)`, a finite bijection: the mover's
register gains the declared edge phase `A(u, v)` of its hop, every
other register is unchanged, `A(v, u) = -A(u, v)`.  The holonomy of a
closed walk is a pair (permutation, phase-shift vector) in the wreath
product of `Z_N` by the symmetric group.  `natural_section_iff_generators`
and `natural_section_iff_holonomy` apply verbatim; the invariant reads:
two labels fixed by every holonomy's permutation with zero phase shift
on both.

A limit stated in advance: with one particle there is no admissible
pair, so a single-particle flux is invisible to this fibre.  A phase can
obstruct only relative to a second label.  The fixture with one mobile
particle and one frozen reference is the test of whether that limit is
the right one.

Connections declared: the square carries flux `Phi` placed on the edge
`0-1` (`A(0,1) = Phi`, every other edge `0`); the chain and the star
carry `A(i, j) = j` on their edges (nonzero, and pure gauge on a tree);
the disjoint edge `4-5` carries `0`.  A gauge transformation
`A'(u, v) = A(u, v) + g(v) - g(u)` conjugates every holonomy by a
natural automorphism, so every verdict and every group order must be
unchanged by it; that is checked, not assumed.

Predictions (`k` particles, `N = 4`):

| fixture | prediction |
|---|---|
| chain `P4`, `k = 2`, nonzero edge phases | section exists; holonomy trivial (every particle's site path in a closed configuration walk is a closed walk on a tree, so its net phase is `0`) |
| star, `k = 3`, nonzero edge phases | section exists; trivial, for the same reason |
| square, `k = 2`, any `Phi` | no section for every `Phi`: the exchange (permutation part the swap) obstructs before any phase can; its square is the pure phase `(Phi, Phi)` on both registers |
| **square + edge, `k = 2`, one particle on each (8 objects), `Phi = 0`** | **section exists; holonomy trivial** |
| **square + edge, `k = 2`, one on each, `Phi = 1, 2, 3`** | **no section, with the permutation part TRIVIAL: the square particle circulating gains `Phi` on its register while the edge particle gains `0`, so no pair is fixed -- the pure-phase obstruction, relative to the frozen reference** |
| square + edge, `k = 2`, `Phi = N` | section exists: `Z_N` periodicity |
| square + edge, `k = 4`, two on the square and two on the edge, any `Phi` | section exists for every `Phi`: the frozen pair `(2, 3)` has zero shift always; flux on labels that carry no fixed pair changes nothing |
| every fixture under a gauge transformation | identical verdict and identical group order |

Reading, agreed in advance.  If the one-on-each fixture separates
`Phi = 0` from `Phi != 0` with trivial permutation part, the fibre sees
a pure phase obstruction and sees it only relative to a reference label,
as stated.  If `Phi != 0` comes out with a section there, the transport
is dropping the phase; if `Phi = 0` comes out obstructed, the phase
rule is not antisymmetric.  If a gauge transformation changes a verdict,
the family is not what it claims to be.  The Lean half carries the
one-on-each fixture: `Phi = 0` has a natural section, `Phi != 0` has
none, for every `Phi : Fin 4`, decided.

### Results, written after the run (`holonomy_phase.py`, receipt
`receipts/holonomy_phase.json`; Lean `lean/NaturalSections/HopFixturePhase.lean`)

A slip, recorded first.  The square-plus-edge graph at `k = 2` has
THREE configuration components -- both particles on the square (the
two-label exchange, obstructed for every flux), one on each (the
question), both on the edge (frozen) -- and the fixture-level verdict
is the conjunction over all three, so it is "no section" for every
flux.  The first version of the periodicity check read that
fixture-level verdict and printed all-false.  The prediction table
above names the one-on-each COMPONENT, and that is where the question
lives; the checks now read that component (`holonomy_phase.one_on_each`),
and `test_fixture_level_verdict_is_the_conjunction_over_components`
keeps the distinction visible.  No prediction was wrong; a check was
pointed at the wrong object.

At the component level every prediction held (`N = 4`):

| fixture / component | group order | permutation part | phase part | fixed pair | section |
|---|---|---|---|---|---|
| chain `P4`, `k = 2`, tree phases | 1 | trivial | trivial | yes | exists |
| star, `k = 3`, tree phases | 1 | trivial | trivial | yes | exists |
| square, `k = 2`, flux `0, 1, 2, 3` | 2, 8, 4, 8 | the swap | trivial only at `0` | no | NO, every flux |
| **one on each, flux `0`** | 1 | trivial | trivial | yes | **exists** |
| **one on each, flux `1, 2, 3`** | 4, 2, 4 | **trivial** | nontrivial | **no** | **NO: the pure phase obstruction** |
| one on each, flux `4` | 1 | trivial | trivial | yes | exists (`Z_4` periodicity) |
| square + edge, `k = 4`, two on the square, flux `0..3` | 2, 8, 4, 8 | the swap on `0, 1` | -- | yes: `(2, 3)` with zero shift | exists, every flux |
| gauge transformation, every fixture | unchanged | unchanged | -- | unchanged | unchanged |

Periodicity holds at `N = 2, 3, 4, 6`, and the verdict is compatible with
refinement of the modulus: for `N | M` and every `phi` in `Z_N`, the
one-on-each verdict at `(phi, N)` equals the verdict at `((M / N) phi, M)`,
checked for `2 | 4`, `2 | 6`, `3 | 6`, `4 | 8`, `4 | 12`
(`refinement_compatibility`).  The verdict is therefore an invariant of
the directed system of moduli under divisibility -- the finite shape of
"the same in the limit".  That check is a bonus, not the argument; the
argument is the next paragraph.

**The phase group does not need to be finite.**  `HopFixturePhase.lean`
is parametrized over an arbitrary `AbGroup G` -- a type with an
addition, a zero and a negation obeying the group laws, with NO
decidable equality and NO finiteness assumed -- and proves
`section_iff_flux_zero`: over the one-on-each family with flux
`Phi : G`, a natural section exists iff `Phi = 0`.  The forward
direction is group cancellation (`AbGroup.cancel`) applied to the
square particle's register, which the walk `0 -> 1 -> 3 -> 2 -> 0`
returns shifted by exactly `Phi` (`comp_label0`) while the edge
particle's is unchanged (`comp_label1`); the backward direction is the
constant section, natural because every edge phase is `0` or `-0`
(`constant_natural_of_zero_flux`).  Decidability is used only on sites
and labels (`tag_antisymm`, `stag_antisymm`, `two_labels`).  The
`Z_4` instance `fin4Phase` recovers the computed fixture
(`section_iff_flux_zero_fin4`).  Any abelian group the metatheory
supplies -- the integers, the circle -- is an instance; this tree
constructs none of them and needs none.  17 reports, 72 in the tree.

What the phase fibre does and does not see, settled.  It sees a pure
phase obstruction (permutation part trivial) exactly when the flux is
nonzero, and only RELATIVE to a second label: the reference particle's
register is what the square particle's is compared against.  With one
particle there is no admissible pair and nothing to compare, so a
single-particle flux is invisible, as stated before the run.  Flux on
labels that already carry a fixed pair changes nothing (`k = 4`, the
frozen pair).  What the fibre does not see: amplitudes, weights, or any
cancellation -- a holonomy is a group element, never a sum.

## Weighted layer: the types crossed, the predictions, written before the computation ran

Every theorem so far is about group elements; this layer is where sums
enter, and it enters as a NEW layer over `HFamily`: nothing below it is
changed.  Declared in `lean/NaturalSections/WeightedLayer.lean`:

* `Weighting D R`: an amplitude `amp h : R` and a reverse amplitude
  `ramp h : R` for every declared arrow.  `R` is any type with `Mul`,
  `One` (for products) and `Add`, `Zero` (for sums).  Commutativity,
  distributivity and the ring axioms are NOT assumed; the prediction
  below is that no theorem of this layer needs them, and that is
  recorded as a finding if it holds.
* `Walk.weight w : R`: the product of the step amplitudes, `1` on `nil`;
  a backward step contributes `ramp h`.
* `total ws : R`: the sum of the weights of a DECLARED finite list `ws`
  of closed walks at a base `r`.  The set of all closed walks is
  infinite; the finite list is the object the theorems are about.
* `twisted ws p : R`: the sum over `ws` of `weight w` if `w` fixes the
  admissible pair `p` and `0` otherwise -- the sum "read in the local
  convention `p`".  Deciding `w.transport p = p` needs decidable
  equality on the fibre at `r`, which is supplied as an argument.

The proposed theorem, as stated: "if a natural section exists, the
weighted sum over closed walks at a base factors through the section:
the section partitions the admissible pairs into orbits on which the
transport is constant, and the sum reduces to a sum over orbit
representatives times an orbit weight."

Predictions:

| claim | prediction |
|---|---|
| **A1** (section collapses the convention) | PROVED, for every `R` and every `ws`: if `s` is a natural section then `twisted ws (s r) = total ws`.  Every closed walk fixes `s r` (`Walk.transport_of_natural`), so every term is read in full.  No ring law is used. |
| **A2** (orbit form) | NOT true as stated.  `twisted ws` is constant on a holonomy orbit only when `ws` is closed under conjugation by the holonomy with weight preserved; a single generator walk on a family whose holonomy group is transitive on pairs but has non-identity elements with fixed pairs (four labels, the ladder, holonomy the full symmetric group) gives two pairs in one orbit with different twisted sums.  The counterexample is computed; the repaired hypothesis is stated, not proved. |
| **A3** (converse of A1 fails) | `twisted ws p = total ws` does NOT imply a section: on the two-label square (no section) with amplitudes `+-1` in the integers, a list of three closed walks -- the empty walk, the exchange walk with weight `-1`, and a backtrack-then-exchange walk with weight `+1` -- has `twisted = total = 1` at every pair with every amplitude nonzero.  PROVED as a countermodel. |
| **B1** (counting detects the class) | With unit weights in the natural numbers, `twisted ws p = total ws` iff every walk in `ws` fixes `p`; hence if `ws` carries a walk moving every pair (as it does when `ws` contains the forest generators of a family with no section), `twisted ws p < total ws` for every `p`.  PROVED. |
| **B2** (ring sums are silent) | For every value `v` in the ring there is a weighting with `twisted ws p = v`, on the obstructed square and on the unobstructed chain alike (a backtrack walk with amplitude `v`).  The class constrains NOTHING about the value of a ring-weighted sum: no cancellation is forced, no bound, no lower bound on distinct orbits reachable by the value.  PROVED as a theorem, on both families. |
| **B3** (what the class does force) | Structure, not value: no section means for every pair `p` some closed walk moves `p`, so `twisted ws p` misses the weight of at least one walk of `ws` whenever `ws` contains that walk.  Whether the missing weight is visible in the value depends on `R`: in the natural numbers yes (B1), in a ring it can be `0` (A3).  PROVED as `twisted ws p = total ws - moved ws p` with `moved` the sum over the moving walks, in the natural numbers. |
| existing theorems needing change | NONE.  `Step`, `Walk`, `transport`, `Forest`, both iff theorems and every fixture are imported as they are; the layer uses `Walk.transport_of_natural` and nothing else from them. |

Computed fixtures (`weighted_sum.py`): closed walks at the base up to a
declared length on the chain `P4` and the square at `k = 2` (unit
weights, sign weights `amp = -1` on flipping hops) and on the ladder at
`k = 4` (the orbit counterexample).  Predicted: on the chain `twisted =
total` at every pair; on the square `twisted < total` at every pair
under unit weights and `twisted = number of even-parity walks` under
sign weights; on the ladder, with `ws` the generator walks, two pairs of
one holonomy orbit with different twisted sums.

Reading, agreed in advance.  If A1 fails, the definition of `twisted`
is not reading the convention it claims to.  If B2 fails, the ring is
constraining the sum through some law the layer did not declare.  If
the ladder shows twisted sums constant on every orbit, A2 holds more
generally than predicted and the conjugation hypothesis is not needed.

### Results, written after the run (`weighted_sum.py`, receipt
`receipts/weighted_sum.json`; Lean `lean/NaturalSections/WeightedLayer.lean`)

A slip, recorded first.  The first version of the sign weighting for A3
put `-1` on the arrow `{0,1} -> {1,2}`, which the exchange walk does not
traverse (it uses `{1,2} -> {0,1}`); `decide` refuted the claimed weight
`-1`, which is the kernel doing its job.  The weighting was corrected to
`-1` on both arrows between `{0,1}` and `{1,2}`, giving the exchange
`-1` and backtrack-then-exchange `+1` as pre-registered.  No prediction
changed; a witness was mis-specified and the checker caught it.

A second catch, by the axiom audit: the first version of
`value_silent_about_class` packaged the two existentials with
`Exists.choose`, and `verify_lean.py` refused it by name --
`depends on disallowed axioms: ['Classical.choice']`.  The goal is a
`Prop`, so `Exists.elim` does the job without choice, and the audit
passes again.  Recorded because it is the whitelist biting on a real
proof, not on an injection.

Every prediction held:

| claim | outcome | evidence |
|---|---|---|
| A1 | PROVED for every `R` with `Mul`, `One`, `Add`, `Zero`, every weighting, every list: `twisted ws (s r) = total ws` when `s` is natural. | `twisted_of_natural`, no axioms |
| A2 | As predicted, not true as stated.  Ladder, four labels, `ws` = one generator walk of holonomy the transposition `(0, 2, 1, 3)`: the pairs `(0, 3)` and `(1, 0)` lie in one holonomy orbit (the group is the full symmetric group, transitive on ordered pairs) and have twisted sums `1` and `0`.  The hypothesis the orbit form needs is closure of `ws` under conjugation by the holonomy with weight preserved; it is stated, not proved. | `orbit_counterexample`, `test_orbit_counterexample` |
| A3 | PROVED countermodel over the integers with every amplitude nonzero: on the square, `ws = [nil, exchange, backtrack ; exchange]` with weights `1, -1, +1`, `twisted = total = 1` at both pairs, and the square has no natural section. | `Sq.sum_blind_to_obstruction`, `Sq.weights_ws3` |
| B1 | PROVED: with unit weights in the natural numbers `twisted ws p = total ws` iff every walk in `ws` fixes `p`, and one moving walk in `ws` makes `twisted ws p < total ws`. | `count_eq_length_iff`, `count_lt_of_mover`, `count_le_length`, `total_unit` |
| B2 | PROVED: for every integer `v` a weighting with `twisted = total = v` exists on the obstructed square and on the unobstructed chain alike (a backtrack walk with amplitude `v`).  The class constrains nothing about the value of a ring-weighted sum. | `Sq.every_value_square`, `Ch.every_value_chain`, `value_silent_about_class`, `every_value` |
| B3 | The forced content is structural: no section means every pair is moved by some closed walk, and in the natural numbers that is visible (B1); in a ring it can vanish (A3).  Computed: chain `18` closed walks up to length `6`, `twisted = total` at both pairs; square `147` walks, `twisted = 95 < 147` at both pairs with `52` movers, and under sign weights `twisted = 95` (the even walks) while `total = 43 = 95 - 52`; star `31` walks, `twisted = 29` with `2` movers. | receipt `fixtures`, `test_square_twisted_below_total_and_sign_twisted_counts_even_walks` |
| existing theorems changed | NONE.  `WeightedLayer.lean` imports `NaturalSections` and `HopFixture` as they are and uses `Walk.transport_of_natural`, `Step.inv_transport`, `square_no_natural_section` and the fixtures' walks; no definition below the layer was edited. | the diff |

A finding about the types, as predicted: no theorem of the layer uses
commutativity, associativity, distributivity, or any ring law.  `R`
needs `Mul` and `One` for products and `Add` and `Zero` for sums, and
the counting results need the natural numbers' order.  "Commutative
ring" was the declared ambition; what the theorems consume is two
monoid-shaped operations, and the layer's signature says so.

What a natural section buys for a weighted sum, in one sentence: the
freedom to read every closed walk in one convention, so that the
convention-dependent sum `twisted` is the convention-free sum `total`
(A1); and what its absence forces is that no single convention reads
every walk (B3), which the value shows only when the weights cannot
cancel (B1 versus A3, B2).

## Re-presentation: what removes an obstruction and what cannot -- predictions, written before the computation ran

The question: over a declared class of re-presentations of a family,
does some member carry a natural section?  Two kinds of change are
declared and kept apart:

* A **pointwise re-presentation**: the same objects and the same arrows,
  each object presented through a presentation isomorphism
  `g a : PresIso (D.obs a) (O' a)` of its own, every arrow's transport
  conjugated accordingly: `iso' h = (g a).symm ; D.iso h ; g b`.  This is
  "the same family, described differently at every object" -- a change
  of convention at each object, carried consistently along the arrows.
* A **change of family**: different arrows (deleting hops), different
  objects (the labelled cover), or a different fibre (the symmetrised
  pair).  These are the three moves already on record: remove an arrow,
  build a cover, take a quotient.

Predictions:

| claim | prediction |
|---|---|
| **T1** (pointwise re-presentation never changes the class) | PROVED, for every `HFamily` and every pointwise `g`: a natural section of `D` exists iff one exists for the re-presented family.  A section `s` goes to `a ↦ (g a).mapPair (s a)` and back through `(g a).symm`; naturality is carried by the sealed `mapPair_trans` and `mapPair_symm_left`.  No obstruction is a presentation artifact. |
| **T1 on the fixtures** | The square at two labels has no natural section under any of its `2^6 = 64` pointwise re-presentations (each object's `Bool` carrier presented by the identity or the swap); the chain has one under all `64`.  Computed exhaustively and, in Lean, stated for every `g` as an instance of T1. |
| **T2** (what removes it: deleting arrows) | On the square's two-label configuration graph (six objects, eight undirected hops, two of them flipping), the class becomes trivial exactly for those hop subsets in which every remaining cycle has even flip parity.  Predicted: no single deletion suffices; the minimum cut has size `2`; the cuts are enumerated, all `2^8 = 256` subsets, per component.  Removing an arrow is the first of the two rules, and this is what it costs. |
| **T3** (what removes it: building structure) | The labelled cover of the same graph (the two-label family with the flip bit dropped, which is the family of labelled configurations read through unlabelled ones) has a section -- the negative control already on record -- and the frozen reference of the four-label fixture supplies a fixed pair without touching the mobile pair's obstruction.  Building structure is the second rule; it does not remove the obstruction of the pair that carries it, it adds a pair that does not. |
| **the residual** | What survives both rules within a declared budget of deletions and additions is the class itself: T1 says it cannot be described away, T2 says what it costs to cut, T3 says what it costs to cover.  That residual is named in the reading below and is not a rule. |

Reading, agreed in advance.  If any pointwise re-presentation of the
square comes out clean, T1's proof is wrong or the enumeration is not
conjugating the transports.  If a single deletion trivialises the
square's class, the cut prediction is wrong and the number is recorded
as computed.

### Results, written after the run (`representation.py`, receipt
`receipts/representation.json`; Lean `lean/NaturalSections/Represent.lean`)

| claim | outcome |
|---|---|
| T1 | PROVED for every `HFamily` and every pointwise re-presentation `P : Repres D`: `natural_section_iff_repres`.  The section is pushed by `a ↦ (P.g a).mapPair (s a)` (`Repres.push_natural`) and pulled back through `(P.g a).symm` (`Repres.pull_natural`); the only sealed facts used are `mapPair_trans` and `mapPair_symm_left`.  `obstruction_survives_repres` is the contrapositive; `square_obstruction_survives` and `chain_section_survives` instantiate it for EVERY re-presentation of those two families, in any carriers and observers. |
| T1 on the fixtures | square: `64` re-presentations, `0` with a section; chain: `64`, `64`; star: `64`, `0`.  The class was invariant in every case, as the theorem says it must be. |
| T2 | square: `256` hop subsets, `207` with a section, minimum deletion `2`, no single deletion suffices, eight minimal cuts (the two flipping hops together are one of them; the others isolate a flipping hop so that every remaining cycle crosses both or neither).  Chain: all `64` subsets keep the section.  Star: minimum deletion `1` -- not predicted, recorded as computed: its configuration graph carries a single odd cycle. |
| T3 | The cover (flip bit dropped) has a section on every graph.  The frozen reference is the `k = 4` result already on record. |

What this settles, in the tree's own words.  Two rules were guessed:
remove an obstruction, or build structure.  The theorems now say what
each one is and what it costs.  Removing is deleting arrows; T2 prices
it, and T1 says that no re-description at the objects -- however clever,
in whatever carriers -- counts as removing, because the class does not
move under any of them.  Building is adding a cover or a reference; T3
says it works and does not touch the pair that carries the obstruction.
What neither rule reaches within a declared budget of deletions and
additions is the residual, and the residual is not a third rule: it is
the class, which T1 shows cannot be described away.

## The cut theorem, and whether the dynamics generates the class -- predictions, written before the computation ran

Two questions, both declared before running:

1. **The cut theorem.**  NS-44 computed that deleting the square's two
   flipping hops trivialises its class.  Predicted Lean: the family with
   those two hops removed (`cutFamily`, arrows exactly the non-flipping
   hops, the same transport rule) carries the constant orientation as a
   natural section; `cut_removes_exactly_the_flips` states that the
   deleted arrows are exactly the flipping ones; `cut_theorem` packages
   the cut's section with the square's obstruction.  Minimality of the
   cut stays finite computation (NS-44); the Lean half is the positive
   direction only.
2. **Counts are class-blind.**  The only thing a declared family
   generates by itself is its walks, and the only weight the tower
   produces is a count (B1).  Predicted: the square and its cover (the
   same objects and arrows with every transport the identity) have
   definitionally the same walks -- a length-preserving bijection in
   Lean (`reWalk`, `unWalk`, round trips, `reWalk_length`) -- hence the
   same closed-walk count at every length, while the cover has a natural
   section and the square has none (`dynamics_blind_to_class`).
   Computed: identical count sequences by length up to `6` at the base,
   and different convention-read counts (`twisted`, B1): `147 = 147`
   per length in total, `95` versus `147` at the pair.  So the dynamics
   generates counts, raw counts cannot carry the class, and the class
   enters only when counts are read in a convention -- which is what an
   adapter would have to do.

Reading, agreed in advance.  If the cut family fails to carry the
constant section, the transport rule is flipping a hop the cut kept.  If
any closed-walk count differs between square and cover, the bijection
claim is false and the families do not share their arrows after all.

### Results, written after the run (`dynamics_counts.py`, receipt
`receipts/dynamics_counts.json`; Lean `lean/NaturalSections/CutAndCounts.lean`)

Both predictions held.

1. **The cut theorem is carried** (`cut_theorem`, no axioms): `cutFamily`
   -- the square's objects and exactly its non-flipping hops, transport
   rule unchanged -- carries the constant orientation
   (`cut_natural_section`, decided hop by hop through `cut_no_hop_flips`),
   `cut_removes_exactly_the_flips` states the deleted arrows are exactly
   the flipping ones, and the square itself stays obstructed.  Minimality
   of the two-hop cut remains finite computation (NS-44).
2. **Counts are blind to the class** (`dynamics_blind_to_class`, no
   axioms): `reWalk` and `unWalk` translate the square's walks to the
   cover's and back, inverse and length-preserving, so every closed-walk
   count agrees; the cover carries the constant section
   (`cover_natural_section`) and the square carries none.  Computed:
   counts by length `0..6` at the base are `[1, 0, 2, 0, 16, 0, 128]`
   for BOTH; the convention-read counts (walks whose holonomy fixes the
   pair, B1) are `[1, 0, 2, 0, 12, 0, 80]` on the square and equal to
   the totals on the cover.  On the chain, totals and convention-read
   counts agree, as a section requires.

What this answers.  The only thing a declared family generates by
itself is its walks, and so the only weight it generates is a count of
them.  Those counts cannot carry the class: two families with the same
objects, the same arrows and the same counts differ in it.  The class
lives in the transports, and a count sees it only when read in a
convention.  So an adapter that brings only "how many" brings nothing
the class can bite on; the reading -- which walks count as returning to
themselves -- is where the class enters, and that reading is exactly
what a natural section makes globally consistent.

## Refinement: the class is a mesh invariant -- predictions, written before the computation ran

The question: what survives refining a family?  A SUBDIVISION of a
declared arrow `h0 : a0 -> b0` is: a fresh midpoint object with a
declared presentation, a declared factorization `F` of `h0`'s transport
(first half `F`, second half `F.symm ; iso h0`), and the two half-arrows
added.  The original arrow is RETAINED: its naturality equation is
implied by the two halves' (the halves compose to it), so retention and
deletion agree on sections while retention needs no arrow-removal
machinery; that equivalence is stated in prose, not proved.

Predictions:

| claim | prediction |
|---|---|
| **R1** (single-step invariance, Lean, general) | PROVED for every `HFamily`, every arrow, every declared midpoint and factorization: a natural section exists iff one exists for the subdivided family (`natural_section_iff_subdiv`).  Forward: the midpoint's value is FORCED -- `F.mapPair (s a0)` -- so refining adds no freedom; backward: restrict to the old objects.  Finite chains of subdivisions compose by transitivity of the iff. |
| **R2** (the fixtures' verdicts never move) | Every one-step subdivision of the two-label square is obstructed and every one of the chain keeps its section (`square_subdiv_obstructed`, `chain_subdiv_section`, quantified over ALL declared subdivisions at once).  Computed: subdividing every hop of the square, chain and star once and twice (each hop replaced by two, the flip bit carried by the first half) leaves every verdict identical while objects and hops roughly double and closed-walk counts grow. |
| **R3** (what refinement means here) | Per-step quantities (walk counts, hop counts) are NOT refinement invariants; the class, and parity per cycle, are.  "Has meaning in the limit" = "is a refinement invariant" becomes a checkable definition, and nothing in it orders the refinement sequence: the verdicts cannot tell which refinement came first. |

Reading, agreed in advance.  If some subdivision of the square comes
out clean, the factorization is leaking freedom into the midpoint (the
forced-value lemma is wrong); if the chain loses its section, the
half-arrows fail to compose to the original transport.

### Results, written after the run (`refinement.py`, receipt
`receipts/refinement.json`; Lean `lean/NaturalSections/Refinement.lean`)

All three predictions held.

* **R1 PROVED** (`natural_section_iff_subdiv`, no axioms; 6 reports):
  for every family, arrow, midpoint presentation and factorization, a
  natural section exists iff one exists after the subdivision.  The
  midpoint's value is forced (`Subdiv.push`), the backward direction is
  restriction (`Subdiv.pull`); the only sealed facts used are
  `mapPair_trans` and `mapPair_symm_left`.  `class_refinement_invariant`
  is the contrapositive.
* **R2 held**: `square_subdiv_obstructed` and `chain_subdiv_section`
  quantify over EVERY declared one-step subdivision at once.  Computed
  over two rounds of subdividing every hop: square `6/8 -> 14/16 ->
  30/32` objects/hops with odd generators `2, 2, 2` and no section at
  every round; chain `6/6 -> 12/12 -> 24/24`, section at every round;
  star odd generators `1, 1, 1`, no section at every round.
* **R3**: per-step quantities changed, the class and the per-cycle
  parity count did not.  "Has meaning under refinement" = "is a
  refinement invariant" is now a checkable definition, and nothing in
  the verdicts orders the rounds.

### Review repairs (pull request 98)

A reviewer found four defects; each is repaired here, with the record.

1. **The Lean theorem covered retention, the fixtures replacement.**
   `Subdiv.family` keeps the original arrow; `refinement.py` removes it.
   The prose note that the two agree was not a proof.  Now proved:
   `Repl` is the REPLACEMENT operation -- the arrow removed from the
   family, the two decidabilities that let the instruction point at it
   (`decObj`, `dec0`) declared as data -- and
   `natural_section_iff_repl` carries the iff with the removed arrow's
   equation DERIVED from the two halves (`Repl.h0_equation`).
   `square_repl_obstructed` and `chain_repl_section` quantify over every
   one-step replacement.  The retained version stands as the weaker
   sibling it always was.
   **Second round**: the reviewer then observed that `Repl` removes only
   ONE oriented declaration while the fixtures declare every hop in both
   directions, so the reverse arrow survived with the same constraint.
   `ReplE` is the edge replacement: BOTH oriented declarations removed
   through one shared midpoint with all four half-arrows declared; the
   instruction additionally carries `ne0` (an edge, not a loop) and
   `rev_inverts` (the declared reverse transport inverts the declared
   forward one -- what makes two oriented declarations ONE edge; every
   fixture satisfies it).  The removed forward equation is derived from
   the halves (`ReplE.h0_equation`), the removed reverse equation from
   the forward one and `rev_inverts` (`ReplE.h0r_equation`);
   `natural_section_iff_replE` is the iff, `square_replE_obstructed` and
   `chain_replE_section` the quantified corollaries, and `sqReplE` /
   `chReplE` are concrete instances showing they are not vacuous, and
   `sqReplEFlip` (the flipping edge `{0,1} -- {1,2}`) discharges
   `rev_inverts` nontrivially, by the swap being an involution -- a
   reviewer's hardening suggestion.
   `Repl` stands as the one-orientation special case.
2. **The commands table (the single source of totals) was stale again**;
   it is refreshed below and remains the only place totals live.
3. **NS-51 said objects and hops double.**  Objects follow
   `V' = V + E`, only hops double (`E' = 2E`): square `6 -> 14 -> 30`
   objects against `8 -> 16 -> 32` hops.  The ledger row is corrected
   and the recurrence is now asserted by a test.
4. **"Closed-walk counts grow" was asserted, not computed, and is false
   under the fixed length-6 budget**: they DECREASE -- square
   `147 -> 33 -> 29`, chain `18 -> 10 -> 9`, star `31 -> 29 -> 29` --
   because each old hop becomes two steps.  The counts are now in the
   receipt (`closed_walks_len6`) and pinned by a test; the correct
   statement, which is all R3 needs, is that the counts CHANGE while
   the verdicts do not.

## Budget closure: is "polynomial" forced or declared? -- predictions, written before the computation ran

The question, stated internally.  A budget is a function from a size to
a step allowance.  The tower forces exactly two operations on budgets:
COMPOSITION (chaining -- a walk of refinements, a re-presentation of a
re-presentation: costs substitute) and POINTWISE PRODUCT (nesting -- a
walk of walks, a phase per step: costs multiply).  What it does not
force is the set of GENERATORS: which single moves are declared cheap.
The received robustness claim about computation is, in this vocabulary,
the declaration that presentation moves are linear, plus the two forced
closures.  Predictions:

| claim | prediction |
|---|---|
| **BC1** (the forced closure of linear is polynomial) | PROVED in Lean: every budget in the closure of the linear budgets under composition and pointwise product is polynomially bounded (`gen_linear_polyBounded`), and every polynomial bound `(n+1)^k` is reached (`pow_in_gen_linear`).  So "polynomial" = the two forced operations applied to linear generators: the OPERATIONS are forced, the class is theirs. |
| **BC2** (the generators are not forced) | PROVED in Lean: adjoin one budget outside (the doubling budget `2^n`) as a declared generator and the closure escapes every polynomial bound (`two_pow_not_polyBounded`, `generators_decide_the_class`).  The class is determined by the declared generators, not by the closure operations alone.  "Polynomial" is therefore forced RELATIVE to the declaration that elementary moves cost linearly -- a declaration, not a theorem, and now visibly so. |
| **BC3** (the decision layer fits the forced class; the summation layer does not) | Computed: an instrumented section-decider (parity potentials plus a generator check) stays within a DECLARED linear budget `steps <= 60 * (V + E)` on every fixture, across refinement rounds and re-presentations; the instrumented closed-walk summation meter exceeds that same budget on the square at walk-length budget `6` and grows by a factor above `2` per added length `2`.  Deciding whether a keyed convention exists is cheap in the forced class; evaluating keyless sums is not. |

Reading, agreed in advance.  If the decider breaches its declared
linear budget, the potential construction is not the linear-time object
it claims to be and the budget or the code is wrong -- say which.  If
the summation meter fits the linear budget, the contrast claim dies.
BC1/BC2 are theorems and can only fail by being unprovable; a blocked
lemma is recorded with its blocker.

What this answers, in the tree's own words.  A keyed convention (a
natural section) either exists or does not, and deciding which is a
computation inside the closure the tower forces on linear declarations.
The obstruction's cost lives elsewhere: in sums read without a key.
And the key that survives gauge is never among the attributes gauge
moves (the re-presentation theorem): when it exists at all, it is a
reference pair no walk moves -- the boundary, not the bulk.

### Results, written after the run (`budget_meter.py`, receipt
`receipts/budget_meter.json`; Lean `lean/NaturalSections/Budgets.lean`)

* **BC1 PROVED, then repaired on review**: `gen_linear_polyBounded` --
  every budget in the closure of the linear budgets under composition
  and pointwise product is polynomially bounded -- and
  `pow_in_gen_linear` -- every bound `(n+1)^k` is reached.  An earlier
  version of this bullet ended: the class of polynomial budgets "is
  exactly what the two forced operations make of linear generators".
  Both halves were wrong and a reviewer caught both.  The operations
  are DECLARATIONS (nothing ties them to walks, refinement, or
  re-presentation, and no exhaustiveness theorem exists), and the
  closure is NOT the polynomial class: its members are all monotone
  (`gen_linear_mono`) while the parity budget `n % 2` is polynomially
  bounded and outside it (`parity_not_gen_linear` -- the reviewer's
  example, proved).  The repaired statement is DOMINATION:
  `PolyBounded` is exactly the downward closure of `Gen Linear` under
  pointwise `<=` (`polyBounded_iff_dominated`).
* **BC2 PROVED**: `two_pow_escapes` exhibits, for every `k` and `c`, a
  size where the doubling budget beats `c (n+1)^k` (the witness is
  `n = k (k+c+4) + c + 1`, through `s*s <= 2^s` for `s >= 4`);
  `two_pow_not_polyBounded` and `generators_decide_the_class` package
  it: one adjoined generator changes the class.  "Polynomial" holds
  RELATIVE to the declarations in force -- the linear generators AND
  the two closure operations (a reviewer corrected the claim that the
  operations were forced; they are declared, as the generators are).
* **BC3 held as a finite observation, twice corrected on review.**  The
  instrumented decider stayed within the declared budget
  `steps <= 60 (V+E)` on all `54` instances (nine fixtures, three
  refinement rounds each, with and without a nontrivial
  re-presentation -- an earlier version of this bullet said `36` over
  four graphs; a reviewer corrected it against the receipt and the
  count is now pinned), every verdict matching the reference
  computation.  The summation meter on the square: `11, 91, 731, 5851`
  steps at length budgets `2, 4, 6, 8`, growth factors `8.27, 8.03,
  8.00` -- above `2` per added length as predicted -- but the breach of
  the linear budget comes at length `8`, not `6` as pre-registered:
  `731 <= 840` fits.  The miss is pinned by
  `test_sum_meter_breaches_the_linear_budget_at_length_8_not_6`.  And
  the claim is NARROWED: the meter varies walk length while the
  declared size measure stays `V + E = 14`, so exceeding one linear
  bound at four sampled lengths is a finite observation -- `5851 > 840`
  at length `8` -- and establishes neither nonlinearity nor
  non-polynomial growth.  A reviewer observed this; the asymptotic
  reading is withdrawn.

What the run answers, internally.  Deciding whether a keyed convention
exists is a computation that stayed within a declared linear budget on
every instance run -- and the polynomial class it lives in is, by
proof, the domination closure of the declared linear generators.
Evaluating keyless sums exceeded that same declared budget at the
sampled lengths -- a finite observation; whether the meter's cost lies
outside the closure ASYMPTOTICALLY is not established by this receipt
and is not claimed.  The received robustness of "polynomial" is the
sum of one theorem (the domination closure) and declarations (the
linear generators and the two closure operations).  An earlier version
of this paragraph said the operations were forced and that no budget
in the closure covers the walk count; a reviewer corrected both, and
the corrections are recorded in the repair record below.

### Review repairs (PR #99, round 1)

Four findings, all accepted, repaired at this commit:

1. **"Forced" operations.**  `Gen`'s constructors carry no bridge
   theorem to walks, refinement, or re-presentation, and no
   exhaustiveness theorem.  Reclassified as declarations -- in the Lean
   header, this file, and the ledger (NS-54, NS-55).
2. **BC1 overclaim.**  `Gen Linear` is not the polynomial class: its
   members are monotone, and the reviewer's example `n % 2` separates.
   Repaired to the domination iff (`polyBounded_iff_dominated`), with
   the countermodel proved (`parity_not_gen_linear`, NS-57).
3. **BC3 overclaim.**  The meter varies walk length while the declared
   size measure stays `V + E = 14`; four sampled lengths prove no
   asymptotic statement.  Downgraded to the finite observation
   `5851 > 840` at length `8` (NS-56).
4. **Instance total.**  Nine fixtures x three rounds x two
   presentations = `54` instances, as the receipt records; this file,
   the ledger, and the PR body said `36` over four graphs.  Corrected
   everywhere and pinned
   (`test_decider_within_declared_budget_everywhere_with_matching_verdicts`).

## Faces: the first two-dimensional rung -- predictions, written before the computation ran

The tower so far is one-dimensional: objects and hops, walks, flux.
This rung adds FACES.  The fixture is the chord square: four objects,
the four square hops, and one chord `0-3`, giving five edges and two
triangular faces (`T1 = 0-1-3`, `T2 = 0-3-2`) whose boundaries share
the chord and compose to the outer square walk.  Phases live in an
arbitrary `AbGroup`, as on the phase rung: no finiteness, no
decidability of the fibre.  A face is ADMITTED by imposing that the
flux around its boundary is zero -- admission is a constraint event,
exactly as everywhere else in this tree.  Predictions:

| claim | prediction |
|---|---|
| **TC1** (boundary identity) | PROVED in Lean: the outer walk's flux is the sum of the two face fluxes, `fluxOuter = fluxT1 + fluxT2`, by group laws alone (no commutativity, no finiteness). |
| **TC2** (sections = all faces flat) | PROVED in Lean: over the chord-square family a natural section exists iff `fluxT1 = 0` and `fluxT2 = 0`.  Forward by walking each triangle and cancelling; backward by an explicit potential on the four objects. |
| **TC3** (the outer boundary is blind) | PROVED in Lean: for every nonzero `Phi` there is a phase assignment with `fluxOuter = 0` and no natural section (`fluxT1 = Phi`, `fluxT2 = -Phi`).  Filling one face transfers the whole obstruction to the other (`fluxT1 = 0` makes the section criterion exactly `fluxT2 = 0`). |
| **TC4** (the finite instances) | Computed over `Z_N`, `N in {2, 3, 4}`: brute-force potential existence agrees with `(fluxT1, fluxT2) = (0, 0)` on all `N^5` assignments; section count `N^3` (8, 27, 64); outer-flux-zero count `N^4` (16, 81, 256); outer-zero-but-obstructed count `N^4 - N^3` (8, 54, 192); among the `N^4` assignments with face `T1` filled, exactly `N^3` admit sections. |

Reading, agreed in advance.  If TC3 fails, the outer boundary
determines the class and faces add nothing at this size -- record it.
If the TC4 counts miss, the pre-registration was wrong and the miss is
recorded next to the computed value, as on the budget rung.  What TC1
+ TC2 + TC3 would say together: admitting a face is the event that
forces its boundary flux to zero; when every independent loop is
filled the section exists; and the sum over the outer boundary alone
cannot see an interior obstruction that the faces see.  The
obstruction lives on faces, not on the bulk total.

### Results, written after the run (`two_complex.py`, receipt
`receipts/two_complex.json`; Lean `lean/NaturalSections/TwoComplex.lean`)

* **TC1 PROVED**: `outer_flux_eq_add` -- the outer walk's flux is the
  sum of the two face fluxes, the shared chord cancelling, by the five
  group laws alone (no commutativity, no finiteness, no decidability
  of the fibre).
* **TC2 PROVED**: `section_iff_faces_zero` -- a natural section of the
  chord-square family exists iff BOTH face fluxes vanish.  Forward:
  walk each triangle, fix the pair, cancel in the group
  (`fluxT1_zero_of_fixed`, `fluxT2_zero_of_fixed`).  Backward: the
  explicit potential `theta` (zero at `0`, following the tree `0-1-3`
  and the edge `2-0`), one `pair_step` per oriented hop, ten cases.
* **TC3 PROVED**: `outer_zero_but_obstructed` -- for every nonzero
  `Phi`, the assignment `Phi` on `1-3`, `-Phi` on `3-2`, zero
  elsewhere has outer flux zero and no natural section.  And
  `fill_transfers`: with `T1`'s flux zero, the section criterion is
  exactly `T2`'s flux -- admitting a face moves the whole residual
  obstruction onto the faces that remain.
* **TC4 CONFIRMED, every count as pre-registered**: over `Z_N` for
  `N in {2, 3, 4}`, brute-force potential existence agrees with
  `(fluxT1, fluxT2) = (0, 0)` on all `N^5` assignments; the boundary
  identity holds everywhere; sections `8, 27, 64` (`N^3`); outer-zero
  `16, 81, 256` (`N^4`); outer-zero-but-obstructed `8, 54, 192`
  (`N^4 - N^3`); with `T1` filled, `N^4` assignments remain of which
  exactly `N^3` admit sections.  No misses this rung.

What the rung answers, internally.  A face is a constraint event: its
admission forces the flux around its boundary to zero, and TC2 says
that when every face is admitted the keyed convention exists -- the
first two-dimensional instance of remove-the-obstruction /
build-the-structure pricing.  TC3 is the sharp point: the OUTER
boundary total can vanish while the class is still obstructed, so the
obstruction is not a bulk number; it lives on the faces, and only
admitting the chord's faces makes it visible or removable.  Counts
remain blind exactly as on the one-dimensional rungs: the outer-zero
class splits `N^3` sectioned against `N^4 - N^3` obstructed with the
same outer flux.

## Repair mass: pricing the chord-square obstruction -- predictions, written before the computation ran

The faces rung decided EXISTENCE: a natural section exists iff both
face fluxes vanish.  This rung prices NON-existence.  Declare the
gauge coboundary `d0 theta` on the chord square (per oriented edge,
the potential difference), the residual `w - d0 theta`, and a mass on
edge assignments: the SUPPORT mass counts the edges carrying a nonzero
phase (`DecidableEq` on the fibre is declared for the mass; nothing
else changes).  The repair mass of `w` is the least mass over all
gauge repairs -- the least number of edges any gauge-equivalent
assignment must still carry.

A declared import, stated in advance: the existence layer used only
the five group laws; the PRICING layer additionally declares
commutativity (flux additivity under pointwise sums needs it).
Existence is commutativity-free; pricing buys commutativity.  That
asymmetry is recorded as a finding, not hidden.

| claim | prediction |
|---|---|
| **QM1** (zero repair mass = existence) | PROVED in Lean, commutativity-free: some gauge repair has mass zero iff both face fluxes vanish iff a natural section exists (composing with the faces rung).  The quantitative reading of "repair iff the obstruction class is zero". |
| **QM2** (the quotient is the flux pair) | PROVED in Lean, with declared commutativity: `w'` is gauge-equivalent to `w` iff the two face fluxes agree -- the gauge classes are exactly the pairs `(fluxT1, fluxT2)`, so the quotient of assignments by repairs is the group of flux pairs. |
| **QM3** (exact price, support mass) | PROVED in Lean, any commutative fibre: the least repair mass is `0` iff `(f1, f2) = (0, 0)`; it is `<= 1` iff `f1 = 0` or `f2 = 0` or `f2 = -f1` (the chord is the ONLY single edge lying in both faces, and it prices exactly the anti-diagonal); it is always `<= 2`.  So the price is 0 at the origin, 1 on the three axes away from the origin, and 2 elsewhere; the chord's anti-diagonal is a third axis the outer boundary cannot see.  (An earlier sentence here said "2 minus the number of declared axes the class lies on" -- false at the origin, where all three axis conditions hold and the formula gives -1 while QM1 proves 0; a reviewer corrected it.) |
| **QM4** (the finite surveys) | Computed over `Z_N`, `N in {2, 3, 4}`, for the support mass AND a second declared circular gauge `cd(k) = min(k, N-k)`: every gauge class has exactly `N^3` members; the support-mass trichotomy matches QM3 on all `N^2` classes, with class counts at price `0 / 1 / 2` equal to `1 / 3(N-1) / (N-1)(N-2)` (N=2: 1,3,0; N=3: 1,6,2; N=4: 1,9,6); circular-gauge price is `0` iff `(0,0)`, satisfies `phi_circ <= cd(f1) + cd(f2)`, and on the anti-diagonal `(f, -f)` equals `cd(f)` exactly (the chord alone carries it). |

Reading, agreed in advance.  If QM2 fails, the flux pair is not a
complete gauge invariant and the faces rung's quotient reading is
wrong -- record it.  If the QM4 counts miss, the pre-registration was
wrong and the miss is recorded next to the computed value.  What
QM1-QM3 would say together: the obstruction class does not merely
exist or not -- it has a PRICE in edges, the price is decided by which
of three declared axes the class lies on, and one of those axes exists
only because of the chord.  Admitting a face changed what is
repairable; the mass says by how much.

### Results, written after the run (`quotient_mass.py`, receipt
`receipts/quotient_mass.json`; Lean `lean/NaturalSections/QuotientMass.lean`)

* **QM1 PROVED, commutativity-free**:
  `repair_mass_zero_iff_faces_zero` and `repair_mass_zero_iff_section`
  -- some gauge repair has support mass zero iff both face fluxes
  vanish iff a natural section exists.  The exactness half is the
  explicit potential (`exact_of_fluxes_zero`); the coboundary
  telescopes (`fluxT1_d0`, `fluxT2_d0`) close the other half.
* **QM2 PROVED, with the declared commutativity**: `residual_flux1/2`
  (every repair preserves the flux pair) and `reaches_of_sameClass`
  (everything with the same flux pair is reached), so the gauge
  classes are EXACTLY the flux pairs.  As predicted, this layer is
  where commutativity enters -- flux additivity under pointwise sums
  -- and nowhere earlier.
* **QM3 PROVED**: `repair_mass_le_one_iff` -- price at most one iff
  `f1 = 0` or `f2 = 0` or `f2 = -f1`, the chord's anti-diagonal, an
  axis only because the chord lies in both faces --
  and `repair_mass_le_two` -- price at most two, always.  With QM1's
  zero case the least repair mass is decided for every class.
* **QM4 CONFIRMED, every count as pre-registered**: `N^2` classes of
  exactly `N^3` members with `im(d0)` the zero class; support-mass
  trichotomy matching QM3 on every class, counts `1 / 3(N-1) /
  (N-1)(N-2)` at price `0 / 1 / 2` (N=2: 1,3,0; N=3: 1,6,2; N=4:
  1,9,6); circular price zero only at the origin, bounded by
  `cd(f1) + cd(f2)`, exactly `cd(f)` on the anti-diagonal.  No misses
  this rung.

What the rung answers, internally.  The obstruction class is not a
yes/no: it has a price, counted in edges no repair can empty, and the
price is decided by which of three axes the class lies on.  Two of
those axes are the faces themselves; the third exists only because
the chord lies in both faces at once -- the interior edge is the only
single place a mixed obstruction can live.  And the layering is now a
theorem about the theory itself: deciding whether a section exists
needed five group laws; pricing the failure needed one more
declaration (commutativity).  Existence is cheaper than pricing, and
the tree now says so with receipts.

## Aggregation: which mass functions are forced -- predictions, written before the computation ran

The repair-mass rung DECLARED the support mass and priced with it.
This rung asks what forces that shape.  Declare, per edge, a local
gauge (a value in `Nat` computed from the edge's phase); a DIAGNOSTIC
takes a finite list of edges and an assignment and returns one `Nat`.
Two axioms are on the table: ADDITIVITY -- the diagnostic of a
concatenation of edge lists is the sum of their diagnostics -- and SINGLETON
CALIBRATION -- on a one-edge list the diagnostic IS the declared local
gauge.  Predictions:

| claim | prediction |
|---|---|
| **AG1** (the unweighted selection) | PROVED in Lean, any edge index, any dependent carriers: additivity plus singleton calibration force the diagnostic to be the edge sum of the declared gauges, by finite list induction; the empty list is forced to zero by additivity alone. |
| **AG2** (the weighted selection) | PROVED in Lean: additivity plus magnitude-sufficiency (the singleton value is a function of the declared gauge alone) plus homogeneity of that function force the weighted sum with weights the singleton values at gauge `1`. |
| **AG3** (both axioms are load-bearing) | PROVED by countermodel, concrete two-edge fixture: the MAX aggregator satisfies calibration and violates additivity (`max 1 1 = 1` against `1 + 1 = 2`); the DOUBLED sum satisfies additivity and violates calibration (`2` against `1`); each disagrees with the edge sum on a named instance. |
| **AG4** (the tie-in, and the finite survey) | PROVED in Lean: the chord square's support mass is exactly the edge sum of the per-edge indicator gauge over the five-edge list, so ANY additive calibrated diagnostic on those gauges equals it.  Computed over `Z_3`, all `243` assignments and all disjoint subset pairs: the edge sum has `0` additivity violations and `0` calibration failures; the max aggregator's additivity violations are positive, with a named witness; the doubled sum fails calibration on exactly `810` singleton instances (five edges times the `162` assignments with a nonzero gauge at that edge). |

Reading, agreed in advance.  If AG1 fails, the support mass was a
choice among many shapes even after the two axioms, and the pricing
rung's mass needs a third declared axiom -- record which.  If the
`810` misses, the pre-registration was wrong and the miss is recorded.
What AG1-AG4 would say together: the PRICING SHAPE is not another
free declaration stacked on the gauge -- once the per-edge gauges are
declared and the observer is additive and calibrated, the edge sum is
forced, and the only remaining freedom is the per-edge gauge itself
(and, replacing calibration with magnitude-sufficiency and
homogeneity, one weight per edge -- an earlier parenthetical said
"without calibration" alone, which additivity does not deliver:
singleton values may depend nonlinearly on the gauge; a reviewer
corrected it).  The declarations
thin as the tower climbs: fibre, then faces, then gauges -- the
aggregator is not among them.

### Results, written after the run (`aggregation.py`, receipt
`receipts/aggregation.json`; Lean `lean/NaturalSections/Aggregation.lean`)

* **AG1 PROVED**: `forced_sum` -- additivity over concatenation plus
  singleton calibration force the edge sum, over any edge index and
  dependent carriers, by list induction; `nil_zero` -- the empty list
  is forced to zero by additivity alone (concatenate the empty list
  with itself; no edge inhabitant is needed, and the axiom was stated
  in concatenation form for exactly that reason).
* **AG2 PROVED**: `forced_weighted_sum` -- additivity plus
  magnitude-sufficiency plus homogeneity force the weighted sum with
  weights the singleton values at gauge `1`.
* **AG3 PROVED**: `max_calibrated` + `max_not_additive` (and the
  disagreement with the sum), `scaled_additive` +
  `scaled_not_calibrated` -- each axiom fails alone on the two-edge
  unit-gauge fixture, so neither is redundant.
* **AG4 PROVED AND CONFIRMED, every count as pre-registered**:
  `suppMass_is_edge_sum` and `aggregation_determines_suppMass` in
  Lean; over `Z_3`, `243` assignments x `243` disjoint subset pairs:
  edge sum `0` violations and `0` calibration failures; max aggregator
  `28560` additivity violations with the witness recorded; doubled sum
  exactly `810` calibration failures.  No misses this rung.

What the rung answers, internally.  The support mass was introduced on
the pricing rung as a declaration.  This rung narrows what was
actually declared: the per-edge gauges.  Once those are fixed, an
additive calibrated observer has NO remaining freedom -- the edge sum
is forced -- and replacing calibration with magnitude-sufficiency and
homogeneity leaves exactly one weight per edge (an earlier sentence
said "dropping calibration" alone did this; additivity by itself does
not -- singleton values may depend nonlinearly on the gauge, or on the
whole assignment -- and `forced_weighted_sum` obtains weights only
from the two added axioms; a reviewer corrected it).  The declarations
thin as the tower climbs, and which axiom carries which freedom is now
itself proved: additivity kills the aggregator's shape; within
magnitude-sufficient homogeneous observers, calibration kills the
weights.

## Equivariant bridge to the sealed selector theorem -- predictions, written before the computation ran

The sealed `ContactKernel.no_equivariant_pair_valued_map` rules out a
total map `sel : DiffObs Bool Bool → Bool × Bool` commuting with the
negation relabelling `swapObs`.  The sealed
`PresentationNaturality` module states in two places (its section 10
and its section 14 non-claims) that deriving that theorem from the
general obstruction `no_natural_section_of_fixed_point_free` is OPEN:
the two quantify over different objects -- raw-pair-valued maps out of
the observer type, versus sections of the admissible-pair bundle.  This
rung builds the bridge, in `lean/NaturalSections/EquivariantBridge.lean`.
The seal is not amended: the sealed OPEN record stays where it is; what
is added is a research derivation alongside it.

The gap, stated exactly.  A section assigns an ADMISSIBLE pair
(`NonZeroPair boolEqObs`); the sealed selector assigns a RAW pair,
which may be diagonal, and no observer admits a diagonal pair
(`zero_refl` is a field).  So the bridge needs a map from raw pairs to
admissible pairs that commutes with the negation action -- possible
precisely because the negation action on raw pairs is free, so each of
its two orbits `{(F,F),(T,T)}` and `{(F,T),(T,F)}` can be mapped
orbitwise onto the admissible orbit.  Declared construction:
`pairRetract` sends `(F,F) ↦ (F,T)`, `(T,T) ↦ (T,F)`, and is the
identity on the two admissible pairs.

Declared derivation route, written before the file: from an equivariant
`sel`, the section `fun _ => pairRetract (sel boolEqObs)` over
`autoFamily boolEqObs negIso` is natural -- using ONLY the equivariance
law at `boolEqObs`, the sealed fixed-point equation `swapObs_boolEqObs`,
and the equivariance of `pairRetract`; never the fact that negation
fixes no Boolean.  The contradiction is then produced by the sealed
`no_natural_section_of_fixed_point_free` applied with the sealed
`negIso_fixed_point_free`.  What the bridge does NOT claim: independence
from `negIso_fixed_point_free` -- that sealed input is the Bool-instance
fixed-point-freeness the general theorem consumes, and it is cited, not
re-proved.  The claim is about the ROUTE: the sealed selector statement
becomes an instance of the section obstruction, which is exactly the
derivation the sealed module records as missing.

Predictions:

| item | prediction |
|---|---|
| **EB1** (the retraction) | PROVED: `pairRetract` lands in `NonZeroPair boolEqObs`, is the identity on admissible pairs (`pairRetract_fixes_admissible`), commutes with the negation action (`pairRetract_equivariant`, for every raw pair), and its four values are as declared above (`pairRetract_table`, by `decide` -- the finite instance check of this rung; no Python is needed because there is no computational claim beyond these four values). |
| **EB2** (the bridge) | PROVED: `sectionOf_natural` -- an equivariant `sel` yields a natural section of `autoFamily boolEqObs negIso` -- and `no_equivariant_pair_valued_map_via_sections`: no equivariant `sel` exists, with the `False` produced by the sealed `no_natural_section_of_fixed_point_free` + `negIso_fixed_point_free`, not by a direct fixed-point argument. |
| **EB3** (the translation is the identity) | The research notion `Equivariant sel` is DEFINITIONALLY the sealed equivariance law (`equivariant_iff_sealed_shape` by `Iff.rfl`), and the derived proposition IS the sealed proposition: `bridge_statement_is_the_sealed_statement`, an equality of the two proofs whose elaboration forces the two STATEMENTS to be definitionally equal, closed by `rfl` (definitional proof irrelevance).  If this `rfl` fails to elaborate, the fallback declared now is: state the translation as a definition and prove the transported statement, recording the mismatch -- the OPEN discipline. |
| **EB4** (inventory and axioms) | 8 new reports (the seven named above plus `sealed_selector_content_along_bridge`), tree total `218`; all within `{propext, Quot.sound}`.  Sharper, and recorded so a miss is visible: `pairRetract_table`, `pairRetract_fixes_admissible`, `pairRetract_equivariant`, `equivariant_iff_sealed_shape`, `bridge_statement_is_the_sealed_statement` with NO axioms; `sectionOf_natural`, `no_equivariant_pair_valued_map_via_sections`, `sealed_selector_content_along_bridge` on `['Quot.sound']` exactly (the sealed `swapObs_boolEqObs` realizes `funext` through `Quot.sound`; nothing here should need `propext`). |

Reading, agreed in advance.  If `sectionOf_natural` cannot be proved
without invoking "negation fixes no Boolean", the bridge is circular
and the rung is recorded OPEN with that blocker.  If the `rfl` of EB3
fails, the types do not align and the transported-statement fallback is
used, recorded as a miss against EB3.  If any report needs `propext`,
EB4's sharper half missed and the computed set is recorded next to it.

### Results, written after the run (Lean
`lean/NaturalSections/EquivariantBridge.lean`)

The module elaborated clean on the first pass; every mathematical
prediction held, and EB4's sharper half missed on one report.

* **EB1 PROVED**: `pairRetract` is total into `NonZeroPair boolEqObs`
  (admissibility by the sealed `boolEqObs_nonzero_ft` / `_tf`, cited
  not re-proved), `pairRetract_fixes_admissible` (the diagonal cases
  refuted by the pairs' own admissibility, the off-diagonal by
  `Subtype.ext rfl`), `pairRetract_equivariant` (four cases, each
  `Subtype.ext rfl`; the no-fixed-Boolean fact nowhere used), and
  `pairRetract_table` by `decide` -- the rung's finite instance check.
  No Python, as declared: there is no computational claim beyond the
  four table values.
* **EB2 PROVED**: `sectionOf_natural` consumes exactly the three
  declared inputs -- the equivariance law at `boolEqObs`, the sealed
  `swapObs_boolEqObs`, and `pairRetract_equivariant`; the equivariance
  equation at the fixed point is only ever REWRITTEN with, never
  refuted.  `no_equivariant_pair_valued_map_via_sections` then gets its
  `False` from the sealed `no_natural_section_of_fixed_point_free`
  applied with the sealed `negIso_fixed_point_free`.  The circularity
  the reading clause feared did not arise.
* **EB3 held, no fallback needed**: `equivariant_iff_sealed_shape` is
  `Iff.rfl`, and `bridge_statement_is_the_sealed_statement` -- the
  equation between `sealed_selector_content_along_bridge` and the
  sealed `ContactKernel.no_equivariant_pair_valued_map` -- elaborates
  and closes by `rfl`.  The types align exactly; the translation is
  the identity and no translation definition was needed.
* **EB4: count held, axiom split missed by one.**  8 new reports, tree
  total `218`, all within the whitelist.  The split came out 4 + 4,
  not the predicted 5 + 3: `bridge_statement_is_the_sealed_statement`
  reports `['Quot.sound']`, not "no axioms" -- its statement NAMES the
  two proof constants, so their dependencies (through the sealed
  `swapObs_boolEqObs`'s `funext`) are in its report even though its own
  proof is `rfl`.  The miss is recorded here next to the prediction,
  which stands unedited above.  The other seven came out exactly as
  predicted: `pairRetract_table`, `pairRetract_fixes_admissible`,
  `pairRetract_equivariant`, `equivariant_iff_sealed_shape` with no
  axioms; `sectionOf_natural`,
  `no_equivariant_pair_valued_map_via_sections`,
  `sealed_selector_content_along_bridge` on `['Quot.sound']`; nothing
  needed `propext`.

What the rung answers, internally.  The sealed module kept its selector
theorem and its section obstruction side by side and recorded the
derivation of one from the other as OPEN, because they quantify over
different objects.  The missing object was one equivariant map: a
retraction from raw pairs to admissible pairs commuting with the
action, which exists because the action on raw pairs is free.  With it,
every equivariant selector is a natural section in disguise, and the
selector theorem is an instance of the section obstruction -- statement
identity machine-checked, seal untouched.

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
* An earlier version of this bullet read: "Nothing here derives
  `ContactKernel.no_equivariant_pair_valued_map` or touches the OPEN
  items the sealed module records."  NARROWED as of the
  equivariant-bridge rung: `EquivariantBridge.lean` derives that sealed
  statement's content from the sealed section obstruction (NS-82).  The
  sealed module's own OPEN record is untouched -- the seal is not
  amended, and this tree claims no authority over it -- and the other
  sealed OPEN item, the general embedding of the flat `Family` into
  `HFamily`, remains open here too.
* The countermodels separate the fixed-point reading from the
  fixed-pair reading; they say nothing about which automorphisms arise
  from any presentation theory.

## Commands (run from the repository root)

| command | exit | key line |
|---|---|---|
| `python research/natural_sections/verify_pins.py` | 0 | `import closure of ['Derivation.PresentationNaturality']: 12 module(s), all pinned`; `sealed prefixes clean` |
| `python research/natural_sections/verify_lean.py` | 0 | `Lean #print axioms declarations: 218 within ['Quot.sound', 'propext']` (the eight PR #99 repair theorems, the 24 faces theorems, the 35 repair-mass theorems, the 10 aggregation theorems, and the 8 equivariant-bridge theorems included; of the bridge's 8, four report `no axioms` and four `['Quot.sound']`); 119 `no axioms` (an earlier revision of this row said 115, the pre-bridge total, while in the same breath crediting the bridge's four new no-axiom reports; a reviewer caught the contradiction and a fresh `verify_lean.py` run counts 119) (the budget theorems use `omega` and `funext`, so they carry the whitelist pair) (the re-presentation, cut and counts theorems among them); 7 in `Hop3`, 6 in `Hop4`, 12 in `HopPhase` and 5 in the weighted layer on `['propext']`, and the three counting theorems (`omega`) on `['Quot.sound', 'propext']`; `write root respected` |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python run_representation.py --out receipts` | 0 | `square re-presentation: {... 're_presentations': 64, 'with_section': 0 ...}`; `square deletion: {... 'minimum_deletion': 2 ... 'single_deletion_suffices': False}`; `chain re-presentation: {... 64, 'with_section': 64 ...}`; `star deletion: {'minimum_deletion': 1 ...}` |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python run_weighted_sum.py --out receipts` | 0 | `square_2x2_k2: 147 closed walks up to length 6; total_unit 147, total_sign 43`, `pair (0, 1): twisted_unit 95 ... movers 52`; `orbit counterexample: ... 'twisted_at_fixed': 1, 'twisted_at_moved': 0`; `every value: {'square_2x2': [-3, -1, 0, 2, 7], 'chain_P4': [-3, -1, 0, 2, 7]}` |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python run_holonomy_phase.py --out receipts` | 0 | `one on each, flux 1: order 4, permutation part trivial, fixed pair False`; `gauge invariance: True`; `periodicity: {... True}`; `refinement compatibility: {... True}` |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python run_holonomy_fixture.py --out receipts` | 0 | five chains `section exists`; square, ladder, star, triangle `NO natural section` |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python run_holonomy_group.py --out receipts` | 0 | `k=3 square_2x2: NO natural section; parity says clean; ... group order(s) 3`; `k=3 star_K13: section exists` |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python run_holonomy_group.py --out receipts` (k = 4) | 0 | `runs.k4` in the receipt: `square_plus_edge` components of orders 1, 3, 2 with common fixed points all, `[3]`, `[2, 3]` |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s . -p "test_*.py"` | 0 | `Ran 123 tests`, `OK` (the clean rebuild included) |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python run_aggregation.py --out receipts` | 0 | `pairs 243, additivity violations {'edge_sum': 0, 'max_agg': 28560, 'doubled': 0}, calibration failures {'edge_sum': 0, 'max_agg': 0, 'doubled': 810}` |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python run_quotient_mass.py --out receipts` | 0 | `N=3: classes 9, orbits N^3 True, supp price matches QM3 True, counts {0: 1, 1: 6, 2: 2}, circ antidiagonal exact True` |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python run_two_complex.py --out receipts` | 0 | `N=3: total 243, sections 27, outer-zero 81, outer-zero-obstructed 54, boundary identity True, potential==flux True` |
| `cd research/natural_sections && python -m mypy` | 0 | strict, 36 source files (an earlier row said 27 after the faces and repair-mass modules had raised it to 30 and then 33; a reviewer corrected the stale receipt, and the aggregation modules raise it to 36) |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python run_budget_meter.py --out receipts` | 0 | `decider all within budget: True`; `decider all verdicts match: True`; `sum meter len 8: 1171 walks, 5851 steps, within linear budget: False`; `growth factors: [8.27, 8.03, 8.0]` |
| `cd research/natural_sections && PYTHONDONTWRITEBYTECODE=1 python run_refinement.py --out receipts` | 0 | square rounds `6/8 -> 14/16 -> 30/32` objects/hops, odd `2, 2, 2`, `section False` throughout; chain `section True` throughout; `verdicts invariant: {... True}` |
