import Derivation.Basic
import Derivation.Attachment
import Derivation.PrimitiveCore

/-!
# Translation: a finite setting as a regime of the sealed grammar

The primitive-difference signature (`PrimitiveCore.Setting`) carries a
carrier, an asserted difference relation, two designated endpoints, a
retention store, a protection store and an admitted operation family.  A
*finite* setting — carrier `{0, …, n-1}`, decidable stores, finitely many
operations closed on the carrier — is encoded as a regime of the sealed
grammar with no new primitive:

* every store is a binary judgment form whose instances are the pairs it
  asserts (form 0 the difference relation, form 1 retention, form 2
  protection);
* every admitted operation is a binary judgment form whose instances are
  its graph (form `3 + k` for the `k`-th operation);
* no rule and no standing requirement: the demand on the designated pair
  is the seed target the engine imposes.

The encoding is faithful instance by instance (`derivable_rel`,
`derivable_ret`, `derivable_prot`, `derivable_op`), and every candidate
reading of the setting except `E` is here shown equivalent to a decidable
statement about derivable instances of the encoding at the designated pair
(`W_iff` … `F_iff`); `E` is handled in `Chains`.  The encoding carries no
requirement, so the designated pair travels beside it: two settings that
differ only in their endpoints share one regime.

AuthorityEffect: None.
-/

namespace Translation

open Derivation

/-! ## 1. Finite settings -/

/-- A finite setting: carrier `{0, …, n-1}`, boolean-valued stores, two
endpoints inside the carrier, and a finite operation family closed on the
carrier.  Operations are functions on `Nat`; only their values below `n`
matter. -/
structure FiniteSetting where
  n : Nat
  rel : Nat → Nat → Bool
  ret : Nat → Nat → Bool
  prot : Nat → Nat → Bool
  a : Nat
  b : Nat
  ops : List (Nat → Nat)
  a_lt : a < n
  b_lt : b < n
  ops_closed : ∀ g ∈ ops, ∀ x, x < n → g x < n

/-- The sealed signature the finite setting presents: carrier `Fin n`,
stores read as `= true`, operations lifted to the carrier. -/
def toSetting (F : FiniteSetting) : PrimitiveCore.Setting where
  X := Fin F.n
  r := fun x y => F.rel x.val y.val = true
  a := ⟨F.a, F.a_lt⟩
  b := ⟨F.b, F.b_lt⟩
  ret := fun x y => F.ret x.val y.val = true
  prot := fun x y => F.prot x.val y.val = true
  Ops := fun g => ∃ h, h ∈ F.ops ∧ ∀ x, (g x).val = h x.val

instance (F : FiniteSetting) (x y : Fin F.n) : Decidable ((toSetting F).r x y) :=
  inferInstanceAs (Decidable (F.rel x.val y.val = true))

/-! ## 2. List apparatus -/

theorem getD_mem {α : Type} {d : α} {l : List α} {k : Nat} (h : k < l.length) :
    l.getD k d ∈ l := by
  rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem h]
  exact List.getElem_mem h

/-- Every entry two (the sealed `Attachment.getD_lt` reads the entry). -/
theorem getD_of_all_two (l : List Nat) (hall : ∀ a ∈ l, a = 2) (i : Nat) (hi : i < l.length) :
    l.getD i 0 = 2 := by
  rw [Attachment.getD_lt hi]
  exact hall _ (List.getElem_mem hi)

theorem list_two_inj {x y x' y' : Nat} (h : [x, y] = [x', y']) : x = x' ∧ y = y' := by
  injection h with h1 h2
  injection h2 with h2 _
  exact ⟨h1, h2⟩

/-- All ordered pairs over the carrier. -/
def pairs (n : Nat) : List (Nat × Nat) :=
  (List.range n).flatMap (fun x => (List.range n).map (fun y => (x, y)))

theorem mem_pairs {n : Nat} {p : Nat × Nat} : p ∈ pairs n ↔ p.1 < n ∧ p.2 < n := by
  unfold pairs
  rw [List.mem_flatMap]
  constructor
  · rintro ⟨x, hx, hp⟩
    obtain ⟨y, hy, rfl⟩ := List.mem_map.mp hp
    exact ⟨List.mem_range.mp hx, List.mem_range.mp hy⟩
  · rintro ⟨h1, h2⟩
    exact ⟨p.1, List.mem_range.mpr h1, List.mem_map.mpr ⟨p.2, List.mem_range.mpr h2, rfl⟩⟩

