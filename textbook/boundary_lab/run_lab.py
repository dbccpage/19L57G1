"""Read-only research examples for the boundary/swap lessons.

AuthorityEffect: None. The three models keep their owners and meanings.
No model translation, general cost theorem, or reader learning is inferred.
"""
import argparse
import hashlib
from itertools import permutations, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'research/side_free/code'))
from research.boundary_seed.code.boundary import model as boundary  # noqa: E402
from research.oriented_boundary import oriented_boundary as oriented  # noqa: E402
from sidefree import model as control, candidates  # noqa: E402
from sidefree.enumerate import minima  # noqa: E402

assert Path(control.__file__).resolve() == ROOT / 'research/side_free/code/sidefree/model.py'

PINS = (
    'research/boundary_seed/code/boundary/model.py',
    'research/boundary_seed/lean/BoundarySeed/Basic.lean',
    'research/boundary_seed/SEED.md',
    'research/boundary_seed/CLAIM_LEDGER.md',
    'research/side_free/code/sidefree/model.py',
    'research/side_free/code/sidefree/candidates.py',
    'research/side_free/code/sidefree/enumerate.py',
    'research/side_free/code/sidefree/requirement.py',
    'research/side_free/code/sidefree/presentation.py',
    'research/side_free/lean/SideFree/Basic.lean',
    'research/side_free/lean/SideFree/Forget.lean',
    'research/side_free/CLAIM_LEDGER.md',
    'research/side_free/STATUS.md',
    'research/oriented_boundary/oriented_boundary.py',
    'research/oriented_boundary/lean/OrientedBoundary/Basic.lean',
    'research/oriented_boundary/CLAIM_LEDGER.md',
    'research/oriented_boundary/BLIND_RECONCILIATION.md',
)


def plain(value):
    return json.loads(json.dumps(value))


def boundary_case(reading, placement):
    history = [e for side in placement
               for e in (boundary.Supply('a'), boundary.AdmitOccurrence('a', side))]
    state = boundary.replay(history, boundary.genesis(reading))
    assert state.placement == placement and state.n_marks() == len(placement)
    return {'reading': reading, 'placement': list(placement),
            'contents': [sorted(boundary.contents(state, side)) for side in (0, 1)],
            'names': [boundary.observation_holds(state, boundary.SideNamed(side, name))
                      for side, name in ((0, 'near'), (1, 'far'))],
            'equal_profiles': boundary.sides_collapsed(state),
            'holding_judgments': len(boundary.observations(state))}


def report_case(mask):
    admitted = tuple(d for i, d in enumerate(oriented.ALL_JUDGMENTS) if mask & (1 << i))
    preserves = oriented.swap_in_aut(admitted)
    witnesses = oriented.breaking_witnesses(admitted)
    assert preserves == (not witnesses)
    assert preserves == all(a == b for a, b in admitted)
    return plain({'mask': mask, 'admitted': admitted, 'swap_preserves_all': preserves,
                  'breaking_witnesses': witnesses})


def permutation_case(labels, permitted, keep_labels, key_choice):
    state = control.Regime(tuple(labels))
    autos = control.automorphisms_under(state, permitted, keep_labels, key_choice)
    # Independent exhaustive oracle: relocate the labels, then compare keys.
    oracle = []
    images = []
    for pi in permutations(range(len(labels))):
        if not permitted and pi != tuple(range(len(labels))):
            continue
        relocated = [''] * len(labels)
        for old, new in enumerate(pi):
            relocated[new] = labels[old]
        native_image = control.rename_marks(state, pi)
        assert native_image.marks == tuple(relocated)
        images.append({'permutation': list(pi), 'labels': list(native_image.marks)})
        if not keep_labels or tuple(relocated) == tuple(labels):
            oracle.append(pi)
    assert autos == oracle
    separating = control.marks_separable_under(state, 0, 1, permitted, keep_labels, key_choice)
    assert separating == all(pi[0] != 1 for pi in oracle)
    separated_pairs = []
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            answer = control.marks_separable_under(state, i, j, permitted, keep_labels, key_choice)
            assert answer == all(pi[i] != j for pi in oracle)
            if answer:
                separated_pairs.append([i, j])
    return plain({'labels': labels, 'permutations_permitted': permitted,
                  'keep_labels': keep_labels, 'key_choice': key_choice,
                  'automorphisms': autos, 'separates_0_1': separating,
                  'separated_pairs': separated_pairs, 'images': images})


