import Translation
import Chains

/-!
# Execution: represented operations drive a process

A finite setting is encoded as a regime whose operation graphs are the
instances of binary forms (`Translation.encode`: form `3 + k` carries the
graph of the `k`-th operation as instances `(3 + k, [x, y])`).  This module
runs a word of operation indices by *reading those instances*.  A
configuration carries the encoded graph, the remaining word, the active
datum and an output tape; one `step` consumes the head `k` of the word by
looking the instance `(3 + k, [active, y])` up in the graph and moving to
`y`; `run` is `iterate step` for the length of the word, by definition.

Nothing here reads the operation functions `F.ops`.  They enter once, in the
*statement* `lookup_encode` that reading the graph is faithful, through the
merged `Translation.derivable_op`; the machine never calls them.  The
reference evaluator `evalWord` reads the same graph through the same
`lookup`, so the correspondence `run_evalWord` relates two graph-readers
with different control structure (a configuration machine and a fold), and
`evalWord_encode` carries both to the merged `Chains.run`, which is the
`F.ops`-reading fold: that is the bridge from the represented machine to
the operations it represents.

Configuration status: **DECLARED_HOST_CONFIG**.  `Config` is a structure of
the metatheory whose `graph` field is a copy of the encoded instances.  The
process reads encoded data; it does not itself live in the sealed grammar.

The proofs unfold the machine's definitions by `show` and `change` rather
than by `simp`, so that no matcher equation is minted behind the
environment census.

AuthorityEffect: None.
-/

namespace Execution

open Derivation Translation

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

/-- A value read from the graph is an instance of the graph. -/
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

/-- An edge in the graph is found. -/
theorem lookup_isSome {f x y : Nat} {l : List Inst} (h : (f, [x, y]) ∈ l) :
    (lookup f x l).isSome = true := by
  change ((l.find? (isEdge f x)).map value).isSome = true
  cases hf : l.find? (isEdge f x) with
  | none => exact absurd (isEdge_self f x y) (List.find?_eq_none.mp hf (f, [x, y]) h)
  | some i => rfl

/-- **Reading the graph is faithful.**  At form `3 + k` from an admitted `x`,
the encoded graph reads the `k`-th operation's value.  This is the one place
`F.ops` appears, and only in the statement: the value is fixed by the merged
`derivable_op`, not read by the machine. -/
theorem lookup_encode (F : FiniteSetting) {k x : Nat} (hk : k < F.ops.length) (hx : x < F.n) :
    lookup (3 + k) x (encode F).insts = some (F.ops.getD k id x) := by
  have hmem : (3 + k, [x, F.ops.getD k id x]) ∈ (encode F).insts :=
    derivable_encode.mp ((derivable_op F hk hx).mpr rfl)
  have hsome := lookup_isSome hmem
  cases hl : lookup (3 + k) x (encode F).insts with
  | none =>
      rw [hl] at hsome
      cases hsome
  | some y =>
      have hy : (3 + k, [x, y]) ∈ (encode F).insts := lookup_mem hl
      rw [(derivable_op F hk hx).mp (derivable_encode.mpr hy)]

/-! ## 2. The configuration machine -/

/-- A configuration: the encoded graph, the remaining word of operation
indices, the active datum, and the output tape of data visited.
DECLARED_HOST_CONFIG: a metatheory structure carrying encoded data. -/
structure Config where
  graph : List Inst
  word : List Nat
  active : Nat
  output : List Nat

/-- One step: consume the head `k` of the word by reading the edge of form
`3 + k` leaving the active datum.  No word, or no edge, yields no step. -/
def step (c : Config) : Option Config :=
  match c.word with
  | [] => none
  | k :: w =>
    match lookup (3 + k) c.active c.graph with
    | none => none
    | some y => some ⟨c.graph, w, y, c.output ++ [y]⟩

/-- Iterate `step` a given number of times; a missing step is a refusal. -/
def iterate : Nat → Config → Option Config
  | 0, c => some c
  | n + 1, c =>
    match step c with
    | none => none
    | some c' => iterate n c'

/-- **Run** is `iterate step` for the length of the word, by definition. -/
def run (c : Config) : Option Config := iterate c.word.length c

/-- The reference evaluator: a fold over the word reading the same graph
through the same `lookup`. -/
def evalWord (graph : List Inst) : List Nat → Nat → Option Nat
  | [], a => some a
  | k :: w, a =>
    match lookup (3 + k) a graph with
    | none => none
    | some y => evalWord graph w y

