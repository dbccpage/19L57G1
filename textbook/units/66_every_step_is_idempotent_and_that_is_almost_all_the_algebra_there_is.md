# Unit 66. Every step is idempotent, and that is almost all the algebra there is

**Claim.** Repeating the same concrete passage event is idempotent. Different events may fail to commute, and the stated sound trace rewrites do not decide every replay equivalence.

**Status:** FROZEN (the step normal form, all-state idempotence, post-terminal absorption, typed-trace erasure, three frame commutation families, five non-commutation countermodels, non-environment trace invariance, refusal persistence, scoped vs. unscoped replay equivalence witnesses, and the sound/terminating/confluent/incomplete rewrite system `Rw`); ADMITTED (`TRecord`, `WFRecord`, `Aligned`, `LegalTrace`, `licenseInsensitive`, `budgetInsensitive`, `occInsensitive`, `ReplayEqvOn`, `RepresentsZero`, `Rw`, `RwStar`, `consNF`, `nf`, and `noRedex`); VERIFIED_FINITE (`artifacts/trace_algebra.json`).
**Lean:** `lean4/Derivation/TraceAlgebra.lean` lines 77–1001.
**Axioms:** `propext`, `Quot.sound` on 46 of 71 public theorem reports; `propext` on 11; `none` on 14 (`artifacts/lean_axioms.txt` lines 1005–1075).
**Depends on:** Unit 54 (`PrimitivePassage.PState`, `PEvent`, `step`, `replayP`, `genesisP`, `terminal_absorbing`), Unit 65 (`TransitionAlphabet.Accepted`, `guardHolds`, `accepted_eq_guardHolds`, `occS`..`haltS`, `step_*_acc`/`_inert`/`_live`/`_eq`, `isEnvOwned`, `nonEnv_preserves_occ_licensed`, `wAssert`, `wFunded`, `wObstructed`).

---

## First pass

Idempotent means that applying the same event twice has the same result as applying it once. It does not say that different events may be swapped.

Next compare short event lists. The declared duplicate-removal and post-halt rewrites preserve replay, but some equivalent histories still have different rewrite normal forms. Sound rewriting is weaker than a complete equivalence test.

## Detailed claim and formal anchors

Every single-step transition of `PrimitivePassage` decomposes into the guarded normal form `step s e = if guardHolds s e = true then postOf s e else s` (`step_eq_ite`); every event constructor is idempotent at every state (`step_idem : step (step s e) e = step s e`) and absorbed after `.halt` (`trace_absorbs`); erasing any `Aligned` chain of typed transition records `TRecord` to its event list reproduces its end state under `replayP` (`replay_erases`, `legal_trace_replays`); `.setLicense`, `.setBudget`, and `.admitOcc` commute with their respective insensitive event families (`comm_setLicense`, `comm_setBudget`, `comm_setBudget_setLicense`, `comm_admitOcc`) while failing to commute across five concrete countermodels (`noncomm_license_extension`, `noncomm_budget_extension`, `noncomm_terminal`, `noncomm_supply_retention`, `noncomm_same_store`); non-environment traces preserve `occ` and `licensed` (`internal_trace_preserves_occ`, `internal_trace_preserves_license`) and `.refuse` is append-only (`refusal_persists_replay`, `refusal_not_erasable`); and the two-rule event-list rewrite system `Rw` (`e :: e :: l → e :: l` and `.halt :: r :: l → [.halt]`) is sound at every start state, length-decreasing, and confluent with unique normal form `nf l`, yet incomplete for unscoped replay equivalence because `[.setBudget 1, .setBudget 2]` and `[.setBudget 2]` replay identically from every state while having distinct `nf` values (`TraceAlgebra.step_eq_ite`, `TraceAlgebra.inert_iff_guard_fails`, `TraceAlgebra.trace_absorbs`, `TraceAlgebra.step_idem`, `TraceAlgebra.replay_erases`, `TraceAlgebra.legal_trace_replays`, `TraceAlgebra.comm_setLicense`, `TraceAlgebra.comm_setBudget`, `TraceAlgebra.comm_setBudget_setLicense`, `TraceAlgebra.comm_admitOcc`, `TraceAlgebra.noncomm_license_extension`, `TraceAlgebra.noncomm_budget_extension`, `TraceAlgebra.noncomm_terminal`, `TraceAlgebra.noncomm_supply_retention`, `TraceAlgebra.noncomm_same_store`, `TraceAlgebra.same_store_observationally_equal`, `TraceAlgebra.internal_trace_preserves_occ`, `TraceAlgebra.internal_trace_preserves_license`, `TraceAlgebra.internal_blocks_cannot_supply_or_license`, `TraceAlgebra.refusal_persists_replay`, `TraceAlgebra.refusal_not_erasable`, `TraceAlgebra.replay_eqv_scoped`, `TraceAlgebra.replay_eqv_not_unscoped`, `TraceAlgebra.rw_sound`, `TraceAlgebra.rw_length`, `TraceAlgebra.rw_confluent`, `TraceAlgebra.nf_unique`, `TraceAlgebra.nf_sound`, `TraceAlgebra.rewrite_not_complete`).

