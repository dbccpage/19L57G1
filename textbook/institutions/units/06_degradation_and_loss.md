# Unit 06. Degradation, aggregates, and loss

**Claim.** Known summaries add no new distinctions. Removing a member can lose
distinctions, while a complete representative preserves combined answers
without recording how the family was assembled.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Appending any list of aggregates (presentations the family already
knows) leaves both information and knowledge unchanged; a member is essential
exactly when the remaining members do not know it; an aggregate hides whether
it arose from one fine member or from a family that exceeds its members; losing
a member can turn a separated pair into unanimous agreement while losing
knowledge; and a member that guesses a report beyond its own partition cannot
locate the pair on which it guessed, whereas the family locates it exactly when
another member splits that pair.

**Status:** derived. **Lean:** `Inst.information_congr_mem`,
`Inst.aggregates_inert`, `Inst.aggregates_inert_knows`, `Inst.essential_iff`,
`Inst.duplicate_inert`, `Inst.aggregate_hides_exceeding`,
`Inst.consensus_after_loss` (`actor_institution`); `Reading.Guess`,
`Reading.guess_iff_witness`, `Reading.own_guess_invisible`,
`Reading.guess_visible_iff`, `Reading.shared_guess`, `Reading.guess_witness`
(`two_theorems`). **Sources:**
`research/actor_institution/lean/ResearchActorInstitution/Institution.lean`
lines 250–360;
`research/two_theorems/lean/ResearchTwoTheorems/Reading.lean` lines 476–539.

Unit 03 showed that appending one already-known presentation leaves information
unchanged (`information_append_of_knows`), while appending an unknown one
strictly increases it (`information_lt_of_not_knows`). This unit extends that
single-step fact to arbitrary lists of summaries or digests, characterizes when
removing a member loses information, and exhibits two structural blind spots of
aggregates and member loss: an aggregate erases the provenance of exceeding,
and losing the sole separating member creates unanimity on a merged pair while
destroying knowledge. It then connects this to a member's guess (`Guess D p s`):
a report `s` that `[p]` does not know splits some pair that `p` merges, and no
quantity computed from `p` alone can tell that pair apart, whereas a second
member in the family can.

</details>

## First pass

Return to I04's two members and question [0,0,1]. Both members
together determine it. Repeat the first member's table: the answer
signatures get longer, but their groups stay the same.

Now remove the first member. The remaining table [0,1,1] merges inputs
1 and 2, whose requested answers differ. The family loses that knowledge.

A full representative of the original family can preserve all its
distinctions in one table. That summary does not tell us whether its
groups originally came from one fine table or two coarser tables.
Loss of that history differs from loss of the represented answers.

**Predict:** does every aggregation necessarily lose answer information?

<details><summary>Check your prediction</summary>

No. The full representative preserves the family partition. A coarser
summary may discard distinctions. Appending an already-known summary
adds none; these are different operations with different conclusions.

</details>

## What you need first

Unit 01 (`pQ`), Unit 02 (`Knows`, `knows_iff_determined`, `knows_mono`,
`known_extension_inert`), Unit 03 (`information`, `information_mono`,
`information_append_of_knows`, `information_lt_of_not_knows`,
`not_knows_iff_witness`), and Unit 04 (`Exceeds`, `p1`, `p2`, `q3`). From
`two_theorems` (`Institution.lean` lines 250–252 and `Reading.lean` lines
356–366), `parity` is `x % 2`, `half` is `x / 2`, and `Grounded D Q s` is the
synonym `Knows D Q s` when `s` is read as a report (studied in full in Unit 09).

