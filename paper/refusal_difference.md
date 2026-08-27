# Refusal as a Difference Source

**Question** (the bridge investigation's F3, posed for this
investigation):  can the failed re-admission of one already admitted
token, when that failure/refusal is itself admitted as object-language
data, produce a second distinguishable state without a second token?

**Verdict up front.**  Yes — under exactly one of the studied
disciplines, and the result is stronger than asked: the tagged-refusal
discipline produces a *witnessed, canonically oriented* difference from
one token in two admissions.  But the price table shows no free lunch:
its declaration bundles precisely the capabilities (occurrence
reification + one unary observable) that the explicit route admits one
by one.  What is genuinely new is *where the choice lives*: the
symmetry-breaking choice that every other route pays per act is here
made once, in the discipline declaration.  Refusal is the first studied
orientation source that never enters a symmetric state.

**Protocol.**  Constructive comparison first; end-only name comparison.
Lean: `lean4/Derivation/Refusal.lean` (16 theorems; imports the
admission model's core and the primitive-difference layer for the
translation results).  Python: `code/derivation/refusal.py`, artifact
`artifacts/refusal.json` — deterministic BFS over a reduced signature
(supplies, admissions, one unary form, unary instances; carrier capped
at 2; 7-event horizon).  Nothing here modifies the earlier developments;
the disciplines are *declared alternatives* to the first development's
admission rule.  Statement tags as in the companion papers.

---

# FORMAL SPINE

## R1. The disciplines

**[declared metatheory]**  Five re-admission disciplines over one
reduced signature (state: admitted tokens in order, discipline-tagged
indices, a refusal counter, one optional unary form and its instances):

