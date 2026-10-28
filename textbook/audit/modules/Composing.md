# Audit: Composing

| field | value |
|---|---|
| Path | lean4/Derivation/Composing.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 4cfd6fe526456e38 |
| Lines | 228 |
| Imported by root `Derivation.lean` | no. Imported by `lean4/ParkedAudit.lean` (line 5) and listed first in its `parkedModules`; `ParkedAudit` is a default target in `lean4/lakefile.toml` (`defaultTargets = ["Derivation", "ParkedAudit"]`), so the module is built by plain `lake build` and its seven theorems are reported in `artifacts/lean_axioms.txt` (lines 1483–1489, "does not depend on any axioms"). The caller's note that it is imported by neither root nor ParkedAudit is incorrect at this commit |
| Imports | none explicit (implicit `Init`; the header says so and withdraws an earlier "imports NOTHING") |
| Declarations | 1 structure (`Web`), 10 def (`Composable`, `noneCompose`, `HasIdentity`, `allCompose`, `allSelect`, `LeftReach`, `RightReach`, `RelAssoc`, `RelAssocLeft`, `skewCompose`), 7 theorem; namespace `Composing` |
| Axiom reports in `artifacts/lean_axioms.txt` | 7 lines, all "does not depend on any axioms" |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
Composing declares composition as a three-place relation over a family of arrows between nodes, with no operator, no identity and no associativity law, and exhibits each categorical guarantee failing against a stated predicate: a web where nothing composes (not total; no identity), a web where everything composes (not single-valued, yet a total selection function exists), and a skew web where a result reachable by left bracketing is unreachable by right bracketing (not associative, even one-way). Its header is a record of withdrawn overclaims: it does not say composites form no collection, does not say selection is impossible, does not refute inverses, and proves no bridge to any other module. It uses no arithmetic, lists or order; it does use dependent indexing of arrows by endpoints, and says that is load-bearing.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `Web` | 79 | structure | `Node : Type`, `Arr : Node → Node → Type`, `Composes : (a b c) → Arr a b → Arr b c → Arr a c → Prop` | ADMITTED (declared shape; header: "It does not claim `Web` is forced") |
| `Composable W a b c f g` | 86 | def | `∃ h, Composes a b c f g h` | ADMITTED |
| `noneCompose` | 92 | def | `Node = Unit`, `Arr = Bool`, `Composes = False` | ADMITTED (countermodel) |
| `HasIdentity W a` | 105 | def | an arrow neutral on both sides under `Composes` | ADMITTED |
| `allCompose` | 118 | def | `Composes = True` | ADMITTED (countermodel) |
| `allSelect` | 134 | def | constant `true` selection on `allCompose` | ADMITTED (witness) |
| `LeftReach`, `RightReach` | 151, 156 | def | results reachable by left / right bracketing | ADMITTED |
| `RelAssoc W` | 163 | def | `LeftReach ↔ RightReach` for all data | ADMITTED |
| `RelAssocLeft W` | 171 | def | the one-way law | ADMITTED |
| `skewCompose` | 181 | def | `Composes f g h := h = (f && !g)` | ADMITTED (countermodel) |

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `composition_may_fail` | 99 | `¬ Composable noneCompose () () () true true` | REFUTED (refutes "composition is total") | none | S |
| `noneCompose_no_identity` | 112 | `¬ HasIdentity noneCompose ()` | REFUTED (refutes "identities exist") | none | S |
| `composite_may_be_nonunique` | 126 | two distinct composites of one pair in `allCompose` | REFUTED (refutes "composition is single-valued") | none | S |
| `selection_is_possible` | 142 | `allSelect` always yields a valid composite | FROZEN (over `allCompose`; a positive witness refuting the withdrawn "no selection function") | none | S |
| `relAssocLeft_of_relAssoc` | 176 | `RelAssoc W → RelAssocLeft W` | FROZEN | none | A |
| `skew_not_relAssocLeft` | 188 | `¬ RelAssocLeft skewCompose` | REFUTED (witness `f = true, g = false, k = true, w = false`, `u = true`) | none | S |
| `skew_not_relAssoc` | 198 | `¬ RelAssoc skewCompose` | REFUTED | none | S |

