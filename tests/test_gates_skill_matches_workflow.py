"""The gates skill names every gate script the workflow runs.

The skill is prose and drifts; `.github/workflows/verify.yml` is what CI
actually runs.  Every `python ci/...py` or `python research/...py` command
the workflow issues, `python3` included, must be named in
`.claude/skills/gates/SKILL.md`, so a
gate the skill omits fails here by path."""

from __future__ import annotations

from pathlib import Path
import re

REPO = Path(__file__).resolve().parent.parent
WORKFLOW = REPO / ".github" / "workflows" / "verify.yml"
SKILL = REPO / ".claude" / "skills" / "gates" / "SKILL.md"
COMMAND = re.compile(r"python3? ((?:ci|research)/[A-Za-z0-9_./-]+\.py)")


def workflow_scripts() -> list[str]:
    return sorted(set(COMMAND.findall(WORKFLOW.read_text(encoding="utf-8"))))


def test_every_workflow_gate_script_is_named_in_the_gates_skill() -> None:
    scripts = workflow_scripts()
    assert scripts, "the workflow names no gate script — the pattern is broken"
    skill = SKILL.read_text(encoding="utf-8")
    missing = [s for s in scripts if s not in skill]
    assert missing == [], f"workflow gate scripts absent from the gates skill: {missing}"
