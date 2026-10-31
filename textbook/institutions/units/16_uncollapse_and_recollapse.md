# Unit 16. Uncollapse, recollapse, and families of regimes

**Claim.** Admissions in one regime can alter an existing view and restore
collapse. Adding another regime to a family follows a different rule.
Comparisons between regimes require explicit input correspondences.

<details>
<summary>Detailed statement, sources, and classification (optional)</summary>

**Detailed statement.** Under extension of a single regime by admissions (`applyDelta`), a
collapsed pair can become separated (`uncollapse_by_delta`); on a well-formed
regime, a delta keeps a collapsed pair `d, d'` collapsed unless one of its items
is a `.newInst f args` mentioning `d` or `d'` (`uncollapse_only_by_mention`,
`uncollapse_only_by_mention_delta`), while mentioning is not sufficient when a
rule already derives every plug (`mention_not_sufficient`). Conversely, a
separated pair can be collapsed again by admitting a rule (`recollapse_by_rule`)
or an instance (`recollapse_by_instance`), which alters an existing view rather
than only adding views (`recollapse_changes_views`) and fails `validResponse`
when it collapses the target (`recollapse_not_validResponse`) or a protected
requirement (`recollapse_breaks_requirement`). Under a family of regimes
(`collapsedIn`), adding `r'` uncollapses a pair iff `r'` separates it
(`uncollapse_family_sep_iff`), raw indices depend on presentation
(`family_index_dependence`), carrying correspondence maps repairs the dependence
and prevents a renamed copy from uncollapsing (`family_index_repaired`,
`collapsedInR_rename_cons`), and `separable r` is a constructive apartness whose
indistinguishability relation is `collapsed r` (`separable_isApart`,
`collapsed_iff_indist`).

**Status:** derived. **Lean:** `ResearchUncollapse.uncollapse_by_delta`,
`ResearchUncollapse.collapsed_ruleAll`,
`ResearchUncollapse.uncollapse_only_by_mention`,
`ResearchUncollapse.uncollapse_only_by_mention_delta`,
`ResearchUncollapse.mention_not_sufficient`,
`ResearchUncollapse.recollapse_by_rule`,
`ResearchUncollapse.recollapse_by_instance`,
`ResearchUncollapse.recollapse_not_validResponse`,
`ResearchUncollapse.recollapse_breaks_requirement`,
`ResearchUncollapse.separable_unadmitted`, `ResearchUncollapse.collapsedIn`,
`ResearchUncollapse.uncollapse_family_sep_iff`,
`ResearchUncollapse.family_index_dependence`, `ResearchUncollapse.collapsedInR`,
`ResearchUncollapse.family_index_repaired`,
`ResearchUncollapse.collapsedInR_rename_cons`,
`ResearchUncollapse.separable_isApart`,
`ResearchUncollapse.collapsed_iff_indist` (`uncollapse`);
`RegimeBridge.verdict_mono`, `RegimeBridge.recollapse_changes_views`
(`two_theorems`). **Sources:**
`research/uncollapse/lean/ResearchUncollapse.lean` lines 44–386;
`research/two_theorems/lean/ResearchTwoTheorems/RegimeBridge.lean` lines
200–229.

Units 00 through 15 worked at the level of presentations `Nat → Nat` and static
observer views `List (List Nat)`. In the sealed Genesis spine
(`lean4/Derivation/Basic.lean`), distinctions arise from a `Regime`—a tuple of
admitted data count, form arities, admitted instances, uniform rules, and
imposed requirements—where two data `d, d'` are `separable r d d'` when some
well-formed context `c` derives `plug c d` and not `plug c d'` (or vice versa),
and `collapsed r d d'` when every well-formed context gives the same
derivability to both. This unit connects the institutions spine to `Regime` by
answering when "adding a regime" can uncollapse a collapsed pair under its two
possible readings—extending a single regime by admissions (`applyDelta`) or
joining a regime to a family of regimes (`collapsedIn` / `collapsedInR`)—and
why admitting a rule or instance into a regime can *recollapse* a separated
pair whereas appending a presentation to an `Institution` or a view to an
`Evaluator` never can.

</details>

## First pass

Keep inputs 0 and 1. A unary test currently answers Yes on 0 and
No on 1, so it separates them. Admit an instance making the same test
answer Yes on 1 as well. Its answers become Yes/Yes, and this distinction
is lost. A rule deriving every plug can have the same effect.

