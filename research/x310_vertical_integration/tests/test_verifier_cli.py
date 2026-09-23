"""Direct verifier entry points must start without preloaded site modules."""
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


@pytest.mark.parametrize("cwd", [ROOT, REPO])
@pytest.mark.parametrize("script,args,expected", [
    ("verify.py", ["--help"], "--check"),
    ("verify_sources.py", [], "PASS: all source pins match"),
])
def test_verifier_without_site_preloaded_modules(
    cwd: Path, script: str, args: list[str], expected: str,
) -> None:
    env = {key: value for key, value in os.environ.items() if not key.startswith("PYTHON")}
    result = subprocess.run(
        [sys.executable, "-S", str(ROOT / script), *args],
        cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert expected in result.stdout
