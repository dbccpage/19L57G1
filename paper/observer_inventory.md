# Nine-slot inventory of existing objects

**Goal.** Record a declared classification of objects this derivation
already has, as a nine-slot tuple in which each slot is named for what
it hosts — the carrier, the local state, its support, the defect
readings, the reversal maps, the optional closure, the residuals, the
maps, and the terminal slot — instantiated on the two-element fragment
of `paper/primitive_difference.md`.  The inventory is not a dynamics,
not a next challenge, and not a necessity claim about any slot.

**Protocol.** Constructive facts first, in the names already used by
`lean4/Derivation/PrimDiff.lean` and `lean4/Derivation/ObserverInventory.lean`.
Finite checks live in `code/derivation/observer_inventory.py` with
artifact `artifacts/observer_inventory.json`.  Objects that live in
other modules are *named* as citations; this paper does not re-prove
them and does not import them into the Lean instance.

Statement tags as in the companion paper: **[declared metatheory]**,
**[definition]**, **[finite computation]**, **[theorem]**,
**[bounded theorem]**, **[conjecture]**, **[counterexample]**,
**[unresolved]**.

---

## 1. What the inventory is

**[declared metatheory] — provenance and refusal.** A classification
grid of nine single-letter slot names, together with an outside phrase
for the pair of maps in the reversal slot, was offered through the
operator channel on 2026-08-31 and refused as vocabulary by author
ruling.  The classification *content* — the census, the residuals, the
theorems — is internal and was retained under this repository's own
words; the offered names appear nowhere in this repository, and this
note deliberately describes the offer without reproducing it.  Any
future claim of independent convergence between this inventory and an
external slot grid is false by construction.  Nothing below treats
the carving as derived, and nothing below authorizes a response to a
challenge.

**[definition]** (`ObserverInventory.Slot`, `slotList`) The slots are
`carrier`, `local_state`, `support`, `defect`, `reversal`, `closure`,
`residual`, `maps`, `terminal`.
**[theorem]** (`slot_count`, `slots_nodup`) There are nine, and the
list has no repetition.

On the two-element fragment they bind as follows.

| slot | binding on `Bool` |
|---|---|
| `carrier` | the carrier `Bool` |
| `local_state` | a local pair-state: empty, `D2`, `D2rev`, or `S2` |
| `support` | that same relation, read as support |
| `defect` | collision of a collapse map, versus obstruction relative to `Irrefl` |
| `reversal` | relation `Transpose`, and pushforward along `Bool.not` |
| `closure` | `Clos`; the empty family is the identity |
| `residual` | more than one residual (`edgeCount`, `isSymBit`) |
| `maps` | `Bool.not` is an automorphism of `S2` and not of `D2` |
| `terminal` | underdetermined: `Irrefl` does not single out a local state |

Witness assignments are extra data on pairs, not a tenth slot of the
supplied tuple.  They are recorded here because the tuple was asked to
host them, and because the existing A2 theorems already separate
presence from multiplicity.

Objects named elsewhere, not proved in this instance:
`PrimitivePassage.PState.occ` as a larger carrier, `PState.wit` as a
witness store, `obstP` as a later obstruction reading,
`Attachment.up_iff_legal` as one-edge *supply* (not a reversal map),
`AttachOutcome` / `PState.licensed` / `PState.halted` /
`Horizon.worldAt_quiescent` as status fields that could fill the
terminal slot in a history-bearing module.  Those names are
citations.  Filling the slots with them is an operator reading, not a
theorem of this file.

## 2. Local states

**[definition]** (`EmptyRel`) The empty relation on `Bool`.
**[theorem]** (`empty_irrefl`) It is irreflexive.
**[theorem]** (`empty_ne_D2`) It is not `D2`.

**[theorem]** (`bool_irrefl_full_classification`) Every decidable
irreflexive relation on `Bool` equals `EmptyRel` or `D2` or `D2rev`
or `S2`.  The census quantifies over pointwise-decidable relations
(`[∀ x y, Decidable (r x y)]`), as the pointed census already does.
**[finite computation]** The same census on `range(2)` has four
relations, exactly those four (`observer_inventory.json:irrefl_census`).

The nonempty fragment remains
`PrimDiff.bool_irrefl_nonempty_classification`.  Carrier 3 is outside
this census.

## 3. Witnesses are data

**[definition]** (`zeroW`, `oneW`) The zero assignment, and the
assignment with one witness on the oriented pair and none on the
reverse.