This changes an existing view. It differs from adding a new view while
retaining all old views, which keeps an old separation available.
It also differs from adding another regime to a family: a new member
that separates the pair suffices for that family's separation.

**Predict:** can we compare the same index numbers across independently
renamed regimes without specifying what they refer to?

<details><summary>Check your prediction</summary>

No. Shared index spellings need not designate corresponding inputs.
The repaired family comparison carries correspondence maps. No bridge
between these distinct update rules is supplied merely by calling each
operation an admission.

</details>

## What you need first

Unit 05 (`correspondence_matters`, `knows_rename`) and Unit 11 (`apart_persists`).
From the sealed Genesis spine (`lean4/Derivation/Basic.lean`, `Mention.lean`,
`Inertia.lean`, `Apartness.lean`, `Ignition.lean`):
- `Regime` has fields `data : Nat`, `forms : List Nat`,
  `insts : List (Nat × List Nat)`, `rules : List Nat`, and
  `reqs : List (Nat × Nat)`.
- `Item` has constructors `.newDatum`, `.newForm a`, `.newInst f args`, and
  `.newRuleAll f`; `applyItem` and `applyDelta` apply one item or a list of
  items to a regime.
- `separable r d d'` is `∃ c, wfCtx r c ∧ ¬ (derivable r (plug c d) ↔
  derivable r (plug c d'))`; `collapsed r d d'` is `∀ c, wfCtx r c →
  (derivable r (plug c d) ↔ derivable r (plug c d'))`.

### 1. Regime views and why recollapse alters a view (`two_theorems`)

```lean
-- Lean (research), research/two_theorems/lean/ResearchTwoTheorems/RegimeBridge.lean lines 200–229
theorem verdict_mono {E E' : Evaluator} (h : ∀ c, c ∈ E → c ∈ E') {a b : Nat}
    (hv : verdictB E a b = true) : verdictB E' a b = true := by ...

theorem recollapse_changes_views (r r' : Regime) (cs cs' : List Ctx)
    (hcs : ∀ c, c ∈ cs ↔ wfCtx r c) (hcs' : ∀ c, c ∈ cs' ↔ wfCtx r' c)
    {a b : Nat} (ha : a < r.data) (hb : b < r.data) (ha' : a < r'.data) (hb' : b < r'.data)
    (hsep : separable r a b) (hcol : collapsed r' a b) :
    ∃ v, v ∈ regimeViews r cs ∧ v ∉ regimeViews r' cs' := by ...
```

Each well-formed context `c` of a regime `r` defines a view `ctxView r c` of the
admitted data `d < r.data` for which `plug c d` is derivable, and `regimeViews r cs`
collects those views across `cs`. Adding views to an `Evaluator` is monotone
(`verdict_mono`). Therefore, whenever a regime admission turns a separated pair
`a, b` into a collapsed pair, at least one view of `regimeViews r cs` is no
longer present in `regimeViews r' cs'` (`recollapse_changes_views`): admitting a
rule or instance mutates the extension of existing contexts rather than only
appending a new view.

## The theorems

First, Reading (E)—extension of a single regime by admissions, uncollapse only
by a mentioning instance, and recollapse:

```lean
-- Lean (research), research/uncollapse/lean/ResearchUncollapse.lean lines 45–128, 163–227
theorem uncollapse_by_delta :
    collapsed R2L 0 1 ∧ applyDelta R2L deltaU0 = some U0 ∧
      ¬ collapsed U0 0 1 :=
  ⟨R2L_collapsed, by decide, separable_not_collapsed U0_separable⟩

theorem collapsed_ruleAll (r : Regime) (f : Nat) {d d' : Nat}
    (h : collapsed r d d') :
    collapsed { r with rules := insertNew r.rules f } d d' := by ...

theorem uncollapse_only_by_mention (r : Regime) (hwf : r.wf) (it : Item)
    (s : Regime) (hs : applyItem r it = some s) {d d' : Nat}
    (h : collapsed r d d')
    (hno : ¬ ∃ f args, it = .newInst f args ∧ (d ∈ args ∨ d' ∈ args)) :
    collapsed s d d' := by ...

theorem uncollapse_only_by_mention_delta {d d' : Nat} :
    ∀ (δ : List Item) (r s : Regime), r.wf → applyDelta r δ = some s →
      collapsed r d d' →
      (∀ it ∈ δ, ¬ ∃ f args, it = .newInst f args ∧ (d ∈ args ∨ d' ∈ args)) →
      collapsed s d d' := by ...

theorem mention_not_sufficient :
    collapsed Rall 0 1 ∧ applyItem Rall (.newInst 0 [0]) = some Rall0 ∧
      (0, [0]) ∉ Rall.insts ∧ collapsed Rall0 0 1 := by ...

theorem recollapse_by_rule :
    separable U0 0 1 ∧ applyItem U0 (.newRuleAll 0) = some U0rule ∧
      collapsed U0rule 0 1 := by ...

theorem recollapse_by_instance :
    separable U0 0 1 ∧ applyItem U0 (.newInst 0 [1]) = some U0both ∧
      collapsed U0both 0 1 := by ...

theorem recollapse_not_validResponse :
    applyDelta U0 [.newRuleAll 0] = some U0rule ∧
      ¬ validResponse U0 0 1 [.newRuleAll 0] := by ...

theorem recollapse_breaks_requirement :
    applyDelta U0 [.newDatum, .newInst 0 [1]] = some U0new ∧ (0, 1) ∈ U0.reqs ∧
      separable U0new 1 2 ∧ collapsed U0new 0 1 ∧
      ¬ validResponse U0 1 2 [.newDatum, .newInst 0 [1]] := by ...

theorem separable_unadmitted : ¬ 99 < U0.data ∧ separable U0 0 99 :=
  ⟨by decide, ⟨⟨0, [none]⟩, by decide, by decide⟩⟩
```

Second, Reading (F)—families of regimes, index dependence, correspondence maps,
and the apartness link:

```lean
-- Lean (research), the same file, lines 239–386
def collapsedIn (S : List Regime) (d d' : Nat) : Prop :=
  ∀ r ∈ S, collapsed r d d'

theorem uncollapse_family_sep_iff (r' : Regime) (S : List Regime) {d d' : Nat}
    (hS : collapsedIn S d d') :
    ¬ collapsedIn (r' :: S) d d' ↔ separable r' d d' :=
  ⟨fun h => separable_of_not_collapsed r' ((uncollapse_family_iff r' S hS).mp h),
   uncollapse_family r' S⟩

theorem family_index_dependence :
    renameRegime swap01 A3 = B3 ∧ collapsed A3 1 2 ∧ separable B3 1 2 ∧
      collapsed B3 (swap01 1) (swap01 2) ∧ ¬ collapsedIn [A3, B3] 1 2 := by ...

def collapsedInR (S : List (Regime × (Nat → Nat))) (d d' : Nat) : Prop :=
  ∀ p ∈ S, collapsed p.1 (p.2 d) (p.2 d')

theorem family_index_repaired : collapsedInR [(A3, id), (B3, swap01)] 1 2 := by ...

theorem collapsedInR_rename_cons {S : List (Regime × (Nat → Nat))} {d d' : Nat}
    (hS : collapsedInR S d d') {r : Regime} {ρ : Nat → Nat} (hm : (r, ρ) ∈ S)
    {n : Nat} (σ : DRen n) (hn : r.data = n) :
    collapsedInR ((renameRegime σ.f r, σ.f ∘ ρ) :: S) d d' := ...

theorem separable_isApart (r : Regime) : Apartness.IsApart (separable r) where ...

theorem collapsed_iff_indist (r : Regime) (d d' : Nat) :
    collapsed r d d' ↔ Apartness.Indist (separable r) d d' := by ...
```

## The proof, step by step

**Step 1. Reading (E): `uncollapse_only_by_mention` and `uncollapse_only_by_mention_delta`.**
Case-split on the admitted item `it : Item`:
- `.newDatum`: by `collapsed_fresh_datum` (using `hwf` to ensure existing
  instances only mention `< r.data`), `collapsed` is preserved.
- `.newForm a`: by `collapsed_fresh_form` (using `hwf` to ensure existing
  instances and rules only reference `< r.forms.length`), `collapsed` is
  preserved.
- `.newRuleAll f`: `collapsed_ruleAll` shows that adding `f` to `r.rules`
  replaces `derivable r (plug c e)` by `derivable r (plug c e) ∨ c.form = f`,
  preserving the equivalence between `d` and `d'` without needing `hwf`.
- `.newInst f args`: if `d ∉ args` and `d' ∉ args`, `collapsed_append_unmentioning`
  preserves `collapsed`.
