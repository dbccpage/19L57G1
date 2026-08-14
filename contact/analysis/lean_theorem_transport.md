# Theorem transport across the contact boundary

Run: primitive-difference contact collision, 2026-08-13. Pre-contact base
`a5caee2`; sealed blind-native-base `ccd3a53`; contact Lean spine committed at
`ebb1e0b`.

**Anchor, stated exactly.** Not everything cited here is at `ebb1e0b`. Seven
declarations were added after that commit, verified absent at `ebb1e0b` by
`git grep`: `ContactKernel.toDiffObs`, `ContactKernel.toDiffObs_fields`,
`ContactKernel.toDiffObs_apart`,
`ContactBridge.collapse_collision_is_pair_blocked`,
`ContactBridge.pair_blocked_iff_collapse_collision` (the collision run), plus
`ContactKernel.kernel_from_obs_iff_pair` and
`ContactKernel.eq_ofDiffObs_of_fields` (packet 2). Each of the six theorems
among them carries a matching `#print axioms` line in `lean4/Derivation.lean`.

*Anchor history.* This paragraph said "Five" after packet 2 had already added
two more, and its line citations were not regenerated when
`ContactKernel.lean` grew — every `ContactKernel` reference below the
insertion point had drifted, in the worst case by 255 lines. Both faults are
repaired here, and neither can recur silently: `ci/check_transport_citations.py`
recomputes every cited line from the Lean sources and fails on drift
(`--fix` regenerates them), and `tests/test_transport_citations.py` runs it.
As of this revision **173 citations are verified and none is unresolved**.

`artifacts/lean_axioms.txt` carries 1184 reports over 43 sources, all within
`{propext, Quot.sound}`. Throughout this document **"on disk" means the
current working tree**, and every line number below is machine-verified
against it rather than asserted. The collision tree also carries docstring
corrections (scope qualifiers on the minimality remarks, `sufficiency only` on
`kernel_two_point_presentation`, and the superseded-terminal stamp in
`PrimitiveContact`) that are text-only and change no statement.

Supplied external file sha256
`d9cdb350a53c513e3e211e72f17262be6ba85d7da6159f910388c7137e814a89` (READ-ONLY,
never copied into the repository); manifest sha256
`3b65253d8338b5f0283a29a194fe673d0200ca091284ab92ef315246e328065f`; prose stage
PROSE_INPUT_ABSENT.

Companion document: `lean_definition_map.md` (all 103 supplied declarations,
one row each). This document answers the different question — **for each
important notion pair, which direction of transport is proved, under exactly
which hypotheses, and where a direction fails, what refutes it.**

`contact/analysis/` is the only repository location permitted to quote the
supplied development's vocabulary. Quotations are labeled **SUPPLIED_INPUT**.

---

## 0. Ruling: comments are not evidence

**Only formal statements count.** Doc-comments, section headers, declaration
names, and slogans — on either side of the boundary — are never evidence for
any claim in this document. Where a supplied comment advertises content that
its declaration does not state, the disposition is recorded in the gap table
(§6) and the advertised content is **REFUSED** transport: it is not restated,
not weakened-and-restated, and not used as motivation for any native
declaration. Where a supplied *declaration name* carries an interpretive
slogan, the slogan is dropped and only the statement is transported (gap row
G20); the native reconstruction uses native names throughout, and the
vocabulary firewall keeps supplied identifiers out of `lean4/`, `code/`, and
`paper/` entirely.

The same ruling binds this repository's own prose: the native module
doc-comments quoted or paraphrased below are navigational only; every claim
here is anchored to a named declaration that exists on disk in the collision
tree of this run — commit `ebb1e0b` plus the seven later-committed
declarations named in the anchor note above, seven and no more.

---

## 1. The standing identification, and what it is not

`H_struct` — **the supplied core structure is field-for-field the native
`DiffInterface.DiffObs`** (`lean4/Derivation/DiffInterface.lean:33`, sealed at
base `a5caee2`): a valued difference map, a zero predicate on values, and
three equivalence law FIELDS. Differences: field spelling, binder implicitness
on two law fields, and universe polymorphism (supplied `Type u`/`Type v`,
native monomorphic `Type`).

- Evidence FINITE_COMPUTATION: a scratch bridge file kept **outside** the
  repository compiles both structures, converts in both directions, and proves
  both round trips plus the zero-relation match; all three reports read "does
  not depend on any axioms". Hashes in `contact_countermodels.json`
  (`correspondence_map.scratch_bridge_check`).
- **Reproducibility limit, stated where the premise is used.** The vocabulary
  firewall forbids committing that scratch file, so `H_struct` is **not
  re-runnable from this repository**: no CI job, test, or reviewer can
  reproduce it, and only the two sha256 values stand as the record. Every
  claim resting on `H_struct` — in particular the
  CONTACT_EQUIVALENT terminal — inherits that limitation, and the artifact and
  receipt scopes say so.
- `H_struct` is therefore **definitional at `Type 0`, not a mathematical
  admission**. It is renaming plus a universe restriction.
- What it is **not**: it is not a claim that the two *developments* are
  equivalent, and it is not a claim that the native side had the supplied
  file's quotient-descent layer before this run. It did not; see §2.3–§2.6.

**Recorded provenance asymmetry (METATHEORY).** The three equivalence laws are
*admitted fields* on the supplied side — nothing in the supplied file derives
them (FINITE_COMPUTATION by inspection of all 103 declarations). On the native
side the same three laws are *proved* at the kernel observer
`DiffInterface.kernelObs` (`DiffInterface.lean:54`, `rfl`/`.symm`/`.trans`) and
at the passage's declared observation stage
(`ContactBridge.declared_zero_as_view`, `ContactBridge.lean:628`). Identical
statements; different provenance. This is the content of hypothesis H1 and is
sharpened in §2.16.

---

## 2. Notion pairs

Legend for the transport tables:

- **PROVED** — a named Lean declaration on disk (anchor note above: `ebb1e0b`
  plus the seven later-committed declarations) establishes the direction; its
  exact hypotheses are listed.
- **PROVED-UNDER-H** — established only under the listed extra hypothesis
  (always an explicit `Decidable` instance argument; never a classical
  principle used as a proof step).
- **REFUTED** — a countermodel theorem on disk refutes the direction; carrier
  size and minimality status are given.
- **PRICED-OPEN** — no countermodel can exist (the schema is classically
  true), so the cell is recorded OPEN with an exact reverse-mathematics price.

### 2.1 Difference datum ↔ native observer

| direction | status | Lean evidence | exact hypotheses |
|---|---|---|---|
| supplied structure → `DiffInterface.DiffObs` | PROVED (FINITE_COMPUTATION) | scratch bridge conversion, both round trips, axiom-free reports | carrier and value type in `Type 0` |
| `DiffObs` → supplied structure | PROVED (FINITE_COMPUTATION) | same | same |

No failed direction. The universe restriction is the whole gap and it is a
presentation fact, not a mathematical one.

### 2.2 Induced relation, setoid, quotient, exactness

| direction | status | Lean evidence | exact hypotheses |
|---|---|---|---|
| induced relation ↔ `DiffInterface.ZeroRel` | PROVED | `DiffInterface.ZeroRel` (`:42`) — sealed at base, same definition | `H_struct` |
| equivalence of the induced relation | PROVED | `DiffInterface.zeroRel_equivalence` (`:45`) — sealed at base | `H_struct` |
| setoid, quotient, projection | PROVED | `DiffInterface.obsSetoid` (`:69`), `DiffInterface.ObsQuotient` (`:72`), `DiffInterface.ObsQuotient.mk` (`:74`) — sealed at base | `H_struct` |
| soundness (related ⇒ classes equal) | PROVED | `DiffInterface.obsQuotient_eq_of_zero` (`:78`) — sealed at base | `H_struct` |
| **effectiveness** (classes equal ⇒ related) | PROVED **this run** | `ObsDescent.obsQuotient_exact` (`ObsDescent.lean:83`), packaged as `ObsDescent.obsQuotient_mk_eq_iff` (`:88`) | `H_struct`; axioms `[propext, Quot.sound]`, matching the supplied report |
| projection is epi | PROVED **this run** | `ObsDescent.obsQuotient_mk_surjective` (`:96`) | `H_struct` |

The native base had soundness only. Effectiveness and epi-ness are new native
content this run; they are exactly what makes the descent uniqueness of §2.14
global.

### 2.3 Unary descent (observable factors through the quotient)

| direction | status | Lean evidence | exact hypotheses |
|---|---|---|---|
| compatibility ⇒ factorization | PROVED | `ObsDescent.descend_exists_iff` (`:119`) `.mpr`; witness `ObsDescent.descend` (`:108`) | `hf : ClassConstant O f`, i.e. `∀ x y, ZeroRel O x y → f x = f y` |
| factorization ⇒ compatibility | PROVED | `ObsDescent.descend_exists_iff` (`:119`) `.mp` | a map `F : ObsQuotient O → Y` with `∀ x, F (ObsQuotient.mk O x) = f x` |
| computation rule | PROVED | `ObsDescent.descend_mk` (`:113`), by `rfl` | as above |
| uniqueness | PROVED | `ObsDescent.descend_unique` (`:134`) | two maps `F G` each satisfying `∀ x, · (ObsQuotient.mk O x) = f x` |
| one witness blocks descent | PROVED | `ObsDescent.descend_blocked_of_witness` (`:142`) | `hxy : ZeroRel O x y`, `hne : f x ≠ f y` |

