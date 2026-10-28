# Unit 26. Facts never entail the irreflexivity law

**Claim.** Take any relation `r` on any carrier with a point `a`. There
is a relation `r'` that asserts everything `r` asserts and also asserts
`a` against itself. So `r'` extends the facts of `r` and is not
irreflexive. Hence no set of asserted facts, however many and however
irreflexive as facts, entails irreflexivity as a *law*: the law is a
declaration, never a consequence. **Status:** derived. **Lean:**
`Bridge.irrefl_law_not_entailed` (`lean4/Derivation/Bridge.lean` lines
227-236). **Axioms:** none. **Depends on:** `Irrefl` (Unit 24), the
distinction between a law protected and a fact asserted (Unit 25).

## Question

Units 24 and 25 did real work with irreflexivity: it turned a witness
into a distinction and a merge into an obstruction. Could the law itself
be *earned*? If a structure's asserted facts are all irreflexive, has it
thereby committed to irreflexivity, so that a self-edge would be a
contradiction rather than a new fact?

## What we already possess

- `Irrefl r := ∀ x, ¬ r x x`.
- `D2` is irreflexive as a fact set (`D2_irrefl`): neither point is
  related to itself (Unit 24).
- A law is something protected (Unit 25); a fact is something asserted
  (Unit 23).
- The admission model: a history admits facts one at a time, and nothing
  admitted can later be withdrawn (Units 03, 06).

## New concept: a fact set versus a law, separated by one extension

Given `r` and a point `a`, define `r' x y :⇔ r x y ∨ (x = a ∧ y = a)`.
Then:

- `r'` **extends** `r`: whatever `r` asserts, `r'` asserts (left
  disjunct).
- `r'` asserts `a` against itself (right disjunct, with `rfl` twice).
- So `r'` is not irreflexive.

That is the whole proof. Its force is in the quantifiers: *any* `r`,
including an irreflexive one, including one with a million edges all
irreflexive. Irreflexivity-as-fact ("no self-edge so far") is true of
`D2`; irreflexivity-as-law ("no self-edge can be asserted") is not a
consequence of any facts, because the facts are always consistent with
one more self-edge. In the bare signature, assertions only ever add.

## Plain-language interpretation

A ledger has never recorded a thing as differing from itself. Does that
make "nothing differs from itself" a rule of the ledger? No. The next
entry can be a self-difference, and nothing already written contradicts
it. For the rule to hold it must be *imposed*, from outside the entries.
That is what Genesis means when it writes, in the bridge paper, that the
law "is a declaration, never a derivation".

This closes the loop of Units 23 to 26. The bare assertion gives no
distinctness (23). The law gives distinctness (24) and obstruction (25).
And the law is not for sale inside the system: it has to be brought in
(26). The provenance table of the bridge paper records exactly this
verdict for the irreflexivity ingredient: constructible as a fact,
declared only as a law.

The finite computation beside it says the same about the admission
engine: in every studied scenario a self-edge state is reachable after
three admissions. No admission discipline studied forbids it; only a
declared protected property could.

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

/-- No fact set on an inhabited carrier has the law as a consequence. -/
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

**`law_is_extra` (book).** Side by side: from a witness *and the law*,
distinctness (Unit 24); from the witness alone, an extension that breaks
the law (this unit). Both halves are Genesis theorems; the book only
places them next to each other.

**Axioms.** None, for every theorem in this unit, Genesis and book.

## What has been proved

- Every relation on a pointed carrier has a non-irreflexive extension
  (Genesis, derived).
- Hence no fact set entails the law on its extensions (book, as a
  negated existence on `Bool`).
- On `D2`: irreflexive as facts, with a named non-irreflexive extension
  that keeps the witness (book).
- In the admission engine, a self-edge state is reachable in three
  events in every studied scenario (Genesis, verified finite).

## What has not been proved

- That the law should not be adopted. The theorem says it cannot be
  derived from facts; Units 24 and 25 say what it buys once adopted. The
  decision is the metatheory's, and Genesis records it as such.
- That there is no *other* route to the law: a signature with negative
  facts ("`a` is not related to `a`" as an admitted assertion), or with a
  closure operation, is a different system. Genesis's bare signature
  has positive assertions only, and the theorem is about that.
- That the ban on `xrx` in the sibling repositories' seed prompts is
  this law. It is a declared constraint of a different model, admitted
  there as a sentence; this theorem is one reason it had to be admitted
  rather than derived, but the book does not identify the two.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `∃ r' : α → α → Prop` | the extension | metatheory quantification over relations |
| `Or.inl`, `Or.inr`, `rfl` | the proof | metatheory logic |
| `Irrefl` | the law | declared protected property; this unit shows it is not entailed |
| the point `a` | somewhere to put the self-edge | metatheory; the theorem is about inhabited carriers |

**What the system holds.** Facts. Never the law, unless it is admitted
from outside as a protected property. After Unit 26 the status of
irreflexivity in Genesis is settled: a priced admission, in the finitude
rule's terms, not a derivation.

**Phrases to read with care.**

- "Irreflexive as a fact" (true of `D2`) and "irreflexive as a law"
  (`Irrefl` protected under every extension) are different claims. The
  bridge paper's provenance table keeps them in separate cells.
- "Finite facts" in the docstring is not a restriction the proof uses;
  the proof works for any `r`. The word records that the facts a
  history admits are finitely many.

## Student exercise

Why does the theorem need the point `a`? State what happens on the
empty carrier, and whether the claim "the law is not entailed" survives
there.

## Answer

On the empty carrier every relation is irreflexive, vacuously:
`∀ x, ¬ r x x` has nothing to check. So every extension of any relation
is irreflexive, and the law *is* entailed, trivially. The theorem's
hypothesis `(a : α)` excludes exactly this case. The claim survives in
the form Genesis states it: on every carrier with a point, facts do not
entail the law. A carrier with a point is also the only kind in which a
law about points says anything.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Bridge.lean` lines 227-236; `PrimDiff.lean` line 28 (`Irrefl`), 106-110 (`D2_irrefl`) |
| Axiom report | `artifacts/lean_axioms.txt`: `Bridge.irrefl_law_not_entailed` does not depend on any axioms |
| Paper | `paper/bridge_provenance.md` B5 ("Irreflexivity: fact versus law"), B7 provenance table row "irreflexivity: as-fact constructible; as-law declared only", B8 countermodel index "self-edge extension of any fact set"; `paper/native_derivation_map.md` row "irreflexivity fact entails irreflexivity law: FALSE" |
| Ledger | No `CL-*` entry names this theorem; the bridge paper's B5 and B7 carry it, and the claim ledger's bridge entries cite the provenance table |
| Artifact | `artifacts/bridge.json`, `scenarios[*].min_events_to.self_edge = 3` for `single_dedup`, `two_dedup`, `occurrence`; `provenance_table` |
| Test | `tests/test_bridge.py::test_provenance_table_covers_all_ingredients`, `::test_classify_shapes` |
| Check (Python) | `python textbook/checks/u26_irrefl_law.py`: `D2` and its extension; 69 irreflexive fact sets on carriers 1 to 3, each with a non-irreflexive extension containing it; the three bridge scenarios' self-edge depth |
| Check (book Lean) | `python textbook/checks/u26_lean.py`: nine book theorems plus the Genesis theorem kernel-checked, Lean 4.33.0; no axioms anywhere |
