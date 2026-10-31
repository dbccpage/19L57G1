# Unit 73 — A Side Can Be Imposed, Not Chosen Symmetrically, and Composition Without an Operator

**Claim.** On an inhabited carrier, an orbit-constant equivariant endomap exists exactly when the action has a common fixed point. A separate composition relation need not supply uniqueness or associativity.



---

## First pass

First consider a swap of the two items `false` and `true`. A rule
that always returns `false` picks the same side throughout the pair.
Now compare two operations:

| Operation | Result |
|---|---|
| Swap the input, then apply the constant rule | `false` |
| Apply the constant rule, then swap its output | `true` |

The rule does not commute with the swap. **Equivariant** means these
two operations agree; **orbit-constant** means the chosen output is
the same for inputs related by the permitted symmetries.

**Predict.** Would returning the input unchanged satisfy both conditions?

<details>
<summary>Check your prediction</summary>

No. It commutes with the swap but changes its output along the orbit.
With an inhabited carrier, having both properties requires a common
fixed point: an item unchanged by every permitted symmetry. The swap has none. The inhabitant hypothesis matters:
on the empty carrier the conditions hold vacuously.

</details>

**A separate composition question.** A relation can allow both arrows
`false` and `true` as composites of the same pair of arrows. Choosing
`true` is then possible, but the relation has not determined it uniquely.
Existence, uniqueness, selection, and associativity are separate questions.

<details>
<summary>Detailed statement and formal anchors (optional)</summary>

## Detailed claim and formal anchors

In `lean4/Derivation/Breaking.lean`, an action `act : Sym → W → W` on an inhabited carrier `w : W` admits an endomap `s : W → W` that is simultaneously orbit-constant (`∀ g w, s (act g w) = s w`) and equivariant (`∀ g w, s (act g w) = act g (s w)`) if and only if `act` has a common fixed point (`∃ p, ∀ g, act g p = p`) (`selector_iff_common_fixed_point`).

Consequently, for any fixed-point-free involution `B : Break` (`no_orbit_constant_equivariant_endomap`) or any fixed-point-free family `S : Symmetry` (`no_orbit_constant_equivariant_selector`), no inhabited carrier admits an orbit-constant equivariant selector, although a side can be imposed without equivariance (`imposable_but_not_equivariant` on `boolBreak` via `constFalse`); and on the 3-element type `Tri`, no fixed-point-free involution exists at all (`no_fixed_point_free_involution_on_Tri`), whereas the 3-cycle `rot` forms a valid `Symmetry` (`triSymmetry`).

In the parked companion module `lean4/Derivation/Composing.lean`, a relational `Web` (`Composes : (a b c : Node) → Arr a b → Arr b c → Arr a c → Prop`) can fail totality (`composition_may_fail`), fail identity existence (`noneCompose_no_identity`), have non-unique composites (`composite_may_be_nonunique`) while still admitting a total composite-selection function (`selection_is_possible`), and fail both one-way and full relational associativity (`skew_not_relAssocLeft`, `skew_not_relAssoc`).

Every theorem in both modules is axiom-free (`none`), and neither module defines a Layer 3 bridge to `Regime`, `DiffObs`, `PresIso`, `NonZeroPair`, or `HFamily`.

</details>

## Question

Suppose a carrier `W` carries a reflection `e : W → W` with `e (e w) = w` and `e w ≠ w` (or, more generally, an action `act : Sym → W → W` with no common fixed point). Can we define a selector `s : W → W` that picks the same representative on both sides of each orbit (`s (e w) = s w`) while also commuting with the reflection (`s (e w) = e (s w)`)? Why does restricting to a single fixed-point-free involution exclude the 3-element carrier `Tri`, and what exact premise does the selector obstruction actually consume? Second, if we drop the assumption that arrow composition is a total single-valued binary operator and instead declare only a three-place composition relation `Composes a b c f g h : Prop` (`Web`), which algebraic properties can fail independently, and does non-uniqueness of composites prevent a total selector function from picking a valid composite for every pair?

---

## What we already possess

