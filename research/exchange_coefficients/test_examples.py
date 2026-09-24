"""Exact mathematical checks and deliberate false-claim controls."""
from fractions import Fraction
from itertools import combinations, product
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import examples as ep
import bipartite_index as bi
import claim_example as gate


def test_exchange_bridge_all_graphs_and_operator_identities():
    value = ep.report()
    assert value['all_simple_graphs_n_2_through_5'] == 1098
    assert value['graph_matrix_entry_comparisons'] == 104778
    assert value['operator_basis_equalities_n_1_through_6'] == 10350


def test_two_occupant_index_has_checked_positive_and_negative_certificates():
    records = bi.all_records()
    assert len(records) == 1098
    counts = {(sites, bipartite, gauge): sum(
        row.graph.sites == sites
        and (row.site_bipartition is not None) == bipartite
        and row.diagonal_gauge_exists == gauge for row in records)
        for sites in range(2, 6) for bipartite in (False, True) for gauge in (False, True)}
    assert {key: value for key, value in counts.items() if value} == {
        (2, True, True): 2,
        (3, False, False): 1, (3, True, True): 7,
        (4, False, False): 23, (4, True, False): 7, (4, True, True): 34,
        (5, False, False): 648, (5, True, False): 170, (5, True, True): 206,
    }
    # This equivalence is an exhaustive observation at the stated bound.
    assert all(bi.linear_forest(row.graph) == row.diagonal_gauge_exists for row in records)
    for row in records:
        matrix = ep.occupancy_matrix(row.graph.sites, row.graph.edges)
        assert bi.verify_certificate(matrix, row.certificate)

    postings = bi.inverted_index(records)
    bipartite_four = bi.query(records, postings, sites=4, site_bipartite=True)
    assert len(bipartite_four) == 41
    assert sum(row.diagonal_gauge_exists for row in bipartite_four) == 34
    assert len(bi.query(records, postings, sites=4, site_bipartite=True,
                        diagonal_gauge_exists=False)) == 7
    assert len(bi.query(records, postings, sites=5, linear_forest=True)) == 206
    assert len(bi.catalog()['rows']) == 1098

    for name in ('chain', 'square', 'star'):
        row = bi.analyze(4, ep.FIXTURES[name])
        assert row.site_bipartition is not None
        assert row.diagonal_gauge_exists == (name == 'chain')
        assert bi.verify_certificate(ep.occupancy_matrix(4, ep.FIXTURES[name]), row.certificate)
        assert bool(ep.gauge_solutions(4, ep.FIXTURES[name])) == row.diagonal_gauge_exists
    assert bi.linear_forest(bi.graph_key(4, ep.FIXTURES['chain']))
    assert not bi.linear_forest(bi.graph_key(4, ep.FIXTURES['star']))

    # Independent brute-force cross-check of the BFS decision through size 4.
    assert all(bool(ep.gauge_solutions(row.graph.sites, row.graph.edges))
               == row.diagonal_gauge_exists for row in records if row.graph.sites <= 4)


def test_two_occupant_index_rejects_bad_inputs_and_bad_certificates():
    for edges in ([(0, 0)], [(0, 4)], [(0, 1), (1, 0)]):
        try:
            bi.graph_key(4, edges)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid graph accepted')
    square = ep.occupancy_matrix(4, ep.FIXTURES['square'])
    assert not bi.verify_certificate(square, bi.Gauge((1,) * 6))
    assert not bi.verify_certificate(square, bi.OddLoop((0, 1, 0)))
    try:
        bi.classify_matrix([[0, 2], [2, 0]])
    except ValueError:
        pass
    else:
        raise AssertionError('Unsupported coefficient accepted')
    try:
        bi.query([], {}, site_bipartite=1)
    except ValueError:
        pass
    else:
        raise AssertionError('Ill-typed indexed feature accepted')


def test_gauge_preserves_star_charpoly():
    original = ep.exchange_matrix(4, ep.FIXTURES['star'])
    for g in product((-1, 1), repeat=6):
        changed = [[g[i] * original[i][j] * g[j] for j in range(6)] for i in range(6)]
        assert ep.charpoly(changed) == ep.charpoly(original)


