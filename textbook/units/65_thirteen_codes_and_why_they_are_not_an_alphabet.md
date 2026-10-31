# Unit 65. Thirteen codes, and why they are not an alphabet

**Claim.** On the declared class of live states whose protected pairs are retained, thirteen effect classes summarize accepted single transitions. Equal class signatures can behave differently under a common suffix, so they do not form a composable event alphabet.

<details>
<summary>Sources and classification (optional)</summary>

**Status:** FROZEN (the guard characterization, 13-code partition on `WFClass`, 12-code guard-erased collapse, non-congruence countermodels, non-invariance countermodels, refusal preservation of `obstEffect`, load-bearing `WFClass` countermodel `outsideClass`, refutation of unqualified environment ownership, and 13 store-coherent witnesses); ADMITTED (the profile types `ObstEffect`, `ObstMove`, `FieldDelta`, `GuardKind`, `BudgetDelta`, `Continuity`, `Origin`, `Profile`, `ClassSig`, `EffectSig`, `EffectClass`, and `WFClass`); VERIFIED_FINITE (`artifacts/transition_alphabet.json`).
**Lean:** `lean4/Derivation/TransitionAlphabet.lean` lines 75–1893.
**Axioms:** `propext`, `Quot.sound` on 100 of 116 public theorem reports; `propext` on 7; `none` on 9 (`artifacts/lean_axioms.txt` lines 889–1004).
**Depends on:** Unit 54 (`PrimitivePassage.PState`, `PEvent`, `step`, `replayP`, `genesisP`, `obstP`, `obstructedPairs`, `nextFamilyP`, `step_halted`, `wfPair`, `refineOk`, `colOk`).

---

</details>

## First pass

Use the [Change lab](../change_lab/README.md) if event replay is unfamiliar.

An **effect class** is a short summary of one event acting on one state.
Compare two admissions from the empty live state:

| First request | Occurrences afterward |
|---|---|
| Admit token 0 | `[0]` |
| Admit token 2 | `[2]` |

Both transitions receive the same effect signature. The summary records
the kind of change while omitting the admitted token's value. Here
**accepted** means the full state changed; it is the defined test
`step s e ≠ s`.

**Predict.** Now send the same request, admit token 0, to both outputs.
Must the resulting occurrence lists agree?

<details>
<summary>Check your prediction</summary>

No. The first stays `[0]`; the second becomes `[2, 0]`. Admission
deduplicates a token already present. Equal summaries of earlier steps
therefore cannot replace the information needed for later replay.

</details>

The thirteen-class theorem uses a declared class of live states in which
every protected pair is retained. These thirteen summaries are not the
eleven event constructors or a complete record of their parameters.

<details>
<summary>Detailed statement and formal anchors (optional)</summary>

## Detailed claim and formal anchors

On the eleven-constructor primitive-passage transition system `(PState, PEvent, step)`, acceptance `Accepted s e := decide (step s e ≠ s)` coincides with the explicit constructor guard `guardHolds s e`; on the live well-formed class `WFClass s` (`s.halted = false ∧ ∀ p ∈ s.prot, p ∈ s.wit`), every accepted transition `(s, e)` maps through the five-component projection `sigOf s e : ClassSig` to a unique member of a thirteen-element `EffectClass` codebook (`declared_codebook_size : (dedup (allClasses.map classSig)).length = 13`); erasing the guard label (`eraseGuard : ClassSig → EffectSig`) merges `.refineObservation` and `.extendObservation` (`refine_addCol_effect_merge`) into a twelve-element codebook (`guard_erased_codebook_size = 12`) even though `.refineCol` does not check `s.licensed` while `.addCol` does (`refine_addCol_domain_countermodel`); and these thirteen codes are a one-step transition codebook on `(s, e)` rather than a composable event alphabet because equal signatures are separated by a common suffix (`classSig_not_right_congruent_occurrence`, `classSig_not_right_congruent_budget`), the dropped profile components `ObstEffect` (`.untouched` vs. `.preserved`) and `BudgetDelta` (`.rewritten` vs. `.spentOne`) vary across pre-states (`preserved_untouched_not_invariant`, `budgetDelta_not_invariant`), `WFClass` is load-bearing for retention (`retention_creates_outside_class`), and `nextFamilyP` emits the environment-classified constructor `.setBudget 1` (`env_ownership_claim_refuted`, `internal_family_env_only_unit_funding`) (`TransitionAlphabet.accepted_eq_guardHolds`, `TransitionAlphabet.exists_unique_class`, `TransitionAlphabet.declared_codebook_size`, `TransitionAlphabet.guard_erased_codebook_size`, `TransitionAlphabet.classSig_not_right_congruent_occurrence`, `TransitionAlphabet.classSig_not_right_congruent_budget`, `TransitionAlphabet.refine_addCol_effect_merge`, `TransitionAlphabet.refine_addCol_domain_countermodel`, `TransitionAlphabet.preserved_untouched_not_invariant`, `TransitionAlphabet.budgetDelta_not_invariant`, `TransitionAlphabet.budgetDelta_of_funded_guard`, `TransitionAlphabet.retention_creates_outside_class`, `TransitionAlphabet.refuse_preserves`, `TransitionAlphabet.env_ownership_claim_refuted`, `TransitionAlphabet.internal_family_env_only_unit_funding`, `TransitionAlphabet.nonEnv_preserves_occ_licensed`, `TransitionAlphabet.class_witnesses`, `TransitionAlphabet.class_witness_sizes`).