/-! ## 3. The encoding -/

/-- The instances of one binary form: the pairs a store asserts. -/
def storeInsts (n f : Nat) (s : Nat → Nat → Bool) : List Inst :=
  ((pairs n).filter (fun p => s p.1 p.2)).map (fun p => (f, [p.1, p.2]))

theorem mem_storeInsts {n f : Nat} {s : Nat → Nat → Bool} {i : Inst} :
    i ∈ storeInsts n f s ↔ ∃ x y, x < n ∧ y < n ∧ s x y = true ∧ i = (f, [x, y]) := by
  unfold storeInsts
  rw [List.mem_map]
  constructor
  · rintro ⟨p, hp, rfl⟩
    have hp' := List.mem_filter.mp hp
    have hb := mem_pairs.mp hp'.1
    exact ⟨p.1, p.2, hb.1, hb.2, hp'.2, rfl⟩
  · rintro ⟨x, y, hx, hy, hs, rfl⟩
    exact ⟨(x, y), List.mem_filter.mpr ⟨mem_pairs.mpr ⟨hx, hy⟩, hs⟩, rfl⟩

/-- The instances of a list of stores on consecutive forms from `f`. -/
def storesFrom (n : Nat) : Nat → List (Nat → Nat → Bool) → List Inst
  | _, [] => []
  | f, s :: rest => storeInsts n f s ++ storesFrom n (f + 1) rest

theorem mem_storesFrom {n : Nat} {i : Inst} :
    ∀ (f : Nat) (stores : List (Nat → Nat → Bool)),
      i ∈ storesFrom n f stores ↔
        ∃ k, k < stores.length ∧ ∃ x y, x < n ∧ y < n ∧
          stores.getD k (fun _ _ => false) x y = true ∧ i = (f + k, [x, y])
  | _, [] => by
      constructor
      · intro h
        exact absurd h List.not_mem_nil
      · rintro ⟨k, hk, _⟩
        exact absurd hk (Nat.not_lt_zero k)
  | f, s :: rest => by
      show i ∈ storeInsts n f s ++ storesFrom n (f + 1) rest ↔ _
      rw [List.mem_append, mem_storeInsts, mem_storesFrom (f + 1) rest]
      constructor
      · rintro (⟨x, y, hx, hy, hs, rfl⟩ | ⟨k, hk, x, y, hx, hy, hs, rfl⟩)
        · exact ⟨0, Nat.succ_pos _, x, y, hx, hy, by rw [List.getD_cons_zero]; exact hs, rfl⟩
        · refine ⟨k + 1, Nat.succ_lt_succ hk, x, y, hx, hy, ?_, ?_⟩
          · rw [List.getD_cons_succ]
            exact hs
          · have hf : f + 1 + k = f + (k + 1) := by omega
            rw [hf]
      · rintro ⟨k, hk, x, y, hx, hy, hs, rfl⟩
        cases k with
        | zero =>
            rw [List.getD_cons_zero] at hs
            exact Or.inl ⟨x, y, hx, hy, hs, rfl⟩
        | succ k =>
            refine Or.inr ⟨k, Nat.lt_of_succ_lt_succ hk, x, y, hx, hy, ?_, ?_⟩
            · rw [List.getD_cons_succ] at hs
              exact hs
            · have hf : f + (k + 1) = f + 1 + k := by omega
              rw [hf]

/-- The graph of one operation as the instances of form `f`. -/
def graphInsts (n f : Nat) (g : Nat → Nat) : List Inst :=
  (List.range n).map (fun x => (f, [x, g x]))

theorem mem_graphInsts {n f : Nat} {g : Nat → Nat} {i : Inst} :
    i ∈ graphInsts n f g ↔ ∃ x, x < n ∧ i = (f, [x, g x]) := by
  unfold graphInsts
  rw [List.mem_map]
  constructor
  · rintro ⟨x, hx, rfl⟩
    exact ⟨x, List.mem_range.mp hx, rfl⟩
  · rintro ⟨x, hx, rfl⟩
    exact ⟨x, List.mem_range.mpr hx, rfl⟩

