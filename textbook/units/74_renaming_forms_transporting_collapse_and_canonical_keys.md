# Unit 74 — Renaming Forms, Transporting Collapse, and Canonical Keys

**Claim.** Form renaming transports the stated observations. The bridge from record relabeling to isomorphism requires ordered requirements; list equality, membership equality, and Python search results remain distinct.

<details>
<summary>Sources and classification (optional)</summary>

**Status:** `FROZEN` / `CONDITIONAL` (ordered requirements `∀ q ∈ r.reqs, q.1 ≤ q.2` required for `relabel_iso`, `iso_of_relabel_eq`, `Iso.of_components`, and `isoRefl`)
- **Lean:** `Derivation.renameForms_arity`, `Derivation.renameForms_gf`, `Derivation.collapsed_renameForms`, `Derivation.collapsed_renameDataForm`, `Derivation.Iso.symm`, `Derivation.Iso.collapsed_transport`, `Derivation.Iso.trans`, `Derivation.relabel_iso`, `Derivation.iso_of_relabel_eq`, `Derivation.Iso.of_components`
- **Axioms:** Within `{propext, Quot.sound}` (`mapInstForm_gf` and `plug_mapCtxForm` are `none`; `Regime.ext'`, `permForms_getD`, `renameForms_arity`, `collapsed_congr`, `mapReq_eq_sortPair`, `sortPair_*`, `relabel_*` use `propext`; the remaining declarations use `{propext, Quot.sound}`)
- **Depends on:** Unit 07 (`Erasure`), Unit 29 (`CountTransport`), Unit 31 (`TransitionTransport`), Unit 59 (`RenamingStructure`)

---

</details>

## First pass

A form has an index and an arity: how many arguments it expects.
Start with form 0 taking one argument and form 1 taking two. Swap the
two form indices:

| Before renaming | After renaming |
|---|---|
| Form 0 expects one argument | Form 1 expects one argument |
| Form 1 expects two arguments | Form 0 expects two arguments |
| Instance `(0, [0])` | Instance `(1, [0])` |
| Rule names form 0 | Rule names form 1 |

The argument datum 0 has stayed fixed; its form reference changed.
The book's `form_swap_table` checks the whole arity, instance, and rule
update.

**Predict.** Can we swap just the instance's form tag and leave the
arity table unchanged?

<details>
<summary>Check your prediction</summary>

No. The unchanged table would make form 1 expect two arguments, but
the instance has only one. A consistent renaming updates every affected
reference and the form table together.

</details>

Later comparisons need their own hypotheses. The declared `Iso` relation
uses sorted requirements; raw unordered records can fail even self-comparison.
Record equality, repeated list entries, and bounded Python search are
also different checks. Running out of search budget supplies no proof
that two records are non-isomorphic.

<details>
<summary>Detailed statement and formal anchors (optional)</summary>

## Detailed claim and formal anchors

In the parked form-renaming and isomorphism modules (`lean4/Derivation/FormRenaming.lean`, `FormTransport.lean`, `IsoCollapse.lean`, `IsoCanon.lean`, `IsoBridge.lean`, and their five `*Compat.lean` companions), permuting a regime's form-arity list via `permForms` and relabelling instance and rule form indices via `renameForms` preserves form arities (`renameForms_arity`), has a two-sided inverse on fixed-form-length fibres (`renameForms_gf`), and transports `wfCtx`, `derivable`, and observational collapse (`collapsed_renameForms`, `collapsed_renameDataForm`).

Across the membership-based isomorphism relation `Minimality.Iso`, `Iso.symm` and `Iso.trans` establish symmetry and transitivity, `Iso.collapsed_transport` transports observational collapse along `h.dmap`, `relabel_iso` establishes that the combined datum-and-form relabelling action produces an isomorphic regime when requirements are ordered, `iso_of_relabel_eq` establishes the canonical-key soundness kernel, and `Iso.of_components` bridges componentwise membership equality to `Iso`.