</details>

## Question

The primitive-passage grammar `PEvent` has eleven constructors (`admitOcc`, `assertWit`, `admitWit`, `protect`, `declareObs`, `refineCol`, `addCol`, `refuse`, `setBudget`, `setLicense`, `halt`). When we classify every accepted transition `s ↦ step s e` of a live well-formed state `s` (`WFClass s`) by which of the nine state fields changed (`FieldDelta`), which constructor guard was checked (`GuardKind`), whether the obstructed-pair list gained, lost, or kept its pairs (`ObstMove`), whether the post-state is live or halted (`Continuity`), and the constructor's declared policy label (`Origin`), how many distinct transition signatures arise? Why does erasing the guard label drop the count from 13 to 12? And why do those 13 signatures form only a **one-step transition codebook** on `(s, e)`, rather than a composable event alphabet?

---

## What we already possess

From Unit 54 (`lean4/Derivation/PrimitivePassage.lean`), we have the nine-field ledger `PState` (`occ`, `asserted`, `wit`, `prot`, `obs`, `budget`, `licensed`, `refusals`, `halted`), the eleven-constructor event type `PEvent`, the single-step transition `step : PState → PEvent → PState`, the helper predicates `wfPair`, `refineOk`, `colOk`, the pair obstruction predicate `obstP s i j`, the obstructed-pair list `obstructedPairs s`, and the internal response family `nextFamilyP s`.

---

## New concept: the seven-axis `Profile`, the five-axis `ClassSig`, and the thirteen `EffectClass` codes

`TransitionAlphabet` builds its classification in nine sections:

1. **Acceptance and explicit guards (Section 1, lines 75–365):**
   - `Accepted (s : PState) (e : PEvent) : Bool := decide (step s e ≠ s)`.
   - Named post-states `occS`, `assS`, `witS`, `protS`, `obsS`, `refineS`, `colS`, `refuseS`, `budS`, `licS`, `haltS` (lines 100–128) isolate the eleven record updates, and `occS_ne`..`haltS_ne` (lines 136–182) prove that each update differs from `s` whenever its guard holds.
   - `guardHolds (s : PState) : PEvent → Bool` (line 189) writes out the exact boolean guard for each of the 11 constructors, and `accepted_eq_guardHolds` (line 359) establishes `Accepted s e = guardHolds s e` for every `s` and `e`.

2. **Exact obstruction delta (`ObstEffect` and `ObstMove`, Section 2, lines 595–921):**
   - `gainedPairs s t` filters `obstructedPairs t` for pairs not in `obstructedPairs s`; `lostPairs s t` filters `obstructedPairs s` for pairs not in `obstructedPairs t`.
   - `obstEffect (s t : PState) : ObstEffect` checks `!(lostPairs s t).isEmpty` first (`.removed`), then `!(gainedPairs s t).isEmpty` (`.created`), then `(obstructedPairs s).isEmpty` (`.untouched`), and otherwise `.preserved`.
   - `coarse : ObstEffect → ObstMove` maps `.created ↦ .creates`, `.removed ↦ .removes`, and both `.preserved` and `.untouched` to `.inert`.
   - Constructor lemmas prove that `occS`, `assS`, `witS`, `refuseS`, `budS`, `licS`, and `haltS` leave `obstructedPairs` unchanged; `protS` and `obsS` either leave `obstructedPairs` unchanged or create an obstruction; and `colS` and `refineS` shrink `obstructedPairs` (`obstructedPairs_colS_sub`, `obstructedPairs_refineS_sub`, `colS_lost_ne_nil`, `refineS_lost_ne_nil`), giving `obstEffect = .removed`.
   - **Audit note on `gainedPairs` for `colS` and `refineS`:** The docstring at line 591 says "each constructor lemma below establishes one of the two difference lists empty." For `colS` and `refineS`, the module establishes the subset inclusions `obstructedPairs_colS_sub` and `obstructedPairs_refineS_sub` together with `colS_lost_ne_nil` and `refineS_lost_ne_nil`; the equations `gainedPairs s (colS s cols c) = []` and `gainedPairs s (refineS s cols v p) = []` follow in one line from those subset lemmas via `filter_notmem_eq_nil` (proved explicitly in `textbook/checks/u65_lean.py`).