/-- The graphs of a list of operations on consecutive forms from `f`. -/
def graphsFrom (n : Nat) : Nat → List (Nat → Nat) → List Inst
  | _, [] => []
  | f, g :: rest => graphInsts n f g ++ graphsFrom n (f + 1) rest

theorem mem_graphsFrom {n : Nat} {i : Inst} :
    ∀ (f : Nat) (ops : List (Nat → Nat)),
      i ∈ graphsFrom n f ops ↔
        ∃ k, k < ops.length ∧ ∃ x, x < n ∧ i = (f + k, [x, ops.getD k id x])
  | _, [] => by
      constructor
      · intro h
        exact absurd h List.not_mem_nil
      · rintro ⟨k, hk, _⟩
        exact absurd hk (Nat.not_lt_zero k)
  | f, g :: rest => by
      show i ∈ graphInsts n f g ++ graphsFrom n (f + 1) rest ↔ _
      rw [List.mem_append, mem_graphInsts, mem_graphsFrom (f + 1) rest]
      constructor
      · rintro (⟨x, hx, rfl⟩ | ⟨k, hk, x, hx, rfl⟩)
        · exact ⟨0, Nat.succ_pos _, x, hx, rfl⟩
        · refine ⟨k + 1, Nat.succ_lt_succ hk, x, hx, ?_⟩
          have hf : f + 1 + k = f + (k + 1) := by omega
          rw [hf, List.getD_cons_succ]
      · rintro ⟨k, hk, x, hx, rfl⟩
        cases k with
        | zero => exact Or.inl ⟨x, hx, rfl⟩
        | succ k =>
            refine Or.inr ⟨k, Nat.lt_of_succ_lt_succ hk, x, hx, ?_⟩
            have hf : f + (k + 1) = f + 1 + k := by omega
            rw [hf, List.getD_cons_succ]

/-- **The encoding**: the carrier as data, one binary form per store and per
operation, their instances, no rule, no standing requirement. -/
def encode (F : FiniteSetting) : Regime :=
  ⟨F.n,
   [2, 2, 2] ++ F.ops.map (fun _ => 2),
   storesFrom F.n 0 [F.rel, F.ret, F.prot] ++ graphsFrom F.n 3 F.ops,
   [],
   []⟩

theorem encode_rules (F : FiniteSetting) : (encode F).rules = [] := rfl

theorem encode_reqs (F : FiniteSetting) : (encode F).reqs = [] := rfl

theorem encode_forms_length (F : FiniteSetting) :
    (encode F).forms.length = 3 + F.ops.length := by
  show ([2, 2, 2] ++ F.ops.map (fun _ => 2)).length = 3 + F.ops.length
  rw [List.length_append, List.length_map]
  rfl

/-- Every form of the encoding is binary. -/
theorem encode_forms_two (F : FiniteSetting) : ∀ a ∈ (encode F).forms, a = 2 := by
  intro a ha
  rcases List.mem_append.mp ha with h | h
  · rcases List.mem_cons.mp h with rfl | h
    · rfl
    rcases List.mem_cons.mp h with rfl | h
    · rfl
    rcases List.mem_cons.mp h with rfl | h
    · rfl
    exact absurd h List.not_mem_nil
  · obtain ⟨_, _, rfl⟩ := List.mem_map.mp h
    rfl

theorem encode_forms_getD (F : FiniteSetting) {f : Nat} (hf : f < (encode F).forms.length) :
    (encode F).forms.getD f 0 = 2 :=
  getD_of_all_two _ (encode_forms_two F) f hf

/-- The instances of the encoding, form by form. -/
theorem mem_encode_insts {F : FiniteSetting} {i : Inst} :
    i ∈ (encode F).insts ↔
      (∃ k, k < [F.rel, F.ret, F.prot].length ∧ ∃ x y, x < F.n ∧ y < F.n ∧
        [F.rel, F.ret, F.prot].getD k (fun _ _ => false) x y = true ∧ i = (0 + k, [x, y])) ∨
      (∃ k, k < F.ops.length ∧ ∃ x, x < F.n ∧ i = (3 + k, [x, F.ops.getD k id x])) := by
  show i ∈ storesFrom F.n 0 [F.rel, F.ret, F.prot] ++ graphsFrom F.n 3 F.ops ↔ _
  rw [List.mem_append, mem_storesFrom, mem_graphsFrom]

