# Unit 03. Information counts the classes a family cuts the carrier into

**Claim.** The information of a family is the number of signature classes
on the carrier. It never exceeds the carrier, never falls when the family
grows, and stays the same when a claim is added exactly when the family
knows that claim: `Knows D Q q ↔ information D (Q ++ [q]) = information D Q`.
**Status:** derived. **Lean:** `Institution.knows_iff_information_eq`
(`two_theorems`), with `information_le_carrier`, `information_mono` and
`information_lt_of_not_knows`. **Sources:**
`research/two_theorems/lean/ResearchTwoTheorems/Institution.lean` lines
61–63, 137–139, 155–182, 186–190, 209–246, 248–287, 291–300;
`lean4/Derivation/Compression.lean` lines 519–521, 549–551, 582–585,
599–625, 692–698, 343–347, 713–.

"Information" is the second word of this part that wants to mean more than
it does. Here it is a number: how many groups of data the family's members,
taken together, can tell apart. This unit proves four things about that
number and then ties it to Unit 02's "knows": a family knows a claim
exactly when adding the claim leaves the number where it was.

## What you need first

Unit 00 (`sigList`, `SigEq`, `sigEq_iff_sigList`) and Unit 02 (`Knows`,
`knows_iff_determined`, `knows_iff_sigList`).

### 1. Counting distinct signatures

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 519–521
def memB (s : List Nat) : List (List Nat) → Bool
  | [] => false
  | a :: t => if s = a then true else memB s t
```

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 549–551
def dedupL : List (List Nat) → List (List Nat)
  | [] => []
  | s :: t => bif memB s t then dedupL t else s :: dedupL t
```

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 582–585
/-- The number of distinct signatures over `D`: the class count of
`pQ D Q` on `D`. -/
def classCount (D : List Nat) (Q : List (Nat → Nat)) : Nat :=
  (dedupL (D.map (sigList Q))).length
```

`memB s l` says whether the signature `s` occurs in the list `l`. `dedupL`
walks a list of signatures and drops every entry that occurs again later,
so each signature is kept once (its last occurrence). `classCount` maps
every datum of the carrier to its signature, drops the repeats, and counts
what is left. The sealed file writes its own membership test and its own
deduplication so that no library search is involved; both are list
recursions.

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Institution.lean lines 61–63
/-- Information of an institution on `D`: how many signature classes it
cuts `D` into (Genesis `classCount`). -/
def information (D : List Nat) (Q : Institution) : Nat := classCount D Q
```

```python
# Python (research), research/actor_institution/model.py lines 140–142
def information(n: int, Q: Institution) -> int:
    """`Institution.information`: the number of distinct signatures."""
    return len({sig(Q, x) for x in range(n)})
```

```
# Gloss, on the carrier [0, 1, 2] with p1 = (0, 1, 0), p2 = (0, 1, 1), q3 = (0, 0, 1)
family ()         signatures (), (), ()            1 class
family (p1)       signatures 0, 1, 0               2 classes: {0, 2} and {1}
family (p1, p2)   signatures (0,0), (1,1), (0,1)   3 classes
```

### 2. Two sealed facts about counting

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 692–698
/-- The class count never exceeds the domain length. -/
theorem refine_bounded (D : List Nat) (Q : List (Nat → Nat)) :
    classCount D Q ≤ D.length := by
  have h1 := length_dedupL_le (D.map (sigList Q))
  have h2 : (D.map (sigList Q)).length = D.length := by simp
  show (dedupL (D.map (sigList Q))).length ≤ D.length
  omega
```

Dropping repeats never lengthens a list (`length_dedupL_le`), and mapping
keeps the length, so there are at most as many classes as data.

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 599–625
/-- Distinct-value counting is monotone under determination: if the
`G`-value of every point of `D` is determined by its `F`-value, then
`G` takes no more distinct values on `D` than `F`. -/
theorem count_le_of_determines (F G : Nat → List Nat) :
    ∀ D : List Nat,
      (∀ a, a ∈ D → ∀ b, b ∈ D → F a = F b → G a = G b) →
      (dedupL (D.map G)).length ≤ (dedupL (D.map F)).length := by
  intro D
  induction D with
  | nil => intro _; exact Nat.le_refl 0
  | cons d t ih =>
    intro h
    have ht : ∀ a, a ∈ t → ∀ b, b ∈ t → F a = F b → G a = G b :=
      fun a ha b hb =>
        h a (List.mem_cons_of_mem _ ha) b (List.mem_cons_of_mem _ hb)
    have iht := ih ht
    show (dedupL (G d :: t.map G)).length ≤
      (dedupL (F d :: t.map F)).length
    rw [dedupL_cons, dedupL_cons]
    cases hcF : memB (F d) (t.map F) with
    | true =>
      rw [memG_of_memF h hcF]
      exact iht
    | false =>
      cases hcG : memB (G d) (t.map G) with
      | true => exact Nat.le_succ_of_le iht
      | false => exact Nat.succ_le_succ iht
```

