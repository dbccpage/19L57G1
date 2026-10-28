/-!
# B1(ii)–(iii): how many phases interference forces, and that finitely many suffice

AuthorityEffect: None.  Core Lean only.

A finite cyclic phase group of order `N` is written as the exponents
`0, …, N - 1`; conjugation sends `j` to `neg N j = (N - j) % N`.

* ADMISSION (part of A_amp, priced): the mixing readout depends on the
  relative phase `g` only through `Re g`, and `Re g = Re ḡ`.  So an admitted
  readout on phases is a function `r` with `Invariant N r`.  Nothing here
  assumes `r` is the real part; the statements hold for every invariant
  readout.
* THEOREMS:
  - `readout_factors`: an invariant readout is a function of the class
    representative `rep N j = min j (N - j)`, which is at most `N / 2`;
  - `multiplicity_bound`: `k` phases with pairwise different readouts force
    `k ≤ N / 2 + 1`;
  - `realizable_iff`: for `k ≥ 1` and `N ≥ 1`, some invariant readout
    separates `k` phases of the order-`N` group exactly when
    `2k - 2 ≤ N`; so the least order is `2k - 2` (for `k ≥ 2`), the sign
    group `N = 2` works exactly when `k ≤ 2`, and `k = 3` needs order four;
  - `finite_order_suffices` (B1(iii)): for every `k` some finite order
    realizes `k` separated phases.  The circle is not needed for any finite
    multiplicity.

Outside the system: `N` and `k` are metatheory numbers; each statement is
proved once, uniformly, and no totality of phase groups is held.  That the
real part on the order-`N` roots of unity is injective on class
representatives (so `Re` itself realizes the bound for every `N`) is a
classical fact about the cosine, not proved here; it is proved here for
`N = 4` over `ℤ[i]` (`Gauss.mu4_readout_values`).
-/

namespace ResearchQmBridge
namespace Multiplicity

/-- Conjugation on the exponents of the order-`N` cyclic group. -/
def neg (N j : Nat) : Nat := (N - j) % N

/-- The class representative of `j` under conjugation. -/
def rep (N j : Nat) : Nat := min j (N - j)

/-- An admitted readout on phases: invariant under conjugation. -/
def Invariant (N : Nat) (r : Nat → Int) : Prop := ∀ j, j < N → r (neg N j) = r j

theorem rep_le {N j : Nat} (h : j < N) : rep N j ≤ N / 2 := by
  unfold rep; omega

theorem rep_lt {N j : Nat} (h : j < N) : rep N j < N := by
  unfold rep; omega

theorem rep_neg {N j : Nat} (h : j < N) : rep N (neg N j) = rep N j := by
  unfold rep neg
  rcases Nat.eq_zero_or_pos j with rfl | hj
  · simp
  · have : (N - j) % N = N - j := Nat.mod_eq_of_lt (by omega)
    rw [this]; omega

theorem rep_invariant (N : Nat) : Invariant N (fun j => (rep N j : Int)) := by
  intro j hj
  simp only [rep_neg hj]

theorem rep_eq_self {N j : Nat} (h : 2 * j ≤ N) : rep N j = j := by
  unfold rep; omega

/-- An invariant readout is a function of the class representative. -/
theorem readout_factors {N : Nat} {r : Nat → Int} (hr : Invariant N r) {j : Nat} (hj : j < N) :
    r (rep N j) = r j := by
  unfold rep
  by_cases hc : j ≤ N - j
  · rw [Nat.min_eq_left hc]
  · rw [Nat.min_eq_right (by omega)]
    have hpos : 0 < j := by omega
    have hn : neg N j = N - j := by
      unfold neg; exact Nat.mod_eq_of_lt (by omega)
    rw [← hn]
    exact hr j hj

/-! ## A choice-free pigeonhole on lists of naturals -/

theorem filter_split (p : Nat → Bool) : ∀ l : List Nat,
    (l.filter p).length + (l.filter (fun x => !p x)).length = l.length
  | [] => rfl
  | a :: t => by
    have ih := filter_split p t
    cases h : p a <;> simp [h] <;> omega

theorem nodup_const_le_one {l : List Nat} {m : Nat} (hn : l.Nodup) (hl : ∀ x ∈ l, x = m) :
    l.length ≤ 1 := by
  match l, hn, hl with
  | [], _, _ => simp
  | [_], _, _ => simp
  | a :: b :: t, hn, hl =>
    exfalso
    have ha := hl a (by simp)
    have hb := hl b (by simp)
    exact (List.nodup_cons.mp hn).1 (by simp [ha, hb])

theorem nodup_le : ∀ (m : Nat) {l : List Nat}, l.Nodup → (∀ x ∈ l, x < m) → l.length ≤ m
  | 0, l, _, hl => by
    cases l with
    | nil => simp
    | cons a t => exact absurd (hl a (by simp)) (Nat.not_lt_zero a)
  | m + 1, l, hn, hl => by
    have h1 : (l.filter (fun x => x != m)).length ≤ m :=
      nodup_le m (hn.filter _) (fun x hx => by
        have ⟨hxl, hxm⟩ := List.mem_filter.mp hx
        have := hl x hxl
        simp at hxm; omega)
    have h2 : (l.filter (fun x => !(x != m))).length ≤ 1 :=
      nodup_const_le_one (hn.filter _) (fun x hx => by
        have ⟨_, hxm⟩ := List.mem_filter.mp hx
        simpa using hxm)
    have := filter_split (fun x => x != m) l
    omega

