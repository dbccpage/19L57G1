# Better Than What? Measuring the Gap Between Evaluation and Selection

**Author:** Jeremy H. Carroll

**Status:** draft — no version, no release, no hashes.

**AuthorityEffect:** `None`

---

## Abstract

A comparison is not one act. Deciding that one thing is better than another
requires a carrier, a declared measure, an evaluation under that measure,
and an authorization that the comparison stands. These are independent
declarations, routinely collapsed into a single reported verdict.

We measure the gap between the second and third. In a finite obstruction
setting, a single demand to make two objects distinguishable has **three**
tied minimal responses under one admission reading and **five** under
another, together with a countably infinite family indexed by arity;
refining the measure collapses this to one isomorphism class that still
contains **two** concrete responses. Separately, two positive measures can
assign **opposite orderings** to the same pair of nonzero classes, while the
zero verdict is invariant under every positive measure.

Consequently evaluation determines neither the selection nor the ranking. A
system that reports a single answer has made a selection its inputs did not
force, and possesses no internal marker distinguishing that selection from a
derivation. Capability does not close the gap, which lies between
description stages rather than within one.

We give the legitimate closure — declaring an invariance narrows the
admissible measures, and at the limit forces one — and a worked adversarial
record of the failure occurring in practice.

---

## For any reader: three doors and two sandcastles

*This section assumes nothing and stands alone. A reader who stops here has
the whole claim.*

Three doors, a car behind one. You pick; the host opens another to show a
goat; you may switch. Switching wins two times in three, which has annoyed
people for fifty years.

The forgotten part: **that answer depends on a rule you were never shown.**
Does the host always open a goat door? Does he know where the car is? Would
he have opened yours? Change any of these and the answer changes. Same three
doors, same choice, same visible evidence. The number was never in the
doors. It was in a declared rule.

Two children build sandcastles; one taller, one wider. Which is better? You
cannot answer from the sand. Choose height and the first wins; choose width
and the second does. Nothing about the castles changed.

Ask a machine and it answers at once, fluently, with reasons — and does not
mention that it chose the measure. It cannot: from the inside, *the answer*
and *one of several answers, picked* are indistinguishable.

**How large is that gap?** Take the smallest interesting case: make two
objects distinguishable, as cheaply as possible. The cheapest solution costs
two moves. There are **three** genuinely different two-move answers — not
three spellings of one, three that cannot be transformed into each other.
Change one starting assumption and there are **five**. Loosen the tools and
there is **no end** to them. Sharpen the measure to break the tie and it
nearly works: you reach a single kind of answer, which still contains **two**
concrete ones, mirror images, with nothing preferring either.

Most famous counterintuitive results take something away. This one gives
something back: where you expected one answer, there are three, or five, or
infinitely many.

---

## 1. Four declarations, routinely collapsed

*[Draft. Carrier, measure, evaluation, authorization as independent
declarations. The reported verdict collapses them. Cross-reference the
observer-packet formulation: an observer is not a primitive but a declared
regime under which a comparison becomes evaluable.]*

---

## 2. The measurement

*[Draft. Setup: finite carrier, licensed repairs as a declared linear
subspace, positive weights, the separation demand. Then the counts, with the
enumeration and its declared bounds:*

- *3 tied non-isomorphic minimal responses (reading L), 5 (reading F)*
- *countably infinite tie family indexed by arity, one per k ≥ 1*
- *minimum cost exactly two items, both readings*
- *refined measure: unique up to isomorphism, class still containing two
  concrete responses related by the transposition of the demand*

*State the bounds. These are bounded theorems, not asymptotics.]*

---

## 3. The ordering is measure-relative; the zero verdict is not

