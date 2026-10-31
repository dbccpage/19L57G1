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

## Actual steps and changing encodings: Lessons 08–13

The continuation consumes `research/native_bridge/bridge.py` and the
sealed `primitive_passage` functions read-only. It adds no research result,
source correction, event-selection rule, or physical correspondence.

| Lesson | Meaning used | Owner and scope |
|---|---|---|
| 08–09 | Deterministic steps, histories, actual paths, composition, equal events | NB-1/2; `Path.run_events`, `Path.events_injective`, `Path.events_append` |
| 10 | State-threaded target histories and replay agreement | NB-7/9; `Sim.run_trHist`, `trHist_append`, `budgetSim` |
| 11 | Injective budget codes with one core and one native observation | NB-9/16; `toggle_encoding`, `budgetSim_nobs` |
| 12 | Faithful observations are constant on source cycles into this passage | NB-8/16; `passage_sim_cycle`, `ObsSim.obs_const_on_cycle`, `toggle_no_faithful_obs`; positive control `idObsSim_faithful` |
| 13 | Decode labels and check actual targets, with joined rows | NB-12/13; `realize_iff`, `realize_events`, `unrealized_step`; G013's indexed `Trace` supplies adjacency |

The new switch has states 0/1 and events flip/hold. Its four source-step
entries are supplied. Each target event writes the next state's code to
the otherwise initial live passage state's budget. Both full encodings
are distinct, their cores agree, and their specified native observations
agree. Reading budget is an explicitly changed observation with successful
recovery on the two used codes. No argument says that every possible
target observation is constant.

The packet records 126 histories: two starts, both event choices, lengths
zero through five. A separate population covers all sixteen deterministic
two-state/two-event tables on the same history bound, giving 2,016
translated histories. Those bounded Python computations are distinct from
the owner's general Lean history theorem. The original 512 map settings
and 65,536 factorization cases are unchanged.

Seven trace cases include an unknown label, the native mislabelled halt
counterexample, two locally valid but disconnected rows, an empty history,
and a valid inert repeated admission. The book adds adjacency to the
owner's Python `realize` helper; it checks local equations only. In Lean,
the indexed trace requires adjacency before the realizer is applied.
Thus the Python helper's output alone is not the full typed-trace claim.

For the book's Lean, the exact UTF-8/LF text of G013 `Trace.lean` and the
native-bridge Path, Passage, Sim, Observe and Realize modules is assembled
in dependency order. Only their import lines are removed; sealed imports
remain compiled read-only dependencies. Unknown imports fail review.
Sixteen selected owner declarations and four new book exhibits add twenty
axiom reports: fourteen `{propext, Quot.sound}`, one `{propext}`, five
empty. Together with the earlier map reports the driver checks 290:
146 both-axiom, 132 `propext`, two `Quot.sound`, ten empty. This is a
selected report scope, not every research declaration's census.

The source-text hashes include all consumed Lean bodies and the current
owner ledger/README. Re-elaboration checks those bodies now; it does not
reissue or modify the owner's frozen receipts. Event selection remains
NB-15 OPEN; X310/G012 read-back remains NB-17 OPEN. Native admission paths
and all domain adapters are not taught by this selected continuation.

Changed three-state practice checks its arbitrary codes 2/5/8, writes
8/8/2 and a repaired connected halt row using the same actual step owner.
Every example remains supplied mathematical data. Reader explanations,
transfer and retention require independent reader evidence.
