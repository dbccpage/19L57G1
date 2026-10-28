# Claims

AuthorityEffect: None.

| Claim | Status | Statement | Evidence |
| --- | --- | --- | --- |
| V1 | PROVED_THEOREM | At `genesis` under `require 0 0`, the quiescence verdict of the world the interpreter produces under code `c` is `c.guardRequire`; the obstruction certificate for `(0, 0)` is its negation. | `ResearchInterpreterVerdict.quiescent_reads_guard`, `ResearchInterpreterVerdict.obstructed_reads_guard` |
| V2 | PROVED_THEOREM | For every step function `s`, some code `c` makes `interpStep c` and `s` disagree on quiescence at that witness. The interpreter is not a step function. | `ResearchInterpreterVerdict.interp_not_step` |
| V2c | PROVED_THEOREM | Every coded member `d` disagrees with the code `flipGuard d` on quiescence and on the obstruction certificate there. | `ResearchInterpreterVerdict.coded_member_separated`, `ResearchInterpreterVerdict.coded_member_separated_obstructed` |
| V2s | PROVED_THEOREM | A quiescence difference is a support difference; so V2 yields a support-level separation. | `ResearchInterpreterVerdict.supp_ne_of_quiescent_ne`, `ResearchInterpreterVerdict.verdict_entails_supp` (uses `NoOutside.support_quiescent`) |
| V3 | PROVED_THEOREM | Interpretation and quotation determine one reflective step, `rstep`; it satisfies both; the kernel's code still runs to the sealed step under it. | `ResearchInterpreterVerdict.lawful_unique`, `ResearchInterpreterVerdict.rstep_interprets`, `ResearchInterpreterVerdict.rstep_quotes`, `ResearchInterpreterVerdict.rstep_self_description` |
| V3l | PROVED_THEOREM | The lift of a step function quotes and never interprets; `rstep` is the lift of no step function, and the difference is a quiescence verdict at `genesis`. | `ResearchInterpreterVerdict.liftStep_quotes`, `ResearchInterpreterVerdict.liftStep_not_interprets`, `ResearchInterpreterVerdict.rstep_ne_lift`, `ResearchInterpreterVerdict.rstep_not_lift` |
| V4 | PROVED_THEOREM | `VSep` is irreflexive, symmetric and cotransitive; the uncoded role is verdict-separated from every coded member. | `ResearchInterpreterVerdict.vsep_irrefl`, `ResearchInterpreterVerdict.vsep_symm`, `ResearchInterpreterVerdict.vsep_cotrans`, `ResearchInterpreterVerdict.vsep_uncoded`, `ResearchInterpreterVerdict.vsep_kernel` |
| V4s | PROVED_THEOREM | `verdictBoundary` satisfies candidates A, Bs, Bc and D of `PrimitiveCore` by proof; the sealed declared relation is contained in `VSep`. | `ResearchInterpreterVerdict.boundary_A`, `ResearchInterpreterVerdict.boundary_Bs`, `ResearchInterpreterVerdict.boundary_Bc`, `ResearchInterpreterVerdict.boundary_D`, `ResearchInterpreterVerdict.declared_le_derived` |
| V4f | DECLARED | Candidate F holds with the retention and protection stores declared to be `VSep`. Same status as the sealed `i5_boundary_is_F`. | `ResearchInterpreterVerdict.boundary_F` |
| V5 | PROVED_THEOREM | Identifying `none` with any coded member is obstructed relative to `Irrefl`. | `ResearchInterpreterVerdict.collapse_obstructed` |
| V5v | PROVED_THEOREM | Any reading that keeps the coded meanings and identifies `none` with a coded member, or with the lift of any step function, reports a quiescence verdict different from the lawful meaning's at an accessible reflective world. | `ResearchInterpreterVerdict.identification_changes_quiescence`, `ResearchInterpreterVerdict.identification_with_step_changes_quiescence` |
| V6 | PROVED_THEOREM | A code and its `dedupAdmit` flip are never separated by one quiescence verdict: `VSep` is strictly coarser than `≠` among codes. | `ResearchInterpreterVerdict.quiescent_admitTok`, `ResearchInterpreterVerdict.coded_pair_not_vsep` |
| V7 | PROVED_THEOREM | At the `genesis` witness `nextFamily` under `close` is empty for every code; at the two-token world reached by two admissions it reads the guard, and the interpreter is separated from every step function at that verdict too. | `ResearchInterpreterVerdict.nextFamily_blind_at_genesis`, `ResearchInterpreterVerdict.twoWorld_reached`, `ResearchInterpreterVerdict.family_reads_guard`, `ResearchInterpreterVerdict.interp_not_step_family` |
| Bl | OPEN | Locatedness of `VSep` on the carrier. Not `≠` (V6); no boolean realization is given or refuted. | none |
| inputs | VERIFIED_FINITE | The pinned consumed modules are exactly the outside imports of every module of `lean/`, and their files exist. Unchanged contents are not checked: no digests are pinned. | `tests/test_model.py` |

Lean reach: only the declarations named in TREE_CONTRACT.json. This is not a
census of every compiled constant.
