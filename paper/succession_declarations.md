# What a successive-state model must declare

Classification: **analysis of already-certified results**. This document
runs no new derivation, introduces no object-language notion, and licenses
no new claim. Every number below is read from `artifacts/claims.json` and
every theorem named is already exported. What is new is the *statement of
what the existing results mean together*, which had not been said.

`AuthorityEffect: None`.

---

## The question

A successive-state model — any account in which a system has a state and a
next state — is not a single assumption. It is a bundle. To write one down
at all you must supply:

1. a carrier that persists across the step,
2. a distinguished *next*, single-valued,
3. an order that individuates the states.

The question this document answers is narrow: **which of those does the
present system derive, and which must be declared?** The answer is that it
derives none of them, and that the reason is not an omission but a set of
proved results.

---

## 1. Nothing generates a demand

**[theorem]** (Challenge 0, model-scoped) No successor is internally forced.
The model contains no transition machinery other than external-event-indexed
admission; a proposal cannot mutate state without an admission event.

**[theorem]** (`supply_no_op`) Bare supply does not change the admitted
state.

**[bounded theorem]** (§11(f)) No object-language endogenous demand
generator was derived. Under the declared pair-separation closure policy the
fixed finite datum set reaches the all-pairs-separated fixpoint within
`n(n-1)/2` rounds; closure terminates.

Read together: the system does not produce its own occasions for change.
Every demand enters as a declared challenge. "External" here means *not
entailed by the object language* — it does not name an agent, and nothing
in the formalism pushes.

---

## 2. Given a demand, the next state is not single-valued

This is the load-bearing result, and it is the one that had not been stated
as a fact about succession.

A successive-state model needs `next` to be a **function**. Given a state
and an occasion, there must be *the* successor. What the derivation
computed is that the minimum valid response to a separation requirement is
not unique:

| claim ledger key | reading L | reading F |
|---|---|---|
| `CL-3-MIN-TWO` (minimum cost) | 2 items | 2 items |
| `CL-3-NONUNIQUE-MU1` (tied classes, item-count measure) | **3** | **5** |
| `CL-3-UNIQUE-MU2` (refined measure) | 1 | 1 |

and, beyond the tabulated bound, a **countably infinite tie family indexed
by arity** — one non-isomorphic member for every arity `k >= 1` (§11(d)).

So a demand determines a *set* of minimal responses, not a state. Under one
declared measure that set is infinite. Single-valued succession is therefore
not a fact about this system; it is a property one obtains only after
declaring a measure — and the two declared measures disagree about whether
it holds.

---

## 3. Even single-valuedness up to isomorphism is a declared invariance

The refined measure returns uniqueness **up to isomorphism**. That is not
the same as a successor function, and closing the gap requires a second
declaration, of a different kind.

The derivation's expansion policy is:

> one challenge branch per automorphism orbit of collapsed pairs
> (isomorphism-equivariant)

and the record states what it replaced:

> replaces raw least-pair selection, which was not equivariant

with a regression test, `test_least_pair_selection_is_not_equivariant`, and
an exhaustive congruence test,
`test_orbit_policy_transition_congruence_exhaustive`.

This is worth stating plainly. The obvious rule — *take the least pair* —
is well defined, deterministic, and **wrong**, because "least" depends on
how the data happened to be numbered, and the numbering is presentation,
visible only to the metatheory. A policy built on it makes the trajectory
depend on labels that carry no internal content. The replacement is a
policy that depends only on the automorphism orbit, and
`expansions_with_multiple_orbits` is **0** across all six branch families
(`F_mu1`, `F_mu2`, `L_mu1`, `L_mu2`, `closed_F`, `closed_L`).

The requirement that a rule not depend on presentation is an **invariance
principle**, and it is declared, not derived. It is also load-bearing: it
is what rejects the naive deterministic rule. Determinism and invariance
pull against each other here, and invariance was chosen.

---

## 4. What succession costs, itemized

Assembling a next-state relation in this system requires:

| declaration | what it fixes | derived? |
|---|---|---|
| a cost measure | which responses count as minimal | no — `mu1` and `mu2` are declared, and disagree |
| an invariance requirement | that the rule ignore presentation | no — declared; rejects least-pair selection |
| a representative selection | which member of a tie class is taken | no — residual freedom inside an orbit |
| a continuation policy | that there be a next demand at all | no — declared external metatheory |

Four declarations, none derived, and the first two are in tension. That is
the itemized answer to what a successive-state model must import.

---

## 5. What this does NOT claim

* It does **not** refute any external model of computation, and names
  none. The result is model-scoped: in a system with no imported
  succession, none arises. That is a statement about this system, not an
  impossibility theorem about others.
* It does **not** claim the tie counts are complete beyond the declared
  bounds (items <= 2, arity <= 2 concrete, 15 rounds, node guards). The
  infinite arity-indexed family is proved; the tabulated counts are
  bounded.
* It does **not** derive plurality from nothing.
  `no_coherent_path_retains_multiplicity` shows that multiplicity survives
  an attempted universal collapse, but it is conditional on an admitted
  network with a missing coherent path.
* It does **not** supply a map from this structure to any observed
  domain. Semantic interpretation is kept distinct from presentation
  identity, internal identity, observational equivalence, and behavioral
  separation, and none of the results above is such a map.
* It introduces no counting, magnitude, norm, observer, container, or
  clock.

---

## 6. Open

* Whether the four declarations in §4 are **minimal** — whether some
  smaller set suffices to state a successor relation — is not proved. That
  would need the Challenge-3 treatment applied to succession policies: a
  declared candidate space of policies, a cost measure over them, and
  exhaustive enumeration. It is not attempted here.
* The tension in §3 between determinism and invariance is exhibited on one
  example (least-pair selection) and is not characterized. Whether every
  presentation-independent selection rule is multivalued at the minimum is
  **OPEN**.
