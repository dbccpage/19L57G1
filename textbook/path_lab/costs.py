"""Read-only native path-cost examples; AuthorityEffect: None."""
from dataclasses import replace
from itertools import product
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT/'code'))
sys.path.insert(0, str(ROOT/'research/native_bridge'))
from derivation.primitive_passage import GENESIS_P, PS, preplay, pstep  # noqa: E402
from research.native_structure import structure as native  # noqa: E402

LEAN_SOURCES = tuple('research/native_structure/lean/ResearchNativeStructure/'+name+'.lean'
                     for name in ('Cells', 'Boundary', 'Closed'))
PINS = ('research/native_structure/README.md', 'research/native_structure/CLAIMS.md',
        'research/native_structure/structure.py', 'research/native_bridge/bridge.py',
        'code/derivation/primitive_passage.py', 'code/derivation/trace_algebra.py',
        'textbook/path_lab/costs.py', *LEAN_SOURCES)
EVENTS = (('setBudget',0), ('setBudget',1), ('setBudget',2),
          ('setLicense',False), ('setLicense',True), ('halt',))
EVENT_NAMES = ('write budget 0', 'write budget 1', 'write budget 2',
               'write license off', 'write license on', 'halt')
HISTORIES = ((), (1,0), (1,1), (3,4), (1,3), (5,3), (3,5))
HISTORY_NAMES = ('empty history', 'write 1, then 0', 'write 1 twice',
                 'license off, then on', 'write 1, then license off',
                 'halt, then license off', 'license off, then halt')


def snapshot(state):
    assert replace(state,budget=0,licensed=True,halted=False) == GENESIS_P
    return {'budget':state.budget,'licensed':state.licensed,'halted':state.halted}


def history_case(start, indices):
    state = start
    rows = []
    for index in indices:
        event = EVENTS[index]
        after = pstep(state,event)
        delta = after.budget-state.budget
        changes = int(after != state)
        assert native.budget_delta(state,event) == delta
        assert native.writes(state,event) == changes
        rows.append({'before':snapshot(state),'event':index,'after':snapshot(after),
                     'delta':delta,'changes':changes})
        state = after
    events = [EVENTS[i] for i in indices]
    totals = {kind:native.path_cost(cost,start,events)
              for kind,cost in (('delta',native.budget_delta),('changes',native.writes))}
    assert totals == {kind:sum(row[kind] for row in rows) for kind in ('delta','changes')}
    assert totals['delta'] == state.budget-start.budget
    assert state == preplay(events,start)
    return {'start':snapshot(start),'events':list(indices),'end':snapshot(state),
            'rows':rows,'totals':totals,'loop':state==start}


def square_case(start, first, second):
    forward = history_case(start,(first,second))
    backward = history_case(start,(second,first))
    commutes = native.commutes(start,EVENTS[first],EVENTS[second])
    assert commutes == (forward['end']==backward['end'])
    boundaries = {kind:native.d_square(cost,start,EVENTS[first],EVENTS[second])
                  for kind,cost in (('delta',native.budget_delta),('changes',native.writes))}
    assert boundaries == {kind:forward['totals'][kind]-backward['totals'][kind]
                          for kind in ('delta','changes')}
    if commutes:
        assert boundaries == {'delta':0,'changes':0}
    return {'first':first,'second':second,'forward':forward,'backward':backward,
            'commutes':commutes,'boundaries':boundaries}


def finite_height_cases():
    # Three supplied points, all six directed edges. Reverse costs are
    # defined to negate their forward edge. This finite model is separate
    # from a global potential on every passage state and event.
    rows = []
    for ab,bc,ac in product((-1,0,1),repeat=3):
        costs = {(0,1):ab,(1,2):bc,(0,2):ac,
                 (1,0):-ab,(2,1):-bc,(2,0):-ac}
        candidates = [[0,b,c] for b,c in product((-1,0,1),repeat=2)
                      if all([0,b,c][v]-[0,b,c][u]==value
                             for (u,v),value in costs.items())]
        # Any potential can be shifted to value 0 at the first point.
        # The two edges from it force b=ab and c=ac, so the search bound
        # loses no integer-valued potential on this declared graph.
        candidate = [0,ab,ac]
        reconstructed = all(candidate[v]-candidate[u]==value
                            for (u,v),value in costs.items())
        assert reconstructed == bool(candidates) == (ab+bc-ac == 0)
        assert len(candidates) == int(reconstructed)
        rows.append({'costs':[ab,bc,ac],'loop_total':ab+bc-ac,
                     'potential':candidates[0] if candidates else None})
    return rows


def build_costs():
    assert Path(native.__file__).resolve()==ROOT/'research/native_structure/structure.py'
    assert Path(sys.modules['bridge'].__file__).resolve()==ROOT/'research/native_bridge/bridge.py'
    starts = {f'{budget}_{int(licensed)}_{int(halted)}':PS(budget=budget,licensed=licensed,halted=halted)
              for budget,licensed,halted in product(range(3),(False,True),(False,True))}
    histories = {key+'_'+str(i):history_case(start,indices)
                 for key,start in starts.items() for i,indices in enumerate(HISTORIES)}
    squares = {key+f'_{a}_{b}':square_case(start,a,b)
               for key,start in starts.items() for a,b in product(range(6),repeat=2)}
    loop = histories['0_1_0_1']
    assert loop['loop'] and loop['totals']=={'delta':0,'changes':2}
    assert histories['0_1_0_2']['totals']=={'delta':1,'changes':1}
    assert squares['0_1_0_1_3']['commutes']
    assert not squares['0_1_0_1_0']['commutes']
    assert not squares['0_1_0_5_3']['commutes']
    assert squares['0_1_1_5_3']['commutes']
    # A changed cost question in practice: count license changes only.
    license_changes=lambda s,e:int(pstep(s,e).licensed != s.licensed)
    practice_budget=native.path_cost(license_changes,GENESIS_P,[EVENTS[1],EVENTS[0]])
    practice_license=native.path_cost(license_changes,GENESIS_P,[EVENTS[3],EVENTS[4]])
    assert (practice_budget,practice_license)==(0,2)
    practice=history_case(PS(budget=2),(0,2,2))
    assert practice['loop'] and practice['totals']=={'delta':0,'changes':2}
    levels=(2,5,1)
    practice_edges=[levels[1]-levels[0],levels[2]-levels[1],levels[2]-levels[0]]
    assert practice_edges==[3,-4,-1] and practice_edges[0]+practice_edges[1]-practice_edges[2]==0
    return {'classification':'supplied finite native passage cost cases',
            'physical_observations':0,'events':EVENTS,'event_names':EVENT_NAMES,
            'history_names':HISTORY_NAMES,'starts':{key:snapshot(s) for key,s in starts.items()},
            'histories':histories,'squares':squares,'height_cases':finite_height_cases(),
            'commuting_squares':sum(r['commutes'] for r in squares.values()),
            'practice':practice,'license_only_loop_costs':[practice_budget,practice_license],
            'practice_graph_edges':practice_edges,
            'global_change_count_exact':False,'global_change_count_closed':True}


def check_cost_population():
    count = 0
    for budget,licensed,halted in product(range(3),(False,True),(False,True)):
        start=PS(budget=budget,licensed=licensed,halted=halted)
        for n in range(4):
            for word in product(range(6),repeat=n):
                history_case(start,word)
                count += 1
    assert count==3108
    return count
