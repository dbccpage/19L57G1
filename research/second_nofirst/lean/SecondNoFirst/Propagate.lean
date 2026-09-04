import SecondNoFirst.NoFirst

/-!
# Stage three: demands propagate from a declaration

With a stake declared, growth generates.  The one-sided form is the pinned
theorem, reconstructed unchanged in `Inherited.lean` and re-exported here
under its own name so the register can cite it; the two-sided forms over
the sealed regime are proved here, in both label directions.

The last two theorems of this file are the ones the sibling two-sided tree
records as a CONJECTURE with no Lean.  They are proved here over the
sealed regime, under hypotheses stated in full: the stake that labels
every distinct pair apart, and a well-formed regime that carries no
demand.  A proof over the sealed regime is not a proof of the sibling's
statement over its own carrier; the sibling's row stands as the sibling
wrote it, and this rung's row says which carrier it is about.

AuthorityEffect: None.
-/

namespace SecondNoFirst
namespace Propagate

open SecondNoFirst.Sealed
open SecondNoFirst.Stake
open SecondNoFirst.NoFirst

/-! ## 1. The pinned one-sided theorem, re-exported -/

/-- **growth_generates_pinned.**  The pinned one-sided generation theorem,
re-exported under this rung's name with its hypotheses unchanged.  Its
statement and its proof are the sibling's, reconstructed under the span
pin recorded in `SOURCE_MANIFEST.json`; this rung claims no credit for it
and states nothing new here. -/
theorem growth_generates_pinned (C : Inherited.Commitment) (w : Inherited.World)
    (d e : Nat) (hfresh : d ∉ w.data) (hmem : e ∈ w.data)
    (hC : C.holds d e = true) (hsep : Inherited.satB w (d, e) = false) :
    (d, e) ∈ Inherited.demands C (Inherited.grow w d) ∧
      (d, e) ∉ Inherited.demands C w :=
  Inherited.growth_generates C w d e hfresh hmem hC hsep

/-! ## 2. Growth over the sealed regime -/

/-- Growth over the sealed regime: the datum admission of the sealed
grammar.  The fresh datum's index is the old data count. -/
def growR (r : Regime) : Regime := { r with data := r.data + 1 }

/-- Growth is exactly what the sealed datum admission does. -/
theorem stepE_admitDatum (r : Regime) : stepE r .admitDatum = some (growR r) := rfl

/-- Growth admits no form, no instance and no rule. -/
theorem growR_forms (r : Regime) : (growR r).forms = r.forms := rfl

theorem growR_insts (r : Regime) : (growR r).insts = r.insts := rfl

theorem growR_rules (r : Regime) : (growR r).rules = r.rules := rfl

theorem growR_data (r : Regime) : (growR r).data = r.data + 1 := rfl

/-- Derivability does not move under growth: the instances and the rules
are the same collections. -/
theorem derivable_growR (r : Regime) (i : Inst) :
    derivable (growR r) i ↔ derivable r i := Iff.rfl

/-- A context well formed before a growth step is well formed after it:
the forms are unchanged and the data only grow. -/
theorem wfCtx_growR (r : Regime) (c : Ctx) (h : wfCtx r c) : wfCtx (growR r) c := by
  refine ⟨h.1, h.2.1, h.2.2.1, ?_⟩
  intro s hs
  have := h.2.2.2 s hs
  cases s with
  | none => exact trivial
  | some x => exact Nat.lt_succ_of_lt this

