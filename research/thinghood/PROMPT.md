# 19L57G1 research run -- thinghood and the unforced dynamical law

Run this as one autonomous construction workflow on merged `main`.

This is not a summary of the sealed derivation.  It is the first
construction run that must answer two caller-supplied questions by
building additional structure, or prove that the questions stop at a
named open obstruction.

Continue until the theorem lattice for these two questions closes, or a
smallest named obstruction remains.  Do not stop after restating an
existing theorem, after one attractive definition, or after one
countermodel.

Do not ask the user questions.  Do not wait for guidance.  Branch on
genuine alternatives and return the strongest defensible terminal
result.

AuthorityEffect: None.

---

## 0. Why this run exists

The sealed record already answers "what is Primitive Difference?" and
already answers "at an active obstruction, what responses exist?".
It does **not** answer the next two questions, and it must not be
quoted as if it had.

The caller supplies both questions as an externally imposed challenge.
The word **thing** is supplied.  It is not yet a native object.  Your
job is to give it a typed meaning cheap enough to justify, or to prove
that no such object exists in a declared candidate space.

---

## 1. Repository boundary

Work only under `research/thinghood/`.

Sealed, do not modify or regenerate:

```text
prompt/                 including prompt.md and seed_prompt.md
paper/
code/
lean4/Derivation/
artifacts/
```

Also do not amend `CLAUDE.md`, `.github/workflows/verify.yml`, or any
sibling research tree.  Registering this tree in CI is a later author
act, not part of this run.

`prompt/prompt.md` and `prompt/seed_prompt.md` remain byte-identical.

Read the sealed record.  Do not rewrite it.  A contradiction with a
sealed theorem may be recorded only as a named conflict, with the old
statement, the counterexample, and the affected claim IDs.

Use only this repository.  No network research, no external files, no
prior project instructions, no plugins, no imported theory names.
External citation is not permitted anywhere in this repository.

---

## 2. Evidence classes

Every substantive item has exactly one status:

```text
METATHEORY
SUPPLIED_INPUT
DEFINITION
DECLARED_POLICY
DERIVED_THEOREM
CONDITIONAL_THEOREM
FINITE_COMPUTATION
COUNTERMODEL
CONJECTURE
OPEN
REFUSED
```

The words "forced", "minimal", "free", "canonical", "equivalent",
"universal", and "complete" appear only with a proof or a precise
conditional scope.

---

## 3. The two questions

These are `SUPPLIED_INPUT`.  They are not derived from the inscription.

### Q1. What is a thing?

What is the cheapest object for which collapse can fail a law?

You must:

1. Declare a finite candidate space of objects (carrier, structure,
   and optional law), with an explicit metatheory bill for each
   candidate.
2. Declare a cost measure on that bill.  Different measures are
   different runs; do not silently switch.
3. Define, as a predicate on a candidate, what it means that a
   collapse **fails a law** of that candidate.  Collision without a
   law is not failure of a law.
4. Enumerate the cheapest survivors.  Retain every tied
   non-isomorphic minimum.
5. Prove that cheaper candidates fail the predicate, with a
   countermodel for each rejected class.
6. State whether the survivor coincides with the sealed Primitive
   Difference candidate, is strictly cheaper, is strictly richer, or
   is incomparable.  Coincidence is a theorem, not a slogan.

A datum with no law is not a thing in this sense: identifying two
admitted data can leave every profile unchanged.  Bare assertion
without a fidelity commitment collides and remains admissible.  Those
are sealed facts you may cite.  They are starting constraints, not
the answer to Q1.

### Q2. Is there a forced dynamical law?

In this repository, there is not.

There is a two-rule at an **already active** obstruction
(`PrimitivePassage.two_rule`: repair at the same level, or create
structure).  The obstruction itself is not forced from the
inscription.  That is correctly left open:

- `paper/primitive_difference.md` S6 item 6
- `paper/primitive_difference.md` S9 last bullet
- `research/genesis_continuation/` **OB-1**

