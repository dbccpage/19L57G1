# What a successive-state computation model must declare

Classification: **analysis of already-certified results**, sibling to
`paper/succession_declarations.md`. No new derivation run, no
object-language notion, no new claim. `AuthorityEffect: None`.

This document does not name, target, or refute any external model of
computation. It describes a *structure* — the one any successive-state
account of computing must exhibit — and asks which of its components the
present system derives. The answer is none, and each "no" is pointed at the
theorem that makes it a declaration rather than an omission.

---

## The target, stated structurally

A successive-state computation model exhibits four things:

* **C1** a **persistent carrier** — something that survives a step and
  carries state across it;
* **C2** a **single-valued step** — given a configuration and an occasion,
  *the* next configuration;
* **C3** an **index with a distinguished successor** — an order in which
  steps occur, individuating them;
* **C4** an **occasion to step at all** — something that makes the next
  step arise.

Each is named here by its role, not by any model's vocabulary for it.

---

## The mapping

`paper/succession_declarations.md` §4 itemizes five declarations this
system requires before a next-state relation can be written. The four
components above land on them as follows.

| component | requires | this system |
|---|---|---|
| **C1** persistent carrier | a declared state shape | `Regime` is a **declared** frozen shape. State changes only through admission events; `Supply` provably does not change it (`supply_no_op`). Nothing derives the carrier. |
| **C2** single-valued step | cost measure + demand selection + response selection | **three** declarations, and one of the other two fights them (below) |
| **C3** index with successor | the admission order | internal identity **is** the admission index, and the entries are presentation tokens *visible only to the metatheory*. The order individuates, and is forgotten at the isomorphism quotient. |
| **C4** occasion to step | a continuation policy | **[bounded theorem]** no object-language endogenous demand generator was derived; closure terminates. Demands are supplied. |

---

## C2 is the expensive one, and it is contested

Getting a single-valued step costs three of the five declarations: a cost
measure to say which responses are minimal, a demand selection to say which
pair is challenged, and a response selection to pick among minimal
responses.

It is contested because the **invariance requirement** — the fifth
declaration — actively rejects the obvious way to get it. Least-pair
selection is well defined, total and deterministic; it was replaced because
"least" depends on how the data happened to be numbered, and the numbering
is presentation. The regression test
`test_least_pair_selection_is_not_equivariant` records that the
deterministic rule was presentation-dependent.

So C2 is not merely undeclared here. It is the component that the system's
own invariance constraint most directly obstructs. A rule that ignores
presentation does not, on the present evidence, deliver a function: the
minimum valid response has 3 tied classes in one reading and 5 in the other
under the item-count measure, plus a countably infinite family indexed by
arity, and collapses to uniqueness only *up to isomorphism* under the
refined measure.

---

## What this does NOT claim

* It does **not** claim any model of computation is impossible,
  inconsistent, or refuted. It names none, and no impossibility result
  appears here or in the sibling document.
* It does **not** claim these four components are the *right*
  decomposition, or a minimal one. The decomposition is **declared** for
  this analysis, exactly as the candidate space and cost measures are
  declared elsewhere. A different decomposition could yield a different
  itemization.
* It does **not** claim that a system requiring declarations is thereby
  defective. Every account imports something; the content here is the
  *itemization*, not a verdict.
* It does **not** supply a map from this structure to any observed domain
  or to any computational practice. Semantic interpretation is kept
  distinct from presentation identity, internal identity, observational
  equivalence, and behavioral separation, and nothing above is such a map.
  Whether these components correspond to anything realized is outside
  every result cited.
* It introduces no counting, magnitude, norm, observer, container, or
  clock.

---

## Open

* Whether **C1–C4** are independent, or whether some component follows from
  the others under a declared candidate space of computation models, is not
  proved. That would need the Challenge-3 treatment applied to model
  structures, and is not attempted.
* The stronger question inherited from the sibling document stands as
  scoped there: whether, for a measure that does not itself force
  uniqueness, every presentation-independent selection rule is multivalued
  at the minimum — and whether that holds independently of measure choice.
  A positive answer would say **C2** is unavailable to any
  presentation-independent account, not merely absent from this one. That
  is the result worth wanting, and it is **OPEN**.
