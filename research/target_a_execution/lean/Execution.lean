import Derivation.Basic

/-!
# Execution: Represented Operations and Parameterized Runner

Target A: Represented Execution Substrate.
A fixed deterministic interpreter executing encoded program graphs and data enablements
directly from stored carrier data without calling unencoded operation functions (F.ops).

Key theorems:
- lookup_mem: a looked-up edge is an instance in the graph.
- run_nil: running an empty word leaves configuration unchanged.
- run_evalWord: agreement between stepwise configuration runner and reference fold.
- stepDetOf_inr: moving to a next state requires firing exactly the unique enabled operation.
- stepDetOf_branch: two or more enabled operations cause explicit branch refusal (non-selection).
- fire_clock / fire_fuel / fire_tape: strict monotonicity and resource accounting.

Axiom boundary: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
AuthorityEffect: None.
Configuration status: DECLARED_HOST_CONFIG.
-/

namespace Execution

open Derivation

/-! ## 1. Reading the encoded graph -/

/-- Whether an instance is an edge of form `f` leaving `x`: `(f, [x, y])`. -/
def isEdge (f x : Nat) : Inst → Bool
  | (g, [x', _]) => decide (g = f ∧ x' = x)
  | _ => false

/-- The value an edge assigns: the second argument. -/
def value : Inst → Nat
  | (_, [_, y]) => y
  | _ => 0

/-- Read the graph: the value of the first edge of form `f` leaving `x`. -/
def lookup (f x : Nat) (l : List Inst) : Option Nat := (l.find? (isEdge f x)).map value

theorem isEdge_true {f x : Nat} : ∀ {i : Inst}, isEdge f x i = true → ∃ y, i = (f, [x, y])
  | (g, [x', y]), h => by
      have h' : decide (g = f ∧ x' = x) = true := h
      obtain ⟨rfl, rfl⟩ := of_decide_eq_true h'
      exact ⟨y, rfl⟩
  | (_, []), h => by cases h
  | (_, [_]), h => by cases h
  | (_, _ :: _ :: _ :: _), h => by cases h

theorem isEdge_self (f x y : Nat) : isEdge f x (f, [x, y]) = true := by
  show decide (f = f ∧ x = x) = true
  exact decide_eq_true ⟨rfl, rfl⟩

theorem value_edge (f x y : Nat) : value (f, [x, y]) = y := rfl

/-- A value read from the graph is an instance in the graph. -/
theorem lookup_mem {f x y : Nat} {l : List Inst} (h : lookup f x l = some y) : (f, [x, y]) ∈ l := by
  change (l.find? (isEdge f x)).map value = some y at h
  cases hf : l.find? (isEdge f x) with
  | none =>
      rw [hf] at h
      cases h
  | some i =>
      rw [hf] at h
      have hmem := List.mem_of_find?_eq_some hf
      have hedge := List.find?_some hf
      obtain ⟨y', rfl⟩ := isEdge_true hedge
      have hy : y' = y := Option.some.inj h
      subst hy
      exact hmem

/-- An edge in the graph is found by lookup. -/
theorem lookup_isSome {f x y : Nat} {l : List Inst} (h : (f, [x, y]) ∈ l) :
    (lookup f x l).isSome = true := by
  change ((l.find? (isEdge f x)).map value).isSome = true
  cases hf : l.find? (isEdge f x) with
  | none => exact absurd (isEdge_self f x y) (List.find?_eq_none.mp hf (f, [x, y]) h)
  | some i => rfl

/-! ## 2. The configuration word machine -/

/-- A configuration carrying graph, remaining word, active datum, and output tape. -/
structure Config where
  graph : List Inst
  word : List Nat
  active : Nat
  output : List Nat

/-- Step the word machine by reading the edge leaving the active datum. -/
def step (c : Config) : Option Config :=
  match c.word with
  | [] => none
  | k :: w =>
    match lookup (3 + k) c.active c.graph with
    | none => none
    | some y => some ⟨c.graph, w, y, c.output ++ [y]⟩

/-- Iterate stepping n times. -/
def iterate : Nat → Config → Option Config
  | 0, c => some c
  | n + 1, c =>
    match step c with
    | none => none
    | some c' => iterate n c'

/-- Run word machine for the length of the word. -/
def run (c : Config) : Option Config := iterate c.word.length c

/-- Reference fold reading graph instances through lookup. -/
def evalWord (graph : List Inst) : List Nat → Nat → Option Nat
  | [], a => some a
  | k :: w, a =>
    match lookup (3 + k) a graph with
    | none => none
    | some y => evalWord graph w y

theorem step_nil (g : List Inst) (a : Nat) (out : List Nat) :
    step ⟨g, [], a, out⟩ = none := rfl

theorem iterate_zero (c : Config) : iterate 0 c = some c := rfl

theorem run_nil (g : List Inst) (a : Nat) (out : List Nat) :
    run ⟨g, [], a, out⟩ = some ⟨g, [], a, out⟩ := rfl

theorem iterate_evalWord (g : List Inst) :
    ∀ (w : List Nat) (a : Nat) (out : List Nat),
      (iterate w.length ⟨g, w, a, out⟩).map Config.active = evalWord g w a
  | [], _, _ => rfl
  | k :: w, a, out => by
      dsimp [List.length, iterate, step, evalWord]
      cases hl : lookup (3 + k) a g with
      | none => rfl
      | some y => exact iterate_evalWord g w y (out ++ [y])

theorem run_evalWord (g : List Inst) (w : List Nat) (a : Nat) (out : List Nat) :
    (run ⟨g, w, a, out⟩).map Config.active = evalWord g w a :=
  iterate_evalWord g w a out

/-! ## 3. Data-driven Control, State, and Protection Obligations -/

inductive ProtectionKind
  | separated
  | collapsed
  | reflexive
deriving DecidableEq, Repr

structure ProtectionObligation where
  kind : ProtectionKind
  u : Nat
  v : Nat
deriving DecidableEq, Repr

structure State where
  graph : List Inst
  nops : Nat
  active : Nat
  tape : List Nat
  clock : Nat
  fuel : Nat
  obligations : List ProtectionObligation := []
  designatedPair : Option (Nat × Nat) := none

inductive Fired
  | ok (s : State)
  | exhausted
  | noEdge
  | protectionViolation

inductive Terminal
  | halt
  | exhausted
  | refuse
  | branch
deriving DecidableEq, Repr

/-- Operation k is enabled at datum x if its control form self-instance is present. -/
def enabled (g : List Inst) (nops x k : Nat) : Bool :=
  decide (lookup (3 + nops + k) x g = some x)

/-- The enabled operations at datum x, in index order. -/
def enabledAt (g : List Inst) (nops x : Nat) : List Nat :=
  (List.range nops).filter (fun k => enabled g nops x k)

def checkObligation (g : List Inst) (k : Nat) (obl : ProtectionObligation) : Option ProtectionObligation :=
  match obl.kind with
  | .separated =>
    if obl.u == obl.v then none
    else
      match lookup (3 + k) obl.u g, lookup (3 + k) obl.v g with
      | some u', some v' => if u' != v' then some ⟨.separated, u', v'⟩ else none
      | _, _ => none
  | .collapsed => none
  | .reflexive =>
    if obl.u != obl.v then none
    else
      match lookup (3 + k) obl.u g with
      | some u' => if u' == obl.u then some ⟨.reflexive, obl.u, obl.u⟩ else none
      | none => none

def checkDesignatedPair (g : List Inst) (k : Nat) : Option (Nat × Nat) → Option (Option (Nat × Nat))
  | none => some none
  | some (a, b) =>
    if a == b then none
    else
      match lookup (3 + k) a g, lookup (3 + k) b g with
      | some a', some b' => if a' != b' then some (some (a', b')) else none
      | _, _ => none

def checkAllObligations (g : List Inst) (k : Nat) :
    List ProtectionObligation → Option (List ProtectionObligation)
  | [] => some []
  | obl :: rest =>
    match checkObligation g k obl, checkAllObligations g k rest with
    | some obl', some rest' => some (obl' :: rest')
    | _, _ => none

/-- Fire operation k at the active datum, evaluating protection obligations and designated pair. -/
def fire (s : State) (k : Nat) : Fired :=
  match s.fuel with
  | 0 => .exhausted
  | f + 1 =>
    match lookup (3 + k) s.active s.graph with
    | none => .noEdge
    | some y =>
      match checkDesignatedPair s.graph k s.designatedPair,
            checkAllObligations s.graph k s.obligations with
      | some dp', some obls' =>
        .ok ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f, obls', dp'⟩
      | _, _ => .protectionViolation

theorem fire_exhausted {s : State} {k : Nat} (h : s.fuel = 0) : fire s k = .exhausted := by
  show (match s.fuel with
        | 0 => Fired.exhausted
        | f + 1 =>
          match lookup (3 + k) s.active s.graph with
          | none => Fired.noEdge
          | some y =>
            match checkDesignatedPair s.graph k s.designatedPair,
                  checkAllObligations s.graph k s.obligations with
            | some dp', some obls' =>
              Fired.ok ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f, obls', dp'⟩
            | _, _ => Fired.protectionViolation) = .exhausted
  rw [h]

theorem fire_succ (s : State) (k f : Nat) (hf : s.fuel = f + 1) :
    fire s k = (match lookup (3 + k) s.active s.graph with
                | none => Fired.noEdge
                | some y =>
                  match checkDesignatedPair s.graph k s.designatedPair,
                        checkAllObligations s.graph k s.obligations with
                  | some dp', some obls' =>
                    Fired.ok ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f, obls', dp'⟩
                  | _, _ => Fired.protectionViolation) := by
  show (match s.fuel with
        | 0 => Fired.exhausted
        | f' + 1 =>
          match lookup (3 + k) s.active s.graph with
          | none => Fired.noEdge
          | some y =>
            match checkDesignatedPair s.graph k s.designatedPair,
                  checkAllObligations s.graph k s.obligations with
            | some dp', some obls' =>
              Fired.ok ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f', obls', dp'⟩
            | _, _ => Fired.protectionViolation) = _
  rw [hf]

theorem fire_ok {s s' : State} {k : Nat} (h : fire s k = .ok s') :
    lookup (3 + k) s.active s.graph = some s'.active ∧ s'.tape = s.tape ++ [s'.active] ∧
      s'.clock = s.clock + 1 ∧ s.fuel = s'.fuel + 1 ∧ s'.graph = s.graph ∧ s'.nops = s.nops ∧
      ∃ dp' obls',
        checkDesignatedPair s.graph k s.designatedPair = some dp' ∧
        checkAllObligations s.graph k s.obligations = some obls' ∧
        s'.designatedPair = dp' ∧ s'.obligations = obls' := by
  obtain ⟨f, hf⟩ : ∃ f, s.fuel = f + 1 := by
    cases hfu : s.fuel with
    | zero =>
        rw [fire_exhausted hfu] at h
        cases h
    | succ f => exact ⟨f, rfl⟩
  rw [fire_succ s k f hf] at h
  cases hl : lookup (3 + k) s.active s.graph with
  | none =>
      rw [hl] at h
      cases h
  | some y =>
      rw [hl] at h
      cases hdp : checkDesignatedPair s.graph k s.designatedPair with
      | none =>
          rw [hdp] at h
          cases h
      | some dp' =>
          rw [hdp] at h
          cases hobl : checkAllObligations s.graph k s.obligations with
          | none =>
              rw [hobl] at h
              cases h
          | some obls' =>
              rw [hobl] at h
              have h'' : Fired.ok ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f, obls', dp'⟩ = Fired.ok s' := h
              cases h''
              exact ⟨rfl, rfl, rfl, hf, rfl, rfl, ⟨dp', obls', rfl, rfl, rfl, rfl⟩⟩

theorem fire_clock {s s' : State} {k : Nat} (h : fire s k = .ok s') : s'.clock = s.clock + 1 :=
  (fire_ok h).2.2.1

theorem fire_fuel {s s' : State} {k : Nat} (h : fire s k = .ok s') : s.fuel = s'.fuel + 1 :=
  (fire_ok h).2.2.2.1

theorem fire_tape {s s' : State} {k : Nat} (h : fire s k = .ok s') : s'.tape = s.tape ++ [s'.active] :=
  (fire_ok h).2.1

theorem fire_protection_preserved {s s' : State} {k : Nat} (h : fire s k = .ok s') :
    ∃ dp' obls',
      checkDesignatedPair s.graph k s.designatedPair = some dp' ∧
      checkAllObligations s.graph k s.obligations = some obls' ∧
      s'.designatedPair = dp' ∧ s'.obligations = obls' :=
  (fire_ok h).2.2.2.2.2.2

/-! ## 4. The Parameterized Deterministic Runner -/

abbrev Reader := State → List Nat

def ctrlReader (s : State) : List Nat := enabledAt s.graph s.nops s.active

/-- Parameterized deterministic step:
    - [] => halt
    - [k] => fires k
    - >= 2 ops => branch (explicit refusal to select) -/
def stepDetOf (read : Reader) (s : State) : Terminal ⊕ State :=
  match read s with
  | [] => .inl .halt
  | [k] =>
    match fire s k with
    | .ok s' => .inr s'
    | .exhausted => .inl .exhausted
    | .noEdge => .inl .refuse
    | .protectionViolation => .inl .refuse
  | _ :: _ :: _ => .inl .branch

def stepDet (s : State) : Terminal ⊕ State := stepDetOf ctrlReader s

def nextOf (read : Reader) (s : State) : State :=
  match stepDetOf read s with
  | .inr s' => s'
  | .inl _ => s

def iterOf (read : Reader) : Nat → State → State
  | 0, s => s
  | n + 1, s => nextOf read (iterOf read n s)

def obsOf (read : Reader) (n : Nat) (s : State) : List Nat := (iterOf read n s).tape

def runDetOf (read : Reader) : Nat → State → Terminal × State
  | 0, s =>
    match stepDetOf read s with
    | .inl t => (t, s)
    | .inr _ => (.exhausted, s)
  | b + 1, s =>
    match stepDetOf read s with
    | .inl t => (t, s)
    | .inr s' => runDetOf read b s'

def runDet (bound : Nat) (s : State) : Terminal × State := runDetOf ctrlReader bound s

theorem stepDetOf_inr {read : Reader} {s s' : State} (h : stepDetOf read s = .inr s') :
    ∃ k, read s = [k] ∧ fire s k = .ok s' := by
  revert h
  show (match read s with
        | [] => Sum.inl Terminal.halt
        | [k] =>
          match fire s k with
          | .ok t => Sum.inr t
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse
          | .protectionViolation => Sum.inl Terminal.refuse
        | _ :: _ :: _ => Sum.inl Terminal.branch) = Sum.inr s' → _
  cases hr : read s with
  | nil =>
      intro h
      cases h
  | cons k rest =>
      cases rest with
      | nil =>
          show (match fire s k with
                | .ok t => Sum.inr t
                | .exhausted => Sum.inl Terminal.exhausted
                | .noEdge => Sum.inl Terminal.refuse
                | .protectionViolation => Sum.inl Terminal.refuse) = Sum.inr s' → _
          cases hf : fire s k with
          | ok t =>
              intro h
              injection h with ht
              subst ht
              exact ⟨k, rfl, hf⟩
          | exhausted =>
              intro h
              cases h
          | noEdge =>
              intro h
              cases h
          | protectionViolation =>
              intro h
              cases h
      | cons k' rest' =>
          intro h
          cases h

theorem stepDetOf_branch {read : Reader} {s : State} {k1 k2 : Nat} {rest : List Nat}
    (h : read s = k1 :: k2 :: rest) : stepDetOf read s = .inl .branch := by
  have hstep : stepDetOf read s =
      (match read s with
      | [] => .inl .halt
      | [k] =>
        match fire s k with
        | .ok s' => .inr s'
        | .exhausted => .inl .exhausted
        | .noEdge => .inl .refuse
        | .protectionViolation => .inl .refuse
      | _ :: _ :: _ => .inl .branch) := rfl
  rw [hstep, h]

theorem stepDetOf_halt {read : Reader} {s : State} (h : read s = []) :
    stepDetOf read s = .inl .halt := by
  have hstep : stepDetOf read s =
      (match read s with
      | [] => .inl .halt
      | [k] =>
        match fire s k with
        | .ok s' => .inr s'
        | .exhausted => .inl .exhausted
        | .noEdge => .inl .refuse
        | .protectionViolation => .inl .refuse
      | _ :: _ :: _ => .inl .branch) := rfl
  rw [hstep, h]

theorem refusal_preserves_state {read : Reader} {s : State} {t : Terminal}
    (h : stepDetOf read s = .inl t) : nextOf read s = s := by
  unfold nextOf
  rw [h]

theorem stepDetOf_refuse_protectionViolation {read : Reader} {s : State} {k : Nat}
    (hr : read s = [k]) (hf : fire s k = .protectionViolation) :
    stepDetOf read s = .inl .refuse := by
  have hstep : stepDetOf read s =
      (match read s with
      | [] => .inl .halt
      | [k] =>
        match fire s k with
        | .ok s' => .inr s'
        | .exhausted => .inl .exhausted
        | .noEdge => .inl .refuse
        | .protectionViolation => .inl .refuse
      | _ :: _ :: _ => .inl .branch) := rfl
  rw [hstep, hr]
  dsimp
  rw [hf]

theorem stepDetOf_refuse_noEdge {read : Reader} {s : State} {k : Nat}
    (hr : read s = [k]) (hf : fire s k = .noEdge) :
    stepDetOf read s = .inl .refuse := by
  have hstep : stepDetOf read s =
      (match read s with
      | [] => .inl .halt
      | [k] =>
        match fire s k with
        | .ok s' => .inr s'
        | .exhausted => .inl .exhausted
        | .noEdge => .inl .refuse
        | .protectionViolation => .inl .refuse
      | _ :: _ :: _ => .inl .branch) := rfl
  rw [hstep, hr]
  dsimp
  rw [hf]

theorem nextOf_tape {read : Reader} {s : State} :
    s.tape <+: (nextOf read s).tape := by
  unfold nextOf
  cases hs : stepDetOf read s with
  | inl t =>
      exact List.prefix_rfl
  | inr s' =>
      obtain ⟨k, _, hfire⟩ := stepDetOf_inr hs
      rw [fire_tape hfire]
      exact List.prefix_append _ _

end Execution