def test_false_claims_are_not_promoted():
    results = gate.examples()['results']
    assert results['true_finite_claim']['status'] == 'CERTIFIED'
    assert results['false_promotion']['status'] == 'REFUSED'
    assert results['unsupported_claim']['status'] == 'REFUSED'
    assert gate.assess({'kind': 'integer_matrix_equality', 'left': [[True]], 'right': [[1]]})['status'] == 'REFUSED'


def test_boundary_cancellation_and_signless_control():
    def boundary(chain, signed):
        result = {}
        for cell, coefficient in chain.items():
            for i in range(len(cell)):
                face = cell[:i] + cell[i + 1:]
                result[face] = result.get(face, 0) + coefficient * ((-1) ** i if signed else 1)
        return {cell: c for cell, c in result.items() if c}
    for size in range(2, 7):
        cell = tuple(range(size))
        assert boundary(boundary({cell: 1}, True), True) == {}
    assert boundary(boundary({(0, 1, 2): 1}, False), False) == {(0,): 2, (1,): 2, (2,): 2}


def test_rational_phase_and_odd_amplitude_examples():
    # Exact rational turns modulo one; no floating-point complex theorem.
    for n, k in product(range(9), range(8)):
        q = Fraction(n, k + 1) % 1
        assert (q + 1) % 1 == q
        assert ((k + 1) * q) % 1 == 0
    half = Fraction(1, 2)
    assert half != 0 and (half + half) % 1 == 0
    weight = lambda x, y: 3 if x == 0 and y == 1 else -3 if x == 1 and y == 0 else 0
    for x, y in product(range(3), repeat=2):
        assert weight(y, x) == -weight(x, y)
    assert all(weight(x, x) == 0 for x in range(3))


def test_axiom_parser_rejects_missing_duplicate_and_extra_dependencies():
    from verify import parse_axioms
    good = "'Example.check' depends on axioms: [propext, Quot.sound]"
    assert parse_axioms(good, ['Example.check']) == {'Example.check': ['propext', 'Quot.sound']}
    bad = ['', good + '\n' + good, good.replace('Quot.sound', 'Classical.choice'),
           good.replace('Example.check', 'Example.other')]
    for text in bad:
        try:
            parse_axioms(text, ['Example.check'])
        except AssertionError:
            pass
        else:
            raise AssertionError('Invalid axiom evidence was accepted')


def test_axiom_parser_and_theorem_census_read_primed_names():
    # Names ending in zero, one and two apostrophes (added 2026-09-18).
    # The quote-blind report capture and a primeless `\w+` theorem
    # pattern both fail this case.
    from verify import declared_theorems, parse_axioms
    names = ['Example.step', "Example.step'", "Example.step''"]
    text = ("'Example.step' does not depend on any axioms\n"
            "'Example.step'' depends on axioms: [propext]\n"
            "'Example.step''' depends on axioms: [propext, Quot.sound]\n")
    assert parse_axioms(text, names) == {
        'Example.step': [], "Example.step'": ['propext'],
        "Example.step''": ['propext', 'Quot.sound']}
    source = ("theorem step : True := trivial\n"
              "theorem step' : True := trivial\n"
              "theorem step'' : True := trivial\n")
    assert declared_theorems(source) == ['step', "step'", "step''"]


def test_matrix_checker_rejects_malformed_shapes():
    for value in [[], [[1, 2]], [[1.0]], [[True]], 'matrix', None]:
        assert gate.assess({'kind': 'integer_matrix_equality', 'left': value, 'right': value})['status'] == 'REFUSED'
    assert gate.assess({'kind': 'integer_matrix_equality', 'left': [[0]], 'right': [[0]]})['status'] == 'CERTIFIED'


def test_custom_containers_cannot_override_equality():
    class AlwaysEqual(list):
        def __eq__(self, other):
            return True
        def __ne__(self, other):
            return False
    for value in [None, [], 'request']:
        assert gate.assess(value)['status'] == 'REFUSED'
    deceptive = AlwaysEqual([[1]])
    assert deceptive == [[2]]
    assert gate.assess({'kind': 'integer_matrix_equality', 'left': deceptive, 'right': [[2]]})['status'] == 'REFUSED'
