import Derivation.PrimDiff

/-!
# The passage through Primitive Difference

Phase VI of the contact-and-passage run.  A minimal, self-contained
dynamics carrying exactly the passage chain

  PrimitiveDifference → RetainedDifference → FaithfulPresentation →
  DeclaredObservation → ZeroRel → ProtectedCollapse →
  ActiveObstruction → ExhaustiveSameLevelFamily →
  RepairFamily | ExtensionProposalFamily → AuthorizationAndBudget →
  Replay → Remeasurement → RefusalRecord | Terminal →
  RepresentedNextFamily

with one status per arrow (theorem, declaration, or false without
extra hypotheses), necessity countermodels, and the P1–P8 theorems.

The single deliberate refinement over the sealed `Completion.obstC`:
observation here is an `Option` — `none` is *pre-observational*, not
"an observer that sees nothing".  Active obstruction is therefore a
FOUR-condition conjunction (retained, protected, observation
declared, observer-zero on the pair), and the pre-observational
purity of Primitive Difference is a theorem
(`obst_requires_observation`), not a convention.  The exact relation
to the sealed three-condition predicate is proved
(`obst_agrees_when_declared`, `obst_diverges_when_undeclared`).

Naming discipline: "forced", "complete", "exhaustive" appear only
with a proof over a declared finite universe.  Refusal is a record;
the terminal is absorbing; proposal is not execution.
-/

namespace PrimitivePassage

/-! ## State and events

Every notion the passage separates is a separate field.  Positions in
`occ` are occurrence identities (0-cells); `wit` is the retained
positive witness store (1-cells); `prot` is the protected-demand
store; `obs` is the declared observation, `none` before any observer
is admitted. -/

structure PState where
  occ : List Nat
  wit : List (Nat × Nat)
  prot : List (Nat × Nat)
  obs : Option (List (List Nat))
  budget : Nat
  licensed : Bool
  refusals : List (Nat × Nat)
  halted : Bool
deriving Repr, DecidableEq

def genesisP : PState :=
  { occ := [], wit := [], prot := [], obs := none, budget := 0,
    licensed := true, refusals := [], halted := false }

inductive PEvent where
  | admitOcc (t : Nat)
  | admitWit (i j : Nat)
  | protect (i j : Nat)
  | declareObs
  | refineCol (v : List Nat) (p : Nat)
  | addCol (c : List Nat)
  | refuse (i j : Nat)
  | setBudget (n : Nat)
  | setLicense (b : Bool)
  | halt
deriving Repr, DecidableEq

/-! ## Observation semantics -/

/-- One column separates two occurrence positions. -/
def sepCol (c : List Nat) (i j : Nat) : Bool :=
  (decide (i ∈ c)) != (decide (j ∈ c))

/-- Observer separation, only meaningful under a declared
observation. -/
def sepP (cols : List (List Nat)) (i j : Nat) : Bool :=
  cols.any (fun c => sepCol c i j)

/-- The zero relation of a declared observation: no declared column
separates.  Defined only on the declared side — a pre-observational
state has no zero relation at all. -/
def zeroP (cols : List (List Nat)) (i j : Nat) : Bool :=
  !sepP cols i j

theorem zeroP_cons (c : List Nat) (rest : List (List Nat))
    (i j : Nat) :
    zeroP (c :: rest) i j = ((!sepCol c i j) && zeroP rest i j) := by
  unfold zeroP sepP
  simp [List.any_cons, Bool.not_or]

/-! ## Active obstruction: the four-condition conjunction -/

/-- Active obstruction: the pair is retained, protected, an
observation IS declared, and the declared observation does not
separate the pair.  Four independent conditions. -/
def obstP (s : PState) (i j : Nat) : Bool :=
  (decide ((i, j) ∈ s.wit)) && (decide ((i, j) ∈ s.prot))
    && (match s.obs with
        | none => false
        | some cols => zeroP cols i j)

/-- **P1, half 1: Primitive Difference precedes observation.**  The
witness store is independent of the observation field: states
differing only in `obs` retain the same witnesses. -/
theorem wit_independent_of_obs (s : PState)
    (o : Option (List (List Nat))) (i j : Nat) :
    ((i, j) ∈ ({ s with obs := o } : PState).wit)
      ↔ ((i, j) ∈ s.wit) := Iff.rfl

