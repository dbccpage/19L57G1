import Derivation.Completion

/-!
# Ultra closure, Phase V–VI: event production and the constitution

Phase V internalizes the event source.  The sealed kernel consumes
explicit events; here the world carries a first-order *policy* (data),
a fixed interpreter maps represented state to the complete family of
next event blocks, and a driver iterates it.  The headline theorem:
the driver *reproduces* the previously supplied tower stream — what PR
#10 had to supply as metatheory is now generated from represented
state, relative to the fixed interpreter.  No hidden tie-break (the
tower family is a proved singleton; the closure family retains every
accepted response), no hidden fresh-name source (fresh identity is the
canonical numeral of the current carrier length — a priced import of
arithmetic and ordering, recorded), explicit budget and license
(emitted as represented events), explicit stop (the empty family).

Phase V also represents the kernel constitution as data: a finite
description family with a fixed family interpreter, and the verified
self-description theorem `interp_describe` — the kernel's own
description executes to exactly the sealed step.  The distinctions
quotation / executable description / verified self-description are
kept as separate definitions.  What remains metatheory is the family
interpreter itself: descriptions are members of a finite data family;
the interpreter is a function over all of them and is not a member.
That stratification boundary is the run's named irreducible
obligation, stated, not hidden.

Phase VI separates autonomy from arbitrary iterability with a
nine-level ladder, proved for the tower driver.
-/

namespace Constitution

open Represented

/-! ## G1 — the represented scheduler -/

/-- The policy store: first-order data, admitted into the generative
state.  `idle` produces nothing; `tower` produces the reflective
growth block; `close` produces the complete family of accepted
responses to current violations. -/
inductive Policy where
  | idle
  | tower
  | close
deriving Repr, DecidableEq

structure GWorld where
  w : World
  pol : Policy
deriving Repr, DecidableEq

/-- Fresh identity: the canonical numeral of the current carrier
length.  A deterministic name function, not a random oracle — and not
free: it imports arithmetic and ordering (the successor structure the
reflective chain already priced). -/
def freshName (w : World) : Nat := w.data.length

def towerBlock (w : World) : List Event :=
  [.setBudget 1, .admitTok (freshName w),
   .require 0 (freshName w), .addView [freshName w]]

/-- The closure family: for every currently violated recorded
requirement, every accepted same-level repair and every accepted
extension — all candidates, no selection. -/
def closeBlocks (w : World) : List (List Event) :=
  (w.reqs.filter (fun r => violB w r)).flatMap fun r =>
    (repairFamily w r).map (fun m => [Event.mark m.1 m.2]) ++
      (Completion.augFamily w r).map (fun c => [Event.addView c])

/-- The fixed interpreter from represented state to the complete
next-event family.  This function is part of the constitution (fixed
metatheory); the policy it reads and the family it emits are
represented. -/
def nextFamily : GWorld → List (List Event)
  | ⟨_, .idle⟩ => []
  | ⟨w, .tower⟩ => [towerBlock w]
  | ⟨w, .close⟩ => closeBlocks w

/-- The tower family is a proved singleton: executing its head is not
a tie-break, because there is nothing to select among. -/
theorem nextFamily_tower_singleton (w : World) :
    (nextFamily ⟨w, .tower⟩).length = 1 := rfl

/-- Completeness of the closure family, repair side: every accepted
same-level repair of every violated requirement appears. -/
theorem closeBlocks_complete_repair {w : World} {r : Req}
    {m : View × Nat} (hr : r ∈ w.reqs) (hv : violB w r = true)
    (hm : m ∈ repairFamily w r) :
    [Event.mark m.1 m.2] ∈ closeBlocks w := by
  unfold closeBlocks
  simp only [List.mem_flatMap]
  refine ⟨r, ?_, ?_⟩
  · exact List.mem_filter.mpr ⟨hr, hv⟩
  · simp only [List.mem_append, List.mem_map]
    exact Or.inl ⟨m, hm, rfl⟩

/-- Completeness of the closure family, extension side: every accepted
extension of every violated requirement appears — both orientations,
by `Completion.augFamily_retains_ties`. -/
theorem closeBlocks_complete_aug {w : World} {r : Req} {c : View}
    (hr : r ∈ w.reqs) (hv : violB w r = true)
    (hc : c ∈ Completion.augFamily w r) :
    [Event.addView c] ∈ closeBlocks w := by
  unfold closeBlocks
  simp only [List.mem_flatMap]
  refine ⟨r, ?_, ?_⟩
  · exact List.mem_filter.mpr ⟨hr, hv⟩
  · simp only [List.mem_append, List.mem_map]
    exact Or.inr ⟨c, hc, rfl⟩

