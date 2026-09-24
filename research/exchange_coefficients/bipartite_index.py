"""Finite index of two-occupant, unit-hopping presentation certificates.

The input Hamiltonian is exactly -sum_(p,q adjacent) c†_p c_q on the sorted
two-occupant basis.  The coefficients come from ``examples.occupancy_matrix``.
This module decides whether diagonal ±1 basis rephasings make every nonzero
off-diagonal entry negative.  It does not decide sign freedom under other
representations, transformations, or sampling algorithms.

AuthorityEffect: None.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import combinations, product

from examples import occupancy_matrix


@dataclass(frozen=True)
class GraphKey:
    sites: int
    edges: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class Gauge:
    signs: tuple[int, ...]


@dataclass(frozen=True)
class OddLoop:
    vertices: tuple[int, ...]


@dataclass(frozen=True)
class Record:
    graph: GraphKey
    site_bipartition: tuple[int, ...] | None
    certificate: Gauge | OddLoop

    @property
    def diagonal_gauge_exists(self) -> bool:
        return isinstance(self.certificate, Gauge)


def graph_key(sites: int, edges) -> GraphKey:
    """Keep labelled graphs exact; no graph-isomorphism claim is made."""
    if type(sites) is not int or sites < 2:
        raise ValueError("sites must be an integer at least two")
    normalized = set()
    for edge in edges:
        if (not isinstance(edge, (tuple, list)) or len(edge) != 2
                or any(type(v) is not int or v < 0 or v >= sites for v in edge)
                or edge[0] == edge[1]):
            raise ValueError("edges must join distinct sites in range")
        pair = tuple(sorted(edge))
        if pair in normalized:
            raise ValueError("duplicate edge")
        normalized.add(pair)
    return GraphKey(sites, tuple(sorted(normalized)))


def bipartition(graph: GraphKey) -> tuple[int, ...] | None:
    """Return a site coloring, or None when the site graph is not bipartite."""
    neighbors = [[] for _ in range(graph.sites)]
    for a, b in graph.edges:
        neighbors[a].append(b)
        neighbors[b].append(a)
    colors = [-1] * graph.sites
    for root in range(graph.sites):
        if colors[root] >= 0:
            continue
        colors[root] = 0
        queue = deque([root])
        while queue:
            a = queue.popleft()
            for b in neighbors[a]:
                if colors[b] < 0:
                    colors[b] = 1 - colors[a]
                    queue.append(b)
                elif colors[b] == colors[a]:
                    return None
    return tuple(colors)


def linear_forest(graph: GraphKey) -> bool:
    """Check whether every site component is a path or an isolated vertex."""
    degree = [0] * graph.sites
    parent = list(range(graph.sites))

    def root(vertex: int) -> int:
        while parent[vertex] != vertex:
            vertex = parent[vertex]
        return vertex

    for a, b in graph.edges:
        degree[a] += 1
        degree[b] += 1
        ra, rb = root(a), root(b)
        if ra == rb:
            return False
        parent[ra] = rb
    return max(degree) <= 2


def _validate_matrix(matrix) -> None:
    size = len(matrix)
    if not size or any(len(row) != size for row in matrix):
        raise ValueError("matrix must be nonempty and square")
    for i in range(size):
        if matrix[i][i] != 0:
            raise ValueError("diagonal must vanish")
        for j in range(size):
            if type(matrix[i][j]) is not int or matrix[i][j] not in (-1, 0, 1):
                raise ValueError("entries must be integer -1, 0, or 1")
            if matrix[i][j] != matrix[j][i]:
                raise ValueError("matrix must be symmetric")


def _path_to_root(vertex: int, parent: list[int]) -> list[int]:
    path = []
    while vertex >= 0:
        path.append(vertex)
        vertex = parent[vertex]
    return path


def _tree_cycle(a: int, b: int, parent: list[int]) -> tuple[int, ...]:
    left = _path_to_root(a, parent)
    right = _path_to_root(b, parent)
    left_positions = {vertex: i for i, vertex in enumerate(left)}
    common = next(vertex for vertex in right if vertex in left_positions)
    return tuple(left[:left_positions[common] + 1]
                 + list(reversed(right[:right.index(common)])) + [a])


def classify_matrix(matrix) -> Gauge | OddLoop:
    """Exact signed-graph decision with a checkable certificate either way."""
    _validate_matrix(matrix)
    size = len(matrix)
    signs = [0] * size
    parent = [-1] * size
    for root in range(size):
        if signs[root]:
            continue
        signs[root] = 1
        queue = deque([root])
        while queue:
            a = queue.popleft()
            for b, value in enumerate(matrix[a]):
                if value == 0:
                    continue
                required = signs[a] * (-value)
                if not signs[b]:
                    signs[b] = required
                    parent[b] = a
                    queue.append(b)
                elif signs[b] != required:
                    result = OddLoop(_tree_cycle(a, b, parent))
                    assert verify_certificate(matrix, result)
                    return result
    result = Gauge(tuple(signs))
    assert verify_certificate(matrix, result)
    return result


def verify_certificate(matrix, certificate: Gauge | OddLoop) -> bool:
    """Check a diagonal gauge or a negative closed transport loop directly."""
    _validate_matrix(matrix)
    size = len(matrix)
    if isinstance(certificate, Gauge):
        signs = certificate.signs
        return (len(signs) == size and all(type(s) is int and s in (-1, 1) for s in signs)
                and all(not matrix[i][j] or signs[i] * matrix[i][j] * signs[j] == -1
                        for i in range(size) for j in range(size) if i != j))
    if isinstance(certificate, OddLoop):
        walk = certificate.vertices
        if (len(walk) < 4 or walk[0] != walk[-1]
                or len(set(walk[:-1])) != len(walk) - 1
                or any(type(v) is not int or v < 0 or v >= size for v in walk)):
            return False
        sign = 1
        for a, b in zip(walk, walk[1:]):
            if not matrix[a][b]:
                return False
            sign *= -matrix[a][b]
        return sign == -1
    return False


def analyze(sites: int, edges) -> Record:
    graph = graph_key(sites, edges)
    matrix = occupancy_matrix(graph.sites, graph.edges)
    certificate = classify_matrix(matrix)
    return Record(graph, bipartition(graph), certificate)


def all_records(min_sites: int = 2, max_sites: int = 5) -> list[Record]:
    """Exhaust simple labelled graphs in the declared finite range."""
    if min_sites < 2 or max_sites < min_sites:
        raise ValueError("invalid site range")
    records = []
    for sites in range(min_sites, max_sites + 1):
        possible = list(combinations(range(sites), 2))
        for choices in product((False, True), repeat=len(possible)):
            edges = [edge for edge, chosen in zip(possible, choices) if chosen]
            records.append(analyze(sites, edges))
    return records


def inverted_index(records: list[Record]) -> dict[tuple[str, object], set[int]]:
    """Postings retrieve candidates; the certificate remains the evidence."""
    postings: dict[tuple[str, object], set[int]] = {}
    for row, record in enumerate(records):
        features = {
            'sites': record.graph.sites,
            'site_bipartite': record.site_bipartition is not None,
            'linear_forest': linear_forest(record.graph),
            'diagonal_gauge_exists': record.diagonal_gauge_exists,
        }
        for name, value in features.items():
            postings.setdefault((name, value), set()).add(row)
    return postings


def query(records: list[Record], postings, **features) -> list[Record]:
    allowed = {'sites', 'site_bipartite', 'linear_forest', 'diagonal_gauge_exists'}
    if not features or not features.keys() <= allowed:
        raise ValueError("specify known indexed features")
    if any((type(value) is not int if name == 'sites' else type(value) is not bool)
           for name, value in features.items()):
        raise ValueError("feature types must be exact")
    hits = set(range(len(records)))
    for name, value in features.items():
        hits.intersection_update(postings.get((name, value), set()))
    return [records[i] for i in sorted(hits)]


def catalog() -> dict:
    """A replayable finite catalogue; every row has a checked witness."""
    records = all_records()
    counts = {}
    rows = []
    for record in records:
        graph = record.graph
        matrix = occupancy_matrix(graph.sites, graph.edges)
        assert verify_certificate(matrix, record.certificate)
        bipartite = record.site_bipartition is not None
        gauge = record.diagonal_gauge_exists
        name = ('bipartite_' if bipartite else 'nonbipartite_') + ('gauge' if gauge else 'odd_loop')
        size_counts = counts.setdefault(str(graph.sites), {})
        size_counts[name] = size_counts.get(name, 0) + 1
        basis = list(combinations(range(graph.sites), 2))
        if isinstance(record.certificate, Gauge):
            witness = {'kind': 'diagonal_gauge', 'basis_signs': record.certificate.signs}
        else:
            witness = {'kind': 'negative_exchange_loop',
                       'basis_walk': [basis[i] for i in record.certificate.vertices]}
        rows.append({'sites': graph.sites, 'edges': graph.edges,
                     'site_bipartition': record.site_bipartition,
                     'linear_forest': linear_forest(graph),
                     'diagonal_gauge_exists': gauge, 'witness': witness})
    return {
        'authority_effect': 'None',
        'family': 'two occupants, sorted-pair basis, unit negative hopping',
        'allowed_transform': 'diagonal basis rephasing by plus or minus one',
        'label_policy': 'simple labelled site graphs; no isomorphism quotient',
        'sites': [2, 3, 4, 5],
        'counts': counts,
        'linear_forest_matches_all_rows': all(
            row['linear_forest'] == row['diagonal_gauge_exists'] for row in rows),
        'rows': rows,
    }
