"""Finite, provenance-explicit data for the symmetry--obstruction bridge.

This module is a contract, not a genesis claim.  A presentation, its symmetry,
a repair map, and a residual are all supplied data.  Later modules may prove
facts relative to this contract, but cannot relabel an admission as a result.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Tuple


BinaryVector = Tuple[int, ...]
Point = int


class Origin(str, Enum):
    """How a bridge datum entered the finite assessment."""

    ADMITTED = "admitted"
    DECLARED = "declared"
    DERIVED = "derived"
    COMPUTED = "computed"
    PROVED = "proved"
    OPEN = "open"
    REFUSED = "refused"


@dataclass(frozen=True)
class Provenance:
    """A typed label that prevents a datum from acquiring authority by use."""

    label: str
    origin: Origin

    def __post_init__(self) -> None:
        if not self.label:
            raise ValueError("provenance label must be nonempty")

    def to_data(self) -> dict[str, str]:
        return {"label": self.label, "origin": self.origin.value}


def binary_vector(values: Iterable[int]) -> BinaryVector:
    """Validate and normalize a nonempty vector over the two-element field."""

    vector = tuple(values)
    if not vector or any(value not in (0, 1) for value in vector):
        raise ValueError("binary vectors must be nonempty tuples of zeroes and ones")
    return vector


@dataclass(frozen=True)
class Involution:
    """A declared presentation symmetry with order at most two."""

    carrier: Tuple[Point, ...]
    image: Tuple[Point, ...]
    provenance: Provenance

    def __post_init__(self) -> None:
        if not self.carrier or self.carrier != tuple(sorted(set(self.carrier))):
            raise ValueError("carrier must be a nonempty sorted tuple of unique labels")
        if len(self.image) != len(self.carrier) or set(self.image) != set(self.carrier):
            raise ValueError("involution image must permute the carrier")
        positions = {point: index for index, point in enumerate(self.carrier)}
        for point, image in zip(self.carrier, self.image):
            if self.image[positions[image]] != point:
                raise ValueError("declared action is not an involution")

    def apply_point(self, point: Point) -> Point:
        try:
            return self.image[self.carrier.index(point)]
        except ValueError as error:
            raise ValueError("point lies outside the presentation carrier") from error

    def apply_vector(self, vector: BinaryVector) -> BinaryVector:
        """Push a coordinate cochain forward along the declared involution."""

        checked = binary_vector(vector)
        if len(checked) != len(self.carrier):
            raise ValueError("cochain dimension must match the presentation carrier")
        positions = {point: index for index, point in enumerate(self.carrier)}
        result = [0] * len(checked)
        for index, image in enumerate(self.image):
            result[positions[image]] = checked[index]
        return tuple(result)

    def point_orbit(self, point: Point) -> Tuple[Point, ...]:
        image = self.apply_point(point)
        return (point,) if image == point else tuple(sorted((point, image)))

    def vector_orbit(self, vector: BinaryVector) -> Tuple[BinaryVector, ...]:
        checked = binary_vector(vector)
        image = self.apply_vector(checked)
        return (checked,) if image == checked else tuple(sorted((checked, image)))

    def to_data(self) -> dict[str, Any]:
        return {
            "carrier": list(self.carrier),
            "image": list(self.image),
            "provenance": self.provenance.to_data(),
        }


@dataclass(frozen=True)
class FiniteRepairMap:
    """A declared finite repair differential represented by its full table."""

    potentials: Tuple[BinaryVector, ...]
    images: Tuple[BinaryVector, ...]
    zero: BinaryVector
    provenance: Provenance

    def __post_init__(self) -> None:
        if not self.potentials or len(self.potentials) != len(self.images):
            raise ValueError("repair table must have equally many nonempty inputs and images")
        checked_potentials = tuple(binary_vector(vector) for vector in self.potentials)
        checked_images = tuple(binary_vector(vector) for vector in self.images)
        checked_zero = binary_vector(self.zero)
        if checked_potentials != self.potentials or checked_images != self.images:
            raise ValueError("repair table vectors must already be normalized")
        if len(set(self.potentials)) != len(self.potentials):
            raise ValueError("repair potentials must be unique")
        if any(len(vector) != len(checked_zero) for vector in self.images):
            raise ValueError("repair images and zero must have one common dimension")
        if any(checked_zero):
            raise ValueError("declared zero cochain must be identically zero")

    @property
    def boundary_image(self) -> frozenset[BinaryVector]:
        return frozenset(self.images)

    def boundary(self, potential: BinaryVector) -> BinaryVector:
        checked = binary_vector(potential)
        try:
            return self.images[self.potentials.index(checked)]
        except ValueError as error:
            raise ValueError("potential lies outside the declared repair domain") from error

    def is_boundary(self, residual: BinaryVector) -> bool:
        checked = binary_vector(residual)
        if len(checked) != len(self.zero):
            raise ValueError("residual dimension must match the repair codomain")
        return checked in self.boundary_image

    def to_data(self) -> dict[str, Any]:
        return {
            "boundary_image": [list(vector) for vector in sorted(self.boundary_image)],
            "images": [list(vector) for vector in self.images],
            "potentials": [list(vector) for vector in self.potentials],
            "provenance": self.provenance.to_data(),
            "zero": list(self.zero),
        }


@dataclass(frozen=True)
class BridgeContract:
    """The entire finite input boundary for the five-goal bridge program."""

    symmetry: Involution
    repair: FiniteRepairMap
    residual: BinaryVector
    residual_provenance: Provenance

    def __post_init__(self) -> None:
        checked = binary_vector(self.residual)
        if checked != self.residual:
            raise ValueError("residual must already be normalized")
        if len(checked) != len(self.symmetry.carrier):
            raise ValueError("residual dimension must match the presentation carrier")
        if len(checked) != len(self.repair.zero):
            raise ValueError("residual dimension must match the repair codomain")

    @property
    def residual_orbit(self) -> Tuple[BinaryVector, ...]:
        return self.symmetry.vector_orbit(self.residual)

    @property
    def residual_is_boundary(self) -> bool:
        return self.repair.is_boundary(self.residual)

    @property
    def repair_image_is_symmetric(self) -> bool:
        return all(
            self.symmetry.apply_vector(boundary) in self.repair.boundary_image
            for boundary in self.repair.boundary_image
        )

    def to_data(self) -> dict[str, Any]:
        return {
            "repair": self.repair.to_data(),
            "repair_image_is_symmetric": self.repair_image_is_symmetric,
            "residual": list(self.residual),
            "residual_is_boundary": self.residual_is_boundary,
            "residual_orbit": [list(vector) for vector in self.residual_orbit],
            "residual_provenance": self.residual_provenance.to_data(),
            "symmetry": self.symmetry.to_data(),
        }


def two_coordinate_contract() -> BridgeContract:
    """The displayed finite fixture used by all five bridge goals."""

    symmetry = Involution(
        carrier=(0, 1),
        image=(1, 0),
        provenance=Provenance("coordinate-swap", Origin.DECLARED),
    )
    repair = FiniteRepairMap(
        potentials=((0,), (1,)),
        images=((0, 0), (1, 1)),
        zero=(0, 0),
        provenance=Provenance("diagonal-boundary-map", Origin.DECLARED),
    )
    return BridgeContract(
        symmetry=symmetry,
        repair=repair,
        residual=(1, 0),
        residual_provenance=Provenance("displayed-residual", Origin.DECLARED),
    )
