# Unit 62: What protection buys

| field | value |
|---|---|
| **Claim** | On the passage state machine (`PrimitivePassage.PState`, `step`, `replayP`), protected separation `protSep s i j = true` is sufficient for trace stability `TraceStableSep s i j` across every event replay (`protSep_trace_stable`, via `prot_mono`, `sep_preserved`, `protSep_persists`, `protSep_replays`). The converse over all `PState` (and over genesis-reachable `PState`) is false: on a halted state every replay is inert (`replay_halted`), so an unprotected separation is trace-stable (`halted_stable_not_protected`, `Textbook.U62.reachable_halted_stable_not_protected`). On a live unfunded state (`budget = 0`), an unprotected separation is stable over the syntactic fragment `RestrictedTrace` that omits `admitOcc`, `setBudget`, and `setLicense` (`unfunded_restricted_stable_not_protected`), but can be broken under the full grammar once `setBudget` funds a refinement (`Textbook.U62.reachable_unfunded_restricted_but_not_trace_stable`). Whenever a live funded state carries an accepted refinement witness that merges the pair on its separating column, that single step destroys `SepHere` (`separation_breakable`, instantiated at `sUnprot` by `unprotected_separation_unstable`). Whether `TraceStableSep` implies `protSep = true` on all live funded states is open (`openExactStabilityCharacterization : Prop`). On any declared state (`s.obs = some cols`), quiescence (`∀ i j, obstP s i j = false`) holds if and only if every retained protected pair is separated (`quiescent_iff_protected_separated`, `quiescence_is_protected_separation`), making every retained protected pair of a quiescent declared state trace-stable (`quiescent_retained_protected_trace_stable`). |
| **Mark** | `CONDITIONAL` for `sepP_append`, `sepP_refine`, `prot_mono`, `sep_preserved`, `protSep_persists`, `protSep_replays`, `protSep_trace_stable`, `trace_stable_restricted_stable`, `replay_halted`, `restricted_step_inert_unfunded`, `restricted_replay_inert_unfunded`, `separation_breakable`, `quiescent_iff_protected_separated`, `quiescence_is_protected_separation`, `quiescent_retained_protected_trace_stable`; `REFUTED` for the converse of sufficiency (`halted_stable_not_protected` and `Textbook.U62.reachable_halted_stable_not_protected`); `VERIFIED_FINITE` for `unfunded_restricted_stable_not_protected`, `unprotected_separation_unstable`, and `Textbook.U62.reachable_unfunded_restricted_but_not_trace_stable`; `OPEN` (`ADMITTED` as a `Prop` definition, unproved) for `openExactStabilityCharacterization`. |
| **Role** | Audit-repaired trace-stability and quiescence analysis on `PrimitivePassage` (`lean4/Derivation/StableContent.lean`, `code/derivation/stable_content.py`), superseding the withdrawn draft claim `CL-PD2-STABLE-CONTENT` with `CL-PD2-TRACE-STABILITY`. |
| **AuthorityEffect** | `None`. No state fields or transition rules are added to `PrimitivePassage.PState` or `PrimitivePassage.step`. |
| **Source** | `lean4/Derivation/StableContent.lean` (582 lines; 11 definitions, 18 theorems); `code/derivation/stable_content.py` (227 lines); `artifacts/primitive_passage.json` (`stable_content` section); `textbook/audit/modules/StableContent.md`; `textbook/audit/probes/F1/sc_reachable_witness.lean`. |
| **Axioms** | `[propext, Quot.sound]` on all 18 theorems in `StableContent` and both book theorems in `Textbook.U62`. |

---

## Question

In `PrimitivePassage` (Unit 51), a state `s : PState` with a declared observation `s.obs = some cols` separates two occurrence indices `(i, j)` when `sepP cols i j = true` (some column `c ∈ cols` contains `i` XOR `j`).

1. If `(i, j)` is currently separated at `s`, is that separation preserved after every finite event sequence `h : List PEvent` replayed via `replayP h s` (`TraceStableSep s i j`), and what role does membership `(i, j) ∈ s.prot` play?
2. Does `TraceStableSep s i j` imply that `(i, j)` is protected (`protSep s i j = true`), either across all `s : PState` or across genesis-reachable states?
3. How can an unprotected separation be destroyed by a single legal step, and what remains open between the sufficiency of `protSep` and single-step witness-borne destruction?

---

## What we already possess

From Unit 51 (`PrimitivePassage.lean`) and Unit 54 (`TransitionAlphabet.lean`):

- A passage state `s : PState` carries `occ : List Nat`, `asserted : List (Nat × Nat)`, `wit : List (Nat × Nat)`, `prot : List (Nat × Nat)`, `obs : Option (List (List Nat))`, `budget : Nat`, `licensed : Bool`, `refusals : List (Nat × Nat)`, and `halted : Bool`.
- Two indices `(i, j)` are separated by a column list `cols` when `sepP cols i j = cols.any (fun c => sepCol c i j)` is `true`.
- When `s.obs = some cols`, the refinement guard `refineOk s v p` requires both:
  1. some protected retained pair `(a, b) ∈ s.prot` is obstructed at `s` (`obstP s a b = true`) and becomes separated when `v` is replaced by `p :: v`, and
  2. **monotone protection preservation:** every protected pair `(a, b) ∈ s.prot` that is already separated by `cols` (`sepP cols a b = true`) remains separated after replacing every occurrence of `v` in `cols` by `p :: v`.
