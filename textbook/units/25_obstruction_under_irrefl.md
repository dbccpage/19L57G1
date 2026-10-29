# Unit 25. Under irreflexivity, collapsing a related pair is obstructed

**Claim.** Merging the ends of a recorded pair creates a self-pair in the
pushed relation. The definition calls this a collision. It calls it an
obstruction when the collision also violates the selected protected property.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Identify two points `a`, `b` of a relation by a map `c` with
`c a = c b`. If `r a b` was asserted, the identification *collides*: an
asserted edge has both ends sent to one point. A collision becomes an
*obstruction* only relative to a protected law the pushed-forward
relation violates; with irreflexivity protected, every such collision is
an obstruction, because the pushforward now asserts `c a` against itself.
With no law protected, the same collision is admissible.

**Status:** conditional (on the protected law). **Lean:**
`PrimDiff.obstruction_under_irrefl` (`lean4/Derivation/PrimDiff.lean` lines
220-227), with `Push` (165-167), `CollapseCollision` (172-176),
`FidelityObstruction` (178-183), `collision_not_irrefl` (199-203),
`bare_collapse_admissible` (205-212). **Axioms:** none. **Depends on:**
`Irrefl` (Unit 24), Unit 23 (the bare self-difference).

</details>

## First pass

Begin with exactly `P → Q` on two points. A map sends both P and Q
to one target point M. To **push the relation forward**, send each
arrow's ends through that map. The result is `M → M`.

Three separate questions now have answers:

| Question | Answer |
|---|---|
| Can we construct the pushed relation? | Yes: it contains `M → M` |
| Did one source arrow's ends merge? | Yes: this is a collision |
| Does the target satisfy “no self-pairs”? | No |

If no-self-pairs is the protected property, the last two answers give
an **obstruction** in this definition. If the chosen property always
holds, the same map has a collision without an obstruction.

Neither verdict executes or prevents a merge. The model supplies a
relation, a map, and a property to check; an enforcement mechanism would
be additional structure.

**Predict:** must the source itself satisfy no-self-pairs for the
collision theorem to apply? Read the answer after trying the main example.

<details>
<summary>Check your prediction</summary>

No. The theorem assumes an asserted pair and a map identifying its
ends. A one-point self-pair with the identity map also meets those
hypotheses. The theorem does not certify that the source satisfied the
protected property before the map.

</details>

## Question

What happens to a recorded pair when a map sends both ends to one
target point? Which selected property does the target relation violate?

## What we already possess

- `Irrefl` and the fact that a self-pair refutes it (Units 23, 24).
- The idea of a map between carriers, `c : α → β`, and of two points
  being *identified* by it: `c a = c b`.
- A relation on the target can be built from a relation on the source by
  pushing edges along the map.

## New concept: pushforward, collision, obstruction

Three definitions, each a plain construction on relations and functions.

- **Pushforward.** `Push r c x y :⇔ ∃ u v, r u v ∧ c u = x ∧ c v = y`:
  the target relates `x` to `y` when some source edge is sent onto them.
- **Collision.** `CollapseCollision r c :⇔ ∃ u v, r u v ∧ c u = c v`: some
  source edge has both ends identified. Stated positively, as an
  existence, so a collision is a thing one can exhibit.
- **Obstruction.** `FidelityObstruction P r c :⇔ CollapseCollision r c ∧
  ¬ P (Push r c)`: a collision *together with* a protected property `P`
  that the pushforward fails.

This definition requires both parts. It is not a test for every possible
failure of `P`, and it does not include `P r` as a premise. For a claim
that a previously satisfied property was lost, check the source property
separately. The optional transitivity example below shows a property
that holds before a map and fails after it without a collision.

The theorem says: if `r a b` and `c a = c b`, then
`FidelityObstruction Irrefl r c`. The collision is immediate (the edge
`(a, b)`). The law fails downstream because `Push r c (c a) (c a)` holds,
the edge having been sent onto one point, and that is a self-pair.

Two things the statement does *not* assume. It does not assume `r` is
irreflexive: the law is protected in the *conclusion*, as the property
the pushforward must keep, and the book's check applies the theorem to
the self-difference on `Unit` with the identity map. And it does not
assume anything about the rest of `r` or `c`.

## Plain-language interpretation

Two entries in the ledger are recorded as different. Someone proposes to
merge them into one. Three readings of what happens:

