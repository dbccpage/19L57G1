import SecondEngine.Kernel
import SecondEngine.IsoKernel
import SecondEngine.Orbit
import SecondEngine.Stake

/-!
# What the rules read at the genesis of reading L

Native to continuation one.

The sealed Python genesis of reading L supplies four tokens and admits
two data; it imposes no requirement.  (The sealed Lean regime `R2L` is
the later Challenge 3 regime and carries the imposed requirement; it is
not this one.)  `genL` is the regime of two data and nothing else, and
`genL_replays` shows that the genesis history, with its tokens mirrored
as numbers, replays to it.

At `genL` the two data are collapsed (no instance is admitted) and in one
orbit (the swap is an automorphism, `swapL`).  So E-four, which labels a
pair in one orbit apart, has a demand there; E-three, which labels it
same, has none; E-one never has one; and the flip of E-one has one.

`minima_differ_at_genL` is the fact the ledger cites for the refusal of
uniqueness among the count-minimal engines of the class: two of them,
alike in every capability but the rule their generator reads, part at
the root of reading L -- one has a demand and the other none.

AuthorityEffect: None.
-/

namespace SecondEngine
namespace Genesis

open Sealed Orbit Stake

/-- The genesis regime of reading L: two data and nothing else. -/
def genL : Regime := ⟨2, [], [], [], []⟩

/-- The swap of the two data, as an inhabitant of `Iso genL genL`. -/
def swapL : Iso genL genL where
  dmap := swap01
  dinv := swap01
  fmap := id
  finv := id
  dmap_lt := by decide
  dinv_lt := by decide
  dinv_dmap := by decide
  dmap_dinv := by decide
  fmap_lt := fun _ hf => nomatch hf
  finv_lt := fun _ hf => nomatch hf
  finv_fmap := fun _ hf => nomatch hf
  fmap_finv := fun _ hf => nomatch hf
  arity := fun _ hf => nomatch hf
  insts_fwd := fun _ hp => nomatch hp
  insts_bwd := fun _ hp => nomatch hp
  rules_fwd := fun _ hf => nomatch hf
  rules_bwd := fun _ hf => nomatch hf
  reqs_fwd := fun _ hq => nomatch hq
  reqs_bwd := fun _ hq => nomatch hq

/-- The genesis history of reading L, its four tokens mirrored as
numbers, replays to `genL`. -/
theorem genL_replays :
    replayE [.supply 0, .supply 1, .supply 1, .supply 2, .admitDatum, .admitDatum]
      genesis = some genL := by
  decide

/-- The two data of `genL` lie in one orbit. -/
theorem genL_one_orbit : OneOrbit genL 0 1 := ⟨swapL, rfl⟩

/-- The two data of `genL` are collapsed. -/
theorem genL_collapsed : collapsed genL 0 1 := collapsed_of_no_insts genL rfl 0 1

/-- E-four has a demand at `genL`. -/
theorem e4_demands_at_genL : Demand E4 genL 0 1 :=
  Or.inl ⟨genL_one_orbit, genL_collapsed⟩

/-- E-three has no demand at `genL`. -/
theorem e3_quiet_at_genL : ¬ Demand E3 genL 0 1 := by
  rintro (⟨hno, _⟩ | ⟨_, hs⟩)
  · exact hno genL_one_orbit
  · exact separable_not_collapsed hs genL_collapsed

/-- The flip of E-one has a demand at `genL`. -/
theorem e1_flip_demands_at_genL : Demand E1.flip genL 0 1 :=
  e1_flip_demands genL 0 1 (Or.inl genL_collapsed)

/-- Two count-minimal engines of the class part at the root of reading
L: the one reading E-four has a demand there, the one reading E-one has
none. -/
theorem minima_differ_at_genL : Demand E4 genL 0 1 ∧ ¬ Demand E1 genL 0 1 :=
  ⟨e4_demands_at_genL, e1_never_demands genL 0 1⟩

end Genesis
end SecondEngine
