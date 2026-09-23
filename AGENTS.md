# AGENTS.md

Instructions for any coding agent working in this repository. `CLAUDE.md` is
the full contract and the authority; this file is the short form. Where the
two agree, follow either; where a detail is only in `CLAUDE.md`, `CLAUDE.md`
governs.

## No hosted CI — settled, do not reopen

**This repository does not use hosted GitHub Actions CI, and never will.**
It is a permanent decision by the author (2026-09-08), not an outage or a
billing problem. Do not propose enabling, restoring, paying for, or
"fixing" hosted CI. Do not treat an absent, dormant, skipped, or failed
Actions run as a defect — there is nothing there to investigate.

`.github/workflows/verify.yml` is the written contract only: the canonical
list of the twelve gate families and their order. It does not execute.
"Green" means the gates were run **locally**, by the author or by an agent
at the author's direction, and the pass is a local receipt. A merge rests
on those local receipts; the absence of a hosted check never blocks it.

See `CLAUDE.md`, section **No hosted CI**, for the full statement.

## The rest, in one breath

- The author merges; an agent prepares the pull request and does not merge
  unless told to. Every pull request targets `main` directly; no stacked
  pull requests.
- The blind protocol seals `prompt/`, `paper/`, `code/`, `lean4/Derivation/`,
  `artifacts/` and the root file `lean4/Derivation.lean`; do not edit those
  or `CLAUDE.md` without the author's explicit say-so. Research lives under
  `research/`, outside the seal, and consumes the sealed sources read-only.
- No external terminology as an input to the sealed derivation. Outside
  the seal, research may use explicitly classified supplied vocabulary;
  this supplies no native derivation or proved bridge. The six existing
  fenced paper comparisons remain historical records in their existing
  positions. External citations remain prohibited repository-wide. The
  prose watchlist and identifier firewall keep their current populations.
  See the author's 2026-09-23 vocabulary ruling in `CLAUDE.md`.
- Run the twelve gate families locally before asking for a merge, with
  `python ci/run_gates.py` (see `CLAUDE.md`, **Running the gates**);
  `research/README.md` says which research trees the contract enumerates.
