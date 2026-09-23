"""Keep wrapped generated-helper reports inside the axiom audit population."""
from __future__ import annotations

import subprocess

import pytest

from verify import audit_theorems_and_axioms


@pytest.mark.parametrize("axes, expected_error", [
    ("[propext,\n Quot.sound]", None),
    ("[propext,\n Classical.choice]", "VIOLATION"),
    ("[propext,\n Quot.sound", "Some census theorems were not audited"),
])
def test_wrapped_axiom_report(
    monkeypatch: pytest.MonkeyPatch, axes: str, expected_error: str | None,
) -> None:
    name = "G012TypedTranslation.NativeAdmission.step_identity_or_weight_increases._proof_1_9"
    reports = iter([
        subprocess.CompletedProcess(["lean"], 0, f"G012_TYPED_TRANSLATION_THEOREM: {name}\n", ""),
        subprocess.CompletedProcess(["lean"], 0, f"'{name}' depends on axioms: {axes}\n", ""),
    ])

    def run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return next(reports)

    monkeypatch.setattr("verify.subprocess.run", run)
    if expected_error is None:
        names, axioms = audit_theorems_and_axioms()
        assert names == [name]
        assert axioms == {name: ["propext", "Quot.sound"]}
    else:
        with pytest.raises(RuntimeError, match=expected_error):
            audit_theorems_and_axioms()
