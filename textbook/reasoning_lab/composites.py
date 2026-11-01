"""P203 teaching records from native operations; AuthorityEffect: None."""
from dataclasses import replace
from fractions import Fraction
from itertools import product,permutations,combinations
from pathlib import Path
import hashlib,json,sys

ROOT=Path(__file__).resolve().parents[2];SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from research.p203_composite_systems import composite_systems as native  # noqa: E402

LOCI=('a1','a2','b1','b2')
LEAN_SOURCE='research/p203_composite_systems/lean/CompositeSystems.lean'
PINS=('research/p203_composite_systems/composite_systems.py',LEAN_SOURCE,
      'research/p203_composite_systems/README.md','research/p203_composite_systems/CLAIMS.md',
      'textbook/reasoning_lab/composites.py')
PREPARATIONS=('One zero record','Two matching pairs','Two opposite pairs','Four records with a repeat')
PROCEDURES=('Change A2 only','Change A2, then copy A2 to B1','Copy A2 to B1, then change A2',
            'Flip B1 between 0 and 1','Set B1 to zero')
READOUTS=('B1 value','B1 even/odd','Always zero')
MENUS=('Two separate copy rules','Add the A2 to B1 copy','Add a joint constant write','Hide the A2 read in its label')
PAIRS=(('a1','b2'),('a2','b1'),('a1','a2'))
SHARE_ANSWERS=('0','1/4','1/2','3/4','1')
DISTANCE_ANSWERS=('unreachable','0','1','2','3')

def state(values):
    if len(values)!=4 or any(type(v) is not int or v<0 for v in values):
        raise ValueError('Supply four nonnegative integer fields')
    return native.CarrierState(dict(zip(LOCI,values)))

def fields(s):return [s[k] for k in LOCI]

def transition(name,reads,writes,fn):
    return native.Transition(name,frozenset(reads),frozenset(writes),fn)

def operations():
    return (transition('change_A2',('a2',),('a2',),lambda s:{'a2':s['a2']+1}),
            transition('relay',('a2',),('b1',),lambda s:{'b1':s['a2']}),
            transition('flip_B1',('b1',),('b1',),lambda s:{'b1':1-s['b1']}),
            transition('zero_B1',(),('b1',),lambda s:{'b1':0}))

def preparations(index):
    rows=(((0,0,0,0),),((0,0,0,0),(0,1,1,0)),
          ((0,0,1,0),(0,1,0,0)),((0,0,0,0),(0,0,0,0),(0,1,0,0),(0,1,1,0)))
    return [state(v) for v in rows[index]]

def probe(index,value):return value if index==0 else value%2 if index==1 else 0

def observable(index):
    return native.Observable(READOUTS[index],frozenset({'b1'}),lambda s:probe(index,s['b1']))

def apply_procedure(index,s):
    change,relay,flip,zero=operations()
    baseline=relay.apply(s) if index in (1,2) else s
    altered=(change.apply(s) if index==0 else relay.apply(change.apply(s)) if index==1
             else change.apply(relay.apply(s)) if index==2 else flip.apply(s) if index==3 else zero.apply(s))
    return baseline,altered

def distribution(rows,obs):
    return {str(k):str(v) for k,v in sorted(native.compute_marginal_distribution(rows,obs).items())}

def network_case(preparation,procedure,readout):
    initial=preparations(preparation);obs=observable(readout);rows=[];base=[];altered=[]
    for i,s in enumerate(initial):
        b,t=apply_procedure(procedure,s);base.append(b);altered.append(t)
        rows.append({'index':i,'initial':fields(s),'baseline':fields(b),'altered':fields(t),
                     'before_mark':obs.measure(b),'after_mark':obs.measure(t)})
    p=native.compute_marginal_distribution(base,obs);q=native.compute_marginal_distribution(altered,obs)
    tvd=native.total_variation_distance(p,q)
    return {'preparation':preparation,'procedure':procedure,'readout':readout,'rows':rows,
            'baseline_shares':distribution(base,obs),'altered_shares':distribution(altered,obs),
            'answer':str(tvd),'marks_changed':sum(r['before_mark']!=r['after_mark'] for r in rows),
            'b_fields_changed':sum(r['baseline'][2:]!=r['altered'][2:] for r in rows),
            'baseline_rule':'Copy A2 to B1' if procedure in (1,2) else 'Keep the starting record'}

