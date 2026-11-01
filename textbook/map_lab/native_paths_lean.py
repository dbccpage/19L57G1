"""Re-elaborate exact owner bodies plus book exhibits; AuthorityEffect: None."""
import json
import re
from .native_paths import ROOT, LEAN_SOURCES

REPORTS = tuple('ResearchNativeBridge.'+name for name in (
    'Path.run_events', 'Path.events_injective', 'Path.events_append',
    'Sim.run_trHist', 'Sim.trHist_append', 'toggle_encoding', 'passage_sim_cycle',
    'nobs_of_core', 'ObsSim.obs_const_on_cycle', 'budgetSim_nobs',
    'toggle_no_faithful_obs', 'idObsSim_faithful', 'realize_iff', 'realize_events',
    'unrealized_step', 'halted_path'))

BOOK = r'''
namespace Textbook.NativePaths
open ResearchNativeBridge PrimitivePassage

theorem two_flips :
    run toggle [(), ()] false = false ∧
    (run step (toggleSim.trHist false [(), ()]) (toggleSim.enc false)).budget = 0 := by
  decide

theorem repeat_keeps_endpoint :
    replayP [.admitOcc 0] genesisP = replayP [.admitOcc 0, .admitOcc 0] genesisP := by
  decide

theorem repeat_changes_events :
    ([PEvent.admitOcc 0] : List PEvent) ≠ [.admitOcc 0, .admitOcc 0] := by
  decide

theorem native_reading_cannot_recover_switch :
    ¬ ∃ decode : NObs → Bool, ∀ b, decode (nobs (toggleSim.enc b)) = b := by
  intro ⟨decode, h⟩
  have hf := h false
  have ht := h true
  change decode (nobs genesisP) = false at hf
  change decode (nobs genesisP) = true at ht
  exact Bool.false_ne_true (hf.symm.trans ht)

end Textbook.NativePaths
'''
BOOK_NAMES = tuple('Textbook.NativePaths.'+name for name in (
    'two_flips', 'repeat_keeps_endpoint', 'repeat_changes_events',
    'native_reading_cannot_recover_switch'))


def build_native_checks():
    allowed = {'Trace', 'ResearchNativeBridge.Path', 'ResearchNativeBridge.Passage',
               'ResearchNativeBridge.Sim'}
    texts = []
    for path in LEAN_SOURCES:
        text = (ROOT/path).read_text(encoding='utf-8')
        for module in re.findall(r'^import (\S+)\s*$', text, re.M):
            if module != 'Derivation.TraceAlgebra' and module not in allowed:
                raise ValueError('Native-path import needs review: '+module)
        texts.append(re.sub(r'^import \S+\s*\n', '', text, flags=re.M))
    names = (*REPORTS, *BOOK_NAMES)
    return '\n'.join([*texts, BOOK, *('#print axioms '+n for n in names)]), names


def expected_native_reports():
    path = ROOT/'textbook/map_lab/native_paths_axioms.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    if set(data) != set((*REPORTS, *BOOK_NAMES)) or any(
            set(value)-{'propext', 'Quot.sound'} for value in data.values()):
        raise ValueError('Native-path report population or axiom boundary changed')
    return {name: 'depends on axioms: ['+', '.join(value)+']' if value
            else 'does not depend on any axioms' for name, value in data.items()}
