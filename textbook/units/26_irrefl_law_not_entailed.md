# Unit 26. Keeping positive entries does not exclude a self-pair

**Claim.** On a carrier with a point, every positive relation record has an
unrestricted extension containing a self-pair. Thus a record with no
self-pairs now does not by itself restrict every allowed extension.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Take any relation `r` on any carrier with a point `a`. There
is a relation `r'` that asserts everything `r` asserts and also asserts
`a` against itself. So `r'` extends the facts of `r` and is not
irreflexive. Thus inclusion of positive entries, by itself, cannot ensure
irreflexivity of every unrestricted extension. This is not a claim that
irreflexivity cannot be proved for a fixed, specified relation.

**Status:** derived. **Lean:**
`Bridge.irrefl_law_not_entailed` (`lean4/Derivation/Bridge.lean` lines
227-236). **Axioms:** none. **Depends on:** `Irrefl` (Unit 24), the
distinction between a law protected and a fact asserted (Unit 25).

</details>

## First pass

A **positive entry** says a pair holds. It does not say which other
pairs are forbidden. Suppose a complete table on two different points
contains exactly `P → Q`. We can check that this specified relation
has no self-pairs.

Now ask a different question: must **every extension keeping the listed
positive entries** also have no self-pairs? No. Add `P → P`. The new
relation retains `P → Q` and violates the no-self-pair condition.

| Question | Answer in this example |
|---|---|
| Is this specified record irreflexive? | Yes |
| Is every unrestricted positive extension irreflexive? | No |
| Have we specified a rule rejecting self-pair additions? | No |

This theorem answers the second question. It does not prevent proving
irreflexivity for a fixed relation or checking a complete finite table.
For two points, checking both diagonal entries absent suffices for the
fixed relation. Keeping them absent in allowed extensions requires that
additional restriction to remain in force.

The example concerns the supplied records and extension rule. It does
not establish a general claim that observation can never support a
scientific law.

## Question

Does checking irreflexivity of one relation also prove it for every
relation containing the same positive entries? What additional condition
would exclude a self-pair extension?

## What we already possess

- `Irrefl r := ∀ x, ¬ r x x`.
- `D2` is irreflexive as a fact set (`D2_irrefl`): neither point is
  related to itself (Unit 24).
- A law is something protected (Unit 25); a fact is something asserted
  (Unit 23).
- The extension condition used here: for all `x, y`, `r x y → r' x y`.
  It compares two relations on the same carrier. It does not itself
  describe an event, a history, or a restriction on future admissions.

## New concept: a fact set versus a law, separated by one extension

Given `r` and a point `a`, define `r' x y :⇔ r x y ∨ (x = a ∧ y = a)`.
Then:

- `r'` **extends** `r`: whatever `r` asserts, `r'` asserts (left
  disjunct).
- `r'` asserts `a` against itself (right disjunct, with `rfl` twice).
- So `r'` is not irreflexive.

That is the whole proof. It works for any `r` once a point is supplied;
`r` need not be finite or irreflexive. The allowed extensions in this
statement have only the inclusion condition. Adding `(a, a)` respects
that condition.

Compare three distinct claims:

1. **A property of a specified relation:** `Irrefl D2`, proved by checking
   its definition.
2. **A guarantee over every unrestricted positive extension:** for every
   `r'` containing `r`, `Irrefl r'`. The theorem refutes this guarantee
   on a carrier with a point.
3. **A restriction on allowed extensions:** only admit `r'` satisfying a
   no-self-pair condition. This is extra information about the allowed
   family, not a consequence of inclusion alone.

For a fixed two-point relation, the two negative facts `¬ r P P` and
`¬ r Q Q` do prove irreflexivity because P and Q exhaust the carrier.
The book checks this finite argument separately. Those negative facts
are more information than the positive entries preserved by the theorem.

## Plain-language interpretation

A completed table can answer “are there any self-pairs in this record?”
The answer can be proved. It does not answer “which edits will a policy
allow?” An unrestricted positive extension may add a self-pair. A policy
that excludes such additions needs an explicit condition beyond keeping
the old positive entries.

Units 23–26 now distinguish a pair being recorded, every recorded pair
having unequal ends, a map violating a selected protected property, and
restrictions on extensions. The bridge paper's fact/law distinction is
read in that scope. The theorem supplies no rule for choosing a protected
property and no mechanism for enforcing one.

The separate bridge computation reports a self-edge state after three
admissions in each of its three scenarios. It checks those scenarios;
it does not quantify over every possible admission discipline.

## Pseudocode

```
# Gloss
given any relation r on carrier α, and a point a:
  r' x y := r x y  or  (x = a and y = a)
  r' extends r:            r x y -> r' x y            (left)
  r' a a holds:            a = a and a = a            (right)
  so r' is not irreflexive.
conclusion: for no r does "r's facts" entail "Irrefl holds of every extension".
```

