import RepresentedEmitter

/-!
Scoped negative for the represented two-edge instance channel.

Class `InClass` is stored form-0 ternary instructions. Membership does
not mention E1, owed-separation, or separability. It is nonempty, and
every `Enabled` output names a member as its instruction. A successful
functional-graph run of such an instruction is `Enabled` as well.

E1 is a reading of a class member that yields an output, together with a
sealed step that stores that output. The storing event may be
`admitInst`; forbidding every such event would exclude the channel under
test. Native store without that tuple's `admitInst` is a separate
predicate (`NativeStore`) and is unsatisfiable on the sealed grammar.

E2′ is an owed pair at the post-state, not an `impose` origin, produced
by `Enabled` firing, not `reqs` membership.

E3 is a freshly owed pair whose payload is rule-produced (the census
tag: already-separable, or admitted-not-rule-produced, does not
qualify). Rule-produced plus a ruled `admitInst` leaves separability
unchanged, so the pair cannot be freshly owed.

`no_member_is_endogenous` uses class membership: the reading names the
stored instruction. This closes OB-1 negatively for this class only.

A sibling class `I1Class` is the Stage-1 pair-instance encoding: a
stored binary form-0 instance with distinct endpoints. It is disjoint
from `InClass`. Channel E1 for that encoding is the step that stores
the pair instance itself. Shared E2′ requires `Enabled` firing, which
those pair instances are not. Unruled I1 samples separate their
endpoints. Literal `reqs` E2 is not used. OB-1 remains OPEN outside
these two classes.

AuthorityEffect: None.
-/

namespace InstanceDemand.NoGo
open Derivation
open InstanceDemand
open InstanceDemand.Emitter

/-- Stored Stage-3 instruction. Membership does not mention the output. -/
def InClass (r : Regime) (c : Inst) : Prop :=
  ∃ k l o, c = (0, [k, l, o]) ∧ c ∈ r.insts

/-- The instruction is read as producing an Enabled composition output. -/
def readsOutput (r : Regime) (c out : Inst) : Prop :=
  c ∈ r.insts ∧ Enabled r.insts out ∧
    ∃ k l o, c = (0, [k, l, o]) ∧ out.1 = 3 + o

/-- Channel E1: a stored instruction is read, and a sealed step stores
the output. The step may be `admitInst` of that output. -/
def E1 (r s : Regime) (e : Event) (c out : Inst) : Prop :=
  readsOutput r c out ∧ stepE r e = some s ∧
    out ∈ s.insts ∧ out ∉ r.insts

/-- Store that is not the tuple's own `admitInst`. Unsatisfiable. -/
def NativeStore (r s : Regime) (e : Event) (out : Inst) : Prop :=
  stepE r e = some s ∧ out ∈ s.insts ∧ out ∉ r.insts ∧
    e ≠ Event.admitInst out.1 out.2

def OwedSeparation (r : Regime) (i j : Nat) : Prop :=
  i < j ∧ j < r.data ∧ ¬ separable r i j

/-- Owed pair after the step, not an `impose`, produced by Enabled firing.
The pair need not be in `reqs`. -/
def E2prime (r s : Regime) (e : Event) (out : Inst) (i j : Nat) : Prop :=
  out.2 = [i, j] ∧ OwedSeparation s i j ∧
    (∀ x y, e ≠ Event.impose x y) ∧ Enabled r.insts out

/-- Collapsed after, not owed before, and rule-produced.
Admitted-not-rule-produced payloads do not qualify. -/
def E3 (r s : Regime) (out : Inst) (i j : Nat) : Prop :=
  out.2 = [i, j] ∧ OwedSeparation s i j ∧
    ¬ OwedSeparation r i j ∧ out.1 ∈ r.rules

theorem class_independent_of_coverage :
    InClass (seed 3 0 2 1 false) (0, [0, 1, 2]) ∧
    InClass (seed 3 0 2 1 true) (0, [0, 1, 2]) :=
  ⟨⟨0, 1, 2, rfl, by simp [seed]⟩, ⟨0, 1, 2, rfl, by simp [seed]⟩⟩

