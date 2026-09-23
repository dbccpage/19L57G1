"""A failed Git read of a present HEAD source must not become drift."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO = Path(__file__).resolve().parents[1]
TREES = (
    "balance_carrier",
    "closed_family",
    "convention_price",
    "fresh_characters",
    "path_dependent_cost",
    "reach_additivity",
    "reach_measure",
    "standing_commitment",
)


def verifier(tree: str) -> ModuleType:
    path = REPO / "research" / tree / "verify_pins.py"
    spec = importlib.util.spec_from_file_location(f"custody_{tree}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    old = sys.dont_write_bytecode
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = old
    return module


@pytest.mark.parametrize("tree", TREES)
def test_present_head_source_git_error_fails(tree: str, monkeypatch: pytest.MonkeyPatch,
                                             capsys: pytest.CaptureFixture[str]) -> None:
    module = verifier(tree)
    manifest = json.loads((module.HERE / "SOURCE_MANIFEST.json").read_text("ascii"))
    path = sorted(manifest["pins"])[0]
    if tree == "convention_price":
        real_git = module.git

        def fake_git(*args: str) -> str:
            if args == ("rev-parse", f"HEAD:{path}"):
                raise RuntimeError("git rev-parse: injected read error")
            return real_git(*args)

        monkeypatch.setattr(module, "git", fake_git)
    else:
        real_git = module.git
        real_git_text = module.git_text

        def fake_git(*args: str) -> bytes:
            if args[:1] == ("status",):
                return b""
            return real_git(*args)

        def fake_git_text(*args: str) -> str:
            if args == ("rev-parse", f"HEAD:{path}"):
                raise RuntimeError("git rev-parse: injected read error")
            return real_git_text(*args)

        monkeypatch.setattr(module, "git", fake_git)
        monkeypatch.setattr(module, "git_text", fake_git_text)

    assert module.main([]) == 1
    assert f"FAIL: could not read {path} at HEAD" in capsys.readouterr().out


@pytest.mark.parametrize("tree", TREES)
def test_absent_head_source_is_reported(tree: str, monkeypatch: pytest.MonkeyPatch,
                                        capsys: pytest.CaptureFixture[str]) -> None:
    module = verifier(tree)
    manifest = json.loads((module.HERE / "SOURCE_MANIFEST.json").read_text("ascii"))
    path = sorted(manifest["pins"])[0]
    head_read = ("rev-parse", f"HEAD:{path}")
    head_lookup = ("ls-tree", "-r", "--name-only", "HEAD", "--", path)
    if tree == "convention_price":
        real_git = module.git

        def fake_git(*args: str) -> str:
            if args == head_read:
                raise RuntimeError("git rev-parse: path absent")
            if args == head_lookup:
                return ""
            return real_git(*args)

        monkeypatch.setattr(module, "git", fake_git)
    else:
        real_git = module.git
        real_git_text = module.git_text

        def fake_git(*args: str) -> bytes:
            if args[:1] == ("status",):
                return b""
            return real_git(*args)

        def fake_git_text(*args: str) -> str:
            if args == head_read:
                raise RuntimeError("git rev-parse: path absent")
            if args == head_lookup:
                return ""
            return real_git_text(*args)

        monkeypatch.setattr(module, "git", fake_git)
        monkeypatch.setattr(module, "git_text", fake_git_text)

    assert module.main([]) == 0
    assert f"DRIFT: {path} is absent at HEAD" in capsys.readouterr().out


def test_present_head_span_git_error_fails(monkeypatch: pytest.MonkeyPatch,
                                           capsys: pytest.CaptureFixture[str]) -> None:
    module = verifier("balance_carrier")
    manifest = json.loads((module.HERE / "SOURCE_MANIFEST.json").read_text("ascii"))
    path = manifest["spans"][0]["path"]
    real_git = module.git

    def fake_git(*args: str) -> bytes:
        if args == ("show", f"HEAD:{path}"):
            raise RuntimeError("git show: injected read error")
        if args[:1] == ("status",):
            return b""
        return real_git(*args)

    monkeypatch.setattr(module, "git", fake_git)
    assert module.main([]) == 1
    assert f"FAIL: could not read span {path}:" in capsys.readouterr().out
