# Frontier Run 006 — Refusal, Reflection, and the Remaining Bridge

**Mission.**  Determine whether repeated presentation or attempted
re-admission of one opaque token can generate the missing two-ness or
witnessed difference without importing a second token, hidden occurrence
identity, undeclared time/order, or an already two-valued result
algebra.  Central question: can an internalized refusal/non-change
create Primitive Difference, or does every such construction merely move
the external import into a result constructor, history position, second
sort, or reflective rule?

## TERMINAL

```text
FREE_REFUSAL_BRIDGE_FAILS
UNIQUE_MINIMUM_WITNESSED_BRIDGE_IN_CLASS
MULTIPLE_MINIMUM_WEAKER_BRIDGES
```

The terminal is split by target because the minima are target-relative
— the run's central structural finding (per-verdict correction of the
earlier single-line `MULTIPLE_MINIMUM_BRIDGES`, which conflated three
bridge targets):

| target | minimum result in the declared 44-protocol class |
|---|---|
| two carrier elements | three tied routes under order A (second token / occurrence / reification); order B selects occurrence |
| separable / oriented pair | two tied routes under order A (reification + tag, reification + relation); order B selects the tag route |
| witnessed relation | **one** minimum route, the same under **both** orders: reification + automatic relation |
| witnessed irreflexive fact | **one** minimum route, identical to the above |
| irreflexivity as a law | not reached; separately declared |

The free fragment reaches nothing (refusal per se fails).  The weaker
milestones have multiple tied minima with order-dependent winners.  The
witnessed milestones have a **unique minimum bridge** — datum retention
+ the relation rule, no tag, singleton algebra, one token — now also
verified in Lean (`min_witnessed_route_closes`).  Every construction
that succeeds moves the import into a result constructor, a tag
observable, a relation rule, a reification/occurrence rule, or a second
token — nothing arrives from the token itself.

The run's stratification, with each strict step separately evidenced:

```text
history difference < state difference < carrier two-ness <
carrier separability < witnessed relation < protected irreflexivity law
```

(histories collapse to one state, `histories_collapse`; judgments
change state without carrier growth, `judgment_carrier_bound`; the
occurrence pair is two-but-collapsed, `two_carrier ↛ separable_pair`;
the tag route separates without any relation, `separable_pair ↛
witnessed_relation`; facts never entail the law,
`bridge_facts_not_law`).  These layers do not collapse into one another
for free: each step has its own non-empty, target-specific price.

* **Proved** (Lean, 20 new theorems): silent-refusal inertia
  horizon-free (T1); result streams never feed back — trace/object
  separation (T2); the constructor-channel dependency core (T3); the
  judgment variant's carrier bound (T4); a sufficient priced bridge and
  its orientation, plus the *unique minimum* witnessed route with no
  tag store and no result store even present in the state
  (`min_witnessed_route_closes`) (T5); facts-not-law carried over (T6);
  the invariance ceiling in fully general form (T7); reflective
  dynamics — fixpoint, two-cycle, and horizon-free chain growth: the
  declared reflective semantics realizes a chain whose carrier is
  literally `range (n+1)` and whose relation is literally successor
  (T8).
* **Computed only within bounds** (44 protocols, 6-event horizon,
  carrier cap 4): the nine-state-level-notion matrix (13 of 72
  non-reflexive implications hold, countermodels for the rest), the
  minimum-price table with all ties — unique witnessed minimum under
  both orders, multiple order-dependent minima at the weaker milestones
  — the target-relative dependency checks, and the in-class structural
  fact that every refusal link is born off-diagonal.
* **Refuted**: that refusal per se is a new difference source (the
  untagged reification is occurrence admission — checkpoint PR #6 —
  and the free fragment reaches nothing); that carrier separability can
  arrive without a tag or relation import, or result-outcome
  distinction without the binary algebra (target-relative dependencies,
  zero exceptions in class); that a single cheapest bridge exists *at
  the weaker milestones* (the cost orders disagree there; at the
  witnessed milestones the minimum is unique and order-independent).
