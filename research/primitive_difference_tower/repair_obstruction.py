"""Finite certificates for a residual outside a declared repair image.

Here an obstruction is only finite nonmembership: a specified residual is not
one of the outputs in a specified full repair table.  The word carries no
unwritten claim about a homology group, a universal differential, or a
physical process.
"""

from __future__ import annotations

from dataclasses import dataclass

from bridge_contract import BinaryVector, BridgeContract, Origin, Provenance


@dataclass(frozen=True)
class DeclaredRepairObstruction:
    """A replayable nonmembership certificate for one declared finite table."""

    residual: BinaryVector
    repair_table: tuple[tuple[BinaryVector, BinaryVector], ...]
    provenance: Provenance

    def __post_init__(self) -> None:
        if not self.repair_table:
            raise ValueError("a declared repair obstruction needs a nonempty table")
        if any(image == self.residual for _, image in self.repair_table):
            raise ValueError("a residual in the declared image is not an obstruction")

    @property
    def excludes_every_declared_potential(self) -> bool:
        return all(image != self.residual for _, image in self.repair_table)

    def to_data(self) -> dict[str, object]:
        return {
            "provenance": self.provenance.to_data(),
            "repair_table": [
                {"image": list(image), "potential": list(potential)}
                for potential, image in self.repair_table
            ],
            "residual": list(self.residual),
            "scope": "nonmembership in this declared finite repair table only",
        }


def certify_declared_repair_obstruction(
    contract: BridgeContract,
) -> DeclaredRepairObstruction:
    """Enumerate the declared table and refuse to certify a boundary as one."""

    if contract.residual_is_boundary:
        raise ValueError("the declared repair table already repairs this residual")
    table = tuple(zip(contract.repair.potentials, contract.repair.images))
    return DeclaredRepairObstruction(
        residual=contract.residual,
        repair_table=table,
        provenance=Provenance(
            "enumerated-declared-repair-nonmembership", Origin.COMPUTED
        ),
    )
