"""Worked example of a finite claim schema, not a natural-language truth gate."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from examples import FIXTURES, exchange_matrix, occupancy_matrix


def is_matrix(value):
    return (type(value) is list and bool(value) and
            all(type(row) is list and len(row) == len(value) and
                all(type(entry) is int for entry in row) for row in value))


def assess(request):
    if type(request) is not dict:
        return {'status': 'REFUSED', 'reason': 'Malformed request container.'}
    kind = request.get('kind')
    if kind == 'conjecture':
        return {'status': 'CONJECTURE', 'reason': 'No certification requested or inferred.'}
    if kind != 'integer_matrix_equality':
        return {'status': 'REFUSED', 'reason': 'No checker for this claim schema.'}
    left, right = request.get('left'), request.get('right')
    if not is_matrix(left) or not is_matrix(right):
        return {'status': 'REFUSED', 'reason': 'Malformed integer-matrix payload.'}
    digest = hashlib.sha256(json.dumps([left, right], separators=(',', ':')).encode()).hexdigest()
    if left != right:
        return {'status': 'REFUSED', 'artifact_sha256': digest, 'reason': 'Matrices differ.'}
    return {'status': 'CERTIFIED', 'artifact_sha256': digest,
            'scope': 'Equality of these two submitted finite integer matrices only.'}


def examples():
    star = FIXTURES['star']
    signed = exchange_matrix(4, star)
    occupancy = occupancy_matrix(4, star)
    unsigned = exchange_matrix(4, star, False)
    requests = {
        'labelled_uncertainty': {'kind': 'conjecture', 'text': 'A broader bridge may exist.'},
        'true_finite_claim': {'kind': 'integer_matrix_equality', 'left': signed, 'right': occupancy},
        'false_promotion': {'kind': 'integer_matrix_equality', 'left': unsigned, 'right': occupancy,
                            'claimed_status': 'CERTIFIED'},
        'unsupported_claim': {'kind': 'all_requests_settled', 'claimed_status': 'CERTIFIED'},
    }
    outputs = {name: assess(value) for name, value in requests.items()}
    assert [v['status'] for v in outputs.values()] == ['CONJECTURE', 'CERTIFIED', 'REFUSED', 'REFUSED']
    return {'requests': requests, 'results': outputs,
            'limit': 'The Python example is not a formally verified implementation of the Lean State type. Neither checker certifies prose or the meaning of an unspecified interpretation.'}


if __name__ == '__main__':
    value = examples()
    target = Path(__file__).resolve().parent / 'evidence' / 'claim_gate_example.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps(value['results'], indent=2))
