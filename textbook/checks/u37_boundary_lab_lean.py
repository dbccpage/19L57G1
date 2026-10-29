"""Native statements and finite boundary/swap examples; AuthorityEffect: None."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from booklean import main  # noqa: E402
from textbook.boundary_lab.lean_cases import build_checks, expected_reports  # noqa: E402

if __name__ == '__main__':
    source, names = build_checks()
    raise SystemExit(main(source, expected_reports(names), 'BoundaryLab'))
