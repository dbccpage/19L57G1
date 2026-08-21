# Representative selection: what the engine already does, and where honesty stops

Classification: **analysis of already-certified results**, together with one
**unproved correspondence**, flagged as such throughout. No new derivation
run, no object-language notion, no new claim. `AuthorityEffect: None`.

Sibling to `paper/succession_declarations.md`,
`paper/candidate_measure_space.md`, and
`paper/computation_declarations.md`, which respectively itemize the five
declarations, show that measure refinement stops at a class, and record
that **C2** is unreachable by that mechanism. This page asks what the
remaining declaration — representative selection — actually is.

---

## 1. Thesis

The engine already implements **quotient succession**: from a regime class,
under a declared measure and the orbit policy, the set of child classes is
well defined and equivariant. Measure refinement stops at a class containing
two concrete deltas. The route to a single concrete successor identified
here is symmetry-breaking, whose correspondence to that pair is
**unproved** — and it is *not* claimed to be the only route, since
establishing that is precisely what the unproved correspondence would do.
Residual honesty therefore stops at refusing single-valued concrete
succession.

An earlier version of this thesis added that the obstruction "lives in a
**parked, axiom-unaudited** module". That is **WITHDRAWN**: the root now
imports `Derivation.Breaking` and reports every one of its exported
theorems, each depending on no axioms at all. The change narrows what is
missing rather than supplying it — the correspondence is exactly as
unproved as before, and it is now the *only* thing missing, which is a
sharper statement than the one it replaces.

---

## 2. What the engine already is

Not four postures of equal standing. One of them is a description of the
code.

**Response side.** `_quotient` groups minimum deltas by the isomorphism
class of the resulting regime and returns `(representative, class size)`:

```python
grouped.setdefault(canonical(child), []).append(delta)
return [(members[0], len(members)) for _, members in sorted(grouped.items())]
```

`members[0]` is a **reporting label**, not a chosen successor. What matters
is that `build_tree` then attaches *every* class as an edge:

```python
classes = _quotient(node.regime, target, mr)
for rep, size in classes:
    _attach(...)
```

At Challenge 3 under the item-count measure this yields 3 child edges in
reading L and 5 in reading F. The tree's answer to response-side
non-uniqueness is **retain all non-isomorphic minima**. That is not a
successor function; it is an explicit multi-successor relation at the
quotient level.

**Demand side.** `closure_challenge_orbits` is documented as

> one representative (least member) per automorphism orbit of the collapsed
> pairs, or the empty tuple at the fixpoint

The invariant part is the *set of orbits*: renaming carries orbits onto
orbits. The least member is bookkeeping — within an orbit every pair is
related by an automorphism, so the child isomorphism class does not depend
on which member is named. This policy **replaced** raw least-pair
selection, which was not equivariant; the regression test
`test_least_pair_selection_is_not_equivariant` records the defect, and
`test_orbit_policy_transition_congruence_exhaustive` the congruence.

Note the asymmetry. On the demand side, multiple orbits produce **one
challenge per orbit** — branching, not selection. In every exported family
`expansions_with_multiple_orbits` is 0, so that residual is latent rather
than exercised.

---

## 3. What remains between a class and a concrete successor

`paper/candidate_measure_space.md` §5: under the refined measure the unique
isomorphism class still contains **two concrete deltas** — mark either
member of the target pair — related by the transposition swapping that
pair. No refinement of the cost measure closes this. The measure delivers a
singleton *class*; a concrete successor needs one more declaration of a
different kind.

---

## 4. Three layers, with their evidence status kept apart

The obstruction has a shape already formalized here. Its standing must be
reported in three separate layers, because they have three different
evidential statuses.

**Layer 1 — proved and audited.** `lean4/Derivation/Minimality.lean`
declares into `namespace Derivation` and its theorems carry `#print axioms`
reports in `artifacts/lean_axioms.txt`, all within `{propext, Quot.sound}`:

| declaration | axioms |
|---|---|
| `Derivation.deltaU0_valid` | `propext, Quot.sound` |
| `Derivation.cost1_insufficient` | `propext` |
| `Derivation.cost1_insufficient_F` | `propext` |
| `Derivation.mu2_unique` | `propext, Quot.sound` |

with `deltaU0`, `deltaU1`, `swap01` and `isoU1U0 : Iso U1 U0` as
definitions. So the two concrete deltas and the transposition relating
their results are Lean objects, not merely enumeration output.

**Layer 2 — proved, and now AUDITED.** `lean4/Derivation/Breaking.lean`
proves, for a carrier with a fixed-point-free involution:

* `no_orbit_constant_equivariant_endomap` — given an inhabitant, no
  selector is both `OrbitConstant` and `Equivariant`;
* `imposable_but_not_equivariant` — a selector *can* be `Represents` and
  `OrbitConstant`, and fails exactly at `Equivariant`.

It also proves the obstruction in a form the involution shape cannot
reach:

