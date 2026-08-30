import Derivation.PrimDiff

/-!
# P3 -- S9.3, proof-relevant witness types: the Lean half (PROMPT.md step 26)

The finite enumeration of `research/s9_obligations/witness_types.py`
computed, over the two-element carrier with the designated pair `(0, 1)`,
a pair of witness assignments that every question of the vocabulary `V1`
answers identically and one question of `V2_ANON` separates, and a pair
that every question of `V1_V2_ANON` answers identically although the two
are not isomorphic as witness families.  This module formalizes both
pairs as concrete finite types, exactly as P3 proposed them in the
receipt key `lean_targets` (`P3_FINDINGS.md`, step 26), and proves the
statements P3 asked for: presence-equal, count-equal, non-isomorphic as
witness families, the separating `V2_ANON` question, and the negative
half -- that no `V1` question separates the first pair, and that no
`V1_V2_ANON` question separates the second -- under an encoding of each
vocabulary as an explicit finite list of decidable questions.

The encoding, as P3 declared it: carrier `Bool` with designated
`(false, true)`; token domain `Fin k`; an assignment is
`W : Bool -> Bool -> Fin k -> Bool`, with `W x y t = true` meaning that
token `t` occurs at the ordered pair `(x, y)`.  The function type is the
metatheory's encoding of a finite table, not an object-language device:
the object language of P3 has no maps, and no question below takes,
returns, or ranges over one.  A2's count is recovered as the cardinality
`card (W x y)` of the store, never admitted a second time (P3 step 21).

The questions are the four kinds of P3's step 22 at carrier size 2:
`presence(p)`, `count_eq(p, q)`, `count_lt(p, q)`, `share(p, q)`, with
`eval` mirroring `witness_types.evaluate` question by question.  The
lists `presenceList` (4), `countList` (6 + 12), and `shareList` (6) were
transcribed from `witness_types.vocabulary` at `(N, T) = (2, 2)` in the
Python order by a one-off rendering script, and the joins `v1List` (22),
`v2AnonList` (10), and `v1V2AnonList` (28) are built as the Python
`vocabulary` builds them.  That the transcription equals the Python
list is checked by no gate: the residual P3 named is still the
residual, narrowed to a mechanical transcription whose lengths are
proved here and whose entries a reader can compare line by line.

Isomorphism of witness families, exactly as P3 declared it: a carrier
bijection fixing the designated points together with a token bijection
transporting the assignment (`WitnessIso`).  The sealed package has
`Function.Injective` and `Function.Surjective` but no `Function.Bijective`,
so the receipt's `Function.Bijective` is spelled as their conjunction
(`Bijective`); the content is the same.

Proof routes, as P3 proposed them: every finite claim goes through
`decide`, with the core instances for `Bool`, `Fin k`, `Nat`, and list
membership; the two non-isomorphism claims do not, because their
quantifiers range over function types, and go instead through a property
transported by every witness isomorphism -- for the separating pair,
that some token is shared by `(0, 1)` and `(1, 0)`, which is the very
`V2_ANON` question that separates it; for the invisible pair, that two
distinct tokens are so shared, which no question of `V1_V2_ANON` can ask.
Both transports are stated for a token domain `Fin k` with `k` a
variable.  Beyond the proposal, `v1ListReadsCounts` proves the "only
when" half of P3's step 25 for the list at carrier size 2: two
assignments with equal count vectors answer every `V1` question
identically, again with `k` a variable.

Names: the eight statements P3 proposed keep the names of the receipt
(`S9_3_sep_*`, `S9_3_inv_*`); every other declaration of this module is
named in lowerCamelCase, so that `P3_FINDINGS.md` can cite it without
colliding with the resolver of `test_witness_types.py`, which reads an
underscored token as a receipt citation.

No carrier-general claim is made here: the lists are those of carrier
size 2, and the theorems with `k` a variable are general in the token
domain only.  Nothing under `lean4/Derivation/` is touched.
AuthorityEffect: None -- this module proposes.
-/

namespace S9Obligations.WitnessTypes

open PrimDiff

/-! ## The encoding -/

