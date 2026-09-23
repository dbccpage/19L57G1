# Foundations program: status of plans A to G

AuthorityEffect: None.  This note records where each plan of the
2026-09-23 foundations roadmap stands, what evidence each result rests on,
and which decisions the author made.  It certifies nothing; every result
named here is checked by its own tree's verifier.  Counts dated 2026-09-23.

## Status

| Plan | Where | Status |
| --- | --- | --- |
| A. Evidence graph and claim repair | `research/evidence_graph/`; the Section 3 corrections in the owner trees and the sealed paper | Graph merged (#229). Claim-scope corrections and the author's vocabulary ruling merged (#231), with seven custody repins its paper edits required. Correction handoff merged (#232); its correction version stays OPEN until a correction review is recorded. |
| B. Second-seed Challenges 3 to 5 | `research/second_*/` | Run blind, headless, from `research/second/SEED.md` alone. Rung three (#239, open, unmerged by the seed's rule) took leftover L-2, the first-demand index, by the seed's selection rule and names X-3 next. Challenges 3 to 5 remain ahead. |
| C. Native transition bridge | `research/native_bridge/` (#235) | Proved: actual-step paths, typed-record correspondence, cycle theorem, commuting translations, G013 read-back with a refusal. |
| D. Structural layer | `research/native_structure/` (#236) | Proved: swap cells, boundaries, cost transport and exactness, descent, a declared symmetry. Open: a proof-relevant cell calculus. |
| E. Conservation ladder | `research/conservation_ladder/` (#237) | Proved: exact dual-number derivatives, first variation, symmetry-generated charge, a worked instance, a counterexample per premise. Open: the smooth tier. |
| F. Domain adapters | `research/domain_adapters/` (#238) | Proved: adapter composition, a faithful counter, refusals for reversible domains, the proposal/license map. |
| G. Tooling and consolidation | this note; the `lean` and `research` jobs of `.github/workflows/verify.yml` | Each new tree's canonical verifier runs in the `lean` job (it builds Lean) and its receipt check in the `research` job. |

## Decisions recorded

- **Library of analysis (author, 2026-09-23).**  Plan E is algebraic
  first: exact dual-number derivatives over the integers, no external
  library, every theorem within `{propext, Quot.sound}`.  A separate
  package pinned to an analysis library, which would bring
  `Classical.choice` into that package's axiom scope, was deferred.  The
  smooth tier is OPEN until the author approves such a package.
- **No second implementation language.**  Every finite search in plans
  C to F completes in under thirty seconds on this machine (measured
  2026-09-23: the largest, `native_structure`'s square census over 240
  states and 28 events, about six seconds).  No profile shows a search
  bottleneck, so no Rust implementation or differential replay is added.
- **No common helper.**  Each new tree keeps the canonical new-tree
  verifier and its own tests, pins and receipt.  The research job calls
  each tree's own `verify.py --check` and `run.py --check`; it does not
  replace them with a shared checker.

## The adapter diagram

For a domain adapter (`research/domain_adapters/`), with source step `g`,
translation `tr`, encoding `enc`, and observations `obsA` and `obsN`:

```text
      s  --- g(-, e) --->  g s e
      |                      |
     enc                    enc
      |                      |
      v                      v
   enc s --- replay tr ---> enc (g s e)        (Sim.comm)

   obsN (enc s) = obsMap (obsA s)              (Adapter.obs_comm)
```

The squares compose along paths (`Sim.lift_append`, `Adapter.replay_obs`)
and across adapters (`Sim.comp`).  The passage's core only grows along a
step or stays fixed (`step_keep_or_grow`).  So a domain with a cycle is
encoded with a constant core: only budget and license can carry it
(`passage_sim_cycle`, `swap_core`).

## Reproducing the receipts

Each tree, from its own directory:

```text
python verify.py --check
python run.py --check
```

Or the registered steps through the local runner:

```text
python ci/run_gates.py --job lean --step "tree verifier"
python ci/run_gates.py --job research --step "receipt regenerates"
```

No hosted checks run and none are expected.
