# Why nothing happens, and exactly what it costs to make something happen

`AuthorityEffect: None.` Open research tree. Touches nothing under the seal.

This tree answers one question and answers it exhaustively: **why a world built
from marks that mean nothing sits still, and what has to be given up for it to
move.** The answer is not that the right start has not been found yet. It is that
no start can work, and the reason is one line.

---

## 1. The obstruction

Take a rule `f` that carries one inscription to one inscription, computed from
the inscription alone. It cannot see which glyph is which -- glyphs are
forgettable -- so renaming the input renames the output. Write `r` for a
renaming. Then

    r(f(s)) = f(r(s)) = f(s)   whenever r(s) = s

**Whatever a renaming already left alone in the start, it leaves alone in the
successor.** What is held still can only grow, never shrink, for every rule, at
every step, forever.

Proved in `lean/SymmetryFloor.lean` as `floor`, and iterated as
`floor_iterated`. Both **depend on no axioms at all**.

### What the proof does not assume

- `G` is not a group: no identity, no inverses, no associativity.
- `act` is not an action: no `act 1 x = x`, no composition law.
- `X` is not this carrier, not finite, not anything.

So the result is not about inscriptions. It holds for any notion of state and
any notion of renaming whatever. **A different start cannot escape it, because
the start never entered the proof.** The starts are not the variable. Single-
valuedness is.

---

## 2. The obstruction is the whole story, not a side condition

It would be easy to read §1 as a technicality that a cleverer rule might slip
past. It is not, and the reason is the converse.

`held(s) <= held(t)` is not merely **necessary** for some rule to carry `s` to
`t`. It is **sufficient**: every such pair extends to a rule, and no other
constraint exists. Checked over all 30,625 pairs of the 175 inscriptions with at
most two dividers and three data: **zero disagreements**
(`floor.containment_matches_constructibility`).

So containment is the *complete* description of what a state-read rule may do.
There is no other freedom to find and no other constraint to evade.

### Counted, not argued

On a closed carrier of 8 inscriptions there are `8**8 = 16,777,216` maps. Every
one was enumerated by index arithmetic that never consults the characterisation
it is checking. Exactly **128** agree with the renamings, matching the
characterisation exactly (`floor.counted_rule_count`).

---

## 3. The exit, and its price

Drop single-valuedness. A step now offers a **set**. The set must still be
carried to itself -- but its members need not be. So a break becomes possible,
and it is not free: the set has to hold every way of presenting what it
contains.

Computed (`floor.price_of_a_break`):

| to break | costs |
| --- | --- |
| any one renaming | **2** offered successors |
| every renaming at once | **4** offered successors |

The smallest set that breaks everything is `<a|>`, `<b|>`, `<|a>`, `<|b>`. Those
four are one object. Nothing separates them and nothing selected one. **That is
what breaking a symmetry costs when there is no outside to do the selecting.**

Proved in Lean as `offered_set_carried`, `members_move`, `price_is_two`.

---

## 4. What the world then does

The step is declared once, and it is the weakest thing that is not nothing:
**one glyph appears**, anywhere, with nothing selecting where. It agrees with the
renamings because it was written without reference to which glyph is which, and
`thread.step_agrees_with_renamings` checks that rather than assuming it.

Every inscription of size `k` has a predecessor of size `k-1`, so generation `k`
is the complete set of inscriptions of size `k`. Nothing is sampled.

| generation | objects | closed form | held by every renaming | one possible past |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 |
| 2 | 4 | 4 | 1 | 3 |
| 4 | 25 | 25 | 1 | 3 |
| 6 | 196 | 196 | 1 | 3 |
| 8 | 1681 | 1681 | 1 | 3 |

### Four findings

**(a) The count has a closed form, and it factors.**

    a(n) = (3**n + 1) / 2
    objects(k) = a(ceil(k/2)) * a(floor(k/2))

Exact to generation 10. The count splits into two halves, which is the
reflection doing what a reflection does.

**(b) There is exactly one place where nothing happens, and it is always
available.** At every generation precisely one object is held still by every
renaming: the one with no data at all -- `<>`, `<|>`, `<||>`, `<|||>`. The
numerator never moves off 1 while the total grows like `3**k / 4`. **Nothing
compels the world to start.** Staying still is permanently available and never
gets any wider.

**(c) The world does not remember.** By generation 8 only **3 objects in 1681**
have a single possible past. The rest could have arrived up to eight different
ways and nothing in them says which. A history is therefore not something a
state *has*; it is something separately kept. A replayable event list is not a
convenience of such a design -- it is a requirement of it.

**(d) A break does not ratchet.** `<|a>` is held still by nothing; its successor
`<a|a>` is held still by a reflection. What is held can rise again.

---

## 5. Distance from the still thread

The thread of §4(b) is the one place nothing happens, so everything else is
measured by distance from it. That distance is the **data count**, and three
facts pin it (`thread`, and the tests beside it):

1. **`held` is everything exactly when the distance is zero.** The thread is not
   one still object among others; it is the only one there is.
2. **One step never lowers the distance.** Checked across the whole step relation
   to generation 8: zero descents.
3. Therefore **the thread is left once and never regained.** Every other
   symmetry loss can be repaired, by (d). This one cannot.

So the world has exactly one irreversible act, and it is the first datum. Not the
first divider -- dividers may be added forever with nothing broken. The first
**datum**. Everything after it is reversible in what it holds still; the return
to the thread is closed permanently.

### What can be held at each distance

| distance | held-set sizes available |
| --- | --- |
| 0 | 4 |
| 1 | 1 |
| 2 | 1, 2 |
| 3 | 1 |

A composite renaming -- exchange the glyphs *and* reflect -- can never hold an
inscription with an odd data count: a centre datum would have to be its own
exchange, and neither is. Reflection alone has no such obstruction, because its
centre may be a datum. Both checked to generation 8.

---

## 6. What this settles, and what it does not

**Settled.** The three-part condition the programme was working under --
a rule that is single-valued, a start, and nothing supplied -- is
over-determined. Pick all three and nothing moves, by theorem, in any carrier.
That is why no choice of start has worked and no future choice will.

**Settled.** The cost of the exit is exact: 2 offered successors to break one
renaming, 4 to break them all, and one irreversible act to leave the thread.

**Not settled.** Whether dropping a *different* one of the three is cheaper.
Supplying one asymmetry at the start, or refusing a first state at all, are the
two alternatives, and neither is priced here. They are named so they cannot
later be claimed as done.

**Not claimed.** That this is anything but a growth process that breaks
symmetry. No reading of it as any outside subject is offered or intended.