## Question

Unit 65 showed that single-step transitions `(s, e)` cannot be quotiented into a state-independent event alphabet. What algebraic laws **do** hold on finite event traces `l : List PEvent` under `replayP`? Specifically:
1. Is every event idempotent (`step (step s e) e = step s e`), even `.refineCol` and `.addCol` which spend budget?
2. Which pairs of events commute at every state, and why do disjoint write targets fail to ensure commutation?
3. If we orient adjacent idempotence (`e :: e :: l → e :: l`) and post-terminal absorption (`.halt :: r :: l → [.halt]`) into a rewrite system on event lists, is it sound, terminating, and confluent—and does it capture all state-independent replay equivalences?

---

## What we already possess

From Unit 54 (`lean4/Derivation/PrimitivePassage.lean`), we have `PState`, `PEvent`, `step`, `replayP`, `genesisP`, and `terminal_absorbing : step (step s .halt) e = step s .halt`.

From Unit 65 (`lean4/Derivation/TransitionAlphabet.lean`), we have `Accepted s e`, `guardHolds s e`, `accepted_eq_guardHolds : Accepted s e = guardHolds s e`, the eleven named post-state constructors `occS`..`haltS` and their acceptance/inertness equations `step_*_acc`/`_inert`/`_live`/`_eq`, the environment policy tag `isEnvOwned`, `nonEnv_preserves_occ_licensed`, and the concrete witness states `wAssert`, `wFunded`, and `wObstructed`.

---

## New concept: step normal form, all-state idempotence, frame commutation, and the two-rule trace normalizer

`TraceAlgebra` establishes eight results on `step` and `replayP`:

1. **The step normal form (Section 1, lines 77–176):**
   - `postOf (s : PState) : PEvent → PState` bundles the eleven named post-state constructors `occS`..`haltS` into a single function.
   - `step_eq_ite` (line 108) establishes `step s e = if guardHolds s e = true then postOf s e else s`, and `inert_iff_guard_fails` (line 181) establishes `step s e = s ↔ guardHolds s e = false`.

2. **All-state idempotence and terminal absorption (Section 2, lines 181–352):**
   - `terminal_absorbs`, `replayP_halted`, and `trace_absorbs` (`replayP (.halt :: l) s = step s .halt`) lift `step_halted` to traces.
   - `guardHolds_post_false` (line 251) establishes that for **every** event `e` and state `s`, if `Accepted s e = true`, then `guardHolds (step s e) e = false`. Why does this hold even for the two funded events `.refineCol v p` and `.addCol c` (even when `s.budget ≥ 2`)?
     - After `.refineCol v p`, the column `v` in `cols` has been replaced by `p :: v`, which is one element longer; `v_not_mem_map` (line 223) establishes `v ∉ cols.map (fun c => if c = v then p :: c else c)`, so `refineOk` is `false` on the second attempt (`refineOk_false_of_not_mem`)!
     - After `.addCol c`, `c` belongs to `cols ++ [c]` (`mem_append_singleton`), so `colOk` is `false` on the second attempt (`colOk_false_of_mem`)!
   - Combining `Accepted s e = false` (where `step s e = s`) and `Accepted s e = true` (where `guardHolds (step s e) e = false`) yields `step_idem (s : PState) (e : PEvent) : step (step s e) e = step s e` (line 336).

