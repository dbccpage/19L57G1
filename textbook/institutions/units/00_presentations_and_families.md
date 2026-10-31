# Unit 00. A presentation, a family, a signature

**Claim.** Presentations report values on supplied inputs. A family combines
those reports into an answer list called a signature. These definitions
are supplied; their use of actor and institution does not make a claim
about people or organizations.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Before anything can be proved about actors and institutions,
three things must be admitted: a presentation is a function from data
numbers to values; a family is a list of presentations; the signature of a
datum under a family is the list of the members' values at it. Nothing
below derives these from the mark.

**Status:** admitted. **Lean:** `Compression.sigList`, `Compression.SigEq`
(sealed), `Institution.Institution` (`two_theorems`). **Sources:**
`lean4/Derivation/Compression.lean` lines 60–72;
`research/two_theorems/lean/ResearchTwoTheorems/Institution.lean` lines
56–59; `research/two_theorems/README.md`.

This unit has one small theorem, proved at the end, and it is there to
show that the three admissions already have consequences. Its job is to
fix what the words of this part are attached to, so that every later unit
can be read for what it is: a result about functions read on a finite list,
not a result about people, organizations or minds.

</details>

## First pass

Use three cards, A, B, and C, and two supplied reporting tables:

| Card | First table | Second table | Combined signature |
|---|---|---|---|
| A | 0 | 0 | [0,0] |
| B | 1 | 1 | [1,1] |
| C | 0 | 1 | [0,1] |

A presentation is one reporting table. A family is the list of tables.
A signature is the row of answers for one card, in family order. The
first table merges A with C; the second merges B with C. Their combined
signatures distinguish all three cards.

This part calls a presentation an actor and a family an institution.
Those are names for these mathematical objects. No person or organization
has yet been modeled.

**Predict:** if we repeat the first table, will any previously equal
signatures become different?

<details><summary>Check your prediction</summary>

No. Equal old answers stay equal when the same answer is copied. Later
lessons distinguish additional reports from additional distinctions.

</details>

## What you need first

Part 1's Unit 00 (the mark and the external constructor) and Unit 01 (what
an admitted definition is). This part begins where part 1's representation
has already admitted data numbers: a datum is a number, and a finite list
of numbers is a **carrier** `D`.

### 1. A presentation

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 60–67
namespace Compression

/-! ## Signatures and agreement -/

/-- The answer signature of `x` under the declared family `Q`: the
list of answers, in family order.  The family is represented data. -/
def sigList (Q : List (Nat → Nat)) (x : Nat) : List Nat :=
  Q.map (fun q => q x)
```

The type `Nat → Nat` is the type of a presentation: a function that takes a
data number and returns a value number. The sealed file never names the
type separately; it writes `Nat → Nat` each time. A presentation is read
only on the carrier, and on the carrier it is a finite table.

```python
# Python (research), research/actor_institution/model.py line 25
Presentation = tuple[int, ...]
```

```
# Gloss
a presentation on the carrier [0, 1, 2] is a table of three values:
    p1 = (0, 1, 0)    means  p1(0) = 0,  p1(1) = 1,  p1(2) = 0
two data with the same value are MERGED by p; with different values,
TOLD APART by p (the Lean says: separated)
```

Why a function. Genesis's representation admits data as numbers and keeps
their names in the metatheory (part 1, Unit 00). A presentation is the
least structure that can *say something about* data: for each datum, one
value. It says nothing about why the value is what it is. The research
brief calls such a function an **actor**: a presentation of admitted
distinctions, the distinctions being which pairs of data it tells apart.

### 2. A family

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Institution.lean lines 55–59
/-- DECLARED: an institution is a represented question family. -/
abbrev Institution := List (Nat → Nat)

/-- The institution as one actor: Genesis's joint presentation. -/
def actor (D : List Nat) (Q : Institution) : Nat → Nat := pQ D Q
```

A family is a list. `abbrev` means the name is a pure abbreviation: Lean
sees `List (Nat → Nat)` wherever `Institution` is written, so every sealed
theorem about lists of presentations applies to institutions unchanged.
The tree's word for a family is **institution**; a presentation read as a
member of one is a **member**; and the tree's `actor` is the family's
*representative*, a single presentation standing for the whole family,
which Unit 01 explains. The brief's "actor" is a member; the tree's
`actor` is the representative. Both words are attached to functions read on
the carrier, and this part says which it means each time.

```python
# Python (research), research/actor_institution/model.py line 26
Institution = tuple[Presentation, ...]
```

