# 01. A form and a recorded instance

[Previous](00_ledger_and_demand.md) · [Search lab](README.md) · [Next: price](02_count_the_price.md)

## Build one answer in two steps

A **form** specifies how many entry positions a judgment has. A one-slot
form can be written `F(x)`. Here `x` is a placeholder to be filled by an
admitted entry. The number of slots is called the form's **arity**.

First admit a one-slot form F. Then record the **instance** `F(A)`:
that form filled with A. These are two additions. Having an empty form
does not supply any particular instance of it.

In this rule-free ledger, a well-formed instance succeeds exactly when
it has been recorded. Nothing else derives additional instances.

| Test | Fill with A | Fill with B |
|---|---|---|
| `F(_)` | `F(A)` is recorded | `F(B)` is not recorded |

`_` marks the place to fill. The test succeeds on A and fails on B, so
it witnesses their separation. A failed check here means **not derivable
under these rules**; it is not a proved negative fact about a physical item.

## Another answer uses two slots

Return to the original ledger, with no forms or instances. For an
alternative two-item answer, admit a two-slot form G and record `G(A, B)`.
The test `G(_, B)` succeeds on A and fails on B. This also meets the demand.

The two-slot form records ordered positions: `G(A, B)` and `G(B, A)` are
different instances. The positions and their order are supplied by this
grammar. The printed letters did not generate them.

A test may have several holes. Every hole is filled with the **same**
chosen entry. Thus `G(_, _)` becomes `G(A,A)` when filled with A, and
`G(B,B)` when filled with B. For our recorded link `G(A,B)`, this test
fails on both entries. `G(_,B)` is the witness that works here.

## What would not work?

- A form without a recorded instance supplies no successful test here.
- An instance on a form that has not been admitted is refused as
  ill-formed: the admission kernel reports `unknown form 0`.
- A rule saying that every tuple succeeds on the same new form makes
  every test on that form succeed for both entries. It does not separate them.

## Your turn

Record `G(A, A)` instead. Find a test with a hole that succeeds on A and
fails on B. State the form, what stays fixed, and what fills the hole.

AuthorityEffect: None. These are instances of the declared admission grammar.
