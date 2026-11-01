"""Selected X301 owner reports; no Python refinement claim."""
import re
from .semantics import OWNER

SUFFIXES = '''constructive_lem_fails satisfaction_compositional_conj
satisfaction_compositional_neg satisfaction_modus_ponens
empty_intervention_cannot_discriminate panel_agreement_not_truth
grounding_firewall_refuses_panel_illusion refusal_preserves_state'''.split()
NAMES = tuple('X301FormalSemantics.' + n for n in SUFFIXES)


def build_checks():
    text = (OWNER / 'lean/FormalSemantics.lean').read_text(encoding='utf-8')
    if re.search(r'^import ', text, re.M):
        raise ValueError('Review changed X301 imports before assembly')
    return text + '\n' + '\n'.join('#print axioms ' + n for n in NAMES), NAMES


def expected_reports():
    return {name: ('depends on axioms: [propext, Quot.sound]' if name.rsplit('.', 1)[1] in
                   {'grounding_firewall_refuses_panel_illusion', 'refusal_preserves_state'}
                  else 'does not depend on any axioms') for name in NAMES}