def candidate_case(bits):
    aug = candidates.Augmentation(*bits)
    state = control.replay(candidates.candidate_history(candidates.caller_wholes(), aug),
                           control.genesis())
    permitted, keep = candidates.flags(aug)
    row = permutation_case(state.marks, permitted, keep, 'arity')
    cost = len(candidates.changed_coordinates(aug))
    assert state.marks == ('a',) * (3 if aug.extra_mark else 2)
    row.update(name=candidates.point_name(aug), coordinates=list(bits), mu1=cost,
               one_step=cost == 1, eligible=cost <= 1, satisfies=row['separates_0_1'],
               class_key=[*candidates.effective_structure(aug),
                          control.canonical_under(state, permitted, keep)],
               identity_only=control.no_permitted_renaming_moves_an_index(state, permitted))
    return plain(row)


def build_packet():
    boundaries = {reading + '_' + ''.join(map(str, sides)): boundary_case(reading, sides)
                  for reading in ('U', 'O') for n in range(4)
                  for sides in product((0, 1), repeat=n)}
    reports = {str(mask): report_case(mask) for mask in range(16)}
    menu = {''.join(str(int(v)) for v in bits): candidate_case(bits)
            for bits in product((False, True), repeat=3)}
    transfer = {}
    for n in (2, 3):
        for labels in product(('a', 'b'), repeat=n):
            for permitted, keep in product((False, True), repeat=2):
                for key in ('arity', 'empty'):
                    ident = ''.join(labels) + f'_{int(permitted)}{int(keep)}_{key}'
                    transfer[ident] = permutation_case(labels, permitted, keep, key)
    primary = minima(list(menu.values()), 'mu1')
    excluded = [r['name'] for r in menu.values() if r['identity_only']]
    secondary = minima(list(menu.values()), 'mu1', excluded)
    assert primary['minimum'] == 1 and primary['points'] == ['withdraw_mark_permutations']
    assert primary['class_count'] == 1 and secondary['minimum'] is None
    assert boundaries['U_']['equal_profiles'] and not boundaries['O_']['equal_profiles']
    return {'authority_effect': 'None', 'digest_mode': 'UTF-8 text with LF normalization',
            'source_text_sha256': {p: hashlib.sha256((ROOT / p).read_text(encoding='utf-8').encode()).hexdigest()
                                   for p in PINS},
            'scope': 'Three declared research models; no cross-model discharge or physical claim',
            'boundary_cases': boundaries, 'report_cases': reports,
            'control_menu': menu, 'transfer_cases': transfer,
            'primary_minimum': primary, 'secondary_minimum': secondary,
            'populations': {'Boundary states': 30, 'Report subsets': 16,
                            'Control candidates': 8, 'Label/permutation/key cases': 96}}


def check_recorded(directory=SOURCE):
    actual = plain(build_packet())
    saved = json.loads((directory / 'recorded_lab.json').read_text(encoding='utf-8'))
    if saved != actual:
        raise ValueError('Boundary lesson differs from recomputed source-backed cases')
    import re
    rows = re.findall(r'^\| ([^|]+) \| (\d+) \|$',
                      (directory / 'SOURCE_MAP.md').read_text(encoding='utf-8'), re.M)
    counts = {k: int(v) for k, v in rows}
    if len(rows) != len(actual['populations']) or counts != actual['populations']:
        raise ValueError('Boundary lesson population table differs')
    from textbook.boundary_lab.figures import render_figures
    for name, svg in render_figures(actual).items():
        if (directory / 'figures' / name).read_text(encoding='utf-8') != svg:
            raise ValueError('Boundary lesson figure differs: ' + name)
    return actual['populations']


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    if args.write:
        packet = plain(build_packet())
        (SOURCE / 'recorded_lab.json').write_text(json.dumps(packet, indent=1, sort_keys=True) + '\n',
                                                 encoding='utf-8', newline='\n')
        from textbook.boundary_lab.figures import render_figures
        (SOURCE / 'figures').mkdir(exist_ok=True)
        for name, svg in render_figures(packet).items():
            (SOURCE / 'figures' / name).write_text(svg, encoding='utf-8', newline='\n')
    print(check_recorded())
