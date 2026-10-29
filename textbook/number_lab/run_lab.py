"""Recompute numerical teaching cases from read-only owners; AuthorityEffect: None."""
import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'code'))
from derivation import weight_profile as wp  # noqa: E402
from research.qm_bridge import model as bridge  # noqa: E402

NATIVE_SOURCES = (
    'research/two_theorems/lean/ResearchTwoTheorems/Observer.lean',
    'research/two_theorems/lean/ResearchTwoTheorems/Institution.lean',
    'research/qm_bridge/lean/ResearchQmBridge/Residual.lean',
    'research/qm_bridge/lean/ResearchQmBridge/Gauss.lean',
    'research/qm_bridge/lean/ResearchQmBridge/Multiplicity.lean',
    'research/qm_bridge/lean/ResearchQmBridge/Instance.lean')
PINS = ('code/derivation/weight_profile.py', 'lean4/Derivation/WeightProfile.lean',
        'research/qm_bridge/model.py', 'research/qm_bridge/input.json',
        'research/qm_bridge/README.md', 'research/qm_bridge/CLAIMS.md',
        'research/qm_bridge/TREE_CONTRACT.json', *NATIVE_SOURCES)


def count_table(values):
    return dict(enumerate(values))


def same(values, other):
    return wp.same_profile((0, 1), count_table(values), count_table(other))


def coordinate_case(a, b):
    p = (bridge.GI(*a), bridge.GI(*b))
    expected_weights = [sum(x*x for x in a), sum(x*x for x in b)]
    summed = [a[0]+b[0], a[1]+b[1]]
    expected_readout = sum(x*x for x in summed)
    expected_cross = a[0]*b[0]+a[1]*b[1]
    assert list(bridge.weights(p)) == expected_weights
    assert bridge.mix(p) == expected_readout
    assert bridge.cross(*p) == expected_cross
    assert expected_readout == sum(expected_weights)+2*expected_cross
    return {'inputs': [list(a), list(b)], 'weights': expected_weights, 'sum': summed,
            'readout': expected_readout, 'cross': expected_cross}


def groups(order):
    classes = sorted({tuple(sorted({j, (-j) % order})) for j in range(order)})
    assert bridge.orbits(order) == len(classes) == order//2+1
    readings = [min(j, order-j) for j in range(order)]
    assert all(readings[j] == readings[(-j) % order] for j in range(order))
    assert len(set(readings)) == len(classes)
    return {'order': order, 'groups': [list(c) for c in classes],
            'group_label_readings': readings, 'maximum_distinct': len(classes)}


def lookup_case(carrier, weights, readouts):
    questions = [lambda i: weights[i][0], lambda i: weights[i][1]]
    q = lambda i: readouts[i]
    witnesses = [[i, j] for i in carrier for j in carrier if i < j
                 and weights[i] == weights[j] and readouts[i] != readouts[j]]
    count_before = len({tuple(weights[i]) for i in carrier})
    count_after = len({(*weights[i], readouts[i]) for i in carrier})
    assert bridge.challenge(carrier, questions, q) == bool(witnesses)
    assert bridge.knows(carrier, questions, q) == (not witnesses)
    assert bridge.class_count(carrier, questions) == count_before
    assert bridge.class_count(carrier, [*questions, q]) == count_after
    assert bool(witnesses) == (count_after > count_before)
    return {'carrier': carrier, 'witnesses': witnesses, 'knows': not witnesses,
            'information_before': count_before, 'information_after': count_after}