* `no_orbit_constant_equivariant_selector` — the same conclusion for any
  family of transformations with **no common fixed point**. No involution
  law, no group law, no identity, no inverses, no composition. `ofBreak`
  exhibits `Break` as the one-symbol case, so the general result subsumes
  the involution one rather than sitting beside it.
* `no_fixed_point_free_involution_on_Tri` — **why the generalization is
  not cosmetic.** The three-point carrier admits no fixed-point-free
  involution at all, so `Break` cannot be instantiated over it while
  `Symmetry` can. An earlier version of this bullet explained that by
  the general fact — a fixed-point-free involution pairs its carrier
  into two-cycles, so every finite `Break` carrier has even cardinality.
  That general statement is **not proved anywhere in this repository**;
  it is WITHDRAWN as an assertion and left OPEN. What is proved is the
  three-point case, and only it is cited here.
* `selector_exists_at_common_fixed_point` — the hypothesis is spent, not
  decorative: where a point IS fixed by every symbol, the constant
  selector at it is both orbit-constant and equivariant.
* `no_selector_of_no_common_fixed_point` — the obstruction under the
  **weakest** premise it actually spends: not that every point is moved
  by some symbol, but only that no point is fixed by every symbol.
  `no_common_fixed_point` derives that premise from `Symmetry`'s field,
  in that direction only; the converse needs a decidability this
  development does not assume.
* `selector_iff_common_fixed_point` — **the exact characterization.**
  Given an inhabitant, an orbit-constant equivariant selector exists
  *precisely* when some point is fixed by every symbol. Both directions
  are proved, so what the obstruction costs is now stated rather than
  asserted. An earlier version of this page said `Symmetry`'s field was
  "exactly what the obstruction costs"; that was WITHDRAWN when the
  field turned out to be sufficient but stronger than needed.

An earlier version of this paragraph said the module is **parked** — that
it elaborated under the per-module gate while the root did not import it,
so it emitted no `#print axioms` report and no gate inspected its axiom
surface. **That is WITHDRAWN.** The root now imports it and reports all
seven exported theorems, each of which *does not depend on any axioms* at
all. The parked-module residual is closed for this module and remains
open for the others; closing it here is not evidence about them.

What has NOT changed is the ceiling:

> It proves nothing about `DiffObs`, `PresIso`, `NonZeroPair`, or any
> other structure in this repository. No bridge is proved.

**Layer 3 — unproved.** That `{deltaU0, deltaU1}` (or `{U0, U1}` under
`Iso`) is a `Break`-model in the sense that makes Layer 2 apply to
selecting among those deltas. The shape matches — a two-element carrier
with a fixed-point-free involution — but **no bridge theorem exists**, and
none is asserted here.

If Layer 3 held, then "break the symmetry by reading something that is not
isomorphism-invariant" would not be one option among several. It would be
the **only** branch remaining once a single concrete orbit-constant
representative is demanded, and equivariance would be the price. That
conditional is stated, not discharged.

### Which tie the obstruction reaches, and which it does not

The obstruction bites **within** a tie class and **not across** classes.
The distinction is easy to lose and worth stating in one place, because
losing it converts a narrow result into a false one.

*Across* the tied classes there is no symmetry to obstruct. The three
reading-L classes and five reading-F classes are separated by an
**isomorphism invariant** — `U0_not_iso_BL`, `U0_not_iso_BD`,
`BL_not_iso_BD`, and `markK_pairwise_noniso` for the arity family — so an
equivariant rule is permitted to read what distinguishes them. It is not
merely permitted in principle: `mu2` is presentation-independent and
selects uniquely, grammar-wide (`mu2_unique`, `mu2_unique_F`). Any claim
that no invariant rule can break the Challenge-3 tie is therefore
**refuted by a theorem already in this repository**.

An earlier version added a parity remark said to reinforce it: that a
fixed-point-free involution pairs its carrier into two-cycles, so a
finite `Break` carrier has even cardinality, and since three and five
are odd, `Break` could not be instantiated on the tie sets at any choice
of involution. **That is WITHDRAWN.** No theorem in this repository
proves the general even-cardinality statement; only the three-point case
is proved (`no_fixed_point_free_involution_on_Tri`), and the five-element
reading-F tie set was never covered by it at all. The remark is removed
rather than repaired, because the paragraph above does not need it: the
tie is already refuted by `mu2_unique` and `mu2_unique_F`, which are
proved.

*Within* a class the symmetry is real. Each class contains exactly two
concrete deltas, exchanged by the transposition of the required pair
(`swap01`, `swap12`, with `isoU1U0` and `isoU2F_U0F` collapsing them).
That two-element orbit is the shape `Break` describes, and it is exactly
what Layer 3 would have to package. The obstruction, if bridged, says
that choosing one of the two concrete presentations cannot be done
equivariantly — a claim about presentation, not about which minimal
response the mathematics prefers.

Both readings can be true at once, and only one of them is a claim about
what the system forces.

---

## 5. The parked residual, and the price that was paid

`CLAUDE.md` records **elaboration is not auditing** as an open residual: a
module the root does not import is typechecked but contributes no axiom
report. For most of this page's life that was a recorded limitation with
no consequence.

