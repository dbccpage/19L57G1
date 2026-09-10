import Signature

/-!
# Constructive Codec, Inversion, and Step Commutation

Constructive encoder and decoder mapping between typed finite structures
and the five-part relational carrier (data, forms, insts, rules, reqs).
Proves exact round-trip invertibility, structured refusal preservation,
and operational transition commutation.

AuthorityEffect: None.
Axiom boundary: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
-/

namespace G012TypedTranslation

/-! ## 1. Relational Carrier Grammar -/

inductive DataToken where
  | elements : List Element → DataToken
  | malformed : String → DataToken
  deriving DecidableEq, Repr

inductive FormToken where
  | sig : Signature → FormToken
  | malformed : String → FormToken
  deriving DecidableEq, Repr

inductive InstToken where
  | insts : List ConstBinding → List RelTuple → InstToken
  | malformed : String → InstToken
  deriving DecidableEq, Repr

inductive RuleToken where
  | rules : List FuncEntry → RuleToken
  | malformed : String → RuleToken
  deriving DecidableEq, Repr

inductive ReqToken where
  | reqs : List Element → ReqToken
  | malformed : String → ReqToken
  deriving DecidableEq, Repr

structure RelationalState where
  data : List DataToken
  forms : List FormToken
  insts : List InstToken
  rules : List RuleToken
  reqs : List ReqToken
  deriving DecidableEq, Repr

/-! ## 2. Structured Refusals and Result Monad -/

inductive Refusal where
  | malformedEncoding (msg : String)
  | invalidSignature (msg : String)
  | carrierMismatch (msg : String)
  deriving DecidableEq, Repr

inductive Result (α : Type) (ε : Type) where
  | ok : α → Result α ε
  | err : ε → Result α ε
  deriving DecidableEq, Repr

/-! ## 3. Bidirectional Encoding and Decoding -/

def encode (s : TypedStructure) : RelationalState :=
  { data := [.elements s.elements],
    forms := [.sig s.sig],
    insts := [.insts s.constBindings s.relTuples],
    rules := [.rules s.funcEntries],
    reqs := [.reqs s.elements] }

def decode (r : RelationalState) : Result TypedStructure Refusal :=
  match r.data, r.forms, r.insts, r.rules with
  | [.malformed msg], _, _, _ => .err (.malformedEncoding msg)
  | _, [.malformed msg], _, _ => .err (.malformedEncoding msg)
  | _, _, [.malformed msg], _ => .err (.malformedEncoding msg)
  | _, _, _, [.malformed msg] => .err (.malformedEncoding msg)
  | [.elements elems], [.sig sig], [.insts cb rt], [.rules fe] =>
      .ok ⟨sig, elems, cb, rt, fe⟩
  | _, _, _, _ =>
      .err (.malformedEncoding "Unrecognized relational carrier token structure")

/-! ## 4. Operational Relational Transitions -/

structure RelationalOp where
  addedElements : List Element := []
  addedConstants : List ConstBinding := []
  addedTuples : List RelTuple := []
  addedFuncEntries : List FuncEntry := []
  deriving DecidableEq, Repr

def encodeOp (_s : TypedStructure) : StructureOp → RelationalOp
  | .addElement sort val =>
      { addedElements := [⟨sort, val⟩] }
  | .setConstant id val =>
      { addedConstants := [⟨id, val⟩] }
  | .addTuple rel args =>
      { addedTuples := [⟨rel, args⟩] }
  | .setFunctionValue func args val =>
      { addedFuncEntries := [⟨func, args, val⟩] }

def stepRelational (r : RelationalState) (op : RelationalOp) : RelationalState :=
  let nextData := match r.data with
    | [.elements es] => [.elements (op.addedElements ++ es)]
    | other => other
  let nextInsts := match r.insts with
    | [.insts cb rt] => [.insts (op.addedConstants ++ cb) (op.addedTuples ++ rt)]
    | other => other
  let nextRules := match r.rules with
    | [.rules fe] => [.rules (op.addedFuncEntries ++ fe)]
    | other => other
  let nextReqs := match r.reqs with
    | [.reqs reqElems] => [.reqs (op.addedElements ++ reqElems)]
    | other => other
  { data := nextData,
    forms := r.forms,
    insts := nextInsts,
    rules := nextRules,
    reqs := nextReqs }

/-! ## 5. Core Theorems -/

/-- Round-trip inversion theorem: decode(encode(S)) == ok(S). -/
theorem decode_encode_inversion (s : TypedStructure) :
    decode (encode s) = Result.ok s := by
  rfl

/-- Refusal preservation theorem: corrupted carrier maps to structured refusal. -/
theorem refusal_preservation (msg : String) (s : TypedStructure) :
    decode { encode s with data := [.malformed msg] } = Result.err (.malformedEncoding msg) := by
  rfl

/-- Refusal preservation on corrupted forms. -/
theorem refusal_preservation_forms (msg : String) (s : TypedStructure) :
    decode { encode s with forms := [.malformed msg] } = Result.err (.malformedEncoding msg) := by
  rfl

/-- Operational transition commutation theorem:
    encode(stepOp s op) == stepRelational (encode s) (encodeOp s op). -/
theorem step_commutation (s : TypedStructure) (op : StructureOp) :
    encode (stepOp s op) = stepRelational (encode s) (encodeOp s op) := by
  cases op <;> rfl

theorem step_commutation_addElement (s : TypedStructure) (sort : SortId) (val : String) :
    encode (stepOp s (.addElement sort val)) = stepRelational (encode s) (encodeOp s (.addElement sort val)) := by
  rfl

theorem step_commutation_setConstant (s : TypedStructure) (id : ConstId) (val : String) :
    encode (stepOp s (.setConstant id val)) = stepRelational (encode s) (encodeOp s (.setConstant id val)) := by
  rfl

theorem step_commutation_addTuple (s : TypedStructure) (rel : RelId) (args : List String) :
    encode (stepOp s (.addTuple rel args)) = stepRelational (encode s) (encodeOp s (.addTuple rel args)) := by
  rfl

theorem step_commutation_setFunctionValue (s : TypedStructure) (func : FuncId) (args : List String) (val : String) :
    encode (stepOp s (.setFunctionValue func args val)) = stepRelational (encode s) (encodeOp s (.setFunctionValue func args val)) := by
  rfl

end G012TypedTranslation
