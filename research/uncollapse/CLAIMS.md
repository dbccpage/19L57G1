# Claims

AuthorityEffect: None.

| Claim | Status | Statement | Evidence |
| --- | --- | --- | --- |
| U1 | PROVED_THEOREM | `R2L` collapses 0, 1; after `deltaU0` the pair is separated. | `ResearchUncollapse.uncollapse_by_delta` |
| U2 | PROVED_THEOREM | Admitting a rule never turns a collapsed pair separated. | `ResearchUncollapse.collapsed_ruleAll` |
| U3 | PROVED_THEOREM | On a well-formed regime, one item uncollapses only if it is an instance mentioning a target datum. | `ResearchUncollapse.uncollapse_only_by_mention` |
| U4 | PROVED_THEOREM | A separated pair can be collapsed again, by a rule and by an instance. | `ResearchUncollapse.recollapse_by_rule`, `ResearchUncollapse.recollapse_by_instance` |
| U5 | PROVED_THEOREM | Over a family with shared indices that collapses the pair, adding `r'` uncollapses exactly when `r'` does not collapse the pair; a witnessed separation in `r'` suffices. Getting a witness from non-collapse is not proved (constructively it needs a context enumeration). | `ResearchUncollapse.collapsedIn_cons`, `ResearchUncollapse.uncollapse_family`, `ResearchUncollapse.uncollapse_family_iff` |
| U6 | PROVED_THEOREM | `separable r` is a positive apartness and `collapsed r` is its indistinguishability, hence an equivalence. | `ResearchUncollapse.separable_isApart`, `ResearchUncollapse.collapsed_iff_indist`, `ResearchUncollapse.collapsed_equivalence` |
| U7 | PROVED_THEOREM | The family apartness is an apartness whose indistinguishability is collapse in every member. | `ResearchUncollapse.familyApart_isApart`, `ResearchUncollapse.collapsedIn_iff_indist` |
| U4b | PROVED_THEOREM | The rule re-collapse of U4 is an admissible operation but not a valid response: it erases the imposed requirement `(0, 1)`. | `ResearchUncollapse.recollapse_not_validResponse` |
| U9 | PROVED_THEOREM | `collapsedIn` depends on presentation: a regime and its renaming disagree on the raw pair `(1, 2)` and agree on the transported pair. | `ResearchUncollapse.family_index_dependence` |
| U10 | PROVED_THEOREM | `separable` ranges over bare naturals: `separable U0 0 99` holds with 99 unadmitted. No theorem here restricts to admitted data. | `ResearchUncollapse.separable_unadmitted` |
| U8 | OPEN | `applyItem` preserves `Regime.wf`, so U3 chains along a delta. | none |
| inputs | VERIFIED_FINITE | The pinned consumed modules are exactly the Lean imports and exist in the sealed package. | `tests/test_model.py` |

Lean reach: only the declarations named in TREE_CONTRACT.json. This is not a
census of every compiled constant.
