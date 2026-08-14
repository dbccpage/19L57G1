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
`{i-1, i, i+1}` — radius ONE, not two.  Under that reading sealed
"depth `k`" indexes radius `k-1`, and the threshold `2 * d + 3` at
`d = 1` gives `n = 5`, the length of the sealed `depth2_obstruction_n5`
instance.  §3 turns the reading into a typed correspondence on each of
the two sealed chains: over the interior indices of `reflState 4` and
of `reflState 5`, sealed `Generator.profile2` equality and this module's
radius-one `profileD` equality are the SAME relation, decided
elementwise, and each sealed theorem is then carried across it.  The
general-`n` form of that correspondence is NOT proved.

**What is proved here and what is not.**  Proved: for every fixed
radius, all deep-interior points share one depth-`d` profile
(`depth_d_outrun`), horizon-free — no bound on `n` beyond deepness of
the two points — and a colliding deep pair exists from `n ≥ 2d + 3`
(`depth_d_obstruction`); and, on the two sealed chains only, the radius
correspondence of §3.  NOT proved here: the general-`n` radius
correspondence, and any statement about COLOURED views, finite view
alphabets, repair strategies, or the capacity bound that would need a
pigeonhole.  Those remain OPEN; see
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

/-! ## Radius correspondence with the sealed depth-2 instances

Sealed `Generator.profile2` reads the radius-ONE ball, so the sealed
depth-2 constants belong to this module's `d = 1` case.  Each theorem
below states that correspondence as a typed equivalence on ONE sealed
chain — `Generator.profile2` equality holds exactly where radius-one
`profileD` equality holds, over that chain's interior indices — and then
carries the matching sealed theorem across it.  Both are decided on
their own chain.  Neither is a general-`n` statement, and neither
re-instantiates `depth_d_obstruction` in place of the sealed result. -/

/-- **The `n = 5` correspondence, and the sealed collision carried
across it.**  First conjunct: over the interior indices `1, 2, 3, 4` of
`reflState 5`, sealed `Generator.profile2` equality and radius-one
`profileD` equality are the same relation.  Second and third conjuncts:
the deep pair `(2, 3)` of `Generator.depth2_obstruction_n5`, transported
— the proof consumes that sealed theorem and does not appeal to
`depth_d_obstruction`. -/
theorem radius_one_agrees_with_sealed_depth2_n5 :
    (∀ i ∈ [1, 2, 3, 4], ∀ j ∈ [1, 2, 3, 4],
        (profile2 (reflState 5) i = profile2 (reflState 5) j ↔
          profileD 5 i 1 = profileD 5 j 1))
      ∧ profileD 5 2 1 = profileD 5 3 1 ∧ (2 : Nat) ≠ 3 :=
  have corr : ∀ i ∈ [1, 2, 3, 4], ∀ j ∈ [1, 2, 3, 4],
      (profile2 (reflState 5) i = profile2 (reflState 5) j ↔
        profileD 5 i 1 = profileD 5 j 1) := by decide
  ⟨corr,
   (corr 2 (by decide) 3 (by decide)).mp depth2_obstruction_n5.1,
   depth2_obstruction_n5.2⟩

/-- **The `n = 4` correspondence, and the sealed separation carried
across it.**  First conjunct: the same equivalence over the interior
indices `1, 2, 3` of `reflState 4`.  Second conjunct: the pair `(1, 3)`
that `Generator.depth2_separates_near_ends_n4` separates is separated by
the radius-one profile too — again proved from the sealed theorem.
Third conjunct: the arithmetic reason this is consistent with
`depth_d_outrun` rather than a counterexample to it — at `n = 4` and
radius one the deepness side-conditions `1 < i` and `i + 1 < 4` hold
only at `i = 2`, so `(1, 3)` is not a deep pair.  That conjunct is
arithmetic and mentions no profile; it is stated inside this theorem so
the reason travels with the result it explains. -/
theorem radius_one_agrees_with_sealed_depth2_n4 :
    (∀ i ∈ [1, 2, 3], ∀ j ∈ [1, 2, 3],
        (profile2 (reflState 4) i = profile2 (reflState 4) j ↔
          profileD 4 i 1 = profileD 4 j 1))
      ∧ profileD 4 1 1 ≠ profileD 4 3 1
      ∧ ∀ i, 1 < i → i + 1 < 4 → i = 2 :=
  have corr : ∀ i ∈ [1, 2, 3], ∀ j ∈ [1, 2, 3],
      (profile2 (reflState 4) i = profile2 (reflState 4) j ↔
        profileD 4 i 1 = profileD 4 j 1) := by decide
  ⟨corr,
   fun h => depth2_separates_near_ends_n4
     ((corr 1 (by decide) 3 (by decide)).mpr h),
   fun i h0 h1 => by omega⟩

end SeparationCapacity