def build_packet():
    tables = list(product(range(4), repeat=2))
    proportion_cases = []
    for a, b in product(tables, tables):
        expected = all(a[i]*sum(b) == b[i]*sum(a) for i in range(2))
        assert same(a, b) == expected
        fractions = None
        if sum(a) and sum(b):
            fractions = all(Fraction(a[i], sum(a)) == Fraction(b[i], sum(b)) for i in range(2))
            assert expected == fractions
        proportion_cases.append({'a': list(a), 'b': list(b), 'raw_match': expected,
                                 'positive_share_match': fractions})
    assert same((2, 3), (4, 6)) and not same((2, 3), (6, 4))
    assert same((2, 3), (0, 0)) and same((0, 0), (3, 2)) and not same((2, 3), (3, 2))
    assert wp.total((0, 0, 1), {0: 2, 1: 3}) == 7
    assert not wp.carrier_list((0, 0, 1))
    bounded_descent = {'coefficients': [1, 1], 'zero_box': wp.descends(1, 1, 0),
                       'one_box': wp.descends(1, 1, 1)}
    assert bounded_descent['zero_box'] and not bounded_descent['one_box']
    signed = []
    for a, b in product(range(-3, 4), repeat=2):
        readout = wp.mix_sum((0, 1), {0: a, 1: b})
        assert readout == (a+b)*(a+b)
        assert wp.read_out(1, 1, a, b) == a+b
        signed.append({'inputs': [a, b], 'weights': [a*a, b*b], 'readout': readout})
    spec = bridge.load()
    box = spec['polarization_box']
    values = list(product(range(-box, box+1), repeat=2))
    buckets = defaultdict(list)
    for a, b in product(values, values):
        row = coordinate_case(a, b)
        buckets[tuple(row['weights'])].append(row)
    comparisons = 0
    for rows in buckets.values():
        for a, b in product(rows, rows):
            assert (a['readout'] != b['readout']) == (a['cross'] != b['cross'])
            comparisons += 1
    carrier, preps = bridge.instance()
    instance = [coordinate_case((preps[i][0].re, preps[i][0].im),
                                (preps[i][1].re, preps[i][1].im)) for i in carrier]
    assert carrier == [0, 1, 2]
    assert [r['readout'] for r in instance] == [4, 2, 0]
    weights = [r['weights'] for r in instance]
    readouts = [r['readout'] for r in instance]
    domain_cases = [lookup_case([i for i in carrier if mask & (1 << i)], weights, readouts)
                    for mask in range(8)]
    assert bridge.instance_report() == dict(information_weights=1, information_with_readout=3,
                                            knows=False, challenge=True, readouts=readouts)
    generic_witness_tables = 0
    for flat in product(range(2), repeat=9):
        ws = [list(flat[3*i:3*i+2]) for i in range(3)]
        qs = [flat[3*i+2] for i in range(3)]
        generic_witness_tables += not lookup_case(carrier, ws, qs)['knows']
    loops = [groups(n) for n in range(1, spec['max_order']+1)]
    least = []
    for k in range(2, spec['max_multiplicity']+1):
        actual = bridge.least_order(k, spec['max_order'])
        expected = next((r['order'] for r in loops if r['maximum_distinct'] >= k), None)
        assert actual == expected == 2*k-2
        least.append({'distinct_readings': k, 'least_order_within_bound': actual})
    assert bridge.mu4_readouts() == [4, 2, 0, 2]
    practice = [coordinate_case((2, 0), b) for b in ((2, 0), (0, 2), (-2, 0), (0, -2))]
    assert [r['readout'] for r in practice] == [16, 8, 0, 8]
    count_examples = []
    for a, b in [((2, 3), (4, 6)), ((2, 3), (6, 4)),
                 ((3, 1), (6, 2)), ((3, 1), (3, 2))]:
        products = [[a[i]*sum(b), b[i]*sum(a)] for i in range(2)]
        assert same(a, b) == all(x == y for x, y in products)
        count_examples.append({'a': list(a), 'b': list(b), 'totals': [sum(a), sum(b)],
                               'cross_products': products, 'raw_match': same(a, b)})
    return {'authority_effect': 'None',
            'source_text_sha256': {p: hashlib.sha256((ROOT/p).read_text(encoding='utf-8').encode()).hexdigest() for p in PINS},
            'digest_mode': 'UTF-8 text with LF normalization',
            'bounds': {'count_entry_maximum': 3, 'signed_absolute_bound': 3,
                       'coordinate_absolute_bound': box, 'maximum_order': spec['max_order']},
            'proportion_cases': proportion_cases, 'signed_cases': signed,
            'shares_example': {'before': count_examples[0]['a'], 'after': count_examples[0]['b'],
                               'totals': count_examples[0]['totals'],
                               'cross_products': count_examples[0]['cross_products']},
            'zero_chain': [[2, 3], [0, 0], [3, 2]],
            'bounded_descent': bounded_descent,
            'coordinate_instance': instance, 'domain_cases': domain_cases,
            'generic_witness_tables': generic_witness_tables,
            'loops': loops, 'least_orders': least, 'mu4_readouts': bridge.mu4_readouts(),
            'practice_coordinates': practice,
            'selected_count_examples': count_examples,
            'populations': {'Count-table comparisons': len(proportion_cases),
                            'Positive-total share comparisons': 225,
                            'Signed input pairs': len(signed),
                            'Coordinate input pairs': len(values)**2,
                            'Weight-equal preparation comparisons': comparisons,
                            'Source-instance carrier subsets': len(domain_cases),
                            'Binary presentation tables': 512,
                            'Positive loop orders': len(loops),
                            'Least-order probes': len(least)}}


def check_recorded(directory=SOURCE):
    packet = build_packet()
    if json.loads((directory/'recorded_lab.json').read_text(encoding='utf-8')) != packet:
        raise ValueError('Number lesson differs from recomputed source-backed cases')
    rows = re.findall(r'^\| ([^|]+) \| (\d+) \|$', (directory/'SOURCE_MAP.md').read_text(encoding='utf-8'), re.M)
    if len(rows) != len(packet['populations']) or {k: int(v) for k, v in rows} != packet['populations']:
        raise ValueError('Number lesson population table differs')
    from textbook.number_lab.figures import render_figures
    for name, svg in render_figures(packet).items():
        if (directory/'figures'/name).read_text(encoding='utf-8') != svg:
            raise ValueError('Number lesson figure differs: '+name)
    return packet['populations']


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    if args.write:
        packet = build_packet()
        (SOURCE/'recorded_lab.json').write_text(json.dumps(packet, indent=1, sort_keys=True)+'\n', encoding='utf-8', newline='\n')
        from textbook.number_lab.figures import render_figures
        (SOURCE/'figures').mkdir(exist_ok=True)
        for name, svg in render_figures(packet).items():
            (SOURCE/'figures'/name).write_text(svg, encoding='utf-8', newline='\n')
    print(check_recorded())