def graph_operations(menu):
    local=[transition('copy_A',('a1',),('a2',),lambda s:{'a2':s['a1']}),
           transition('copy_B',('b1',),('b2',),lambda s:{'b2':s['b1']})]
    extra=(operations()[1] if menu==1 else
           transition('constant_pair',(),('a2','b1'),lambda s:{'a2':7,'b1':8}) if menu==2 else
           transition('hidden_read',(),('b1',),lambda s:{'b1':s['a2']}))
    return local if menu==0 else local+[extra]

def graph_case(menu,pair):
    ops=graph_operations(menu);g=native.InteractionGraph.derive_from_operations(LOCI,ops)
    u,v=PAIRS[pair];distance=g.shortest_path_distance(u,v)
    return {'menu':menu,'pair':pair,'from':u,'to':v,'edges':sorted(sorted(e) for e in g.edges),
            'answer':'unreachable' if distance is None else str(distance),
            'operations':[{'name':t.name,'reads':sorted(t.reads),'writes':sorted(t.writes)} for t in ops],
            'executed_operations':0}

def native_limits():
    s=state((0,1,0,0));cut=native.BipartiteCut(frozenset(LOCI[:2]),frozenset(LOCI[2:]))
    liar=native.Observable('mislabelled',frozenset({'b1'}),lambda x:x['a2'])
    report=native.verify_operational_non_signaling([s],cut,[operations()[0]],liar)
    assert not report['non_signaling_satisfied'] and report['max_tvd']==1
    hidden=graph_operations(3)[-1]
    assert hidden.apply(s)['b1']==1 and graph_case(3,1)['answer']=='unreachable'
    bad=transition('invalid_write',(),('a2',),lambda x:{'b1':99})
    try:bad.apply(s)
    except ValueError:pass
    else:raise AssertionError('Write guard did not reject undeclared update')
    # The frozen dataclass wraps a mutable dict: callbacks must not mutate it.
    def mutate(x):x.values['b1']=99;return {}
    escaped=state((0,0,0,0));transition('mutating_callback',(),(),mutate).apply(escaped)
    assert escaped['b1']==99
    # A crossing declaration alone neither changes every readout nor forces TVD>0.
    crossing=transition('unused_A_read',('a2','b1'),('b1',),lambda x:{'b1':1-x['b1']})
    balanced=preparations(1)
    assert native.verify_leaky_intervention_divergence(balanced,cut,crossing,observable(0))==0
    pair=native.DuplicateObserverPair('a1','b1',lambda x:x)
    unpaired=state((0,0,1,0))
    unchecked=native.verify_duplicate_observer_agreement([unpaired],pair,{k:k for k in LOCI})
    assert unchecked['symmetric_count']==1 and not unchecked['duplicate_agreement_satisfied']
    empty=native.verify_duplicate_observer_agreement([],pair,{k:k for k in LOCI})
    assert empty['symmetric_agreement_rate']==1 and not empty['duplicate_agreement_satisfied']
    return {'write_dictionary_guard_rejects_extra_keys':True,'read_labels_are_not_checked':True,
            'observable_labels_are_not_checked':True,'shallow_frozen_state_can_be_mutated':True,
            'crossing_can_have_zero_share_distance':True,'observer_helper_does_not_validate_pair_map':True,
            'empty_observer_rate_is_not_evidence':True}

def composition_cases():
    a=native.CarrierState({'a':2});b=native.CarrierState({'b':5});c=native.CarrierState({'c':7})
    checked=native.verify_associativity_isomorphism(a,b,c);assert all(checked.values())
    try:a.tensor(native.CarrierState({'a':2}))
    except ValueError:pass
    else:raise AssertionError('Shared names silently merged')
    return {'left':dict(a.tensor(b).tensor(c).values),'right':dict(a.tensor(b.tensor(c)).values),
            'shared_name_even_same_value_refused':True,'projections_preserved':checked}