theorem two_args_lt {n x y : Nat} (hx : x < n) (hy : y < n) : ∀ a ∈ [x, y], a < n := by
  intro a ha
  rcases List.mem_cons.mp ha with rfl | ha
  · exact hx
  · rcases List.mem_cons.mp ha with rfl | ha
    · exact hy
    · exact absurd ha List.not_mem_nil

/-- The encoding is a well-formed regime of the sealed grammar. -/
theorem encode_wf (F : FiniteSetting) : (encode F).wf := by
  have hlen := encode_forms_length F
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro p hp
    rcases mem_encode_insts.mp hp with ⟨k, hk, x, y, hx, hy, _, rfl⟩ | ⟨k, hk, x, hx, rfl⟩
    · have hk3 : k < 3 := hk
      refine ⟨?_, ?_, two_args_lt hx hy⟩
      · show 0 + k < (encode F).forms.length
        omega
      · show [x, y].length = (encode F).forms.getD (0 + k) 0
        rw [encode_forms_getD F (by omega)]
        rfl
    · refine ⟨?_, ?_, two_args_lt hx (F.ops_closed _ (getD_mem hk) x hx)⟩
      · show 3 + k < (encode F).forms.length
        omega
      · show [x, F.ops.getD k id x].length = (encode F).forms.getD (3 + k) 0
        rw [encode_forms_getD F (by omega)]
        rfl
  · intro f hf
    exact absurd hf List.not_mem_nil
  · intro q hq
    exact absurd hq List.not_mem_nil
  · intro a ha
    rw [encode_forms_two F a ha]
    decide

/-! ## 4. Faithfulness: derivable instances are exactly the stores and graphs -/

theorem derivable_encode {F : FiniteSetting} {i : Inst} :
    derivable (encode F) i ↔ i ∈ (encode F).insts := by
  unfold derivable
  constructor
  · rintro (h | h)
    · exact h
    · exact absurd h List.not_mem_nil
  · exact Or.inl

