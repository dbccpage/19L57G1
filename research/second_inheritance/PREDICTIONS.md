# Predictions, written and hashed before the first run

`AuthorityEffect: None`.  Each prediction carries its falsifier.  A missed
prediction is recorded next to its value in `STATUS.md` and never edited
here.  The sha256 of this file as frozen is recorded in `STATUS.md` and
pinned by `test_inheritance.py`.

- R0-1 (replay).  The sealed challenge reports and both closed baselines
  regenerate from the sealed kernel and agree with the committed
  artifacts on every compared field, and the sibling dual summary
  regenerates byte for byte.  Falsifier: any compared field or byte that
  differs.
- R0-2 (grammar census).  The sealed event grammar has exactly six event
  kinds, exactly one of which never changes state; the sealed engine
  declares exactly two policies; the sibling dual tree declares exactly
  three events; and the two inputs the seed names as remaining are
  supplied by trees absent from `main` at the snapshot, so their custody
  is OPEN.  Falsifier: a different count, or either named tree present.
- R0-3 (inertia).  From both sealed genesis readings, any number of
  supplies up to the bound leaves the regime unchanged; under no
  declaration and under the all-free stake the demand set is empty at
  every state; growing to the data bound under the all-free stake admits
  no form, answers nothing, and leaves every state totally collapsed, so
  the tree is a single chain of growth steps.  Falsifier: a changed
  regime, a demand, an admitted form, or a branch.
