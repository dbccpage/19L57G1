# Declared weights, their profile, and what the climb costs

**Contact response.**  The caller supplied an external package and
asked that this development reach it, attempt to climb it, and show
what climbing requires.  Sections 1–5 below are the native
derivation: they were carried out first, in this repository's own
vocabulary, with no external term used and no external result
targeted.  Section 6 is the only place the supplied package is
named, and it is a comparison, not evidence: nothing in sections 1–5
depends on it, and nothing in section 6 upgrades a claim.

Evidence: `lean4/Derivation/WeightProfile.lean` (25 theorems, axiom
reports propext / Quot.sound only), `code/derivation/weight_profile.py`
and `artifacts/weight_profile.json` (exhaustive within the declared
bounds recorded there), ledger claim CL-PD2-WEIGHT-PROFILE.

---

## 1. The datum is declared

A **weight assignment** attaches a count to each position of a finite
carrier.  Nothing in the passage calculus produces one.  It joins the
standing list of supplied inputs — fresh token supply, protection,
observer transport, budget, activation — and is priced the same way:
named, never derived.

The question this note answers is the only one the datum can answer
alone: **what does it fix, and what does it not?**

## 2. The profile is exactly a ray

Two assignments have the same normalized profile exactly when they
agree after cross-multiplying by each other's totals.  Stating it
that way keeps everything in integers: no division, no reals, no
completion.

- It is an equivalence on positive-total assignments
  (`profile_refl`, `profile_symm`, `profile_trans`).
- It is invariant under positive rescaling (`profile_scale`).
- Its classes are **exactly** the positive rays (`profile_iff_ray`) —
  an exact fiber classifier, in both directions, not an
  approximation.

What survives normalization: **support** (`profile_support`) and
**order** (`profile_order`).  What does not: the **total**
(`profile_forgets_total`), exhibited by doubling.

This is the same shape as `Compression`: the profile is a
question-relative compression, its fibers are exactly its
equivalence classes, and asking what it forgets is asking which
declared question family it is adequate for.

## 3. A lift adds nothing to the profile

Call an assignment `c` together with a declared modulus map `m` a
**decorated presentation** of `w` when `m ∘ c = w` pointwise.  Then
every decorated presentation of `w` carries `w`'s profile
(`lift_profile_redundant`), and any two decorated presentations of
the same weights carry the same profile
(`lifts_agree_on_profile`).

The proof is one line.  That is the entire content of the
redundancy, and saying so plainly is the point: a one-line identity
is exactly as strong as a one-line identity.

## 4. A correction made during the work

The first draft of the Lean module claimed something stronger and
more interesting: that two decorated presentations with the same
moduli could be separated by a declared mixing question, so that the
decoration carried a real datum invisible to the profile.

**The Python mirror refuted it.**  Over unsigned counts, squaring is
injective, so a decorated presentation is *determined* by the
weights it presents (`sq_injective`,
`unsigned_decoration_determined`).  The decoration is not merely
invisible to the profile — over unsigned values it is not there at
all, and it adds nothing to *any* question.

The claim was replaced by the true one, which is sharper and locates
the cost precisely:

> The extra representational capacity is **exactly a declared
> sign**.  Two *signed* decorations with identical moduli at every
> position are separated by the declared mixing read-out
> (`signed_decoration_visible_to_mixing`).  Without the sign there is
> no capacity; with it, the capacity is the sign's, not the lift's.

So redundancy is relative, and the relativity is now located: the
profile question, any question at all over unsigned values, and the
mixing question over signed values give three different answers, and
which one applies is fixed by the declared data — never by the
weights.

## 5. What descends, and the climb

**Descent.**  A declared linear read-out over two positions is
constant on modulus-blind inputs **exactly** when its cross term
vanishes (`descent_iff_subsingleton_support`).  `sq_add_sub`
isolates the obstruction: the gap between the two sign choices is
four times the cross term, and nothing else.  Anything that
genuinely mixes two positions does not descend.

**The climb.**  Nothing above singles out a read-out law.  Three
further declarations would be needed, and all three are stated in
the Lean module as **propositions that are never proved**:

| Import | Lean name | What it would assert |
| --- | --- | --- |
| Decorated carrier | `openDecoratedCarrierImport` | a set of decorated values with a modulus map onto the weights and a combination operation |
| Disjoint additivity | `openDisjointAdditivityImport` | the read-out of a split carrier is the sum of the parts' read-outs |
| Read-out uniqueness | `openReadOutUniquenessImport` | exactly one modulus-blind, nonnegative, additive read-out exists |

The third is the expensive one.  It is what a uniqueness claim
actually asserts, and nothing in this development proves it.

**Why all three are necessary** is itself proved, not assumed: the
weights do **not** determine a decoration
(`weights_do_not_force_decoration`).  Two different decorations sit
over the same carrier, one presenting the weights and one not, and
the declared mixing read-out separates them.  Any uniqueness law
therefore needs strictly more than the weights.

So the climb is **priced, not paid**.  What this development can say
is: here is the ladder, here are its three rungs, here is the proof
that you cannot skip them, and here is the exact point at which
declared data must be added.

---

## 6. Comparison with the supplied package

*This section names the supplied package.  It is a comparison only.
No claim in sections 1–5 depends on it, and nothing here upgrades a
theorem.*

The package (`qm_020`, "Born normalization and conditional Hilbert
lift") states a redundancy result and fences a uniqueness claim as an
import.  Matching it against the native derivation:

| Package statement | Native counterpart | Status |
| --- | --- | --- |
| Direct normalization gives a unit-sum profile | `profile_iff_ray` and the support/order theorems | derived, and sharper — the classes are exactly rays, with no division |
| Scale invariance of normalization | `profile_scale`, `profile_forgets_total` | derived |
| Normalization factors through the scalar-ray quotient, fibers exactly ray classes | `profile_iff_ray` (both directions) | derived |
| The lift reproduces the same law | `lift_profile_redundant`, `lifts_agree_on_profile` | derived, one line |
| The lift is "probability-redundant but dynamics-capable" | `unsigned_decoration_determined` + `signed_decoration_visible_to_mixing` | **sharpened and partly corrected**: over unsigned values there is no capacity at all; the capacity is exactly the declared sign |
| Row-sparsity of descent-compatible maps | `descent_iff_subsingleton_support`, `sq_add_sub` | derived for the two-position case |
| Uniqueness requires imported representation assumptions | `openDecoratedCarrierImport`, `openDisjointAdditivityImport`, `openReadOutUniquenessImport` | agreed, and stated as unproved propositions here too |
| Strict aggregation for exponents above one | — | **not available natively**: this development has no reals and no limits, so the strict inequality cannot even be stated here.  Recorded as outside scope, not as a gap in the package |
| Uniqueness as ontology | — | not claimed here, in any form |

**Where the two agree.** The package's central line — that the
normalization is a free re-encoding while the uniqueness is an
import — is exactly what the native derivation produces
independently, and the native version fixes the fiber structure
exactly rather than up to a convention.

**Where the native derivation is stronger.** The redundancy is not
merely "the lift reproduces the law".  Over unsigned values the lift
is *determined*, so there is nothing to reproduce; and the capacity
the package attributes to the lift is isolated here as a separate
declared datum — the sign — with its own price.  That is a finer
line than the package draws, and it was found by a mirror refuting a
draft claim, not by agreeing with the package.

**Where this development cannot follow.** Anything requiring reals,
limits, or completions is not statable here, and is left where it
is.  No part of section 6 is used as evidence anywhere in this
repository.
