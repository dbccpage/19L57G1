# Figures — the single source

**AuthorityEffect:** None. A register is not evidence. Each row *names*
its evidence; the row itself proves nothing.

Every figure CODA restates from the sealed derivation lives here, once.
Prose elsewhere under `coda/` cites a figure id; it does not carry a
number with no source.

## Why this file exists

Three copies of the same counts existed in
`000_no_self_authorization/` — in the outline, the paper, and the essay —
and nothing compared any of them to the machine. The outline said so in
its own text: *"no gate compares these copies against it — if they
drifted, nothing would fail."* The sealed paper's §12 shows what that
costs when left alone: its receipts sat at 82 tests and 51 axiom reports
while the true figures reached 435 and 1314, and the stale text was the
flattering one.

The fix is not to compare copies. It is to have one source and cite it.
**You cannot drift from a copy you did not make.**

`tests/test_coda_figures.py` binds every row below to the machine and
fails by name on drift, when that test is present. This register is the
source either way.

## Rules

- A figure is registered here or it is not used in `coda/` prose.
- A row's `kind` says what backs it:
  - `claim` — a key in `artifacts/claims.json`. Machine-checked.
  - `lean` — a theorem name in `artifacts/lean_axioms.txt`, resolved
    uniquely. Machine-checked.
  - `external` — an external frame. **Not checked here**, and the gate
    asserts that it is not, so an unbacked figure cannot pass as backed.
- Prose citing a figure writes its id, e.g. `FIG-TIED-L`.
- Drift is a finding for a human. The gate never rewrites prose.

---

## FIG-TIED-L

- kind: claim
- value: 3
- claim_key: CL-3-NONUNIQUE-MU1.L
- phrase: 3 tied non-isomorphic minimal responses under reading L
- scope: within declared bounds — items at most 2, arity at most 2

## FIG-TIED-F

- kind: claim
- value: 5
- claim_key: CL-3-NONUNIQUE-MU1.F
- phrase: 5 tied non-isomorphic minimal responses under reading F
- scope: same declared bounds as FIG-TIED-L

## FIG-TIED-ARITY

- kind: lean
- value: countably infinite
- lean_theorem: markK_pairwise_noniso
- phrase: a countably infinite tie family, one member for every arity
- scope: absolute over arities, no bound

## FIG-MU2-CLASSES

- kind: claim
- value: 1
- claim_key: CL-3-UNIQUE-MU2.L
- phrase: 1 isomorphism class under the refined measure
- scope: grammar-wide for reading L; within bounds for reading F

## FIG-MIN-COST

- kind: claim
- value: 2
- claim_key: CL-3-MIN-TWO.L.0
- phrase: minimum response cost is exactly 2 items
- scope: absolute over the item grammar, both readings

## FIG-MU2-CONCRETE

- kind: lean
- value: 2
- lean_theorem: augFamily_retains_ties
- phrase: the class still contains 2 concrete responses
- scope: the theorem retains both orientations of the demand. Reading
  those two retained orientations AS "the two concrete responses" is a
  stated identification, not a proved bijection — recorded so the row is
  not read as more than it is

## FIG-GAUGE-ORDER

- kind: external
- value: opposite orderings
- external_frame: observer-object gauge note; `foc_bind_4`
- phrase: two positive gauges can assign opposite orderings
- scope: **not machine-checked in this repository.** The zero verdict's
  invariance and the order reversal are external theorems, cited and not
  re-proved. `foc_bind_4` types them the same way

---

`AuthorityEffect: None.`
