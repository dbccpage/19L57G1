"""Read-only operational-protocol teaching cases; AuthorityEffect: None."""
from dataclasses import asdict
from itertools import product
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
SOURCE=Path(__file__).resolve().parent
OWNER=ROOT/'research/p200_operational_protocols'
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(OWNER))
import protocol as native  # noqa: E402
import commutation  # noqa: E402
import embedded_observer as observers  # noqa: E402
import non_signaling as counts  # noqa: E402

LEAN_SOURCES=tuple('research/p200_operational_protocols/lean/'+name+'.lean'
                   for name in ('Protocol','Commutation','Observers','NonSignaling'))
PINS=tuple('research/p200_operational_protocols/'+name for name in (
    'protocol.py','commutation.py','embedded_observer.py','non_signaling.py',
    'README.md','CLAIMS.md'))+LEAN_SOURCES+('textbook/reasoning_lab/protocols.py',)
INPUTS=((0,0),(0,1),(0,2),(1,1))
PROBES=(('keep the value',lambda n:n),('always write 0',lambda n:0),
        ('even/odd remainder',lambda n:n%2))
PROCEDURES=(('read A',('readA',)),
    ('read A, then advance A',('readA','advanceA')),
    ('advance A, then read A',('advanceA','readA')),
    ('read A, advance A, read A again',('readA','advanceA','readA')),
    ('read both targets',('readA','readB')),
    ('read A and advance it',('disturbA',)),
    ('advance A, then read B',('advanceA','readB')),
    ('advance A, send, receive, read B',('advanceA','send','receive','readB')))
PAIRS=(('read A / advance A',('readA','advanceA')),
       ('read B / advance A',('readB','advanceA')),
       ('read B / advance message',('readB','advanceM')),
       ('read A / read B',('readA','readB')),
       ('read-and-advance A / advance A',('disturbA','advanceA')),
       ('read-and-advance A / leave A alone',('disturbA','identityA')))
LABELS={'readA':'read A into record A','readB':'read B into record B',
        'advanceA':'advance A','advanceM':'advance message',
        'disturbA':'read A, then advance it','identityA':'leave A unchanged',
        'send':'copy A into message','receive':'copy message into B'}


def cycle(n):
    return (n+1)%3


def operate(state,name,probe):
    if name=='readA': return native.non_disturbing_readout_1(state,probe)
    if name=='readB': return native.non_disturbing_readout_2(state,probe)
    if name=='advanceA': return native.intervene_l1(state,cycle)
    if name=='advanceM': return native.intervene_m(state,cycle)
    if name=='disturbA': return native.disturbing_readout_1(state,probe,cycle,cost=1)
    if name=='identityA': return commutation.step_l1(lambda n:n)(state)
    # Book adapters for the exact field updates of the owner's Lean relay.
    # The Python contrast helper constructs fresh states internally;
    # it is not used as a replay operation on arbitrary supplied states.
    if name=='send': return state.with_update(native.Locus.M,state.l1)
    if name=='receive': return state.with_update(native.Locus.L2,state.m)
    raise ValueError('Unknown supplied protocol operation: '+name)


def independent_step(state,name,probe):
    values=list(state.to_tuple())
    if name=='readA': values[3]=probe(values[0])
    elif name=='readB': values[4]=probe(values[1])
    elif name=='advanceA': values[0]=(values[0]+1)%3
    elif name=='advanceM': values[2]=(values[2]+1)%3
    elif name=='disturbA':
        values[3]=probe(values[0]);values[0]=(values[0]+1)%3;values[5]+=1
    elif name=='send': values[2]=values[0]
    elif name=='receive': values[1]=values[2]
    elif name!='identityA': raise ValueError(name)
    return native.CarrierState(*values)


