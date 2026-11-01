# Unit 00. The mark and the external constructor

**Claim.** Before any theorem can be proved about ⟨⟩, a formal language must
be admitted from outside. The mark does not supply one.

<details><summary>Source and classification record (optional)</summary>

**Status:** admitted. **Lean:** none. **Sources:** `prompt/seed_prompt.md`
§1; `paper/paper.md` §2 and §3.

This unit has no theorem. It sets out what the rest of the book takes for
granted, so that every later theorem can be read for what it is: a precise
result inside a chosen representation, not a result about why that
representation was chosen.

</details>

## Question

Does seeing a mark also give us rules for using it?

## First pass

Write `<>` on a card. For this book's starting point, treat that inscription
as one opaque item: we are not allowed to infer an inside, a pair or an
operation from how it looks.

### A mark and a chosen rule

Suppose we now choose a notebook with five fields: admitted data, forms,
individual statements, rules and demands. That notebook design is a
**representation**: a supplied way to describe a model. The mark did not
choose those fields for us.

Someone outside the described system chooses the representation. The
book calls that role the **external constructor**. The reasoning tools
used to describe and check the model are its **metatheory**. These words
name our setup; they do not introduce an observer inside the notebook.

<details><summary>Predict: does the space inside the brackets make the notebook empty?</summary>

No. The starting notebook is empty because we chose all its admission
fields to be empty. The inscription's appearance supplies no such rule.

</details>

### Two uses of “admit”

We **admit a definition** when we supply the model's language and rules.
Within that chosen model, an **admission event** can add a datum or another
allowed entry. Defining the notebook is different from putting a datum in it.

A theorem then proves something under those definitions and its stated
premises. A successful proof does not show that the definitions were the
only possible choice or that a physical device follows them.

Change the inscription to a star but keep its required opaque treatment.
Its shape still supplies no pairing rule. A formal claim about renaming
an entire model would need its own definitions and proof.

Before continuing, explain which came from the inscription and which we
supplied: the five fields, their starting contents and the lookup rule.
The source discussion below records exactly what the seed supplies.
Continue to [Unit 01](01_genesis_underivable.md).

<details><summary>More detail: The mark</summary>

## The mark

The seed gives exactly one object-language inscription:

```
<>
```

and instructs that it be treated "as one opaque atomic datum"
(`prompt/seed_prompt.md` §1). The book writes it ⟨⟩.

**Why this mark.** The seed supplies `<>` as an opaque inscription. Its
typography licenses no internal operation. Replacing a displayed symbol
while retaining that reading is a notational choice; an invariance claim
about an entire renamed formal model would need its own statement and proof.

**The notation is arbitrary.** To a reader, `<>` shows two glyphs, an
opening and a closing, and an empty space between them. The seed forbids
the object language every one of those readings: it may not see "two marks,
an inside, an outside, order, direction, emptiness, containment, a pair, a
string, a set, a point, a relation, a value, or a boundary"
(`prompt/seed_prompt.md` §1). Those are available only to the external
metatheory, unless later admitted and justified.

**The system does not inherit the structure of the inscription.** That ⟨⟩
looks empty does not make the starting state empty, and that it looks like a
pair of brackets does not give the system a notion of pairing. Unit 01's
empty ledger is empty because nothing has been admitted, not because ⟨⟩
"means nothing".

</details>

<details><summary>More detail: The external constructor</summary>

## The external constructor

A mark alone proves nothing. To prove anything, we need a language in which
statements are made, and a declared notion of when a statement follows.
Neither can be read off ⟨⟩.

So someone outside the system supplies them. This book calls that party the
**external constructor**: the declared metatheory together with whoever
chooses, within it, how the starting point is represented. In Genesis the
constructor works in two places.

| Layer | What it supplies | Where |
|---|---|---|
| Metatheory | strings, indices, finite data structures, arithmetic; Lean 4 as the proof checker | `paper/paper.md` §1 and §2 |
| Representation | regimes, judgment forms, instances, rules, demands, admission events, contexts, derivability | `paper/paper.md` §3; `lean4/Derivation/Basic.lean` |

The paper marks the first layer **[declared metatheory]** and the second
**[definition]**. This book marks both **admitted**.

The seed also names a second external role: a caller who presents challenges
(`<a>`, then `<ab>`, then a demand that they be separated). The seed calls
these "metatheoretic interventions", not object-language conclusions
(`prompt/seed_prompt.md` §3). They too come from outside.

</details>

<details><summary>More detail: The three layers</summary>

## The three layers

Every theorem in this book sits in the third of three layers:

1. **The inscription.** ⟨⟩, opaque.
2. **The admitted representation.** The metatheory and the definitions the
   constructor chose.
3. **The theorem.** A statement proved inside layer 2.

A theorem in layer 3 can be exact, kernel-checked and free of extra
hypotheses, and still say nothing about whether layer 2 was the necessary
choice. That is not a defect of Lean or of Genesis. It is the boundary the
programme investigates: how little must be admitted before anything can be
established, and what each admission buys.

</details>

<details><summary>More detail: Outside the system</summary>

## Outside the system

This whole unit is about what sits outside. Two parties are outside, and
the book counts both as admitted, never as derived: the external
constructor (the metatheory and the chosen representation) and the caller
who presents challenges.

**What the system holds.** Nothing yet. Not even ⟨⟩ is in the ledger in
reading L (Unit 05).

**What the outside does not bring with it.** Admitting a metatheory does not
admit its totalities into the system. Lean has unbounded types such as
`Nat`; the system gets none of them. The constructor is not an observer
inside the system, and the system gets no viewpoint from it. Later ledger
contents enter through the model's declared admission rules and events
(README, **No imports from nowhere**). A numerical price requires a named
cost measure. Calling a metatheoretic definition “admitted” does not by
itself assign such a price.

</details>

<details><summary>More detail: What this unit establishes, and what it does not</summary>

## What this unit establishes, and what it does not

It establishes no mathematical fact. It fixes the reading of every later
unit.

It does not claim that Genesis's representation is the only one, or the
best. Other representations of the same seed are possible, and nothing in
this book compares them.

It does not claim that the mark and the representation are unrelated. The
representation was built to honour the seed's restrictions: Genesis keeps
token identity in the metatheory and counts data without naming them
(`paper/paper.md` §2 and §3). That fidelity is a design property, checked by
tests and by the erasure bridge (ledger entry `CL-TOKEN-ERASURE`). It is not
a derivation of the representation from the mark.

</details>

<details><summary>More detail: Sources</summary>

## Sources

| Item | Where |
|---|---|
| The inscription and its restrictions | `prompt/seed_prompt.md` §1 |
| Challenges as metatheoretic interventions | `prompt/seed_prompt.md` §3 |
| Declared metatheory | `paper/paper.md` §1, §2 |
| Admitted definitions | `paper/paper.md` §3; `lean4/Derivation/Basic.lean` |
| Token erasure bridge | `paper/paper_claim_ledger.md`, `CL-TOKEN-ERASURE` |

</details>