- On a halted state (`s.halted = true`), every event `e : PEvent` is a no-op (`step_halted : s.halted = true → step s e = s`).
- From Unit 54 (`TransitionAlphabet.internal_family_emits_budget_write`), the generated repair block `repairBlock` itself emits `.setBudget 1`, so excluding `.setBudget` is a syntactic filter on event lists rather than an internal/external ownership boundary.

---

## New concept

### 1. Protected separation, trace stability, and restricted stability (Lines 61–100)

`StableContent.lean` separates the static state predicate from the dynamic trace-quantified predicates:

- **Protected separation (`protSep s i j : Bool`):**
  $$\mathrm{protSep}(s, i, j) \iff (i, j) \in s.\mathrm{prot} \;\land\; \exists \mathrm{cols},\; s.\mathrm{obs} = \mathrm{some}\;\mathrm{cols} \;\land\; \mathrm{sepP}\;\mathrm{cols}\;i\;j = \mathrm{true}.$$
- **Current separation (`SepHere s i j : Prop`):** $\exists \mathrm{cols},\; s.\mathrm{obs} = \mathrm{some}\;\mathrm{cols} \land \mathrm{sepP}\;\mathrm{cols}\;i\;j = \mathrm{true}$.
- **Trace stability (`TraceStableSep s i j : Prop`):**
  $$\mathrm{TraceStableSep}(s, i, j) :\iff \forall h : \mathrm{List}\;\mathrm{PEvent},\; \mathrm{SepHere}(\mathrm{replayP}\;h\;s, i, j).$$
- **Restricted trace stability (`RestrictedStableSep s i j : Prop`):** Defines `IsTraceExcludedEvent : PEvent → Bool` to be `true` on `.admitOcc _`, `.setBudget _`, and `.setLicense _`, and `false` on the remaining 8 event constructors; `RestrictedTrace h` holds when `∀ e ∈ h, IsTraceExcludedEvent e = false`; and `RestrictedStableSep s i j` requires `SepHere (replayP h s) i j` for all `h` satisfying `RestrictedTrace h`.

### 2. Sufficiency: protected separation implies trace stability (Lines 103–291)

The sufficiency proof proceeds in five steps:

1. **`sepP_append`:** Appending a new column `c` to `cols` preserves `sepP cols i j = true` because `List.any` over `cols ++ [c]` is the boolean OR of `cols.any` and `[c].any`.
2. **`sepP_refine`:** If `s.obs = some cols`, `refineOk s v p = true`, `(i, j) ∈ s.prot`, and `sepP cols i j = true`, then the second conjunct of `refineOk` (`s.prot.all ...`) instantiated at `(i, j) ∈ s.prot` directly yields `sepP (cols.map (fun c => if c = v then p :: c else c)) i j = true`.
3. **`prot_mono`:** Every event constructor in `step s e` either leaves `s.prot` unchanged or appends `[(a, b)]` (in `.protect a b`), so `(i, j) ∈ s.prot → (i, j) ∈ (step s e).prot`.
4. **`sep_preserved`:** By 11-way case analysis on `e : PEvent`, if `s.obs = some cols`, `(i, j) ∈ s.prot`, and `sepP cols i j = true`, then `(step s e).obs` is some `cols'` with `sepP cols' i j = true` (using `sepP_refine` in the accepted `.refineCol` branch, `sepP_append` in the accepted `.addCol` branch, and `cols' = cols` in the remaining 9 branches).
5. **`protSep_persists` $\to$ `protSep_replays` $\to$ `protSep_trace_stable`:** Combining `prot_mono` and `sep_preserved` shows `protSep s i j = true → protSep (step s e) i j = true`, which inducts over any trace `h : List PEvent` to give `protSep_trace_stable`.

### 3. Why the converse is false, and the genesis-reachable repair (Lines 295–446)

Does `TraceStableSep s i j` imply `protSep s i j = true`? No:

- **Countermodel 1 (Halted absorption, `halted_stable_not_protected`):** On any state with `s.halted = true`, induction on `h` via `step_halted` proves `replay_halted : replayP h s = s`. Thus at
  $$s_{\mathrm{Halt}} = \{\mathrm{occ} = [0, 1],\; \mathrm{prot} = [],\; \mathrm{obs} = \mathrm{some}\;[[0]],\; \mathrm{halted} = \mathrm{true}, \dots\},$$
  the pair `(0, 1)` is separated by `[[0]]` after every replay (`TraceStableSep sHalt 0 1`), yet `(0, 1) ∉ sHalt.prot` (`protSep sHalt 0 1 = false`).
- **Countermodel 2 (Live unfunded restricted stability, `unfunded_restricted_stable_not_protected`):** On any state with `s.obs = some cols` and `s.budget = 0`, no event with `IsTraceExcludedEvent e = false` can change `obs` or `budget` (`restricted_step_inert_unfunded`, `restricted_replay_inert_unfunded`), because `.refineCol` and `.addCol` both require `0 < s.budget` while `.setBudget` is excluded. Thus at `sUnfunded` (identical to `sHalt` except `halted = false`), `RestrictedStableSep sUnfunded 0 1` holds while `protSep sUnfunded 0 1 = false`.

