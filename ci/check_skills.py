"""Skill declaration gate.

Usage: python ci/check_skills.py

Skills in ``.claude/skills/`` are APPARATUS. They run commands and report
what the commands printed. They hold no authority in this repository: they
approve nothing, merge nothing, register no claim, and gate nothing. A
skill's output is evidence about the command it ran and about nothing
wider.

That is a property worth enforcing rather than asserting, because prose
drifts. Every skill must therefore carry the literal line
``AuthorityEffect: None``. A skill that quietly acquires authority by
rewording its own description fails here.

Each skill must:

* live at ``.claude/skills/<name>/SKILL.md``;
* open with YAML frontmatter delimited by ``---`` lines;
* declare ``name`` and ``description`` in that frontmatter;
* have ``name`` equal to its directory name, so the invoked skill and the
  tracked file cannot diverge;
* contain the literal line ``AuthorityEffect: None`` in its body.

The population is enumerated by a filesystem walk, independently of the
frontmatter parser that classifies it. A malformed skill therefore fails
the check instead of vanishing from both sides of it -- the failure mode
that once made the transport citation totality invariant tautological.

This gate does NOT judge whether a skill's procedure is correct, and it
cannot: a skill is prose plus commands, and no CI step can check that a
human or a model followed it. It checks the declaration and the shape.
Read a pass as "every tracked skill is well formed and declares no
authority", never as "the skills are right".
"""

import pathlib
import sys

SKILL_ROOT = pathlib.Path(".claude") / "skills"
AUTHORITY = "AuthorityEffect: None"


def frontmatter(text: str) -> dict[str, str] | None:
    """Parse the leading ``---`` block. None if it is absent or unclosed."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fields: dict[str, str] = {}
    for index in range(1, len(lines)):
        line = lines[index]
        if line.strip() == "---":
            return fields
        key, sep, value = line.partition(":")
        if sep and not key.startswith(" "):
            fields[key.strip()] = value.strip()
    return None


def main() -> int:
    failures: list[str] = []
    if not SKILL_ROOT.is_dir():
        print(f"no {SKILL_ROOT} directory; no skills to check")
        return 0

    # Population: the filesystem, not the parser.
    skill_files = sorted(SKILL_ROOT.rglob("SKILL.md"))
    directories = sorted(p for p in SKILL_ROOT.iterdir() if p.is_dir())

    if directories and not skill_files:
        print(
            f"FAIL: {SKILL_ROOT} holds {len(directories)} directories and no "
            "SKILL.md - the enumeration is broken or every skill is malformed"
        )
        return 1

    for directory in directories:
        if not (directory / "SKILL.md").is_file():
            failures.append(f"{directory}: directory with no SKILL.md")

    for path in skill_files:
        text = path.read_text(encoding="utf-8")
        fields = frontmatter(text)
        if fields is None:
            failures.append(f"{path}: missing or unclosed --- frontmatter")
            continue
        for required in ("name", "description"):
            if not fields.get(required):
                failures.append(f"{path}: frontmatter has no {required}")
        declared = fields.get("name", "")
        expected = path.parent.name
        if declared and declared != expected:
            failures.append(
                f"{path}: frontmatter name {declared!r} does not match "
                f"directory {expected!r}"
            )
        if AUTHORITY not in text:
            failures.append(f"{path}: does not declare {AUTHORITY!r}")

    for failure in failures:
        print(f"FAIL: {failure}")
    if failures:
        return 1
    print(
        f"skills well formed: {len(skill_files)} skill(s), each declaring "
        f"{AUTHORITY!r}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
