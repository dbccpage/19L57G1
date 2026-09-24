# conservation_ladder

AuthorityEffect: None.  Plan E of the foundations roadmap: a conditional
conservation theorem whose conserved quantity is constructed from a
symmetry.  Every hypothesis is stated, and each essential one has a
counterexample.  Integer arithmetic only; no library of analysis is used,
by the author's choice of 2026-09-23.

## The ladder

1. **Stepwise implies pathwise.**  For any step function, a quantity
   preserved by every step is preserved along every actual-step path of
   `research/native_bridge`.  This rung is conditional and supplies no
   conserved quantity.
2. **Exact first derivatives.**  Polynomial expressions are evaluated over
   dual numbers (`ε² = 0`).  The dual coefficient is *exactly* the
   syntactic directional derivative.  That is the only sense of
   differentiation used.
3. **A variational interface.**  The following are all supplied:
   - integer configurations and histories;
   - a two-point weight, and an action that sums it along a history;
   - admissible variations that move one interior point by `εv`.

   The dual coefficient of the varied action is the stationarity equation.
   So "stationary under every admissible variation" and "satisfies the
   stationarity equation" are the same condition, proved.
4. **Symmetry to charge.**  A generator `ξ` is a symmetry when the weight's
   dual coefficient along the generated flow vanishes.  If the weight is
   invariant and the history is stationary, the charge `D₂L·ξ` is
   conserved.
5. **A worked instance.**  The central weight is invariant under rotation
   for every integer coefficient `c`.  Its charge is
   `2(x₀y₁ - y₀x₁)`, which is not constant on edges.  The history
   `q_{k+1} = (2-c)q_k - q_{k-1}` is stationary, and the charge is
   constant along it and along every path of its step system.
6. **Each premise is needed.**
   - Drop the symmetry (a potential on one coordinate): the charge moves
     along that weight's own stationary history.
   - Drop stationarity: it moves along an arbitrary history.
   - A generator that is not a symmetry (a constant shift, once `c ≠ 0`):
     it is refused.

The sealed passage sits on rung 1 only.  A quantity preserved by every
passage event cannot distinguish a live state from its budget or license
variants or from its halted version.  The passage supplies no action,
variation or one-parameter generator, and this tree does not attribute
one to it.  Nor can any action supply a nontrivial charge on the states
reachable from genesis (2026-09-24): a quantity preserved by every event
keeps its genesis value there.  Off the reachable set such a quantity
exists (occurrence distinctness), so the no-go is about reachability.  The
smooth tier, and a symmetry of the passage itself, are open (`CLAIMS.md`).

## Checks

```text
python verify.py --check   # pins, tests, strict typing, Lean build, named axiom reports
python run.py --check      # the finite receipt regenerates byte-identically
```
