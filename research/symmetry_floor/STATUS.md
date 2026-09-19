# STATUS — symmetry_floor

`AuthorityEffect: None.` Open research tree. Nothing under the seal is touched.
The only changed path outside `research/symmetry_floor/` is the corresponding
local-receipt row and count in `research/README.md`.

## Terminals

| terminal | scope |
| --- | --- |
| `FLOOR_PROVED` | A renaming-equivariant single-valued rule cannot break a renaming the state holds still. Lean, no axioms. Arbitrary `G`, `act`, `X`. This preserves the held set; it does not force the successor to equal the state. |
| `CHARACTERISATION_EXHAUSTED` | Held-set containment is necessary and sufficient, over all 30,625 pairs at dividers ≤ 2, data ≤ 3. |
| `COUNT_EXHAUSTED` | All 16,777,216 maps on a closed 8-inscription carrier enumerated; 128 agree, matching the characterisation. |
| `EXIT_PRICED` | Within the declared finite carrier, invariant offered sets need at least 2 successors to break one non-identity renaming and 4 to break all three. |
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

Since 2026-09-18 that expectation is also checked rather than read off by
eye. From this directory:

```powershell
python verify_lean.py --check
```

It runs the same `lean SymmetryFloor.lean`, requires exactly the six
reports with the axioms above, and compares them with every theorem the
compiled file contains, generated ones included. It adds no lakefile and
writes no tracked file. Like everything else here it is a local receipt:
no gate runs it.

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