theorem class_nonempty : ∃ r c, InClass r c :=
  ⟨seed 3 0 2 1 false, (0, [0, 1, 2]), class_independent_of_coverage.1⟩

/-- Every Enabled output names a stored form-0 ternary as its instruction. -/
theorem class_covers_enabled {r : Regime} {i : Inst}
    (h : Enabled r.insts i) :
    ∃ k l o, InClass r (0, [k, l, o]) ∧ i.1 = 3 + o := by
  rcases h with ⟨k, l, o, _x, _z, _y, hc, _, _, _, hi⟩
  exact ⟨k, l, o, ⟨k, l, o, rfl, hc⟩, congrArg Prod.fst hi⟩

/-- A successful functional-graph run of a stored instruction is Enabled. -/
theorem class_covers_functional {r : Regime} {k l o x y : Nat}
    (hc : (0, [k, l, o]) ∈ r.insts) (hxy : x < y)
    (hr : (Execution.run ⟨r.insts, [k, l], x, []⟩).map Execution.Config.active = some y) :
    InClass r (0, [k, l, o]) ∧ Enabled r.insts (3 + o, [x, y]) :=
  ⟨⟨k, l, o, rfl, hc⟩, (raw_mem _ _).mp (execution_output_retained _ k l o x y hc hxy hr)⟩

theorem native_store_impossible {r s : Regime} {e : Event} {out : Inst}
    (h : NativeStore r s e out) : False :=
  h.2.2.2 (new_stored_instance_needs_event h.1 h.2.1 h.2.2.1)

/-- A writer of instances other than `admitInst` of the new tuple is not
a sealed `Event`. That missing operation would be a grammar extension. -/
theorem missing_operation_is_extension {r s : Regime} {e : Event} {out : Inst}
    (h : NativeStore r s e out) : False :=
  native_store_impossible h

theorem non_admitInst_keeps_insts {r s : Regime} {e : Event}
    (h : stepE r e = some s) (hne : ∀ f args, e ≠ Event.admitInst f args) :
    s.insts = r.insts := by
  cases e with
  | supply t => cases h; rfl
  | admitDatum => cases h; rfl
  | admitForm a =>
      change (if 1 ≤ a then some { r with forms := r.forms ++ [a] } else none) = some s at h
      split at h
      · cases h; rfl
      · cases h
  | admitInst f args => exact False.elim (hne f args rfl)
  | admitRuleAll f =>
      change (if f < r.forms.length then some { r with rules := insertNew r.rules f }
        else none) = some s at h
      split at h
      · cases h; rfl
      · cases h
  | impose i j =>
      change (if i < j ∧ j < r.data then some { r with reqs := insertNew r.reqs (i, j) }
        else none) = some s at h
      split at h
      · cases h; rfl
      · cases h

theorem admitInst_step_inv {r s : Regime} {f : Nat} {args : List Nat}
    (h : stepE r (.admitInst f args) = some s) :
    f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
      (∀ x ∈ args, x < r.data) ∧
      s = { r with insts := insertNew r.insts (f, args) } := by
  change (if f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
      (∀ x ∈ args, x < r.data) then
    some { r with insts := insertNew r.insts (f, args) } else none) = some s at h
  split at h
  · cases h
    rename_i hcond
    exact ⟨hcond.1, hcond.2.1, hcond.2.2, rfl⟩
  · cases h

theorem derivable_iff_of_ruled_admitInst {r s : Regime} {f : Nat} {args : List Nat}
    (h : stepE r (.admitInst f args) = some s) (hf : f ∈ r.rules) (k : Inst) :
    derivable s k ↔ derivable r k := by
  have inv := admitInst_step_inv h
  have hs : s.insts = insertNew r.insts (f, args) := by rw [inv.2.2.2]
  have hr : s.rules = r.rules := by rw [inv.2.2.2]
  constructor
  · intro d
    cases d with
    | inl hk =>
        have hk' : k ∈ insertNew r.insts (f, args) := hs ▸ hk
        cases (mem_insertNew).1 hk' with
        | inl hin => exact Or.inl hin
        | inr heq =>
            have hk1 : k.1 = f := congrArg Prod.fst heq
            exact Or.inr (hk1 ▸ hf)
    | inr hk => exact Or.inr (hr ▸ hk)
  · intro d
    cases d with
    | inl hk => exact Or.inl (hs ▸ (mem_insertNew).2 (Or.inl hk))
    | inr hk => exact Or.inr (hr ▸ hk)

