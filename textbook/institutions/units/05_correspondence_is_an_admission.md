# Unit 05. The shared carrier is an admission

**Claim.** Combining members requires an explicit correspondence between their
inputs. A common invertible relabeling preserves knowledge; changing
one member's alignment can change it. A correspondence may merge only
pairs the intended observed answer also merges.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Re-indexing one member's data by a permutation can destroy what a
family knows, while applying one invertible renaming simultaneously to the
carrier, every member, and the claim leaves knowledge unchanged. More
generally, reading an observer or a family through a correspondence `f`
transports sharpness for the composed presentation along any `f`. If the
pulled-back observer is sharp for `q`, then `q` is constant on the fibers
of `f`: `f x = f y` forces `q x = q y` on the carrier. Identity is one
case where this forces `f` to be injective; it is not the only possible
observed presentation with that consequence.

**Status:** derived. **Lean:** `Inst.correspondence_matters`,
`Inst.knows_rename` (`actor_institution`); `Correspondence.Faithful`,
`Correspondence.faithful_actor_iff`, `Correspondence.verdict_pullback`,
`Correspondence.sharp_pullback_iff`,
`Correspondence.fiberConstant_of_sharp_pullback`,
`Correspondence.faithful_of_sharp_identity`,
`Correspondence.sharp_identity_pullback` (`two_theorems`). **Sources:**
`research/actor_institution/lean/ResearchActorInstitution/Institution.lean`
lines 200–245;
`research/two_theorems/lean/ResearchTwoTheorems/Correspondence.lean` lines
35–178.

Unit 00 introduced the supplied tables and their common carrier `D`. Unit 04
showed that `[p1, p2]` knows `q3` on `[0, 1, 2]` while neither member alone
does. This unit shows what happens when that third admission is varied: if
`p2` reads its data through a swap of `0` and `1` while `p1` and `q3` do not,
the family no longer knows `q3`. By contrast, if one renaming is applied across
the carrier, every member, and the claim together, knowledge is unchanged. It
then connects this to the fidelity contract of `two_theorems`: an unrestricted
map can merge points before any observer evaluates them. One necessary
condition for sharp observation is that every pair merged by the
correspondence must also be merged by the observed presentation. The
observer must additionally supply the intended distinctions. The reverse
fiber condition is not what the theorem states.

</details>

## First pass

The two members in I04 report [0,1,0] and [0,1,1]. Together they
determine the question [0,0,1]. Their rows must refer to the same inputs.

Swap only the second member's entries at 0 and 1. It now reports
[1,0,1]. The combined answers at 0 and 2 both become [0,1], although
the requested answer differs there. Recovery fails.

Relabeling the entire setup consistently is different: move the carrier,
both member tables, and the requested question together. Their agreements
are preserved.

**Predict:** if a correspondence merges two inputs, can a later observer
recover a requested distinction between them?

<details><summary>Check your prediction</summary>

No. Equal correspondence outputs supply the same later input. Sharp
observation of a question therefore requires the question to agree on
each merged pair. It does not require the correspondence to be constant
on the question's groups; that reverses the condition.

</details>

## What you need first

Use I00’s signatures, I01’s representative, I02’s recovery rule and I04’s two-member example. We will define the new observer and correspondence terms below.

<details>
<summary>Prerequisite source names (optional)</summary>

Unit 00 (`SigEq`), Unit 01 (`pQ`, `pQ_exact`), Unit 02 (`FiberConstant`,
`Knows`, `knows_iff_determined`), and Unit 04 (`p1`, `p2`, `q3`).

</details>

An **observer** here is a supplied list of yes/no tests called **views**.
A view lists the inputs on which its answer is yes. It separates two
inputs when exactly one belongs to that list. An observer separates a
pair when at least one of its views does. The source names are
`Evaluator`, `sepB`, and `verdictB`, from sealed `Represented.lean`.
These definitions describe tests on supplied numbers, with no physical
instrument or measurement procedure attached.

**Sharp for q** means that the observer merges exactly the input pairs
whose q-values agree. It must retain every distinction q makes and add
none. We can therefore ask separately what the correspondence preserves
and what the later views distinguish.

### 1. Re-indexing one member

