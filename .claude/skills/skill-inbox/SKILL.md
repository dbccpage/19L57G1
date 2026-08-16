---
name: skill-inbox
description: Append a candidate skill idea to the skills inbox. Use when someone proposes a new skill, a gap in the existing set, or a procedure worth capturing as apparatus.
---

# Skill inbox

**AuthorityEffect: None.** This skill only appends a dated note to a
markdown file. It creates no skill directory, registers no claim, and
gates nothing. An entry here is a candidate, not an approval.

Filing is not deciding. Nothing downstream reads this file, so an entry
changes no behaviour until a separate reviewed change implements it.

## What to do

Append one block to `paper/skill_inbox.md` (create the file with the
header below if it does not exist):

```markdown
## YYYY-MM-DD — <short name>

- **Need:** one sentence on the gap
- **Proposed behaviour:** what the skill would run or record
- **Not in scope:** what it must not do (authority, merge, ledger, math)
- **Source:** who/what suggested it
```

Rules:

- Append only. Never edit or delete earlier entries. The record of what
  was proposed and when is the point; rewriting it destroys the data.
- Do not create `.claude/skills/<name>/` from this skill.
- Do not treat an inbox entry as a commitment to implement, a schedule, or
  a priority.
- Use an absolute date, not "today" or "last week".

## Header for a new file

```markdown
# Skill inbox

Candidates only. AuthorityEffect: None. Nothing here is approved or scheduled.
```

## What this cannot do

It cannot judge whether a candidate is a good idea, and no gate checks the
entries. `ci/check_skills.py` will check the SHAPE of any skill that is
eventually built from an entry here, and nothing more — it never inspects
this inbox.
