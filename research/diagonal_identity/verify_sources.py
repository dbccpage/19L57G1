"""Custody wrapper for the scaffold runner.

AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from typing import Any

import verify_pins


def verify_sources() -> list[str]:
    try:
        verify_pins.verify()
    except ValueError as error:
        return [str(error)]
    return []


def verify_manifest(manifest: dict[str, Any] | None = None) -> list[str]:
    return verify_pins.verify(manifest)
