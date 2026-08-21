"""Regression tests for the portable-interface pin verifier."""

from __future__ import annotations

import json
from pathlib import PurePosixPath
from typing import Any
import unittest
from unittest.mock import patch

import verify_pins


def _pins() -> dict[str, Any]:
    payload: dict[str, Any] = json.loads(
        verify_pins.PINS_PATH.read_text(encoding="utf-8")
    )
    return payload


class VerifyPinsTests(unittest.TestCase):
    def test_current_pins_verify(self) -> None:
        lines = verify_pins.verify_pins()
        self.assertTrue(any("exports resolve" in line for line in lines))

    def test_hash_mismatch_is_refused(self) -> None:
        pins = _pins()
        pins["modules"][0]["sha256"] = "0" * 64
        with patch.object(verify_pins, "_read_pins", return_value=pins):
            with self.assertRaisesRegex(ValueError, r"hash mismatch for .*\.lean"):
                verify_pins.verify_pins()

    def test_export_naming_no_declaration_is_refused(self) -> None:
        pins = _pins()
        pins["exports"].append(
            {
                "name": "zzz_probe_absent",
                "module": pins["modules"][0]["path"],
                "kind": "THEOREM",
            }
        )
        with patch.object(verify_pins, "_read_pins", return_value=pins):
            with self.assertRaisesRegex(
                ValueError, r"exports declared in no pinned source: .*zzz_probe_absent"
            ):
                verify_pins.verify_pins()

    def test_export_naming_an_unpinned_module_is_refused(self) -> None:
        pins = _pins()
        pins["exports"].append(
            {
                "name": "ZeroRel",
                "module": "lean4/Derivation/NotPinned.lean",
                "kind": "DEFINITION",
            }
        )
        with patch.object(verify_pins, "_read_pins", return_value=pins):
            with self.assertRaisesRegex(ValueError, r"names unpinned module"):
                verify_pins.verify_pins()

    def test_empty_export_list_is_refused(self) -> None:
        """An empty population must fail closed, not vacuously pass."""

        pins = _pins()
        pins["exports"] = []
        with patch.object(verify_pins, "_read_pins", return_value=pins):
            with self.assertRaisesRegex(ValueError, r"at least one export"):
                verify_pins.verify_pins()

    def test_traversal_path_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, r"unsafe path in pins"):
            verify_pins._safe_relative("../../etc/passwd")

    def test_declaration_scan_ignores_prose_beginning_with_a_keyword(self) -> None:
        """The trap this repository has hit twice.

        A docstring line that happens to begin with the word ``theorem``
        has defeated a grep-based declaration count here before. The scan
        anchors at column zero, so an indented or comment-prefixed line
        must not register as a declaration.
        """

        source = (
            "/-- theorem sounding_prose is not a declaration -/\n"
            "  theorem indented_is_not_column_zero : True := trivial\n"
            "theorem genuinely_declared : True := trivial\n"
        )
        with patch.object(
            verify_pins, "_git_bytes", return_value=source.encode("utf-8")
        ):
            names = verify_pins._declared_names(PurePosixPath("fake.lean"))
        self.assertEqual(names, {"genuinely_declared"})


if __name__ == "__main__":
    unittest.main()
