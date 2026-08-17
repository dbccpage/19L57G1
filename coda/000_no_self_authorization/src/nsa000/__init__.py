"""Illustration layer for NSA-000. AuthorityEffect: None.

These objects demonstrate the *shape* of evaluation vs selection.
They do not re-enumerate the sealed derivation and they do not
mint FIG-* counts.
"""

from __future__ import annotations

from nsa000.born_lift import (
    born_from_weights,
    modulus_squared,
    optional_amplitude_lift,
)
from nsa000.gauges import Castle, better, height_measure, width_measure
from nsa000.selection import Report, evaluate_set, report_one
from nsa000.ties import Orientation, cost_two_orientations, iso_classes

__all__ = [
    "Castle",
    "Orientation",
    "Report",
    "better",
    "born_from_weights",
    "modulus_squared",
    "cost_two_orientations",
    "evaluate_set",
    "height_measure",
    "iso_classes",
    "optional_amplitude_lift",
    "report_one",
    "width_measure",
]
