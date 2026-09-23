"""Tests for operational transition and replay commutation.

Verifies that for any valid operational transition step(S, op) on a typed structure,
the encoding commutes with the relational operation:
encode(step(S, op)) == step_relational(encode(S), encode_op(op, S.signature))
across diverse signatures, relations, functions, and multi-step execution traces.

AuthorityEffect: None.
"""

from __future__ import annotations

from codec import (
    decode,
    encode,
    encode_op,
    step_commutation_holds,
    step_relational,
)
from signature import (
    AddElement,
    AddRelationTuple,
    ConstantSymbol,
    FunctionSymbol,
    RelationSymbol,
    SetConstant,
    SetFunctionValue,
    Signature,
    TypedStructure,
    step,
)


def test_transition_commutation_add_element() -> None:
    """encode(step(S, AddElement)) == step_relational(encode(S), encode_op)."""
    sig = Signature(sorts=("item",))
    struct = TypedStructure.create(sig, carriers={"item": ["a"]})
    op = AddElement("item", "b")

    assert step_commutation_holds(struct, op)


def test_transition_commutation_set_constant() -> None:
    """encode(step(S, SetConstant)) == step_relational(encode(S), encode_op)."""
    sig = Signature(
        sorts=("color",),
        constants=(ConstantSymbol("active_color", "color"),),
    )
    struct = TypedStructure.create(
        sig,
        carriers={"color": ["red", "blue"]},
        constants={"active_color": "red"},
    )
    op = SetConstant("active_color", "blue")

    assert step_commutation_holds(struct, op)


def test_transition_commutation_add_relation_tuples_various_arities() -> None:
    """encode(step(S, AddRelationTuple)) commutes across 0-ary, 1-ary, 2-ary relations."""
    sig = Signature(
        sorts=("node",),
        relations=(
            RelationSymbol("Initialized", ()),
            RelationSymbol("Visited", ("node",)),
            RelationSymbol("Edge", ("node", "node")),
        ),
    )
    struct = TypedStructure.create(
        sig,
        carriers={"node": ["u", "v", "w"]},
    )

    ops = [
        AddRelationTuple("Initialized", ()),
        AddRelationTuple("Visited", ("u",)),
        AddRelationTuple("Edge", ("u", "v")),
        AddRelationTuple("Edge", ("v", "w")),
    ]

    current = struct
    for op in ops:
        assert step_commutation_holds(current, op)
        current = step(current, op)


def test_transition_commutation_set_function_value() -> None:
    """encode(step(S, SetFunctionValue)) == step_relational(encode(S), encode_op)."""
    sig = Signature(
        sorts=("elem",),
        functions=(FunctionSymbol("succ", ("elem",), "elem"),),
    )
    struct = TypedStructure.create(
        sig,
        carriers={"elem": ["0", "1", "2"]},
    )
    op1 = SetFunctionValue("succ", ("0",), "1")
    op2 = SetFunctionValue("succ", ("1",), "2")

    assert step_commutation_holds(struct, op1)
    s1 = step(struct, op1)
    assert step_commutation_holds(s1, op2)


def test_multistep_trace_commutation_and_decode_invariance() -> None:
    """Long trace of interleaved operations maintains commutation and round-trip decode."""
    sig = Signature(
        sorts=("user", "role"),
        constants=(ConstantSymbol("admin_role", "role"),),
        relations=(
            RelationSymbol("HasRole", ("user", "role")),
            RelationSymbol("SuperAdmin", ("user",)),
        ),
        functions=(FunctionSymbol("default_role", ("user",), "role"),),
    )
    s = TypedStructure.create(
        sig,
        carriers={"user": ["alice"], "role": ["viewer", "admin"]},
        constants={"admin_role": "admin"},
    )

    ops = [
        AddElement("user", "bob"),
        AddRelationTuple("HasRole", ("alice", "admin")),
        AddRelationTuple("SuperAdmin", ("alice",)),
        SetFunctionValue("default_role", ("alice",), "admin"),
        AddRelationTuple("HasRole", ("bob", "viewer")),
        SetFunctionValue("default_role", ("bob",), "viewer"),
    ]

    rel_state = encode(s)
    current_struct = s

    for op in ops:
        assert step_commutation_holds(current_struct, op)
        next_struct = step(current_struct, op)
        rel_op = encode_op(op, current_struct)
        rel_state = step_relational(rel_state, rel_op)

        # Commutation assertion
        assert encode(next_struct) == rel_state

        # Roundtrip decode assertion
        dec_res = decode(rel_state)
        assert dec_res.is_ok()
        assert dec_res.unwrap() == next_struct

        current_struct = next_struct


def test_replacement_cycle_is_a_nonmonotone_codec_witness() -> None:
    """A finite two-state witness for the native-admission cycle obstruction.

    The Lean obstruction uses the actual native replay function. This test
    separately checks the Python cycle; it does not identify the Python
    string parser with the Lean typed-token codec.
    """
    sig = Signature(sorts=("item",), constants=(ConstantSymbol("chosen", "item"),))
    a = TypedStructure.create(sig, carriers={"item": ["a", "b"]}, constants={"chosen": "a"})
    set_b, set_a = SetConstant("chosen", "b"), SetConstant("chosen", "a")
    b = step(a, set_b)
    assert a != b and step(b, set_a) == a
    ra, rb = encode(a), encode(b)
    assert decode(ra).unwrap() == a and decode(rb).unwrap() == b
    assert step_relational(ra, encode_op(set_b, a)) == rb
    assert step_relational(rb, encode_op(set_a, b)) == ra
    assert set(ra.insts) - set(rb.insts) == {"bind:chosen:a"}
    assert set(ra.reqs) - set(rb.reqs) == {"req:const:chosen:item:a"}