**Audit finding on reachability (`textbook/audit/modules/StableContent.md` §6, §8, and `textbook/audit/probes/F1/sc_reachable_witness.lean`):** Neither `sHalt` nor `sUnfunded` is reachable from `genesisP`: both have `prot = []` alongside a nonempty column `[0]`, whereas `colOk` and `refineOk` require a protected obstructed pair to create or refine a column, and `prot` never shrinks (`prot_mono`). Does the converse of `protSep_trace_stable` hold if we restrict to genesis-reachable states? Still no! Consider the 9-event history from `genesisP`:
$$\mathrm{histLive} = [\mathrm{admitOcc}\;0,\; \mathrm{admitOcc}\;1,\; \mathrm{admitOcc}\;2,\; \mathrm{assertWit}\;1\;2,\; \mathrm{admitWit}\;1\;2,\; \mathrm{protect}\;1\;2,\; \mathrm{declareObs},\; \mathrm{setBudget}\;1,\; \mathrm{addCol}\;[1]].$$
At $s_{\mathrm{live}} = \mathrm{replayP}\;\mathrm{histLive}\;\mathrm{genesisP}$, the protected obstructed pair `(1, 2)` legitimizes `addCol [1]` (spending the budget from $1$ to $0$). Column `[1]` separates `(1, 2)` (protected) *and* separates `(0, 1)` (unprotected, since $1 \in [1]$ and $0 \notin [1]$).

- Appending `.halt` gives a 10-event genesis-reachable halted state $s_{\mathrm{halt}} = \mathrm{replayP}\;\mathrm{histHalt}\;\mathrm{genesisP}$ where `TraceStableSep s_halt 0 1` holds and `protSep s_halt 0 1 = false` (`Textbook.U62.reachable_halted_stable_not_protected`).
- Leaving $s_{\mathrm{live}}$ unhalted gives a genesis-reachable live unfunded state where `RestrictedStableSep s_live 0 1` holds and `protSep s_live 0 1 = false`, yet `¬ TraceStableSep s_live 0 1` holds because the 5-event continuation
  $$\mathrm{breakTail} = [\mathrm{setBudget}\;1,\; \mathrm{assertWit}\;0\;2,\; \mathrm{admitWit}\;0\;2,\; \mathrm{protect}\;0\;2,\; \mathrm{refineCol}\;[1]\;0]$$
  refines `[[1]]` into `[[0, 1]]` (discharging the new protected obstruction `(0, 2)` while preserving `(1, 2)`), which contains both `0` and `1` and destroys the unprotected separation of `(0, 1)` (`Textbook.U62.reachable_unfunded_restricted_but_not_trace_stable`).

### 4. Witness-borne instability, the open gap, and quiescence (Lines 449–582)

- **Sufficiency of a breaking refinement (`separation_breakable` and `unprotected_separation_unstable`):** If `s.halted = false`, `s.obs = some cols`, `refineOk s v p = true`, `0 < s.budget`, and the refined column list `cols.map (fun c => if c = v then p :: c else c)` fails to separate `(i, j)`, then `¬ SepHere (step s (.refineCol v p)) i j`. At `sUnprot` (`occ = [0, 1, 2]`, `prot = [(1, 2)]`, `obs = some [[0]]`, `budget = 1`), `(0, 1)` is separated by `[[0]]` and unprotected, while `(1, 2)` is protected and obstructed (`neither 1 nor 2` lies in `[0]`). Stepping by `.refineCol [0] 1` produces `obs = some [[1, 0]]`, separating the protected pair `(1, 2)` and destroying the unprotected separation of `(0, 1)`.
- **Audit finding on the `separation_breakable` docstring (`textbook/audit/modules/StableContent.md` §11.1):** Module docstring item 4 (lines 30–33) and the docstring of `separation_breakable` (lines 449–452) state that an unprotected separation is destroyed "only when" / "exactly when" a concrete breaking refinement witness exists. In fact, the Lean theorem `separation_breakable` proves only the *sufficiency* of the breaking witness (given the 5 hypotheses, `¬ SepHere (step s (.refineCol v p)) i j`). As recorded in `paper/paper_change_log.md` (dated 2026-08-18), the claim ledger was narrowed to the sufficiency direction while the docstring prose in `StableContent.lean` remained unedited.
- **The open characterization (`openExactStabilityCharacterization`):** Whether every trace-stable separation on a live funded state is protected is recorded as an unproved `Prop` definition (lines 504–506):
  ```lean
  def openExactStabilityCharacterization : Prop :=
    ∀ (s : PState) (i j : Nat), s.halted = false → 0 < s.budget →
      SepHere s i j → TraceStableSep s i j → protSep s i j = true
  ```
- **Quiescence (`quiescent_iff_protected_separated`, `quiescence_is_protected_separation`, `quiescent_retained_protected_trace_stable`):** Defining `quiescentP s : Prop := ∀ i j, obstP s i j = false`, on any declared state `s.obs = some cols`, `quiescentP s` holds if and only if every pair `pr ∈ s.prot` with `pr ∈ s.wit` satisfies `sepP cols pr.1 pr.2 = true` (equivalently `protSep s pr.1 pr.2 = true`), and by `protSep_trace_stable` every such pair is trace-stable.

---

## Plain-language interpretation

When an observer column `c` separates two items `i` and `j` (putting one inside `c` and leaving the other outside `c`), a later `.refineCol` event can add the missing item to `c` in order to separate some third pair. If that happens, `i` and `j` end up on the same side of `c`, destroying their separation.

