import Derivation.CapacityBound
import Derivation.Pigeonhole
import Translation

/-!
# Chains: the admitted operations as forms, and reading E

An admitted operation is encoded as a binary form whose instances are its
graph.  Following that form from a datum `x` means taking the unique `y`
with `(3 + k, [x, y])` derivable (`follow_derivable`, `follow_unique`), and a
word of operation indices runs by following its forms in order (`run`).

* `E_iff`: irreducibility under the admitted family (the sealed
  `PrimDiff.Irred` over the closure `Clos`) is exactly "no word over the
  operation forms runs the two endpoints to the same datum" — every member
  of the closure runs a word (`clos_word`) and every word runs a member
  (`word_in_clos`).
* `E_iff_noChain`: the word criterion is decidable — a word longer than
  `n * n` revisits a pair of positions and shortens (`shorten`, by the
  sealed `Pigeonhole.pigeonhole`, with the sealed `CapacityBound.encode`
  coding the pair), so words of length at most `n * n` suffice.

AuthorityEffect: None.
-/

namespace Chains

open Derivation Translation

/-! ## 1. Following an operation form -/

/-- Following the `k`-th operation form from `x`. -/
def follow (F : FiniteSetting) (k x : Nat) : Nat := F.ops.getD k id x

theorem follow_derivable (F : FiniteSetting) {k x : Nat} (hk : k < F.ops.length) (hx : x < F.n) :
    derivable (encode F) (3 + k, [x, follow F k x]) :=
  (derivable_op F hk hx).mpr rfl

theorem follow_unique (F : FiniteSetting) {k x y : Nat} (hk : k < F.ops.length) (hx : x < F.n)
    (h : derivable (encode F) (3 + k, [x, y])) : y = follow F k x :=
  (derivable_op F hk hx).mp h

theorem follow_lt (F : FiniteSetting) {k x : Nat} (hk : k < F.ops.length) (hx : x < F.n) :
    follow F k x < F.n :=
  F.ops_closed _ (getD_mem hk) x hx

/-- Running a word of operation indices, leftmost first. -/
def run (F : FiniteSetting) : List Nat → Nat → Nat
  | [], x => x
  | k :: w, x => run F w (follow F k x)

/-- A word over the admitted operation indices. -/
def WordOk (F : FiniteSetting) (w : List Nat) : Prop := ∀ k ∈ w, k < F.ops.length

theorem wordOk_tail {F : FiniteSetting} {k : Nat} {w : List Nat} (h : WordOk F (k :: w)) :
    WordOk F w :=
  fun j hj => h j (List.mem_cons_of_mem _ hj)

theorem wordOk_head {F : FiniteSetting} {k : Nat} {w : List Nat} (h : WordOk F (k :: w)) :
    k < F.ops.length :=
  h k List.mem_cons_self

theorem run_append (F : FiniteSetting) :
    ∀ (u v : List Nat) (x : Nat), run F (u ++ v) x = run F v (run F u x)
  | [], _, _ => rfl
  | k :: u, v, x => run_append F u v (follow F k x)

theorem run_lt (F : FiniteSetting) :
    ∀ (w : List Nat) (x : Nat), WordOk F w → x < F.n → run F w x < F.n
  | [], _, _, hx => hx
  | _ :: w, _, hw, hx =>
      run_lt F w _ (wordOk_tail hw) (follow_lt F (wordOk_head hw) hx)

/-! ## 2. Words and the closure of the admitted family -/

/-- An operation lifted to the carrier. -/
def liftOp (F : FiniteSetting) (g : Nat → Nat) (hg : g ∈ F.ops) : Fin F.n → Fin F.n :=
  fun x => ⟨g x.val, F.ops_closed g hg x.val x.isLt⟩

