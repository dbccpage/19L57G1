"""Actual-step and translation examples from read-only owners; AuthorityEffect: None."""
from dataclasses import asdict
from itertools import product
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'code'))
from derivation.primitive_passage import GENESIS_P, PS, preplay, pstep  # noqa: E402
from research.native_bridge import bridge  # noqa: E402

LEAN_SOURCES = (
    'research/g013_trace_calculus/lean/Trace.lean',
    *('research/native_bridge/lean/ResearchNativeBridge/'+name+'.lean'
      for name in ('Path', 'Passage', 'Sim', 'Observe', 'Realize')))
PINS = ('code/derivation/primitive_passage.py', 'code/derivation/trace_algebra.py',
        'research/native_bridge/bridge.py', 'research/native_bridge/CLAIMS.md',
        'research/native_bridge/README.md', *LEAN_SOURCES,
        'textbook/map_lab/native_paths.py')


def encoded(bit):
    return PS(budget=bit)


def budget_reading(state):
    # This exact form of native observation is justified only for the
    # genesis-core states used by this exhibit. No finite truncation of
    # an arbitrary Nat-valued relation is presented as its whole value.
    assert bridge.core(state) == bridge.core(GENESIS_P)
    assert state.obs is None and not state.wit and not state.prot and not state.refusals
    return {'zero_relation': 'undeclared', 'active_obstructions': [], 'refusals': []}


def translated_history(table, start, events):
    source = start
    target = encoded(start)
    rows = []
    for event in events:
        after = table[2*source+event]
        native_event = ('setBudget', after)
        following = pstep(target, native_event)
        assert following == encoded(after)
        rows.append({'source_before': source, 'event': event, 'source_after': after,
                     'target_before': asdict(target), 'target_event': list(native_event),
                     'target_after': asdict(following),
                     'native_reading': budget_reading(following)})
        source, target = after, following
    assert preplay([tuple(row['target_event']) for row in rows], encoded(start)) == target
    return {'start': start, 'events': list(events), 'source_end': source,
            'target_end': asdict(target), 'rows': rows}


def checked_trace(steps):
    """Require adjacency before using the owner's per-row realizer.

    Lean's indexed Trace already supplies adjacency. The Python owner's
    realize helper checks labels and target equations, not cross-row links.
    """
    if any(left[1] != right[0] for left, right in zip(steps, steps[1:])):
        return {'valid': False, 'reason': 'disconnected rows', 'events': None}
    events = bridge.realize(bridge.witness_decoder, steps)
    if events is None:
        reason = ('unknown label' if any(bridge.witness_decoder(label) is None
                                        for _, _, label in steps)
                  else 'event reaches a different target')
        return {'valid': False, 'reason': reason, 'events': None}
    return {'valid': True, 'reason': 'every row is an actual step',
            'events': [list(event) for event in events]}


def build_paths():
    assert Path(bridge.__file__).resolve() == ROOT/'research/native_bridge/bridge.py'
    assert Path(sys.modules[pstep.__module__].__file__).resolve() == ROOT/'code/derivation/primitive_passage.py'
    # Event 0 means flip, 1 means hold: two admitted source operations.
    toggle = (1, 0, 0, 1)
    histories = {f'{start}_'+''.join(map(str, events)): translated_history(toggle, start, events)
                 for start in range(2) for n in range(6)
                 for events in product(range(2), repeat=n)}
    assert len(histories) == 126
    assert bridge.budget_sim(lambda s, e: toggle[2*s+e], [0, 1], [0, 1]) == {
        'squares': 4, 'distinct_encodings': 2, 'distinct_cores': 1}
    assert encoded(0) != encoded(1)
    assert budget_reading(encoded(0)) == budget_reading(encoded(1))
    first = pstep(GENESIS_P, ('admitOcc', 0))
    stopped = pstep(GENESIS_P, ('halt',))
    examples = {
        'actual admission': [(GENESIS_P, first, 'admitOcc')],
        'wrong event label': [(GENESIS_P, stopped, 'admitOcc')],
        'actual halt': [(GENESIS_P, stopped, 'halt')],
        'unknown label': [(GENESIS_P, first, 'wave')],
        'disconnected rows': [(GENESIS_P, first, 'admitOcc'), (GENESIS_P, stopped, 'halt')],
        'empty history': [],
        'repeated admission': [(GENESIS_P, first, 'admitOcc'), (first, first, 'admitOcc')]}
    traces = {name: {'record_id': 'Record '+chr(65+index), **checked_trace(steps), 'rows': [
        {'before': asdict(src), 'label': label, 'after': asdict(dst)}
        for src, dst, label in steps]} for index, (name, steps) in enumerate(examples.items())}
    assert [row['valid'] for row in traces.values()] == [True, False, True, False, False, True, True]
    # The weaker Python helper accepts disconnected locally valid rows;
    # the additional adjacency gate is load-bearing, not a native theorem.
    assert bridge.realize(bridge.witness_decoder, examples['disconnected rows']) is not None
    once = preplay([('admitOcc', 0)], GENESIS_P)
    twice = preplay([('admitOcc', 0), ('admitOcc', 0)], GENESIS_P)
    assert once == twice and bridge.realize_report()['endpoints_joined']
    assert pstep(stopped, ('admitOcc', 0)) == stopped
    # Changed three-state practice: budget codes are arbitrary supplied
    # numbers. The repaired halt row retains the occurrence.
    codes = (2, 5, 8)
    dial = 1
    writes = []
    for advance in (True, False, True):
        dial = (dial+1) % 3 if advance else dial
        writes.append(codes[dial])
    assert writes == [8, 8, 2] and dial == 0
    repaired = checked_trace([(GENESIS_P, first, 'admitOcc'),
                              (first, pstep(first, ('halt',)), 'halt')])
    assert repaired['valid'] and pstep(first, ('halt',)).occ == (0,)
    return {'classification': 'supplied finite switch and native passage examples',
            'physical_observations': 0, 'source_table': list(toggle),
            'event_names': ['flip', 'hold'], 'histories': histories, 'traces': traces,
            'distinct_encodings': 2, 'distinct_cores': 1, 'distinct_native_readings': 1,
            'native_reader_recovers_state': False, 'budget_reader_recovers_state': True,
            'practice_dial_writes': writes, 'practice_repaired_halt_valid': repaired['valid'],
            'same_endpoint_different_histories': True,
            'event_selection': 'supplied, not derived',
            'python_realizer_requires_adjacency_gate': True}


def check_paths_population():
    """All two-state/two-event deterministic tables, starts, histories <=5."""
    count = 0
    for table in product(range(2), repeat=4):
        for start in range(2):
            for n in range(6):
                for events in product(range(2), repeat=n):
                    expected = start
                    for event in events:
                        expected = table[2*expected+event]
                    row = translated_history(table, start, events)
                    assert row['source_end'] == expected == row['target_end']['budget']
                    count += 1
    assert count == 2016
    return count