You must not close any of the three.  You must make the non-closure
machine-checkable.

---

## 4. Sealed facts you may cite and must not over-read

Cite these as existing evidence.  Do not re-prove them as if they were
this run's discovery.  Do not read a dynamical law out of them.

From `lean4/Derivation/PrimDiff.lean` and
`paper/primitive_difference.md` S3:

- `CollapseCollision` is prior to any law: some asserted edge has
  both endpoints identified.
- `FidelityObstruction P r c` is a collision **together with** a
  protected law `P` that the pushforward violates.
- Identifying a witnessed pair always collides
  (`collision_of_identifying_witness`).
- Bare assertion: the collision exists and the collapse remains
  admissible (`bare_collapse_admissible`, `selfdiff_consistent`).
- Relative to preservation of `Irrefl`, the same collision is an
  obstruction (`obstruction_under_irrefl`).
- Among the three axiom choices studied there -- none, symmetry,
  irreflexivity -- only irreflexivity produces that soundness
  transfer.  The wider axiom lattice is still OPEN (S9 first
  bullet).  This run may enlarge that lattice only inside this tree,
  and only with the same honesty: uncompared axioms stay OPEN.

From `lean4/Derivation/PrimitivePassage.lean`:

- `obstP` is a four-gate conjunction.  No maximal proper subset
  entails obstruction (`obst_conditions_independent` and the four
  `gate_*_independent` theorems).
- `two_rule` fires **at** `obstP`, for an in-bounds protected pair:
  `repairFamily` nonempty, or same-level exhaustion and
  `extensionProposals` nonempty.
- The extension grammar is declared, not manufactured by the
  obstruction (`extension_always_available` uses the declared
  singleton-column universe).
- Proposal is not execution (`proposal_not_execution`).
- Pre-observational states obstruct nothing
  (`obst_requires_observation`).

From `paper/paper.md`:

- Challenge 0: no successor is internally forced from the
  inscription.
- Section 9 / section 11(f): no object-language endogenous demand
  generator was derived.  A collapsed pair, by itself, is not an
  active obstruction.

From `research/genesis_continuation/continuation_plan.md`:

- **OB-1** -- the challenge source.  Terminal `OB1_UNCHANGED`.
  Continuing past it requires an out-of-class repair channel or a
  theorem for a wider declared class.  This run does not supply
  either by declaration.

S6 item 6: the Primitive Difference object is a static tuple; every
continuation is an external act.

S9 last bullet: this paper characterizes a strong candidate once
carrier, two designated occurrences, relation, witness,
irreflexivity, and orientation exist.  It does not derive them from
the inscription.  The gap must not be silently filled by the
metatheory.

---

## 5. What this run must construct

Build, under this directory, a finite reference model of thinghood
and a scoped account of dynamics.  Minimum surface:

```text
research/thinghood/
  STATUS.md              update the result section; do not weaken the boundary
  PROMPT.md              this file; keep byte-identical
  CLAIM_LEDGER.md        stable IDs, class, evidence, falsifier
  thing.py               deterministic typed candidates, cost, collapse-fails-law
  test_thing.py          positive and negative tests
  run_thing.py           sorted timestamp-free JSON receipt
  receipts/thing.json    regenerated receipt
  lean/                  optional; required for every theorem-level claim
```

Python is deterministic and fully type-annotated.  Tests must include
negative cases that fail the run if a forbidden claim is smuggled.
Lean, if used, builds with no `sorry`, `admit`, custom `axiom`,
`unsafe`, or `partial`.  Axiom reports stay inside
`{propext, Quot.sound}`.

Do not add files under sealed paths to "complete" a theorem.  If a
claim needs a sealed change, downgrade it to OPEN and name the
missing sealed theorem.

---

## 6. Phases

Execute in order.  A later phase may not assume a unique survivor
from an earlier phase that still has ties.