## Python

```python
from derivation.primdiff import D2, irreflexive, irreflexive_relations_on

ext = D2.rel | {(0, 0)}
print(irreflexive(D2.rel), irreflexive(ext), D2.rel <= ext)
rels = irreflexive_relations_on(3)
print(len(rels), all(not irreflexive(r | {(0, 0)}) for r in rels))
```

Output:

```text
True False True
64 True
```

## Line-by-line Python explanation

`D2.rel` is `{(0, 1)}`; `irreflexive` (`primdiff.py` line 61) finds no
self-pair: `True`. Add `(0, 0)`: the extension contains the original
(`<=` is subset) and is not irreflexive.

`irreflexive_relations_on(3)` (line 335) lists every irreflexive
relation on three points, all 64 subsets of the six off-diagonal pairs.
For each, adding `(0, 0)` breaks irreflexivity. The check script does
this for carriers 1, 2, 3 (1, 4, 64 fact sets) and reads the bridge
artifact: in each of the three admission scenarios the first self-edge
state is reached after 3 events (a datum, a binary form, an instance on
the diagonal), so the engine, as declared, does not enforce the law.

The Python here is illustration of a theorem that needs no computation;
Genesis's own artifact for this unit is the bridge scenario table, not an
enumeration of relations.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Bridge.lean lines 227-236
/-- Any irreflexive fact set has a bare-signature extension with a
self-edge: finite facts never entail the irreflexivity *law*.  The law is
a declared protected property, not a consequence. -/
theorem irrefl_law_not_entailed {α : Type} (r : α → α → Prop)
    (a : α) :
    ∃ r' : α → α → Prop,
      (∀ x y, r x y → r' x y) ∧ ¬ PrimDiff.Irrefl r' :=
  ⟨fun x y => r x y ∨ (x = a ∧ y = a),
   fun _ _ h => Or.inl h,
   fun hi => hi a (Or.inr ⟨rfl, rfl⟩)⟩
```

```lean
-- Lean (book), textbook/checks/u26_lean.py
def withSelf {α : Type} (r : α → α → Prop) (a : α) : α → α → Prop :=
  fun x y => r x y ∨ (x = a ∧ y = a)

theorem withSelf_extends {α : Type} (r : α → α → Prop) (a : α) :
    ∀ x y, r x y → withSelf r a x y := fun _ _ h => Or.inl h
theorem withSelf_self {α : Type} (r : α → α → Prop) (a : α) :
    withSelf r a a a := Or.inr ⟨rfl, rfl⟩
theorem withSelf_not_irrefl {α : Type} (r : α → α → Prop) (a : α) :
    ¬ Irrefl (withSelf r a) := fun hi => hi a (withSelf_self r a)

/-- No relation on Bool has only irreflexive unrestricted extensions. -/
theorem no_facts_entail_law :
    ¬ ∃ r : Bool → Bool → Prop,
      ∀ r' : Bool → Bool → Prop, (∀ x y, r x y → r' x y) → Irrefl r' :=
  fun ⟨r, h⟩ =>
    (irrefl_law_not_entailed r false).elim fun r' ⟨hsub, hni⟩ => hni (h r' hsub)
```

## Line-by-line Lean explanation

**The statement.** For any carrier `α`, relation `r` and point `a`,
there exists `r'` with two properties: it extends `r`, and it is not
irreflexive. The point `a` is needed only to have somewhere to put the
self-edge; on an empty carrier the law would hold vacuously of every
relation, and the theorem asks for a point.

**The witness** `fun x y => r x y ∨ (x = a ∧ y = a)`: `r` with the one
pair `(a, a)` added.

**Extension** `fun _ _ h => Or.inl h`: given `h : r x y`, the left
disjunct proves `r' x y`.

**Not irreflexive** `fun hi => hi a (Or.inr ⟨rfl, rfl⟩)`: assume
`hi : Irrefl r'`; at the point `a` it says `¬ r' a a`; but `r' a a` holds
by the right disjunct with both equations `rfl`. `False`.

**The book's `no_facts_entail_law`.** The strong form of the claim: there
is no relation on `Bool` whose facts force the law on every extension.
Assume such an `r` with its guarantee `h`. Genesis's theorem at `r` and
`false` gives an extension `r'` with `hsub` (extends) and `hni` (not
irreflexive); `h r' hsub : Irrefl r'` contradicts `hni`. The carrier is
fixed to `Bool` only to supply the point; any inhabited carrier works
the same way.

