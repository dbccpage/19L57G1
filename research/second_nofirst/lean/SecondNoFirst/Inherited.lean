/-!
# The pinned one-sided stake, reconstructed verbatim

PIN NOTE (whole file).  Every declaration below is reproduced VERBATIM
from the sibling tree's Lean sources at the blobs and spans recorded in
`SOURCE_MANIFEST.json`:

* `World`, `genesis`, `sepB`, `satB`, `violB`, `quiescentB` from
  `research/standing_commitment/lean/StandingCommitment/Base.lean`;
* `pairsOf`, `pairsOf_cons`, `pairsOf_mem`, `Commitment`, `total`,
  `empty`, `demands`, `demands_congr`, `grow`, `satB_grow`,
  `demands_grow`, `growth_generates`, `fixpoint_reopens`,
  `filter_of_false`, `empty_commitment_has_no_demand`, and
  `empty_commitment_generates_nothing` from
  `research/standing_commitment/lean/StandingCommitment/Commitment.lean`.

Six of these are pinned individually by SPAN as well as by blob:
`Commitment`, `demands`, `demands_congr`, `growth_generates`,
`fixpoint_reopens`, and `empty_commitment_generates_nothing`.
`verify_pins.py` recomputes each span hash at the snapshot and at HEAD.

The only changes are the outer namespace and the doc comments.  Nothing
of the sibling package is imported: the sibling's prose is not consumed,
only its theorems, and those are consumed by reconstruction under a pin.

HONESTY NOTE.  Reconstruction re-elaborates the pinned proofs here.  The
theorems are the sibling's; the elaboration is this package's.  Where the
prompt asks for a pinned theorem to be "cited, not reproved", that is what
a reconstruction can offer: the statement and the proof are unchanged, and
the ledger records the sibling as their origin.  The rung claims no credit
for any theorem in this file.

AuthorityEffect: None.
-/

namespace SecondNoFirst
namespace Inherited

/-! ## The represented state -/

abbrev View := List Nat

abbrev Req := Nat × Nat

/-- The represented state.  `budget` is the fuel, `augLicensed` the
structure-creation authorization, `refusals` the represented unresolved
obstructions, `notes` a represented but transition-inert commentary
field. -/
structure World where
  data : List Nat
  views : List View
  reqs : List Req
  refusals : List Req
  budget : Nat
  augLicensed : Bool
  notes : List Nat
deriving Repr, DecidableEq

def genesis : World := ⟨[], [], [], [], 0, true, []⟩

def sepB (c : View) (i j : Nat) : Bool :=
  (decide (i ∈ c)) != (decide (j ∈ c))

def satB (w : World) (r : Req) : Bool :=
  w.views.any (fun c => sepB c r.1 r.2)

def violB (w : World) (r : Req) : Bool :=
  (decide (r ∈ w.reqs)) && !satB w r

def quiescentB (w : World) : Bool :=
  w.reqs.all (fun r => satB w r)

/-! ## Pairs of the admitted data -/

/-- The ordered pairs drawn from a list of admitted data, each earlier
element paired with each later one. -/
def pairsOf : List Nat → List Req
  | [] => []
  | d :: rest => rest.map (fun e => (d, e)) ++ pairsOf rest

theorem pairsOf_cons (d : Nat) (rest : List Nat) :
    pairsOf (d :: rest) = rest.map (fun e => (d, e)) ++ pairsOf rest := rfl

/-- Every pair drawn from the data has both members in the data. -/
theorem pairsOf_mem : ∀ {l : List Nat} {r : Req}, r ∈ pairsOf l → r.1 ∈ l ∧ r.2 ∈ l
  | [], r, h => absurd h (by simp [pairsOf])
  | d :: rest, r, h => by
    rw [pairsOf_cons, List.mem_append] at h
    rcases h with hl | hr
    · rcases List.mem_map.mp hl with ⟨e, he, hre⟩
      subst hre
      exact ⟨List.mem_cons_self, List.mem_cons_of_mem d he⟩
    · have := pairsOf_mem hr
      exact ⟨List.mem_cons_of_mem d this.1, List.mem_cons_of_mem d this.2⟩

/-! ## The one-sided standing commitment -/