/-- The phases `k - 1, …, 1, 0`. -/
def down : Nat → List Nat
  | 0 => []
  | n + 1 => n :: down n

theorem mem_down {n j : Nat} : j ∈ down n → j < n := by
  induction n with
  | zero => simp [down]
  | succ n ih =>
    intro h
    simp only [down, List.mem_cons] at h
    rcases h with rfl | h
    · omega
    · have := ih h; omega

theorem length_down (n : Nat) : (down n).length = n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [down, ih]

/-- The cast of `down n` to the integers has no repeats. -/
theorem down_cast_nodup : ∀ n : Nat, ((down n).map (fun j : Nat => (j : Int))).Nodup
  | 0 => List.Pairwise.nil
  | n + 1 => by
    refine List.Pairwise.cons ?_ (down_cast_nodup n)
    intro b hb he
    obtain ⟨j, hj, rfl⟩ := List.mem_map.mp hb
    have hlt := mem_down hj
    have : n = j := Int.ofNat.inj he
    omega

/-! ## The multiplicity bound and its tightness -/

/-- `k` phases of the order-`N` group with pairwise different readouts. -/
def Separates (N : Nat) (r : Nat → Int) (ps : List Nat) : Prop :=
  (∀ j ∈ ps, j < N) ∧ (ps.map r).Nodup

/-- NECESSITY: separated phases number at most `N / 2 + 1`. -/
theorem multiplicity_bound {N : Nat} {r : Nat → Int} (hr : Invariant N r) {ps : List Nat}
    (hs : Separates N r ps) : ps.length ≤ N / 2 + 1 := by
  obtain ⟨hlt, hd⟩ := hs
  have hmap : ps.map r = ps.map (fun j => r (rep N j)) :=
    List.map_congr_left (fun j hj => (readout_factors hr (hlt j hj)).symm)
  rw [hmap] at hd
  have hrep : (ps.map (rep N)).Nodup := by
    have hp : ps.Pairwise (fun a b => rep N a ≠ rep N b) :=
      List.Pairwise.of_map (fun j => r (rep N j)) (fun a b h he => h (by rw [he])) hd
    exact List.pairwise_map.mpr hp
  have := nodup_le (N / 2 + 1) hrep (fun x hx => by
    obtain ⟨j, hj, rfl⟩ := List.mem_map.mp hx
    exact Nat.lt_succ_of_le (rep_le (hlt j hj)))
  simpa using this

/-- SUFFICIENCY: when `k ≤ N / 2 + 1`, the class readout separates the
phases `0, …, k - 1`. -/
theorem rep_separates {N k : Nat} (hN : 0 < N) (hk : k ≤ N / 2 + 1) :
    Separates N (fun j => (rep N j : Int)) (down k) := by
  refine ⟨fun j hj => ?_, ?_⟩
  · have := mem_down hj; omega
  · have hmap : (down k).map (fun j => (rep N j : Int)) =
        (down k).map (fun j : Nat => (j : Int)) :=
      List.map_congr_left (fun j hj => by
        have := mem_down hj
        show ((rep N j : Nat) : Int) = (j : Int)
        rw [rep_eq_self (by omega)])
    rw [hmap]
    exact down_cast_nodup k

/-- Some invariant readout separates `k` phases of the order-`N` group. -/
def Realizable (N k : Nat) : Prop :=
  ∃ r : Nat → Int, Invariant N r ∧ ∃ ps : List Nat, ps.length = k ∧ Separates N r ps

/-- The least phase group for multiplicity `k` has order `2k - 2`. -/
theorem realizable_iff {N k : Nat} (hN : 0 < N) (hk : 1 ≤ k) :
    Realizable N k ↔ 2 * k - 2 ≤ N := by
  constructor
  · rintro ⟨r, hr, ps, hlen, hs⟩
    have := multiplicity_bound hr hs
    omega
  · intro h
    exact ⟨_, rep_invariant N, down k, length_down k, rep_separates hN (by omega)⟩

/-- The sign group carries exactly two separated phases. -/
theorem signs_iff {k : Nat} (hk : 1 ≤ k) : Realizable 2 k ↔ k ≤ 2 := by
  rw [realizable_iff (by decide) hk]
  constructor <;> intro h <;> omega

theorem three_needs_four : ¬ Realizable 2 3 ∧ ¬ Realizable 3 3 ∧ Realizable 4 3 := by
  refine ⟨?_, ?_, ?_⟩
  · rw [realizable_iff (by decide) (by decide)]; decide
  · rw [realizable_iff (by decide) (by decide)]; decide
  · rw [realizable_iff (by decide) (by decide)]; decide

/-- B1(iii): every finite multiplicity is met by a finite phase group. -/
theorem finite_order_suffices (k : Nat) : ∃ N, 0 < N ∧ Realizable N k := by
  refine ⟨2 * k + 1, by omega, ?_⟩
  exact ⟨_, rep_invariant _, down k, length_down k, rep_separates (by omega) (by omega)⟩

end Multiplicity
end ResearchQmBridge
