# The declaration bill between the pre-quotient germ and the descent layer

Classification: **analysis of already-certified results**. No new derivation
run, no object-language notion, no new claim. `AuthorityEffect: None`.

Sibling to `paper/succession_declarations.md`,
`paper/candidate_measure_space.md` and
`paper/computation_declarations.md`.

This page answers one question: *what still has to be declared to climb
from the pre-quotient difference germ to the quotient-and-descent layer?*
It does not import, restate, or name any supplied vocabulary; the working
identifier denylist is enforced by `tests/test_primitive_contact.py`, and
comparison against supplied material belongs in `contact/`, not here.

---

## 1. Two layers already exist, and they are not the same object

**Lower layer — the germ.** `lean4/Derivation/PrimDiff.lean` states its own
ceiling in its header:

> Candidates for the weakest formal object deserving the name *primitive
> difference*, before contexts, profiles, observers, quotients, or repairs
> exist. Self-contained: nothing here imports or assumes the regime model
> of the earlier development.
>
> Metatheory used (declared): types, functions, one binary relation symbol
> per structure, propositional logic, and finite case analysis. **No
> quotient machinery, no context spaces, no state.**

Its candidate glossary runs `A1` (a relation with one asserted pair, no
axioms), `A1i` (plus irreflexivity), `A2` (witnessed non-identification),
`A3` (non-factorization through a point), `A4` (irreducibility under an
admitted operation family), `A5` (the two-element carriers `D2` and `S2`).

**Upper layer — quotient and descent.** `lean4/Derivation/DiffInterface.lean`
and `lean4/Derivation/ObsDescent.lean` carry the quotient machinery, and
their theorems are **audited**: they appear in `artifacts/lean_axioms.txt`
with `#print axioms` reports, within `{propext, Quot.sound}`. Among them:

| theorem | what it settles |
|---|---|
| `ObsDescent.deltaDescend_exists_iff` | descent of the two-place difference holds *exactly when* the congruence condition does |
| `ObsDescent.deltaDescend_unique` | the descended map is unique |
| `ObsDescent.deltaDescend_blocked_of_witness` | a witness blocks descent |
| `ObsDescent.collapseAllObs_all_zero` | total collapse: the zero relation holds everywhere |
| `ObsDescent.collapseAllObs_not_deltaConstant` | and the difference is still not class-constant there |
| `ObsDescent.collapseAllObs_no_view_descend` | one-place views fail to descend in that model |

The upper layer is not the lower layer with more theorems. It is the lower
layer **plus declarations**, and the point of this page is to name them.

---

## 2. What the germ supplies, and what it does not

The germ supplies a carrier, a relation, an asserted pair, and — at `A1i`
— irreflexivity. From that it reaches distinctness-style consequences and
the two-element realizations by finite case analysis, using no quotient.

What it does **not** supply, and what no theorem in it derives:

* **Zero-difference as an equivalence.** The upper layer needs a
  zero predicate on a value type together with reflexivity, symmetry and
  transitivity. In the germ there is no value type and no such predicate;
  in the upper layer those laws are *structure fields*, supplied when the
  interface is instantiated. Nothing derives them from `A1i`.
* **A congruence licence for descent.** `deltaDescend_exists_iff` proves
  descent holds **iff** the congruence condition holds. That is a genuine
  theorem, and it is a theorem *about* the condition — it does not
  establish the condition. The germ gives no reason for it to hold.

So the ascent is not blocked by a missing proof. It is priced by two
declarations, of the same genre as the five in
`succession_declarations.md` §4.

---

## 3. Where failures live: value, pairing, composite

The failures this repository has actually paid for sort by *what the
failure lives on*, and the same three positions organize the descent
layer. These are working tags for failure analysis, not object-language
structure, and deliberately carry no imported vocabulary.

| tag | the failure lives on | apparatus instance | descent instance |
|---|---|---|---|
| **value** | one object's value | a committed report read as current | the zero predicate on a single value |
| **pairing** | two descriptions of one relation disagreeing | a population enumerated with the classifier's own pattern | congruence failing on a zero-related pair, so the two-place map does not descend |
| **composite** | two sound parts whose composition is not covered | elaboration and the axiom whitelist jointly missing a parked module | a one-place view descending while the pair does not |

The third row is the interesting one in both columns: each part is fine and
the composite is not. That is the same shape as the standing
elaboration-is-not-auditing residual, and it is why the upper layer's
obstruction results are stated about *pairs* rather than about points.

---

## 4. Why no graded structure appears for free

A graded construction of this kind needs composition as a **total,
single-valued, associative operation**. The repository declines to supply
one, and does so explicitly: `lean4/Derivation/Composing.lean` provides
composition as a three-place *relation* and refutes each guarantee
separately —

* `composition_may_fail` — not total;
* `composite_may_be_nonunique` — not single-valued;
* `skew_not_relAssoc` — not associative;
* `noneCompose_no_identity` — no identity.

That is the same obstruction class as succession: the system hands back a
relation with multiple minima where an operation was wanted, and
single-valuedness is a declaration, not a derivation. So the three tags
above stay an **analysis of failures**. They are not, and are not claimed
to be, an object-language graded structure.

`Composing.lean` is also **parked** — it elaborates but emits no
`#print axioms` report, so its axiom surface is uninspected. It is quoted
here, not leaned on.

---

## 5. What this does NOT claim

* It does **not** derive the descent layer from the germ. It itemizes two
  declarations that separate them.
* It does **not** import, restate, or name supplied vocabulary. Comparison
  against supplied material lives in `contact/`, under the protocol
  recorded there.
* It does **not** claim the germ's candidate list is complete or that any
  member is forced. They are declared candidates.
* It does **not** claim a graded complex exists, or that one is
  constructible here; §4 gives the reason it does not appear.
* It does **not** un-park `Composing.lean` or promote its theorems into
  the audited inventory.
* It introduces no counting, magnitude, observer, container, or clock.

---

## 6. Open

* Whether the two declarations in §2 are **independent**, and whether they
  are minimal for the ascent, is not proved. That would need the
  Challenge-3 treatment applied to interface declarations.
* Whether any weaker germ candidate (`A2`–`A4`) shortens the bill is not
  examined here.