/-- A STANDING COMMITMENT: a decidable condition on ordered pairs of data,
declared once, saying which pairs must be kept apart whenever both are
admitted.  It emits nothing and reads no state; it is a condition, not a
producer.  A datum is never required apart from itself. -/
structure Commitment where
  holds : Nat → Nat → Bool
  irrefl : ∀ i, holds i i = false

/-- The commitment that keeps every distinct pair apart. -/
def total : Commitment where
  holds i j := i != j
  irrefl i := bne_self_eq_false i

/-- The commitment that requires nothing. -/
def empty : Commitment where
  holds _ _ := false
  irrefl _ := rfl

/-- The demands of a state: pairs of admitted data the commitment keeps
apart that the state does not yet separate.  Read off the state; not
emitted by anything. -/
def demands (C : Commitment) (w : World) : List Req :=
  (pairsOf w.data).filter (fun r => C.holds r.1 r.2 && !satB w r)

/-- Demands depend on the admitted data and the views, and on nothing else
in the represented state. -/
theorem demands_congr (C : Commitment) {w w' : World}
    (hd : w.data = w'.data) (hv : w.views = w'.views) :
    demands C w = demands C w' := by
  have hs : ∀ r : Req, satB w r = satB w' r := by
    intro r; show w.views.any _ = w'.views.any _; rw [hv]
  simp only [demands, hd, hs]

/-! ## Growth -/

/-- Growth: take in one more datum.  Nothing else moves. -/
def grow (w : World) (d : Nat) : World := { w with data := d :: w.data }

/-- Growth does not change what the state separates. -/
theorem satB_grow (w : World) (d : Nat) (r : Req) : satB (grow w d) r = satB w r := rfl

/-- The demands after a growth step: exactly the demands the new datum
brings, followed by the demands that were already there. -/
theorem demands_grow (C : Commitment) (w : World) (d : Nat) :
    demands C (grow w d)
      = (w.data.map (fun e => (d, e))).filter
          (fun r => C.holds r.1 r.2 && !satB w r)
        ++ demands C w := by
  simp only [demands, grow, pairsOf_cons, List.filter_append, satB]

/-- **The generation theorem.**  If the state grows by a datum it did not
already hold, and the commitment keeps that datum apart from something
already admitted which the state does not separate it from, then the grown
state carries a demand the old state did not. -/
theorem growth_generates (C : Commitment) (w : World) (d e : Nat)
    (hfresh : d ∉ w.data) (hmem : e ∈ w.data)
    (hC : C.holds d e = true) (hsep : satB w (d, e) = false) :
    (d, e) ∈ demands C (grow w d) ∧ (d, e) ∉ demands C w := by
  constructor
  · rw [demands_grow]
    refine List.mem_append_left _ ?_
    rw [List.mem_filter]
    refine ⟨List.mem_map.mpr ⟨e, hmem, rfl⟩, ?_⟩
    show (C.holds d e && !satB w (d, e)) = true
    rw [hC, hsep]; rfl
  · intro hbad
    have := (List.mem_filter.mp hbad).1
    exact hfresh (pairsOf_mem this).1

/-- **A discharged state is not a finished state.**  If every demand has
been met, one growth step under the same commitment reopens the process. -/
theorem fixpoint_reopens (C : Commitment) (w : World) (d e : Nat)
    (hquiet : demands C w = []) (hfresh : d ∉ w.data) (hmem : e ∈ w.data)
    (hC : C.holds d e = true) (hsep : satB w (d, e) = false) :
    demands C (grow w d) ≠ [] := by
  intro hnil
  have h := (growth_generates C w d e hfresh hmem hC hsep).1
  rw [hnil] at h
  exact absurd h (by simp)

/-! ## The matching negative -/

theorem filter_of_false {α : Type} (p : α → Bool) (hp : ∀ a, p a = false) :
    ∀ l : List α, l.filter p = []
  | [] => rfl
  | a :: t => by
      rw [List.filter_cons, hp a]
      exact filter_of_false p hp t

theorem empty_commitment_has_no_demand (w : World) : demands empty w = [] :=
  filter_of_false _ (fun _ => rfl) (pairsOf w.data)

/-- **Growth alone generates nothing.**  Under the empty commitment, no
sequence of growth steps produces a demand.  Generation is a property of
the declaration, not of growth. -/
theorem empty_commitment_generates_nothing (w : World) (ds : List Nat) :
    demands empty (ds.foldl grow w) = [] :=
  empty_commitment_has_no_demand _

end Inherited
end SecondNoFirst
