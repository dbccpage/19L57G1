"""Source-backed P201 teaching cases; AuthorityEffect: None. No measurements."""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from research.p201_relational_spacetime import relational_spacetime as native  # noqa: E402

DIM=native.PhysicalDimension
LEAN_SOURCE='research/p201_relational_spacetime/lean/RelationalSpacetime.lean'
PINS=('research/p201_relational_spacetime/relational_spacetime.py',LEAN_SOURCE,
      'research/p201_relational_spacetime/README.md',
      'research/p201_relational_spacetime/CLAIMS.md','textbook/reasoning_lab/calibration.py')
STANDARDS=tuple(native.CalibrationStandard(name,DIM.LENGTH,F(base))
                for name,base in (('V',1),('U',2),('W',4)))
OBJECTS=(('X',F(12)),('Y',F(18)),('zero length',F(0)))


def check_quantity(q):
    """Book-side premises; the native dataclasses do not enforce these."""
    if not isinstance(q.dimension,DIM) or q.dimension!=q.standard.dimension:
        raise ValueError('Quantity kind and standard kind must agree')
    if type(q.value) is not F or type(q.standard.base_magnitude) is not F:
        raise ValueError('Use exact Fraction values and standards')
    if q.value<0 or q.standard.base_magnitude<=0:
        raise ValueError('This lesson uses nonnegative readings and positive standards')
    return q


def quantity(value,standard):
    return check_quantity(native.RelationalQuantity(F(value),standard.dimension,standard))


def magnitude(q):
    check_quantity(q)
    return q.value*q.standard.base_magnitude


def convert(q,new_standard,scale):
    check_quantity(q)
    check_quantity(native.RelationalQuantity(q.value,q.dimension,new_standard))
    if type(scale) is not F or scale<=0:
        raise ValueError('The unit scale must be an exact positive fraction')
    if new_standard.base_magnitude!=scale*q.standard.base_magnitude:
        raise ValueError('Scale must match the new standard divided by the old standard')
    result=native.RelationalQuantity.rescale_standard(q,new_standard,scale)
    if magnitude(result)!=magnitude(q):
        raise ValueError('Conversion changed the represented magnitude')
    return result


def ratio(a,b):
    check_quantity(a);check_quantity(b)
    return native.compute_dimensionless_ratio(a,b)


def record(q):
    return {'number':str(q.value),'kind':q.dimension.value,'standard':q.standard.name,
            'standard_size':str(q.standard.base_magnitude),'magnitude':str(magnitude(q))}


def native_limits():
    """Retain counterexamples to unchecked API premises; never change the owner."""
    u,w=STANDARDS[1],STANDARDS[2];q=quantity(6,u)
    wrong=native.RelationalQuantity.rescale_standard(q,w,F(1,2))
    assert wrong.value==12 and wrong.value*w.base_magnitude==48 and magnitude(q)==12
    zero=native.CalibrationStandard('zero standard',DIM.LENGTH,F(0))
    malformed=native.RelationalQuantity(F(1),DIM.LENGTH,zero)
    try:
        native.compute_dimensionless_ratio(q,malformed)
    except ZeroDivisionError:
        zero_error='ZeroDivisionError'
    else:
        raise AssertionError('Review changed native zero-standard behavior')
    duration=native.CalibrationStandard('T',DIM.DURATION,F(2))
    wrong_kind=native.RelationalQuantity(F(3),DIM.LENGTH,duration)
    assert native.compute_dimensionless_ratio(q,wrong_kind).is_ok()
    for bad in (malformed,wrong_kind,native.RelationalQuantity(F(-1),DIM.LENGTH,u)):
        try:check_quantity(bad)
        except ValueError:pass
        else:raise AssertionError('Book premises accepted malformed quantity')
    try:convert(q,w,F(1,2))
    except ValueError:pass
    else:raise AssertionError('Wrong scale accepted')
    return {'raw_wrong_scale_changes_magnitude':True,'raw_zero_standard_error':zero_error,
            'raw_kind_mismatch_accepted':True,'book_checks_refuse_these_inputs':True,
            'python_signed_fractions_exceed_lean_nat_quantity':True}


