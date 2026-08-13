# Controller universality: the genuine test, and its refutation

Run: PR #12, Phase VII.  Sources:
`lean4/Derivation/ControllerCategory.lean`,
`code/derivation/controller_category.py`,
`artifacts/primitive_controller_category.json`.

The sealed run proved only
UNIQUE_PROBE_COMPLIANT_DESCRIPTOR_IN_DECLARED_TOGGLE_CLASS and said
so.  This phase builds the actual mathematical comparison the label
was standing in for — and the honest answer is refutation, with an
exact salvage.

## The comparison class (variable event grammars, not guard toggles)

`KindDesc`: ten Booleans, one per passage event kind — 1024
controllers (`allKinds_length`, `allKinds_complete`), each executing
`interpK d s e = if enabled d e then step s e else s`.  The full
controller is the sealed passage step exactly (`interpK_full`).

## Two-rule compliance in the broad class

`ResponseLive` (refine + addCol + setBudget enabled) is the
syntactic support for the two-rule response universe, and it is
behaviorally exact:

- all 128 live members execute the two-rule resolution at the
  certified obstruction (`tworule_executable_of_live`, generic;
  exhaustive Python over all 128);
- each of the three response kinds is load-bearing: three
  countermodels over the represented next-family battery
  (`dead_without_addcol`, `dead_without_budget`,
  `dead_without_refine`).

**NONUNIQUE_CONTROLLER_FAMILY** (theorem): the live set has 128
members, and the difference is real but response-invisible — the
full controller and the no-refuse controller agree on every
refusal-free event at every state (`nonrefuse_agree`) and differ at
a certified obstruction (`refuse_distinguishes`).  Probe-style
compliance in a genuine class does not pin a unique controller; the
sealed six-toggle uniqueness was class-relative, exactly as its own
scope note stated.

## The category and the initiality question

Objects: controllers.  Morphisms: simulations (`Sim`), with category
laws proved (`comp_id`, `id_comp`, `comp_assoc`).  Genuine morphism
content exists: refusal erasure is a simulation from the full
controller to the no-refuse controller (`erase_sim` — the step reads
the refusal store only on refusal events).

**Existence is trivial; uniqueness fails everywhere.**

- `every_pair_connected`: every ordered pair of controllers admits a
  simulation — the constant map to a halted state commutes with
  every step (`constSim`, via the absorbing terminal).  So weak
  initiality is universal and vacuous; the entire question is
  uniqueness.
- `sims_never_unique`, `no_initial_ctrl`, `no_initial_live_ctrl`:
  two distinct constant simulations exist between any pair, so NO
  object is initial — in the full category or the live subcategory.
  Terminal: **INITIALITY_REFUTED_BY_constant_simulations_countermodel**.

## The strict refinement, and where uniqueness really lives

Requiring morphisms to preserve genesis and liveness
(`StrictSim`) excludes the constants (`const_not_strict`); identity
and refusal-erasure survive.  Even so, **global uniqueness still
fails**: an invariant-twist countermodel (`strict_not_unique`) —  a
map keyed to a duplicate-occurrence invariant that the step
preserves in both directions and genesis lacks — differs from
refusal-erasure only on states carrying the invariant
(`twist_ne_erase_at_dup`).

The exact salvage: **uniqueness on the genesis-reachable orbit**
(`strict_agree_on_reachable`, via `sim_pinned`): any two strict
simulations agree on every state replayable from genesis; the
countermodel lives only off the orbit (`reachable_no_dup`,
`twist_erase_agree_reachable`).

## Verdict

The controller has no genuine universal property in the declared
class: not initial, not uniquely weakly initial, and the strict
refinement rescues uniqueness only orbit-relatively.  What is true
and proved: response-liveness is exactly the two-rule support; the
live family is essentially non-unique (tied minima retained: the
refusal toggle and its like are response-invisible); simulations
agree on everything replayable.  Agreement is a replay theorem, not
a categorical one — consistent with this repository's oldest
discipline: replayability, not universality, is what the
constitution actually buys.

Terminals: NONUNIQUE_CONTROLLER_FAMILY,
INITIALITY_REFUTED_BY_constant_simulations_countermodel (with
STRICT_UNIQUENESS_ON_REACHABLE_ORBIT as the proved positive scope).