Finally, `lean4/Derivation.lean` (62 direct module imports, 1 482 axiom reports) together with `lean4/ParkedAudit.lean` (12 parked modules, 48 axiom reports) and `ci/check_declaration_axioms.py` (which also audits `Type`-valued definitions such as `Iso.symm`, `Iso.trans`, `relabel_iso`, `iso_of_relabel_eq`, and `Iso.of_components`) account for all 75 modules in `lean4/Derivation/` and all 1 530 lines of `artifacts/lean_axioms.txt`.

</details>

## Question

Units 29 and 31 showed how to relabel **datum** indices while leaving form indices fixed. What happens when we also permute **form** indices? How does observational collapse transport across both the record-level combined action (`renameForms` after `renameRegime`) and the set-membership isomorphism relation `Minimality.Iso`? What is the exact bridge between Lean's `relabel` action and Python's canonical-key deduplication in `code/derivation/iso.py` — including the four concrete places where record equality, list membership, permutation budgets, and requirement pair ordering diverge? And how do the two root targets `lean4/Derivation.lean` and `lean4/ParkedAudit.lean` audit all 75 modules in `lean4/Derivation/`?

---

## What we already possess

From earlier units we possess:

1. `Regime`, `Ctx`, `plug`, `wfCtx`, `derivable`, `collapsed` (`Basic.lean`, Units 00, 08, 09).
2. Bounded index bijections `DRen n` (`f`, `g`, `fbound`, `gbound`, `fg`, `gf`) and the datum-side action `renameRegime` (`CountTransport.lean`, Unit 29), together with the requirement-carrying datum action `renameRegimeR` and `mapReq` (`TransitionTransport.lean`, Unit 31).
3. The canonical isomorphism structure `Iso r s : Type` (`Minimality.lean`, Unit 21), which bundles bounded datum and form bijection pairs (`dmap`/`dinv`, `fmap`/`finv`), arity preservation (`arity`), and two-way list-membership implications (`insts_fwd`/`insts_bwd`, `rules_fwd`/`rules_bwd`, `reqs_fwd`/`reqs_bwd` via `sortPair`).

---

## New concept

### 1. Form renaming and arity preservation (`FormRenaming.lean`)

While data live only as a count `r.data : Nat`, forms live as an explicit arity list `r.forms : List Nat` whose $j$-th entry records the arity of form $j$. If a form bijection sends old form index $i$ to new form index $\varphi(i)$ with inverse $g$, then position $j$ of the permuted arity list must hold the arity of the form that lands at $j$, namely old position $g(j)$:

```lean
def permForms (g : Nat → Nat) (forms : List Nat) : List Nat :=
  (List.range forms.length).map (fun j => forms.getD (g j) 0)

def mapInstForm (φ : Nat → Nat) (i : Inst) : Inst := (φ i.1, i.2)

def renameForms (φ g : Nat → Nat) (r : Regime) : Regime :=
  { r with
    forms := permForms g r.forms
    insts := r.insts.map (mapInstForm φ)
    rules := r.rules.map φ }
```

- `permForms_getD` establishes `(permForms g forms).getD j 0 = forms.getD (g j) 0` for $j < \text{forms.length}$.
- `renameForms_arity` establishes that when $\varphi(i) < r.\text{forms.length}$ and $g(\varphi(i)) = i$, the new arity at $\varphi(i)$ equals the old arity at $i$:
  `(renameForms φ g r).forms.getD (φ i) 0 = r.forms.getD i 0`.
- `renameForms_gf` establishes that for any bounded bijection $\sigma : \text{DRen } r.\text{forms.length}$, applying `renameForms σ.f σ.g` followed by `renameForms σ.g σ.f` returns $r$ identically.

### 2. Observational transport under form and combined actions (`FormTransport.lean`)

A form renaming relabels the form index of a context while leaving its datum/hole slots untouched:

```lean
def mapCtxForm (φ : Nat → Nat) (c : Ctx) : Ctx := ⟨φ c.form, c.slots⟩
```

Because slots are untouched, `plug_mapCtxForm` holds by `rfl`:
`plug (mapCtxForm φ c) d = mapInstForm φ (plug c d)`.
Combined with `derivable_renameForms` and `wfCtx_renameForms` (which uses `permForms_getD` on the arity check), this yields:

