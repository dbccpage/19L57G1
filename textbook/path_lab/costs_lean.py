"""Re-elaborate exact native cost bodies plus book claims; AuthorityEffect: None."""
import json
import re
from .costs import ROOT, LEAN_SOURCES

REPORTS=tuple('ResearchNativeStructure.'+name for name in (
    'swap_sound','parallel_not_cell','boundary_boundary','boundary_zero_iff_commutes',
    'pathCost_append','exact_pathCost','exact_closed','closed_swap_cost',
    'closed_cell_cost','not_exact_of_cycle','budgetDelta_exact','writes_not_exact',
    'writes_closed','writes_closed_not_exact'))
BOOK_NAMES=tuple('Textbook.PathCosts.'+name for name in (
    'budget_loop','duplicate_write','halt_changes_square','shift_potential',
    'three_point_potential','cannot_erase_loop'))
BOOK=r'''
namespace Textbook.PathCosts
open PrimitivePassage ResearchNativeStructure TransitionAlphabet

theorem budget_loop :
    replayP [.setBudget 1, .setBudget 0] genesisP = genesisP ∧
    pathCost budgetDelta genesisP [.setBudget 1, .setBudget 0] = 0 ∧
    pathCost writes genesisP [.setBudget 1, .setBudget 0] = 2 := by decide

theorem duplicate_write :
    pathCost budgetDelta genesisP [.setBudget 1, .setBudget 1] = 1 ∧
    pathCost writes genesisP [.setBudget 1, .setBudget 1] = 1 := by decide

theorem halt_changes_square :
    step (step genesisP .halt) (.setLicense false) ≠
      step (step genesisP (.setLicense false)) .halt ∧
    step (step (haltS genesisP) .halt) (.setLicense false) =
      step (step (haltS genesisP) (.setLicense false)) .halt := by decide

theorem shift_potential (phi : PState → Int) (k : Int) (s : PState) (e : PEvent) :
    dEdge (fun t => phi t + k) s e = dEdge phi s e := by
  simp only [dEdge]
  omega

theorem three_point_potential (a b c : Int) :
    (∃ x y : Int, x - 0 = a ∧ y - x = b ∧ y - 0 = c) ↔ a + b = c := by
  constructor
  · rintro ⟨x,y,hx,hxy,hy⟩
    omega
  · intro h
    exact ⟨a,c,by omega,by omega,by omega⟩

theorem cannot_erase_loop : ¬ Cell genesisP [.setBudget 1,.setBudget 0] [] := by
  intro h
  have hl := (cell_perm h).length_eq
  simp at hl

end Textbook.PathCosts
'''


def build_cost_checks():
    texts=[]
    for path in LEAN_SOURCES:
        text=(ROOT/path).read_text(encoding='utf-8')
        imports=re.findall(r'^import (\S+)\s*$',text,re.M)
        allowed={'Derivation.TraceAlgebra','ResearchNativeStructure.Cells',
                 'ResearchNativeStructure.Boundary'}
        if set(imports)-allowed:
            raise ValueError('Native cost import needs review: '+str(imports))
        texts.append(re.sub(r'^import \S+\s*\n','',text,flags=re.M))
    names=(*REPORTS,*BOOK_NAMES)
    return '\n'.join([*texts,BOOK,*('#print axioms '+n for n in names)]),names


def expected_cost_reports():
    data=json.loads((ROOT/'textbook/path_lab/costs_axioms.json').read_text(encoding='utf-8'))
    if set(data)!=set((*REPORTS,*BOOK_NAMES)) or any(set(v)-{'propext','Quot.sound'} for v in data.values()):
        raise ValueError('Cost report population or axiom boundary changed')
    return {n:'depends on axioms: ['+', '.join(v)+']' if v else 'does not depend on any axioms'
            for n,v in data.items()}
