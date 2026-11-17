import ResearchActorInstitution.Chain

/-!
# B2: a parity square with no global assignment

AuthorityEffect: None.  Outside the seal; consumes `research/two_theorems`
and `research/actor_institution` read-only.

* EXTERNALLY IMPOSED CHALLENGE (R_ctx): a 3 × 3 square of nine entries and
  six contexts, the three rows and the three columns.  Every context asks
  that the sum of its three outcomes has a stated parity `p c`.  The square
  read in the plan has `p` even on every context but the last column.
* ADMITTED AT A PRICE (A_par): an outcome `±1` is presented as a natural
  number read through its parity (`0` for `+1`, `1` for `-1`), so the
  product of three outcomes is `-1` exactly when their sum is odd.  The
  theorems below need no bound on the values; `Bits` records the `{0, 1}`
  reading where a witness is built.
* ADMITTED (Genesis): a finite carrier `D : List Nat` and presentations
  `Nat → Nat` on it.  A context-indexed table gives one presentation per
  context and entry.
* CORRESPONDENCE (actor-institution tree): an entry shared by its row and its column is one
  outcome exactly when its two copies correspond on the carrier,
  `Corr D (T (rowOf i) i) (T (colOf i) i)`, with `Corr` the notion of
  `research/actor_institution` (`Chain.Corr`), used as it stands.

Proved:

* B2(i) `no_global_assignment`: on a nonempty carrier no table meets the
  square's parities with every shared entry corresponding; the proof is the
  parity count (each entry is counted twice, the targets sum to an odd
  number).  `exhaustive_no_assignment` decides the same thing at one point
  by running through all `2⁹` assignments of `{0, 1}` values, and
  `exhaustive_no_global` reads a table through it.
* `global_iff_even`: for every parity target a global table (one
  presentation per entry) meets it on a nonempty carrier exactly when the
  six targets sum to an even number.  The challenge definitions therefore
  give both answers; which one holds is decided by the target, not by the
  definitions.
* B2(ii) `drop_one_context`: for each of the six contexts, a global table
  in `{0, 1}` meets the other five on every carrier.
* B2(iii) `mismatch_at_every_point`, `context_indexed_exists`: every table
  meeting the square on a carrier breaks the correspondence of some shared
  entry at every carrier point, and context-indexed tables in `{0, 1}` that
  meet the square exist on every carrier.  Within tables of presentations
  on one carrier, giving up the correspondence is necessary and enough.

Not proved here: B2(iv), that tables other than the operator realization
meet the challenge in a sense that selects nothing (OPEN); minimality over
any class of squares larger than this one.
-/

namespace ResearchQmBridge
namespace Parity

open ResearchActorInstitution.Chain (Corr)

/-- The nine entries, read row by row: entry `3 r + j` sits in row `r`,
column `j`. -/
abbrev Entry := Fin 9

/-- The six contexts: rows `0, 1, 2`, then columns `3, 4, 5`. -/
abbrev Ctx := Fin 6

/-- The row context of an entry. -/
def rowOf (i : Entry) : Ctx := ⟨i.val / 3, by omega⟩

/-- The column context of an entry. -/
def colOf (i : Entry) : Ctx := ⟨3 + i.val % 3, by omega⟩

/-- The first, second and third entry of a context. -/
def m₁ (c : Ctx) : Entry :=
  if h : c.val < 3 then ⟨3 * c.val, by omega⟩ else ⟨c.val - 3, by omega⟩

def m₂ (c : Ctx) : Entry :=
  if h : c.val < 3 then ⟨3 * c.val + 1, by omega⟩ else ⟨c.val, by omega⟩

def m₃ (c : Ctx) : Entry :=
  if h : c.val < 3 then ⟨3 * c.val + 2, by omega⟩ else ⟨c.val + 3, by omega⟩

/-- The contexts of each entry are its row and its column, and nothing else:
checked over every entry and context. -/
theorem incidence :
    ∀ c : Ctx, ∀ i : Entry, (i = m₁ c ∨ i = m₂ c ∨ i = m₃ c) ↔ (c = rowOf i ∨ c = colOf i) := by
  decide

/-- The square's parity target: even on every context but the last column. -/
def square : Ctx → Nat := fun c => if c.val = 5 then 1 else 0

/-- A context-indexed table: one presentation per context and entry.  Only
the three entries of each context are read. -/
abbrev Table := Ctx → Entry → Nat → Nat

/-- The sum of the three outcomes of context `c` at carrier point `x`. -/
def ctxSum (T : Table) (c : Ctx) (x : Nat) : Nat :=
  T c (m₁ c) x + T c (m₂ c) x + T c (m₃ c) x

