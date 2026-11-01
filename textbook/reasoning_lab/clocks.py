"""P202 clock/readout teaching cases; AuthorityEffect: None. No observations."""
from dataclasses import dataclass,replace
from fractions import Fraction
from itertools import product
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2];SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from research.p201_relational_spacetime import relational_spacetime as native  # noqa: E402

LEAN_SOURCE='research/p201_relational_spacetime/lean/RelationalSpacetime.lean'
PINS=('research/p201_relational_spacetime/relational_spacetime.py',LEAN_SOURCE,
      'research/p201_relational_spacetime/README.md','research/p201_relational_spacetime/CLAIMS.md',
      'textbook/reasoning_lab/clocks.py')
RULES=('Python: fast +1, slow on alternate steps','Lean: fast +2, slow +1')
STARTS=(0,1);SPANS=tuple(range(7));HORIZONS=(0,1,3,5)
RATE_ANSWERS=('refuse','1','2','3','3/2','5/2','5/3')


def natural(n):
    if type(n) is not int or n<0:raise ValueError('Use a nonnegative integer')
    return n


def checked_python(s):
    if tuple(k for k,_ in s.registers)!=('a','b'):
        raise ValueError('The teaching state has exactly the ordered registers a and b')
    for _,v in s.registers:natural(v)
    for v in (s.clock_fast.ticks,s.clock_slow.ticks,s.step_index):natural(v)
    if (s.clock_fast.period,s.clock_slow.period)!=(1,2):
        raise ValueError('The native transition fixes periods 1 and 2; these are not tuning controls')
    return s


@dataclass(frozen=True)
class LeanState:
    """Book execution adapter for the exact Lean field updates, not a native Python state."""
    a:int;b:int;fast:int;slow:int


def setup(rule,a=0,b=3,offsets=(0,0)):
    for v in (a,b,*offsets):natural(v)
    if rule==0:
        s=native.RelationalState.create({'a':a,'b':b})
        return checked_python(replace(s,clock_fast=native.ClockSubsystem(offsets[0],1),
                                      clock_slow=native.ClockSubsystem(offsets[1],2)))
    if rule==1:return LeanState(a,b,*offsets)
    raise ValueError('Unknown supplied clock rule')


def step(rule,s):
    if rule==0:return checked_python(native.step_relational(checked_python(s)))
    if rule==1:return LeanState(s.a+1,s.b+1,s.fast+2,s.slow+1)
    raise ValueError('Unknown supplied clock rule')


def fields(rule,s):
    if rule==0:
        checked_python(s)
        return (s.get_reg('a'),s.get_reg('b'),s.clock_fast.ticks,s.clock_slow.ticks)
    if rule==1:return (s.a,s.b,s.fast,s.slow)
    raise ValueError('Unknown supplied clock rule')


def advance(rule,s,n):
    natural(n)
    for _ in range(n):s=step(rule,s)
    return s


def timeline(rule,start,span,*,a=0,b=3,offsets=(0,0)):
    natural(start);natural(span)
    s=advance(rule,setup(rule,a,b,offsets),start);initial=s
    rows=[{'index':0,'values':list(fields(rule,s))}]
    for k in range(span):
        s=step(rule,s);rows.append({'index':k+1,'values':list(fields(rule,s))})
    first,last=fields(rule,initial),fields(rule,s)
    df,ds=last[2]-first[2],last[3]-first[3]
    if rule==0:
        result=native.measure_relative_clock_rate(initial,s)
        answer=str(result.unwrap()) if result.is_ok() else 'refuse'
    else:answer=str(Fraction(df,ds)) if ds else 'refuse'
    expected_slow=(start+span)//2-start//2 if rule==0 else span
    expected_fast=span if rule==0 else 2*span
    assert (df,ds)==(expected_fast,expected_slow)
    if ds:assert Fraction(df,ds)==Fraction(expected_fast,expected_slow)
    return {'rule':rule,'start':start,'span':span,'rows':rows,
            'fast_change':df,'slow_change':ds,'answer':answer,
            'reason':'No change on the dividing slow counter' if not ds else None}


