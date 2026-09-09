# Coherent process limits: the represented process observed at finite scales

AuthorityEffect: None.  Outside the sealed derivation; consumes it read-only.
Not registered in `.github/workflows/verify.yml`: its checks run locally
through `verify.py` (section 7).

**Result.**  The process of the represented execution family — the merged
`Control` machine run by its deterministic runner — is observed at finite
scales, where a scale is the number of steps watched and the observation at
scale `n` is the tape after `n` steps.  The observations are **compatible at
every scale** as a theorem: each is a prefix of the next (`obs_prefix`,
`obs_prefix_add`), because a step only appends.  Abstractly, compatible
families of finite words over a finite carrier are exactly the sequences
(`ofSeq_toSeq`, `toSeq_ofSeq`, constructed without choice — a bijection, not
the limit's universal property, which is not claimed), eventual
agreement is not compatibility (`eventual_not_compatible`), and the even
scales have the same threads (`thread_even`, `even_thread`), carried by the
restriction of a thread to those scales (`restrictEven`, `restrictEven_eq`).  What the tape
observation loses is the fuel (`lost_fuel`, on the `forever` program); what
determines the next datum is the program and the active datum
(`next_active_det`).  A shifted observation is not a function of the prefix
(`shift_not_local`).  The three verdicts are separate: the observation is
injective on tapes; the process's image is not dense (no realized tape
extends `[0, 1, 0, 2]`, since realized tapes are functional); it is not
surjective.  The **connected experiment**: the `forever` program, identified
from the family's artifact, observed at scales 3, 6, 12 and 24 — one state
at fuel 24 read by `obs` at four scales, so each observation is a prefix of
the next by `obs_prefix_add`, the artifact's own recorded tape (six entries)
a prefix of every finer one and an extension of the coarsest, and the bound `L ≤ 3 · zeros ≤ L + 2` derived at scale 3
from the visible period holding at every finer scale with the readout
unchanged.  On the cycle's sequence `i ↦ i % 3` the bound is a theorem for
every `L` (`zeros_bound`): the frequency of datum 0 is `1 / 3` up to
`2 / (3 L)`, precision `ε` needs `L ≥ 2 / (3 ε)`.  The run's tape **is** that
sequence's prefix (`forever_iter`, `forever_obs`), so the bound is a fact
about the observation itself (`forever_run_bound`) and not only about the
arithmetic; and the observation does not read the declared fuel while fuel
lasts (`obs_fuel_indep`).  No interval, circle or
real number is used; the topology of the thread space is declared — totally
disconnected — and none of those is claimed.

**A finding for the family that wrote the artifact, and its repair.**  Its
`setting_json` is the sealed `Setting.json`, whose `ops` field is set-valued
— sorted, repetitions collapsed — so it determines neither the index order
the enablements refer to (taken alone it puts the constant map at index 0)
nor the operation count.  The producer now records `ops_in_index_order` on
every run and this family reads it, cross-checks it against the sealed table
set and replays every run (`identify_programs`); for a record without the
field the order is still recovered as the one ordering under which every run
replays, and an enablement naming an operation the sealed schema collapsed
is refused by name.  That is the artifact contract doing its job.

Lean: 42 authored theorems, 83 reports with the compiler-generated ones,
all within `{propext, Quot.sound}`, in a package importing the sealed package
and the represented execution package.  Python: the abstract system and the
observations mirrored; the artifact consumed and never written; every
recorded run replayed; compatibility checked on every identified program,
every datum, twelve scales; the three verdicts computed over the 64
deterministic programs on the recorded setting; the experiment at four
scales; 43 tests, strict typing over nine files, two byte-identical records.
Execution base `f5c445f40f339031e1a3191c5147b4eba98525b8`, the represented
execution family's repaired commit, at which its artifact is frozen and pinned;
no sealed path and no sibling path is written.

## 1. The abstract inverse system (`lean/Limits.lean`)

| definition | content |
|---|---|
| `Stage c n` | a word of length `n` over a carrier of size `c`: `Fin n → Fin c` |
| `bond c n` | forget the last entry |
| `Compatible c t` | the bonding holds at **every** scale |
| `Thread c` | the compatible families |
| `ofSeq`, `toSeq` | the prefixes of a sequence; the sequence read at scale `i + 1` |
| `eventual` | constant 0 except at scale 1 |
| `ebond`, `ECompatible`, `EThread`, `eofSeq`, `etoSeq` | the even-scale subsystem |

