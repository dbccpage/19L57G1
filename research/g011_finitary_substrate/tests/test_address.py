"""Pytest suite for hierarchical tree addresses."""

from ordinals import Ordinal
from address import Address, Root, Child


def test_address_construction_and_identity() -> None:
    r1 = Address.root()
    r2 = Root()
    assert r1 == r2
    assert r1.is_root()
    assert r1.depth() == Ordinal.zero()
    assert r1.parent() is None
    assert r1.branch_ordinal() is None

    o0 = Ordinal.from_nat(0)
    o1 = Ordinal.from_nat(1)

    c0 = r1.child(o0)
    assert not c0.is_root()
    assert c0.parent() == r1
    assert c0.branch_ordinal() == o0
    assert c0.depth() == Ordinal.from_nat(1)

    c1 = r1.child(o1)
    assert c0 != c1
    assert c0 != r1


def test_address_prefix_relations() -> None:
    root = Address.root()
    o0 = Ordinal.from_nat(0)
    o1 = Ordinal.from_nat(1)

    c0 = root.child(o0)
    c00 = c0.child(o0)
    c01 = c0.child(o1)
    c1 = root.child(o1)

    # Root is prefix of all
    assert root.is_prefix_of(root)
    assert root.is_prefix_of(c0)
    assert root.is_prefix_of(c00)
    assert root.is_prefix_of(c1)

    # Strict prefix
    assert root.is_strict_prefix_of(c0)
    assert not root.is_strict_prefix_of(root)

    # Descendant prefix
    assert c0.is_prefix_of(c00)
    assert c0.is_prefix_of(c01)
    assert not c0.is_prefix_of(c1)
    assert not c00.is_prefix_of(c0)


def test_address_disjointness() -> None:
    root = Address.root()
    o0 = Ordinal.from_nat(0)
    o1 = Ordinal.from_nat(1)

    c0 = root.child(o0)
    c1 = root.child(o1)
    c00 = c0.child(o0)
    c10 = c1.child(o0)

    # Siblings are disjoint
    assert c0.is_disjoint_from(c1)
    assert c1.is_disjoint_from(c0)

    # Cross-tree descendants are disjoint
    assert c00.is_disjoint_from(c10)
    assert c00.is_disjoint_from(c1)
    assert c10.is_disjoint_from(c0)

    # Ancestor and descendant are NOT disjoint
    assert not root.is_disjoint_from(c0)
    assert not c0.is_disjoint_from(c00)
    assert not c00.is_disjoint_from(c00)


def test_address_path_roundtrip() -> None:
    root = Address.root()
    path = (Ordinal.from_nat(2), Ordinal.from_nat(0), Ordinal.from_nat(4))

    addr = Address.from_path(path)
    assert addr.depth() == Ordinal.from_nat(3)
    assert addr.to_path() == path

    assert Address.from_path(()).is_root()
    assert Address.root().to_path() == ()


def test_deep_address_hierarchy() -> None:
    root = Address.root()
    # Build a deep address of depth 10
    curr = root
    for i in range(10):
        curr = curr.child(Ordinal.from_nat(i))

    assert curr.depth() == Ordinal.from_nat(10)
    assert root.is_prefix_of(curr)
    assert not curr.is_prefix_of(root)

    # Sibling branch under same deep parent
    parent = curr.parent()
    assert parent is not None
    sibling = parent.child(Ordinal.from_nat(99))
    assert curr.is_disjoint_from(sibling)
    assert sibling.is_disjoint_from(curr)


def test_address_type_enforcement() -> None:
    root = Address.root()
    try:
        root.child("not_an_ordinal")  # type: ignore[arg-type]
        assert False, "expected TypeError"
    except TypeError:
        pass