3. **Typed transition records and legal traces (Section 3, lines 355–410):**
   - `TRecord` packages `(pre, ev, guard, post, cls, spend, profile)`; `WFRecord r` asserts that all fields match those computed from `(r.pre, r.ev)` with `Accepted r.pre r.ev = true` and `WFClass r.pre`; `Aligned s tr` chains `r.pre = s` and `r.post = step r.pre r.ev`.
   - `replay_erases` (line 396) establishes `Aligned s tr → replayP (eraseTrace tr) s = endState s tr`, and `legal_trace_replays` (line 406) applies `replay_erases` to `h.1 : Aligned s tr`.
   - **Audit note on `TRecord` and ledger `CL-PD2-TRACE-ALGEBRA`:** The ledger entry `CL-PD2-TRACE-ALGEBRA` states that a typed transition record binds `pre`, `ev`, `guard`, `post`, `cls`, `spend`, and `profile`, and continues "From there the laws are DERIVED." In `TraceAlgebra.lean`, no theorem ever reads `r.cls`, `r.spend`, or `r.profile`, and `legal_trace_replays` drops `h.2 : ∀ r ∈ tr, WFRecord r` and calls `replay_erases tr s h.1`. The algebraic laws in Sections 2 and 4–8 are proved directly from `step_eq_ite` and `guardHolds` on `PState` and `PEvent`.

4. **Three frame commutation families and five countermodels (Section 4, lines 425–660):**
   - Because guards read fields they do not write, disjoint write targets do not commute in general. Instead, `TraceAlgebra` defines three boolean insensitivity predicates:
     - `licenseInsensitive e` (true on all constructors except `addCol`, `setLicense`, `halt`) → `comm_setLicense`;
     - `budgetInsensitive e` (true on all except `refineCol`, `addCol`, `setBudget`, `halt`) → `comm_setBudget` (and `comm_setBudget_setLicense`);
     - `occInsensitive e` (true on `protect`, `declareObs`, `refuse`, `setBudget`, `setLicense`) → `comm_admitOcc`.
   - Five countermodels prove non-commutation when a guard reads a written field or when two events append to the same list store: `noncomm_license_extension`, `noncomm_budget_extension`, `noncomm_terminal`, `noncomm_supply_retention`, and `noncomm_same_store` (`.assertWit 0 1` vs. `.assertWit 1 0` on `wAssert`).
   - **Audit note on `same_store_observationally_equal` (line 652):** After `.assertWit 0 1` then `.assertWit 1 0` vs. the reverse order on `wAssert`, the `.asserted` lists are `[(0, 1), (1, 0)]` and `[(1, 0), (0, 1)]`. `same_store_observationally_equal` establishes that each `.asserted` list is a subset of the other (`all (fun p => decide (p ∈ ...)) = true`). Despite the word `observationally` in the theorem name, this is mutual list membership on `.asserted`, not the context/observer-based equivalence of earlier units.

5. **Non-environment trace invariants and append-only refusals (Sections 5–6, lines 664–722):**
   - `internal_trace_preserves_occ` and `internal_trace_preserves_license` lift `nonEnv_preserves_occ_licensed` to any trace `l` with `∀ e ∈ l, isEnvOwned e = false`.
   - **Audit note on `internal_blocks_cannot_supply_or_license` (line 686):** This theorem states `(∀ e ∈ b, e ≠ .admitOcc 0) ∧ (∀ e ∈ b, e ≠ .setLicense false)` for `b ∈ nextFamilyP s` (instantiating `0` and `false`); the general statements for arbitrary `t : Nat` and `x : Bool` were already proved in Unit 65 as `TransitionAlphabet.internal_family_no_occurrence_supply` and `TransitionAlphabet.internal_family_no_license_write`.
   - `refusal_persists_step`, `refusal_persists_replay`, and `refusal_not_erasable` show that once `(i, j) ∈ s.refusals`, it remains in `(replayP l s).refusals` for every trace `l`.

6. **Scoped replay equivalence and the two-rule rewrite system `Rw` (Sections 7–8, lines 725–1001):**
   - `ReplayEqvOn C l₁ l₂ := ∀ s, C s → replayP l₁ s = replayP l₂ s`. For `RepresentsZero s := 0 ∈ s.occ`, `[.admitOcc 0]` and `[]` are equivalent on `RepresentsZero` (`replay_eqv_scoped`) but not at `genesisP` (`replay_eqv_not_unscoped`).
   - `Rw` has two reduction rules (`Rw.idem : Rw (e :: e :: l) (e :: l)` and `Rw.absorb : Rw (.halt :: r :: l) [.halt]`) closed under `Rw.cons`. It is sound at every state (`rw_sound`, `rwStar_sound`), strictly decreases list length (`rw_length`), and normalizes every list `l` to a unique redex-free normal form `nf l` (`rwStar_to_nf`, `rw_confluent`, `nf_unique`, `nf_sound`).
   - `rewrite_not_complete` (line 984) establishes `(∀ s : PState, replayP [.setBudget 1, .setBudget 2] s = replayP [.setBudget 2] s) ∧ nf [.setBudget 1, .setBudget 2] ≠ nf [.setBudget 2]`.
   - **Audit note on unscoped replay equivalence (lines 741 vs. 984):** The docstring above `replay_eqv_not_unscoped` at line 741 says "Replay equivalence without a declared start class is not a relation this dynamics satisfies." That sentence overstates `replay_eqv_not_unscoped`, which only refutes unscoped equivalence for the pair `[.admitOcc 0]` vs. `[]`. Unscoped replay equivalence (`ReplayEqvOn (fun _ => True) l₁ l₂`, i.e., `∀ s, replayP l₁ s = replayP l₂ s`) is a well-defined equivalence relation satisfied by every `RwStar`-related pair (`rwStar_sound`) as well as by `[.setBudget 1, .setBudget 2]` and `[.setBudget 2]` (`rewrite_not_complete`).

