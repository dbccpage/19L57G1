# Unit 51. Separate the witness, the laws, and the allowed operations

**Claim.** Nine predicates on one declared setting separate relation witnesses,
laws, stores, and allowed operations. There are 17 proved implications,
51 proved countermodels, and four recorded open locatedness cells;
the open labels are not independence theorems.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** `PrimitiveCore` puts every datum the candidate readings of a
primitive difference mention into one signature `Setting` (a carrier, an
asserted relation, two endpoints, a retention store, a protected-demand
store, an admitted operation family) and defines nine predicates on it:
W (bare witnessed pair), A (witnessed irreflexive), Bs, Bc, Bl (A plus
symmetry, cotransitivity, locatedness), C (witness plus demand), D
(endpoints do not factor through a point), E (no admitted composite
identifies the endpoints), F (A plus retention plus demand).

Of the 72 ordered cells (P, Q), P ≠ Q, 68 have named theorems:
17 implications `imp_P_Q` for every Setting and 51 countermodels
`nimp_P_Q` on carriers of one, two or three points. Four cells targeting
Bl remain recorded OPEN; their labels are data, not proofs.

Beside the matrix: `D_iff_ne` (D is metatheoretic inequality),
`cotrans_auto_on_two` (irreflexive on two points implies cotransitive),
`located_of_decidable`, `e_empty_iff_d`, `prot_not_from_witness`,
`ret_not_from_witness`, `bool_class`.

**Status:** FROZEN (implications,
countermodels), OPEN (four located cells, scoped), VERIFIED_FINITE (the
Python scan of 56 088 settings agrees cell by cell). **Lean:**
`lean4/Derivation/PrimitiveCore.lean` lines 36-916, imports `PrimDiff`.
**Axioms:** 81 exported reports within `{propext, Quot.sound}`; most use
none. **Depends on:** Unit 14 (`factors_through_point_iff`), Unit 23
(`selfdiff_consistent`), Unit 24 (`irrefl_witness_ne`), Unit 25
(`obstruction_under_irrefl`), the two-point carriers `D2`, `S2` and the
closure `Clos` / `Irred` of `PrimDiff`.

</details>

## First pass

Draw an arrow when the declared relation holds. The names A and B
designate endpoints; two names need not designate different points.

| Setting | Arrow A to B? | No point has a self-arrow? | A and B unequal? |
|---|---|---|---|
| One point with a loop; both names designate it | Yes | No | No |
| Two points; one arrow from A to B | Yes | Yes | Yes |
| Two points; no arrows | No | Yes | Yes |

An asserted arrow alone does not establish inequality. Adding the law
“no self-arrows” does: equal endpoints would turn the witnessed arrow
into a forbidden loop.

Now ask a different question: can an allowed transformation merge the
endpoints? With no generators admitted, identity still belongs to the
operation closure and keeps two distinct points apart. Admit a constant
map sending both to A, and they can merge. The original arrow can remain.

**Predict:** does finding no countermodel in the finite Boolean tables
settle an open implication for arbitrary proposition-valued relations?

<details>
<summary>Check your prediction</summary>

No. Those tables explicitly decide their entries. A finite carrier alone
does not supply decisions for an arbitrary relation. Read an open cell
as a remaining obligation, not as a proved implication or impossibility.

</details>

## Question

"A primitive difference" has been read nine ways across the earlier
units. Which readings force the two endpoints apart, which follow from
which, and what does each extra law or store cost? And where does the
matrix stop being able to answer?

## What we already possess

- A relation `r` on a type, irreflexivity (`∀ x, ¬ r x x`), the
  oriented pair `D2` and its symmetrisation `S2` on `Bool` (Units 14,
  23, 24).
- `irrefl_witness_ne`: an irreflexive witness `r a b` gives `a ≠ b`
  (Unit 24); `factors_through_point_iff`: `a = b` exactly when the
  selection factors through `Unit` (Unit 14).
- `Clos F`, the closure of an operation family under identity and
  composition, and `Irred F a b`: no closed map identifies `a` and `b`
  (`PrimDiff`); `merger_erases`, `irred_empty_iff_ne`.
- `bool_irrefl_witness_classification`: on `Bool` with endpoints
  `false, true`, an irreflexive witnessed relation is `D2` or `S2`.

## New concept: one signature, nine predicates, a decided matrix