- **What protection buys (`protSep_trace_stable`):** Adding `(i, j)` to the protected store `s.prot` activates the veto inside `refineOk`: no `.refineCol` event is ever accepted if it would merge an already-separated pair in `s.prot`. Since `.addCol` only appends new columns and no other event alters existing columns, a separated pair in `s.prot` stays separated across every future sequence of events.
- **Why unprotected separation can fail (`unprotected_separation_unstable`):** If `(0, 1)` is separated by `[[0]]` but is *not* in `s.prot`, and `(1, 2)` *is* in `s.prot` and needs to be separated, the step `.refineCol [0] 1` is legal and funded: it expands `[0]` to `[1, 0]`, which separates `(1, 2)` while merging `(0, 1)`.
- **Why trace stability does not force protection (`halted_stable_not_protected`):** If the machine has already halted (`halted = true`), no future event can change `obs`, so even an unprotected separation is frozen forever—not because `refineOk` guards it, but because the whole machine is absorbed.

---

## Pseudocode

```text
function PROT_SEP(s, i, j):
    if s.obs is None:
        return False
    return ((i, j) in s.prot) and SEP_P(s.obs, i, j)

function IS_TRACE_EXCLUDED_EVENT(e):
    return e.kind in {"admitOcc", "setBudget", "setLicense"}

function QUIESCENT_P(s, n):
    for i in 0 .. n - 1:
        for j in 0 .. n - 1:
            if OBST_P(s, i, j):
                return False
    return True

# Reachable live-unfunded and halted countermodels from GENESIS_P:
HIST_LIVE = [
    admitOcc(0), admitOcc(1), admitOcc(2),
    assertWit(1, 2), admitWit(1, 2), protect(1, 2),
    declareObs, setBudget(1), addCol([1])
]
s_live = REPLAY_P(HIST_LIVE, GENESIS_P)   # obs = [[1]], prot = [(1, 2)], budget = 0
s_halt = STEP(s_live, halt)               # halted = True; (0, 1) is TraceStableSep, unprotected

# Breaking (0, 1) from s_live by leaving RestrictedTrace via setBudget(1):
BREAK_TAIL = [
    setBudget(1), assertWit(0, 2), admitWit(0, 2), protect(0, 2),
    refineCol([1], 0)
]
s_broken = REPLAY_P(BREAK_TAIL, s_live)   # obs = [[0, 1]]; (0, 1) no longer separated
```

---

## Python

From `code/derivation/stable_content.py` and `textbook/checks/u62_stable_content.py`:

```python
from derivation.primitive_passage import (
    GENESIS_P,
    PS,
    PEvent,
    obst_p,
    preplay,
    pstep,
    sep_p,
)


def prot_sep(s: PS, i: int, j: int) -> bool:
    """Protected separation: protected AND separated by the declared
    observation."""
    if s.obs is None:
        return False
    return (i, j) in s.prot and sep_p(s.obs, i, j)


def quiescent_p(s: PS, n: int) -> bool:
    """No pair below n is actively obstructed."""
    return all(not obst_p(s, i, j)
               for i in range(n) for j in range(n))


def is_trace_excluded_event(e: PEvent) -> bool:
    """Event forms omitted by the restricted trace fragment."""
    return e[0] in ("admitOcc", "setBudget", "setLicense")


def halted_countermodel() -> dict[str, object]:
    """Countermodel 1 to the converse: on an absorbed state every
    replay is inert, so an UNPROTECTED separation is trace stable."""
    s = PS(occ=(0, 1), obs=((0,),), halted=True)
    inert = all(pstep(s, e) == s for e in event_battery(2))
    assert s.obs is not None
    return {
        "separated": sep_p(s.obs, 0, 1),
        "not_protected": not prot_sep(s, 0, 1),
        "every_event_inert": inert,
        "trace_stable_but_unprotected": (
            inert and sep_p(s.obs, 0, 1) and not prot_sep(s, 0, 1)),
    }


def unprotected_unstable() -> dict[str, object]:
    """Witness-borne instability at sUnprot."""
    s = PS(occ=(0, 1, 2), asserted=((1, 2),), wit=((1, 2),),
           prot=((1, 2),), obs=((0,),), budget=1)
    t = pstep(s, ("refineCol", (0,), 1))
    assert s.obs is not None and t.obs is not None
    return {
        "before_separated_unprotected": sep_p(s.obs, 0, 1),
        "refinement_accepted": t != s,
        "after_broken_unprotected": not sep_p(t.obs, 0, 1),
        "protected_pair_now_separated": sep_p(t.obs, 1, 2),
        "protected_separation_intact": prot_sep(t, 1, 2),
    }
```

---

## Line-by-line Python explanation

- **`prot_sep(s, i, j)`:** Returns `False` when `s.obs is None` and otherwise checks `(i, j) in s.prot and sep_p(s.obs, i, j)`, mirroring `StableContent.protSep`.
- **`quiescent_p(s, n)`:** Checks `not obst_p(s, i, j)` for all `i, j in range(n)`, mirroring `StableContent.quiescentP` on a carrier bounded by `n`.
- **`is_trace_excluded_event(e)`:** Mirrors `StableContent.IsTraceExcludedEvent` by testing whether the event tag `e[0]` is one of `"admitOcc"`, `"setBudget"`, or `"setLicense"`.
- **`persistence_check(n)` and `replay_persistence_check(n, depth)`:** Test `protSep_persists` and `protSep_replays` across the 4 sample states `sample_states(3)` and all depth-2 traces (pruned to breadth 24) from `event_battery(3)`.
- **`halted_countermodel()`, `unfunded_countermodel()`, and `unprotected_unstable()`:** Mirror `halted_stable_not_protected` (`sHalt`), `unfunded_restricted_stable_not_protected` (`sUnfunded`), and `unprotected_separation_unstable` (`sUnprot`).
- **`exercise_reachable_witnesses()` (in `textbook/checks/u62_stable_content.py`):** Replays `hist_live` from `GENESIS_P` to construct the genesis-reachable live unfunded state `s_live` (`obs = ((1,),)`, `prot = ((1, 2),)`, `budget = 0`) and its halted successor `s_halt`, then replays `break_tail` from `s_live` to show that `.setBudget 1` followed by protecting `(0, 2)` and refining `(1,)` with `0` into `(0, 1)` destroys `sep_p(obs, 0, 1)` while preserving `prot_sep(s, 1, 2)`.

