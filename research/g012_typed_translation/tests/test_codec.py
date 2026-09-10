"""Tests for constructive codec, round-trip invertibility, and structured refusals.

Verifies bidirectional encoding and decoding across diverse multi-sorted signatures,
relations with various arities, functions, constants, and structured refusals
on corrupted or malformed carriers.

AuthorityEffect: None.
"""

from __future__ import annotations

import pytest

from codec import (
    Err,
    Ok,
    RefusalCode,
    RelationalState,
    decode,
    encode,
)
from signature import (
    ConstantSymbol,
    FunctionSymbol,
    RelationSymbol,
    Signature,
    TypedStructure,
)


def test_roundtrip_empty_structure() -> None:
    """Round-trip invertibility on minimal signature with empty carriers."""
    sig = Signature(sorts=("atom",))
    struct = TypedStructure.create(sig, carriers={"atom": ()})

    encoded = encode(struct)
    res = decode(encoded)

    assert isinstance(res, Ok)
    assert res.unwrap() == struct


def test_roundtrip_multisorted_relations_and_constants() -> None:
    """Round-trip invertibility across multiple sorts, relations, and constants."""
    sig = Signature(
        sorts=("node", "color"),
        constants=(
            ConstantSymbol("default_color", "color"),
            ConstantSymbol("root", "node"),
        ),
        relations=(
            RelationSymbol("Active", ()),
            RelationSymbol("Tag", ("node", "color")),
            RelationSymbol("Edge", ("node", "node")),
            RelationSymbol("HyperEdge", ("node", "node", "color")),
        ),
        functions=(
            FunctionSymbol("next_color", ("color",), "color"),
            FunctionSymbol("link", ("node", "color"), "node"),
        ),
    )

    struct = TypedStructure.create(
        signature=sig,
        carriers={
            "node": ["n0", "n1", "n2"],
            "color": ["red", "blue"],
        },
        constants={
            "default_color": "blue",
            "root": "n0",
        },
        relations={
            "Active": [()],
            "Tag": [("n0", "red"), ("n1", "blue")],
            "Edge": [("n0", "n1"), ("n1", "n2")],
            "HyperEdge": [("n0", "n1", "red")],
        },
        functions={
            "next_color": [(( "red",), "blue"), (("blue",), "red")],
            "link": [(("n0", "red"), "n1"), (("n1", "blue"), "n2")],
        },
    )

    encoded = encode(struct)
    res = decode(encoded)

    assert isinstance(res, Ok)
    decoded_struct = res.unwrap()
    assert decoded_struct == struct
    assert decoded_struct.signature == sig
    assert decoded_struct.carrier_for("node") == ("n0", "n1", "n2")
    assert decoded_struct.carrier_for("color") == ("blue", "red")
    assert decoded_struct.constant_val("default_color") == "blue"


def test_refusal_on_unsorted_or_duplicate() -> None:
    """Codec must return UNSORTED_OR_DUPLICATE on unsorted or duplicated carrier fields."""
    bad_state = RelationalState(
        data=("elem:s:b", "elem:s:a"),  # unsorted
        forms=("sort:s",),
        insts=(),
        rules=(),
        reqs=(),
    )
    res = decode(bad_state)
    assert isinstance(res, Err)
    assert res.unwrap_err().code == RefusalCode.UNSORTED_OR_DUPLICATE

    dup_state = RelationalState(
        data=("elem:s:a", "elem:s:a"),  # duplicate
        forms=("sort:s",),
        insts=(),
        rules=(),
        reqs=(),
    )
    res_dup = decode(dup_state)
    assert isinstance(res_dup, Err)
    assert res_dup.unwrap_err().code == RefusalCode.UNSORTED_OR_DUPLICATE


def test_refusal_on_malformed_syntax() -> None:
    """Codec must return MALFORMED_ENCODING on unparseable tokens."""
    malformed_states = [
        RelationalState(data=(), forms=("invalid_prefix:foo",), insts=(), rules=(), reqs=()),
        RelationalState(data=(), forms=("sort:",), insts=(), rules=(), reqs=()),
        RelationalState(data=("not_elem_prefix",), forms=("sort:s",), insts=(), rules=(), reqs=()),
        RelationalState(data=(), forms=("sort:s",), insts=("invalid_inst",), rules=(), reqs=()),
        RelationalState(data=(), forms=("sort:s",), insts=(), rules=("invalid_rule",), reqs=()),
    ]
    for st in malformed_states:
        res = decode(st)
        assert isinstance(res, Err)
        assert res.unwrap_err().code in (
            RefusalCode.MALFORMED_ENCODING,
            RefusalCode.INVALID_SIGNATURE,
        )


