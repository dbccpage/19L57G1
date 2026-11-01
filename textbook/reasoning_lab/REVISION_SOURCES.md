# Optional source details: supports and withdrawal

Lessons 62–64 select `research/x302_operational_reasoning`, outside the
seal. The parcel/lamp wording and reading sequence are book apparatus.
They do not extend the sealed derivation or establish observations.

## Python owner and teaching checks

`reasoning.py` supplies `OperationalTMS`, formula constructors, explicit
inference operations, conflict scans and withdrawal. The book uses
`add_axiom`, `add_hypothesis`, valid implication/conjunction steps,
`detect_contradictions`, `compute_minimal_retractions` and `revise`.
It does not modify private conflict sets or use a different revision engine.
The source calls the supplied positive withdrawal costs “entrenchment.”

The notebook stores multiple derivation records of the same formula.
Each record has one recorded justification. Support is the union along
that justification, not a search for logically indispensable assumptions.
Conjunction followed by taking one component can retain hypothesis names
that another derivation of the same component would not use.

The conflict scan compares recorded active formulas: a formula and its
direct negation, unequal values of the same variable, or an explicitly
derived contradiction record. Inferences are requested explicitly.
Scanning is not saturation under the deduction rules, and absence of
recorded conflicts is not a general satisfiability certificate.

The candidate routine first minimizes the number of withdrawn names,
then total supplied cost. It retains all remaining ties sorted by names.
The default revision chooses the first. An explicitly supplied withdrawal
is checked for hitting recorded conflicts and excluding named axioms;
that API does not enforce minimum size/cost or validate every extra name.
The lessons select candidates returned by the routine. The book control
also uses a valid larger withdrawal to check independent surviving records.

Fixed-premise conflicts raise an error after insertion has begun. That
error supplies no rollback guarantee; the failed teaching instance is
discarded. The exposed node mapping is not an immutable storage boundary.
Only the declared operations on well-formed book inputs are exercised.
The native inference validator has no final rejection branch for unmatched
rule kinds. The book uses its stated implication/conjunction branches;
validation of these calls does not validate every other possible rule tag.

`revision.py` checks the lessons and computational practice questions 1–9.
Its independent oracle enumerates all eight subsets of three hypothesis
names. It compares every one of the 128 families of nonempty supports at
all 27 cost assignments from 1–3: 3,456 notebooks, constructed using public
native operations. It replays every returned tied candidate and checks
deactivation, surviving fixed assumptions and rescanned conflicts. The
additional 9/1/1 example checks count-before-cost priority. These are finite
calculations, not an unbounded proof of Python correctness.

## Exact Lean scope

The book wrapper assembles the unchanged whole
`lean/OperationalReasoning.lean` body and checks the eighteen named reports
in its `Inventory.lean`. Seventeen reports have empty axiom sets;
`conj_intro_support_mem` uses exactly `propext`. The source text pins are in
`revision_sources.json`; updating them requires reviewing changed sources.

Lean support is a list, allowing repeated names; Python uses a set.
The Lean membership results express the corresponding support collection,
but no full Python-to-Lean refinement is established. Its formula names
and carrier values are natural numbers, unlike the Python string labels
and general value objects. Lean's `derivation_soundness` assumes a valuation
satisfying every fixed premise and every supported hypothesis.

`retraction_restores_consistency` requires both a hitting set and a conflict
list containing the support of **every derivation of contradiction**.
Python's finite scan of recorded nodes does not establish that coverage
hypothesis. Do not replace it with “the program found no conflict.”
The eighteen reports do not prove the Python optimizer or an empirical
correspondence. No imported school of revision or psychological model is
needed to read the lessons; owner terminology remains supplied research.

## Reproduce

From the repository root, run:

```powershell
python textbook/checks/u00_revision.py
python textbook/checks/u00_revision_lean.py
```

The second command uses the installed book Lean toolchain and temporary
source assembly. It does not rewrite the research package or its receipt.
The canonical local textbook job discovers both wrappers. Its full receipt
must be reported separately from these focused checks. No media changed.

AuthorityEffect: None. No independent reader trial or physical evidence is supplied.
