"""Selected native channel calculations; AuthorityEffect: None."""
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[2];SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from research.x300_observer_information import information as native  # noqa: E402
LEAN_SOURCE='research/x300_observer_information/lean/ObserverInformation.lean'
PINS=('research/x300_observer_information/information.py',LEAN_SOURCE,
      'research/x300_observer_information/README.md','research/x300_observer_information/CLAIMS.md',
      'textbook/reasoning_lab/channels.py')
NAMES=('Keep the value','Flip 0 and 1','Reset to 0','Forget into equal chances',
       'Copy with one-quarter flip','Keep 0; randomize 1')
ROWS=(((1,0),(0,1)),((0,1),(1,0)),((1,0),(1,0)),
      ((F(1,2),F(1,2)),)*2,((F(3,4),F(1,4)),(F(1,4),F(3,4))),((1,0),(F(1,2),F(1,2))))
PAIRS=(('A','B'),('A','C'),('B','C'));READOUT={'A':0,'B':0,'C':1}
POSTS=('Keep the stored answer','Flip the stored answer','Reset the stored answer to 0')
POST_MAPS=({0:0,1:1},{0:1,1:0},{0:0,1:0})

def exact(value):
    if type(value) is bool or not isinstance(value,(int,F)):raise ValueError('Use explicit integer or Fraction probabilities')
    value=F(value)
    if not 0<=value<=1:raise ValueError('Probability outside zero to one')
    return value

def make_channel(rows):
    if len(rows)!=2 or any(len(row)!=2 for row in rows):raise ValueError('Use two complete binary rows')
    checked=tuple(tuple(exact(v) for v in row) for row in rows)
    return native.Channel({x:{y:checked[x][y] for y in (0,1)} for x in (0,1)},input_alphabet=(0,1))

def matrix(channel):return tuple(tuple(channel.prob(y,x) for y in (0,1)) for x in (0,1))
def stringify(rows):return [[str(v) for v in row] for row in rows]

def order_case(first,second):
    a,b=make_channel(ROWS[first]),make_channel(ROWS[second])
    left,right=a.compose(b),b.compose(a);lm,rm=matrix(left),matrix(right)
    preparations=[]
    for p in (F(1),F(1,2),F(3,4)):
        dist=native.DiscreteDistribution({0:p,1:1-p})
        sequential=b.apply(a.apply(dist));out=left.apply(dist);reverse=right.apply(dist)
        assert all(sequential.prob(i)==out.prob(i) for i in (0,1))
        preparations.append({'input_p0':str(p),'first_then_second_p0':str(out.prob(0)),
                             'second_then_first_p0':str(reverse.prob(0))})
    return {'first':first,'second':second,'first_rows':stringify(matrix(a)),'second_rows':stringify(matrix(b)),
            'forward_rows':stringify(lm),'reverse_rows':stringify(rm),
            'answer':'yes' if lm==rm else 'no','preparations':preparations}

def record_case(pair,post):
    a,b=PAIRS[pair];initial=native.Channel.deterministic(READOUT)
    final=initial.compose(native.Channel.deterministic(POST_MAPS[post]))
    outputs={x:next(y for y,p in final.transition(x).items() if p==1) for x in READOUT}
    return {'pair':pair,'post':post,'left':a,'right':b,'stored':[READOUT[a],READOUT[b]],
            'processed':[outputs[a],outputs[b]],'answer':'yes' if outputs[a]!=outputs[b] else 'no'}

def limits():
    try:native.DiscreteDistribution({0:F(1,4),1:F(1,4)})
    except native.UnnormalizedDistributionError:pass
    else:raise AssertionError('Malformed row rescaled')
    try:native.DiscreteDistribution({0:0.1,1:0.9})
    except native.FloatProbabilityError:pass
    else:raise AssertionError('Raw float row accepted')
    # Native convenience helpers convert floats before the row guard sees them.
    raw=native.Channel.binary_symmetric(0.1)
    assert raw.prob(1,0)==F(0.1) and raw.prob(1,0)!=F(1,10)
    try:exact(0.1)
    except ValueError:pass
    else:raise AssertionError('Book float guard bypassed')
    extra=native.Channel({0:{0:1},1:{1:1}},input_alphabet=(0,))
    assert extra.input_alphabet==(0,1)
    zero=native.DiscreteDistribution({0:1,1:0});assert zero.support()==(0,) and zero.prob('unknown')==0
    incomplete=native.Channel({0:{0:1}})
    try:make_channel(ROWS[0]).compose(incomplete)
    except KeyError:pass
    else:raise AssertionError('Composition accepted uncovered intermediate output')
    # A chosen preparation does not identify the complete process.
    half=native.DiscreteDistribution({0:F(1,2),1:F(1,2)})
    keep,flip=make_channel(ROWS[0]),make_channel(ROWS[1])
    assert keep.apply(half).items()==flip.apply(half).items() and matrix(keep)!=matrix(flip)
    return {'unnormalized_rows_refused':True,'direct_float_rows_refused':True,
            'native_binary_helper_accepts_exact_binary_float_value':True,
            'input_alphabet_parameter_is_not_an_exact_whitelist':True,
            'support_omits_zero_entries_and_unknown_prob_returns_zero':True,
            'composition_requires_all_positive_intermediate_outputs':True,
            'one_preparation_does_not_identify_channel':True,
            'world_side_information_is_not_readout_only_processing':True}

