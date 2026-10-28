# Keep the model attached to the word

AuthorityEffect: None. This is a reading map, not a new transport theorem.
The source paths identify the owners of each definition.

## Where the definitions live

| Setting | What is recorded | What an observation reads | Where change is checked |
|---|---|---|---|
| Python admission/search ledger | Tokens, forms, instances, uniform rules, imposed pairs | Positive derivability in well-formed contexts | Admission checks shapes; a separate search filter checks all imposed separations |
| Lean counting ledger and token-aware ledger | A datum count, or a token list, plus the corresponding structural fields | The declared formal context semantics | `stepE` / `stepT` and their `Option` results |
| Difference-interface stage | Liveness, retained relation, guarded relation, observer with laws | The observer's zero relation | A closure-step record carries its refinement and discharge proofs |
| Passage state used here | Occurrences, asserted/retained/protected pair stores, optional observation, budget, permission, refusal and halt | Membership columns after observation is declared | `step` / `pstep`, with event-specific guards |
| Represented-world kernel | Data, views, requirements, refusals, budget, augmentation license, notes | Membership columns, with a view list present from genesis | A different `step`; its obstruction includes menu exhaustion |
| Institution presentations | A declared finite carrier, presentation functions, and their family | Ordered presentation values, collected as a signature | The institution results concern those functions; they are not a general event-authorization kernel |

### Exact sources

- `code/derivation/model.py`, `observe.py`, `candidates.py`, `engine.py`.
- `lean4/Derivation/Basic.lean`, `Mention.lean`, `Erasure.lean`.
- `lean4/Derivation/DiffInterface.lean`.
- `code/derivation/primitive_passage.py`; `lean4/Derivation/PrimitivePassage.lean`.
- `code/derivation/represented.py`; `lean4/Derivation/Represented.lean`.
- `lean4/Derivation/Compression.lean` and
  `research/two_theorems/lean/ResearchTwoTheorems/Institution.lean`.

## Three words that do different jobs

**Witness.** A separating-test witness gives a test and different answers.
The passage's `wit` store instead contains retained positive pair records.
Such a record can coexist with observer agreement. Follow the source type
before drawing an implication from the word.

**Obstruction.** Passage activity is retention, protection, declared
observation, and observer-zero. The represented-world predicate
`obstructed` additionally expresses exhaustion of its declared repair
menu. The lab exhibits a passage-active state with an existing repair;
the corresponding displayed world example is not obstructed by that
world's stronger definition.

**Cost or budget.** Search mu1 counts items; mu2 compares item count and
new-form arity sum. Passage budget spends one on an accepted column
refinement or append. Declaring an empty observation is a separate event.
Neither defines the other's resource accounting.

## Bridges must say what they preserve

Unit 07's `erase_step` and `erase_replay` relate two **Lean** ledgers;
erasing a duplicate admission turns it into supply. The correspondence
to the actual Python program is separately tested, not proved by that
Lean-to-Lean theorem alone.

`Completion.ofWorld` copies the represented world's requirement list into
both retention and protection. That is a stated identification, with
its own transport results. It does not establish that retention and
protection were independent stores in the original represented world.

The passage's `obst_agrees_when_declared` relates its predicate to the
three-condition expression when an observation has been declared.
Its pre-observational policy must still be stated separately.

The two world comparisons in this lab are concrete computations on
specified associated records. They are not a proved operational bridge
for all events or all worlds. Likewise, formal preservation says nothing
about a device's actual readings until a measurement correspondence is
supplied and tested.
