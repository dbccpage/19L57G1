/-!
# G012 Multi-Sorted Signatures and Typed Structures

Constructive inductive definitions of multi-sorted relational signatures
with constants, relations, and functions, alongside typed finite structure
representations and operational transition steps.

AuthorityEffect: None.
Axiom boundary: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
-/

namespace G012TypedTranslation

/-- Inductive sort identifier. -/
inductive SortId where
  | mk : String → SortId
  deriving DecidableEq, Repr

/-- Inductive constant symbol identifier. -/
inductive ConstId where
  | mk : String → ConstId
  deriving DecidableEq, Repr

/-- Inductive relation symbol identifier. -/
inductive RelId where
  | mk : String → RelId
  deriving DecidableEq, Repr

/-- Inductive function symbol identifier. -/
inductive FuncId where
  | mk : String → FuncId
  deriving DecidableEq, Repr

/-- Constant symbol declaration. -/
structure ConstDecl where
  id : ConstId
  sort : SortId
  deriving DecidableEq, Repr

/-- Relation symbol declaration with arity sorts. -/
structure RelDecl where
  id : RelId
  arity : List SortId
  deriving DecidableEq, Repr

/-- Function symbol declaration with argument sorts and target sort. -/
structure FuncDecl where
  id : FuncId
  arity : List SortId
  target : SortId
  deriving DecidableEq, Repr

/-- Multi-sorted relational signature. -/
structure Signature where
  sorts : List SortId
  consts : List ConstDecl
  rels : List RelDecl
  funcs : List FuncDecl
  deriving DecidableEq, Repr

/-- Element in a typed structure carrier. -/
structure Element where
  sort : SortId
  val : String
  deriving DecidableEq, Repr

/-- Constant binding. -/
structure ConstBinding where
  id : ConstId
  val : String
  deriving DecidableEq, Repr

/-- Relation tuple assertion. -/
structure RelTuple where
  rel : RelId
  args : List String
  deriving DecidableEq, Repr

/-- Function evaluation entry. -/
structure FuncEntry where
  func : FuncId
  args : List String
  val : String
  deriving DecidableEq, Repr

/-- Canonical finite typed structure over a signature. -/
structure TypedStructure where
  sig : Signature
  elements : List Element
  constBindings : List ConstBinding
  relTuples : List RelTuple
  funcEntries : List FuncEntry
  deriving DecidableEq, Repr

/-- Operational transitions on typed structures. -/
inductive StructureOp where
  | addElement (sort : SortId) (val : String)
  | setConstant (id : ConstId) (val : String)
  | addTuple (rel : RelId) (args : List String)
  | setFunctionValue (func : FuncId) (args : List String) (val : String)
  deriving DecidableEq, Repr

/-- Operational transition step applying StructureOp to TypedStructure. -/
def stepOp (s : TypedStructure) : StructureOp → TypedStructure
  | .addElement sort val =>
      { s with elements := ⟨sort, val⟩ :: s.elements }
  | .setConstant id val =>
      { s with constBindings := ⟨id, val⟩ :: s.constBindings }
  | .addTuple rel args =>
      { s with relTuples := ⟨rel, args⟩ :: s.relTuples }
  | .setFunctionValue func args val =>
      { s with funcEntries := ⟨func, args, val⟩ :: s.funcEntries }

/-! ## Structural Properties and Constructive Theorems -/

theorem sortId_inj (s1 s2 : String) (h : SortId.mk s1 = SortId.mk s2) : s1 = s2 := by
  cases h
  rfl

theorem constId_inj (c1 c2 : String) (h : ConstId.mk c1 = ConstId.mk c2) : c1 = c2 := by
  cases h
  rfl

theorem relId_inj (r1 r2 : String) (h : RelId.mk r1 = RelId.mk r2) : r1 = r2 := by
  cases h
  rfl

theorem funcId_inj (f1 f2 : String) (h : FuncId.mk f1 = FuncId.mk f2) : f1 = f2 := by
  cases h
  rfl

theorem element_eq (e1 e2 : Element) (h_sort : e1.sort = e2.sort) (h_val : e1.val = e2.val) : e1 = e2 := by
  cases e1; cases e2
  congr

theorem constDecl_eq (c1 c2 : ConstDecl) (h_id : c1.id = c2.id) (h_sort : c1.sort = c2.sort) : c1 = c2 := by
  cases c1; cases c2
  congr

theorem relDecl_eq (r1 r2 : RelDecl) (h_id : r1.id = r2.id) (h_ar : r1.arity = r2.arity) : r1 = r2 := by
  cases r1; cases r2
  congr

theorem funcDecl_eq (f1 f2 : FuncDecl) (h_id : f1.id = f2.id) (h_ar : f1.arity = f2.arity) (h_tgt : f1.target = f2.target) : f1 = f2 := by
  cases f1; cases f2
  congr

theorem constBinding_eq (b1 b2 : ConstBinding) (h_id : b1.id = b2.id) (h_val : b1.val = b2.val) : b1 = b2 := by
  cases b1; cases b2
  congr

theorem relTuple_eq (t1 t2 : RelTuple) (h_rel : t1.rel = t2.rel) (h_args : t1.args = t2.args) : t1 = t2 := by
  cases t1; cases t2
  congr

theorem funcEntry_eq (e1 e2 : FuncEntry) (h_func : e1.func = e2.func) (h_args : e1.args = e2.args) (h_val : e1.val = e2.val) : e1 = e2 := by
  cases e1; cases e2
  congr

theorem typedStructure_eq (s1 s2 : TypedStructure)
    (h_sig : s1.sig = s2.sig)
    (h_elems : s1.elements = s2.elements)
    (h_consts : s1.constBindings = s2.constBindings)
    (h_rels : s1.relTuples = s2.relTuples)
    (h_funcs : s1.funcEntries = s2.funcEntries) : s1 = s2 := by
  cases s1; cases s2
  congr

end G012TypedTranslation