def test_refusal_on_carrier_mismatch() -> None:
    """Codec must refuse when constants, tuples, or functions reference nonexistent elements."""
    sig = Signature(
        sorts=("item",),
        constants=(ConstantSymbol("c0", "item"),),
        relations=(RelationSymbol("R", ("item",)),),
    )
    struct = TypedStructure.create(
        sig,
        carriers={"item": ["a"]},
        constants={"c0": "a"},
        relations={"R": [("a",)]},
    )
    encoded = encode(struct)

    # Corrupt constant binding to reference unadmitted 'b'
    corrupted_insts = tuple(i.replace("bind:c0:a", "bind:c0:b") for i in encoded.insts)
    corrupted_state = RelationalState(
        data=encoded.data,
        forms=encoded.forms,
        insts=corrupted_insts,
        rules=encoded.rules,
        reqs=encoded.reqs,
    )
    res = decode(corrupted_state)
    assert isinstance(res, Err)
    assert res.unwrap_err().code == RefusalCode.CARRIER_MISMATCH


def test_refusal_on_function_non_functional() -> None:
    """Codec must refuse if a function maps the same inputs to distinct values."""
    sig = Signature(
        sorts=("elem",),
        functions=(FunctionSymbol("f", ("elem",), "elem"),),
    )
    struct = TypedStructure.create(
        sig,
        carriers={"elem": ["0", "1"]},
        functions={"f": [(( "0",), "1")]},
    )
    encoded = encode(struct)

    # Inject a conflicting rule mapping 0 to 0
    extra_rule = "rule:func:f:(0)->0"
    extra_req = "req:func_out:f:elem:0"
    double_mapped_state = RelationalState(
        data=encoded.data,
        forms=encoded.forms,
        insts=encoded.insts,
        rules=tuple(sorted(set(encoded.rules) | {extra_rule})),
        reqs=tuple(sorted(set(encoded.reqs) | {extra_req})),
    )
    res = decode(double_mapped_state)
    assert isinstance(res, Err)
    assert res.unwrap_err().code == RefusalCode.FUNCTION_NON_FUNCTIONAL


def test_refusal_on_missing_requirement() -> None:
    """Codec must refuse if instantiated facts lack required support in reqs."""
    sig = Signature(
        sorts=("s",),
        relations=(RelationSymbol("R", ("s",)),),
    )
    struct = TypedStructure.create(
        sig,
        carriers={"s": ["x"]},
        relations={"R": [("x",)]},
    )
    encoded = encode(struct)

    # Strip the req:arg requirement
    stripped_reqs = tuple(r for r in encoded.reqs if not r.startswith("req:arg:R:s:x"))
    corrupted_state = RelationalState(
        data=encoded.data,
        forms=encoded.forms,
        insts=encoded.insts,
        rules=encoded.rules,
        reqs=stripped_reqs,
    )
    res = decode(corrupted_state)
    assert isinstance(res, Err)
    assert res.unwrap_err().code == RefusalCode.MISSING_REQUIREMENT


def test_empty_relational_state_decodes_to_empty_structure() -> None:
    """Empty relational state is valid and decodes to empty structure."""
    res = decode(RelationalState((), (), (), (), ()))
    assert isinstance(res, Ok)
    assert len(res.unwrap().signature.sorts) == 0


def test_fuzz_corrupted_strings_never_raise() -> None:
    """Fuzz test ensuring decoding corrupted string tuples never raises unhandled exceptions."""
    corrupted_cases = [
        RelationalState(("elem:",), ("sort:s",), (), (), ()),
        RelationalState(("elem:s:a:extra",), ("sort:s",), (), (), ()),
        RelationalState((), ("rel:R",), (), (), ()),
        RelationalState((), ("func:f",), (), (), ()),
        RelationalState((), ("const:c",), (), (), ()),
        RelationalState((), ("sort:s",), ("tup:R",), (), ()),
        RelationalState((), ("sort:s",), ("bind:c",), (), ()),
        RelationalState(
            ("elem:s:1",),
            ("sort:s", "sort:s"),  # duplicate
            (),
            (),
            (),
        ),
    ]
    for st in corrupted_cases:
        res = decode(st)
        assert isinstance(res, Err)
        assert res.unwrap_err().code in RefusalCode