**Failed direction:** none at this notion pair — the `↔` closes it. The
*unconditional* failure case is a countermodel, not a gap:

| refuted statement | countermodel | carrier | minimality |
|---|---|---|---|
| "every view descends" | `ObsDescent.collapseAllObs_no_view_descend` (`:476`), via `collapseAllObs_id_not_classConstant` (`:469`) | 2 (`Bool`) | **Minimal.** On a subsingleton carrier every view is class-constant (`Subsingleton.elim`), so no descent obstruction can live at carrier ≤ 1. METATHEORY remark; no Lean declaration claims more. |

### 2.4 Binary descent (the difference map factors through the quotient)

| direction | status | Lean evidence | exact hypotheses |
|---|---|---|---|
| compatibility ⇒ factorization | PROVED | `ObsDescent.deltaDescend_exists_iff` (`:169`) `.mpr`; witness `ObsDescent.deltaDescend` (`:156`) | `h : DeltaConstant O`, i.e. `∀ x x' y y', ZeroRel O x x' → ZeroRel O y y' → O.delta x y = O.delta x' y'` |
| factorization ⇒ compatibility | PROVED | `ObsDescent.deltaDescend_exists_iff` (`:169`) `.mp` | a map `F` with `∀ x y, F (mk x) (mk y) = O.delta x y` |
| computation rule | PROVED | `ObsDescent.deltaDescend_mk` (`:161`), by `rfl` | as above |
| uniqueness | PROVED | `ObsDescent.deltaDescend_unique` (`:188`) | two maps `F G` each computing `O.delta` on classes |
| four-point witness blocks descent | PROVED | `ObsDescent.deltaDescend_blocked_of_witness` (`:200`) | `hx : ZeroRel O x x'`, `hy : ZeroRel O y y'`, `hne : O.delta x y ≠ O.delta x' y'` |

| refuted statement | countermodel | carrier | minimality |
|---|---|---|---|
| "the difference map always descends" | `ObsDescent.collapseAllObs_no_delta_descend` (`:458`), via `collapseAllObs_not_deltaConstant` (`:452`) | 2 (`Bool`) | Minimal, same METATHEORY argument as §2.3. |

