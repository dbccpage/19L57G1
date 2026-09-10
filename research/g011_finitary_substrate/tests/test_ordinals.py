"""Pytest suite for endogenous finitary ordinals."""

from ordinals import Ordinal, Zero, Succ


def test_ordinal_identity_and_equality() -> None:
    z1 = Zero()
    z2 = Ordinal.zero()
    assert z1 == z2
    assert hash(z1) == hash(z2)

    o1 = Ordinal.from_nat(1)
    o2 = Ordinal.zero().succ()
    assert o1 == o2
    assert o1 != z1
    assert z1 != o1

    o3 = Ordinal.from_nat(3)
    assert o3 == Ordinal.zero().succ().succ().succ()
    assert o3 != o1


def test_ordinal_order_relations() -> None:
    z = Ordinal.zero()
    o1 = Ordinal.from_nat(1)
    o2 = Ordinal.from_nat(2)
    o3 = Ordinal.from_nat(3)

    assert z <= z
    assert z < o1
    assert o1 < o2
    assert o2 < o3
    assert z < o3

    assert not (o1 < z)
    assert not (o2 < o1)
    assert not (o1 < o1)

    assert o3 > o2
    assert o2 >= o1
    assert z <= o3

    # Trichotomy
    assert z.compare(z) == 0
    assert z.compare(o1) == -1
    assert o1.compare(z) == 1
    assert o2.compare(o3) == -1
    assert o3.compare(o2) == 1


def test_ordinal_addition() -> None:
    z = Ordinal.zero()
    o2 = Ordinal.from_nat(2)
    o3 = Ordinal.from_nat(3)
    o5 = Ordinal.from_nat(5)

    assert z.add(o3) == o3
    assert o3.add(z) == o3
    assert o2.add(o3) == o5
    assert o3.add(o2) == o5

    # Associativity: (o2 + o3) + o2 == o2 + (o3 + o2)
    assert (o2.add(o3)).add(o2) == o2.add(o3.add(o2))


def test_ordinal_multiplication() -> None:
    z = Ordinal.zero()
    o1 = Ordinal.from_nat(1)
    o2 = Ordinal.from_nat(2)
    o3 = Ordinal.from_nat(3)
    o6 = Ordinal.from_nat(6)

    assert z.mul(o3) == z
    assert o3.mul(z) == z
    assert o1.mul(o3) == o3
    assert o3.mul(o1) == o3
    assert o2.mul(o3) == o6
    assert o3.mul(o2) == o6

    # Distributivity: 2 * (1 + 2) == 2 * 1 + 2 * 2
    lhs = o2.mul(o1.add(o2))
    rhs = (o2.mul(o1)).add(o2.mul(o2))
    assert lhs == rhs


def test_ordinal_predecessor_and_subtraction() -> None:
    z = Ordinal.zero()
    o1 = Ordinal.from_nat(1)
    o3 = Ordinal.from_nat(3)
    o5 = Ordinal.from_nat(5)

    assert z.pred() == z
    assert o1.pred() == z
    assert o3.pred() == Ordinal.from_nat(2)

    assert o5.sub(z) == o5
    assert z.sub(o5) == z
    assert o5.sub(o5) == z
    assert o5.sub(o3) == Ordinal.from_nat(2)
    assert o3.sub(o5) == z  # truncated subtraction

    # Inverse cancellation: (a + b) - b == a
    for a in range(5):
        for b in range(5):
            oa = Ordinal.from_nat(a)
            ob = Ordinal.from_nat(b)
            assert (oa.add(ob)).sub(ob) == oa


def test_ordinal_algebraic_laws_matrix() -> None:
    for a in range(4):
        for b in range(4):
            oa = Ordinal.from_nat(a)
            ob = Ordinal.from_nat(b)

            # Commutativity of addition
            assert oa.add(ob) == ob.add(oa)

            # Commutativity of multiplication
            assert oa.mul(ob) == ob.mul(oa)

            # Multiplicative identity
            assert oa.mul(Ordinal.from_nat(1)) == oa

            # Antisymmetry of le: if a <= b and b <= a then a == b
            if oa <= ob and ob <= oa:
                assert oa == ob


def test_ordinal_error_handling() -> None:
    o = Ordinal.from_nat(2)
    try:
        o.add("invalid")  # type: ignore[arg-type]
        assert False, "expected TypeError"
    except TypeError:
        pass

    try:
        Ordinal.from_nat(-1)
        assert False, "expected ValueError"
    except ValueError:
        pass
