# Ordered coefficients and exchange transport

AuthorityEffect: None.

This tree ports operator-supplied examples into a separate research package.
The author requested this comparison after prior discussion and an external
supplement. It is not an independent or blind derivation. Neither the example
target nor the added insertion/removal convention follows from the seed.
No external supplement, manuscript, or local absolute path is a runtime input.

The read-only source is commit
`cea346d7f3603fd8da374947e76c9b3cd426d122`. `SOURCE_MANIFEST.json` binds its
twenty-module import closure. Verification stages those exact Git blobs into
the ignored `lean/pinned/` directory and builds inside this tree. It refuses
source drift, an unavailable ancestor, and extra or missing staged modules.

## Declared convention and proved correspondence

Configurations are sorted two-site subsets. Removing or inserting a site
contributes `(-1)^r`, where `r` is the number of occupied earlier sites;
inserting at an occupied site gives zero. Each adjacency move receives weight
minus one. These conventions are explicit additional inputs.

`ExchangeCoefficients.ordered_eq_transport` equates the resulting four-term
coefficient with the pinned `hopB`/`flipB` coefficient,
for every loop-free Boolean adjacency and every pair `x < y`, `u < v`.
`scaled_eq` allows every integer scale; `finite_matrix_eq` gives equality of
the matrices at every finite site count. Adjacency symmetry is unnecessary
for this correspondence. The independent Python occupancy implementation uses
bitsets and does not call transport to build its move matrix.

The general proof uses only `propext` and `Quot.sound`. Equality is rewritten
using the natural-number equality lemma before simplification, avoiding a
more general order-instance dependency. The three finite fixtures and general
closed-loop sign-invariance proofs require no axioms.

## Reproducible examples

`HAMILTONIAN_INDEX.md` reports the bounded two-occupant graph index built by
`bipartite_index.py`. Its 1,098 checkable gauge or negative-loop certificates
are regenerated in `evidence/bipartite_catalog.jsonl` by `verify.py`.

| Result | Evidence | Exact scope |
|---|---|---|
| Ordered coefficients equal transport coefficients | `lean/ExchangeCoefficients.lean` | General two-site theorem with the hypotheses above |
| Chain, square, star matrices agree entrywise | `three_fixtures`; `examples.py` | 36 entries per six-state matrix |
| All simple labelled graphs agree | `examples.py` | 1,098 graphs, sizes 2..5; 104,778 entries |
| Removal/insertion identities | `examples.py` | 10,350 basis equalities at sizes 1..6; general operator library remains open |
| Star characteristic polynomials differ | `examples.py` | Signed: `λ²(λ²−3)²`; unsigned: `(λ²−4)(λ²−1)²` |
| Closed odd loops survive vertex sign changes | `path_gauge`, `closed_odd_gauge`; Python controls | General Boolean theorem; all 64 vertex sign assignments checked for each six-state fixture |
| Signed boundary cancels; unsigned control fails | pinned `d2_zero_unrestricted`; `test_examples.py` | General coefficient theorem plus finite controls |
| Odd integer weights vanish on the diagonal; rational half is nonzero and doubles to zero | pinned `SlotEx`/`Receiver` results; Python examples | Declared integer weights and rational turns |
| A certified typed state contains its proposition's proof | `lean/ClaimExample.lean` | Separate from the Python implementation |
| A false matrix equality and an unsupported schema are refused | `claim_example.py` | Submitted finite integer matrices; no arbitrary-prose checker |

The polynomial calculation uses an exact trace recurrence and independently
checks determinant values by rational row elimination. Agreement at seven
distinct arguments determines a degree-six polynomial. Vertex sign changes
preserve the star polynomial in the exhaustive finite control.

## Run locally

With Python 3.11+ and Lean 4.33.0 installed, from this directory:

```text
python verify.py
```

`--lake PATH` selects Lake explicitly. `--python-only` reports Lean as
`NOT_RUN`. Python uses the standard library; optional pytest can run
`test_examples.py`. Assertions must be enabled. `evidence/verification.json`
binds the current inputs and result bytes. `AXIOM_DECLARATIONS.json` lists
the sixteen named new theorems and four inherited results reported by the
audit. This is a scoped inventory, not a theorem that all prose is correct.

This tree is a local receipt and is not added to the written gate-11 census.
No dynamics, endogenous demand, general many-occupant correspondence, or
semantic equivalence between Python and Lean is established here. The typed
claim example and the finite checker do not translate arbitrary language into
propositions. The checker accepts plain JSON-shaped containers; custom list
subclasses cannot override matrix equality. Counts and matrices are computations,
not unrestricted proofs.

## Integration limit

The native namespace used by the imported definitions adds one occurrence to
the prose census. The watched vocabulary and all previous counts are unchanged.
The `second_stream` source manifest also pins that census file in its entirety
at both its historical snapshot and HEAD. Its byte-equality check therefore
fails on this addition. A pass from this package's verifier does not discharge
that separate check. Its historical pins have not been rewritten.
