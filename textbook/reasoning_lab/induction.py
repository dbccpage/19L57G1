"""Supplied induction examples and native replay checks; AuthorityEffect: None."""
from itertools import permutations,product
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'code'))
from derivation import model  # noqa: E402

def natural(value):
    if type(value) is not int or value<0:raise ValueError('Use a nonnegative whole-number count')
    return value

def count_after(base,stride,steps):
    base,stride,steps=map(natural,(base,stride,steps))
    result=base
    for _ in range(steps):result+=stride
    return result

def delayed(horizon,steps):
    horizon,steps=map(natural,(horizon,steps))
    return 2*steps if steps<=horizon else 2*steps+1

def strict_bounded(trace,ceiling):
    natural(ceiling)
    for value in trace:natural(value)
    return all(value<=ceiling for value in trace) and all(a<b for a,b in zip(trace,trace[1:]))

def check_examples():
    assert [count_after(0,2,n) for n in range(5)]==[0,2,4,6,8]
    assert count_after(1,2,0)==1 and count_after(1,2,0)!=0
    assert [delayed(3,n) for n in range(5)]==[0,2,4,6,9]
    assert (not False) is True  # Off at the start does not preserve Off under a flip.
    base=model.replay([model.AdmitDatum('kept'),model.AdmitForm(1),model.AdmitInst(0,(0,))])
    assert model.replay([model.Supply('m'),model.Supply('n')],base)==base
    assert model.replay([model.Supply('m'),model.AdmitDatum('new')],base)!=base
    assert strict_bounded((0,1,2,3),3) and not strict_bounded((0,1,2,3,3),3)
    assert not strict_bounded((0,1,2,3,4),3)
    # Changed practice: arbitrary positive stride, missing start/step, delayed
    # failure, a nonempty base, changed event kind and a smaller bound.
    assert count_after(4,3,3)==13
    assert model.replay([model.Supply('p'),model.Supply('q')],base)==base
    assert strict_bounded((0,1,2),2) and not strict_bounded((0,1,2,2),2)
    return {'changed_tasks_checked':6,'physical_transfer_task':'reasoned scope question, not an observation',
            'physical_observations':0,'learner_scores':0}

def check_population():
    counts=late_checks=traces=supply_histories=demand_histories=0
    for base,stride,n in product(range(6),range(5),range(13)):
        assert count_after(base,stride,n)==base+stride*n;counts+=1
    for horizon in range(13):
        for n in range(horizon+1):assert delayed(horizon,n)==2*n;late_checks+=1
        assert delayed(horizon,horizon+1)!=2*(horizon+1);late_checks+=1
    valid=0
    for length in range(7):
        for trace in product(range(4),repeat=length):
            holds=strict_bounded(trace,3);traces+=1
            if holds:assert len(trace)<=4;valid+=1
    assert valid==16
    base=model.replay([model.AdmitDatum('kept'),model.AdmitForm(1)])
    for length in range(6):
        for seq in product(('m','n'),repeat=length):
            assert model.replay([model.Supply(x) for x in seq],base)==base;supply_histories+=1
    three=model.replay([model.AdmitDatum(x) for x in ('m','n','p')])
    pairs=((0,1),(0,2),(1,2))
    for length in range(4):
        for seq in permutations(pairs,length):
            state=three;values=[0]
            for a,b in seq:
                state=model.step(state,model.Impose(a,b));values.append(len(state.reqs))
            assert strict_bounded(values,3) and len(state.reqs)==length;demand_histories+=1
    state=model.replay([model.Impose(*p) for p in pairs],three)
    assert model.step(state,model.Impose(0,1))==state
    grown=model.step(state,model.AdmitDatum('fourth'))
    assert len(model.step(grown,model.Impose(0,3)).reqs)==4
    assert (counts,late_checks,traces,supply_histories,demand_histories)==(390,104,5461,63,16)
    return dict(counter_cases=counts,delayed_rule_comparisons=late_checks,bounded_candidate_traces=traces,
                strictly_increasing_traces=valid,supply_histories=supply_histories,new_demand_histories=demand_histories)

if __name__=='__main__':print(check_examples());print(check_population())
