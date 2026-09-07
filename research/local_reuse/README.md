# Reuse at an intermediate state

AuthorityEffect: None.

**The replay-and-branching statement is true under the stated hypotheses.
Unrestricted reuse from a bare difference is not a property of the current
driver.** The unchanged process can answer a declared finite subproblem, keep
all its tied alternatives, and stop at a result or a recorded bound. Its
semantic state and its execution context must travel with the restart.

The new proofs import the existing Genesis definitions. The experiments call
the existing engine. The packet changes no original implementation, frozen
input, claim ledger, or artifact. The audited source is
`93853697ed845284ecbb9a9b51a78c9bf5b070cb`; the historical sealed object remains
`sealed-derivation-v1` at `3100c4ed5ce70d2b6cff6d2ccd3b0251cf918d0a`.

## What is proved

For an admission prefix `p`, suffix `q`, and complete regime `r`, the actual
Lean replay functions satisfy

```text
replay (p ++ q) r = (replay p r).bind (replay q)
```

This covers every finite history cut, including refusal propagation. Both the
token-aware and token-erased existing models are covered. If the prefix
reaches state `s`, replaying the suffix from `s` gives exactly the original
result. Keeping only an observed difference is not the same as keeping `s`.

For the existing `TransStep` response relation, a path with rounds `p ++ q`
exists exactly when it has an intermediate state reached by `p` from which
`q` reaches the endpoint. That intermediate state is unique for the recorded
prefix. Every supplied finite family of valid suffixes can share the prefix,
and every resulting path replays through the existing admission semantics.
This theorem accepts any finite list length; it does not establish that a
requested number of distinct valid alternatives exists or is affordable.

The response-existence theorem retains all its hypotheses: well-formed state,
two admitted distinct target indices, and satisfaction of every standing
requirement. A fresh unary form and one instance then provide a valid response.
It does not produce the next challenge or prove that this response is the
selected minimum for every declared cost measure.

Full-state datum renaming transports finite valid response paths and preserves
their number of rounds. The action carries the requirement store and fixes
later fresh indices. This is a theorem about the response relation; an
arbitrary rewrite of one field is not such a transport.

The later passage-state model also supports every finite family of suffix
replays from a shared prefix. A rewrite certified by its existing `RwStar`
calculus preserves the endpoint inside any prefix and suffix. If the prefix
already records a halted state, every further suffix leaves that state fixed.
These statements preserve the complete passage state, including its guards,
observations, budget, and terminal flag. They do not turn a refused or halted
execution into a successful answer.

## What the unchanged executable demonstrates

The committed computation record contains full exports, not just counts.

| Experiment | Result |
|---|---|
| Reading L, measure `mu2`, seven requested rounds, external supply enabled | 12 nodes, 11 edges, depth 7, three bound-frontier nodes; all emitted tied classes retained |
| Same request with external supply disabled | two nodes, one edge; the separation is answered and closure stops at depth 1 |
| Restart the open run at its depth-2 node using its complete history, sole closure target, and five remaining rounds | the same ten descendant classes and the same full exported node/edge multisets after ID/depth normalization |
| Every original open-run edge, at every split of its parent history | 180 successful replay decomposition checks |
| Initial Reading L at bounds `(2, 2)` | `mu1`: six raw minima in three classes; `mu2`: two raw minima in one class |
| Initial Reading F at the same bounds | `mu1`: ten raw minima in five classes; `mu2`: two raw minima in one class |

These are finite computations. The universal statements above are separately
proved in Lean. There is no universal proof connecting Python candidate
enumeration, queue scheduling, global merging, and every metadata field to the
Lean response relation.

## Necessary context and counterexamples

1. **Keep the admission state and standing requirements.** A new instance can
   separate a new pair while destroying an earlier separation. Forgetting the
   earlier requirement changes which responses the engine accepts.
2. **Distinguish a fresh root from a continuation.** The driver processes one
   supplied root target first; later nodes use closure-challenge orbits. A new
   call at an already solved node reissues the old target and self-merges,
   whereas the original run's next move supplies a datum. A state with two
   closure orbits also shows that one root target does not represent both.
3. **Preserve generated-name freshness.** A reachable state already containing
   `w2` absorbs the generated datum named `w2`. A structurally identical state
   without that token grows instead. Likewise, an existing `g2` makes a supply
   move self-merge. The original driver is unchanged; these failures are
   retained as counterexamples to unrestricted token-name portability.
4. **Respect the actual candidate and resource domain.** The fast minimum
   search rejects rule-bearing bases. Nine symmetric admitted data exceed its
   default permutation budget even at zero requested rounds. The node guard
   is checked before expansion: guard one can still produce four nodes.
   A missing response below two items becomes an available response at two;
   bounded absence is not global impossibility.
5. **A state alone is not a driver checkpoint.** Exact execution resumption
   also depends on whether the root has been processed, queue, global canonical map,
   representative depths, node count, and remaining limits. The compatible
   restart example supplies a case where those differences do not change the
   result; it does not introduce a general checkpoint API.

## Changes of representation and carrier

The proved transport is a specified bijection of complete states. It does not
license dropping a requirement, adding a cost-free observation, or silently
reinterpreting an instance. Changing the carrier requires a separately
specified map and a proof of the observations and obligations it preserves.
Adding a datum by an existing admission is available under its own semantics;
that alone is not a proof that an intended carrier split has been represented.

The existing admissions retain previously admitted instances. A concrete
two-datum countermodel proves that no admission history changes the state
with only the left instance into the state with only the right instance.
Thus an arbitrary inverse move is unavailable in this event language.
Re-encoding that change in another presentation requires extra definitions.

The existing passage rewrite calculus supplies specific sound changes of
trace. It also contains a counterexample to completeness of its normalizer;
that counterexample concerns the declared rewrite rules, not every possible
calculus. Commutation needs the stated guard and frame hypotheses. Replacing
events merely because their written supports differ is not justified.

On passage states, `RenamingStructure.act_up_comm_comp` and
`act_up_comm_twostep` commute composed or successive renamings with one
declared `Up` block. They require well-formed stores, a nonhalted state,
matching carrier length, and an in-range parent. The block adds one fresh
occurrence and its asserted, retained, protected parent edge. These are
bijection laws for that block; they do not supply an arbitrary carrier split.

`BoundaryCancellation.d2_zero_unrestricted` proves coefficientwise
cancellation for the twice-applied declared alternating boundary, including
lists with repeated vertices. Its `signless_countermodel` shows that replacing
the coefficients with `+1` breaks that cancellation over the integers. The
signs and coefficient system are declared inputs. This supplies a specific
algebraic check, not an automatic choice of a successful sign change. These
passage and boundary results do not establish a bridge to the Python driver.

A separated two-datum state also has no further collapsed-pair response step.
The existing fixed-carrier bound rules out seven closed accepted rounds on two
data. Both facts are compatible with the user's allowed stopped outcome.

## What remains open

The repository does not define a faithful encoding for every outside problem,
a general correctness criterion for their answers, or automatic successful
changes of representation and carrier. Those broader claims are OPEN or
undefined at this interface. No result here establishes that they are
undecidable or unknowable. Repeated use of the same rule schema is the proved
core; a stronger state-independent identity of continuation trees is not
asserted.

See [CLAIMS.md](CLAIMS.md) for exact theorem/evidence bindings and
[REPRODUCE.md](REPRODUCE.md) for independent replay.
