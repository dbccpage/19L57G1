/-!
# Observer visibility: passivity, kernel cover, necessity

Native development.  A gauge is an abelian group with a nonnegative
integer mass `nu` (a decidable subsemiring of the rationals), vanishing
only at zero.  Diagrams are finite lists of covering edges with identity
restrictions.  AuthorityEffect: None.
-/

namespace ObserverVisibility

structure AbGroup (G : Type) where
  add : G → G → G
  zero : G
  neg : G → G
  add_assoc : ∀ a b c, add (add a b) c = add a (add b c)
  add_comm : ∀ a b, add a b = add b a
  zero_add : ∀ a, add zero a = a
  add_neg : ∀ a, add a (neg a) = zero

namespace AbGroup

variable {G : Type} (P : AbGroup G)

theorem add_zero (a : G) : P.add a P.zero = a := by
  rw [P.add_comm, P.zero_add]

theorem neg_add (a : G) : P.add (P.neg a) a = P.zero := by
  rw [P.add_comm, P.add_neg]

end AbGroup

structure Gauge (G : Type) where
  grp : AbGroup G
  nu : G → Nat
  nu_zero : nu grp.zero = 0
  nu_neg : ∀ x, nu (grp.neg x) = nu x
  nu_tri : ∀ x y, nu (grp.add x y) ≤ nu x + nu y
  nu_faith : ∀ x, nu x = 0 → x = grp.zero

structure LinCon (G H : Type) (NG : Gauge G) (NH : Gauge H) where
  toFun : G → H
  map_add : ∀ x y, toFun (NG.grp.add x y) = NH.grp.add (toFun x) (toFun y)
  map_zero : toFun NG.grp.zero = NH.grp.zero
  contract : ∀ x, NH.nu (toFun x) ≤ NG.nu x

variable {G H : Type}

def sumNu (N : Gauge G) : List G → Nat
  | [] => 0
  | x :: xs => N.nu x + sumNu N xs

theorem sumNu_nonneg (N : Gauge G) (xs : List G) : 0 ≤ sumNu N xs :=
  Nat.zero_le _

theorem passivity_term (NG : Gauge G) (NH : Gauge H)
    (f : LinCon G H NG NH) (x : G) :
    NH.nu (f.toFun x) ≤ NG.nu x :=
  f.contract x

def Jlist (NG : Gauge G) (NH : Gauge H) :
    List (LinCon G H NG NH × G) → Nat
  | [] => 0
  | p :: ps => NH.nu (p.1.toFun p.2) + Jlist NG NH ps

theorem j_le_i (NG : Gauge G) (NH : Gauge H) :
    ∀ items : List (LinCon G H NG NH × G),
      Jlist NG NH items ≤ sumNu NG (items.map Prod.snd)
  | [] => Nat.le_refl 0
  | p :: ps =>
    Nat.add_le_add (p.1.contract p.2) (j_le_i NG NH ps)

theorem sumNu_zero_each (N : Gauge G) :
    ∀ xs : List G, sumNu N xs = 0 → ∀ x ∈ xs, N.nu x = 0
  | [], _, x, hx => by cases hx
  | y :: ys, h, x, hx => by
    have hs : N.nu y + sumNu N ys = 0 := h
    have hy : N.nu y = 0 := (Nat.add_eq_zero_iff.mp hs).1
    have ht : sumNu N ys = 0 := (Nat.add_eq_zero_iff.mp hs).2
    cases hx with
    | head => exact hy
    | tail _ hmem => exact sumNu_zero_each N ys ht x hmem

theorem i_zero_forces_j_zero (NG : Gauge G) (NH : Gauge H)
    (items : List (LinCon G H NG NH × G))
    (hI : sumNu NG (items.map Prod.snd) = 0) :
    Jlist NG NH items = 0 := by
  have hj := j_le_i NG NH items
  have hle : Jlist NG NH items ≤ 0 := Nat.le_trans hj (Nat.le_of_eq hI)
  exact Nat.eq_zero_of_le_zero hle

/-- One observer on a coboundary list: `none` means the slot is unwatched,
so its mass sits in `I` and contributes `0` to this observer's `J`.
Extra coboundary values with no watcher are likewise unwatched. -/
def Jobs (NG : Gauge G) (NH : Gauge H) :
    List (Option (LinCon G H NG NH)) → List G → Nat
  | [], _ => 0
  | _, [] => 0
  | none :: fs, _x :: xs => Jobs NG NH fs xs
  | some f :: fs, x :: xs => NH.nu (f.toFun x) + Jobs NG NH fs xs