* **Imported, explicitly, by the successful routes**: receipt
  reification (coproduct into the carrier) or occurrence identity or a
  second token, for two-ness; a tag observable or a relation rule + its
  witness, for separability; the irreflexivity law, always separately.
* **Open**: the general invariance ceiling with structural hypotheses
  (T7's general lemma is proved; identifying invariant substructures
  beyond the two-element case is not); a Lean-general T10 over an
  abstract protocol grammar; typed refusals (F3 below); chain
  initiality (F4 below).
* **Single best next theorem target**: the class-general provenance
  normal form in Lean — a protocol-grammar-level theorem with
  target-relative conclusions (separable pairs pull back to the tag or
  relation channel; result distinctions to the constructor channel;
  witnessed relations to the relation channel), with the finite
  search's 44 instances as its decidable shadow.

---

# FORMAL SPINE

## FR1. The protocol space (exact definitions)

**[declared metatheory]**  A protocol is
`(algebra, retention, tagging, reflection, autorel, tokens)` with:
result algebra of 1 or 2 constructors (`New`; optionally `Refused`);
retention of refusal results as `none` / `judgment` / `occurrence`
(re-append the token; position identity is a flagged metatheoretic
import) / `datum` (reify a receipt into the carrier); optional tag
(built-in unary observable on receipts); optional reflection (receipts
presentable); optional autorel (reification also asserts a relation
instance subject → receipt); one token or the two-token control.
Constraints: tag/reflection/autorel require datum retention.  44 valid
protocols; events are `Present(token)` and, where enabled, `Reflect`.
This is a *search space*, not a curated list.

The run's non-negotiable distinctions are honored structurally: results
are host values unless a retention rule internalizes them; receipts are
carrier data only under `datum`; judgments are a separate store; the
trace is never object data (FR3).

## FR2. Notions of two-ness: twelve declared, nine in the state-level matrix

**[definition]**  Kept separate throughout: two carrier elements; two
token identities; two occurrences; two histories (metatheoretic — any
no-op yields distinct histories with equal states, `histories_collapse`);
two states; two event classes; two result constructors; two
object-language judgments; a second sort (receipts); a witnessed
relation with two endpoints; a witnessed irreflexive relation; oriented
versus symmetric difference.

**Scope of the matrix.**  Only the *state-level* notions are state
predicates, so only they enter the implication matrix: the nine keys
carrier / tokens / occurrences / result constructors / judgments /
second sort / witnessed relation / witnessed irreflexive / separable
pair (the last is the unoriented core of the declared oriented-versus-
symmetric notion).  The remaining declared notions are evaluated
separately at their own levels: two histories and two states are
metatheoretic (`histories_collapse`; the dynamics rows); two event
classes is protocol-level (the report flag); orientation is a per-state
refinement of separability (`oriented_two`).  It is a
**nine-state-level-notion implication matrix**, not a twelve-notion
matrix.

**[finite computation]** (`notion_matrix`) Over every reachable state of
every protocol: 13 of 72 non-reflexive implications hold; each failure has
a recorded countermodel.  Holding chains:
`witnessed_irreflexive → witnessed_relation → separable_pair →
second_sort → two_carrier`, and `two_tokens / two_occurrences →
two_carrier`.  Notable refutations: `two_carrier ↛ separable_pair`
(occurrence state), `separable_pair ↛ two_result_constructors` (the tag
route separates under a singleton algebra), `two_result_constructors ↛
two_carrier` (judgment mode sees both constructors with one datum).

**In-class structural fact** (`witnessed_relation →
witnessed_irreflexive`, exhaustively): every refusal link is born
off-diagonal, because a receipt is always fresh — self-refusal is
impossible by construction.  Refusal links are irreflexive *facts* for
free; the *law* is still separate (FR7).

## FR3. T1/T2 — inertia and trace/object separation

**[theorem]** (`silent_repetition_inert`)  Horizon-free: any history of
presentations of already-present tokens fixes the silent state exactly —
arbitrary repetition included.

