# Unit 27. The abstraction barrier

**Claim.** A fixed function receiving only a group label must return the
same answer for inputs with the same label. To use a distinction that
the label does not retain, it needs different input or a different grouping.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** If an abstraction identifies two cases, no operation defined only
on that abstraction can tell them apart: for any relation `rel` on a type
and any function `f` out of the quotient by `rel`, `rel a b` gives
`f ⟦a⟧ = f ⟦b⟧`. Instantiated at Challenge 2: in `R2L`, where `⟨a⟩` and
`⟨ab⟩` are collapsed, every function defined on the collapse classes
returns one value on both.

**Status:** derived. **Lean:**
`Derivation.quotient_barrier` (`lean4/Derivation/Quot.lean` lines 17-20),
`quot_barrier` (23-26), `collapseRel` (31), `barrier_R2L` (33-35).
**Axioms:** `Quot.sound` for the two general theorems; `propext,
Quot.sound` for the instance, inherited through `R2L_collapsed`.
**Depends on:** `collapsed` (Unit 08), `R2L_collapsed` (Unit 16).

</details>

## First pass

Suppose two cards, P and Q, both have the color blue. Group the cards
by color and pass only the group label `blue` to a function. The
function receives the same input for P and Q, so it returns the same
answer. It cannot answer a question about their different shapes from
that label alone.

The grouping is called a **quotient**. The theorem concerns one fixed
function whose input is only the quotient value. Reading the original
card, changing the grouping, or adding another input changes the question.

**Predict:** if one function gives the same answer on two cards, must
their complete records be identical?

<details>
<summary>Check your prediction</summary>

No. A function returning only the number of positive tests can give
equal counts while the positive tests themselves differ. The Python
link example below checks this.

</details>

The [Map lab](../map_lab/README.md) builds consistent grouping and
recovering answers from a group step by step. The formal section below
also distinguishes an equivalence relation from arbitrary generating
relations.

## Question

The paper's required question 5 (`paper/paper.md` §10) asks: if a current
abstraction identifies two cases that a declared task requires to be
separate, can any operation defined only on that abstraction recover the
distinction? Genesis answers no. Why is that a theorem and not a remark,
what exactly does "defined only on that abstraction" rule in and out, and
what does it say about Challenge 3, where the distinction is in fact
recovered?

## What we already possess

- `collapsed r d d'`: every well-formed context treats `d` and `d'` alike
  (Unit 08).
- `R2L = ⟨2, [], [], [], [(0, 1)]⟩`, the Challenge 2 regime in reading L:
  two data, no forms, no instances, and the imposed demand `(0, 1)`.
  `Derivation.R2L_collapsed : collapsed R2L 0 1` (Unit 16): with no
  instances, nothing separates the two data.
- The engine's own quotient, by isomorphism: `canonical` gives one key to
  isomorphic regimes (Unit 21).

## New concept: a quotient type, and the one axiom that governs it

Lean can build a new type out of an old one and a relation. Given a type
`α` and a relation `rel : α → α → Prop`, `Quot rel` identifies related
elements. Equality of quotient values also identifies chains of related
elements, their reverses, and each element with itself. For an arbitrary
`rel`, this can identify more pairs than `rel` itself contains. The
book's chain example has `0 rel 1` and `1 rel 2` but not `0 rel 2`;
the classes of 0 and 2 are nevertheless equal.

Three constructions used here are:

- `Quot.mk rel a : Quot rel` is the class of `a`;
- `Quot.sound : rel a b → Quot.mk rel a = Quot.mk rel b` is an axiom:
  related elements have one class. It is one of the two axioms Genesis
  permits (the other is `propext`);
- `Quot.lift g h : Quot rel → β` builds a function out of the quotient
  from a function `g : α → β` and a proof `h` that `g` gives equal values
  on related elements.

`Setoid α` is a relation packaged with a proof that it is an equivalence;
`Quotient s` is `Quot` for a setoid, and `a ≈ b` is its relation. Genesis
proves the barrier in both forms and uses the raw `Quot` form, which asks
for no equivalence proof.

One more piece: `congrArg f : x = y → f x = f y`. A function applied to
equal inputs gives equal outputs. That is the whole proof.

## Plain-language interpretation