Neither `Breaking.lean` nor `Composing.lean` contains any explicit `import` line; both elaborate over Lean's implicit `Init` prelude (`Bool`, `Empty`, `Unit`, `And`, `Or`, `Exists`, `False`, `Eq`).
- `Breaking.lean` (445 lines) is imported by `lean4/Derivation.lean` (line 62), which prints `#print axioms` reports for 7 of its 15 theorems (`artifacts/lean_axioms.txt` lines 1476–1482), and is discussed in `paper/representative_selection.md`.
- `Composing.lean` (228 lines) is **parked**: it is not imported by `lean4/Derivation.lean`, but is imported by the second `defaultTargets` root `lean4/ParkedAudit.lean` (line 5), which prints `#print axioms` reports for all 7 of its theorems (`artifacts/lean_axioms.txt` lines 1483–1489).

---

## New concept

### Part 1: Fixed-point-free involutions, general symmetries, and the selector characterization (`Breaking.lean`)

1. **`Break` and its models (`emptyBreak`, `fourBreak`, `boolBreak`, lines 84–195).**
   - `structure Break` (lines 84–91) packages `Whole : Type`, `e : Whole → Whole`, `e_involutive : ∀ w, e (e w) = w`, and `e_no_fixed : ∀ w, e w ≠ w`.
   - `ne_image` (line 94) restates `e_no_fixed`, and `two_cycle` (lines 99–101) bundles `⟨B.e_no_fixed w, B.e_involutive w⟩`.
   - `SingleOrbit B : Prop := ∀ w w' : B.Whole, w' = w ∨ w' = B.e w` (lines 107–108).
   - Three models demonstrate that `Break` forces neither non-emptiness nor two-element cardinality:
     - `emptyBreak` (lines 112–116): `Whole := Empty`, `e x := nomatch x` (0 elements).
     - `fourBreak` (lines 122–131): `Whole := Bool × Bool`, `e p := (!p.1, p.2)` (4 elements in two 2-element orbits `{(false, false), (true, false)}` and `{(false, true), (true, true)}`). `fourBreak_not_singleOrbit` (lines 138–142) establishes `¬ SingleOrbit fourBreak`.
     - `boolBreak` (lines 179–183): `Whole := Bool`, `e := not` (2 elements in a single orbit, proved by `boolBreak_singleOrbit`, lines 188–194).
2. **Selectors on `Break`: `Represents`, `OrbitConstant`, `Equivariant` (lines 146–219).**
   - For `s : Selector B` (`B.Whole → B.Whole`):
     - `Represents B s : Prop := ∀ w, s w = w ∨ s w = B.e w` (lines 149–150).
     - `OrbitConstant B s : Prop := ∀ w, s (B.e w) = s w` (lines 153–154).
     - `Equivariant B s : Prop := ∀ w, s (B.e w) = B.e (s w)` (lines 157–158).
   - `no_orbit_constant_equivariant_endomap` (lines 172–175): given an inhabitant `w : B.Whole`, `OrbitConstant B s`, and `Equivariant B s`, derives `False` in one line:
     $$B.\mathrm{e}\;(s\;w) \stackrel{\text{equi}}{=} s\;(B.\mathrm{e}\;w) \stackrel{\text{const}}{=} s\;w,$$
     contradicting `B.e_no_fixed (s w)`. Notice two crucial facts documented in the comment (lines 163–171):
     1. The proof does **not** use `Represents B s`.
     2. The proof **does** require an inhabitant `w : B.Whole`: on `emptyBreak`, `emptySel` vacuously satisfies `Represents`, `OrbitConstant`, and `Equivariant` (`Textbook.U73.emptySel_all_three`).
   - On `boolBreak`, `constFalse : Selector boolBreak := fun _ => false` (line 196) satisfies `constFalse_represents` (line 198) and `constFalse_orbitConstant` (line 204), and fails `constFalse_not_equivariant` (line 210), packaged together as `imposable_but_not_equivariant` (lines 214–218): a side can be imposed (`constFalse`), or equivariance can be preserved without orbit-constancy (`id`, proved in `Textbook.U73.idSel_equivariant_not_orbitConstant`), but not both.