/-- The initial configuration of a setting: its encoded instances as the
graph, a word, a start datum, an empty tape. -/
def init (F : FiniteSetting) (w : List Nat) (x : Nat) : Config :=
  ⟨(encode F).insts, w, x, []⟩

/-- Resume a halted configuration on a further word. -/
def resume (c : Config) (v : List Nat) : Option Config :=
  run ⟨c.graph, v, c.active, c.output⟩

theorem step_nil (g : List Inst) (a : Nat) (out : List Nat) : step ⟨g, [], a, out⟩ = none := rfl

theorem iterate_zero (c : Config) : iterate 0 c = some c := rfl

/-- The empty word is the unit: nothing is read and nothing moves. -/
theorem run_nil (g : List Inst) (a : Nat) (out : List Nat) :
    run ⟨g, [], a, out⟩ = some ⟨g, [], a, out⟩ := rfl

/-! ## 3. The configuration machine agrees with the reference -/

theorem iterate_evalWord (g : List Inst) :
    ∀ (w : List Nat) (a : Nat) (out : List Nat),
      (iterate w.length ⟨g, w, a, out⟩).map Config.active = evalWord g w a
  | [], _, _ => rfl
  | k :: w, a, out => by
      show (match (match lookup (3 + k) a g with
                   | none => none
                   | some y => some (⟨g, w, y, out ++ [y]⟩ : Config)) with
             | none => none
             | some c' => iterate w.length c').map Config.active =
           (match lookup (3 + k) a g with
             | none => none
             | some y => evalWord g w y)
      cases lookup (3 + k) a g with
      | none => rfl
      | some y => exact iterate_evalWord g w y (out ++ [y])

/-- **Correspondence.**  The active datum after a run is what the reference
fold computes. -/
theorem run_evalWord (c : Config) :
    (run c).map Config.active = evalWord c.graph c.word c.active := by
  rcases c with ⟨g, w, a, out⟩
  exact iterate_evalWord g w a out

/-- A run that halts has consumed its word. -/
theorem iterate_word (g : List Inst) :
    ∀ (w : List Nat) (a : Nat) (out : List Nat) (c : Config),
      iterate w.length ⟨g, w, a, out⟩ = some c → c.word = []
  | [], a, out, c, h => by
      have h' : some (⟨g, [], a, out⟩ : Config) = some c := h
      obtain rfl := Option.some.inj h'
      rfl
  | k :: w, a, out, c, h => by
      revert h
      show (match (match lookup (3 + k) a g with
                   | none => none
                   | some y => some (⟨g, w, y, out ++ [y]⟩ : Config)) with
             | none => none
             | some c' => iterate w.length c') = some c → c.word = []
      cases lookup (3 + k) a g with
      | none =>
          intro h
          cases h
      | some y => exact iterate_word g w y (out ++ [y]) c

theorem run_word {c c' : Config} (h : run c = some c') : c'.word = [] := by
  rcases c with ⟨g, w, a, out⟩
  exact iterate_word g w a out c' h

/-- A run that halts keeps its graph. -/
theorem iterate_graph (g : List Inst) :
    ∀ (w : List Nat) (a : Nat) (out : List Nat) (c : Config),
      iterate w.length ⟨g, w, a, out⟩ = some c → c.graph = g
  | [], a, out, c, h => by
      have h' : some (⟨g, [], a, out⟩ : Config) = some c := h
      obtain rfl := Option.some.inj h'
      rfl
  | k :: w, a, out, c, h => by
      revert h
      show (match (match lookup (3 + k) a g with
                   | none => none
                   | some y => some (⟨g, w, y, out ++ [y]⟩ : Config)) with
             | none => none
             | some c' => iterate w.length c') = some c → c.graph = g
      cases lookup (3 + k) a g with
      | none =>
          intro h
          cases h
      | some y => exact iterate_graph g w y (out ++ [y]) c

/-! ## 4. Concatenation: the machine is stepwise, not a whole-word fold -/

theorem evalWord_append (g : List Inst) :
    ∀ (u v : List Nat) (a : Nat),
      evalWord g (u ++ v) a = (evalWord g u a).bind (evalWord g v)
  | [], _, _ => rfl
  | k :: u, v, a => by
      show (match lookup (3 + k) a g with
            | none => none
            | some y => evalWord g (u ++ v) y) =
           (match lookup (3 + k) a g with
            | none => none
            | some y => evalWord g u y).bind (evalWord g v)
      cases lookup (3 + k) a g with
      | none => rfl
      | some y => exact evalWord_append g u v y

