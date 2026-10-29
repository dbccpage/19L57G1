"""Bundle the growth desk; AuthorityEffect: None."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from textbook.search_lab.build_results import build, render  # noqa: E402,F401
if __name__ == '__main__':
    source=Path(__file__).resolve().parent
    build(source, source/'results.html')
