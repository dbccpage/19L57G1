# Optional source details: meanings, changes and reports

Lessons 56–61 select `research/x301_formal_semantics` outside the seal.
Its models and vocabulary are supplied research, not a derivation from
the seed. The card interpretation, aliases and reading sequence are book
apparatus. This is a selected introduction, not whole-tree validation.

## Exact Python scope

`formulas.py` supplies the formula constructors. `model.py` evaluates
against supplied relations and an assignment. The book aliases `form_0`
as blue and `form_1` as triangular, both unary. Positions 0–2 name A–C.
Custom domain `selected` supplies the finite quantifier domain.

Atomic answers are 0 or 1; identity is resolved-value equality. The
connectives and bounded folds preserve binary values from these leaves.
Intermediate rational scores are supported separately by `valuation.py`;
the evaluator does not produce half-valued atoms. Its negation gives 1
only at zero, so it is not probability complementation. Python boolean
conversion recognizes exactly 1, distinct from testing equality with zero.

The constructors do not establish well-formed native states or formulas.
Unknown relation names evaluate to zero; unknown domain names return an
empty list. Numbered-form evaluation filters unresolved nonnumeric terms
before checking arity, and does not generally check carrier membership.
Custom relation/domain names can override built-in names. The examples
supply declared names, in-range positions and matching arities; there is
no general malformed-input validation claim. The five-field conversion
to the native regime drops custom relations/domains. No general codec or
Python-to-Lean refinement is proved here.

`intervention.py` tries each candidate independently from the same starting
model. Its reference predicate means that some supplied candidate changes
the formula value. It is not a physical trial. Behavioral congruence in
Python also compares the starting evaluations; Lean compares only the
explicitly supplied state/sequence combinations, which need not include
the empty sequence. Isomorphism transport and general congruence are
outside these six lessons.

## Panels, guards and custody

`Panel` enforces length at least three, not unique identifiers or independent
sources. Projection callbacks can add facts. For positive consensus, the
Python guard rejects a starting value other than 1 or any candidate result
other than 1; absent positive consensus it refuses without an illusion
receipt. It can refuse a true starting claim after an intervention removes
a fact. A receipt's negative verdict label must retain that temporal scope.
When the starting value is already false and no candidate keeps it false,
the implementation can select the first candidate's name while storing
the starting value as the after readout; this is not a replay certificate.

Refusal retains the original object reference. Frozen dataclasses do not
freeze the nested mappings or constrain arbitrary callbacks. A disposable
shared-dictionary control demonstrates mutation despite retained reference.
All main examples use pure procedures and immutable relation sets.

`panel.py` checks a hash of its recorded fields. Recomputing the hash after
editing fields can pass; it does not establish their truth, author or
physical source. The deterministic receipt contrast supplies a fixed
example timestamp. Actual guard receipts retain the source's clock.

## Lean evidence

The entire unchanged `lean/FormalSemantics.lean` body is assembled into the
existing book driver. Its relations take three scores, its terms range over
natural numbers, and its quantifiers use explicit finite lists. `dataCount`
alone does not restrict relation arguments. These definitions differ from
the Python finite tuple representation and rational score type.

Eight selected native reports cover `constructive_lem_fails`,
`satisfaction_compositional_conj`, `satisfaction_compositional_neg`,
`satisfaction_modus_ponens`, `empty_intervention_cannot_discriminate`,
`panel_agreement_not_truth`, `grounding_firewall_refuses_panel_illusion`
and `refusal_preserves_state`. The first six have empty axiom sets;
the last two use exactly `propext, Quot.sound`. Combined Reasoning has
198 reports: 160 empty, five `propext`, 33 both. These are selected reports,
not the native full census or the repository's twelve-family gate contract.

Lean's panel counterexample already has a false starting model and uses
the empty intervention sequence. Its illusion condition does not require
a changed answer. Its guard checks the specified after-model value, unlike
Python's additional starting check. Its receipt has no checksum field.
Without positive panel consensus Lean proceeds to the proposed state;
Python refuses. At an after-score of half, Lean's zero-only test also
does not refuse on that score alone. These policy differences remain explicit.
Its execution theorem returns the current mathematical state on refusal;
it proves no Python callback purity or physical truth claim.

## Reproducible finite examples

`semantics.py` runs native bare imports in a separate `-I` interpreter and
checks module paths and six UTF-8/LF text hashes from
`semantics_sources.json`. It leaves other routes' imported modules intact.
The declared populations are 24 assignments over eight blue-membership
models, 64 model/domain pairs, 96 honest-panel/menu contexts and 25 ordered
score pairs on the quarter grid. These finite checks do not prove behavior
for every model or callback. Seven changed computational tasks are checked;
the eighth asks for a proposed observation procedure. No trial or learner
score is fabricated. AuthorityEffect: None.
