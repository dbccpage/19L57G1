# F5 — The Composite Generator: Reflective Growth + Pair-Separation Closure

**Mission.**  Settle F5 of the frontier run
(`paper/refusal_as_difference.md`): the reflective chain grows a fresh
element at every round, and the pair-separation closure policy of the
first checkpoint demands the separation of every retained pair.  Is
their composite the development's first *self-sustaining* challenge
generator — obstructions arising forever with no additional event
supplied per round after the declared transition and closure policy are
fixed? And is the full obstruction-*repair* cycle self-sustaining, or
does every repair strategy in a declared class either import per
repair, act vacuously, or end generation?

Both component declarations are sealed checkpoints: the reflective
refusal semantics (`stepRefl`, FR10) and the closure policy (declared,
not endogenous, at the first checkpoint).  The question is precisely
whether their union needs any per-round supplement.

## TERMINAL

```text
ENDOGENOUS_GENERATION_PROVED
ENDOGENOUS_REPAIR_FAILS_IN_DECLARED_CLASS
GENERATION_REPAIR_EXCLUSION_IN_CLASS
```

Split by claim, since the two halves of F5 come apart:

* **Generation — proved, horizon-free** (`generation_never_dries`):
  from the third round on, the composite always has a live obstruction
  (elements 1 and 2 are distinct carrier elements with identical
  depth-1 profiles, for every chain length ≥ 3), and the only event
  consumed is the internally enabled reflection.  This is the first
  horizon-free challenge generator exhibited in the development; no
  minimality or uniqueness claim is made.  F5's generation half is
  **true** for the declared rule.
* **Self-sustaining repair cycle — absent from the declared bounded
  search**: over the five declared
  repair strategies, every branch lands in exactly one of three fates —
  fires-unrepaired (bare, presence-automark, depth-2), repairs with a
  fresh import at every firing round (per-pair marking), or generation
  dead (valued automark).  The F5-positive class — fires, repairs,
  never imports — is **empty within the declared 15-round
  computation**.  The class-general cycle claim remains open.
* **The exclusion**: within the five declared strategies and the
  15-round computation, no strategy both fires, clears every firing
  round, and avoids recurring imports.  The valued strategy prevents
  every demand rather than repairing a demand that fired.  Scope:
  horizon-free Lean cores for the four depth-1 strategies;
  instance-backed and bounded evidence for depth 2 (Lean instances at
  lengths 4 and 5, trajectories to the 15-round bound). The structural
  fixed-depth outrun is now proved by
  `SeparationCapacity.depth_d_outrun` and `depth_d_obstruction`. The
  general-`n` correspondence between sealed `Generator.profile2` and
  radius-one `SeparationCapacity.profileD`, and a repair-strategy-class
  consequence of the coloured capacity theorem, remain OPEN.

The remaining bridge obligation, exactly stated: **a repair channel
that separates without minting identity-grade distinctions** — or a
proof that none exists (G1).  Nothing in this run produces one.

* **Proved** (Lean, 16 new theorems, axioms within {propext,
  Quot.sound}): the chain's tag store (`reflective_chain_tags`); the
  depth-1 characterizations (`chain_tagged_iff`, `chain_hasIn_iff`,
  `chain_hasOut_iff`); the three profile classes (`middle_profile`,
  `endpoint0_profile`, `endpointN_profile`); the obstruction set
  identified exactly
  (`depth1_obstructions_are_exactly_middle_pairs`, an iff);
  endogenous generation (`generation_never_dries`); presence-automark
  vacuity (`automark_presence_vacuous`); the per-pair outrun
  (`finite_marks_outrun` — every finite marking is outgrown); the
  valued-mark collapse (`valued_marks_collapse_generation`); the
  direct-transposition result (`middle_swap_not_relation_preserving` —
  swapping interior points 1 and 2 does not preserve the successor
  relation; full rigidity is not proved); the depth-2
  instances (`depth2_separates_near_ends_n4`,
  `depth2_obstruction_n5`).
* **Computed only within bounds** (15 rounds per branch, depths 1–2,
  five strategies): the per-strategy trajectories, the classification
  table, the in-bounds exclusion (`endogenous_cycle_found: false`),
  and the Lean agreement checks.
* **Refuted**: that the composite hides a per-round import in its
  *generation* (it does not — proved); that any declared strategy
  realizes the endogenous cycle within the 15-round search; that presence marking
  repairs anything (vacuous by theorem); and that depth 2 escapes the
  observed obstruction (it separates near the ends and is outrun at
  length 5 and within the declared bound).
* **Imported, explicitly, where repair succeeds**: a fresh observable
  per repaired pair (per-pair marking — recurring), or the unbounded
  valued alphabet (identity-grade observation — one declaration that
  ends generation), or the depth-2 regime (one declaration, outrun at
  the proved switch point and within the declared bound). The
  structural all-depth outrun is now a theorem; the interface and
  strategy consequences named below are not.