A *Setting* fixes everything at once, so that "P implies Q" is a
statement over one class of models and a countermodel is one explicit
structure. The *matrix* is the 9 × 9 table of ordered pairs. A cell is
IMPLIES when `∀ S, P S → Q S` is proved, COUNTERMODEL when `∃ S, P S ∧
¬ Q S` is proved by naming `S`, OPEN when neither is proved and the
reason is recorded. *Minimum carrier* for a countermodel means: no
countermodel on fewer points exists, proved for the two cases the paper
cites (`cotrans_auto_on_two`, `no_witness_on_subsingleton`).

## Plain-language interpretation

Put the nine readings side by side and ask, for each pair, "if the
first holds, must the second?". The answer is yes in 17 cases, no in 51
with a small picture showing why, and unsettled in 4.

The three facts worth carrying out of the matrix. First, a witness
alone does not force unequal endpoints: the one-point model where the
single point is "different from itself" satisfies W and none of the
other eight readings. This particular countermodel does not say that
every witnessed relation is a self-relation. Add the law "no
point differs from itself" and the endpoints come apart (A → D). Second,
a demand is not a fact: the same one-point self-difference with
everything retained and protected satisfies C, and still its two
endpoints are one point. Third, irreducibility is relative to what you
admit: with no operation generators, the closure still contains identity.
Then "no map in the closure merges the endpoints" is exactly "the
endpoints differ"; admit one constant map and it fails,
while the witness and the law stand untouched.

The four OPEN cells are a different kind of fact. Locatedness asks for
a Boolean function realising the relation. The explicit Boolean tables
in the finite scan decide each entry, so they are located and cannot
refute an implication from A to Bl. A finite carrier alone does not
supply decisions for an arbitrary proposition-valued relation. The
book example below makes that distinction precise. The four general
implications are neither proved nor refuted here; this is not a proof
of their independence or of impossibility of further formal work.

## Pseudocode

```
Setting = (X, r, a, b, ret, prot, Ops)
W  = r a b
A  = W ∧ irreflexive r
Bs = A ∧ symmetric r         Bc = A ∧ cotransitive r       Bl = A ∧ located r
C  = W ∧ prot a b
D  = ¬ (a and b both the image of a one-point map)   -- i.e. a ≠ b
E  = ∀ f ∈ Clos Ops, f a ≠ f b
F  = A ∧ ret a b ∧ prot a b
for P ≠ Q: IMPLIES if proved ∀S; COUNTERMODEL if some named S has P ∧ ¬Q; else OPEN
```

## Python

Genesis's `code/derivation/primitive_core.py` enumerates every Setting
on one, two and three points with the declared store and operation
choices, evaluates the nine readings (`evaluate`), scans for the
key-minimal countermodel where one is found (`scan_settings`), and checks
the result against the declared matrix labels (`matrix_report`, raising on any
mismatch). Its output is `artifacts/primitive_implication_matrix.json`
and `artifacts/primitive_candidates.json`.

```python
def evaluate(s: Setting) -> dict[str, bool]:
    w = (s.a, s.b) in s.r
    a = w and irreflexive(s.r)
    return {
        "W": w, "A": a,
        "Bs": a and symmetric(s.r),
        "Bc": a and cotransitive(s.n, s.r),
        "Bl": a,
        "C": w and (s.a, s.b) in s.prot,
        "D": s.a != s.b,
        "E": all(f[s.a] != f[s.b] for f in closure_cached(s.n, s.ops)),
        "F": a and (s.a, s.b) in s.ret and (s.a, s.b) in s.prot,
    }
```

The check's run:

```text
settings scanned: 56088; candidate extents {'W': 28044, 'A': 2352, 'Bs': 312, 'Bc': 1272, 'Bl': 2352, 'C': 14022, 'D': 37248, 'E': 24832, 'F': 588}
the matrix (row = source, column = target; I implies, C countermodel, O open):
        W   A  Bs  Bc  Bl   C   D   E   F
    W   .   C   C   C   C   C   C   C   C
    A   I   .   C   C   O   C   I   C   C
   Bs   I   I   .   C   O   C   I   C   C
   Bc   I   I   C   .   O   C   I   C   C
   Bl   I   I   C   C   .   C   I   C   C
    C   I   C   C   C   C   .   C   C   C
    D   C   C   C   C   C   C   .   C   C
    E   C   C   C   C   C   C   I   .   C
    F   I   I   C   C   O   I   I   C   .
  tally {'IMPLIES': 17, 'COUNTERMODEL': 51, 'OPEN_LOCATED': 4}; expected_equals_computed True
the cells the lesson teaches, with the key-minimal witness found by the scan and Lean's name:
    W->D: COUNTERMODEL nimp_w_d     n=1 r=[(0, 0)] a=0 b=0 ret=[] prot=[] ops=0
    A->D: IMPLIES      imp_a_d      (implication)
    C->A: COUNTERMODEL nimp_c_a     n=1 r=[(0, 0)] a=0 b=0 ret=[] prot=[(0, 0)] ops=0
    C->D: COUNTERMODEL nimp_c_d     n=1 r=[(0, 0)] a=0 b=0 ret=[] prot=[(0, 0)] ops=0
    E->D: IMPLIES      imp_e_d      (implication)
    D->E: COUNTERMODEL nimp_d_e     n=2 r=[] a=0 b=1 ret=[] prot=[] ops=1
    A->E: COUNTERMODEL nimp_a_e     n=2 r=[(0, 1)] a=0 b=1 ret=[] prot=[] ops=1
   A->Bc: COUNTERMODEL nimp_a_bc    n=3 r=[(0, 1)] a=0 b=1 ret=[] prot=[] ops=0
  Bs->Bc: COUNTERMODEL nimp_bs_bc   n=3 r=[(0, 1), (1, 0)] a=0 b=1 ret=[] prot=[] ops=0
   A->Bs: COUNTERMODEL nimp_a_bs    n=2 r=[(0, 1)] a=0 b=1 ret=[] prot=[] ops=0
    A->C: COUNTERMODEL nimp_a_c     n=2 r=[(0, 1)] a=0 b=1 ret=[] prot=[] ops=0
    A->F: COUNTERMODEL nimp_a_f     n=2 r=[(0, 1)] a=0 b=1 ret=[] prot=[] ops=0
    F->C: IMPLIES      imp_f_c      (implication)
    D->W: COUNTERMODEL nimp_d_w     n=2 r=[] a=0 b=1 ret=[] prot=[] ops=0
    E->W: COUNTERMODEL nimp_e_w     n=2 r=[] a=0 b=1 ret=[] prot=[] ops=0
   A->Bl: OPEN_LOCATED open_cell_a_bl no finite countermodel can exist (every finite decidable relation is located)
  Bc->Bl: OPEN_LOCATED open_cell_bc_bl no finite countermodel can exist (every finite decidable relation is located)
  Bs->Bl: OPEN_LOCATED open_cell_bs_bl no finite countermodel can exist (every finite decidable relation is located)
   F->Bl: OPEN_LOCATED open_cell_f_bl no finite countermodel can exist (every finite decidable relation is located)
cotransitivity first bites at three points:
  any A-but-not-Bc setting on at most two points: False; the key-minimal A->Bc witness has n = 3
  Lean's `tri` evaluated: {'W': True, 'A': True, 'Bs': False, 'Bc': False, 'Bl': True, 'C': False, 'D': True, 'E': True, 'F': False}
Lean's one- and two-point models evaluated:
    unitBare: W=T A=F Bs=F Bc=F Bl=F C=F D=F E=F F=F  as Lean proves: True
    unitFull: W=T A=F Bs=F Bc=F Bl=F C=T D=F E=F F=F  as Lean proves: True
      d2Bare: W=T A=T Bs=F Bc=T Bl=T C=F D=T E=T F=F  as Lean proves: True
    d2Merged: W=T A=T Bs=F Bc=T Bl=T C=F D=T E=F F=F  as Lean proves: True
      s2Bare: W=T A=T Bs=T Bc=T Bl=T C=F D=T E=T F=F  as Lean proves: True
   boolEmpty: W=F A=F Bs=F Bc=F Bl=F C=F D=T E=T F=F  as Lean proves: True
two-element classification: survivors [{'label': 'oriented', 'r': [[0, 1]]}, {'label': 'symmetric', 'r': [[0, 1], [1, 0]]}] (count 2)
artifacts: matrix equals True; candidates equals True; Bl equals A in the finite universe: True
failures: []
```

## Line-by-line Python explanation