1. **Bare.** The pushed relation can be constructed. It now says the one
   entry differs from itself, which the bare rules permit (Unit 23). The
   recorded difference is not lost; it is carried onto the merged entry
   (`push_witness`). The always-true protected property gives no obstruction.
2. **Collision noticed.** Whatever the rules, the merge sent a recorded
   difference onto a single entry. That is a fact about the merge, and
   it holds with or without any law (`collision_of_identifying_witness`).
3. **Irreflexivity protected.** The merged ledger would break the rule
   "nothing differs from itself". Relative to keeping that rule, the
   merge is obstructed.

For this proposed map, collision is present under either choice of
protected property. The pushforward exists in both cases. The verdict
changes when irreflexivity replaces the always-true property. This is
the source's fidelity dichotomy. It supplies no operational rule that
executes or rejects the map.

There is a useful analogy to checking demands in an admission regime,
but the two models have different data and operations. The admission
guard, response-validity check, relation pushforward, and
`FidelityObstruction` are separate definitions. This unit supplies no
theorem translating one mechanism into another.

<details>
<summary>Optional boundary case: a property can be lost without this obstruction</summary>

A relation is **transitive** if having `x → y` and `y → z` always
means it also has `x → z`. Take four points with exactly two arrows,
`0 → 1` and `2 → 3`. There is no two-arrow chain, so this relation
is transitive: the condition has no chain to complete.

Map point 2 to point 1 and leave the others fixed:

```text
Before:  0 → 1     2 → 3
After:   0 → 1 → 3       (no 0 → 3)
```

Neither arrow's own ends merge, so there is no collision. But the new
relation is not transitive: the displayed chain is missing its shortcut.
The source satisfies the chosen property and the target fails it,
yet `FidelityObstruction` is false because its collision conjunct fails.

This supplied book example marks the definition's scope. It is not a
claim that transitivity should be protected. The Python check calls the
native merge and pushforward functions; four book proofs check these
claims on `Fin 4`.

</details>

## Pseudocode

```
# Gloss
given r a b, and a map c with c a = c b:
  collision: the edge (a, b) is sent to one point.            -- always
  pushforward: Push r c (c a) (c a) holds, via (a, b).
  protect Irrefl: Push r c must have no self-pair; it has one.  -- fails
  so FidelityObstruction Irrefl r c.
protect nothing: the pushforward exists and carries the pair; admissible.
```

## Python

```python
from derivation.primdiff import D2, collision, irreflexive, merge_map, pushforward

f = merge_map(2, 0, 1)
pushed = pushforward(D2.rel, f)
print(f, sorted(pushed), collision(D2.rel, f), irreflexive(pushed))
print(collision(D2.rel, (0, 1)))
```

Output:

```text
(0, 0) [(0, 0)] True False
False
```

## Line-by-line Python explanation

`merge_map(2, 0, 1)` (`primdiff.py` line 102) is the map on two points
sending both to 0, written as the tuple `(0, 0)` (position `i` holds the
image of `i`).

`pushforward(rel, f)` (line 319) is `{(f x, f y) for (x, y) in rel}`:
`D2`'s single edge `(0, 1)` becomes `(0, 0)`.

`collision(rel, f)` (line 323) is `any(f x == f y for (x, y) in rel)`:
`True`. `irreflexive(pushed)` is `False`: the pushforward has a
self-pair. The two outputs are the two halves of the obstruction.

The identity map `(0, 1)` does not collide: `False`.

`collapse_report(3)` (line 376) checks, over all 27 776 merges of
pointed structures with carrier at most 3, that collision holds exactly
when the pushforward fails irreflexivity, that collision is invariant
under transposing the relation, that identifying a witnessed pair always
collides, and that the pushforward always exists. The check script reruns
it and compares with the artifact, and shows a non-irreflexive relation
colliding too (the theorem needs no law on the source).

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/PrimDiff.lean lines 165-183, 199-203, 219-227
def Push {α β : Type} (r : α → α → Prop) (c : α → β) : β → β → Prop :=
  fun x y => ∃ u v, r u v ∧ c u = x ∧ c v = y

def CollapseCollision {α β : Type} (r : α → α → Prop) (c : α → β) : Prop :=
  ∃ u v, r u v ∧ c u = c v