/-- The explicit stop outcome: a quiescent world generates the empty
family under the closure policy — the generator's silence is a
represented verdict, not an exception. -/
theorem nextFamily_stop {w : World} (hq : quiescentB w = true) :
    nextFamily ⟨w, .close⟩ = [] := by
  show closeBlocks w = []
  unfold closeBlocks
  have hnil : w.reqs.filter (fun r => violB w r) = [] := by
    cases hf : w.reqs.filter (fun r => violB w r) with
    | nil => rfl
    | cons x t =>
        exfalso
        have hx : x ∈ w.reqs.filter (fun r => violB w r) := by
          rw [hf]
          exact List.mem_cons_self
        have ⟨hmem, hviol⟩ := List.mem_filter.mp hx
        unfold quiescentB at hq
        simp only [List.all_eq_true] at hq
        have hsat := hq x hmem
        unfold violB at hviol
        simp only [Bool.and_eq_true] at hviol
        rw [hsat] at hviol
        exact absurd hviol.2 (by decide)
  rw [hnil]
  rfl

/-! ## G2 — the represented driver, and the reproduction theorem -/

/-- The driver-generated history: at each stage, execute the unique
member of the tower family computed from the *replayed represented
state*.  Nothing else is consumed. -/
def towerGen : Nat → List Event
  | 0 => [.admitTok 0]
  | k + 1 =>
      towerGen k ++ towerBlock (replay (towerGen k) genesis)

theorem towerBlock_eq (k : Nat) :
    towerBlock (worldAt k) = blockEvents (k + 1) := by
  unfold towerBlock blockEvents freshName
  rw [worldAt_growth]

/-- **The event source, internalized (relative to the fixed
interpreter).**  The driver's generated history equals the previously
*supplied* tower stream: what entered PR #10 as a metatheoretic
history producer is now computed, stage by stage, from the replayed
represented state by the represented policy.  The remaining
metatheory is the interpreter (`nextFamily`) and the arithmetic of
the canonical fresh name — both fixed constitution, both recorded. -/
theorem driver_reproduces_tower : ∀ k, towerGen k = histUpTo k := by
  intro k
  induction k with
  | zero => rfl
  | succ m ih =>
      show towerGen m ++ towerBlock (replay (towerGen m) genesis) =
        histUpTo m ++ blockEvents (m + 1)
      rw [ih, show replay (histUpTo m) genesis = worldAt m from rfl,
        towerBlock_eq]

/-- The complete-family form: the driver appends exactly the unique
family member — the generation step is the represented family, not a
hidden choice. -/
theorem nextFamily_complete (k : Nat) :
    nextFamily ⟨replay (towerGen k) genesis, .tower⟩ =
      [towerBlock (replay (towerGen k) genesis)] := rfl

/-- Resource replenishment is a represented act: the driver's block
opens with an explicit budget event.  Self-funding is a policy choice,
visible in the emitted history, priced as such. -/
theorem budget_replenishment_represented (w : World) :
    (towerBlock w).head? = some (.setBudget 1) := rfl

def genWorld (k : Nat) : GWorld :=
  ⟨replay (towerGen k) genesis, .tower⟩

theorem gen_growth (k : Nat) :
    (genWorld k).w.data.length = k + 1 := by
  unfold genWorld
  rw [driver_reproduces_tower]
  exact worldAt_growth k

/-- Acceptance along the generated run, concrete stage: the third
generated world is quiescent — every emitted event was accepted by the
sealed checks (the Python mirror verifies acceptance exhaustively to
the declared bound). -/
theorem gen_three_quiescent : quiescentB (genWorld 3).w = true := by
  have h := driver_reproduces_tower 3
  unfold genWorld
  rw [h]
  exact worldAt_three_quiescent

/-! ## Phase VI — autonomy separated from iterability

The nine-level ladder, proved for the tower driver.  Levels: (1) a
step exists at every stage; (2) the trace is prefix-compatible; (3)
the next family is computed from represented state; (4) the kernel
itself triggers the family's execution (the driver's recursion
consumes nothing external); (5–6) selection-freeness: the family is a
proved singleton, so all ties are (vacuously) retained and no selector
exists; (7) resources persist by represented replenishment events;
(8) the process stays lawful across expressive extensions (each block
ends in an accepted `addView`; instance-verified here, exhaustively
bound-verified in the mirror); (9) productivity holds under the
explicit measure (strict carrier growth).  An arbitrarily iterable
theorem gives (1)–(2); autonomy in the sense proved here is
(1)–(9) *relative to the fixed interpreter and the declared policy
data*.  Nothing stronger is claimed. -/
theorem tower_driver_autonomy :
    (∀ k, towerGen k <+: towerGen (k + 1)) ∧
      (∀ k, nextFamily (genWorld k) =
        [towerBlock (genWorld k).w]) ∧
      (∀ k, towerGen (k + 1) =
        towerGen k ++ towerBlock (genWorld k).w) ∧
      (∀ k, (nextFamily (genWorld k)).length = 1) ∧
      (∀ k, (towerBlock (genWorld k).w).head? =
        some (.setBudget 1)) ∧
      (∀ k, (genWorld k).w.data.length <
        (genWorld (k + 1)).w.data.length) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro k
    exact ⟨towerBlock (replay (towerGen k) genesis), rfl⟩
  · intro k
    rfl
  · intro k
    rfl
  · intro k
    rfl
  · intro k
    rfl
  · intro k
    rw [gen_growth, gen_growth]
    omega