/-- Collapse survives the restriction from the grown regime to the old
one: every context of the old regime is a context of the grown one, and
derivability agrees. -/
theorem collapsed_of_growR (r : Regime) (d d' : Nat)
    (h : collapsed (growR r) d d') : collapsed r d d' :=
  fun c hw => h c (wfCtx_growR r c hw)

/-! ## 3. Growth generates, two-sided, over the sealed regime -/

/-- **growth_generates_apart.**  In the sealed grammar reconstructed here,
extended by a declared two-sided stake: a fresh datum admitted into a
regime, labelled apart from a held datum with which the grown regime
collapses it, is a demand of the grown regime and was not a demand
before.  The negative half is at the level of a definition -- the fresh
index is not a held index before the growth -- and the positive half is
the content. -/
theorem growth_generates_apart (S : Stake) (r : Regime) (e : Nat)
    (hmem : e < r.data) (hlab : S.label e r.data = Label.apart)
    (hcol : collapsed (growR r) e r.data) :
    Demand S (growR r) e r.data ∧ ¬ Demand S r e r.data := by
  constructor
  · refine ⟨hmem, by rw [growR_data]; exact Nat.lt_succ_self _,
      by rw [hlab]; rfl, ?_⟩
    rw [hlab]
    exact collapsed_not_separable hcol
  · intro h
    exact absurd h.2.1 (Nat.lt_irrefl _)

/-- **growth_generates_apart_of_no_insts.**  The same, with the collapse
hypothesis discharged rather than assumed: at a regime with no admitted
instance the grown regime has none either, so every pair of it is
collapsed. -/
theorem growth_generates_apart_of_no_insts (S : Stake) (r : Regime)
    (hi : r.insts = []) (e : Nat) (hmem : e < r.data)
    (hlab : S.label e r.data = Label.apart) :
    Demand S (growR r) e r.data ∧ ¬ Demand S r e r.data :=
  growth_generates_apart S r e hmem hlab
    (collapsed_of_no_insts (growR r) (by rw [growR_insts]; exact hi) e r.data)

/-- **growth_generates_same.**  In the sealed grammar reconstructed here,
extended by a declared two-sided stake: a fresh datum labelled same as a
held datum from which the grown regime separates it is a demand of the
grown regime and was not a demand before. -/
theorem growth_generates_same (S : Stake) (r : Regime) (e : Nat)
    (hmem : e < r.data) (hlab : S.label e r.data = Label.same)
    (hsep : separable (growR r) e r.data) :
    Demand S (growR r) e r.data ∧ ¬ Demand S r e r.data := by
  constructor
  · refine ⟨hmem, by rw [growR_data]; exact Nat.lt_succ_self _,
      by rw [hlab]; rfl, ?_⟩
    rw [hlab]
    exact separable_not_collapsed hsep
  · intro h
    exact absurd h.2.1 (Nat.lt_irrefl _)

/-! ## 4. The profile of the fresh datum -/

/-- A well-formed context has a hole, so plugging it names the plugged
datum among the arguments. -/
theorem mem_plug_of_hole (c : Ctx) (d : Nat) (h : none ∈ c.slots) :
    d ∈ (plug c d).2 := by
  unfold plug
  exact List.mem_map.mpr ⟨none, h, rfl⟩

/-- **fresh_profile.**  At a well-formed regime, a well-formed context of
the grown regime derives the datum admitted by one growth step exactly
when the context's form carries a uniform rule.  No admitted instance can
name it: every admitted instance of a well-formed regime names only data
admitted before the growth, and a well-formed context has a hole, so
plugging the fresh datum names an index no admitted instance carries. -/
theorem fresh_profile (r : Regime) (hwf : r.wf) (c : Ctx)
    (hc : wfCtx (growR r) c) :
    derivable (growR r) (plug c r.data) ↔ c.form ∈ r.rules := by
  constructor
  · intro h
    cases h with
    | inr h => exact h
    | inl h =>
        rw [growR_insts] at h
        have hbound := (hwf.1 _ h).2.2 r.data (mem_plug_of_hole c r.data hc.2.2.1)
        exact absurd hbound (Nat.lt_irrefl _)
  · intro h; exact Or.inr h

/-- Two data both of empty profile are collapsed: no well-formed context
derives either, so every well-formed context gives the same answer. -/
theorem collapsed_of_both_empty (r : Regime) (d d' : Nat)
    (hd : ∀ c : Ctx, wfCtx r c → ¬ derivable r (plug c d))
    (hd' : ∀ c : Ctx, wfCtx r c → ¬ derivable r (plug c d')) :
    collapsed r d d' := by
  intro c hw
  constructor
  · intro h; exact absurd h (hd c hw)
  · intro h; exact absurd h (hd' c hw)

/-! ## 5. At most one, over the sealed regime

The sibling two-sided tree records the corresponding statement as a
CONJECTURE with no Lean.  What follows is a proof over the SEALED REGIME,
which is a different carrier from the sibling's; the sibling's row is not
edited, and this rung's row says which carrier its proof is about. -/

/-- **apart_at_most_one.**  In the sealed grammar reconstructed here,
extended by the declared two-sided stake that labels every distinct pair
apart: a regime carrying no demand separates every pair of held data, so
at most one held datum has the empty profile -- two would be collapsed,
and a collapsed pair under this stake is a demand. -/
theorem apart_at_most_one (r : Regime)
    (hq : ∀ i j, i < j → j < r.data → ¬ Demand allApart r i j)
    (i j : Nat) (hij : i < j) (hj : j < r.data)
    (hi : ∀ c : Ctx, wfCtx r c → ¬ derivable r (plug c i))
    (hj' : ∀ c : Ctx, wfCtx r c → ¬ derivable r (plug c j)) : False := by
  refine hq i j hij hj ⟨hij, hj, ?_, ?_⟩
  · show (if i = j then Label.free else Label.apart).labelled = true
    rw [if_neg (Nat.ne_of_lt hij)]; rfl
  · show ¬ honour r (if i = j then Label.free else Label.apart) i j
    rw [if_neg (Nat.ne_of_lt hij)]
    exact collapsed_not_separable (collapsed_of_both_empty r i j hi hj')

/-- The label the all-apart stake gives a distinct pair. -/
theorem allApart_label {i j : Nat} (h : i ≠ j) :
    allApart.label i j = Label.apart := by
  show (if i = j then Label.free else Label.apart) = Label.apart
  rw [if_neg h]

/-- Under the all-apart stake, a demand at a held pair is exactly a
collapsed held pair. -/
theorem allApart_demand_iff (r : Regime) (i j : Nat) (hij : i < j)
    (hj : j < r.data) : Demand allApart r i j ↔ collapsed r i j := by
  constructor
  · intro h
    have := h.2.2.2
    rw [allApart_label (Nat.ne_of_lt hij)] at this
    exact collapsed_of_not_separable this
  · intro h
    refine ⟨hij, hj, ?_, ?_⟩
    · rw [allApart_label (Nat.ne_of_lt hij)]; rfl
    · rw [allApart_label (Nat.ne_of_lt hij)]
      exact collapsed_not_separable h

/-- Collapse is transitive through a shared partner. -/
theorem collapsed_trans (r : Regime) (a b c : Nat)
    (hab : collapsed r a c) (hbc : collapsed r b c) : collapsed r a b :=
  fun x hw => (hab x hw).trans (hbc x hw).symm

/-- **apart_at_most_one_new_demand.**  In the sealed grammar reconstructed
here, extended by the declared two-sided stake that labels every distinct
pair apart: from a well-formed regime carrying no demand, one growth step
generates at most one demand.  Two held data both collapsed with the fresh
datum would be collapsed with each other in the grown regime, hence in the
base regime, hence a demand of the base regime -- which carries none. -/
theorem apart_at_most_one_new_demand (r : Regime)
    (hq : ∀ i j, i < j → j < r.data → ¬ Demand allApart r i j)
    (e e' : Nat) (he : e < r.data) (he' : e' < r.data) (hne : e ≠ e')
    (hd : Demand allApart (growR r) e r.data)
    (hd' : Demand allApart (growR r) e' r.data) : False := by
  have hce : collapsed (growR r) e r.data :=
    (allApart_demand_iff (growR r) e r.data he
      (by rw [growR_data]; exact Nat.lt_succ_self _)).mp hd
  have hce' : collapsed (growR r) e' r.data :=
    (allApart_demand_iff (growR r) e' r.data he'
      (by rw [growR_data]; exact Nat.lt_succ_self _)).mp hd'
  have hbase : collapsed r e e' :=
    collapsed_of_growR r e e' (collapsed_trans (growR r) e e' r.data hce hce')
  rcases Nat.lt_or_ge e e' with hlt | hge
  · exact hq e e' hlt he' ((allApart_demand_iff r e e' hlt he').mpr hbase)
  · have hlt' : e' < e := Nat.lt_of_le_of_ne hge (fun h => hne h.symm)
    exact hq e' e hlt' he
      ((allApart_demand_iff r e' e hlt' he).mpr
        (fun x hw => (hbase x hw).symm))

/-- **apart_no_old_demand.**  Under the stake labelling every distinct pair
apart: at a regime carrying no demand, one growth step creates no demand at
a pair of data held BEFORE the growth.  Growth admits no instance and no
rule, so it changes no old pair's collapse, and an old demand of the grown
regime would already have been a demand of the base. -/
theorem apart_no_old_demand (r : Regime)
    (hq : ∀ i j, i < j → j < r.data → ¬ Demand allApart r i j)
    (i j : Nat) (hij : i < j) (hj : j < r.data)
    (hd : Demand allApart (growR r) i j) : False := by
  have hgrown : j < (growR r).data := by
    rw [growR_data]; exact Nat.lt_succ_of_lt hj
  have hcol : collapsed (growR r) i j :=
    (allApart_demand_iff (growR r) i j hij hgrown).mp hd
  exact hq i j hij hj
    ((allApart_demand_iff r i j hij hj).mpr (collapsed_of_growR r i j hcol))

/-- **apart_at_most_one_demand_after_growth.**  The TOTAL bound, in the
sealed grammar reconstructed here extended by the stake labelling every
distinct pair apart: from a well-formed regime carrying no demand, the
regime reached by one growth step carries at most one demand ALTOGETHER --
any two of its demands are the same pair.  An old pair cannot be one, by
`apart_no_old_demand`; two distinct new pairs cannot both be, by
`apart_at_most_one_new_demand`.

This replaces a weaker earlier statement.  RECORDED, because the earlier
version's doc comment claimed this total bound while its statement bounded
only the demands naming the fresh datum: an adversarial reading of the
package before it was committed found the gap between the doc and the
statement, and the statement was strengthened to match rather than the doc
weakened to match the statement. -/
theorem apart_at_most_one_demand_after_growth (r : Regime)
    (hq : ∀ i j, i < j → j < r.data → ¬ Demand allApart r i j)
    (i j i' j' : Nat)
    (hd : Demand allApart (growR r) i j)
    (hd' : Demand allApart (growR r) i' j') :
    i = i' ∧ j = j' := by
  have hbound : ∀ a b : Nat, Demand allApart (growR r) a b → b = r.data := by
    intro a b h
    have hlt : b < r.data + 1 := by
      have := h.2.1; rw [growR_data] at this; exact this
    rcases Nat.lt_or_ge b r.data with hb | hb
    · exact absurd (apart_no_old_demand r hq a b h.1 hb h) (fun x => x)
    · omega
  have hj : j = r.data := hbound i j hd
  have hj' : j' = r.data := hbound i' j' hd'
  refine ⟨?_, by rw [hj, hj']⟩
  by_cases hii : i = i'
  · exact hii
  · exfalso
    have hi : i < r.data := by have := hd.1; omega
    have hi' : i' < r.data := by have := hd'.1; omega
    exact apart_at_most_one_new_demand r hq i i' hi hi' hii
      (by rw [← hj]; exact hd) (by rw [← hj']; exact hd')

end Propagate
end SecondNoFirst
