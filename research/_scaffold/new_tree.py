"""Create an independent seed research tree. AuthorityEffect: None."""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import subprocess
import sys

REPO = Path(__file__).resolve().parents[2]
TEMPLATES = Path(__file__).resolve().parent / "new_tree_templates"


def create(repo: Path, name: str) -> Path:
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*", name):
        raise ValueError("tree name must be lowercase words joined by underscores")
    root = "Research" + "".join(part[0].upper()+part[1:] for part in name.split("_"))
    destination = repo / "research" / name
    if destination.exists():
        raise ValueError(f"{destination}: already exists")
    toolchain = (repo / "lean4/lean-toolchain").read_text(encoding="utf-8")
    for template in sorted(TEMPLATES.rglob("*.tmpl")):
        relative = template.relative_to(TEMPLATES).as_posix()[:-5].replace("__ROOT__", root)
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        text = template.read_text(encoding="utf-8").replace("__ROOT__", root).replace("__TREE__", name)
        path.write_text(text, encoding="utf-8", newline="\n")
    (destination / "lean/lean-toolchain").write_text(toolchain, encoding="utf-8", newline="\n")
    subprocess.run([sys.executable, str(destination / "verify.py"), "--write-pins"], cwd=destination, check=True)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument("--repo", type=Path, default=REPO)
    args = parser.parse_args()
    try:
        print(create(args.repo.resolve(), args.name))
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
