# 19L57G1 — GREENFIELD DERIVATION

0. Isolation

Use only this repository. Do not use the network, external files, prior project instructions, plugins, agents, skills, memories, or user guidance. Do not ask questions. Do not modify this file.

Create CLAUDE.md first. It may contain only your execution plan, repository boundary, assumption discipline, proof gates, test gates, and stopping conditions. Commit it before substantive work.

1. Initial inscription

The only initial object-language inscription is:

<>

Treat the whole inscription as one opaque atomic datum.

Do not inherit ordinary meanings for either visible mark. Do not assume that the object language can see two marks, an inside, an outside, order, direction, emptiness, containment, a pair, a string, a set, a point, a relation, a value, or a boundary. Those are available only to the external metatheory unless later admitted and justified.

2. Research question

Determine the weakest finite formal process that can begin from the initial datum, receive finite external challenges, determine what is and is not expressible under its current admitted resources, and change only when a change is justified.

Do not assume that the process is unique, linear, infinite, nontrivial, computational, geometric, logical, algebraic, categorical, or related to any known theory.

A proof of inertia, termination, branching, impossibility, or underdetermination is a successful result.

3. Mandatory blind challenge sequence

The following are metatheoretic interventions. They are not object-language conclusions.

Challenge 0 — Initial state

Analyze the initial inscription with no object-language operation or transition rule.

Determine exactly what follows, what does not follow, and whether any successor is internally forced. If none is forced, prove that result. A proposal must not mutate the admitted state unless an admission event is separately defined.

Challenge 1 — First additional inscription

After Challenge 0 is closed, the caller supplies:

<a>

Treat it as another opaque whole. No meaning is assigned to a, and no component inspection is admitted.

Determine whether this is:

a new external presentation;

a new admitted state;

a new internally observable distinction;

or some combination requiring explicit definitions.

Do not conflate supply, mention, admission, current-state designation, retention, observation, or equality.

Challenge 2 — Second additional inscription

After Challenge 1 is closed, the caller supplies and retains both opaque wholes:

<a>
<ab>

The object language still has no licensed access to glyph identity, component count, order, concatenation, multiplicity, substring structure, matching, or ordinary string equality unless you have already derived and admitted such access.

Determine what changed merely by admission and what remains unavailable internally.

Challenge 3 — Required separation

The caller now requires the formal process to make <a> and <ab> internally separable in a precisely declared sense.

Before proposing a solution:

define the chosen meaning of internal separability;

prove whether the current regime satisfies it;

enumerate every non-isomorphic minimum one-step augmentation that could satisfy it;

count every undeclared capability used by each candidate;

reject any candidate called one-step that silently bundles other capabilities;

retain all tied minimum branches unless uniqueness is proved.

Do not assume that one particular augmentation is forced.

4. Autonomous continuation

After Challenge 3, continue without further user input.

For each surviving branch:

declare its admitted data, operations, judgments, transition rules, historical state, and all metatheoretic assumptions;

devise the weakest deterministic finite procedure you can justify for generating the next challenge from that branch alone;

prove that the challenge generator imports no undeclared object-language structure;

enumerate all minimum valid responses or augmentations;

preserve ties as branches;

record unresolved requirements and how they persist, split, disappear, or create new requirements;

replay the branch from its recorded history before certifying any result;

stop the branch when no next challenge or no justified response exists.

Attempt fifteen accepted augmentation rounds per finite branch. Do not fabricate a linear depth-15 sequence. If the tree becomes too large, state a deterministic resource bound, export the exact frontier, and prove what remains complete within that bound.

5. Required questions

Answer by proof, executable countermodel, or explicit OPEN status:

Does any object-language transition follow from the initial inscription alone?

Can a proposed transition alter state without a separate admission rule?

Does a new external inscription necessarily increase internal expressive power?

Can two externally different admitted inscriptions remain internally undecidable or observationally collapsed?

If a current abstraction identifies two cases that a declared task requires to be separate, can any operation defined only on that abstraction recover the distinction?