/-- Every word runs as a member of the closure of the admitted family. -/
theorem word_in_clos (F : FiniteSetting) :
    ∀ (w : List Nat), WordOk F w →
      ∃ f : Fin F.n → Fin F.n, PrimDiff.Clos (toSetting F).Ops f ∧
        ∀ x : Fin F.n, (f x).val = run F w x.val
  | [], _ => ⟨id, PrimDiff.Clos.id, fun _ => rfl⟩
  | k :: w, hw => by
      obtain ⟨f, hf, hfx⟩ := word_in_clos F w (wordOk_tail hw)
      have hk : k < F.ops.length := wordOk_head hw
      refine ⟨f ∘ liftOp F (F.ops.getD k id) (getD_mem hk),
        PrimDiff.Clos.comp hf (PrimDiff.Clos.base ⟨F.ops.getD k id, getD_mem hk, fun _ => rfl⟩),
        ?_⟩
      intro x
      show (f (liftOp F (F.ops.getD k id) (getD_mem hk) x)).val = run F w (follow F k x.val)
      rw [hfx]
      rfl

/-- Every member of the closure runs some word. -/
theorem clos_word (F : FiniteSetting) {f : Fin F.n → Fin F.n}
    (h : PrimDiff.Clos (toSetting F).Ops f) :
    ∃ w, WordOk F w ∧ ∀ x : Fin F.n, (f x).val = run F w x.val := by
  induction h with
  | base hg =>
      obtain ⟨g, hg, hgx⟩ := hg
      obtain ⟨k, hk, hgk⟩ := List.mem_iff_getElem.mp hg
      refine ⟨[k], fun j hj => ?_, fun x => ?_⟩
      · rw [List.mem_singleton.mp hj]
        exact hk
      · show _ = follow F k x.val
        rw [hgx x]
        show g x.val = F.ops.getD k id x.val
        rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hk, hgk]
        rfl
  | id => exact ⟨[], fun _ hj => absurd hj List.not_mem_nil, fun _ => rfl⟩
  | @comp f g _ _ ihf ihg =>
      obtain ⟨wf, hwf, hf⟩ := ihf
      obtain ⟨wg, hwg, hg⟩ := ihg
      refine ⟨wg ++ wf, ?_, ?_⟩
      · intro j hj
        rcases List.mem_append.mp hj with h | h
        · exact hwg j h
        · exact hwf j h
      · intro x
        show (f (g x)).val = run F (wg ++ wf) x.val
        rw [run_append, ← hg x, ← hf (g x)]

/-- **E translates**: irreducibility under the admitted family is exactly
that no word over the operation forms runs the endpoints to the same
datum. -/
theorem E_iff (F : FiniteSetting) :
    PrimitiveCore.E (toSetting F) ↔ ∀ w, WordOk F w → run F w F.a ≠ run F w F.b := by
  constructor
  · intro h w hw heq
    obtain ⟨f, hf, hfx⟩ := word_in_clos F w hw
    apply h f hf
    apply Fin.ext
    exact (hfx ⟨F.a, F.a_lt⟩).trans (heq.trans (hfx ⟨F.b, F.b_lt⟩).symm)
  · intro h f hf heq
    obtain ⟨w, hw, hfx⟩ := clos_word F hf
    apply h w hw
    have ha := hfx ⟨F.a, F.a_lt⟩
    have hb := hfx ⟨F.b, F.b_lt⟩
    exact ha.symm.trans ((congrArg Fin.val heq).trans hb)

/-! ## 3. The bound: a long word revisits a pair of positions -/

/-- The code of a pair of carrier positions: the sealed
`CapacityBound.encode n [y, x]`, written out. -/
def code (n x y : Nat) : Nat := x * n + y

theorem code_lt {n x y : Nat} (hx : x < n) (hy : y < n) : code n x y < n * n := by
  have h : y + n * x < n ^ 2 := CapacityBound.encode_lt n [y, x] (two_args_lt hy hx)
  rw [Nat.pow_two] at h
  show x * n + y < n * n
  rw [Nat.mul_comm x n, Nat.add_comm (n * x) y]
  exact h