`evaluate` is the nine definitions on a finite table: `W` is
membership of the pair, `A` adds the irreflexivity check, `Bs` and `Bc`
add symmetry and cotransitivity by exhaustive loops, `C` reads the
demand store, `D` is Python inequality, `E` computes the closure of the
operation family under composition and tests every member, `F` reads
both stores. `Bl` is set equal to `A`: on a finite table every relation
is decidable and so located, which is the reason the four OPEN cells
have no countermodel in this universe.

The matrix block prints the 72 cells from the report and tallies them.
The teaching block prints, for each cell the lesson discusses, the
status, the Lean theorem name the mirror computes from the status
(`lean_tag`), and the *key-minimal* witness: the scan orders witnesses
by carrier size first, then relation size, then store sizes, so the
printed witness is the smallest in that declared order, not merely
some witness. Note the two one-point witnesses for the C row and the
three-point witnesses for the two cotransitivity cells.

The cotransitivity block asks the scan whether any setting on at most
two points is A and not Bc: none, matching `cotrans_auto_on_two`. The
model block re-evaluates Lean's six smallest named models and checks
each against the facts Lean proves about it. Then the two-point
classification and the two artifacts.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/PrimitiveCore.lean lines 36-105
structure Setting where
  X : Type
  r : X → X → Prop
  a : X
  b : X
  ret : X → X → Prop
  prot : X → X → Prop
  Ops : (X → X) → Prop

def Cotrans {X : Type} (r : X → X → Prop) : Prop :=
  ∀ x y, r x y → ∀ z, r x z ∨ r z y

def Located {X : Type} (r : X → X → Prop) : Prop :=
  ∃ f : X → X → Bool, ∀ x y, r x y ↔ f x y = true

theorem located_of_decidable {X : Type} (r : X → X → Prop)
    [inst : ∀ x y, Decidable (r x y)] : Located r :=
  ⟨fun x y => decide (r x y), fun _x _y =>
    ⟨fun h => decide_eq_true h, fun h => of_decide_eq_true h⟩⟩

def W (S : Setting) : Prop := S.r S.a S.b
def A (S : Setting) : Prop := S.r S.a S.b ∧ PrimDiff.Irrefl S.r
def Bs (S : Setting) : Prop := A S ∧ (∀ x y, S.r x y → S.r y x)
def Bc (S : Setting) : Prop := A S ∧ Cotrans S.r
def Bl (S : Setting) : Prop := A S ∧ Located S.r
def C (S : Setting) : Prop := S.r S.a S.b ∧ S.prot S.a S.b
def D (S : Setting) : Prop :=
  ¬ ∃ p : Unit → S.X, p () = S.a ∧ p () = S.b
def E (S : Setting) : Prop := PrimDiff.Irred S.Ops S.a S.b
def F (S : Setting) : Prop := A S ∧ S.ret S.a S.b ∧ S.prot S.a S.b

theorem D_iff_ne : ∀ S : Setting, D S ↔ S.a ≠ S.b := fun S =>
  ⟨fun hd he => hd ((PrimDiff.factors_through_point_iff S.a S.b).mpr he),
   fun hne hex => hne ((PrimDiff.factors_through_point_iff S.a S.b).mp hex)⟩
```

```lean
-- Lean (Genesis), lean4/Derivation/PrimitiveCore.lean lines 113-123, 156-176, 240-260, 404-414
theorem cotrans_auto_on_two (r : Bool → Bool → Prop)
    (hi : PrimDiff.Irrefl r) : Cotrans r := by
  intro x y hxy z
  have hne : x ≠ y := PrimDiff.irrefl_witness_ne hi hxy
  cases x <;> cases y <;> cases z
  · exact absurd rfl hne
  · exact absurd rfl hne
  · exact Or.inr hxy
  · exact Or.inl hxy
  · exact Or.inl hxy
  · exact Or.inr hxy
  · exact absurd rfl hne
  · exact absurd rfl hne

def unitBare : Setting where
  X := Unit
  r := fun _ _ => True
  a := ()
  b := ()
  ret := fun _ _ => False
  prot := fun _ _ => False
  Ops := fun _ => False

def d2Bare : Setting where
  X := Bool
  r := PrimDiff.D2
  a := false
  b := true
  ret := fun _ _ => False
  prot := fun _ _ => False
  Ops := fun _ => False

def triR : Fin 3 → Fin 3 → Prop := fun x y => x = 0 ∧ y = 1

def tri : Setting where
  X := Fin 3
  r := triR
  a := 0
  b := 1
  ret := fun _ _ => False
  prot := fun _ _ => False
  Ops := fun _ => False

