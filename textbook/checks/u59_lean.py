"""Unit 59 check: kernel-check the book's Lean for Unit 59.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u59_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Attachment
import Derivation.RenamingStructure

namespace Textbook.U59
open PrimitivePassage Attachment RenamingStructure

/-- On s12 (occ = [1, 2]), the canonical fresh token is 3 and the Up block
at parent 0 targets position 2. -/
theorem freshTok_s12_val : freshTok s12 = 3 := rfl

theorem upBlock_s12_0 :
    upBlock s12 0 =
      [.admitOcc 3, .assertWit 0 2, .admitWit 0 2, .protect 0 2] := rfl

/-- Why `WFStores` is load-bearing in `up_executes`: on a live state whose
stores already contain `(0, 2)` before position 2 exists,
`attachChecked` returns `.attached` (since `0 < 2` and the state is live),
yet the duplicate-pair guards reject all three edge events and the
asserted, witnessed, and protected stores fail to grow. -/
def sIll : PState :=
  { s12 with asserted := [(0, 2)], wit := [(0, 2)], prot := [(0, 2)] }

theorem sIll_not_wf : ¬ WFStores sIll := by
  intro ⟨hwa, _, _⟩
  have h := (hwa (0, 2) List.mem_cons_self).2
  revert h
  decide

theorem sIll_attach_partial :
    attachChecked sIll 0 = .attached (replayP (upBlock sIll 0) sIll) ∧
    (replayP (upBlock sIll 0) sIll).occ.length = 3 ∧
    (replayP (upBlock sIll 0) sIll).asserted.length = sIll.asserted.length ∧
    (replayP (upBlock sIll 0) sIll).wit.length = sIll.wit.length ∧
    (replayP (upBlock sIll 0) sIll).prot.length = sIll.prot.length := by
  refine ⟨by decide, by decide, by decide, by decide, by decide⟩

/-- A concrete transposition in `Renaming 2`: swap positions 0 and 1,
fix every position `>= 2`. -/
def swap01F : Nat → Nat
  | 0 => 1
  | 1 => 0
  | x => x

theorem swap01F_idem (x : Nat) : swap01F (swap01F x) = x := by
  match x with
  | 0 => rfl
  | 1 => rfl
  | n + 2 => rfl

def swap01Ren : Renaming 2 where
  f := swap01F
  g := swap01F
  fg := swap01F_idem
  gf := swap01F_idem
  fbound := by
    intro x hx
    match x with
    | 0 => decide
    | 1 => decide
    | n + 2 => omega
  ffix := by
    intro x hx
    match x with
    | 0 => omega
    | 1 => omega
    | n + 2 => rfl

/-- Acting by `swap01Ren` on `s12` reverses its two tokens. -/
theorem act_swap01_s12 : (act swap01Ren s12).occ = [2, 1] := by decide

/-- Why the scope hypothesis `n <= s.occ.length` in `act_comp` and `act_inv`
is load-bearing: a renaming at scale 3 that swaps positions 1 and 2 moves
position 1 out of range on a 2-element carrier, so `getD` reads default 0
and `act (invRen σ) (act σ s12) ≠ s12`. -/
def swap12F : Nat → Nat
  | 1 => 2
  | 2 => 1
  | x => x

theorem swap12F_idem (x : Nat) : swap12F (swap12F x) = x := by
  match x with
  | 0 => rfl
  | 1 => rfl
  | 2 => rfl
  | n + 3 => rfl

def swap12Ren3 : Renaming 3 where
  f := swap12F
  g := swap12F
  fg := swap12F_idem
  gf := swap12F_idem
  fbound := by
    intro x hx
    match x with
    | 0 => decide
    | 1 => decide
    | 2 => decide
    | n + 3 => omega
  ffix := by
    intro x hx
    match x with
    | 0 => omega
    | 1 => omega
    | 2 => omega
    | n + 3 => rfl

theorem act_inv_out_of_scope :
    (act swap12Ren3 s12).occ = [1, 0] ∧
    act (invRen swap12Ren3) (act swap12Ren3 s12) ≠ s12 := by
  refine ⟨by decide, ?_⟩
  intro h
  have hocc := congrArg PState.occ h
  revert hocc
  decide

/-- Concrete 3-vertex path and star witnessed stores. -/
theorem tree3_stores :
    (treeAt pathPolL 2).wit = [(0, 1), (1, 2)] ∧
    (treeAt starPolL 2).wit = [(0, 1), (0, 2)] := by
  constructor <;> decide

end Textbook.U59

#print axioms Textbook.U59.freshTok_s12_val
#print axioms Textbook.U59.upBlock_s12_0
#print axioms Textbook.U59.sIll_not_wf
#print axioms Textbook.U59.sIll_attach_partial
#print axioms Textbook.U59.swap01F_idem
#print axioms Textbook.U59.act_swap01_s12
#print axioms Textbook.U59.swap12F_idem
#print axioms Textbook.U59.act_inv_out_of_scope
#print axioms Textbook.U59.tree3_stores
#print axioms Attachment.clamp_rewrote_input
#print axioms Attachment.freshTok_fresh
#print axioms Attachment.up_iff_legal
#print axioms Attachment.up_exec_eq
#print axioms Attachment.up_executes
#print axioms Attachment.attachChecked_refuses
#print axioms Attachment.length_not_fresh_countermodel
#print axioms Attachment.halted_up_inert
#print axioms Attachment.Renaming.f_inj
#print axioms Attachment.upBlock_transport
#print axioms Attachment.upFamily_transport
#print axioms Attachment.act_up_comm
#print axioms Attachment.treeAt_spec
#print axioms Attachment.attachBlock_is_upBlock
#print axioms Attachment.attach_residue
#print axioms Attachment.parent_unique
#print axioms Attachment.parent_exists
#print axioms Attachment.all_reach
#print axioms Attachment.path4_star4_not_isomorphic
#print axioms Attachment.equal_size_not_renaming_related
#print axioms Attachment.equal_cost_non_isomorphic_extensions
#print axioms RenamingStructure.Renaming.ext
#print axioms RenamingStructure.comp_id
#print axioms RenamingStructure.id_comp
#print axioms RenamingStructure.comp_assoc
#print axioms RenamingStructure.inv_comp
#print axioms RenamingStructure.comp_inv
#print axioms RenamingStructure.act_id
#print axioms RenamingStructure.act_comp
#print axioms RenamingStructure.act_inv
#print axioms RenamingStructure.wf_act
#print axioms RenamingStructure.act_up_comm_comp
#print axioms RenamingStructure.act_up_comm_twostep
#print axioms RenamingStructure.upFamily_orbit_closed
#print axioms RenamingStructure.collapse_not_a_renaming
#print axioms RenamingStructure.collapse_pushforward_ill_formed
#print axioms RenamingStructure.equivariance_summary
"""