def FidelityObstruction {α β : Type}
    (P : (β → β → Prop) → Prop) (r : α → α → Prop) (c : α → β) : Prop :=
  CollapseCollision r c ∧ ¬ P (Push r c)

theorem collision_not_irrefl {α β : Type} {r : α → α → Prop}
    {c : α → β} (h : CollapseCollision r c) : ¬ Irrefl (Push r c) := by
  intro hi
  obtain ⟨u, v, huv, hc⟩ := h
  exact hi (c u) ⟨u, v, huv, rfl, hc.symm⟩

theorem obstruction_under_irrefl {α β : Type} {r : α → α → Prop}
    {a b : α} (h : r a b) {c : α → β} (hc : c a = c b) :
    FidelityObstruction Irrefl r c :=
  ⟨collision_of_identifying_witness h hc,
   collision_not_irrefl (collision_of_identifying_witness h hc)⟩
```

```lean
-- Lean (book), textbook/checks/u25_lean.py
theorem obstruction_iff_collision {α β : Type} (r : α → α → Prop)
    (c : α → β) : FidelityObstruction Irrefl r c ↔ CollapseCollision r c :=
  ⟨fun h => h.1, fun h => ⟨h, collision_not_irrefl h⟩⟩

theorem no_obstruction_without_law {α β : Type} (r : α → α → Prop)
    (c : α → β) : ¬ FidelityObstruction (fun _ => True) r c :=
  fun h => h.2 trivial

/-- No irreflexivity premise on `r`: the self-difference with the identity. -/
theorem obstruction_without_irrefl_premise :
    FidelityObstruction Irrefl (fun (_ : Unit) _ => True) id :=
  obstruction_under_irrefl (a := ()) (b := ()) trivial rfl
```

## Line-by-line Lean explanation

**`collision_not_irrefl`.** Assume `hi : Irrefl (Push r c)`. Open the
collision: `u`, `v`, the edge `huv : r u v`, and `hc : c u = c v`.
Irreflexivity at the point `c u` says `¬ Push r c (c u) (c u)`. But
`⟨u, v, huv, rfl, hc.symm⟩` is a proof of exactly that: the source edge
`(u, v)`, with `c u = c u` by `rfl` and `c v = c u` by `hc.symm`. So
`hi (c u) (…) : False`.

**`obstruction_under_irrefl`.** The conclusion is a conjunction. First
part: `collision_of_identifying_witness h hc`, which is just
`⟨a, b, h, hc⟩` (lines 194-197). Second part: the previous theorem
applied to that same collision. The proof builds the collision twice
rather than naming it once; the book's `obstruction_under_irrefl'`
writes the two parts out with `constructor`.

**`obstruction_iff_collision` (book).** Under the protected law
`Irrefl`, the second conjunct is a consequence of the first, so
obstruction and collision coincide. This is what makes the law the
whole content of "obstruction": with `P := fun _ => True` nothing is
ever obstructed (`no_obstruction_without_law`, since `¬ True` is
unprovable), and with `P := Irrefl` every collision is.

**`obstruction_without_irrefl_premise` (book).** The theorem's `r` is the
always-true relation on `Unit`, `a = b = ()`, `c = id`. The identity
identifies `()` with `()`, trivially; the relation is not irreflexive;
the conclusion still holds. So the conditionality of this unit is in
the *protected* law, not in a hypothesis about the source. The
sentence "under irreflexivity" in the title means "when irreflexivity is
what is protected".

**Axioms.** The Genesis results and original seven book reports use none.
The four added finite transitivity reports use `propext`; they are
separate teaching proofs inside the existing library-axiom boundary.

## What has been proved

- Identifying a witnessed pair always collides, law or no law (Genesis,
  derived).