/-- **P1, half 2: obstruction does not precede observation.**  In a
pre-observational state nothing is obstructed, whatever is retained
and protected. -/
theorem obst_requires_observation (s : PState) (i j : Nat)
    (h : s.obs = none) : obstP s i j = false := by
  unfold obstP
  rw [h]
  simp

/-- The declared-observation refinement, exact relation to a
three-condition reading: once an observation is declared, the
four-condition form is the three-condition form. -/
theorem obst_agrees_when_declared (s : PState)
    (cols : List (List Nat)) (h : s.obs = some cols) (i j : Nat) :
    obstP s i j =
      ((decide ((i, j) ∈ s.wit)) && (decide ((i, j) ∈ s.prot))
        && zeroP cols i j) := by
  unfold obstP
  rw [h]

/-- And they diverge exactly on pre-observational states: a
three-condition reading that treats "no observation" as "observer
zero" calls this state obstructed; the four-condition form does not.
Concrete divergence witness. -/
theorem obst_diverges_when_undeclared :
    (((decide (((0 : Nat), (1 : Nat)) ∈ [((0 : Nat), (1 : Nat))]))
        && (decide (((0 : Nat), (1 : Nat)) ∈ [((0 : Nat), (1 : Nat))]))
        && zeroP [] 0 1) = true) ∧
    obstP { occ := [0, 1], wit := [(0, 1)], prot := [(0, 1)],
            obs := none, budget := 0, licensed := true,
            refusals := [], halted := false } 0 1 = false := by
  constructor
  · decide
  · decide

/-- **P5: every proper subset of the four obstruction conditions is
insufficient.**  The four maximal proper subsets, each realized by a
concrete state that fails to obstruct, plus the non-vacuity witness
with all four conditions. -/
theorem obst_conditions_independent :
    -- retained, protected, declared, but separated (zero fails)
    obstP { occ := [0, 1], wit := [(0, 1)], prot := [(0, 1)],
            obs := some [[0]], budget := 0, licensed := true,
            refusals := [], halted := false } 0 1 = false ∧
    -- retained, protected, zero-vacuous, but NOT declared
    obstP { occ := [0, 1], wit := [(0, 1)], prot := [(0, 1)],
            obs := none, budget := 0, licensed := true,
            refusals := [], halted := false } 0 1 = false ∧
    -- retained, declared, zero, but not protected
    obstP { occ := [0, 1], wit := [(0, 1)], prot := [],
            obs := some [], budget := 0, licensed := true,
            refusals := [], halted := false } 0 1 = false ∧
    -- protected, declared, zero, but not retained
    obstP { occ := [0, 1], wit := [], prot := [(0, 1)],
            obs := some [], budget := 0, licensed := true,
            refusals := [], halted := false } 0 1 = false ∧
    -- all four: obstructed
    obstP { occ := [0, 1], wit := [(0, 1)], prot := [(0, 1)],
            obs := some [], budget := 0, licensed := true,
            refusals := [], halted := false } 0 1 = true := by
  decide

/-! ## The step function

Guards mirror the sealed kernel's discipline: dedup admission,
well-formedness at protection, certificate-bearing refusal, budget
and license gates on structure creation, absorbing terminal. -/

def wfPair (s : PState) (i j : Nat) : Bool :=
  (i != j) && (decide (i < s.occ.length))
    && (decide (j < s.occ.length))

/-- Same-level acceptance: refine an existing column by one point.
The move must discharge some obstruction and break no protected
separation (monotone preservation, as in the sealed kernel). -/
def refineOk (s : PState) (v : List Nat) (p : Nat) : Bool :=
  match s.obs with
  | none => false
  | some cols =>
      (decide (v ∈ cols)) && (decide (p < s.occ.length))
        && !(decide (p ∈ v))
        && (s.prot.any (fun r =>
              obstP s r.1 r.2
                && sepCol (p :: v) r.1 r.2))
        && (s.prot.all (fun r =>
              !sepP cols r.1 r.2 || sepP (cols.map
                (fun c => if c = v then p :: c else c)) r.1 r.2))

/-- Structure-creating acceptance: a new column, in bounds, not
already present, separating some obstructed pair. -/
def colOk (s : PState) (c : List Nat) : Bool :=
  match s.obs with
  | none => false
  | some cols =>
      c.all (fun p => decide (p < s.occ.length))
        && !(decide (c ∈ cols))
        && (s.prot.any (fun r => obstP s r.1 r.2 && sepCol c r.1 r.2))