<details>
<summary>Lean source: swap01 (optional)</summary>

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Institution.lean lines 200–201
/-- Swap the indices `0` and `1`. -/
def swap01 : Nat → Nat := fun x => if x = 0 then 1 else if x = 1 then 0 else x
```

</details>

`swap01` exchanges `0` and `1` and leaves `2` fixed. Composing `p2` with
`swap01` produces the table `(p2 1, p2 0, p2 2) = (1, 0, 1)` on `[0, 1, 2]`:
the same multiset of values as `p2 = (0, 1, 1)`, but aligned differently
against `p1` and `q3`.

### 2. Faithful correspondences and pullback observers

A **correspondence** f sends each original input to the input a later
test receives. Calling it **faithful on D** means different inputs in D
never become the same later input. It says nothing yet about how useful
the later tests are.

<details>
<summary>Lean source: Faithful, collapsed_of_merged, constant_collapses_all (optional)</summary>

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Correspondence.lean lines 35–48, 72–73, 99–100
def Faithful (D : List Nat) (f : Nat → Nat) : Prop :=
  ∀ x, x ∈ D → ∀ y, y ∈ D → f x = f y → x = y

theorem collapsed_of_merged (E : Evaluator) (f : Nat → Nat) {x y : Nat}
    (h : f x = f y) : verdictB E (f x) (f y) = false := by
  rw [h]
  exact verdict_irrefl E (f y)

theorem constant_collapses_all (E : Evaluator) (x y : Nat) :
    verdictB E ((fun _ => 0) x) ((fun _ => 0) y) = false :=
  verdict_irrefl E 0
```

</details>

A map `f : Nat → Nat` is `Faithful` on `D` when it merges no two data of `D`.
If `f` merges `x` and `y` (`f x = f y`), then every observer `E` returns
`verdictB E (f x) (f y) = false` (`collapsed_of_merged`), because no view can
separate a datum from itself (`verdict_irrefl`). In particular, the constant
map `fun _ => 0` collapses every pair under every observer
(`constant_collapses_all`) and is not faithful on `[0, 1]`
(`constant_not_faithful`, lines 51–53).

<details>
<summary>Lean source: pullback, verdict_pullback (optional)</summary>

```lean
-- Lean (research), the same file, lines 99–100, 121–126
def pullback (D : List Nat) (f : Nat → Nat) (E : Evaluator) : Evaluator :=
  E.map (fun c => D.filter (fun x => decide (f x ∈ c)))

theorem verdict_pullback (D : List Nat) (f : Nat → Nat) (E : Evaluator) {x y : Nat}
    (hx : x ∈ D) (hy : y ∈ D) :
    verdictB (pullback D f E) x y = verdictB E (f x) (f y) := by
  unfold pullback verdictB
  rw [List.any_map]
  exact congrArg (List.any E) (funext fun c => sep_pullback c hx hy)
```

</details>

To **pull back** a view, list the original inputs whose f-values pass
that view. Suppose f sends inputs 0,1,2 to 4,4,9, and the later view is
`[9]`. Only input 2 passes, so its pulled-back view is `[2]`.

This works one view at a time. `pullback D f E` collects the resulting
original-input views. Its verdict on x,y agrees with E's verdict on
f(x),f(y), for x,y in D (`verdict_pullback`).

### 3. A necessary condition is not the whole procedure

In that example, let q report `[0,0,1]`. The map merges 0 with 1, which
q also merges. The later view `[9]` is enough to observe q sharply,
even though f is not faithful on all three inputs.

Remove every later view. The same f still merges only pairs q merges,
but the empty observer now also merges 0 with 2, where q differs.
Sharpness fails. Even a faithful map followed by an empty observer would
fail to observe a nonconstant q sharply. Preserving an available
distinction and actually using a test that detects it are different
requirements.

```python
# Python (research), research/two_theorems/model.py lines 524–531
def faithful(D: Carrier, f: Presentation) -> bool:
    """``Faithful D f``: the correspondence merges no two carrier points."""
    return all(f(x) != f(y) or x == y for x in D for y in D)


def pullback(D: Carrier, f: Presentation, E: Evaluator) -> Evaluator:
    """``pullback``: the observer's views read back along ``f`` onto ``D``."""
    return tuple(tuple(x for x in D if f(x) in c) for c in E)
```

## The theorems

First, the contrast between re-indexing one member and renaming the whole
institution:

<details>
<summary>Lean source: correspondence_matters, knows_rename (optional)</summary>

