# Native terms

Every term this packet uses, in dependency order, with the source
classification vocabulary of `CLAUDE.md` ("Assumption discipline"):

    metatheory apparatus | supplied object-language datum |
    externally imposed challenge | admitted primitive |
    derived definition | proved theorem | deterministic computation |
    countermodel | optional realization | conjecture |
    open obstruction | refuted claim

No term below is introduced by this packet. Each already occurs in the
repository at the location named. Where a term is *declared* rather than
derived, that is stated, because it is the whole content of this packet's
conclusion.

## On the forbidden-synonym column

The work order for this packet asks each term to record its forbidden
imported synonym, if any. **That column is deliberately empty.**

Writing the barred word in order to bar it would itself put external
terminology into the repository, which `CLAUDE.md` prohibits without
qualification. The list of barred words lives in the work order, which is
not a repository file, and it stays there. A reader who needs it should
read it there.

This is a boundary decision, not an oversight, and it is the same
decision `paper/paper.md` §13 makes about the comparison section.

## Dependency order

### Layer 0 — what is presented

| term | source | depends on | where |
|---|---|---|---|
| inscription | supplied object-language datum | — | `prompt/seed_prompt.md`; `engine.GENESIS_L/F` |
| presentation token | metatheory apparatus | inscription | `model.Regime.data` docstring |
| supply | metatheory apparatus | presentation token | `model.Supply` |

`supply` is the load-bearing separation of Layer 0: `model.step` returns
the regime unchanged on `Supply`. Presentation is not admission.

### Layer 1 — what is admitted

| term | source | depends on | where |
|---|---|---|---|
| admission | metatheory apparatus | supply | `model.AdmitDatum/Form/Inst/RuleAll` |
| datum | admitted primitive | admission | `model.Regime.data` |
| form (with arity) | admitted primitive | admission | `model.Regime.forms` |
| instance | admitted primitive | form, datum | `model.Regime.insts` |
| uniform rule | admitted primitive | form | `model.Regime.rules` |
| requirement | externally imposed challenge | datum | `model.Impose`, `Regime.reqs` |
| regime | metatheory apparatus | all of the above | `model.Regime` |

A regime's five fields are exactly `data, forms, insts, rules, reqs`. It
is frozen; nothing mutates it.

### Layer 2 — how state moves

| term | source | depends on | where |
|---|---|---|---|
| event | metatheory apparatus | supply, admission, requirement | `model.Event` |
| history | metatheory apparatus | event | sequences of events |
| replay | derived definition | history, regime | `model.replay` |
| certify | derived definition | replay | `model.certify` |

`replay` is the whole of the state rule: a regime is admissible exactly
when it equals the replay of its recorded history from genesis.

### Layer 3 — what can be seen

| term | source | depends on | where |
|---|---|---|---|
| context | derived definition | form, datum | `observe.contexts` |
| plugging | derived definition | context, datum | `observe.plug` |
| derivable | derived definition | instance, uniform rule | `observe.derivable` |
| profile | derived definition | context, derivable | `observe.profile` |
| observational collapse | derived definition | profile | `observe` docstring |
| internal separability | derived definition (**declared sense**) | profile | `observe` docstring |
| witness | derived definition | context | `observe.witness` |
| collapsed pair | derived definition | profile | `observe.collapsed_pairs` |

"Internal separability" carries a declared sense — behavioral separation
by positive derivability — and no other. Absence of a distinguishing
context is not converted into equality anywhere.

### Layer 4 — what may be proposed

| term | source | depends on | where |
|---|---|---|---|
| item | metatheory apparatus (**declared**) | admission | `candidates.Item` |
| candidate / delta | metatheory apparatus (**declared**) | item | `candidates.Delta` |
| declared bounds | metatheory apparatus (**declared**) | — | `candidates.Bounds(2, 2)` |
| cost measure | metatheory apparatus (**declared**) | delta | `candidates.mu1`, `mu2` |
| valid response | derived definition | delta, requirement, profile | `candidates.response_valid_*` |
| minimum valid response | derived definition, **relative to a declared measure and bounds** | valid response, cost measure | `candidates.min_responses` |

Four items only: fresh datum, fresh form, fresh instance, uniform rule.
The candidate space and both measures are declared bounds of the
derivation, recorded in the paper. This is the first place where the
process depends on something it does not derive.

### Layer 5 — how continuations are counted

| term | source | depends on | where |
|---|---|---|---|
| isomorphism relation | metatheory apparatus (**implemented, declared**) | regime | `iso.find_iso` |
| canonical key | metatheory apparatus | isomorphism relation | `iso.canonical` |
| non-isomorphic continuation | derived definition | canonical key | `engine._quotient` |
| tie class | derived definition | minimum valid response, canonical key | `engine._quotient` |

Presentation tokens are deliberately forgotten by the canonical key. This
is the only sanctioned way to quotient branches, and it is cross-checked
against a brute-force minimum over all bijection pairs.

### Layer 6 — where the next challenge comes from

| term | source | depends on | where |
|---|---|---|---|
| pair-separation closure policy | metatheory apparatus (**declared, not derived**) | collapsed pair, orbit | `engine.closure_challenge_orbits` |
| orbit | derived definition | isomorphism relation | `iso.pair_orbits` |
| external continuation policy | metatheory apparatus (**declared, external**) | supply | `engine.build_tree`, `supply=` |
| round | metatheory apparatus (**declared bound**) | — | `max_rounds=15` |
| node guard | metatheory apparatus (**declared bound**) | — | `pre_expansion_node_guard=250` |

This layer is entirely declared. `engine.py`'s own module docstring says
so: "No object-language endogenous demand generator was derived; both
components are declared metatheory." This is OB-1.

### Layer 7 — how the process ends and is recorded

| term | source | depends on | where |
|---|---|---|---|
| branch / node / edge | metatheory apparatus | regime, history | `engine.Node`, `engine.Edge` |
| terminal | derived definition | targets, responses | status `terminal_all_separated`, `terminal_no_response` |
| refusal | derived definition | — | `refusal.py`; `RefusalFrontier.lean` |
| frontier | derived definition | node guard, round | status `frontier_guard`, `completed` |
| artifact | metatheory apparatus | export | `artifacts/*.json` |
| claim ledger | metatheory apparatus | claim | `paper/paper_claim_ledger.md` |

### Classification vocabulary used by the ledger

`theorem`, `bounded theorem`, `finite computation`, `countermodel`,
`declared metatheory`, `unresolved`, `refused`. These are the classes
`claims.md` uses; they are the repository's own, counted from the ledger,
not invented here.

## Gaps

Marked as required by the work order. A gap is a term this packet needed
and the repository does not define.

1. **No term for a derived demand.** The repository has `requirement`
   (externally imposed) and the declared closure policy, and nothing
   between them. There is no native term for "an obstruction the object
   language itself raises", because no such object was derived. OB-1.
2. **No term for the whole process.** The repository names its parts —
   regime, event, replay, candidate, branch, terminal — and names the
   module that runs them, but has no native noun for the composite, and
   `CL-NO-UNIVERSAL-PROPERTY` refuses to call it minimal or initial.
   `process_candidate.md` therefore introduces the label **P** as a
   local abbreviation with no properties attached, and takes care to
   claim nothing of P that is not claimed of its parts.
