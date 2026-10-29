"""Exact native source with numerical book examples; AuthorityEffect: None."""
import json
import re
from .run_lab import ROOT, SOURCE, NATIVE_SOURCES

WEIGHT_REPORTS = ('WeightProfile.profile_trans', 'WeightProfile.zero_scale_boundary',
                  'WeightProfile.signed_square_presentations_split',
                  'WeightProfile.profile_forgets_total')
BOOK_NAMES = ('counts_and_duplicates', 'positive_proportions', 'zero_middle',
              'signed_steps', 'new_signed_readings', 'coordinate_square',
              'doubled_readings', 'mirror_same_reading', 'six_position_groups',
              'position_labels_break_reversal', 'singleton_lookup')

BOOK_SOURCE = '''
namespace Textbook.NumberLab
open WeightProfile
open ResearchQmBridge.Gauss ResearchQmBridge.Gauss.GI
open ResearchQmBridge.Multiplicity

def a : Weights | 0 => 2 | 1 => 3 | _ => 0
def b : Weights | 0 => 4 | 1 => 6 | _ => 0
def z : Weights := fun _ => 0
def reversed : Weights | 0 => 3 | 1 => 2 | _ => 0

theorem counts_and_duplicates :
    total [0, 1] a = 5 ∧ total [0, 0, 1] a = 7 ∧ ¬ CarrierList [0, 0, 1] := by
  simp [total, a, CarrierList]

theorem positive_proportions : SameProfile [0, 1] a b := by
  intro p hp
  simp at hp
  rcases hp with rfl | rfl <;> decide

theorem zero_middle :
    SameProfile [0, 1] a z ∧ SameProfile [0, 1] z reversed ∧
      ¬ SameProfile [0, 1] a reversed := by
  refine ⟨?_, ?_, ?_⟩
  · intro p _; change a p * 0 = 0 * 5; omega
  · intro p _; change 0 * 5 = reversed p * 0; omega
  · intro h
    have h0 := h 0 (by decide)
    change 2 * 5 = 3 * 5 at h0
    omega

theorem signed_steps : (3 : Int) + (-2) = 1 ∧ (-2 : Int) + (-1) = -3 ∧
    (-2 : Int) * (-2) = 4 := by decide

theorem new_signed_readings : mixSum 3 2 = 25 ∧ mixSum 3 (-2) = 1 := by decide

theorem coordinate_square : norm ⟨3, 4⟩ = 25 ∧ add ⟨2, 0⟩ ⟨0, -2⟩ = ⟨2, -2⟩ := by decide

theorem doubled_readings :
    weights (⟨2, 0⟩, ⟨2, 0⟩) = (4, 4) ∧
    weights (⟨2, 0⟩, ⟨0, 2⟩) = (4, 4) ∧
    weights (⟨2, 0⟩, ⟨-2, 0⟩) = (4, 4) ∧
    mix (⟨2, 0⟩, ⟨2, 0⟩) = 16 ∧
    mix (⟨2, 0⟩, ⟨0, 2⟩) = 8 ∧
    mix (⟨2, 0⟩, ⟨-2, 0⟩) = 0 := by decide

theorem mirror_same_reading :
    mix (⟨2, 0⟩, ⟨0, 2⟩) = mix (⟨2, 0⟩, ⟨0, -2⟩) ∧
    (⟨0, 2⟩ : GI) ≠ ⟨0, -2⟩ := by decide

theorem six_position_groups :
    (List.range 6).map (rep 6) = [0, 1, 2, 3, 2, 1] ∧
    Invariant 6 (fun j => (rep 6 j : Int)) ∧
    Separates 6 (fun j => (rep 6 j : Int)) [0, 1, 2, 3] := by
  refine ⟨by decide, rep_invariant 6, ?_⟩
  unfold Separates
  decide

theorem position_labels_break_reversal : ¬ Invariant 4 (fun j => (j : Int)) := by
  intro h
  have h1 := h 1 (by decide)
  change (3 : Int) = 1 at h1
  omega

theorem singleton_lookup :
    ResearchTwoTheorems.Institution.Knows [0]
      ResearchQmBridge.Instance.weightsQ ResearchQmBridge.Instance.readout := by decide

end Textbook.NumberLab
'''


def build_checks():
    local = {'ResearchTwoTheorems.Observer', 'ResearchTwoTheorems.Institution',
             'ResearchQmBridge.Residual', 'ResearchQmBridge.Gauss'}
    sealed = {'Derivation.Represented', 'Derivation.NoOutside', 'Derivation.Compression',
              'Derivation.PresentationRelativity', 'Derivation.CapacityBound'}
    imports = {'Derivation.WeightProfile'}
    texts = []
    for path in NATIVE_SOURCES:
        text = (ROOT/path).read_text(encoding='utf-8')
        for module in re.findall(r'^import (\S+)\s*$', text, re.M):
            if module in sealed:
                imports.add(module)
            elif module not in local:
                raise ValueError('New native import needs book review: '+module)
        texts.append(re.sub(r'^import \S+\s*\n', '', text, flags=re.M))
    contract = json.loads((ROOT/'research/qm_bridge/TREE_CONTRACT.json').read_text(encoding='utf-8'))
    names = [*contract['axiom_declarations'], *WEIGHT_REPORTS,
             *('Textbook.NumberLab.'+n for n in BOOK_NAMES)]
    source = '\n'.join([*('import '+m for m in sorted(imports)), *texts, BOOK_SOURCE,
                        *('#print axioms '+n for n in names)])
    return source, names


def expected_reports(names):
    values = json.loads((SOURCE/'expected_axioms.json').read_text(encoding='utf-8'))
    if set(values) != set(names) or any(set(v)-{'propext', 'Quot.sound'} for v in values.values()):
        raise ValueError('Number book report population or axiom boundary changed')
    return {n: 'depends on axioms: ['+', '.join(values[n])+']' if values[n]
            else 'does not depend on any axioms' for n in names}