EXPECTED = {
    "Textbook.U59.freshTok_s12_val": NONE,
    "Textbook.U59.upBlock_s12_0": NONE,
    "Textbook.U59.sIll_not_wf": NONE,
    "Textbook.U59.sIll_attach_partial": BOTH,
    "Textbook.U59.swap01F_idem": NONE,
    "Textbook.U59.act_swap01_s12": BOTH,
    "Textbook.U59.swap12F_idem": NONE,
    "Textbook.U59.act_inv_out_of_scope": BOTH,
    "Textbook.U59.tree3_stores": BOTH,
    "Attachment.clamp_rewrote_input": NONE,
    "Attachment.freshTok_fresh": BOTH,
    "Attachment.up_iff_legal": BOTH,
    "Attachment.up_exec_eq": BOTH,
    "Attachment.up_executes": BOTH,
    "Attachment.attachChecked_refuses": BOTH,
    "Attachment.length_not_fresh_countermodel": BOTH,
    "Attachment.halted_up_inert": BOTH,
    "Attachment.Renaming.f_inj": NONE,
    "Attachment.upBlock_transport": BOTH,
    "Attachment.upFamily_transport": BOTH,
    "Attachment.act_up_comm": BOTH,
    "Attachment.treeAt_spec": BOTH,
    "Attachment.attachBlock_is_upBlock": BOTH,
    "Attachment.attach_residue": BOTH,
    "Attachment.parent_unique": BOTH,
    "Attachment.parent_exists": BOTH,
    "Attachment.all_reach": BOTH,
    "Attachment.path4_star4_not_isomorphic": BOTH,
    "Attachment.equal_size_not_renaming_related": BOTH,
    "Attachment.equal_cost_non_isomorphic_extensions": BOTH,
    "RenamingStructure.Renaming.ext": NONE,
    "RenamingStructure.comp_id": NONE,
    "RenamingStructure.id_comp": NONE,
    "RenamingStructure.comp_assoc": NONE,
    "RenamingStructure.inv_comp": BOTH,
    "RenamingStructure.comp_inv": BOTH,
    "RenamingStructure.act_id": BOTH,
    "RenamingStructure.act_comp": BOTH,
    "RenamingStructure.act_inv": BOTH,
    "RenamingStructure.wf_act": BOTH,
    "RenamingStructure.act_up_comm_comp": BOTH,
    "RenamingStructure.act_up_comm_twostep": BOTH,
    "RenamingStructure.upFamily_orbit_closed": BOTH,
    "RenamingStructure.collapse_not_a_renaming": BOTH,
    "RenamingStructure.collapse_pushforward_ill_formed": BOTH,
    "RenamingStructure.equivariance_summary": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U59"))