/-- The three store forms assert exactly their stores. -/
theorem derivable_store (F : FiniteSetting) {k x y : Nat} (hk : k < 3) (hx : x < F.n)
    (hy : y < F.n) :
    derivable (encode F) (k, [x, y]) ↔
      [F.rel, F.ret, F.prot].getD k (fun _ _ => false) x y = true := by
  rw [derivable_encode, mem_encode_insts]
  constructor
  · rintro (⟨k', _, x', y', _, _, hs, h⟩ | ⟨k', _, x', _, h⟩)
    · injection h with h1 h2
      have hk' : k' = k := by omega
      subst hk'
      obtain ⟨rfl, rfl⟩ := list_two_inj h2
      exact hs
    · injection h with h1 _
      omega
  · intro hs
    exact Or.inl ⟨k, hk, x, y, hx, hy, hs, by rw [Nat.zero_add]⟩

/-- Form 0 asserts exactly the difference relation. -/
theorem derivable_rel (F : FiniteSetting) {x y : Nat} (hx : x < F.n) (hy : y < F.n) :
    derivable (encode F) (0, [x, y]) ↔ F.rel x y = true :=
  derivable_store F (by decide) hx hy

/-- Form 1 asserts exactly the retention store. -/
theorem derivable_ret (F : FiniteSetting) {x y : Nat} (hx : x < F.n) (hy : y < F.n) :
    derivable (encode F) (1, [x, y]) ↔ F.ret x y = true :=
  derivable_store F (by decide) hx hy

/-- Form 2 asserts exactly the protection store. -/
theorem derivable_prot (F : FiniteSetting) {x y : Nat} (hx : x < F.n) (hy : y < F.n) :
    derivable (encode F) (2, [x, y]) ↔ F.prot x y = true :=
  derivable_store F (by decide) hx hy

/-- Form `3 + k` asserts exactly the graph of the `k`-th operation. -/
theorem derivable_op (F : FiniteSetting) {k x y : Nat} (hk : k < F.ops.length) (hx : x < F.n) :
    derivable (encode F) (3 + k, [x, y]) ↔ y = F.ops.getD k id x := by
  rw [derivable_encode, mem_encode_insts]
  constructor
  · rintro (⟨k', hk', x', y', _, _, _, h⟩ | ⟨k', _, x', _, h⟩)
    · injection h with h1 _
      have hk3 : k' < 3 := hk'
      omega
    · injection h with h1 h2
      have hk' : k' = k := by omega
      subst hk'
      obtain ⟨rfl, rfl⟩ := list_two_inj h2
      rfl
  · rintro rfl
    exact Or.inr ⟨k, hk, x, hx, rfl⟩

/-! ## 5. The readings, decided on the encoding -/

/-- The designated pair is asserted by the difference form. -/
def Witnessed (F : FiniteSetting) : Prop := derivable (encode F) (0, [F.a, F.b])

/-- No self-instance of the difference form is derivable. -/
def NoSelf (F : FiniteSetting) : Prop := ∀ x, x < F.n → ¬ derivable (encode F) (0, [x, x])

/-- Every derivable link has its reverse derivable. -/
def Symmetric (F : FiniteSetting) : Prop :=
  ∀ x, x < F.n → ∀ y, y < F.n →
    derivable (encode F) (0, [x, y]) → derivable (encode F) (0, [y, x])

/-- Every derivable link splits every admitted datum. -/
def Splitting (F : FiniteSetting) : Prop :=
  ∀ x, x < F.n → ∀ y, y < F.n → derivable (encode F) (0, [x, y]) →
    ∀ z, z < F.n → derivable (encode F) (0, [x, z]) ∨ derivable (encode F) (0, [z, y])

/-- The designated pair is asserted by the retention form. -/
def Retained (F : FiniteSetting) : Prop := derivable (encode F) (1, [F.a, F.b])

/-- The designated pair is asserted by the protection form. -/
def Protected (F : FiniteSetting) : Prop := derivable (encode F) (2, [F.a, F.b])

instance (F : FiniteSetting) : Decidable (Witnessed F) := by
  unfold Witnessed; infer_instance

instance (F : FiniteSetting) : Decidable (NoSelf F) := by
  unfold NoSelf; infer_instance

instance (F : FiniteSetting) : Decidable (Symmetric F) := by
  unfold Symmetric; infer_instance

instance (F : FiniteSetting) : Decidable (Splitting F) := by
  unfold Splitting; infer_instance

instance (F : FiniteSetting) : Decidable (Retained F) := by
  unfold Retained; infer_instance

instance (F : FiniteSetting) : Decidable (Protected F) := by
  unfold Protected; infer_instance

theorem W_iff (F : FiniteSetting) : PrimitiveCore.W (toSetting F) ↔ Witnessed F := by
  show F.rel F.a F.b = true ↔ derivable (encode F) (0, [F.a, F.b])
  exact (derivable_rel F F.a_lt F.b_lt).symm

theorem irrefl_iff (F : FiniteSetting) : PrimDiff.Irrefl (toSetting F).r ↔ NoSelf F := by
  constructor
  · intro h x hx hd
    exact h ⟨x, hx⟩ ((derivable_rel F hx hx).mp hd)
  · intro h x hr
    exact h x.val x.isLt ((derivable_rel F x.isLt x.isLt).mpr hr)

theorem symm_iff (F : FiniteSetting) :
    (∀ x y, (toSetting F).r x y → (toSetting F).r y x) ↔ Symmetric F := by
  constructor
  · intro h x hx y hy hd
    exact (derivable_rel F hy hx).mpr (h ⟨x, hx⟩ ⟨y, hy⟩ ((derivable_rel F hx hy).mp hd))
  · intro h x y hr
    exact (derivable_rel F y.isLt x.isLt).mp
      (h x.val x.isLt y.val y.isLt ((derivable_rel F x.isLt y.isLt).mpr hr))

theorem cotrans_iff (F : FiniteSetting) :
    PrimitiveCore.Cotrans (toSetting F).r ↔ Splitting F := by
  constructor
  · intro h x hx y hy hd z hz
    rcases h ⟨x, hx⟩ ⟨y, hy⟩ ((derivable_rel F hx hy).mp hd) ⟨z, hz⟩ with h1 | h1
    · exact Or.inl ((derivable_rel F hx hz).mpr h1)
    · exact Or.inr ((derivable_rel F hz hy).mpr h1)
  · intro h x y hr z
    rcases h x.val x.isLt y.val y.isLt ((derivable_rel F x.isLt y.isLt).mpr hr) z.val z.isLt
      with h1 | h1
    · exact Or.inl ((derivable_rel F x.isLt z.isLt).mp h1)
    · exact Or.inr ((derivable_rel F z.isLt y.isLt).mp h1)

/-- **A translates**: the witnessed irreflexive reading is the derivable link
on the designated pair together with no derivable self-instance. -/
theorem A_iff (F : FiniteSetting) : PrimitiveCore.A (toSetting F) ↔ Witnessed F ∧ NoSelf F :=
  and_congr (W_iff F) (irrefl_iff F)

theorem Bs_iff (F : FiniteSetting) :
    PrimitiveCore.Bs (toSetting F) ↔ (Witnessed F ∧ NoSelf F) ∧ Symmetric F :=
  and_congr (A_iff F) (symm_iff F)

theorem Bc_iff (F : FiniteSetting) :
    PrimitiveCore.Bc (toSetting F) ↔ (Witnessed F ∧ NoSelf F) ∧ Splitting F :=
  and_congr (A_iff F) (cotrans_iff F)

/-- Locatedness is automatic on a finite setting (the sealed
`located_of_decidable`), so the located reading is the reading A. -/
theorem Bl_iff (F : FiniteSetting) : PrimitiveCore.Bl (toSetting F) ↔ Witnessed F ∧ NoSelf F :=
  ⟨fun h => (A_iff F).mp h.1,
   fun h => ⟨(A_iff F).mpr h,
     PrimitiveCore.located_of_decidable (toSetting F).r
       (inst := fun x y => inferInstanceAs (Decidable (F.rel x.val y.val = true)))⟩⟩

theorem C_iff (F : FiniteSetting) : PrimitiveCore.C (toSetting F) ↔ Witnessed F ∧ Protected F := by
  show (F.rel F.a F.b = true ∧ F.prot F.a F.b = true) ↔ _
  exact and_congr (derivable_rel F F.a_lt F.b_lt).symm (derivable_prot F F.a_lt F.b_lt).symm

theorem D_iff (F : FiniteSetting) : PrimitiveCore.D (toSetting F) ↔ F.a ≠ F.b := by
  rw [PrimitiveCore.D_iff_ne]
  show (⟨F.a, F.a_lt⟩ : Fin F.n) ≠ ⟨F.b, F.b_lt⟩ ↔ F.a ≠ F.b
  constructor
  · intro h he
    exact h (Fin.ext he)
  · intro h he
    exact h (Fin.ext_iff.mp he)

theorem F_iff (F : FiniteSetting) :
    PrimitiveCore.F (toSetting F) ↔ (Witnessed F ∧ NoSelf F) ∧ Retained F ∧ Protected F := by
  show (PrimitiveCore.A (toSetting F) ∧ F.ret F.a F.b = true ∧ F.prot F.a F.b = true) ↔ _
  exact and_congr (A_iff F)
    (and_congr (derivable_ret F F.a_lt F.b_lt).symm (derivable_prot F F.a_lt F.b_lt).symm)

end Translation

#print axioms Translation.getD_mem
#print axioms Translation.getD_of_all_two
#print axioms Translation.list_two_inj
#print axioms Translation.mem_pairs
#print axioms Translation.mem_storeInsts
#print axioms Translation.mem_storesFrom
#print axioms Translation.mem_graphInsts
#print axioms Translation.mem_graphsFrom
#print axioms Translation.encode_rules
#print axioms Translation.encode_reqs
#print axioms Translation.encode_forms_length
#print axioms Translation.encode_forms_two
#print axioms Translation.encode_forms_getD
#print axioms Translation.mem_encode_insts
#print axioms Translation.two_args_lt
#print axioms Translation.encode_wf
#print axioms Translation.derivable_encode
#print axioms Translation.derivable_store
#print axioms Translation.derivable_rel
#print axioms Translation.derivable_ret
#print axioms Translation.derivable_prot
#print axioms Translation.derivable_op
#print axioms Translation.W_iff
#print axioms Translation.irrefl_iff
#print axioms Translation.symm_iff
#print axioms Translation.cotrans_iff
#print axioms Translation.A_iff
#print axioms Translation.Bs_iff
#print axioms Translation.Bc_iff
#print axioms Translation.Bl_iff
#print axioms Translation.C_iff
#print axioms Translation.D_iff
#print axioms Translation.F_iff