3. **Full profile `Profile`, projected signature `ClassSig`, and guard-erased `EffectSig` (Section 3, lines 925–1200):**
   - `FieldDelta` records a 9-tuple of booleans (`t.occ != s.occ`, ..., `t.halted != s.halted`), with ten named patterns `fdOcc`..`fdHalted`.
   - `GuardKind` has 11 constructors (one per `PEvent` constructor); `BudgetDelta` has 3 (`.unchanged`, `.spentOne`, `.rewritten`); `Continuity` has 2 (`.continuation`, `.absorption`); `Origin` has 2 (`.environment` on `admitOcc`, `setBudget`, `setLicense`, `halt`; `.internal` on the other 7).
   - `Profile` bundles all 7 components (`fields`, `guard`, `obst`, `budget`, `cont`, `origin`, `accepted`); `ClassSig` projects onto the 5 components `(fields, guard, move, cont, origin)` where `move = coarse obst`; and `eraseGuard : ClassSig → EffectSig` drops `guard` to leave the 4-tuple `(fields, move, cont, origin)`.

4. **The well-formed class `WFClass` (Section 4, lines 1209–1320):**
   - `WFClass s` holds when `s.halted = false` and `∀ p ∈ s.prot, p ∈ s.wit` (boolean checker `wfB s`). Protection-within-retention is preserved by `step` (`protSubWit_step`) and by replay from genesis (`protSubWit_replay`). Liveness is an additional hypothesis of `wf_of_replay`; `.halt` exits the class (`halt_leaves_class` in the book). `WFClass` does not check endpoint bounds or distinctness (`class_does_not_check_bounds`).
   - On `outsideClass` (`prot = [(0, 1)]`, `wit = []`, `obs = some []`), `wfB outsideClass = false`, and accepting `.admitWit 0 1` creates an active obstruction (`coarse (obstEffect outsideClass (step outsideClass (.admitWit 0 1))) = .creates`, theorem `retention_creates_outside_class`), which no accepted `.admitWit` inside `WFClass` can ever do.

5. **The thirteen `EffectClass` codes and twelve `EffectSig` values (Sections 5–6, lines 1332–1670):**
   - `EffectClass` has 13 constructors: nine constructors of `PEvent` contribute one class each (`supplyOccurrence`, `assertDifference`, `retainDifference`, `refineObservation`, `extendObservation`, `recordRefusal`, `writeBudget`, `writeLicense`, `absorbTerminal`), while `.protect` splits into `protectQuiet` vs. `protectObstructing` and `.declareObs` splits into `declareQuiet` vs. `declareObstructing` (`9 + 2 + 2 = 13`).
   - For every `s` with `WFClass s` and every `e` with `Accepted s e = true`, `sig_eq_classSig` establishes `sigOf s e = classSig (classOf s e)`, and `classSig_inj` + `exists_unique_class` prove that this class is unique.
   - `declared_codebook_size` establishes `(dedup (allClasses.map classSig)).length = 13`, and `guard_erased_codebook_size` establishes `(dedup (allClasses.map (fun k => eraseGuard (classSig k)))).length = 12`, because `.refineObservation` and `.extendObservation` share `⟨fdObsBudget, .removes, .continuation, .internal⟩` (`refine_addCol_effect_merge`).
   - **Audit note on ledger `CL-PD2-TRANSITION-CODEBOOK`:** The ledger sentence "Erasing the guard leaves twelve declared code values (`declared_codebook_size`, `guard_erased_codebook_size`)" cites both the 13-value theorem and the 12-value theorem next to the number 12; `declared_codebook_size` is the 13-code count before guard erasure, and `guard_erased_codebook_size` is the 12-code count after guard erasure.

6. **Why the thirteen codes are not a composable alphabet (Sections 6–9, lines 1628–1893):**
   - **Right congruence fails (`classSig_not_right_congruent_occurrence`, `classSig_not_right_congruent_budget`):** Equal `sigOf` codes at the same start state can be separated by a single follow-up event.
   - **Guard erasure merges distinct acceptance domains (`refine_addCol_domain_countermodel`):** `.refineCol` does not check `s.licensed`, so on `wRefineUnlicensed` (`licensed = false`), `.refineCol [] 0` is accepted while on `wFundedUnlicensed` (`licensed = false`), `.addCol [0]` is refused.
   - **Dropped components are pre-state sensitive (`preserved_untouched_not_invariant`, `budgetDelta_not_invariant`), with two scoped invariants (`budgetDelta_of_funded_guard`, `refuse_preserves`).**
   - **`Origin` is not causal provenance (`internal_family_emits_budget_write`, `env_ownership_claim_refuted`, `internal_family_env_only_unit_funding`):** `nextFamilyP` never emits `admitOcc`, `setLicense`, or `halt`, but every extension block `[.setBudget 1, .addCol c]` begins with `.setBudget 1`, which carries `Origin.environment`.
   - **Audit note on Section 9 witness sizes (`class_witness_sizes`):** Section 9 is titled "One minimum witness per class", while its docstring (lines 1840–1848) notes that the Lean witnesses (`genesisP`, `wAssert`, ..., `wRefine`) are required to be **store-coherent** (`wit ⊆ asserted`, `prot ⊆ wit`, in-bounds positions), giving `sizeP wRefine = 8` and `sizeP wFunded = 7`; the Python mirror searches all 6,144 states of `WFClass` in the bounded pool and finds smaller witnesses that omit the extra store-coherence conditions outside `prot ⊆ wit`.