*[Draft. The value is the support function of the dual body
`K(w) = ker(Aᵀ) ∩ {|zᵢ| ≤ wᵢ}`, so the measure enters only through that
body — and the map is strongly non-injective: an unbounded family of weight
vectors is observationally identical.*

*Then the sandcastle, formalized: two positive weightings assign opposite
orders to the same pair of nonzero classes, while `Φ = 0 ⟺ x = 0` under
every positive weighting. So the only content invariant under change of
measure is whether a difference exists at all. Any verdict that **ranks**
has imported a measure.]*

---

## 4. What a fluent system does with a gap

*[Draft. It fills it and reports the filling as a derivation. Not deception
— unauthorized selection. Reporting a set reads as failure; reporting one
answer reads as competence. Capability does not help: the gap is between
description stages, not within one, so a more capable system is a more
fluent filler of the same gap.]*

### Worked record

*[Transcript only. No adjectives, no interpretation — the reader draws the
inference. Five instances from one adversarially-reviewed session of a
language model operating under an explicit verification discipline:*

1. *a record asserted not to exist, without the lookup being run; it existed*
2. *a "finding" of zero results from a query against the wrong key, which
   would have reported an audited substrate as unaudited*
3. *a self-check exercising its own re-implementation rather than the
   production path*
4. *the same defect again after repair, at a different boundary, inside
   machinery written to prevent it*
5. *a confirmation drawn from a reproduction that had silently broken*

*For each: what was claimed, what was the case, what caught it. In every
instance the catch was external — a reviewer substituting values into the
code, a gate failing, a figure surprising enough to re-check.]*

---

## 5. The legitimate closure

*[Draft. Not detection — declaration. Two forms:*

*(a) Report the selection as an object: which of the tied minima was taken.*

*(b) Stronger: declare an invariance that forces it. Admissible measures are
antitone in the declared symmetry — more symmetry, fewer measures — and at
the maximal-symmetry endpoint the measure is forced up to scale; a
transitive isometric group forces the Euclidean form. The freedom is
**relocated**, from "which measure" to "which symmetry", not removed. A
symmetry declaration is checkable in a way a measure choice is not.*

*(c) Verification by something that did not generate the claim. A checker
exercising its own copy of the logic certifies the copy — observed twice in
§4.]*

---

## 6. Physics: this is gauge freedom, applied to claims

*[Draft, and the terminus. Physicists already live with this structure and
do not regard it as a defect: gauge freedom is redundancy in description,
observables must be gauge-invariant, and gauge fixing is a declared,
undetermined choice that changes intermediate quantities and no prediction.
Coulomb or Lorenz — you declare, you do not discover.*

*The claim of this paper is that the same discipline applies to claims
rather than fields, and that the residual freedom is not an embarrassment to
be quotiented away.*

*Then the one step a physicist can check in their own currency: the
conditional Hilbert lift in the Born-normalization treatment, where the lift
is a selection and the derivation is conditional on it. Cite it, state what
it does and does not establish, and stop. The rest is a research programme
and this paper does not ask anyone to accept one.]*

---

## Non-claims

- **No impossibility theorem about evaluation and authority.** None is
  proved here and none is known to us. The defensible position is that this
  calculus is a discipline *for* an authorization it must be handed, not a
  construction of one.
- Authorization may be local, incomplete, and capricious. Nothing here
  denies that; the claim is that it is not *derived*, and must therefore be
  declared and replayable.
- No claim about consciousness, intent, or what a system understands.
- No safety guarantee. A declared selection may still be a poor one. It is
  merely checkable.
- **Every figure in this paper is currently a restatement, not a result of
  it.** The counts originate in the sealed derivation's exported claim data;
  §2 is a draft placeholder and does not yet reproduce the enumeration. In
  the source, the arity-indexed family is proved and the tabulated counts
  are bounded theorems under declared bounds — but until §2 is written,
  this paper asserts none of that on its own authority, and no gate compares
  these copies against the source.
- §4 is one session, adversarially reviewed. It is a worked instance, not a
  frequency estimate.
- No result here is mechanized. Nothing is proof-assistant checked.
- Nothing in this paper authorizes anything.