```
# Gloss
a family on [0, 1, 2]:   Q = (p1, p2)   with   p1 = (0, 1, 0),  p2 = (0, 1, 1)
```

What the list gives the family and nothing more: **retention** (the
members are kept, in order), **comparison** (two data can be compared on
every member), and **combination** (a representative can be computed from
all members at once, Unit 01). The brief's "institution is a family of
presentations with retention, comparison and combination" is attached to
exactly these three list operations.

### 3. A signature, and agreement

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 69–72
/-- Agreement of `x` and `x'` on every question of the declared
family. -/
def SigEq (Q : List (Nat → Nat)) (x x' : Nat) : Prop :=
  ∀ q, q ∈ Q → q x = q x'
```

`sigList Q x` (quoted above) is the list of the members' values at `x`,
in family order: the datum's **signature**. `SigEq Q x x'` says every
member gives `x` and `x'` the same value: the family **cannot tell them
apart**. The sealed file calls the members *questions* and the values
*answers*; this part keeps the trees' words, members and values.

```python
# Python (research), research/actor_institution/model.py lines 131–132
def sig(Q: Institution, x: int) -> tuple[int, ...]:
    return tuple(q[x] for q in Q)
```

```
# Gloss
signature of datum x under (p1, p2):   (p1(x), p2(x))
on [0, 1, 2]:   datum 0 -> (0, 0),   datum 1 -> (1, 1),   datum 2 -> (0, 1)
no two signatures agree, so the family tells every pair apart,
although p1 merges 0 with 2 and p2 merges 1 with 2
```

## The worked example

Three data, two members, and a third presentation `q3 = (0, 0, 1)` that
will be the claim of Unit 04:

| datum | `p1` | `p2` | signature | `q3` |
|---|---|---|---|---|
| 0 | 0 | 0 | (0, 0) | 0 |
| 1 | 1 | 1 | (1, 1) | 0 |
| 2 | 0 | 1 | (0, 1) | 1 |

`p1` cannot tell 0 from 2. `p2` cannot tell 1 from 2. The family tells
every pair apart. Keep the table; Units 01 to 06 return to it.

```
python textbook/institutions/checks/i00_signatures.py
```

prints this table from the tree's own definitions.

## A first theorem: agreement is equality of signatures

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 74–90
/-- Family agreement is exactly signature equality. -/
theorem sigEq_iff_sigList (Q : List (Nat → Nat)) (x x' : Nat) :
    SigEq Q x x' ↔ sigList Q x = sigList Q x' := by
  induction Q with
  | nil => exact ⟨fun _ => rfl, fun _ q hq => by cases hq⟩
  | cons q T ih =>
    constructor
    · intro h
      show q x :: sigList T x = q x' :: sigList T x'
      rw [h q List.mem_cons_self,
        ih.mp (fun q' hq' => h q' (List.mem_cons_of_mem _ hq'))]
    · intro h q' hq'
      have hh : q x :: sigList T x = q x' :: sigList T x' := h
      injection hh with h1 h2
      cases hq' with
      | head => exact h1
      | tail _ hm => exact ih.mpr h2 q' hm
```

**Status:** derived. It says the two ways of writing "the family cannot
tell `x` from `x'`" agree: member by member (`SigEq`) and as one list
(`sigList`). Every later unit switches between the two freely because of
this theorem.

**The proof, step by step.**

**Step 1. `induction Q`.** A family is a list, and a list is either empty
(`nil`) or a first member `q` in front of a shorter list `T` (`cons`). The
theorem is proved for the empty family, and then for `q :: T` assuming it
for `T`. The assumption is named `ih`.

**Step 2. The empty family.** `SigEq [] x x'` says "every member of the
empty list agrees", which holds for no reason at all: there is no member.
`sigList [] x = sigList [] x'` is `[] = []`, true by `rfl`. Left to right:
given anything, `rfl`. Right to left: given equality of the empty lists and
a supposed member `q` with `hq : q ∈ []`, `cases hq` finds no way a member
can be in the empty list, which closes the goal.

**Step 3. The family `q :: T`, left to right.** Assume `h : SigEq (q :: T)
x x'`. `show` rewrites the goal to what `sigList` computes to on a `cons`:
the value of `q` in front of the signature under `T`. Two rewrites close
it: `h q List.mem_cons_self` says `q x = q x'` (the first member agrees,
because it is a member), and `ih.mp` applied to "every member of `T`
agrees" (obtained from `h`, since a member of `T` is a member of `q :: T`
by `List.mem_cons_of_mem`) says the signatures under `T` are equal.