---

## Plain-language interpretation

When a live well-formed ledger `s` (`WFClass s`) accepts an event `e`, we can summarize the transition `s ↦ step s e` by five items (`ClassSig`):
1. Which of the 9 fields of `PState` changed (`FieldDelta`)?
2. Which constructor's guard was checked (`GuardKind`)?
3. Did the set of obstructed pairs gain pairs (`.creates`), lose pairs (`.removes`), or stay the same (`.inert`) (`ObstMove`)?
4. Did the ledger remain live (`.continuation`) or halt (`.absorption`) (`Continuity`)?
5. Is the constructor labeled `.environment` or `.internal` (`Origin`)?

Across all 11 event constructors and all well-formed states, every accepted step lands in **exactly one of 13 classes** (`exists_unique_class`, `declared_codebook_size`). Nine constructors always produce the same class whenever accepted; `.protect i j` splits into two classes (`protectObstructing` if `(i, j)` is immediately obstructed in `protS s i j`, `protectQuiet` otherwise); and `.declareObs` splits into two classes (`declareObstructing` when `s.prot` is non-empty, `declareQuiet` when `s.prot = []`).

If we erase the constructor guard label (`eraseGuard`), `.refineObservation` and `.extendObservation` collapse into a single 4-tuple (`fdObsBudget`, `.removes`, `.continuation`, `.internal`), leaving **12** guard-erased signatures (`guard_erased_codebook_size`). That merge is an effect merge, not a domain merge: `.refineCol` does not check `s.licensed`, whereas `.addCol` requires `s.licensed = true` (`refine_addCol_domain_countermodel`).

Why are these 13 classes a **one-step codebook** rather than an **event alphabet**? Because replacing one accepted step by another with the same code does not preserve what happens on the next step:
- At `genesisP`, `.admitOcc 0` and `.admitOcc 2` both have code `.supplyOccurrence`, yet a follow-up `.admitOcc 0` is inert after the first and accepted after the second (`classSig_not_right_congruent_occurrence`).
- At `s = budS wObstructed 2` (budget `2`), `.setBudget 0` and `.setBudget 1` both have code `.writeBudget`, yet a follow-up `.addCol [0]` is refused after the first and accepted after the second (`classSig_not_right_congruent_budget`).

---

## Pseudocode

```text
ACCEPTED(s, e):
  return step(s, e) != s   -- equal to guardHolds(s, e)

CLASS_OF(s, e) -> EffectClass (13 values):
  match e:
    admitOcc _     -> return supplyOccurrence
    assertWit _ _  -> return assertDifference
    admitWit _ _   -> return retainDifference
    protect i j    -> return protectObstructing if obstP(protS(s,i,j), i, j) else protectQuiet
    declareObs     -> return declareObstructing if s.prot != [] else declareQuiet
    refineCol _ _  -> return refineObservation
    addCol _       -> return extendObservation
    refuse _ _     -> return recordRefusal
    setBudget _    -> return writeBudget
    setLicense _   -> return writeLicense
    halt           -> return absorbTerminal

SIG_OF(s, e) -> ClassSig:
  t := step(s, e)
  return (fieldDelta(s, t), guardOf(e), coarse(obstEffect(s, t)), continuityOf(t), originOf(e))
  -- Theorem sig_eq_classSig: if WFClass(s) and Accepted(s, e), then SIG_OF(s, e) == classSig(CLASS_OF(s, e))
```

---

## Python

From `code/derivation/transition_alphabet.py` (lines 52–90, 201–227, 299–314):