```lean
-- Lean (research), research/actor_institution/lean/ResearchActorInstitution/Institution.lean lines 209–245
theorem correspondence_matters :
    Knows [0, 1, 2] [p1, p2] q3 ∧
    ¬ Knows [0, 1, 2] [p1, fun x => p2 (swap01 x)] q3 := by
  decide

theorem knows_rename {σ τ : Nat → Nat} (hστ : ∀ x, σ (τ x) = x)
    (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows (D.map τ) (Q.map (fun p => fun x => p (σ x))) (fun x => q (σ x)) ↔
      Knows D Q q := by
  rw [knows_iff_determined, knows_iff_determined]
  constructor
  · intro h x hx y hy hs
    have h1 := h (τ x) (List.mem_map.mpr ⟨x, hx, rfl⟩)
      (τ y) (List.mem_map.mpr ⟨y, hy, rfl⟩) ?_
    · show q x = q y
      have h2 : q (σ (τ x)) = q (σ (τ y)) := h1
      rw [hστ, hστ] at h2
      exact h2
    · intro p' hp'
      obtain ⟨p, hp, rfl⟩ := List.mem_map.mp hp'
      show p (σ (τ x)) = p (σ (τ y))
      rw [hστ, hστ]
      exact hs p hp
  · intro h x' hx' y' hy' hs
    obtain ⟨x, hx, rfl⟩ := List.mem_map.mp hx'
    obtain ⟨y, hy, rfl⟩ := List.mem_map.mp hy'
    show q (σ (τ x)) = q (σ (τ y))
    rw [hστ, hστ]
    apply h x hx y hy
    intro p hp
    have h2 : p (σ (τ x)) = p (σ (τ y)) :=
      hs (fun z => p (σ z)) (List.mem_map.mpr ⟨p, hp, rfl⟩)
    rw [hστ, hστ] at h2
    exact h2
```

</details>

Second, the fidelity contract for an institution's representative and for
pulled-back observers (`Sharp D E p` means `∀ x ∈ D, ∀ y ∈ D, verdictB E x y =
false ↔ p x = p y`):

<details>
<summary>Lean source: faithful_actor_iff, sharp_pullback_iff, fiberConstant_of_sharp_pullback, faithful_of_sharp_identity (optional)</summary>

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/Correspondence.lean lines 72–79, 131–161
theorem faithful_actor_iff (D : List Nat) (Q : Institution) :
    Faithful D (pQ D Q) ↔ Knows D Q (fun x => x) := by
  rw [knows_iff_determined]
  constructor
  · intro h x hx y hy hs
    exact h x hx y hy ((pQ_exact D Q x hx y hy).mpr hs)
  · intro h x hx y hy hp
    exact h x hx y hy ((pQ_exact D Q x hx y hy).mp hp)

theorem sharp_pullback_iff (D : List Nat) (f : Nat → Nat) (E : Evaluator)
    (p : Presentation) :
    Sharp (D.map f) E p ↔ Sharp D (pullback D f E) (fun x => p (f x)) := by
  unfold Sharp
  constructor
  · intro h x hx y hy
    rw [verdict_pullback D f E hx hy]
    exact h (f x) (List.mem_map.mpr ⟨x, hx, rfl⟩) (f y) (List.mem_map.mpr ⟨y, hy, rfl⟩)
  · intro h x' hx' y' hy'
    obtain ⟨x, hx, rfl⟩ := List.mem_map.mp hx'
    obtain ⟨y, hy, rfl⟩ := List.mem_map.mp hy'
    rw [← verdict_pullback D f E hx hy]
    exact h x hx y hy

theorem fiberConstant_of_sharp_pullback (D : List Nat) (f : Nat → Nat) (E : Evaluator)
    (q : Presentation) (h : Sharp D (pullback D f E) q) : FiberConstant D f q := by
  intro x hx y hy hf
  have hv : verdictB (pullback D f E) x y = false := by
    rw [verdict_pullback D f E hx hy]
    exact collapsed_of_merged E f hf
  exact (h x hx y hy).mp hv

theorem faithful_of_sharp_identity (D : List Nat) (f : Nat → Nat) (E : Evaluator)
    (h : Sharp D (pullback D f E) (fun x => x)) : Faithful D f :=
  fiberConstant_of_sharp_pullback D f E (fun x => x) h
