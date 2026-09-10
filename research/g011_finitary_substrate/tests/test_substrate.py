"""Pytest suite for the integrated endogenous operational substrate."""

from substrate import (
    Ordinal,
    Zero,
    Succ,
    Address,
    Root,
    Child,
    AddressRegistry,
    fresh_address,
    Val,
    NumVal,
    AddrVal,
    Instr,
    AllocAddr,
    SuccReg,
    WriteMem,
    ReadMem,
    Halt,
    State,
    run_with_fuel,
    Halted,
    rec_fuel,
    build_finitary_substrate,
)


def test_build_finitary_substrate_manifest() -> None:
    manifest = build_finitary_substrate()
    assert manifest["terminal"] == "FINITARY_SUBSTRATE_INTERNAL"
    assert manifest["authority_effect"] == "None"


def test_end_to_end_substrate_workflow() -> None:
    # 1. Allocate three fresh disjoint addresses in succession
    reg = AddressRegistry.empty()
    addrs: list[Address] = []
    for _ in range(3):
        reg, fresh = reg.allocate()
        addrs.append(fresh)

    assert len(addrs) == 3
    for i in range(3):
        for j in range(i + 1, 3):
            assert addrs[i] != addrs[j]
            assert addrs[i].is_disjoint_from(addrs[j])

    # 2. Run a program allocating two more addresses into memory and transferring values
    r_addr1 = Ordinal.from_nat(0)
    r_addr2 = Ordinal.from_nat(1)
    r_val = Ordinal.from_nat(2)
    r_out = Ordinal.from_nat(3)

    prog = [
        AllocAddr(r_addr1),
        AllocAddr(r_addr2),
        SuccReg(r_val),
        SuccReg(r_val),
        SuccReg(r_val),  # r_val = 3
        WriteMem(r_addr1, r_val),
        ReadMem(r_out, r_addr1),
        WriteMem(r_addr2, r_out),
        Halt(),
    ]

    res = run_with_fuel(Ordinal.from_nat(15), prog, State())
    assert isinstance(res, Halted)
    st = res.state
    assert st.halted
    assert len(st.addrs) == 2
    assert st.get_reg(r_out) == NumVal(Ordinal.from_nat(3))


def test_structural_recursion_power() -> None:
    # Exponentiation base^exp via pure structural recursion
    # 2^3 = 8
    two = Ordinal.from_nat(2)
    three = Ordinal.from_nat(3)

    def mul_two(_: Ordinal, acc: Ordinal) -> Ordinal:
        return acc.mul(two)

    pow2_3 = rec_fuel(three, Ordinal.from_nat(1), mul_two)
    assert pow2_3 == Ordinal.from_nat(8)