- `collapsed_renameForms`: `collapsed (renameForms σ.f σ.g r) d d' ↔ collapsed r d d'`.
- `collapsed_renameDataForm`: composing a datum bijection $\sigma : \text{DRen } n$ ($r.\text{data} = n$) with a form bijection $\tau : \text{DRen } r.\text{forms.length}$ transports collapse:
  `collapsed (renameForms τ.f τ.g (renameRegime σ.f r)) (σ.f d) (σ.f d') ↔ collapsed r d d'`.
- `collapsed_congr`: two regimes agreeing on `forms`, `data`, `insts`, and `rules` (even if `reqs` differ) have identical `collapsed` relations.

**Why the record action and `Minimality.Iso` are distinct relations:**
1. `Iso` compares `insts`, `rules`, and `reqs` by list membership (`∈`), so `Iso` equates a regime with `insts = [p]` and one with duplicate entry `insts = [p, p]`, which no length-preserving list map `renameForms`/`renameRegime` can equate.
2. `renameRegime` leaves `reqs` untouched, whereas `Iso` requires `reqs` to map via `sortPair (dmap q.1, dmap q.2)`.

### 3. Transporting collapse across `Minimality.Iso` (`IsoCollapse.lean`)

Because `Minimality.Iso` is broader than the record action, `IsoCollapse.lean` establishes collapse transport directly from `Iso`'s fields:

- `Iso.symm (h : Iso r s) : Iso s r` swaps `(dmap, fmap)` with `(dinv, finv)` and establishes the reversed arity equation from `h.arity (h.finv f)` and `h.fmap_finv`.
- `Iso.cmap` maps a context $c$ to `⟨h.fmap c.form, c.slots.map (Option.map h.dmap)⟩`; `Iso.plug_cmap`, `Iso.wfCtx_cmap`, and `Iso.derivable_imap` transport plugging, context well-formedness, and derivability across $h$.
- `Iso.collapsed_transport` establishes that for $d, d' < r.\text{data}$:
  `collapsed s (h.dmap d) (h.dmap d') ↔ collapsed r d d'`.

### 4. Relabelling action, canonical-key soundness kernel, and list-reorder bridge (`IsoCanon.lean`, `IsoBridge.lean`)

To connect record-level relabelling to `Minimality.Iso`, `IsoCanon.lean` combines `renameRegimeR` (which maps `reqs` via `mapReq`) with `renameForms`:

```lean
def relabel (r : Regime) (π : DRen r.data) (φ : DRen r.forms.length) : Regime :=
  renameForms φ.f φ.g (renameRegimeR π.f r)
```

- `mapReq_eq_sortPair` establishes `mapReq f q = sortPair (f q.1, f q.2)`.
- `Iso.trans (h : Iso r s) (k : Iso s t) : Iso r t` composes two isomorphisms unconditionally (using `sortPair_map_sortPair` on `reqs`).
- `relabel_iso` constructs `Iso r (relabel r π φ)` under the hypothesis `hord : ∀ q ∈ r.reqs, q.1 ≤ q.2` (needed for `reqs_bwd`, because `sortPair (π.g (sortPair (π.f q.1, π.f q.2)))` simplifies to `sortPair (q.1, q.2)`, which equals `q` only when $q.1 \le q.2$).
- `iso_of_relabel_eq` establishes the **soundness kernel**: if `relabel r πr φr = relabel s πs φs` as regimes and both $r$ and $s$ have ordered requirements, then `Iso r s` holds via `(relabel_iso r πr φr hr).trans ((heq ▸ relabel_iso s πs φs hs).symm)`.
- `Iso.of_components` (`IsoBridge.lean`) closes the **list-reorder step**: if $A$ and $B$ have equal `data` and `forms`, equivalent membership `∀ x, x ∈ A.field ↔ x ∈ B.field` on `insts`, `rules`, and `reqs`, and ordered requirements on both sides, then `Iso A B` holds via the identity maps.

### 5. The five `*Compat` modules and the two-target audit architecture (`Derivation.lean` + `ParkedAudit.lean`)

