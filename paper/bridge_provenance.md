# The Bridge: Provenance of the Primitive Difference Ingredients

**Question.**  Can the opaque inscription be elaborated into a witnessed
irreflexive datum, or which components must be externally admitted?

**Verdict up front (the bridge does not close silently).**  The
inscription elaborates into *none* of the six ingredients.  Each has a
theorem-level provenance boundary or a bounded computed price under the
declared event alphabet; and under that external admission alphabet, a
single deduplicated datum can support only a *diagonal* binary witness
(a self-edge) — the exact degenerate countermodel that the
primitive-difference layer excludes.  The form and instance of that
self-edge remain externally admitted; nothing is derived from the
inscription itself.
The gap between `<>` and the witnessed irreflexive datum is therefore
real, priced, and now explicitly itemized rather than silently filled by
the metatheory.

**Protocol.**  Constructive analysis first; comparisons at the end.
Lean: `lean4/Derivation/Bridge.lean` — this module deliberately imports
*both* prior developments (the admission model and the
primitive-difference layer), because the question is exactly the bridge
between them.  Python: `code/derivation/bridge.py`, artifact
`artifacts/bridge.json` — exhaustive reachability over bounded admission
histories (event alphabet: supplies/admissions of the declared tokens,
one binary form, all binary instances over two indices; all statements
scoped to that alphabet and to histories of at most 7 events).
Statement tags as in the companion papers.

---

# FORMAL SPINE

## B1. The three admission scenarios

**[declared metatheory]**  Scenario `single_dedup`: one opaque token
under the first development's presentation-identity dedup.  Scenario
`two_dedup`: a second, externally supplied distinct token.  Scenario
`occurrence`: one opaque token under a *declared* occurrence-admission
discipline (admission always appends; occurrences are distinguished only
by metatheoretic position — a flagged import, B4).

**[finite computation]** (`artifacts/bridge.json`, scenarios; 7-event
horizon):

| scenario | states | max carrier | carrier 2 | binary form | oriented witness | symmetric witness | self-edge |
|---|---|---|---|---|---|---|---|
| single_dedup | 20 | **1** | never | 1 event | **never** | **never** | 3 events |
| two_dedup | 130 | 2 | 2 | 1 | 4 | 5 | 3 |
| occurrence | 69 | 2 | 2 | 1 | 4 | 5 | 3 |

## B2. Carrier and two-ness

**[theorem]** (`single_token_carrier_bound`, via
`stepT_preserves_atMostTok`)  One opaque inscription never yields a
carrier of size two: any history whose datum admissions all carry the
same token leaves at most one admitted datum — regardless of how often
the inscription is re-supplied or re-admitted.

**[theorem]** (`second_token_required`)  Contrapositive, witness-
producing form: a state with two admitted data comes only from a history
that admits some token *different* from the first.  Two-ness is
externally purchased.

**[finite computation]**  The `occurrence` scenario shows the *declared*
alternative: an occurrence-admission discipline reaches carrier 2 from
one token at the same event cost as a second token.  Its price is B4.

## B3. Relation, witness, and the self-edge boundary

**[theorem]** (`no_admitForm_no_forms`)  Histories without a form
admission never have a form: nothing derives a relation symbol.

**[theorem]** (`no_forms_no_witness`)  With an empty form table no
instance is admissible: the witness presupposes the externally admitted
relation.

**[finite computation]**  Sharpest single-token fact: within the
declared alphabet and horizon, **given a single deduplicated datum,
every admitted binary witness is necessarily a self-edge** (externally
admitted form + externally admitted diagonal instance, 3 admissions).
Nothing here is derived from the inscription itself — the form and
instance are external events of the declared alphabet; the point is
that with one deduplicated datum they can only ever land on the
diagonal.  This is precisely the one-point self-difference that the
primitive-difference layer proved consistent (`selfdiff_consistent`)
and then excluded by the irreflexivity commitment: the degenerate case
is not an artifact of the earlier paper, it is the only witness shape a
single-datum carrier supports.

## B4. Occurrences, designation, and the position import

**[theorem]** (`no_swap_fixed_offdiag_pair`)  On the symmetric
two-element state no ordered off-diagonal pair is swap-fixed: an
equivariant *ordered designation* does not exist.  Unordered two-ness is
swap-invariant; naming a first and a second element is not.