---

## Lean 4

From `lean4/Derivation/StableContent.lean` and `textbook/checks/u62_lean.py`:

```lean
namespace StableContent

open PrimitivePassage

def protSep (s : PState) (i j : Nat) : Bool :=
  (decide ((i, j) ∈ s.prot))
    && (match s.obs with
        | none => false
        | some cols => sepP cols i j)

def SepHere (s : PState) (i j : Nat) : Prop :=
  ∃ cols, s.obs = some cols ∧ sepP cols i j = true

def TraceStableSep (s : PState) (i j : Nat) : Prop :=
  ∀ h : List PEvent, SepHere (replayP h s) i j

theorem sepP_refine (s : PState) (cols : List (List Nat))
    (v : List Nat) (p : Nat) (i j : Nat)
    (hobs : s.obs = some cols) (hro : refineOk s v p = true)
    (hp : (i, j) ∈ s.prot) (hsep : sepP cols i j = true) :
    sepP (cols.map (fun c => if c = v then p :: c else c)) i j
      = true := by
  unfold refineOk at hro
  rw [hobs] at hro
  simp only [Bool.and_eq_true] at hro
  have hall := hro.2
  rw [List.all_eq_true] at hall
  have hthis := hall (i, j) hp
  rw [hsep] at hthis
  simp only [Bool.not_true, Bool.false_or] at hthis
  exact hthis

theorem protSep_trace_stable (s : PState) (i j : Nat)
    (h : protSep s i j = true) : TraceStableSep s i j := by
  intro tr
  have hrep := protSep_replays tr s i j h
  unfold protSep at hrep
  simp only [Bool.and_eq_true] at hrep
  cases hobs : (replayP tr s).obs with
  | none =>
      exfalso
      have := hrep.2
      rw [hobs] at this
      exact Bool.noConfusion this
  | some cols =>
      refine ⟨cols, hobs, ?_⟩
      have := hrep.2
      rw [hobs] at this
      exact this

theorem halted_stable_not_protected :
    TraceStableSep sHalt 0 1 ∧ protSep sHalt 0 1 = false := by
  constructor
  · intro tr
    rw [replay_halted tr sHalt rfl]
    exact ⟨[[0]], rfl, by decide⟩
  · decide

theorem separation_breakable (s : PState) (cols : List (List Nat))
    (v : List Nat) (p : Nat) (i j : Nat)
    (hh : s.halted = false) (hobs : s.obs = some cols)
    (hro : refineOk s v p = true) (hfund : 0 < s.budget)
    (hbroken :
      sepP (cols.map (fun c => if c = v then p :: c else c)) i j
        = false) :
    ¬ SepHere (step s (.refineCol v p)) i j := by
  intro hsep
  obtain ⟨cols', hobs', hsep'⟩ := hsep
  have hstep : (step s (.refineCol v p)).obs
      = some (cols.map (fun c => if c = v then p :: c else c)) := by
    simp only [step, hh]
    rw [if_neg (fun hc : false = true => Bool.noConfusion hc),
        if_pos (by
          rw [hro, decide_eq_true hfund]
          rfl),
        hobs]
  rw [hstep] at hobs'
  have : cols' = cols.map (fun c => if c = v then p :: c else c) :=
    Option.some.inj hobs'.symm
  rw [this, hbroken] at hsep'
  exact Bool.noConfusion hsep'

def openExactStabilityCharacterization : Prop :=
  ∀ (s : PState) (i j : Nat), s.halted = false → 0 < s.budget →
    SepHere s i j → TraceStableSep s i j → protSep s i j = true

def quiescentP (s : PState) : Prop := ∀ i j, obstP s i j = false

theorem quiescent_iff_protected_separated (s : PState)
    (cols : List (List Nat)) (hobs : s.obs = some cols) :
    quiescentP s ↔
      (∀ pr, pr ∈ s.prot → pr ∈ s.wit →
        sepP cols pr.1 pr.2 = true) := by
  constructor
  · intro hq pr hp hw
    obtain ⟨a, b⟩ := pr
    have h := hq a b
    rw [obst_agrees_when_declared s cols hobs] at h
    rw [decide_eq_true hw, decide_eq_true hp] at h
    simp only [Bool.true_and] at h
    cases hb : sepP cols a b with
    | true => rfl
    | false =>
        exfalso
        unfold zeroP at h
        rw [hb] at h
        exact Bool.noConfusion h
  · intro hs i j
    rw [obst_agrees_when_declared s cols hobs]
    by_cases hw : (i, j) ∈ s.wit
    · by_cases hp : (i, j) ∈ s.prot
      · have hsep := hs (i, j) hp hw
        unfold zeroP
        rw [decide_eq_true hw, decide_eq_true hp, hsep]
        rfl
      · rw [decide_eq_false hp]
        simp
    · rw [decide_eq_false hw]
      simp

end StableContent
```

And the genesis-reachable countermodels in `textbook/checks/u62_lean.py` (`namespace Textbook.U62`):

