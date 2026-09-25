# closed_family: closing a declared family, and what it costs a section

`AuthorityEffect: None.`

The pinned `Family` of `lean4/Derivation/PresentationNaturality.lean`
declares, in the span pinned in `SOURCE_MANIFEST.json`, that nothing is
assumed about closure under composition or inverses and that the family is
exactly what it lists. `PresIso` already carries `refl`, `symm`, and
`trans`. This rung builds the closure from those three operations and
measures what a section owes it.

## Frozen inputs

Native `PROMPT.md` sha256
`1f57b81d2f56cd340ed2e0d116bf994420f3a40f3e7db5f3a290587f550df0f4`.
Sources pinned at snapshot `f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be` of
`main`: four blobs, one span, and **eight source projections**, each binding
a contiguous slice of `lean/ClosedFamily/Base.lean` to an exact line range
of a pinned sealed source, checked at the snapshot and at `HEAD`.

## Declared readings

1. **No prediction freeze.** This rung ran on a direct author instruction in
   the operator channel, not on a frozen terminalizer charter, so there is
   no `PREDICTIONS.md` and `verify_pins.py` records zero freezes. Both
   branches of the substantive question were nonetheless written into
   `PROMPT.md` before the proof was attempted, and `PROMPT.md` states which
   one holds nowhere. A reader who wants a pre-registered record has the
   charter's terminal list and nothing stronger.
2. **The operation laws are proved on the transported bundle, not on the
   records.** `IsNatural` reads exactly one thing about an isomorphism: what
   its `mapPair` does. Associativity, both units, and both inverse laws are
   therefore stated and proved there. Equality of `PresIso` records would
   need function extensionality on two bijections and is not attempted; no
   sentence in this tree says the records are equal.
3. **The closure is a free construction, not an assumption.** `Path` is an
   inductive type of finite words in the declared arrows and their formal
   inverses, indexed by its endpoints so that no object equality is ever
   transported by hand. `pathIso` interprets a word by the pinned `refl`,
   `symm`, and `trans` and by nothing else.
4. **The result is named by what it is.** The structure the closure produces
   has an outside name; it is not used here, and `test_forbidden.py` carries
   that name, assembled from fragments, in its scan.

## Terminals, each with its scope

- **CLOSURE_BUILT** (PROVED_THEOREM): `closure D` is a `Family` in the
  pinned sense, with the same objects and observers and with every word as
  an arrow. `sec_closure_eq : Sec (closure D) = Sec D` holds by `rfl` —
  closing changes the arrows and not the objects, so the two families have
  literally the same sections. The added formal operations are exhibited by
  `closure_contains_inverse` and `closure_contains_composite`; this does not
  claim the arrow type grows strictly for every declared family.
- **The operation laws hold on the bundle** (PROVED_THEOREM):
  `mapPair_nil` (identity), `mapPair_comp` (composition), `mapPair_inv`
  (both inverse laws), `comp_assoc` (associativity of concatenation, on the
  words themselves), `nil_comp` (left unit, by `rfl`), `comp_nil` (right
  unit).
- **OBLIGATION_UNCHANGED** (PROVED_THEOREM) — the terminal this rung exists
  for. `natural_iff_natural_closure`: a section is natural for the closure
  **exactly when** it is natural for the declared family. Closing enlarges
  the arrows and imposes no new obligation on a section. Corollaries:
  `has_natural_section_iff` (the obstruction is unchanged too — a declared
  family carries a natural section iff its closure does) and
  `natural_closure_closure` (closing a closure imposes nothing further).
  `OBLIGATION_ENLARGED` does not fire.
- **The substantive half is the backward step.** `natural_symm`: naturality
  runs backwards along a declared arrow. The pinned `IsNatural` states one
  direction only; a closed family demands the other, and it follows from
  the pinned `mapPair_symm_left`. `natural_on_path` then carries it along an
  arbitrary word by induction.
- **Axiom-free.** 21 `#print axioms` reports, and every one reads *does not
  depend on any axioms* — no `propext`, no `Quot.sound`. The whole
  construction, the reconstructed statements included, is axiom-free.
- **OB1_UNCHANGED, S66_UNCHANGED, S9_LAST_UNCHANGED, NS95_GROWTH_UNCHANGED**:
  this rung touches none of the protected opens. It proves nothing about the
  challenge source, nothing about the two paper items, and nothing about the
  growth question of the arithmetic chain; `test_forbidden.py` fails the run
  on a claim to the contrary.
- **MANUAL_RECEIPT_DECLARED**: no CI gate reads this tree's pins or Lean
  audit. `verify_pins.py` and `verify_lean.py` are manual receipts, as in
  the sibling trees.
  2026-09-24: withdrawn for the Lean audit only.  The `lean` job of
  `.github/workflows/verify.yml` now runs `verify_lean.py`; `verify_pins.py`
  is still read by no gate.

## What this rung does and does not settle

It settles that the pinned family's deliberate non-closure is **free**: the
declared list and its closure impose the same obligations on a section, and
carry a natural section under exactly the same conditions. So the pinned
`Family` loses nothing by listing rather than closing, and a reader who
suspected the declaration was a gap can stop suspecting it.

It does **not** make the closure a structure of any named kind, does not
prove the record-level laws, and says nothing about families with additional
declared relations among their arrows — the free closure imposes none, and a
family whose arrows are meant to satisfy relations is a different object,
not treated here (OPEN, named in the leftovers).

## A live find, recorded

