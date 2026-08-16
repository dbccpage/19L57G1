# The cost bill for a successive-state account

Classification: **consolidation of already-certified results**. It
introduces nothing. Every line is carried over from
`paper/succession_declarations.md`, `paper/candidate_measure_space.md`, or
`paper/computation_declarations.md`, and every figure is already in
`artifacts/claims.json`. No new derivation run, no object-language notion,
no new claim, no ledger entry. `AuthorityEffect: None`.

This page exists so the account can be read in one place. It is
deliberately short and deliberately unexciting. Nothing here is promoted:
no statement is strengthened relative to its source, and where a source
states a scope, the scope travels with the line.

---

## 1. The bill

What must be declared before a successive-state account can be written
down, and what forces each to be a declaration rather than a derivation.

| # | declaration | what it fixes | why it is not derived |
|---|---|---|---|
| 1 | **cost measure** | which responses count as minimal | `mu1` and `mu2` are both declared and *disagree* about uniqueness |
| 2 | **invariance requirement** | that the rule ignore presentation | declared; it is what rejected least-pair selection |
| 3 | **demand selection** | which collapsed pair is challenged | constrained to one branch per automorphism orbit; residual wherever several orbits exist |
| 4 | **response selection** | which minimal delta is taken from a tie class | 3 classes in reading L and 5 in F under `mu1`, plus a countably infinite family indexed by arity |
| 5 | **continuation policy** | that there be a next demand at all | **[bounded theorem]** no endogenous demand generator was derived; closure terminates |

A structural account of computing exhibits four components. They land on
the same bill:

| component | requires | paid by |
|---|---|---|
| **C1** persistent carrier | a declared state shape | declared `Regime`; `supply_no_op` shows presentation alone changes nothing |
| **C2** single-valued step | items 1, 3 and 4 — and item 2 obstructs it | see §2 |
| **C3** index with a distinguished successor | the admission order, whose entries are metatheory-visible tokens | not derived |
| **C4** occasion to step | item 5 | not derived |

---

## 2. The one tension on the bill

Items 1 and 2 are coupled: the measure creates the non-uniqueness that
makes a selection necessary, and the invariance requirement constrains
which selection rules are permitted.

The collision actually exhibited in code is narrower. Least-pair selection
is well defined, total and deterministic — and was **rejected**, because
"least" depends on how the data happened to be numbered. The regression
test `test_least_pair_selection_is_not_equivariant` records the defect;
`test_orbit_policy_transition_congruence_exhaustive` records the
replacement's congruence.

**Determinism and invariance pull against each other, and invariance won.**
That is a code change with a test, not a reading.

---

## 3. Two facts that price the bill

**Given a demand, the minimum response is not single-valued.** Under the
item-count measure: 3 tied non-isomorphic classes in reading L, 5 in
reading F, within the declared bounds — plus a countably infinite tie
family, one member for every arity `k >= 1`. Under the refined measure the
minimum is unique up to isomorphism, grammar-wide for reading L and within
bounds for reading F.

**Refining the measure does not reach a single-valued step.** Even the
unique class under the refined measure contains **two concrete deltas**,
related by the transposition swapping the requirement pair. The measure
delivers at best a singleton *class*. The remaining step to one concrete
response is item 4, not a further measure.

---

## 4. What is *not* on the bill

Recorded so the bill is not read as "everything must be declared."

* That the initial inscription generates nothing — **[theorem]**.
* That supply without admission changes no state — **[theorem]**,
  `supply_no_op`.
* That admission without judgment structure yields total observational
  collapse — **[theorem]**.
* That the minimum response cost is exactly two items, in both readings —
  **[theorem]**, absolutely over the item grammar.
* That every supplied separation demand on a well-formed accepted regime
  is answerable — **[theorem]**.
* That pair-separation closure terminates — **[bounded theorem]**.

---

## 5. Scope, and what would change the bill

Every tree-level figure is relative to the declared bounds (items <= 2,
arity <= 2 concrete, 15 rounds, node guards). The tie counts of 3 and 5
are a **[bounded theorem]**; the arity-indexed family is not bounded.

The bill is an account of **this** system. It is not an impossibility
result about any other, and no external model is named or refuted here.

What would change its standing is the scoped open question already
recorded in `paper/succession_declarations.md` §6: whether, for a measure
that does not itself force uniqueness, every presentation-independent
selection rule is multivalued at the minimum — and whether that holds
independently of measure choice over presentation-independent measures. A
positive answer to the second would say item 4 is unavailable to any
presentation-independent account, rather than merely absent from this one.
It is **OPEN**, and no selection rule has been enumerated anywhere in this
chain.

---

## 6. Non-claims

* Does not claim the bill is **minimal** or that its five items are
  independent; that would need the Challenge-3 treatment applied to
  succession policies, and is not attempted.
* Does not claim the four-component decomposition in §1 is the right or
  only decomposition; it is declared for the analysis.
* Does not claim single-valued succession is impossible in any account —
  only that this system does not supply it and that measure refinement
  cannot manufacture it.
* Does not enumerate selection rules.
* Does not name, target, or refute any external model of computation.
* Introduces no counting, magnitude, observer, container, or clock.