3. **Why `Break` cannot be instantiated on `Tri`, and the generalization to `Symmetry` (lines 243–424).**
   - `inductive Tri | t0 | t1 | t2` (lines 322–324) has 3 elements. `no_fixed_point_free_involution_on_Tri` (lines 347–385) establishes by finite case analysis on `e .t0`, `e .t1`, `e .t2` that no `e : Tri → Tri` can satisfy both `∀ w, e (e w) = w` and `∀ w, e w ≠ w`.
   - `structure Symmetry` (lines 243–247) drops the involution law and single-operator restriction: it declares `Whole : Type`, `Sym : Type`, `act : Sym → Whole → Whole`, and `no_common_fixed : ∀ w, ∃ g, act g w ≠ w`. Every `Break` embeds into `Symmetry` via `ofBreak` (lines 314–318, `Sym := Unit`), while `triSymmetry` (lines 334–338) instantiates `Symmetry` on `Tri` using the 3-cycle `rot` (`t0 ↦ t1 ↦ t2 ↦ t0`).
   - What exact premise does the selector obstruction use? Not even `∀ w, ∃ g, act g w ≠ w`, but the constructively weaker negation `¬ ∃ p, ∀ g, act g p = p`!
     - `no_selector_of_no_common_fixed_point` (lines 269–274) establishes that for any bare action `act : Sym → W → W`, inhabitant `w : W`, and `s : W → W`, if `¬ ∃ p, ∀ g, act g p = p`, then `s` cannot be both orbit-constant and equivariant because `s w` would be fixed by every `g`: `act g (s w) = s (act g w) = s w`.
     - `no_common_fixed_point` (lines 283–285) establishes `(∀ w, ∃ g, S.act g w ≠ w) → ¬ ∃ p, ∀ g, S.act g p = p` (while noting that the converse requires decidability not assumed in `Breaking.lean`), and `no_orbit_constant_equivariant_selector` (lines 306–310) is its immediate corollary.
     - Conversely, when `act` **does** have a common fixed point `p : W` (`∀ g, act g p = p`), `selector_exists_at_common_fixed_point` (lines 398–402) shows that the constant map `fun _ => p` is both orbit-constant and equivariant.
     - Combining both directions on an inhabited carrier `(w : W)`, `selector_iff_common_fixed_point` (lines 415–423) establishes the exact characterization:
       $$\bigl(\exists s : W \to W,\; (\forall g\,w,\; s(\mathrm{act}\;g\;w) = s\;w) \land (\forall g\,w,\; s(\mathrm{act}\;g\;w) = \mathrm{act}\;g\;(s\;w))\bigr) \;\Longleftrightarrow\; \bigl(\exists p : W,\; \forall g,\; \mathrm{act}\;g\;p = p\bigr).$$

### Part 2: Relational composition without an operator (`Composing.lean`)

`structure Web` (lines 79–82) declares `Node : Type`, `Arr : Node → Node → Type`, and a three-place relation `Composes : (a b c : Node) → Arr a b → Arr b c → Arr a c → Prop`. Using three concrete 1-node (`Node := Unit`), 2-arrow (`Arr _ _ := Bool`) models, `Composing.lean` separates four independent questions:

| Question | Predicate in `Composing.lean` | Witness `Web` | Theorem in `Composing.lean` (and descriptive shorthand) |
| :--- | :--- | :--- | :--- |
| Must every composable pair have a composite? | `Composable W a b c f g` (L86) | `noneCompose` (`Composes := False`, L92) | `composition_may_fail` (L99; shorthand: `not_all_composable`) |
| Must a node have a two-sided neutral arrow? | `HasIdentity W a` (L105) | `noneCompose` (L92) | `noneCompose_no_identity` (L112; shorthand: `not_has_identity`) |
| Is a composite unique when it exists? | `Composes` single-valuedness | `allCompose` (`Composes := True`, L118) | `composite_may_be_nonunique` (L126; shorthand: `not_unique_composite`) |
| Does non-uniqueness forbid a total selector? | `∀ a b c f g, Composes a b c f g (sel a b c f g)` | `allCompose` with `allSelect := true` (L134) | `selection_is_possible` (L142) |
| Does left-bracketed reachability equal right-bracketed reachability? | `RelAssocLeft` (L171) and `RelAssoc` (L163) | `skewCompose` (`h = (f && !g)`, L181) | `relAssocLeft_of_relAssoc` (L176), `skew_not_relAssocLeft` (L188), `skew_not_relAssoc` (L198; shorthand: `not_relAssoc`) |

---

## Plain-language interpretation