Induction over `δ : List Item` using `Ignition.applyItem_wf` lifts this to any
well-formed delta (`uncollapse_only_by_mention_delta`).

**Step 2. Recollapse and `validResponse`.**
In `U0` (two data `0, 1`, one unary form `0`, instance `0 [0]`, requirement
`(0, 1)`), the sole well-formed context `⟨0, [none]⟩` (`ctx_unary`) derives `0`
and not `1`, so `separable U0 0 1`. Admitting `.newRuleAll 0` (`U0rule`) or
`.newInst 0 [1]` (`U0both`) makes `⟨0, [none]⟩` derive both `0` and `1`, so
`collapsed U0rule 0 1` and `collapsed U0both 0 1` (`recollapse_by_rule`,
`recollapse_by_instance`). Because `validResponse r a b δ` requires the
resulting regime `s` both to separate the target `(a, b)` and to keep every
requirement `(x, y) ∈ r.reqs` separable, `[.newRuleAll 0]` is not a valid
response to `(0, 1)` (`recollapse_not_validResponse`), and
`[.newDatum, .newInst 0 [1]]`—which separates `(1, 2)` while collapsing the
required pair `(0, 1)`—is not a valid response to `(1, 2)`
(`recollapse_breaks_requirement`).

**Step 3. Reading (F): `uncollapse_family_sep_iff`, `family_index_dependence`, and `collapsedInR`.**
For a family `S : List Regime` with `collapsedIn S d d'`, joining `r'` gives
`¬ collapsedIn (r' :: S) d d' ↔ ¬ collapsed r' d d'`. Because all well-formed
contexts of `r'` are enumerated by `Ignition.ctxList r'`, `¬ collapsed r' d d'`
constructively yields a separating context (`separable_of_not_collapsed`), so
`¬ collapsedIn (r' :: S) d d' ↔ separable r' d d'` (`uncollapse_family_sep_iff`).
However, `B3 = renameRegime swap01 A3` collapses `(swap01 1, swap01 2) = (0, 2)`
while separating the raw pair `(1, 2)`, so `¬ collapsedIn [A3, B3] 1 2`
(`family_index_dependence`, the regime-level counterpart of Unit 05's
`correspondence_matters`). Pairing each member with its correspondence map in
`collapsedInR` restores `collapsedInR [(A3, id), (B3, swap01)] 1 2`
(`family_index_repaired`), and `collapsed_rename` shows that adjoining any
bijectively renamed member `(renameRegime σ.f r, σ.f ∘ ρ)` preserves
`collapsedInR` (`collapsedInR_rename_cons`).

**Step 4. Constructive apartness (`separable_isApart`, `collapsed_iff_indist`).**
For any regime `r`, `separable r` is irreflexive, symmetric, and cotransitive
(by `by_cases` on the decidable equivalence `derivable r (plug c x) ↔
derivable r (plug c z)`), so `Apartness.IsApart (separable r)` holds, and its
negation `Apartness.Indist (separable r)` is equivalent to `collapsed r`.

## The same fact in Python

The check verifies:

1. Pin and import hygiene of `research/uncollapse/model.py` (`consumed_modules`
   matches `lean_imports`).
2. `bridge_checks` and `recollapse_witness` from `two_theorems/model.py`: on
   admitted data `d < r.data`, `verdict(regime_views(r), a, b)` matches
   `separable(r, a, b)` (`0` mismatches); in `R0 -> R0_RULE`, admitting rule `0`
   mutates the view `[0]` into `[0, 1]` (`lost_views == [[0]]`), recollapsing
   `(0, 1)`; and unadmitted datum `99` lies in no view of `R0` while
   `separable(R0, 0, 99)` holds (`separable_unadmitted`).
3. Direct finite checks of `uncollapse_by_delta` (`R2L -> U0`),
   `mention_not_sufficient` (`Rall -> Rall0`), `recollapse_by_instance`
   (`U0 -> U0both`), `recollapse_breaks_requirement` (`U0 -> U0new`),
   `family_index_dependence` (`[A3, B3]`), and `family_index_repaired`
   (`[(A3, id), (B3, swap01)]`).

```
python textbook/institutions/checks/i16_uncollapse.py
```

## Outside the system

**Metatheory used by this unit.**

