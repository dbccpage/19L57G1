import json

import pytest

from eg_reports import parse_report, report_program, validate_payload


def test_report_requires_actual_terminal_and_population() -> None:
    theorem = {"module": "M", "declaration": "M.t", "kind": "theorem", "elaborated_type": "True",
               "local_hypotheses": [], "conclusion": "True", "axioms": []}
    lines = ['EG_REACH ["M"]', 'EG_MODULE "M"', "EG_THEOREM " + json.dumps(theorem), 'EG_END {"modules": 1, "theorems": 1}']
    report = parse_report("\n".join(lines), ["M"])
    validate_payload(report)
    report["theorems"][0]["local_hypotheses"] = [{"name": "h", "type": "False"}]
    with pytest.raises(ValueError, match="COMPILED_PAYLOAD_CHANGED"):
        validate_payload(report)
    with pytest.raises(ValueError, match="COMPILED_MODULE_POPULATION"):
        parse_report("\n".join(lines[:-1]), ["M"])
    with pytest.raises(ValueError, match="COMPILED_MODULE_POPULATION"):
        parse_report("\n".join(lines), ["M", "Extra"])


def test_generated_program_has_no_unvalidated_module_input() -> None:
    assert b"import M" in report_program(["M"])
    with pytest.raises(ValueError, match="REPORT_MODULE_POPULATION"):
        report_program(["M\nrun_cmd"])