def step (s : PState) : PEvent → PState
  | .admitOcc t =>
      if s.halted then s
      else if t ∈ s.occ then s else { s with occ := s.occ ++ [t] }
  | .admitWit i j =>
      if s.halted then s
      else if wfPair s i j && !(decide ((i, j) ∈ s.wit)) then
        { s with wit := s.wit ++ [(i, j)] }
      else s
  | .protect i j =>
      if s.halted then s
      else if (decide ((i, j) ∈ s.wit))
          && !(decide ((i, j) ∈ s.prot)) then
        { s with prot := s.prot ++ [(i, j)] }
      else s
  | .declareObs =>
      if s.halted then s
      else match s.obs with
        | none => { s with obs := some [] }
        | some _ => s
  | .refineCol v p =>
      if s.halted then s
      else if refineOk s v p && decide (0 < s.budget) then
        match s.obs with
        | none => s
        | some cols =>
            { s with
              obs := some (cols.map
                (fun c => if c = v then p :: c else c)),
              budget := s.budget - 1 }
      else s
  | .addCol c =>
      if s.halted then s
      else if colOk s c && s.licensed && decide (0 < s.budget) then
        match s.obs with
        | none => s
        | some cols =>
            { s with obs := some (cols ++ [c]),
                     budget := s.budget - 1 }
      else s
  | .refuse i j =>
      if s.halted then s
      else if obstP s i j && !(decide ((i, j) ∈ s.refusals)) then
        { s with refusals := s.refusals ++ [(i, j)] }
      else s
  | .setBudget n => if s.halted then s else { s with budget := n }
  | .setLicense b =>
      if s.halted then s else { s with licensed := b }
  | .halt => { s with halted := true }

def replayP (h : List PEvent) (s : PState) : PState := h.foldl step s

/-! ## Arrow statuses, proved

Each passage arrow is a theorem, a declaration (an admission event is
required, with a countermodel showing the arrow is false without it),
or false without extra hypotheses. -/

/-- **PrimitiveDifference → RetainedDifference is a DECLARATION.**
Supplying a witnessed difference does not retain it: retention is a
separate admission event.  Countermodel: the genesis extension by
occurrences alone retains nothing. -/
theorem retention_not_free :
    (replayP [.admitOcc 7, .admitOcc 8] genesisP).wit = [] := by
  decide

/-- Retention, once admitted, is a theorem-level invariant: the
witness store is append-only under every event. -/
theorem retention_persists (s : PState) (e : PEvent) (i j : Nat)
    (h : (i, j) ∈ s.wit) : (i, j) ∈ (step s e).wit := by
  cases e <;> simp only [step] <;> repeat' split
  all_goals
    first
      | exact h
      | (simp only [List.mem_append]; exact Or.inl h)

/-- **P2: fidelity is separate.**  Admitting a witness never creates
protection: the protection store is unchanged by witness admission,
at every state. -/
theorem witness_no_protection (s : PState) (i j : Nat) :
    (step s (.admitWit i j)).prot = s.prot := by
  simp only [step]
  repeat' split
  all_goals rfl

/-- P2 countermodel side: a retained, observed-collapsed witness with
no protection is not an obstruction. -/
theorem no_protection_no_obstruction :
    obstP { occ := [0, 1], wit := [(0, 1)], prot := [],
            obs := some [], budget := 9, licensed := true,
            refusals := [], halted := false } 0 1 = false := by decide

/-!
**RetainedDifference → FaithfulPresentation is a DECLARATION**:
faithfulness of a presentation is a demand on the presenting map, not
a fact following from retention
(`PrimDiff.const_presentation_unfaithful` is the countermodel:
constant presentations exist and lose every asserted pair).  What
protection buys is the barrier theorem: -/

/-- **P3: the faithful-presentation barrier.**  If a presentation
identifies the two endpoints, then no function of the presented image
alone separates their images — recovery data must come from outside
the quotient (here: from the retained store, which is exactly what
retention is for). -/
theorem quotient_no_recovery {X Q : Type} (q : X → Q) (a b : X)
    (hq : q a = q b) (g : Q → Q → Prop) :
    g (q a) (q b) ↔ g (q a) (q a) := by rw [hq]

/-!
**FaithfulPresentation → DeclaredObservation is a DECLARATION** with
its own event (`declareObs`); the zero relation exists only after it
(`obst_requires_observation`).  P4 demands the ZeroRel laws before
any quotient is taken: -/

