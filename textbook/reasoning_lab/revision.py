"""Read-only X302 teaching checks; AuthorityEffect: None."""
from copy import deepcopy
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from research.x302_operational_reasoning import reasoning as n  # noqa: E402

OWNER = ROOT / 'research/x302_operational_reasoning'
MP = n.JustificationKind.MODUS_PONENS
CONJ = n.JustificationKind.CONJUNCTION_INTRO


def verify_sources():
    expected = json.loads(Path(__file__).with_name('revision_sources.json').read_text(encoding='utf-8'))
    actual = {name: hashlib.sha256((OWNER / name).read_text(encoding='utf-8').encode()).hexdigest()
              for name in expected}
    assert actual == expected, 'Review changed X302 sources before updating the book pins'
    assert Path(n.__file__).resolve() == OWNER / 'reasoning.py'
    return actual


def chain(costs=(1, 1), extra=False, conflict_on_last=False):
    t = n.OperationalTMS()
    p, q, r = (n.Atom(name) for name in ('P', 'Q', 'R'))
    ids = {'rule1': t.add_axiom('rule1', n.Implies(p, q)),
           'rule2': t.add_axiom('rule2', n.Implies(q, r)),
           'a': t.add_hypothesis('a', p, costs[0])}
    ids['q'] = t.apply_inference(q, MP, (ids['rule1'], ids['a']))
    ids['r'] = t.apply_inference(r, MP, (ids['rule2'], ids['q']))
    ids['b'] = t.add_hypothesis('b', n.Not(r if conflict_on_last else q), costs[1])
    if extra:
        ids['c'] = t.add_hypothesis('c', q)
        ids['r2'] = t.apply_inference(r, MP, (ids['rule2'], ids['c']))
    return t, ids


def subsets(items):
    return [frozenset(c) for size in range(len(items) + 1)
            for c in combinations(items, size)]


def expected_candidates(family, weights):
    # Independent finite oracle: inspect all eight subsets, then compare scores.
    valid = [s for s in subsets(tuple(weights)) if all(s & c for c in family)]
    score = lambda s: (len(s), sum(weights[h] for h in s))
    best = min(map(score, valid))
    return sorted((s for s in valid if score(s) == best), key=lambda s: tuple(sorted(s)))


def family_notebook(family, weights):
    """Realize conflict supports using only public premise/inference operations."""
    t = n.OperationalTMS()
    atoms = {h: n.Atom(h) for h in weights}
    ids = {h: t.add_hypothesis(h, atoms[h], weights[h]) for h in weights}
    for index, support in enumerate(family):
        names = sorted(support)
        formula, node = atoms[names[0]], ids[names[0]]
        for h in names[1:]:
            formula = n.And(formula, atoms[h])
            node = t.apply_inference(formula, CONJ, (node, ids[h]))
        t.add_axiom('conflict' + str(index), n.Not(formula))
    assert set(t.detect_contradictions()) == set(family)
    return t


