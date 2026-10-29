"""Exact research source plus finite book adapters; AuthorityEffect: None."""
import json
from .run_lab import ROOT, SOURCE, build_packet

NATIVE = (
    'BoundarySeed.genesis_initial_datum', 'BoundarySeed.genesis_placement_nil',
    'BoundarySeed.no_observation_at_genesis', 'BoundarySeed.O_name_judgment_at_genesis',
    'BoundarySeed.U_no_name_judgment_at_genesis', 'BoundarySeed.sides_collapsed_at_genesis_U',
    'BoundarySeed.sides_distinct_at_genesis_O', 'BoundarySeed.no_event_follows',
    'OrientedBoundary.swap_iff', 'OrientedBoundary.b_is_empty',
    'OrientedBoundary.not_in_aut_needs_witness', 'OrientedBoundary.s2u_swap_is_automorphism',
    'OrientedBoundary.s2o_swap_is_not_automorphism', 'OrientedBoundary.s2o_breaks_at_one_witness',
    'SideFree.retained_replays_from_genesis', 'SideFree.shared_policy_retains_one_mark',
    'SideFree.base_exchange_is_an_automorphism', 'SideFree.exchange_moves_zero_to_one',
    'SideFree.keep_labels_exchange_is_an_automorphism',
    'SideFree.extra_mark_exchange_is_an_automorphism',
    'SideFree.retainedPlus_replays_from_genesis',
    'SideFree.withdrawal_does_not_move_zero_to_one', 'SideFree.exchange_is_not_the_identity',
)


def ls(values, item=str):
    return '[' + ', '.join(item(v) for v in values) + ']'


def boolean(value):
    return 'true' if value else 'false'


def pairs(values):
    return ls(values, lambda p: f'({boolean(p[0])}, {boolean(p[1])})')


def build_checks():
    paths = ('research/boundary_seed/lean/BoundarySeed/Basic.lean',
             'research/oriented_boundary/lean/OrientedBoundary/Basic.lean',
             'research/side_free/lean/SideFree/Basic.lean',
             'research/side_free/lean/SideFree/Forget.lean')
    sources = [(ROOT / p).read_text(encoding='utf-8') for p in paths]
    imported = 'import SideFree.Basic\n'
    assert sources[-1].count(imported) == 1
    sources[-1] = sources[-1].replace(imported, '', 1)
    lines = [*sources, '''
namespace Textbook.BoundaryLab

/-- Python reports push-forward permutations. Lean reads entries at indices.
The second list is the inverse; the first retains the reported convention. -/
def surviving (labels : List String) (keep : Bool)
    (perms : List (List Nat × List Nat)) : List (List Nat) :=
  (perms.filter (fun p => decide
    (SideFree.freeKey keep (SideFree.freeRename p.2 ⟨labels⟩) =
      SideFree.freeKey keep ⟨labels⟩))).map Prod.fst
''']
    packet = build_packet()
    names = []
    for ident, row in packet['boundary_cases'].items():
        name = 'boundary_' + ident
        state = 'state_' + ident
        lines.append(f'def {state} : BoundarySeed.Regime := ⟨.{row["reading"]}, .initial, {ls(row["placement"], boolean)}⟩')
        lines.append(f'''theorem {name} :
  BoundarySeed.contents {state} false = {ls(row['contents'][0])} ∧
  BoundarySeed.contents {state} true = {ls(row['contents'][1])} ∧
  decide (BoundarySeed.sideProfile {state} false = BoundarySeed.sideProfile {state} true) = {boolean(row['equal_profiles'])} ∧
  BoundarySeed.holds {state} (.sideNamed false .near) = {boolean(row['names'][0])} ∧
  BoundarySeed.holds {state} (.sideNamed true .far) = {boolean(row['names'][1])} := by decide
''')
        names.append('Textbook.BoundaryLab.' + name)
    for ident, row in packet['report_cases'].items():
        name = 'reports_' + ident
        lines.append(f'''theorem {name} :
  OrientedBoundary.swapInAut {pairs(row['admitted'])} = {boolean(row['swap_preserves_all'])} ∧
  ({pairs(row['admitted'])}.filter OrientedBoundary.distinguishes) = {pairs(row['breaking_witnesses'])} := by decide
''')
        names.append('Textbook.BoundaryLab.' + name)
    cases = [('menu_' + k, row) for k, row in packet['control_menu'].items()]
    cases += [('labels_' + k, row) for k, row in packet['transfer_cases'].items() if k.endswith('_arity')]
    for ident, row in cases:
        n = len(row['labels'])
        from itertools import permutations
        ps = list(permutations(range(n))) if row['permutations_permitted'] else [tuple(range(n))]
        # Inversion makes the source actions agree on the supplied finite case.
        bindings = [(pi, [pi.index(i) for i in range(n)]) for pi in ps]
        paired = ls(bindings, lambda p: f'({ls(p[0])}, {ls(p[1])})')
        value = f'surviving {ls(row["labels"], json.dumps)} {boolean(row["keep_labels"])} {paired}'
        claims = [f'{value} = {ls(row["automorphisms"], ls)}']
        for image in row['images']:
            pi = image['permutation']
            inverse = [pi.index(i) for i in range(n)]
            claims.append(f'(SideFree.freeRename {ls(inverse)} ⟨{ls(row["labels"], json.dumps)}⟩).marks = {ls(image["labels"], json.dumps)}')
        for i in range(n):
            for j in range(i + 1, n):
                answer = [i, j] in row['separated_pairs']
                claims.append(f'({value}).all (fun pi => !(SideFree.moves pi {i} {j})) = {boolean(answer)}')
        lines.append(f'theorem {ident} :\n  ' + ' ∧\n  '.join(claims) + ' := by decide\n')
        names.append('Textbook.BoundaryLab.' + ident)
    lines.append('end Textbook.BoundaryLab')
    lines.extend('#print axioms ' + name for name in [*NATIVE, *names])
    return '\n'.join(lines), [*NATIVE, *names]


def expected_reports(names):
    axioms = json.loads((SOURCE / 'expected_axioms.json').read_text(encoding='utf-8'))
    if set(axioms) != set(names):
        raise ValueError('Boundary book report population changed; review the exact names')
    if any(set(a) - {'propext', 'Quot.sound'} for a in axioms.values()):
        raise ValueError('Boundary book report leaves the declared axiom boundary')
    return {name: 'depends on axioms: [' + ', '.join(axioms[name]) + ']'
            if axioms[name] else 'does not depend on any axioms' for name in names}