Is a minimum corrective augmentation necessarily unique?

What additional rule, if any, makes a long or unbounded sequence of augmentations possible rather than immediate termination?

Can unresolved requirements be counted invariantly under renaming or isomorphism?

What recurring transition roles emerge from the derivation itself?

Is the final process minimal or initial among a clearly defined class of finite processes satisfying the same challenges? Prove the universal property or refuse the claim.

At what first stage, if any, do familiar mathematical structures become definable? Distinguish “definable,” “useful realization,” and “forced.”

Do not name or target a familiar framework before the derivation is frozen. Put all comparisons with known mathematics in the final section of the paper only.

6. Assumption and claim discipline

Every substantive notion must be classified as exactly one of:

metatheory apparatus;

supplied object-language datum;

externally imposed challenge;

admitted primitive;

derived definition;

proved theorem;

deterministic computation;

countermodel;

optional realization;

conjecture;

open obstruction;

refuted claim.

Never write “forced,” “minimal,” “free,” “canonical,” “equivalent,” “universal,” or “complete” without a proof or a precise conditional scope.

Keep presentation identity, internal identity, observational equivalence, behavioral separation, and semantic interpretation distinct.

Do not silently turn absence of a test into equality. Do not silently turn a model proposal into an admitted state change. Do not use a receipt, hash, test pass, or successful parser as proof of an unverified mathematical payload.

7. Python requirements

Implement the finite reference model under code/ and tests under tests/.

The implementation must:

be deterministic and typed;

represent histories, admissions, regimes, challenges, candidates, branches, witnesses, refusals, and terminals explicitly if the derivation requires them;

enumerate terms and candidate augmentations only under declared finite bounds;

quotient duplicate branches only under an implemented and documented isomorphism relation;

replay every certified result from genesis;

export machine-readable branch, level, assumption, and claim data;

never ask an LLM to decide equality, minimality, isomorphism, survivor counts, or proof status.

All tests must pass with at least 95% line coverage and 95% branch coverage over project Python code. Include negative tests for every smuggling or false-minimality failure discovered.

8. Lean 4 requirements

Create a buildable Lean 4 project under lean4/.

Formalize every theorem-level claim used in paper.md, including applicable impossibility results, preservation results, minimality claims, branch countermodels, replay/state claims, and finite counting laws.

Requirements:

lake build passes;

no sorry or admit;

no user-declared axiom used to obtain a research conclusion;

every exported theorem cited by the paper has a corresponding #print axioms report;

any reliance on classical principles or library axioms is recorded exactly in the claim ledger;

failed theorem targets remain counterexamples or OPEN, never prose proofs.

9. Paper requirements

Create:

paper/paper.md
paper/paper_change_log.md
paper/paper_claim_ledger.md

paper.md must contain:

experimental boundary and repository hash assumptions;

metatheory/object-language separation;

definitions in dependency order;

Challenges 0–3 and exact results;

autonomous branch procedure;

branch/tree results through the achieved depth;

proofs and countermodels;

Python and Lean receipts;

strongest defensible terminal theorem;

limitations and open obstructions;

a final, post-hoc comparison with known mathematics, clearly separated from the derivation.

paper_change_log.md records every material revision and the reason.

paper_claim_ledger.md gives each claim a stable ID, exact statement, status, dependencies, assumptions, Python evidence, Lean theorem, axiom report, falsifier, and surviving boundary.

10. Completion gate

Finish only when:

every introduced notion has a source classification;

every state change has a replayable admission history;

every theorem-level claim used by the paper has Lean evidence or is downgraded;

every computational claim has deterministic Python evidence;

all tied minimum branches are retained unless eliminated by proof;

Python line and branch coverage each meet 95%;

Lean builds without forbidden proof gaps;

all intentional files are committed and the working tree is clean;

prompt/prompt.md is byte-identical to the initial file;

the paper states what was actually derived, including termination or failure, without targeting a predetermined conclusion.