"""Exact P200 bodies and scoped book claims; AuthorityEffect: None."""
import json
import re
from .protocols import ROOT,SOURCE,LEAN_SOURCES

REPORTS=tuple('P200OperationalProtocols.'+name for name in (
    'prepare_product_records','prepare_symmetric_eq','record1_preserves_target',
    'readout1_preserves_l1','readout1_preserves_r2','readout1_readout2_comm','coincidence_iff',
    'readout_step_commutation','readout1_stepL2_commutation','readout2_stepM_commutation',
    'readout_replayL1_commutation','disturbing_readout_fails_commute',
    'swap_involutive','readout1_swap','readout2_swap','swap_symmetric_eq',
    'inter_observer_agreement','inter_observer_coincidence','asymmetric_observation_divergence',
    'spacelike_non_signaling','spacelike_marginal_invariance',
    'spacelike_sequence_non_signaling','causal_signaling_divergence'))
BOOK_NAMES=tuple('Textbook.Protocols.'+name for name in (
    'stale_after_change','readout_same_target_not_commutes','coarse_agreement_not_identity',
    'different_probes_break_agreement','disturbance_counter_not_repair','overlap_can_commute',
    'relay_needs_readout','remote_record_list','agreement_iff_under_injective_probe'))
BOOK=r'''
namespace Textbook.Protocols
open P200OperationalProtocols

def initial : CarrierState := { l1 := 1, l2 := 1 }
def advance (n : Nat) := (n+1)%3

theorem stale_after_change :
    (interveneL1 advance (readout1 id initial)).l1 = 2 ∧
    (interveneL1 advance (readout1 id initial)).r1 = 1 ∧
    (readout1 id (interveneL1 advance (readout1 id initial))).r1 = 2 := by decide

theorem readout_same_target_not_commutes : ¬ Commutes (readout1 id) (stepL1 advance) := by
  intro h
  have bad := congrArg CarrierState.r1 (h ({} : CarrierState))
  change (1 : Nat) = 0 at bad
  exact Nat.one_ne_zero bad

theorem coarse_agreement_not_identity :
    let s : CarrierState := { l1 := 0, l2 := 2 }
    (jointReadout (fun n => n%2) s).r1 = (jointReadout (fun n => n%2) s).r2 ∧ s.l1 ≠ s.l2 := by
  decide

theorem different_probes_break_agreement :
    let s := readout2 (fun _ => 0) (readout1 id initial)
    s.l1 = s.l2 ∧ s.r1 ≠ s.r2 := by decide

theorem disturbance_counter_not_repair :
    let s : CarrierState := {}
    let a := readout1_disturbing id advance 1 (stepL1 advance s)
    let b := stepL1 advance (readout1_disturbing id advance 1 s)
    a.l1 = b.l1 ∧ a.dist = 1 ∧ b.dist = 1 ∧ a.r1 ≠ b.r1 := by decide

theorem overlap_can_commute : Commutes (readout1 id) (stepL1 id) := fun _ => rfl

theorem relay_needs_readout :
    let s : CarrierState := { l1 := 1 }
    (causalRelay s).l2 = 1 ∧ (causalRelay s).r2 = 0 ∧
      (readout2 id (causalRelay s)).r2 = 1 := by decide

theorem remote_record_list (states : List CarrierState) (f probe : Nat → Nat) :
    states.map (fun s => (readout2 probe (interveneL1 f s)).r2) =
      states.map (fun s => (readout2 probe s).r2) := rfl

theorem agreement_iff_under_injective_probe (probe : Nat → Nat)
    (hinj : ∀ a b, probe a = probe b → a = b) (s : CarrierState) :
    (jointReadout probe s).r1 = (jointReadout probe s).r2 ↔ s.l1 = s.l2 := by
  change probe s.l1 = probe s.l2 ↔ s.l1 = s.l2
  exact ⟨hinj _ _,congrArg probe⟩

end Textbook.Protocols
'''


def build_checks():
    texts=[]
    for path in LEAN_SOURCES:
        text=(ROOT/path).read_text(encoding='utf-8')
        imports=set(re.findall(r'^import (\S+)\s*$',text,re.M))
        if imports-{'Protocol','Commutation'}:
            raise ValueError('Protocol import needs review: '+str(imports))
        texts.append(re.sub(r'^import \S+\s*\n','',text,flags=re.M))
    names=(*REPORTS,*BOOK_NAMES)
    return '\n'.join([*texts,BOOK,*('#print axioms '+name for name in names)]),names


def expected_reports():
    data=json.loads((SOURCE/'protocols_axioms.json').read_text(encoding='utf-8'))
    if set(data)!=set((*REPORTS,*BOOK_NAMES)) or any(set(v)-{'propext','Quot.sound'} for v in data.values()):
        raise ValueError('Protocol report population or axiom boundary changed')
    return {name:'depends on axioms: ['+', '.join(v)+']' if v else 'does not depend on any axioms'
            for name,v in data.items()}