**Step 4. The family `q :: T`, right to left.** Assume the two signature
lists are equal. `have hh` restates that equality in its computed form,
`q x :: sigList T x = q x' :: sigList T x'`. `injection` is the rule that
two equal lists have equal heads and equal tails: `h1 : q x = q x'` and
`h2 : sigList T x = sigList T x'`. Now take a member `q'` with `hq' : q' ∈
q :: T`. `cases hq'`: either `q'` is the head `q`, and `h1` is the answer,
or `q'` is in the tail `T`, and `ih.mpr h2` gives agreement on every member
of `T`, applied to `q'`.

## The same fact in Python

`model.sig` computes the signature as a tuple. Equal signatures are the
Python form of `SigEq`, and the theorem is what licenses reading the one
as the other.

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `Nat → Nat` | a presentation | metatheory: Lean's function type. The system holds the table on `D`, finitely many values. |
| `List (Nat → Nat)` | a family | metatheory (finite data structure); a family is finitely many tables |
| `List Nat` | the carrier `D` and a signature | metatheory |
| `∀ q, q ∈ Q → …` | agreement on every member | a quantifier over a finite list: discharged by walking the list (`induction Q`) |
| `Prop`, `↔`, `=` | the statement | metatheory (Lean's logic) |
| `induction`, `injection`, `cases`, `rw` | checking the proof | metatheory (part 1, Unit 00, the external constructor) |

`Nat → Nat` has no bound: a presentation is defined at every number, and
at numbers naming no admitted datum. That is a property of Lean. The
system holds a presentation only as its table on the carrier, and every
theorem of this part reads presentations on the carrier only (`x ∈ D`).
Off the carrier nothing is claimed.

**What the system holds.** A carrier, a finite list of data numbers; a
family, a finite list of tables on it; nothing else. No collection of "all
presentations", no space of possible families. When a unit says "for every
presentation", the quantifier is Lean's, proved once for an arbitrary
function, and it puts no totality into the system.

**Admissions relied on, and their price.**

1. *A presentation is a function.* Price: the values are numbers, so two
   values are either equal or not, with nothing in between; and a
   presentation says nothing about how it arrived at a value.
2. *A family is a list.* Price: order and repetition are kept (the family
   `[p1, p1]` is a different list from `[p1]`), and membership `q ∈ Q` is
   list membership. Unit 06 shows a repeated member changes nothing that
   the family knows.
3. *A shared carrier.* Every member is read on the same `D`: datum 0 of
   `p1` is datum 0 of `p2`. This is an admission of **correspondence**, and
   Unit 05 shows that without it the family knows nothing of what Unit 04
   says it knows. Nothing in a presentation says which of another
   presentation's data is "the same datum".

**Phrases to read with care.**

- "The actor" and "the institution" are names for a function and a list.
  Nothing in this part gives either a viewpoint, an intention or a memory.
  "The institution cannot tell `x` from `x'`" means every member gives them
  the same value.
- "The member answers" means the function has a value there. No one is
  asked anything; the value is in the table.
- "Three data" (the worked example) means the carrier `[0, 1, 2]` was
  admitted with three numbers. The system did not count anything; the
  carrier was written down.

## What it shows, and what it does not

It shows what every word of this part is attached to: presentation,
member, family, carrier, signature, merged, told apart, cannot tell apart.
It shows that the two readings of "cannot tell apart" agree
(`sigEq_iff_sigList`), which is the one derived fact here.

It does not show that these are the right definitions of actor and
institution. They are chosen. The research brief proposed the words; the
trees attached them to the least structure that supports the theorems of
Units 01 to 15; and whether a richer notion of institution (one with
members that act, or that learn) is needed is open, and outside this part.

It does not show that the carrier is shared. That is admitted, and it is
the admission Unit 05 is about.

## Sources

| Item | Where |
|---|---|
| `sigList`, `SigEq` | `lean4/Derivation/Compression.lean` lines 66–72 |
| `sigEq_iff_sigList` | `lean4/Derivation/Compression.lean` lines 75–90; sealed axiom report in `artifacts/lean_axioms.txt` |
| `Institution`, `actor` | `research/two_theorems/lean/ResearchTwoTheorems/Institution.lean` lines 56–59 |
| Python mirror | `research/actor_institution/model.py` lines 25–26, 131–132 |
| Check | `textbook/institutions/checks/i00_signatures.py` |
| Ledger | `research/two_theorems/CLAIMS.md`, the declared vocabulary rows; `research/actor_institution/README.md`, the vocabulary table |