def countdown(horizon):
    """Separate supplied countermodel: pred on a hidden Nat, lamp on at zero."""
    natural(horizon)
    left,right=horizon,horizon+1;rows=[]
    for k in range(horizon):
        rows.append({'index':k,'left':int(max(left-k,0)==0),'right':int(max(right-k,0)==0)})
    assert all(r['left']==r['right']==0 for r in rows)
    next_row={'index':horizon,'left':1,'right':0}
    return {'horizon':horizon,'left_start':left,'right_start':right,
            'rows':rows,'next':next_row,'answer':'no',
            'classification':'supplied countdown contrast, not the P202 transition'}


def native_limits():
    base=setup(0,a=2,b=3)
    shifted=replace(base,clock_fast=native.ClockSubsystem(10,1),clock_slow=native.ClockSubsystem(7,2),step_index=1)
    assert native.are_future_equivalent(base,shifted,8) and base!=shifted
    assert native.future_trajectory(base,0)==() and native.future_trajectory(base,-1)==()
    assert len(native.future_trajectory(base,3))==3
    assert native.future_trajectory(base,3)[-1]==advance(0,base,2).observable_readout()
    assert native.future_trajectory(base,3)[-1]!=advance(0,base,3).observable_readout()
    incomplete=native.RelationalState.create({'a':0})
    try:native.step_relational(incomplete)
    except KeyError:missing=True
    else:raise AssertionError('Review changed missing-register behavior')
    mislabeled=replace(base,clock_fast=native.ClockSubsystem(0,9),clock_slow=native.ClockSubsystem(0,9))
    reset=native.step_relational(mislabeled)
    assert (reset.clock_fast.period,reset.clock_slow.period)==(1,2)
    # Raw interval subtraction does not certify a replay or increasing counters.
    backwards=replace(base,clock_fast=native.ClockSubsystem(2,1),clock_slow=native.ClockSubsystem(2,2))
    assert native.measure_relative_clock_rate(backwards,base).unwrap()==1
    try:checked_python(mislabeled)
    except ValueError:pass
    else:raise AssertionError('Mislabelled periods accepted')
    try:countdown(-1)
    except ValueError:pass
    else:raise AssertionError('Negative teaching horizon accepted')
    return {'hidden_clocks_can_differ_with_same_register_future':True,
            'raw_zero_and_negative_horizons_are_empty':True,'missing_register_raises_KeyError':missing,
            'period_metadata_does_not_configure_transition':True,
            'raw_rate_does_not_certify_reachability_or_monotone_interval':True,
            'python_three_step_rates':['3','3/2'],'lean_positive_span_rate':'2'}