**[theorem]** (`trace_erasure`, `histories_collapse`)  The traced runner
returns host-visible results (`New`/`Existing`); its state projection
*is* the silent replay.  Two metatheoretically distinct histories (one
and two presentations — different lengths, different result streams)
erase to one object state.  Host-visible refusal adds no object-language
distinction.

## FR4. T3 — result-constructor accounting, refined by the search

**[theorem]** (`singleton_algebra_monochrome`,
`mono_code_swap_invariant`, `distinct_code_not_swap_invariant`,
`distinction_needs_two_constructors`)  A retained receipt pair
distinguishes exactly when its constructor codes differ; a singleton
algebra forces monochrome, swap-invariant, collapsed stores.  Through
the constructor channel, the two-ness of a distinguishing result is
imported by the result type.

**[finite computation — target-relative refinement]**  The class has
three binary-import channels — result constructors, tag observables,
relation instances — but they are **not interchangeable**, and no
target-independent three-channel theorem is claimed.  The search scopes
each channel to its target, with zero exceptions in class (FR8):

* **result-outcome distinction** — the binary result algebra is
  required and suffices (`result_distinction_without_binary_algebra`
  empty); result codes are host values and never enter carrier
  profiles, so constructors alone never separate carrier elements;
* **carrier-pair separability** — a tag or a relation rule is required
  (`separable_without_tag_or_relation`,
  `oriented_without_tag_or_relation` empty); the tag route separates
  under a singleton algebra (`separable_pair ↛
  two_result_constructors`);
* **witnessed relation** — the relation channel is required
  (`witnessed_without_relation_rule` empty).

## FR5. T4 — refusal-to-carrier, answered per variant

| variant | answer | evidence |
|---|---|---|
| retention `none` (R0/R1) | no new object-level difference | `silent_repetition_inert`; report row |
| retention `judgment` (R2) | a second **judgment**, never a second datum | `judgment_variant_second_judgment_not_datum`, `judgment_carrier_bound` (horizon-free) |
| retention `occurrence` (R5) | second carrier element by position import, collapsed | report row; PR #6 equivalence |
| retention `datum` (R3) | second carrier element (coproduct import), collapsed unless tagged/relational | report rows |
| second token (R6) | second carrier element by presentation import, collapsed | control row; bridge checkpoint |

## FR6. T5 — refusal-to-witness: a sufficient bridge and the unique minimum bridge

**[theorem]** (`priced_bridge_closes`, `priced_bridge_oriented`)  A
*sufficient, non-minimum* construction (`stepP`: occurrence-style
reification + tag + automatic relation; its `if` is host-level control
flow, not a stored result constructor — `PState` has no result store)
reaches, in two presentations of one token: carrier 2, relation
`[(0, 1)]`, all links off-diagonal, tag `[1]`, and a state that is not
swap-invariant.

**[theorem]** (`min_witnessed_route_closes`)  The *unique minimum*
witnessed route — the same single protocol under **both** cost orders:
datum retention + the relation rule, no tag, singleton algebra, one
token — verified in Lean on a state type (`MState`) that has **no tag
store and no result store at all**, with the receipt entering as a
literal coproduct (`MItem = tok ⊕ receipt`).  Two presentations of one
token yield the two-element carrier, the witnessed relation `[(0, 1)]`,
and only off-diagonal links.

**[finite computation]** (`minimum_table`)  Minimum protocols with all
ties, two cost orders, split by target:

* Order A (total imports): `two_carrier` at cost 1 with **three tied
  minima** (second token / occurrence / reification) — precisely the
  bridge checkpoint's three purchases; `separable_pair` and
  `oriented_pair` at cost 2 with **two tied minima** — the **relation
  route** (datum + autorel) and the **tag route** (datum + tag);
  `witnessed_relation` / `witnessed_irreflexive` at cost 2 with a
  **unique minimum** (the relation route).
* Order B (lexicographic: external acts, sorts+constructors, rules):
  `two_carrier` selects **occurrence** uniquely; `separable_pair` and
  `oriented_pair` select the **tag route** uniquely — so A and B
  disagree at the weaker milestones; `witnessed_relation` /
  `witnessed_irreflexive` select the **relation route** uniquely —
  agreeing with order A.