theorem tri_not_bc : ¬ Bc tri := by
  intro hbc
  have hsplit : triR 0 2 ∨ triR 2 1 :=
    hbc.2 (0 : Fin 3) (1 : Fin 3) triR_edge (2 : Fin 3)
  cases hsplit with
  | inl hl =>
      have hl' : (0 : Fin 3) = 0 ∧ (2 : Fin 3) = 1 := hl
      exact absurd hl'.2 (by decide)
  | inr hr =>
      have hr' : (2 : Fin 3) = 0 ∧ (1 : Fin 3) = 1 := hr
      exact absurd hr'.1 (by decide)
```

```lean
-- Lean (Genesis), lean4/Derivation/PrimitiveCore.lean lines 500-562, 660-677, 715-716, 748-749, 792-820
theorem nimp_w_d : ∃ S : Setting, W S ∧ ¬ D S :=
  ⟨unitBare, unitBare_w, unitBare_not_d⟩

theorem nimp_a_bc : ∃ S : Setting, A S ∧ ¬ Bc S :=
  ⟨tri, tri_a, tri_not_bc⟩

def open_cell_a_bl : String :=
  "OPEN: no internal countermodel exists (every decidable relation is located, located_of_decidable); underivability of Located from the candidate laws is metatheoretic; Located is admitted as separate data"

theorem imp_a_d : ∀ S : Setting, A S → D S := fun S h =>
  (D_iff_ne S).mpr (PrimDiff.irrefl_witness_ne h.2 h.1)

theorem nimp_a_e : ∃ S : Setting, A S ∧ ¬ E S :=
  ⟨d2Merged, d2Merged_a, d2Merged_not_e⟩

theorem nimp_c_a : ∃ S : Setting, C S ∧ ¬ A S :=
  ⟨unitFull, unitFull_c, unitFull_not_a⟩

theorem nimp_c_d : ∃ S : Setting, C S ∧ ¬ D S :=
  ⟨unitFull, unitFull_c, unitFull_not_d⟩

theorem nimp_d_e : ∃ S : Setting, D S ∧ ¬ E S :=
  ⟨boolEmptyMerged, boolEmptyMerged_d, boolEmptyMerged_not_e⟩

theorem imp_e_d : ∀ S : Setting, E S → D S := fun S h =>
  (D_iff_ne S).mpr (h id PrimDiff.Clos.id)

theorem e_empty_iff_d : ∀ S : Setting,
    S.Ops = (fun _ => False) → (E S ↔ D S) := by
  intro S h
  unfold E
  rw [h]
  exact (PrimDiff.irred_empty_iff_ne S.a S.b).trans (D_iff_ne S).symm

theorem prot_not_from_witness : ∃ S : Setting, A S ∧ ¬ S.prot S.a S.b :=
  ⟨d2Bare, d2Bare_a, fun h => h⟩

theorem ret_not_from_witness : ∃ S : Setting, A S ∧ ¬ S.ret S.a S.b :=
  ⟨d2Bare, d2Bare_a, fun h => h⟩