```

</details>

A consistent renaming preserves the same answer rows when its read-back rule recovers each old input. A correspondence that merges inputs supplies the same later input for both, so no later view can separate that pair. The observer must still distinguish all pairs required by the chosen q.

<details>
<summary>Detailed proof steps (optional)</summary>

## The proof, step by step

**Step 1. `correspondence_matters` by `decide`.** On `[0, 1, 2]`, `p1` is
`(0, 1, 0)` and `fun x => p2 (swap01 x)` is `(1, 0, 1)`. Both send `0` and `2`
to the same signature `(0, 1)`, whereas `q3 = (0, 0, 1)` sends `0` to `0` and
`2` to `1`. So `[p1, fun x => p2 (swap01 x)]` merges `{0, 2}` while `q3` splits
it, and `Knows` fails.

**Step 2. `knows_rename` via `knows_iff_determined`.** Suppose `σ (τ x) = x`
for every `x`. Rewriting both sides of `knows_rename` with Unit 02's
`knows_iff_determined` reduces the equivalence to preservation of pairwise
determination along `τ` and `σ`:

- Left to right: given `x, y ∈ D` with `SigEq Q x y`, their images `τ x, τ y`
  lie in `D.map τ`. Every member of the renamed family has the form
  `fun z => p (σ z)` for `p ∈ Q`, and on `τ x` and `τ y` its values simplify by
  `hστ` to `p x` and `p y`, which are equal by `hs`. Applying `h` gives
  `q (σ (τ x)) = q (σ (τ y))`, which simplifies by `hστ` to `q x = q y`.
- Right to left: every `x', y' ∈ D.map τ` has the form `τ x, τ y` with
  `x, y ∈ D`. The hypothesis that every renamed member `fun z => p (σ z)`
  agrees on `τ x` and `τ y` simplifies by `hστ` to `SigEq Q x y`, so `h` yields
  `q x = q y`, which is `q (σ (τ x)) = q (σ (τ y))`.

The printed theorem needs only `σ (τ x) = x`: old inputs can be renamed
and read back. It does not require the reverse equation on every natural
number. For example, τ(x)=x+10 and σ(y)=y−10 (natural-number subtraction)
read back every old input, although σ also sends 0 through 9 to 0.

**Step 3. `faithful_actor_iff`.** By Unit 02 (`knows_iff_determined`), the
institution `Q` knows the identity `fun x => x` on `D` iff `SigEq Q x y → x = y`
for all `x, y ∈ D`. By Unit 01 (`pQ_exact`), `pQ D Q x = pQ D Q y ↔ SigEq Q x y`.
Substituting `pQ_exact` into the definition of `Faithful D (pQ D Q)` gives the
equivalence immediately. As a corollary (`empty_actor_constant`,
`empty_actor_not_faithful`, lines 83–94), the empty family's representative is
constant on `D` and is not faithful on `[0, 1]`.

**Step 4. `sharp_pullback_iff` and `fiberConstant_of_sharp_pullback`.**
By `verdict_pullback`, the pulled-back observer `pullback D f E` gives `false`
on `x, y ∈ D` exactly when `E` gives `false` on `f x, f y ∈ D.map f`.
Substituting this into `Sharp` shows that `E` is sharp for `p` on `D.map f` iff
`pullback D f E` is sharp for the composed presentation `fun x => p (f x)` on
`D`—no injectivity assumption on `f` is needed. Conversely, if `pullback D f E`
is sharp for some presentation `q` on `D` and `f x = f y`, then
`collapsed_of_merged` forces `verdictB (pullback D f E) x y = false`, and
sharpness for `q` forces `q x = q y`. That is `FiberConstant D f q`. Specializing
`q` to `fun x => x` gives `faithful_of_sharp_identity` (and with `hf : Faithful D f`,
`sharp_identity_pullback` on lines 165–177 gives the converse for the identity).

</details>

## The same fact in Python

The check verifies three things:

1. `correspondence_matters`: on `range(3)`, `(P1, P2)` knows `Q3`, while
   replacing `P2` by `(P2[1], P2[0], P2[2])` breaks `Knows`.
2. `knows_rename`: over all 6 permutations of `range(3)`, the empty
   family, each singleton and one ordering of each distinct partition pair,
   and every partition as the claim, permuting the carrier,
   every member, and the claim together leaves `knows` unchanged.
3. `correspondence_checks`: on `D = (0, 1, 2)` from `two_theorems`, the
   constant map is not faithful and collapses all pairs, `faithful(D, pQ)`
   matches `knows(D, Q, id)` with 0 mismatches, `sharp_pullback_iff` holds with
   0 mismatches across all maps `D → D` and observers of 1 or 2 views, and
   `fiberConstant_of_sharp_pullback` has 0 violations.

```
python textbook/institutions/checks/i05_correspondence.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `decide` | `correspondence_matters`, `constant_not_faithful`, `empty_actor_not_faithful` | kernel evaluation of closed decidable statements on `[0, 1, 2]` and `[0, 1]` |
| `funext` | `verdict_pullback` | function extensionality on `fun c => sep_pullback c hx hy` inside `List.any`; uses Lean's standard `Quot.sound` / `propext` foundation |
| `List.map`, `List.filter` | `knows_rename`, `pullback` | finite list transformations on the carrier and the observer's views |
| `σ`, `τ` with `∀ x, σ (τ x) = x` | `knows_rename` | metatheory functions providing a left-invertible renaming |

