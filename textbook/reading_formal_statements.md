# Reading a formal statement, one piece at a time

[Start here](START_HERE.md) · [Practice](reading_formal_practice.md)

The purpose of symbols is to say exactly which objects, conditions, and
conclusions are meant. Start by matching each name to a small example.

## 1. Name the objects before reading the formula

Use this supplied table. We keep only the blue answer, naming the groups
U and V. We want to recover triangle.

| Original card | Stored group label | Requested triangle answer |
|---|---|---|
| A | U | No |
| B | U | Yes |
| C | V | Yes |

A **domain** is the collection of allowed inputs. Here D lists A, B, C.
A **function** assigns one output to each of its inputs. Name the recorder
p and the requested-answer function q. Thus p(A)=U and q(A)=No.
We are looking for a lookup function g that receives only a stored label.

The letters name functions; they are not extra observations. A lookup
cannot inspect a card after receiving its label unless that access is
explicitly added to the model.

## 2. Read the equality as two routes

The desired equation is:

```text
g(p(x)) = q(x)
```

On the left, record x using p, then apply g to the stored label. On the
right, ask q on the original card. Equality requires the answers to agree.

For A the equation requires g(U)=No. For B it requires g(U)=Yes.
A function has one output at U, so this table has no successful lookup.
The specific conflicting pair explains the failure.

## 3. Add the two quantifiers

The full claim says:

```text
There exists a lookup g such that, for every x in D, g(p(x)) = q(x).
```

**There exists** means at least one suitable g satisfies the claim. **For every**
requires that same g to work for each listed input. Choosing a different
lookup for each card would change the statement.

Restrict D to A and C. Now U→No and V→Yes works. The smaller-domain claim
is true while the earlier three-card claim is false. Always carry the domain.

Unit 61 writes this shape as `FactorsOn D p q`. Its native functions have
natural-number inputs and outputs: 0, 1, 2, and so on. For an exact native
instance, encode A/B/C as 0/1/2, U/V as 0/1, and No/Yes as 0/1. Then p's
three recorded values are [0,0,1] and q's are [0,1,1]. The book check proves
the failed full-domain claim and successful smaller-domain claim with
that encoding. It does not silently change the native types.

## 4. Read a condition separately from an algorithm

A **type** states what kind of value a name may have. In Lean, `Prop`
is the type of statements. A field `Zero : R → Prop`
specifies a condition on reports of type R. It does not, by that type
alone, supply a program deciding the condition for every report.
`Bool` has the two values `true` and `false`; executing a function still
requires an implementation, not merely its name and type.

Unit 44's abstract observer has a difference function, a zero condition,
and proofs of the zero relation's equivalence laws. The proofs do not add
a required decision procedure. Its finite Python examples supply concrete
tests as additional implementations. Unit 67's quotient results can be
stated using the abstract condition without running such a test. The
quotient groups inputs related by that condition into classes, as in the Map lab.

This does not claim that every abstract observer is uncomputable. It says
the interface does not require a decider.

<details>
<summary>Optional: how the book checks this interface distinction</summary>

A proposition is a statement; P is its name here. A book-Lean example
uses an arbitrary supplied P: its two different
Boolean inputs are zero-related exactly when P holds. Constructing that
observer needs no `Decidable P` argument. Supplying a decider for that
specific zero question would supply a decider for P.

</details>

## 5. Separate the hypothesis from the conclusion

For the recovery criterion, the hypothesis says that whenever p merges
two inputs in D, q gives those inputs the same answer. The conclusion says
a suitable lookup exists on D. The theorem proves the implication; it
does not establish that your proposed p and q satisfy the hypothesis.

The actual finite-list construction in Unit 61 searches D for a matching
representative and expresses g using the given p and q. Running it also
requires implementations of those supplied functions. A different theorem's
existence statement should be read with its own proof and assumptions,
rather than inheriting this particular algorithm.

Read result labels the same way. In Unit 44's generic driver, `closed`
is the tag returned when its supplied next-step function returns `none`.
The book check gives such a return while a protected, retained zero-pair
is still active. To interpret the tag as “all demands met,” the particular
driver needs additional properties. A stopping label alone does not prove
that the intended job is finished.

Useful symbols, when they appear in the formal register:

| Notation | Read it as |
|---|---|
| `x ∈ D` | x belongs to D |
| `f : X → Y` | f is a function from inputs of type X to outputs of type Y |
| `∀ x` | for every x in the declared type |
| `∃ g` | there exists a g of the declared type |
| `A → B` between statements | if A, then B |
| `A ↔ B` | both if-A-then-B and if-B-then-A |
| `¬ A` | A is false |

The arrow is used in function types and in implications. Its surrounding
types tell you which reading is intended. See the [Reasoning lab](reasoning_lab/README.md)
for witnesses, counterexamples, and quantifier order.

## 6. Move from a familiar example to its formal owner

| Concrete route | Suggested next source reading |
|---|---|
| First steps | Units 08–10: the declared tests and their answers |
| Search lab | Units 17–22: the addition grammar and scoped prices |
| Change lab | Units 51, 54–55, 62: passage events, guards, and protection |
| Path lab | Units 59–60, 63: the separately declared attachment, cell, and graph settings |
| Map lab | Units 61 and 67: finite factorization and observer-quotient descent |
| Growth lab | Its research source map: commitments and supplied growth |
| [Boundary lab](boundary_lab/README.md) | Its research source map for the three distinct models; Unit 37 for the separate two-dot classification example |
| [Same-record lab](identification_lab/README.md) | Its research source map for equal-profile requirements, bounded matching calculations, and the limits of separation pruning |
| [Number lab](number_lab/README.md) | Unit 64 for the separate arithmetic definitions; its research source map for the admitted finite readout model and general invariant-readout bounds |

These are reading suggestions, not transport theorems between the models.
For example, the Path lab's graph edge and a function arrow have different
definitions. The [model map](change_lab/MODEL_MAP.md) identifies several
other owner boundaries.

For the worked material, open the [Map lab](map_lab/README.md),
[Unit 61](units/61_compressing_a_presentation_against_a_question_list.md),
[Unit 44](units/44_reflect_obstruct_close_or_propose.md), or
[Unit 67](units/67_descending_a_view_through_the_observer_quotient.md).
Try the [practice](reading_formal_practice.md) before its
[answers](reading_formal_answers.md).

AuthorityEffect: None. The table is supplied teaching data. The interface
example is checked by `textbook/checks/u44_observer_spec_lean.py`, outside
the seal. No undecidability theorem, physical correspondence, or novice
learning outcome is claimed.
