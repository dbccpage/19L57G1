"""Kernel-check the lab's finite Python/Lean agreement; AuthorityEffect: None."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from booklean import BOTH, main  # noqa: E402
from textbook.change_lab.lean_cases import build_lean_checks  # noqa: E402

if __name__ == "__main__":
    source, names = build_lean_checks()
    raise SystemExit(main(source, {name: BOTH for name in names}, "PassageLab"))