- **`Breaking.lean`:** Imagine a pair of shoes `{Left, Right}` under the reflection `e` that swaps `Left ↔ Right`.
  - If you want a rule `s` that picks **the same shoe** regardless of which one you hand it (`OrbitConstant`: `s(Left) = s(Right)`), you can impose `constFalse` ("always pick `Left`").
  - If you want a rule `s` that **respects the reflection** (`Equivariant`: swapping the input swaps the output), you can use `id` ("keep whichever shoe you were handed").
  - What you cannot have is both at once: if `s(e(w)) = s(w)` and `s(e(w)) = e(s(w))`, then `e(s(w)) = s(w)`, meaning the chosen shoe `s(w)` would have to be its own opposite (`Left = Right`). An orbit-constant equivariant selector exists on an inhabited set if and only if the symmetry has a stationary anchor point (`selector_iff_common_fixed_point`).
- **`Composing.lean`:** If "composing arrow `f` with arrow `g` gives `h`" is written as a relation `Composes a b c f g h` rather than a function `g ∘ f = h`:
  - Some pairs `(f, g)` may have **zero** composites (`noneCompose`: `composition_may_fail` and `noneCompose_no_identity`).
  - Some pairs `(f, g)` may have **multiple** composites (`allCompose`: `composite_may_be_nonunique`). Yet having multiple composites does **not** stop us from defining a function `allSelect` that picks `true` every time (`selection_is_possible`).
  - Even when every pair `(f, g)` has a unique composite `h = f && !g` (`skewCompose`), bracketing `((true, false), true)` on the left gives `(true && !false) && !true = true && false = false`, whereas bracketing `(true, (false, true))` on the right gives `true && !(false && !true) = true && !false = true` (`skew_not_relAssocLeft` and `skew_not_relAssoc`).

---

## Pseudocode

```text
FUNCTION has_orbit_constant_equivariant_selector(carrier, symbols, act):
    IF carrier IS EMPTY:
        RETURN True   # vacuous empty selector
    FOR EACH p IN carrier:
        IF ALL(act(g, p) == p FOR g IN symbols):
            RETURN True   # constant selector s(w) = p works
    RETURN False          # no_selector_of_no_common_fixed_point

FUNCTION rel_assoc_left(web):
    FOR EACH a, b, c, d IN web.nodes:
        FOR EACH f IN web.arrows(a, b), g IN web.arrows(b, c), k IN web.arrows(c, d), w IN web.arrows(a, d):
            left_ok  = ANY(web.composes(a,b,c,f,g,u) AND web.composes(a,c,d,u,k,w) FOR u IN web.arrows(a,c))
            right_ok = ANY(web.composes(b,c,d,g,k,v) AND web.composes(a,b,d,f,v,w) FOR v IN web.arrows(b,d))
            IF left_ok AND NOT right_ok:
                RETURN False
    RETURN True
```

---

## Python

The standalone check script `textbook/checks/u73_breaking_composing.py` tests `emptyBreak`, `boolBreak`, `fourBreak`, all 27 endomaps on `Tri`, `triSymmetry`, `tri_fix0`, `noneCompose`, `allCompose`, `skewCompose`, and the `artifacts/lean_axioms.txt` / `KIND_ROLE_OVERRIDES` audit properties:

```python
@dataclass(frozen=True)
class FiniteBreak(Generic[W]):
    carrier: list[W]
    e: Callable[[W], W]

    def is_valid(self) -> bool:
        return all(self.e(self.e(w)) == w for w in self.carrier) and all(
            self.e(w) != w for w in self.carrier
        )

    def single_orbit(self) -> bool:
        return all(
            w2 == w1 or w2 == self.e(w1)
            for w1 in self.carrier
            for w2 in self.carrier
        )

    def represents(self, s: Callable[[W], W]) -> bool:
        return all(s(w) == w or s(w) == self.e(w) for w in self.carrier)

    def orbit_constant(self, s: Callable[[W], W]) -> bool:
        return all(s(self.e(w)) == s(w) for w in self.carrier)

    def equivariant(self, s: Callable[[W], W]) -> bool:
        return all(s(self.e(w)) == self.e(s(w)) for w in self.carrier)
```

---

## Line-by-line Python explanation

