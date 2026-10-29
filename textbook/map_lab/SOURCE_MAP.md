# Source map and scope

AuthorityEffect: None. The finite cards, maps, labels, drawings, and checking
apparatus are supplied teaching data outside the sealed derivation.

## Owners and definitions

| Lesson | Meaning used | Native owner and boundary |
|---|---|---|
| 00, 03 | q is recovered by g after p on a declared domain | `Compression.FactorsOn`, `FiberConstant`, `factors_iff_fiberConstant`; the Python functions `factors_on`, `valid_factor_maps`, `fiber_constant` |
| 01–02 | Exact signature agreement gives classes; a representative labels each class | `sigList`, `SigEq`, `pQ`, `pQ_exact`; Python `sig_list`, `sig_eq`, `p_quotient`, `partition_of` |
| 04 | A paired view is class-constant iff both components are | `ObsDescent.classConstant_pair_iff`, `pair_descend_exists_iff`, `view_descends_pair_blocked`; finite encoded-pair cases are checked independently |
| 05 | Extra questions refine; duplicating or postprocessing answers adds no distinction | `Compression.enlarge_refines`, `dup_no_refine`, `postcompose_no_refine`; the finite controls concern the named families |
| 06 | Factor maps agree on observed image; quotient descent is unique on the quotient | `Compression.factor_unique_on_image`, `factor_not_unique_off_image`; `ObsDescent.descend_unique`, using quotient surjectivity |
| 07 | Fixed-domain factorization differs from global class-constancy | `ObsDescent.classConstant_iff_fiberConstant_all`, `descend_iff_factorsOn_all`, `fiberConstant_fixed_D_not_classConstant` |

The sealed files are `lean4/Derivation/Compression.lean`,
`DiffInterface.lean`, `ObsDescent.lean`, and `code/derivation/compression.py`.
Existing longer treatments are Units 61 and 67 and Institutions 00–02.

## Four cards and a precise finite adapter

A/B/C match `textbook/first_steps/cards.json`. D is separately supplied
as amber and round. Blue answers are 1,1,0,0; triangle answers 0,1,1,0.
The paired requested value is encoded as two times blue plus triangle,
so its four codes retain both Boolean components. The display decodes
these codes back into ordered Yes/No pairs.

The native Python `p_quotient(D,Q)` returns one value per entry of D,
aligned with D's order. On D = [1,3], its two entries do not occupy original
positions 0 and 1. The wrapper zips them with D before building a full
four-position table, using zero at excluded positions only as a teaching
extension. Native pQ agreement is checked on D; no agreement of that
arbitrary extension with Lean pQ outside D is claimed.

Forward and reverse orders choose different first representatives.
Those are two supplied orders, not all possible permutations. Empty D
has zero classes and no representative. An empty question family on a
nonempty D has one class.

| Population | Size |
|---|---:|
| Selected card domains | 16 |
| Kept-question families | 4 |
| Requested-answer choices | 4 |
| Representative-order choices | 2 |
| Recorded map settings | 512 |
| Four-label-presentation/binary-target/domain cases | 65536 |

The additional census covers every four-label presentation and binary
target on four positions, on all sixteen domains. The existing source's
canonical report bounds are not changed; this is a separately declared
book population using its actual functions.

Recovery on the observed image is checked by the source's exhaustive
lookup enumeration and pairwise constancy, with an independent blocking-pair
calculation. Complete lookup examples additionally enumerate four input
labels A/B/C/D into two Boolean outputs, or four ordered-pair outputs.
Their count is restricted to those finite alphabets. They do not enumerate
all total `Nat → Nat` maps, whose off-image behavior is unconstrained.

## Finite representation versus global quotient

The displayed recorder labels its actual classes by selected members.
Its image may be a proper subset of the four allowed lookup labels.
The native quotient type consists of equivalence classes themselves;
every class has a representative. This is why uniqueness on the whole
quotient does not contradict nonuniqueness on unused external labels.

The book's concrete global observer example uses a four-element `Fin 4`
carrier and `DiffInterface.kernelObs` on its blue view. The actual native
descent and blocking theorems are instantiated there. This is distinct
from a claim about all natural-number inputs. The native natural-number
dictionary requires factorization on every finite domain, not just one.

The packet checks loaded source origins and normalized UTF-8/LF hashes.
Book-Lean checks use actual native definitions and pin their axiom reports.
They check 128 domain/family/order settings against native pQ, signatures,
class counts, and explicit lookups, with four requested-factorization
outcomes per setting. There are 256 grouped case declarations, three
general book checking/composition lemmas, and five four-card observer
instances: 264 book declarations. Six native theorem reports bring the
total to 270. Exact axiom reports are 132 `{propext, Quot.sound}`, 131
`{propext}`, two `{Quot.sound}`, and five empty. The book results are
**derived (book Lean)**, outside the sealed census. Finite
correspondence is not a general Python-to-Lean refinement or an empirical
device correspondence. Reader comprehension and transfer remain unmeasured.
