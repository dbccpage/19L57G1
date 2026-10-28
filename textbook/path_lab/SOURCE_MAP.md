# Source map and evidence scope

AuthorityEffect: None. These are supplied teaching representations outside
the sealed derivation. Native sources are consumed read-only.

## Owners and meanings

| Lesson | Declared teaching meaning | Native connection and boundary |
|---|---|---|
| 00–01 | A simple undirected graph; walks use consecutive admitted edges and may traverse them backwards | Edges are dimension-one cells in `LadderGeneral.ComplexN`. Teaching walks are separately supplied sequences, not `PEvent` or `NEvent` histories. No graph-path theorem is silently imported from `Attachment.Reaches`. |
| 02 | Departures −1, arrivals +1, added at equal vertices | `LadderGeneral.bdN`, `pushN`, `coeffN` evaluate the signed edge chain. The walk's canonical edge coefficient is +1 for increasing traversal and −1 for decreasing traversal. |
| 03 | Three complete facets permit a face-admission step; no request means no admission | `shellN`, `stepN`, `nstep`, `nreplay`, `uniform_guarded_filler`, `shell_refuses_general`, `shell_no_self_fill`, `wf_nreplay` |
| 04–05 | Alternating deletion boundary; linear combination of faces with coefficients +1 or −1 | `sgn`, `bdN`, `pushN`, `coeffN`; native `BoundaryCancellation.d2_zero_unrestricted` proves coefficientwise cancellation for every finite vertex list and every target list |
| 06 | Formula cancellation does not imply a valid cell guard; all-positive deletion is a different formula | `BoundaryCancellation.illformed_countermodel`, `signless_countermodel`; strict ascent controls face distinctness, not the unrestricted cancellation identity |

The formal owners are `lean4/Derivation/LadderGeneral.lean` and
`BoundaryCancellation.lean`. Executable owners are
`code/derivation/attachment_ladder.py` (cell store/guard/step) and
`boundary_cancellation.py` (the boundary formula and signless control).
Existing longer treatments are Units 60 and 65. The cell calculus has no
passage observer, protection, budget, license, or activation field.

## Supplied finite case

The carrier is positions 0, 1, 2, 3, displayed as A, B, C, D. Drawing
coordinates serve only display. All four vertices are admitted first.
The five selectable edges, in mask order, are AB, BC, AC, CD, AD.
Each selected edge is admitted through the actual guarded source step.
The two candidate faces are ABC and ACD, requested in that order.

We compare every subset of the five edges and every subset of the two
face requests. No face is present before the requests. Both candidate
face lists have exact arity and strict ascent; a missing facet blocks
the request. A successful repeated request is then checked inert.
The second admitted face's chain coefficient can be +1 or −1; this
coefficient is independent of its cell membership.

| Population | Size |
|---|---:|
| Edge subsets on the five declared edges | 32 |
| Face-request subsets | 4 |
| Second-face coefficient choices | 2 |
| Recorded face/boundary settings | 256 |
| Recorded edge-subset/walk settings | 192 |
| Raw vertex words of length zero through four | 341 |

The six proposed walks are A→B→C, A→B→C→A, A→B→C→D→A, A→B→A,
A→B→D, and A. Each consecutive pair must be a present undirected edge.
A zero-step walk is valid and closed under this declared convention.
An invalid sequence supplies no valid-walk endpoint tally in the desk.
We do not enumerate all graphs, all walks, all complexes, or all dimensions.

The raw-word check includes repeats and the empty word. Its source
double-boundary coefficients vanish. This is a bounded check of the
unrestricted native theorem, not an admission claim about those raw lists.
The all-positive triangle control uses both `bd_no_sign` and `push_no_sign`;
its vertex coefficients are +2, +2, +2. It is different from changing only
one edge sign while keeping the signed endpoint-boundary rule.

## Independent checks and proofs

The packet pins normalized UTF-8/LF source-text hashes and verifies loaded
module origins. It compares the actual face guards with explicit facet
membership and the absence of the candidate face. Independent expansion
of a triangle as AB + BC − AC checks its first boundary. Independent
arrival/departure counts check every valid walk's endpoint boundary and
the start/end formula. The two Python boundary owners agree on all 341
raw words. The transfer exercise's shared-edge signs are checked directly.

Book-Lean checks use the actual `LadderGeneral` and `BoundaryCancellation`
definitions: 128 admission-history cases and 32 grouped walk cases covering
all 192 proposed walks. The admission cases also check both coefficients'
exact uncombined first and second boundary lists. There are 160 book
declarations, each with exactly `{propext, Quot.sound}`, plus four native
theorem reports. Three native reports have those same axioms; the native
signless countermodel has none. All 164 reports are pinned by the runner.
The 160 cases are **derived (book Lean)**, outside the sealed census.
The native unrestricted theorem supplies the general
per-cell cancellation claim; finite correspondence checks do not establish
a general Python-to-Lean refinement or a bridge to physical space.

The primitive input encoding uses natural-number vertex labels, finite
lists, and integer coefficients. The learner can select recorded inputs,
not arbitrary raw Python integers. A repeated list can satisfy the algebraic
identity while failing the increasing-order admission guard.

Novice understanding, unfamiliar-example transfer, delayed retention,
reading time, and real-world measurement correspondences remain unmeasured.
