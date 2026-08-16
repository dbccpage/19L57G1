---
name: anti-skill-inbox
description: Append an anti-skill — a procedure this repository should refuse to encode, or a reverse of an existing skill — to the anti-skill inbox. Use when a proposed automation would launder authority, hide a residual, or reintroduce a known failure mode.
---

# Anti-skill inbox

**AuthorityEffect: None.** This skill only appends a dated note to a
markdown file. It bans nothing by itself and registers no claim. An
entry here is a warning, not a rule change.

An anti-skill is a procedure or habit this repository should REFUSE to
encode — often the reverse of a skill that already exists. "Merge on
green." "Trust a receipt without asking its domain." "Count theorems by
grepping for `theorem`." Each of those is a real failure this repository
has paid for, and each would look like a reasonable automation.

## What to do

Append one block to `paper/anti_skill_inbox.md` (create the file with the
header below if it does not exist):

```markdown
## YYYY-MM-DD — <short name>

- **Anti-pattern:** one sentence on the behaviour to refuse
- **Why it is anti:** which residual, gate, or failure mode it would hide or reintroduce
- **Related skill (if any):** the skill whose reverse this is
- **Source:** who/what surfaced it
```

Rules:

- Append only. Never edit or delete earlier entries.
- Do not implement enforcement from this skill.
- Do not treat an anti-skill entry as a CI gate. Enforcement, if it is
  ever wanted, is a separate change with its own review and its own
  injection evidence.
- Prefer anti-patterns that ACTUALLY OCCURRED here, with the incident
  named. A hypothetical anti-pattern is weaker evidence than one that
  already cost something.

## Header for a new file

```markdown
# Anti-skill inbox

Procedures this repository should refuse to encode as skills.
AuthorityEffect: None. Nothing here is enforced by CI unless a separate
gate is added later under its own review.
```

## What this cannot do

It cannot prevent anything. Recording an anti-pattern is not a control,
and reading this file is not a gate. Treating the list as protection would
itself be an anti-pattern — the same one `paper/pr_review_template.md`
records about itself.