def check_examples():
    verify_sources()
    # Lessons and changed practice use the same declared inference grammar.
    for final in (False, True):
        t, ids = chain(conflict_on_last=final)
        assert t.get_node(ids['rule1']).support == t.get_node(ids['rule2']).support == frozenset()
        assert t.get_node(ids['q']).support == t.get_node(ids['r']).support == frozenset({'a'})
        assert t.detect_contradictions() == (frozenset({'a', 'b'}),)
        assert t.compute_minimal_retractions() == [frozenset({'a'}), frozenset({'b'})]
        chosen = deepcopy(t).revise()
        assert chosen.retracted_hypotheses == frozenset({'a'})
        rec = t.revise(frozenset({'a'}))
        assert set(rec.deactivated_nodes) == {ids[h] for h in ('a', 'q', 'r')}
        assert all(t.get_node(ids[h]).is_active for h in ('rule1', 'rule2', 'b'))
        assert all(t.get_node(nid).formula not in (n.Not(n.Atom('P')), n.Not(n.Atom('Q')))
                   for nid in rec.surviving_beliefs if nid != ids['b'])
        assert not t.detect_contradictions()

        t, ids = chain(costs=(4, 1), conflict_on_last=final)
        assert t.compute_minimal_retractions() == [frozenset({'b'})]
        assert t.revise().retracted_hypotheses == frozenset({'b'})
        assert all(t.get_node(ids[h]).is_active for h in ('a', 'q', 'r'))

        t, ids = chain(extra=True, conflict_on_last=final)
        assert set(t.detect_contradictions()) == {frozenset({'a', 'b'}), frozenset({'b', 'c'})}
        assert t.compute_minimal_retractions() == [frozenset({'b'})]
        try:
            t.revise(frozenset({'a'}))
        except ValueError:
            pass
        else:
            raise AssertionError('Non-hitting withdrawal unexpectedly accepted')
        rec = t.revise(frozenset({'a', 'b'}))
        assert not t.get_node(ids['q']).is_active
        assert t.get_node(ids['c']).is_active and t.get_node(ids['r2']).is_active
        assert not t.detect_contradictions()

    # The scan is not an inference-closure algorithm.
    t = n.OperationalTMS()
    p, q = n.Atom('P'), n.Atom('Q')
    rule = t.add_axiom('rule', n.Implies(p, q))
    a = t.add_hypothesis('a', p)
    t.add_hypothesis('b', n.Not(q))
    assert t.detect_contradictions() == ()
    t.apply_inference(q, MP, (rule, a))
    assert t.detect_contradictions() == (frozenset({'a', 'b'}),)

    t = n.OperationalTMS()
    t.add_axiom('q', q)
    try:
        t.add_axiom('not_q', n.Not(q))
    except n.FoundationalInconsistencyError:
        pass
    else:
        raise AssertionError('Fixed-only conflict unexpectedly accepted')
    # The error is not a rollback contract: discard this failed example instance.

    # A consistent recorded assertion can disagree with a supplied comparison.
    t = n.OperationalTMS()
    t.add_hypothesis('blue', n.Atom('blue'))
    comparison = {'blue': False}
    assert not t.detect_contradictions() and not comparison['blue']
    return {'lesson_notebooks': 2, 'computational_practice_questions': 9,
            'false_inference_closure_claim_rejected': True,
            'fixed_conflict_error_checked': True, 'consistency_is_not_truth': True}


def check_population():
    verify_sources()
    supports = subsets(('a', 'b', 'c'))[1:]
    counts = {'conflict_families': 0, 'weighted_notebooks': 0, 'tied_candidate_replays': 0}
    for family in subsets(tuple(supports)):
        family = sorted(family, key=lambda c: (len(c), tuple(sorted(c))))
        counts['conflict_families'] += 1
        for values in product((1, 2, 3), repeat=3):
            weights = dict(zip(('a', 'b', 'c'), values))
            t = family_notebook(family, weights)
            expected = expected_candidates(family, weights)
            assert t.compute_minimal_retractions() == expected
            default = deepcopy(t).revise()
            assert default.retracted_hypotheses == expected[0]
            for choice in expected:
                trial = deepcopy(t)
                before = dict(trial.nodes)
                receipt = trial.revise(choice)
                expected_off = {nid for nid, node in before.items() if node.support & choice}
                assert set(receipt.deactivated_nodes) == expected_off
                assert set(receipt.surviving_beliefs) == set(before) - expected_off
                assert not trial.detect_contradictions()
                assert all(trial.get_node(nid).is_active for nid, node in before.items()
                           if node.commitment == n.CommitmentClass.AXIOM)
                counts['tied_candidate_replays'] += 1
            counts['weighted_notebooks'] += 1
    assert counts['conflict_families'] == 128 and counts['weighted_notebooks'] == 3456
    # Cardinality precedes weight, including the changed high-cost example.
    family = [frozenset({'a', 'b'}), frozenset({'a', 'c'})]
    t = family_notebook(family, {'a': 9, 'b': 1, 'c': 1})
    assert t.compute_minimal_retractions() == [frozenset({'a'})]
    return counts


if __name__ == '__main__':
    print(json.dumps({'examples': check_examples(), 'population': check_population()}, sort_keys=True))