Read `F` as the finer labelling and `G` as the coarser one. If equal
`F`-labels force equal `G`-labels, then `G` has no more distinct labels
than `F`. The proof walks the carrier: at each datum `d`, if its `F`-label
occurs again later then so does its `G`-label (`memG_of_memF`, the lemma
just above it in the file), so whenever the fine count does not grow the
coarse count does not grow either; and when the fine count grows by one
the coarse count grows by at most one. Both cases are the induction
hypothesis plus one step of arithmetic.

The third sealed fact is about a family that grows:

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 343–347
/-- The class of `x` splits under the enlargement: some point of `D`
agrees with `x` on the old family but not on the new one. -/
def SplitsAt (D : List Nat) (Q Q' : List (Nat → Nat))
    (x : Nat) : Prop :=
  ∃ x', x' ∈ D ∧ SigEq Q x x' ∧ ¬ SigEq Q' x x'
```

```lean
-- Lean (Genesis), lean4/Derivation/Compression.lean lines 713–718 (statement)
/-- A split under an enlargement strictly increases the class
count. -/
theorem strict_split_increases (D : List Nat)
    (Q Q' : List (Nat → Nat)) (hsub : ∀ q, q ∈ Q → q ∈ Q')
    (x : Nat) (hx : x ∈ D) (hs : SplitsAt D Q Q' x) :
    classCount D Q < classCount D Q'
```

If the larger family `Q'` contains the smaller `Q`, and some class of `Q`
is split by `Q'` (two data the old family merged and the new one tells
apart), then the count goes strictly up. Its proof is a second walk of the
carrier of the same shape as `count_le_of_determines`, tracking the datum
where the split happens; this unit uses the statement.

### 3. The Boolean test, and "know or witness"

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Institution.lean lines 186–190
/-- The Boolean knowledge test, a list computation over the represented
carrier. -/
def knowsB (D : List Nat) (Q : Institution) (q : Nat → Nat) : Bool :=
  D.all (fun x => D.all (fun y =>
    (!(decide (sigList Q x = sigList Q y))) || decide (q x = q y)))
```

For every pair `x`, `y` of the carrier: either their signatures differ, or
`q` agrees on them. That is Unit 02's right-hand side, computed.

```lean
-- Lean (research), the same file, lines 209–236
/-- **Know or witness.**  For every question the institution either knows
it or exhibits two points of `D` it cannot tell apart on which the
question differs.  Decided by `knowsB`; no excluded middle, no choice. -/
theorem know_or_witness (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows D Q q ∨ ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ SigEq Q x y ∧ q x ≠ q y := by
  cases h : knowsB D Q q with
  | true =>
    left
    rw [knows_iff_sigList]
    intro x hx y hy hs
    unfold knowsB at h
    rw [List.all_eq_true] at h
    have h1 := h x hx
    rw [List.all_eq_true] at h1
    have h2 := h1 y hy
    rw [decide_eq_true hs, Bool.not_true, Bool.false_or] at h2
    exact of_decide_eq_true h2
  | false =>
    right
    unfold knowsB at h
    obtain ⟨x, hx, h1⟩ := all_false_witness _ D h
    obtain ⟨y, hy, h2⟩ := all_false_witness _ D h1
    obtain ⟨h3, h4⟩ := Bool.or_eq_false_iff.mp h2
    have h5 : sigList Q x = sigList Q y := by
      cases hd : decide (sigList Q x = sigList Q y) with
      | true => exact of_decide_eq_true hd
      | false => rw [hd] at h3; exact Bool.noConfusion h3
    exact ⟨x, hx, y, hy, (sigEq_iff_sigList Q x y).mpr h5, of_decide_eq_false h4⟩
```

The proof does case analysis on the *value* of `knowsB`, a Boolean the
system computes, not on the truth of `Knows`. If the value is `true`, every
pair passed the test, so `q` agrees wherever the signatures agree. If it is
`false`, some pair failed; `all_false_witness` (lines 194–207, a list
recursion) finds the `x` whose inner test failed, then the `y`, and the
failed test says exactly: signatures equal, `q` values different. So for
every claim the family either knows it or has a concrete pair showing it
does not. This is what lets the unit avoid excluded middle below.

```lean
-- Lean (research), the same file, lines 238–246
theorem not_knows_iff_witness (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    ¬ Knows D Q q ↔ ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ SigEq Q x y ∧ q x ≠ q y := by
  constructor
  · intro hn
    rcases know_or_witness D Q q with h | h
    · exact absurd h hn
    · exact h
  · rintro ⟨x, hx, y, hy, hs, hne⟩ hk
    exact hne ((knows_iff_determined D Q q).mp hk x hx y hy hs)
```

Not knowing is having a witness pair, in both directions.

## The theorems

Four statements, in the order they depend on each other.

```lean
-- Lean (research), the same file, lines 137–139
theorem information_le_carrier (D : List Nat) (Q : Institution) :
    information D Q ≤ D.length :=
  refine_bounded D Q
```

**Bounded.** The information is at most the number of data. It is the
sealed `refine_bounded`, renamed.

```lean
-- Lean (research), the same file, lines 155–161
theorem information_mono {D : List Nat} {Q Q' : Institution}
    (hsub : ∀ q, q ∈ Q → q ∈ Q') : information D Q ≤ information D Q' := by
  unfold information classCount
  apply count_le_of_determines (sigList Q') (sigList Q) D
  intro a ha b hb hab
  exact (sigEq_iff_sigList Q a b).mp
    (enlarge_refines Q Q' hsub a b ((sigEq_iff_sigList Q' a b).mpr hab))
```

**Monotone.** A family that contains another has at least as much
information. It is `count_le_of_determines` with the larger family's
signature as the fine label and the smaller's as the coarse one: equal
signatures on `Q'` give equal signatures on `Q` (`enlarge_refines`,
sealed, line 338: every member of `Q` is a member of `Q'`).

```lean
-- Lean (research), the same file, lines 163–182
theorem sigList_append_eq_of_knows {D : List Nat} {Q : Institution}
    {q : Nat → Nat} (h : Knows D Q q) {a b : Nat} (ha : a ∈ D) (hb : b ∈ D)
    (hab : sigList Q a = sigList Q b) :
    sigList (Q ++ [q]) a = sigList (Q ++ [q]) b := by
  apply (sigEq_iff_sigList _ a b).mp
  intro q' hq'
  rcases List.mem_append.mp hq' with hq' | hq'
  · exact (sigEq_iff_sigList Q a b).mpr hab q' hq'
  · rw [List.mem_singleton.mp hq']
    exact (knows_iff_sigList D Q q).mp h a ha b hb hab

/-- A known question adds no information. -/
theorem information_append_of_knows {D : List Nat} {Q : Institution}
    {q : Nat → Nat} (h : Knows D Q q) :
    information D (Q ++ [q]) = information D Q := by
  apply Nat.le_antisymm
  · unfold information classCount
    exact count_le_of_determines (sigList Q) (sigList (Q ++ [q])) D
      (fun a ha b hb hab => sigList_append_eq_of_knows h ha hb hab)
  · exact information_mono (fun q' hq' => List.mem_append_left _ hq')
```

**A known claim adds nothing.** `Q ++ [q]` is the family with `q` appended.
If `Q` knows `q`, then two data with the same `Q`-signature have the same
`(Q ++ [q])`-signature: on the old members by assumption, on `q` because
`q` is determined by the signature (Unit 02). So the appended family's
count is at most the old one's (`count_le_of_determines`), and at least it
(`information_mono`); two inequalities make an equality
(`Nat.le_antisymm`).

```lean
-- Lean (research), the same file, lines 248–273
/-- Ignorance is exactly a split of some class under adjoining the
question (Genesis `SplitsAt`). -/
theorem not_knows_iff_split (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    ¬ Knows D Q q ↔ ∃ x, x ∈ D ∧ SplitsAt D Q (Q ++ [q]) x := by
  rw [not_knows_iff_witness]
  constructor
  · rintro ⟨x, hx, y, hy, hs, hne⟩
    exact ⟨x, hx, y, hy, hs, fun h' =>
      hne (h' q (List.mem_append_right _ (List.mem_singleton_self q)))⟩
  · rintro ⟨x, hx, y, hy, hs, hnot⟩
    refine ⟨x, hx, y, hy, hs, ?_⟩
    intro heq
    apply hnot
    intro q' hq'
    rcases List.mem_append.mp hq' with hq' | hq'
    · exact hs q' hq'
    · rw [List.mem_singleton.mp hq']
      exact heq

/-- Ignorance is exactly a strict information increase on learning. -/
theorem information_lt_of_not_knows {D : List Nat} {Q : Institution}
    {q : Nat → Nat} (hn : ¬ Knows D Q q) :
    information D Q < information D (Q ++ [q]) := by
  obtain ⟨x, hx, hs⟩ := (not_knows_iff_split D Q q).mp hn
  exact strict_split_increases D Q (Q ++ [q])
    (fun q' hq' => List.mem_append_left _ hq') x hx hs
```

**An unknown claim adds something.** A witness pair (same signature,
different `q`-values) is exactly a class of `Q` that `Q ++ [q]` splits,
and a split strictly raises the count (sealed `strict_split_increases`).

```lean
-- Lean (research), the same file, lines 275–287
/-- **Knowledge is information stationarity.** -/
theorem knows_iff_information_eq (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows D Q q ↔ information D (Q ++ [q]) = information D Q := by
  constructor
  · exact information_append_of_knows
  · intro heq
    rcases know_or_witness D Q q with h | h
    · exact h
    · exfalso
      have hlt := information_lt_of_not_knows
        ((not_knows_iff_witness D Q q).mpr h)
      rw [heq] at hlt
      exact Nat.lt_irrefl _ hlt
```

**The claim.** Knowing is stationarity of the count.

## The proof, step by step

**Step 1. `constructor`.** Two implications.

**Step 2. Left to right: `exact information_append_of_knows`.** If the
family knows `q`, appending `q` leaves the count unchanged. That is the
theorem proved above, and it is used as it stands.

**Step 3. Right to left: `intro heq`.** Assume the count is unchanged,
`heq : information D (Q ++ [q]) = information D Q`. The goal is
`Knows D Q q`.

**Step 4. `rcases know_or_witness D Q q with h | h`.** Either the family
knows `q` or there is a witness pair. This is a case split on a computed
Boolean (section 3), not an appeal to "every proposition is true or
false".

**Step 5. First case: `exact h`.** The family knows `q`. Done.

**Step 6. Second case: `exfalso`.** There is a witness pair `h`. We show
this contradicts `heq`, so the case cannot occur. The goal becomes `False`.

**Step 7. `have hlt := …`.** A witness pair means the family does not know
`q` (`not_knows_iff_witness`, right to left), and not knowing means the
count strictly rises (`information_lt_of_not_knows`):
`hlt : information D Q < information D (Q ++ [q])`.

**Step 8. `rw [heq] at hlt`.** Replace `information D (Q ++ [q])` in `hlt`
by `information D Q`. Now `hlt : information D Q < information D Q`.

**Step 9. `exact Nat.lt_irrefl _ hlt`.** No number is less than itself.
Contradiction; the second case is closed, and with it the theorem.

So: a known claim leaves the count alone (Step 2), an unknown one raises
it (Step 7), and a count cannot both stay and rise (Steps 8 and 9).

### One consequence: known claims are inert

```lean
-- Lean (research), the same file, lines 291–300
/-- Adjoining a known question changes what is known of nothing. -/
theorem known_extension_inert {D : List Nat} {Q : Institution} {q : Nat → Nat}
    (h : Knows D Q q) (q' : Nat → Nat) :
    Knows D (Q ++ [q]) q' ↔ Knows D Q q' := by
  constructor
  · intro h'
    rw [knows_iff_sigList] at h' ⊢
    intro x hx y hy hs
    exact h' x hx y hy (sigList_append_eq_of_knows h hx hy hs)
  · exact knows_mono (fun q'' hq'' => List.mem_append_left _ hq'')
```

Appending a known claim changes nothing about what else is known: the
new family's signature merges exactly the pairs the old one merged
(`sigList_append_eq_of_knows`), and a larger family knows whatever a
smaller one does (`knows_mono`, Unit 02's file, lines 129–133).

## The same fact in Python

`model.information` counts the distinct signatures with a set. The check
takes every carrier `range(n)` with `n ≤ 4`, every family of at most two
partitions, and every partition `q` as the added claim, and tests four
things: the count is at most `n`; the count after appending is at least
the count before; `model.knows` agrees with "the count is unchanged"; and
when `knows` is false the count strictly rises. 1905 (family, claim)
pairs, no violation. The proofs for every carrier and every family are
the Lean above.

```
python textbook/institutions/checks/i03_information.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `List (List Nat)`, `D.map`, `dedupL`, `.length` | the list of signatures and its count | metatheory list operations; each is a recursion over a finite list the system holds |
| `Nat` for `information D Q` | the count | a metatheory number; by `refine_bounded` it never exceeds the length of the carrier, so the system holds nothing larger than what it already had |
| `Q ++ [q]` | "adding a claim to the family" | list append; the family is a list (Unit 00's second admission) |
| `Bool`, `List.all`, `decide`, `!`, `\|\|` | `knowsB` | a finite computation over the carrier |
| `cases h : knowsB D Q q` | know or witness | case analysis on a computed Boolean value, not excluded middle; the tree's axiom report lists `propext` and `Quot.sound` only |
| `Nat.le_antisymm`, `Nat.lt_irrefl`, `Nat.le_succ_of_le`, `Nat.succ_le_succ`, `omega` | arithmetic on counts | metatheory arithmetic on bounded numbers |
| `∀ D`, `∀ q`, `∃ x` | the statements | over the finite carrier and over Lean's function type; `∃ x, x ∈ D ∧ …` is discharged by a list search, never by choice |

**What the system holds.** The carrier, the members' tables, the claim's
table, and one number computed from them. After "learning" `q` it holds
one more table and a possibly larger number, still at most the length of
the carrier. Nothing enters that was not a table already.

**Admissions relied on, and their price.** Unit 00's three, and Unit 02's
definition of knowing. One more, of a word rather than an object: the
trees name `classCount` "information". The number is derived; the name is
a proposal (the `actor_institution` README says so in its vocabulary
table). Its price is that every sentence of the form "the family has more
information" must be read as "the family cuts the carrier into more
classes", and nothing else.

**Phrases to read with care.**

- "Information" is not a quantity carried from anywhere to anywhere and
  belongs to no observer. It is a count of classes on the carrier.
- "Learning `q`", "adjoining `q`": appending `q` to the family's list.
  Nothing happens to anyone; the list is one entry longer. The order of the
  list does not matter to the count: two families with the same members
  have the same information (`information_mono` both ways).
- "Cuts the carrier into classes" names the signature classes of Unit 00.
  There is no space the carrier sits in and no partition held by the
  system apart from the tables; the classes are read off the tables by
  `dedupL`.
- "Ignorance has a witness": the witness is two data of the carrier, found
  by a list search. No one is ignorant; the family's tables do not
  determine `q` on that pair.

## What it shows, and what it does not

It shows that the number is well behaved: bounded by the carrier,
monotone in the family, unchanged by a known claim, strictly raised by an
unknown one. And it shows the last two are a single fact read two ways:
knowing is stationarity.

It shows how to decide knowing without excluded middle: run `knowsB`, and
read either the proof or the witness pair off its value.

It does not show by how much an unknown claim raises the count. The
theorem says strictly, that is by at least one; it can be more. On the
carrier `[0, 1, 2, 3]` the empty family has one class and the claim that
gives each datum its own value has four, so appending it raises the count
by three.

It does not turn the count into a measure of anything beyond the carrier.
`information D Q` is relative to `D`; a different carrier gives a
different number, and the sealed docstring of `classCount` says so.

It does not give determination from a count. Two families with the same
information can know different claims (Unit 08,
`Chain.information_without_determination`). The count says how many
classes there are, not which.

## Sources

| Item | Where |
|---|---|
| `memB`, `dedupL`, `classCount` | `lean4/Derivation/Compression.lean` lines 519–521, 549–551, 582–585 |
| `count_le_of_determines`, `refine_bounded` | `lean4/Derivation/Compression.lean` lines 599–625, 692–698 |
| `SplitsAt`, `strict_split_increases` | `lean4/Derivation/Compression.lean` lines 343–347, 713– |
| `information`, `information_le_carrier`, `information_mono` | `research/two_theorems/lean/ResearchTwoTheorems/Institution.lean` lines 61–63, 137–139, 155–161 |
| `sigList_append_eq_of_knows`, `information_append_of_knows` | the same file, lines 163–182 |
| `knowsB`, `all_false_witness`, `know_or_witness`, `not_knows_iff_witness` | the same file, lines 186–246 |
| `not_knows_iff_split`, `information_lt_of_not_knows`, `knows_iff_information_eq`, `known_extension_inert` | the same file, lines 248–300; axiom reports emitted by the tree's `AxiomReport.lean` and checked by `research/two_theorems/verify.py --check` (`propext`, `Quot.sound`) |
| Python mirror | `research/actor_institution/model.py` lines 140–142 |
| Check | `textbook/institutions/checks/i03_information.py` |
| Ledger | `research/two_theorems/CLAIMS.md` TT-09 (stationarity and strict increase), TT-10 (known claims inert), TT-15 (know or witness); sealed counting in `paper/paper_claim_ledger.md`, `CL-PD2-COMPRESSION` |
