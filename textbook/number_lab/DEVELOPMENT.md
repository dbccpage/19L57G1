# Reproduce the Number lab

AuthorityEffect: None. Run from the repository root after the existing
sealed library has been built. These commands do not write to native
research sources or receipts.

```powershell
python textbook/number_lab/run_lab.py
python -m unittest discover -s textbook/number_lab -p "test_*.py"
python textbook/checks/u64_number_lab_lean.py
python -m unittest discover -s textbook/media -p "test_number_lab_wiki.py"
python ci/check_textbook.py --python-only
```

`run_lab.py` recomputes the finite populations listed in the source map,
compares the packet and count table, and regenerates each SVG in memory
to detect stale figures. `--write` intentionally refreshes only teaching
records and figures. Review the meaning of any change; never update a
native receipt or watchlist pin to accommodate a lesson.

The Lean driver uses the existing compiled sealed library and reads exact
research sources into a temporary book driver. Research imports are
replaced only by the corresponding included texts. The driver reports
the precise selected theorem list and its expected axiom dependencies.
Research build directories remain untouched. This does not run a complete
research-tree verifier or prove the model applies to an apparatus.

The authoring tests inject wrong proportions, zero-domain claims,
forgotten signs, coordinate readings, determination, group counts, and
stale figures. Wiki checks reject false pages and assets. Rendered PNG
previews separately check the static figures' legibility, bounds, and
text collisions. This route adds no custom browser application; hosted
rendering and responsive layout need their own review.

The full textbook job and the repository's twelve local gate families
are distinct checks. Keep their receipt scopes explicit. Reader feedback
supports readability but does not establish scored novice transfer or
retention.


For the fraction branch, run `python textbook/number_lab/fraction_toolkit.py`.
The existing `u64_number_lab.py` now checks those named examples and finite
populations alongside the original packet. Seven added book identities
are checked by `python textbook/checks/u00_reasoning_lab_lean.py`, using
the QVal body already consumed there. The Number readout driver stays
at 37 reports; the combined Reasoning driver has 155. Two assembled false
fraction conclusions fail and unmodified source recovers.

The existing Number Wiki authoring tests now expect 21 pages, with direct
core/prerequisite and fraction-practice links. The old packet and all five
figures are unchanged. Published hub disclosures, lesson examples, keyboard
use and narrow layout are checked separately; no new browser application
or synthetic learning result is added.
