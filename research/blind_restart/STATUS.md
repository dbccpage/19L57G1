# Blind restart kernel — status

A packet asking whether a fresh solver, given the demands and none of the
answers, reaches what this repository already derived — and making the
comparison mechanical rather than impressionistic.

## Repository boundary

This tree is an explicitly non-sealed research surface. It must not
modify or regenerate anything under `prompt/`, `paper/`, `code/`,
`lean4/Derivation/`, or `artifacts/`. It reads two artifacts and writes
nothing outside this directory.

It follows the precedent of the sibling trees
`research/primitive_difference_tower/`, `research/portable_interface/`,
and `research/genesis_continuation/`, and takes its vocabulary from the
last of those: `research/genesis_continuation/native_terms.md` lists
every native term in dependency order with its source classification.
The kernel introduces no term that file does not already fix.

Nothing external is named here. The sibling export surface states the
rule this tree also follows: it names only objects this repository
constructs, in this repository's own vocabulary, and the direction of the
bridge is what makes it a bridge rather than a merge.

## What is here

| file | role |
|---|---|
| `KERNEL.md` | the whole of what a solver is given. Demands and a reply format; no results |
| `scoring_key.py` | resolves every expected value from `artifacts/` at run time |
| `score_packet.py` | compares a submitted packet to the key |
| `verify_pins.py` | hash pin, key resolution, and the leak gate |
| `SOURCE_PINS.json` | the two artifacts the key reads, by canonical blob hash |
| `test_blind_restart.py` | tests for the scorer and the gate |

Eight stages, twenty-five fields. Run it by pasting `KERNEL.md` into a
solver, saving its packet, and scoring:

```powershell
python research/blind_restart/verify_pins.py
python research/blind_restart/score_packet.py <packet.json>
```

## The leak gate

The design problem this tree exists to solve: a staged prompt that states
its own expected results is a leading question, and a solver agreeing
with it is not evidence. The proposal that prompted this work asked for
"typed holes, never prefilled answers" and then tabulated the answers
next to the stages. The principle was right; the table broke it.

So the answers live in the key, which the solver never sees, and
`verify_pins.py` proves mechanically that `KERNEL.md` does not contain
them: no decimal digit, no standalone `true`/`false`/`null`, and no
rendering of any expected value. Every expected value is a number, a
truth value, an absence, or a list of numbers, so none can be written in
the kernel without tripping it. The cost is that the kernel spells its
quantities as words.

The rule is blunt because a subtle rule would be arguable and this one is
not. Its known limit: it cannot catch a leak phrased in prose — a kernel
saying "no successor is forced" states an answer while carrying no digit
and no token. Nothing here closes that, and the gate must not be read as
proving the kernel is neutral. It proves one specific way of leaking is
absent.

## Nonclaims

- **A solver reproducing these values is not evidence about the
  mathematics.** That is settled by the Lean theorems and the exhaustive
  enumeration cited in `paper/paper_claim_ledger.md`. A solver agreeing
  adds nothing to it, and this tree must never be cited as if it did.
- **A solver failing is evidence about the solver or the kernel**, not
  about the derivation.
- **A pass is not a gate on the derivation.** `verify_pins.py` and the
  tests are deterministic and gateable. A solver's reply is not
  reproducible and is never a gate. `.claude/skills/inject/SKILL.md`
  puts the boundary exactly: behaviour outside the machine is outside
  the domain of any injection.
- **The scorer decides; the solver only submits.** `prompt/seed_prompt.md`
  is sealed and says: never ask an LLM to decide equality, minimality,
  isomorphism, survivor counts, or proof status. A packet is data.
- **A scored run is a receipt about one reply**, not a measurement of a
  model. No sampling discipline, repetition count, or temperature is
  recorded, and none is claimed.

## Two stages refused, not deferred

The proposal that prompted this tree asked for two further stages. Both
are refused, and the refusal is recorded here rather than left as an
absence a later reader might mistake for an oversight.

**An unjoinable overlap in the rewrite system.** This repository proves
the opposite. `lean4/Derivation/TraceAlgebra.lean::rw_confluent` proves
confluence, and `artifacts/trace_algebra.json` reports
`confluence_failures: 0`. Composition is deliberately a relation, with
`composition_may_fail` and `composite_may_be_nonunique` proved in
`lean4/Derivation/Composing.lean`. A stage demanding the overlap would
demand a solver produce something the development refutes.