| theorem | content |
|---|---|
| `toSeq_ofSeq`, `ofSeq_toSeq`, `stable` | **the thread space is the sequence space** (CL-CP-01), a bijection; no axiom in the first and third |
| `eventual_agrees`, `eventual_not_compatible` | eventual agreement is not compatibility (CL-CP-02) |
| `etoSeq_eofSeq`, `eofSeq_etoSeq`, `estable`, `thread_even`, `even_thread`, `restrictEven_eq`, `thread_restrictEven` | the even scales have the same threads, carried by restriction (CL-CP-03) |
| `shift_not_local` | shifting needs the entry beyond the boundary (CL-CP-06) |

The contrast with the sealed `wit_no_infinite`: there, arbitrary finite
witnesses need not assemble; here they assemble because the family is
compatible by construction and the bonding is restriction.  No compactness
is invoked.

## 2. The process at step scales (`lean/Observe.lean`)

| definition | content |
|---|---|
| `next` | one step of the runner; a terminal keeps the state |
| `iter n`, `obs n` | `n` steps; the tape after them |
| `cyc`, `zero`, `succ3`, `base`, `forever` | the family's three-point setting and its cycle-everywhere program, transcribed |
| `zeros L` | the zeros among the first `L` entries of `i ↦ i % 3` |

