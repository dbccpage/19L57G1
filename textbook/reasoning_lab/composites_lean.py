"""Exact P203 body and book claims; AuthorityEffect: None."""
import re
from .composites import ROOT,LEAN_SOURCE

OWNER_SUFFIXES='''tensor_assoc_left_inv tensor_assoc_right_inv assoc_preserves_projA
assoc_preserves_projB assoc_preserves_projC assoc_inv_preserves_projA
assoc_inv_preserves_projB assoc_inv_preserves_projC toLeft_fromLeft fromLeft_toLeft
toRight_fromRight fromRight_toRight assoc_carrier_commute assoc_carrier_inv_commute
toProduct_fromProduct fromProduct_toProduct non_signaling_bipartite non_signaling_projB
non_signaling_a1_b1 non_signaling_a1_b2 non_signaling_a2_b1 non_signaling_a2_b2
non_signaling_sequenceA leaky_footprint_divergence mediated_signaling_divergence
swap_involutive swap_symmetric_eq duplicate_observer_agreement readout_swap_equivariance_B1
readout_swap_equivariance_A1 asymmetric_observer_divergence disconnected_cut_no_bridge
connected_cut_with_bridge'''.split()
OWNER_NAMES=tuple('P203CompositeSystems.'+n for n in OWNER_SUFFIXES)
BOOK_NAMES=tuple('Textbook.Composites.'+n for n in ('regroup_middle','local_list_projection',
    'relay_order','read_label_counterexample','equal_shares_not_rows','coarse_probe_hides',
    'injective_probe_converse','partial_symmetry_readout','different_probe_marks'))
BOOK=r'''
namespace Textbook.Composites
open P203CompositeSystems

theorem regroup_middle (a b c : Nat) :
    projB_right ((tensor_assoc Nat Nat Nat).toFun ((a,b),c)) = b := rfl

theorem local_list_projection (f : Nat × Nat → Nat × Nat) (states : List NetworkState) :
    states.map (fun s => projB (interveneA f s)) = states.map projB := by
  induction states with
  | nil => rfl
  | cons s tail ih => exact congrArg (fun rest => projB s :: rest) ih

theorem relay_order (s : NetworkState) :
    (relay_A_to_B (intervene_a2 (fun x => x+1) s)).b1 ≠
      (intervene_a2 (fun x => x+1) (relay_A_to_B s)).b1 :=
  Nat.succ_ne_self s.a2

theorem read_label_counterexample :
    let s : NetworkState := ⟨2,5,7,0⟩
    projB (intervene_a2 (fun x => x+1) s) = projB s ∧
      (intervene_a2 (fun x => x+1) s).a2 ≠ s.a2 := by decide

theorem equal_shares_not_rows :
    ([0,1] : List Nat).count 0 = ([1,0] : List Nat).count 0 ∧
    ([0,1] : List Nat).count 1 = ([1,0] : List Nat).count 1 ∧
    ([0,1] : List Nat) ≠ [1,0] := by decide

theorem coarse_probe_hides : (0 : Nat) % 2 = 2 % 2 ∧ (0 : Nat) ≠ 2 := by decide

theorem injective_probe_converse (probe : Nat → Nat) (s : NetworkState)
    (hinj : ∀ a b, probe a = probe b → a = b)
    (h : readoutA1 probe s = readoutB1 probe s) : s.a1 = s.b1 :=
  hinj s.a1 s.b1 h

theorem partial_symmetry_readout :
    let s : NetworkState := ⟨3,0,3,8⟩
    (∀ probe : Nat → Nat, readoutA1 probe s = readoutB1 probe s) ∧ s.a2 ≠ s.b2 := by
  exact ⟨fun _ => rfl,by decide⟩

theorem different_probe_marks :
    let s : NetworkState := ⟨2,0,2,0⟩
    readoutA1 (fun x => x) s ≠ readoutB1 (fun x => x+1) s := by decide

end Textbook.Composites
'''

def build_checks():
    text=(ROOT/LEAN_SOURCE).read_text(encoding='utf-8')
    if 'import ' in text or re.findall(r'^theorem (\w+)',text,re.M)!=OWNER_SUFFIXES:
        raise ValueError('Review changed P203 source/import/report population')
    assert len(OWNER_NAMES)==33 and len(BOOK_NAMES)==9
    names=(*OWNER_NAMES,*BOOK_NAMES)
    return text+'\n'+BOOK+'\n'+'\n'.join('#print axioms '+n for n in names),names

def expected_reports():return {n:'does not depend on any axioms' for n in (*OWNER_NAMES,*BOOK_NAMES)}