**UNIQUE_MINIMUM_WITNESSED_BRIDGE_IN_CLASS** at the witnessed targets;
**MULTIPLE_MINIMUM_WEAKER_BRIDGES** (with order-dependent winners) at
two-ness and separability; each branch's exact price recorded in the
artifact.

## FR7. T6 — irreflexivity provenance (boundary preserved)

**[theorem]** (`bridge_facts_not_law`)  The priced bridge's facts do not
entail the law: a superset relation with a self-edge extends them.  The
in-class structural irreflexivity of refusal links (FR2) is a fact
generator, not a law; the law remains a declaration, exactly as at the
earlier checkpoints.

## FR8. T10 — target-relative provenance dependencies (exhaustive in class)

**[finite computation, exhaustive in class]** (`normal_form_check`)
Each claim has its own check, and each check quantifies over all 44
protocols; the claims made are exactly the claims checked:

* all 16 witnessed-irreflexive-reaching protocols make at least one
  purchase from: second token; occurrence identity; receipt reification
  (coproduct); binary result algebra; tag observable; relation rule +
  witness — zero violations;
* every witnessed-relation reacher has the relation rule;
* every one-token two-carrier reacher has reification or occurrence
  retention;
* every separable-pair reacher and every oriented-pair reacher has a
  tag or a relation rule;
* every two-result-constructor reacher has the binary result algebra.

`normal_form_holds_in_class` is the conjunction of these five checks.
The channels are target-relative (FR4); no target-independent
interchangeability is checked because none is claimed.

**[unresolved]**  The class-general Lean form (over an abstract protocol
grammar rather than the 44-point space) is the single best next theorem
target.

## FR9. T7 — the invariance ceiling, now a theorem

**[theorem]** (`equivariant_output_invariant`)  Fully general: for any
action on states and results and any equivariant construction `F`, if a
state is a fixed point of the symmetry then so is `F` of it.  Choice-free
construction lands in the invariant substructure — the general principle
behind the two-element obstruction (`equivariant_witness_is_S2`,
checkpoint PR #5).  Structural content per instance (identifying the
invariant substructure) remains case-by-case; the two-element case is
done, the general classification is an open obligation.

**The bypass, stated precisely**: tagged/relational refusal states are
never fixed points of the swap (`priced_bridge_oriented`), so the
ceiling does not constrain them.  Orientation cost is relocated to the
declaration, never eliminated.

## FR10. T8 — reflective dynamics, classified

**[theorem]**  Three declared reflective semantics realize three
dynamics; nothing is inferred from finite depth:

* fixed point — `untyped_reflect_fixpoint` (idempotent at depth one);
* two-cycle — `toggle_two_cycle` (replacing retention with a binary
  toggle);
* growth under an explicitly supplied constructor —
  `reflective_chain_growth` (**for every n**, `n` reflections yield a
  carrier of exactly `n + 1` elements), and moreover
  `reflective_chain_is_initial_segment`: the carrier **is**
  `range (n + 1)`, with `reflective_chain_successor_relation`: the
  relation **is** the successor relation, every link an irreflexive fact
  (`reflective_chain_irreflexive_facts`).

**The declared reflective protocol realizes a successor chain — proved
horizon-free.**  Realization, not derivation: `stepRefl` itself appends
the current length and inserts the predecessor–successor edge, so the
successor shape is the *declaration's* content; what the theorems add
is that the realization is exact (`data` **is** `range (n+1)`, `rel`
**is** successor) and holds for every `n`, not up to a tested depth.
Refusal by itself derives no numerals — that reading is explicitly
disclaimed.  The order is object-level (links and tags), unlike
occurrence positions, and the purchase ledger applies: the chain's
order is the autorel constructor's content; nothing here is free.  The
open half is initiality (F4): whether every realization admits a unique
structure map from this chain.