---

## Plain-language interpretation

When we look for laws that hold across **all** states `s : PState` without consulting `s`, almost every candidate commutation or cancellation law fails because guards read stores that other steps write, and list stores remember the order in which pairs were appended (`[(0, 1), (1, 0)] ≠ [(1, 0), (0, 1)]`).

Two all-state laws, however, hold unconditionally for every event and every state:
1. **All-state idempotence (`step_idem`):** Running the exact same event `e` twice in a row has the same effect as running `e` once (`step (step s e) e = step s e`). For nine of the eleven constructors, this happens because the first step writes the item (`t ∈ occ`, `(i, j) ∈ asserted`, `budget = n`, `halted = true`, etc.) whose absence the guard checks. For `.addCol c`, the first step appends `c` to `obs`, and `colOk` refuses any column already in `obs`. For `.refineCol v p`, the first step replaces every copy of `v` in `obs` by `p :: v`, which has length `v.length + 1`, so `v` is no longer in `obs` (`v_not_mem_map`) and `refineOk` refuses a second split of `v`!
2. **Post-terminal absorption (`trace_absorbs`):** Once `.halt` runs, every subsequent event in the trace is a no-op (`replayP (.halt :: l) s = step s .halt`).

Turning those two all-state laws into a list normalizer `nf` (collapse adjacent duplicates `e :: e` to `e`, and truncate anything after `.halt`) gives a terminating, confluent rewrite system `Rw` that is sound at every state (`nf_sound`), but deliberately incomplete (`rewrite_not_complete`): two distinct budget writes `[.setBudget 1, .setBudget 2]` also reduce to `[.setBudget 2]` at every state, yet `nf` keeps both because `.setBudget 1 ≠ .setBudget 2`.

---

## Pseudocode

```text
STEP_NORMAL_FORM(s, e):
  return postOf(s, e) if guardHolds(s, e) else s

CONS_NF(e, r):
  if r == []:      return [e]
  if e == r[0]:    return r
  return [e] + r

NF(l : List PEvent):
  if l == []:            return []
  if l[0] == halt:       return [halt]
  return CONS_NF(l[0], NF(l[1:]))
  -- Properties: noRedex(NF(l)) == true, RwStar(l, NF(l)),
  -- and for all s : PState, replayP(NF(l), s) == replayP(l, s).
```

---

## Python

From `code/derivation/trace_algebra.py` (lines 51–90, 231–254):

```python
def post_of(s: PS, e: PEvent) -> PS:
    """Lean ``postOf``: the state an event installs once its guard is
    discharged."""
    kind = e[0]
    if kind == "admitOcc":
        return replace(s, occ=s.occ + (cast(int, e[1]),))
    if kind == "assertWit":
        return replace(s, asserted=s.asserted
                       + ((cast(int, e[1]), cast(int, e[2])),))
    if kind == "admitWit":
        return replace(s, wit=s.wit + ((cast(int, e[1]), cast(int, e[2])),))
    if kind == "protect":
        return replace(s, prot=s.prot + ((cast(int, e[1]), cast(int, e[2])),))
    if kind == "declareObs":
        return replace(s, obs=())
    if kind == "refineCol":
        if s.obs is None:
            return s
        v, p = cast(Col, e[1]), cast(int, e[2])
        cols: Cols = tuple((p,) + c if c == v else c for c in s.obs)
        return replace(s, obs=cols, budget=s.budget - 1)
    if kind == "addCol":
        if s.obs is None:
            return s
        return replace(s, obs=s.obs + (cast(Col, e[1]),),
                       budget=s.budget - 1)
    if kind == "refuse":
        return replace(s, refusals=s.refusals
                       + ((cast(int, e[1]), cast(int, e[2])),))
    if kind == "setBudget":
        return replace(s, budget=cast(int, e[1]))
    if kind == "setLicense":
        return replace(s, licensed=cast(bool, e[1]))
    return replace(s, halted=True)


def step_by_normal_form(s: PS, e: PEvent) -> PS:
    """Lean ``step_eq_ite``: the step IS the guarded post-state."""
    return post_of(s, e) if guard_holds(s, e) else s


def cons_nf(e: PEvent, r: list[PEvent]) -> list[PEvent]:
    """Lean ``consNF``."""
    if not r:
        return [e]
    if e == r[0]:
        return list(r)
    return [e] + list(r)


def nf(l: list[PEvent]) -> list[PEvent]:
    """Lean ``nf``: the computed normal form."""
    if not l:
        return []
    if l[0] == ("halt",):
        return [("halt",)]
    return cons_nf(l[0], nf(l[1:]))


def no_redex(l: list[PEvent]) -> bool:
    """Lean ``noRedex``."""
    if len(l) < 2:
        return True
    return l[0] != l[1] and l[0] != ("halt",) and no_redex(l[1:])
```