**`law_is_extra` (book).** Side by side: under `Irrefl r`, every asserted
pair is unequal (Unit 24); for any `r` with a supplied point, some
unrestricted extension is not irreflexive. Both halves are Genesis
theorems. The second half has no asserted-pair premise. A self-pair,
when present, already disproves irreflexivity of its relation.

**Axioms.** None, for every theorem in this unit, Genesis and book.

## What has been proved

- Every relation on a pointed carrier has a non-irreflexive extension
  (Genesis, derived).
- Hence no relation on `Bool` has only irreflexive unrestricted positive
  extensions (book, as a negated existence).
- On `D2`: irreflexive as facts, with a named non-irreflexive extension
  that keeps the witness (book).
- Two diagonal absences suffice to prove irreflexivity for a fixed
  relation on `Bool`; the inequality relation is irreflexive by its
  definition; every relation on `Empty` is irreflexive (book).
- In the admission engine, a self-edge state is reachable in three
  events in every studied scenario (Genesis, verified finite).

## What has not been proved

- That the no-self-pair restriction should or should not be adopted.
  Units 24 and 25 explain particular consequences of using it.
- That irreflexivity of a fixed relation is unprovable. `D2_irrefl`, a
  complete finite diagonal check, and the definition `r x y := x ≠ y`
  each supply proofs in their stated settings.
- That a family of constrained extensions cannot preserve the property.
  Such a family has conditions beyond the positive inclusion used here.
- A general claim about how scientific laws are justified. The theorem
  contains no measurements, model-fitting procedure, or prediction rule.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `∃ r' : α → α → Prop` | the extension | metatheory quantification over relations |
| `Or.inl`, `Or.inr`, `rfl` | the proof | metatheory logic |
| `Irrefl` | the property | a predicate on a relation; requiring it of allowed extensions is separate |
| the point `a` | somewhere to put the self-edge | metatheory; the theorem is about inhabited carriers |

**What the model contains.** A carrier and relations compared by
inclusion of positive pairs. A protected property can be specified in
the separate obstruction definition. This theorem neither assigns a
price nor performs an admission or a rejection.

**Phrases to read with care.**

- "Irreflexive as a fact" concerns the specified relation. A protected
  restriction concerns the allowed family of extensions. On a carrier
  with a point, that family cannot include every positive extension
  while also requiring all its members to be irreflexive.
- "Finite facts" in the docstring is not a restriction the proof uses;
  the proof works for any `r`. The word records that the facts a
  history admits are finitely many.

## Student exercise

Why does the theorem need the point `a`? State what happens on the
empty carrier, and whether the claim "the law is not entailed" survives
there under the same unrestricted-extension reading.

## Answer

<details>
<summary>Worked answer</summary>

On the empty carrier every relation is irreflexive, vacuously:
`∀ x, ¬ r x x` has nothing to check. So every extension of any relation
is irreflexive, and the law *is* entailed, trivially. The theorem's
hypothesis `(a : α)` excludes exactly this case. The claim survives in
the form Genesis proves: on a carrier with a supplied point, every
relation has a non-irreflexive positive extension. Empty carriers have
no place to put the added self-pair and are explicitly outside that
statement.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Bridge.lean` lines 227-236; `PrimDiff.lean` line 28 (`Irrefl`), 106-110 (`D2_irrefl`) |
| Axiom report | `artifacts/lean_axioms.txt`: `Bridge.irrefl_law_not_entailed` does not depend on any axioms |
| Paper | `paper/bridge_provenance.md` B5 ("Irreflexivity: fact versus law"), B7 provenance table row "irreflexivity: as-fact constructible; as-law declared only", B8 countermodel index "self-edge extension of any fact set"; `paper/native_derivation_map.md` row "irreflexivity fact entails irreflexivity law: FALSE" |
| Ledger | No `CL-*` entry names this theorem; the bridge paper's B5 and B7 carry it, and the claim ledger's bridge entries cite the provenance table |
| Artifact | `artifacts/bridge.json`, `scenarios[*].min_events_to.self_edge = 3` for `single_dedup`, `two_dedup`, `occurrence`; `provenance_table` |
| Test | `tests/test_bridge.py::test_provenance_table_covers_all_ingredients`, `::test_classify_shapes` |
| Check (Python) | `python textbook/checks/u26_irrefl_law.py`: `D2` and its extension; 69 irreflexive fact sets on carriers 1 to 3 with self-pair extensions; the three bridge scenarios' self-edge depth; 16 complete two-point relations and both diagonal checks; 8 positive extensions of `D2`, of which 2 are irreflexive |
| Check (book Lean) | `python textbook/checks/u26_lean.py`: twelve book reports plus the Genesis result kernel-checked, Lean 4.33.0, including finite negative checks, the inequality relation, and the empty carrier; no axioms anywhere |
