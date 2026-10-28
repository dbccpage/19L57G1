# 01. A test and its witness

[Previous: names and answers](00_names_and_answers.md) · [First steps](README.md) · [Next: answer patterns](02_answer_patterns.md)

## Predict before reading

Keep the question **blue?** and the table from Lesson 00.

Can the machine tell A from C? Can it tell A from B? Give one reason for
each prediction.

## What “tell apart” means here

A **test** is a specified question together with the procedure for
obtaining its answer. In this example, the procedure reads a supplied
table. It does not inspect an actual physical card.

Two cards are **separated by a test** when that test gives different
answers on them.

- **blue?** answers yes on A and no on C. It separates A and C.
- **blue?** answers yes on A and yes on B. It does not separate A and B.

A **witness** is the particular test that demonstrates a separation.
For A and C, name **blue?**, then give both answers. That is more useful
than saying “they look different.” It states what the machine can use.

## One test is enough

Suppose we also make **triangle?** available. It answers no on A and yes
on B. That test witnesses their separation.

We do not need every test to disagree. A separation needs at least one
available test with different answers. The word **some** in a mathematical
statement often means “at least one,” and a witness tells us which one.

## A non-example

“A is called A and B is called B” names two labels. It does not identify
an available test of this machine with different answers. To use labels
as a test, we would have to supply that question explicitly.

## Your turn

In the [explorer](explorer.html), select only **triangle?**. Predict the
answers for A and C, then run the questions. Are they separated? State
the witness and the two answers, or explain why this question is not a
witness.

Now compare B and C under the same question. Keep what *you* can see
separate from the single answer the machine is allowed to read.

## Connection to the longer book

Unit 08 defines a context: a well-formed question with a hole that a datum
can fill. Units 19 and 20 construct particular separating contexts. Our
card questions are a finite teaching model. [Exact sources](SOURCE_MAP.md).