---

## Line-by-line Python explanation

- **`post_of(s, e)` and `step_by_normal_form(s, e)` (lines 51–90):** `post_of` computes the unguarded record update for each of the 11 constructors; `step_by_normal_form` returns `post_of(s, e)` when `guard_holds(s, e)` is `True` and `s` otherwise, mirroring `step_eq_ite`.
- **`cons_nf(e, r)` and `nf(l)` (lines 231–246):** Recursively normalizes a list of events from right to left: if the head is `("halt",)`, truncates the entire list to `[("halt",)]`; otherwise normalizes the tail `r = nf(l[1:])` and drops `e` if `r` already starts with `e`.
- **`no_redex(l)` (lines 249–253):** Checks that no adjacent pair in `l` is equal (`l[0] != l[1]`) and `("halt",)` never appears before the final slot (`l[0] != ("halt",)`).

---

## Lean 4

From `lean4/Derivation/TraceAlgebra.lean` (selected declarations and theorems across lines 77–1001):

```lean
namespace TraceAlgebra

open PrimitivePassage TransitionAlphabet

theorem step_eq_ite (s : PState) (e : PEvent) :
    step s e = if guardHolds s e = true then postOf s e else s

theorem inert_iff_guard_fails (s : PState) (e : PEvent) :
    step s e = s ↔ guardHolds s e = false

theorem trace_absorbs (l : List PEvent) (s : PState) :
    replayP (.halt :: l) s = step s .halt

theorem guardHolds_post_false (s : PState) (e : PEvent)
    (hacc : Accepted s e = true) : guardHolds (step s e) e = false

theorem step_idem (s : PState) (e : PEvent) :
    step (step s e) e = step s e := by
  cases hacc : Accepted s e with
  | false => simp only [(accepted_false_iff s e).mp hacc]
  | true =>
      exact (inert_iff_guard_fails (step s e) e).mpr
        (guardHolds_post_false s e hacc)

theorem replay_erases (tr : List TRecord) (s : PState) (h : Aligned s tr) :
    replayP (eraseTrace tr) s = endState s tr

theorem legal_trace_replays (tr : List TRecord) (s : PState)
    (h : LegalTrace s tr) :
    replayP (eraseTrace tr) s = endState s tr :=
  replay_erases tr s h.1

theorem comm_setLicense (s : PState) (b : Bool) (e : PEvent)
    (h : licenseInsensitive e = true) :
    step (step s (.setLicense b)) e = step (step s e) (.setLicense b)

theorem comm_setBudget (s : PState) (n : Nat) (e : PEvent)
    (h : budgetInsensitive e = true) :
    step (step s (.setBudget n)) e = step (step s e) (.setBudget n)

theorem comm_admitOcc (s : PState) (t : Nat) (e : PEvent)
    (h : occInsensitive e = true) :
    step (step s (.admitOcc t)) e = step (step s e) (.admitOcc t)

theorem noncomm_same_store :
    step (step wAssert (.assertWit 0 1)) (.assertWit 1 0)
      ≠ step (step wAssert (.assertWit 1 0)) (.assertWit 0 1) := by decide

theorem internal_trace_preserves_occ (l : List PEvent) (s : PState)
    (h : ∀ e ∈ l, isEnvOwned e = false) : (replayP l s).occ = s.occ

theorem internal_trace_preserves_license (l : List PEvent) (s : PState)
    (h : ∀ e ∈ l, isEnvOwned e = false) :
    (replayP l s).licensed = s.licensed

theorem refusal_persists_replay (l : List PEvent) (s : PState) (i j : Nat)
    (h : (i, j) ∈ s.refusals) : (i, j) ∈ (replayP l s).refusals

inductive Rw : List PEvent → List PEvent → Prop where
  | idem (e : PEvent) (l : List PEvent) : Rw (e :: e :: l) (e :: l)
  | absorb (r : PEvent) (l : List PEvent) : Rw (.halt :: r :: l) [.halt]
  | cons (e : PEvent) {l l' : List PEvent} : Rw l l' → Rw (e :: l) (e :: l')

theorem rw_sound (l l' : List PEvent) (h : Rw l l') (s : PState) :
    replayP l s = replayP l' s

theorem rw_length (l l' : List PEvent) (h : Rw l l') :
    l'.length < l.length

theorem rw_confluent (l a b : List PEvent) (ha : RwStar l a)
    (hb : RwStar l b) : ∃ c, RwStar a c ∧ RwStar b c

theorem nf_unique (l a b : List PEvent) (ha : RwStar l a) (hb : RwStar l b)
    (hna : noRedex a = true) (hnb : noRedex b = true) : a = b

theorem nf_sound (l : List PEvent) (s : PState) :
    replayP (nf l) s = replayP l s

theorem rewrite_not_complete :
    (∀ s : PState, replayP [PEvent.setBudget 1, PEvent.setBudget 2] s
      = replayP [PEvent.setBudget 2] s) ∧
    nf [PEvent.setBudget 1, PEvent.setBudget 2] ≠ nf [PEvent.setBudget 2]
```

