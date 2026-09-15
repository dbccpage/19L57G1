# Target: Endogenous Continuum

AuthorityEffect: None.

Local research tree testing four finite constructions over discrete relational
structures. It consumes three sealed derivation sources in read-only mode. The
word “continuum” names the research target; no continuous carrier or analytical
limit is constructed here.

## Overview of Pathways

This research program explores four distinct endogenous tracks for relational systems:

1. **Track 1: Endogenous Observer Enclosure**
   Implements finite observer panels carried with relational states and checks
   append-only trace invariants under the declared local transitions.

2. **Track 2: Projective System**
   The Python model checks complete families of finite movegraphs, bonding-map
   morphisms, composition, full coherent threads, and finite path-metric
   properties. The Lean model proves identity and composition for finite binary
   carrier prefixes and proves that explicitly copied costs are unchanged. It
   does not prove transition preservation for the attached Lean movegraphs.

3. **Track 3: Dissipative Cycle Filtering**
   Checks finite autonomous transition graphs, validates closed-cycle witnesses,
   and prunes declared sinks and feeders. The Lean bound requires both strict
   potential decrease and an explicit lower bound.

4. **Track 4: Confluence-Driven Internal Quotienting**
   Checks bounded rewrite censuses and rejects empty or truncated censuses. The
   Lean local-to-global theorem assumes termination and local confluence; unique
   normal forms are conditional on those hypotheses.

## Verification

Run verification via:

- `python research/endogenous_continuum/verify_sources.py`
- `python research/endogenous_continuum/verify.py --check`

The second command runs the focused tests, strict typing, the Lean build, and
the declared theorem/axiom inventory before comparing `evidence/receipt.json`
byte-for-byte. `evidence/receipt.json` is marked `-text` locally so checkout
line-ending conversion cannot invalidate that comparison.
