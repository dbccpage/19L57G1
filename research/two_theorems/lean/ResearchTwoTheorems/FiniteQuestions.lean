import ResearchTwoTheorems.Reading

/-!
# Finite tables for questions (2026-10-28, after the second review)

AuthorityEffect: None.  Outside the seal.

`Institution := List (Nat → Nat)` stores total functions on `Nat`.  The
finitude rule admits no infinite object the system has not derived or
priced, so every use the tree makes of a question must be a use of its
finite table over the admitted carrier `D`.  This module makes that
exact.

* `tabulate D q` is the finite table of `q` over `D`: the list of pairs
  `(x, q x)` for `x ∈ D`.  `ofTable t` reads a table back as a function
  (first match; `0` off the table).  `ofTable_tabulate`: on `D` the
  round trip is the identity.
* `encode D Q` tabulates every member of an institution; `decode` reads
  the tables back.  On `D` nothing the tree says can tell the two apart:
  signatures (`sigList_decode_encode`), agreement (`sigEq_decode_encode`),
  the actor (`actor_decode_encode`), knowledge (`knows_decode_encode`,
  `knows_tabulated`) and information (`information_decode_encode`) are
  preserved.
* `tabulate_pQ_mem`: the table of a question's representative `pQ D [q]`
  lies in `D × D`.  With `Reading.knows_iff_knows_pQ`, knowledge of any
  question is knowledge of one of the finitely many tables `D → D`.

So the function type is notation for its table on `D`; off `D` the
function is never consulted, and no claim of the tree reads it there.
-/

namespace ResearchTwoTheorems
namespace FiniteQuestions

open Represented Compression Institution Reading

/-- A finite table: pairs `(point, answer)`. -/
abbrev Table := List (Nat × Nat)

/-- The table of `q` over `D`. -/
def tabulate (D : List Nat) (q : Nat → Nat) : Table :=
  D.map (fun x => (x, q x))

/-- First-match lookup in a table. -/
def find : Table → Nat → Option Nat
  | [], _ => none
  | (k, v) :: t, x => if k = x then some v else find t x

/-- A table read as a function: `0` off the table. -/
def ofTable (t : Table) : Nat → Nat := fun x => (find t x).getD 0

theorem find_tabulate_cons (a : Nat) (t : List Nat) (q : Nat → Nat) (x : Nat) :
    find (tabulate (a :: t) q) x =
      if a = x then some (q a) else find (tabulate t q) x := rfl

/-- On `D`, the round trip through the table is the identity. -/
theorem ofTable_tabulate (D : List Nat) (q : Nat → Nat) {x : Nat}
    (hx : x ∈ D) : ofTable (tabulate D q) x = q x := by
  induction D with
  | nil => cases hx
  | cons a t ih =>
    unfold ofTable
    rw [find_tabulate_cons]
    by_cases hax : a = x
    · subst hax
      rw [if_pos rfl]
      rfl
    · rw [if_neg hax]
      have hxt : x ∈ t := by
        cases hx with
        | head => exact absurd rfl hax
        | tail _ hm => exact hm
      exact ih hxt

/-- The table of a question's representative lies in `D × D`. -/
theorem tabulate_pQ_mem (D : List Nat) (q : Nat → Nat) {e : Nat × Nat}
    (he : e ∈ tabulate D (pQ D [q])) : e.1 ∈ D ∧ e.2 ∈ D := by
  obtain ⟨x, hx, rfl⟩ := List.mem_map.mp he
  exact ⟨hx, pQ_mem D [q] hx⟩

theorem tabulate_length (D : List Nat) (q : Nat → Nat) :
    (tabulate D q).length = D.length := by
  unfold tabulate
  rw [List.length_map]

/-! ## Institutions as lists of tables -/

/-- An institution stored as finite tables. -/
abbrev FinInstitution := List Table

/-- Tabulate every member over `D`. -/
def encode (D : List Nat) (Q : Institution) : FinInstitution :=
  Q.map (tabulate D)

/-- Read every table back as a question. -/
def decode (T : FinInstitution) : Institution := T.map ofTable

theorem decode_encode_length (D : List Nat) (Q : Institution) :
    (decode (encode D Q)).length = Q.length := by
  unfold decode encode
  rw [List.length_map, List.length_map]

/-- On `D`, the decoded institution has the signatures of the original. -/
theorem sigList_decode_encode (D : List Nat) (Q : Institution) {x : Nat}
    (hx : x ∈ D) : sigList (decode (encode D Q)) x = sigList Q x := by
  unfold sigList decode encode
  rw [List.map_map, List.map_map]
  apply List.map_congr_left
  intro q _
  exact ofTable_tabulate D q hx

theorem sigEq_decode_encode (D : List Nat) (Q : Institution) {x y : Nat}
    (hx : x ∈ D) (hy : y ∈ D) :
    SigEq (decode (encode D Q)) x y ↔ SigEq Q x y := by
  rw [sigEq_iff_sigList, sigEq_iff_sigList,
    sigList_decode_encode D Q hx, sigList_decode_encode D Q hy]

/-- `pick` reads its test on `D` only. -/
theorem pick_congr (D : List Nat) (P P' : Nat → Bool)
    (h : ∀ z, z ∈ D → P z = P' z) : pick D P = pick D P' := by
  induction D with
  | nil => rfl
  | cons a t ih =>
    rw [pick_cons, pick_cons, h a List.mem_cons_self,
      ih (fun z hz => h z (List.mem_cons_of_mem _ hz))]

/-- On `D`, the decoded institution has the actor of the original. -/
theorem actor_decode_encode (D : List Nat) (Q : Institution) {x : Nat}
    (hx : x ∈ D) : actor D (decode (encode D Q)) x = actor D Q x := by
  unfold actor pQ
  rw [pick_congr D _ _ (fun z hz => by
    rw [sigList_decode_encode D Q hz, sigList_decode_encode D Q hx])]

/-- Knowledge is preserved by storing the institution as tables. -/
theorem knows_decode_encode (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows D (decode (encode D Q)) q ↔ Knows D Q q := by
  rw [knows_iff_sigList, knows_iff_sigList]
  constructor
  · intro h x hx y hy hs
    exact h x hx y hy (by
      rw [sigList_decode_encode D Q hx, sigList_decode_encode D Q hy]; exact hs)
  · intro h x hx y hy hs
    rw [sigList_decode_encode D Q hx, sigList_decode_encode D Q hy] at hs
    exact h x hx y hy hs

/-- Knowledge of a question is knowledge of its table. -/
theorem knows_tabulated (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows D Q (ofTable (tabulate D q)) ↔ Knows D Q q :=
  knows_congr (fun _ hx => ofTable_tabulate D q hx)

/-- Information is preserved by storing the institution as tables. -/
theorem information_decode_encode (D : List Nat) (Q : Institution) :
    information D (decode (encode D Q)) = information D Q := by
  unfold information classCount
  rw [List.map_congr_left (fun x hx => sigList_decode_encode D Q hx)]

/-- Every statement the tree makes of an institution factors through its
tables on `D`: knowledge, information and the actor agree, in one line. -/
theorem encoding_faithful (D : List Nat) (Q : Institution) :
    (∀ q, Knows D (decode (encode D Q)) q ↔ Knows D Q q) ∧
    information D (decode (encode D Q)) = information D Q ∧
    (∀ x, x ∈ D → actor D (decode (encode D Q)) x = actor D Q x) :=
  ⟨knows_decode_encode D Q, information_decode_encode D Q,
    fun _ hx => actor_decode_encode D Q hx⟩

end FiniteQuestions
end ResearchTwoTheorems