* **Open**: G1 (no non-identity repair channel — class-general), the
  general-`n` `Generator.profile2`/`profileD · · 1` interface
  correspondence, a repair-strategy-class consequence of
  `CapacityBound.capacity_bound`, G3 (repair-power = generation-poison
  as a conservation law), G4 (the sealed engine as the import branch),
  and carried F4 (chain initiality). The former G2 structural depth-`d`
  outrun is CLOSED.
* **Single best next theorem target**: derive a declared
  repair-strategy-class exclusion from `CapacityBound.capacity_bound`.
  The capacity theorem bounds local finite-alphabet views; it does not
  itself quantify over strategies or prove the class-general cycle
  exclusion.

---

# FORMAL SPINE

## FG1. The composite and its bounds (exact declarations)

**[declared metatheory]**  The composite consists of the two sealed
declarations: the reflective refusal semantics (`stepRefl` — each round
reifies a tagged receipt of refusing the newest receipt and links
predecessor to successor) and the pair-separation closure policy
(after each admission, every unordered pair of distinct carrier
elements must be separable under the declared observation regime;
unseparated pairs are obstructions).  Bounds: fifteen accepted rounds
per branch; observation depths 1 and 2; the five-strategy repair class
of FG5.  Reflection is internally enabled and is never counted as an
import; both component declarations are one-time prices already on the
ledger of their checkpoints.

## FG2. The observation regime, structurally

**[definition + theorem]**  Depth-1 observation of element `i` is
`profile1`: the tag bit, whether some relation instance enters `i`,
whether some leaves it.  Element indices are metatheoretic bookkeeping,
never observable.  The chain's stores are characterized exactly:
`reflective_chain_tags` (the tag store is the non-zero initial
segment), `chain_tagged_iff`, `chain_hasIn_iff` (both ↔ `1 ≤ i ≤ n`),
`chain_hasOut_iff` (↔ `i < n`).

## FG3. The three profile classes; the obstruction set identified

**[theorem]**  Every chain element is seed, interior, or tip:
`endpoint0_profile` (`(false, false, true)`), `middle_profile`
(`(true, true, true)`), `endpointN_profile` (`(true, true, false)`).

**[theorem — an iff, no judgment]**
(`depth1_obstructions_are_exactly_middle_pairs`)  For distinct
`i, j ≤ n`: profiles coincide **iff** both are interior.  The closure
policy's demand is exactly the set of interior pairs — `(n-1)(n-2)/2`
of them at length `n` (count computed; growth quadratic).

## FG4. Endogenous generation — proved

**[theorem]** (`generation_never_dries`)  For every `n ≥ 3`, elements 1
and 2 are distinct carrier elements with equal depth-1 profiles.  The
composite fires at every round from the third on, forever, and the only
event consumed is the internally enabled reflection. No additional
event is supplied per round after the declared reflective transition
and closure policy are fixed. This is self-continuation relative to
those declarations, not absolute self-origination. No minimality or
uniqueness theorem is claimed.

The chain already auto-tags every receipt
(`automark_presence_vacuous`), so generation survives presence-grade
marking by construction: the demand is not an artifact of stinginess
with observables, but of their *presence-only* grade.

## FG5. The repair class and its three fates

**[declared metatheory]**  Five strategies, each a declared response to
the closure demand:

| strategy | declaration | fate (evidence) |
|---|---|---|
| bare | none | fires unrepaired forever (`generation_never_dries`; trajectories) |
| per-pair fresh marks | a fresh observable per repaired pair | repairs every round, imports at every firing round (trajectories); **never endogenous** — every finite marking is outgrown (`finite_marks_outrun`, horizon-free) |
| presence automark | one rule: every receipt is marked | **vacuous** (`automark_presence_vacuous`): receipts are already tagged; interior still collapses |
| valued automark | one rule: every receipt carries a *distinguishable* value (its index) | **generation dead** (`valued_marks_collapse_generation`): every pair separates, no obstruction ever arises; the price is an unbounded observable alphabet — presentation identity made observable |
| depth-2 regime | one declaration: profiles of neighbours visible | separates near the ends (`depth2_separates_near_ends_n4`), **outrun** in the deep interior (`depth2_obstruction_n5`); fires unrepaired from length 5 within bounds |

**[finite computation]** (`exclusion_check`, 15 rounds)  Trajectories,
first-fire rounds (3 for depth-1 strategies, 5 for depth-2, never for
valued), repair/import counts per round, and the classification table.
Per-pair marking needs a fresh import at *every* firing round within
the bound — repair debt tracks growth one-for-one.

## FG6. The exclusion, and its scope

**[bounded computation + theorem cores]**  The F5-positive
classification — fires, repairs, never imports — is empty over the
declared five-strategy, 15-round computation:
`endogenous_cycle_found: false`.  No declared strategy both fires,
clears every firing round, and avoids recurring imports.  The valued
strategy prevents demands instead of repairing fired ones.  For the
four depth-1 strategies the stated cores are horizon-free theorems;
for depth 2 the switch points (lengths 4 and 5) are Lean-verified and
the trajectory is computed to round 15. The structural fixed-depth
outrun is proved separately; the general-`n` sealed-profile interface
and the repair-strategy-class consequence remain open.

