# A finite Hamiltonian index at the exchange boundary

AuthorityEffect: None. This is post-seal research. "Hamiltonian", "fermion",
"SQL", and "GIN" are supplied research vocabulary, not native names or
inputs to the sealed derivation. No claim here changes the seal.

## Where the extra structure enters

The sealed `paper/primitive_difference.md` starts with a witnessed relation.
Irreflexivity is an additional fidelity law: it prevents identification of a
witnessed pair while preserving that law. The dependency table in
`paper/native_derivation_map.md` separately refuses inference of the full
irreflexivity law from off-diagonal facts and of an orientation from two-ness.
These are distinctions and protected collapses; they do not define an exchange
operator or a Hamiltonian.

`research/sign_tower/FINDINGS.md` finds no sign on the certified native quotient
observables. `research/natural_sections/STATUS.md` then declares a two-label
hop/flip transport and constructs exchange loops on the square and star.
`research/exchange_coefficients/README.md` adds sorted two-site occupancy,
insertion/removal signs `(-1)^r`, and unit negative hopping. Its Lean theorem
equates the declared ordered coefficient and the pinned hop/flip coefficient;
its independent Python matrix construction agrees on all 1,098 labelled
simple graphs with two through five sites. The extra convention is the point
at which this note starts calling the matrices Hamiltonians. It is not a
derivation of fermions from irreflexivity alone.

The precise family indexed here is

`H(G) = -sum_{{p,q} in E(G)} (c†_p c_q + c†_q c_p)`

on the **sorted two-occupant basis**, with no on-site terms or interactions.
The allowed presentation change is only a diagonal basis rephasing by `+1`
or `-1`. A matrix is *diagonal-sign-gaugeable* here when one such rephasing
makes every nonzero off-diagonal matrix entry `-1`. This term is deliberately
narrower than any general use of "sign-problem-free".

## Exact finite result

`bipartite_index.py` builds the ordered-occupancy matrix, checks site
bipartiteness, and searches the signed configuration graph. Its breadth-first
search returns either a diagonal sign assignment (checked on every nonzero
entry) or a closed configuration walk whose transport product is `-1`
(checked directly). For a closed walk, every vertex sign occurs twice, so
that product survives every allowed diagonal rephasing. The verifier checks
every catalogued certificate against a freshly constructed matrix.

| sites | bipartite and gaugeable | bipartite and obstructed | nonbipartite and obstructed |
| ---: | ---: | ---: | ---: |
| 2 | 2 | 0 | 0 |
| 3 | 7 | 0 | 1 |
| 4 | 34 | 7 | 23 |
| 5 | 206 | 170 | 648 |
| **total** | **249** | **177** | **672** |

The 1,098 rows are in `evidence/bipartite_catalog.jsonl`, one case per line,
with exact labelled site edges, a site coloring when one exists, and a
checkable gauge or negative loop. `evidence/bipartite_summary.json` holds the
counts and declared scope. The source is executable rather than a hand
classification: `verify.py` regenerates both files and binds their bytes in
`evidence/verification.json`. The finite tests independently compare the
breadth-first answer with exhaustive sign assignments through four sites.

In particular, the four-site square with edges `(0,1), (0,2), (1,3), (2,3)`
has bipartition `{0,3} | {1,2}`. Its two-occupant walk

`{0,1} -> {0,3} -> {0,2} -> {1,2} -> {0,1}`

has transport product `-1`. The star with edges `(0,1), (0,2), (0,3)` is also
bipartite and has no site cycle, but has a negative exchange walk. Thus an
index hit for **site bipartiteness alone** cannot certify this diagonal gauge.
These statements concern this basis and transformation class; they do not
rule out other representations or algorithms for the same free Hamiltonian.

All 1,098 finite rows agree with a sharper feature: a diagonal gauge exists
exactly when every connected site component is a path or isolated vertex
(`linear_forest`). The general-size characterization is a **conjecture here**,
not a sealed or Lean theorem. The intended proof obligation is to connect
closed configuration walks to exchange parity: particles cannot pass within
a path component, while a cycle or a three-arm branch should supply an
explicit exchange walk. The finite agreement and individual certificates do
not discharge that arbitrary-size obligation.

## Relational/index interpretation

The exact case key must include the site graph **and** occupancy, ordered
basis, coefficient convention, and allowed transformation class. The current
catalog fixes the last four globally and indexes the labelled site graphs.
`inverted_index` stores postings for site count, site bipartiteness, linear
forest, and diagonal-gauge verdict; `query` intersects postings. This is the
same retrieval role a SQL inverted index would play. The returned row is a
candidate; `verify_certificate` checks its mathematical payload.

A database extension could store an exact `hamiltonian_spec` row, a separate
`certificate` row with its checker and source pin, and feature postings over
the specification. A GIN index over those postings would shorten retrieval;
it would neither create a missing exchange witness nor prove that a physical
Hamiltonian was represented faithfully. `research/domain_adapters/CLAIMS.md`
leaves operator-family adapters open, and `research/native_bridge/CLAIMS.md`
shows why a commuting state encoding alone is too weak: observation and event
selection remain separate obligations.

The next useful extension is to formalize the linear-forest criterion and
then add certificates for a second, explicitly specified transformation
class. A broad Hamiltonian search must carry a representation-preserving
adapter, exact coefficient data, a witness or obstruction, and an explicit
`UNKNOWN` outcome. This catalog neither classifies all Hamiltonians nor
locates a general complexity boundary.
