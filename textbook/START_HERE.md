# Start Here: A Reader's Entrance to Genesis

**AuthorityEffect: None.** This page is an entrance for a reader who has not
met this repository, formal logic, Python, or the Lean proof checker before.
It introduces the question the book studies and points you to the first lesson.

---

## 1. We begin with a mark

Everything in this book starts from a single written inscription:

```
<>
```

In the lessons, we write this mark as ⟨⟩.

When you look at `<>` on a page, your eyes see two angled strokes, a left side
and a right side, and an empty gap in the middle. Those features belong to how
the mark is printed on the page. They do not belong to the system we are
studying. Inside the system, ⟨⟩ is treated as one undivided, opaque item.

## 2. A mark does not internally establish a mathematical universe

Writing down a mark does not create numbers, sets, containers, points,
functions, rules of logic, or a surrounding space.

- The mark ⟨⟩ does not establish an empty set.
- The brackets do not establish a box or container with an inside and an outside.
- Writing two different marks, such as ⟨A⟩ and ⟨B⟩, does not by itself give the
  system a way to tell them apart.
- Repeating a letter, such as ⟨AA⟩ or ⟨ARA⟩, does not by itself give the system
  a notion of sameness or a relation between two things.

Until a rule or an observation is explicitly introduced, the system has no way
to compare, count, or derive anything at all.

## 3. Structure must be admitted or derived

Because nothing comes for free from the mark, every piece of machinery used in
this book is tracked on an explicit ledger. Each step is either:

- **Admitted:** chosen and supplied from outside at a stated price — such as
  the background language in which we keep the ledger, a new datum, a new
  relational form, a recorded fact, or a protected requirement.
- **Derived:** proved step by step from what has already been admitted, with no
  hidden assumptions and no skipped steps.

Keeping **admitted** and **derived** separate is the central discipline of the
book. A definition is a choice, not a proof. Showing that a chosen rule works
does not show that it was the only rule that could have been chosen.

## 4. What a witnessed difference is

In ordinary talk, we say two things are different simply because we gave them
different names, like "datum 0" and "datum 1". Inside a formal system, having
two labels in an outside list is not enough.

A **witnessed difference** is a distinction that a specified observation inside
the system can actually detect — for example, a test with one open slot that
succeeds when datum 0 is plugged in and fails when datum 1 is plugged in. When
no available test can tell two items apart, the two items are **observationally
collapsed** relative to that stage of the system, even though their outside
labels differ.

## 5. Why richer structures appear

The progression in this book moves forward only when an earlier, simpler setup
cannot meet an admitted requirement:

1. **At the mark ⟨⟩ (`Unit 00`–`Unit 04`):** Nothing is derivable, supplying a
   label without admitting it changes nothing, and no next step is forced from
   inside.
2. **Admitting data without relations (`Unit 05`–`Unit 16`):** Even after two
   distinct tokens ⟨A⟩ and ⟨AB⟩ are admitted as data, there are no recorded
   facts relating them. Every test gives the same answer on both, so they
   remain collapsed.
3. **Answering a separation demand (`Unit 17`–`Unit 22`):** When an external
   requirement demands that datum 0 and datum 1 be separated, a single
   addition of cost 1 cannot do the job (`Unit 18`). Meeting the demand
   requires admitting both a form and a recorded instance, such as a directed
   link (`Unit 19`) or a self-loop (`Unit 20`), and which repairs are cheapest
   depends on the admitted cost measure (`Unit 21`–`Unit 22`).
4. **Laws, obstructions, and repair (`Unit 23`–`Unit 46`):** Recording a single
   fact never forces a general law such as irreflexivity (`Unit 23`–`Unit 26`).
   When a protected law is admitted alongside observations that merge what the
   law keeps apart, an **obstruction** arises, and the system must either
   repair its observation, extend its carrier, or record a refusal.
5. **Observers, quotients, higher cells, and the interpreter boundary
   (`Unit 47`–`Unit 74`):** Later lessons examine what happens when the
   observer's own views are put on the books, how higher-dimensional boundary
   shells and equivalence quotients behave, and why the interpreter that runs
   a family of transition codes remains distinct from the codes in its family.
6. **Actors and institutions (`Part 2`):** The second part of the book studies
   what happens when several presentations (actors) are combined into a family
   (an institution): how information counts distinguishable classes, when a
   family determines a claim that no single member determines, why
   correspondence across members is an admission, when an institution must
   demur rather than assert, and what it costs to probe an unknown partition.

## 6. What this book is — and what it is not

This book is an **introductory mathematical narrative** through a formal
derivation. It is written so that every step can be read, run on a computer in
a few lines of Python, checked by the Lean 4 proof assistant, and questioned on
its own terms.

- **It is not a proof that the physical universe follows this progression.**
- **It does not derive the physical world from a mark.**
- **A computer check or a formal theorem about a finite ledger is a statement
  about that mathematical model, never an empirical law of nature.**

---

## How to read this book

No prior study of mathematics, logic, Python, or Lean is assumed. Later
lessons contain longer formal statements, so work through their examples
before trying to read every theorem name.

Use three passes for a difficult lesson:

1. Read the question and first-pass example. Say what changes in your own words.
2. Read one definition at a time. Check its symbols against the example.
3. Read the formal statement, its hypotheses, and the limits of the result.

The short videos preview groups of lessons. Pause or replay them as needed;
their fifteen-second duration is not a target for understanding a definition.

1. **First lesson:** Start at [`Unit 00: The mark and the external constructor`](units/00_mark_and_constructor.md),
   then proceed in order to [`Unit 01: Nothing is derivable at genesis`](units/01_genesis_underivable.md),
   [`Unit 02`](units/02_underivable_of_empty.md), and [`Unit 03`](units/03_supply_no_op.md).
2. **Table of contents and rules of the book:** See [`textbook/README.md`](README.md)
   for the full list of Units 00–74 in Part 1 and the link to Part 2.
3. **Part 2 (Actors and institutions):** After Part 1 (or after `Unit 61` on
   presentations and compression), see [`textbook/institutions/README.md`](institutions/README.md).
4. **Complete theorem-to-lesson map and dependency graph:** See
   [`textbook/derivation_coverage.md`](derivation_coverage.md).
5. **Module-by-module source audit:** See [`textbook/audit/README.md`](audit/README.md).
6. **15-second video introduction script:** See
   [`textbook/video_script_15s.md`](video_script_15s.md).