theorem wfCtx_iff_of_admitInst {r s : Regime} {f : Nat} {args : List Nat} {c : Ctx}
    (h : stepE r (.admitInst f args) = some s) :
    wfCtx s c ↔ wfCtx r c := by
  have inv := admitInst_step_inv h
  have hd : s.data = r.data := by rw [inv.2.2.2]
  have hf : s.forms = r.forms := by rw [inv.2.2.2]
  simp [wfCtx, hd, hf]

theorem separable_iff_of_ruled_admitInst {r s : Regime} {f : Nat} {args : List Nat}
    {i j : Nat}
    (h : stepE r (.admitInst f args) = some s) (hf : f ∈ r.rules) :
    separable s i j ↔ separable r i j := by
  constructor
  · intro ⟨c, hw, hd⟩
    refine ⟨c, (wfCtx_iff_of_admitInst h).mp hw, ?_⟩
    intro hiff
    apply hd
    have di := derivable_iff_of_ruled_admitInst h hf (plug c i)
    have dj := derivable_iff_of_ruled_admitInst h hf (plug c j)
    exact di.trans (hiff.trans dj.symm)
  · intro ⟨c, hw, hd⟩
    refine ⟨c, (wfCtx_iff_of_admitInst h).mpr hw, ?_⟩
    intro hiff
    apply hd
    have di := derivable_iff_of_ruled_admitInst h hf (plug c i)
    have dj := derivable_iff_of_ruled_admitInst h hf (plug c j)
    exact di.symm.trans (hiff.trans dj)

theorem owed_iff_of_ruled_admitInst {r s : Regime} {f : Nat} {args : List Nat}
    {i j : Nat}
    (h : stepE r (.admitInst f args) = some s) (hf : f ∈ r.rules) :
    OwedSeparation s i j ↔ OwedSeparation r i j := by
  have inv := admitInst_step_inv h
  have hd : s.data = r.data := by rw [inv.2.2.2]
  have hs := separable_iff_of_ruled_admitInst (i := i) (j := j) h hf
  constructor
  · intro ⟨hij, hj, hns⟩
    exact ⟨hij, hd ▸ hj, fun hsep => hns (hs.mpr hsep)⟩
  · intro ⟨hij, hj, hns⟩
    exact ⟨hij, hd ▸ hj, fun hsep => hns (hs.mp hsep)⟩

theorem shape_imposed_fails_E2p {r s : Regime} {out : Inst} {i j : Nat} :
    ¬ E2prime r s (Event.impose i j) out i j := by
  intro h
  exact h.2.2.1 i j rfl

theorem shape_unruled_fails_E3 {r s : Regime} {out : Inst} {i j : Nat}
    (hun : out.1 ∉ r.rules) : ¬ E3 r s out i j := by
  intro h
  exact hun h.2.2.2

theorem shape_ruled_fails_E3 {r s : Regime} {f : Nat} {args : List Nat}
    {out : Inst} {i j : Nat}
    (h : stepE r (.admitInst f args) = some s) (hf : f ∈ r.rules) :
    ¬ E3 r s out i j := by
  intro hE
  have hiff := owed_iff_of_ruled_admitInst (i := i) (j := j) h hf
  exact hE.2.2.1 (hiff.mp hE.2.1)

/-- After unruled emission of the Enabled output, the endpoints separate,
so the pair is not owed at the post-state. -/
theorem shape_unruled_emission_fails_owed {n x z y : Nat}
    (hxy : x < y) (hyn : y < n) :
    ¬ OwedSeparation (emit (seed n x z y false)) x y := by
  intro h
  exact h.2.2 (unruled_emission_separates n x z y hxy hyn)

