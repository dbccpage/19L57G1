import StandingCommitment.Base

/-!
# Demands as a consequence of growth

The sealed estate records, as its first standing obstruction, that no
object-language endogenous demand generator was derived: every challenge
generator it built needed an external ordering, and the local-strategy
class was later excluded outright.  So the machine has a dynamics and no
source of work.

This rung asks a narrower question that the exclusion does not cover.  A
local strategy is a rule that *looks at a state and emits a next demand*.
A STANDING COMMITMENT is not that.  It is a predicate declared once,
saying which pairs must be kept apart *whenever both are admitted*, and it
emits nothing: it is a condition, not a producer.  The question is whether
a state that GROWS under a standing commitment thereby acquires demands
that were not there before, with no act between the growth and the demand.

The answer here is yes, and it is quantitative: with the commitment that
keeps every distinct pair apart, ONE growth step on a state of `n` data
adds exactly `n` demands (`demand_count_grows`).  One declaration at
genesis, unboundedly many demands, and no external act at any step after
the first.

What this does NOT do, stated here so it cannot be mistaken later: the
commitment is a PARAMETER of every theorem below.  Nothing here produces
one.  The estate's standing obstruction concerns where the first
requirement comes from and is untouched; what changes is the accounting,
from one external act per demand to one external act in total.  And the
matching negative is proved: under the empty commitment, growth generates
nothing (`empty_commitment_generates_nothing`), so generation is a
property of the declaration and not of growth.  That is the same shape as
the sealed `no_guard_no_obstruction`: no stake, no obstruction.

AuthorityEffect: None.
-/

namespace StandingCommitment
namespace Standing

/-! ## 1. Pairs of the admitted data -/

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

/-- One growth step adds as many pairs as there were data. -/
theorem pairsOf_length_cons (d : Nat) (rest : List Nat) :
    (pairsOf (d :: rest)).length = rest.length + (pairsOf rest).length := by
  rw [pairsOf_cons, List.length_append, List.length_map]

/-! ## 2. The standing commitment -/

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

/-! ## 3. The demands a state carries under a commitment -/

/-- The demands of a state: pairs of admitted data the commitment keeps
apart that the state does not yet separate.  Read off the state; not
emitted by anything. -/
def demands (C : Commitment) (w : World) : List Req :=
  (pairsOf w.data).filter (fun r => C.holds r.1 r.2 && !satB w r)

/-- Demands depend on the admitted data and the views, and on nothing else
in the represented state.  In particular the fuel, the authorization, the
refusal store and the inert field do not enter. -/
theorem demands_congr (C : Commitment) {w w' : World}
    (hd : w.data = w'.data) (hv : w.views = w'.views) :
    demands C w = demands C w' := by
  have hs : ∀ r : Req, satB w r = satB w' r := by
    intro r; show w.views.any _ = w'.views.any _; rw [hv]
  simp only [demands, hd, hs]

/-! ## 4. Growth -/

/-- Growth: take in one more datum.  Nothing else moves -- no view, no recorded
requirement, no gate, no refusal.  This is the whole of the step. -/
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

/-- **No demand is lost by growing.**  Growth is monotone on the demand
store: it can only add. -/
theorem demands_persist_under_growth (C : Commitment) (w : World) (d : Nat)
    {r : Req} (h : r ∈ demands C w) : r ∈ demands C (grow w d) := by
  rw [demands_grow]
  exact List.mem_append_right _ h

/-! ## 5. Growth generates -/

/-- **The generation theorem.**  If the state grows by a datum it did not
already hold, and the commitment keeps that datum apart from something
already admitted which the state does not separate it from, then the grown
state carries a demand the old state did not.  No act occurs between the
growth and the demand: the demand is a consequence of the growth. -/
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
been met, one growth step under the same commitment reopens the process.
The fixpoint is not absorbing under growth. -/
theorem fixpoint_reopens (C : Commitment) (w : World) (d e : Nat)
    (hquiet : demands C w = []) (hfresh : d ∉ w.data) (hmem : e ∈ w.data)
    (hC : C.holds d e = true) (hsep : satB w (d, e) = false) :
    demands C (grow w d) ≠ [] := by
  intro hnil
  have h := (growth_generates C w d e hfresh hmem hC hsep).1
  rw [hnil] at h
  exact absurd h (by simp)

/-! ## 6. How much is generated -/

/-- Under the total commitment on a state that separates nothing and whose
data are distinct, one growth step adds exactly as many demands as there
were data.  One declaration; a demand store that grows with the square of
the number of growth steps; no external act at any step. -/
theorem demand_count_grows (w : World) (d : Nat)
    (hnoviews : w.views = []) (hfresh : d ∉ w.data) :
    (demands total (grow w d)).length
      = w.data.length + (demands total w).length := by
  have hsat : ∀ r : Req, satB w r = false := by
    intro r; show w.views.any _ = false; rw [hnoviews]; rfl
  have hkeep : ∀ r : Req, r ∈ w.data.map (fun e => (d, e)) →
      ((total.holds r.1 r.2 && !satB w r) = true) := by
    intro r hr
    rcases List.mem_map.mp hr with ⟨e, he, hre⟩
    subst hre
    have hne : d ≠ e := fun h => hfresh (h ▸ he)
    show ((d != e) && !satB w (d, e)) = true
    rw [hsat, bne_iff_ne.mpr hne]; rfl
  rw [demands_grow, List.length_append]
  congr 1
  rw [List.filter_eq_self.mpr hkeep, List.length_map]

/-! ## 7. The matching negative

The estate's own shape: no stake, no obstruction.  Here: no commitment, no
demand, however much the state grows. -/

/-- Under the empty commitment a state carries no demand, whatever its data
and views. -/
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

/-! ## 8. What is still declared

Every theorem above takes the commitment as a parameter.  Nothing here
constructs one, and the two exhibited commitments are written down by hand
in section 2.  The standing obstruction of the sealed estate concerns the
first requirement and is untouched; what this rung changes is the
accounting.  Recorded as a proposition about the statements themselves,
not as a theorem: the type of every result above mentions `Commitment` in
its hypotheses, and no result has `Commitment` in its conclusion. -/

/-- A concrete instance of the accounting claim, decided: from three
admitted data and no views, two growth steps under the total commitment
take the demand store from three to ten, with one declaration and no act
between the steps. -/
theorem accounting_instance :
    (demands total ⟨[1, 2, 3], [], [], [], 0, true, []⟩).length = 3
      ∧ (demands total (grow ⟨[1, 2, 3], [], [], [], 0, true, []⟩ 4)).length = 6
      ∧ (demands total (grow (grow ⟨[1, 2, 3], [], [], [], 0, true, []⟩ 4) 5)).length
          = 10 := by
  decide

end Standing
end StandingCommitment