## FG7. The direct transposition fails

**[theorem]** (`middle_swap_not_relation_preserving`)  The direct
transposition of interior points 1 and 2 does not preserve the
successor relation.  This is enough to distinguish the example from
the earlier branch in which that swap is an admitted symmetry.  It is
not a quantified automorphism theorem and does not prove full rigidity
of the directed chain.  A complete invariance-versus-expressiveness
classification therefore remains open.

## FG8. What F5 now says

The conjecture split.  Its generation half is a theorem for the
declared composite: refusal
supplies the datum, closure supplies the demand, and after those
declarations no additional event is supplied per round. The composite
is self-continuing relative to the declared transition and closure
policy; it does not originate those declarations. Its cycle half is
not realized by any of the five
declared strategies through the 15-round search.  The theorem cores
explain the depth-1 fates, while the class-general cycle claim remains
open.  The bridge obligation left standing is G1: a repair channel
that separates the interior of an unbounded chain without minting
identity-grade distinctions, or a proof that no such channel exists.
Until one or the other arrives, the bounded evidence reads:
**endogenous demands, exogenous payments.**

`PresentationRelativity` supplies the conditional refinement mechanism
beneath this trade-off. If a supplied comparison `q` does not factor
through a presentation `p`,
`forced_split_of_factorization_failure` extracts a represented pair
identified by `p` and separated by `q`; every presentation carrying
both must split that pair and strictly increase represented class
count. `jointPresentation_strict_of_factorization_failure` constructs
one ordered-first-match joint refinement. In the generator fixture the
supplied comparison is `id`, hence identity-grade by declaration. The
theorem neither generates that comparison nor supplies the
non-identity repair channel required by G1.

`ClosureSymmetry` sharpens what this obstruction means without adding
a new agent. The `p` and `q` maps are internal faces of one attempted
closure. Every residual pair generates its transposition: `p` remains
invariant under that symmetry and `q` does not. Conversely, every such
represented invariance break is a residual and refutes factorization.
This identifies obstruction with failed closure under the attempt's
own symmetry; it does not generate `q`, authorize a repair, or close
G1.

---

# FRONTIER CONJECTURES

**G1. No non-identity repair channel (capacity conservation).**
*Conjecture:* in any class extending this one whose observables are
finitely many per declaration and depth-bounded, every strategy that
separates all interior pairs of arbitrarily long chains carries an
unbounded observable alphabet — i.e. is identity-grade — and therefore
kills generation.  The valued/per-pair routes realize the two ways of
paying (all at once / one at a time); G1 says there is no third way.

**G2. General depth-`d` outrun — CLOSED structurally; interface
residual OPEN.** `SeparationCapacity.depth_d_outrun` proves that all
deep-interior points share the declared radius-`d` `profileD`, and
`depth_d_obstruction` supplies a distinct colliding deep pair from
`n ≥ 2d + 3`. What remains OPEN is not this structural statement: it is
the general-`n` correspondence between sealed `Generator.profile2` and
`profileD · · 1` (only the `n = 4,5` instances are transported) and the
repair-strategy consequence named under G1.

**G3. Repair-power = generation-poison, class-general.**  *Conjecture:*
the F1 choice-cost conservation extends to demands: any declaration
strong enough to discharge every future separation demand is strong
enough to prevent every demand from arising.  In-class this is the
exclusion (FG6); the conjecture is its closure under new strategy
declarations.

**G4. The sealed engine is the import branch.**  *Conjecture:* feeding
the composite's obstruction stream to the first checkpoint's
augmentation engine (mark/link candidates, minimum responses)
instantiates the per-pair strategy — identifying the historical
engine's per-round supplies as the living branch of this trade-off
rather than an accident of its design.  A finite check away.

---

# Post-hoc comparison with existing names

*(End-only.)*

* The exclusion is a finite capacity bound of the familiar shape:
  separating `n` items needs enough distinguishable observables, and
  bounded-depth local views of a long path cannot tell deep interior
  positions apart — the same phenomenon as locality/quantifier-depth
  lower bounds on linear orders, here with the observation depth
  playing the quantifier-depth role.
* Valued automarking is ordinal labeling: making each element carry
  its own address.  That it kills generation is the observation that a
  totally ordered address space leaves nothing indiscernible — and
  costs exactly the identity structure the development refuses to
  presuppose.
* The generation/repair trade-off echoes productivity-versus-quiescence
  tensions in process theory: the demand stream stays live only while
  the system stays partially blind.
* The failed direct transposition and the local profile collapse point
  toward the standard distinction between automorphism invariance and
  bounded expressiveness.  Full directed-chain rigidity is not proved
  in this run.
* Relative to the sealed checkpoints: this run proves the generation
  half of F5, refutes its cycle half in the declared bounded class,
  proves that one direct transposition is not a symmetry, and names G1
  as the remaining bridge obligation.