/-- CHALLENGE: every context has the target parity at every carrier point. -/
def Meets (D : List Nat) (p : Ctx → Nat) (T : Table) : Prop :=
  ∀ c : Ctx, ∀ x, x ∈ D → ctxSum T c x % 2 = p c % 2

/-- Every shared entry is one outcome: its row copy and its column copy
correspond on the carrier. -/
def Shared (D : List Nat) (T : Table) : Prop :=
  ∀ i : Entry, Corr D (T (rowOf i) i) (T (colOf i) i)

/-- The `{0, 1}` reading of the outcomes that are read. -/
def Bits (D : List Nat) (T : Table) : Prop :=
  ∀ c : Ctx, ∀ x, x ∈ D → T c (m₁ c) x ≤ 1 ∧ T c (m₂ c) x ≤ 1 ∧ T c (m₃ c) x ≤ 1

/-- A global table: one presentation per entry, whatever the context. -/
def globalTable (A : Entry → Nat → Nat) : Table := fun _ i => A i

theorem shared_global (D : List Nat) (A : Entry → Nat → Nat) : Shared D (globalTable A) :=
  fun _ _ _ => rfl

/-- `Shared` says exactly that each entry has one presentation that both of
its context copies correspond to. -/
theorem shared_iff_one_presentation (D : List Nat) (T : Table) :
    Shared D T ↔ ∃ A : Entry → Nat → Nat,
      ∀ i : Entry, Corr D (T (rowOf i) i) (A i) ∧ Corr D (T (colOf i) i) (A i) := by
  constructor
  · intro h
    exact ⟨fun i => T (rowOf i) i, fun i => ⟨fun _ _ => rfl, fun x hx => (h i x hx).symm⟩⟩
  · intro ⟨A, hA⟩ i x hx
    exact ((hA i).1 x hx).trans ((hA i).2 x hx).symm

/-! ## The six constraints and the nine correspondences, written out -/

section Unfold

variable {D : List Nat} {p : Ctx → Nat} {T : Table} {x : Nat}

theorem meets_six (hm : Meets D p T) (hx : x ∈ D) :
    (T 0 0 x + T 0 1 x + T 0 2 x) % 2 = p 0 % 2 ∧
    (T 1 3 x + T 1 4 x + T 1 5 x) % 2 = p 1 % 2 ∧
    (T 2 6 x + T 2 7 x + T 2 8 x) % 2 = p 2 % 2 ∧
    (T 3 0 x + T 3 3 x + T 3 6 x) % 2 = p 3 % 2 ∧
    (T 4 1 x + T 4 4 x + T 4 7 x) % 2 = p 4 % 2 ∧
    (T 5 2 x + T 5 5 x + T 5 8 x) % 2 = p 5 % 2 :=
  ⟨hm 0 x hx, hm 1 x hx, hm 2 x hx, hm 3 x hx, hm 4 x hx, hm 5 x hx⟩

theorem shared_nine (hs : Shared D T) (hx : x ∈ D) :
    T 0 0 x = T 3 0 x ∧ T 0 1 x = T 4 1 x ∧ T 0 2 x = T 5 2 x ∧
    T 1 3 x = T 3 3 x ∧ T 1 4 x = T 4 4 x ∧ T 1 5 x = T 5 5 x ∧
    T 2 6 x = T 3 6 x ∧ T 2 7 x = T 4 7 x ∧ T 2 8 x = T 5 8 x :=
  ⟨hs 0 x hx, hs 1 x hx, hs 2 x hx, hs 3 x hx, hs 4 x hx, hs 5 x hx,
   hs 6 x hx, hs 7 x hx, hs 8 x hx⟩

end Unfold

/-! ## B2(i): no global assignment -/

/-- The parity count: if one carrier point carries all six constraints and
all nine correspondences, the targets sum to an even number. -/
theorem targets_even {D : List Nat} {p : Ctx → Nat} {T : Table} {x : Nat} (hx : x ∈ D)
    (hm : Meets D p T) (hs : Shared D T) :
    (p 0 + p 1 + p 2 + p 3 + p 4 + p 5) % 2 = 0 := by
  obtain ⟨h0, h1, h2, h3, h4, h5⟩ := meets_six hm hx
  obtain ⟨s0, s1, s2, s3, s4, s5, s6, s7, s8⟩ := shared_nine hs hx
  omega

/-- **B2(i).**  On a nonempty carrier no context-indexed table meets the
square with every shared entry corresponding. -/
theorem no_global_assignment {D : List Nat} {x : Nat} (hx : x ∈ D) (T : Table)
    (hm : Meets D square T) : ¬ Shared D T := by
  intro hs
  exact absurd (targets_even hx hm hs) (by decide)