**[theorem]** (`witnesses_are_data`) The two assignments are
unequal; `oneW false true = 1` and `oneW true false = 0`; the zero
assignment has empty presence; the one-oriented assignment has
presence relation `D2`.

This is the model already named
`PrimDiff.single_oriented_witness_consistent`.  It is an existence
fact, not a uniqueness fact.  Multiplicity remains invisible to
presence (`PrimDiff.multiplicity_invisible_to_presence`).  A second
same-orientation witness is likewise not derived as necessary.

**[finite computation]** The Python mirror records the same
inequalities (`observer_inventory.json:witnesses`).

## 4. Two defect readings

**[theorem]** (`collision_is_not_obstruction`) There is a relation
on the one-point carrier that asserts its pair and is not
irreflexive.  Collision of a collapse map can hold of a structure
that remains a legitimate bare assertion
(`PrimDiff.collapse_unobstructed_without_fidelity`).  Obstruction
relative to `Irrefl` is the same collision plus the protected law
(`PrimDiff.obstruction_under_irrefl`).  The two readings occupy the
defect slot as a pair; they are not fused.

**[finite computation]** On carrier 2, `D2` and `S2` collide under
the merge of the two points while remaining irreflexive as sources;
the empty relation does not collide under that merge
(`observer_inventory.json:defect`).

## 5. Two reversal maps

**[definition]** (`pushNot`) Pushforward of a relation along
`Bool.not`.

**[theorem]** (`transpose_involutive`) `Transpose` is an involution
on relations: two applications restore the original.  The square is
the identity, not a distinct opposite.

**[theorem]** (`transpose_D2_eq_D2rev`, `transpose_D2rev_eq_D2`)
Relation transpose carries `D2` onto `D2rev` and back.

**[theorem]** (`pushNot_D2_eq_D2rev`) Carrier-swap pushforward
likewise carries `D2` onto `D2rev`.  That is the map already named
`PrimDiff.swap_carries_D2_to_D2rev`.

**[theorem]** (`transpose_eq_pushNot_on_D2`) The two operations
agree as output on `D2`.

**[theorem]** (`transpose_ne_pushNot`) They are not the same
operation: there is a relation (a self-loop) on which they disagree.
**[finite computation]** `{(0,0)}` is that countermodel
(`observer_inventory.json:reversal`).

The reversal slot is therefore two maps that happen to agree on the
oriented two-element object.  Identifying them as operations is false.
`Attachment.up_iff_legal` is one-edge supply with a fresh token; it
is not a reversal map of this fragment, and does not occupy the
reversal slot.

## 6. Closure, residuals, maps, status

**[theorem]** (`closure_empty_family_is_identity`) Closure of the empty
operation family is the identity (`PrimDiff.clos_empty_id` on
`Bool`).  Higher cells are optional on this fragment.

**[definition]** (`edgeCount`, `isSymBit`) Two `Nat`-valued
readings of a local state: off-diagonal occupancy, and the
both-orientations bit.

**[theorem]** (`residuals_not_unique`) `edgeCount D2 = 1`,
`edgeCount S2 = 2`, `isSymBit D2 = 0`, `isSymBit S2 = 1`, and the
two readings disagree on `D2`.  No unique residual is derived from
the local state.  Cost measures `mu1`/`mu2` and `PState.budget` live
elsewhere and are not selected here.

**[theorem]** (`swap_not_auto_of_D2`, `swap_not_auto_of_D2rev`)
`Bool.not` is not an automorphism of `D2`
(`PrimDiff.swap_auto_of_S2_not_of_D2`), nor of `D2rev` — it carries
each orientation onto the other.  It is an automorphism of `S2`.
That is the maps distinction on this fragment.

**[theorem]** (`empty_ne_D2`, with `empty_irrefl` and `D2_irrefl`)
Both empty and `D2` are legal irreflexive local states, so
irreflexivity does not determine the local state: two distinct
states satisfy the constraint.  An earlier draft of this sentence
concluded that no next state is "a function of" the carrier and
local state; that was a non-sequitur (the identity is such a
function) and is WITHDRAWN in favour of the underdetermination
statement above, which is what the cited theorems prove.
History-bearing status fields named above remain the place a
terminalizer would be recorded, when one is declared.

## 7. What this does not claim

**[declared metatheory]** The inventory does not produce a unique
residual, a unique next state, or a necessity that any particular
witness assignment inhabit the store.  It classifies objects that
already exist.  Carrier 3, loops as 2-cells, and every
history-bearing filling of the terminal slot remain outside the
two-element instance.