**[finite computation]**  Dynamics per protocol: `fixpoint` for all
non-reifying protocols; `growth_to_cap` for every reflective protocol
(cap 4 within the search; the Lean growth theorem is horizon-free).

## FR11. What still does not follow from `<>`

Unchanged by this run, restated exactly: no successor state, no second
carrier element, no relation, no witness, no irreflexivity law, no
orientation follows from the opaque inscription under silent
deduplication (T1 strengthens this to horizon-free).  Everything the
refusal routes achieve is achieved by their *declarations*; the token
contributes exactly one admission, once.

---

# FRONTIER CONJECTURES

**F1. Choice-cost conservation.**  *Conjecture:* across the ladder act →
declaration → meta-declaration, the number of symmetry-breaking choices
needed to reach an oriented difference is invariant: it can be relocated
(this run: to the protocol declaration) but not reduced.  The general
lemma `equivariant_output_invariant` is the fixed-point half; the
missing half is a census of fixed points at the declaration level.

**F2. The result algebra is the first internalized meta-layer.**  The
three binary-import channels (constructor, tag, relation — each scoped
to its own target, FR4) are all *about* the admission process itself.  *Conjecture:* they are the three
shadows of one construction — internalizing the step function's own
branch — and the tower result algebra / tag / relation is the beginning
of a reflective hierarchy whose n-th layer internalizes the (n-1)-th
layer's control flow.  The reflective chain (FR10) is its first rung.

**F3. Typed refusals generate the augmentation lattice.**  *Conjecture:*
a refusal discipline whose receipts record the *kind* of failure
(duplicate, ill-formed, out-of-range) reproduces the first checkpoint's
Challenge-3 minimum classes (mark, link, self-loop shadows) as refusal
shadows.  A concrete finite search away.

**F4. Proto-numerals: from conjecture to structure theory.**  The chain
theorems make the refusal tower a successor structure; the remaining
conjecture is initiality — that every object realizing "one token plus
reflective tagged refusal" admits a unique structure map from the chain.
If proved, arithmetic's germ sits strictly below Primitive Difference's
symmetric branch: numerals before sets, succession before collection.

**F5. A first genuine endogenous challenge?**  The reflective chain
generates, at each stage, a *fresh unseparated element* — and the
closure policy of the first checkpoint would then demand its separation.
*Conjecture:* the composite (reflective refusal + pair-separation
closure) is the first self-sustaining challenge generator in the
project: refusal supplies the datum, closure supplies the demand.  Its
price is the union of both declarations — but unlike every previous
generator, no *per-round* external act remains.  Testing whether this
composite is genuinely autonomous (or hides a per-round import) is a
sharp, falsifiable next target.

---

# Post-hoc comparison with existing names

*(End-only.)*

* The three binary-import channels mirror the standard trichotomy of
  distinguishing data in semantics: return values, labels, and edges;
  the normal form says a discriminator must live somewhere — a finite
  no-free-lunch analogous to information-flow lower bounds.
* The reflective chain theorems show a declared repetition-refusal
  semantics *realizing* the ordinals below omega — succession as
  reified failure of idempotence — echoing the set-theoretic
  construction of successor as adjoining the previous stage, but with
  the previous stage's *rejection* rather than its collection; the
  construction is a realization by declaration, not a derivation from
  refusal alone.
* Trace/object separation is weak-versus-strong equivalence in process
  semantics once more; the result algebra is an observation alphabet,
  and T3 is the fact that testing power resides in the alphabet.
* The invariance ceiling's general form is the orbit-fixing triviality
  underlying definability-by-invariance arguments; its content per
  instance is the classification of invariants, as in classical
  symmetry-method proofs.
* Relative to the sealed checkpoints: this run closes PR #6's F1
  (relocation proved at both levels), settles PR #6's F2 in the
  realization sense (a declared reflective semantics realizes a
  successor chain, horizon-free; initiality stays open as F4), confirms
  PR #5's purchase list as target-relative in-class dependencies, and
  leaves F5 — the composite endogenous generator — as the project's
  sharpest open question.