theorem code_inj {n x y x' y' : Nat} (hx : x < n) (hy : y < n) (hx' : x' < n) (hy' : y' < n)
    (h : code n x y = code n x' y') : x = x' ∧ y = y' := by
  have h2 : CapacityBound.encode n [y, x] = CapacityBound.encode n [y', x'] := by
    show y + n * x = y' + n * x'
    unfold code at h
    rw [Nat.mul_comm x n, Nat.add_comm (n * x) y, Nat.mul_comm x' n,
      Nat.add_comm (n * x') y'] at h
    exact h
  obtain ⟨hy2, hx2⟩ := list_two_inj
    (CapacityBound.encode_inj n [y, x] [y', x'] rfl (two_args_lt hy hx) (two_args_lt hy' hx') h2)
  exact ⟨hx2, hy2⟩

/-- The pair of positions after the first `p` indices of a word. -/
def state (F : FiniteSetting) (w : List Nat) (p : Nat) : Nat :=
  code F.n (run F (w.take p) F.a) (run F (w.take p) F.b)

theorem wordOk_take {F : FiniteSetting} {w : List Nat} (hw : WordOk F w) (p : Nat) :
    WordOk F (w.take p) :=
  fun j hj => hw j (List.mem_of_mem_take hj)

/-- Two equal position pairs cut the word between them. -/
theorem cut (F : FiniteSetting) (w : List Nat) (hw : WordOk F w) (hlen : F.n * F.n < w.length)
    (p q : Nat) (hpq : p < q) (hq : q < F.n * F.n + 1) (hst : state F w p = state F w q)
    (heq : run F w F.a = run F w F.b) :
    ∃ w', WordOk F w' ∧ w'.length < w.length ∧ run F w' F.a = run F w' F.b := by
  have hql : q ≤ w.length := by omega
  obtain ⟨ha, hb⟩ := code_inj (run_lt F _ _ (wordOk_take hw p) F.a_lt)
    (run_lt F _ _ (wordOk_take hw p) F.b_lt) (run_lt F _ _ (wordOk_take hw q) F.a_lt)
    (run_lt F _ _ (wordOk_take hw q) F.b_lt) hst
  refine ⟨w.take p ++ w.drop q, ?_, ?_, ?_⟩
  · intro j hj
    rcases List.mem_append.mp hj with h | h
    · exact hw j (List.mem_of_mem_take h)
    · exact hw j (List.mem_of_mem_drop h)
  · rw [List.length_append, List.length_take, List.length_drop]
    have hmin : min p w.length = p := Nat.min_eq_left (by omega)
    rw [hmin]
    omega
  · rw [run_append, run_append, ha, hb, ← run_append, ← run_append, List.take_append_drop]
    exact heq

/-- A word longer than `n * n` that identifies the pair shortens. -/
theorem shorten (F : FiniteSetting) (w : List Nat) (hw : WordOk F w)
    (hlen : F.n * F.n < w.length) (heq : run F w F.a = run F w F.b) :
    ∃ w', WordOk F w' ∧ w'.length < w.length ∧ run F w' F.a = run F w' F.b := by
  have hstate : ∀ p, p < F.n * F.n + 1 → state F w p < F.n * F.n := by
    intro p _
    exact code_lt (run_lt F _ _ (wordOk_take hw p) F.a_lt) (run_lt F _ _ (wordOk_take hw p) F.b_lt)
  obtain ⟨p, hp, q, hq, hpq, hst⟩ := Pigeonhole.pigeonhole (F.n * F.n) (state F w) hstate
  rcases Nat.lt_or_gt_of_ne hpq with hlt | hgt
  · exact cut F w hw hlen p q hlt hq hst heq
  · exact cut F w hw hlen q p hgt hp hst.symm heq

theorem bounded_shorten (F : FiniteSetting) :
    ∀ (m : Nat) (w : List Nat), w.length ≤ m → WordOk F w → run F w F.a = run F w F.b →
      ∃ w', WordOk F w' ∧ w'.length ≤ F.n * F.n ∧ run F w' F.a = run F w' F.b
  | 0, w, hl, hw, heq => ⟨w, hw, Nat.le_trans hl (Nat.zero_le _), heq⟩
  | m + 1, w, hl, hw, heq => by
      rcases Nat.lt_or_ge (F.n * F.n) w.length with hgt | hle
      · obtain ⟨w', hw', hlt, heq'⟩ := shorten F w hw hgt heq
        exact bounded_shorten F m w' (by omega) hw' heq'
      · exact ⟨w, hw, hle, heq⟩

/-! ## 4. The decidable criterion -/

/-- All words over `k` operation indices of length at most `L`. -/
def words (k : Nat) : Nat → List (List Nat)
  | 0 => [[]]
  | L + 1 => [] :: (List.range k).flatMap (fun i => (words k L).map (fun w => i :: w))

theorem mem_words (k : Nat) :
    ∀ (L : Nat) (w : List Nat), w ∈ words k L ↔ (∀ i ∈ w, i < k) ∧ w.length ≤ L
  | 0, w => by
      constructor
      · intro h
        have hw : w = [] := List.mem_singleton.mp h
        subst hw
        exact ⟨fun _ h => absurd h List.not_mem_nil, Nat.le_refl 0⟩
      · rintro ⟨_, hl⟩
        cases w with
        | nil => exact List.mem_singleton.mpr rfl
        | cons i t => exact absurd hl (Nat.not_succ_le_zero _)
  | L + 1, w => by
      show w ∈ [] :: (List.range k).flatMap (fun i => (words k L).map (fun w => i :: w)) ↔ _
      rw [List.mem_cons, List.mem_flatMap]
      constructor
      · rintro (rfl | ⟨i, hi, hw⟩)
        · exact ⟨fun _ h => absurd h List.not_mem_nil, Nat.zero_le _⟩
        · obtain ⟨t, ht, rfl⟩ := List.mem_map.mp hw
          obtain ⟨hall, hl⟩ := (mem_words k L t).mp ht
          refine ⟨fun j hj => ?_, Nat.succ_le_succ hl⟩
          rcases List.mem_cons.mp hj with rfl | hj
          · exact List.mem_range.mp hi
          · exact hall j hj
      · rintro ⟨hall, hl⟩
        cases w with
        | nil => exact Or.inl rfl
        | cons i t =>
            refine Or.inr ⟨i, List.mem_range.mpr (hall i List.mem_cons_self),
              List.mem_map.mpr ⟨t, ?_, rfl⟩⟩
            exact (mem_words k L t).mpr
              ⟨fun j hj => hall j (List.mem_cons_of_mem _ hj), Nat.le_of_succ_le_succ hl⟩

/-- **The decidable criterion**: no word of length at most `n * n` over the
operation forms runs the endpoints to the same datum. -/
def NoChain (F : FiniteSetting) : Prop :=
  ∀ w ∈ words F.ops.length (F.n * F.n), run F w F.a ≠ run F w F.b

instance (F : FiniteSetting) : Decidable (NoChain F) := by
  unfold NoChain; infer_instance

theorem noChain_iff (F : FiniteSetting) :
    (∀ w, WordOk F w → run F w F.a ≠ run F w F.b) ↔ NoChain F := by
  constructor
  · intro h w hw
    exact h w ((mem_words _ _ w).mp hw).1
  · intro h w hw heq
    obtain ⟨w', hw', hl, heq'⟩ := bounded_shorten F w.length w (Nat.le_refl _) hw heq
    exact h w' ((mem_words _ _ w').mpr ⟨hw', hl⟩) heq'

/-- **E is decided on the encoding**: irreducibility under the admitted
family is the bounded chain criterion. -/
theorem E_iff_noChain (F : FiniteSetting) : PrimitiveCore.E (toSetting F) ↔ NoChain F :=
  (E_iff F).trans (noChain_iff F)

end Chains

#print axioms Chains.follow_derivable
#print axioms Chains.follow_unique
#print axioms Chains.follow_lt
#print axioms Chains.wordOk_tail
#print axioms Chains.wordOk_head
#print axioms Chains.run_append
#print axioms Chains.run_lt
#print axioms Chains.word_in_clos
#print axioms Chains.clos_word
#print axioms Chains.E_iff
#print axioms Chains.code_lt
#print axioms Chains.code_inj
#print axioms Chains.wordOk_take
#print axioms Chains.cut
#print axioms Chains.shorten
#print axioms Chains.bounded_shorten
#print axioms Chains.mem_words
#print axioms Chains.noChain_iff
#print axioms Chains.E_iff_noChain