### Phase I -- candidate grammar for Q1

Declare the objects that could host law-failure under collapse.
Each candidate is a tuple of priced ingredients.  Independent
admissions stay independent.  At least the following classes must
appear, each with a yes/no for "collapse can fail a law of this
object" and a cheapest witness or a countermodel:

1. a carrier with no relation and no law
2. a carrier with one asserted pair and no law (sealed A1)
3. metatheoretic inequality with no asserted pair (sealed A3)
4. an asserted pair plus irreflexivity (sealed A1i)
5. an asserted pair plus symmetry only
6. at least one richer law from a declared finite axiom list
   (if you cannot finish the list, the remainder is OPEN, not
   silently equal to irreflexivity)
7. a sealed passage state: retained, protected, observed, or not
   -- priced separately, because those stores are not free

Retention, protection, observation, budget, and license are further
purchases.  They may make a *later* thing.  They are not smuggled
into the cheapest one.

### Phase II -- cost and minimality

State the cost measure in one paragraph, then implement it.
Prove, over the declared space:

- every candidate with cost below the minimum fails
  "collapse can fail a law"
- every minimum survivor satisfies it
- ties are retained

If the cheapest survivor is A1i, that is a theorem of this run
relating Q1 to the sealed Primitive Difference object.  It is not
permission to rename Primitive Difference as "thing" in the sealed
papers.

If a cheaper survivor exists, exhibit it and say exactly which
sealed sentence it does **not** contradict.

### Phase III -- thing versus difference versus datum

Keep three notions distinct in every lemma name and every ledger
row:

- **datum** -- admitted occurrence; collapse of two data need not
  fail any law
- **difference** -- the sealed Primitive Difference candidate
- **thing** -- an object for which some collapse fails a law of
  that object

Write the implication lattice among the three, with countermodels
on the failing arrows.  An identification of any two is REFUSED
until a proof over the declared space.

### Phase IV -- the dynamical-law question

Prove, or restate with exact hypotheses as `CONDITIONAL_THEOREM`
backed by sealed names, each of the following.  A missing proof is
OPEN, not a narrative yes.

1. From the inscription alone, no object-language successor is
   forced.
2. A collapsed pair is not an active obstruction.
3. `obstP` requires four independent gates.
4. `two_rule` has `obstP` (and the in-bounds protected pair) among
   its hypotheses.  Removing `obstP` makes the statement false, or
   inapplicable.  Exhibit the failure.
5. Therefore `two_rule` is a response rule **at an already active
   obstruction**, not a dynamical law of the inscription.

Issue the terminal `NO_FORCED_DYNAMICAL_LAW` only with those five
in hand.  Do not issue it from Q1.

### Phase V -- keep the three opens open

Add negative tests or Lean countermodels that fail the run if any of
these are claimed closed:

- S6 item 6: an endogenous next challenge following from the static
  difference object
- S9 last bullet: silent elaboration of the opaque inscription into
  a witnessed irreflexive datum
- OB-1: an object-language endogenous demand generator

A theorem "the genesis regime has `obstP`" is REFUSED.  A theorem
"the inscription is a thing" is REFUSED unless every priced
ingredient is derived from the inscription, which the sealed record
says it is not.

The only legal terminals for this phase are `OB1_UNCHANGED`,
`S66_UNCHANGED`, `S9_LAST_UNCHANGED`, or a **narrower** open that
strictly refines one of them without closing it.

### Phase VI -- receipt and strongest defensible result

Write `CLAIM_LEDGER.md` and `receipts/thing.json`.  Update
`STATUS.md` with the terminals, the cheapest survivor class (or
OPEN), and the exact scope of `NO_FORCED_DYNAMICAL_LAW`.

The strongest defensible result states Q1 and Q2 separately.  Do not
bundle them.  Q1 may close while Q2 stays a scoped negative.  Q2
must not be used to answer Q1.

---