/-- For any observer, `J ≤ I`. Unwatched slots only add to `I`. -/
theorem j_le_i_unwatched (NG : Gauge G) (NH : Gauge H) :
    ∀ (fs : List (Option (LinCon G H NG NH))) (xs : List G),
      Jobs NG NH fs xs ≤ sumNu NG xs
  | [], _xs => Nat.zero_le _
  | _f :: _fs, [] => Nat.le_refl 0
  | none :: fs, _x :: xs =>
    Nat.le_trans (j_le_i_unwatched NG NH fs xs)
      (Nat.le_add_left (sumNu NG xs) (NG.nu _x))
  | some f :: fs, x :: xs =>
    Nat.add_le_add (f.contract x) (j_le_i_unwatched NG NH fs xs)

/-- `I = 0` forces this observer's `J` to vanish. -/
theorem jobs_zero_of_i_zero (NG : Gauge G) (NH : Gauge H)
    (xs : List G) (hI : sumNu NG xs = 0)
    (fs : List (Option (LinCon G H NG NH))) :
    Jobs NG NH fs xs = 0 :=
  Nat.eq_zero_of_le_zero
    (Nat.le_trans (j_le_i_unwatched NG NH fs xs) (Nat.le_of_eq hI))

/-- `I = 0` forces every listed observer's `J` to vanish. -/
theorem i_zero_forces_every_j_zero (NG : Gauge G) (NH : Gauge H)
    (xs : List G) (hI : sumNu NG xs = 0)
    (observers : List (List (Option (LinCon G H NG NH)))) :
    ∀ fs ∈ observers, Jobs NG NH fs xs = 0 :=
  fun fs _ => jobs_zero_of_i_zero NG NH xs hI fs

/-- Joint kernel predicate: killed by every listed watcher. -/
def inJointKer (NG : Gauge G) (NH : Gauge H)
    (fs : List (LinCon G H NG NH)) (x : G) : Prop :=
  ∀ f ∈ fs, f.toFun x = NH.grp.zero

def allGreen (NG : Gauge G) (NH : Gauge H) :
    List (LinCon G H NG NH × G) → Prop
  | [] => True
  | p :: ps => p.1.toFun p.2 = NH.grp.zero ∧ allGreen NG NH ps

theorem allGreen_iff_in_joint_ker (NG : Gauge G) (NH : Gauge H) :
    ∀ items : List (LinCon G H NG NH × G),
      allGreen NG NH items ↔
        ∀ p ∈ items, p.1.toFun p.2 = NH.grp.zero
  | [] => by
    constructor
    · intro _ p hp
      cases hp
    · intro _
      trivial
  | p :: ps => by
    constructor
    · intro h q hq
      have hp : p.1.toFun p.2 = NH.grp.zero ∧ allGreen NG NH ps := h
      cases hq with
      | head => exact hp.1
      | tail _ hmem =>
        exact (allGreen_iff_in_joint_ker NG NH ps).mp hp.2 q hmem
    · intro h
      exact ⟨h p (List.Mem.head _),
        (allGreen_iff_in_joint_ker NG NH ps).mpr fun q hq =>
          h q (List.Mem.tail _ hq)⟩

theorem allGreen_of_in_joint_ker (NG : Gauge G) (NH : Gauge H)
    (items : List (LinCon G H NG NH × G))
    (h : ∀ p ∈ items, p.1.toFun p.2 = NH.grp.zero) :
    allGreen NG NH items :=
  (allGreen_iff_in_joint_ker NG NH items).mpr h

theorem in_joint_ker_of_allGreen (NG : Gauge G) (NH : Gauge H)
    (items : List (LinCon G H NG NH × G))
    (h : allGreen NG NH items) :
    ∀ p ∈ items, p.1.toFun p.2 = NH.grp.zero :=
  (allGreen_iff_in_joint_ker NG NH items).mp h

/-! ## Integer plane gauge -/

abbrev V := Int × Int

def vadd (p q : V) : V := (p.1 + q.1, p.2 + q.2)
def vneg (p : V) : V := (-p.1, -p.2)
def vzero : V := (0, 0)

def vGrp : AbGroup V where
  add := vadd
  zero := vzero
  neg := vneg
  add_assoc := by
    intro a b c
    apply Prod.ext <;> simp [vadd, Int.add_assoc]
  add_comm := by
    intro a b
    apply Prod.ext <;> simp [vadd, Int.add_comm]
  zero_add := by
    intro a
    apply Prod.ext <;> simp [vadd, vzero]
  add_neg := by
    intro a
    apply Prod.ext
    · change a.1 - a.1 = 0
      exact Int.sub_self a.1
    · change a.2 - a.2 = 0
      exact Int.sub_self a.2