def checked_practice():
    a=native.CarrierState({'p':3,'q':8});b=native.CarrierState({'r':5})
    joined=a.tensor(b);assert joined.values=={'p':3,'q':8,'r':5}
    assert joined.project(('q','r')).values=={'q':8,'r':5}
    try:a.tensor(native.CarrierState({'q':8,'r':5}))
    except ValueError:pass
    else:raise AssertionError('Practice overlap was accepted')
    left=((4,9),1);right=(left[0][0],(left[0][1],left[1]));assert right==(4,(9,1))
    s=state((4,2,9,6));baseline,first=apply_procedure(1,s);other,second=apply_procedure(2,s)
    assert fields(baseline)==fields(other)==[4,2,2,6]
    assert fields(first)==[4,3,3,6] and fields(second)==[4,3,2,6]
    assert network_case(3,3,0)['answer']=='1/2' and network_case(3,3,2)['answer']=='0'
    constant=transition('constant_pair',(),('x','y'),lambda s:{'x':7,'y':8})
    g=native.InteractionGraph.derive_from_operations(('x','y'),[constant])
    assert g.edges==frozenset({frozenset({'x','y'})})
    swap={'a1':'b1','a2':'b2','b1':'a1','b2':'a2'}
    g=native.InteractionGraph.derive_from_operations(LOCI,graph_operations(0))
    s=state((3,0,3,8));assert g.is_automorphism(swap) and not native.is_symmetric_state(s,swap)
    assert native.DuplicateObserverPair('a1','b1',lambda x:x).coincidence(s)
    assert native.DuplicateObserverPair('a1','b1',lambda x:x%2).coincidence(state((0,0,2,0)))
    assert native_limits()['observable_labels_are_not_checked']
    return {'changed_tasks_checked':7,'physical_observations':0}

def build_packet():
    assert Path(native.__file__).resolve()==ROOT/'research/p203_composite_systems/composite_systems.py'
    cases={f'{a}_{b}_{c}':network_case(a,b,c) for a,b,c in product(range(4),range(5),range(3))}
    graphs={f'{a}_{b}':graph_case(a,b) for a,b in product(range(4),range(3))}
    assert cases['1_3_0']['answer']=='0' and cases['1_3_0']['marks_changed']==2
    assert cases['0_1_0']['answer']=='1' and cases['0_2_0']['answer']=='0'
    assert graphs['1_0']['answer']==graphs['2_0']['answer']=='3'
    return {'authority_effect':'None','classification':'supplied P203 definitions and explicit caller premises',
            'physical_observations':0,'preparations':list(PREPARATIONS),'procedures':list(PROCEDURES),
            'readouts':list(READOUTS),'menus':list(MENUS),'pairs':[list(p) for p in PAIRS],
            'share_answers':list(SHARE_ANSWERS),'distance_answers':list(DISTANCE_ANSWERS),
            'cases':cases,'graphs':graphs,'composition':composition_cases(),'native_limits':native_limits(),
            'practice':checked_practice(),
            'source_text_sha256':{p:hashlib.sha256((ROOT/p).read_text(encoding='utf-8').encode()).hexdigest() for p in PINS},
            'digest_mode':'UTF-8/LF source text','formal_carrier':'unbounded Nat fields in Lean; Python integer maps'}

def independent_distribution(values):
    return {v:Fraction(values.count(v),len(values)) for v in set(values)} if values else {}