The all-zero observer (`ObsDescent.collapseAllObs`, `:437`) is the exact
counterpart of the supplied `Bool` instance; both sides prove the same four
facts, and both are axiom-free where the statement is a discrimination
(supplied reports for the two discrimination theorems read "does not depend on
any axioms"; the native proofs use `Bool.noConfusion`).

### 2.5 Mod-setoid descent ↔ the equality layer

The whole "mod" stratum of the supplied file (its value-side and target-side
setoid variants, roughly 28 declarations across sections C, D, I and J of
`lean_definition_map.md`) transports through **one** reduction:

> `ObsDescent.classConstant_comp_mk_iff` (`ObsDescent.lean:276`)
> `ClassConstant O (fun x => Quotient.mk S (f x)) ↔ ∀ x y, ZeroRel O x y → S.r (f x) (f y)`
> Hypotheses: none beyond `O : DiffObs X R`, `f : X → Y`, `S : Setoid Y`.
> Proof: `Quotient.exact` one way, `Quotient.sound` the other.

| direction | status | Lean evidence | exact hypotheses |
|---|---|---|---|
| mod-compatibility ⇔ equality-layer compatibility at `Quotient.mk S ∘ f` | PROVED (both) | `ObsDescent.classConstant_comp_mk_iff` (`:276`) | none extra |
| mod-descent existence ⇔ mod-compatibility (unary) | PROVED (both) | `ObsDescent.descendMod_exists_iff` (`:284`) | none extra |
| mod-descent existence ⇔ mod-compatibility (binary) | PROVED (both) | `ObsDescent.deltaDescendMod_exists_iff` (`:293`) | none extra |
| transport along a coarsening | PROVED | `ObsDescent.descendMod_exists_of_coarsen` (`:334`), built on `coarsenMap` (`:261`) and `coarsenMap_mk` (`:267`) | `h : ∀ a b, S.r a b → T.r a b`, plus an existing mod-`S` factorization |
| product setoid, componentwise effectiveness | PROVED | `ObsDescent.pairSetoid` (`:318`), `ObsDescent.pairSetoid_mk_eq_iff` (`:327`) | none extra |

**Failed direction:** none. The reduction is an `↔` with no side condition, so
no countermodel is possible and none is claimed. What is *not* claimed: that
each of the ~28 supplied mod-declarations has its own native declaration. It
does not; the per-declaration accounting is in `lean_definition_map.md`, where
every such row names the native theorem plus the one step (contraposition,
`Iff.mp`/`Iff.mpr`, `Iff.trans`) that yields the supplied statement.

### 2.6 Pairing and the flagship obstruction

| direction | status | Lean evidence | exact hypotheses |
|---|---|---|---|
| pair compatibility ⇔ componentwise compatibility | PROVED (both) | `ObsDescent.classConstant_pair_iff` (`:212`) | none extra; axiom-free on both sides |
| joint descent ⇔ component descents | PROVED (both) | `ObsDescent.pair_descend_exists_iff` (`:225`) | none extra |
| **flagship**: one view descends, the pair is blocked | PROVED | `ObsDescent.view_descends_pair_blocked` (`:248`) | `hf : ClassConstant O f`; `hxy : ZeroRel O x y`; `hg : g x ≠ g y` |

The native statement is in **witness form**, which is the constructively
primary one and is also the form the supplied file's own witness variants use.
The supplied negation-hypothesis variant (`¬ ClassConstant O g` instead of a
witness) follows in one step from `pair_descend_exists_iff` +
`descend_exists_iff`; there is no separately named native declaration for it,
and that is recorded rather than papered over.

**Failed direction:** none. The obstruction is an implication, not an
equivalence claim, and both of its conjuncts are proved from the stated
hypotheses.

### 2.7 Tag/fingerprint construction

| direction | status | Lean evidence | exact hypotheses |
|---|---|---|---|
| tagged difference datum → native kernel observer of the tag-forgetting view | PROVED | `ObsDescent.tag_view_zeroRel` (`:350`): `ZeroRel (kernelObs fun p : K × X => φ p.2) s t ↔ φ s.2 = φ t.2`, by `Iff.rfl` | none |
| native kernel observer → tagged difference datum | PROVED | same `Iff.rfl` read in the other direction | none |

**Relation status is `same-third-notion`, not an implication.** The third
notion is "equal fingerprints under the reference view". The supplied
presentation makes the difference *value* a `Prop` (the only place in the
supplied file where the value type is `Prop`); the native presentation makes it
the ordered pair of views. The induced relations agree *definitionally*, and
neither value presentation is a specialization of the other. Value grade is
presentation here; §2.13 prices that fact separately.

### 2.8 Observer complement ↔ native apartness (the meet)

The supplied primitive yields a difference relation only as the **complement of
its zero relation** — refutation grade, no endpoint data, no positive witness.
That is `ContactBridge.obsApart` (`ContactBridge.lean:116`).

**Free, unconditional (each is a law field contraposed):**

| statement | Lean | hypotheses |
|---|---|---|
| irreflexivity | `ContactBridge.obsApart_irrefl` (`:119`) | none |
| symmetry | `ContactBridge.obsApart_symm` (`:124`) | none |
| double-negation stability | `ContactBridge.obsApart_stable` (`:130`) | none |
| zero-pairs are indistinguishable | `ContactBridge.zeroRel_indist` (`:135`) | none |

**The meet, in both directions:**

| direction | status | Lean evidence | exact hypotheses |
|---|---|---|---|
| positive apartness → observer | PROVED | `ContactBridge.apartObs` (`:224`), relation match `apartObs_zeroRel` (`:236`, `Iff.rfl`) | `h : Apartness.IsApart r` — the three admissions spent one-for-one (irreflexivity→reflexivity, symmetry→symmetry, cotransitivity→transitivity) |
| …with the relation recovered | PROVED-UNDER-H | `ContactBridge.apartObs_roundtrip` (`:244`); packaged `ContactBridge.isApart_repr` (`:256`) | additionally `[∀ x y, Decidable (r x y)]` |
| observer → positive apartness | PROVED-UNDER-H | `ContactBridge.obsApart_isApart` (`:265`) | `[∀ x y, Decidable (ZeroRel O x y)]` (irreflexivity and symmetry need none; **cotransitivity spends it**) |
| …with the zero relation recovered | PROVED-UNDER-H | `ContactBridge.indist_obsApart_iff` (`:274`) | `[∀ x y, Decidable (ZeroRel O x y)]` |

**Failed directions, and why they are priced rather than countermodelled.**
Dropping the decidability hypothesis does **not** admit an internal
countermodel: each unconditional schema is classically true, so no model inside
the metatheory can refute it. The honest treatment is an exact price:

| dropped hypothesis | exact price | Lean | status |
|---|---|---|---|
| decidability for cotransitivity | **exactly** the weak law of excluded middle | `ContactBridge.cotrans_schema_iff_wlem` (`:519`) — an `↔` against `∀ P : Prop, ¬ P ∨ ¬ ¬ P`; forward direction uses the three-point pricing observer `ContactBridge.wlemZero` (`:454`) on `ContactBridge.Tri` (`:443`) | PRICED-OPEN; record `ContactBridge.open_bridge_cotrans` (`:607`) |
| decidability for stability | **exactly** double-negation elimination | `ContactBridge.stability_schema_iff_dne` (`:550`) — an `↔` against `∀ P : Prop, ¬ ¬ P → P`; forward direction uses a two-point observer with `delta x y := x = y ∨ P` | PRICED-OPEN |
| decidability for locatedness | **implies** the weak law of excluded middle; converse not claimed | `ContactBridge.located_schema_implies_wlem` (`:578`) | PRICED-OPEN; record `ContactBridge.open_bridge_located` (`:612`), which states in full that the converse would need a function-comprehension principle beyond the weak law |

**Gate note (DECLARED_POLICY, verified):** in all three theorems the classical
principle occurs only as a *quantified statement inside the proposition*. No
proof step anywhere in `lean4/` uses a classical principle; every case split is
on an explicitly hypothesized `Decidable` instance or on a `Bool`/constructor.

**Necessity of each apartness admission** (i.e. why the supplied side's three
law fields are not free) is priced by sealed native countermodels, cited not
re-proved:

| dropped admission | countermodel | carrier | minimality |
|---|---|---|---|
| reflexivity of the zero side | `Apartness.bare_breaks_refl` (`Apartness.lean:101`) | 1 | Minimal — one point is the least on which self-difference can be asserted. |
| symmetry | `Apartness.irrefl_alone_breaks_symm` (`:107`) | 2 | Minimal — on a subsingleton every relation is symmetric (METATHEORY). |
| transitivity/cotransitivity | `Apartness.symm_without_cotrans_breaks_trans` (`:143`) | 3 | Minimal — proved on the contact side by `ContactBridge.bool_bs_repr` (`:398`): at carrier 2, witness + irreflexivity + symmetry already force representability with **no** decidability hypothesis. |

### 2.9 Native asserted relation → observer complement (representability)

This is the direction that carries the primary verdict. The question: which
relations are complements of some observer's zero relation?

**The characterization (both directions, fully constructive):**

> `ContactBridge.obsApart_repr_iff` (`ContactBridge.lean:319`)
> `(∃ O : DiffObs X Prop, ∀ x y, obsApart O x y ↔ r x y) ↔ (Equivalence (fun x y => ¬ r x y) ∧ ∀ x y, ¬ ¬ r x y → r x y)`
> Hypotheses: none beyond `r : X → X → Prop`.

Reading: **the supplied primitive's entire expressive range over relations is
the double-negation-stable complements of equivalences** — read off the
statement, this characterizes representability by a **Prop-valued** observer:
both sides of the biconditional quantify `∃ O : DiffObs X Prop`. At other
value types only the forward direction is available (from
`ContactBridge.obsApart_stable` plus the sealed
`DiffInterface.zeroRel_equivalence`); no biconditional is proved there, and
none is claimed.

**Subsumption, stated exactly.** The crown is Prop-only, so only the Prop-only
failure below is an *instance* of it: `unit_total_not_repr` refutes
`∃ O : DiffObs Unit Prop`. The other three —
`d2_not_obs_complement`, `triSym_not_obs_complement` and
`d_not_witnessed_repr` — each quantify `∃ (R : Type) (O : DiffObs _ R)` and
are therefore **strictly stronger than any crown instance, not instances of
it**: they refute representability (respectively witness transport) at *every*
value type, where the crown speaks only at `Prop`. Read as a count: one of the
four rows is Prop-only and three are value-type-general. All statements in this
section quantify over `Type` (universe 0).

**Failed directions, with countermodels:**

| what fails | countermodel (Lean) | carrier | minimality |
|---|---|---|---|
| the total relation on one point (native readings W, C; models `unitBare`, `unitFull` cited) — **Prop-valued observers only**: the statement refutes `∃ O : DiffObs Unit Prop`, and no value-type-general form is proved | `ContactBridge.unit_total_not_repr` (`:350`) | **1** | Minimal — carrier 1 is the least carrier on which any relation exists; the refutation is `obsApart_irrefl` applied at `((), ())`. METATHEORY. |
| the **oriented** two-point witness, over **every** value type `R` | `ContactBridge.d2_not_obs_complement` (`:362`) | **2** | Minimal: on a subsingleton carrier every relation is symmetric, so the phenomenon (free symmetry of the complement kills orientation) cannot appear below carrier 2. METATHEORY; no Lean declaration claims more. **This theorem quantifies over all value types `R`** — it is a signature-level, not a value-choice, refutation. Re-exported at the sealed interface as `PrimitiveContact.native_interface_not_representable` (`PrimitiveContact.lean:137`). |
| the symmetric three-point relation (native reading Bs) | `ContactBridge.triSym_not_obs_complement` (`:377`) | **3** | **Minimal, and the minimality is proved**: `ContactBridge.bool_bs_repr` (`:398`) shows that on carrier 2 a witnessed irreflexive symmetric relation is *always* representable, with no decidability hypothesis (finite case analysis routes every double negation through the witness or ex falso). |
| an endpoint witness over the empty relation (native readings D, E; models `boolEmpty_d`, `boolEmpty_e` cited) | `ContactBridge.d_not_witnessed_repr` (`:426`) | **2** | **Minimality unclaimed at the carrier**: the content is the *witness gap*, not the carrier size — the empty relation is perfectly representable (it is the all-zero shape), but no observer over it carries the endpoint witness. Carrier 2 is simply the least carrier with a distinct pair to witness. This replays the sealed `PrimDiff.meta_diff_without_assertion` (`PrimDiff.lean:63`). |

**FINITE_COMPUTATION corroboration** (generator `code/run_primitive_contact.py`,
artifact `artifacts/primitive_contact.json`, block `enumerations.E2`): over
carriers 1, 2, 3 there are 2, 16, 512 relations, of which **1, 2, 5** are
representable — exactly the Bell numbers `1, 2, 5`, i.e. exactly the partitions
of the carrier. That is the crown's content counted by machine: representable
= complement of an equivalence (decidably, on a finite carrier). Witnessed
representable counts: 0, 1, 3.

**Carrier size of the exhibited countermodel per native candidate reading**
(native → supplied direction), recorded in `contact_countermodels.json`:

| reading | W | A | Bs | Bc | Bl | C | D | E | F |
|---|---|---|---|---|---|---|---|---|---|
| carrier of the exhibited countermodel | 1 | 2 | 3 | 2 | 2 | 1 | 2 | 2 | 2 |
| carrier minimality | METATHEORY | METATHEORY | **PROVED** (`bool_bs_repr`) | inherited | inherited | METATHEORY | **unclaimed** | **unclaimed** | inherited |

**Read the second row before quoting the first.** Exactly ONE of the nine has a
Lean-proved carrier minimality: Bs at 3, by the positive `bool_bs_repr` at
carrier 2. The entries marked METATHEORY are minimal only in the weak sense
that the reading cannot be posed below that carrier (a reading demanding a
distinguished pair needs two points; every relation on a subsingleton is
symmetric) — an argument in the metatheory, not a Lean declaration. The two
marked **unclaimed** are the rows whose own §4 entries say so:
`d_not_witnessed_repr` and `no_kernel_over_allzero` refute a *witness gap*, not
a carrier bound. Any summary that calls all nine "minimum finite
countermodels" overstates this table.

Bc, Bl and F fail *through their A-conjunct*: the sealed models `d2Bare_bc`
(`PrimitiveCore.lean:351`), `d2Bare_bl` (`:357`) and `d2Protected_f` (`:336`)
all carry the oriented two-point relation, which `d2_not_obs_complement`
refutes. Those three rows therefore inherit carrier 2 and inherit its
minimality argument; **no separate countermodel is claimed for them** — they
are not three further refutations, they are three consequences of the A row.

### 2.10 Observer complement → the native candidate readings

Here the supplied side *does* transport, and the price is explicit. The
observer's faithful image in the native candidate matrix is
`ContactBridge.obsSetting` (`:143`): carrier, complement relation, a chosen
pair, and **empty** retention/protection/operation stores — an observer carries
no such content, so its image declares none (DECLARED_POLICY, and the emptiness
is `rfl`).

| reading | status | Lean | exact hypotheses |
|---|---|---|---|
| W | PROVED | `ContactBridge.obsSetting_w` (`:156`) | `hab : obsApart O a b` |
| A | PROVED | `ContactBridge.obsSetting_a` (`:161`) | `hab` (irreflexivity free) |
| Bs | PROVED | `ContactBridge.obsSetting_bs` (`:166`) | `hab` (symmetry free) |
| Bc | PROVED-UNDER-H | `ContactBridge.obsSetting_bc` (`:184`), via `ContactBridge.obsApart_cotrans` (`:175`) | `hab` **and** `[∀ x y, Decidable (ZeroRel O x y)]` |
| Bl | PROVED-UNDER-H | `ContactBridge.obsSetting_bl` (`:193`), via sealed `PrimitiveCore.located_of_decidable` | `hab` **and** `[∀ x y, Decidable (ZeroRel O x y)]` |
| D | PROVED | `ContactBridge.obsSetting_d` (`:203`), via sealed `PrimitiveCore.imp_a_d` | `hab` |
| E | PROVED, **scope-limited** | `ContactBridge.obsSetting_e` (`:211`), via sealed `PrimitiveCore.e_empty_iff_d` at the `rfl`-empty operation family | `hab`; **scope: the empty admitted family only** |
| C | **REFUTED** | `ContactBridge.obsSetting_not_c` (`:290`) | none — holds for every `O`, `a`, `b` |
| F | **REFUTED** | `ContactBridge.obsSetting_not_f` (`:297`) | none |

**The two negative cells are not gaps but content.** Protection is *freely
declarable over* an observer and *never derivable from* it — both halves in one
statement: `ContactBridge.kernel_prot_independent` (`:304`), which exhibits C
holding after one `prot` declaration and failing without it. This is the
observer-stratum echo of the sealed `PrimitiveCore.prot_not_from_witness`
(`:804`) and `ret_not_from_witness` (`:809`).

**Scope of the E row, stated exactly.** `obsSetting_e` claims E only at the
empty operation family. With one admitted merger E dies; the sealed
`PrimDiff.merger_erases` (`PrimDiff.lean:455`) is the mechanism, and the kernel
stratum instantiates it as `ContactKernel.kernel_not_e_merged`
(`ContactKernel.lean:402`) with carrier 2. Nothing here claims E beyond the
empty-store translation.

### 2.11 Observer ↔ common replacement kernel

The kernel is `ContactKernel.WitnessedDiff` (`ContactKernel.lean:103`): a valued
difference map, a zero predicate, designated endpoints `a b`, a diagonal-zero
law, and a refutation-grade non-zero witness `apart_ab : ¬ Zero (delta a b)`.
**Deliberately absent:** symmetry, transitivity, retention, protection,
operations.

| direction | status | Lean | exact hypotheses |
|---|---|---|---|
| observer + chosen pair → kernel | PROVED | `ContactKernel.ofDiffObs` (`:217`) | `a b : X` **and** `hw : ¬ ZeroRel O a b` |
| same-data kernel exists ↔ a non-zero pair exists | PROVED | `ContactKernel.kernel_from_obs_iff_pair` | none — existence only; not uniqueness of the pair |
| such a kernel is `ofDiffObs` at its own endpoints | PROVED | `ContactKernel.eq_ofDiffObs_of_fields` | `K.delta = O.delta` and `K.Zero = O.Zero`; factorization, not unique pair |
| an arbitrary pair may fail the side condition | PROVED | `ContactKernel.pair_choice_load_bearing` (`:237`) — one `Bool` observer offers both a non-zero pair and a zero pair. This is a statement about PAIRS; it exhibits no two valid choices and no two kernels | carrier 2; carrier remark METATHEORY (a subsingleton carrier has one pair, and by `no_kernel_on_subsingleton` supports no kernel at all) |
| admissible pairs ↔ same-data kernels (fixed observer) | PROVED, bijection | `ContactKernel.toPair` / `ofPair` with both round trips `toPair_ofPair`, `ofPair_toPair` and `ofPair_injective` — the pair choice IS the kernel choice | none |
| observer alone → kernel | NON-UNIQUE, PROVED | `ContactKernel.kernel_not_unique_of_pair` — any observer with an admissible pair has at least two distinct same-data kernels, via `transpose_kernel_ne`; concretely `pair_choice_not_unique` over `boolEqObs` | no carrier or value-type bound within the hypothesis; PRESENTATION GRADE (same `delta`, same `Zero`, same induced `kernelApart`; differing designated endpoints), resting on the ADMITTED `zero_symm` field |
| no relabelling-equivariant pair selector | PROVED, scoped | `ContactKernel.no_swap_equivariant_pair_selector` via `swapObs_boolEqObs` | total selectors on `DiffObs Bool Bool` under the negation action ONLY; transports `Bridge.no_swap_fixed_offdiag_pair` to the observer stratum and claims no priority over it |
| supplied-shape structure alone → any witness | **REFUTED** | `ContactKernel.kernel_no_witness_from_collapse` (`:503`) — over the all-zero observer *no* pair is complement-witnessed | carrier 2; minimality as above |
| kernel → observer (promote to the law fields) | **REFUTED** (symmetry) | `ContactKernel.kernel_not_observer` (`:554`) — the oriented two-element kernel's difference and zero data extend to no `DiffObs`, because the symmetry law field would force symmetry of the zero relation | **2**; minimal — on a subsingleton every relation is symmetric (METATHEORY) |
| kernel → observer (promote to the law fields) | **REFUTED** (transitivity) | `ContactKernel.kernel_zero_not_trans` (`:574`) — the three-point complement kernel's zero chain breaks | **3**; minimal, inherited from the sealed `Apartness.symm_without_cotrans_breaks_trans` data and, on the contact side, from `ContactBridge.bool_bs_repr` (positive at carrier 2) |
| candidate-A setting → kernel | PROVED | `ContactKernel.ofSetting` (`:176`) | `h : PrimitiveCore.A S` (witness + irreflexivity) |
| …with the relation recovered exactly | PROVED-UNDER-H | `ContactKernel.ofSetting_exact` (`:189`) | additionally `[∀ x y, Decidable (S.r x y)]` |
| …without decidability | PRICED-OPEN | `ContactKernel.open_kernel_grade` (`:201`) | the round trip is double-negation-coarse; the residual schema is priced at DNE via `ContactBridge.stability_schema_iff_dne`; no internal countermodel can exist because the gap schema is classically true |
| kernel meets the sealed pre-contact interface | PROVED | `ContactKernel.toNativeKernel` (`:168`) : `WitnessedDiff X R → PrimitiveContact.NativeKernel`, via `toSetting_A` (`:161`) | none — by construction |
| kernel is blind to retention/protection/operations | PROVED | `ContactKernel.ofSetting_ret_irrelevant` (`:207`), by `rfl` | none |
| kernel **+ the two law declarations** → observer | PROVED (record identity) | `ContactKernel.toDiffObs` (`:514`), with `toDiffObs_fields` (`:528`) — fields carried unchanged and `ofDiffObs (toDiffObs K hs ht) K.a K.b K.apart_ab = K`, all three by `rfl` — and `toDiffObs_apart` (`:539`): `obsApart (toDiffObs K hs ht) x y ↔ kernelApart K x y` | `hs`, `ht`: the symmetry and transitivity of the zero side, exactly the two declarations the kernel omits; nothing else |

**The two supplied law fields are exactly the admissions separating observer
from kernel, priced at carriers 2 and 3** — matching the sealed apartness
pricing. That is the precise sense in which the kernel is a *meet*. The last
row is the observer-side half of "replaces both": it is a **record identity**
(DEFINITION grade, `rfl`-proved), not a derivation — the kernel record plus the
two law fields *is* the `DiffObs` record. It is stated as a theorem here
precisely so that the terminal's clause "entry-level content of both sides
re-derives from kernel + separately declared additions" cites a declaration on
both halves rather than prose on one.

### 2.12 Kernel ↔ the native candidate readings

| reading | K → reading | reading → K |
|---|---|---|
| W | PROVED — `ContactKernel.kernel_to_w` (`:639`) | REFUTED — `ContactKernel.no_kernel_on_subsingleton` (`:130`), carrier 1 (native model `unitBare` cited); minimal by construction (carrier 1 is least) |
| A | PROVED — `ContactKernel.toSetting_A` (`:161`) | PROVED-UNDER-H — `ContactKernel.ofSetting` (`:176`) + `ofSetting_exact` (`:189`) under `[∀ x y, Decidable (S.r x y)]`; otherwise `open_kernel_grade` |
| Bs | REFUTED — `ContactKernel.kernel_not_bs` (`:585`), carrier **2**, minimal (subsingleton ⇒ symmetric) | PROVED — `ofSetting`, Bs being within A |
| Bc | REFUTED — `ContactKernel.kernel_not_bc` (`:599`), carrier **3**, minimality inherited from sealed `PrimitiveCore.cotrans_auto_on_two` (`:121`) | PROVED — `ofSetting`, Bc within A |
| Bl | PROVED-UNDER-H — `ContactKernel.kernel_located_of_decidable` (`:614`) under `[∀ v, Decidable (K.Zero v)]`; unconditional cell PRICED-OPEN as `ContactKernel.open_kernel_bl` (`:623`) | PROVED — `ofSetting`, Bl within A |
| C | REFUTED — `ContactKernel.kernel_not_c` (`:628`), for every kernel; freely declarable, never derivable (`ContactBridge.kernel_prot_independent`) | REFUTED — `no_kernel_on_subsingleton`, carrier 1 (native model `unitFull` cited) |
| D | PROVED — `ContactKernel.kernel_to_d` (`:644`), via sealed `imp_a_d` | REFUTED — `ContactKernel.no_kernel_over_allzero` (`:671`), carrier 2; **minimality unclaimed at the carrier** — the content is the witness gap, not the carrier size (`boolEmpty_d` cited) |
| E | PROVED at empty operations — `ContactKernel.kernel_to_e_empty` (`:650`); REFUTED under one declared merger — `ContactKernel.kernel_not_e_merged` (`:657`), carrier 2 | REFUTED — `no_kernel_over_allzero`, carrier 2, minimality unclaimed as for D (`boolEmpty_e` cited) |
| F | REFUTED — `ContactKernel.kernel_not_f` (`:634`), for every kernel | PROVED — `ofSetting` via sealed `imp_f_a`, together with `ofSetting_ret_irrelevant` |

The machine-readable version of this matrix, spanning both strata, is
`ContactKernel.contactCells` (`ContactKernel.lean:956`), 37 literal rows, with
`ContactKernel.contactCells_length : contactCells.length = 37 := rfl` (`:764`).
What is machine-checked there is the **count** and the byte-level agreement of
the Lean literal with its artifact mirror
(`tests/test_primitive_contact.py::test_collision_cells_mirror_lean_literal`);
each row's status and carrier annotation is a **declared label naming the
theorem that carries it**, and it is that theorem, not the row, that is the
evidence.

### 2.13 Value grade vs relation grade

| statement | Lean | reading |
|---|---|---|
| difference *values* carry orientation; the zero *relation* cannot | `ObsDescent.value_orientation_survives` (`ObsDescent.lean:417`): `intDiffObs.delta 0 1 ≠ intDiffObs.delta 1 0 ∧ (ZeroRel intDiffObs 0 1 ↔ ZeroRel intDiffObs 1 0)` | the orientation the native side asserts lives in the values, not in the induced relation |
| two kernels, same induced apartness, different difference maps | `ContactKernel.value_presentation_fork` (`ContactKernel.lean:705`) on `unitValKernel` (`:683`) / `twoValKernel` (`:693`), carrier 2 | value data is strictly finer than the apartness it induces |
| valued kernel morphisms are **not** determined by the carrier map | `ContactKernel.vhom_not_unique` (`:733`), carrier 2 | off-image value freedom; the kernel echo of the sealed `Compression.factor_not_unique_off_image` (`Compression.lean:200`) |
| …uniqueness restored exactly at the epi grade | `ContactKernel.vhom_unique_of_onto` (`:759`) under `hsurj : DeltaOnto K` (`:496`) | the kernel echo of the sealed `PrimitiveCats.phom2_unique_of_epi` (`PrimitiveCats.lean:619`) |

**Relation status: `incomparable` at value grade.** Neither side's value
assignment is recoverable from the other's induced relation
(`value_presentation_fork`), and the supplied file's own tagged construction
uses `Prop` values where the native kernel observer uses paired values (§2.7).
Minimality: carrier 2 in every row; unclaimed below that, because a
subsingleton carrier supports no kernel at all
(`ContactKernel.no_kernel_on_subsingleton`).

### 2.14 Uniqueness scope (a METATHEORY honesty row)

The supplied file's factorization uniqueness is **global**; the sealed native
`Compression` uniqueness is **image-scoped**. These are not in conflict, and
the difference is exactly one fact:

- Global on the quotient side **because the projection is epi**:
  `ObsDescent.obsQuotient_mk_surjective` (`ObsDescent.lean:96`), from which
  `ObsDescent.descend_unique` (`:134`) and `ObsDescent.deltaDescend_unique`
  (`:188`) follow by `funext` + quotient induction.
- Image-scoped on the presentation side, and provably so:
  `Compression.factor_unique_on_image` (`Compression.lean:192`) together with
  the countermodel `Compression.factor_not_unique_off_image`
  (`Compression.lean:200`).
- The kernel stratum reproduces both halves in one pair:
  `ContactKernel.vhom_not_unique` vs `ContactKernel.vhom_unique_of_onto`.

**The difference is precisely codomain coverage by the projection — nothing
more is claimed.** In particular, no claim is made that the sealed corpus was
"missing" a uniqueness theorem; it has the one its notion supports.

### 2.15 Flagship obstruction ↔ native passage obstruction

| direction | status | Lean | exact hypotheses |
|---|---|---|---|
| descent obstruction → collapse collision at the projection | PROVED | `ContactBridge.pair_blocked_is_collapse_collision` (`ContactBridge.lean:678`) | `hxy : ZeroRel O x y`, `hne : ψ x ≠ ψ y`; conclusion `PrimDiff.CollapseCollision (fun u v => ψ u ≠ ψ v) (ObsQuotient.mk O)` |
| collapse collision → descent obstruction | PROVED (added in the audit repair) | `ContactBridge.collapse_collision_is_pair_blocked` (`:688`), by `ObsDescent.obsQuotient_mk_eq_iff` | a collision of `fun u v => ψ u ≠ ψ v` at `ObsQuotient.mk O`; conclusion `∃ x y, ZeroRel O x y ∧ ψ x ≠ ψ y` |
| the two as one biconditional | PROVED | `ContactBridge.pair_blocked_iff_collapse_collision` (`:701`) | none beyond `O`, `ψ` |

With both directions on disk, "the descent obstruction and the native collision
are the same event in two vocabularies" is licensed **at this grade** — and only
at this grade; see non-identification 1 immediately below.

**Two explicit non-identifications (METATHEORY, honesty rows):**

1. The passage obstruction predicate is written with three factors and is
   PROVED equal to the product of **four** total gates (retained, protected,
   declared, plus the collision) by
   `PrimitivePassage.obstP_factors` (`PrimitivePassage.lean:196`); no one of
   the four follows from the other three
   (`PrimitivePassage.gate_zero_independent` (`:499`) and its three
   companions), and the five witness states are
   `PrimitivePassage.obst_conditions_independent` (`:454`). The native
   obstruction is therefore **strictly finer at passage grade**; the flagship
   shape is only its collision conjunct. Scope: independence means
   non-entailment; the gates are NOT jointly free
   (`PrimitivePassage.obs_gates_not_both_false` (`:259`)).
2. The flagship obstruction is a **fixed-quotient descent failure**. The sealed
   `PrimitiveCats.no_terminal_pres` (`PrimitiveCats.lean:548`) and
   `no_terminal_pres2` (`:677`) are **non-existence of universal
   presentations**. These are related in spirit and are **NOT identified**. No
   theorem in this run claims a transport between them.

### 2.16 Placement of the supplied stratum in the passage (hypothesis H1)

| statement | Lean | exact hypotheses |
|---|---|---|
| the passage's declared zero relation **is** a kernel observer's zero relation | `ContactBridge.declared_zero_as_view` (`:628`): `PrimitivePassage.zeroP cols i j = true ↔ ZeroRel (kernelObs (colView cols)) i j` | `cols : List (List Nat)`, `i j : Nat`; proof by list induction over `PrimitivePassage.zeroP_cons` |
| the declared observation stage realizes an observer outright | `ContactBridge.observation_stage_realizes_observer` (`:648`) | `cols`; shipped at the kernel observer's paired value type `List Bool × List Bool` |
| a stage carrying only an observer admits no active obstruction | `ContactBridge.kernel_stage_no_obstruction` (`:666`) over `ContactBridge.kernelStage` (`:657`) | none |
| the kernel licenses passage entry pre-retention | `ContactKernel.kernel_licenses_entry` (`ContactKernel.lean:917`) | none beyond a kernel; reuses sealed `PrimitivePassage.kernel_enters_preretained`. **Scope**: of the three conjuncts only the first (`K.a ≠ K.b`) mentions `K`; conjuncts 2 and 3 are sealed constants about `preRetained` holding with or without any kernel, and no map from an arbitrary kernel into the passage state is constructed — "licenses" names exactly this conjunction, not a transport theorem |
| entry precedes protection and observation, and nothing is obstructed there | `ContactKernel.entry_pre_observation` (`:932`) | none; third conjunct spends sealed `PrimitivePassage.obst_requires_observation` |
| a total two-point presentation costs decidable equality of the carrier | `ContactKernel.kernel_two_point_presentation` (`:945`) | `[DecidableEq X]` — the honest price of totality |

**H1 verified and sharpened:** the supplied primitive is an *admitted observer
at the zero-relation stage*, not a pre-observational witness. At that stage the
native side **proves** (equality grade, via the sealed kernel construction) the
three laws the supplied side admits as fields. **The asymmetry is at the
instance level, not between the signatures** — native `DiffInterface.DiffObs`
carries the same three laws as fields (`DiffInterface.lean:33`), which is what
`H_struct` asserts; what differs is that every concrete observer **of the
sealed corpus at `a5caee2`** is a `kernelObs`, where the laws come out by
`rfl`/`.symm`/`.trans` (verified: at `a5caee2` the only `DiffObs _ _ where`
in `lean4/` is the structure declaration itself; `kernelObs` is the sole
constructor).

**Scope — this is NOT a universal claim about native observers.** This run
itself adds observers that are not `kernelObs`: `ObsDescent.intDiffObs`
(`ObsDescent.lean:359`, laws by linear arithmetic — §2.17),
`ObsDescent.collapseAllObs` (`:437`, laws by `trivial`),
`ContactBridge.wlemZero` (`ContactBridge.lean:454`), the anonymous two-point
observers inside `stability_schema_iff_dne` (`:550`) and
`located_schema_implies_wlem` (`:578`), and — sharpest —
`ContactBridge.apartObs` (`:224`), whose `zero_refl`/`zero_symm`/`zero_trans`
are discharged by `h.irrefl`/`h.symm`/`h.cotrans`, i.e. by the three ADMITTED
`Apartness.IsApart` fields, spent one-for-one (as the `apartObs` docstring
already states). At that native observer the three laws are **exactly as
admitted as on the arriving side**, so no admitted-vs-proved asymmetry holds
there. The asymmetry is asserted only where the observer is a `kernelObs`,
which is what the two placement theorems in the table above establish for the
passage's declared observation stage — and those theorems are correctly scoped
and unaffected. Any summary that reads this row as a structural asymmetry
between the two signatures, or as a universal fact about native observers,
overstates it.

### 2.17 Integer tail ↔ integer observer

The supplied tail (23 declarations) never instantiates the supplied core
structure — the two halves of the supplied file share only a word stem
(FINITE_COMPUTATION). The native side closes that gap:
`ObsDescent.intDiffObs` (`ObsDescent.lean:359`) **is** an observer on `Int`
with difference `a - b`, zero predicate `v = 0`, and **all three law fields
proved** by linear arithmetic; its induced relation is equality
(`ObsDescent.intDiffObs_zeroRel`, `:374`).

| supplied tail shape | count | native lemma | direction |
|---|---|---|---|
| `a ≠ b → a - b ≠ 0` | 8 | `ObsDescent.int_sub_ne_zero_iff` (`:385`), `.mpr` | native-implies (the native `↔` is strictly stronger) |
| `a > b → a - b ≠ 0` | 2 | `ObsDescent.int_sub_ne_zero_of_gt` (`:393`) | native-implies (hypothesis matches exactly: `a > b` is `b < a`) |
| `(s + d) - s = d` | 1 (`@[simp]`) | `ObsDescent.int_add_sub_cancel` (`:411`) | native-implies |
| `(a + c + 2b) - (a + c) = 2b` | 1 | `ObsDescent.int_shift_cancel` (`:398`) | native-implies (same proposition) |
| `2b = 0 ↔ b = 0` and its negation | 2 | `ObsDescent.int_two_mul_eq_zero_iff` (`:403`) | native-implies |
| the 9 integer function definitions | 9 | `ObsDescent.intDiffObs.delta` at the stated arguments | instance-material |

Total 8 + 2 + 1 + 1 + 2 + 9 = **23**, the whole tail. Per-name rows are in
`lean_definition_map.md` §L. **Failed direction: none is claimed in either
direction beyond this subsumption** — the tail contains no statement the native
lemmas do not yield, and the native lemmas contain nothing the tail could
refute.

### 2.18 The raw-quotient barrier (citation-only cell)

`Derivation.quot_barrier` (`lean4/Derivation/Quot.lean:23`) is a barrier at the
level of *raw* quotients, requiring no setoid. The supplied machinery is
setoid-based throughout and therefore cannot state it. **Status:
`NATIVE_MORE_GENERAL`, citation only.** No transport theorem is written in
either direction, and none is claimed.

---

## 3. The factorization-layer dictionary

The sealed native `Compression` layer factors questions through presentations
on a *represented finite domain* `D : List Nat`. The quotient-descent layer
factors views through the observer quotient *globally*. They are the same third
notion, priced differently, and the dictionary is proved — **at `Nat` scope**:
every statement in this section is about `p q : Nat → Nat`, i.e. kernel
observers on the carrier `Nat` with `Nat`-valued views, the typing forced by
`D : List Nat`. Kernel observers at other carriers or view types are outside
these statements, and any citation that says only "for a kernel observer"
should be read with this restriction supplied:

| supplied / descent notion | native `Compression` notion | bridging theorem | grade |
|---|---|---|---|
| `ObsDescent.ClassConstant (kernelObs p) q` — class-constancy | `∀ D : List Nat, Compression.FiberConstant D p q` | `ObsDescent.classConstant_iff_fiberConstant_all` (`ObsDescent.lean:494`) | `↔`, both directions PROVED; `←` instantiates `D := [x, y]` |
| existence of a global factorization through the quotient | `∀ D : List Nat, Compression.FactorsOn D p q` | **`ObsDescent.descend_iff_factorsOn_all`** (`:507`) — the dictionary headline | `↔`, both directions PROVED, via sealed `Compression.factors_iff_fiberConstant` (`Compression.lean:171`) |
| pairing law for views | signature splitting over list append | `ObsDescent.sigEq_append_iff` (`:532`) matched with `ObsDescent.classConstant_pair_iff` (`:212`) | `↔`, both directions PROVED |
| global uniqueness of the factorization | image-scoped uniqueness of the factor | `ObsDescent.obsQuotient_mk_surjective` (`:96`) against sealed `Compression.factor_unique_on_image` / `factor_not_unique_off_image` | citation pair + METATHEORY scope note (§2.14) |
| the quotient's gluing price | representedness + first-match selection | — | METATHEORY: **two priced realizations of one notion**; `Quot.sound` gluing on one side, representedness with first-match selection on the other |

**The `∀ D` quantifier is not removable**, and that is a theorem, not a remark:

> `ObsDescent.fiberConstant_fixed_D_not_classConstant` (`ObsDescent.lean:523`)
> `Compression.FiberConstant [] (fun _ => 0) (fun x => x) ∧ ¬ ClassConstant (kernelObs fun _ : Nat => 0) (fun x => x)`

Countermodel data: the **empty** represented domain `D = []` over the constant
presentation, carrier `Nat`. At any one fixed domain the native notion is
**strictly weaker**. Minimality: the empty domain is the least possible
represented domain, so the separation is exhibited at the extreme point; no
stronger minimality is claimed.

**FINITE_COMPUTATION corroboration** (`artifacts/primitive_contact.json`,
`enumerations.E3_descent_dictionary`): over 64 enumerated
presentation/question combinations, 28 descend, and the fixed-domain divergence
count is 36 — the machine census of the same separation.

---

## 4. Consolidated countermodel index

Every countermodel cited above, with its carrier and minimality status. All 19
are theorems on disk at `ebb1e0b` itself (checked by `git grep` at that commit:
4 in `ContactBridge.lean`, 12 in `ContactKernel.lean`, 3 in `ObsDescent.lean`);
none of them is among the seven later-committed declarations.

| # | Lean theorem | carrier | refutes | minimality |
|---|---|---|---|---|
| 1 | `ContactBridge.unit_total_not_repr` | 1 | representability of the total one-point relation **by a Prop-valued observer** (`∃ O : DiffObs Unit Prop`; readings W, C; `unitBare`/`unitFull` cited) | minimal (least carrier), METATHEORY |
| 2 | `ContactBridge.d2_not_obs_complement` | 2 | representability of the oriented two-point witness **over any value type** (reading A; the sealed interface object) | minimal — METATHEORY: subsingleton ⇒ symmetric |
| 3 | `ContactBridge.triSym_not_obs_complement` | 3 | representability of the symmetric three-point relation (reading Bs) | **minimal, proved** — `bool_bs_repr` is positive at carrier 2 |
| 4 | `ContactBridge.d_not_witnessed_repr` | 2 | witness transport over the empty relation (readings D, E) | carrier minimality **unclaimed**; content is the witness gap |
| 5 | `ContactKernel.no_kernel_on_subsingleton` | 1 | kernel realization from W- or C-grade data | minimal (least carrier) |
| 6 | `ContactKernel.no_kernel_over_allzero` | 2 | kernel realization over the total collapse (readings D, E) | carrier minimality **unclaimed**; content is the witness gap |
| 7 | `ContactKernel.kernel_not_observer` | 2 | kernel→observer promotion (symmetry law field) | minimal — subsingleton ⇒ symmetric |
| 8 | `ContactKernel.kernel_zero_not_trans` | 3 | kernel→observer promotion (transitivity law field) | minimal, inherited from sealed apartness pricing + `bool_bs_repr` |
| 9 | `ContactKernel.kernel_not_bs` | 2 | K → Bs at the kernel stratum | minimal — as row 7 |
| 10 | `ContactKernel.kernel_not_bc` | 3 | K → Bc at the kernel stratum | minimal, inherited from sealed `PrimitiveCore.cotrans_auto_on_two` |
| 11 | `ObsDescent.collapseAllObs_no_delta_descend` | 2 | unconditional descent of the difference map | minimal — subsingleton ⇒ every view class-constant |
| 12 | `ObsDescent.collapseAllObs_no_view_descend` | 2 | unconditional descent of views | minimal — as row 11 |
| 13 | `ObsDescent.fiberConstant_fixed_D_not_classConstant` | `Nat`, `D = []` | removability of the `∀ D` quantifier in the dictionary | extreme point (empty domain); no stronger claim |
| 14 | `ContactKernel.pair_choice_load_bearing` | 2 | an arbitrary pair may fail the side condition — a statement about pairs, not about kernels; non-uniqueness of the kernel is the separate `kernel_not_unique_of_pair` | METATHEORY (subsingleton supports no kernel) |
| 15 | `ContactKernel.kernel_no_witness_from_collapse` | 2 | existence of any complement witness over the total collapse | METATHEORY (subsingleton supports no kernel), as row 14 |
| 16 | `ContactKernel.vhom_not_unique` | 2 | carrier-map determinacy of valued kernel morphisms | METATHEORY (subsingleton supports no kernel), as row 14 |
| 17 | `ContactKernel.kernel_no_terminal` | 3 | any terminal collector of kernels (free-point branching) | carrier 3 as stated; minimality **unclaimed** |
| 18 | `ContactKernel.kernel_gateways_not_identical` | 2 | presentation-identity of initial gateways | matches sealed `PrimitiveCats.two_initials_not_identical` scope |
| 19 | `ContactKernel.kernel_not_e_merged` | 2 | E-transport under one declared merger | inherits the sealed `PrimDiff.merger_erases` pattern |

Universal status, for completeness (not countermodels): the initial gateway is
**inherited, never re-proved** — `ContactKernel.kernel_gateway_unique` (`:811`)
*is* `PrimitiveCats.d2_initial` instantiated; `kernel_gateway_injective`
(`:565`) is `PrimitiveCats.d2_map_injective` instantiated;
`ContactKernel.apartObj_sym_of_observer` (`:802`) places observer-derived
kernels in the symmetric subcategory where `PrimitiveCats.s2_initial_sym`
applies; and `ContactKernel.kernel_no_terminal_collector` (`:886`) derives
from row 17.

---

## 5. Priced OPEN cells — where no countermodel can exist

Four cells are OPEN. In each the reason is the same and is stated exactly: the
schema quantified over all observers/kernels is **classically true**, so no
internal countermodel can exist. The honest output is a price, not a
refutation.

| cell | record (Lean `String` constant) | price proved |
|---|---|---|
| unconditional cotransitivity of an observer complement | `ContactBridge.open_bridge_cotrans` (`:607`) | **exactly** WLEM — `ContactBridge.cotrans_schema_iff_wlem` (`:519`); discharged by pointwise decidability (`obsApart_cotrans`) |
| unconditional locatedness of an observer complement | `ContactBridge.open_bridge_located` (`:612`) | **implies** WLEM — `ContactBridge.located_schema_implies_wlem` (`:578`); converse explicitly not claimed (would need function comprehension beyond WLEM); discharged by decidability (`obsSetting_bl`) |
| kernel round-trip grade without decidability | `ContactKernel.open_kernel_grade` (`:201`) | double-negation-coarse; residual schema priced at DNE via `ContactBridge.stability_schema_iff_dne` (`:550`); exact under `ofSetting_exact` |
| kernel locatedness without decidability | `ContactKernel.open_kernel_bl` (`:623`) | discharged by `ContactKernel.kernel_located_of_decidable` (`:614`); underivability from the kernel fields alone is METATHEORY, so `Located` remains separate data |

These follow the sealed open-cell discipline already in the corpus (the
`open_cell_*_bl` pattern), and each record states its own price in full.

**Registration (audit repair).** All four are registered as open obligations
in `artifacts/primitive_completion_receipt.json` (`open_obligations`, entries
prefixed `COLLISION OPEN CELL`, each carrying its price), which the collision
therefore takes from four entries to eight. The converse of
`located_schema_implies_wlem` is additionally registered under
`frontier_conjectures` as `LOCATEDNESS_SCHEMA_EQUALS_WLEM`, alongside the
enlarged-corpus containment conjecture — three entries to five. A reader
checking whether this run left new unresolved obligations must find them
there, not only here.

---

## 6. Comment-vs-theorem gap table

**Ruling, restated at the point of use: comments are not evidence.** Each row
quotes the supplied comment (SUPPLIED_INPUT), states the declaration's actual
formal content, names the gap exactly, and records the disposition. A
disposition of **REFUSED** means the advertised content is not transported in
any form. A disposition of **RECORDED** means the comment is honest or
near-honest and only naming remains uninterpreted.

The recurring pattern in the supplied tail: **every physics-labeled theorem is
an integer-subtraction fact of the shape `a ≠ b → a - b ≠ 0` or
`a > b → a - b ≠ 0`, with the physics living entirely in variable names and
comments.**

| # | supplied comment (verbatim, SUPPLIED_INPUT) | declaration and actual statement | exact gap | disposition |
|---|---|---|---|---|
| G1 | "Primitive Difference for Phase Fiber Interference: Compares the L1 diagonal mass sum `w1 + w2` with the superposed norm `\|w1 + w2 + Δ_int\|`." | item 81 := `(w1 + w2 + delta_int) - (w1 + w2)` | no norm, no L1 structure, no phases; the definition is identically `delta_int` | **REFUSED** |
| G2 | "**LGGR Non-Factorization Theorem.** When interference cross-term `delta_int ≠ 0`, the Primitive Difference `Δ_int` is non-zero, proving that diagonal L1 data alone cannot carry phase interference." | item 83 : `d ≠ 0 → d ≠ 0` after the file's own simp lemma | no factorization, no L1 space, no interference model appears in the statement; "Non-Factorization" borrows the abstract half's vocabulary without using it | **REFUSED**; content subsumed by `int_add_sub_cancel` + `int_sub_ne_zero_iff` |
| G3 | "Bipartite product defect Primitive Difference: δ_prod = w(a,b) - (margA(a) * margB(b) / W)." | item 84 := `w_ab * total - marg_a * marg_b` | comment describes a division-normalized defect; code is the cross-multiplied form, with no claim relating the two; no tables, no marginalization operator | **REFUSED** |
| G4 | "**LGGR Product Non-Factorization Theorem.** When joint table `w(a,b)` does not factor through its marginals, the bipartite product defect Primitive Difference is non-zero." | item 85 : `u ≠ v → u - v ≠ 0` | the hypothesis *is* the claimed "does not factor" fact restated; nothing about joint tables or marginals is derived | **REFUSED** |
| G5 | "Parity cochain contextuality Primitive Difference: Compares local context products (+1) with global parity closure (-1)." | item 86 := `local_prod - global_target` | no `+1`, no `-1`, no cochain, no context set — two free integers | **REFUSED** |
| G6 | "**LGGR Contextuality Obstruction Theorem.** … the contextuality Primitive Difference is non-zero (2 ≠ 0)." | item 87 : `a ≠ b → a - b ≠ 0` | the advertised instance "(+1) vs (−1), 2 ≠ 0" is never stated or instantiated; no observables, contexts or commutation structure exists in the file | **REFUSED** |
| G7 | "CPTP trace-norm defect Primitive Difference: Compares local trace distance gauge \|\|ρ - σ\|\|_tr with CPTP contracted image \|\|E(ρ) - E(σ)\|\|_tr." | item 88 := `dist_orig - dist_cptp` | no density operators, channels, complete positivity, or trace norm — two free integers | **REFUSED** |
| G8 | "**LGGR CPTP Trace-Norm Contraction Theorem.** … the Primitive Difference is positive and non-zero." | item 89 : `a > b → a - b ≠ 0` | comment claims positivity; the statement proves only `≠ 0` (positivity would be derivable but is not stated); no contraction theorem for any channel class is present | **REFUSED**; order-hypothesis form subsumed by `int_sub_ne_zero_of_gt` |
| G9 | "Non-abelian closed-loop holonomy Primitive Difference: Compares flat gauge Wilson loop (+1) with non-abelian commutator curvature (-1 for Q8 plaquette)." | item 90 := `flat_hol - nonabelian_hol` | no group, no loop, no connection, no Q8 — two free integers | **REFUSED** |
| G10 | "**LGGR Holonomy Curvature Obstruction Theorem.** … the holonomy Primitive Difference is non-zero (2 ≠ 0 for Q8 commutator)." | item 91 : `a ≠ b → a - b ≠ 0` | "Q8 commutator" and "2 ≠ 0" never instantiated | **REFUSED** |
| G11 | "Authority non-promotion defect Primitive Difference: Compares formally derived structure score with unsealed authority status." | item 92 := `derived_score - auth_sealed` | "score" and "status" are free integers; no scoring function, no sealing predicate | **REFUSED** |
| G12 | "**LGGR Authority Non-Promotion Firewall Theorem.** Formal derivation alone (derived_score > 0) without a sealed terminalizer (auth_sealed = 0) leaves a non-zero Primitive Difference, proving StructureDerived ⊬ IsAuth." | item 93 : `a ≠ b → a - b ≠ 0` | **the largest single gap in the supplied file**: a proof-theoretic non-derivability claim between two predicates that are never defined anywhere; no proof system, no derivability relation, no independence argument exists in the file; the comment's hypotheses (`> 0`, `= 0`) differ from the actual hypothesis (`≠`) | **REFUSED** — nothing of this claim is transported, restated, or weakened-and-restated |
| G13 | "Gell-Mann--Hartle two-history integer residual. It compares a declared global integer weight with a local diagonal integer weight; no probability, positivity, or normalization structure is encoded." | item 94 := `total_prob - diag_sum` | **honest comment** — it explicitly disclaims probability/positivity/normalization; residual gap is name-flavor, plus a parameter still named `total_prob` | **RECORDED** |
| G14 | "The two-history integer presentation makes the decoherence residual exactly `2 * D12` …" | item 95 : `(a + c + 2b) - (a + c) = 2b` | the integer identity is real; the decoherence-matrix reading exists only in the caller's choice of substitution; nothing constrains the parameter to be an off-diagonal entry of anything | **RECORDED**; identity subsumed by `int_shift_cancel` |
| G15 | "The two-history residual vanishes exactly when the off-diagonal integer coordinate vanishes." / "… is nonzero exactly when …" | items 96, 97 : `2b = 0 ↔ b = 0` and its negation | accurate as integer statements; "history"/"off-diagonal" is naming only | **RECORDED**; subsumed by `int_two_mul_eq_zero_iff` |
| G16 | "Generic nonzero residual theorem. When global and local integer weights differ, their Primitive Difference is nonzero." / "A nonzero off-diagonal coordinate makes the two-history integer Primitive Difference nonzero." | items 98, 99 | near-honest ("integer weights"); "global/local" and "off-diagonal" remain uninterpreted names | **RECORDED** |
| G17 | "Threshold repair capacity defect… **LGGR Threshold Repair Capacity Absorption Theorem.** When physical defects remain unabsorbed by syndrome repair image B^1 …, the residual logical pairing Primitive Difference is strictly positive and non-zero." | item 101 : `a > b → a - b ≠ 0` | no code, no syndrome map, no coboundary space `B^1`, no threshold theorem; comment claims strict positivity, only `≠ 0` is stated | **REFUSED** |
| G18 | "Classical limit cochain projection defect… **LGGR Classical Limit Cochain Projection Theorem.** When phase fiber fluctuations remain unprojected …, the phase holonomy Primitive Difference is non-zero." | item 103 : `a ≠ b → a - b ≠ 0` | no U(1), no cochains, no projection operator, no limit | **REFUSED** |
| G19 | section headers carrying external program tags ("QM_060/QM_061", "QM_070/QM_071", "QM_120/QM_121", "QM_080/QM_081", "QM_110/QM_111", "QM_090/QM_092", "QM_043", "QM_100/QM_101/QM_102", "QM_112") | headers only; no declarations of their own | the tags refer to an external numbered program; nothing in the file establishes any link to whatever they denote | **REFUSED** |
| G20 | interpretive slogan in the theorem names of the abstract half (`localGreenGlobalRed_*`, supplied items 50, 51, 52, 59, 75, 76) | genuine factorization/obstruction conjunctions — see `lean_definition_map.md` | **the gap is in the name only.** The statements are exactly what they say (one observable factors, the pair does not) and are correctly proved. **No formal overclaim.** | **branding not imported**; content transported in full as `ObsDescent.view_descends_pair_blocked` |

**Simp-tag inventory (FINITE_COMPUTATION):** exactly one `@[simp]` exists in
the supplied file — on the equality of item 82. Conclusion shapes across the
14 tail theorems: 10 disequalities, 2 equalities, 2 iffs; hypothesis shapes: 8
`≠`, 2 `>`, 4 with no hypothesis.

**Axiom profile of the supplied file (FINITE_COMPUTATION, 71 reports):**
**16** theorems axiom-free, **26** `[Quot.sound]` only, **29**
`[propext, Quot.sound]`; 16 + 26 + 29 = 71. `Classical.choice` appears
**nowhere** — including in the 14 `omega`-proved tail theorems. This is exactly
within this repository's gate (`propext` and/or `Quot.sound` only), and the
native reconstruction was held to the same budget.

> **Correction recorded (reported, not softened).** A prior-run scratch
> intermediate for this collision (`inv_contact.md`, section 4 summary line)
> tallied the same 71 reports as "13 axiom-free; 25 `[Quot.sound]`; 33
> `[propext, Quot.sound]`". That summary line is a **miscount**. Recounting the
> 71 verbatim entries of `contact_scratch/axiom_report.txt` — which the same
> intermediate quotes in full, and which are reproduced one per row in
> `lean_definition_map.md` — gives **16 / 26 / 29**. The verbatim entries, not
> the summary line, are the evidence; the totals agree (71) and no
> individual report line differs. Nothing downstream depended on the tally: no
> claim in either deliverable, in `contact_dictionary.md`, or in
> `artifacts/primitive_contact.json` uses the 13/25/33 figures.

**Native axiom profiles, spot-verified against `artifacts/lean_axioms.txt`
(FINITE_COMPUTATION):** `ObsDescent.obsQuotient_mk_eq_iff`,
`descendMod_exists_iff` and `deltaDescendMod_exists_iff` each report
`[propext, Quot.sound]`, matching their supplied counterparts;
`ObsDescent.descend_mk`, `deltaDescend_mk`, `classConstant_pair_iff`,
`collapseAllObs_not_deltaConstant` and `collapseAllObs_id_not_classConstant`
each report "does not depend on any axioms", matching theirs.

---

## 7. What the transport supports

Stated only to the strength the theorems above carry. The recorded terminal
codes are in `PrimitiveContact.contactStatusCurrent` /
`contactVerdictPrimary` (`PrimitiveContact.lean:126`, `:126`) and in
`artifacts/primitive_contact.json`; this section says what the transport
evidence does and does not establish, and nothing further.

1. **Native → supplied is refuted at signature level, permanently.** The
   witness is `ContactBridge.d2_not_obs_complement`, which quantifies over
   **every** value type: no observer's zero-complement is the oriented
   two-element relation. The full expressive range **for Prop-valued
   observers** is characterized by `ContactBridge.obsApart_repr_iff` and
   counted by machine (Bell numbers 1, 2, 5 at carriers 1, 2, 3). Each of the
   nine candidate readings fails representability or witness transport, at the
   carriers tabulated in §2.9 — where the second row of that table is part of
   the claim: **carrier minimality is proved for Bs only**, is METATHEORY for
   W/A/C, is inherited (not separately witnessed) for Bc/Bl/F, and is
   explicitly unclaimed for D/E.

2. **Supplied → native was a content gap, and it is closed this run, not
   pre-existing — and that half is an ABSENCE claim, not a countermodel.** The
   `WITH_COUNTERMODELS` of the primary terminal code covers direction 1 above;
   nothing refutes the supplied layer, and its content is in fact derivable
   natively at the `Nat` scope of §3. The global quotient-descent layer was
   absent from the sealed
   corpus at `a5caee2`; `ObsDescent` reconstructs it in native vocabulary under
   an axiom budget within `{propext, Quot.sound}`, matching the supplied
   reports theorem for theorem. **No claim is made that the sealed corpus
   already contained it**, and the "native strictly stronger" reading is
   explicitly not issued for that reason (recorded in the artifact's
   `verdict.not_issued`).

3. **The shared kernel is a meet, and "replaces" is scoped.**
   `ContactKernel.WitnessedDiff` is realized from both sides
   (`ofSetting`/`ofDiffObs`), recomposes into the observer stratum as a record
   identity (`toDiffObs`, `toDiffObs_fields`, `toDiffObs_apart` — §2.11, last
   row: DEFINITION grade, `rfl`-proved, the observer-side half of "replaces"),
   meets the sealed pre-contact interface (`toNativeKernel`), and carries
   proved universal status: `kernel_gateway_unique` inherited from
   `d2_initial`, and `kernel_no_terminal_collector` **at the induced-apartness
   morphism grade** — it and `kernel_no_terminal` quantify over
   `PrimitiveCats.Hom (apartObj K) (apartObj K')`, morphisms of the induced
   pointed-relation presentations, which discard the value data; the module's
   own valued morphism category `VHom` is a different grade, and no terminality
   statement is proved there. Value rigidity is likewise one-directional:
   `vhom_unique_of_onto` is sufficiency under delta-surjectivity and
   `vhom_not_unique` is one non-onto countermodel — no equivalence, so
   delta-surjectivity is not claimed necessary. It does **not** replace native
   orientation, retention, protection, operations, or passage dynamics — that
   surplus is native-only, and the negative cells of §2.12 say so as theorems.

4. **The scoped equivalence is exactly scoped — and the decidability premise
   is TWO admissions, one per direction.** Apartness → observer spends
   pointwise decidability of the **asserted apartness** relation
   (`isApart_repr`, `apartObs_roundtrip`, both under
   `[∀ x y, Decidable (r x y)]`); observer → apartness spends pointwise
   decidability of the **zero** relation (`obsApart_isApart`,
   `indist_obsApart_iff`, both under `[∀ x y, Decidable (ZeroRel O x y)]`) —
   exactly as tabulated in §2.8. The two are **not** interchangeable: the zero
   relation of `apartObs r h` is `¬ r`, and `Decidable (¬ P)` does not return
   `Decidable P` constructively, which is precisely the residue
   `stability_schema_iff_dne` prices at DNE. Under both admissions plus the
   three apartness admissions the native apartness stratum and the
   supplied-style observer are inter-constructible with matching relations in
   **both** round trips. Dropping decidability is priced (WLEM, DNE,
   WLEM-implication with the converse OPEN); dropping any apartness admission
   is refuted at carriers 1, 2, 3. Sufficiency is what is proved — necessity of
   either decidability admission for a fixed observer is not. **Valuation data,
   orientation, and everything dynamic are outside this scope** (§2.13, §2.15,
   §2.16).

5. **Two things are deliberately not claimed.** The flagship descent
   obstruction is **not** identified with the sealed non-existence of universal
   presentations (§2.15), and the raw-quotient barrier remains strictly more
   general than anything the supplied setoid-based machinery can state
   (§2.18). Nothing in this run touches constitution-class minimality; gateway
   uniqueness is inherited initiality, **up to isomorphism only** (sealed
   `PrimitiveCats.initials_iso`, with
   `ContactKernel.kernel_gateways_not_identical` marking the scope).
