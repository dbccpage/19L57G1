# Typed translation: frozen predictions

`AuthorityEffect: None.`

These predictions are frozen beside `REQUIREMENTS.md` before implementation.
Each is scored mechanically as `HIT`, `MISS`, or `PENDING`.  `FORCED` means the
statement follows from a declaration in the frozen design and is not counted
as discovered content.  `NOT FORCED` means the implementation or proof can
falsify it.  A missed prediction is preserved here and explained beside its
computed value in `STATUS.md`; this file is never repaired to fit an answer.

## P1 — candidate population

**FORCED.** The Cartesian candidate space contains exactly 128 points, with no
pruning, and an independent product enumerator returns the same ordered tuples.

**Falsifier:** either enumerator returns a count other than 128, their ordered
coordinate tuples differ, or any candidate is omitted before evaluation.

## P2 — a bounded typed map exists

**NOT FORCED.** At least one candidate preserves tasks, event kinds, carrier
fields, commuting replay, typed round trips, and total nearby-shell refusals on
the complete frozen spaces.

**Falsifier:** the valid-candidate population is empty, or a reported candidate
has any named counterexample to one preservation clause.

## P3 — the map needs two semantic capabilities

**NOT FORCED.** Every valid candidate uses state-sensitive event translation
and administrative presentations; at least one valid candidate needs no other
non-default semantic capability.  Its statement-price field is therefore two.

**Falsifier:** a memoryless or no-administrative-supply candidate is valid, or
every valid candidate requires a third semantic capability.

## P4 — exact cost fails, with a computed price

**NOT FORCED.** No valid candidate preserves both common measures exactly.
For a least-statement-price valid candidate, maximum forward additive
distortion is 4 for `mu1` and 12 for `mu2` over the complete history census.

**Falsifier:** an exact candidate exists, no priced map exists, or either named
maximum differs from `(4, 12)`.

## P5 — address orientation is a tie

**NOT FORCED.** Exactly two least-price valid candidates survive, differing
only by direct versus complemented outer-side orientation, and their complete
behavior and distortion records are equal after the declared orientation
quotient.

**Falsifier:** the least-price valid count is not two, a further coordinate
differs, or the behavior records remain non-isomorphic under the quotient.

## P6 — the exact-cost obstruction is theorem-level

**NOT FORCED.** Lean proves both: a fixed memoryless rule block cannot preserve
profile equality at the no-instance and one-instance witnesses; and a nonempty
outer-symmetric image of the one source form admission has at least two target
admissions, so `mu1` cannot remain one.

**Falsifier:** either theorem fails to elaborate, is absent from the axiom
inventory, uses an axiom outside `{propext, Quot.sound}`, or its hypotheses do
not match the candidate contract it is cited for.

## P7 — the projected `OR` does not erase provenance

**NOT FORCED.** The map preserves the instance bits, rule bit, events, and
decoded history separately even when distinct source states have equal profile
bits.  At least one equal-profile pair differs in both retained source fields
and translated provenance labels.

**Falsifier:** decoding identifies such a pair, the receipt omits the separate
fields, or equality of the profile projection is reported as state equality.

## P8 — total removal score

**NOT FORCED.** The hand-written dependence map hits exactly 22 of its 37 rows.
The actual experiment names exactly these 15 wrong rows:

`R09, R13, R15, R16, R17, R18, R20, R21, R23, R25, R29, R30, R32, R33, R34`.

**Falsifier:** the vendored population is not 37, the exact-class hit count is
not 22, or the mechanically produced wrong-row id set differs.

## P9 — removal is mixed more often than the prose map says

**NOT FORCED.** Every wrong row in P8 is mechanically `MIXED`: at least one
component survives and at least one changes or becomes `NOT_FORMULATED`.

**Falsifier:** any P8 row is actually `INDEPENDENT` or `DEPENDENT`, or any miss
arises from a prose parser failure rather than before/after probe values.

## P10 — the nearby shell is refused completely

**NOT FORCED.** Every deduplicated non-typed state in the frozen nearby shell
receives a named refusal, with zero silent truncations and at least one example
of each frozen refusal code.

**Falsifier:** a shell state is silently decoded, lacks a refusal, a refusal
code is unused, or the shell population is empty.

## P11 — global extension remains open

**FORCED.** A passing finite computation does not establish a translation for
unbounded data, forms, arities, addresses, histories, or permitted-renaming
systems.  The result remains `OPEN_AT_BOUND` outside the exact frozen carrier
unless a separate general proof is added.

**Falsifier:** a Lean theorem in this tree quantifies over the unbounded source
and target carriers and proves all four preservation clauses without adding an
assumption stronger than this frozen contract.