/-- One-point form with `{0, 1}` values, decided over all `2⁹` assignments:
the nine values `a … i` are the square read row by row. -/
theorem exhaustive_no_assignment :
    ∀ a b c d e f g h i : Fin 2,
    ¬ ((a.val + b.val + c.val) % 2 = 0 ∧ (d.val + e.val + f.val) % 2 = 0 ∧
       (g.val + h.val + i.val) % 2 = 0 ∧ (a.val + d.val + g.val) % 2 = 0 ∧
       (b.val + e.val + h.val) % 2 = 0 ∧ (c.val + f.val + i.val) % 2 = 1) := by
  decide

/-- B2(i) again, through the exhaustive check rather than the parity
count: a table in `{0, 1}` meeting the square with every shared entry
corresponding gives one of the `2⁹` assignments that the check rules out. -/
theorem exhaustive_no_global {D : List Nat} {x : Nat} (hx : x ∈ D) (T : Table)
    (hm : Meets D square T) (hb : Bits D T) : ¬ Shared D T := by
  intro hs
  obtain ⟨h0, h1, h2, h3, h4, h5⟩ := meets_six hm hx
  obtain ⟨s0, s1, s2, s3, s4, s5, s6, s7, s8⟩ := shared_nine hs hx
  obtain ⟨b0, b1, b2⟩ := hb 0 x hx
  obtain ⟨b3, b4, b5⟩ := hb 1 x hx
  obtain ⟨b6, b7, b8⟩ := hb 2 x hx
  rw [← s0, ← s3, ← s6] at h3
  rw [← s1, ← s4, ← s7] at h4
  rw [← s2, ← s5, ← s8] at h5
  exact exhaustive_no_assignment ⟨_, Nat.lt_succ_of_le b0⟩ ⟨_, Nat.lt_succ_of_le b1⟩
    ⟨_, Nat.lt_succ_of_le b2⟩ ⟨_, Nat.lt_succ_of_le b3⟩ ⟨_, Nat.lt_succ_of_le b4⟩
    ⟨_, Nat.lt_succ_of_le b5⟩ ⟨_, Nat.lt_succ_of_le b6⟩ ⟨_, Nat.lt_succ_of_le b7⟩
    ⟨_, Nat.lt_succ_of_le b8⟩ ⟨h0, h1, h2, h3, h4, h5⟩

/-! ## The answer is in the target, not in the definitions -/

/-- A global table for any target with an even sum: rows `0, 1` and
columns `0, 1` are set by one entry each, and the corner settles row `2`. -/
def evenWitness (p : Ctx → Nat) : Entry → Nat → Nat := fun i _ =>
  if i.val = 2 then p 0 % 2
  else if i.val = 5 then p 1 % 2
  else if i.val = 6 then p 3 % 2
  else if i.val = 7 then p 4 % 2
  else if i.val = 8 then (p 2 + p 3 + p 4) % 2
  else 0

/-- On a nonempty carrier a global table meets the target `p` exactly when
the six targets sum to an even number.  So the definitions `Meets` and
`Shared` do not contain the answer of B2(i): the odd sum of `square` does. -/
theorem global_iff_even {D : List Nat} {x : Nat} (hx : x ∈ D) (p : Ctx → Nat) :
    (∃ A : Entry → Nat → Nat, Meets D p (globalTable A)) ↔
      (p 0 + p 1 + p 2 + p 3 + p 4 + p 5) % 2 = 0 := by
  constructor
  · intro ⟨A, hA⟩
    exact targets_even hx hA (shared_global D A)
  · intro he
    refine ⟨evenWitness p, ?_⟩
    intro c y _
    match c with
    | ⟨0, _⟩ => show (0 + 0 + p 0 % 2) % 2 = p 0 % 2; omega
    | ⟨1, _⟩ => show (0 + 0 + p 1 % 2) % 2 = p 1 % 2; omega
    | ⟨2, _⟩ => show (p 3 % 2 + p 4 % 2 + (p 2 + p 3 + p 4) % 2) % 2 = p 2 % 2; omega
    | ⟨3, _⟩ => show (0 + 0 + p 3 % 2) % 2 = p 3 % 2; omega
    | ⟨4, _⟩ => show (0 + 0 + p 4 % 2) % 2 = p 4 % 2; omega
    | ⟨5, _⟩ => show (p 0 % 2 + p 1 % 2 + (p 2 + p 3 + p 4) % 2) % 2 = p 5 % 2; omega

/-! ## B2(ii): dropping any one context makes a global assignment exist -/

