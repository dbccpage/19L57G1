# Quotation register

The declared register of texts this control quotes from the pinned tree, and
one of the three files of this tree in which that tree's own path may appear.
The other two are `SOURCE_MANIFEST.json` and `BOUNDARY_PIN.json`.  Every other
research tree name stays barred everywhere, here included, and
`tests/test_isolation.py` enforces both halves.

Source: `research/boundary_seed`, at merge commit
`6c80c7ae43a704dcf9f109146cc6cf77139ed18e`, landed on `main`.
The vendored quotation bytes are unchanged from the earlier frozen-design pin.

Every quotation below is reproduced byte for byte from the vendored receipt
`boundary_challenge3.json` unless the entry says otherwise, and the reproduced
bytes are what a gate compares against — not this file.  This register exists
so a reader can see what was inherited and from where; the gates read the
vendored bytes.

---

## 1. The requirement, at `requirement.declared`

> the two retained marks are internally separable under a reading exactly when
> no permitted automorphism of the regime carries one of them to the other

The control's requirement is this text with the phrase ` under a reading`
deleted.  Gate `G2` asserts that the pinned text with that phrase deleted is
the control text byte for byte, and that the phrase occurs exactly once so the
deletion is unambiguous.

## 2. The second reading, at `requirement.second_reading`

> some property of a mark that forgets whatever the candidate's declared
> serialization forgets, and that is invariant under every permitted renaming
> of the reading, holds of one retained mark and not of the other

The control's second reading is this text with the phrase ` of the reading`
deleted, asserted the same way.

## 3. The three transferring capability sentences, at
`candidate_space.capability_of`

> **withdraw_mark_permutations** — a mark's admission index is internally
> available: the metatheoretic name definition 3 assigns is declared to be an
> internal designation

> **keep_labels** — a mark's presentation label is internally available: the
> token forgetting of definition 14 is withdrawn

> **extra_mark** — the process extends the caller's history with an admission
> of its own, rather than replaying only what the caller supplied and admitted

Gate `G3` asserts all three byte for byte.

## 4. The two deleted capability sentences, at the same path

> **withdraw_reflection** — the side exchange is not a permitted renaming: the
> two sides are declared distinguishable, which is the part of the O reading
> that reading U does not carry

> **admit_names** — the two sides carry admitted names, so the judgment
> grammar of the reading gains the side-name form

Each contains the whole word *side* or *sides*, which is the mechanical
criterion that drops it.  They are quoted here so a reader can apply the
criterion by eye and get the same partition the gate computes.

## 5. The first cost measure, at `measures.mu1`

> capability count: the number of undeclared capabilities the candidate uses

Inherited whole and used as the deciding measure.

## 6. The exhaustiveness scope, at `candidate_space.exhaustive_over`

> the five declared coordinates and their declared values, and nothing wider.
> It does not enumerate an augmentation that changes the event grammar again,
> that admits more than one further mark in one step, that supplies a datum
> the caller never presented, or that derives the permitted renamings from the
> judgment grammar instead of declaring them (definition 16).  Every
> minimality statement below is scoped to this space

The control inherits this scope and adds one clause of its own, that it does
not enumerate an augmentation admitting a new per-mark datum — which is the
rejected coordinate carried as open obstruction (b).

## 7. The clause this control refutes, at `boundary_dependence`

> the side exchange, its withdrawal, the two side mark properties, the
> counterfactual square, and every separation result of the rung: require the
> admitted boundary and are not formulated after removing it

Refuted only within the scope of this declared carrier, these three
coordinates, and this eight-point enumeration.  What refutes it is that a
separation result of that rung — the withdrawal of the mark permutations —
**is** formulated after removing the admitted primitive, at the same price,
and satisfies the same requirement.

## 8. From the pinned tree's own prose, quoted here rather than byte-compared

Two sentences of the pinned tree's other files are relied on as arguments
rather than as data, and are recorded so the reliance is visible.  They are
transcribed, not byte-pinned, and no gate compares them.

* On the presentation layer, from `code/boundary/presentation.py`: the
  presented side is a fact of the presentation, and which admitted side it
  becomes is a convention declared there and not derived from the inscription.
  This tree keeps the reader and deletes the convention, and that sentence is
  why the deletion falls where it does.

* On the pinned Lean package, from the repository's own workflow comment: that
  package remains a manual receipt.  This tree's Lean package is a manual
  receipt for the same reason, and records it as a live residual rather than
  claiming a gate it does not have.