For a fixed grouping, equal group values supply equal inputs to a fixed
function. Its outputs must therefore agree. The theorem does not depend
on how that function was written. It does not classify every process
with changing state, random inputs, or additional observations.

The word "only" carries the weight. A procedure that reads the original
things is not bound. In Genesis's terms, a procedure that reads the
presentation tokens `<a>` and `<ab>` sees two strings, but the regime's
observational content, the profiles, is the same empty set for both. If a
task needs the difference, a function receiving only that same class
value cannot supply it. Meeting Challenge 3's declared separation task
requires admitted structure visible to a context (Units 16–22). The
theorem does not cause that admission or select a response.

## Pseudocode

```
# Gloss
given: a relation rel on things, and a function f whose input is a class
given: rel a b
step 1: class(a) = class(b)          -- Quot.sound: related things share a class
step 2: f(class(a)) = f(class(b))    -- congrArg: equal inputs, equal outputs
```

## Python

This Python model represents grouping with profiles and canonical keys.
Equal complete profiles represent the same collapse group at a fixed
regime; equal canonical keys represent the same implemented isomorphism
class. These are different groupings. A function reading only the profile
agrees on `<a>` and `<ab>` in this example; a function reading their tokens
can distinguish them.

```python
from derivation.iso import canonical, rename
from derivation.model import AdmitDatum, Impose, replay
from derivation.observe import collapsed_pairs, profile

r2l = replay([AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(0, 1)])
print(collapsed_pairs(r2l), profile(r2l, 0) == profile(r2l, 1))
print(len(profile(r2l, 0)), len(profile(r2l, 1)), r2l.data[0], r2l.data[1])
swapped = rename(r2l, (1, 0), ())
print(canonical(r2l) == canonical(swapped))
```

Output:

```text
((0, 1),) True
0 0 <a> <ab>
True
```

## Line-by-line Python explanation

`replay([...])` builds `R2L`: two data with their tokens, then the demand
`(0, 1)` imposed. The demand may be imposed on a collapsed pair; the regime
then fails to satisfy it (Unit 16).

`collapsed_pairs(r2l)` returns `((0, 1),)`: the one pair is collapsed.
`profile(r2l, 0) == profile(r2l, 1)` is `True`: with no forms there are no
contexts, so both profiles are the empty set.

`len(profile(r2l, d))` is a function that reads only the class. It returns
`0` on both data. `r2l.data[d]` reads the presentation token, which is not
part of the class: `<a>` and `<ab>` differ. The first function is bound by
the barrier, the second is not defined on the abstraction at all.

`rename(r2l, (1, 0), ())` swaps the two data (the empty tuple is the form
permutation; there are no forms). `canonical` is the engine's quotient by
isomorphism: the keys are equal. A fixed function receiving only that
key agrees on both. A computation using other inputs needs its own scope
check; equality of keys does not assert equality of every recorded field.

The check also builds the binary link of Unit 19. Both data have exactly
one positive context, but the contexts differ and the pair is separable.
Equal values of the coarse summary `len(profile)` do not establish equal
complete profiles. The barrier is a one-way implication for each function.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/Quot.lean lines 15-35
/-- Operations defined only on a quotient cannot separate identified
elements. -/
theorem quotient_barrier {α : Sort u} {β : Sort v} (s : Setoid α)
    (f : Quotient s → β) {a b : α} (h : a ≈ b) :
    f (Quotient.mk s a) = f (Quotient.mk s b) :=
  congrArg f (Quotient.sound h)

/-- The same barrier for raw quotients by an arbitrary relation. -/
theorem quot_barrier {α : Sort u} {β : Sort v} (rel : α → α → Prop)
    (f : Quot rel → β) {a b : α} (h : rel a b) :
    f (Quot.mk rel a) = f (Quot.mk rel b) :=
  congrArg f (Quot.sound h)