def timeline(start,names,probe):
    state=start;rows=[]
    for name in names:
        after=operate(state,name,probe)
        assert after==independent_step(state,name,probe)
        rows.append({'operation':name,'before':asdict(state),'after':asdict(after)})
        state=after
    return {'start':asdict(start),'operations':list(names),'rows':rows,'end':asdict(state),
            'records_match':native.coincidence_evaluator(state),
            'targets_match':state.l1==state.l2,
            'current_probe_values':[probe(state.l1),probe(state.l2)]}


def order_case(start,names,probe):
    forward=timeline(start,names,probe);reverse=timeline(start,names[::-1],probe)
    same=commutation.check_commutation(start,lambda s:operate(s,names[0],probe),
                                      lambda s:operate(s,names[1],probe))
    assert same==(forward['end']==reverse['end'])
    return {'forward':forward,'reverse':reverse,'commutes':same}


def ensemble(probe,values=(0,0,1,2)):
    states=[native.prepare_symmetric(native.CarrierState(),n) for n in values]
    first,second=observers.create_duplicate_observers(probe)
    before=[observers.run_joint_protocol(first,second,s) for s in states]
    changed=[observers.run_joint_protocol(first,second,native.intervene_l1(s,cycle)) for s in states]
    left=counts.compute_marginal_r2_distribution(states,lambda n:n,second)
    right=counts.compute_marginal_r2_distribution(states,cycle,second)
    assert left==right and counts.total_variation_distance(left,right)==0
    return {'supplied_rows':len(states),'physical_observations':0,
            'before_agreements':sum(native.coincidence_evaluator(s) for s in before),
            'after_local_agreements':sum(native.coincidence_evaluator(s) for s in changed),
            'remote_counts_before':{str(k):str(v) for k,v in sorted(left.items())},
            'remote_counts_after':{str(k):str(v) for k,v in sorted(right.items())}}


def build_packet():
    for module in (native,commutation,observers,counts):
        assert Path(module.__file__).resolve().parent==OWNER,'Unexpected protocol source origin'
    histories={f'{i}_{q}_{j}':timeline(native.CarrierState(l1=a,l2=b),names,probe)
               for i,(a,b) in enumerate(INPUTS) for q,(_,probe) in enumerate(PROBES)
               for j,(_,names) in enumerate(PROCEDURES)}
    orders={f'{i}_{q}_{j}':order_case(native.CarrierState(l1=a,l2=b),names,probe)
            for i,(a,b) in enumerate(INPUTS) for q,(_,probe) in enumerate(PROBES)
            for j,(_,names) in enumerate(PAIRS)}
    assert histories['3_0_1']['end']['l1']==2 and histories['3_0_1']['end']['r1']==1
    assert histories['3_0_3']['end']['r1']==2
    assert histories['2_2_4']['records_match'] and not histories['2_2_4']['targets_match']
    assert not orders['0_0_0']['commutes'] and orders['0_0_1']['commutes']
    assert not orders['0_0_4']['commutes'] and orders['0_0_5']['commutes']
    readA=native.create_non_disturbing_readout(native.Locus.L1,native.Locus.R1)
    false_metadata=commutation.ProcessStep('claimed B operation',native.Locus.L1,cycle,
        frozenset({native.Locus.L2}),frozenset({native.Locus.L2}))
    assert readA.footprint.is_disjoint(false_metadata.footprint)
    assert not commutation.check_commutation(native.CarrierState(),readA.execute,false_metadata.execute)
    alias=native.create_non_disturbing_readout(native.Locus.L1,native.Locus.L1,lambda n:n+1)
    assert not alias.is_disturbing and alias.execute(native.CarrierState()).l1==1
    zero_price=native.disturbing_readout_1(native.CarrierState(),lambda n:n,cycle,cost=0)
    assert zero_price.l1==1 and zero_price.dist==0
    limits=native.CapacityBounds(3,3,2,2,2)
    assert native.CarrierState(dist=10000).is_valid(bounds=limits)
    assert counts.simulate_causal_propagation_contrast(native.CarrierState(),1)=={
        'spacelike_shift_detected':False,'causal_shift_detected':True,
        'information_transferred_post_coupling':True}
    practice_stale=timeline(native.CarrierState(l1=2),('readA','advanceA','readB'),lambda n:n)
    assert (practice_stale['end']['l1'],practice_stale['end']['r1'],practice_stale['end']['r2'])==(0,2,0)
    practice_relay=timeline(native.CarrierState(l1=2,m=1),('receive','send','readB'),lambda n:n)
    assert (practice_relay['end']['l2'],practice_relay['end']['m'],practice_relay['end']['r2'])==(1,2,1)
    practice_counts=ensemble(lambda n:n,(2,0,2))
    assert practice_counts['before_agreements']==3 and practice_counts['after_local_agreements']==0
    assert practice_counts['remote_counts_after']=={'0':'1/3','2':'2/3'}
    pins={name:hashlib.sha256((ROOT/name).read_text(encoding='utf-8').encode()).hexdigest()
          for name in PINS}
    return {'authority_effect':'None','classification':'supplied six-register protocol model',
            'formal_carrier':'six unbounded natural-number fields','physical_observations':0,
            'source_text_sha256':pins,'digest_mode':'UTF-8 source text with LF normalization',
            'inputs':[{'l1':a,'l2':b} for a,b in INPUTS],
            'probe_names':[name for name,_ in PROBES],
            'procedure_names':[name for name,_ in PROCEDURES],
            'pair_names':[name for name,_ in PAIRS],'operation_labels':LABELS,
            'histories':histories,'orders':orders,
            'ensembles':{str(q):ensemble(probe) for q,(_,probe) in enumerate(PROBES)},
            'practice':{'stale':practice_stale,'relay':practice_relay,'counts':practice_counts},
            'scope_controls':{'footprint_labels_alone_prove_commutation':False,
                'instrument_flag_alone_proves_target_unchanged':False,
                'zero_diagnostic_proves_target_unchanged':False,
                'python_capacity_check_bounds_diagnostic':False}}