def build_packet():
    assert Path(native.__file__).resolve()==ROOT/'research/p201_relational_spacetime/relational_spacetime.py'
    cases={f'{r}_{s}_{h}':timeline(r,s,h) for r,s,h in product(range(2),STARTS,SPANS)}
    assert cases['0_0_3']['answer']=='3' and cases['0_1_3']['answer']=='3/2'
    assert cases['0_0_1']['answer']=='refuse' and cases['0_1_1']['answer']=='1'
    assert all(c['answer']=='2' for c in cases.values() if c['rule']==1 and c['span']>0)
    offset=timeline(1,0,2,a=2,b=3,offsets=(10,3))
    assert offset['rows'][-1]['values'][2:]==[14,5] and offset['answer']=='2'
    assert Fraction(14,5)!=2
    # Changed practice: odd starting index, five transitions; nonzero origins.
    pulse=timeline(0,3,5,a=4,b=2,offsets=(20,9))
    assert pulse['answer']=='5/3' and pulse['rows'][0]['values'][2:]==[23,10] and pulse['rows'][-1]['values'][2:]==[28,13]
    uniform=timeline(1,2,3,a=4,b=2,offsets=(20,9))
    assert uniform['answer']=='2' and uniform['rows'][0]['values'][2:]==[24,11] and uniform['rows'][-1]['values'][2:]==[30,14]
    assert countdown(4)['next']=={'index':4,'left':1,'right':0}
    one=setup(1,a=5,b=7);two=setup(1,a=5,b=7,offsets=(99,42))
    assert one!=two and all(fields(1,advance(1,one,k))[:2]==fields(1,advance(1,two,k))[:2] for k in range(9))
    recorded=native.future_trajectory(setup(0,a=1,b=3),2)
    assert recorded==((1,3),(2,0)) and advance(0,setup(0,a=1,b=3),2).observable_readout()==(3,1)
    pins={n:hashlib.sha256((ROOT/n).read_text(encoding='utf-8').encode()).hexdigest() for n in PINS}
    return {'authority_effect':'None','classification':'two supplied clock rules and a separate countdown countermodel',
            'physical_observations':0,'source_text_sha256':pins,'digest_mode':'UTF-8/LF source text',
            'rules':list(RULES),'starts':list(STARTS),'spans':list(SPANS),'rate_answers':list(RATE_ANSWERS),
            'cases':cases,'horizons':list(HORIZONS),'countdowns':{str(h):countdown(h) for h in HORIZONS},
            'offset_example':offset,'native_limits':native_limits(),
            'formal_carrier':'unbounded Nat fields; declared finite samples only'}


def check_population():
    runs=0
    for rule,start,span,a,b,offsets in product(range(2),range(6),range(9),range(3),range(3),((0,0),(10,3))):
        row=timeline(rule,start,span,a=a,b=b,offsets=offsets)
        for k,record in enumerate(row['rows']):
            n=start+k
            wanted=(a+n,(b+n)%4 if n else b,offsets[0]+n,offsets[1]+n//2) if rule==0 else (a+n,b+n,offsets[0]+2*n,offsets[1]+n)
            assert tuple(record['values'])==wanted
        runs+=1
    comparisons=0
    states=[replace(setup(0,a=a,b=b),clock_fast=native.ClockSubsystem(f,1),clock_slow=native.ClockSubsystem(s,2),step_index=start_index)
            for a,b,f,s,start_index in product(range(3),range(3),range(2),range(2),range(2))]
    for a,b in product(states,repeat=2):
        for h in range(5):
            result=native.are_future_equivalent(a,b,h)
            assert result==(h==0 or a.observable_readout()==b.observable_readout())
            # Independent register-only expansion, excluding clocks and names.
            expected_a=tuple((a.get_reg('a')+k,(a.get_reg('b')+k)%4 if k else a.get_reg('b')) for k in range(h))
            expected_b=tuple((b.get_reg('a')+k,(b.get_reg('b')+k)%4 if k else b.get_reg('b')) for k in range(h))
            assert result==(expected_a==expected_b)
            comparisons+=1
    for h in range(33):assert countdown(h)['next']['left']!=countdown(h)['next']['right']
    assert runs==1944 and comparisons==25920
    return {'clock_runs':runs,'python_readout_comparisons':comparisons,'countdown_horizons':33}


def check_recorded(directory=SOURCE):
    if json.loads((directory/'clocks.json').read_text(encoding='utf-8'))!=build_packet():
        raise ValueError('Clock packet differs from source-backed cases')
    from textbook.search_lab.build_results import render
    if (directory/'clocks.html').read_text(encoding='utf-8')!=render(SOURCE,template_name='clocks.template.html',packet_name='clocks.json'):
        raise ValueError('Clock desk differs from its checked renderer')
    return {'clock_cases':28,'countdown_cases':4,'physical_observations':0}


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');parser.add_argument('--population',action='store_true');args=parser.parse_args()
    if args.write:
        (SOURCE/'clocks.json').write_text(json.dumps(build_packet(),indent=1,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
        from textbook.search_lab.build_results import build
        build(SOURCE,SOURCE/'clocks.html',template_name='clocks.template.html',packet_name='clocks.json')
    print(check_recorded())
    if args.population:print(check_population())