```lean
namespace Textbook.U62

open PrimitivePassage StableContent

def histLive : List PEvent :=
  [.admitOcc 0, .admitOcc 1, .admitOcc 2,
   .assertWit 1 2, .admitWit 1 2, .protect 1 2,
   .declareObs, .setBudget 1, .addCol [1]]

def histHalt : List PEvent := histLive ++ [.halt]

def breakTail : List PEvent :=
  [.setBudget 1, .assertWit 0 2, .admitWit 0 2, .protect 0 2,
   .refineCol [1] 0]

theorem reachable_halted_stable_not_protected :
    TraceStableSep (replayP histHalt genesisP) 0 1 ∧
      protSep (replayP histHalt genesisP) 0 1 = false ∧
      protSep (replayP histHalt genesisP) 1 2 = true := by
  refine ⟨?_, by decide, by decide⟩
  intro tr
  rw [replay_halted tr (replayP histHalt genesisP) (by decide)]
  exact ⟨[[1]], by decide, by decide⟩

theorem reachable_unfunded_restricted_but_not_trace_stable :
    RestrictedStableSep (replayP histLive genesisP) 0 1 ∧
      protSep (replayP histLive genesisP) 0 1 = false ∧
      (replayP histLive genesisP).halted = false ∧
      ¬ TraceStableSep (replayP histLive genesisP) 0 1 := by
  refine ⟨?_, by decide, by decide, ?_⟩
  · intro tr hint
    obtain ⟨ho, _⟩ :=
      restricted_replay_inert_unfunded tr (replayP histLive genesisP) [[1]]
        hint (by decide) (by decide)
    exact ⟨[[1]], ho, by decide⟩
  · intro hts
    obtain ⟨cols, hobs, hsep⟩ := hts breakTail
    have hobs_actual :
        (replayP breakTail (replayP histLive genesisP)).obs = some [[0, 1]] := by
      decide
    rw [hobs_actual] at hobs
    have hcols : cols = [[0, 1]] := Option.some.inj hobs.symm
    rw [hcols] at hsep
    exact absurd hsep (by decide)

end Textbook.U62
```

---

## Line-by-line Lean explanation

- **`sepP_refine`:** Unfolds `refineOk` at `s.obs = some cols`, extracts the second conjunct `s.prot.all (...) = true`, applies `List.all_eq_true` at `(i, j) ∈ s.prot`, and substitutes `sepP cols i j = true` (`!true || sepP ... = true`) to conclude that the mapped columns still separate `(i, j)`.
- **`sep_preserved`, `protSep_persists`, `protSep_replays`, `protSep_trace_stable`:** `sep_preserved` performs a case split over all 11 constructors of `PEvent`. In `.refineCol v p`, when the guard `refineOk s v p && decide (0 < s.budget)` succeeds, `sepP_refine` supplies the post-step separation; in `.addCol c`, when the guard succeeds, `sepP_append` supplies it; in all other cases `s.obs` is unchanged. `protSep_persists` pairs `prot_mono` with `sep_preserved`, `protSep_replays` inducts on the trace `h`, and `protSep_trace_stable` extracts `SepHere` after `replayP tr s`.
- **`replay_halted` and `halted_stable_not_protected`:** `replay_halted` inducts on `h : List PEvent` using `step_halted`. At `sHalt`, `replay_halted` reduces `replayP tr sHalt` to `sHalt`, where `sHalt.obs = some [[0]]` and `sepP [[0]] 0 1 = true` by `decide`.
- **`separation_breakable` and `unprotected_separation_unstable`:** `separation_breakable` unfolds `step s (.refineCol v p)` under `hh : s.halted = false`, `hro : refineOk s v p = true`, `hfund : 0 < s.budget`, and `hobs : s.obs = some cols` to identify the post-step columns with `cols.map (fun c => if c = v then p :: c else c)`, where `hbroken` contradicts `sepP cols' i j = true`. `unprotected_separation_unstable` discharges all 6 conjuncts at `sUnprot` by `decide`.
- **`openExactStabilityCharacterization`:** Defined as a `Prop` (`∀ s i j, s.halted = false → 0 < s.budget → SepHere s i j → TraceStableSep s i j → protSep s i j = true`) with no proof term.
- **`quiescent_iff_protected_separated`:** Rewrites `obstP s a b` on a declared state via `obst_agrees_when_declared s cols hobs` to `decide ((a, b) ∈ s.wit) && decide ((a, b) ∈ s.prot) && zeroP cols a b`, where `zeroP cols a b = !sepP cols a b`. Thus `obstP s a b = false` for all `(a, b)` if and only if every `(a, b)` in both `s.prot` and `s.wit` has `sepP cols a b = true`.
- **`Textbook.U62.reachable_halted_stable_not_protected` and `reachable_unfunded_restricted_but_not_trace_stable`:** Replace the non-reachable states `sHalt` and `sUnfunded` by the genesis-reachable states `replayP histHalt genesisP` and `replayP histLive genesisP`, and refute `TraceStableSep (replayP histLive genesisP) 0 1` by evaluating `replayP breakTail (replayP histLive genesisP)` via `decide`.

---

## What has been proved