def vnu (p : V) : Nat := p.1.natAbs + p.2.natAbs

def vGauge : Gauge V where
  grp := vGrp
  nu := vnu
  nu_zero := rfl
  nu_neg := by
    intro x
    simp [vnu, vGrp]
    change (-x.1).natAbs + (-x.2).natAbs = x.1.natAbs + x.2.natAbs
    rw [Int.natAbs_neg, Int.natAbs_neg]
  nu_tri := by
    intro x y
    simp [vnu, vGrp]
    change (x.1 + y.1).natAbs + (x.2 + y.2).natAbs ≤
      (x.1.natAbs + x.2.natAbs) + (y.1.natAbs + y.2.natAbs)
    have h1 := Int.natAbs_add_le x.1 y.1
    have h2 := Int.natAbs_add_le x.2 y.2
    have hsum := Nat.add_le_add h1 h2
    have hr :
        x.1.natAbs + y.1.natAbs + (x.2.natAbs + y.2.natAbs) =
          x.1.natAbs + x.2.natAbs + (y.1.natAbs + y.2.natAbs) := by
      simp [Nat.add_assoc, Nat.add_left_comm]
    exact Nat.le_trans hsum (Nat.le_of_eq hr)
  nu_faith := by
    intro x h
    have hx : x.1.natAbs = 0 := (Nat.add_eq_zero_iff.mp h).1
    have hy : x.2.natAbs = 0 := (Nat.add_eq_zero_iff.mp h).2
    apply Prod.ext
    · exact Int.natAbs_eq_zero.mp hx
    · exact Int.natAbs_eq_zero.mp hy

def zGauge : Gauge Int where
  grp :=
    { add := Int.add
      zero := 0
      neg := Int.neg
      add_assoc := Int.add_assoc
      add_comm := Int.add_comm
      zero_add := Int.zero_add
      add_neg := fun a => Int.sub_self a }
  nu := Int.natAbs
  nu_zero := rfl
  nu_neg := fun x => Int.natAbs_neg x
  nu_tri := fun x y => Int.natAbs_add_le x y
  nu_faith := fun _x h => Int.natAbs_eq_zero.mp h

def coord : LinCon V Int vGauge zGauge where
  toFun := fun p => p.1
  map_add := by intro x y; rfl
  map_zero := rfl
  contract := by
    intro p
    exact Nat.le_add_right p.1.natAbs p.2.natAbs

/-! ## OV3 three-patch Čech nerve: 6 covering edges -/

/-- Objects: 0,1,2 patches; 3,4,5 overlaps AB, BC, CA. -/
def patch3_s : Nat → V
  | 0 | 1 | 2 => vzero
  | _ => (0, 1)

/-- Edges overlap→patch: (3,0) (3,1) (4,1) (4,2) (5,2) (5,0). -/
def patch3_edges : List (Nat × Nat) :=
  [(3, 0), (3, 1), (4, 1), (4, 2), (5, 2), (5, 0)]

def cob (s : Nat → V) (e : Nat × Nat) : V :=
  vadd (s e.2) (vneg (s e.1))

def patch3_ds : List V := patch3_edges.map (cob patch3_s)

theorem cob_overlap : cob patch3_s (3, 0) = (0, -1) := rfl

theorem patch3_cob_form (e : Nat × Nat) (he : e ∈ patch3_edges) :
    cob patch3_s e = (0, -1) := by
  revert e he
  decide

theorem patch3_mass : sumNu vGauge patch3_ds = 6 := by
  decide

theorem patch3_allGreen :
    ∀ e ∈ patch3_edges, coord.toFun (cob patch3_s e) = (0 : Int) := by
  decide

theorem patch3_full_coverage : patch3_edges.length = 6 := rfl

/-- No recovery modulus: any `f` with `f 0 = 0` fails `I ≤ f (max J)` on
the OV3 section, because `max J = 0` and `I = 6`. -/
theorem no_recovery_modulus :
    ∀ f : Nat → Nat, f 0 = 0 → ¬ sumNu vGauge patch3_ds ≤ f 0 := by
  intro f hf hle
  rw [patch3_mass, hf] at hle
  exact Nat.not_succ_le_zero 5 hle

/-! ## OV4, OV5: coboundary image meeting the joint kernel -/

