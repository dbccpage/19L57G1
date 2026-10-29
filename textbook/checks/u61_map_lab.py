"""Map-lab source correspondence; AuthorityEffect: None."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from textbook.map_lab.run_lab import check_recorded, check_population  # noqa: E402

if __name__ == "__main__":
    print(check_recorded())
    print({'additional_factorization_cases': check_population()})