```python
def accepted(s: PS, e: PEvent) -> bool:
    """Lean ``Accepted``: the transition moves the represented state."""
    return pstep(s, e) != s


def guard_holds(s: PS, e: PEvent) -> bool:
    """Lean ``guardHolds``: the exact acceptance condition, constructor
    by constructor."""
    kind = e[0]
    if kind == "halt":
        return not s.halted
    if s.halted:
        return False
    if kind == "admitOcc":
        return cast(int, e[1]) not in s.occ
    if kind == "assertWit":
        i, j = cast(int, e[1]), cast(int, e[2])
        return wf_pair(s, i, j) and (i, j) not in s.asserted
    if kind == "admitWit":
        i, j = cast(int, e[1]), cast(int, e[2])
        return (wf_pair(s, i, j) and (i, j) in s.asserted
                and (i, j) not in s.wit)
    if kind == "protect":
        i, j = cast(int, e[1]), cast(int, e[2])
        return (i, j) in s.wit and (i, j) not in s.prot
    if kind == "declareObs":
        return s.obs is None
    if kind == "refineCol":
        return refine_ok(s, cast(Col, e[1]), cast(int, e[2])) and s.budget > 0
    if kind == "addCol":
        return col_ok(s, cast(Col, e[1])) and s.licensed and s.budget > 0
    if kind == "refuse":
        i, j = cast(int, e[1]), cast(int, e[2])
        return obst_p(s, i, j) and (i, j) not in s.refusals
    if kind == "setBudget":
        return cast(int, e[1]) != s.budget
    return cast(bool, e[1]) != s.licensed


def sig_of(s: PS, e: PEvent) -> Sig:
    """Lean ``sigOf``: the declared one-step profile projection."""
    t = pstep(s, e)
    kind = cast(str, e[0])
    return (field_delta(s, t), GUARD_OF[kind], COARSE[obst_effect(s, t)],
            continuity_of(t), ORIGIN_OF[kind])


def erase_guard(g: Sig) -> EffectSig:
    """Lean ``eraseGuard``."""
    return (g[0], g[2], g[3], g[4])


def wf_class(s: PS) -> bool:
    """Lean ``wfB`` / ``WFClass``: live, and protection contained in
    retention."""
    return (not s.halted) and all(p in s.wit for p in s.prot)


def class_of(s: PS, e: PEvent) -> str:
    """Lean ``classOf``."""
    kind = cast(str, e[0])
    if kind == "protect":
        i, j = cast(int, e[1]), cast(int, e[2])
        if obst_p(prot_s(s, i, j), i, j):
            return "protectObstructing"
        return "protectQuiet"
    if kind == "declareObs":
        if s.prot:
            return "declareObstructing"
        return "declareQuiet"
    return _SIMPLE_CLASS[kind]
```

---

## Line-by-line Python explanation

- **`accepted(s, e)` and `guard_holds(s, e)` (lines 52–90):** `accepted` checks `pstep(s, e) != s`; `guard_holds` evaluates the 11 constructor guards directly on `s`. Notice that `"refineCol"` checks `refine_ok(s, e[1], e[2]) and s.budget > 0` (without `s.licensed`), whereas `"addCol"` checks `col_ok(s, e[1]) and s.licensed and s.budget > 0`.
- **`sig_of(s, e)` and `erase_guard(g)` (lines 201–211):** `sig_of` computes the 5-tuple `(field_delta(s, t), GUARD_OF[kind], COARSE[obst_effect(s, t)], continuity_of(t), ORIGIN_OF[kind])`; `erase_guard` drops slot `1` (`GUARD_OF[kind]`).
- **`wf_class(s)` (lines 222–226):** Checks `(not s.halted) and all(p in s.wit for p in s.prot)`.
- **`class_of(s, e)` (lines 299–313):** Splits `"protect"` into `"protectObstructing"` vs. `"protectQuiet"` using `obst_p(prot_s(s, i, j), i, j)`, splits `"declareObs"` into `"declareObstructing"` vs. `"declareQuiet"` using `bool(s.prot)`, and maps the remaining 9 kinds via `_SIMPLE_CLASS`.

---

## Lean 4

From `lean4/Derivation/TransitionAlphabet.lean` (selected declarations and theorems across lines 75–1893):

