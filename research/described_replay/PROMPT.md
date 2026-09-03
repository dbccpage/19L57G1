# Described replay: native construction charter

AuthorityEffect: None.

## Boundary

- `METATHEORY`: The source snapshot is
  `f4b1dcd3d3edc9e4d1557ad71ab8bf199cf762be` on `main`.
- `DECLARED_POLICY`: The only write root is
  `research/described_replay/`.
- `REFUSED`: No sealed path, shared path, or sibling research tree is
  writable in this run.
- `REFUSED`: No source outside this repository and no network source is an
  input to this run.
- `DECLARED_POLICY`: The kernel is reconstructed in this tree and is not
  imported from the sealed package.
- `DECLARED_POLICY`: Every result is scoped to the finite class and bounds
  declared in `PREDICTIONS.md`.

## Pinned native supply

Each quotation below is copied from the named LF-normalized span at the
source snapshot. The span hash includes its final LF byte.

### Seed clause one

- `SUPPLIED_OBJECT_LANGUAGE_DATUM`: `prompt/seed_prompt.md`, line 96,
  SHA-256 `702107c247a7fdd83ac648a357eea5bbe60679344e08785b04dba95db881f32e`.

> devise the weakest deterministic finite procedure you can justify for generating the next challenge from that branch alone;

### Seed clause two

- `SUPPLIED_OBJECT_LANGUAGE_DATUM`: `prompt/seed_prompt.md`, line 110,
  SHA-256 `52a7e78214a86cab4790a78a6406200fcf79fd6421641b171033ae31b457a8e1`.

> Attempt fifteen accepted augmentation rounds per finite branch. Do not fabricate a linear depth-15 sequence. If the tree becomes too large, state a deterministic resource bound, export the exact frontier, and prove what remains complete within that bound.

### Seed clause three

- `SUPPLIED_OBJECT_LANGUAGE_DATUM`: `prompt/seed_prompt.md`, line 188,
  SHA-256 `3d5b9cfb399cadc8a0a390ede7299f629ea26cea1b4119625ddf4fa9948feea2`.

> replay every certified result from genesis;

### Refused whole-process claim

- `SUPPLIED_OBJECT_LANGUAGE_DATUM`: `paper/paper_claim_ledger.md`, lines
  689-695, SHA-256
  `8a185b3c88e8f41b31646da6d40a055470627c4709c860dd1d495a8c5cbb9cc9`.

> ### CL-NO-UNIVERSAL-PROPERTY
> - **Statement**: The final process is minimal or initial among a defined
>   class of finite processes satisfying the same challenges.
> - **Class**: unresolved — **claim refused**.  No universal property was
>   proved; per the discipline, the word "minimal" for the whole process is
>   therefore not used.
> - **Deps**: n/a. **Python / Lean / Axioms**: --.

### Standing challenge-source obstruction

- `SUPPLIED_OBJECT_LANGUAGE_DATUM`:
  `research/genesis_continuation/continuation_plan.md`, lines 86-93,
  SHA-256 `96af59792dc84692b3590a4bd6e0cf02b11dd87566b46d7cbb65656cbd2e72ea`.

> * **OB-1** — the challenge source. No object-language endogenous demand
>   generator was derived (`CL-CLOSURE-POLICY`, `paper.md` §11(f)). The one
>   horizon-free generator exhibited (`generation_never_dries`) is for a
>   declared reflective rule. `G1Class.g1_class_exclusion` now proves the
>   cycle impossible for every fixed-radius, fixed-finite-alphabet member of
>   `LocalStrategy`; the earlier five-strategy, 15-round computation remains a
>   historical witness only. Continuing past this requires an out-of-class
>   repair channel or a theorem for a wider declared class. `OB1_UNCHANGED`.

### Trace and endpoint pair

- `SUPPLIED_OBJECT_LANGUAGE_DATUM`:
  `research/admission_sign_shadow/STATUS.md`, lines 59-60, SHA-256
  `610a8679e3f79ceba1fb00ea5b228c6019d44c292c1df1289a96453a8db151a6`.

> - `OCCURRENCE_HISTORY_FROM_RETAINED_TRACE = PROVED`
> - `OCCURRENCE_HISTORY_FROM_ENDPOINT = REFUTED`

## Native translation

- `DECLARED_POLICY`: `DescribedReplay` asks only about a declared finite
  class of processes. It does not alter the refused whole-process claim.
- `DECLARED_POLICY`: A process is a fixed base regime, a finite event list,
  and the shared length bound.
