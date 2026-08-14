import Derivation.Generator

/-!
# Depth-`d` outrun on the reflective chain (G2)

The sealed generator proves that depth-1 observation is outrun by chain
growth (`Generator.generation_never_dries`) and exhibits the depth-2
instances `depth2_separates_near_ends_n4` and `depth2_obstruction_n5`.
This module generalizes the structural half to every fixed radius.

**Radius convention, stated exactly.**  Here `d` is the GRAPH RADIUS of
the observed ball.  The sealed `Generator.profile2` observes the centre
together with its in- and out-neighbour profiles, i.e. the ball
`{i-1, i, i+1}` — radius ONE, not two.  Sealed "depth `k`" therefore
indexes radius `k-1`, and the threshold `2 * d + 3` at `d = 1` gives
`n = 5`, which is exactly `depth2_obstruction_n5`.  §3 records that
correspondence as two theorems rather than a remark.

**What is proved here and what is not.**  Proved: for every fixed
radius, all deep-interior points share one depth-`d` profile
(`depth_d_outrun`), horizon-free — no bound on `n` beyond deepness of
the two points — and a colliding deep pair exists from `n ≥ 2d + 3`
(`depth_d_obstruction`).  NOT proved here: any statement about
COLOURED views, finite view alphabets, repair strategies, or the
capacity bound that would need a pigeonhole.  Those remain OPEN; see
`contact/analysis/separation_capacity_open.md` for the exact residual
and why it is not discharged in this commit.
-/

namespace SeparationCapacity

open Generator RefusalFrontier

/-- Ordered radius-`d` ball around `i`: `[i-d, …, i+d]`.  Unclipped;
on the deep interior no clipping occurs, which is the content of
`profileD_deep`. -/
def ball (i d : Nat) : List Nat :=
  (List.range (2 * d + 1)).map (fun k => i - d + k)

theorem ball_length (i d : Nat) : (ball i d).length = 2 * d + 1 := by
  simp [ball]

/-- Depth-`d` structural profile: the SEALED depth-1 profiles along the
ball.  This is `Generator.profile1` on `Generator.reflState`, not a
private mirror, so every statement below is about the sealed chain. -/
def profileD (n i d : Nat) : List (Bool × Bool × Bool) :=
  (ball i d).map (profile1 (reflState n))

/-- Every point of a deep ball is interior, so the whole deep profile
is the constant `(true, true, true)` list.  This is the structural
uniformity the outrun rests on. -/
theorem profileD_deep (n i d : Nat) (hlo : d < i) (hhi : i + d < n) :
    profileD n i d
      = (List.range (2 * d + 1)).map (fun _ => (true, true, true)) := by
  unfold profileD ball
  rw [List.map_map]
  apply List.map_congr_left
  intro k hk
  have hkr := List.mem_range.mp hk
  show profile1 (reflState n) (i - d + k) = (true, true, true)
  apply middle_profile
  · omega
  · omega

/-- **G2 — the depth-`d` outrun.**  All deep-interior points share one
depth-`d` profile.  Horizon-free: the statement carries no threshold,
only deepness of the two points.

Scope: this is the STRUCTURAL profile.  A regime that also colours the
carrier is not covered; the constant-profile argument says nothing
about colours. -/
theorem depth_d_outrun (n i j d : Nat)
    (hi0 : d < i) (hi1 : i + d < n) (hj0 : d < j) (hj1 : j + d < n) :
    profileD n i d = profileD n j d := by
  rw [profileD_deep n i d hi0 hi1, profileD_deep n j d hj0 hj1]

/-- Obstruction form: a colliding deep pair exists from `n ≥ 2d + 3`.
The threshold is derived, not assumed — it is exactly the least `n`
at which the deep interior holds two distinct points. -/
theorem depth_d_obstruction (d n : Nat) (hn : 2 * d + 3 ≤ n) :
    ∃ i j, i ≠ j ∧ d < i ∧ i + d < n ∧ d < j ∧ j + d < n ∧
      profileD n i d = profileD n j d :=
  ⟨d + 1, d + 2, by omega, by omega, by omega, by omega, by omega,
   depth_d_outrun n (d + 1) (d + 2) d (by omega) (by omega)
     (by omega) (by omega)⟩

/-! ## Correspondence with the sealed depth-2 instances

Sealed `Generator.profile2` reads the radius-ONE ball, so the sealed
depth-2 constants are this module's `d = 1` case.  Both sealed
instances are recovered, so the two conventions are reconciled rather
than left as a naming residual. -/

/-- The sealed `depth2_obstruction_n5` threshold is this module's
`d = 1` instance: `2 * 1 + 3 = 5`. -/
theorem sealed_depth2_is_radius_one :
    ∃ i j, i ≠ j ∧ 1 < i ∧ i + 1 < 5 ∧ 1 < j ∧ j + 1 < 5 ∧
      profileD 5 i 1 = profileD 5 j 1 :=
  depth_d_obstruction 1 5 (by omega)

/-- At `n = 4` and radius one the deep interior is the singleton `{2}`,
so this module claims NO collision there.  That is why the sealed
`depth2_separates_near_ends_n4` is consistent with the outrun: the pair
`(1, 3)` it separates is not deep. -/
theorem deep_interior_singleton_at_four (i : Nat)
    (h0 : 1 < i) (h1 : i + 1 < 4) : i = 2 := by omega

end SeparationCapacity
