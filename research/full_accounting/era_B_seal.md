# Era B — seal, isolate, stopping re-run (2026-08-17)

`AuthorityEffect: None.` 22 commits this day at the walk snapshot.

| SHA | what |
|---|---|
| `59738b00` | Re-run stopping conditions; `verification_20260817.md`; date a stale count |
| `052e657` | Merge PR #57 coda/boundary-and-pin — **this is the seal SHA named in CLAUDE.md** |
| `e34daf06` | Itemize section 12 residuals into a typed register |
| `27a1bba8` | Isolate: remove `coda/` and `coda_meta/` from this repository |
| `9c822e66` | Close R1, R2, R3, R6: mention lemma and count-invariance transport |

Mechanical clauses at `052e657` (line 99.10%, branch 96.73%, 1314
axiom reports within `{propext, Quot.sound}`, artifacts
byte-identical, prompt hashes matching). Judgement clauses of the
stopping conditions remain operator claims: source classification of
every notion; every theorem-level claim has Lean or is downgraded;
tied minima retained unless eliminated by proof; paper states the
strongest defensible terminal.

Coda timeline, because the pin is easy to mis-read:

- `7da1eee0` 2026-08-16 — `coda/` and `coda_meta/` appear.
- `1ed7341a` 2026-08-17 — `paper/coda/` lands (seal breach).
- `6c3d8807` — `paper/coda/` removed (30 files).
- `fd7e3922` — `coda_meta/` moved to a private external repository.
- **`052e657` — `coda/` still in-tree**; `paper/coda/` already gone;
  `coda_meta/` already a pointer.
- `27a1bba8` (after the pin) — `coda/` and `coda_meta/` removed from
  this repository.

After isolate, **external citation is not permitted anywhere in this
repository**. The exception existed only for directories that left.

`Mention.lean` / `CountTransport.lean` land **after** `052e657` the
same calendar day (`9c822e66`); they are sealed residuals, not a new
genesis. R4, R5, R7, R8 close 2026-08-18 (Era C).