### 1. Set congruence of information

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Institution.lean lines 250–253
/-- Information depends on the members as a set. -/
theorem information_congr_mem {D : List Nat} {Q Q' : Institution}
    (h : ∀ p, p ∈ Q ↔ p ∈ Q') : information D Q = information D Q' :=
  Nat.le_antisymm (information_mono (fun p hp => (h p).mp hp))
    (information_mono (fun p hp => (h p).mpr hp))
```

Because `information_mono` (Unit 03) uses only list membership `p ∈ Q → p ∈ Q'`,
two families with the same set of members have the same information regardless
of order or multiplicity. In particular, duplicating a member changes nothing
(`duplicate_inert`, lines 326–336: `information D (p :: p :: Q) =
information D (p :: Q)`).

### 2. A member's guess

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Reading.lean lines 476–487
def Guess (D : List Nat) (p s : Nat → Nat) : Prop := ¬ Knows D [p] s

theorem guess_iff_witness (D : List Nat) (p s : Nat → Nat) :
    Guess D p s ↔ ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ p x = p y ∧ s x ≠ s y := by
  unfold Guess
  rw [not_knows_iff_witness]
  constructor
  · rintro ⟨x, hx, y, hy, hs, hne⟩
    exact ⟨x, hx, y, hy, hs p (List.mem_singleton_self p), hne⟩
  · rintro ⟨x, hx, y, hy, hp, hne⟩
    exact ⟨x, hx, y, hy,
      fun r hr => by rw [List.mem_singleton.mp hr]; exact hp, hne⟩
```

A report `s` is a `Guess` by member `p` on `D` when `[p]` does not know `s`,
which by Unit 03's witness theorem means `p` merges some pair `x, y ∈ D` that
`s` splits (`guess_iff_witness`).

## The theorems

First, the inertness of aggregates and the criterion for an essential member:

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Institution.lean lines 258–323
theorem aggregates_inert (D : List Nat) :
    ∀ (M : Institution) (Q : Institution), (∀ m, m ∈ M → Knows D Q m) →
      information D (Q ++ M) = information D Q := by
  intro M
  induction M with
  | nil => intro Q _; rw [List.append_nil]
  | cons m M' ih =>
    intro Q hM
    have hm : Knows D Q m := hM m List.mem_cons_self
    have h1 : information D ((Q ++ [m]) ++ M') = information D (Q ++ [m]) := by
      apply ih
      intro m' hm'
      exact knows_mono (fun p hp => List.mem_append_left _ hp)
        (hM m' (List.mem_cons_of_mem _ hm'))
    rw [List.append_assoc, List.singleton_append] at h1
    rw [h1]
    exact information_append_of_knows hm

theorem aggregates_inert_knows (D : List Nat) (q : Nat → Nat) :
    ∀ (M : Institution) (Q : Institution), (∀ m, m ∈ M → Knows D Q m) →
      (Knows D (Q ++ M) q ↔ Knows D Q q) := by
  intro M
  induction M with
  | nil => intro Q _; rw [List.append_nil]
  | cons m M' ih =>
    intro Q hM
    have hm : Knows D Q m := hM m List.mem_cons_self
    have h1 : Knows D ((Q ++ [m]) ++ M') q ↔ Knows D (Q ++ [m]) q := by
      apply ih
      intro m' hm'
      exact knows_mono (fun p hp => List.mem_append_left _ hp)
        (hM m' (List.mem_cons_of_mem _ hm'))
    rw [List.append_assoc, List.singleton_append] at h1
    rw [h1]
    exact known_extension_inert hm q

theorem essential_iff (D : List Nat) (Q1 Q2 : Institution) (p : Nat → Nat) :
    information D (Q1 ++ Q2) < information D (Q1 ++ p :: Q2) ↔
      ¬ Knows D (Q1 ++ Q2) p := by
  have hmem : ∀ r, r ∈ Q1 ++ p :: Q2 ↔ r ∈ (Q1 ++ Q2) ++ [p] := by
...
  rw [information_congr_mem (D := D) hmem]
  constructor
  · intro hlt hk
    rw [information_append_of_knows hk] at hlt
    exact Nat.lt_irrefl _ hlt
  · intro hn
    exact information_lt_of_not_knows hn
```

Second, provenance loss in the aggregate and false unanimity after member loss:

```lean
-- Lean (research), the same file, lines 343–360
theorem aggregate_hides_exceeding :
    (∀ x, x ∈ [0, 1, 2, 3] →
      pQ [0, 1, 2, 3] [parity, half] x = pQ [0, 1, 2, 3] [fun x => x] x) ∧
    Exceeds [0, 1, 2, 3] [parity, half] (fun x => x) ∧
    ¬ Exceeds [0, 1, 2, 3] [fun x => x] (fun x => x) := by
  unfold Exceeds
  decide

theorem consensus_after_loss :
    ¬ SigEq [p1, p2] 0 2 ∧ SigEq [p1] 0 2 ∧
    Knows [0, 1, 2] [p1, p2] q3 ∧ ¬ Knows [0, 1, 2] [p1] q3 := by
  unfold SigEq
  decide
```

Third, who can locate a member's guess:

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Reading.lean lines 491–539
theorem own_guess_invisible {D : List Nat} {p : Nat → Nat} {x y : Nat}
    (hx : x ∈ D) (hy : y ∈ D) (hp : p x = p y) (e : Nat → Nat)
    (he : Knows D [p] e) : e x = e y :=
  (knows_iff_determined D [p] e).mp he x hx y hy
    (fun r hr => by rw [List.mem_singleton.mp hr]; exact hp)

theorem guess_visible_iff {Q : Institution} {p : Nat → Nat} {x y : Nat}
    (hpxy : p x = p y) :
    ¬ SigEq Q x y ↔ ∃ r, r ∈ Q ∧ r ≠ p ∧ r x ≠ r y := by
  constructor
  · intro h
    obtain ⟨r, hr, hne⟩ := not_sigEq_witness h
    exact ⟨r, hr, fun hrp => hne (by rw [hrp]; exact hpxy), hne⟩
  · rintro ⟨r, hr, _, hne⟩ hs
    exact hne (hs r hr)

theorem shared_guess {D : List Nat} {Q : Institution} {s : Nat → Nat}
    {x y : Nat} (hx : x ∈ D) (hy : y ∈ D) (hs : SigEq Q x y)
    (hne : s x ≠ s y) : ¬ Grounded D Q s :=
  (ungrounded_iff_witness D Q s).mpr ⟨x, hx, y, hy, hs, hne⟩

theorem guess_witness :
    Guess [0, 1, 2, 3] half (fun x => x) ∧
    Grounded [0, 1, 2, 3] [half, parity] (fun x => x) ∧
    ¬ Grounded [0, 1, 2, 3] [half] (fun x => x) := by
  unfold Guess Grounded
  decide
```

## The proof, step by step

**Step 1. `aggregates_inert` and `aggregates_inert_knows` by induction on `M`.**
When `M = []`, `Q ++ [] = Q`. When `M = m :: M'`, the hypothesis gives
`hm : Knows D Q m`, and by `knows_mono` every `m' ∈ M'` is also known by
`Q ++ [m]`. The induction hypothesis collapses `(Q ++ [m]) ++ M'` to `Q ++ [m]`,
and Unit 03's `information_append_of_knows` (or Unit 02's
`known_extension_inert`) collapses `Q ++ [m]` to `Q`.

**Step 2. `essential_iff`.** By `information_congr_mem`, `Q1 ++ p :: Q2` has the
same information as `(Q1 ++ Q2) ++ [p]`. If `Q1 ++ Q2` knows `p`,
`information_append_of_knows` equates the two counts, contradicting `<`. If
`Q1 ++ Q2` does not know `p`, Unit 03's `information_lt_of_not_knows` gives the
strict inequality.

**Step 3. `aggregate_hides_exceeding` and `consensus_after_loss` by `decide`.**
On `[0, 1, 2, 3]`, both `[parity, half]` and `[fun x => x]` separate all four
points, so their canonical representatives `pQ` are identical (`x ↦ x`). Yet
`[parity, half]` exceeds its members on `fun x => x` while the single-member
family `[fun x => x]` does not. On `[0, 1, 2]`, `[p1, p2]` splits `0` and `2`
and knows `q3`; dropping `p2` leaves `[p1]`, which merges `0` and `2` and no
longer knows `q3`.

**Step 4. `own_guess_invisible`, `guess_visible_iff`, and `shared_guess`.**
If `p x = p y`, then `x` and `y` have the same `[p]`-signature, so by
`knows_iff_determined` every presentation `e` known by `[p]` satisfies
`e x = e y`: no self-check derived from `p` can distinguish the pair where `p`
guessed (`own_guess_invisible`). For the family `Q`, `¬ SigEq Q x y` holds iff
some member `r ∈ Q` satisfies `r x ≠ r y` (`not_sigEq_witness`, lines 499–510,
which walks `Q.all`), and since `p x = p y`, any such `r` is distinct from `p`
(`guess_visible_iff`). If instead `SigEq Q x y` holds while `s x ≠ s y`, the
pair `x, y` witnesses `¬ Grounded D Q s` (`shared_guess`).

## The same fact in Python

The check verifies:

1. `aggregates_inert` and `essential_iff` exhaustively on `range(3)` over all
   families of at most 2 partitions and all partitions as the added/removed
   member.
2. `aggregate_hides_exceeding` and `consensus_after_loss` from
   `actor_institution/model.py`.
3. `guess_checks` on `D = (0, 1, 2, 3)` from `two_theorems/model.py`: `half`
   guesses the identity on `(0, 1)`, every presentation known by `[half]`
   agrees on `(0, 1)`, `[half, parity]` splits `(0, 1)` and grounds the
   identity, and `[half]` alone shares the guess.

```
python textbook/institutions/checks/i06_degradation.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| Induction on `M : List (Nat → Nat)` | `aggregates_inert`, `aggregates_inert_knows` | structural induction on the list of aggregates |
| `decide` | `aggregate_hides_exceeding`, `consensus_after_loss`, `guess_witness` | kernel evaluation on `[0, 1, 2, 3]` and `[0, 1, 2]` |
| `Q.all` and `all_false_witness` | `not_sigEq_witness` | constructive list search finding the member that splits `x` and `y` |

**What the system holds.** The finite carrier `D` and the finite list of member
tables. An aggregate is another table `m` satisfying `Knows D Q m`; a member's
guess is a report table `s` satisfying `¬ Knows D [p] s`.

**Admissions relied on, and their price.** Unit 00's three admissions. Because
`pQ D Q` records only which carrier points share a signature and not which
members separated them, collapsing a family into its representative `pQ D Q`
throws away member-level provenance (`AI-05`). And because `SigEq Q x y`
quantifies only over the current list `Q`, shrinking `Q` weakens the separation
condition and can create agreement by omission (`AI-06`).

**Phrases to read with care.**

- "Hierarchies add no distinctions." "Hierarchy" here means appending tables
  `M` each of which is already functionally determined by `Q` (`∀ m ∈ M,
  Knows D Q m`). If a summary layer introduces a new external observation not
  determined by `Q`, the hypothesis `Knows D Q m` does not apply.
- "Consensus after loss." "Consensus" means `SigEq [p1] 0 2`: all remaining
  members give `0` and `2` the same value. Nothing in the data changed; the
  member that told them apart was removed.
- "A guess" and "stepping back." `Guess D p s` means `¬ Knows D [p] s`. No
  psychological act of guessing or reflecting is represented (`TT-36o`).

## What it shows, and what it does not

It shows that summaries, digests, and duplicate members determined by an
existing family add zero information and zero knowledge, and that removing a
member strictly drops information iff the remaining members do not determine
that member.

It shows that the canonical representative `pQ` cannot distinguish a
two-member exceeding family (`[parity, half]`) from a single fine member
(`[id]`), and that dropping an essential member produces unanimity on the pairs
only that member split.

It shows that a member cannot detect on which pair its own report overclaimed
(`own_guess_invisible`), and that the family detects the pair iff another
member splits it (`guess_visible_iff`).

It does not model why a member might emit an ungrounded report `s` or how a
family chooses which members to retain or drop.

## Sources

| Item | Where |
|---|---|
| `information_congr_mem`, `aggregates_inert`, `aggregates_inert_knows`, `essential_iff`, `duplicate_inert` | `research/actor_institution/lean/ResearchActorInstitution/Institution.lean` lines 250–336 |
| `aggregate_hides_exceeding`, `consensus_after_loss` | the same file, lines 343–360 |
| `Guess`, `guess_iff_witness`, `own_guess_invisible`, `not_sigEq_witness`, `guess_visible_iff`, `shared_guess`, `guess_witness` | `research/two_theorems/lean/ResearchTwoTheorems/Reading.lean` lines 476–539 |
| Python mirrors | `research/actor_institution/model.py` lines 460–464; `research/two_theorems/model.py` lines 862–880 (`guess_checks`) |
| Check | `textbook/institutions/checks/i06_degradation.py` |
| Ledger | `research/actor_institution/CLAIMS.md` AI-05, AI-06; `research/two_theorems/CLAIMS.md` TT-33, TT-33c, TT-36o |
