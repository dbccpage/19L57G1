# E2′ restatement diagnostic

`AuthorityEffect: None.` Scoping diagnostic, not a research result.
Census: `research/endogenous_demand` at `b947873`. Sealed `code/` of
this repository. Script: `reclassify.py`. Lives at repo-root
`ob1_e2_restatement/`: outside the seal and outside `research/`.

E2 = demand is a `reqs` member (the tree's operationalization).
E2′ = demand is an owed separation: designated pair `(i,j)` with
`separable(regime,i,j) == False`, no `Impose` at that step, produced
by a rule firing or grammar closure, not a host pick. The pair need
not be in `reqs`. E1 and E3 are unchanged.

## Table

Produced by `python reclassify.py`. Every row with `witness=yes` names
a concrete reachable state; `already sep` is `derivation.observe.separable`
on that state; `in reqs` is membership in `regime.reqs`.

| id  | E2 fails | E2 status     | E2' fails | flipped     | pair   | in reqs | already sep | last event   |
| --- | -------- | ------------- | --------- | ----------- | ------ | ------- | ----------- | ------------ |
| C1  | E1       | defeated      | E1        | no          | [0, 1] | False   | False       | AdmitDatum   |
| C2  | E1,E2    | defeated      | E1        | no          | [0, 1] | True    | False       | Impose       |
| C3  | E3       | defeated      | E3        | no          | [0, 1] | True    | True        | AdmitInst    |
| C4  | E2       | defeated      | E2'       | restated    | None   | False   | None        | AdmitRuleAll |
| C5  | E1,E2    | defeated      | E1        | no          | [0, 1] | False   | False       | AdmitDatum   |
| C6  | E2       | defeated      | E2'       | restated    | [0, 2] | True    | False       | Impose       |
| C7  | E1       | defeated      | E1        | not claimed | —      | —       | —           | —            |
| C8  | E1       | defeated      | E1        | not claimed | —      | —       | —           | —            |
| C9  | E3       | defeated      | E3        | no          | [0, 1] | False   | True        | AdmitInst    |
| C10 | —        | outside_class | outside   | no          | —      | —       | —           | —            |
| I1  | E2       | OPEN          | E3        | yes         | [0, 1] | False   | True        | AdmitInst    |

Witness notes:

- **C1.** `host_next_demand` returns collapsed `(0,1)`. The pair *is*
  owed (`separable` false, `reqs` empty). Still E1: the host chose.
- **C2.** Closure policy then `Impose`. Pair is in `reqs` and still
  collapsed (Impose writes `reqs`, not profiles). Still E1.
- **C3.** Laundered Impose, then `AdmitInst(0,[0,1])`. Pair in `reqs`
  and now separable. Still E3 (import). The instance also separates,
  which is not a new pass.
- **C4.** `AdmitRuleAll` on an empty instance store. Reader returns
  `()`. No pair designated. Uniform rule does not write `reqs` and
  does not emit insts. E2 restated as E2′: still no derived demand.
- **C5.** `host_holds` after `AdmitDatum`. Pairs are owed. Still E1.
- **C6.** Growth then `Impose(0,2)`. Last event is Impose. E2 restated
  as E2′ supplied.
- **C7, C8.** Cited E1 in the tree; no `separable` witness. Flip not
  claimed.
- **C9.** Unary mark on datum 0. `separable(0,1)` true. Still E3.
- **C10.** Outside the sealed Event type.
- **I1.** Never-selects read of `AdmitInst(0,[0,1])` yields `(0,1)`.
  `reqs` empty, so E2-as-written still fails. Under E2′ the pair is
  **already separable** (`separable((0,1))` true: context
  `(0,(None,1))` is derivable for 0 and not for 1). That is E3,
  vacuous. Independently the instance was **admitted**, not produced
  by a rule, so E2′ derived-not-supplied also fails. I1 does not
  pass. The OPEN remainder dies under E2′.

## Surviving-shape probe

The candidate shape was: a rule that fires on admitted instances to
emit a new instance encoding an owed-separation pair, read by the
fixed interpreter.

The only sealed rule is uniform all-tuples. On two collapsed data plus
`AdmitForm(2)` plus `AdmitRuleAll(0)`:

- `insts = 0`
- `read_pairs = []`
- `collapsed = [[0,1]]`
- `separable(0,1) = False`

The rule does not emit an instance. Previously collapsed pairs stay
collapsed (`derivable` is `form in rules or inst in insts`; a uniform
rule makes every tuple of that form derivable for every datum, so
profiles stay equal). A host that then read `collapsed_pairs` would
be C1 (E1). The never-selects reader sees nothing. Instances enter
`insts` only via `AdmitInst` (supply) or a new Event constructor
(C10, sealed-path amendment).

## The fork

Under E2′ the one live shape the brief asked us to confirm — a rule
firing that *emits* an instance encoding an owed pair, read by the
fixed interpreter — is not a construct in the sealed Event grammar,
and I1 (the OPEN instance-channel remainder) fails E3 on its own
witness because that instance already separates the pair it encodes,
and fails E2′ because the instance was admitted rather than derived.
**The next OB-1 effort should be Outcome B on the wider class (owed
separation), not Outcome A (instance-channel generator hunt),**
because every exhibited census row still dies under E1, E2′ as
supplied, or E3, and the proposed generator shape is not realizable
without a host `AdmitInst` or a seventh Event constructor.

What this did **not** do: it did not prove Outcome B; it did not
search a larger candidate space than C1–C9 and I1; it did not
formalize E2′ in Lean; it did not close OB-1. It decided which of
those two multi-session efforts is worth starting.