- **`FiniteBreak` (lines 21–43 of `u73_breaking_composing.py`):** Mirrors `Breaking.Break`, `SingleOrbit`, `Represents`, `OrbitConstant`, and `Equivariant`. In `main()` (lines 176–205), it verifies that:
  - `empty_break` (carrier `[]`) vacuously satisfies `orbit_constant` and `equivariant`.
  - `bool_break` (carrier `[False, True]`) satisfies `single_orbit()`, has `const_false` satisfying `represents` and `orbit_constant` while failing `equivariant`, and has 0 of its 4 endomaps satisfying both `orbit_constant` and `equivariant`.
  - `four_break` (carrier `(Bool × Bool)`) is a valid `Break` that fails `single_orbit()`.
- **`FiniteAction` and exhaustive `Tri` check (lines 46–69 and 207–238):** Enumerates all $3^3 = 27$ functions `Tri → Tri` on `[0, 1, 2]`:
  - Exactly 4 of the 27 are involutions (`id` and the 3 transpositions), and none of those 4 is fixed-point-free (`no_fixed_point_free_involution_on_Tri`).
  - Under the 3-cycle `tri_rot`, `common_fixed_points()` is `[]` and 0 of the 27 endomaps is both orbit-constant and equivariant (`no_orbit_constant_equivariant_selector`).
  - Under `tri_fix0` (`0 ↦ 0, 1 ↦ 2, 2 ↦ 1`), `common_fixed_points()` is `[0]` and the unique orbit-constant equivariant selector is `s(w) = 0` (`selector_iff_common_fixed_point`).
- **`FiniteWeb` (lines 72–128 and 240–275):** Mirrors `Composing.Web`, `Composable`, `HasIdentity`, `LeftReach`, `RightReach`, `RelAssocLeft`, and `RelAssoc`, verifying `noneCompose`, `allCompose` (with `allSelect`), and `skewCompose` (`(True, False, True)` reaches `False` on the left via `u = True` and fails on the right).
- **Audit checks on `artifacts/lean_axioms.txt` (lines 131–163 and 277–288):**
  - Verifies **Audit Finding 1 of `Breaking.md` (§11):** Although `Breaking.lean` line 52 and `paper/representative_selection.md` line 30 say `Derivation.lean` prints an axiom report for "each of its exported theorems," `Derivation.lean` (lines 1636–1642) only prints 7 of the 15 theorems in `Breaking.lean` (`BREAKING_REPORTED_7`), omitting the other 8 (`BREAKING_UNREPORTED_8`). (All 8 omitted theorems are still checked by `ci/check_declaration_axioms.py` and by our `u73_lean.py`!).
  - Verifies **Audit Finding §11 of `Composing.md`:** Although `Composing.lean` header lines 52–70 state that `Composing.lean` contributes no `#print axioms` lines to `artifacts/lean_axioms.txt`, `lean4/ParkedAudit.lean` (a `defaultTargets` root in `lakefile.toml`) now imports `Derivation.Composing` and emits `#print axioms` lines for all 7 theorems into `artifacts/lean_axioms.txt` (lines 1483–1489).

---

## Lean 4

The check script `textbook/checks/u73_lean.py` kernel-checks four complementary theorems in `Textbook.U73` and prints axiom reports for all 15 theorems in `Breaking` plus all 7 theorems in `Composing`:

```lean
import Derivation.Breaking
import Derivation.Composing

namespace Textbook.U73

open Breaking
open Composing

-- 1. Over emptyBreak, a selector is vacuously Represents, OrbitConstant, and Equivariant
--    (witnessing why an inhabitant w : B.Whole is required by no_orbit_constant_equivariant_endomap).
def emptySel : Selector emptyBreak := fun x => nomatch x

theorem emptySel_all_three :
    Represents emptyBreak emptySel ∧
    OrbitConstant emptyBreak emptySel ∧
    Equivariant emptyBreak emptySel :=
  ⟨(fun w => nomatch w), (fun w => nomatch w), (fun w => nomatch w)⟩

-- 2. On boolBreak, id is Represents and Equivariant, but NOT OrbitConstant
--    (dual to constFalse, which is Represents and OrbitConstant, but NOT Equivariant).
def idSel : Selector boolBreak := id

theorem idSel_equivariant_not_orbitConstant :
    (Represents boolBreak idSel ∧ Equivariant boolBreak idSel) ∧
    ¬ OrbitConstant boolBreak idSel := by
  refine ⟨⟨fun w => Or.inl rfl, fun _ => rfl⟩, ?_⟩
  intro h
  exact Bool.noConfusion (h false)

-- 3. On Tri, an involution fixing t0 and swapping t1 ↔ t2 has a common fixed point t0,
--    so selector_exists_at_common_fixed_point gives an orbit-constant equivariant selector.
def swap12 : Tri → Tri
  | .t0 => .t0
  | .t1 => .t2
  | .t2 => .t1

theorem swap12_has_selector :
    ∃ s : Tri → Tri,
      (∀ _ : Unit, ∀ w : Tri, s (swap12 w) = s w) ∧
      (∀ _ : Unit, ∀ w : Tri, s (swap12 w) = swap12 (s w)) :=
  selector_exists_at_common_fixed_point (fun (_ : Unit) => swap12) .t0 (fun _ => rfl)

-- 4. In Composing, allCompose satisfies full relational associativity RelAssoc
--    (showing RelAssoc is inhabited, whereas skewCompose refutes it).
theorem allCompose_relAssoc : RelAssoc allCompose := by
  intro a b c d f g k w
  exact ⟨fun _ => ⟨true, trivial, trivial⟩, fun _ => ⟨true, trivial, trivial⟩⟩

end Textbook.U73
```