Here it acquired one, and the consequence is what forced the repair. The
single theorem this analysis would most want to lean on — the
orbit-constant/equivariant obstruction — was precisely the theorem no gate
inspected. The substrate (Layer 1) was audited; the obstruction (Layer 2)
was not; the link (Layer 3) did not exist.

**Layer 2 is now audited.** The root imports `Derivation.Breaking`, and
each of its seven exported theorems has a `#print axioms` report inside
the whitelist — in fact inside nothing at all, since every report reads
*does not depend on any axioms*. An earlier version of this section
described the unaudited state in the present tense throughout; those
sentences are moved to the past above rather than deleted, because the
ordering they record is still the finding.

Two things did **not** change, and conflating them with the repair would
be the error this page exists to avoid:

* **Layer 3 still does not exist.** No proof connects `Break` or
  `Symmetry` to the tied delta pair. Auditing Layer 2 makes the
  obstruction citable; it does not make it *applicable* here.
* **The residual is closed for one module, not in general.** Every other
  module the root does not import is still typechecked and still
  unaudited. The general fix — a declaration census for parked modules —
  is untouched, and `CLAUDE.md` records why the obvious regex approach is
  the one already known to break.

So this page still argues from the code and from Layer 1, and cites Layer
2 rather than resting on it. What changed is that the citation is now to
audited theorems; what did not change is that the bridge is missing.

---

## 6. Where this stops

**Refuse single-valued concrete succession.** Keep the quotient transition
as the derived object: from a regime class, under a declared measure and
the orbit policy, the set of child classes is well defined and equivariant.
Concrete deltas on the edges are witnesses, not the identity of the next
state.

That is not a gap awaiting closure. On present evidence it is what the
system supplies, and the further step to one concrete successor is a
declaration the system does not make.

Three routes to that step are visible here: branching, a quotient-valued
next state, or a presentation-dependent or external tie-break. **They are
not claimed exhaustive.** An earlier version of this sentence said the step
was "obtainable *only*" by those three; that word is WITHDRAWN. Their
exhaustiveness is exactly what Layer 2 would establish — and Layer 2
applies to this pair only if the Layer 3 correspondence holds, which is
unproved. Asserting "only" here would have spent the obstruction result
while §4 was still quoting it.

This sentence previously gave a second reason: that Layer 2 was "parked
and axiom-unaudited". That reason is **withdrawn as obsolete** — it is
audited now (§5) — and the withdrawal changes nothing, because the first
reason was always the load-bearing one. An audited theorem about a
structure nobody has connected to the delta pair is exactly as unusable
here as an unaudited one.

---

## 7. Bearing on the scoped opens

| open | stance here |
|---|---|
| (1) for a measure that does not force uniqueness, is every presentation-independent *selection rule* multivalued at the minimum? | **Untouched.** No selection rule has been enumerated anywhere; the size of a minimum *set* is not a theorem about every rule. |
| (2) independently of measure choice? | Answered only inside `M_slice`, and only as two independent behaviours. Not reopened here. |

Structurally, and keeping the conditional: a successive-state model that
requires *one* next configuration must be performing symmetry-breaking
under some name — and **if** the Layer 3 correspondence holds, that costs
equivariance. The **if** is not discharged.

---

## 8. What this does NOT claim

* It does **not** prove the Layer 3 bridge, and does not assert the delta
  pair is a `Break`-model.
* It does **not** claim the audited status of `Breaking.lean` makes its
  theorems applicable to the delta pair. An earlier version of this
  bullet said the page does not un-park the module and that any such
  import "would be a deliberate, separately reviewed change with its own
  axiom audit — not something that rides in on a green elaboration gate."
  The import has since happened, on exactly those terms: deliberate, with
  seven `#print axioms` reports and a pinned axiom artifact. The bullet
  is **WITHDRAWN as a description of the tree** and kept as the standard
  the change was held to.
* It does **not** claim `Break` is forced. It is a declared shape.
* It does **not** claim the routes to a concrete successor listed in §6 are
  **exhaustive**. Two earlier sentences said "only" — in the thesis and in
  §6 — and both are WITHDRAWN. Exhaustiveness is what Layer 2 would
  establish, and Layer 2 reaches this pair only through the unproved
  Layer 3 correspondence. Spending it while §4 still quotes it would be
  the promotion this page exists to avoid. (This bullet also described
  Layer 2 as "parked, axiom-unaudited"; that clause is obsolete per §5
  and is dropped. The unproved correspondence is what carries the point.)
* It does **not** claim single-valued succession is impossible in every
  account. It claims this system does not supply it and that measure
  refinement cannot manufacture it.
* It does **not** identify `_quotient`'s `members[0]` with a `Selector` in
  the `Break` sense; that identification would need definitions not present.
* It does **not** enumerate selection rules, add a selector to the engine,
  the ledger, or CI, or name or refute any external model.
* It introduces no counting, magnitude, observer, container, or clock.
