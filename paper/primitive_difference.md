# Primitive Difference

**Goal.** Derive the weakest defensible formal object that can be called
*Primitive Difference* before contexts, profiles, observers, quotients, or
repairs are available.  The regime model of `paper/paper.md` is **not**
assumed anywhere in the constructive part; it reappears only in the final
comparison, as one realization among others.

**Protocol.** Constructive derivation first, blind to imported
frameworks; comparisons with existing names appear only in the final
section.  Every theorem cited by name is machine-checked in
`lean4/Derivation/PrimDiff.lean` (Lean 4 core, no external libraries; the
namespace imports nothing from the regime model).  Every finite search and
countermodel is deterministic Python
(`code/derivation/primdiff.py`, artifact `artifacts/primdiff.json`),
exhaustive over declared scopes, covered by the repository's 95%/95%
test gates and CI.

Statement tags as in the companion paper: **[declared metatheory]**,
**[definition]**, **[finite computation]**, **[theorem]**,
**[bounded theorem]**, **[conjecture]**, **[counterexample]**,
**[unresolved]**.

---

# FORMAL SPINE

## S1. Candidates and their exact assumptions

Five candidate readings of "a and b are primitively different".  Each is
given with its *exact* metatheory bill.

**A1 — positive apartness datum.**
*Metatheory:* a type (carrier), one binary relation symbol, the ability to
assert one instance.  Nothing else — no axioms, no identity relation of
the object language, no negation.
*Object definition:* a pointed structure `(X, r, a, b)` with the single
asserted fact `r a b`.

**A2 — witnessed non-identification.**
*Metatheory:* as A1, plus witness *multiplicity* (a count or token store
per ordered pair).
*Object definition:* `(X, W : X → X → Nat, a, b)` with `0 < W a b`.  The
induced *presence* relation is `x # y :≡ 0 < W x y`.

**A3 — non-factorization through collapse.**
*Metatheory:* strictly more than A1 — function types, composition, and a
one-point carrier.  This candidate is not expressible in A1's bill.
*Object definition:* the selection of `a, b` does not factor through the
point: there is no `p : 1 → X` with `p(*) = a` and `p(*) = b`.
**[theorem]** (`factors_through_point_iff`) Non-factorization is
*definitionally* metatheoretic inequality `a ≠ b` once functions are
admitted.  A3 is therefore not a primitive: it is the metatheory's own
identity, re-expressed.

**A4 — irreducibility under an admitted operation family.**
*Metatheory:* as A3, plus a declared family `F` of endomaps and closure
under identity and composition (`Clos`).
*Object definition:* `Irred F a b :≡ ∀ f ∈ Clos F, f a ≠ f b`.

**A5 — an initial/minimum carrier for one witnessed distinction.**
*Metatheory:* as A1, plus a chosen two-element carrier.
*Object definitions:* the **oriented** two-element difference
`D2 = ({0,1}, {(0,1)}, 0, 1)` and the **symmetric** one
`S2 = ({0,1}, {(0,1),(1,0)}, 0, 1)`.  Both are retained as branches
(section S6).

One further axiom is studied as the minimal *fidelity commitment*:

**Irreflexivity** `Irrefl r :≡ ∀ x, ¬ r x x` — the weakest object-level
axiom found that gives an asserted difference any consequence at all
(S3, S5).

## S2. Implications and non-implications

**[theorem]** (Lean, each machine-checked)

| implication | status | evidence |
|---|---|---|
| A1i → A1 | holds | definitional |
| A1i → A3 | holds | `irrefl_witness_ne` |
| A1i → A4(∅) | holds | `irrefl_witness_ne` + `irred_empty_iff_ne` |
| A3 ↔ A4(∅) | holds | `irred_empty_iff_ne`, `clos_empty_id` |
| A1 → A3 | **fails** | `selfdiff_consistent`: the one-point self-difference `({*}, r(*,*), *, *)` |
| A3 → A1 | **fails** | `meta_diff_without_assertion`: empty relation on two points |
| A1 → A1i | **fails** | same self-difference countermodel |
| symmetry restores A1 → A3 | **fails** | `symm_selfdiff_consistent` |
| A3 → A4(F), F ∋ a merger | **fails** | `merger_erases` |
| A4 antitone in F | holds | `irred_antitone` |

