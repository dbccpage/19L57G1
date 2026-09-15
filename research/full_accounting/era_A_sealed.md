# Era A — sealed derivation (2026-08-11 … 2026-08-16)

`AuthorityEffect: None.` 190 commits on HEAD before 2026-08-17.
Source of the narrative: `paper/paper_change_log.md` entries 1–15 and
the PR #12–#21 / contact / naturality entries through 2026-08-16, plus
`git log --reverse` on this era. SHAs below are from `eras.md`.

This is the experiment. Everything after either discharges its
residuals, continues it read-only, or hosts a different experiment.

---

## 2026-08-11 — greenfield in one day

Two roots: `5a5990d8` (seed: uninterpreted repository) and `6fb1f66d`
(GitHub Initial commit). Merged as PR #1 `c6bded55`.

| SHA | what |
|---|---|
| `5a5990d8` | uninterpreted seed |
| `933c9524` | `CLAUDE.md` plan; prompt bytes carried identically |
| `23a1f31c` | Python kernel: regime, replay, observe, candidates, iso, engine |
| `cc752c88` | first artifacts (challenges, 4 trees, no-supply, claims) |
| `6e628ee3` | tests: 69, line 99.9% / branch 98.8%, mypy strict |
| `9a68a7ff` | first Lean: 33 exported theorems, axioms `{propext, Quot.sound}` |
| `05f1f231` | correction set 1 (endogenous generator, branch termination) |
| `a52e929d` | paper + correction set 2 (`wfCtx` arity, token-erasure) |
| `bdb81d77` | correction set 3 (equivariant orbits, closure policy, CI, DAG) |

Canonicalization defect (`iso.py` in-place permute) found **before**
any published artifact: would have reported 6 L-classes instead of 3.

Caller corrections 1–3 (change log §§4–6): blindness (no post-hoc
comparison section); minimality scoped; unboundedness downgraded then
removed; “endogenous generator” later renamed to declared
pair-separation closure; no object-language demand generator derived;
CI and DAG exports.

## 2026-08-12 — freeze, then the native spine

| SHA / PR | what |
|---|---|
| `42c6c49b` PR #2 | correction set 4: per-edge merge certificates; honest equivariance; `Ext.lean` |
| change log §8 | paper suite frozen |
| PR #3 | primitive-difference candidates, D2/S2, orientation gap |
| PR #5 | bridge: provenance of those ingredients from `<>` |
| PR #7 | refusal as difference; frontier run 006 |
| F5 | composite generator (`Generator.lean`): fires from round 3, horizon-free, **not genesis from `<>`**; `OBJECT_LANGUAGE_GENERATOR_NOT_IN_SCOPE` |
| DiffInterface | typed difference; obstruction = retained ∧ observer-zero ∧ protected; proposals never apply |
| Represented | can progress causes themselves be represented? |
| Ultra closure PR #11 | `Completion`, `NoOutside`, `Constitution`, `Initiality`; native map |

Ultra-closure terminals (change log §14, narrowed in §15):

- `RELATIVE_REPLAY_CLOSURE_ONLY`
- event source and constitution internalized **relative to a fixed interpreter**
- `KERNEL_CONSTITUTION_REMAINS_META` (the one OPEN bridge)
- unique probe-compliant descriptor in a declared 64-toggle class
  (not categorical initiality)
- `ABSOLUTE_NO_OUTSIDE_UNFORMULABLE`
- `FULL_NATIVE_COMPOSITION` **not claimed**

Axiom reports that day: 33 → … → 295.

## 2026-08-13 — contact collision and goals 1–5

Declared contact input arrived (`CONTACT_PROCESSED_LEAN_ONLY`). One
external Lean file bound by `contact/omega_primdiff/CONTACT_MANIFEST.json`,
read statements-only, vocabulary quoted only in `contact/analysis/`.

New sealed modules: `ObsDescent`, `ContactBridge`, `ContactKernel`.
Axiom reports 1037 → 1149 at that spine.

Goals: renaming structure around Up (`Attachment`); graph-genesis
boundary; general boundary cancellation; one-step codebook and trace
algebra. Contact response: finite weights, **no climb** to an infinite
inner-product completion (that sentence is the refusal of a named
outside target, recorded without naming it in live paper later).

PR #12 / #13: characterization, passage, growth; carrier correction.

## 2026-08-14 — naturality, capacity, fidelity

- Naturality obstruction across presentations
  (`PresentationNaturality`: no natural section of a fixed-point-free
  auto family)
- Heterogeneous many-object transport; bundle coherence
- Coloured separation-capacity bound, closed
- Presentation-relative identity; comparison-forced refinement
- Closure failure as loss of internal symmetry invariance
- Heterogeneous fidelity closure; endogenous quotient generator
- Depth-`d` outrun on the reflective chain
- Packet 5 audit; pair-choice lemma

## 2026-08-16 — receipts stale; stopping conditions claimed

Change log: the paper’s own receipts were stale; measured and
withdrawn. Stopping conditions reported met this day as an **operator
claim**. No gate consumes that report. Re-run the next day
(`verification_20260817.md`) discharges mechanical clauses only.

Coda trees were added around this window under separate rules, then
removed 2026-08-17 (`27a1bba8`). They are not in this repository.
`dbccpage/CODA` is private. Do not treat their absence as a defect.

---

## What Era A proved (the foundation)

Quoted from `paper/paper.md` §11, tags kept:

- (a) initial inscription generates nothing; supply ≠ admission
- (b) admission without judgment structure: total collapse; admission
  need not increase expressive power
- (c) first separability costs **exactly two** items, both readings
- (d) `mu1`: tied (3 classes L, theorem; 5 classes F, bounded); infinite
  arity family in L; `mu2`: unique up to iso, grammar-wide both readings
  (F uniqueness became a theorem 2026-08-18)
- (e) every supplied separation demand on a wf accepted regime is
  answerable
- (f) no object-language endogenous demand generator; pair-separation
  closure terminates
- (g) with external supply, depth 15 reached; beyond exported depths
  unresolved; no unboundedness claimed
- (h) two admission readings L and F survive; no internal fact
  separates them

Native map (`paper/native_derivation_map.md`): two-ness does not
equivariantly yield orientation; orientation is a priced asymmetry;
irreflexivity fact does not entail the law; proposals do not
self-execute; kernel constitution does not interpret itself absolutely.

Succession (`paper/succession_declarations.md`): a successive-state
model needs a persisting carrier, a single-valued next, and an
individuating order. This system derives **none**.

Refutations in this era that a “complete system” plan must not revive:

- Controller **initiality REFUTED** (PR #12, packet VII); uniqueness only
  on the genesis-reachable orbit.
- Graph genesis **by obstruction settled negative** for this calculus
  (Goal 5): growth is supplied, never by `nextFamilyP`.
- Absolute no-outside **unformulable**.
- `FULL_NATIVE_COMPOSITION` not claimed.
- Categorical initiality of the kernel **withdrawn** (toggle-class
  uniqueness only).

That is the foundation. It is a foundation *because* the interesting
results are refusals.