**[declared metatheory / flagged import]**  In the `occurrence`
scenario the two occurrences of `<>` are distinguished by nothing except
their metatheoretic positions in the history.  Any use of "the first
occurrence" as object-level data imports the metatheory's identity of
positions — the same import the primitive-difference layer isolated as
A3.  The discipline is admissible, but the import must be declared, and
this paper declares it rather than filling it silently.

## B5. Irreflexivity: fact versus law

**[theorem]** (`irrefl_law_not_entailed`)  Every irreflexive fact set
has a bare-signature extension with a self-edge: finite facts never
entail the irreflexivity *law*.  The law — the protected property `P`
of `FidelityObstruction` — is a declaration, never a derivation.

**[finite computation]**  Self-edges remain reachable in every scenario
(3 events): no admission discipline studied forbids them; only a
declared protected law does.

## B6. Orientation: metatheoretically free, objectually priced

**[theorem]** (`equivariant_witness_is_S2`)  Any swap-invariant,
irreflexive-as-fact, inhabited relation on the two-element carrier *is*
the symmetric pair: an equivariant (choice-free) introduction rule can
reach `S2` and nothing else.

**[theorem]** (`equivariant_not_D2`)  In particular no equivariant
introduction yields the oriented datum.

**[finite computation]** (`equivariant_scan`)  Of the 16 relations on
the two-element carrier, exactly 4 are swap-invariant, and exactly one
is irreflexive-as-fact and inhabited: the symmetric pair.

**[theorem]** (`order_visible_to_metatheory`,
`order_erased_at_object_level`)  Admission order is present in the token-aware state (the two admission orders produce different token
lists) and erased by token erasure (both orders have identical
object-level states).  A metatheoretic orientation exists *for free*;
internalizing it as object-level asymmetry requires an admitted
asymmetric fact — which is the oriented witness itself, hence external
by `equivariant_not_D2`.

## B7. The provenance table (terminal result)

**Terminal statement, scoped to the declared alphabet, horizon, and the
studied disciplines:**

> **The opaque inscription cannot be elaborated into a witnessed
> irreflexive datum.  Every ingredient is externally admitted, declared,
> or metatheory-only:**

| ingredient | verdict | mechanism | evidence |
|---|---|---|---|
| carrier (size 1) | externally admitted | retention of the inscription; reading-dependent (L/F underdetermination of the first development) | scenario table |
| carrier (size 2) | **not derivable** from one inscription | second distinct token (external), or declared occurrence discipline importing metatheoretic position | `single_token_carrier_bound`, `second_token_required`; scenarios |
| two designated occurrences | externally admitted / declared | designation is an act; no equivariant ordered designation exists | `no_swap_fixed_offdiag_pair`; `equivariant_scan` |
| relation (form) | externally admitted | nothing derives a signature | `no_admitForm_no_forms` |
| witness (instance) | externally admitted (oriented); a declared equivariant rule reaches only `S2` | instances presuppose the form; equivariance obstruction | `no_forms_no_witness`, `equivariant_witness_is_S2`, `equivariant_not_D2` |
| irreflexivity | as-fact constructible; **as-law declared only** | finite facts never entail the law | `irrefl_law_not_entailed` |
| orientation | metatheoretically free (admission order), erased at object level; object-level orientation externally admitted | order-erasure pair of theorems; internalization = the oriented witness itself | `order_visible_to_metatheory`, `order_erased_at_object_level` |

**Minimum state-changing admission count under the predeclared-token
alphabet** for the full witnessed irreflexive datum: two datum
admissions (the second requiring the predeclared distinct token, or the
occurrence declaration), one form admission, one instance admission —
four admissions to the oriented datum, five to the symmetric one.  The
search predeclares its token alphabet and does not require a `Supply`
before an `AdmitDatum`, so this is an admission count, not a full
external-interaction budget; on top of it sit the declared
irreflexivity law and (for `D2`) the orientation choice that no
equivariant rule can make.

## B8. Countermodel index

| countermodel / boundary | shows | where |
|---|---|---|
| every single-token history (exhaustive to 7 events) | carrier 2, oriented and symmetric witnesses unreachable | scenario `single_dedup`; `single_token_carrier_bound` |
| self-edge state at 3 admissions | a single deduplicated datum supports only the diagonal witness (form and instance externally admitted) | scenario table; `selfdiff_consistent` (companion) |
| self-edge extension of any fact set | irreflexivity-as-law underivable | `irrefl_law_not_entailed` |
| the 4 swap-invariant relations | equivariant introduction reaches only `S2` | `equivariant_scan`; `equivariant_witness_is_S2` |
| the two admission orders | orientation free in metatheory, erased at object level | `order_visible_to_metatheory` / `order_erased_at_object_level` |