Why are 13 of the 75 files in `lean4/Derivation/` not imported by `lean4/Derivation.lean`?
1. Five files (`DiffAnchorCompat.lean`, `FormTransportCompat.lean`, `IsoBridgeCompat.lean`, `IsoCanonCompat.lean`, `IsoCollapseCompat.lean`) are **two-line compatibility shims** whose first line is `import Derivation` and whose second line imports the corresponding parked module. They allow downstream consumers to import both the root library and the parked module in a single line; `Derivation.lean` cannot import them without creating a circular import (`Derivation` $\to$ `*Compat` $\to$ `Derivation`).
2. Seven files (`Composing.lean`, `DiffAnchor.lean`, `FormRenaming.lean`, `FormTransport.lean`, `IsoBridge.lean`, `IsoCanon.lean`, `IsoCollapse.lean`) are parked structural modules imported by `lean4/ParkedAudit.lean` (the second `defaultTargets` library in `lean4/lakefile.lean`). Together with the 5 `*Compat` files, that accounts for 12 parked modules; the 13th file not directly listed in `Derivation.lean` is `Derivation/LocalStrategy.lean`, which is transitively imported into the root build via `Derivation/G1Class.lean` (`import Derivation.LocalStrategy`), so 62 direct root imports + 1 transitive root import + 12 `ParkedAudit` imports = **75 modules**.
3. Notice one subtle detail in `ParkedAudit.lean`: its metaprogram `emitAxiomsFor` filters declarations by `isTheorem` (`ConstantInfo.thmInfo`). In `IsoCollapse.lean`, `IsoCanon.lean`, and `IsoBridge.lean`, the five constructors `Iso.symm`, `Iso.trans`, `relabel_iso`, `iso_of_relabel_eq`, and `Iso.of_components` are `def`s returning `Iso r s : Type` (a `structure` in `Type`, not `Prop`), so `ParkedAudit.lean` emits `#print axioms` for the 48 `theorem` declarations across the parked modules (`7 + 3 + 9 + 11 + 10 + 8 + 0 = 48`), while `ci/check_declaration_axioms.py` and `u74_lean.py` explicitly audit the `Type`-valued `def`s as well.

---

## Plain-language interpretation

Think of a regime as a ledger with two kinds of ID numbers: **datum IDs** ($0, 1, \dots, n-1$) for the items being compared, and **form IDs** ($0, 1, \dots, m-1$) for the test tables.
- Earlier lessons showed that swapping datum IDs does not change which items are collapsed. `FormRenaming` and `FormTransport` show that swapping form IDs — provided each form keeps its slot count (arity) — also leaves collapse unchanged.
- `IsoCollapse` and `IsoCanon` connect this relabelling action to Python's `iso.py` canonical-key deduplicator, while keeping four honest boundaries in view:
  1. **List order (`Gap 1`):** `relabel` in Lean maps lists in place without sorting them; `serialize` in Python sorts `insts`, `rules`, and `reqs`. `Iso.of_components` (`IsoBridge.lean`) bridges equal-membership lists to `Iso`.
  2. **Duplicate list entries (`Gap 2`):** `Minimality.Iso` checks list membership (`∈`), so `[(0, [0])]` and `[(0, [0]), (0, [0])]` are `Iso` in Lean (`Textbook.U74.isoSingleDup`), whereas Python's `Regime` stores `frozenset`s that deduplicate on construction.
  3. **Permutation budget (`Gap 3`):** Python's `canonical(r, perm_budget=...)` raises `IsoBudgetError` when color-preserving candidate bijections exceed `perm_budget`; Lean's `Iso` has no budget parameter.
  4. **Ordered requirement pairs (`Gap 4`):** Because `Iso` applies `sortPair` to requirement pairs, a regime containing an unordered requirement `(2, 0)` is not even `Iso` to itself (`sortPair (2, 0) = (0, 2) ≠ (2, 0)`).

---

## Pseudocode

