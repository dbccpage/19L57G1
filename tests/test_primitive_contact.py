"""Tests for the contact-status artifact."""

from __future__ import annotations

from pathlib import Path

import run_primitive_contact
from run_primitive_contact import contact_report

REPO = Path(__file__).resolve().parent.parent


def test_contact_absent_terminal() -> None:
    rep = contact_report(REPO)
    assert rep["package_present"] is False
    assert rep["manifest_present"] is False
    assert rep["status"] == "CONTACT_INPUT_ABSENT"


def test_present_branch_via_stub(tmp_path: Path) -> None:
    (tmp_path / "contact" / "omega_primdiff").mkdir(parents=True)
    rep = contact_report(tmp_path)
    assert rep["package_present"] is True
    assert rep["status"] == "CONTACT_PRESENT_UNPROCESSED"


def test_runner_byte_stable(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    assert run_primitive_contact.main(["--artifacts", str(d1)]) == 0
    assert run_primitive_contact.main(["--artifacts", str(d2)]) == 0
    assert (d1 / "primitive_contact.json").read_bytes() == \
        (d2 / "primitive_contact.json").read_bytes()