## B9. Unresolved obligations

* **[unresolved]** All reachability statements are scoped to the
  declared event alphabet (one binary form, binary instances over two
  indices) and the 7-event horizon; the Lean carrier-bound and
  form-inertia theorems are horizon-free, but a horizon-free Lean
  statement of "only the self-edge witness is single-token reachable"
  is open (it requires the instance-index bound as a lemma).
* **[unresolved]** The occurrence discipline's position import is
  flagged, not formalized: a Lean model of occurrence-admission with an
  explicit position-identity axiom, making the import checkable, is
  open.
* **[unresolved]** Equivariance was analyzed for the swap on the
  two-element carrier; a general statement over all carrier
  automorphism groups (derived introductions land in the invariant
  sublattice) is conjectured in F1 and unproved.
* **[unresolved]** Whether some *weaker* external act than a second
  distinct token (e.g. a supply-failure signal, a refusal event) could
  purchase two-ness — the alphabet studied contains no such acts.

---

# FRONTIER CONJECTURES

**F1. The invariance ceiling.**  *Conjecture:* for every carrier and
every admitted-state automorphism group `G`, anything a choice-free
(equivariant) rule introduces lies in the `G`-invariant sublattice; the
reachable-by-declaration objects are exactly the invariants, and every
non-invariant target (orientation being the first) has an irreducible
choice cost of one external act per broken symmetry generator.  Evidence:
proved for the swap on two elements; the general statement would make
"external act" a measurable quantity (choice per generator).

**F2. Occurrence positions as proto-numerals, sharpened.**  The
occurrence scenario reaches two-ness by importing positions.
*Conjecture:* the minimal admission discipline that makes the position
import *internal* (admitting occurrence-successor as an object judgment)
is exactly a successor structure, and its carrier-growth histories are in
bijection with numerals — the companion F2 conjecture now has a concrete
candidate discipline to formalize.

**F3. Refusal as a difference source.**  B9's last obligation suggests a
genuinely new question: a *failed* dedup (re-admission answered by
designation rather than growth) is itself an event the metatheory can
see.  *Conjecture:* an admission discipline that internalizes refusal
("this supply changed nothing") as an admitted judgment yields a second
object-level distinguishable state from one token — potentially buying
two-ness from the inscription plus its own repetition-refusal, at the
price of admitting the discipline's self-description.  If true, the
carrier-2 verdict weakens from "second token required" to "second token
or reflective refusal required"; if false, the refusal judgment is
provably uninformative.  Either outcome is a theorem target.

**F4. The order-erasure tower.**  Admission order is the third
metatheoretic shadow found (after multiplicity and orientation in the
companion): present in the token-aware state, erased at the object
level.  *Conjecture:* the erasure maps of the three shadows compose into
a single forgetful tower (positions → multiplicities → orientations →
symmetrized presence), and each rung's section (re-adding the data) is
exactly one external act.  This would unify the companion's forgetting
tower with the provenance prices found here.

---

# Post-hoc comparison with existing names

*(End-only, as before.)*

* The carrier-bound theorem is a token-level pigeonhole: with dedup, the
  admitted set is the image of the supplied token set, so one token
  bounds the carrier — the observation parallels the standard fact that
  quotienting a singleton generates nothing new.
* The fact/law split for irreflexivity is the finite shadow of the
  distinction between a diagram's properties and a theory's axioms
  (satisfaction now versus closure under extensions); the self-edge
  extension is the one-step failure of inductive generalization.
* The equivariance obstruction is a baby case of definability-by-
  invariance: choice-free constructions land in the fixed sublattice of
  the symmetry group, so symmetry-breaking data cannot be defined, only
  chosen — the same mechanism as the companion's classifier gap, now
  applied to *introduction* rather than *observation*.
* The order-erasure pair mirrors the first development's
  presentation/internal identity split: admission order is presentation
  data; token erasure is precisely the forgetful functor that the
  earlier erasure simulation made exact.
* Relative to the first development: its Challenge history purchased the
  ingredients in exactly the order and at exactly the prices tabulated
  here — second token at Challenge 1-2 (external supply), relation and
  witness at Challenge 3 (external requirement), fidelity as persistent
  external demands rather than an internal law, orientation never
  purchased (its separability is symmetric, matching
  `equivariant_witness_is_S2`).  The bridge table retrodicts the
  earlier derivation's shape, which is evidence the provenance analysis
  carves the right joints.