---

## Line-by-line Lean explanation

- **`emptySel` and `emptySel_all_three` (lines 11–17):** Define the empty function on `emptyBreak.Whole = Empty` by `nomatch x` and prove that it satisfies `Represents`, `OrbitConstant`, and `Equivariant` simultaneously. This confirms the honesty note in `Breaking.lean` (lines 169–171 and 304–305): without an inhabitant `w : B.Whole`, there is no selector obstruction.
- **`idSel` and `idSel_equivariant_not_orbitConstant` (lines 21–28):** Exhibit the dual of `imposable_but_not_equivariant`: on `boolBreak`, `id` represents every orbit and commutes with `not`, and fails `OrbitConstant` at `false`.
- **`swap12` and `swap12_has_selector` (lines 32–41):** Show that on `Tri`, an involution *with* a fixed point (`t0 ↦ t0, t1 ↔ t2`) satisfies the hypothesis of `selector_exists_at_common_fixed_point`, yielding the constant selector `fun _ => .t0`.
- **`allCompose_relAssoc` (lines 45–47):** Establishes that `allCompose` satisfies `RelAssoc allCompose`, complementing `skew_not_relAssoc : ¬ RelAssoc skewCompose` by showing that `RelAssoc` is non-vacuously satisfiable.
- **Complete 26-theorem `#print axioms` check (lines 51–80 of `u73_lean.py`):** Verifies that all 4 `Textbook.U73` theorems, all 15 `Breaking` theorems (both the 7 in `Derivation.lean` and the 8 omitted from `Derivation.lean`), and all 7 `Composing` theorems depend on **zero axioms** (`none`).

---

## What has been proved

| Module | Total theorems | In `artifacts/lean_axioms.txt` | Axiom footprint | Core established statements |
| :--- | :---: | :---: | :--- | :--- |
| `Breaking` (root-imported) | 15 | 7 (lines 1476–1482 via `Derivation.lean`; 8 helper/model theorems omitted from `Derivation.lean` and covered by `ci/check_declaration_axioms.py` and `u73_lean.py`) | All 15 axiom-free (`none`) | `no_orbit_constant_equivariant_endomap`, `imposable_but_not_equivariant`, `no_selector_of_no_common_fixed_point`, `no_common_fixed_point`, `no_orbit_constant_equivariant_selector`, `no_fixed_point_free_involution_on_Tri`, `selector_exists_at_common_fixed_point`, `selector_iff_common_fixed_point` |
| `Composing` (parked) | 7 | 7 (lines 1483–1489 via `ParkedAudit.lean`) | All 7 axiom-free (`none`) | `composition_may_fail`, `noneCompose_no_identity`, `composite_may_be_nonunique`, `selection_is_possible`, `relAssocLeft_of_relAssoc`, `skew_not_relAssocLeft`, `skew_not_relAssoc` |