def practice():
    # Changed rational channel, not one of the recorded named choices.
    c=make_channel(((F(2,3),F(1,3)),(F(1,4),F(3,4))))
    out=c.apply(native.DiscreteDistribution({0:F(3,5),1:F(2,5)}));assert out.prob(0)==F(1,2)
    a=make_channel(ROWS[1]);b=make_channel(ROWS[2]);assert a.compose(b).prob(0,0)==1 and b.compose(a).prob(1,0)==1
    assert record_case(0,1)['answer']=='no' and record_case(1,1)['answer']=='yes'
    copied={x:(0,x) for x in (0,1)};assert all(copied[x][1]==x for x in copied)
    assert limits()['one_preparation_does_not_identify_channel']
    assert multiply_rows(multiply_rows(ROWS[1],ROWS[4]),ROWS[2])==multiply_rows(ROWS[1],multiply_rows(ROWS[4],ROWS[2]))
    try:make_channel(((F(1,4),F(1,4)),(0,1)))
    except native.UnnormalizedDistributionError:pass
    else:raise AssertionError('Practice row silently normalized')
    return {'changed_tasks_checked':7,'physical_observations':0}

def build_packet():
    assert Path(native.__file__).resolve()==ROOT/'research/x300_observer_information/information.py'
    return {'authority_effect':'None','classification':'supplied X300 channel and deterministic readout examples',
            'physical_observations':0,'channel_names':list(NAMES),'pairs':[list(p) for p in PAIRS],
            'postprocessors':list(POSTS),'orders':{f'{a}_{b}':order_case(a,b) for a,b in product(range(6),repeat=2)},
            'records':{f'{p}_{g}':record_case(p,g) for p,g in product(range(3),repeat=2)},
            'native_limits':limits(),'practice':practice(),
            'source_text_sha256':{p:hashlib.sha256((ROOT/p).read_text(encoding='utf-8').encode()).hexdigest() for p in PINS},
            'digest_mode':'UTF-8/LF source text','quantitative_information_metrics':'not used in this selected route'}

def multiply_rows(a,b):
    return tuple(tuple(sum((a[x][y]*b[y][z] for y in (0,1)),F()) for z in (0,1)) for x in (0,1))

def check_population():
    grid=tuple(F(n,4) for n in range(5));all_rows=[((a,1-a),(b,1-b)) for a,b in product(grid,repeat=2)]
    channels=[make_channel(rows) for rows in all_rows];compositions=applications=triples=postpairs=0
    for a,b in product(range(25),repeat=2):
        composed=channels[a].compose(channels[b]);expected=multiply_rows(all_rows[a],all_rows[b])
        assert matrix(composed)==expected;compositions+=1
        for p in grid:
            out=composed.apply(native.DiscreteDistribution({0:p,1:1-p}))
            assert tuple(out.prob(i) for i in (0,1))==tuple(p*expected[0][i]+(1-p)*expected[1][i] for i in (0,1))
            applications+=1
    for a,b,c in product(range(6),repeat=3):
        ca,cb,cc=(make_channel(ROWS[n]) for n in (a,b,c))
        l=matrix(ca.compose(cb).compose(cc));r=matrix(ca.compose(cb.compose(cc)))
        assert l==r==multiply_rows(multiply_rows(ROWS[a],ROWS[b]),ROWS[c]);triples+=1
    for values in product(range(2),repeat=3):
        for gvalues in product(range(2),repeat=2):
            composed=native.Channel.deterministic(dict(enumerate(values))).compose(native.Channel.deterministic(dict(enumerate(gvalues))))
            for x,y in combinations(range(3),2):
                before=values[x]!=values[y];after=gvalues[values[x]]!=gvalues[values[y]]
                assert (composed.transition(x).items()!=composed.transition(y).items())==after
                assert not after or before;postpairs+=1
    assert (compositions,applications,triples,postpairs)==(625,3125,216,96)
    return {'quarter_grid_compositions':compositions,'output_distributions':applications,
            'named_associative_triples':triples,'deterministic_pair_comparisons':postpairs}

def check_recorded(directory=SOURCE):
    if json.loads((directory/'channels.json').read_text(encoding='utf-8'))!=build_packet():raise ValueError('Channel packet differs from source-backed cases')
    from textbook.search_lab.build_results import render
    if (directory/'channels.html').read_text(encoding='utf-8')!=render(SOURCE,template_name='channels.template.html',packet_name='channels.json'):
        raise ValueError('Channel desk differs from its checked renderer')
    return {'order_contexts':36,'record_contexts':9,'physical_observations':0}

if __name__=='__main__':
    if '--write' in sys.argv:
        (SOURCE/'channels.json').write_text(json.dumps(build_packet(),indent=2)+'\n',encoding='utf-8',newline='\n')
        from textbook.search_lab.build_results import build
        build(SOURCE,SOURCE/'channels.html',template_name='channels.template.html',packet_name='channels.json')
    print(check_recorded())
    if '--population' in sys.argv:print(check_population())