theorem sepCol_irrefl (c : List Nat) (i : Nat) :
    sepCol c i i = false := by
  unfold sepCol
  cases decide (i ∈ c) <;> rfl

theorem sepCol_symm (c : List Nat) (i j : Nat) :
    sepCol c i j = sepCol c j i := by
  unfold sepCol
  cases decide (i ∈ c) <;> cases decide (j ∈ c) <;> rfl

theorem sepCol_trans (c : List Nat) (i j k : Nat)
    (h1 : sepCol c i j = false) (h2 : sepCol c j k = false) :
    sepCol c i k = false := by
  unfold sepCol at *
  cases hi : decide (i ∈ c) <;> cases hj : decide (j ∈ c)
    <;> cases hk : decide (k ∈ c) <;> simp_all

/-- **P4: ZeroRel is reflexive** on every declared observation. -/
theorem zero_refl (cols : List (List Nat)) (i : Nat) :
    zeroP cols i i = true := by
  induction cols with
  | nil => rfl
  | cons c rest ih =>
      rw [zeroP_cons, sepCol_irrefl, ih]
      rfl

/-- **P4: ZeroRel is symmetric** on every declared observation. -/
theorem zero_symm (cols : List (List Nat)) (i j : Nat) :
    zeroP cols i j = zeroP cols j i := by
  induction cols with
  | nil => rfl
  | cons c rest ih =>
      rw [zeroP_cons, zeroP_cons, sepCol_symm, ih]