/-- A witness assignment over the two-element carrier with token domain
`Fin k`: `W x y t = true` means token `t` occurs at `(x, y)`. -/
abbrev Assignment (k : Nat) : Type := Bool → Bool → Fin k → Bool

/-- The cardinality of a store: A2's count, recovered from the token
layer.  Structural recursion on the token domain, so it reduces inside
`decide`. -/
def card : {k : Nat} → (Fin k → Bool) → Nat
  | 0, _ => 0
  | k + 1, w => (if w 0 = true then 1 else 0) + card (fun i : Fin k => w i.succ)

/-- At `Fin 2` the recursion is the receipt's `card`. -/
theorem cardTwo (w : Fin 2 → Bool) :
    card w = (if w 0 = true then 1 else 0) + (if w 1 = true then 1 else 0) := rfl

/-- A store has positive cardinality exactly when some token occurs in
it: presence is the count being nonzero. -/
theorem cardPosIff : ∀ {k : Nat} (w : Fin k → Bool), 0 < card w ↔ ∃ t, w t = true
  | 0, _ => ⟨fun h => absurd h (Nat.lt_irrefl 0), fun ⟨t, _⟩ => t.elim0⟩
  | k + 1, w => by
    have ih := cardPosIff (fun i : Fin k => w i.succ)
    constructor
    · intro h
      cases hw : w 0 with
      | true => exact ⟨0, hw⟩
      | false =>
        have h' : 0 < card (fun i : Fin k => w i.succ) := by
          simp only [card, hw] at h
          simpa using h
        obtain ⟨i, hi⟩ := ih.mp h'
        exact ⟨i.succ, hi⟩
    · intro ⟨t, ht⟩
      induction t using Fin.cases with
      | zero =>
        simp only [card, ht]
        exact Nat.lt_of_lt_of_le Nat.zero_lt_one (Nat.le_add_right 1 _)
      | succ i =>
        have h' : 0 < card (fun i : Fin k => w i.succ) := ih.mpr ⟨i, ht⟩
        simp only [card]
        exact Nat.lt_of_lt_of_le h' (Nat.le_add_left _ _)

/-- The presence relation an assignment induces -- A1's relation, read
off the token layer; `presence(p)` of `V0` asks it at `p`. -/
def presence {k : Nat} (W : Assignment k) : Bool → Bool → Prop :=
  fun x y => ∃ t, W x y t = true

instance {k : Nat} (W : Assignment k) (x y : Bool) : Decidable (presence W x y) := by
  unfold presence; infer_instance

/-! ## The two pairs, rendered from the receipt -/

/-- The separating pair, left: `S(0,1) = {t0}`, `S(1,0) = {t0}`, masks
`(0, 1, 1, 0)` on S7's two-element irreflexive object at `(2, 2)`
(receipt `cells.N2_T2.spaces.witnessed_irreflexive.separating.V1_vs_V2_ANON.first_pair`). -/
def W1 : Assignment 2 := fun x y t =>
  match x, y, t.val with
  | false, true, 0 => true
  | true, false, 0 => true
  | _, _, _ => false

/-- The separating pair, right: `S(0,1) = {t0}`, `S(1,0) = {t1}`, masks
`(0, 1, 2, 0)`. -/
def W2 : Assignment 2 := fun x y t =>
  match x, y, t.val with
  | false, true, 0 => true
  | true, false, 1 => true
  | _, _, _ => false

/-- The invisible pair, left: `S(0,1) = {t0,t1}`, `S(1,0) = {t0,t1}`,
masks `(0, 3, 3, 0)` on S7's object at `(2, 3)` (receipt
`cells.N2_T3.spaces.witnessed_irreflexive.invisible.V1_V2_ANON.first_non_isomorphic_count_equal_pair`). -/
def W3 : Assignment 3 := fun x y t =>
  match x, y, t.val with
  | false, true, 0 => true
  | false, true, 1 => true
  | true, false, 0 => true
  | true, false, 1 => true
  | _, _, _ => false