---

## Line-by-line Lean explanation

1. **Step normal form and all-state idempotence (lines 77–352):**
   - `step_eq_ite` (line 108) splits on `guardHolds s e` and rewrites each accepted branch by `step_*_acc`/`_live`/`_eq` from `TransitionAlphabet`.
   - `v_not_mem_map` (line 223) establishes by length comparison (`congrArg List.length he`) that replacing `v` with `p :: v` in `cols` removes `v` from the list of columns, so `refineOk` fails on `refineS s cols v p` (`refineOk_false_of_not_mem`, line 244).
   - `colOk_false_of_mem` (line 236) establishes that `colOk` fails on `colS s cols c` because `c ∈ cols ++ [c]`.
   - `guardHolds_post_false` (line 251) checks all 11 constructors to show `Accepted s e = true → guardHolds (step s e) e = false`, from which `step_idem` (line 336) follows in five lines.

2. **Typed records and frame commutation (lines 355–660):**
   - `replay_erases` (line 396) inducts on `tr : List TRecord` using only `Aligned s tr`, and `legal_trace_replays` (line 406) projects `h.1 : Aligned s tr`.
   - For each of the three frame families (`licS`, `budS`, `occS`), two lemmas (`guardHolds_*S` and `postOf_*S`) show that `guardHolds` is unchanged and `postOf` commutes with the record update whenever the event satisfies the corresponding insensitivity predicate, yielding `frame_licS` (line 506), `comm_setLicense` (line 513), `frame_budS` (line 543), `comm_setBudget` (line 550), `comm_setBudget_setLicense` (line 563), `frame_occS` (line 586), and `comm_admitOcc` (line 594).
   - Five `decide` theorems (`noncomm_license_extension`..`noncomm_same_store`, lines 620–646) exhibit concrete non-commutation witnesses, and `same_store_observationally_equal` (line 652) checks mutual list membership on `.asserted`.

3. **Internal trace preservation, refusal persistence, and scoped equivalence (lines 664–745):**
   - `internal_trace_preserves_occ` (line 664) and `internal_trace_preserves_license` (line 673) induct on `l : List PEvent` using `TransitionAlphabet.nonEnv_preserves_occ_licensed`.
   - `refusal_persists_step` (line 700) and `refusal_persists_replay` (line 708) show `(i, j) ∈ s.refusals → (i, j) ∈ (replayP l s).refusals`.
   - `replay_eqv_scoped` (line 732) and `replay_eqv_not_unscoped` (line 743) contrast `ReplayEqvOn RepresentsZero [.admitOcc 0] []` with `genesisP`.