/-- Instantiation to the derivation: identify observationally collapsed
data of a fixed regime; any operation defined on the collapse classes gives
equal outputs on `<a>` and `<ab>` in the Challenge 2/3 regime. -/
def collapseRel (r : Regime) (d d' : Nat) : Prop := collapsed r d d'

theorem barrier_R2L {β : Sort v} (f : Quot (collapseRel R2L) → β) :
    f (Quot.mk _ 0) = f (Quot.mk _ 1) :=
  quot_barrier (collapseRel R2L) f R2L_collapsed
```

The book's Lean names the two steps, shows that a function on the raw
carrier is under no barrier, builds a descended function with `Quot.lift`
and applies the barrier to it, and instantiates the reading-F regime.

```lean
-- Lean (book), textbook/checks/u27_lean.py
theorem quot_barrier' {α : Sort u} {β : Sort v} (rel : α → α → Prop)
    (f : Quot rel → β) {a b : α} (h : rel a b) :
    f (Quot.mk rel a) = f (Quot.mk rel b) := by
  have hq : Quot.mk rel a = Quot.mk rel b := Quot.sound h
  exact congrArg f hq

theorem raw_function_separates : (fun n : Nat => n) 0 ≠ (fun n : Nat => n) 1 := by
  decide

def descend (g : Nat → Bool) (hg : ∀ a b, collapseRel R2L a b → g a = g b) :
    Quot (collapseRel R2L) → Bool :=
  Quot.lift g hg

theorem descend_agrees (g : Nat → Bool)
    (hg : ∀ a b, collapseRel R2L a b → g a = g b) :
    descend g hg (Quot.mk _ 0) = descend g hg (Quot.mk _ 1) :=
  barrier_R2L (descend g hg)

theorem barrier_R2F {β : Sort v} (f : Quot (collapseRel R2F) → β) (d d' : Nat) :
    f (Quot.mk _ d) = f (Quot.mk _ d') :=
  quot_barrier (collapseRel R2F) f (R2F_collapsed d d')
```

## Line-by-line Lean explanation

**`quotient_barrier`.** `{α : Sort u} {β : Sort v}` are any two types, at
any universe level; the braces mean Lean infers them. `(s : Setoid α)` is
an equivalence relation on `α`. `(f : Quotient s → β)` is the operation,
defined on the quotient. `{a b : α} (h : a ≈ b)` are two related elements.
The conclusion is that `f` agrees on their classes. The proof:
`Quotient.sound h` turns the relation into the equation `Quotient.mk s a =
Quotient.mk s b`, and `congrArg f` applies `f` to both sides.

**`quot_barrier`.** The same with a bare relation `rel` and the raw
quotient `Quot rel`. `Quot.sound` is the axiom; `Quotient.sound` above is
the same axiom seen through the setoid.

**`collapseRel`.** A name for "collapsed in `r`", so that it can stand as
the relation of a quotient. It is a definition, not an equivalence proof.
The native construction needs no such proof because `Quot` accepts any
generating relation. The book separately packages collapse as a setoid.

**`barrier_R2L`.** Take any `f` out of the quotient of the data of `R2L`
by collapse. Then `f` agrees on the classes of `0` and `1`. The proof is
`quot_barrier` applied to the relation, to `f`, and to `R2L_collapsed :
collapsed R2L 0 1`, which Lean accepts as a proof of `collapseRel R2L 0 1`
by unfolding the definition. The `_` in `Quot.mk _ 0` asks Lean to fill in
the relation from the type of `f`.

**The book's `quot_barrier'`.** `have hq : ... := Quot.sound h` names the
equation of classes; `exact congrArg f hq` is the second step.

**`raw_function_separates`.** The identity on `Nat` returns `0` on `0` and
`1` on `1`, and `decide` checks `0 ≠ 1`. This is a function on the raw
carrier, not on the quotient, and the barrier does not apply to it. It is
here so that the word "only" in the claim is seen to do work.

**`descend`.** `Quot.lift g hg` constructs a function on classes from a
function `g` and a proof that it respects the generating relation. It is
the standard nondependent construction from a representative-level
function. The barrier applies to any function on the quotient, including
a constant function or a composition, however it was defined.

**`descend_agrees`.** `barrier_R2L` applied to the descended function.

**`barrier_R2F`.** This formal quotient uses the whole type `Nat`, not
`Fin R2F.data`. `R2F_collapsed d d'` holds for any natural indices in
this instance-free regime, so the book theorem is correspondingly
general. Its restriction to the three admitted indices is an instance;
the theorem does not admit any other index as a datum.

**Axioms.** The two general theorems use `Quot.sound` and nothing else.
The instances inherit `propext` from `collapsed_of_no_insts`, which is
behind `R2L_collapsed` (Unit 10). `raw_function_separates` uses no axiom:
`decide` on two numerals is a computation.

The added book equivalence helpers report `propext`. The raw-relation
chain example reports `propext, Quot.sound`. These are separate from the
native barrier's exact dependencies.

## What has been proved

- For every relation and every function out of its quotient, related
  elements have equal images (Genesis, derived; two forms).
- At `R2L`, every function on the collapse classes gives one value on
  `⟨a⟩` and `⟨ab⟩` (Genesis, derived).
- At `R2F`, every such function is constant on all three data (book Lean).
- A function on the raw data is not bound (book Lean, by a one-line
  witness).
- Collapse is reflexive and transitive, and can be packaged as a setoid
  using symmetry of `↔` (book). For an arbitrary raw generating relation,
  equal quotient values can arise along a chain even when the endpoints
  are not directly related (`raw_chain_quotient`, book).

## What has not been proved

- That the distinction cannot be recovered by *changing* the abstraction.
  It can: Challenge 3 changes the regime, and Units 18 to 22 price the
  change. The barrier is about staying inside the abstraction.
- Which abstraction is "current". That is a declaration of the
  metatheory: `collapseRel R2L` is chosen here because Challenge 2 ends
  with the two data collapsed. Nothing in the theorem picks the relation.
- A setoid construction in the native `Quot.lean` file: it uses raw
  `Quot`. The book separately proves reflexivity and transitivity of
  collapse and packages its equivalence using symmetry of `↔`. This
  does not add an exported theorem to the sealed derivation.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `Quot`, `Quot.mk`, `Quot.lift` | the quotient and functions out of it | metatheory type former |
| `Quot.sound` | related elements share a class | one of the two permitted axioms |
| `Setoid`, `Quotient`, `≈` | the setoid form | metatheory |
| `congrArg` | equal inputs give equal outputs | metatheory logic |
| `Sort u`, `Sort v` | types at any level | metatheory |
| `propext` | inherited through `R2L_collapsed` | inside the declared boundary |

**What the system holds.** Unchanged: the ledger `R2L`, two data and one
unmet demand. The quotient is a metatheoretic construction over the
ledger's data indices.

**Phrases to read with care.**

- "The system cannot tell the two apart" is right about the regime's
  observational content and wrong if taken to mean the tokens are
  unreadable. The metatheory reads `<a>` and `<ab>` whenever it likes; the
  regime has no context that does.
- "Information was lost in the abstraction" overstates. Nothing was in the
  profiles to lose: both are empty because nothing is asserted. The
  barrier is about what a function can read, not about what was once
  there.

## Student exercise

Someone proposes the operation "return the token of the datum" to recover
the distinction between `⟨a⟩` and `⟨ab⟩` in `R2L`. Does `barrier_R2L`
forbid it? Does it answer the paper's question 5?

## Answer

<details>
<summary>Worked answer</summary>

It is not forbidden and it does not answer the question. The operation
reads the presentation token, which is not part of the collapse class, so
it is not a function out of `Quot (collapseRel R2L)` and the theorem is
silent about it (compare `raw_function_separates`). Question 5 asks about
operations defined only on the abstraction. Reading the token is reading
something the abstraction had already set aside: the engine forgets
tokens on purpose (Unit 21, `canonical`), and the regime has no context
that mentions them (Unit 08). Recovering the distinction inside the regime
means admitting structure that some context can see, which is Challenge 3,
and Unit 18 proves that costs at least two items.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/Quot.lean` lines 17-20, 23-26, 31, 33-35 |
| Axiom report | `artifacts/lean_axioms.txt`: `quotient_barrier` `[Quot.sound]`; `quot_barrier` `[Quot.sound]`; `barrier_R2L` `[propext, Quot.sound]` |
| Paper | `paper/paper.md` §10 required question 5; ledger `paper/paper_claim_ledger.md` `CL-QUOT-BARRIER` ("Python: n/a (purely logical)") |
| Check (Python) | `python textbook/checks/u27_barrier.py`: `R2L` equal profiles and differing tokens; invariant canonical key; separate binary-link example with equal profile sizes and unequal full profiles |
| Check (book Lean) | `python textbook/checks/u27_lean.py`: nine book reports plus three native results kernel-checked, Lean 4.33.0; added collapse/setoid helpers use `propext`, the raw chain uses `propext, Quot.sound`; original dependencies are unchanged |
