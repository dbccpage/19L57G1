"""Recompute the growth teaching models; AuthorityEffect: None."""
import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from research.standing_commitment import standing as native  # noqa: E402

COMMITMENTS = ('total', 'adjacent', 'shared_parity', 'empty', 'bounded')
VIEW_FAMILIES = ((), ((0, 1),), ((1, 2),), ((0, 1), (1, 2)))
PINS = ('research/standing_commitment/standing.py',
        'research/standing_commitment/lean/StandingCommitment/Base.lean',
        'research/standing_commitment/lean/StandingCommitment/Commitment.lean',
        'research/standing_commitment/lean/StandingCommitment/AxiomReport.lean',
        'research/standing_commitment/CLAIM_LEDGER.md',
        'research/two_sided_commitment/CLAIM_LEDGER.md')


def plain(value):
    return json.loads(json.dumps(value))


def separated(views, i, j):
    return any((i in view) != (j in view) for view in views)


def demands(name, data, views):
    return [p for p in native.pairs_of(list(data))
            if native.holds(name, *p) and not separated(views, *p)]


def growth_case(mask, family, name):
    data = [i for i in range(4) if mask & (1 << i)]
    views = VIEW_FAMILIES[family]
    old = demands(name, data, views)
    raw = native.generated_by_growth(name, data, 4)
    fresh = [p for p in raw if not separated(views, *p)]
    after = demands(name, [4] + data, views)
    assert after == fresh + old
    assert all(p not in old for p in fresh)
    assert len(fresh) <= len(data)
    if name == 'total' and not views:
        assert len(fresh) == len(data)
    return plain({'mask': mask, 'family': family, 'commitment': name,
                  'data': data, 'new': 4, 'views': views, 'before': old,
                  'committed_new_pairs': raw, 'new_demands': fresh, 'after': after,
                  'reopens': not old and bool(fresh)})


def independent_race(name, rounds, rate):
    queue = []
    discharged = []
    log = []
    fresh_lists = []
    for n in range(rounds):
        fresh = [(n, i) for i in range(n) if native.holds(name, n, i)]
        # This accounting model has no observation views. A removal is an
        # assumed service, not a constructed repair of a represented world.
        assert not set(fresh).intersection(discharged)
        queue.extend(fresh)
        removed = queue[:rate]
        queue = queue[rate:]
        discharged.extend(removed)
        fresh_lists.append(fresh)
        log.append({'round': n, 'admitted': n, 'generated': len(fresh),
                    'discharged': len(removed), 'backlog': len(queue)})
    return log, plain(fresh_lists)


def race_case(name, rounds, rate):
    result = native.race(name, rounds, rate)
    log, fresh = independent_race(name, rounds, rate)
    assert result['log'] == log
    assert result['generated'] == sum(r['generated'] for r in log)
    assert result['discharged'] == sum(r['discharged'] for r in log)
    assert result['final_backlog'] == result['generated'] - result['discharged']
    assert result['max_backlog'] == max((r['backlog'] for r in log), default=0)
    # The native summary's "ever_cleared_after_first" checks round index >0,
    # not time after the first positive generation. The desk deliberately
    # does not present that field as a semantic clearance criterion.
    return plain({**result, 'fresh_pairs_by_round': fresh})


def reference_holds(name, i, j):
    return {'total': i != j, 'adjacent': i != j and (i+1 == j or j+1 == i),
            'shared_parity': i != j and i%2 == j%2, 'empty': False,
            'bounded': i != j and i < 4 and j < 4}[name]


def check_population():
    count = 0
    for length in range(4):
        for data in product(range(5), repeat=length):
            direct = [(data[i], data[j]) for i in range(length) for j in range(i+1, length)]
            assert native.pairs_of(list(data)) == direct
            for views, name, new in product(VIEW_FAMILIES, COMMITMENTS, range(5)):
                old = demands(name, data, views)
                fresh = [p for p in native.generated_by_growth(name, list(data), new)
                         if not separated(views, *p)]
                assert demands(name, (new,) + data, views) == fresh + old
                if not views and name == 'total' and new not in data:
                    assert len(fresh) == len(data)
                count += 1
    assert count == 15600
    return count


