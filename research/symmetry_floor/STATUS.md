# STATUS — symmetry_floor

`AuthorityEffect: None.` Open research tree. Nothing under the seal is touched:
no file outside `research/symmetry_floor/` is added, changed or read as input.

## Terminals

| terminal | scope |
| --- | --- |
| `FLOOR_PROVED` | A state-read single-valued rule cannot break a renaming the state holds still. Lean, no axioms. Arbitrary `G`, `act`, `X`. |
| `CHARACTERISATION_EXHAUSTED` | Held-set containment is necessary and sufficient, over all 30,625 pairs at dividers ≤ 2, data ≤ 3. |
| `COUNT_EXHAUSTED` | All 16,777,216 maps on a closed 8-inscription carrier enumerated; 128 agree, matching the characterisation. |
| `EXIT_PRICED` | 2 offered successors to break one renaming, 4 to break every one. |
| `THREAD_UNIQUE_TO_GENERATION_8` | Exactly one object per generation is held still by everything, to generation 8. Not proved beyond. |
| `DEPARTURE_IRREVERSIBLE_TO_GENERATION_7` | No step lowers the distance, to generation 7. Not proved beyond. |
| `CLOSED_FORM_TO_GENERATION_10` | `objects(k) = a(ceil(k/2))·a(floor(k/2))`, verified to 10. Not proved. |

## How to run it

From this directory:

```powershell
python -m unittest discover -s . -p "test_*.py"
python -m mypy
python floor.py
python thread.py
```

The Lean is mathlib-free and typechecks standalone, printing its own axiom
reports:

```powershell
cd lean
lean SymmetryFloor.lean
```

Expected: `floor` and `floor_iterated` depend on no axioms; the four `decide`
results depend on `propext`, which is inside the repository whitelist.

## Cost

The suite runs in about **two and a half minutes**, dominated by
`test_exhaustion_over_every_map`, which enumerates all 16,777,216 maps. That
cost is the point of the test and is not reducible without weakening the claim
from *exhaustion* to *sampling*. Recorded here so the runtime is not mistaken
for a hang.

## Not registered with the gate

This tree is **not** listed in `CLAUDE.md`'s gate-11 command block, so no gate
runs it. Registering it is an amendment to that file, which is the author's act
and not an agent's. If the author wants it gated, the addition is:

```powershell
cd research/symmetry_floor
python -m unittest discover -s . -p "test_*.py"
python -m mypy
cd ../..
```

Until then, **every result here is a local receipt**, run by hand at the commit
this tree was written on. No hosted run exists or is expected
(`CLAUDE.md`, *No hosted CI — settled, do not reopen*).

## Checks run before this tree was written

Recorded because they constrain what could be written, not as results:

- The 102 barred identifiers of `tests/test_primitive_contact.py` were read and
  none collides with a name used here.
- The prose census of `ci/check_prose_watchlist.py` omits files with no hits, so
  this tree was written to have none.
- The forbidden-token scan reads comments as text. The Lean file therefore does
  not name the tokens it avoids.

## Leftover

`CLAIM_LEDGER.md` carries four open items, SF-OPEN-1 to SF-OPEN-4. The two that
matter are the unpriced alternatives: supplying one asymmetry at the start, and
refusing a first state at all. Neither is done here and neither should later be
counted as done.