/-- **P4: ZeroRel is transitive** on every declared observation:
zero means "agrees on membership in every declared column", which
composes. -/
theorem zero_trans (cols : List (List Nat)) (i j k : Nat)
    (hij : zeroP cols i j = true) (hjk : zeroP cols j k = true) :
    zeroP cols i k = true := by
  induction cols with
  | nil => rfl
  | cons c rest ih =>
      rw [zeroP_cons] at hij hjk ⊢
      simp only [Bool.and_eq_true, Bool.not_eq_true'] at hij hjk
      have h1 := sepCol_trans c i j k hij.1 hjk.1
      rw [h1, ih hij.2 hjk.2]
      rfl

/-! ## The response universe and the two-rule theorem -/

/-- The declared same-level response universe: refine any declared
column by any in-bounds point.  Finite, and complete over the
declared universe by `menu_complete`. -/
def responseMenu (s : PState) : List (List Nat × Nat) :=
  match s.obs with
  | none => []
  | some cols =>
      cols.flatMap fun v =>
        (List.range s.occ.length).map fun p => (v, p)

/-- Same-level repairs of an obstructed pair: accepted moves whose
refined observation separates the pair. -/
def repairFamily (s : PState) (i j : Nat) :
    List (List Nat × Nat) :=
  (responseMenu s).filter fun m =>
    refineOk s m.1 m.2
      && (match s.obs with
          | none => false
          | some cols =>
              sepP (cols.map
                (fun c => if c = m.1 then m.2 :: c else c)) i j)

/-- The menu is complete over the declared universe: every declared
column and every in-bounds point occur. -/
theorem menu_complete (s : PState) (cols : List (List Nat))
    (h : s.obs = some cols) (v : List Nat) (p : Nat)
    (hv : v ∈ cols) (hp : p < s.occ.length) :
    (v, p) ∈ responseMenu s := by
  unfold responseMenu
  rw [h]
  simp only [List.mem_flatMap]
  exact ⟨v, hv, by
    simp only [List.mem_map]
    exact ⟨p, List.mem_range.mpr hp, rfl⟩⟩

/-- Extension proposals for an obstructed pair: new columns from the
declared universe (the singleton columns over admitted positions)
that would separate the pair.  Proposals are records; execution is
separately gated. -/
def extensionProposals (s : PState) (i j : Nat) :
    List (List Nat) :=
  ((List.range s.occ.length).map (fun p => [p])).filter fun c =>
    colOk s c && sepCol c i j

/-- **The extension family is never empty at an obstruction** (with
in-bounds first endpoint): the singleton column on the first endpoint
always qualifies — it is fresh (a declared observation containing it
would have separated the pair), in bounds, and separating. -/
theorem extension_always_available (s : PState) (i j : Nat)
    (hobst : obstP s i j = true) (hij : i ≠ j)
    (hi : i < s.occ.length) (hprot : ((i, j) ∈ s.prot)) :
    [i] ∈ extensionProposals s i j := by
  have hsep : sepCol [i] i j = true := by
    unfold sepCol
    rw [decide_eq_true (List.mem_singleton.mpr rfl),
        decide_eq_false (by
          intro hmem
          exact hij (List.mem_singleton.mp hmem).symm)]
    rfl
  cases hcols : s.obs with
  | none =>
      rw [obst_requires_observation s i j hcols] at hobst
      cases hobst
  | some cols =>
      rw [obst_agrees_when_declared s cols hcols i j] at hobst
      simp only [Bool.and_eq_true, decide_eq_true_eq] at hobst
      obtain ⟨⟨hwit, hpr⟩, hzero⟩ := hobst
      have hsepfalse : sepP cols i j = false := by
        cases hv : sepP cols i j with
        | false => rfl
        | true =>
            unfold zeroP at hzero
            rw [hv] at hzero
            exact Bool.noConfusion hzero
      have hfresh : ¬ (([i] : List Nat) ∈ cols) := by
        intro hmem
        have : sepP cols i j = true := by
          unfold sepP
          exact List.any_eq_true.mpr ⟨[i], hmem, hsep⟩
        rw [this] at hsepfalse
        exact Bool.noConfusion hsepfalse
      have hobstij : obstP s i j = true := by
        rw [obst_agrees_when_declared s cols hcols i j,
            decide_eq_true hwit, decide_eq_true hpr, hzero]
        rfl
      have hcolok : colOk s [i] = true := by
        unfold colOk
        rw [hcols]
        show (([i] : List Nat).all
            (fun p => decide (p < s.occ.length))
          && !(decide (([i] : List Nat) ∈ cols))
          && s.prot.any
              (fun r => obstP s r.1 r.2 && sepCol [i] r.1 r.2))
          = true
        have h1 : (([i] : List Nat).all
            (fun p => decide (p < s.occ.length))) = true := by
          simp only [List.all_cons, List.all_nil, Bool.and_true]
          exact decide_eq_true hi
        have h3 : (s.prot.any
            (fun r => obstP s r.1 r.2 && sepCol [i] r.1 r.2))
            = true := by
          apply List.any_eq_true.mpr
          refine ⟨(i, j), hprot, ?_⟩
          show (obstP s i j && sepCol [i] i j) = true
          rw [hobstij, hsep]
          rfl
        rw [h1, decide_eq_false hfresh, h3]
        rfl
      unfold extensionProposals
      apply List.mem_filter.mpr
      constructor
      · simp only [List.mem_map]
        exact ⟨i, List.mem_range.mpr hi, rfl⟩
      · rw [hcolok, hsep]
        rfl

/-- **P7, the two-rule theorem.**  At an active obstruction with an
in-bounds protected pair, the response universe never runs dry:
either the same-level repair family is nonempty, or same-level
exhaustion is certified (the family is the exhaustive filter of the
complete menu, `menu_complete`) and the extension-proposal family is
nonempty.  The obstruction is forced to a response: remove it
at the same level, or create structure.  Refusal and the terminal
are separately typed records, not members of either family. -/
theorem two_rule (s : PState) (i j : Nat)
    (hobst : obstP s i j = true) (hij : i ≠ j)
    (hi : i < s.occ.length) (hprot : (i, j) ∈ s.prot) :
    repairFamily s i j ≠ [] ∨
      (repairFamily s i j = [] ∧ extensionProposals s i j ≠ []) := by
  cases hrep : repairFamily s i j with
  | cons m rest => exact Or.inl (by simp)
  | nil =>
      refine Or.inr ⟨rfl, ?_⟩
      intro hempty
      have := extension_always_available s i j hobst hij hi hprot
      rw [hempty] at this
      cases this

/-- Proposal is not execution: an unlicensed live state accepts no
column creation, whatever the proposal family contains. -/
theorem proposal_not_execution (s : PState) (c : List Nat)
    (h : s.licensed = false) (hh : s.halted = false) :
    step s (.addCol c) = s := by
  have hg : ¬ ((colOk s c && s.licensed
      && decide (0 < s.budget)) = true) := by
    intro hc
    simp only [Bool.and_eq_true] at hc
    rw [h] at hc
    exact Bool.noConfusion hc.1.2
  simp only [step, hh]
  rw [if_neg (fun hc : false = true => Bool.noConfusion hc),
      if_neg hg]

/-- Budget gates execution the same way. -/
theorem budget_gates_execution (s : PState) (c : List Nat)
    (h : s.budget = 0) (hh : s.halted = false) :
    step s (.addCol c) = s := by
  have hg : ¬ ((colOk s c && s.licensed
      && decide (0 < s.budget)) = true) := by
    intro hc
    simp only [Bool.and_eq_true] at hc
    rw [h] at hc
    have := hc.2
    simp at this
  simp only [step, hh]
  rw [if_neg (fun hc : false = true => Bool.noConfusion hc),
      if_neg hg]

/-! ## Refusal record and absorbing terminal, separately typed -/

/-- Refusal touches no obstruction-relevant field: it is a record,
not an action. -/
theorem refusal_object_inert (s : PState) (i j : Nat) :
    ((step s (.refuse i j)).occ = s.occ) ∧
    ((step s (.refuse i j)).wit = s.wit) ∧
    ((step s (.refuse i j)).prot = s.prot) ∧
    ((step s (.refuse i j)).obs = s.obs) ∧
    ((step s (.refuse i j)).budget = s.budget) := by
  simp only [step]
  repeat' split
  all_goals exact ⟨rfl, rfl, rfl, rfl, rfl⟩

/-- Refusal does not absorb: the halted flag is untouched. -/
theorem refusal_not_terminal (s : PState) (i j : Nat) :
    (step s (.refuse i j)).halted = s.halted := by
  simp only [step]
  repeat' split
  all_goals rfl

/-- On a halted state every event is inert. -/
theorem step_halted (t : PState) (e : PEvent)
    (h : t.halted = true) : step t e = t := by
  cases t with
  | mk occ wit prot obs budget licensed refusals halted =>
      subst h
      cases e <;> rfl

/-- The terminal is absorbing: after `halt`, every event is inert. -/
theorem terminal_absorbing (s : PState) (e : PEvent) :
    step (step s .halt) e = step s .halt :=
  step_halted _ _ rfl

/-! ## P8: the operational no-outside schema -/

/-- Same represented state, same event, same successor: the step is
a function of represented data alone (the operational no-outside
form; the absolute form quantifies over unrepresented differences
and is not formulable here — not claimed). -/
theorem no_outside_operational (s t : PState) (e : PEvent)
    (h : s = t) : step s e = step t e := by rw [h]

/-- Replay determinism from genesis: the passage state is a function
of its represented history alone. -/
theorem replay_deterministic (h1 h2 : List PEvent) (heq : h1 = h2) :
    replayP h1 genesisP = replayP h2 genesisP := by rw [heq]

/-- Replay composes: history is append-transparent. -/
theorem replay_append (h1 h2 : List PEvent) (s : PState) :
    replayP (h1 ++ h2) s = replayP h2 (replayP h1 s) := by
  simp [replayP, List.foldl_append]

/-! ## Remeasurement: the executed response resolves the obstruction -/

/-- Executing an accepted extension column that separates the pair
kills the obstruction: remeasurement after structure creation
returns non-obstructed.  (The witnessing column enters the declared
observation, so the zero relation no longer holds on the pair.) -/
theorem extension_resolves (s : PState) (c : List Nat) (i j : Nat)
    (cols : List (List Nat)) (hcols : s.obs = some cols)
    (hok : colOk s c = true) (hsep : sepCol c i j = true)
    (hlic : s.licensed = true) (hbud : 0 < s.budget)
    (hh : s.halted = false) :
    obstP (step s (.addCol c)) i j = false := by
  have hguard : (colOk s c && s.licensed
      && decide (0 < s.budget)) = true := by
    rw [hok, hlic, decide_eq_true hbud]
    rfl
  have hstep : step s (.addCol c) =
      { s with obs := some (cols ++ [c]),
               budget := s.budget - 1 } := by
    simp only [step, hh]
    rw [if_neg (fun hc : false = true => Bool.noConfusion hc),
        if_pos hguard, hcols]
  rw [hstep]
  rw [obst_agrees_when_declared _ (cols ++ [c]) rfl i j]
  have hnew : zeroP (cols ++ [c]) i j = false := by
    unfold zeroP sepP
    have : ((cols ++ [c]).any fun d => sepCol d i j) = true :=
      List.any_eq_true.mpr ⟨c, by simp, hsep⟩
    rw [this]
    rfl
  rw [hnew]
  simp

/-! ## RepresentedNextFamily: the policy-driven closure family

The passage's last arrow: the next-event family is computed from the
represented state by a fixed interpreter — repair blocks for every
same-level repair of every obstructed protected pair, extension
blocks (funded and executed as separate events) for every proposal.
The generator's silence on quiescent states is a represented verdict
(`nextFamilyP_stop`); at an obstruction the family is provably
nonempty (`nextFamilyP_nonempty`).  The iteration of this family by
a driver remains metatheoretic, exactly as in the sealed
constitution — stated, not laundered. -/

def obstructedPairs (s : PState) : List (Nat × Nat) :=
  s.prot.filter (fun r => obstP s r.1 r.2)

def nextFamilyP (s : PState) : List (List PEvent) :=
  (obstructedPairs s).flatMap fun r =>
    (repairFamily s r.1 r.2).map
        (fun m => [PEvent.refineCol m.1 m.2])
      ++ (extensionProposals s r.1 r.2).map
          (fun c => [PEvent.setBudget 1, PEvent.addCol c])

/-- The stop outcome is represented: with no obstructed protected
pair the family is empty — silence is a verdict, not an exception. -/
theorem nextFamilyP_stop (s : PState)
    (hq : ∀ r ∈ s.prot, obstP s r.1 r.2 = false) :
    nextFamilyP s = [] := by
  unfold nextFamilyP obstructedPairs
  have hgen : ∀ (l : List (Nat × Nat)),
      (∀ r ∈ l, obstP s r.1 r.2 = false) →
        l.filter (fun r => obstP s r.1 r.2) = [] := by
    intro l hl
    induction l with
    | nil => rfl
    | cons r rest ih =>
        rw [List.filter_cons, hl r List.mem_cons_self,
          if_neg (fun hc : false = true => Bool.noConfusion hc)]
        exact ih (fun x hx => hl x (List.mem_cons_of_mem r hx))
  rw [hgen s.prot hq]
  rfl

/-- At an active obstruction the family is provably nonempty: the
always-available extension proposal contributes its funded block. -/
theorem nextFamilyP_nonempty (s : PState) (i j : Nat)
    (hobst : obstP s i j = true) (hij : i ≠ j)
    (hi : i < s.occ.length) (hprot : (i, j) ∈ s.prot) :
    [PEvent.setBudget 1, PEvent.addCol [i]] ∈ nextFamilyP s := by
  unfold nextFamilyP obstructedPairs
  apply List.mem_flatMap.mpr
  refine ⟨(i, j), ?_, ?_⟩
  · apply List.mem_filter.mpr
    exact ⟨hprot, hobst⟩
  · apply List.mem_append.mpr
    right
    apply List.mem_map.mpr
    exact ⟨[i],
      extension_always_available s i j hobst hij hi hprot, rfl⟩

/-- Completeness, repair side: every accepted separating same-level
move on an obstructed protected pair appears in the family as its
own block. -/
theorem nextFamilyP_complete_repair (s : PState) (i j : Nat)
    (m : List Nat × Nat) (hobst : obstP s i j = true)
    (hprot : (i, j) ∈ s.prot) (hm : m ∈ repairFamily s i j) :
    [PEvent.refineCol m.1 m.2] ∈ nextFamilyP s := by
  unfold nextFamilyP obstructedPairs
  apply List.mem_flatMap.mpr
  refine ⟨(i, j), List.mem_filter.mpr ⟨hprot, hobst⟩, ?_⟩
  apply List.mem_append.mpr
  left
  exact List.mem_map.mpr ⟨m, hm, rfl⟩

/-- Completeness, extension side: every proposal on an obstructed
protected pair appears as its own funded block. -/
theorem nextFamilyP_complete_ext (s : PState) (i j : Nat)
    (c : List Nat) (hobst : obstP s i j = true)
    (hprot : (i, j) ∈ s.prot)
    (hc : c ∈ extensionProposals s i j) :
    [PEvent.setBudget 1, PEvent.addCol c] ∈ nextFamilyP s := by
  unfold nextFamilyP obstructedPairs
  apply List.mem_flatMap.mpr
  refine ⟨(i, j), List.mem_filter.mpr ⟨hprot, hobst⟩, ?_⟩
  apply List.mem_append.mpr
  right
  exact List.mem_map.mpr ⟨c, hc, rfl⟩

end PrimitivePassage