1. **What it supports:**
   - Over an inhabited carrier `w : W`, an action `act : Sym → W → W` admits an orbit-constant equivariant endomap `s : W → W` if and only if `act` has a common fixed point (`selector_iff_common_fixed_point`, axiom-free).
   - On `boolBreak`, `constFalse` is orbit-constant and represents every orbit, failing only equivariance (`imposable_but_not_equivariant`), while on `Tri`, no fixed-point-free involution exists (`no_fixed_point_free_involution_on_Tri`) and `triSymmetry` exhibits a fixed-point-free 3-cycle.
   - In `Composing.Web`, totality (`composition_may_fail`), identity existence (`noneCompose_no_identity`), composite uniqueness (`composite_may_be_nonunique`), and relational associativity (`skew_not_relAssocLeft`, `skew_not_relAssoc`) can all fail on 2-arrow models, and non-uniqueness of composites does not prevent a total composite-selection function (`selection_is_possible`).
2. **What it does not support:**
   - Neither `Breaking.lean` nor `Composing.lean` connects to `Regime`, `DiffObs`, `PresIso`, `NonZeroPair`, `HFamily`, or tied minimal delta pairs: `paper/representative_selection.md` explicitly states that Layer 3 (a bridge from the regime calculus into `Breaking`) does not exist, and `Breaking.lean` lines 428–432 note that tied minimal responses in the regime calculus are separated by an isomorphism invariant rather than forming an orbit of `Symmetry`.
   - `Breaking.lean` does not prove that every finite `Break` carrier has even cardinality: only the 3-element case `Tri` is proved (`no_fixed_point_free_involution_on_Tri`), and the general even-cardinality statement is explicitly marked withdrawn/OPEN in `Breaking.lean` lines 227–235 (`Breaking.md` §4 & §11).
   - `Composing.lean` defines no notion of inverse arrow and establishes nothing about inverses (`Composing.lean` lines 215–220).
3. **The narrowest defensible claim:**
   - For any action `act : Sym → W → W` on an inhabited type `W`, existence of an orbit-constant equivariant endomap is constructively equivalent to existence of a common fixed point (`selector_iff_common_fixed_point`); and for a three-place composition relation `Web`, totality, identity existence, uniqueness, and relational associativity are independent conditions that fail on concrete 1-node `Bool`-arrow models while `allCompose` still admits the total selector `allSelect`.
4. **The next test needed:**
   - Inspect the remaining parked modules in `lean4/Derivation/` — the form-renaming and isomorphism transport family (`FormRenaming`, `FormTransport`, `IsoCollapse`, `IsoCanon`, `IsoBridge`, and the five `*Compat` modules) together with `code/derivation/iso.py` and the two-root audit architecture (`Derivation.lean`, `ParkedAudit.lean`, `ci/check_parked_audit.py`, and `ci/check_declaration_axioms.py`) in Unit 74.

---

## What has not been proved

The in-file self-audit comments in `Breaking.lean` and `Composing.lean` (and their module audits `Breaking.md` and `Composing.md`) document several withdrawn earlier overclaims and remaining gaps:

1. **Audit Finding 1 in `Breaking.md` (§11): 8 of 15 `Breaking` theorems are not listed in `Derivation.lean`.** `Breaking.lean` line 52 and `paper/representative_selection.md` line 30 state that `Derivation.lean` prints an axiom report for "each of its exported theorems." In fact, `Derivation.lean` lines 1636–1642 print only 7 theorems (`no_orbit_constant_equivariant_endomap`, `no_selector_of_no_common_fixed_point`, `no_common_fixed_point`, `no_orbit_constant_equivariant_selector`, `no_fixed_point_free_involution_on_Tri`, `selector_exists_at_common_fixed_point`, `selector_iff_common_fixed_point`), omitting `ne_image`, `two_cycle`, `fourBreak_not_singleOrbit`, `boolBreak_singleOrbit`, `constFalse_represents`, `constFalse_orbitConstant`, `constFalse_not_equivariant`, and `imposable_but_not_equivariant`. All 15 are verified axiom-free in `ci/check_declaration_axioms.py` and `textbook/checks/u73_lean.py`.
2. **Audit Finding in `Composing.md` (§11): Stale header provenance note on `Composing.lean`.** `Composing.lean` lines 52–70 state that `Composing.lean` contributes no `#print axioms` lines to `artifacts/lean_axioms.txt`. That note is stale in the safe direction: `ParkedAudit.lean` (added as a second `defaultTargets` root in `lean4/lakefile.toml`) imports `Derivation.Composing` and emits `#print axioms` reports for all 7 of its theorems into `artifacts/lean_axioms.txt` (lines 1483–1489), while `ci/check_declaration_axioms.py` audits `allSelect` and all other declarations.
3. **Withdrawn overclaims in `Breaking.lean` and `Composing.lean` headers:**
   - *"imports NOTHING"*: withdrawn (`Init` is implicitly imported).
   - *"two-ness derived by `two_arises`"* and *"no global section (`no_global_section`)"*: withdrawn (`emptyBreak` has 0 elements, `fourBreak` has 4, and no quotient or projection is defined in `Breaking.lean`).
   - *"every finite `Break` carrier has even cardinality"*: withdrawn and downgraded to OPEN (lines 227–235); only the `Tri` case is proved.
   - Converse `(¬ ∃ p, ∀ g, act g p = p) → (∀ w, ∃ g, act g w ≠ w)`: not proved because it requires decidability not assumed in `Breaking.lean` (lines 278–282).
   - *"no function could extract the composite"* when uniqueness fails: refuted by `Composing.selection_is_possible` (lines 138–146).
   - *"identities and inverses each exhibited failing"*: withdrawn for inverses (lines 215–220); no inverse predicate is defined in `Composing.lean`.