1. `silent` — re-admission is a designation no-op (the first
   development's semantics);
2. `meta` — re-admission is a state no-op; a refusal *marker* is
   recorded in the history only;
3. `fact` — re-admission increments an admitted refusal counter (a
   state fact attached to no datum);
4. `reify_untagged` — the refusal is reified as another carrier
   occurrence of the same token;
5. `reify_tagged` — as 4, and the discipline tags the reified
   occurrence with a built-in unary observable.

Baselines: `occurrence` admission and `second_token` admission (the
bridge investigation's scenarios).

**Nothing is assumed equivalent.**  Refusal, repetition, occurrence, and
state difference are related only by the theorems and countermodels
below.

## R2. The four-way determination

**[finite computation]** (`artifacts/refusal.json`; scope: reduced
signature, carrier cap 2, 7-event horizon) with the theorem citations
per row:

| discipline | determination | min admissions to: carrier 2 / witnessed / oriented witnessed |
|---|---|---|
| `silent` | **no new object-level difference** | — / — / — |
| `meta` | **one object plus one (metatheoretic) event** | — / — / — |
| `fact` | **two states only** | — (state difference at 2) / — / — |
| `reify_untagged` | **two carrier objects** (collapsed) | 2 / 4 / 4 |
| `occurrence` | **two carrier objects** (collapsed) | 2 / 4 / 4 |
| `second_token` | **two carrier objects** (collapsed) | 2 / 4 / 4 |
| `reify_tagged` | **two carrier objects, witnessed and oriented** | 2 / **2** / **2** |

The tagged row's witness needs **no instance events**
(`witness_without_instances = 2`): the discipline's built-in tag is the
separating observable.

## R3. The strict hierarchy, separated at every gap

History difference < state difference < carrier growth < witnessed
difference:

* **history < state** — **[theorem]** (`silent_eq_meta`,
  `marker_state_invisible`, `markers_invisible`): the meta discipline is
  *state-identical* to silent; histories differing by refusal markers
  replay identically.  Refusal visible only to the metatheory changes
  nothing an object ever sees.
* **state < carrier** — **[theorem]** (`fact_state_changes` vs
  `silent_state_fixed`, `nonreify_carrier_bound`): the fact discipline
  changes state on every refusal while its carrier provably never leaves
  the singleton.  A refusal counter is a state difference that separates
  no pair — there is only one datum to compare.
* **carrier < witnessed** — **[theorem]**
  (`reifyUntagged_two_admissions` + `untagged_translation_collapsed`):
  untagged reification reaches carrier 2 with the two occurrences
  object-collapsed.
* **witnessed** — **[theorem]** (`reifyTagged_two_admissions`,
  `tag_separates`): the tagged discipline's second admission produces a
  separable pair.

## R4. One proved equivalence and its meaning

**[theorem]** (`reifyUntagged_eq_occurrence`,
`reifyUntagged_replay_eq_occurrence`; exhaustively echoed by
`equivalence_check`)  The untagged reifying discipline **is** occurrence
admission: their steppers agree on every state and event.

Repetition-refusal reified without a tag is occurrence admission under
another name.  The interesting content of "refusal" is therefore *not*
the reification — it is the asymmetry the refusal carries, which only
the tag preserves.

## R5. The orientation theorem (the genuinely new phenomenon)

**[theorem]** (`occurrence_state_swap_invariant`)  The untagged
two-occurrence state is swap-invariant: its two elements are symmetric,
so any designation or marking is a per-act choice, and the bridge
investigation's equivariance obstruction applies in full.

**[theorem]** (`tagged_state_not_swap_invariant`,
`canonical_designation`)  The tagged two-occurrence state is *not*
swap-invariant, and the discipline provides a canonical designated
occurrence (the tagged one).  The designation that was proved impossible
to choose equivariantly *from a symmetric state* is here supplied by
**never entering a symmetric state**: the refusal is born asymmetric —
established versus refused.

**Reading, scoped.**  The equivariance obstruction is not violated; it
is bypassed at the declaration level.  The symmetry-breaking choice
still exists, but it is made once — in choosing the discipline — rather
than once per act.  Refusal relocates orientation cost from acts to
declarations.

## R6. No free lunch: the price table

**[theorem]** (`tagged_translation_separable`,
`untagged_translation_collapsed`)  The tag observable's separating
content is exactly one unary form plus one instance: the tagged
two-occurrence state translates to the admission model's unary-mark
regime, and the untagged one to the collapsed bare regime.

**[declared metatheory]** (`capability_prices` in the artifact)  The
declared bill per discipline:

| discipline | imports |
|---|---|
| `silent` | — |
| `meta` | history-only refusal marker |
| `fact` | admitted refusal counter |
| `reify_untagged` | reification (metatheoretic position identity) |
| `reify_tagged` | reification + built-in unary observable (= form + instance) + canonical orientation (per-declaration) |
| `occurrence` | metatheoretic position identity |
| `second_token` | second external presentation |

The tagged discipline's two-admission route and the explicit
four-admission route (second token or occurrence, then form, then
instance) import the *same* capabilities; the tagged discipline bundles
them into the declaration.  The admission-count saving is real but is
purchased entirely at declaration time.

**Scope of the earlier carrier bound.**  The bridge investigation's
`single_token_carrier_bound` was proved for the dedup discipline; the
reifying disciplines escape it by *being different declared
disciplines*, not by refuting it.  Its hypothesis is exactly what
`silent`/`meta`/`fact` satisfy (`nonreify_carrier_bound`).

## R7. Terminal statement

**Scoped to the reduced signature, the declared disciplines, and the
declared search bounds:**

> **Failed re-admission can produce a second distinguishable state
> without a second token — but only when the refusal is reified *and*
> tagged, and the discipline that does so imports exactly the
> capabilities of the explicit route (occurrence reification plus one
> unary observable).**
>
> * Refusal visible only to the metatheory produces one object plus one
>   event — nothing an object sees (`silent_eq_meta`,
>   `markers_invisible`).
> * Refusal admitted as a counter produces two states only — a state
>   difference with a single datum and no separable pair
>   (`fact_state_changes`, `nonreify_carrier_bound`).
> * Refusal reified without a tag *is* occurrence admission
>   (`reifyUntagged_eq_occurrence`) — two collapsed carrier objects.
> * Refusal reified with a tag produces two carrier objects with a
>   witnessed, canonically oriented difference at two admissions
>   (`tag_separates`, `tagged_state_not_swap_invariant`,
>   `canonical_designation`), at the declared price of the bundled
>   capabilities (`tagged_translation_separable`).
>
> Repetition, refusal, occurrence, and state difference are pairwise
> non-equivalent, except for the one proved identity
> (untagged reification = occurrence).  The strict hierarchy
> history < state < carrier < witnessed is separated at every gap.

## R8. Countermodel and separation index

| exhibit | separates | where |
|---|---|---|
| marker histories with equal replay | history diff from state diff | `markers_invisible` |
| fact vs silent on re-admission | state diff from no diff | `fact_state_changes` / `silent_state_fixed` |
| fact carrier bound | state diff from carrier growth | `nonreify_carrier_bound` |
| untagged two-occurrence state | carrier growth from witnessed diff | `reifyUntagged_two_admissions`, `untagged_translation_collapsed` |
| stepper identity | refusal-reification from occurrence: **equal** | `reifyUntagged_eq_occurrence` |
| swap-invariance pair | per-act choice from per-declaration orientation | `occurrence_state_swap_invariant` vs `tagged_state_not_swap_invariant` |

## R9. Unresolved obligations

* **[unresolved]** The reduced signature has one unary form and a
  carrier cap of 2; the discipline comparison at larger carriers (does
  tagging refusals of *distinct* tokens stay canonical?) is open.
* **[unresolved]** A Lean statement of the full four-way determination
  as a single classification theorem over the `Mode` type (the per-mode
  facts are proved; the assembled trichotomy quantified over histories
  is not).
* **[unresolved]** Whether per-declaration choice is itself eliminable:
  a discipline chosen by an equivariant meta-rule — the invariance
  ceiling one level up (F1 below).
* **[bounded theorem]** All search results are exhaustive only within
  the declared bounds; the Lean theorems cited are bound-free but
  per-state or per-stepper.

---

# FRONTIER CONJECTURES

**F1. The invariance ceiling recurs at declaration level.**
*Conjecture:* any meta-rule that selects a discipline equivariantly
(without naming `reify_tagged`'s asymmetry) selects a discipline whose
states remain swap-invariant — the choice cannot be pushed to a meta-
meta-level without reappearing.  Orientation cost is conserved: it can
be relocated (act → declaration → meta-declaration) but not eliminated.
Evidence: the act-level case is proved (bridge equivariance obstruction);
the declaration-level case is this paper's relocation theorem; the
conservation claim is open.

**F2. The refusal tower is a successor structure.**  Each further
re-admission under `reify_tagged` reifies another tagged occurrence:
one token generates the chain (untagged origin, tagged₁, tagged₂, …)
with a canonical linear order (admission order internalized by tags).
*Conjecture:* this chain is the minimal object realizing the companion
conjecture "occurrence bookkeeping as proto-quantity" — numerals as the
refusal tower of a single inscription.  The tower's order is
object-level (each element tagged at birth), unlike occurrence
positions, which stay metatheoretic.  Formalizing the chain and its
initiality is concrete next mathematics.

**F3. Refusal-of-what?  Typed refusals.**  The studied refusal is
uniform.  A discipline whose refusal records *what* was refused
(re-admission vs ill-formed instance vs out-of-range index) would carry
a richer built-in observable family.  *Conjecture:* typed refusals
generate exactly the one-step augmentation lattice of the first
development's Challenge 3 (marks, links, self-loops) as refusal shadows
— collapse diagnostics as difference sources.

**F4. Fidelity refusal.**  The first development's persistent
requirements refuse *collapses*; this paper's disciplines refuse
*re-admissions*.  *Conjecture:* both are instances of one schema —
a protected law plus a reification policy for its violations — and the
`FidelityObstruction` of the primitive-difference layer is the
declarative core of every refusal discipline.  If so, "repair" (the one
notion of the original mandate never yet formalized) is precisely a
refusal discipline whose reified violations are afterwards separated.

---

# Post-hoc comparison with existing names

*(Post-hoc comparison only. This section is not derivational input,
theorem evidence, or authorization; nothing above depends on it.)*

* The strict hierarchy (history / state / carrier / witnessed) parallels
  the ladder from trace equivalence to state equivalence to
  bisimulation-with-observations in process semantics: refusal markers
  are silent transitions, and the meta discipline's invisibility is
  weak-equivalence erasure of internal moves.
* "Refusal" deliberately echoes refusal sets in process testing
  theories; the finding that only *reified, tagged* refusal changes the
  object-level theory matches the fact that refusal information is
  observational only when the semantics internalizes it.
* The tagged discipline is a one-token Peano germ: the refusal tower of
  F2 is a successor chain, and the canonical orientation is the
  asymmetry of successor application — supporting the companion
  conjecture that counting arises from repetition bookkeeping rather
  than from collections.
* The relocation of choice from acts to declarations is the
  constructive-mathematics distinction between choice made pointwise
  and choice made uniformly by a rule; the conjecture that orientation
  cost is conserved across levels is a definability-by-invariance claim
  one level up from the bridge investigation's.
* Relative to the earlier developments: this closes the loop on the
  bridge's open question B9/F3 with a positive-but-priced answer, and
  identifies the first development's persistent-requirement discipline
  as a sibling of the refusal schema (F4) — suggesting the original
  derivation's "repair" machinery was a refusal discipline all along.
