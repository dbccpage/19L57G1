# Verification record — 2026-08-17

**What this is.** A dated, measured run of the verification contract,
recorded because `CLAUDE.md` said the 2026-08-16 stopping-conditions
report was an operator claim that no gate consumes. This record does
not consume it either. It reports what commands printed.

**Object under test:** `052e657` (merge of pull request #57), plus one
uncommitted repair to `paper/native_derivation_completion.md` §3
described below. Run locally on Windows, Python 3.14.2, Lean 4.33.0 —
**not** a CI run. CI is the authority; this is a local reproduction.

**AuthorityEffect:** None. Every line is a quotation of a command's
output, not a judgement about the mathematics.

---

## The eight gate families, as measured

| # | Gate | Result |
|---|---|---|
| 1 | prompt byte-identity | `prompt/prompt.md` `a613a196…`, `prompt/seed_prompt.md` `4ea4682e…` — both match |
| 2 | transport citations | 190 verified, 0 unresolved |
| 3 | tests + independent 95% line/branch | **line 99.10%**, **branch 96.73%**, report covers 54 source files matching the tree, no source modified since it was written |
| 4 | mypy strict | no issues in 54 source files |
| 5 | artifact regeneration | 24 runners executed; 37 json byte-identical, 6 full exports content-identical and hash-pinned, export sets equal in both directions |
| 6 | Lean build + audits | 56 sources, **1314** axiom reports, all within `{propext, Quot.sound}`; report matches the committed artifact; `lean_axioms.txt` regenerates byte-identically (126519 bytes, LF); module census (55) matches `elaborated_modules.txt` |
| 7 | skills declare no authority | 6 skills, each carrying `AuthorityEffect: None` |
| 8 | paper cross-references | 46 citations across 28 documents, all resolve |

Freshness was enforced rather than assumed: `coverage.json` was deleted
before the run and confirmed absent, then confirmed present after — the
stale-report false pass is on record as having happened twice in one
evening, and a file-set check alone does not catch it.

The Lean log was a **full 56-module build**, not an incremental one, so
the 1314 `#print axioms` reports are present in it rather than inherited
from a previous run.

## One repair made during the run

`paper/native_derivation_completion.md` §3 stated the dependency-graph
inventory carried "one record per exported theorem (295)" in the present
tense. The inventory holds **1314**. §18 of the same file already marked
295 as a snapshot and named 1314, so the file carried the figure both
dated and undated; the undated one is now dated. Containment is
unaffected at either count. Found by recomputing rather than by any
gate.

## What this run does NOT establish

This is the part that matters, and it is why the `CLAUDE.md` sentence is
narrowed rather than deleted.

`CLAUDE.md`'s stopping conditions have two kinds of clause. The
mechanical ones are discharged above. The rest are **operator
judgements that no gate can consume**, and running the gates does not
touch them:

- every introduced notion has a source classification;
- every theorem-level claim has Lean evidence **or is downgraded** — the
  audit shows 1314 reports are axiom-clean, not that the paper's claims
  correspond to them;
- all tied minimum branches are retained unless eliminated by proof;
- the paper states the strongest defensible terminal result without
  targeting a predetermined conclusion.

A green run is evidence about what the commands inspected. It is not a
verdict on the mathematics, and reading it as one would be the exact
substitution this repository exists to refuse.

## Standing residual, unchanged

**Elaboration is not auditing.** Every module under `lean4/Derivation/`
elaborates against the pinned census, but a module the root does not
import emits no `#print axioms` report, so the whitelist never inspects
it. "Axiom-clean" is a claim about the 1314 enumerated reports, not
about every declaration in the tree. Closing this needs a
compiler-emitted declaration census; the regex approach is already known
to fail here. It remains **OPEN**.

`AuthorityEffect: None.`