**[finite computation]** (`artifacts/primdiff.json`,
`implication_matrix`, scope: *all* pointed structures with carrier ≤ 3 —
36 ordered implication cells).  Predicate extents: A1 holds in 2,337
structures, A1i in 196, A3 and A4(∅) in exactly the same 3,104 (the
equivalence is extensionally exact within scope).  The non-vacuous
implications that survive are precisely the five theorems above; the 15
failures each carry a recorded countermodel.  `A4` at any sampled family
containing a merger of the designated pair (the merge map itself, or all
constants) has **empty extent**: difference relative to such a family is
the empty notion — the matrix flags these rows as vacuous rather than
letting them masquerade as implications.

**Reading.** Asserted difference (A1/A2) and metatheoretic distinctness
(A3/A4) are *orthogonal*: neither implies the other.  The unique studied
axiom that ties them is irreflexivity.  A4 shows difference is
family-relative all the way down: `F = ∅` collapses it onto the
metatheory's identity, one admitted merger annihilates it.

## S3. Collision versus obstruction (the fidelity dichotomy, stated
precisely)

Collapse of a pair is a *map* `c` with `c a = c b`; the collapsed
structure is the pushforward relation `Push r c`.  Two notions are kept
separate:

* **Collision** — `CollapseCollision r c :≡ ∃ u v, r u v ∧ c u = c v`:
  some asserted edge has both endpoints identified.  Positive (an
  existence), and *prior to any law*.
* **Obstruction** — `FidelityObstruction P r c :≡ CollapseCollision r c ∧
  ¬ P (Push r c)`: a collision **together with** a protected law `P`
  that the pushforward violates.  Obstruction is always relative to the
  protected property.

**[theorem]** (`collision_of_identifying_witness`) Identifying a
witnessed pair *always* produces a collision — with or without any
fidelity commitment.

**[theorem]** (`bare_collapse_admissible`, `push_witness`,
`collapse_unobstructed_without_fidelity`) **Bare A1: the collision
exists, and the collapse remains admissible.**  The pushforward still
carries the asserted pair, and self-relations are allowed in the bare
signature — the collapsed one-point self-difference is a legitimate
structure.

**[theorem]** (`obstruction_under_irrefl`, via `collision_not_irrefl`)
**A1 + Irrefl: the same collision now violates the protected law** — the
pushforward is not irreflexive, so collapse of a witnessed pair is
obstructed *relative to preservation of `Irrefl`*.

**Answer to the posed question, scoped:** relative to preservation of
`Irrefl`, collapse of a witnessed pair is obstructed; among the three
axiom choices studied (none, symmetry, irreflexivity), only
irreflexivity produces the required soundness transfer.  The collision
itself is unconditional; what the fidelity commitment adds is exactly
the protected law that turns the collision into an obstruction.

**[finite computation]** (`collapse` in the artifact) — verified
exhaustively over every pointed structure and every merge with carrier
≤ 3: collision ⟺ pushforward not irreflexive; identifying a witnessed
pair always collides; pushforward always exists.

## S4. Orientation, obstruction-blindness, and what an observer adds

**[theorem]** (`collision_transpose_invariant`) Collapse collision is
invariant under transposing the relation: **the collision level sees
only the symmetrization of a difference.**

**[theorem]** (`orientation_data_invisible_to_collapse`,
`D2_S2_collapse_equiv`) Yet orientation is real data: the oriented edge
`D2` and its reverse are not pointed-isomorphic, `D2` and `S2` are not
pointed-isomorphic (`D2_not_pointed_iso_S2`) — while `D2` and `S2` have
*identical* collision behavior for every collapse map.

**[theorem]** (`symmetric_no_equivariant_classifier`,
`swap_is_S2_automorphism`) On the symmetric two-element difference, the
swap is an automorphism, and every swap-equivariant `Bool`-valued
classifier is constant: **`S2` admits no automorphism-invariant
separating Boolean classifier.**  (Scope: this concerns invariant
separating classifiers into `Bool`; equivariant maps into targets
carrying a nontrivial action are not excluded and were not studied.)

**[theorem]** (`oriented_rigid`, `oriented_classifier_exists`) `D2`'s
orientation cuts the automorphism group to the identity, and an
invariant separating Boolean classifier exists.

**[finite computation]** (`observer` in the artifact) `D2`: 1 unpointed
automorphism, 2 invariant separating Boolean classifiers.  `S2`: 2
automorphisms, 0 such classifiers.

**Answer to the posed question, scoped:** orientation is **the minimum
symmetry-breaking data needed for the specific invariant Boolean
classifier studied here**.  It permits classification; it does not
canonically name the outputs — the two output labels remain externally
interchangeable.  What the symmetric object lacks is exactly this
symmetry-breaking choice; everything further an observer provides in
richer settings (reusable tests, comparison across pairs, profiles)
requires carriers and function spaces this layer does not have.

