# OES — Omega Engine Search (plan)

**AuthorityEffect:** None. Plan only. This page names a
research programme for search past full-text and embeddings.
It does not stand up an index, cut a remote, extract a spine,
or authorize a skill, agent, test, or repo surface.

**Name:** OES. Use that letter string in later pages. Do not
mint a bit-index prefix here.

Product/code record for the existing FTS, TF-IDF, skeletal
bags, typed-graph signature, and lock/key sketch is
`anomalonpy/omega_engine_operations`. This vault cites. It
does not own those files.

A 2026-08-17 multi-color pass (Grok lead, Harper, Benjamin,
Lucas) treated this page as both a paper/engine search plan
and the algorithm later reuse would apply to op-reads, skills,
agents, code, tests, and per-repo tracking. Red named the
hinges. Green made them executable without expanding
authority. Blue supplied parallel typed ontologies and the
op-read interface. This revision records all three. The
earlier note that green item 4 was truncated is withdrawn:
the remainder arrived.

## What OES is

Three searches, one metaphor.

| Layer | What it finds | Status |
| --- | --- | --- |
| FTS + path filters | names, paths, tokens | keep; already shipped in operations |
| Embeddings | paraphrase | keep |
| Spine + lock | shape against a pre-declared hole | research; not shipped |

Do not replace the first two with topology. Add the third.

A **spine** is a typed digraph of *declarable units*.
Sections are containers, not vertices. One signature per
unit, plus containment (`unit ⊂ paper`, `decl ⊂ snapshot`).
One signature per paper is withdrawn: it misses the only hit
that matters — one unit that fills a lock the rest of the
source does not touch.

Claim-unit stable IDs carry the repo prefix:
`prefix:local-id`, and from this vault
`prefix:track:local-id` (`prefix_table.md`,
`vault_layout.md`). Two units with the same local name
under different prefixes are different vertices. Shared-ID
matching across prefixes is forbidden.

The **paper/engine kinds** are: theorem, lemma, proposition,
corollary; definition that introduces a later-referenced
name; displayed equation only when it is itself the claim;
gauge or identification the source treats as a commitment.

Paper units and engine decls use the **same** signature
schema (today: `omega.topo_spine.signature.v2` in operations,
or a successor). Otherwise walk-distance is undefined. The
schema is versioned so historical spines stay comparable
after ontology extensions.

Math kinds are never silently reused on other surfaces. For
every non-paper domain a short ontology document is required
*before* any spine is extracted. It must list: allowed kind
enum, observational edge licenses only, and the analogue of
the conversion-quality gate. That document is the firewall
against category error and AuthorityEffect creep.

Observational edges are not authorization, dependency, or
“implements” edges. Agents receive candidates. Any
AuthorityEffect change follows the normal sealed path.

## Candidate vs jewel

- Spine match, W1 proximity, or shared channels → **candidate**.
- **Jewel** = that candidate fills a lock that was declared
  *before* the spine was scored, with a witness from the
  sealed list below.

“Novel-looking” is unauthorized selection. Banned.

The earlier wording “witness one rung above the same
extractor (second extractor, or a behavioral engine test, or
an explicit filling construction)” is **withdrawn**. Those
three are not equal. In practice the weakest that passes
would be chosen, and a second LLM pass would be claimed as
the rung.

**A witness is valid only if it is one of:**

1. machine-checkable movement of a pre-declared residual or
   cost already present in the sealed derivation (preferred
   on software surfaces: residual certificates already in
   `domain/`), or
2. an explicit construction that a deterministic checker can
   re-execute offline, including a registered test that
   claims to move a residual and is itself a claim unit
   under the test ontology, or
3. a second human admit recorded with identity and timestamp.

Any extractor that reuses the channel-producing code path,
including a second LLM call, is disallowed. The witness must
not depend on the same signature channels that produced the
candidate.

**Lock sources, strongest first:**

1. Engine- or test-internal obstruction (declared residual
   or failing property with no filler). Falsifiable.
2. Imported open problem / issue / TODO, with its own import
   witness.
3. Hole inferred from a spine’s own shape. **Not a jewel.**
   TODO / branch proposal only.

Locks precede branches.

**Lock lifecycle.** States: `open` → `candidate-attached` →
`filled` (with witness) → `superseded` / `retired`.
Conflicting locks cannot both be active. Supersession
requires a reason and a pointer. Optional time- or
version-based decay. Stale locks are retired, not ignored.

## Edges

Script may emit only observational edges.

Paper/engine: `cites_by_number`, `shares_symbol` (exact token
+ local scope), `sequential_in_source` (low weight),
`appears_in`.

Code / skills / agents (script-licensed, only after that
domain’s ontology document exists):

- `references_by_name` (import, call, skill-invocation by
  stable name)
- `shares_identifier` (exact token / skill-id / residual-id
  in scope)
- `sequential_in_source` / `appears_in` (file, package,
  skill-bundle)
- `tested_by_link` only when the test literally names the
  unit
- `cites_by_prefix` when the foreign unit is named and the
  edge crosses a repo prefix (`multi_repo.md`)

Cross-prefix auto-edges that assert ownership, authority, or
lock-filling are forbidden. A foreign fill attempt emits a
residual; only the declaring prefix may mint a jewel.

Human admit, recorded witness: proves, specializes,
quotients, dualizes, implements, satisfies,
depends_for_correctness, authorized_by, dualizes_skill,
same-up-to-gauge.

An extractor that invents a semantic edge retrieves fiction.
Default spine is thin and honest. There is **no auto-thicken
step**. A thin honest spine is the correct outcome when the
source is sparse. Search returns fewer or zero candidates.
Utility is precision of the candidates that appear, not
graph density. “Keep track of every part” means op-read the
units that exist, not invent units to fill the graph.

