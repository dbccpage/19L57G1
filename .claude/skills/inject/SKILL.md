---
name: inject
description: Prove a gate by making it fail on the exact defect it claims to catch, then reversing the injection. Use when adding a new gate or census, when asked whether a gate actually works, or before claiming a gate protects anything.
---

# Prove a gate by injection

**AuthorityEffect: None.** This skill manufactures a temporary defect and
reports what failed. It approves nothing, merges nothing, registers no
claim, and leaves no permanent change. Its output is evidence about one
gate's behaviour on one injected defect — nothing wider.

## The standard

A gate is **not** proved by being green. Green shows only that the gate is
quiet. A gate is proved when:

1. it fails on the injected defect, **and**
2. the failure message names the injected object, **and**
3. it is green again after the injection is reversed, **and**
4. no other gate's receipt was silently altered.

"Observed to pass" is never evidence. "Failed on the injected defect, then
recovered" is.

## Rules for injecting cleanly

- **Localise.** One file, one line, one token where possible. The failure
  message should name that object.
- **Name the probe** so reversal is obvious: `PinProbe.lean`,
  `run_zzz_probe.py`, a comment reading `INJECTION: remove before merge`.
- **Never regenerate a receipt while an injection is live.** Regenerating
  `artifacts/lean_axioms.txt` or `artifacts/elaborated_modules.txt` under
  an injection adopts the defect as the new baseline and destroys the
  test. This is the single easiest way to turn a real proof into a fake
  one.
- **Capture the exact failure line and exit status.** That log is the
  evidence, not your recollection of it.
- **Reverse, then re-run.** Green after reversal is the second half of the
  proof. Confirm with `git status` that nothing survived.

## Injections by gate class

**Population / census gates.** Add a file that belongs in the census; the
pin must fail. Remove one that belongs; it must fail. Point the enumerator
at a directory with no matches; the empty guard must fire before the pin
is consulted. Change the sort locale; the pin must fail, because it is
only as strong as the exact serialisation CI uses.

**Content / receipt gates.** Change one byte in a committed JSON. Delete
one regenerated export. Add an export that was never committed. Alter a
summary's `full_export_sha256` without touching the gzip content.

**Forbidden-token gates.** Insert `sorry`, `admit`, `unsafe`, `partial`,
or a leading `axiom` — including inside a comment or docstring, since the
scan is plain text over whole files. Wrap a prose line so `axiom` begins a
physical line; the pattern is `^\s*axiom\s` and it will fire.

**Domain / reach gates.** Put a type error only in a module the root does
not import. This is the original defect that motivated the per-module
elaboration step.

**Totality / dual-population gates.** Add a citation form one pattern can
see and the other cannot.

**Operator / tooling gates.** Run a command with a flag that does not
exist and watch it return "no matches", which reads as a clean result.
Diff against a moving branch name instead of a pinned SHA. Both have
produced false clean results here, for author and reviewer alike.

## What injection cannot prove

- **That the population is the right mathematical object.** A perfect pin
  of the wrong set is still the wrong set. Injection shows only that the
  gate fires when the live enumeration diverges from the committed pin.
- **That every declaration is free of classical dependencies.** An
  earlier version of this bullet said parked modules "emit no `#print
  axioms` report, so the whitelist never sees them"; that is WITHDRAWN, and
  injection is how the closure was shown to bite — the same defect went
  green before `lean4/ParkedAudit.lean` and failed after. What injection
  still cannot close: the census reports theorems, so a definition carrying
  an axiom that no theorem reaches is unreported, and no census covers a
  top-level `lean4/*.lean`.
- **That a reviewer will follow a procedure.** Behaviour outside the
  machine is outside the domain of any injection.

Record what was injected and what failed. `docs/injection_record.md` carries
the standing table (moved from `CLAUDE.md` on 2026-09-21).