## S5. The two-element question, answered four ways

For the question "is a two-element carrier forced, initial, merely
sufficient, or false?":

* **Forced** — **[theorem]** with irreflexivity:
  `no_witness_on_subsingleton` (no witnessed pair lives on a subsingleton
  carrier), so carrier ≥ 2 and two elements are attained.
* **False as a necessity** without irreflexivity — **[theorem]**
  `one_point_hosts_bare_witness`: the one-point self-difference hosts a
  bare A1 witness.
* **Initial** — **[theorem]** `D2_initial_pointed`: for every witnessed
  structure there is exactly one point-preserving map from `D2`, and it
  preserves the oriented edge.  **[finite computation]**: verified
  brute-force for all 2,337 witnessed pointed structures with carrier
  ≤ 3 (unique map in every case).
* **Merely sufficient, not exhaustive** — **[theorem]**
  `witnessed_irrefl_on_every_larger_carrier`: for every `n`, a witnessed
  irreflexive structure exists on the carrier `Fin (n + 2)` — every
  carrier size ≥ 2 hosts one.

Minimal carriers by axiom set (**[finite computation]**): bare — 1;
irreflexive — 2; irreflexive+symmetric — 2.

## S6. The six posed investigations

1. **Retention: primitive or derived?**  In this layer there is no state
   and no history: the difference object is a timeless tuple.  Retention
   is not expressible, hence neither primitive nor derived *here*; it is
   an apparatus of history-bearing metatheories.  **[declared
   metatheory]** Any retention discipline is a declared rule about
   histories, not a consequence of the difference object (the companion
   development's admission histories are one such declaration).
2. **Are two witnesses forced?**  No.  **[theorem]**
   (`single_oriented_witness_consistent`) One witness for one orientation,
   none for the reverse, is consistent; a second same-orientation witness
   is likewise unforced.  Scope of the multiplicity result, stated
   precisely: **[theorem]** (`multiplicity_invisible_to_presence`)
   *after truncation to the induced presence relation*, multiplicity adds
   no new carrier-pair separations — it still distinguishes witness
   structures from one another (the two assignments in the theorem are
   unequal as structures while presence-equal).
3. **Does repetition create identity or only another occurrence?**  Only
   another occurrence.  **[theorem]** (`repetition_no_new_content`)
   re-asserting a present pair changes nothing at the membership level;
   **[theorem]** (`repetition_new_occurrence`) the occurrence count still
   grows.  No judgment identifying occurrences exists in the signature,
   so repetition cannot create identity — identity of occurrences is
   metatheoretic position, not object content.
4. **Must a faithful presentation preserve the distinction?**
   "Faithful" *means* pair-preserving here; the substantive fact is that
   unfaithful presentations exist and are cheap: **[theorem]**
   (`const_presentation_unfaithful`) every constant presentation into an
   irreflexive target loses every asserted pair, while the identity is
   faithful (`id_presentation_faithful`).  Fidelity of presentations is
   therefore a demand one must impose, never a fact one gets free.
5. **Does collapse create obstruction without an external fidelity
   demand?**  Exactly when irreflexivity is admitted — the dichotomy of
   S3.  The demand can be internalized as one axiom, and that axiom is
   the entire difference between inert assertion and obstructive
   difference.
6. **Does any endogenous next challenge follow?**  No.  The object is a
   static tuple with no admitted dynamics; every continuation (extend the
   carrier, add witnesses, demand separations, observe) is an external
   act.  This reproduces, one layer down, the companion development's
   finding: continuation policies are declared, not derived.

## S7. Strongest defensible Primitive Difference object

**Terminal statement, scoped.**  Within the **studied pointed
one-relation signature** (types, one binary relation, finite case
analysis; axiom comparison restricted to {no axiom, symmetry,
irreflexivity} — the wider axiom lattice is an open obligation, S9):

> **The strongest currently defensible minimal candidate for Primitive
> Difference is a witnessed irreflexive relation.  Its two-element
> realizations are exactly `D2` and `S2`
> (**[theorem]** `bool_irrefl_witness_classification`: every decidable
> irreflexive relation on the two-element carrier asserting the
> designated pair equals `D2` or equals `S2`), and these are
> non-isomorphic (**[theorem]** `D2_not_pointed_iso_S2`) yet have
> identical collapse-collision behavior (**[theorem]**
> `D2_S2_collapse_equiv`).**
>
> * Bare assertion (A1) is *not* defensible as difference: it is
>   consistent with the two points being one point and supports no
>   soundness transfer (**[counterexample]** `selfdiff_consistent`);
>   its collisions never rise to obstruction (S3).
> * Metatheoretic inequality (A3 ≡ A4(∅)) is *not* primitive: it is the
>   metatheory's identity re-expressed through function composition
>   (**[theorem]** `factors_through_point_iff`,
>   `irred_empty_iff_ne`) and carries no object-level witness
>   (**[counterexample]** `meta_diff_without_assertion`).
> * Among the three axiom choices studied, irreflexivity is the unique
>   one converting assertion into consequence: it forces metatheoretic
>   distinctness (**[theorem]** `irrefl_witness_ne`), forces the
>   two-element carrier (**[theorem]** `no_witness_on_subsingleton`),
>   and turns the unconditional collision into an obstruction relative
>   to preservation of `Irrefl` (**[theorem]**
>   `obstruction_under_irrefl`).
> * `D2` is initial among all pointed witnessed structures
>   (**[theorem]** `D2_initial_pointed`) and carries an
>   automorphism-invariant separating Boolean classifier
>   (**[theorem]** `oriented_classifier_exists`); `S2` admits none
>   (**[theorem]** `symmetric_no_equivariant_classifier`).
>
> The branch between `D2` and `S2` is retained: orientation is the
> minimum symmetry-breaking data for the invariant Boolean classifier
> studied here, and nothing at this layer selects between carrying it
> primitively (`D2`) or adding it later (`S2` + choice).

## S8. Countermodel index

| countermodel | refutes | where |
|---|---|---|
| one-point self-difference `({*}, {(*,*)})` | A1→A3, A1→A1i, "assertion has consequences" | `selfdiff_consistent`; artifact `A1->A3` |
| its symmetric reading | "symmetry restores soundness" | `symm_selfdiff_consistent` |
| empty relation on two points | A3→A1 | `meta_diff_without_assertion`; artifact `A3->A1` |
| merge map on the designated pair | A3→A4(F), nonempty families | `merger_erases`; artifact vacuous-extent flags |
| oriented edge vs its reverse | "obstruction profiles classify" | `orientation_data_invisible_to_collapse`; artifact `frontier_profile_countermodel` |
| one-witness model | "two witnesses forced" | `single_oriented_witness_consistent` |
| multiplicities 1 vs 2 | "witness data adds distinctions" | `multiplicity_invisible_to_presence` |
| constant presentation | "presentations preserve distinctions" | `const_presentation_unfaithful` |

## S9. Unresolved obligations

* **[unresolved]** Weakest-axiom claim beyond the studied set: only
  {no axiom, symmetry, irreflexivity} were compared.  A complete lattice
  of one-variable/two-variable Horn axioms over one relation, with the
  soundness-transfer property characterized, is open (finite search is
  feasible; see F3).
* **[unresolved]** The initiality of `D2` is proved for point-preserving
  morphisms; a characterization of *all* edge-preserving morphism classes
  under which some two-element object remains initial is open.
* **[unresolved]** A2 with witness *types* (proof-relevant witnesses with
  their own identity) rather than counts: whether any witness-level
  structure ever becomes observable below function spaces.
* **[bounded theorem]** All finite-search results are exhaustive only for
  carrier ≤ 3 (matrix, initiality echo, collapse verification) and k ≤ 6
  (carrier tables); the Lean theorems where cited are carrier-general.
* **[unresolved]** Lean formalization of the finite-scope matrix itself
  (the countermodels are formalized; the exhaustiveness of the scope
  sweep lives in Python only).
* **[unresolved — the next bridge, deliberately left open]** Whether the
  opaque inscription of the companion development can be *elaborated
  into* a witnessed irreflexive datum, or which of its ingredients must
  be externally admitted.  The provenance of each ingredient — carrier,
  two designated occurrences, relation, witness, irreflexivity,
  orientation — is untested here: this paper characterizes a strong
  candidate once those ingredients exist; it does not derive them from
  the inscription, and the gap must not be silently filled by the
  metatheory.

---

# FRONTIER CONJECTURES

*Nothing in this section is promoted to theorem; each item is a live
construction or conjecture with its current evidence stated.*

**F1. The forgetting tower (witness → assertion → obstruction).**  This
investigation exhibited two forgetful steps that each lose exactly one
kind of data: multiplicity → presence (`multiplicity_invisible_to_
presence`) and orientation → collision
(`collision_transpose_invariant`, `D2_S2_collapse_equiv`).
*Conjecture:* these are the first rungs of a tower of "difference
shadows" — witness structures over pairs of witness structures
(differences *between* differences) whose forgetful maps lose
multiplicity, then orientation, then adjacency of higher cells.  The
two-element analysis suggests each rung has its own initial object and
its own orientation gap.  Evidence: the two proved rungs; nothing above
them yet.

**F2. Occurrence bookkeeping as proto-quantity.**  Repetition creates
occurrences, never identity (S6.3).  The minimal structure that can even
*ask* whether two occurrences are "the same event" is a successor-like
pointer chain over assertions.  *Proposed next mathematics:* derive the
weakest occurrence-tracking object by the same method (candidates,
implications, countermodels) and test whether numerals are its initial
realization — i.e., whether counting is the primitive-difference analysis
of *time* rather than of *space*.

**F3. The fidelity lattice.**  Irreflexivity was the unique
soundness-transferring axiom among the three studied.  *Conjecture:* in
the full finite lattice of universally quantified one-relation axioms,
the soundness-transferring ones form a filter generated by
irreflexivity — i.e., every axiom that makes assertion sound *contains*
irreflexivity's content.  Finite search over small axiom shapes is
feasible with the existing enumerator; not yet run.

**F4. Collision calculus.**  Collapse-collision profiles are computable,
orientation-blind, and fail to classify (S4, S8).  *Conjecture:*
collision profiles classify pointed structures exactly up to
symmetrization and witness-multiplicity — the "collapse shadow" is a
complete invariant of the symmetrized presence relation and nothing
more.  Evidence: true on carrier 2 by the frontier countermodel;
untested above.

**F5. Demand composition.**  Fidelity entered as a single axiom;
presentations showed fidelity is a per-map demand (S6.4).  *Conjecture:*
demands compose associatively (preserve-this-pair demands under map
composition form a monoid action on presentations), and the persistent
requirement discipline of richer layers is the free such action.  This
would make "repair" the closure of one demand under composition —
a candidate origin story for requirement persistence, currently
unproved.

**F6. Where towers could start.**  Three independent tower seeds emerged:
orientation-breaking (F1), occurrence-counting (F2), and demand
composition (F5).  *Conjecture:* they are independent in the strong
sense that no one of them is definable from the other two at this layer —
suggesting the next layer up has at least a three-parameter family of
minimal extensions, not a single canonical successor.  This matches the
tie-retention phenomenology of the companion development (measure-relative
minimality) one level down.

---

# Post-hoc comparison with existing names

*(Comparison authorized at the end only; nothing above depended on it.)*

* **A1/A1i vs constructive apartness.**  A1i is a pointed, inhabited
  fragment of an apartness relation in the sense of constructive
  mathematics (Bishop-style): irreflexivity is kept, but symmetry and
  cotransitivity are *not* forced — both would be further optional axioms
  (symmetry was analyzed; cotransitivity was not needed by anything).
  Primitive Difference is thus strictly weaker than apartness.
* **A2 vs proof relevance.**  Witness multiplicity is a
  Brouwer–Heyting–Kolmogorov-flavored refinement; the result that
  multiplicity is invisible to presence is the finite shadow of the
  distinction between propositional truncation and untruncated data.
* **A3/A4 vs categorical separation.**  Non-factorization through the
  point and irreducibility under endomap families are element-free
  reformulations of inequality; the finding that they re-express the
  metatheory's identity parallels the fact that "monomorphism from 2"
  presupposes the ambient category's equality.
* **D2 vs S2 vs quivers and graphs.**  The oriented/symmetric branch is
  the single-edge case of the quiver-versus-graph distinction; the
  obstruction-blindness theorem says collapse semantics factor through
  the underlying graph of the quiver.
* **Orientation as observer vs pointed classifiers.**  The self-observing
  oriented object echoes the role of a two-point classifier with a
  distinguished point (Sierpinski-style asymmetry): the observer content
  of orientation is the choice of "open point".
* **Relation to the companion regime model** (`paper/paper.md`).  The
  regime model was *not* assumed, and it is not the answer: its
  separability is profile-based and symmetric, so by the
  orientation-blindness theorem it lives at the **obstruction level** of
  the tower — strictly above `D2`, whose orientation data the regime
  model cannot see.  Its unary-mark minimal augmentation is the
  observer/orientation step performed with context machinery; its
  requirement persistence is a declared fidelity demand, exactly as the
  dichotomy of S3 predicts for any layer that wants collapse to be
  obstructive.  Primitive Difference sits below it as the two-object
  germ: `D2` (assertion + fidelity + orientation) is what remains of a
  regime when contexts, profiles, and histories are stripped away.