def check_population():
    transitions=0
    for values,procedure,readout in product(product(range(3),repeat=4),range(5),range(3)):
        # Flip uses a binary B1, stated separately rather than silently clipping.
        if procedure==3 and values[2]>1:continue
        b,t=apply_procedure(procedure,state(values));a1,a2,b1,b2=values
        expected_b=[a1,a2,a2 if procedure in (1,2) else b1,b2]
        expected_t=[a1,a2+1,a2+1 if procedure==1 else a2 if procedure==2 else b1,b2]
        if procedure==3:expected_t=[a1,a2,1-b1,b2]
        if procedure==4:expected_t=[a1,a2,0,b2]
        assert fields(b)==expected_b and fields(t)==expected_t
        assert observable(readout).measure(t)==probe(readout,expected_t[2]);transitions+=1
    lists=0
    for length in range(5):
        for raw in product(range(4),repeat=length):
            ensemble=[state((0,n//2,n%2,0)) for n in raw]
            for procedure,readout in product(range(5),range(3)):
                paired=[apply_procedure(procedure,s) for s in ensemble];obs=observable(readout)
                before=[obs.measure(b) for b,_ in paired];after=[obs.measure(t) for _,t in paired]
                p=independent_distribution(before);q=independent_distribution(after)
                assert native.compute_marginal_distribution([b for b,_ in paired],obs)==p
                assert native.compute_marginal_distribution([t for _,t in paired],obs)==q
                expected=sum((abs(p.get(k,0)-q.get(k,0)) for k in p.keys()|q.keys()),Fraction())/2
                assert native.total_variation_distance(p,q)==expected;lists+=1
    graph_pairs=0;all_edges=list(combinations(LOCI,2))
    for mask in range(64):
        edges={frozenset(e) for i,e in enumerate(all_edges) if mask>>i&1}
        ops=[transition('edge',tuple(e)[:1],tuple(e)[1:],lambda s:{}) for e in sorted(edges,key=lambda e:sorted(e))]
        g=native.InteractionGraph.derive_from_operations(LOCI,ops);assert g.edges==edges
        distances={(u,v):0 if u==v else 1 if frozenset({u,v}) in edges else 99 for u in LOCI for v in LOCI}
        for k in LOCI:
            for u,v in product(LOCI,repeat=2):distances[u,v]=min(distances[u,v],distances[u,k]+distances[k,v])
        for u,v in product(LOCI,repeat=2):
            assert g.shortest_path_distance(u,v)==(None if distances[u,v]==99 else distances[u,v]);graph_pairs+=1
        for perm in permutations(LOCI):
            mapping=dict(zip(LOCI,perm));expected={frozenset(mapping[v] for v in e) for e in edges}==edges
            assert g.is_automorphism(mapping)==expected
            if expected:
                assert all(g.shortest_path_distance(u,v)==g.shortest_path_distance(mapping[u],mapping[v]) for u,v in product(LOCI,repeat=2))
    composition=0
    for a,b,c in product(range(4),repeat=3):
        sa,sb,sc=(native.CarrierState({key:value}) for key,value in zip(('a','b','c'),(a,b,c)))
        assert all(native.verify_associativity_isomorphism(sa,sb,sc).values())
        assert sa.tensor(sb).tensor(sc).values=={'a':a,'b':b,'c':c};composition+=1
    return {'state_procedure_readout_cases':transitions,'ordered_list_comparisons':lists,
            'graph_pair_distances':graph_pairs,'graph_permutations':64*24,'composition_triples':composition}

def check_recorded(directory=SOURCE):
    if json.loads((directory/'composites.json').read_text(encoding='utf-8'))!=build_packet():
        raise ValueError('Composite packet differs from source-backed cases')
    from textbook.search_lab.build_results import render
    if (directory/'composites.html').read_text(encoding='utf-8')!=render(SOURCE,template_name='composites.template.html',packet_name='composites.json'):
        raise ValueError('Composite desk differs from its checked renderer')
    return {'network_cases':60,'graph_cases':12,'physical_observations':0}

if __name__=='__main__':
    if '--write' in sys.argv:
        (SOURCE/'composites.json').write_text(json.dumps(build_packet(),indent=2)+'\n',encoding='utf-8',newline='\n')
        from textbook.search_lab.build_results import build
        build(SOURCE,SOURCE/'composites.html',template_name='composites.template.html',packet_name='composites.json')
    print(check_recorded())
    if '--population' in sys.argv:print(check_population())
