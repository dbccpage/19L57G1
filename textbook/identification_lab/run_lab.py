"""Selected identification-dual examples, recomputed read-only.

AuthorityEffect: None. Starting histories come from the research summary;
bounded searches and replies are recomputed, not treated as general theorems.
"""
import argparse
from collections import defaultdict
import hashlib
from itertools import product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from research.identification_dual import dual  # noqa: E402
from derivation import candidates, export, model, observe  # noqa: E402

BOUNDS = candidates.Bounds(2, 2)
PINS = ('research/identification_dual/dual.py',
        'research/identification_dual/STATUS.md',
        'research/identification_dual/CLAIM_LEDGER.md',
        'research/identification_dual/PROMPT.md',
        'research/identification_dual/PREDICTIONS.md',
        'research/identification_dual/receipts/identification_dual.json',
        'code/derivation/model.py', 'code/derivation/observe.py',
        'code/derivation/candidates.py', 'code/derivation/iso.py',
        'code/derivation/export.py', 'lean4/Derivation/Basic.lean',
        'lean4/Derivation/RuleBridge.lean')


def plain(value):
    return json.loads(json.dumps(value))


def table(regime):
    contexts = observe.contexts(regime)
    answers = [[observe.derivable(regime, observe.plug(c, d)) for c in contexts]
               for d in range(regime.n_data())]
    # Independent table: construct the slots and plug each hole directly.
    oracle_contexts = [(f, slots) for f, arity in enumerate(regime.forms)
                       for slots in product((None, *range(regime.n_data())), repeat=arity)
                       if None in slots]
    assert list(contexts) == oracle_contexts
    oracle = [[f in regime.rules or (f, tuple(d if s is None else s for s in slots)) in regime.insts
               for f, slots in oracle_contexts] for d in range(regime.n_data())]
    assert answers == oracle
    assert all(answers[i] == answers[j] if observe.profiles(regime)[i] == observe.profiles(regime)[j]
               else answers[i] != answers[j]
               for i in range(regime.n_data()) for j in range(regime.n_data()))
    return plain({'regime': export.regime_json(regime), 'contexts': contexts, 'answers': answers,
                  'collapsed_pairs': observe.collapsed_pairs(regime),
                  'classes': dual.class_count(regime)})


def independent_valid(state, target, delta):
    try:
        after = candidates.apply_delta(state.regime, delta)
    except model.AdmissionError:
        return False
    rows = table(after)['answers']
    assert state.mode == dual.IDENTIFY
    want_same, want_sep = state.same | {target}, state.regime.reqs
    return all(rows[i] == rows[j] for i, j in want_same) and all(rows[i] != rows[j] for i, j in want_sep)


def reply(state, target, delta):
    requested = dual.dual_step(state, dual.RequireSame(*target))
    assert requested.regime == state.regime
    child = dual.dual_replay(candidates.delta_events(state.regime, delta), requested)
    valid = dual.response_valid(state, target, delta)
    assert valid == independent_valid(state, target, delta)
    return {'delta': plain(export.delta_json(delta)), 'items': len(delta),
            'mu2': list(candidates.mu2(delta)), 'valid': valid,
            'within_two_item_bound': len(delta) <= 2,
            'after': table(child.regime),
            'same_requirements': plain(sorted(child.same)),
            'diagnostics': plain(dual.diagnostics(state.regime, target, delta))}


def all_candidates(state):
    result = []
    seen = set()
    for count in range(3):
        for delta in candidates.iter_full_deltas(state.regime, count, BOUNDS):
            if delta in seen or any(isinstance(x, candidates.NewRuleAll) and
                                    x.form in state.regime.rules for x in delta):
                continue
            seen.add(delta)
            result.append(delta)
    return result


def probe(state, target, measure, universe):
    source = dual.min_responses(state, target, measure, BOUNDS)
    valid = []
    counts = [0, 0, 0]
    for delta in universe:
        answer = dual.response_valid(state, target, delta)
        assert answer == independent_valid(state, target, delta)
        if answer:
            counts[len(delta)] += 1
            valid.append(delta)
    price = (lambda d: (len(d), -1)) if measure == 'mu1' else candidates.mu2
    least = min(map(price, valid), default=None)
    minima = [d for d in valid if price(d) == least]
    assert (None if source is None else source.cost) == least
    assert set(minima) == (set() if source is None else set(source.deltas))
    classes = defaultdict(list)
    responses = []
    for index, delta in enumerate(minima):
        child = dual.dual_replay((dual.RequireSame(*target),) + candidates.delta_events(state.regime, delta), state)
        classes[dual.state_key(child)].append(index)
        responses.append(reply(state, target, delta))
    without_rules = [d for d in valid if not any(isinstance(x, candidates.NewRuleAll) for x in d)]
    return {'target': list(target), 'measure': measure,
            'candidate_count': len(universe),
            'minimum': None if least is None else (least[0] if measure == 'mu1' else list(least)),
            'valid_by_item_count': counts,
            'classes': list(classes.values()), 'responses': responses,
            'minimum_without_rules': min((len(d) for d in without_rules), default=None)}


def source_states():
    summary = json.loads((ROOT / PINS[5]).read_text(encoding='utf-8'))
    selected = {}
    for g in summary['genesis']:
        if g['id'] not in ('g00', 'g05'):
            continue
        history = tuple(export.event_from_json(e) for e in g['history'])
        state = dual.dual_replay(history)
        assert plain(export.regime_json(state.regime)) == g['regime']
        assert not observe.collapsed_pairs(state.regime)
        selected[g['id']] = (g, history, state)
    assert set(selected) == {'g00', 'g05'}
    return selected


