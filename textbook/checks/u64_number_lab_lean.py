"""Native readout statements and book arithmetic; AuthorityEffect: None."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from booklean import main
from textbook.number_lab.lean_cases import build_checks, expected_reports

if __name__ == '__main__':
    source, names = build_checks()
    raise SystemExit(main(source, expected_reports(names), 'NumberLab'))