/-- List mass of the coboundary of `s` on `edges`. -/
def Iof (s : Nat → V) (edges : List (Nat × Nat)) : Nat :=
  sumNu vGauge (edges.map (cob s))

/-- All-Green for the first-coordinate watcher. -/
def allGreenS (s : Nat → V) (edges : List (Nat × Nat)) : Prop :=
  ∀ e ∈ edges, coord.toFun (cob s e) = (0 : Int)

/-- Coboundary lies in the product of first-coordinate kernels. -/
def inK (s : Nat → V) (edges : List (Nat × Nat)) : Prop :=
  ∀ e ∈ edges, (cob s e).1 = (0 : Int)

/-- The coboundary itself is the group zero on every edge. -/
def cobZero (s : Nat → V) (edges : List (Nat × Nat)) : Prop :=
  ∀ e ∈ edges, cob s e = vzero

/-- Soundness: All-Green forces coboundary mass zero, for every section. -/
def soundS (edges : List (Nat × Nat)) : Prop :=
  ∀ s : Nat → V, allGreenS s edges → Iof s edges = 0

/-- `im(D) ∩ ∏ K_e = {0}`: a coboundary in the joint kernel is zero. -/
def imDCapK0 (edges : List (Nat × Nat)) : Prop :=
  ∀ s : Nat → V, inK s edges → cobZero s edges

theorem trivial_joint_ker_sound (N : Gauge G) (ds : List G)
    (h : ∀ x ∈ ds, x = N.grp.zero) : sumNu N ds = 0 := by
  induction ds with
  | nil => rfl
  | cons x xs ih =>
    have hx : x = N.grp.zero := h x (List.Mem.head _)
    have hxs : ∀ y ∈ xs, y = N.grp.zero := fun y hy =>
      h y (List.Mem.tail _ hy)
    simp [sumNu, hx, N.nu_zero]
    exact ih hxs

theorem allGreenS_iff_inK (s : Nat → V) (edges : List (Nat × Nat)) :
    allGreenS s edges ↔ inK s edges :=
  Iff.rfl

theorem Iof_zero_iff (s : Nat → V) :
    ∀ edges : List (Nat × Nat),
      Iof s edges = 0 ↔ cobZero s edges
  | [] => by
    constructor
    · intro _ e he
      cases he
    · intro _
      rfl
  | e :: es => by
    constructor
    · intro hI f hf
      have hunfold : vGauge.nu (cob s e) + Iof s es = 0 := by
        simpa [Iof, sumNu] using hI
      have he0 : vGauge.nu (cob s e) = 0 := (Nat.add_eq_zero_iff.mp hunfold).1
      have ht : Iof s es = 0 := (Nat.add_eq_zero_iff.mp hunfold).2
      cases hf with
      | head => exact vGauge.nu_faith (cob s e) he0
      | tail _ hmem => exact ((Iof_zero_iff s es).mp ht) f hmem
    · intro h
      have hez : cob s e = vzero := h e (List.Mem.head _)
      have htail : Iof s es = 0 :=
        (Iof_zero_iff s es).mpr fun f hf => h f (List.Mem.tail _ hf)
      simp only [Iof, sumNu, List.map, hez]
      have hz : vGauge.nu vzero = 0 := vGauge.nu_zero
      rw [hz, Nat.zero_add]
      exact htail

/-- OV5: the family is sound iff the coboundary image meets the joint
kernel only at zero.  The two sides are independent: `soundS` is mass
vanishing under All-Green; `imDCapK0` is vanishing of coboundary values
in the kernel.  The bridge is `nu`-faithfulness plus the coordinate
watcher. -/
theorem sound_iff_imD_cap_K (edges : List (Nat × Nat)) :
    soundS edges ↔ imDCapK0 edges := by
  constructor
  · intro hs s hk
    have hag : allGreenS s edges := (allGreenS_iff_inK s edges).mpr hk
    have hI : Iof s edges = 0 := hs s hag
    exact (Iof_zero_iff s edges).mp hI
  · intro him s hag
    have hk : inK s edges := (allGreenS_iff_inK s edges).mp hag
    have hz : cobZero s edges := him s hk
    exact (Iof_zero_iff s edges).mpr hz

/-- OV4: if every kernel is `{0}`, All-Green is `cob = 0`, which forces
`I = 0`. -/
theorem trivial_kers_imply_sound (s : Nat → V) (edges : List (Nat × Nat))
    (h : cobZero s edges) : Iof s edges = 0 :=
  (Iof_zero_iff s edges).mpr h

/-! ## OV6: coboundary along a path; zero coboundary has mass zero -/

