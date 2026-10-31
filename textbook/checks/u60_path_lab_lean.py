"""Kernel-check path-lab cases and native theorem imports; AuthorityEffect: None."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from booklean import BOTH, NONE, main  # noqa: E402
from textbook.path_lab.lean_cases import build_checks  # noqa: E402
from textbook.path_lab.costs_lean import expected_cost_reports  # noqa: E402

if __name__ == "__main__":
    source, names = build_checks()
    expected = {name: BOTH for name in names}
    expected["BoundaryCancellation.signless_countermodel"] = NONE
    expected.update(expected_cost_reports())
    raise SystemExit(main(source, expected, "PathLab"))
