# 04. Recover an answer

[Previous: keep or replace](03_keep_or_replace.md) · [First steps](README.md) · [Practice](PRACTICE.md)

## A new task

Suppose a recorder keeps only the answer to **blue?**. Someone asks:
“Was the card triangular?” The original card is no longer available to
the recorder.

Can it always answer from its stored information? Predict first.

## Find the pair that blocks recovery

A and B both produced **yes** to **blue?** But A was circular and B was
triangular. The recorder would receive the same stored input in both
cases and need to produce different requested answers.

No rule using only that stored answer can always work on our three
cards. The pair A, B is a **blocking witness**: the retained information
merges them while the requested question separates them.

## What successful recovery looks like

Suppose the requested question is **blue?** itself. Recovery is easy:
return the stored answer.

If the recorder instead stores both **blue?** and **triangle?**, it can
recover **triangle?** by returning the second answer. Nothing needs to
be guessed.

**Recoverable** means that one rule gives the requested answer for every
item in the declared list using only its recorded pattern. Every pair
with the same recorded pattern must therefore need the same requested
answer. In the longer book, this is called **factoring through** the
recorded presentation.

## Two names for things you have already used

A **presentation** assigns a value to each item. Our recorder's presentation
assigns the stored answer pattern to each card.

A **fiber** is one group of items assigned the same value. When we record
only **blue?**, the Yes fiber contains A and B; the No fiber contains C.

“The requested answer is constant on each fiber” means that it does not
change within any one recorded group. For **triangle?**, the Yes fiber
fails this check: A needs No and B needs Yes. That is the blocking pair
we found above.

## A non-example

Guessing “yes” whenever the stored answer is yes happens to work for B.
It fails for A. Success on one case does not establish a rule that works
on every case in the declared list.

## Your turn

In the [explorer](explorer.html), record only **triangle?** and ask it to
recover **blue?**. Predict whether it can. If recovery fails, give the
blocking pair and both requested answers.

Then record both questions and repeat the task. Explain what additional
information made recovery possible.

## Take the idea outside this example

Imagine a real device that records a single lamp's on/off answer. Before
using it to recover another measurement, ask which physically different
cases can give the same recorded answer. Could the requested measurement
differ between those cases?

That is a question to investigate. A real measurement correspondence must
be checked: the device may have errors, untested cases, or a different
response rule. Our three-card table supplies no measurements of such a
device. It gives a way to formulate the question precisely.

## Connection to the longer book

Unit 61 relates factorization to constancy on fibers. Institution 02
uses this precise recoverability condition for its defined word “knows.”
That definition does not assert the truth of a supplied target claim.
[Exact sources](SOURCE_MAP.md).