theorem e1_step_is_admitInst {r s : Regime} {e : Event} {c out : Inst}
    (h : E1 r s e c out) : e = Event.admitInst out.1 out.2 :=
  new_stored_instance_needs_event h.2.1 h.2.2.1 h.2.2.2

/-- No class member satisfies E1 ∧ E2′ ∧ E3 together. The reading is of
the stored instruction named by `InClass`; E3 then requires that
instruction's output form already carry a uniform rule, so the store
cannot freshly owe the pair. -/
theorem no_member_is_endogenous
    {r s : Regime} {c out : Inst} {e : Event} {i j : Nat}
    (hc : InClass r c)
    (h : E1 r s e c out ∧ E2prime r s e out i j ∧ E3 r s out i j) : False := by
  rcases hc with ⟨k, l, o, rfl, hc_mem⟩
  rcases h with ⟨hE1, hE2, hE3⟩
  rcases hE1 with ⟨hread, hstep, hmem, hfresh⟩
  rcases hread with ⟨_hc_stored, _henabled, _k', _l', o', hc_read, hform⟩
  injection hc_read with _ hargs
  injection hargs with _ htl
  injection htl with _ hlast
  injection hlast with ho
  have hform' : out.1 = 3 + o := ho ▸ hform
  have he : e = Event.admitInst out.1 out.2 :=
    new_stored_instance_needs_event hstep hmem hfresh
  have hstep' : stepE r (.admitInst out.1 out.2) = some s := he ▸ hstep
  have hpin :
      InClass r (0, [k, l, o]) ∧ Enabled r.insts out ∧ out.1 = 3 + o :=
    ⟨⟨k, l, o, rfl, hc_mem⟩, hE2.2.2.2, hform'⟩
  have hrule : out.1 ∈ r.rules := hE3.2.2.2
  have _pin := hpin
  exact shape_ruled_fails_E3 hstep' hrule hE3

/-! ## Sibling class: Stage-1 pair-instance encoding -/

/-- Stored binary form-0 instance with distinct endpoints.
Membership does not mention E1, owed-separation, or separability. -/
def I1Class (r : Regime) (c : Inst) : Prop :=
  ∃ x y, c = (0, [x, y]) ∧ x ≠ y ∧ c ∈ r.insts

/-- The construct is the pair instance; reading it yields itself. -/
def I1Reads (c out : Inst) : Prop :=
  out = c ∧ ∃ x y, c = (0, [x, y]) ∧ x ≠ y

/-- Channel E1 for I1: a sealed step stores that pair instance. -/
def I1E1 (r s : Regime) (e : Event) (c out : Inst) : Prop :=
  I1Reads c out ∧ stepE r e = some s ∧
    out ∈ s.insts ∧ out ∉ r.insts

theorem i1_class_lone :
    I1Class (lone 2 0 1) (0, [0, 1]) :=
  ⟨0, 1, rfl, by decide, by simp [lone]⟩

theorem i1_class_nonempty : ∃ r c, I1Class r c :=
  ⟨lone 2 0 1, (0, [0, 1]), i1_class_lone⟩

theorem i1_class_covered :
    I1Class (covered 2 0 1) (0, [0, 1]) :=
  ⟨0, 1, rfl, by decide, by simp [covered]⟩

theorem i1_class_covers_reading_L :
    I1Class (lone 2 0 1) (0, [0, 1]) ∧
    I1Class (lone 3 1 2) (0, [1, 2]) :=
  ⟨i1_class_lone, ⟨1, 2, rfl, by decide, by simp [lone]⟩⟩

theorem enabled_output_form {s : List Inst} {i : Inst}
    (h : Enabled s i) : ∃ o, i.1 = 3 + o := by
  rcases h with ⟨_k, _l, o, _x, _z, _y, _, _, _, _, hi⟩
  exact ⟨o, congrArg Prod.fst hi⟩

theorem i1_class_disjoint_instruction {r : Regime} {c : Inst}
    (h : I1Class r c) : ¬ InClass r c := by
  rcases h with ⟨x, y, rfl, _, _⟩
  intro hi
  rcases hi with ⟨k, l, o, hceq, _⟩
  have hlen := congrArg (fun p : Inst => p.2.length) hceq
  simp at hlen

