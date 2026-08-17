# Prefix table — bits 0–3 (plan)

**AuthorityEffect:** None. Versioned mapping object. Letters
are human-facing. Bit codes are machine-facing. Agents and
extractors must read this table. They must not hard-code
either side.

This is the ConfigGauge for the striping layer. A change
here is claim drift for any spine that observes it.
Supersession requires a reason and a pointer. Assigned bit
codes are immutable. Letters may be renamed by supersession.

Parent: `multi_repo.md`. How remotes are earned:
`repo_split.md`. OES composition: `oes.md`.

## Sealed 16-row table (v0)

| Bits | Letter | Status |
| --- | --- | --- |
| `0000` | OER | **assigned.** This vault. Citer. Not a product factory. |
| `0001` | — | **assigned.** Unknown / other. |
| `0010` | — | reserved / never allocate until an admit names the letter |
| `0011` | — | reserved / never allocate until an admit names the letter |
| `0100` | — | reserved / never allocate until an admit names the letter |
| `0101` | — | reserved / never allocate until an admit names the letter |
| `0110` | — | reserved / never allocate until an admit names the letter |
| `0111` | — | reserved / never allocate until an admit names the letter |
| `1000` | — | reserved / never allocate until an admit names the letter |
| `1001` | — | reserved / never allocate until an admit names the letter |
| `1010` | — | reserved / never allocate until an admit names the letter |
| `1011` | — | reserved / never allocate until an admit names the letter |
| `1100` | — | reserved / never allocate until an admit names the letter |
| `1101` | — | reserved / never allocate until an admit names the letter |
| `1110` | — | reserved / never allocate until an admit names the letter |
| `1111` | — | reserved / never allocate until an admit names the letter |

No ad-hoc allocation. A second repo that starts minting keys
before a reserved row is admitted is already violating the
law.

## Named letters waiting for a row

These letters are vocabulary. They do **not** have bit codes.
Assigning a code is the same admit that may cut a remote
(`multi_repo.md` earn checklist). The 4-bit field is small
(14 free). First remotes consume at most three more rows.
Later letters and OEE wait. Overflow, hierarchy, or reuse is
an open residual, not a license to widen the field here.

- OEC — Omega Engine
- OEAS — swarm base class
- OEAG — governance (policy packs; not a live checkout)
- OEOS, OEAR, OETC — later instances
- OEE — history letter; see `archives.md`

## Stable ID rule

Every claim unit is `prefix:local-id` (bit code preferred;
sealed letter only as a display alias). Two units with the
same local name under different prefixes are different
vertices. Shared-ID matching across prefixes is forbidden.

`AuthorityEffect: None.`
