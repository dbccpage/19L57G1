# Bit index (plan)

A structured **128-bit** key (16-byte BLOB). **Not a hash.**
Collisions only if the same (repo, track, program, paper,
claim) tuple is reused. Allocation is sequential and gated
by the database.

Low 64 bits are the original field layout. High 64 bits
default to zero (epoch + reserved).

| Bits | Field | Encoding |
| --- | --- | --- |
| 0–3 | repo | `0000` = 19L57G1 |
| 4–5 | visibility | 00 private, 01 public, 10 unknown, 11 reserved |
| 6–7 | track | 00 N, 01 X, 10 Q, 11 reserved |
| 8–15 | program L1 | controlled vocabulary, 256 slots |
| 16–23 | program L2 | under L1 |
| 24–31 | program L3 | optional or 0 |
| 32–47 | paper seq | within (repo, track, program) |
| 48–63 | claim seq | within paper; 0 = the paper itself |
| 64–95 | generation / epoch | 0 = native |
| 96–127 | reserved | must be zero until defined |

`CHECK (length(bit_key) = 16)` is mandatory in the planned
schema. Short keys are a hard failure.

See `id_schemes.md` for why UUID v7 is not this key. If a
UUID wire form is required, encode the same bits as UUID v8.

Human form example: repo 0, private, spine, L1 mathematics,
L2 foundations, paper 3, claim 12 → 16-byte blob → hex token
in the ledger.

16 bits of paper seq = 65536 papers per program node. 16 bits
of claim seq = 65536 claims per paper. Epoch and reserved
words are unused (zero) until defined. No birthday paradox:
allocation is enumerative.

MSC / arXiv / LoC / HEP codes are optional attributes on the
paper. They are never the primary key.

## Prefix (human identity)

Example: `CL-0-INERTIA`. Track-local namespace + stage +
mnemonic. Unique constraint is on the bit key, not the
mnemonic. A prefix rename is a change-log event.

The earlier `OER-NNN` idea is withdrawn as the primary key.
It may appear as an alias during migration.