## 7. Hard refusals

Cite the rule by name whenever it bound a step.

- **FW-SEAL** -- do not write sealed paths.
- **FW-LAW** -- collision is not obstruction.  Obstruction is
  relative to a protected law.
- **FW-DYNAMICS** -- do not call `two_rule` a law of the
  inscription, a genesis rule, or a forced successor.
- **FW-OB1** -- do not close OB-1, S6 item 6, or S9 last bullet.
- **FW-TIES** -- retain every tied minimum unless uniqueness is
  proved.
- **FW-BILL** -- retention, protection, observation, budget, and
  license are not free.
- **FW-NAME** -- do not name an external theory, architecture, or
  project.  Do not write a barred contact identifier.
- **FW-LEAK** -- this prompt states questions and constraints.  It
  does not state the winning candidate.  Do not treat any sentence
  in section 4 as the answer to Q1.

---

## 8. Adversarial obligations

Each attack has a required disposition.  Record all eight in the
receipt.

1. "A thing is a datum."  Countermodel: observational collapse of
   two admitted data with no law.
2. "A thing is a bare asserted pair."  Countermodel:
   `selfdiff_consistent` / `bare_collapse_admissible`.
3. "Collapse itself is the law."  Refute: collapse is a map;
   failure of a law is `not P (Push r c)`.
4. "Primitive Difference is already the thing, by definition."
   Either prove coincidence over the declared space or retain a
   gap.  Definitional identification is REFUSED.
5. "two_rule forces structure from the seed."  Refute by the
   hypotheses of `two_rule` and by Challenge 0.
6. "Active obstruction follows from inscription."  Refute by
   `obst_requires_observation` and the four-gate independence.
7. "The cheapest thing includes a declared observer."  Price the
   observer separately; exhibit a cheaper law-carrying object
   without one, or OPEN why not.
8. "Closing the candidate list by narrative."  Any axiom or store
   not in the declared space stays OPEN.  Absence of a search is
   not uniqueness.

---

## 9. Legal terminals

Issue only from this list, each with scope:

```text
THINGHOOD_CHARACTERIZED
THING_COINCIDES_WITH_A1I
THING_STRICTLY_CHEAPER_THAN_A1I
THING_STRICTLY_RICHER_THAN_A1I
THING_INCOMPARABLE_WITH_A1I
NO_FORCED_DYNAMICAL_LAW
OB1_UNCHANGED
S66_UNCHANGED
S9_LAST_UNCHANGED
CANDIDATE_SPACE_OPEN
CONTACT_WITH_SEALED_THEOREM
REFUSED
```

`THINGHOOD_CHARACTERIZED` requires Phase I--III.  It does not imply
`NO_FORCED_DYNAMICAL_LAW`.

`NO_FORCED_DYNAMICAL_LAW` requires Phase IV.  It does not imply a
winner for Q1.

The three `*_UNCHANGED` terminals are required.  Missing one is an
incomplete run.

---

## 10. Definition of done

Finish only when:

1. Q1 has a cheapest survivor class with a declared space, a
   declared cost, and a countermodel for every cheaper rejected
   class, or is explicitly OPEN at a named missing comparison.
2. Q2 is answered as: no dynamical law of the inscription; two-rule
   only at an already active obstruction; obstruction not forced
   from the inscription.
3. OB-1, S6 item 6, and S9 last bullet are still open, with
   negative tests.
4. The eight adversarial attacks have dispositions.
5. Every theorem-level claim in this tree has Lean evidence or is
   downgraded.
6. Every computational claim has deterministic Python evidence.
7. Tied minima are retained unless eliminated by proof.
8. No sealed path changed.
9. `PROMPT.md` is byte-identical to the start of the run.
10. `STATUS.md` states the strongest defensible terminal result
    without targeting a predetermined conclusion.

A restatement of S3, of `two_rule`, or of OB-1, with no new
candidate-space work under this directory, is not done.