```lean
namespace TransitionAlphabet

open PrimitivePassage

def Accepted (s : PState) (e : PEvent) : Bool :=
  decide (step s e ≠ s)

theorem accepted_eq_guardHolds (s : PState) (e : PEvent) :
    Accepted s e = guardHolds s e

structure ClassSig where
  fields : FieldDelta
  guard : GuardKind
  move : ObstMove
  cont : Continuity
  origin : Origin
deriving Repr, DecidableEq

structure EffectSig where
  fields : FieldDelta
  move : ObstMove
  cont : Continuity
  origin : Origin
deriving Repr, DecidableEq

def eraseGuard (g : ClassSig) : EffectSig :=
  ⟨g.fields, g.move, g.cont, g.origin⟩

structure WFClass (s : PState) : Prop where
  live : s.halted = false
  protSubWit : ∀ p ∈ s.prot, p ∈ s.wit

inductive EffectClass where
  | supplyOccurrence
  | assertDifference
  | retainDifference
  | protectQuiet
  | protectObstructing
  | declareQuiet
  | declareObstructing
  | refineObservation
  | extendObservation
  | recordRefusal
  | writeBudget
  | writeLicense
  | absorbTerminal
deriving Repr, DecidableEq

theorem sig_eq_classSig (s : PState) (hwf : WFClass s) (e : PEvent)
    (hacc : Accepted s e = true) : sigOf s e = classSig (classOf s e)

theorem exists_unique_class (s : PState) (hwf : WFClass s) (e : PEvent)
    (hacc : Accepted s e = true) :
    ∃ k : EffectClass,
      sigOf s e = classSig k ∧
      ∀ k' : EffectClass, sigOf s e = classSig k' → k' = k

theorem declared_codebook_size :
    (dedup (allClasses.map classSig)).length = 13 := by
  decide

theorem guard_erased_codebook_size :
    (dedup (allClasses.map (fun k => eraseGuard (classSig k)))).length = 12 := by
  decide

theorem classSig_not_right_congruent_occurrence :
    Accepted genesisP (.admitOcc 0) = true ∧
    Accepted genesisP (.admitOcc 2) = true ∧
    sigOf genesisP (.admitOcc 0) = sigOf genesisP (.admitOcc 2) ∧
    step (step genesisP (.admitOcc 0)) (.admitOcc 0) ≠
      step (step genesisP (.admitOcc 2)) (.admitOcc 0) := by
  decide

theorem classSig_not_right_congruent_budget :
    let s := budS wObstructed 2
    Accepted s (.setBudget 0) = true ∧
    Accepted s (.setBudget 1) = true ∧
    sigOf s (.setBudget 0) = sigOf s (.setBudget 1) ∧
    step (step s (.setBudget 0)) (.addCol [0]) ≠
      step (step s (.setBudget 1)) (.addCol [0]) := by
  decide

theorem refine_addCol_effect_merge (s₁ s₂ : PState) (hw₁ : WFClass s₁)
    (hw₂ : WFClass s₂) (v : List Nat) (p : Nat) (c : List Nat)
    (h₁ : Accepted s₁ (.refineCol v p) = true)
    (h₂ : Accepted s₂ (.addCol c) = true) :
    effectSigOf s₁ (.refineCol v p) = effectSigOf s₂ (.addCol c)

theorem refine_addCol_domain_countermodel :
    Accepted wRefineUnlicensed (.refineCol [] 0) = true ∧
    Accepted wFundedUnlicensed (.addCol [0]) = false ∧
    Accepted wFunded (.addCol [0]) = true := by decide

theorem retention_creates_outside_class :
    wfB outsideClass = false ∧
    Accepted outsideClass (.admitWit 0 1) = true ∧
    coarse (obstEffect outsideClass (step outsideClass (.admitWit 0 1)))
      = .creates := by decide

theorem env_ownership_claim_refuted :
    ∃ (s : PState) (b : List PEvent) (e : PEvent),
      b ∈ nextFamilyP s ∧ e ∈ b ∧ isEnvOwned e = true

theorem internal_family_env_only_unit_funding (s : PState) (b : List PEvent)
    (hb : b ∈ nextFamilyP s) (e : PEvent) (he : e ∈ b)
    (hen : isEnvOwned e = true) : e = PEvent.setBudget 1
```

---

## Line-by-line Lean explanation

1. **Acceptance and constructor equations (lines 75–365):**
   - `accepted_true_iff` (line 77), `accepted_false_iff` (line 81), `halted_accepts_nothing` (line 88), and `halt_inert_on_halted` (line 94) establish the basic properties of `Accepted`.
   - For each of the 11 constructors, `step_*_acc`, `step_*_inert`, `step_*_live`, and `step_*_eq` (lines 227–353) express `step s e` in terms of `guardHolds s e` and the named post-states `occS`..`haltS`, yielding `accepted_eq_guardHolds` (line 359).

2. **Obstruction deltas and `FieldDelta` (lines 595–1199):**
   - `obstEffect_split_of_inert` (line 666) shows that when `obstructedPairs t = obstructedPairs s`, `obstEffect s t` is `.untouched` if `obstructedPairs s = []` and `.preserved` otherwise; in both cases `coarse (obstEffect s t) = .inert` (`obstMove_inert_of_eq`, line 654).
   - `obstEffect_colS` (line 833) and `obstEffect_refineS` (line 916) prove that any accepted `.addCol` or `.refineCol` has `obstEffect = .removed` (because `colOk` and `refineOk` require at least one obstructed pair to be newly separated while breaking no existing separation).
   - `fieldDelta_occS`..`fieldDelta_colS` (lines 990–1054) compute the exact 9-boolean `FieldDelta` of each accepted constructor.

