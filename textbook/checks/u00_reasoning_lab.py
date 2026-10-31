"""Reasoning population and source-encoding check; AuthorityEffect: None."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from textbook.reasoning_lab.run_lab import check_population, check_recorded, check_evidence_population  # noqa: E402
from textbook.reasoning_lab import protocols  # noqa: E402
from textbook.reasoning_lab import calibration  # noqa: E402

if __name__ == "__main__":
    print(check_recorded())
    print(check_evidence_population())
    print(check_population())
    print(protocols.check_recorded())
    print({'bounded_protocol_orders':protocols.check_population()})
    print(calibration.check_recorded())
    print({'bounded_calibration_cases':calibration.check_population()})
