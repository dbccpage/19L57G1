# Thread: what grew inside the seal after 2026-08-17

`AuthorityEffect: None.` The seal is a blindness boundary, not a freeze
on `lean4/Derivation/`. After `052e657` the sealed object language still
grew. It did **not** grow a new genesis.

Seal receipt (`verification_20260817.md` at `052e657`): 8 gate families,
55 `Derivation/` modules, 1314 axiom reports. At HEAD: 12 gate families,
75 modules (63 root + 12 parked), 1530 axiom reports.

---

## Already inside the seal (not invented after)

These were ultra-closure / native-continuation work **before** the
stopping re-run. Post-seal touches are comments, inventory, or parked
audit wiring:

- `Completion` — Rule 1 as repair-or-extension; both orientations retained
- `Constitution` — `nextFamily`; `interp_describe`; interpreter remains meta
- `Apartness` — orientations share apartness, differ as data; retained
  orientation is not swap-invariant
- `Attachment` — lawful one-edge Up family
- `Bridge` / `PrimDiff` — priced two-ness, witness, irreflexivity,
  orientation
- `paper/native_derivation_map.md` — 19 PROVED / 2 DECLARED / 8 FALSE /
  1 OPEN (absolute self-interpretation)
- `paper/succession_declarations.md` — successive-state model derives
  none of carrier / unique next / individuating order
- `paper/native_derivation_completion.md` — relative replay closure only;
  `FULL_NATIVE_COMPOSITION` not claimed

Orientation as a *priced bridge* is sealed. The container question
(`<|>`, side-free, kind of order) is **research**, later.

---

## What actually landed in sealed paths after `052e657`

### 2026-08-17 — isolate + residuals R1–R3, R6

- `coda/` and `coda_meta/` removed from this repository.
- `Mention.lean`, `CountTransport.lean`. Collapse never reads `reqs`.
  `CL-COUNT-INVARIANCE` becomes a theorem.

### 2026-08-18 — residual register empty + ledger gate

- `MinimalityF` — `mu2_unique_F` grammar-wide in reading F.
- `RuleBridge` — `rule_item_never_minimal`.
- `TransitionTransport` — least-pair selection is **not** congruent.
- `Rounds` — choice-free closed-run bound `n(n-1)`.
- Gate 9: `ci/check_ledger_evidence.py`.
- Ledger wording walk (`74f8be95`): spine given the ledger's ceiling.

### 2026-08-19–20 — iso / form-renaming, mostly parked

`FormRenaming`, `FormTransport`, `IsoCollapse`, `IsoCanon`, `IsoBridge`,
`DiffAnchor`, plus `*Compat` modules. New theorems toward key soundness.
Full `CL-ISO-SOUND` stays OPEN. Parked modules are why
`ParkedAudit.lean` exists.

### 2026-08-21 — research begins; Breaking generalized

`selector_iff_common_fixed_point`. Not connected to the tied delta pair.
Gate 11 (research job) after the 2026-08-21 green-rollup incident.

### 2026-08-22 — parked axiom census

`lean4/ParkedAudit.lean` + `ci/check_parked_audit.py`. Theorems of the
twelve modules outside the root import closure. 1472 reports then.

### 2026-08-26 — G1 local-strategy class

`LocalStrategy.lean`, `G1Class.lean`, `SeparationCapacity.lean`. Finite
local ⇒ no fire+clear+no-import cycle. G4 engine correspondence
**withdrawn** (`38fca668`); G3/G4 remain conjecture.
`OBJECT_LANGUAGE_GENERATOR_NOT_IN_SCOPE`.

### 2026-08-31 — transposition + nine-slot inventory

`ObserverInventory`: declared classification of **existing** objects,
not a dynamics. Author refused an outside single-letter grid
(`CLAUDE.md`). PrimDiff transposition: both orientations share `S2`;
swap is auto of `S2` not of `D2`.

### 2026-09-01 onward — hygiene

Gate 12 (prose watchlist). Vocabulary purge of comments. Hosted CI
retired permanently (`4c9b5d8f`). Publication-review ledger IDs. Re-measure
at `60c2cb05`: 75 modules, 1530 reports.

Kernel `model.py` / `engine.py` / `iso.py` are **not** a new object
language after the seal.

---

## Direct answer

The native continuation (apartness, attachment, constitution, priced
orientation) was completed **then** sealed. Post-seal sealed work
discharges residuals, parks iso-transport, excludes a local-strategy
class, and inventories what was already there. New theory programs
live under `research/`. The map’s OPEN edge — kernel constitution
interpreting itself absolutely — is still OPEN.
