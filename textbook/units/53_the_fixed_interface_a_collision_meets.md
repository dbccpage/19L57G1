# Unit 53. The fixed interface a collision meets

**Claim.** The native interface packages a witnessed irreflexive relation and two scoped results. Its contact verdict and protocol history record the comparison; they do not add a new derivation.

**Status:** FROZEN (the two re-exports, proved in their
home modules); ADMITTED (the interface definition and the status strings,
declared policy); VERIFIED_FINITE (`contact_status_count`, and the Python
mirror's agreement with the strings). **Lean:**
`lean4/Derivation/PrimitiveContact.lean` lines 77-142, imports
`PrimitiveCore`, `PrimitiveCats`, `ContactBridge`. **Axioms:** 3 exported
reports; `native_kernel_initial` uses `Quot.sound` through `d2_initial`,
the other two none. **Depends on:** Unit 51 (`Setting`, A, `imp_a_d`,
`e_empty_iff_d`), Unit 52 (`d2Obj`, `d2_initial`), Unit 44 (`DiffObs`
and its zero relation); the refutation itself is taught in Unit 67.

## First pass

Separate the mathematical package from its protocol record. The package specifies the native settings and the proved interfaces available for comparison.

The status labels then record what contact processed and what remains incomparable. A recorded status is not an additional theorem connecting the two sides.

## Detailed claim and formal anchors

`PrimitiveContact` fixes, before any outside development is
read, what the native side puts on the table: `NativeKernel`, the class
of settings carrying a pointed witnessed irreflexive relation (reading A
of Unit 51), inhabited by `nativeKernelWitness` (Unit 51's `d2Bare`); and
two re-exported facts under contact-facing names, `native_kernel_initial`
(Unit 52's `d2_initial`) and `native_interface_not_representable`
(ContactBridge's `d2_not_obs_complement`: no difference observer's
apartness on `Bool` is the oriented witness, because an observer's
apartness is symmetric).

The rest of the module is protocol record: the
sealed pre-contact terminal `CONTACT_INPUT_ABSENT`, the current status
`CONTACT_PROCESSED_LEAN_ONLY`, the primary verdict
`CONTACT_INCOMPARABLE_WITH_COUNTERMODELS`, and a two-entry history whose
length is `rfl`.

## Question

When a development written elsewhere arrives to be compared with this
one, what exactly does the native side bring, and in what form is it
held fixed so that the comparison cannot move the goalposts? And why is
the one object the native side names something no observer's apartness
can be?

## What we already possess

- Reading A of a difference, `S.r S.a S.b ∧ Irrefl S.r`, and what A
  brings: D (`imp_a_d`), and E when nothing is admitted
  (`e_empty_iff_d`) (Unit 51).
- `d2Obj`, initial among all pointed witnessed relations; the symmetric
  object is initial only against symmetric targets (Unit 52).
- A difference observer `DiffObs X R`: a difference value `delta x y`,
  a zero predicate, and the three laws making "zero difference" an
  equivalence (Unit 44). Its *apartness*, `obsApart O x y`, is "the
  difference is not zero".

## New concept: an interface committed before contact

An *interface* here is a Lean type together with named theorems about
it, declared at a recorded commit before the outside material is read,
and never edited afterwards. Anything arriving is compared against that
type and those theorems. A *status string* is a declared constant, not a
proposition: it records a decision of the protocol, and its only
mathematical content is that it equals the string the Python generator
writes.

## Plain-language interpretation

The module is a contract signed in advance. Its first half was written
when no outside package existed, and says: the native notion of
difference is a witnessed pair with the law that nothing differs from
itself; here is one example of it, the oriented two-point pair; and here
is the strongest thing we can say about that example, that it is the
first object among all witnessed pairs. When the package did arrive the
first half was not touched. The second half records that it arrived,
that only its Lean was read, and what the verdict was; the mathematics
of the verdict lives in three later modules.

One theorem is re-exported at the interface because it is the whole
point of the comparison: the oriented pair is not what any observer's
apartness can be. An observer says when two things have zero
difference, and "zero difference" is an equivalence, so "not zero" is
symmetric. The oriented pair says `false` differs from `true` and not
the other way round. So no observer, whatever values it uses, has the
oriented pair as its apartness. That is not a limitation of some
observer; it is the shape of the two notions.

## Pseudocode

```
NativeKernel = { S : Setting | A S }          -- witnessed and irreflexive
witness      = d2Bare ∈ NativeKernel
interface facts:
  d2Obj is initial                             (Unit 52)
  for every R and observer O on Bool: apart O ≠ D2   (apart O is symmetric)
protocol record:
  history = [CONTACT_INPUT_ABSENT …, CONTACT_PROCESSED_LEAN_ONLY …]; length 2
  current = CONTACT_PROCESSED_LEAN_ONLY; verdict = CONTACT_INCOMPARABLE_WITH_COUNTERMODELS
```

## Python

Genesis's `code/run_primitive_contact.py` writes
`artifacts/primitive_contact.json`: the status, history and verdict
constants, the interface block naming the Lean binding and the theorems,
and five enumerations. E1 lists every Bool-valued observer (16 difference
tables, 4 zero predicates) and counts how many have the oriented pair as
their zero-complement; the generator refuses to write if that count is
not zero.

```python
oriented = sum(
    1 for t in tables for z in zpreds
    if laws(t, z) and all(
        (not zrel(t, z, x, y)) == ((not x) and y)
        for x in pts for y in pts))
_require(oriented == 0,
         "a Bool-valued observer represented the oriented witness")
```

The check's run:

```text
artifact status 'CONTACT_PROCESSED_LEAN_ONLY'; Lean contactStatusCurrent 'CONTACT_PROCESSED_LEAN_ONLY'; Python STATUS_PROCESSED 'CONTACT_PROCESSED_LEAN_ONLY'
history (2 entries): ['CONTACT_INPUT_ABSENT (pre-contact, blind-native-base ccd3a53)', 'CONTACT_PROCESSED_LEAN_ONLY (2026-08-13, base a5caee2)']
  equals Lean contactStatusHistory: True; equals Python STATUS_HISTORY: True; first entry carries the sealed terminal 'CONTACT_INPUT_ABSENT': True
verdict primary: 'CONTACT_INCOMPARABLE_WITH_COUNTERMODELS'; Lean contactVerdictPrimary 'CONTACT_INCOMPARABLE_WITH_COUNTERMODELS'; Python 'CONTACT_INCOMPARABLE_WITH_COUNTERMODELS'
prose stage: PROSE_INPUT_ABSENT; package present True, manifest present True
the interface block:
  implication_matrix: artifacts/primitive_implication_matrix.json (72 cells, PrimitiveCore.matrixCells)
  kernel: PDA_pointed_witnessed_irreflexive
  lean_binding: PrimitiveContact.NativeKernel
  observer_branching: PrimitiveCats.no_terminal_pres
  orientation_fork: ['PrimitiveCats.s2_initial_sym', 'PrimitiveCats.s2_not_weakly_initial', 'both branches retained']
  universal_status: PrimitiveCats.d2_initial (initial among all pointed witnessed relations)
  witness: PrimitiveContact.nativeKernelWitness
nativeKernelWitness as a Setting: {'W': True, 'A': True, 'Bs': False, 'Bc': True, 'Bl': True, 'C': False, 'D': True, 'E': True, 'F': False}
  reading A holds: True; what A brings (matrix row A): ['W', 'D'] implied, ['Bl'] open
E1 Bool observers re-run: {'delta_tables': 16, 'zero_predicates': 4, 'diag_zero_pairs': 24, 'observer_law_pairs': 20, 'witnessed_kernel_quadruples': 8, 'oriented_complement_observers': 0}; equals artifact: True
  1 points: 1 equivalences; every complement symmetric True, irreflexive True; the oriented witness among them: False
  2 points: 2 equivalences; every complement symmetric True, irreflexive True; the oriented witness among them: False
  3 points: 5 equivalences; every complement symmetric True, irreflexive True; the oriented witness among them: False
failures: []
```

## Line-by-line Python explanation

The first block reads the artifact's `status`, `history` and `verdict`
and compares them with the constants in the generator module and with
the strings Lean declares, copied into the check. This is the only
content the status strings have: three copies that agree.

The interface block is printed as the artifact records it; the check
requires the Lean binding and witness names to be the ones this unit
teaches. The witness is then rebuilt as Unit 51's `Setting` (two points,
one edge, empty stores) and fed to Genesis's `evaluate`: reading A holds,
and the row of the expected matrix for A says what A promises, W and D,
with the located cell open.

E1 is re-run by calling Genesis's own `enum_bool_observers`: the
counts match the artifact, and the oriented-complement count is zero.
The last block is Python (book) and gives the reason at carriers of one,
two and three points: every equivalence has a symmetric, irreflexive
complement, and the oriented pair is never among those complements.

## Lean 4

```lean
-- Lean (Genesis), lean4/Derivation/PrimitiveContact.lean lines 80-142
def contactStatus : String := "CONTACT_INPUT_ABSENT"

def NativeKernel : Type 1 :=
  { S : PrimitiveCore.Setting // PrimitiveCore.A S }

def nativeKernelWitness : NativeKernel :=
  ⟨{ X := Bool, r := PrimDiff.D2, a := false, b := true,
     ret := fun _ _ => False, prot := fun _ _ => False,
     Ops := fun _ => False },
   ⟨PrimDiff.D2_witness, PrimDiff.D2_irrefl⟩⟩

theorem native_kernel_initial : PrimitiveCats.Initial
    PrimitiveCats.d2Obj := PrimitiveCats.d2_initial

def contactStatusHistory : List String :=
  ["CONTACT_INPUT_ABSENT (pre-contact, blind-native-base ccd3a53)",
   "CONTACT_PROCESSED_LEAN_ONLY (2026-08-13, base a5caee2)"]

def contactStatusCurrent : String := "CONTACT_PROCESSED_LEAN_ONLY"

def contactVerdictPrimary : String :=
  "CONTACT_INCOMPARABLE_WITH_COUNTERMODELS"

theorem contact_status_count : contactStatusHistory.length = 2 := rfl

theorem native_interface_not_representable :
    ¬ ∃ (R : Type) (O : DiffInterface.DiffObs Bool R),
        ∀ x y, ContactBridge.obsApart O x y ↔ PrimDiff.D2 x y :=
  ContactBridge.d2_not_obs_complement
```

```lean
-- Lean (Genesis), lean4/Derivation/ContactBridge.lean lines 116-126, 362-370
def obsApart (O : DiffObs X R) (x y : X) : Prop := ¬ ZeroRel O x y

theorem obsApart_symm (O : DiffObs X R) :
    ∀ x y, obsApart O x y → obsApart O y x :=
  fun _ _ hxy hz => hxy (O.zero_symm hz)

theorem d2_not_obs_complement :
    ¬ ∃ (R : Type) (O : DiffObs Bool R),
        ∀ x y, obsApart O x y ↔ PrimDiff.D2 x y := by
  rintro ⟨R, O, hO⟩
  have h1 : obsApart O false true :=
    (hO false true).mpr PrimDiff.D2_witness
  have h2 : PrimDiff.D2 true false :=
    (hO true false).mp (obsApart_symm O false true h1)
  exact absurd h2 (by decide)
```

The book's Lean reads the witness as Unit 51's `d2Bare`, draws from its
membership proof what the interface promises, shows the kernel has a
second member (the symmetric pair, so the interface is a class and not
one object), confirms the re-exports are the originals, and re-proves
the refutation from symmetry alone.

```lean
-- Lean (book), textbook/checks/u53_lean.py
theorem witness_is_d2Bare : nativeKernelWitness.val = d2Bare := rfl

theorem witness_reading_A :
    nativeKernelWitness.val.r nativeKernelWitness.val.a nativeKernelWitness.val.b ∧
    PrimDiff.Irrefl nativeKernelWitness.val.r :=
  nativeKernelWitness.property

theorem witness_endpoints_apart : D nativeKernelWitness.val :=
  imp_a_d _ nativeKernelWitness.property

theorem witness_irreducible : E nativeKernelWitness.val :=
  (e_empty_iff_d _ rfl).mpr witness_endpoints_apart

theorem kernel_endpoints_apart (K : NativeKernel) : K.val.a ≠ K.val.b :=
  (D_iff_ne _).mp (imp_a_d _ K.property)

def symMember : NativeKernel := ⟨s2Bare, s2Bare_bs.1⟩

theorem two_members : nativeKernelWitness.val ≠ symMember.val := by
  intro h
  have h2 : HEq nativeKernelWitness.val.r symMember.val.r := by rw [h]
  have h3 : PrimDiff.D2 = PrimDiff.S2 := eq_of_heq h2
  have h4 : PrimDiff.S2 true false := Or.inr PrimDiff.D2_witness
  rw [← h3] at h4
  exact Bool.noConfusion h4.1

theorem object_of_record :
    PrimitiveCats.d2Obj.X = nativeKernelWitness.val.X ∧
    PrimitiveCats.d2Obj.r = nativeKernelWitness.val.r ∧
    PrimitiveCats.d2Obj.a = nativeKernelWitness.val.a ∧
    PrimitiveCats.d2Obj.b = nativeKernelWitness.val.b :=
  ⟨rfl, rfl, rfl, rfl⟩

theorem initial_is_reexport : native_kernel_initial = PrimitiveCats.d2_initial := rfl

theorem d2_not_symmetric : ¬ ∀ x y, PrimDiff.D2 x y → PrimDiff.D2 y x := by
  intro h
  exact Bool.noConfusion (h false true PrimDiff.D2_witness).1

theorem not_representable_by_symmetry :
    ¬ ∃ (R : Type) (O : DiffInterface.DiffObs Bool R),
        ∀ x y, ContactBridge.obsApart O x y ↔ PrimDiff.D2 x y := by
  rintro ⟨R, O, hO⟩
  apply d2_not_symmetric
  intro x y hxy
  exact (hO y x).mp (ContactBridge.obsApart_symm O x y ((hO x y).mpr hxy))

theorem history_reads :
    contactStatusHistory.length = 2 ∧
    (contactStatusHistory.head? = some
      "CONTACT_INPUT_ABSENT (pre-contact, blind-native-base ccd3a53)") ∧
    contactStatus = "CONTACT_INPUT_ABSENT" ∧
    contactStatusCurrent = "CONTACT_PROCESSED_LEAN_ONLY" :=
  ⟨rfl, rfl, rfl, rfl⟩

theorem sealed_differs_from_current : contactStatus ≠ contactStatusCurrent := by
  decide
```

## Line-by-line Lean explanation

**`NativeKernel` (84-85).** A subtype: a `Setting` together with a proof
of `A`. It lives in `Type 1` because `Setting` carries a `Type` field.
Membership is reading A and nothing more: no store, no operation family
is constrained. The book's `symMember` shows the symmetric two-point
setting is a member too, and `two_members` that it is a different
member: equal settings would have equal relations (through `HEq`, since
the carriers are both `Bool`), and `S2 true false` holds while `D2 true
false` does not.

**`nativeKernelWitness` (89-93).** The structure literal is Unit 51's
`d2Bare` field for field; the book's `witness_is_d2Bare` is `rfl`. The
membership proof is `⟨D2_witness, D2_irrefl⟩`, and `witness_reading_A`
simply returns it. From it, by Unit 51's `imp_a_d`, the endpoints are
apart; by `e_empty_iff_d`, with `Ops` empty, nothing admitted identifies
them. `kernel_endpoints_apart` says the first of these for every member:
it is the promise the interface makes to any arrival.

**`native_kernel_initial` (99-100).** Its proof term is
`PrimitiveCats.d2_initial`; `initial_is_reexport` is `rfl`, and the axiom
report (`Quot.sound`) is inherited. `object_of_record` checks that
`d2Obj` and the witness agree in carrier, relation and points, each by
`rfl`.

**The status declarations (80, 116-131).** Four strings and a list.
`contact_status_count` is `rfl` on the list's length. The book's
`history_reads` reads the head and the two constants by `rfl`, and
`sealed_differs_from_current` decides that the superseded string is not
the current one, which is the module's own warning about reading
`contactStatus` alone.

**`native_interface_not_representable` (137-140)** is `d2_not_obs_complement`
by name. Its proof: suppose an observer's apartness is `D2`; then `false`
is apart from `true` (the witness), so by `obsApart_symm` `true` is apart
from `false`, so `D2 true false`, which `decide` refutes. The book's
`not_representable_by_symmetry` isolates the one property used,
`d2_not_symmetric`, and derives the refutation from `obsApart_symm`
alone; it carries no axioms.

## What has been proved

- The kernel's witness satisfies reading A; every member has its
  endpoints apart (Unit 51's theorem, applied).
- The object of record is initial among all witnessed pointed relations
  (Unit 52's theorem, re-exported unchanged).
- No `DiffObs` on `Bool`, with any value type, has the oriented witness
  as its apartness; the reason is that apartness is symmetric.
- The history has two entries, and the three copies of each status
  string (Lean, Python, artifact) agree.
- Genesis's E1 enumeration: of 16 × 4 Bool-valued observer candidates,
  20 satisfy the three laws and none has the oriented complement.

## What has not been proved

- Nothing about the arriving development is proved here. The verdict
  string is a declared constant; its evidence is the theorem corpus of
  `ObsDescent`, `ContactBridge` and `ContactKernel` (Units 66-67).
- "The strongest universal status the native side brings" (docstring of
  `native_kernel_initial`): "strongest" is not a theorem. What is proved
  is initiality in the pointed witnessed category.
- The interface is a type, not a totality: `NativeKernel` quantifies over
  every `Setting` with a Lean `Type` carrier.

## Outside the system

| Lean | Used for | Status |
|---|---|---|
| `String`, `List String` | the status record | metatheoretic data, declared policy |
| `{ S : Setting // A S } : Type 1` | the interface | a Lean subtype over `Type` |
| `∃ (R : Type) (O : DiffObs Bool R)` | the refutation's scope | quantification over all value types |
| `decide` on `Bool` and `String` | model facts | metatheory |

**What the system holds.** Nothing: the module names an interface and
copies two theorems to it. The commit hashes and the dates in the
docstrings and strings are provenance, not mathematics.

**Phrases to read with care.**

- "Sealed" and "superseded" (docstrings): facts about the repository's
  history, recorded so a reader of `contactStatus` alone is warned.
- "The strongest universal status": see above.
- "DECLARED_POLICY" and "FINITE_COMPUTATION" are the module's own labels
  for its constants and its one `rfl`; take them at that.
- The inventory artefact lists `corpus` among this module's theorems; it
  is a docstring word, not a declaration (audit note 2).

## Student exercise

The refutation is stated for observers on `Bool`. Say, using only
`obsApart_symm`, why it also holds for the symmetric pair's opposite:
could some observer's apartness be `fun x y => x = true ∧ y = false`?
And could one be `S2`?

## Answer

No to the first: the same argument runs with the roles exchanged. If
apartness were `x = true ∧ y = false`, then `true` would be apart from
`false`, so by symmetry `false` would be apart from `true`, giving
`false = true`, which is false. Any apartness that holds one way round
and not the other is refuted the same way.

`S2` is not refuted by this argument, and in fact an observer realises
it: take `delta x y := (x == y)` with values in `Bool` and `Zero v := v =
true`; then zero difference is equality, which is an equivalence, and
apartness is `x ≠ y`, which on `Bool` is `S2`. Symmetry is the only
obstacle the argument uses, and `S2` has it.

## Verification

| Item | Where |
|---|---|
| Lean | `lean4/Derivation/PrimitiveContact.lean` lines 80 (`contactStatus`), 84-93 (`NativeKernel`, witness), 99-100 (`native_kernel_initial`), 116-131 (history, current, verdict, `contact_status_count`), 137-140 (`native_interface_not_representable`); `lean4/Derivation/ContactBridge.lean` 116-126 (`obsApart`, `obsApart_symm`), 362-370 (`d2_not_obs_complement`) |
| Axiom report | `artifacts/lean_axioms.txt` lines 458, 1201-1202 |
| Paper | `paper/primitive_difference_contact.md` "THE EXECUTED COLLISION" and "CONTACT VERDICT"; `paper/paper_claim_ledger.md` `CL-PD2-CONTACT` and its scope note of 2026-08-13 |
| Python | `code/run_primitive_contact.py` (`STATUS_HISTORY`, `VERDICT_PRIMARY`, `enum_bool_observers`), `artifacts/primitive_contact.json` (`status`, `history`, `verdict`, `native_kernel_interface`, `enumerations.E1_bool_observers`) |
| Audit | `textbook/audit/modules/PrimitiveContact.md` findings 1-3 |
| Check (Python) | `python textbook/checks/u53_primitive_contact.py`: the three copies of each status string, the interface block, the witness through Unit 51's evaluator, E1 re-run, and the Python (book) complement census on 1-3 points |
| Check (book Lean) | `python textbook/checks/u53_lean.py`: thirteen book declarations plus five Genesis theorems kernel-checked, Lean 4.33.0 |