3. **Well-formedness and the 13-code partition (lines 1209–1622):**
   - `protSubWit_step` (line 1221) and `wf_of_replay` (line 1254) show that `WFClass` holds on every live state reachable from `genesisP`.
   - Why does `sig_eq_classSig` (line 1397) need `hwf : WFClass s`? Because when `.admitWit i j` is accepted, `obstructedPairs_witS` (line 723) establishes `obstructedPairs (witS s i j) = obstructedPairs s` using `hsub : ∀ p ∈ s.prot, p ∈ s.wit` (if `(i, j)` were already in `s.prot` without being in `s.wit`, as in `outsideClass`, then retaining `(i, j)` would newly activate `obstP` on `(i, j)`, as shown by `retention_creates_outside_class` at line 1755!).
   - `classSig_inj` (line 1580), `exists_unique_class` (line 1589), `declared_codebook_size` (line 1613), and `guard_erased_codebook_size` (line 1620) establish the 13-class bijection and its 12-signature guard-erased image.

4. **Non-congruence, non-invariance, and environment policy limits (lines 1628–1893):**
   - `classSig_not_right_congruent_occurrence` (line 1628) and `classSig_not_right_congruent_budget` (line 1640) exhibit the two suffix-separation countermodels.
   - `preserved_untouched_not_invariant` (line 1675) and `budgetDelta_not_invariant` (line 1685) show why `ObstEffect` and `BudgetDelta` had to be coarsened or dropped to form `ClassSig`, while `budgetDelta_of_funded_guard` (line 1692) and `refuse_preserves` (line 1734) isolate the two cases where those finer values are invariant.
   - `internal_family_no_occurrence_supply` (line 1775), `internal_family_no_license_write` (line 1780), `internal_family_no_terminal` (line 1785), `internal_family_emits_budget_write` (line 1794), `env_ownership_claim_refuted` (line 1798), `internal_family_env_only_unit_funding` (line 1807), and `nonEnv_preserves_occ_licensed` (line 1822) settle the exact boundary between `Origin.environment` and `nextFamilyP`.
   - `class_witnesses` (line 1855) and `class_witness_sizes` (line 1887) verify all 13 classes on the store-coherent witness states.

---

## What has been proved

- **Acceptance equals explicit guard (`accepted_eq_guardHolds`):** `step s e ≠ s` holds if and only if `guardHolds s e = true`.
- **Unique 13-code partition of accepted transitions on `WFClass` (`sig_eq_classSig`, `classSig_inj`, `exists_unique_class`, `declared_codebook_size`, `class_witnesses`):** Every accepted transition of a `WFClass` state realizes the `classSig` of a unique `EffectClass` constructor, and all 13 classes are realized.
- **Guard-erased 12-code collapse and domain separation (`guard_erased_codebook_size`, `refine_addCol_effect_merge`, `refine_addCol_domain_countermodel`):** Erasing `guard` merges `.refineObservation` and `.extendObservation` into one `EffectSig`, reducing 13 signatures to 12, while `wRefineUnlicensed` and `wFundedUnlicensed` separate their acceptance domains via `s.licensed`.
- **Failure of right congruence (`classSig_not_right_congruent_occurrence`, `classSig_not_right_congruent_budget`):** Equal `sigOf` signatures at a common pre-state do not imply equal post-step behavior under a common next event.
- **Load-bearing `WFClass` and scoped invariants (`wf_of_replay`, `retention_creates_outside_class`, `preserved_untouched_not_invariant`, `budgetDelta_not_invariant`, `budgetDelta_of_funded_guard`, `refuse_preserves`).**
- **Exact `Origin.environment` footprint in `nextFamilyP` (`env_ownership_claim_refuted`, `internal_family_env_only_unit_funding`, `nonEnv_preserves_occ_licensed`).**

---

## What has not been proved

- **No quotient transition system or event alphabet:** Because `sigOf s e` is not right-congruent, traces of `EffectClass` codes cannot be replayed without keeping the underlying `PState` and `PEvent` values.
- **Section 9 Lean witnesses are store-coherent, not unconstrained `WFClass` size minima:** As documented at lines 1840–1848 of `TransitionAlphabet.lean` and in `textbook/audit/modules/TransitionAlphabet.md`, `class_witness_sizes` records the sizes of the store-coherent Lean witnesses (`sizeP wRefine = 8`, `sizeP wFunded = 7`), whereas the Python 6,144-state scan over `WFClass` finds smaller witnesses that do not enforce `wit ⊆ asserted` or endpoint bounds.
- **`gainedPairs = []` for `colS` and `refineS` is an unstated corollary in `TransitionAlphabet.lean`:** The file establishes `obstructedPairs_colS_sub` and `obstructedPairs_refineS_sub` rather than stating `gainedPairs s (colS s cols c) = []` directly (proved in `textbook/checks/u65_lean.py`).