```text
FUNCTION rename_forms(phi, g, regime):
    new_forms = [regime.forms[g(j)] FOR j IN 0 .. length(regime.forms) - 1]
    new_insts = [(phi(form_id), args) FOR (form_id, args) IN regime.insts]
    new_rules = [phi(form_id) FOR form_id IN regime.rules]
    RETURN Regime(regime.data, new_forms, new_insts, new_rules, regime.reqs)

FUNCTION relabel(regime, pi, phi):
    step1 = rename_regime_with_reqs(pi.f, regime)   # maps reqs via sort_pair
    RETURN rename_forms(phi.f, phi.g, step1)

FUNCTION iso_holds(r, s, dmap, fmap):
    CHECK r.data == s.data AND length(r.forms) == length(s.forms)
    CHECK FOR ALL f < length(r.forms): s.forms[fmap(f)] == r.forms[f]
    CHECK set_of(s.insts) == {(fmap(i.form), map(dmap, i.args)) FOR i IN r.insts}
    CHECK set_of(s.rules) == {fmap(ru) FOR ru IN r.rules}
    CHECK set_of(s.reqs)  == {sort_pair(dmap(q.1), dmap(q.2)) FOR q IN r.reqs}
```

---

## Python

Executable check script: `textbook/checks/u74_parked_iso.py`.

```python
r1 = Regime(
    data=("d0", "d1", "d2"),
    forms=(1, 2),
    insts=frozenset({(0, (0,)), (1, (0, 1)), (1, (0, 2))}),
    rules=frozenset(),
    reqs=frozenset({(1, 2)}),
)
pi = (2, 1, 0)
phi = (1, 0)
r2 = rename(r1, pi, phi)

assert profile(r1, 1) == profile(r1, 2)
assert isomorphic(r1, r2)
assert canonical(r1) == canonical(r2) == canonical_bruteforce(r1)
assert profile(r2, pi[1]) == profile(r2, pi[2])
```

---

## Line-by-line Python explanation

- `r1 = Regime(...)`: constructs a 3-datum, 2-form regime where form `0` has arity `1`, form `1` has arity `2`, instances are `(0, (0,))`, `(1, (0, 1))`, and `(1, (0, 2))`, and the imposed requirement is `(1, 2)`.
- `pi = (2, 1, 0)` and `phi = (1, 0)`: specifies a datum permutation swapping `0` and `2` and a form permutation swapping form `0` and form `1`.
- `r2 = rename(r1, pi, phi)`: applies the combined datum-and-form relabelling from `code/derivation/iso.py`.
- `assert profile(r1, 1) == profile(r1, 2)`: checks that data `1` and `2` have identical derivability profiles across all well-formed contexts in `r1`, so they are observationally collapsed.
- `assert isomorphic(r1, r2)` and `assert canonical(r1) == canonical(r2) == canonical_bruteforce(r1)`: verifies that `r1` and `r2` receive the same canonical key under both color-refined and brute-force minimization.
- `assert profile(r2, pi[1]) == profile(r2, pi[2])`: verifies `Iso.collapsed_transport` / `collapsed_renameDataForm` — in the renamed regime `r2`, the moved data `pi[1] = 1` and `pi[2] = 0` remain observationally collapsed.
- In addition, `u74_parked_iso.py` checks all four Lean-vs-Python boundary exhibits (`lr_reordered`, `lr_dup`, `IsoBudgetError` at `perm_budget=0`, and `lr_unordered` with `reqs = ((2, 0),)`), and verifies the 75-module / 1 530-axiom-report partition (`1482` from `Derivation.lean` + `48` from `ParkedAudit.lean`).

---

## Lean 4

From `lean4/Derivation/FormTransport.lean`, `IsoCollapse.lean`, `IsoCanon.lean`, `IsoBridge.lean`, and book-Lean `textbook/checks/u74_lean.py`:

```lean
-- Lean (Genesis), lean4/Derivation/FormTransport.lean lines 189-194
theorem collapsed_renameDataForm {n : Nat} (σ : DRen n) (r : Regime)
    (hn : r.data = n) (τ : DRen r.forms.length) (d d' : Nat) :
    collapsed (renameForms τ.f τ.g (renameRegime σ.f r)) (σ.f d) (σ.f d')
      ↔ collapsed r d d' := by
  rw [collapsed_renameForms (renameRegime σ.f r) τ (σ.f d) (σ.f d')]
  exact collapsed_rename σ r hn d d'

-- Lean (Genesis), lean4/Derivation/IsoCollapse.lean lines 164-174
theorem Iso.collapsed_transport (h : Iso r s) {d d' : Nat}
    (hd : d < r.data) (hd' : d' < r.data) :
    collapsed s (h.dmap d) (h.dmap d') ↔ collapsed r d d' := by
  constructor
  · exact h.collapsed_fwd hd hd'
  · intro Hr
    have key := h.symm.collapsed_fwd (d := h.dmap d) (d' := h.dmap d')
      (h.dmap_lt d (List.mem_range.mpr hd)) (h.dmap_lt d' (List.mem_range.mpr hd'))
    rw [symm_dmap, h.dinv_dmap d (List.mem_range.mpr hd),
        h.dinv_dmap d' (List.mem_range.mpr hd')] at key
    exact key Hr

-- Lean (Genesis), lean4/Derivation/IsoCanon.lean lines 225-230
def iso_of_relabel_eq {r s : Regime}
    (πr : DRen r.data) (φr : DRen r.forms.length)
    (πs : DRen s.data) (φs : DRen s.forms.length)
    (hr : ∀ q ∈ r.reqs, q.1 ≤ q.2) (hs : ∀ q ∈ s.reqs, q.1 ≤ q.2)
    (heq : relabel r πr φr = relabel s πs φs) : Iso r s :=
  (relabel_iso r πr φr hr).trans ((heq ▸ relabel_iso s πs φs hs).symm)
```

---

## Line-by-line Lean explanation

1. **In `collapsed_renameDataForm`:**
   - `{n : Nat} (σ : DRen n) (r : Regime) (hn : r.data = n)`: takes a bounded datum bijection $\sigma$ matching `r.data`.
   - `(τ : DRen r.forms.length)`: takes a bounded form bijection $\tau$ matching `r.forms.length`, noting that `renameRegime σ.f r` leaves `forms.length` unchanged.
   - `rw [collapsed_renameForms (renameRegime σ.f r) τ (σ.f d) (σ.f d')]`: strips the outer `renameForms τ.f τ.g` layer using `collapsed_renameForms`.
   - `exact collapsed_rename σ r hn d d'`: finishes by applying Unit 29's datum-renaming transport.
2. **In `Iso.collapsed_transport`:**
   - `(h : Iso r s)` and `{d d' : Nat} (hd : d < r.data) (hd' : d' < r.data)`: requires $d, d'$ to lie in the admitted datum range so `h.dinv_dmap` applies.
   - `exact h.collapsed_fwd hd hd'`: the left-to-right implication pulls collapse back along `h`.
   - `h.symm.collapsed_fwd ...`: for the right-to-left implication, applies `collapsed_fwd` to the inverse isomorphism `h.symm : Iso s r` at `h.dmap d` and `h.dmap d'`, then rewrites `h.symm.dmap (h.dmap d)` to `d` via `symm_dmap` and `h.dinv_dmap`.
3. **In `iso_of_relabel_eq`:**
   - `relabel_iso r πr φr hr : Iso r (relabel r πr φr)` builds the forward isomorphism for $r$.
   - `heq ▸ relabel_iso s πs φs hs : Iso s (relabel r πr φr)` transports the forward isomorphism for $s$ along the equality `heq : relabel r πr φr = relabel s πs φs`.
   - `.symm` inverts that isomorphism to `Iso (relabel r πr φr) s`, and `.trans` composes the two to produce `Iso r s`.

---

## What has been proved

