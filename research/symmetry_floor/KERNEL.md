# Why equivariant deterministic rules preserve held renamings

`AuthorityEffect: None.` Open research tree. Touches nothing under the seal.

This tree asks a narrower question: **what can a single-valued rule do when it
is explicitly required to agree with every declared renaming?** The answer is
that it cannot remove a renaming already held by the input. This is a
stabilizer-preservation result, not a claim that the state cannot change.

---

## 1. The obstruction

Take a rule `f` that carries one inscription to one inscription and explicitly
assume it agrees with each declared renaming. State dependence alone does not
imply this premise; the negative control in the tests is a state function that
fails it. Write `r` for a renaming. Then

    r(f(s)) = f(r(s)) = f(s)   whenever r(s) = s

**Whatever a renaming already left alone in the input, it leaves alone in the
successor.** The held set can only grow under an equivariant single-valued rule.
The successor may nevertheless be a different fully held state.

Proved in `lean/SymmetryFloor.lean` as `floor`, and iterated as
`floor_iterated`. Both **depend on no axioms at all**.

### What the proof does not assume

- `G` is not a group: no identity, no inverses, no associativity.
- `act` is not an action: no `act 1 x = x`, no composition law.
- `X` is not this carrier, not finite, not anything.

So the result is not about inscriptions. It holds for any notion of state and
renaming at every state fixed by the renaming in question. **A non-fixed start
does not evade the theorem; it falls outside its fixed-state hypothesis and
supplies asymmetry.** Equivariance and single-valuedness are both load-bearing.

---

## 2. The obstruction is the whole story, not a side condition

It would be easy to read §1 as a technicality that a cleverer rule might slip
past. It is not, and the reason is the converse.

Within the declared four-renaming carrier, `held(s) <= held(t)` is not merely
**necessary** for an equivariant rule to carry `s` to `t`. It is
**sufficient**: every such pair extends to an equivariant rule. Checked over all
30,625 pairs of the 175 inscriptions with at most two dividers and three data:
**zero disagreements**
(`floor.containment_matches_constructibility`).

So containment is the complete source-target description for equivariant rules
on this finite carrier.

### Counted, not argued

On a closed carrier of 8 inscriptions there are `8**8 = 16,777,216` maps. Every
one was enumerated by index arithmetic that never consults the characterisation
it is checking. Exactly **128** agree with the renamings, matching the
characterisation exactly (`floor.counted_rule_count`).

---

## 3. The exit, and its price

Drop single-valuedness. A step now offers a **set**. At a fully held source the
set must be invariant -- but its members need not be fixed individually. Every
such finite invariant set is a union of complete renaming orbits.

Computed over all orbit unions in the declared 175-inscription closed carrier
(`floor.price_of_a_break`):

| to break | costs |
| --- | --- |
| any one renaming | **2** offered successors |
| every renaming at once | **4** offered successors |

The smallest set that breaks everything is `<a|>`, `<b|>`, `<|a>`, `<|b>`. Those
four are one object. Nothing separates them and nothing selected one. **That is
what breaking a symmetry costs when there is no outside to do the selecting.**

Lean supplies the two-member witness and singleton lower bound as
`offered_set_carried`, `members_move`, and `price_is_two`. The four-member
all-renamings minimum is the finite orbit-union computation.

---

## 4. The declared branching growth relation

The step offers every result of adding **one glyph**, anywhere, with no selected
branch. It agrees with the renamings on the checked finite carrier;
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

**(b) The checked generations contain exactly one fully invariant object.** It
has no data -- `<>`, `<|>`, `<||>`, `<|||>`. These are different states along a
fully invariant thread, so their existence does not mean the state is immobile.
The branching relation selects no successor, and the invariant branch remains
one available branch through generation 8.

**(c) The world does not remember.** By generation 8 only **3 objects in 1681**
have a single possible past. The rest could have arrived up to eight different
ways and nothing in them says which. A history is therefore not something a
state *has*; it is something separately kept. A replayable event list is not a
convenience of such a design -- it is a requirement of it.

**(d) A break does not ratchet.** `<|a>` is held still by nothing; its successor
`<a|a>` is held still by a reflection. What is held can rise again.

---

## 5. Distance from the fully invariant thread

The thread of §4(b) contains the fully invariant object at each checked size.
Distance from it is the **data count**, and three bounded computations pin it
(`thread`, and the tests beside it):

1. **`held` is everything exactly when the distance is zero**, through source
   generation 7.
2. **One step never lowers the distance**, across every checked edge from
   source generations 0 through 7.
3. Therefore no checked path in this no-removal relation returns to distance
   zero after adding data. Other held renamings can return, by (d).

Within the declared no-removal relation, adding the first datum is what leaves
distance zero; adding a divider does not. The finite checks do not promote this
observation into an unbounded theorem.

### What can be held at each distance

| distance | held-set sizes available |
| --- | --- |
| 0 | 4 |
| 1 | 1 |
| 2 | 1, 2 |
| 3 | 1 |

Through generation 8, the composite renaming -- exchange the glyphs *and*
reflect -- holds no inscription with an odd data count. Reflection alone has
checked odd-data examples. No unbounded theorem is claimed here.

---

## 6. What this settles, and what it does not

**Settled.** For arbitrary types and renaming maps, an explicitly equivariant
single-valued rule preserves every renaming that fixes its input. A fully fixed
input therefore maps into the fully fixed locus. The theorem does not say the
successor equals the input, and it does not apply to a non-fixed start.

**Settled within the declared finite carrier.** Invariant offered sets need 2
states to break one non-identity renaming and 4 to break all three. The bounded
growth checks locate the first distance-zero departure at the first datum.

**Not settled.** Whether dropping a *different* one of the three is cheaper.
Supplying one asymmetry at the start, or refusing a first state at all, are the
two alternatives, and neither is priced here. They are named so they cannot
later be claimed as done.

**Not claimed.** That this is anything but a growth process that breaks
symmetry. No reading of it as any outside subject is offered or intended.