/-- Running `u ++ v` is running `u` and continuing with `v`. -/
theorem run_append (g : List Inst) (u v : List Nat) (a : Nat) (out : List Nat) :
    (run ⟨g, u ++ v, a, out⟩).map Config.active = (evalWord g u a).bind (evalWord g v) := by
  rw [run_evalWord]
  exact evalWord_append g u v a

/-- Iterating `a + b` steps is iterating `a` then `b`: a configuration
exists after any prefix of the word. -/
theorem iterate_add : ∀ (a b : Nat) (c : Config), iterate (a + b) c = (iterate a c).bind (iterate b)
  | 0, b, c => by
      rw [Nat.zero_add]
      rfl
  | a + 1, b, c => by
      rw [Nat.succ_add]
      show (match step c with
            | none => none
            | some c' => iterate (a + b) c') =
           (match step c with
            | none => none
            | some c' => iterate a c').bind (iterate b)
      cases step c with
      | none => rfl
      | some c' => exact iterate_add a b c'

/-! ## 5. The word-bridge: the machine computes the operations -/

/-- On the encoding, the graph-reading fold computes the merged `Chains.run`
— the `F.ops`-reading fold — by reading the graph alone. -/
theorem evalWord_encode (F : FiniteSetting) :
    ∀ (w : List Nat) (x : Nat), Chains.WordOk F w → x < F.n →
      evalWord (encode F).insts w x = some (Chains.run F w x)
  | [], _, _, _ => rfl
  | k :: w, x, hw, hx => by
      have hk := Chains.wordOk_head hw
      show (match lookup (3 + k) x (encode F).insts with
            | none => none
            | some y => evalWord (encode F).insts w y) =
           some (Chains.run F w (F.ops.getD k id x))
      rw [lookup_encode F hk hx]
      exact evalWord_encode F w (F.ops.getD k id x) (Chains.wordOk_tail hw)
        (Chains.follow_lt F hk hx)

/-- **The word-bridge.**  For every finite setting of the declared class and
every well-formed word, running the represented word from the encoded graph
halts with the word consumed and the active datum the operations compute.
`run` reads only encoded instances. -/
theorem run_encode (F : FiniteSetting) {w : List Nat} {x : Nat} (hw : Chains.WordOk F w)
    (hx : x < F.n) {c : Config} (h : run (init F w x) = some c) :
    c.active = Chains.run F w x ∧ c.word = [] := by
  refine ⟨?_, run_word h⟩
  have h1 := run_evalWord (init F w x)
  rw [h] at h1
  change some c.active = evalWord (encode F).insts w x at h1
  rw [evalWord_encode F w x hw hx] at h1
  exact Option.some.inj h1

/-- **Totality on well-formed input.**  A well-formed word from an admitted
datum runs to a halt. -/
theorem run_total (F : FiniteSetting) {w : List Nat} {x : Nat} (hw : Chains.WordOk F w)
    (hx : x < F.n) : ∃ c, run (init F w x) = some c := by
  have h1 := run_evalWord (init F w x)
  have h2 : evalWord (init F w x).graph (init F w x).word (init F w x).active =
      some (Chains.run F w x) := evalWord_encode F w x hw hx
  rw [h2] at h1
  cases hr : run (init F w x) with
  | none =>
      rw [hr] at h1
      cases h1
  | some c => exact ⟨c, rfl⟩

/-- The halted active datum stays in the carrier. -/
theorem run_lt (F : FiniteSetting) {w : List Nat} {x : Nat} (hw : Chains.WordOk F w)
    (hx : x < F.n) {c : Config} (h : run (init F w x) = some c) : c.active < F.n := by
  rw [(run_encode F hw hx h).1]
  exact Chains.run_lt F w x hw hx

end Execution

#print axioms Execution.isEdge_true
#print axioms Execution.isEdge_self
#print axioms Execution.value_edge
#print axioms Execution.lookup_mem
#print axioms Execution.lookup_isSome
#print axioms Execution.lookup_encode
#print axioms Execution.step_nil
#print axioms Execution.iterate_zero
#print axioms Execution.run_nil
#print axioms Execution.iterate_evalWord
#print axioms Execution.run_evalWord
#print axioms Execution.iterate_word
#print axioms Execution.run_word
#print axioms Execution.iterate_graph
#print axioms Execution.evalWord_append
#print axioms Execution.run_append
#print axioms Execution.iterate_add
#print axioms Execution.evalWord_encode
#print axioms Execution.run_encode
#print axioms Execution.run_total
#print axioms Execution.run_lt
