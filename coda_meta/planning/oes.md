# OES — Omega Engine Search (plan)

**AuthorityEffect:** None. Plan only. This page names a
research programme for search past full-text and embeddings.
It does not stand up an index, cut a remote, or extract a
spine.

**Name:** OES. Use that letter string in later pages. Do not
mint a bit-index prefix here.

Product/code record for the existing FTS, TF-IDF, skeletal
bags, typed-graph signature, and lock/key sketch is
`anomalonpy/omega_engine_operations`. This vault cites. It
does not own those files.

## What OES is

Three searches, one metaphor.

| Layer | What it finds | Status |
| --- | --- | --- |
| FTS + path filters | names, paths, tokens | keep; already shipped in operations |
| Embeddings | paraphrase | keep |
| Spine + lock | shape against a pre-declared hole | research; not shipped |

Do not replace the first two with topology. Add the third.

A **spine** is a typed digraph of *declarable units* (theorem,
lemma, definition, displayed equation that is itself the
claim, gauge or identification the source treats as a
commitment). Sections are containers, not vertices. One
signature per unit, plus containment (`unit ⊂ paper`,
`decl ⊂ engine snapshot`). One signature per paper is
withdrawn: it misses the only hit that matters — one theorem
that fills an engine lock the rest of the paper does not
touch.

Paper units and engine decls use the **same** signature
schema (today: `omega.topo_spine.signature.v2` in operations,
or a successor). Otherwise walk-distance is undefined.

## Candidate vs jewel

- Spine match, W1 proximity, or shared channels → **candidate**.
- **Jewel** = that candidate fills a lock that was declared
  *before* the spine was scored, with a witness one rung
  above the same extractor (second extractor, or a
  behavioral engine test that a declared cost moves as
  predicted, or an explicit filling construction).

“Novel-looking” is unauthorized selection. Banned.

**Lock sources, strongest first:**

1. Engine-internal obstruction (a declared cost with no
   filler). Falsifiable.
2. Imported open problem, with its own import witness.
3. Hole inferred from a spine’s own shape. **Not a jewel.**
   TODO / branch proposal only.

Locks precede branches. The library scores branches against
pre-declared locks.

## Edges

Script may emit only observational edges: `cites_by_number`,
`shares_symbol` (exact token + local scope),
`sequential_in_source` (low weight), `appears_in`.

Human admit, recorded witness: proves, specializes,
quotients, dualizes, same-up-to-gauge.

An extractor that invents “proves” from English retrieves
fiction. Default spine is thin and honest.

Signature channels are label-invariant. Shared vertex IDs
are not a match.

## Retrieval (once the index exists)

| Query | Call it |
| --- | --- |
| locks this spine nearly fills under licensed ρ\* | jewel *candidate* (jewel only if witness) |
| spines that share channels with this engine | neighbor |
| locks this engine has never posed | TODO, never a jewel |

ρ\* is a licensed edit (left-shift, named gauge, named
repair) whose cost is declared *before* the branch is
scored. Unlicensed “near-key” is a graph-kernel cosine.

MCTS / Everett branching is search in **engine space**. The
library scores a branch or proposes a lock. It is not the
branching. Fitness is a cost already in the sealed
derivation, or a verified lock-fill count. “Sounds like a
better engine” is not a fitness.

## Out of scope until the toys fail

Persistent homology on embedding clouds. That matches prose
vibe. Override only in writing, after the 20-node pairs
exist and the typed signature cannot separate them.

A public paper is an example, not a folder name.

## Next steps (order is the plan)

1. **Conversion audit.** Sample the markdown library.
   Report display-math parse rate and theorem/definition
   label retention. If usable rate is materially below
   ~80 %, fix the converter. Do not extract spines on
   garbage. No invented baseline.
2. **Neutral fixture.** One short public paper with
   numbered theorems. Hand-draw its claim graph
   (typed nodes, observational edges only) in an afternoon.
   Run the extractor. Measure recovery. If it cannot
   recover that graph, it cannot find a jewel.
3. **Toy pairs.** One 20-node paper graph and one 20-node
   engine graph that *should* match on channels **without**
   shared IDs. One pair that must not. If the toys cannot
   be written, the schema is not ready.
4. **Then, and only then:** per-unit spine index with
   containment; lock table (provenance + timestamp);
   declared ρ\* license set; witness protocol one rung
   above channels.

Implementation of (1)–(3) is a go in `anomalonpy`, not a
commit in this vault. This page records the consensus so
later work cannot drift.

`AuthorityEffect: None.`
