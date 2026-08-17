# Change log — NSA-000

**Paper:** `000_no_self_authorization.md`
**AuthorityEffect:** None.

## v0.1 draft (2026-08-17)

First public-object packaging pass. Author has not minted Zenodo.

- Manuscript completed as `000_no_self_authorization.md` with
  mechanism inventory, refusal box, why-care, falsifiability,
  import fence. Body §§1–6 written. Counts cite
  `coda/figures.md` only.
- LinkedIn face: `linkedin_essay.md`.
- Illustration package `src/nsa000/` (gauges, ties, selection,
  Born lift, two figures). Tests required at 100% line coverage
  of that package.
- Notebooks: `00_enter_nsa000.ipynb`, `01_falsify_nsa000.ipynb`.
- `paper.md` reduced to a pointer so it is not a second source.

## v0.1 (same day) — standing attacks, no reveal

- Added `attack_list.md`. Win condition is withdrawal, not
  an unbroken panel.
- Added `situating.md`: comparison permitted in `coda/`,
  not written. Attack 1 remains unanswered.
- Paper: slogan scoped as near-definitional; `FIG-*` named
  as the contribution; authority-source left unanswered;
  “there is more coming” withdrawn as a reveal.
- Essay: last section made boring. Pedagogy, then the paper.

No theorem status in the sealed derivation was changed.

## v0.1 (same day) — review repairs, four hard findings

Found by review of pull request #55 at `1ed7341`. Each was verified
against the machine before repair, not inferred.

**The amplitude lift did not do what it claimed.**
`optional_amplitude_lift` built amplitudes from the RAW weights,
`sqrt(w)`, while its docstring claimed `|c|^2` recovers
`born_from_weights(w)`. It recovered `w` instead, so the two agreed
only when the weights already summed to one. The lift is the module's
whole point — that the amplitude encoding *reproduces* the unit-sum
law and adds nothing — so a lift that failed to reproduce it
demonstrated nothing. Now built from the normalised probabilities.

**The test was hiding it.** `test_born_and_lift` compared
`born_from_weights(modulus_squared(amps))` against `p`, normalising a
second time and cancelling the defect. It now compares
`modulus_squared(amps)` directly, with weights that sum to 4, and
fails against the old implementation. WITHDRAWN: the previous
assertion, which certified a weaker property than the docstring
stated.

**The public zip was not reproducible.** Entries were written with
`zf.write()`, which copies each file's mtime; the committed archive
carried ten distinct wall-clock timestamps. Rebuilding on any other
checkout produced a different digest, so `SHA256SUMS` could not be
verified by anyone but its author — the one thing shipping sums is
for. Entries now carry a fixed 1980-01-01 mtime and a fixed mode,
the same fix `CLAUDE.md` already applies to the repository's
`*.json.gz` exports.

**The shipped zip contained notebooks the repository did not have.**
Both `.ipynb` files had been edited after the archive was built and
the archive was never rebuilt, so two of twenty-four `SHA256SUMS`
entries did not match the tree and the published falsify face was
stale. Rebuilt after all content changes above, in that order.
`scripts/build_zip.py --verify` now checks the sums against the tree,
because the build alone cannot detect a mutation that happens after
it.

Also: non-finite weights and phases are refused. `NaN` passed both
`w < 0` and `total <= 0` and reached the division, returning `NaN`
probabilities silently.

Not repaired here, and left for the author: the reserved
`paper/coda/` tree was removed from this branch rather than carved,
because amending the repository contract is the author's act.
