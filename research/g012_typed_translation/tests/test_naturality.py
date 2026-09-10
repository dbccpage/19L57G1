"""Tests for signature renamings, naturality commutation, and distortion vectors.

Verifies functorial composition, naturality commutation between signature renamings
and relational encoding, and exact rational distortion vector properties in Q.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction

from naturality import (
    DistortionVector,
    Renaming,
    compute_distortion,
    renaming_naturality_commutes,
)
from signature import (
    ConstantSymbol,
    FunctionSymbol,
    RelationSymbol,
    Signature,
    TypedStructure,
)


def test_signature_renaming_functorial_composition() -> None:
    """Functorial composition law: (tau o sigma)_*(S) == tau_*(sigma_*(S))."""
    sig1 = Signature(
        sorts=("A",),
        constants=(ConstantSymbol("c", "A"),),
        relations=(RelationSymbol("R", ("A",)),),
        functions=(FunctionSymbol("f", ("A",), "A"),),
    )
    struct = TypedStructure.create(
        sig1,
        carriers={"A": ["x", "y"]},
        constants={"c": "x"},
        relations={"R": [("x",), ("y",)]},
        functions={"f": [(( "x",), "y"), (("y",), "x")]},
    )

    sigma = Renaming.create(
        sort_map={"A": "B"},
        const_map={"c": "d"},
        rel_map={"R": "P"},
        func_map={"f": "g"},
    )
    tau = Renaming.create(
        sort_map={"B": "C"},
        const_map={"d": "e"},
        rel_map={"P": "Q"},
        func_map={"g": "h"},
    )

    comp = tau.compose(sigma)

    res_composed_action = comp.apply_to_structure(struct)
    res_sequential_action = tau.apply_to_structure(sigma.apply_to_structure(struct))

    assert res_composed_action == res_sequential_action
    assert res_composed_action.signature.sorts == ("C",)
    assert res_composed_action.constant_val("e") == "x"
    assert res_composed_action.tuples_for("Q") == (("x",), ("y",))


def test_renaming_naturality_commutation() -> None:
    """Naturality square commutes: encode(sigma_*(S)) == sigma_rel(encode(S))."""
    sig = Signature(
        sorts=("node", "label"),
        constants=(ConstantSymbol("root", "node"),),
        relations=(
            RelationSymbol("Flag", ()),
            RelationSymbol("Arc", ("node", "node")),
            RelationSymbol("HasLabel", ("node", "label")),
        ),
        functions=(FunctionSymbol("next_node", ("node",), "node"),),
    )

    struct = TypedStructure.create(
        sig,
        carriers={
            "node": ["u", "v"],
            "label": ["l1", "l2"],
        },
        constants={"root": "u"},
        relations={
            "Flag": [()],
            "Arc": [("u", "v")],
            "HasLabel": [("u", "l1"), ("v", "l2")],
        },
        functions={"next_node": [(( "u",), "v")]},
    )

    sigma = Renaming.create(
        sort_map={"node": "vertex", "label": "tag"},
        const_map={"root": "source"},
        rel_map={"Flag": "Active", "Arc": "Edge", "HasLabel": "Tagged"},
        func_map={"next_node": "succ"},
    )

    assert renaming_naturality_commutes(sigma, struct)


def test_distortion_vector_exact_rational_values() -> None:
    """Distortion vector components are exact Fractions with correct bounds."""
    sig = Signature(
        sorts=("datum",),
        relations=(
            RelationSymbol("Form", ()),
            RelationSymbol("Instance", ("datum",)),
        ),
    )
    struct = TypedStructure.create(
        sig,
        carriers={"datum": ["0", "1"]},
        relations={
            "Form": [()],
            "Instance": [("0",), ("1",)],
        },
    )

    distortion = compute_distortion(struct)

    assert isinstance(distortion.state_expansion, Fraction)
    assert isinstance(distortion.mark_count_ratio, Fraction)
    assert isinstance(distortion.address_depth_ratio, Fraction)

    # All ratios are strictly positive
    assert distortion.state_expansion > 0
    assert distortion.mark_count_ratio > 0
    assert distortion.address_depth_ratio > 0

    # Address depth ratio for depth 3 relational vs arity depth 2
    # max arity = 1, struct_depth = 2, rel_depth = 3 -> 3/2
    assert distortion.address_depth_ratio == Fraction(3, 2)


def test_distortion_vector_invariant_under_renaming() -> None:
    """Distortion vector is invariant under signature renamings."""
    sig = Signature(
        sorts=("X", "Y"),
        constants=(ConstantSymbol("c", "X"),),
        relations=(RelationSymbol("R", ("X", "Y")),),
    )
    struct = TypedStructure.create(
        sig,
        carriers={"X": ["x1", "x2"], "Y": ["y1"]},
        constants={"c": "x1"},
        relations={"R": [("x1", "y1")]},
    )

    sigma = Renaming.create(
        sort_map={"X": "SortX", "Y": "SortY"},
        const_map={"c": "constC"},
        rel_map={"R": "RelR"},
    )
    renamed_struct = sigma.apply_to_structure(struct)

    orig_distortion = compute_distortion(struct)
    renamed_distortion = compute_distortion(renamed_struct)

    assert orig_distortion == renamed_distortion