/-! ## G3 — the constitution as data

A finite description family (`ConstitutionDesc`) with a fixed family
interpreter (`interpStep`).  The kernel's own description executes to
exactly the sealed step (`interp_describe`) — a verified
self-description with executable semantics *relative to the family
interpreter*.  The three levels are kept apart:

* **quotation** — a `ConstitutionDesc` is inert data;
* **executable description** — `interpStep d` is a semantics, but the
  execution is performed by the fixed interpreter, which is
  constitution, not state;
* **verified self-description** — `interp_describe` proves the
  described kernel and the sealed kernel coincide.

What is *not* achieved — and is recorded as the named irreducible
obligation rather than hidden: the family interpreter is a function
over the description family and not a member of it, so the outermost
interpretation relation remains metatheoretic.  `G4` below is the
honest boundary, not a theorem laundered through the word
"self-apply". -/

structure ConstitutionDesc where
  dedupAdmit : Bool
  guardRequire : Bool
  guardAccept : Bool
  gateBudget : Bool
  gateLicense : Bool
  certRefusal : Bool
deriving Repr, DecidableEq

def kernelDesc : ConstitutionDesc := ⟨true, true, true, true, true, true⟩

/-- The fixed family interpreter: one small-step machine consuming a
description and an event.  With every toggle on it is the sealed
kernel; each toggle names one load-bearing guard of the constitution
(the separations are proved in `Initiality`). -/
def interpStep (d : ConstitutionDesc) (w : World) : Event → World
  | .admitTok t =>
      if d.dedupAdmit && decide (t ∈ w.data) then w
      else { w with data := w.data ++ [t] }
  | .require i j =>
      if !d.guardRequire || reqOkB w i j then
        { w with reqs := w.reqs ++ [(i, j)] }
      else w
  | .mark v p =>
      if (!d.guardAccept || markOkB w v p)
          && (!d.gateBudget || decide (0 < w.budget)) then
        { markApply w v p with budget := w.budget - 1 }
      else w
  | .addView c =>
      if (!d.guardAccept || augOkB w c)
          && (!d.gateLicense || w.augLicensed)
          && (!d.gateBudget || decide (0 < w.budget)) then
        { augApply w c with budget := w.budget - 1 }
      else w
  | .refuse i j =>
      if (!d.certRefusal || obstructedB w (i, j))
          && !(decide ((i, j) ∈ w.refusals)) then
        { w with refusals := w.refusals ++ [(i, j)] }
      else w
  | .note n => { w with notes := w.notes ++ [n] }
  | .setBudget n => { w with budget := n }
  | .setAugLicense b => { w with augLicensed := b }

/-- **Verified self-description.**  The kernel's own description,
executed by the family interpreter, is exactly the sealed step. -/
theorem interp_describe (w : World) (e : Event) :
    interpStep kernelDesc w e = step w e := by
  cases e with
  | admitTok t =>
      simp only [interpStep, step, kernelDesc, Bool.true_and]
      by_cases hmem : t ∈ w.data
      · rw [if_pos (by rw [decide_eq_true hmem]),
            if_pos hmem]
      · rw [if_neg (by rw [decide_eq_false hmem]; decide),
            if_neg hmem]
  | require i j =>
      simp only [interpStep, step, kernelDesc, Bool.not_true,
        Bool.false_or]
  | mark v p =>
      simp only [interpStep, step, kernelDesc, Bool.not_true,
        Bool.false_or]
  | addView c =>
      simp only [interpStep, step, kernelDesc, Bool.not_true,
        Bool.false_or]
  | refuse i j =>
      simp only [interpStep, step, kernelDesc, Bool.not_true,
        Bool.false_or]
  | note n => rfl
  | setBudget n => rfl
  | setAugLicense b => rfl

/-- The description family is finite and completely enumerated: the
constitution family is a closed, represented search space (64
members). -/
def bools : List Bool := [false, true]

def allDescs : List ConstitutionDesc :=
  bools.flatMap fun a => bools.flatMap fun b =>
    bools.flatMap fun c => bools.flatMap fun e =>
      bools.flatMap fun f => bools.map fun g => ⟨a, b, c, e, f, g⟩

theorem allDescs_length : allDescs.length = 64 := by decide

theorem allDescs_complete : ∀ d : ConstitutionDesc, d ∈ allDescs := by
  intro d
  cases d with
  | mk a b c e f g =>
      cases a <;> cases b <;> cases c <;> cases e <;> cases f <;>
        cases g <;> decide

end Constitution