def build_packet():
    assert Path(native.__file__).resolve()==ROOT/'research/p201_relational_spacetime/relational_spacetime.py'
    u=STANDARDS[1];conversions={}
    for i,(name,mag) in enumerate(OBJECTS):
        old=quantity(mag/u.base_magnitude,u)
        for j,new in enumerate(STANDARDS):
            scale=new.base_magnitude/u.base_magnitude
            changed=convert(old,new,scale)
            conversions[f'{i}_{j}']={'object':name,'before':record(old),'after':record(changed),
                'scale':str(scale),'answer':str(changed.value)}
    v=STANDARDS[0];duration=native.CalibrationStandard('T',DIM.DURATION,F(2))
    cases=(('Both readings use U',quantity(6,u),quantity(9,u)),
           ('X uses U; Y uses the smaller V',quantity(6,u),quantity(18,v)),
           ('The first length is zero',quantity(0,u),quantity(9,u)),
           ('The dividing length is zero',quantity(6,u),quantity(0,u)),
           ('Length compared with duration',quantity(6,u),quantity(9,duration)),
           ('Both model lengths are doubled',quantity(12,u),quantity(18,u)))
    comparisons=[]
    for name,a,b in cases:
        result=ratio(a,b)
        answer=str(result.unwrap()) if result.is_ok() else 'refuse'
        comparisons.append({'name':name,'first':record(a),'second':record(b),'answer':answer,
            'reason':None if result.is_ok() else result.unwrap_err()})
    assert comparisons[0]['answer']==comparisons[1]['answer']==comparisons[5]['answer']=='2/3'
    assert comparisons[2]['answer']=='0' and comparisons[3]['answer']==comparisons[4]['answer']=='refuse'
    # Changed practice: another magnitude, unequal standards, and the same-ratio control.
    p=native.CalibrationStandard('P',DIM.LENGTH,F(3));r=native.CalibrationStandard('R',DIM.LENGTH,F(6))
    assert convert(quantity(5,p),r,F(2)).value==F(5,2)
    assert ratio(quantity(5,p),quantity(5,r)).unwrap()==F(1,2)
    assert ratio(quantity(2,p),quantity(4,p)).unwrap()==ratio(quantity(6,p),quantity(12,p)).unwrap()
    assert ratio(quantity(2,p),quantity(8,p)).unwrap()==F(1,4)
    unchecked=native.RelationalQuantity.rescale_standard(quantity(5,p),r,F(1,2))
    assert unchecked.value==10 and magnitude(unchecked)==60 and magnitude(quantity(5,p))==15
    s=native.CalibrationStandard('S',DIM.LENGTH,F(2));t=native.CalibrationStandard('T',DIM.LENGTH,F(6))
    before=[quantity(n,s) for n in (3,9)];after=[quantity(n,t) for n in (3,9)]
    assert [magnitude(q) for q in before]==[6,18] and [magnitude(q) for q in after]==[18,54]
    assert ratio(*before).unwrap()==ratio(*after).unwrap()==F(1,3)
    pins={name:hashlib.sha256((ROOT/name).read_text(encoding='utf-8').encode()).hexdigest() for name in PINS}
    return {'authority_effect':'None','classification':'supplied nonnegative rational calibration examples',
            'formal_scope':'Lean Quantity has Nat numerator and positive Nat denominator; Python Fraction is broader',
            'physical_observations':0,'source_text_sha256':pins,'digest_mode':'UTF-8/LF source text',
            'objects':[name for name,_ in OBJECTS],
            'standards':[{'name':s.name,'size':str(s.base_magnitude)} for s in STANDARDS],
            'conversion_answers':['0','3','9/2','6','9','12','18'],
            'conversions':conversions,'comparisons':comparisons,'native_limits':native_limits(),
            'practice':{'changed_conversion':'5/2','mixed_standard_ratio':'1/2','larger_same_ratio':'1/2'}}


def check_population():
    bases=(F(1,2),F(1),F(2),F(3));values=tuple(F(i) for i in range(6))
    counts={'conversions':0,'same_kind_ratios':0,'common_rescalings':0,'cross_kind_refusals':0}
    for d,value,old_base,new_base in product(DIM,values,bases,bases):
        old=native.CalibrationStandard('old',d,old_base);new=native.CalibrationStandard('new',d,new_base)
        converted=convert(quantity(value,old),new,new_base/old_base)
        assert converted.value*new_base==value*old_base
        counts['conversions']+=1
    for d,a,b,ba,bb in product(DIM,values,values,bases,bases):
        sa=native.CalibrationStandard('A',d,ba);sb=native.CalibrationStandard('B',d,bb)
        qa,qb=quantity(a,sa),quantity(b,sb);result=ratio(qa,qb)
        if b==0:assert result.is_err()
        else:assert result.unwrap()==a*ba/(b*bb)
        counts['same_kind_ratios']+=1
        for common_base in bases:
            common=native.CalibrationStandard('common',d,common_base)
            aa=convert(qa,common,common_base/ba);ab=convert(qb,common,common_base/bb)
            changed=ratio(aa,ab)
            assert changed.is_ok()==result.is_ok()
            if result.is_ok():assert changed.unwrap()==result.unwrap()
            counts['common_rescalings']+=1
    for d,e,a,b,ba,bb in product(DIM,DIM,values,values,bases,bases):
        if d==e:continue
        result=ratio(quantity(a,native.CalibrationStandard('A',d,ba)),quantity(b,native.CalibrationStandard('B',e,bb)))
        assert result.is_err() and 'dimension mismatch' in result.unwrap_err()
        counts['cross_kind_refusals']+=1
    assert counts=={'conversions':384,'same_kind_ratios':2304,'common_rescalings':9216,'cross_kind_refusals':6912}
    return counts


def check_recorded(directory=SOURCE):
    if json.loads((directory/'calibration.json').read_text(encoding='utf-8'))!=build_packet():
        raise ValueError('Calibration packet differs from source-backed cases')
    from textbook.search_lab.build_results import render
    if (directory/'calibration.html').read_text(encoding='utf-8')!=render(SOURCE,template_name='calibration.template.html',packet_name='calibration.json'):
        raise ValueError('Calibration desk differs from its checked renderer')
    return {'conversions':9,'comparisons':6,'physical_observations':0}


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');parser.add_argument('--population',action='store_true');args=parser.parse_args()
    if args.write:
        (SOURCE/'calibration.json').write_text(json.dumps(build_packet(),indent=1,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
        from textbook.search_lab.build_results import build
        build(SOURCE,SOURCE/'calibration.html',template_name='calibration.template.html',packet_name='calibration.json')
    print(check_recorded())
    if args.population:print(check_population())