/-- The invisible pair, right: `S(0,1) = {t0,t1}`, `S(1,0) = {t0,t2}`,
masks `(0, 3, 5, 0)`. -/
def W4 : Assignment 3 := fun x y t =>
  match x, y, t.val with
  | false, true, 0 => true
  | false, true, 1 => true
  | true, false, 0 => true
  | true, false, 2 => true
  | _, _, _ => false

/-! ## The vocabularies, as explicit finite lists of decidable questions -/

/-- One expressible question at carrier size 2, in the four kinds of P3's
step 22 below the named vocabulary.  Every argument is a carrier point;
no argument is a map. -/
inductive Q where
  | presence (p : Bool × Bool)
  | countEq (p q : Bool × Bool)
  | countLt (p q : Bool × Bool)
  | share (p q : Bool × Bool)
  deriving DecidableEq

/-- The kinds that read only the count vector: everything but `share`. -/
def Q.readsCountsOnly : Q → Bool
  | .share _ _ => false
  | _ => true

/-- Evaluation of a question on an assignment, mirroring
`witness_types.evaluate`: presence is "some token occurs", the count
questions compare cardinalities, and `share` is "some token occurs at
both pairs".  Uses `TOKEN_EQ` only in `share`, through the token
variable `t` occurring twice. -/
def eval {k : Nat} : Q → Assignment k → Bool
  | .presence (x, y), W => decide (∃ t, W x y t = true)
  | .countEq (x, y) (u, v), W => decide (card (W x y) = card (W u v))
  | .countLt (x, y) (u, v), W => decide (card (W x y) < card (W u v))
  | .share (x, y) (u, v), W => decide (∃ t, W x y t = true ∧ W u v t = true)

/-- `V0` at `(2, 2)`: the 4 presence questions, ordered pairs row-major. -/
def presenceList : List Q := [
  .presence (false, false),
  .presence (false, true),
  .presence (true, false),
  .presence (true, true)]

/-- The count questions at `(2, 2)`: `count_eq(p, q)` over the 6
unordered pairs `p < q`, then `count_lt(p, q)` over the 12 ordered pairs
`p != q`, in the Python order. -/
def countList : List Q := [
  .countEq (false, false) (false, true),
  .countEq (false, false) (true, false),
  .countEq (false, false) (true, true),
  .countEq (false, true) (true, false),
  .countEq (false, true) (true, true),
  .countEq (true, false) (true, true),
  .countLt (false, false) (false, true),
  .countLt (false, false) (true, false),
  .countLt (false, false) (true, true),
  .countLt (false, true) (false, false),
  .countLt (false, true) (true, false),
  .countLt (false, true) (true, true),
  .countLt (true, false) (false, false),
  .countLt (true, false) (false, true),
  .countLt (true, false) (true, true),
  .countLt (true, true) (false, false),
  .countLt (true, true) (false, true),
  .countLt (true, true) (true, false)]

/-- The `share(p, q)` questions at `(2, 2)` over the 6 unordered pairs
`p < q`. -/
def shareList : List Q := [
  .share (false, false) (false, true),
  .share (false, false) (true, false),
  .share (false, false) (true, true),
  .share (false, true) (true, false),
  .share (false, true) (true, true),
  .share (true, false) (true, true)]

/-- `V1 = V0 + count_eq + count_lt`, 22 questions. -/
def v1List : List Q := presenceList ++ countList

/-- `V2_ANON = V0 + share`, 10 questions. -/
def v2AnonList : List Q := presenceList ++ shareList

/-- `V1_V2_ANON = V0 + count_eq + count_lt + share`, 28 questions. -/
def v1V2AnonList : List Q := presenceList ++ countList ++ shareList

/-- The receipt's `sizes_by_cell.N2_T2.V1`. -/
theorem v1ListLength : v1List.length = 22 := rfl

/-- The receipt's `sizes_by_cell.N2_T2.V2_ANON`. -/
theorem v2AnonListLength : v2AnonList.length = 10 := rfl

/-- The receipt's `sizes_by_cell.N2_T2.V1_V2_ANON`. -/
theorem v1V2AnonListLength : v1V2AnonList.length = 28 := rfl

