"""Elementary fraction teaching checks; AuthorityEffect: None."""
from fractions import Fraction as F
from itertools import product

def check_examples():
    assert F(3,4)==F(6,8) and F(1,4)!=F(1,8)
    assert F(1,2)+F(1,4)==F(3,4) and F(1,3)+F(1,4)==F(7,12)
    assert F(3,4)+F(1,2)==F(5,4) and F(5,8)-F(1,8)==F(1,2)
    assert F(1,2)*F(3,4)==F(3,8) and F(2,3)*F(9,10)==F(3,5)
    assert F(3,4)/F(1,2)==F(3,2) and F(3,2)*F(1,2)==F(3,4)
    assert F(1,3)/F(1,6)==2 and 2*F(1,6)==F(1,3)
    assert (F(1,2)+F(1,4))*F(2,3)==F(1,2)
    assert F(1,2)+(F(1,4)*F(2,3))==F(2,3)
    assert F(0,4)/F(1,4)==0
    for operation in (lambda:F(3,0),lambda:F(1,4)/F(0,4)):
        try:operation()
        except ZeroDivisionError:pass
        else:raise AssertionError('A zero denominator/divisor was accepted')
    return {'changed_tasks_checked':6,'zero_refusals':2,'physical_observations':0}

def check_population():
    representations=list(product(range(7),range(1,7)))
    additions=products=quotients=refusals=scalings=0
    for a,b in representations:
        for k in range(1,5):assert F(a,b)==F(a*k,b*k);scalings+=1
        for c,d in representations:
            x,y=F(a,b),F(c,d)
            total=x+y;assert total.numerator*(b*d)==(a*d+c*b)*total.denominator;additions+=1
            multiplied=x*y;assert multiplied.numerator*(b*d)==a*c*multiplied.denominator;products+=1
            if c:
                divided=x/y;assert divided.numerator*(b*c)==a*d*divided.denominator
                assert divided*y==x;quotients+=1
            else:
                try:x/y
                except ZeroDivisionError:refusals+=1
                else:raise AssertionError('Zero-value divisor accepted')
    assert (additions,products,quotients,refusals,scalings)==(1764,1764,1512,252,168)
    return {'additions':additions,'products':products,'positive_divisor_quotients':quotients,
            'zero_divisor_refusals':refusals,'positive_scalings':scalings}

if __name__=='__main__':print(check_examples());print(check_population())