def check_population():
    comparisons=0
    for a,b,m,r1,r2,diagnostic in product(range(3),range(3),range(2),range(2),range(2),range(2)):
        state=native.CarrierState(a,b,m,r1,r2,diagnostic)
        for table in product(range(3),repeat=3):
            probe=lambda n,values=table:values[n%3]
            for _,names in PAIRS:
                a1=operate(operate(state,names[0],probe),names[1],probe)
                b1=operate(operate(state,names[1],probe),names[0],probe)
                a2=independent_step(independent_step(state,names[0],probe),names[1],probe)
                b2=independent_step(independent_step(state,names[1],probe),names[0],probe)
                assert (a1,b1)==(a2,b2)
                if names in (('readB','advanceA'),('readB','advanceM'),('readA','readB'),('disturbA','identityA')):
                    assert a1==b1
                comparisons+=1
    assert comparisons==23328
    return comparisons


def check_recorded(directory=SOURCE):
    wanted=json.loads(json.dumps(build_packet()))
    if json.loads((directory/'protocols.json').read_text(encoding='utf-8'))!=wanted:
        raise ValueError('Protocol packet differs from the source-backed cases')
    from textbook.search_lab.build_results import render
    if (directory/'protocols.html').read_text(encoding='utf-8')!=render(
            SOURCE,template_name='protocols.template.html',packet_name='protocols.json'):
        raise ValueError('Protocol desk differs from the source-backed cases')
    return {'histories':96,'record_predictions':192,'orders':72,'ensembles':3,
            'physical_observations':0}


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true');parser.add_argument('--population',action='store_true')
    args=parser.parse_args()
    if args.write:
        (SOURCE/'protocols.json').write_text(json.dumps(build_packet(),indent=1,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
        from textbook.search_lab.build_results import build
        build(SOURCE,SOURCE/'protocols.html',template_name='protocols.template.html',packet_name='protocols.json')
    print(check_recorded())
    if args.population: print({'bounded_order_comparisons':check_population()})