- `DECLARED_POLICY`: A description records the event list. It is not
  reconstructed from the final regime.
- `DECLARED_POLICY`: Admission-only means `AdmitDatum`, `AdmitForm`,
  `AdmitInst`, and `AdmitRuleAll`; it excludes `Supply` and `Impose`.
- `DECLARED_POLICY`: A described-state result distinguishes one successful
  step, completed input, and invalid input.
- `DECLARED_POLICY`: Exactly one step means one event is consumed and one
  pointer advance occurs, even when the event leaves the regime unchanged.
- `DECLARED_POLICY`: A candidate class member receives a validated
  description as a metatheoretic argument. Because no event in the declared
  alphabet reads that argument, the candidate executes its own fixed event
  list. This reading is tested rather than hidden.
- `DECLARED_POLICY`: The stage-four declared terminal is that replay ends
  with at least one admitted datum. A candidate report is read from whether
  its own fixed replay contains the designated report datum.
- `DECLARED_POLICY`: The finite outside-class reporter may exhaust the class.
  Its existence is not evidence for a reporting member inside the class.
- `DECLARED_POLICY`: A description is itself a class process only when its
  admission-event list uses the class token alphabet and meets the shared
  bound. This is checked explicitly for self-description witnesses.
- `OPEN`: Cross-language equivalence between the Python reconstruction and
  the Lean reconstruction is not claimed. Each proves or computes its own
  stated payload.
- `OPEN`: Any question beyond the declared finite bounds remains
  `OPEN_UNBOUNDED`.

## Ordered stages

### 1. Description and decoder

- `DECLARED_POLICY`: Encode each event position and event symbol as one
  fresh description token admitted by `AdmitDatum`.
- `PREDICTION`: Prove `decode_encode_id`, `encode_injective`,
  `encode_admission_only`, and the exact decoder-domain statement.
- `PREDICTION`: Construct two different histories with the same endpoint as
  this tree's own countermodel.
- `REFUSED`: The pinned sibling statement is not used as this tree's proof.

### 2. One-event stepper

- `DECLARED_POLICY`: One application consumes at most the event at the
  current pointer and calls the reconstructed one-event transition once.
- `PREDICTION`: Prove `stepper_one`, `stepper_iterate`, `stepper_total`, and
  `stepper_no_replay`.
- `REFUSED`: The stepper definition may not call whole-history replay.

### 3. One member against the class

- `DECLARED_POLICY`: Search every class member as a candidate and every
  class member as a described target. Retain the full candidate-target
  matrix and all successful candidates.
- `FINITE_COMPUTATION`: Every reproduction cell is checked by the local
  `certify` predicate and written to a deterministic receipt.
- `REFUSED`: A supplied description is not an endogenous challenge source.

### 4. Self-description and bounded reporting

- `DECLARED_POLICY`: Check self-description separately from class-wide
  reproduction.
- `DECLARED_POLICY`: Build the outside-class terminal table by exhaustion,
  compute its declared cost, then search every in-class candidate within the
  predeclared cost bound.
- `PREDICTION`: If the in-class search misses, construct a bounded diagonal
  member against each fixed candidate and prove the disagreement in Lean.
- `OPEN`: The unbounded reporting question remains `OPEN_UNBOUNDED` on every
  branch.

### 5. Cost ledger and register

- `DECLARED_POLICY`: The only cost is the number of one-event stepper
  applications plus the number of admission events in the description.
- `DECLARED_POLICY`: Check a supplied response and find responses using the
  same local separation predicate. Enumeration retains all ties at the first
  successful cost level.
- `FINITE_COMPUTATION`: Record the two declared measures as a finite table,
  including its largest row within the bound.
- `OPEN`: The enlarged class, the unbounded reporting and cost questions,
  the all-policy quotient frontier, and OB-1 remain unexecuted leftovers.

## Refusals and completion

- `REFUSED`: No claim ranges over every process.
- `REFUSED`: No bounded result is restated without its class and bound.
- `REFUSED`: No table or receipt is called a proof.
- `REFUSED`: No tie is silently selected.
- `REFUSED`: No result narrows `OB1_UNCHANGED`, `S66_UNCHANGED`, or
  `S9_LAST_UNCHANGED`.
- `REFUSED`: No census pin is regenerated by this run.
- `REFUSED`: No outside term is committed in prose or an identifier.
- `METATHEORY`: Completion requires all five stages, deterministic receipts,
  strict typing, a clean local Lean build with complete axiom reports, pin and
  scope checks, negative tests, injection records, and an exact stage
  register.