theorem int_path (x y z : Int) : z + -x = (y + -x) + (z + -y) := by
  rw [Int.add_comm (y + -x)]
  rw [Int.add_assoc]
  rw [← Int.add_assoc (-y) y (-x)]
  rw [Int.add_left_neg]
  rw [Int.zero_add]

/-- Chord equals the sum of the two path coboundaries.  Face flux of a
coboundary is therefore zero, which is the finite-group reason `Phi`
vanishes exactly on cochains with both fluxes zero. -/
theorem cob_along_path (s : Nat → V) (a b c : Nat) :
    cob s (a, c) = vadd (cob s (a, b)) (cob s (b, c)) := by
  apply Prod.ext
  · change (s c).1 + -(s a).1 =
      ((s b).1 + -(s a).1) + ((s c).1 + -(s b).1)
    exact int_path (s a).1 (s b).1 (s c).1
  · change (s c).2 + -(s a).2 =
      ((s b).2 + -(s a).2) + ((s c).2 + -(s b).2)
    exact int_path (s a).2 (s b).2 (s c).2

theorem phi_zero_of_zero_coboundary (ds : List V)
    (h : ∀ x ∈ ds, x = vzero) : sumNu vGauge ds = 0 :=
  trivial_joint_ker_sound vGauge ds h

/-! ## OV7: `I - max J = edge_loss + fragment` -/

def obsList : List V → Nat
  | [] => 0
  | p :: ps => p.1.natAbs + obsList ps

theorem obs_le_mass : ∀ xs : List V, obsList xs ≤ sumNu vGauge xs
  | [] => Nat.le_refl 0
  | p :: ps =>
    Nat.add_le_add (Nat.le_add_right p.1.natAbs p.2.natAbs) (obs_le_mass ps)

theorem nat_gap (I obs maxJ : Nat) (hObs : obs ≤ I) (hMax : maxJ ≤ obs) :
    I - maxJ = (I - obs) + (obs - maxJ) := by
  have h1 : (I - obs) + obs - maxJ = (I - obs) + (obs - maxJ) :=
    Nat.add_sub_assoc hMax (I - obs)
  have h2 : (I - obs) + obs = I := Nat.sub_add_cancel hObs
  rw [← h1, h2]

theorem gap_splits (xs : List V) (maxJ : Nat)
    (hMax : maxJ ≤ obsList xs) :
    sumNu vGauge xs - maxJ =
      (sumNu vGauge xs - obsList xs) + (obsList xs - maxJ) :=
  nat_gap (sumNu vGauge xs) (obsList xs) maxJ (obs_le_mass xs) hMax

/-! ## OV8: dual coefficients of absolute value at most 1 bound mass -/

def pairing : List Int → List V → Int
  | [], _ => 0
  | _, [] => 0
  | y :: ys, p :: xs => y * p.2 + pairing ys xs

theorem dual_one (y : Int) (p : V) (h : y.natAbs ≤ 1) :
    (y * p.2).natAbs ≤ vnu p := by
  have hm : (y * p.2).natAbs = y.natAbs * p.2.natAbs := Int.natAbs_mul y p.2
  rw [hm]
  have hle : y.natAbs * p.2.natAbs ≤ p.2.natAbs := by
    have hmul := Nat.mul_le_mul_right p.2.natAbs h
    exact Nat.le_trans hmul (Nat.le_of_eq (Nat.one_mul p.2.natAbs))
  exact Nat.le_trans hle (Nat.le_add_left p.2.natAbs p.1.natAbs)

theorem dual_pair_le_mass :
    ∀ (ys : List Int) (xs : List V),
      (∀ y ∈ ys, y.natAbs ≤ 1) →
      (pairing ys xs).natAbs ≤ sumNu vGauge xs
  | [], xs, _ => by
    have : pairing [] xs = 0 := by cases xs <;> rfl
    rw [this]
    exact Nat.zero_le _
  | _y :: _ys, [], _ => by
    change (0 : Int).natAbs ≤ 0
    exact Nat.le_refl 0
  | y :: ys, p :: ps, h => by
    have hy : y.natAbs ≤ 1 := h y (List.Mem.head _)
    have ht : ∀ z ∈ ys, z.natAbs ≤ 1 :=
      fun z hz => h z (List.Mem.tail _ hz)
    have hone := dual_one y p hy
    have hrest := dual_pair_le_mass ys ps ht
    have hadd := Int.natAbs_add_le (y * p.2) (pairing ys ps)
    exact Nat.le_trans hadd (Nat.add_le_add hone hrest)

end ObserverVisibility