/-- No question is listed twice in the largest list. -/
theorem v1V2AnonListNodup : v1V2AnonList.Nodup := by decide

/-- No question is listed twice in the `V1` list. -/
theorem v1ListNodup : v1List.Nodup := by decide

/-- No question is listed twice in the `V2_ANON` list. -/
theorem v2AnonListNodup : v2AnonList.Nodup := by decide

/-- Every `V1` question reads only the count vector. -/
theorem v1ListReadsCountsOnly : ∀ q ∈ v1List, q.readsCountsOnly = true := by decide

/-! ## Isomorphism of witness families -/

/-- Bijectivity, spelled as injective and surjective: the sealed package
carries `Function.Injective` and `Function.Surjective` and no
`Function.Bijective`. -/
abbrev Bijective {α β : Type} (f : α → β) : Prop :=
  Function.Injective f ∧ Function.Surjective f

/-- Isomorphism of witness families, exactly as P3 declared it: a carrier
bijection `s` fixing the designated points and a token bijection `r`
with `W x y t = W' (s x) (s y) (r t)`.  Metatheoretic apparatus, in no
vocabulary: it quantifies over maps. -/
def WitnessIso {k : Nat} (W W' : Assignment k) : Prop :=
  ∃ (s : Bool → Bool) (r : Fin k → Fin k),
    s false = false ∧ s true = true ∧ Bijective s ∧ Bijective r ∧
    ∀ x y t, W x y t = W' (s x) (s y) (r t)

/-- Token `t` occurs at both `(0, 1)` and `(1, 0)`. -/
def Shared {k : Nat} (W : Assignment k) (t : Fin k) : Prop :=
  W false true t = true ∧ W true false t = true

/-- Some token is shared by `(0, 1)` and `(1, 0)`: the question
`share((0,1),(1,0))` of `V2_ANON`. -/
def SomeShared {k : Nat} (W : Assignment k) : Prop := ∃ t, Shared W t

/-- Two distinct tokens are shared by `(0, 1)` and `(1, 0)`: a "how many"
that no question of `V1_V2_ANON` asks. -/
def TwoShared {k : Nat} (W : Assignment k) : Prop :=
  ∃ t u, t ≠ u ∧ Shared W t ∧ Shared W u

instance {k : Nat} (W : Assignment k) (t : Fin k) : Decidable (Shared W t) := by
  unfold Shared; infer_instance

instance {k : Nat} (W : Assignment k) : Decidable (SomeShared W) := by
  unfold SomeShared; infer_instance

instance {k : Nat} (W : Assignment k) : Decidable (TwoShared W) := by
  unfold TwoShared; infer_instance

/-- The number of shared tokens, the receipt's `common_token_count` at
carrier size 2 (the `((0,1),(1,0))` entry of its `intersection_profile`,
read the same way). -/
def sharedCount {k : Nat} (W : Assignment k) : Nat :=
  card (fun t => W false true t && W true false t)

/-- The transport equation of a point-fixing carrier map carries a shared
token `t` to the shared token `r t`: at `(false, true)` and
`(true, false)` the equation reads off `Shared` directly. -/
theorem sharedTransport {k : Nat} {W W' : Assignment k} {s : Bool → Bool}
    {r : Fin k → Fin k} (hf : s false = false) (ht : s true = true)
    (he : ∀ x y t, W x y t = W' (s x) (s y) (r t)) {t : Fin k} (hs : Shared W t) :
    Shared W' (r t) := by
  obtain ⟨h1, h2⟩ := hs
  constructor
  · have e := he false true t
    rw [hf, ht] at e
    exact e.symm.trans h1
  · have e := he true false t
    rw [hf, ht] at e
    exact e.symm.trans h2

/-- `SomeShared` is transported by every witness isomorphism; neither
bijectivity is used. -/
theorem someSharedTransport {k : Nat} {W W' : Assignment k} (h : WitnessIso W W')
    (hs : SomeShared W) : SomeShared W' := by
  obtain ⟨s, r, hf, ht, _, _, he⟩ := h
  obtain ⟨t, hs⟩ := hs
  exact ⟨r t, sharedTransport hf ht he hs⟩

/-- `TwoShared` is transported by every witness isomorphism: the token
map is injective, so two distinct shared tokens stay distinct. -/
theorem twoSharedTransport {k : Nat} {W W' : Assignment k} (h : WitnessIso W W')
    (hs : TwoShared W) : TwoShared W' := by
  obtain ⟨s, r, hf, ht, _, hbr, he⟩ := h
  obtain ⟨t, u, htu, hst, hsu⟩ := hs
  exact ⟨r t, r u, fun e => htu (hbr.1 e),
    sharedTransport hf ht he hst, sharedTransport hf ht he hsu⟩

/-! ## Step 26 for the separating pair (receipt cell `N2_T2`, space `witnessed_irreflexive`) -/

/-- Presence-equal: the same pairs carry a nonempty store. -/
theorem S9_3_sep_presence_equal :
    ∀ x y : Bool, (∃ t : Fin 2, W1 x y t = true) ↔ (∃ t : Fin 2, W2 x y t = true) := by
  decide

/-- Count-equal: A2's count, recovered as cardinality, agrees at every
pair. -/
theorem S9_3_sep_count_equal : ∀ x y : Bool, card (W1 x y) = card (W2 x y) := by
  decide

/-- The negative half: no question of `V1`, as the explicit list
`v1List`, separates the pair (receipt
`coarse_differing_question_count = 0`). -/
theorem S9_3_sep_V1_indistinguishable : ∀ q ∈ v1List, eval q W1 = eval q W2 := by
  decide

/-- The one `V2_ANON` question that separates the pair,
`share((0,1),(1,0))`, in its own terms: `W1` shares a token across the
designated pair and its reverse, `W2` does not. -/
theorem S9_3_sep_V2_ANON_separates :
    (∃ t : Fin 2, W1 false true t = true ∧ W1 true false t = true) ∧
    ¬ (∃ t : Fin 2, W2 false true t = true ∧ W2 true false t = true) := by
  decide

/-- The same, read off the list: exactly one question of `v2AnonList`
answers differently on the pair, and it is `share((0,1),(1,0))` (receipt
`fine_differing_question_count = 1`, `first_fine_differing_question`). -/
theorem sepExactlyOneV2AnonQuestionDiffers :
    v2AnonList.filter (fun q => eval q W1 != eval q W2) =
      [.share (false, true) (true, false)] := by
  decide

/-- Non-isomorphic as witness families: `SomeShared` is transported by
every witness isomorphism, holds of `W1`, and fails of `W2`.  The
separating `V2_ANON` question is itself the invariant. -/
theorem S9_3_sep_not_isomorphic : ¬ WitnessIso W1 W2 :=
  fun h => S9_3_sep_V2_ANON_separates.2 (someSharedTransport h S9_3_sep_V2_ANON_separates.1)

/-- The pair is unequal as raw data (it differs at `(1, 0)`, token `t1`). -/
theorem sepRawDataDiffer : W1 ≠ W2 :=
  fun h => absurd (congrFun (congrFun (congrFun h true) false) 1) (by decide)

/-- Both assignments induce the sealed `S2`: the pair lives on S7's
symmetric two-element object, as the receipt's space
`witnessed_irreflexive` at `N = 2` requires. -/
theorem sepPresenceS2 :
    (∀ x y, presence W1 x y ↔ S2 x y) ∧ (∀ x y, presence W2 x y ↔ S2 x y) := by
  decide

/-- Hence both induced relations are irreflexive, by the sealed
`S2_irrefl`; the pair is inside S7's object class. -/
theorem sepPresenceIrrefl : Irrefl (presence W1) ∧ Irrefl (presence W2) :=
  ⟨fun x h => S2_irrefl x ((sepPresenceS2.1 x x).mp h),
   fun x h => S2_irrefl x ((sepPresenceS2.2 x x).mp h)⟩

/-! ## Step 26 for the invisible pair (receipt cell `N2_T3`, space `witnessed_irreflexive`) -/

/-- The negative half: no question of `V1_V2_ANON`, as the explicit list
`v1V2AnonList`, separates the pair. -/
theorem S9_3_inv_V1_V2_ANON_indistinguishable :
    ∀ q ∈ v1V2AnonList, eval q W3 = eval q W4 := by
  decide

/-- Count-equal: what the pair hides is token-level, not a count. -/
theorem S9_3_inv_count_equal : ∀ x y : Bool, card (W3 x y) = card (W4 x y) := by
  decide

/-- The invariant that differs, as the receipt records it
(`first_non_isomorphic_count_equal_pair_characterization`:
`common_token_count` 2 against 1). -/
theorem invSharedCounts : sharedCount W3 = 2 ∧ sharedCount W4 = 1 := by
  decide

/-- The same invariant in the form the transport lemma carries: `W3` has
two distinct shared tokens, `W4` does not. -/
theorem invTwoShared : TwoShared W3 ∧ ¬ TwoShared W4 := by
  decide

/-- Non-isomorphic as witness families: `TwoShared` is transported by
every witness isomorphism, holds of `W3`, and fails of `W4`. -/
theorem S9_3_inv_not_isomorphic : ¬ WitnessIso W3 W4 :=
  fun h => invTwoShared.2 (twoSharedTransport h invTwoShared.1)

/-- The pair is unequal as raw data (it differs at `(1, 0)`, token `t1`). -/
theorem invRawDataDiffer : W3 ≠ W4 :=
  fun h => absurd (congrFun (congrFun (congrFun h true) false) 1) (by decide)

/-- Both assignments induce the sealed `S2` as well: the invisible pair
also lives on S7's object. -/
theorem invPresenceS2 :
    (∀ x y, presence W3 x y ↔ S2 x y) ∧ (∀ x y, presence W4 x y ↔ S2 x y) := by
  decide

/-- Hence both induced relations are irreflexive, by the sealed
`S2_irrefl`. -/
theorem invPresenceIrrefl : Irrefl (presence W3) ∧ Irrefl (presence W4) :=
  ⟨fun x h => S2_irrefl x ((invPresenceS2.1 x x).mp h),
   fun x h => S2_irrefl x ((invPresenceS2.2 x x).mp h)⟩

/-! ## Beyond the proposal: `V1` reads only the count vector -/

/-- A question that reads only counts answers identically on two
assignments with equal count vectors, for a token domain `Fin k` with
`k` a variable. -/
theorem evalReadsCounts {k : Nat} (W W' : Assignment k)
    (hc : ∀ x y, card (W x y) = card (W' x y)) :
    ∀ q : Q, q.readsCountsOnly = true → eval q W = eval q W'
  | .presence (x, y), _ => by
    simp only [eval]
    apply decide_eq_decide.mpr
    rw [← cardPosIff (W x y), ← cardPosIff (W' x y), hc]
  | .countEq (x, y) (u, v), _ => by
    simp only [eval, hc]
  | .countLt (x, y) (u, v), _ => by
    simp only [eval, hc]
  | .share _ _, h => Bool.noConfusion h

/-- The "only when" half of P3's step 25 for the list at carrier size 2:
two assignments with equal count vectors answer every `V1` question
identically, whatever the token domain size `k`.  No `V1` question can
separate a count-equal pair, so what `share((0,1),(1,0))` sees of `W1`
against `W2` is not expressible without `TOKEN_EQ` in these
vocabularies. -/
theorem v1ListReadsCounts {k : Nat} (W W' : Assignment k)
    (hc : ∀ x y, card (W x y) = card (W' x y)) :
    ∀ q ∈ v1List, eval q W = eval q W' :=
  fun q hq => evalReadsCounts W W' hc q (v1ListReadsCountsOnly q hq)

/-- The separating pair's negative half, re-derived from count-equality
alone through `v1ListReadsCounts`, in agreement with the `decide` proof. -/
theorem sepV1IndistinguishableViaCounts : ∀ q ∈ v1List, eval q W1 = eval q W2 :=
  v1ListReadsCounts W1 W2 S9_3_sep_count_equal

end S9Obligations.WitnessTypes
