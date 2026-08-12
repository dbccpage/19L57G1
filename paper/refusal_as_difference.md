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
MULTIPLE_MINIMUM_BRIDGES
```

Within the declared 44-protocol class: the refusal bridge **closes** for
priced protocols and **fails** for the free fragment, with **incomparable
tied minima** under the declared cost orders and a **provenance normal
form proved in-class**: every route from one opaque token to a witnessed
irreflexive datum factors through at least one explicit purchase, and
the two cost orders disagree on which purchase is cheapest.  Every
construction that succeeds moves the import into a result constructor,
a tag observable, a relation rule, a reification/occurrence rule, or a
second token — nothing arrives from the token itself.

* **Proved** (Lean, 19 new theorems): silent-refusal inertia
  horizon-free (T1); result streams never feed back — trace/object
  separation (T2); the constructor-channel dependency core (T3); the
  judgment variant's carrier bound (T4); the priced constructive bridge
  and its orientation (T5); facts-not-law carried over (T6); the
  invariance ceiling in fully general form (T7); reflective dynamics —
  fixpoint, two-cycle, and horizon-free chain growth with the chain's
  carrier literally `range (n+1)` and its relation literally successor
  (T8).
* **Computed only within bounds** (44 protocols, 6-event horizon,
  carrier cap 4): the notion matrix (13 of 72 non-trivial implications
  hold, countermodels for the rest), the minimum-price table with ties,
  the normal-form check, and the in-class structural fact that every
  refusal link is born off-diagonal.
* **Refuted**: that refusal per se is a new difference source (the
  untagged reification is occurrence admission — checkpoint PR #6 —
  and the free fragment reaches nothing); that distinction can arrive
  without a binary import (three channels exist — constructor, tag,
  relation — and at least one must be purchased); that a single
  cheapest bridge exists (the cost orders disagree).
* **Imported, explicitly, by the successful routes**: receipt
  reification (coproduct into the carrier) or occurrence identity or a
  second token, for two-ness; a tag observable or a relation rule + its
  witness, for separability; the irreflexivity law, always separately.
* **Open**: the general invariance ceiling with structural hypotheses
  (T7's general lemma is proved; identifying invariant substructures
  beyond the two-element case is not); a Lean-general T10 over an
  abstract protocol grammar; typed refusals (F3 below).
* **Single best next theorem target**: the class-general provenance
  normal form in Lean — a protocol-grammar-level theorem that every
  reachable separable pair pulls back to one of the three binary-import
  channels (constructor / tag / relation), with the finite search's 44
  instances as its decidable shadow.

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

## FR2. Twelve notions of two-ness

**[definition]**  Kept separate throughout: two carrier elements; two
token identities; two occurrences; two histories (metatheoretic — any
no-op yields distinct histories with equal states, `histories_collapse`);
two states; two event classes; two result constructors; two
object-language judgments; a second sort (receipts); a witnessed
relation with two endpoints; a witnessed irreflexive relation; oriented
versus symmetric difference.

**[finite computation]** (`notion_matrix`) Over every reachable state of
every protocol: 13 of 72 non-trivial implications hold; each failure has
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

**[finite computation — refinement]**  The search shows the constructor
channel is one of exactly **three** binary-import channels in the class:
result constructors, tag observables, relation instances.
`separable_pair ↛ two_result_constructors` — the tag route separates
with a singleton algebra.  The corrected dependency (the normal form,
FR8): a separable pair requires *at least one* of the three channels;
each is a declared purchase.

## FR5. T4 — refusal-to-carrier, answered per variant

| variant | answer | evidence |
|---|---|---|
| retention `none` (R0/R1) | no new object-level difference | `silent_repetition_inert`; report row |
| retention `judgment` (R2) | a second **judgment**, never a second datum | `judgment_variant_second_judgment_not_datum`, `judgment_carrier_bound` (horizon-free) |
| retention `occurrence` (R5) | second carrier element by position import, collapsed | report row; PR #6 equivalence |
| retention `datum` (R3) | second carrier element (coproduct import), collapsed unless tagged/relational | report rows |
| second token (R6) | second carrier element by presentation import, collapsed | control row; bridge checkpoint |

## FR6. T5 — refusal-to-witness: the priced bridges

**[theorem]** (`priced_bridge_closes`, `priced_bridge_oriented`)  The
protocol with datum retention + autorel reaches, in two presentations of
one token: carrier 2, relation `[(0, 1)]`, all links off-diagonal, tag
`[1]`, and a state that is not swap-invariant.  A witnessed,
irreflexive-as-fact, oriented datum from one token — with every
capability visible in the step function itself.

**[finite computation]** (`minimum_table`)  Minimum protocols with all
ties, two cost orders:

* Order A (total imports): `separable_pair` and `oriented_pair` at cost
  2 with **two incomparable tied minima** — the **relation route**
  (datum + autorel) and the **tag route** (datum + tag);
  `witnessed_relation`/`witnessed_irreflexive` at cost 2, unique
  (relation route); `two_carrier` at cost 1 with **three tied minima**
  (second token / occurrence / reification) — precisely the bridge
  checkpoint's three purchases.
* Order B (lexicographic: external acts, sorts+constructors, rules):
  the **tag route wins separability** while the **relation route wins
  witnessed relation** — the two orders disagree on the cheapest
  bridge.

**MULTIPLE_MINIMUM_BRIDGES**, with each branch's exact price recorded in
the artifact.

## FR7. T6 — irreflexivity provenance (boundary preserved)

**[theorem]** (`bridge_facts_not_law`)  The priced bridge's facts do not
entail the law: a superset relation with a self-edge extends them.  The
in-class structural irreflexivity of refusal links (FR2) is a fact
generator, not a law; the law remains a declaration, exactly as at the
earlier checkpoints.

## FR8. T10 — the provenance normal form (in-class theorem)

**[finite computation, exhaustive in class]** (`normal_form_check`)  All
16 witnessed-irreflexive-reaching protocols make at least one purchase
from: second token; occurrence identity; receipt reification
(coproduct); binary result algebra; tag observable; relation rule +
witness.  Zero violations.  Finer dependencies, zero exceptions:
witnessed relations occur only with the relation rule; carrier growth
from one token occurs only with reification or occurrence retention.

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

**The refusal tower is a successor structure — proved, not
conjectured.**  One token, reflected n times under the priced
discipline, is the initial segment of the numerals with successor.  The
order is object-level (links and tags), unlike occurrence positions.
The purchase ledger applies: the chain's order is the autorel
constructor's content; nothing here is free.

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
three binary-import channels (constructor, tag, relation) are all
*about* the admission process itself.  *Conjecture:* they are the three
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
* The reflective chain theorems construct the ordinals below omega in
  von Neumann style from repetition-refusal — succession as reified
  failure of idempotence — echoing the set-theoretic construction of
  successor as adjoining the previous stage, but with the previous
  stage's *rejection* rather than its collection.
* Trace/object separation is weak-versus-strong equivalence in process
  semantics once more; the result algebra is an observation alphabet,
  and T3 is the fact that testing power resides in the alphabet.
* The invariance ceiling's general form is the orbit-fixing triviality
  underlying definability-by-invariance arguments; its content per
  instance is the classification of invariants, as in classical
  symmetry-method proofs.
* Relative to the sealed checkpoints: this run closes PR #6's F1
  (relocation proved at both levels), proves PR #6's F2 (the tower is a
  successor structure), confirms PR #5's purchase list as an in-class
  normal form, and leaves F5 — the composite endogenous generator — as
  the project's sharpest open question.
