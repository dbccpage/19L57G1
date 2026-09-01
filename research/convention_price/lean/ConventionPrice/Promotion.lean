/-
Promotion: the general two-label cure theorem (PROVED_THEOREM).

Every hop-parity family is cured by a slot assignment within the
{identity, exchange} bound after which every walk over the relabelled
hops has holonomy parity zero -- in either traversal direction.  The
witness is explicit: at each hop, the near slot is the identity and
the far slot copies the hop's own parity.  FW-SCOPE: this is a
two-label statement; nothing here mentions a larger fibre.

The contrast with `pointwise_parity_blind` is the point: the pointwise
subgroup cannot change any cycle parity, while the full slot group can
set every hop parity, and hence every cycle parity, to zero.
-/

import ConventionPrice.ParityLaws

namespace ConventionPrice

variable {H : Type}

/-- One traversal of a hop drawn from a hop family `H`; `fwd` is the
traversal direction.  At parity level the inverse of a two-label
transport is itself, so the relabelled parity below does not consult
`fwd`; carrying it in the statement is what makes "either direction"
part of the theorem rather than a remark. -/
structure Traversal (H : Type) where
  hop : H
  fwd : Bool

/-- The relabelled parity of a traversal under hop parities `t` and a
slot assignment `sl` (near slot, far slot) per hop: both slot parities
are consumed whichever direction the hop is traversed. -/
def relabelledPar (t : H → Bool) (sl : H → Bool × Bool) (x : Traversal H) : Bool :=
  (sl x.hop).1 ^^ (t x.hop ^^ (sl x.hop).2)

/-- The curing assignment: near slot identity, far slot the hop's own
parity. -/
def cureSlots (t : H → Bool) : H → Bool × Bool := fun h => (false, t h)

theorem cure_kills (t : H → Bool) (x : Traversal H) :
    relabelledPar t (cureSlots t) x = false := by
  show (false ^^ (t x.hop ^^ t x.hop)) = false
  rw [xor_self', xor_false']

theorem holo_all_false (l : List Bool) (h : ∀ x, x ∈ l → x = false) :
    holo l = false := by
  induction l with
  | nil => rfl
  | cons x rest ih =>
      rw [holo_cons, h x (List.Mem.head rest), false_xor']
      exact ih fun y hy => h y (List.Mem.tail x hy)

/-- Target 4.  Every two-label hop-parity family is cured by SOME slot
assignment within the {identity, exchange} bound: after relabelling,
every walk -- closed or not, in any traversal directions -- has
holonomy parity zero, so in particular every cycle parity vanishes. -/
theorem slot_group_sections (t : H → Bool) :
    ∃ sl : H → Bool × Bool, ∀ w : List (Traversal H),
      holo (w.map (relabelledPar t sl)) = false := by
  refine ⟨cureSlots t, fun w => holo_all_false _ fun x hx => ?_⟩
  obtain ⟨y, _, rfl⟩ := List.mem_map.mp hx
  exact cure_kills t y

end ConventionPrice