theorem instruction_disjoint_i1 {r : Regime} {c : Inst}
    (h : InClass r c) : ¬ I1Class r c :=
  fun hi => i1_class_disjoint_instruction hi h

theorem i1_reads_not_enabled {s : List Inst} {c out : Inst}
    (h : I1Reads c out) (he : Enabled s out) : False := by
  rcases h with ⟨rfl, _x, _y, hc, _⟩
  rcases enabled_output_form he with ⟨o, hf⟩
  have h0 : out.1 = 0 := congrArg Prod.fst hc
  omega

theorem i1_lone_not_owed {n x y : Nat} (hxy : x < y) (hy : y < n) :
    ¬ OwedSeparation (lone n x y) x y := by
  intro h
  have hne : x ≠ y := Nat.ne_of_lt hxy
  exact h.2.2 (lone_pair_separates n x y hne hy)

theorem i1_e1_is_admitInst {r s : Regime} {e : Event} {c out : Inst}
    (h : I1E1 r s e c out) : e = Event.admitInst out.1 out.2 :=
  new_stored_instance_needs_event h.2.1 h.2.2.1 h.2.2.2

/-- No I1-class member satisfies I1E1 ∧ E2′ ∧ E3. Shared E2′ requires
Enabled firing; a pair-instance payload is not an Enabled output. -/
theorem no_i1_member_is_endogenous
    {r s : Regime} {c out : Inst} {e : Event} {i j : Nat}
    (_hc : I1Class s c)
    (h : I1E1 r s e c out ∧ E2prime r s e out i j ∧ E3 r s out i j) : False := by
  exact i1_reads_not_enabled h.1.1 h.2.1.2.2.2

end InstanceDemand.NoGo

#print axioms InstanceDemand.NoGo.class_independent_of_coverage
#print axioms InstanceDemand.NoGo.class_nonempty
#print axioms InstanceDemand.NoGo.class_covers_enabled
#print axioms InstanceDemand.NoGo.class_covers_functional
#print axioms InstanceDemand.NoGo.native_store_impossible
#print axioms InstanceDemand.NoGo.missing_operation_is_extension
#print axioms InstanceDemand.NoGo.non_admitInst_keeps_insts
#print axioms InstanceDemand.NoGo.admitInst_step_inv
#print axioms InstanceDemand.NoGo.derivable_iff_of_ruled_admitInst
#print axioms InstanceDemand.NoGo.wfCtx_iff_of_admitInst
#print axioms InstanceDemand.NoGo.separable_iff_of_ruled_admitInst
#print axioms InstanceDemand.NoGo.owed_iff_of_ruled_admitInst
#print axioms InstanceDemand.NoGo.shape_imposed_fails_E2p
#print axioms InstanceDemand.NoGo.shape_unruled_fails_E3
#print axioms InstanceDemand.NoGo.shape_ruled_fails_E3
#print axioms InstanceDemand.NoGo.shape_unruled_emission_fails_owed
#print axioms InstanceDemand.NoGo.e1_step_is_admitInst
#print axioms InstanceDemand.NoGo.no_member_is_endogenous
#print axioms InstanceDemand.NoGo.i1_class_lone
#print axioms InstanceDemand.NoGo.i1_class_nonempty
#print axioms InstanceDemand.NoGo.i1_class_covered
#print axioms InstanceDemand.NoGo.i1_class_covers_reading_L
#print axioms InstanceDemand.NoGo.enabled_output_form
#print axioms InstanceDemand.NoGo.i1_class_disjoint_instruction
#print axioms InstanceDemand.NoGo.instruction_disjoint_i1
#print axioms InstanceDemand.NoGo.i1_reads_not_enabled
#print axioms InstanceDemand.NoGo.i1_reads_not_enabled._proof_1_1
#print axioms InstanceDemand.NoGo.i1_lone_not_owed
#print axioms InstanceDemand.NoGo.i1_e1_is_admitInst
#print axioms InstanceDemand.NoGo.no_i1_member_is_endogenous
