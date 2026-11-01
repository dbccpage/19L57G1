# Combining systems: sources and scope

AuthorityEffect: None. Selected teaching from `p203_composite_systems`,
outside the sealed derivation. Begin with the [seven lessons](30_join_records_keep_names.md)
before these optional implementation and proof details.

## Definitions that must remain separate

| Topic | Python owner | Lean owner |
|---|---|---|
| Joining | Disjoint named integer dictionaries; overlap raises ValueError | Generic product associator with explicit inverse |
| Network | A finite supplied set of names with integer values | Four fixed unbounded Nat fields |
| Local update | Callback plus declared read/write sets; returned update keys checked | Function of A's pair placed into A's fields only |
| B readout | Callback plus unchecked footprint label | Function receiving only B's pair |
| Graph | Read/write and multi-write edges, undirected, shortest-path calculation | `hasMediatingBridge b = b`; no implemented graph or shortest-path theorem |
| Shares | Exact rational counts over a supplied equal-weight finite list | Pointwise readout preservation; no distribution or TVD formalization |
| Symmetry | Explicit graph-permutation check and separate value/readout helpers | Fixed subsystem swap and specified readout equations |

Owners are `research/p203_composite_systems/composite_systems.py` and
`research/p203_composite_systems/lean/CompositeSystems.lean`. Their README,
ledger, source manifest and receipt remain unchanged. Broad native wording
is not promoted beyond the inspected definitions. In particular the Lean
Nat fields are not a finite state space, and the Boolean bridge equations
do not certify graph derivation or arbitrary-cut reachability.

The named dictionary merge flattens bracket groupings; generic nested
products use different types connected by an explicit associator. The
examples support the respective definitions, without a general Python-to-Lean
refinement claim. Neither supplies statistical independence of preparations.

## Execution and metadata boundaries

The Python transition's returned dictionary is checked against its declared
write set. Actual reads are not inspected, and observable footprints are
unchecked metadata. A retained counterexample labels an A2-reading function
as B-local; its reading changes after an A2 increment despite passing the
footprint checks. Another callback copies A2 into B1 without declaring its
A2 read, so the graph misses that dependency.

`CarrierState` is a frozen dataclass containing an ordinary mutable dict.
A retained disposable-state callback directly mutates that dictionary and
returns an empty update, bypassing the returned-key guard. The desk uses
explicit nonmutating callbacks and known field dependencies. No generic
callback confinement theorem follows from the raw guard.

`BipartiteCut` checks disjoint parts, not coverage of an independently
given ambient universe. The book explicitly supplies exactly A1/A2/B1/B2
and their cut. Declared reads/writes for each selected operation are retained.

Python's graph joins each declared read to each distinct declared write and
each pair of distinct writes; read/read pairs alone add no edge. Registers
outside the supplied vertex list are ignored. No operation is run during
graph construction. A constant joint write creates an edge by this convention
without copying between the registers. Undirected distance counts neither
directional executable steps nor physical length, timing or speed.

## Pointwise preservation, lists and readouts

The native Lean local-change theorems preserve each B readout for arbitrary
Nat inputs and arbitrary permitted A functions/B probes. The book proves
preservation of the entire mapped B-pair list as well. Equal shares for
one selected list/readout are weaker: a binary flip of [0,1] changes both
paired readings but keeps both shares. A constant probe hides every change.
Neither a cut-crossing declaration nor the native negative-control helper
guarantees positive TVD for every list, intervention or observable.

The native leaky/mediated Lean inequalities are concrete witnesses, not
universal divergence statements. For the desk's two relay orders the baseline
also runs the relay, without the A2 intervention. Comparing against an untouched
baseline would mix the relay's own effect with the intervention's effect.

Repeated rows retain equal individual weight. Empty lists return empty
share tables and numerical distance zero, not observations or a supported
universal non-signaling claim. The native duplicate-observer helper likewise
returns symmetric agreement rate one with no symmetric rows, while its
`duplicate_agreement_satisfied` flag is false. The book retains both values.

The observer helper does not validate a graph automorphism or ensure its
map carries the first observed register to the second. An identity map can
classify a record as symmetric while A1/B1 differ. The book's valid swap
example supplies the whole bijection, checks graph preservation separately,
and keeps value symmetry and same-probe premises explicit. Graph symmetry
alone supplies no theorem about arbitrary operation or readout symmetry.

## Checked populations

| Population | Count | Actual scope |
|---|---:|---|
| Recorded list/procedure/readout contexts | 60 | Four named lists × five procedures × three probes |
| Recorded graph/query contexts | 12 | Four named rule lists × three endpoint pairs |
| Additional state/procedure/readout cases | 1134 | Fields 0..2; five procedures, three probes; binary flip restricted to B1 0/1 |
| Ordered-list share comparisons | 5115 | All 341 ordered lists of length 0..4 on four A2/B1 bit pairs; five procedures × three probes |
| Graph distances | 1024 | All 64 simple undirected four-vertex graphs × 16 ordered endpoint pairs |
| Graph/permutation checks | 1536 | All 64 graphs × all 24 bijections; distance invariance checked for accepted automorphisms |
| Composition triples | 64 | Three disjoint singleton records with values 0..3 |

Every state update is compared to separate four-field arithmetic. List shares
use an independent counting expansion and the half-sum absolute-difference
formula. Graph distances use a separate all-pairs distance expansion rather
than the owner's queue search. These finite checks do not bound Nat fields
or arbitrary callbacks. Seven changed practice cases are also calculated.

Actual handlers check 300 share predictions and 60 graph predictions,
including wrong answers, missing-prediction gates, context resets and
prediction-change hiding. These fixtures establish no browser layout or
reader learning result. Rendering is checked separately at publication.

## Exact Lean evidence

The full native `CompositeSystems.lean` text is re-elaborated unchanged in
its own namespace; no imports are removed. All 33 explicit native theorems
have selected axiom reports. Nine book theorems cover regrouping, mapped-list
preservation, relay order, a misleading read label, equal multiplicities
with different lists, a coarse probe, the injective converse, partial
symmetry and different probes. All 42 added reports are axiom-free.

The logic-through-composite portion contributes 114 reports: 100 empty axiom sets,
two exactly `propext`, twelve exactly `propext, Quot.sound`. The native
59-theorem compiled census also includes generated declarations and is not
replaced or regenerated by this book check. The selected proof reports do
not establish Python graph correctness or a distribution theorem in Lean.
Source hashes use UTF-8/LF text in `composites.json`. The subsequent
[valuation continuation](VALUATIONS_SOURCES.md) brings the combined driver
to 148 reports.

See [DEVELOPMENT](DEVELOPMENT.md) for commands. Physical correspondence,
broader research integration, comprehensive accessibility and independently
observed novice comprehension, transfer and retention remain open.