**A residual with a rational dual certificate.** Not merely missing —
refused three times in this repository's own record. `prompt/prompt_pr14.md`
classes the packaging SPECULATIVE and states it is not forced by the
kernel; `artifacts/primitive_completion_receipt.json` lists the
realization "sold as forced ontology" among its enumerated attacks; and
two transport gaps in `contact/analysis/lean_theorem_transport.md` are
REFUSED for asserting that structure over code that compares two values
for difference. There is no rational coefficient object and no second
map anywhere in the sealed tree. Encoding this as a stage would
reproduce precisely the failure mode the gates were built to catch.

## Three corrections carried into the stages

Recorded because the proposal stated each the other way, and a reader
comparing the two should see which the artifacts support.

1. **The two readings are of admission semantics**, not of structure.
   `L` is strict admission, `F` possession admission — whether the
   initial inscription is retained at genesis. `code/derivation/engine.py`
   fixes both, and `CL-READING-UNDERDETERMINATION` classes the choice
   between them **unresolved** and internally unresolvable. They are
   present from the first stage, not introduced late.

2. **The tie under the first measure is finite within the declared
   bounds** — `CL-3-NONUNIQUE-MU1` gives 3 under `L` and 5 under `F`,
   under `candidate_bounds {max_items: 2, max_arity: 2}`. A separate and
   unbounded result, `CL-3-INFINITE-TIES`, proves a countably infinite
   tied family in reading `L` only, one member per arity, pairwise
   non-isomorphic. The two are different claims with different scopes,
   and the stage here scores the bounded one because that is what the
   artifact carries.

3. **The second measure resolves the tie completely** —
   `CL-3-UNIQUE-MU2` is 1 in both readings, grammar-wide in Lean
   (`mu2_unique`, `mu2_unique_F`). What survives it is weaker and
   different: within the single class sit two concrete candidates, a
   representative-selection residue recorded in
   `paper/candidate_measure_space.md`. Uniqueness of a class is not
   uniqueness of a candidate.

## Verification boundary

The `research` job in `.github/workflows/verify.yml` runs the three
commands below. Each is evidence about the commit it ran on.

```powershell
python research/blind_restart/verify_pins.py
cd research/blind_restart
python -m unittest discover -s . -p "test_*.py"
python -m mypy
```

The vocabulary firewall in `tests/test_primitive_contact.py` reaches this
tree, as it reaches every tracked path outside `contact/analysis/`.

**What no gate here checks:** whether the kernel's demands are the right
demands, whether a solver followed the firewall rules it was given, and
whether a submitted packet was produced by reasoning rather than by
recall. A solver that has read this repository will score well and prove
nothing. That is the central limitation of the instrument and it is not
closeable from inside it.

## Injection record

A gate is not proved by being green.

| injection | observed |
|---|---|
| packet asserts a cost floor one below the artifact | `FAIL cost_floor.minimum_cost.L: expected [2,-1], got [1,-1]` |
| packet asserts the first measure leaves one class | `FAIL tie_under_first_measure.tie_classes.F` |
| empty packet | eight `absent from the packet` lines, `0 of 25`, exit 1 |
| truth value submitted as a number | fails: values compare as canonical renderings, and `"false"` is not `"0"` |
| integer submitted as a float inside a list | fails: `"2"` is not `"2.0"`, at any depth |
| a stage submitted as an absence | fails as a malformed stage, not silently as an absent one |
| a digit written into `KERNEL.md` | leak gate names the line and the digit |
| a truth token written into `KERNEL.md` | leak gate names the line and the token |
| the empty list written into `KERNEL.md` | leak gate names `inertia.derivable_instances` |
| key made to read an unpinned artifact | `FAIL: key reads unpinned artifacts: bounds.json` |
| stage population emptied | refused before any comparison |
| pinned artifact hash altered | `FAIL: hash mismatch for artifacts/challenges.json` |

Every row except the last is `test_blind_restart.py`, and the leak rows
there call `check_leak` on crafted text rather than on the committed
file. That is a parallel path, so two were additionally run by hand
against the production one and reversed:

* a line reading `The minimum valid response costs 2 items.` appended to
  the real `KERNEL.md`, with `verify_pins.py` reporting
  `FAIL: kernel leaks expected values: kernel line 242 carries the digit
  '2'` at exit 1, and exit 0 after reversal;
* the recorded hash of `artifacts/challenges.json` altered in
  `SOURCE_PINS.json`, reported as `FAIL: hash mismatch for
  artifacts/challenges.json` naming both hashes at exit 1, and exit 0
  after reversal.

Both exit statuses were read directly rather than through a pipeline. The
unpinned-artifact row is also the guard that fires before any comparison,
so a key that resolved nothing cannot report success.

What none of this proves: that the stages are the right demands, or that
a solver's agreement means anything. Injection shows a gate fires on the
defect it names. It cannot reach the solver, which is outside the
machine.