/-- The square's parities on every context but `k`. -/
def MeetsExcept (D : List Nat) (p : Ctx → Nat) (k : Ctx) (T : Table) : Prop :=
  ∀ c : Ctx, c ≠ k → ∀ x, x ∈ D → ctxSum T c x % 2 = p c % 2

/-- One `{0, 1}` assignment for each dropped context: the last column's
odd parity is carried by an entry of the dropped row, or by the top row
when a column is dropped, or by nothing when the last column is dropped. -/
def dropValue (k : Ctx) (i : Entry) : Nat :=
  if k.val < 3 then (if i.val = 3 * k.val + 2 then 1 else 0)
  else if k.val = 5 then 0
  else (if i.val = 2 ∨ i.val = k.val - 3 then 1 else 0)

/-- The assignments, checked on all six dropped contexts and all five
remaining contexts. -/
theorem dropValue_meets :
    ∀ k c : Ctx, c ≠ k →
      (dropValue k (m₁ c) + dropValue k (m₂ c) + dropValue k (m₃ c)) % 2 = square c % 2 ∧
      dropValue k (m₁ c) ≤ 1 ∧ dropValue k (m₂ c) ≤ 1 ∧ dropValue k (m₃ c) ≤ 1 := by
  decide

/-- **B2(ii).**  For each context `k`, a global table with `{0, 1}` values
meets the square on every other context, on every carrier. -/
theorem drop_one_context (k : Ctx) :
    ∃ A : Entry → Nat → Nat, ∀ D : List Nat,
      MeetsExcept D square k (globalTable A) ∧ Bits D (globalTable A) := by
  refine ⟨fun i _ => dropValue k i, fun D => ⟨?_, ?_⟩⟩
  · intro c hc x _
    exact (dropValue_meets k c hc).1
  · intro c x _
    by_cases hc : c = k
    · subst hc
      have hk : ∀ k : Ctx,
          dropValue k (m₁ k) ≤ 1 ∧ dropValue k (m₂ k) ≤ 1 ∧ dropValue k (m₃ k) ≤ 1 := by
        decide
      exact hk c
    · exact (dropValue_meets k c hc).2

/-! ## B2(iii): the correspondence is what has to go -/

/-- **B2(iii), necessity.**  A table meeting the square on a carrier breaks
the correspondence of some shared entry at every carrier point: outcomes
there are indexed by context, not by entry alone. -/
theorem mismatch_at_every_point {D : List Nat} (T : Table) (hm : Meets D square T) :
    ∀ x, x ∈ D → ∃ i : Entry, T (rowOf i) i x ≠ T (colOf i) i x := by
  intro x hx
  by_cases h : ∃ i : Entry, T (rowOf i) i x ≠ T (colOf i) i x
  · exact h
  · exfalso
    have hall : ∀ i : Entry, T (rowOf i) i x = T (colOf i) i x := by
      intro i
      by_cases e : T (rowOf i) i x = T (colOf i) i x
      · exact e
      · exact absurd ⟨i, e⟩ h
    have hD : x ∈ [x] := List.mem_cons_self
    have hm' : Meets [x] square T := fun c y hy => by
      rw [List.mem_singleton] at hy; subst hy; exact hm c y hx
    have hs : Shared [x] T := fun i y hy => by
      rw [List.mem_singleton] at hy; subst hy; exact hall i
    exact no_global_assignment hD T hm' hs

/-- The context-indexed witness: every outcome is `0` except one entry of
the last column, read in that column only. -/
def contextValue (c : Ctx) (i : Entry) : Nat := if c.val = 5 ∧ i.val = 2 then 1 else 0

theorem contextValue_meets :
    ∀ c : Ctx,
      (contextValue c (m₁ c) + contextValue c (m₂ c) + contextValue c (m₃ c)) % 2 = square c % 2 ∧
      contextValue c (m₁ c) ≤ 1 ∧ contextValue c (m₂ c) ≤ 1 ∧ contextValue c (m₃ c) ≤ 1 := by
  decide

/-- **B2(iii), sufficiency.**  Once the correspondence is given up, a table
with `{0, 1}` outcomes meets the square on every carrier. -/
theorem context_indexed_exists (D : List Nat) :
    ∃ T : Table, Meets D square T ∧ Bits D T :=
  ⟨fun c i _ => contextValue c i,
   fun c _ _ => (contextValue_meets c).1, fun c _ _ => (contextValue_meets c).2⟩

/-- The context-indexed witness breaks exactly one correspondence: entry
`2`, read `0` in its row and `1` in its column. -/
theorem contextValue_breaks_one :
    ∀ i : Entry, (contextValue (rowOf i) i ≠ contextValue (colOf i) i ↔ i.val = 2) := by
  decide

end Parity
end ResearchQmBridge