**What the system holds.** For `correspondence_matters`: the carrier `[0, 1, 2]`
and the tables `p1`, `p2`, `fun x => p2 (swap01 x)`, and `q3`. For
`Correspondence.lean`: the carrier `D`, the map `f`'s values on `D`, and the
finite view lists of `E` and `pullback D f E`.

**Admissions relied on, and their price.** This unit prices the third admission
of Unit 00 (the shared carrier). Identifying datum `x` of one member with datum
`x` of another is an external correspondence supplied by the presentation of the
family, not a consequence of the members' individual tables (`AI-04`). When an
observer reads through a correspondence `f`, collapses caused by `f x = f y`
belong to `f` rather than the observer (`TT-19`), and sharpness for the identity
through `f` requires `f` to be faithful (`TT-20`, `TT-21`).

**Phrases to read with care.**

- "Correspondence matters." The displayed one-member permutation changes
  the joint groups and loses the stated question. Not every one-member
  permutation must change recoverability. Consistent renaming preserves
  the knowledge relation when the theorem's read-back condition holds.
- "Faithful correspondence." `Faithful D f` is injectivity of `f` restricted to
  `D`. It is required when observing the identity `fun x => x` sharply through
  `f`, and is not required when observing a coarser presentation `p` whose
  fibers already merge the pairs merged by `f`.

## What it shows, and what it does not

It shows that the alignment of data across members of a family is an explicit
admission: permuting a single member (`swap01`) destroys the exceeding witness
of Unit 04, while permuting the carrier, all members, and the claim by one
left-invertible renaming preserves `Knows`.

It shows the exact relationship between a correspondence `f`, an institution's
representative `pQ D Q`, and a pulled-back observer `pullback D f E`:
`pQ D Q` is faithful on `D` iff `Q` knows the identity on `D`; sharpness
transports along every `f` without assuming fidelity; and sharp observation of
`q` through `f` forces `FiberConstant D f q`.
The last implication is a necessary condition. It does not establish
sharpness for an arbitrary supplied observer satisfying no further condition.

It does not show how to discover whether two members in the wild share a
carrier alignment without already having a joint observation or an admitted
correspondence.

## Sources

| Item | Where |
|---|---|
| `swap01`, `correspondence_matters`, `knows_rename` | `research/actor_institution/lean/ResearchActorInstitution/Institution.lean` lines 200–245 |
| `Faithful`, `collapsed_of_merged`, `constant_collapses_all`, `constant_not_faithful`, `faithful_iff_fiberIdentity` | `research/two_theorems/lean/ResearchTwoTheorems/Correspondence.lean` lines 35–68 |
| `faithful_actor_iff`, `empty_actor_constant`, `empty_actor_not_faithful` | the same file, lines 72–94 |
| `pullback`, `verdict_pullback`, `sharp_pullback_iff`, `fiberConstant_of_sharp_pullback`, `faithful_of_sharp_identity`, `sharp_identity_pullback` | the same file, lines 99–177 |
| Python mirrors | `research/actor_institution/model.py` line 459 (`correspondence_matters`); `research/two_theorems/model.py` lines 524–582 (`faithful`, `pullback`, `fiber_constant`, `correspondence_checks`) |
| Check | `textbook/institutions/checks/i05_correspondence.py` |
| Ledger | `research/actor_institution/CLAIMS.md` AI-04; `research/two_theorems/CLAIMS.md` TT-19, TT-20, TT-21, TT-21c |
