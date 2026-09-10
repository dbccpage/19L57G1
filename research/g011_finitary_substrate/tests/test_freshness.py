"""Pytest suite for deterministic address freshness allocator."""

from ordinals import Ordinal
from address import Address
from freshness import (
    AddressRegistry,
    fresh_address,
    fresh_index,
    max_branch_index,
    has_branch,
    root_branch_index,
)


def test_fresh_index_on_empty() -> None:
    empty: tuple[Address, ...] = ()
    assert not has_branch(empty)
    assert fresh_index(empty) == Ordinal.zero()
    assert fresh_address(empty) == Address.root().child(Ordinal.zero())


def test_fresh_address_collision_freedom() -> None:
    root = Address.root()
    o0 = Ordinal.from_nat(0)
    o1 = Ordinal.from_nat(1)
    o2 = Ordinal.from_nat(2)

    allocated: list[Address] = [
        root,
        root.child(o0),
        root.child(o1),
        root.child(o0).child(o2),
    ]

    fresh = fresh_address(allocated)
    assert fresh not in allocated
    assert fresh == root.child(Ordinal.from_nat(2))

    # Adding the fresh address and allocating again produces another non-colliding address
    allocated.append(fresh)
    fresh2 = fresh_address(allocated)
    assert fresh2 not in allocated
    assert fresh2 == root.child(Ordinal.from_nat(3))
    assert fresh != fresh2


def test_fresh_address_disjointness_from_siblings() -> None:
    root = Address.root()
    allocated = [root.child(Ordinal.from_nat(i)) for i in range(5)]

    fresh = fresh_address(allocated)
    assert fresh not in allocated

    for addr in allocated:
        assert fresh.is_disjoint_from(addr)


def test_address_registry_allocation_sequence() -> None:
    reg = AddressRegistry.empty()
    assert reg.count == Ordinal.zero()
    assert len(reg.allocated) == 0

    allocated_addrs: list[Address] = []
    for i in range(10):
        reg, fresh = reg.allocate()
        assert fresh not in allocated_addrs
        assert reg.contains(fresh)
        assert reg.count == Ordinal.from_nat(i + 1)
        allocated_addrs.append(fresh)

    # All allocated addresses are pairwise distinct and disjoint
    for i in range(len(allocated_addrs)):
        for j in range(i + 1, len(allocated_addrs)):
            assert allocated_addrs[i] != allocated_addrs[j]
            assert allocated_addrs[i].is_disjoint_from(allocated_addrs[j])


def test_fresh_address_determinism() -> None:
    # Pure function determinism: no reliance on random/time oracles
    root = Address.root()
    s = [root.child(Ordinal.from_nat(1)), root.child(Ordinal.from_nat(3))]

    res1 = fresh_address(s)
    res2 = fresh_address(s)
    assert res1 == res2
    assert res1 == root.child(Ordinal.from_nat(4))


def test_large_allocation_sequence() -> None:
    reg = AddressRegistry.empty()
    seen: set[Address] = set()
    for i in range(50):
        reg, fresh = reg.allocate()
        assert fresh not in seen
        assert fresh.depth() == Ordinal.from_nat(1)
        seen.add(fresh)


def test_freshness_with_deep_descendants() -> None:
    root = Address.root()
    # Populate addresses with deep nested branches
    c1 = root.child(Ordinal.from_nat(1))
    c1_deep = c1.child(Ordinal.from_nat(5)).child(Ordinal.from_nat(10))
    c3 = root.child(Ordinal.from_nat(3))
    c3_deep = c3.child(Ordinal.from_nat(20))

    allocated = [root, c1, c1_deep, c3, c3_deep]
    fresh = fresh_address(allocated)

    # Fresh address should be root.child(4) because top-level branch max is 3
    assert fresh == root.child(Ordinal.from_nat(4))
    assert fresh not in allocated
    for a in allocated:
        if not a.is_root():
            assert fresh.is_disjoint_from(a)
