# 01. A function gives one answer per input

[Previous](00_rule_and_record.md) · [Reasoning lab](README.md) · [Next](02_read_if.md)

## Predict first

We write `A → Yes`, `B → Yes`, `C → No`. Is there anything wrong with
A and B receiving the same output?

## Fix the inputs and outputs

A **function** assigns exactly one output to each input in its declared
**domain**, the collection of inputs it covers. Here the domain is A, B,
C and the allowed outputs are Yes and No. The blue column is a function.
The arrow means “is assigned to.”

Two inputs may receive the same output. A and B both receive Yes.
The forbidden situation is one input receiving different outputs in
the same function: `A → Yes` and `A → No`.

If a supposed table for this whole domain gives no output for C, it is
incomplete as a function on A, B, C. We could instead declare a smaller
domain, but we must say so.

## A second function cannot undo every merge

Suppose a machine keeps only the blue answer. Could a second function
recover **round?** from that answer alone?

A and B give the same kept input, Yes. But their round answers differ.
The second function would have to send Yes to both Yes and No. That
cannot be one function. The pair A/B blocks this recovery task.

This does not say no recovery is possible with additional information.
Keeping both blue and triangle answers changes the input to the task.

## Your turn

Keep only **round?** instead. Find two cards with the same kept answer
but different blue answers. Explain why they block recovery of blue.

AuthorityEffect: None. The source map connects this example to factorization.
