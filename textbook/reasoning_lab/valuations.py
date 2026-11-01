"""Source-backed P204 teaching records; AuthorityEffect: None."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[2];SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from research.p204_operational_valuations import valuations as native  # noqa: E402
LEAN_SOURCE='research/p204_operational_valuations/lean/OperationalValuations.lean'
PINS=('research/p204_operational_valuations/valuations.py',LEAN_SOURCE,
      'research/p204_operational_valuations/README.md','research/p204_operational_valuations/CLAIMS.md',
      'textbook/reasoning_lab/valuations.py')
SPACE=native.OutcomeSpace((0,1));GRID=tuple(F(n,4) for n in range(5))
PREPARATIONS=('Always outcome 0','Always outcome 1','Outcome 0 has share 3/4','Equal shares','Outcome 0 has share 1/4')
P0=(F(1),F(0),F(3,4),F(1,2),F(1,4))
RESPONSES=('Always yes','Always no','Yes only on outcome 0','Half response on 0; full response on 1')
EFFECTS=((F(1),F(1)),(F(0),F(0)),(F(1),F(0)),(F(1,2),F(1)))
JOINTS=('Matching 00/11 equally','Opposite 01/10 equally','All four pairs equally','Matching 00/11 with shares 3/4 and 1/4')
JOINT_WEIGHTS=((F(1,2),0,0,F(1,2)),(0,F(1,2),F(1,2),0),(F(1,4),)*4,(F(3,4),0,0,F(1,4)))
PARTITIONS=('A reveals its outcome','A has graded branches','One certain branch and one impossible branch')
PART_FIRST=((F(1),F(0)),(F(1,4),F(3,4)),(F(1),F(1)))
B_RESPONSES=('B yes only on 0','B half response on 0; full response on 1')
ANSWERS=('0','1/4','1/2','5/8','3/4','7/8','1')

def checked_weights(space,mapping):
    if set(mapping)!=set(space.outcomes):raise ValueError('Name every outcome exactly once; no extra labels')
    if any(type(v) is bool or not isinstance(v,(int,F)) for v in mapping.values()):
        raise ValueError('Use exact integers or Fractions, not booleans or floats')
    return mapping

def state(p0):return native.OperationalState(SPACE,checked_weights(SPACE,{0:p0,1:1-p0}))
def effect(weights):return native.OperationalEffect(SPACE,checked_weights(SPACE,dict(zip(SPACE,weights))))

def pairing_case(preparation,response):
    s=state(P0[preparation]);e=effect(EFFECTS[response]);value=native.evaluate(e,s)
    rows=[{'outcome':i,'share':str(s.probability(i)),'response':str(e.weight(i)),
           'contribution':str(s.probability(i)*e.weight(i))} for i in SPACE]
    assert value==sum((F(r['contribution']) for r in rows),F())
    assert value+native.evaluate(e.complement(),s)==1
    return {'preparation':preparation,'response':response,'rows':rows,'answer':str(value),
            'complement':str(native.evaluate(e.complement(),s))}

def joint_state(index):
    space=native.tensor_outcome_space(SPACE,SPACE)
    return native.OperationalState(space,dict(zip(space,JOINT_WEIGHTS[index])))

def branch_case(joint,partition,response):
    s=joint_state(joint);a=effect(PART_FIRST[partition]);parts=(a,a.complement())
    b=effect(EFFECTS[2 if response==0 else 3]);u=native.OperationalEffect.unit_effect(SPACE)
    report=native.verify_non_signaling_across_cut(s,SPACE,SPACE,parts,b)
    rows=[]
    for index,e in enumerate(parts):
        chance=native.evaluate(native.tensor_product_effects(e,u),s)
        both=native.evaluate(native.tensor_product_effects(e,b),s)
        rows.append({'branch':index,'a_weights':[str(e.weight(i)) for i in SPACE],
                     'chance':str(chance),'joint_yes':str(both),
                     'conditional':'undefined' if chance==0 else str(both/chance)})
    marginal=native.marginal_state_b(s,SPACE,SPACE)
    assert report['non_signaling'] and sum((F(r['joint_yes']) for r in rows),F())==report['marginal_eval']
    return {'joint':joint,'partition':partition,'response':response,
            'joint_rows':[{'a':a,'b':b,'share':str(s.probability((a,b)))} for a,b in s.space],
            'rows':rows,'marginal':[str(marginal.probability(i)) for i in SPACE],
            'answer':str(report['summed_eval']),'unit_eval':str(report['unit_eval'])}

def mixture_and_square():
    s0,s1=state(F(1)),state(F(0));e0,e1=effect((1,0)),effect((0,1))
    mixes=[]
    for p,q in product(GRID,repeat=2):
        s=native.convex_combination_states((p,1-p),(s0,s1))
        e=native.convex_combination_effects((q,1-q),(e0,e1))
        expected=p*q+(1-p)*(1-q)
        assert native.evaluate(e,s)==expected and native.verify_bilinearity((p,1-p),(s0,s1),(q,1-q),(e0,e1))
        mixes.append({'state_first':str(p),'effect_first':str(q),'answer':str(expected)})
    square=native.SquareStateSpace();w1,v1=square.decomposition_diagonal_1();w2,v2=square.decomposition_diagonal_2()
    assert w1!=w2 and v1==v2==square.center_state
    return {'binary_mixtures':mixes,'independent_half_half':'1/2','coordinated_matching':'1',
            'square_vertices':[[str(x) for x in s.vector] for s in square.extreme_states],
            'square_weights':[[str(x) for x in w] for w in (w1,w2)],
            'square_center':[str(x) for x in square.center_state.vector]}

def native_limits():
    # The native constructors ignore keys outside the supplied space.
    s=native.OperationalState(SPACE,{0:1,99:-7});e=native.OperationalEffect(SPACE,{0:1,99:9})
    assert s.vector==(1,0) and e.vector==(1,0)
    for mapping in ({0:1,99:-7},{0:True,1:0}):
        try:checked_weights(SPACE,mapping)
        except ValueError:pass
        else:raise AssertionError('Book input guard accepted ambiguous mapping')
    assert native.OperationalState(SPACE,{0:True}).vector==(1,0)
    other=native.OutcomeSpace((1,0));assert other!=SPACE
    try:native.evaluate(native.OperationalEffect(other,{0:1}),s)
    except ValueError:pass
    else:raise AssertionError('Different outcome order accepted without transport')
    try:native.verify_non_signaling_across_cut(joint_state(0),SPACE,SPACE,(effect((F(1,2),0)),),effect((1,1)))
    except ValueError:pass
    else:raise AssertionError('Incomplete partition accepted')
    extra=native.OutcomeSpace(((0,0),(0,1),(1,0),(1,1),('extra','extra')))
    wider=native.OperationalState(extra,{(0,0):1})
    assert native.marginal_state_b(wider,SPACE,SPACE).vector==(1,0)
    # The raw marginal reducer does not require exact product-space equality.
    return {'extra_keys_ignored_by_native_constructors':True,'bool_is_native_int':True,
            'outcome_order_is_part_of_space_identity':True,'incomplete_partition_refused':True,
            'raw_marginal_can_ignore_zero_mass_extra_outcomes':True,
            'lean_binary_Nat_normalized_weights_are_endpoints':True}

def practice():
    try:native.OperationalState(SPACE,{0:F(2,3),1:F(2,3)})
    except ValueError:pass
    else:raise AssertionError('Unnormalized practice preparation accepted')
    assert effect((1,1)).vector==(1,1)
    assert native.evaluate(effect((F(1,3),1)),state(F(2,3)))==F(5,9)
    mixed=native.convex_combination_states((F(1,3),F(2,3)),(state(1),state(0)))
    assert mixed.vector==(F(1,3),F(2,3))
    try:native.convex_combination_states((F(2,3),F(2,3)),(state(1),state(0)))
    except ValueError:pass
    else:raise AssertionError('Unnormalized practice mixture accepted')
    independent=mixture_and_square()
    assert independent['binary_mixtures'][12]['answer']=='1/2'
    assert native.evaluate(effect((1,0)),state(1))==native.evaluate(effect((0,1)),state(0))==1
    assert native.evaluate(effect((0,1)),state(1))==native.evaluate(effect((1,0)),state(0))==0
    assert native.SquareStateSpace().demonstrates_non_unique_decomposition()
    assert native.ClassicalSimplex(SPACE).is_unique_decomposition(mixed,(F(1,3),F(2,3)))
    assert branch_case(0,0,0)['rows'][0]['conditional']=='1'
    assert branch_case(0,0,0)['answer']=='1/2'
    assert branch_case(0,2,0)['rows'][1]['conditional']=='undefined'
    return {'changed_tasks_checked':8,'physical_observations':0}

def build_packet():
    assert Path(native.__file__).resolve()==ROOT/'research/p204_operational_valuations/valuations.py'
    return {'authority_effect':'None','classification':'supplied P204 finite probability models',
            'physical_observations':0,'preparations':list(PREPARATIONS),'responses':list(RESPONSES),
            'joints':list(JOINTS),'partitions':list(PARTITIONS),'b_responses':list(B_RESPONSES),
            'answers':list(ANSWERS),'cases':{f'{p}_{e}':pairing_case(p,e) for p,e in product(range(5),range(4))},
            'branches':{f'{s}_{a}_{b}':branch_case(s,a,b) for s,a,b in product(range(4),range(3),range(2))},
            'mixtures':mixture_and_square(),'native_limits':native_limits(),'practice':practice(),
            'source_text_sha256':{p:hashlib.sha256((ROOT/p).read_text(encoding='utf-8').encode()).hexdigest() for p in PINS},
            'digest_mode':'UTF-8/LF source text'}

def check_population():
    assert len(mixture_and_square()['binary_mixtures'])==25
    pairings=mixtures=cuts=squares=0
    for p,a,b in product(GRID,repeat=3):
        value=native.evaluate(effect((a,b)),state(p));assert value==a*p+b*(1-p) and 0<=value<=1
        assert value+native.evaluate(effect((a,b)).complement(),state(p))==1;pairings+=1
    for p,q,r,a,b in product(GRID,repeat=5):
        s=native.convex_combination_states((r,1-r),(state(p),state(q)))
        expected_p=r*p+(1-r)*q;assert s.vector==(expected_p,1-expected_p)
        assert native.evaluate(effect((a,b)),s)==a*expected_p+b*(1-expected_p);mixtures+=1
    for counts in product(range(5),repeat=4):
        if sum(counts)!=4:continue
        s=native.OperationalState(native.tensor_outcome_space(SPACE,SPACE),{k:F(n,4) for k,n in zip(product(range(2),repeat=2),counts)})
        for a0,a1,b0,b1 in product(GRID,repeat=4):
            e=effect((a0,a1));b=effect((b0,b1))
            report=native.verify_non_signaling_across_cut(s,SPACE,SPACE,(e,e.complement()),b)
            expected=b0*F(counts[0]+counts[2],4)+b1*F(counts[1]+counts[3],4)
            assert report['non_signaling'] and report['summed_eval']==expected;cuts+=1
    sq=native.SquareStateSpace()
    for counts in product(range(5),repeat=4):
        if sum(counts)!=4:continue
        weights=tuple(F(n,4) for n in counts);s=native.convex_combination_states(weights,sq.extreme_states)
        a,b,c,d=weights;assert s.vector==((a+d)/2,(b+c)/2,(a+b)/2,(c+d)/2)
        simplex=native.ClassicalSimplex(sq.space)
        assert simplex.is_unique_decomposition(s,s.vector)
        rebuilt=simplex.decompose(s);assert tuple(rebuilt.values())==s.vector;squares+=1
    return {'pairings':pairings,'state_mixtures':mixtures,'complete_partition_comparisons':cuts,
            'square_and_indicator_decompositions':squares,'bilinear_mixtures':25}

def check_recorded(directory=SOURCE):
    if json.loads((directory/'valuations.json').read_text(encoding='utf-8'))!=build_packet():
        raise ValueError('Valuation packet differs from source-backed cases')
    from textbook.search_lab.build_results import render
    if (directory/'valuations.html').read_text(encoding='utf-8')!=render(SOURCE,template_name='valuations.template.html',packet_name='valuations.json'):
        raise ValueError('Valuation desk differs from its checked renderer')
    return {'pairing_contexts':20,'branch_contexts':24,'physical_observations':0}

if __name__=='__main__':
    if '--write' in sys.argv:
        (SOURCE/'valuations.json').write_text(json.dumps(build_packet(),indent=2)+'\n',encoding='utf-8',newline='\n')
        from textbook.search_lab.build_results import build
        build(SOURCE,SOURCE/'valuations.html',template_name='valuations.template.html',packet_name='valuations.json')
    print(check_recorded())
    if '--population' in sys.argv:print(check_population())