- A collision makes the pushforward non-irreflexive (Genesis, derived).
- Hence, relative to `Irrefl`, collapsing a witnessed pair is obstructed
  (Genesis, derived; the ledger's "collision exists without any protected
  law and rises to obstruction only relative to `Irrefl`").
- Without a protected law the collapse is admissible: the pushforward
  exists and carries the pair (Genesis, `bare_collapse_admissible`,
  `collapse_unobstructed_without_fidelity`).
- Under `Irrefl`, obstruction is exactly collision; under the trivial law
  nothing is obstructed; the theorem needs no law on the source (book).
- Within carrier 3, all four computed invariants over 27 776 merges
  (Genesis engine, verified finite).
- A supplied four-point example is transitive before the map and not
  after it, with no collision and hence no `FidelityObstruction` for
  transitivity (book). General property loss is a broader question.

## What has not been proved

- That any particular law *should* be protected. `Irrefl` is studied
  here for its exact relation to inequality (Unit 24). The claim is not
  that every other law has no consequences or that all laws were searched.
- That the engine's Challenge 3 machinery is an instance of
  `FidelityObstruction`. The analogy is the book's; the frozen
  derivation does not state such a bridge, and the book does not invent
  one.
- Orientation. `collision_transpose_invariant` (lines 229-237) shows the
  collision level cannot see which way an edge points: transposing `r`
  changes nothing about which maps collide. An observer that cares about
  orientation needs more than this layer provides.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `c : α → β`, `c a = c b` | the identification | a metatheory map; nothing in the structure performs merges |
| `Push`, `CollapseCollision` | the constructions | metatheory definitions on relations |
| `P`, instantiated to `Irrefl` | the protected law | declared; the parameter is explicit in `FidelityObstruction` |
| `id`, `Unit`, `trivial` | the premise-free instance | metatheory |

**What the system holds.** In the primitive-difference model: a relation
and, optionally, a protected property. The obstruction is a verdict the
metatheory passes on a proposed map, relative to that property. The
structure does not refuse the map. The metatheory can prove a verdict
about it; executing or enforcing that verdict needs an additional policy.

**Phrases to read with care.**

- "Obstructed" is always "obstructed relative to `P`". Genesis's
  definition carries `P` as an argument so that the phrase cannot be
  written without it.
- "Collision" is not a failure. It is an observation about a map,
  available before any law is chosen.

## Student exercise

Take `S2` (both orientations asserted on `Bool`) and the merge to one
point. Is it a collision? An obstruction under `Irrefl`? What is the
pushforward, and does the pushforward "remember" that two edges were
merged, or one?

## Answer

<details>
<summary>Worked answer</summary>

Yes and yes: `(false, true)` is an asserted edge whose ends are
identified, so `obstruction_under_irrefl (Or.inl D2_witness) rfl` applies
with `c := fun _ => ()`. The pushforward is the relation on `Unit`
holding of `((), ())`, the self-difference of Unit 23. It does not
remember how many edges were merged: the pushforward of `D2` under the
same map is the same relation. The collision level sees the
symmetrization only, which is the content of
`collision_transpose_invariant`.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/PrimDiff.lean` lines 165-183 (definitions), 185-212 (`push_witness`, `collision_of_identifying_witness`, `collision_not_irrefl`, `bare_collapse_admissible`), 214-227 (`collapse_unobstructed_without_fidelity`, `obstruction_under_irrefl`), 229-237 (`collision_transpose_invariant`) |
| Axiom report | `artifacts/lean_axioms.txt`: `obstruction_under_irrefl`, `collision_not_irrefl`, `bare_collapse_admissible`, `collapse_unobstructed_without_fidelity` do not depend on any axioms |
| Paper | `paper/primitive_difference.md` S3 ("Collision versus obstruction (the fidelity dichotomy)"), the scoped answer at the end of S3; `paper/observer_inventory.md` on the two defect readings |
| Ledger | `paper/paper_claim_ledger.md`, `CL-PD-INVENTORY` (cites `PrimDiff.obstruction_under_irrefl` and `PrimDiff.collapse_unobstructed_without_fidelity`: "the two defect readings stay distinct") |
| Artifact | `artifacts/primdiff.json`, `collapse`: `merge_cases_checked = 27776`, `collision_iff_pushforward_not_irreflexive`, `collision_transpose_invariant`, `identifying_witnessed_pair_always_collides`, `pushforward_always_exists`, all `true` |
| Test | `tests/test_primdiff.py::test_collapse_collision_and_pushforward` |
| Check (Python) | `python textbook/checks/u25_obstruction.py`: the `D2` merge; identity and non-irreflexive-source cases; `collapse_report(3)` matches the artifact; 3 872 witnessed-pair collisions among 13 888 unordered merges; separate four-point transitivity-loss example without collision |
| Check (book Lean) | `python textbook/checks/u25_lean.py`: eleven book reports plus four Genesis results kernel-checked, Lean 4.33.0; the four added transitivity reports use `propext`, the original eleven reports use no axioms |