1. **Sufficiency of protected separation (`protSep_trace_stable`):** If `protSep s i j = true`, then `(i, j)` remains separated after every finite replay `h : List PEvent` (`TraceStableSep s i j`).
2. **Refutation of the converse (`halted_stable_not_protected` and `Textbook.U62.reachable_halted_stable_not_protected`):** Both on the literal state `sHalt` and on the 10-event genesis-reachable state `replayP histHalt genesisP`, the pair `(0, 1)` is `TraceStableSep` while `protSep _ 0 1 = false`.
3. **Restricted-fragment stability on unfunded states (`unfunded_restricted_stable_not_protected` and `Textbook.U62.reachable_unfunded_restricted_but_not_trace_stable`):** On a live state with `s.obs = some cols` and `s.budget = 0`, no event outside `{admitOcc, setBudget, setLicense}` alters `obs` or `budget`, so an unprotected separation is `RestrictedStableSep`. On the genesis-reachable state `replayP histLive genesisP`, `(0, 1)` is `RestrictedStableSep` yet *not* `TraceStableSep` (broken by `breakTail`).
4. **Sufficiency of a breaking refinement witness (`separation_breakable`, `unprotected_separation_unstable`):** A single funded, accepted `.refineCol v p` step that merges `(i, j)` on its separating column destroys `SepHere`.
5. **Quiescence characterization (`quiescent_iff_protected_separated`, `quiescence_is_protected_separation`, `quiescent_retained_protected_trace_stable`):** On a declared state `s.obs = some cols`, no pair is obstructed (`quiescentP s`) if and only if every pair in `s.prot ∩ s.wit` is separated by `cols` (and hence `protSep = true` and `TraceStableSep`).

---

## What has not been proved

1. **`openExactStabilityCharacterization` (OPEN):** Whether `TraceStableSep s i j` implies `protSep s i j = true` on all live (`s.halted = false`), funded (`0 < s.budget`) states with `SepHere s i j` is unproved and recorded explicitly as `openExactStabilityCharacterization : Prop`.
2. **Necessity of the single-step breaking witness in `separation_breakable`:** Despite the "only when" / "exactly when" phrasing in module docstring item 4 and the docstring of `separation_breakable` (audited as an interpretation defect in `textbook/audit/modules/StableContent.md` §11.1 and noted in `paper/paper_change_log.md` on 2026-08-18), `separation_breakable` proves only that the 5 witness hypotheses *suffice* to destroy `SepHere` in one `.refineCol` step; it does not prove that every failure of `TraceStableSep` arises from such a witness.
3. **Any ownership semantics for `IsTraceExcludedEvent`:** Excluding `admitOcc`, `setBudget`, and `setLicense` is a syntactic predicate on `PEvent`; as proved in `TransitionAlphabet.internal_family_emits_budget_write` (Unit 54), the internal repair block itself emits `setBudget`.

---

## Outside the system

- **Metatheoretic universal quantification in `TraceStableSep`, `RestrictedStableSep`, and `quiescentP`:** `TraceStableSep s i j` quantifies `∀ h : List PEvent` over the infinite type of all finite event lists, and `quiescentP s` quantifies `∀ i j : Nat` over all pairs of natural numbers (though `obstP s i j` is `false` outside the finite list `s.wit`).
- **Python finite battery bounds (`stable_content_report(3)`):** The Python mirror `code/derivation/stable_content.py` checks single-step persistence and depth-2, breadth-24 replay persistence over a 49-event battery on 4 sample states at carrier size `n = 3`. The unconditional universal statements over all `s : PState` and `h : List PEvent` are the Lean theorems.

---

## Student exercise

Consider the 9-event genesis-reachable live state $s_{\mathrm{live}} = \mathrm{replayP}\;\mathrm{histLive}\;\mathrm{genesisP}$ where
$$\mathrm{histLive} = [\mathrm{admitOcc}\;0,\; \mathrm{admitOcc}\;1,\; \mathrm{admitOcc}\;2,\; \mathrm{assertWit}\;1\;2,\; \mathrm{admitWit}\;1\;2,\; \mathrm{protect}\;1\;2,\; \mathrm{declareObs},\; \mathrm{setBudget}\;1,\; \mathrm{addCol}\;[1]].$$

1. Write down all 9 fields of $s_{\mathrm{live}}$, and check `sepP`, `protSep`, and `obstP` at $s_{\mathrm{live}}$ for the pairs $(0, 1)$, $(1, 2)$, and $(0, 2)$. Is $s_{\mathrm{live}}$ quiescent (`quiescentP`)?
2. Explain why neither `.addCol [0]` nor `.refineCol [1] 0` changes $s_{\mathrm{live}}$ directly, and why every event $e$ with `IsTraceExcludedEvent e = false` leaves $s_{\mathrm{live}}.\mathrm{obs} = \mathrm{some}\;[[1]]$ and $s_{\mathrm{live}}.\mathrm{budget} = 0$.
3. Trace the 5-event continuation
   $$\mathrm{breakTail} = [\mathrm{setBudget}\;1,\; \mathrm{assertWit}\;0\;2,\; \mathrm{admitWit}\;0\;2,\; \mathrm{protect}\;0\;2,\; \mathrm{refineCol}\;[1]\;0]$$
   from $s_{\mathrm{live}}$. Verify that all 5 hypotheses of `separation_breakable` hold at the state immediately before `.refineCol [1] 0` for the pair $(i, j) = (0, 1)$, and check the post-step values of `sepP` and `protSep` on $(0, 1)$, $(1, 2)$, and $(0, 2)$.

---

## Answer

