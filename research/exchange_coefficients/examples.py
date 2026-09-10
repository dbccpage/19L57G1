"""Exact ordered-occupancy and exchange-transport examples.

Declared inputs: ordered finite sites, at most one occupant per site, insertion
and removal weighted by (-1) to the number of occupied earlier sites, and a
negative unit weight for each allowed move. Matrix orientation is [target][source].
These operator-supplied conventions are not forced by the initial inscription.
AuthorityEffect: None.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import hashlib
import json
from pathlib import Path

PIN = "cea346d7f3603fd8da374947e76c9b3cd426d122"
FIXTURES = {
    "chain": [(0, 1), (1, 2), (2, 3)],
    "square": [(0, 1), (0, 2), (1, 3), (2, 3)],
    "star": [(0, 1), (0, 2), (0, 3)],
}
LOOPS = {
    "square": [(0, 1), (0, 3), (0, 2), (1, 2), (0, 1)],
    "star": [(0, 1), (1, 3), (0, 3), (2, 3), (0, 2), (1, 2), (0, 1)],
}


def adjacency(edges):
    return set(edges) | {(v, u) for u, v in edges}


def transport(adjacency_set, a, b):
    """Literal HopFixture.hopB/flipB reading; zero for a missing move."""
    x, y = a
    u, v = b
    straight = (x == u and (y, v) in adjacency_set) or (y == v and (x, u) in adjacency_set)
    flip = (v == x and (y, u) in adjacency_set) or (u == y and (x, v) in adjacency_set)
    return -1 if flip else 1 if straight else 0


def exchange_matrix(n, edges, signed=True):
    basis = list(combinations(range(n), 2))
    adj = adjacency(edges)
    return [[-transport(adj, a, b) if signed else -abs(transport(adj, a, b))
             for a in basis] for b in basis]


def remove(mask, site, signed=True):
    if not mask & (1 << site):
        return None
    parity = (mask & ((1 << site) - 1)).bit_count()
    return (-1 if signed and parity % 2 else 1), mask ^ (1 << site)


def insert(mask, site, signed=True):
    if mask & (1 << site):
        return None
    parity = (mask & ((1 << site) - 1)).bit_count()
    return (-1 if signed and parity % 2 else 1), mask | (1 << site)


def occupancy_matrix(n, edges, signed=True):
    """Independent full occupation-bit implementation of -sum A(q,p)c†p cq.
    It does not use the repository move or flip formula."""
    basis = [sum(1 << i for i in pair) for pair in combinations(range(n), 2)]
    index = {mask: i for i, mask in enumerate(basis)}
    matrix = [[0] * len(basis) for _ in basis]
    for column, mask in enumerate(basis):
        for q, p in adjacency(edges):
            removed = remove(mask, q, signed)
            if removed is None:
                continue
            sign1, middle = removed
            inserted = insert(middle, p, signed)
            if inserted is not None:
                sign2, target = inserted
                matrix[index[target]][column] -= sign1 * sign2
    return matrix


def compose_on_basis(first, second, mask, p, q):
    value = second(mask, q)
    if value is None:
        return {}
    sign, middle = value
    final = first(middle, p)
    return {} if final is None else {final[1]: sign * final[0]}


def add_vectors(a, b):
    keys = a.keys() | b.keys()
    return {k: a.get(k, 0) + b.get(k, 0) for k in keys if a.get(k, 0) + b.get(k, 0)}


def verify_operator_identities(n):
    """Check remove/insert + insert/remove = delta, and each same-kind sum = zero."""
    count = 0
    for mask in range(1 << n):
        for p, q in product(range(n), repeat=2):
            ac = add_vectors(compose_on_basis(remove, insert, mask, p, q),
                             compose_on_basis(insert, remove, mask, q, p))
            assert ac == ({mask: 1} if p == q else {})
            for op in (remove, insert):
                assert add_vectors(compose_on_basis(op, op, mask, p, q),
                                   compose_on_basis(op, op, mask, q, p)) == {}
            count += 3
    return count


def multiply(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def charpoly(matrix):
    """Trace recurrence; descending coefficients, exact divisions checked."""
    n = len(matrix)
    current = [[int(i == j) for j in range(n)] for i in range(n)]
    coefficients = [1]
    for k in range(1, n + 1):
        current = multiply(matrix, current)
        trace = sum(current[i][i] for i in range(n))
        assert trace % k == 0
        ck = -trace // k
        coefficients.append(ck)
        for i in range(n):
            current[i][i] += ck
    return coefficients


def determinant(matrix):
    """Independent exact row elimination over rational numbers."""
    a = [[Fraction(x) for x in row] for row in matrix]
    value = Fraction(1)
    for k in range(len(a)):
        pivot = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            value *= -1
        diagonal = a[k][k]
        value *= diagonal
        for i in range(k + 1, len(a)):
            factor = a[i][k] / diagonal
            for j in range(k + 1, len(a)):
                a[i][j] -= factor * a[k][j]
    assert value.denominator == 1
    return int(value)


def poly_value(coefficients, x):
    result = 0
    for coefficient in coefficients:
        result = x * result + coefficient
    return result


def verify_charpoly(matrix, coefficients):
    n = len(matrix)
    assert len(coefficients) == n + 1 and coefficients[0] == 1
    # Both sides have degree n; agreement at n+1 distinct arguments fixes them.
    for x in range(n + 1):
        shifted = [[x * int(i == j) - matrix[i][j] for j in range(n)] for i in range(n)]
        assert determinant(shifted) == poly_value(coefficients, x)


def gauge_solutions(n, edges):
    basis = list(combinations(range(n), 2))
    adj = adjacency(edges)
    solutions = []
    for vertex_signs in product((-1, 1), repeat=len(basis)):
        if all(vertex_signs[i] * transport(adj, a, b) * vertex_signs[j] == 1
               for i, a in enumerate(basis) for j, b in enumerate(basis) if transport(adj, a, b)):
            solutions.append(vertex_signs)
    return solutions


def loop_sign(edges, walk, vertex_signs=None):
    adj = adjacency(edges)
    value = 1
    for a, b in zip(walk, walk[1:]):
        edge = transport(adj, a, b)
        assert edge != 0
        value *= edge if vertex_signs is None else vertex_signs[a] * edge * vertex_signs[b]
    return value


def report():
    fixtures = {}
    for name, edges in FIXTURES.items():
        signed = exchange_matrix(4, edges)
        occupancy = occupancy_matrix(4, edges)
        unsigned = exchange_matrix(4, edges, False)
        assert signed == occupancy
        assert unsigned == occupancy_matrix(4, edges, False)
        assert signed == [list(c) for c in zip(*signed)]
        polynomials = {'signed': charpoly(signed), 'unsigned': charpoly(unsigned)}
        verify_charpoly(signed, polynomials['signed'])
        verify_charpoly(unsigned, polynomials['unsigned'])
        sign_assignments = gauge_solutions(4, edges)
        assert bool(sign_assignments) == (name == 'chain')
        row = {'basis': list(combinations(range(4), 2)), 'edges': edges,
               'signed_matrix': signed, 'unsigned_matrix': unsigned,
               'entry_comparisons_per_interpretation': 36,
               'characteristic_polynomials_descending': polynomials,
               'gauges_removing_exchange_signs': len(sign_assignments)}
        if name in LOOPS:
            walk = LOOPS[name]
            assert loop_sign(edges, walk) == -1
            for values in product((-1, 1), repeat=6):
                vertex_signs = dict(zip(combinations(range(4), 2), values))
                assert loop_sign(edges, walk, vertex_signs) == -1
            row.update({'exchange_loop': walk, 'loop_sign': -1, 'gauges_checked': 64})
        fixtures[name] = row
    assert fixtures['star']['characteristic_polynomials_descending'] == {
        'signed': [1, 0, -6, 0, 9, 0, 0],
        'unsigned': [1, 0, -6, 0, 9, 0, -4]}
    # Exhaust every simple labelled graph on at most five sites, not just fixtures.
    graph_count = entry_count = 0
    for n in range(2, 6):
        possible = list(combinations(range(n), 2))
        for bits in product((False, True), repeat=len(possible)):
            edges = [e for e, selected in zip(possible, bits) if selected]
            actual = occupancy_matrix(n, edges)
            assert actual == exchange_matrix(n, edges)
            graph_count += 1
            entry_count += len(actual) ** 2
    return {'source_commit': PIN, 'fixtures': fixtures,
            'all_simple_graphs_n_2_through_5': graph_count,
            'graph_matrix_entry_comparisons': entry_count,
            'operator_basis_equalities_n_1_through_6': sum(verify_operator_identities(n) for n in range(1, 7)),
            'scope': 'Exact finite computations; the arbitrary-size coefficient theorem is in Lean.'}


def main():
    result = report()
    output = Path(__file__).resolve().parent / 'evidence' / 'examples.json'
    output.parent.mkdir(exist_ok=True)
    data = json.dumps(result, indent=2, sort_keys=True) + '\n'
    output.write_text(data, encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'fixtures'}, indent=2))
    print('Exact star roots: unsigned (-2,-1,-1,1,1,2); signed (-sqrt(3),-sqrt(3),0,0,sqrt(3),sqrt(3))')
    print('Receipt SHA256:', hashlib.sha256(data.encode()).hexdigest())


if __name__ == '__main__':
    main()