4. **The two-rule rewrite system `Rw` and `nf` (lines 756–1001):**
   - `rw_sound` (line 766) uses `step_idem` for `Rw.idem` and `replayP_halted` for `Rw.absorb`; `rw_length` (line 787) establishes `l'.length < l.length`.
   - `rw_preserves_nf` (line 856), `nf_noRedex` (line 888), `noRedex_nf_eq` (line 897), and `rwStar_to_nf` (line 922) show that `nf l` is reachable from `l` by `RwStar`, has `noRedex (nf l) = true`, and is invariant under `RwStar`, yielding `rw_confluent` (line 957), `nf_unique` (line 966), and `nf_sound` (line 974).
   - `rewrite_not_complete` (line 984) establishes that `[.setBudget 1, .setBudget 2]` and `[.setBudget 2]` replay identically at every `s : PState` while `nf [.setBudget 1, .setBudget 2] ≠ nf [.setBudget 2]`.

---

## What has been proved

- **Guarded step normal form (`step_eq_ite`, `inert_iff_guard_fails`):** `step s e` installs `postOf s e` when `guardHolds s e = true` and returns `s` when `guardHolds s e = false`.
- **All-state idempotence and post-terminal absorption (`guardHolds_post_false`, `step_idem`, `trace_absorbs`):** Every constructor `e : PEvent` satisfies `step (step s e) e = step s e` at every `s : PState`, and `replayP (.halt :: l) s = step s .halt`.
- **Typed trace erasure (`replay_erases`, `legal_trace_replays`):** Any `Aligned` chain of `TRecord` values erases to an event list whose `replayP` from `s` equals `endState s tr`.
- **Frame commutation and five countermodels (`comm_setLicense`, `comm_setBudget`, `comm_setBudget_setLicense`, `comm_admitOcc`, `noncomm_license_extension`, `noncomm_budget_extension`, `noncomm_terminal`, `noncomm_supply_retention`, `noncomm_same_store`, `same_store_observationally_equal`).**
- **Non-environment trace preservation and append-only refusals (`internal_trace_preserves_occ`, `internal_trace_preserves_license`, `internal_blocks_cannot_supply_or_license`, `refusal_persists_step`, `refusal_persists_replay`, `refusal_not_erasable`).**
- **Sound, terminating, confluent, incomplete two-rule rewrite system (`rw_sound`, `rwStar_sound`, `rw_length`, `rwStar_to_nf`, `rw_confluent`, `nf_unique`, `nf_sound`, `rewrite_not_complete`).**

---

## What has not been proved

- **Completeness of `nf` is refuted (`rewrite_not_complete`):** The two-rule normalizer `nf` does not identify all unscoped replay-equivalent traces (for instance, `[.setBudget 1, .setBudget 2]` vs. `[.setBudget 2]`), and `TraceAlgebra` does not claim that no richer canonicalizer could exist.
- **Unscoped replay equivalence is not empty:** As noted in `textbook/audit/modules/TraceAlgebra.md`, the docstring at line 741 overgeneralizes `replay_eqv_not_unscoped` (`[.admitOcc 0]` vs. `[]`); `rwStar_sound` and `rewrite_not_complete` both exhibit nontrivial pairs `(l₁, l₂)` satisfying `∀ s : PState, replayP l₁ s = replayP l₂ s`.
- **`TRecord` profile fields (`cls`, `spend`, `profile`) are not consumed by any theorem in `TraceAlgebra.lean`:** Contrary to the phrasing in `CL-PD2-TRACE-ALGEBRA` ("From there the laws are DERIVED"), `legal_trace_replays` uses only `Aligned s tr`, and the algebraic laws are proved directly on `PState` and `PEvent`.
- **`same_store_observationally_equal` is mutual list membership on `.asserted`:** It checks `all (fun p => decide (p ∈ ...))` on the two `.asserted` lists, not context/observer equivalence.
- **Frame insensitivity predicates are not proved necessary in Lean:** Necessity/tightness of `licenseInsensitive`, `budgetInsensitive`, and `occInsensitive` is checked over the finite battery in `code/derivation/trace_algebra.py` (`frame_report`) and witnessed by the five countermodels in Lean.

---

## Outside the system

1. **Metatheory types and quantifiers:**
   - The inductive relations `Rw` and `RwStar`, the predicate transformer `ReplayEqvOn (C : PState → Prop)`, `TRecord`, and the all-quantifiers `∀ s : PState` and `∀ l : List PEvent` belong to the Lean metatheory.
2. **What the system itself holds:**
   - The ledger holds a single `PState` updated step by step; `nf l` and `RwStar l (nf l)` are metatheoretic operations on event lists.
3. **Admissions and their prices:**
   - `postOf`, `TRecord`, `WFRecord`, `Aligned`, `LegalTrace`, `licenseInsensitive`, `budgetInsensitive`, `occInsensitive`, `ReplayEqvOn`, `RepresentsZero`, `Rw`, `RwStar`, `consNF`, `nf`, and `noRedex` are admitted definitions in `TraceAlgebra.lean`.