---

## Outside the system

1. **Metatheory types and quantifiers:**
   - The classifier types `FieldDelta`, `GuardKind`, `ObstEffect`, `ObstMove`, `BudgetDelta`, `Continuity`, `Origin`, `Profile`, `ClassSig`, `EffectSig`, `EffectClass`, and the all-quantifiers over `s : PState` and `e : PEvent` belong to the Lean metatheory.
2. **What the system itself holds:**
   - The ledger holds only the nine fields of `PState`; `sigOf s e` and `classOf s e` are metatheoretic comparisons between `s` and `step s e`.
3. **Admissions and their prices:**
   - All profile records, enums, `WFClass`, and `sizeP` are admitted definitions in `TransitionAlphabet.lean`.
4. **Phrases to read without importing outside structure:**
   - As the docstring at lines 1113–1122 states, `Origin.environment` vs. `Origin.internal` is a static 4-vs-7 tag on `PEvent` constructors (`isEnvOwned`), not an issuer capability or causal provenance record.

---

## Student exercise

Let `s = budS wObstructed 2` (so `s.occ = [0, 1]`, `s.asserted = s.wit = s.prot = [(0, 1)]`, `s.obs = some []`, `s.budget = 2`, `s.licensed = true`, `s.halted = false`).

1. Verify that `Accepted s (.setBudget 0) = true` and `Accepted s (.setBudget 1) = true`, and compute `classOf s (.setBudget 0)`, `classOf s (.setBudget 1)`, `budgetDeltaOf s (step s (.setBudget 0))`, and `budgetDeltaOf s (step s (.setBudget 1))`.
2. Why do `.setBudget 0` and `.setBudget 1` have the same `sigOf` at `s` even though their `budgetDeltaOf` values differ?
3. Compare `step (step s (.setBudget 0)) (.addCol [0])` and `step (step s (.setBudget 1)) (.addCol [0])`.

---

<details>
<summary>Student exercise answer</summary>

1. **Acceptance, `classOf`, and `budgetDeltaOf` at `s = budS wObstructed 2`:**
   - Since `s.halted = false` and `s.budget = 2`, both `0 ≠ 2` and `1 ≠ 2` hold, so `Accepted s (.setBudget 0) = true` and `Accepted s (.setBudget 1) = true`.
   - Both transitions map to `classOf = .writeBudget` with `sigOf = classSig .writeBudget = ⟨fdBudget, .budgetWrite, .inert, .continuation, .environment⟩`.
   - However, `budgetDeltaOf s (step s (.setBudget 0))` is `.rewritten` (since `0 + 1 ≠ 2`), whereas `budgetDeltaOf s (step s (.setBudget 1))` is `.spentOne` (since `1 + 1 = 2`).
2. **Why `sigOf` agrees:**
   - `ClassSig` drops the `budget : BudgetDelta` component of `Profile` (retaining only the boolean `fields.budget = true` inside `FieldDelta`), so both transitions project to the same 5-tuple `classSig .writeBudget`.
3. **Separation by the common suffix `.addCol [0]`:**
   - After `.setBudget 0`, the budget is `0`, so `.addCol [0]` fails `0 < budget` and returns `step s (.setBudget 0)` unchanged (`Accepted = false`).
   - After `.setBudget 1`, the budget is `1`, `licensed = true`, and `colOk` holds for `[0]`, so `.addCol [0]` is accepted (`Accepted = true`) and updates `obs` to `some [[0]]` and `budget` to `0` (`classSig_not_right_congruent_budget`).

---

</details>

## Verification

| Check | Source |
|---|---|
| Lean | `lean4/Derivation/TransitionAlphabet.lean` lines 75–1893 (`lake build Derivation.TransitionAlphabet`) |
| Axiom report | `artifacts/lean_axioms.txt` lines 889–1004 (100 `[propext, Quot.sound]`, 7 `[propext]`, 9 `none`) |
| Paper | `paper/paper_claim_ledger.md` `CL-PD2-TRANSITION-CODEBOOK`; `paper/paper_change_log.md` ("Goals 2 and 3", 2026-08-13) |
| Python | `code/derivation/transition_alphabet.py`, `code/run_transition_alphabet.py`, `tests/test_transition_alphabet.py`, `artifacts/transition_alphabet.json` |
| Audit | `textbook/audit/modules/TransitionAlphabet.md` (Section 9 store-coherent witness sizes vs. 6,144-state scan; implicit `gainedPairs = []` for `colS`/`refineS`; ledger citation note on `declared_codebook_size` vs. `guard_erased_codebook_size`) |
| Check (Python) | `python textbook/checks/u65_transition_alphabet.py` |
| Check (book Lean) | `python textbook/checks/u65_lean.py` |