| Lean | Used for | Status |
|---|---|---|
| `decide`, `by_cases` on `derivable` / `wfCtx` | `uncollapse_by_delta`, `separable_of_not_collapsed`, `separable_isApart`, `collapsed_iff_indist` | decidable instances on finite regime records and `Ignition.ctxList` |
| Induction on `δ : List Item` | `uncollapse_only_by_mention_delta` | structural induction over the delta list |

**What the system holds.** Finite `Regime` records (`data`, `forms`, `insts`,
`rules`, `reqs`), finite `Item` deltas, and finite lists of regimes `List Regime`.

**Admissions relied on, and their price.** Under Reading (E), well-formedness
`r.wf` is required for `uncollapse_only_by_mention`: if a regime has latent
out-of-range instances (`d ≥ r.data` or `f ≥ r.forms.length`), admitting
`.newDatum` or `.newForm` can activate them without mentioning `d` (`U2`).
Also, `separable r d d'` in `Basic.lean` ranges over all `d, d' : Nat`, not only
`d, d' < r.data` (`separable_unadmitted`, `U7`). Under Reading (F), comparing
the same raw index `d` across members of `List Regime` is an unpriced
correspondence admission (`family_index_dependence`, `U9`), priced explicitly by
the map `ρ : Nat → Nat` in `collapsedInR` (`U10`).

**Phrases to read with care.**

- "Adding a regime." In `Basic.lean` there is no multi-regime state, so "adding
  a regime" must be disambiguated into Reading (E) (`applyDelta` on one regime)
  or Reading (F) (`r' :: S` in `collapsedIn` / `collapsedInR`).
- "Recollapse." Appending a member to an `Institution` (`Knows`, `apart_persists`
  in Unit 11) or a view to an `Evaluator` (`verdict_mono`) never collapses a
  separated pair. Admitting a rule or instance to a `Regime` can collapse a
  separated pair because it enlarges `derivable` inside existing contexts, which
  alters existing views (`recollapse_changes_views`).

## What it shows, and what it does not

It shows that under single-regime extension (`applyDelta`), a well-formed regime
uncollapses `d, d'` only when an admitted `.newInst f args` mentions `d` or
`d'`, that mentioning is not sufficient when a rule already derives all plugs,
and that admitting a rule or instance can recollapse a separated pair by
altering the regime's views—which `validResponse` refuses whenever it collapses
the target or a protected requirement.

It shows that under a family of regimes, `collapsedIn` uncollapses iff the new
member separates the pair, that raw index sharing is presentation-dependent, and
that `collapsedInR` repairs this dependence so a renamed copy never uncollapses.

It does not claim that `separable r d d'` implies `d, d' < r.data` without an
explicit admissibility hypothesis (`separable_unadmitted`).

## Sources

| Item | Where |
|---|---|
| `uncollapse_by_delta`, `collapsed_ruleAll`, `uncollapse_only_by_mention`, `uncollapse_only_by_mention_delta` | `research/uncollapse/lean/ResearchUncollapse.lean` lines 45–128 |
| `U0rule`, `U0both`, `ctx_unary`, `Rall`, `Rall0`, `mention_not_sufficient`, `recollapse_by_rule`, `recollapse_by_instance`, `recollapse_not_validResponse`, `U0new`, `recollapse_breaks_requirement`, `separable_unadmitted` | the same file, lines 135–227 |
| `collapsedIn`, `uncollapse_family_sep_iff`, `A3`, `B3`, `swap01`, `family_index_dependence`, `collapsedInR`, `family_index_repaired`, `collapsedInR_rename_cons` | the same file, lines 239–330 |
| `separable_isApart`, `collapsed_iff_indist`, `collapsed_equivalence`, `familyApart`, `familyApart_isApart`, `collapsedIn_iff_indist` | the same file, lines 339–386 |
| `verdict_mono`, `recollapse_changes_views` | `research/two_theorems/lean/ResearchTwoTheorems/RegimeBridge.lean` lines 200–229 |
| Python mirrors | `research/uncollapse/model.py` lines 15–45; `research/two_theorems/model.py` lines 588–686 (`Regime`, `separable`, `bridge_checks`, `recollapse_witness`) |
| Check | `textbook/institutions/checks/i16_uncollapse.py` |
| Ledger | `research/uncollapse/CLAIMS.md` U1–U10; `research/two_theorems/CLAIMS.md` TT-22, TT-23, TT-24, TT-24c |