| theorem | content |
|---|---|
| `stepDet_inr`, `next_tape` | a step is the firing of the one enabled operation and only appends |
| `obs_prefix`, `obs_prefix_add` | **compatibility at every scale** (CL-CP-04) |
| `next_active_det` | the next datum is a function of the program and the active datum |
| `lost_fuel` | same tape, different fuel, different next observation (CL-CP-05) |
| `zeros_eq`, `zeros_bound` | `zeros L = (L + 2) / 3`; `L ≤ 3 · zeros L ≤ L + 2` (CL-CP-08) |
| `iter_succ`, `next_halt`, `next_branch`, `next_exhausted`, `next_refuse`, `next_fire`, `next_fuel` | one step, by cases: what fires, what stands, what the fuel does |
| `same_next`, `obs_fuel_indep`, `obs_fuel_eq` | **the observation does not read the declared fuel while fuel lasts** (CL-CP-04's obligation) |
| `enabledAt_forever`, `lookup_forever`, `cyc_mod`, `forever_iter`, `forever_obs` | **the tape is the sequence**: after `n` steps the tape is the first `n + 1` entries of `i ↦ i % 3` (CL-CP-08's obligation) |
| `forever_length`, `forever_zeros`, `forever_run_bound` | the bound carried from the sequence to the run |

## 3. The artifact consumed (`limits.py`)

`research/represented_execution/evidence/process.json` is read, never
written, and pinned by digest in `SOURCE_MANIFEST.json` at the commit at
which that family is frozen.  Its fragment must be `control`.  Its eight
recorded controlled runs identify the four programs: the operation order is
the one permutation of the sorted tables under which every run replays to
its recorded tape and terminal; none or several is a refusal.  The
identified `forever` program is the cycle enabled everywhere.

## 4. The connected experiment, the verdicts, the failures

| item | what is recorded |
|---|---|
| scales 3, 6, 12, 24 | one state at fuel 24, read by `obs`; tapes of length 4, 7, 13, 25; zeros 2, 3, 5, 9; `3 · zeros − L ∈ {0, 1, 2}` at each |
| compatibility | each observation a prefix of the next; the artifact's recorded tape (fuel 5) a prefix of the scale-6, 12 and 24 observations and an extension of the scale-3 one |
| the bound | derived at scale 3 from `[0, 1, 2, 0]`; the readout unchanged at every finer scale |
| lost fuel | fuel 0 and fuel 1 from datum 0: tape `[0]` both; after a step `[0]` and `[0, 1]` |
| shift | `[0, 1, 2]` and `[0, 1, 0]` share the prefix `[0, 1]` and shift to `[1, 2]`, `[1, 0]` |
| verdicts | injective on tapes; not dense — no realized tape of the 64 × 3 runs extends `[0, 1, 0, 2]`, all are functional; not surjective |

The receipt (`run.py`) refuses an artifact whose fragment is not `control`,
programs the runs do not identify uniquely, observations that are not
prefix-compatible, a recorded tape not prefix-related to the observed run,
and a bound that fails at any scale.

## 5. Item 3's square, and item 3's second paragraph

The commuting law holds for the scale system of run-observations: observing
then advancing is advancing then observing, with the coarse observation the
prefix (`obs_prefix`).  For a per-state observation that reads only the tape,
the square fails — the failure pair is `lost_fuel`, the lost information is
the fuel, and the repair is to observe the fuel, after which the next datum
is determined (`next_active_det`).  For a fork the runner stops with the
terminal `branch` and the tape freezes: lifting the successor relation to
threads is not built.

The causal footprint of a step is what the merged `fire` reads and writes:
the enablement self-instance and the operation edge at the active datum;
the active datum, the tape, the clock and the fuel, keeping the program.  An
edit away from the active datum does not change the step; an edit at it does
(the family's mutation tests).  The process has one locus of activity, so
independence and interaction between two loci are not built.

## 6. What "the limit" is here, and is not

The thread space is all sequences over the carrier.  The process generates
functional tapes — equal entries have equal successors — hence, on a finite
carrier, eventually periodic ones: a strict subset, exhibited by the prefix
`[0, 1, 0, 2]` no realized tape extends.  The limiting quantity of the
experiment is the rational `1 / 3`, isolated by a bound on naturals with a
computable precision rule; the existence of the limit and effective access to
it are separated by that rule.  Topology, declared and not proved: the
product of the discrete topologies on the finite stages, totally
disconnected; not an interval, not a circle.  An interval would need an order
or metric compatible with the stages and an identification of threads
(dyadic twins, for instance) that this family does not make.

## 7. Evidence

**Lean** (`lean/`, `evidence/lean.json`): 42 authored theorems and 41
compiler-generated ones (the proof terms of bounds inside definitions and of
case splits inside theorems), 83 reports, all within `{propext, Quot.sound}`;
the report population equals the environment census of the `Limits` and
`Observe` namespaces in both directions; no private theorem; forbidden-token
scan clean.  `Classical.choice` was observed once, when `omega` negated a
conjunction goal classically; the conjunction is now split first and the
reliance is gone.

**Python** (`limits.py`, `run.py`, `evidence/limits.json`, `tests/`): 43
tests, strict typing over nine files, the two records replay byte-identically.
`verify.py`, `verify_sources.py`, `verify_lean.py` and `run.py` follow the
sibling families' files with names, pins and refusals changed; this tree's
directory is always first on the path, and `run.py` and `verify_lean.py`
refuse by name if a foreign guard is imported.

**Custody** (`verify_sources.py`, `SOURCE_MANIFEST.json`): at
`f5c445f40f339031e1a3191c5147b4eba98525b8`, the eight derivation modules and
the consumed `translation`, `execution` and `control` modules by digest and
runtime origin; the sealed `lean4/Derivation` tree, the merged
`local_reuse`, `ignition`, `magnification`, `setting_translation` and
`represented_execution` Lean trees, and the `setting_translation` and
`represented_execution` Python trees by Git tree object; the Lean
configuration of the six packages and the represented execution family's
artifact by digest.  An untracked source in any of the nine trees is refused.
The two records are `-text` by an in-tree `.gitattributes`.

```powershell
cd research/coherent_process_limits
python verify.py     # sources, tests, mypy, lean (lake build + census), limits --check
```

Regenerate the two records deliberately and never under a live injection:
`python run.py --write`, `python verify_lean.py --write`.

## Not claimed

* An interval, circle, integration theory or real number: the limit is a
  totally disconnected thread space and a rational frequency with a bound on
  naturals.  The topology is declared, not proved.
* That the `forever` tape after `n` steps *is* the first `n + 1` entries of
  `i ↦ i % 3`: computed at every recorded scale; the proved bound is on the
  sequence.  This is the labeled missing connection.
* The general theorem that every realized tape is functional along a whole
  run, or eventually periodic: the one-step determinism is proved; the rest
  is computed over the declared class of 64 programs.
* Lifting a fork's successor relation to threads; a second locus of activity.
* That the Python mirrors compute the Lean predicates: the agreement is on
  the stated finite populations.

## Files and running

| file | role |
|---|---|
| `lean/Limits.lean` | the abstract inverse system, its bijection with the sequence space, the negatives, the cofinal rescaling |
| `lean/Observe.lean` | the process at step scales, compatibility, the lost fuel, the next datum, the bound |
| `lean/Inventory.lean` | the environment census |
| `limits.py` | the mirrors, the artifact consumed and the programs identified, the experiment, the verdicts |
| `run.py`, `evidence/limits.json` | the record and its refusals |
| `verify_lean.py`, `evidence/lean.json` | the Lean build, two-way census and reliance record |
| `verify_sources.py`, `SOURCE_MANIFEST.json` | custody of the consumed inputs, the artifact included |
| `verify.py` | every check in order |
| `tests/` | the abstract system, the artifact, the observations, the experiment, custody, the parser, the records |
| `CLAIMS.md` | one `CL-CP-*` entry per claim |