theorem f_ops_irrelevant : ∀ S : Setting, ∀ O' : (S.X → S.X) → Prop,
    F { S with Ops := O' } ↔ F S := fun _ _ => Iff.rfl
```

The book's Lean tallies the exported table in Lean (Genesis proves
only its length), assembles all nine readings on one model from the
model facts, chains two implications into a third cell, checks the
cotransitivity split at the third point, exhibits the merger inside the
closure, and adds a model of its own.

```lean
-- Lean (book), textbook/checks/u51_lean.py
theorem tally :
    (matrixCells.filter (fun c => c.2.2 == "IMPLIES")).length = 17 ∧
    (matrixCells.filter (fun c => c.2.2 == "COUNTERMODEL")).length = 51 ∧
    (matrixCells.filter (fun c => c.2.2 == "OPEN_LOCATED")).length = 4 := by
  decide

theorem open_cells_target_bl :
    matrixCells.all (fun c => c.2.2 != "OPEN_LOCATED" || c.2.1 == "Bl") = true := by
  decide

theorem nine_on_d2Bare :
    W d2Bare ∧ A d2Bare ∧ ¬ Bs d2Bare ∧ Bc d2Bare ∧ Bl d2Bare ∧
    ¬ C d2Bare ∧ D d2Bare ∧ E d2Bare ∧ ¬ F d2Bare :=
  ⟨d2Bare_a.1, d2Bare_a, d2Bare_not_bs, d2Bare_bc, d2Bare_bl, d2Bare_not_c,
   imp_a_d _ d2Bare_a, (e_empty_iff_d d2Bare rfl).mpr (imp_a_d _ d2Bare_a), d2Bare_not_f⟩

theorem demand_without_difference : C unitFull ∧ ¬ A unitFull ∧ ¬ D unitFull :=
  ⟨unitFull_c, unitFull_not_a, unitFull_not_d⟩

theorem self_witness_located : Located unitBare.r :=
  located_of_decidable (fun _ _ => True)

theorem f_to_d_by_chain : ∀ S : Setting, F S → D S :=
  fun S h => imp_a_d S (imp_f_a S h)

theorem bs_to_d_by_chain : ∀ S : Setting, Bs S → D S :=
  fun S h => imp_a_d S (imp_bs_a S h)

theorem d2_cotrans : Cotrans PrimDiff.D2 :=
  cotrans_auto_on_two _ PrimDiff.D2_irrefl

theorem tri_split_fails : ¬ (triR 0 2 ∨ triR 2 1) := by decide

theorem merger_in_closure :
    ∃ f, PrimDiff.Clos d2Merged.Ops f ∧ f false = f true :=
  ⟨fun _ => false, PrimDiff.Clos.base rfl, rfl⟩

def twoSym : Setting where
  X := Bool
  r := PrimDiff.S2
  a := false
  b := true
  ret := fun _ _ => False
  prot := fun _ _ => True
  Ops := fun f => f = fun _ => false

theorem twoSym_readings : C twoSym ∧ Bs twoSym ∧ D twoSym ∧ ¬ F twoSym ∧ ¬ E twoSym :=
  ⟨⟨Or.inl PrimDiff.D2_witness, True.intro⟩, s2Bare_bs,
   (D_iff_ne _).mpr (show (false : Bool) ≠ true by decide), fun h => h.2.1,
   fun h => h (fun _ => false) (PrimDiff.Clos.base rfl) rfl⟩

theorem d_at_bool : D d2Bare ↔ (false : Bool) ≠ true := D_iff_ne d2Bare
```

## Checked scope examples (optional)

On a three-point carrier, let the relation always contain 0 → 1,
and let 1 → 2 hold exactly when an arbitrary proposition P holds.
This relation is irreflexive regardless of P. A Boolean realizer
would decide P by its answer at (1,2). The conditional proof below
does not construct a nonlocated relation or settle any OPEN cell.

```lean
def paramRel (P : Prop) (x y : Fin 3) : Prop :=
  (x = 0 ∧ y = 1) ∨ (x = 1 ∧ y = 2 ∧ P)

theorem param_witness_irrefl (P : Prop) :
    paramRel P 0 1 ∧ PrimDiff.Irrefl (paramRel P) := by
  refine ⟨Or.inl ⟨rfl, rfl⟩, ?_⟩
  intro x h
  rcases h with ⟨h0, h1⟩ | ⟨h1, h2, _⟩
  · exact (by decide : (0 : Fin 3) ≠ 1) (h0.symm.trans h1)
  · exact (by decide : (1 : Fin 3) ≠ 2) (h1.symm.trans h2)

/-- A Boolean realizer for that relation supplies a decision for the parameter.
This is conditional, not a nonlocated countermodel or an independence proof. -/
theorem located_requires_parameter_split (P : Prop) :
    Located (paramRel P) → P ∨ ¬ P := by
  rintro ⟨f, hf⟩
  have hp : paramRel P 1 2 ↔ P := by simp [paramRel]
  cases hv : f 1 2 with
  | false =>
    exact Or.inr (fun h => Bool.noConfusion (hv.symm.trans ((hf 1 2).mp (hp.mpr h))))
  | true => exact Or.inl (hp.mp ((hf 1 2).mpr hv))
```

## Line-by-line Lean explanation

**The signature (36-44).** Seven fields. `X : Type` is a Lean type;
`Ops` is a predicate on maps `X → X`. There is no observation field,
which is why `F` cannot see what any map does (`f_ops_irrelevant` is
`Iff.rfl`).

**The axes (49-67).** `Cotrans`: an asserted pair splits against every
third point. `Located`: some Boolean function realises `r`.
`located_of_decidable` builds that function with `decide` whenever `r`
is pointwise decidable; this is the whole reason for the four OPEN
cells.

**The nine predicates (72-100) and `D_iff_ne` (105).** Read them as
the pseudocode. `D` is written as non-factorisation through `Unit`;
`D_iff_ne` turns it into `S.a ≠ S.b` both ways through Unit 14's
theorem. The book's `d_at_bool` is the instance.

**`cotrans_auto_on_two` (113-123).** On `Bool`, with `r` irreflexive:
from `r x y` get `x ≠ y` (Unit 24); then `cases` on `x`, `y`, `z` gives
eight goals, four of which have `x = y` and are closed by `hne`, and in
the other four `z` equals `x` or `y`, so one disjunct is `hxy` itself.
The book's `d2_cotrans` applies it to the oriented pair.

**The models (156-316).** Thirteen structure literals; each field is
written out. `unitBare` has one point, asserted different from itself,
nothing stored; `unitFull` the same with both stores full; `d2Bare` the
oriented pair; `d2Merged` the same with one admitted map, the constant
`false`; `tri` the single edge `0 → 1` on three points; `boolEmpty` two
points and no relation.

**The model facts (321-492)** are one line each. `unitBare_not_a`:
irreflexivity fails at `()`. `unitBare_not_d`: `D` would give `() ≠ ()`.
`unitBare_not_e`: the identity is in the closure and identifies the
one point with itself. `d2Merged_not_e` (367): the constant map is
admitted, hence closed, and identifies `false` with `true`; the book's
`merger_in_closure` exhibits it. `tri_not_bc` (404-414): cotransitivity
at `(0, 1)` against `2` demands `triR 0 2` or `triR 2 1`; the first
needs `2 = 1`, the second `2 = 0`, both decided false. The book's
`tri_split_fails` is the split decided directly.

**The matrix (500-781).** Each implication is a projection or a short
chain: `imp_a_d` is `irrefl_witness_ne` through `D_iff_ne`; `imp_e_d`
instantiates irreducibility at the identity, which is in every closure;
`imp_f_c` projects two conjuncts. Each countermodel names a model and
two model facts. The book's `f_to_d_by_chain` and `bs_to_d_by_chain`
show that `imp_f_d` and `imp_bs_d` follow from `imp_a_d` by chaining,
and `nine_on_d2Bare` reads all nine columns of one row of the Python
table off the model facts.

**The scoped theorems (792-833).** `e_empty_iff_d`: with `Ops` empty,
rewrite and use `irred_empty_iff_ne`. `prot_not_from_witness`,
`ret_not_from_witness`: `d2Bare` is A with both stores empty; the
book's `demand_without_difference` is the converse picture, C without A
or D. `bool_class`: the classification of Unit 24's module restated at
the Setting level.

**The table (841-916).** `matrixCells` is a literal list of 72 triples;
Genesis proves its length is 72 by `rfl`. The book's `tally` decides
the three counts and `open_cells_target_bl` that every OPEN entry
targets Bl. Neither checks that an entry's status matches a theorem of
that name; that correspondence is checked in Python (`lean_tag`), not
in Lean.

## What has been proved

- 17 implications for every Setting and 51 countermodels by named
  finite models (Genesis); the Python scan of 56 088 settings finds a
  countermodel in exactly the 51 cells and none in the 21 others
  (mirror, `expected_equals_computed`).
- A → D; W, C do not give D; E → D; D, A do not give E once one map
  is admitted; with no generators admitted E is D, since the closure
  contains identity (Genesis).
- Irreflexive on `Bool` implies cotransitive, so the A → Bc and
  Bs → Bc countermodels on three points have no two-point
  counterpart; no A-witness lives on a subsingleton (Genesis, Unit 24's
  module).
- Every decidable relation is located (Genesis).
- The tally of the exported table and that every OPEN entry targets
  Bl (book).
- On `Bool` with endpoints `false, true`, an A-relation is `D2` or `S2`
  (Genesis; the mirror lists the two survivors).

## What has not been proved

- The four cells A, Bs, Bc, F → Bl: OPEN. A decidable A-relation
  cannot refute them, because it is located. No general implication
  or nonlocated countermodel for these cells is supplied. The book
  parameter example proves a conditional requirement for a Boolean
  realizer, not independence or an actual nonlocated relation.
- Minimum carrier in general: `cotrans_auto_on_two` is about the type
  `Bool`, not about every two-element type; no transport along
  bijections is formalised. The paper's "provably minimally" rests on
  `Bool` and subsingletons.
- That `matrixCells` matches the theorem names: Lean proves the length
  and the book the tally; the row-by-row correspondence is a Python
  check.
- That any reading is *the* primitive difference: the matrix orders
  readings, it does not select one. The later modules (Units 52-54)
  take that up with categories and contact.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `Setting.X : Type`, `Ops : (X → X) → Prop` | the models | metatheoretic containers |
| `Located` (`∃ f : X → X → Bool`) | the Bl axis | admitted data; underivability metatheoretic |
| `Unit`, `Bool`, `Fin 3` | the countermodel carriers | library types |
| `decide` on `Bool` / `Fin 3` / `String` equalities | model facts, the tally | metatheory |
| `PrimDiff.Clos`, `Irred` | the E axis | Unit 24's module |
| the four `open_cell_*` strings, `matrixCells` | labels | data, not propositions |

**What the system holds.** Nothing: this module is a classification of
readings, over Lean types. The kernel enters only when a later module
(`ContactKernel`, Unit 67) lifts it into a `Setting`.

**Phrases to read with care.**

- "Minimum carrier proved where cited" (ledger): proved for `Bool` and
  for subsingletons; "carrier size" over arbitrary types is not
  formalised.
- "Machine-readable ... for mechanical cross-checking" (header):
  the cross-check is the Python `lean_tag`; Lean checks the length.
- "Located (boolean realizability)" (paper): a metatheoretic
  existential over a function space, as the module's own prose says.
- "Not yet an obstruction, because obstruction requires an observation"
  (`f_ops_irrelevant` docstring): commentary; the theorem says only
  that `F` does not mention `Ops`.

## Student exercise

The row for D has eight countermodels and the row for E has seven and
one implication. Using only `boolEmpty` and `boolEmptyMerged`, say
which cells each one settles, and why neither row can contain an
implication into W.

## Answer

<details>
<summary>Worked answer</summary>

`boolEmpty` (two points, empty relation, no maps) satisfies D (the
points differ) and E (the closure of the empty family is the identity
alone, which keeps them apart) and nothing that mentions `r` or the
stores, so it settles D → W, A, Bs, Bc, Bl, C, F and E → W, A, Bs, Bc,
Bl, C, F: fourteen cells. `boolEmptyMerged` adds the constant map, which
identifies the points inside the closure, so D holds and E fails: it
settles D → E, the eighth cell of the D row. The E row's remaining cell
is the implication E → D, from the identity in every closure. Neither
row can have an implication into W because W is `r a b` and both D and
E are silent about `r`: a model with the endpoints apart and `r` empty
satisfies either without W, which is exactly `boolEmpty`.

</details>

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/PrimitiveCore.lean` lines 36-105 (signature, axes, nine predicates, `D_iff_ne`), 113-123 (`cotrans_auto_on_two`), 156-316 (thirteen models), 321-492 (model facts), 500-781 (the 72 cells), 792-833 (`e_empty_iff_d`, the two `*_not_from_witness`, `f_ops_irrelevant`, `bool_class`), 841-916 (`matrixCells`) |
| Axiom report | `artifacts/lean_axioms.txt` lines 377-457: 81 reports, all within `{propext, Quot.sound}`; the 48 model facts not exported |
| Paper | `paper/primitive_difference_contact.md` "The implication matrix" and "The OPEN cells, scoped exactly"; `paper/paper_claim_ledger.md` `CL-PD2-MATRIX` |
| Python | `code/derivation/primitive_core.py` (`evaluate`, `scan_settings`, `matrix_report`, `lean_tag`, `two_element_classification`), `code/run_primitive_core.py`, `artifacts/primitive_implication_matrix.json`, `artifacts/primitive_candidates.json`, `tests/test_primitive_core.py` (`test_every_matrix_cell_status`, `test_a_bc_minimal_countermodel_is_carrier_three`, `test_two_element_classification`) |
| Check (Python) | `python textbook/checks/u51_primitive_core.py`: the scan, the printed matrix and tally, key-minimal witnesses for the taught cells, the two-point cotransitivity check, Lean's models re-evaluated, the classification, both artifacts |
| Check (book Lean) | `python textbook/checks/u51_lean.py`: fourteen book reports plus seventeen Genesis theorems kernel-checked, Lean 4.33.0 |
