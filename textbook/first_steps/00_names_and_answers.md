# 00. Names and answers

[First steps](README.md) · [Next: a test and its witness](01_a_test_and_its_witness.md)

## Try this first

Three cards have names: A, B, and C. A small machine can answer only one
question about them: **blue?**

| Card | What the card is like | Machine's answer to blue? |
|---|---|---|
| A | Blue circle | Yes |
| B | Blue triangle | Yes |
| C | Amber triangle | No |

Suppose we rename card A to **Sun**. We keep the card and the machine's
question exactly as they were.

**Predict:** which answer in the last column should change?

## Three things to keep separate

A **label** is a name used to refer to an item. Here A is a label.
The circle on the first card is a feature of the supplied example.
The answer **yes** is what the machine returns to a particular question.

Changing a label changes how we refer to a card. It supplies no new answer
to **blue?** So the prediction is: none of those answers changes.

We chose a machine that does not inspect labels. A different machine
could have a question such as “Does the label begin with S?” That would
be an additional question with additional supplied answers. We would have
to say that we had introduced it.

## What did we assume?

We supplied the three cards, their labels, the question, and the table.
We declared that this machine reads only the answers to selected questions.
Those choices make the example possible.

In this book, an **admission** is an explicit addition under a stated rule.
Admitting a feature or a question is a choice we record. A conclusion is
**derived** when it follows from the choices and rules already given.
Here the unchanged answers follow from keeping the question and its table
unchanged while renaming a card.

## A non-example

If we paint A amber, we have changed a card feature in the supplied model.
Keeping the interpretation of **blue?**, its answer would change. Painting
the card is a different operation from renaming it.

## Your turn

Open the [explorer](explorer.html). Keep **blue?** selected. Rename a card,
then run the question. Say which part changed: the label, the card's
supplied features, the selected question, or its answer.

Before moving on, explain why different names alone give this machine no
way to tell A and B apart. The next lesson makes “tell apart” precise.

## Connection to the longer book

The supplied example prepares for Unit 00's separation of the external
constructor from the system, Unit 03's inert supply event, and Unit 07's
token erasure. Renaming a display label here is a teaching operation; it
is not an additional sealed event. [Exact sources](SOURCE_MAP.md).
