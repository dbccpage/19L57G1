"""Reasoning book proofs and their exact axiom reports; AuthorityEffect: None."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from booklean import BOTH, NONE, PROPEXT, main  # noqa: E402
from textbook.reasoning_lab.lean_cases import NAMES, SOURCE  # noqa: E402
from textbook.reasoning_lab.protocols_lean import expected_reports  # noqa: E402
from textbook.reasoning_lab.calibration_lean import expected_reports as calibration_reports  # noqa: E402

if __name__ == "__main__":
    expected = {"Textbook.ReasoningLab." + name: NONE for name in NAMES}
    expected["Textbook.ReasoningLab.recover_on_smaller_domain"] = PROPEXT
    for name in ("individual_without_common", "no_recovery_on_full_domain"):
        expected["Textbook.ReasoningLab." + name] = BOTH
    expected.update(expected_reports())
    expected.update(calibration_reports())
    raise SystemExit(main(SOURCE, expected, "ReasoningLab"))
