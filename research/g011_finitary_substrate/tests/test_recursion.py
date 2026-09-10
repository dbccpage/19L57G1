"""Pytest suite for fuel-bounded endogenous recursion and instruction evaluation."""

from ordinals import Ordinal
from address import Address
from recursion import (
    Val,
    NumVal,
    AddrVal,
    Nop,
    SetZero,
    SuccReg,
    PredReg,
    CopyReg,
    AllocAddr,
    WriteMem,
    ReadMem,
    Jump,
    BranchIfZero,
    Halt,
    State,
    Halted,
    OutOfFuel,
    step,
    run_with_fuel,
    rec_fuel,
)


def test_stepper_basic_instructions() -> None:
    r0 = Ordinal.from_nat(0)
    r1 = Ordinal.from_nat(1)

    prog = [
        Nop(),               # pc 0
        SuccReg(r0),         # pc 1
        PredReg(r0),         # pc 2
        SuccReg(r0),         # pc 3
        CopyReg(r1, r0),     # pc 4
    ]

    # Nop
    s0 = State()
    s1 = step(prog, s0)
    assert s1.pc == Ordinal.from_nat(1)
    assert not s1.halted

    # SuccReg
    s2 = step(prog, s1)
    assert s2.pc == Ordinal.from_nat(2)
    assert s2.get_reg(r0) == NumVal(Ordinal.from_nat(1))

    # PredReg
    s3 = step(prog, s2)
    assert s3.pc == Ordinal.from_nat(3)
    assert s3.get_reg(r0) == NumVal(Ordinal.zero())

    # SuccReg again
    s4 = step(prog, s3)
    assert s4.pc == Ordinal.from_nat(4)
    assert s4.get_reg(r0) == NumVal(Ordinal.from_nat(1))

    # CopyReg
    s5 = step(prog, s4)
    assert s5.pc == Ordinal.from_nat(5)
    assert s5.get_reg(r1) == NumVal(Ordinal.from_nat(1))


def test_stepper_memory_allocation_and_access() -> None:
    r_addr = Ordinal.from_nat(0)
    r_val = Ordinal.from_nat(1)
    r_read = Ordinal.from_nat(2)

    prog = [
        AllocAddr(r_addr),              # pc 0: alloc fresh addr -> r_addr
        SuccReg(r_val),                 # pc 1: r_val := 1
        SuccReg(r_val),                 # pc 2: r_val := 2
        WriteMem(r_addr, r_val),        # pc 3: mem[r_addr] := 2
        ReadMem(r_read, r_addr),        # pc 4: r_read := mem[r_addr]
        Halt(),                         # pc 5: halt
    ]

    res = run_with_fuel(Ordinal.from_nat(10), prog, State())
    assert isinstance(res, Halted)
    final = res.state
    assert final.halted
    assert len(final.addrs) == 1
    addr_val = final.get_reg(r_addr)
    assert isinstance(addr_val, AddrVal)
    assert final.get_reg(r_read) == NumVal(Ordinal.from_nat(2))


def test_stepper_branching_and_loop() -> None:
    # Program: compute 2 + 3 by decrementing r1 and incrementing r0 until r1 == 0
    r0 = Ordinal.from_nat(0)  # accumulator
    r1 = Ordinal.from_nat(1)  # counter

    prog = [
        # pc 0: BranchIfZero r1 target: 4
        BranchIfZero(r1, Ordinal.from_nat(4)),
        # pc 1: PredReg r1
        PredReg(r1),
        # pc 2: SuccReg r0
        SuccReg(r0),
        # pc 3: Jump 0
        Jump(Ordinal.from_nat(0)),
        # pc 4: Halt
        Halt(),
    ]

    init_state = State().set_reg(r0, NumVal(Ordinal.from_nat(2))).set_reg(r1, NumVal(Ordinal.from_nat(3)))

    # Insufficient fuel -> OutOfFuel
    res_partial = run_with_fuel(Ordinal.from_nat(5), prog, init_state)
    assert isinstance(res_partial, OutOfFuel)
    assert not res_partial.state.halted

    # Sufficient fuel -> Halted with r0 == 5
    res_full = run_with_fuel(Ordinal.from_nat(20), prog, init_state)
    assert isinstance(res_full, Halted)
    assert res_full.state.halted
    assert res_full.state.get_reg(r0) == NumVal(Ordinal.from_nat(5))
    assert res_full.state.get_reg(r1) == NumVal(Ordinal.zero())


def test_fuel_monotonicity() -> None:
    # Fuel monotonicity: if fuel F halts, fuel F + K halts with identical state
    prog = [SuccReg(Ordinal.zero()), Halt()]
    s0 = State()

    res1 = run_with_fuel(Ordinal.from_nat(2), prog, s0)
    assert isinstance(res1, Halted)

    res2 = run_with_fuel(Ordinal.from_nat(10), prog, s0)
    assert isinstance(res2, Halted)

    assert res1.state == res2.state


def test_structural_recursion_scheme() -> None:
    # Pure endogenous structural recursion scheme on Ordinals
    # Compute triangular number T(n) = sum_{i=1}^n i
    def step_fn(curr_ordinal: Ordinal, acc: Ordinal) -> Ordinal:
        return acc.add(curr_ordinal.succ())

    # T(0) = 0
    assert rec_fuel(Ordinal.from_nat(0), Ordinal.zero(), step_fn) == Ordinal.zero()
    # T(3) = 1 + 2 + 3 = 6
    assert rec_fuel(Ordinal.from_nat(3), Ordinal.zero(), step_fn) == Ordinal.from_nat(6)
    # T(4) = 10
    assert rec_fuel(Ordinal.from_nat(4), Ordinal.zero(), step_fn) == Ordinal.from_nat(10)


def test_memory_refusal_on_scalar_address() -> None:
    # Attempting to write/read memory using a NumVal instead of AddrVal triggers immediate halt refusal
    r_bad_addr = Ordinal.from_nat(0)
    r_val = Ordinal.from_nat(1)
    r_out = Ordinal.from_nat(2)

    prog_write = [WriteMem(r_bad_addr, r_val)]
    s = State().set_reg(r_bad_addr, NumVal(Ordinal.from_nat(5)))
    s_halted = step(prog_write, s)
    assert s_halted.halted

    prog_read = [ReadMem(r_out, r_bad_addr)]
    s_read_halted = step(prog_read, s)
    assert s_read_halted.halted


def test_unwritten_memory_read_returns_zero() -> None:
    r_addr = Ordinal.from_nat(0)
    r_out = Ordinal.from_nat(1)
    addr = Address.root().child(Ordinal.from_nat(10))

    s = State().set_reg(r_addr, AddrVal(addr))
    prog = [ReadMem(r_out, r_addr), Halt()]

    res = run_with_fuel(Ordinal.from_nat(5), prog, s)
    assert isinstance(res, Halted)
    assert res.state.get_reg(r_out) == NumVal(Ordinal.zero())
