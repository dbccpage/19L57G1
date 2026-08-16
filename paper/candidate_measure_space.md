# A declared candidate space of cost measures, and what it shows at Challenge 3

Classification: **declared metatheory apparatus**, plus a **deterministic
computation** over it. No new object-language notion. No claim that the
space is complete, minimal, or initial. `AuthorityEffect: None`.

Sibling to `paper/succession_declarations.md`, whose scoped open questions
this space exists to make well-posed.

---

## 1. Domain (already fixed)

From `code/derivation/candidates.py`. A **delta** is a canonically sorted
tuple of items — `NewDatum`, `NewForm(arity)`, `NewInst(form, args)`,
`NewRuleAll(form)`. The candidate space at a regime is the set of
well-formed deltas within the declared `Bounds(max_items=2, max_arity=2)`,
the bounds the derivation already uses. A **valid response** to a target
pair separates that pair and preserves every imposed requirement.

The measure space is over **deltas**, not over regimes or histories.

---

## 2. What a measure is, and the invariance filter

A **cost measure** is a total function `mu : Delta -> C` with `C` totally
ordered, so that "minimum valid response" denotes the set of valid deltas
attaining the least value.

A measure is **presentation-independent** when `mu(delta) = mu(phi . delta)`
for every regime isomorphism `phi` — bijections on datum and form indices
preserving arities, instances, rules and requirement pairs, tokens
forgotten.

This filter is not a new structure. It is the *same declared invariance*
already enforced on demand selection, the one that rejected least-pair
selection for reading raw indices. A measure weighting by token glyphs, by
raw datum index, or by "least index in the tuple" fails it, in the same
defect class.

**Declared space.** `M` is the set of presentation-independent total
measures on the bounded candidate space; `M` is **not** claimed finite. For
computation, a declared finite slice:

| name | value on a delta |
|---|---|
| `mu1` | item count |
| `mu2` | (item count, sum of new-form arities), lex |
| `mu_type` | (n_datum, n_form, n_inst, n_rule), lex |
| `mu_arity` | (item count, sorted tuple of new-form arities), lex |

`mu1` and `mu2` are already certified in the derivation. `mu_type` and
`mu_arity` are the minimal extensions that still read only isomorphism
invariants. `M_slice = {mu1, mu2, mu_type, mu_arity}`.

---

## 3. Enumeration at Challenge 3

**[deterministic computation]**, bounds `max_items=2`, `max_arity=2`, both
admission readings. Computed by an enumeration that does **not** reuse
`engine._quotient` or `candidates.min_responses`: classes were recomputed
from `canonical()` directly, so recovering the certified `mu1` / `mu2`
figures is a control on the enumeration before its new figures are believed.

| measure | reading L | reading F | forces uniqueness? |
|---|---|---|---|
| `mu1` | 6 deltas, **3 classes** | 10 deltas, **5 classes** | no |
| `mu2` | 2 deltas, 1 class | 2 deltas, 1 class | yes, up to isomorphism |
| `mu_type` | 6 deltas, **3 classes** | 10 deltas, **5 classes** | no |
| `mu_arity` | 2 deltas, 1 class | 2 deltas, 1 class | yes, up to isomorphism |

Control: the `mu1` and `mu2` rows reproduce `CL-3-NONUNIQUE-MU1` (L 3, F 5)
and `CL-3-UNIQUE-MU2` (L 1, F 1) exactly, and the delta counts match
`valid_deltas_at_minimum` in `artifacts/challenges.json`.

---

## 4. Three things the enumeration shows that the table does not

**(a) Every valid delta within bounds costs exactly 2.** Six in reading L,
ten in reading F; there are no valid responses at cost 0 or 1. So `mu1`'s
minimum set *is* the entire valid set. Within these bounds `mu1` does not
select a minimum so much as fail to reduce, and the same holds for
`mu_type`, since every valid delta carries the type signature
`(0, 1, 1, 0)` — one new form, one new instance, nothing else.

That is a fact about the **bounds**, not about `mu1`. Outside them `mu1`
would discriminate by item count against responses of cost 3 or more,
while remaining non-unique at the floor — the arity-indexed tie family
sits at cost 2 across arities. "Fails to reduce" is confined to
`max_items=2` and is not a general property of the measure.

**(b) `mu_arity` is equivalent to `mu2` here, provably rather than by
coincidence.** Every valid delta contains exactly one `NewForm`: two forms
at cost 2 leave no room for an instance, and a form without an instance
contributes no derivable context (form-irrelevance) and so separates
nothing. The arity multiset is therefore always a one-tuple, and
`(2, (a,))` orders identically to `(2, a)`. `mu_arity` adds no
discriminating power at these bounds.

**(c) Consequently `M_slice` is four measures but only two independent
behaviours**, and the pairing is forced by (a) and (b) rather than observed:
a non-discriminating regime `{mu1, mu_type}` and an arity-discriminating
regime `{mu2, mu_arity}`. Evidence drawn from the slice must be reported as
two probes, not four. This does not change the slice's answer to scoped
open (2); it changes how much weight that answer carries.

---

## 5. "Unique up to isomorphism" is still not a successor function

Under `mu2` and `mu_arity` the single isomorphism class contains **two
concrete deltas** — mark either member of the target pair — related by the
transposition swapping the requirement pair.

So even where a measure forces uniqueness, what it forces is uniqueness of
a *class*, not of a delta. Obtaining an actual next state still requires the
representative-selection declaration that
`paper/succession_declarations.md` §4 itemizes. Uniqueness up to
isomorphism and a single-valued step are different things, and only the
former is achieved here.

---

## 6. Bearing on the scoped opens

| open (from the sibling document) | what this shows |
|---|---|
| (1) for a measure that does not itself force uniqueness, is every presentation-independent *selection rule* multivalued at the minimum? | `mu1` and `mu_type` do not force uniqueness, and their minima are multivalued (3 / 5). But **no selection rule was enumerated** — only the size of each minimum set. The open stands. |
| (2) independently of measure choice over presentation-independent measures? | Inside `M_slice`: **no** — `mu2` and `mu_arity` force uniqueness up to isomorphism. This agrees with the withdrawal already recorded in the sibling document, and is confined to two independent behaviours by §4(c). |

---

## 7. Scope, and what was not done

* Challenge 3 only: one demand, formless base, readings L and F.
* Declared bounds only (`max_items=2`, `max_arity=2`).
* `M_slice` only. **Nothing is claimed about all of `M`**, which is not
  claimed finite.
* **No selection rule was enumerated.** Multivaluedness of a minimum *set*
  is evidence against single-valued succession; it is not a theorem about
  every presentation-independent selection rule.
* No measure is added to the engine, to any runner, or to the claim ledger.
  `mu_type` and `mu_arity` exist in this analysis only; no artifact records
  them, and no gate checks the figures in §3.
* Presentation-independence of measures is **not derived**. It is the same
  declared invariance already used to reject least-pair selection.
* No carrier, clock, counting, observer, or next-state function is
  introduced.
