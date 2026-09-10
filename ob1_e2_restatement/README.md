# OB-1 E2′ restatement diagnostic

AuthorityEffect: None. Planning packet at the repository root: outside
the sealed derivation (`prompt/`, `paper/`, `code/`, `lean4/Derivation/`,
`artifacts/`) and outside `research/`. Not a research tree. Not
registered in CI.

`reclassify.py` reprints the E2 vs E2′ table. `FINDING.md` records the
fork: Outcome B on owed separation, not Outcome A.

Census pin: `b947873` (`research/endogenous_demand/candidates.py`
digest). The script imports the live tree read-only and fails if that
file's bytes move. `python reclassify.py --check` fails if `FINDING.md`
drifts from a fresh table.
