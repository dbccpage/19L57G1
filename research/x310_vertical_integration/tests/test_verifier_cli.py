"""A clean interpreter must reach the documented verifier entry point."""
from pathlib import Path
import os
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


@pytest.mark.parametrize("cwd", [ROOT, REPO])
def test_verifier_help_without_site_preloaded_modules(cwd: Path) -> None:
    env = {key: value for key, value in os.environ.items() if not key.startswith("PYTHON")}
    result = subprocess.run(
        [sys.executable, "-S", str(ROOT / "verify.py"), "--help"],
        cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "--check" in result.stdout