---

## Outside the system

- **Implicit `Init` prelude.** Both modules use only Lean's built-in `Init` types (`Bool`, `Empty`, `Unit`, `Tri` with `deriving DecidableEq`) and logical connectives, with zero external `Derivation.*` imports.
- **Constructive axiom-free proofs.** Every theorem in `Breaking.lean` (15/15) and `Composing.lean` (7/7) has empty axiom footprint (`does not depend on any axioms`) in the Lean 4 kernel — no `propext`, no `Quot.sound`, and no `Classical.choice`.

---

## Student exercise

1. On `fourBreak` (`Whole := Bool × Bool`, `e(b₁, b₂) = (!b₁, b₂)`), define `s(b₁, b₂) = (false, b₂)`.
   - Does `s` satisfy `Represents fourBreak s`?
   - Does `s` satisfy `OrbitConstant fourBreak s`?
   - Does `s` satisfy `Equivariant fourBreak s`?
2. On `skewCompose` (`Node := Unit`, `Arr _ _ := Bool`, `Composes _ _ _ f g h := (h = (f && !g))`), evaluate all possible left-bracketed results `LeftReach skewCompose () () () () f g k w` and right-bracketed results `RightReach skewCompose () () () () f g k w` for `(f, g, k) = (true, true, true)`. Do `LeftReach` and `RightReach` agree on `(true, true, true)`, or do they disagree? Compare with `(true, false, true)`.

---

<details>
<summary>Student exercise answer</summary>

1. For `s(b₁, b₂) = (false, b₂)` on `fourBreak`:
   - **`Represents fourBreak s` is True:** If `b₁ = false`, `s(false, b₂) = (false, b₂) = (b₁, b₂)`. If `b₁ = true`, `s(true, b₂) = (false, b₂) = (!true, b₂) = e(true, b₂)`.
   - **`OrbitConstant fourBreak s` is True:** `s(e(b₁, b₂)) = s(!b₁, b₂) = (false, b₂) = s(b₁, b₂)`.
   - **`Equivariant fourBreak s` is False:** At `(false, false)`, `s(e(false, false)) = (false, false)`, whereas `e(s(false, false)) = e(false, false) = (true, false) != (false, false)` (as required by `no_orbit_constant_equivariant_endomap`).
2. For `skewCompose` (`h = f && !g`):
   - On `(f, g, k) = (true, true, true)`:
     - **Left bracketing `((true, true), true)`:** First step `u = true && !true = false`; second step `w = u && !true = false && false = false`.
     - **Right bracketing `(true, (true, true))`:** First step `v = true && !true = false`; second step `w = true && !v = true && !false = true`.
     - Thus `(true, true, true)` also witnesses failure of associativity (`LeftReach` reaches `false`, `RightReach` reaches `true`), just as `(true, false, true)` reaches `false` on the left (`u = true`, `w = false`) and `true` on the right (`v = false`, `w = true`).

---

</details>

## Verification

Run both check scripts from the repository root:

```bash
python textbook/checks/u73_breaking_composing.py
python textbook/checks/u73_lean.py
```

Both commands exit with status `0` and `failures: []`.
