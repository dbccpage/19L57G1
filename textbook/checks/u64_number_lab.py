"""Source-backed numerical teaching calculations; AuthorityEffect: None."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from textbook.number_lab.run_lab import check_recorded

if __name__ == '__main__':
    print(check_recorded())