def build_packet():
    assert Path(native.__file__).resolve() == ROOT / PINS[0]
    for c, i, j in product(COMMITMENTS, range(13), range(13)):
        assert native.holds(c, i, j) == reference_holds(c, i, j)
    growth = {f'{m}_{f}_{c}': growth_case(m, f, c)
              for m, f, c in product(range(16), range(4), COMMITMENTS)}
    races = {f'{c}_{h}_{r}': race_case(c, h, r)
             for c, h, r in product(COMMITMENTS, range(13), range(13))}
    thresholds = {}
    for c, h in product(COMMITMENTS, range(13)):
        clearing = [r for r in range(13) if races[f'{c}_{h}_{r}']['final_backlog'] == 0]
        least = min(clearing)
        assert native.threshold(c, h, 12) == least
        log = races[f'{c}_{h}_0']['log']
        peak = max((r['generated'] for r in log), default=0)
        thresholds[f'{c}_{h}'] = {'least_final_clearing_rate': least, 'peak_generation': peak}
    assert thresholds['bounded_8'] == {'least_final_clearing_rate': 1, 'peak_generation': 3}
    assert races['bounded_8_1']['max_backlog'] == 3
    assert races['bounded_8_1']['final_backlog'] == 0
    assert races['total_8_1']['final_backlog'] == 21
    # Discharged-state reopening is a separate represented-world exhibit.
    assert growth['15_3_total']['before'] == []
    assert growth['15_3_total']['new_demands'] == [[4, 3]]
    pins = {p: hashlib.sha256((ROOT/p).read_text(encoding='utf-8').encode()).hexdigest() for p in PINS}
    return {'authority_effect': 'None', 'source_text_sha256': pins,
            'digest_mode': 'UTF-8 text with LF normalization', 'commitments': COMMITMENTS,
            'view_names': ['No views', 'View {0,1}', 'View {1,2}', 'Both views'],
            'growth_cases': growth, 'races': races, 'thresholds': thresholds}


def check_recorded(directory=SOURCE):
    packet = plain(build_packet())
    if json.loads((directory/'recorded_lab.json').read_text(encoding='utf-8')) != packet:
        raise ValueError('Recorded growth lesson differs from recomputed source-backed cases')
    counts = {'Growth settings': 320, 'Race settings': 845, 'Threshold comparisons': 65,
              'Additional list/view/commitment/new-item cases': 15600}
    rows = re.findall(r'^\| ([^|]+) \| (\d+) \|$', (SOURCE/'SOURCE_MAP.md').read_text(encoding='utf-8'), re.M)
    if {k: int(v) for k, v in rows} != counts or len(rows) != len(counts):
        raise ValueError('Growth lesson population table differs')
    from textbook.growth_lab.figures import render_figures
    for name, svg in render_figures(packet).items():
        p = SOURCE/'figures'/name
        if not p.is_file() or p.read_text(encoding='utf-8') != svg:
            raise ValueError('Growth lesson figure differs: '+name)
    return counts


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--population', action='store_true')
    args = ap.parse_args()
    if args.write:
        packet = plain(build_packet())
        (SOURCE/'recorded_lab.json').write_text(json.dumps(packet, indent=1, sort_keys=True)+'\n',encoding='utf-8',newline='\n')
        from textbook.growth_lab.figures import render_figures
        (SOURCE/'figures').mkdir(exist_ok=True)
        for name, svg in render_figures(packet).items():
            (SOURCE/'figures'/name).write_text(svg,encoding='utf-8',newline='\n')
    print(check_recorded())
    if args.population:
        print({'additional_cases':check_population()})
