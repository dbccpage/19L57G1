"""Bundle the passage desk with the shared local renderer; AuthorityEffect: None."""
from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from textbook.search_lab.build_results import build, render  # noqa: E402,F401

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "results.html")
    args = parser.parse_args()
    build(Path(__file__).resolve().parent, args.output)
    print(args.output.resolve())