1. **Fields and pair status of $s_{\mathrm{live}} = \mathrm{replayP}\;\mathrm{histLive}\;\mathrm{genesisP}$:**
   - The 9 fields of $s_{\mathrm{live}}$ are:
     $$\mathrm{occ} = [0, 1, 2],\; \mathrm{asserted} = [(1, 2)],\; \mathrm{wit} = [(1, 2)],\; \mathrm{prot} = [(1, 2)],\; \mathrm{obs} = \mathrm{some}\;[[1]],\; \mathrm{budget} = 0,\; \mathrm{licensed} = \mathrm{true},\; \mathrm{refusals} = [],\; \mathrm{halted} = \mathrm{false}.$$
     (Note: `.addCol [1]` succeeded at step 9 because `(1, 2)` was in `wit ∩ prot` and obstructed under `obs = some []`, `1 ∈ occ`, `licensed = true`, and `budget = 1 > 0`, decrementing `budget` to $0$.)
   - Under `cols = [[1]]`:
     - Pair $(0, 1)$: $0 \notin [1]$ and $1 \in [1]$, so `sepP [[1]] 0 1 = true`. Since $(0, 1) \notin s_{\mathrm{live}}.\mathrm{prot}$, `protSep s_live 0 1 = false` and `obstP s_live 0 1 = false`.
     - Pair $(1, 2)$: $1 \in [1]$ and $2 \notin [1]$, so `sepP [[1]] 1 2 = true`. Since $(1, 2) \in s_{\mathrm{live}}.\mathrm{prot} \cap s_{\mathrm{live}}.\mathrm{wit}$, `protSep s_live 1 2 = true` and `obstP s_live 1 2 = false`.
     - Pair $(0, 2)$: $0 \notin [1]$ and $2 \notin [1]$, so `sepP [[1]] 0 2 = false`. Since $(0, 2) \notin s_{\mathrm{live}}.\mathrm{wit}$, `protSep s_live 0 2 = false` and `obstP s_live 0 2 = false`.
   - Because the only pair in `s_live.prot ∩ s_live.wit` is $(1, 2)$ and `sepP [[1]] 1 2 = true`, `quiescent_iff_protected_separated` confirms that `quiescentP s_live` holds.

2. **Inertness under `RestrictedTrace` at $s_{\mathrm{live}}$:**
   - Both `.addCol` and `.refineCol` are guarded by `decide (0 < s.budget)`. Since $s_{\mathrm{live}}.\mathrm{budget} = 0$, both guards evaluate to `false` and return $s_{\mathrm{live}}$ unchanged.
   - Among the remaining event constructors, `.declareObs` is a no-op when `s.obs = some [[1]]`, `.assertWit`, `.admitWit`, `.protect`, `.refuse`, and `.halt` never modify `obs` or `budget`, and `.admitOcc`, `.setBudget`, `.setLicense` have `IsTraceExcludedEvent e = true`. Thus `restricted_replay_inert_unfunded` guarantees `RestrictedStableSep s_live 0 1`.

3. **Tracing `breakTail` and checking the 5 hypotheses of `separation_breakable`:**
   - After the first 4 events `[.setBudget 1, .assertWit 0 2, .admitWit 0 2, .protect 0 2]` from $s_{\mathrm{live}}$, we reach a state $s_{\mathrm{pre}}$ with:
     $$\mathrm{occ} = [0, 1, 2],\; \mathrm{wit} = [(1, 2), (0, 2)],\; \mathrm{prot} = [(1, 2), (0, 2)],\; \mathrm{obs} = \mathrm{some}\;[[1]],\; \mathrm{budget} = 1,\; \mathrm{halted} = \mathrm{false}.$$
   - At $s_{\mathrm{pre}}$, for `cols = [[1]]`, `v = [1]`, `p = 0`, and `(i, j) = (0, 1)`, the 5 hypotheses of `separation_breakable` hold:
     1. `hh : s_pre.halted = false`.
     2. `hobs : s_pre.obs = some [[1]]`.
     3. `hro : refineOk s_pre [1] 0 = true`: `[1] ∈ [[1]]`, `0 ∈ s_pre.occ`, `0 ∉ [1]`, the protected pair `(0, 2) ∈ s_pre.prot` is obstructed under `[[1]]` (`obstP s_pre 0 2 = true`) and becomes separated by `0 :: [1] = [0, 1]` (`sepCol [0, 1] 0 2 = true`), and the only already-separated protected pair `(1, 2) ∈ s_pre.prot` remains separated under `[[0, 1]]` (`sepP [[0, 1]] 1 2 = true` since $1 \in [0, 1]$ and $2 \notin [0, 1]$).
     4. `hfund : 0 < s_pre.budget` ($0 < 1$).
     5. `hbroken : sepP [[0, 1]] 0 1 = false` (since both $0 \in [0, 1]$ and $1 \in [0, 1]$).
   - Stepping $s_{\mathrm{pre}}$ by `.refineCol [1] 0` produces $s_{\mathrm{broken}}$ with `obs = some [[0, 1]]` and `budget = 0`: the unprotected separation of $(0, 1)$ is destroyed (`sepP [[0, 1]] 0 1 = false`), while both protected pairs $(1, 2)$ and $(0, 2)$ satisfy `protSep = true` (`quiescentP s_broken` holds).

---

## Verification

Run both standalone verification scripts from the repository root:

```text
$ python textbook/checks/u62_stable_content.py
Unit 62 StableContent check: sufficiency_step=True; sufficiency_traces=True; quiescence_iff=True; reachable_live_obs=((1,),); broken_obs=((0, 1),); failures=[]

$ python textbook/checks/u62_lean.py
Unit 62 Lean check: exit=0; axiom reports as expected: 20 of 20; failures: []
```