The working-denylist scan inherited from the sibling tree matched
**substrings**. This tree reconstructs the sealed `zeroRel_transport`
verbatim under pin, and that sealed native identifier *contains* a
working-denylist token as a substring, so the scan flagged a sealed name on
its first run here. The firewall bars identifiers, so the scan now matches
whole identifiers, with `_` and digits as identifier characters. The pin was
not touched and no name was renamed. The same substring defect is present in
the sibling trees' copies of the scan; it has not bitten them because none
of them reconstructs this sealed module, and repairing their copies is
outside this write root.

## The injection record

| Gate | Injection | Observed failure |
|---|---|---|
| Pin integrity | first digit of the pinned `PresentationNaturality.lean` blob flipped in `SOURCE_MANIFEST.json` | `FAIL: lean4/Derivation/PresentationNaturality.lean blob at f4b1dcd... is ef4d76c7..., pinned 0f4d76c7...`; exit 1, then 0 after reversal |
| Span pin | the declared-family span's first line moved to `217` | `FAIL: span lean4/Derivation/PresentationNaturality.lean:217-221 at f4b1dcd... hashes 9b07e025..., pinned 4b39a974...`; exit 1, then 0 after reversal |
| Source projection | a trailing comment added to one line inside a reconstructed block of `Base.lean` | `FAIL: research/closed_family/lean/ClosedFamily/Base.lean:52-81 is not the declared exact projection of pinned lean4/Derivation/PresentationNaturality.lean`; exit 1, then 0 after reversal |
| Lean forbidden token | a comment carrying the first forbidden token appended to `Closure.lean` | `FAIL: Closure.lean contains forbidden token sorry`; exit 1, then 0 after reversal |
| Census scan (FW-PIN, FW-NAME) | a probe file carrying a watched noun placed in the write root | `test_no_watched_prose_word_in_the_write_root` fails naming the file, its line, and the token; exit 1, then 0 after deletion |
| Axiom-report list — **the injection that did NOT fire, and what closed it** | one `#print axioms` line removed from `AxiomReport.lean` | **`lean audit clean: 5 sources, 20 axiom reports`, exit 0.** The audit diffed *reported* against *listed*, and removing a line removes the report as well as the listing, so neither direction could see the drop: the list was checking itself against the environment it generates. This is the parked-module blind spot in miniature. Closed by adding a SOURCE census to `verify_lean.py` — every `theorem` declared in the originating module must be listed. The same injection then gave `FAIL: ClosedFamily.Closure.comp_nil is declared in Closure.lean but not listed in AxiomReport.lean`, exit 1, and exit 0 after reversal |
| Denylist scan, real case | (found live, not injected) the sealed `zeroRel_transport`, reconstructed verbatim | the substring scan flagged it; repaired to whole-identifier matching, recorded above, nothing renamed |

## Leftovers, named and priced, executed nowhere

1. **Record-level laws** — OPEN: associativity, units and inverses as
   equalities of `PresIso` records rather than of their bundle actions.
   Price: function extensionality on `Bij`, plus a decision about whether
   the transport-proof fields are compared by proof irrelevance.
2. **Families with declared relations** — OPEN: the free closure imposes no
   relations among words. A family intended to satisfy relations is a
   different object and the quotient of the word type by them is not built
   here. Price: a declared relation set and a quotient with a proved
   congruence, which is exactly the sealed discipline for quotients.
3. **The heterogeneous case** — OPEN: the pinned `HFamily` lets the carrier
   and residual type vary with the object. This rung closes the flat
   `Family` only. Price: the same construction with `Hom a b` in place of a
   flat `Arr`, which the pinned module says needs no dependent transport.
4. **The next rung, named so it cannot be smuggled in later**: whether the
   fixed-point obstruction of the pinned module is *invariant* under
   closing — this rung shows the existence of a natural section is, but the
   obstruction's own witness data is not compared. Named, not started.

## The registration diff this tree does NOT apply

    - name: closed_family pins and Lean audit
      run: |
        python research/closed_family/verify_pins.py
        python -m unittest discover -s research/closed_family -p "test_*.py"

## Commands (run from this directory unless noted)

| command | exit | key line |
|---|---|---|
| `python verify_pins.py` | 0 | `pins clean: 4 sources and 1 spans at snapshot and HEAD; sealed prefixes unchanged; nothing outside the write root; 8 source projections exact; native PROMPT.md frozen; 0 predictions freezes reconstructed` |
| `python verify_lean.py` | 0 | `lean audit clean: 5 sources, 21 axiom reports (21 axiom-free), axioms within ['Quot.sound', 'propext'], 14 originating theorems all listed` |
| `python -m unittest discover -s . -p "test_*.py"` | 0 | refusal scans pass |
| `python ci/check_prose_watchlist.py` (repository root) | 0 | clean without a repin |

## Source pin semantics (2026-09-22)

By the author's ruling, `verify_pins.py` separates two claims that it used to
merge.

- **Provenance, which still fails.** The pinned blobs and spans at the
  snapshot, the exact source projections, the frozen native `PROMPT.md`, the
  recorded prediction freezes where this tree has them, and the rule that the
  worktree carries nothing outside the write root.
- **Currency, which is now reported.** That nothing pinned has moved between
  the snapshot and HEAD is printed as `DRIFT:` lines, followed by a
  `drift since the snapshot:` count. It no longer fails. Pass
  `--require-current` to restore the old failure.

Why the change: the snapshot blob is fixed history, so once the author edited
a sealed or contract file, no repin could satisfy both sides, and this check
had been red for weeks for that reason alone. What this tree claims is about
its snapshot, and that is what the check now enforces.

The `python verify_pins.py` row in the commands table above records a run made
under the earlier wording, and is kept as the dated record of that run.