def build_packet():
    states = source_states()
    roots, probes = {}, {}
    for name, (g, history, kept) in states.items():
        released = dual.dual_step(kept, dual.Retract())
        assert released.regime == model.Regime(kept.regime.data, kept.regime.forms,
                                               kept.regime.insts, kept.regime.rules, frozenset())
        assert not released.same
        assert observe.profiles(kept.regime) == observe.profiles(released.regime)
        roots[name] = {'source_reading': g['reading'], 'history': g['history'],
                       'kept': table(kept.regime), 'released': table(released.regime)}
        for setting, state in [('keep', kept), ('release', released)]:
            universe = all_candidates(state)
            for target in dual.separated_pairs(state.regime):
                for measure in ('mu1', 'mu2'):
                    key = name + '_' + setting + '_' + ''.join(map(str, target)) + '_' + measure
                    probes[key] = probe(state, target, measure, universe)
    unary = dual.dual_step(states['g00'][2], dual.Retract())
    first_choices = {'focused': (candidates.NewInst(1, (1,)),),
                     'uniform': (candidates.NewRuleAll(1),)}
    paths = {}
    for name, delta in first_choices.items():
        child = dual.dual_replay((dual.RequireSame(0, 1),) + candidates.delta_events(unary.regime, delta), unary)
        next_probe = probe(child, (0, 2), 'mu1', all_candidates(child))
        paths[name] = {'first': reply(unary, (0, 1), delta), 'next': next_probe,
                       'least_total_items_along_this_choice': 1 + next_probe['minimum']}
    binary = states['g05'][2]
    larger_delta = (candidates.NewForm(1), candidates.NewRuleAll(0), candidates.NewInst(1, (2,)))
    larger = reply(binary, (0, 1), larger_delta)
    assert larger['valid'] and not larger['within_two_item_bound']
    assert probes['g00_release_01_mu1']['minimum'] == 1
    assert len(probes['g00_release_01_mu1']['classes']) == 2
    assert probes['g00_release_02_mu1']['minimum'] == 2
    assert probes['g05_keep_01_mu1']['minimum'] is None
    assert probes['g05_release_01_mu1']['minimum_without_rules'] is None
    assert paths['focused']['least_total_items_along_this_choice'] == 3
    assert paths['uniform']['least_total_items_along_this_choice'] == 2
    practice_history = tuple(model.AdmitDatum(x) for x in ('X', 'Y', 'Z')) + (
        model.AdmitForm(1), model.AdmitForm(1),
        model.AdmitInst(0, (0,)), model.AdmitInst(1, (1,)))
    practice = dual.dual_replay(practice_history)
    practice_probe = probe(practice, (0, 1), 'mu1', all_candidates(practice))
    assert practice_probe['minimum'] == 2 and len(practice_probe['responses']) == 4
    promised_practice = dual.dual_replay((model.Impose(0, 2), model.Impose(1, 2)), practice)
    promised_probe = probe(promised_practice, (0, 1), 'mu1', all_candidates(promised_practice))
    assert promised_probe['minimum'] == 2 and len(promised_probe['responses']) == 3
    return {'authority_effect': 'None',
            'source_text_sha256': {p: hashlib.sha256((ROOT / p).read_text(encoding='utf-8').encode()).hexdigest()
                                   for p in PINS},
            'digest_mode': 'UTF-8 text with LF normalization',
            'scope': 'Two replayed source starting states; selected bounded probes, not the full research campaign',
            'roots': roots, 'probes': probes, 'paths': paths, 'larger_reply': larger,
            'practice': {'classification': 'Supplied book example, not a research campaign state',
                         'history': [export.event_json(e) for e in practice_history],
                         'before': table(practice.regime), 'probe': practice_probe,
                         'promised_probe': promised_probe},
            'populations': {'Replayed starting states': 2, 'Root pair/setting/measure probes': 24,
                            'Selected continuation branches': 2, 'Outside-bound replies': 1,
                            'Changed-table practice probes': 2}}


def check_recorded(directory=SOURCE):
    packet = plain(build_packet())
    if json.loads((directory / 'recorded_lab.json').read_text(encoding='utf-8')) != packet:
        raise ValueError('Identification lesson differs from recomputed source-backed cases')
    import re
    rows = re.findall(r'^\| ([^|]+) \| (\d+) \|$', (directory / 'SOURCE_MAP.md').read_text(encoding='utf-8'), re.M)
    if len(rows) != len(packet['populations']) or {k: int(v) for k, v in rows} != packet['populations']:
        raise ValueError('Identification lesson population table differs')
    from textbook.identification_lab.figures import render_figures
    for name, svg in render_figures(packet).items():
        if (directory / 'figures' / name).read_text(encoding='utf-8') != svg:
            raise ValueError('Identification lesson figure differs: ' + name)
    return packet['populations']


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    if args.write:
        packet = plain(build_packet())
        (SOURCE / 'recorded_lab.json').write_text(json.dumps(packet, indent=1, sort_keys=True)+'\n', encoding='utf-8', newline='\n')
        from textbook.identification_lab.figures import render_figures
        (SOURCE / 'figures').mkdir(exist_ok=True)
        for name, svg in render_figures(packet).items():
            (SOURCE / 'figures' / name).write_text(svg, encoding='utf-8', newline='\n')
    print(check_recorded())