## 4. External and admitted assumptions
- `Web` is a declared shape with `Type`-valued fields: `Node : Type` and `Arr : Node → Node → Type`. Universe: `Type` (0) appears as a field type — a Type universe inside a structure; metatheory. Finitude flag: the module places a `Type` of nodes and a family of `Type`s of arrows inside the declared object. Nothing in the paper reads this as an internally available universe; `primitive_difference_ascent.md` reads the theorems only as "the repository declines to supply" a total operation. Flagged, consistent with the prose.
- No library lemmas beyond `Bool.noConfusion`, `trivial`, `rfl`.
- Unearned identity: none found. Unrestricted external universe: the `Type` fields (flagged above; declared, not asserted as system content). Unbounded internal function: `allSelect` is a total function, presented as a metatheoretic witness. Silent observer: none. Presentation correspondence: none. Cost: none. Admitted-as-forced: none found (header: "not forced"). Finite-as-universal: the countermodels are on one-node, two-arrow webs and are presented as witnesses of failure, not as universal facts. none found.

## 5. Derived consequences
No Lean module imports Composing (grep: only ParkedAudit). `paper/primitive_difference_ascent.md` §4 (lines 142–151) cites four theorems as the reason "no graded structure appears for free".

## 6. Counterexamples and limitations
All substantive theorems are countermodels (section 3). The header's "What this does NOT claim" list is accurate against the Lean: no claim about collections or subtypes of composites, no inverse law defined or refuted, no magnitude, no bridge to `DiffObs`/`PresIso`/`HFamily`/`Break`.

## 7. Axiom dependencies
All seven: none. `allSelect` probed: none (probe2.lean). None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 7 theorems in the artifact (lines 1483–1489) via `ParkedAudit`. Cited by `paper/primitive_difference_ascent.md`; not by `paper.md` or the ledger (grep). Probe: probe2.lean (`allSelect`), exit 0.

## 9. Related Python implementations
none found (grep for `Composes`, `RelAssoc`, `Web` in `code/` and `tests/`: no hits — not re-run in this session beyond the earlier reference index; recorded as none found by that index).

## 10. Textbook placement proposal
- Prerequisites: none from the kernel; a reader needs only the idea of a relation versus an operation.
- Substantive: `Web`, the four negative results and `selection_is_possible`. Auxiliary: `relAssocLeft_of_relAssoc`.
- Lesson title: "Composition without an operator". Question: which of totality, uniqueness, identity and associativity does a bare composition relation give you for free? (None.)
- Omit: nothing; but the textbook should state, as the module does, that this proves nothing about the regime calculus.

## 11. Interpretation findings
- Header lines 52–54 and 64–70: "`lean4/Derivation.lean` does not import it, so it contributes no `#print axioms` report and appears in no axiom inventory … Because no `#print axioms` line names anything here, the whitelist in `ci/check_lean_audit.py` never sees this module: a dependency on `Classical.choice` in this file would fail no gate. The reports quoted above were taken by hand". At this commit `ParkedAudit` emits one report per theorem of this module into `artifacts/lean_axioms.txt` (lines 1483–1489), and `ci/check_lean_audit.py` reads that file (per ParkedAudit's header and `CLAUDE.md`). The docstring's residual is therefore closed for its theorems; the defs (`allSelect` etc.) remain outside the census. INTERPRETATION DEFECT (minor: stale provenance note in the safe direction — the module is now audited, not merely elaborated).
- `primitive_difference_ascent.md` §4: "`lean4/Derivation/Composing.lean` provides composition as a three-place relation and refutes each guarantee separately". Lean: each guarantee is refuted on a specific declared web, not "for composition in general". The prose's next sentence ("single-valuedness is a declaration, not a derivation") is the correct reading. none found beyond noting the witnesses are specific webs.
- Vacuity: `noneCompose` has arrows (`Bool`), so `composition_may_fail` is not vacuous; `RelAssoc` is satisfiable (e.g. `allCompose`, not proved here). none found.
- Finitude: `Type`-valued fields of `Web` — flagged in section 4; prose-consistent.
