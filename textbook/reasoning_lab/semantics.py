"""Read-only X301 controls in an isolated interpreter; AuthorityEffect: None."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OWNER = ROOT / 'research/x301_formal_semantics'


def check_examples():
    # Native modules use bare imports named model and valuation. A separate
    # isolated process avoids replacing any modules used by other book routes.
    result = subprocess.run([sys.executable, '-I', str(Path(__file__).resolve()), '--worker'],
                            cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        raise RuntimeError('Isolated X301 control failed:\n' + result.stderr)
    return json.loads(result.stdout)


def worker():
    from dataclasses import replace
    from fractions import Fraction
    import hashlib
    from itertools import combinations, product

    sys.path.insert(0, str(OWNER))
    import formulas as f
    import intervention as i
    import model as m
    import panel as p
    import valuation as v

    modules = (f, i, m, p, v)
    for module in modules:
        assert Path(module.__file__).resolve().parent == OWNER
    source_hashes = {Path(module.__file__).name:
                     hashlib.sha256(Path(module.__file__).read_text(encoding='utf-8').encode()).hexdigest()
                     for module in modules}
    lean = OWNER / 'lean/FormalSemantics.lean'
    source_hashes['lean/FormalSemantics.lean'] = hashlib.sha256(lean.read_text(encoding='utf-8').encode()).hexdigest()
    expected_hashes = json.loads((Path(__file__).parent / 'semantics_sources.json').read_text(encoding='utf-8'))
    assert source_hashes == expected_hashes, 'Review changed native source text before updating the book pin'
    base = m.RelationalModel(data=('A', 'B', 'C'), forms=(1, 1),
                             insts=frozenset({(0, (0,)), (0, (1,)), (1, (1,)), (1, (2,))}))
    blue, triangle = f.atom('form_0', 'x'), f.atom('form_1', 'x')
    value = lambda state, formula, x=0: m.evaluate(state, formula, {'x': x})
    assert [value(base, blue, x) for x in range(3)] == [1, 1, 0]
    assert [value(base, triangle, x) for x in range(3)] == [0, 1, 1]
    all_blue, some_blue = f.forall('x', 'selected', blue), f.exists('x', 'selected', blue)
    table = []
    for domain in ((0, 1), (0, 1, 2), (2,), ()):
        state = replace(base, custom_domains={'selected': domain})
        table.append([str(value(state, all_blue)), str(value(state, some_blue))])
    assert table == [['1', '1'], ['0', '1'], ['0', '0'], ['1', '0']]
    # A typo is computationally empty, not a validation error in the native API.
    assert value(base, f.forall('x', 'misspelled', blue)) == 1
    assert value(base, f.exists('x', 'misspelled', blue)) == 0
    assert not v.HALF.is_true and not v.HALF.is_false and not bool(v.HALF)
    assert v.pseudo_complement(v.HALF) == 0
    assert v.join(v.HALF, v.pseudo_complement(v.HALF)) == Fraction(1, 2)

    identity = i.Intervention('keep', lambda state: state)
    remove_a = i.remove_instance_intervention(0, (0,))
    remove_b = i.remove_instance_intervention(0, (1,))
    remove_c = i.remove_instance_intervention(0, (2,))
    add_a = i.add_instance_intervention(0, (0,))
    assert not i.has_empirical_reference(blue, base, [identity], {'x': 0})
    assert i.find_discriminating_witness(blue, base, [identity, remove_a], {'x': 0}) is remove_a
    absent = remove_a.apply(base)
    # Independent candidates from the original differ from ordered execution.
    assert [value(interv.apply(absent), blue) for interv in (add_a, remove_a)] == [1, 0]
    assert value(remove_a.apply(add_a.apply(absent)), blue) == 0

    honest = p.Panel([p.Observer(str(n), lambda state: state) for n in range(3)])
    altered = p.Panel([p.Observer(str(n), add_a.apply) for n in range(3)])
    assert altered.has_positive_consensus(absent, blue, {'x': 0}) and value(absent, blue) == 0
    assert p.Panel([p.Observer('same', add_a.apply)] * 3).has_positive_consensus(absent, blue, {'x': 0})
    proposed = replace(base, data=base.data + ('D',))
    direct = p.evaluate_with_grounding_firewall(absent, blue, altered, [], proposed_mutation=proposed, assignment={'x': 0})
    changed = p.evaluate_with_grounding_firewall(base, blue, honest, [remove_a], proposed_mutation=proposed, assignment={'x': 0})
    for result, starting in ((direct, absent), (changed, base)):
        assert result.is_refusal and result.state is starting and result.receipt.verify_checksum()
    assert changed.receipt.observable_readout_before == '1' and changed.receipt.observable_readout_after == '0'
    fallback = p.evaluate_with_grounding_firewall(absent, blue, altered, [add_a], assignment={'x': 0})
    assert fallback.is_refusal and fallback.receipt.refuting_intervention == add_a.name
    assert fallback.receipt.observable_readout_after == '0' and value(add_a.apply(absent), blue) == 1
    accepted = p.evaluate_with_grounding_firewall(base, blue, honest, [], proposed_mutation=proposed, assignment={'x': 0})
    assert not accepted.is_refusal and accepted.state is proposed
    no_panel = p.evaluate_with_grounding_firewall(absent, blue, honest, [], assignment={'x': 0})
    assert no_panel.is_refusal and no_panel.receipt is None

    # A disposable shared dictionary exposes the callback limit. This is not
    # an operation on a research file or on any previously admitted state.
    shared = {'flag': frozenset({(0,)})}
    mutable_state = m.RelationalModel(data=('A',), custom_relations=shared)
    flag = f.atom('flag', '0')
    def mutate_dictionary(state):
        shared['flag'] = frozenset()
        return state
    dirty = p.evaluate_with_grounding_firewall(mutable_state, flag, honest,
                [i.Intervention('shared dictionary contrast', mutate_dictionary)])
    assert dirty.is_refusal and dirty.state is mutable_state and not shared['flag']

    # Hash consistency does not check factual assertions. Fix the timestamp
    # only for this supplied receipt; the native guard retains its own clock.
    receipt = p.PanelIllusionReceipt.create(formula_repr='supplied claim', panel_size=3,
        observer_ids=('0', '1', '2'), refuting_intervention='supplied change',
        observable_readout_before='1', observable_readout_after='0', timestamp='book-example')
    edited = replace(receipt, ground_truth_verdict=True)
    assert receipt.verify_checksum() and not edited.verify_checksum()
    assert replace(edited, receipt_sha256=edited.compute_sha256()).verify_checksum()

    # Changed practice questions 1-7, independent of the main example's member.
    assert [value(base, triangle, x) for x in (0, 1)] == [0, 1]
    subset = replace(base, custom_domains={'selected': (1, 2)})
    assert value(subset, f.forall('x', 'selected', triangle)) == value(subset, some_blue) == 1
    third = v.RationalValuation(Fraction(1, 3))
    assert v.pseudo_complement(third) == 0 and v.join(third, v.pseudo_complement(third)) == third
    assert not i.has_empirical_reference(blue, base, [remove_c], {'x': 1})
    assert i.has_empirical_reference(blue, base, [remove_c, remove_b], {'x': 1})
    cpanel = p.Panel([p.Observer(str(n), i.add_instance_intervention(0, (2,)).apply) for n in range(3)])
    assert cpanel.has_positive_consensus(base, blue, {'x': 2}) and value(base, blue, 2) == 0
    bresult = p.evaluate_with_grounding_firewall(base, blue, honest, [remove_b], assignment={'x': 1})
    assert bresult.is_refusal and value(base, blue, 1) == 1

    subsets = [tuple(c) for size in range(4) for c in combinations(range(3), size)]
    atom_checks = domain_checks = guard_checks = 0
    for blue_members in subsets:
        state = replace(base, insts=frozenset({(0, (x,)) for x in blue_members} | {(1, (1,)), (1, (2,))}))
        for x in range(3):
            assert value(state, blue, x) == int(x in blue_members)
            atom_checks += 1
            for menu in ([], [identity], [i.remove_instance_intervention(0, (x,))],
                         [i.add_instance_intervention(0, (x,))]):
                result = p.evaluate_with_grounding_firewall(state, blue, honest, menu, assignment={'x': x})
                expected_refusal = x not in blue_members or any(value(interv.apply(state), blue, x) != 1 for interv in menu)
                assert result.is_refusal == expected_refusal and result.state is state
                guard_checks += 1
        for domain in subsets:
            scoped = replace(state, custom_domains={'selected': domain})
            assert value(scoped, all_blue) == int(all(x in blue_members for x in domain))
            assert value(scoped, some_blue) == int(any(x in blue_members for x in domain))
            domain_checks += 1
    pairs = 0
    for a, b in product((Fraction(n, 4) for n in range(5)), repeat=2):
        av, bv = v.RationalValuation(a), v.RationalValuation(b)
        assert v.meet(av, bv) == min(a, b) and v.join(av, bv) == max(a, b)
        assert v.implies(av, bv) == (1 if a <= b else b)
        pairs += 1
    return dict(owner_utf8_lf_sha256=source_hashes, atom_assignments=atom_checks,
                domain_pairs=domain_checks, guard_contexts=guard_checks, score_pairs=pairs,
                changed_tasks_checked=7, physical_observations=0, learner_scores=0)


if __name__ == '__main__':
    print(json.dumps(worker() if sys.argv[1:] == ['--worker'] else check_examples(), sort_keys=True))
