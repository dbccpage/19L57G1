# Claims

AuthorityEffect: None.

| Claim | Status | Statement | Evidence |
| --- | --- | --- | --- |
| U1 | PROVED_THEOREM | `R2L` collapses 0, 1; after the two-item delta `deltaU0` the pair is separated. | `ResearchUncollapse.uncollapse_by_delta` |
| U2 | PROVED_THEOREM | Admitting a rule never turns a collapsed pair separated. | `ResearchUncollapse.collapsed_ruleAll` |
| U3 | PROVED_THEOREM | On a well-formed regime, one item uncollapses only if it is an instance mentioning a target datum. Without well-formedness this is not claimed. | `ResearchUncollapse.uncollapse_only_by_mention` |
| U3d | PROVED_THEOREM | The same along a whole delta: on a well-formed regime, a delta keeps a collapsed pair collapsed unless one of its items is an instance mentioning a target datum. | `ResearchUncollapse.uncollapse_only_by_mention_delta` (uses `Ignition.applyItem_wf`) |
| U3n | PROVED_THEOREM | Mentioning is not sufficient: a new instance mentioning datum 0 leaves a collapsed pair collapsed. | `ResearchUncollapse.mention_not_sufficient` |
| U4 | PROVED_THEOREM | A separated pair can be collapsed again, by a rule and by an instance. | `ResearchUncollapse.recollapse_by_rule`, `ResearchUncollapse.recollapse_by_instance` |
| U4b | PROVED_THEOREM | The rule re-collapse is not a valid response to the target `(0, 1)`, by the target clause alone. A delta that separates its target `(1, 2)` but collapses the imposed requirement `(0, 1)` fails `validResponse` by the requirement clause. | `ResearchUncollapse.recollapse_not_validResponse`, `ResearchUncollapse.recollapse_breaks_requirement` |
| U5 | PROVED_THEOREM | Over a family with shared indices that collapses the pair, adding `r'` uncollapses exactly when `r'` separates the pair (equivalently, does not collapse it). | `ResearchUncollapse.collapsedIn_cons`, `ResearchUncollapse.uncollapse_family`, `ResearchUncollapse.uncollapse_family_iff`, `ResearchUncollapse.separable_of_not_collapsed` (uses `Ignition.ctxList`), `ResearchUncollapse.uncollapse_family_sep_iff` |
| U6 | PROVED_THEOREM | `separable r` is a positive apartness and `collapsed r` is its indistinguishability; collapse is an equivalence (here by transport through that link; directly it needs no cotransitivity). | `ResearchUncollapse.separable_isApart`, `ResearchUncollapse.collapsed_iff_indist`, `ResearchUncollapse.collapsed_equivalence` |
| U7 | PROVED_THEOREM | The family apartness is an apartness whose indistinguishability is collapse in every member. | `ResearchUncollapse.familyApart_isApart`, `ResearchUncollapse.collapsedIn_iff_indist` |
| U9 | PROVED_THEOREM | The raw family `collapsedIn` depends on presentation: a regime and its renaming disagree on the raw pair `(1, 2)` and agree on the transported pair. | `ResearchUncollapse.family_index_dependence` |
| U9r | PROVED_THEOREM | With a correspondence map per member (`collapsedInR`) the same two members collapse `1, 2`, and adding a member's renaming by a bijection, carried with the composed map, never uncollapses. | `ResearchUncollapse.collapsedInR_cons`, `ResearchUncollapse.family_index_repaired`, `ResearchUncollapse.collapsedInR_rename_cons` |
| U10 | PROVED_THEOREM | `separable` ranges over bare naturals: `separable U0 0 99` holds with 99 unadmitted. No theorem here restricts to admitted data. | `ResearchUncollapse.separable_unadmitted` |
| U8 | PROVED_THEOREM | `applyItem` and `applyDelta` preserve `Regime.wf`. Proved in the ignition tree, not re-proved here and outside this tree's axiom-report scope. | `Ignition.applyItem_wf`, `Ignition.applyDelta_wf` (research/ignition); consumed by U3d |
| inputs | VERIFIED_FINITE | The pinned consumed modules are exactly the outside imports of every module of `lean/`, and their files exist. Unchanged contents are not checked: no digests are pinned. | `tests/test_model.py` |

Lean reach: only the declarations named in TREE_CONTRACT.json. This is not a
census of every compiled constant.