1. **What it supports:**
   - **Form renaming and transport (`FormRenaming.lean`, `FormTransport.lean`):** `permForms` and `renameForms` preserve form count and arities (`permForms_length`, `renameForms_arity`), invert on fixed-form-length fibres (`renameForms_gf`), and preserve context well-formedness (`wfCtx_renameForms`), derivability (`derivable_renameForms`), and observational collapse (`collapsed_renameForms`, `collapsed_renameDataForm`).
   - **Isomorphism algebra and collapse transport (`IsoCollapse.lean`, `IsoCanon.lean`, `IsoBridge.lean`):** `Minimality.Iso` is symmetric (`Iso.symm`), transitive (`Iso.trans`), and transports observational collapse (`Iso.collapsed_transport`). Under ordered requirements (`∀ q ∈ r.reqs, q.1 ≤ q.2`), `relabel` produces an isomorphic regime (`relabel_iso`), equal relabellings imply `Iso` (`iso_of_relabel_eq`), and equal component memberships imply `Iso` (`Iso.of_components`).
   - **Book-Lean boundary witnesses (`Textbook.U74`) and four-layer audit pipeline (`Derivation.lean`, `ParkedAudit.lean`, `ci/check_parked_audit.py`, `ci/check_declaration_axioms.py`):** `sortPair_unordered` establishes `sortPair (2, 0) = (0, 2) ≠ (2, 0)`; `rSingle_rDup_lengths_ne` and `isoSingleDup` show that two regimes of different `insts` list lengths (`1` vs `2`) are `Minimality.Iso` via `Iso.of_components` and have identical collapse relations (`rSingle_rDup_collapsed_iff`); and all 75 modules in `lean4/Derivation/` (63 in `Derivation`'s import closure + 12 in `ParkedAudit.parkedModules`) and all 1,530 `#print axioms` lines (1,482 root + 48 parked) plus all `Type`-valued `def`s stay within `{propext, Quot.sound}`.
2. **What it does not support:**
   - It does not lift `TransStep` under form renaming (`FormTransport.lean`).
   - It does not formalize `serialize`'s sorting step ("equal sorted lists $\Rightarrow$ equal list membership"), Python's colour-refinement search (`_refine`, `_class_perms`), or the completeness direction ("`Iso r s` $\Rightarrow$ equal canonical key", which fails on un-deduplicated lists) in Lean.
   - It does not make the action `renameRegime` (which leaves `reqs` untouched) an `Iso` when `π` moves a requirement pair (`FormTransport.md` §4 & §11.2).
3. **The narrowest defensible claim:**
   - In Lean, observational collapse `collapsed` is invariant under `renameForms`, `renameRegime`, and `Minimality.Iso`; `relabel_iso`, `iso_of_relabel_eq`, and `Iso.of_components` construct `Minimality.Iso` witnesses when `∀ q ∈ reqs, q.1 ≤ q.2`; and `Derivation.lean`, `ParkedAudit.lean`, `ci/check_parked_audit.py`, and `ci/check_declaration_axioms.py` audit all 75 modules and all 1,530 `#print axioms` reports within `{propext, Quot.sound}`.
4. **The next test needed:**
   - Formalize list sorting and deduplication on `Regime` components in Lean and compose `iso_of_relabel_eq` with `Iso.of_components` along sorted-list membership equivalence.

---

## What has not been proved

1. **No transition-step lift under form renaming (`FormTransport.md` §4):** `FormTransport.lean` transports `wfCtx`, `derivable`, and `collapsed`, and explicitly notes that lifting `validResponse`, `respond`, and `TransStep` to form renamings is not established there.
2. **No Lean formalization of `serialize`'s sorting step or canonical-key completeness (isomorphic $\Rightarrow$ equal canonical key, `IsoCanon.md` §4, `IsoBridge.md` §4):** `IsoCanon.lean` and `IsoBridge.lean` establish `iso_of_relabel_eq` and `Iso.of_components`, and explicitly leave the sorted-list-to-membership combinatorial step and the converse direction outside their scope.
3. **Action (`collapsed_renameDataForm`) vs. `Iso` (`Iso.collapsed_transport`) (`FormTransport.md` §11.2):** `renameRegime` leaves `reqs` untouched, whereas `Iso` maps `reqs` via `sortPair`. The headline of register R6 in `paper/structural_necessity.md` groups `collapsed_renameDataForm` and `Iso.collapsed_transport` together under "full-isomorphism collapse transport," whereas only `Iso.collapsed_transport` (and `IsoCanon.relabel_iso`, which uses `renameRegimeR`) transports `reqs`.
4. **Requirement ordering is a genuine condition (`IsoCanon.md` §4):** Without `∀ q ∈ r.reqs, q.1 ≤ q.2`, neither `isoRefl` nor `relabel_iso` holds because `sortPair` flips unordered requirement pairs.

---

## Outside the system

| Item | Kind | Role and cost |
|---|---|---|
| `DRen n` (`f, g : Nat → Nat`) | Metatheory structure | Bounded index bijections on datum indices ($n = r.\text{data}$) and form indices ($m = r.\text{forms.length}$). |
| `Minimality.Iso r s` | Metatheory `Type` structure | Pairs of bounded maps with membership-equivalence proofs on `insts`, `rules`, `reqs`. |
| `ParkedAudit.lean` metaprogram | Lean 4 `MetaM` command | Elaborates the 12 parked modules and prints `#print axioms` for their 48 `theorem` declarations during `lake build`. |
| `perm_budget` in `iso.py` | External Python execution bound | Bounds the number of candidate permutation pairs searched by `canonical` before raising `IsoBudgetError`. |

---

## Student exercise

Consider the regime `r_unord` with `data = 3`, `forms = [1]`, `insts = [(0, [0])]`, `rules = []`, and `reqs = [(2, 0)]`.
1. What does `relabel` do to `r_unord.reqs` under the identity datum bijection $\pi = \text{id}$ and identity form bijection $\varphi = \text{id}$?
2. Why does the backward requirement condition `reqs_bwd` of `Iso r_unord (relabel r_unord id id)` fail?

---

<details>
<summary>Student exercise answer</summary>

1. Under $\pi = \text{id}$, `relabel` maps each requirement $q \in r\_\text{unord}.\text{reqs}$ by `mapReq id q`, which by `mapReq_eq_sortPair` equals `sortPair (q.1, q.2)`. For $q = (2, 0)$, $\min(2, 0) = 0$ and $\max(2, 0) = 2$, so `(relabel r_unord id id).reqs = [(0, 2)]`.
2. In `Iso r_unord (relabel r_unord id id)`, the field `reqs_bwd` requires that for every $q \in (relabel\ r\_\text{unord}\ \text{id}\ \text{id}).\text{reqs} = [(0, 2)]$, the sorted inverse image `sortPair (id q.1, id q.2) = sortPair (0, 2) = (0, 2)` belong to $r\_\text{unord}.\text{reqs} = [(2, 0)]$. Because $(0, 2) \neq (2, 0)$, `(0, 2) ∉ [(2, 0)]`, so `reqs_bwd` fails. This is why `relabel_iso`, `iso_of_relabel_eq`, and `Iso.of_components` require ordered requirement pairs `∀ q ∈ r.reqs, q.1 ≤ q.2` (as `Regime.wf` provides).

---

</details>

## Verification

| Check | Source / Command | Result |
|---|---|---|
| Frozen Lean modules | `lean4/Derivation/{FormRenaming,FormTransport,IsoCollapse,IsoCanon,IsoBridge}.lean` and `*Compat.lean` | Built by `lake build` (`ParkedAudit` target, exit 0); 38 theorems in `artifacts/lean_axioms.txt` |
| Python check | `python textbook/checks/u74_parked_iso.py` | Exit 0 (`failures: []`; verifies `rename`, `isomorphic`, `canonical`, `collapsed_transport`, Gaps 1–4, and the 75-module / 1 530-axiom census) |
| Book-Lean check | `python textbook/checks/u74_lean.py` | Exit 0 (`47 of 47; failures: []`; checks `Textbook.U74.*`, the 5 `Type`-valued `Iso` defs, and all 38 theorems across `FormRenaming`, `FormTransport`, `IsoCanon`, `IsoCollapse`) |
| Claim status | `FROZEN` / `CONDITIONAL` (ordered requirements for `relabel_iso`, `iso_of_relabel_eq`, `Iso.of_components`) | Matches `textbook/audit/modules/{FormRenaming,FormTransport,IsoCollapse,IsoCanon,IsoBridge}.md` |
