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

## Native path costs: Lessons 07–12

This selected introduction consumes `research/native_structure`'s current
README, ledger, Python functions, and Cells, Boundary and Closed Lean
bodies read-only. Its meaning of `Cell` is a verified-swap relation on
native event histories, not a vertex-list face in `LadderGeneral`.

| Lesson | Meaning used | Owner and scope |
|---|---|---|
| 07–08 | State/event cost, path sum, potential, telescoping | NS-7/8; `pathCost_append`, `exact_pathCost`, `budgetDelta_exact` |
| 09 | Nonzero full-state return loop excludes every potential | NS-7/8; `not_exact_of_cycle`, `writes_not_exact` |
| 10 | Two orders agree at the actual starting state; compare their costs | NS-6/7; `boundary_boundary`, `boundary_zero_iff_commutes`, `exact_closed` |
| 11 | State-change count is closed but not exact | NS-8/10; `writes_closed`, `writes_closed_not_exact` |
| 12 | Verified adjacent swaps preserve a closed cost, but do not identify all equal-end paths | NS-1/4/7; `swap_sound`, `parallel_not_cell`, `closed_swap_cost`, `closed_cell_cost` |

The passage slice varies budget 0/1/2, both license values, and live/halted
status, giving twelve full states. Every other field is initial. Six
events write those three budgets, either license value, or halt. Snapshot
projection checks that no omitted field changes in this slice; full-state
equality is computed with the actual owner, not inferred from one budget.

The packet records seven histories from each start, giving 84 history
records and 168 cost-question selections. It checks all ordered event
pairs from each start: 432 comparisons, of which 348 commute and 84 do
not. An independent history population covers every event list of length
zero through three from all twelve starts, giving 3,108 native histories.
The original 256 face/boundary cases, 192 walk cases and 341 raw words
remain unchanged.

Every cost row calls the owner's `path_cost`, `budget_delta`, `writes`
and actual passage step. Independent before/after arithmetic checks the
signed change and 0/1 change count. Both routes are replayed before the
commuting-square premise is decided. Noncommuting pairs remain visible;
a zero reading for one cost is not treated as full-state commutation.
The budget loop returns the entire genesis state, with signed cost 0
and change count 2. Repeated budget writes count only their actual changes.

A separate supplied three-point graph assigns costs in −1/0/1 to AB,
BC and AC, and defines reverse edges by negation. Of 27 tables, seven
have a potential. Each successful witness is reconstructed and checked on
all six directed edges. Rejection uses the triangle loop's nonzero total.
The finite search fixes A at zero; AB and AC force B and C into −1/0/1,
so it excludes no possible integer potential on this declared graph.
This is separate from a global potential on every native passage state.
The practice graph with levels 2/5/1 is checked separately; its costs
3/−4/−1 lie outside that 27-table population.

The book re-elaborates the three exact research bodies after removing
only import lines, with a whitelist of reviewed imports. Fourteen selected
owner reports and six new book reports add twenty `{propext, Quot.sound}`
sets. Together with the earlier Path-lab checks, the driver has 184 reports:
183 with those two axioms and one empty. These are selected report scopes,
not an all-declaration research census or a reissue of frozen receipts.
The new book statements check the budget loop, inert repeat, start-sensitive
halt square, all-integer potential shifts, three-point reconstruction,
and impossibility of deleting a loop by swaps.

The 348 finite commuting comparisons illustrate the general closedness
theorem; they do not prove it. The source proof covers every native state
and event. No physical costs, measured conservation laws, proof-relevant
cell calculus, observer-descent treatment, native action, or generated
charge is added. NS-17's action question and the separate conservation
carrier remain outside this introduction. Reader learning remains unmeasured.