Signature channels are label-invariant. Shared vertex IDs
are not a match. Until the channel vector is a versioned
object, implementers must not fall back to embedding cosine
or ID overlap.

## Retrieval and op-read

| Query | Call it |
| --- | --- |
| locks this spine nearly fills under licensed ρ\* | jewel *candidate* (jewel only if witness) |
| spines that share channels with this engine | neighbor |
| locks this unit would introduce / this engine has never posed | TODO, never a jewel |

ρ\* is a licensed edit (left-shift, named gauge, named
repair) whose cost is declared *before* the branch is
scored. Unlicensed “near-key” is a graph-kernel cosine.

The ρ\* license set is a **first-class sealed object**:
versioned; default empty or the observational set only.
Adding a left-shift requires an explicit admit record with
AuthorityEffect review. Silent growth inside an agent loop
is refused.

MCTS / Everett branching is search in **engine space**. The
library scores a branch or proposes a lock. It is not the
branching. Fitness is a cost already in the sealed
derivation, or a verified lock-fill count. “Sounds like a
better engine” is not a fitness.

**Op-read** (the “keep track of every part” interface), given
a skill, agent, or repo version, only after that domain’s
ontology document exists:

1. Extract its claim-unit spine under that ontology.
2. Query the lock table for near-fills under licensed ρ\*.
3. Surface new holes the unit would introduce.
4. Return candidates only. Never auto-promote to jewel.
   Never write AuthorityEffect. The spine is evidence, not
   authorization.

A thin-spine **diff** between two versions of the same
repo/skill surfaces new claim units, lost observational
edges, or unauthorized thickening. That is a drift detector,
not a jewel finder.

## Blue: parallel ontologies (documents before extract)

Same algorithm. Parallel typed ontologies. No vibe matching.
No unlicensed ρ\*. Locks still pre-declared. Witnesses still
replayable.

Required short documents, each before any extract in that
domain:

- `paper_spine_kinds` — the paper/engine list above (this
  file)
- `code_spine_kinds.md` — written. Kinds, observational
  edges, conversion-quality analogue, Residual miniature,
  lock/op-read examples
- `agent_spine_kinds` — TrajectoryStep, ToolCall,
  Observation, AuthorityEffectRecord, SkillInvocation.
  Not written. No extract on agent surfaces until it is

Never force the paper ontology onto software.

Cross-domain toy pairs are required before any claim that
the shared signature works across domains: one 20-node paper
graph and one 20-node code/skill graph that *should* match
on channels without shared IDs; one pair that must not.

## Out of scope until the toys fail

Persistent homology on embedding clouds. That matches prose
vibe. Override only in writing, after the 20-node pairs
exist and the typed signature cannot separate them.

A public paper is an example, not a folder name.

## Residuals that remain (unexecuted, not unstated)

Policy above is locked. These artifacts still do not exist.
Downstream jewel or production-index claims stay provisional
until they do.

1. Conversion / parsing CI numbers (named parser, two rates).
2. Neutral fixture recovery against the numeric bar below.
3. Paper/engine 20-node match and non-match toys, then the
   written channel vector that makes two independent
   implementations agree on those decisions.
4. Versioned ρ\* object and lock table actually running the
   lifecycle states.
5. Domain ontology documents for any non-paper surface
   before first extract. `code_spine_kinds.md` exists as
   plan. `agent_spine_kinds` does not. Neither is an
   extractor.
6. **Human-admit pressure.** Observational default + no
   auto-thicken is the throttle. Soft auto-admit heuristics
   under scale remain a defect class, not a future feature.

## Next steps (order is the plan)

1. **Conversion / parsing gate as a CI artifact**, owned by
   the operations package. Fixed sample or full corpus, named
   parser, two numbers: display-math (or AST) parse rate and
   label/symbol retention rate. Threshold ~80 %. Below
   threshold, spine-extraction jobs are refused. No invented
   baseline. Later, the same pattern for docstring /
   test-discovery fidelity once `code_spine_kinds` exists.
2. **Neutral fixture.** One short public paper with numbered
   theorems. Hand-draw its claim graph (typed nodes,
   observational edges only) in an afternoon. Pass only if:
   node recovery ≥ 90 % (stable ID or text-hash);
   licensed-edge recovery ≥ 80 %; zero semantic edges
   invented by the extractor. Containment precision/recall
   measured separately and not folded into those two
   numbers.
3. **Toy pairs (paper/engine).** One 20-node paper graph and
   one 20-node engine graph that *should* match on channels
   **without** shared IDs. One pair that must not. Then write
   the channel vector so two independent implementations
   produce the same match / non-match on those toys. If the
   toys cannot be written, the schema is not ready.
4. **Write the ρ\* license object** (versioned, default
   observational / empty). Do not grow it in an agent loop.
5. **Lock table** with the lifecycle states, conflict ban,
   supersession reason+pointer, and retire-not-ignore.
   Then the per-unit spine index with containment.
6. **Domain ontology documents** (`code_spine_kinds`,
   `agent_spine_kinds`) before any production use on those
   surfaces, plus the cross-domain toy pairs.

Axiom (`axiom.md`) is not a fourth search layer. FTS,
embeddings, and spine/lock stay in operations. The free
org may later query *candidate* events those tools emit.
It does not score jewels.

Implementation of (1)–(3) is a go in `anomalonpy`, not a
commit in this vault. This page records the consensus so
later work cannot drift.

`AuthorityEffect: None.`