4. **Phrases to read without importing outside structure:**
   - "Transition monoid" in the module header refers to finite lists `List PEvent` acting on `PState` via `replayP`, not to an infinite quotient monoid stored inside the ledger.

---

## Student exercise

Consider the event list
```
l = [.setBudget 1, .setBudget 1, .addCol [0], .addCol [0], .halt, .admitOcc 9]
```
and the witness state `wObstructed` (`occ = [0, 1]`, `asserted = wit = prot = [(0, 1)]`, `obs = some []`, `budget = 0`, `licensed = true`, `halted = false`).

1. Compute `nf l` step by step using `consNF` and `nf_halt`, and verify `noRedex (nf l) = true`.
2. Give an explicit sequence of `Rw` steps from `l` to `nf l`. Why does the second `.addCol [0]` in `l` do nothing when replayed on `wObstructed` even before `.halt`?
3. Replace the first two events of `l` by `[.setBudget 2, .setBudget 1]` to form `l' = [.setBudget 2, .setBudget 1, .addCol [0], .halt]`. Does `replayP l' s = replayP (nf l) s` hold for every `s : PState`? Does `nf l' = nf l` hold?

---

## Answer

1. **Computing `nf l`:**
   - Starting from the suffix `[.halt, .admitOcc 9]`, `nf [.halt, .admitOcc 9] = [.halt]` by `nf_halt`.
   - Prepending `.addCol [0]` gives `consNF (.addCol [0]) [.halt] = [.addCol [0], .halt]`.
   - Prepending the first `.addCol [0]` gives `consNF (.addCol [0]) [.addCol [0], .halt] = [.addCol [0], .halt]`.
   - Prepending `.setBudget 1` twice gives `nf l = [.setBudget 1, .addCol [0], .halt]`, which has `noRedex (nf l) = true`.
2. **Explicit `Rw` reduction and why the second `.addCol [0]` is inert:**
   - `l` reduces in three `Rw` steps:
     1. `Rw.idem (.setBudget 1) _` collapses the two `.setBudget 1` events;
     2. `Rw.cons (.setBudget 1) (Rw.idem (.addCol [0]) _)` collapses the two `.addCol [0]` events;
     3. `Rw.cons _ (Rw.cons _ (Rw.absorb (.admitOcc 9) []))` drops `.admitOcc 9` after `.halt`.
   - When replayed on `wObstructed`, the first `.addCol [0]` is accepted and appends `[0]` to `obs` (making `obs = some [[0]]`) while spending the budget to `0`. Even if budget remained positive, the second `.addCol [0]` would fail `colOk` because `[0]` is already a member of `obs = some [[0]]` (`colOk_false_of_mem`).
3. **Incompleteness on `l'`:**
   - For every `s : PState`, `step (step s (.setBudget 2)) (.setBudget 1) = step s (.setBudget 1)` (if `s.halted = true`, both sides equal `s`; if `s.halted = false`, both sides set `budget := 1`), so `replayP l' s = replayP (nf l) s` holds for all `s : PState`.
   - Yet `nf l' = [.setBudget 2, .setBudget 1, .addCol [0], .halt] ≠ [.setBudget 1, .addCol [0], .halt] = nf l`.

---

## Verification

| Check | Source |
|---|---|
| Lean | `lean4/Derivation/TraceAlgebra.lean` lines 77–1001 (`lake build Derivation.TraceAlgebra`) |
| Axiom report | `artifacts/lean_axioms.txt` lines 1005–1075 (46 `[propext, Quot.sound]`, 11 `[propext]`, 14 `none`) |
| Paper | `paper/paper_claim_ledger.md` `CL-PD2-TRACE-ALGEBRA`; `paper/paper_change_log.md` ("Goals 2 and 3", items 7–8) |
| Python | `code/derivation/trace_algebra.py`, `code/run_trace_algebra.py`, `tests/test_trace_algebra.py`, `artifacts/trace_algebra.json` |
| Audit | `textbook/audit/modules/TraceAlgebra.md` (unscoped equivalence docstring vs. `rewrite_not_complete`; unused `TRecord` profile fields in `legal_trace_replays`; `same_store_observationally_equal` as list-membership equality; `internal_blocks_cannot_supply_or_license` instance scope) |
| Check (Python) | `python textbook/checks/u66_trace_algebra.py` |
| Check (book Lean) | `python textbook/checks/u66_lean.py` |
