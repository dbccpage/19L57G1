# Local reuse of the existing process

AuthorityEffect: None.

This is a post-seal analysis of the existing repository at
`93853697ed845284ecbb9a9b51a78c9bf5b070cb`. It adds no object-language
operation and changes no original source. The historical frozen object is
separately `sealed-derivation-v1` at
`3100c4ed5ce70d2b6cff6d2ccd3b0251cf918d0a`.

The supplied question asks whether the same process can start at an
intermediate difference, explore several alternatives for a finite number of
rounds, and then return a result or a bounded obstruction. It also asks whether
changing the representation or the carrier provides a justified next move.
The question is a work order, not evidence for its proposed conclusion.

We separate six statements before reporting results:

1. A successful admission history can be cut at any position and its suffix
   replayed from the complete intermediate regime with the same endpoint.
   Failed admissions must keep their refusal behavior.
2. Finite paths of the existing valid-response relation can be split and
   concatenated. Every path through a chosen intermediate state participates;
   the statement does not choose a preferred alternative.
3. The unchanged executable driver can be used for a bounded subproblem when
   its actual input contract is supplied. A fresh driver call is not assumed
   to be the same operation as resuming its internal queue.
4. A bare difference, by itself, supplies all driver inputs and guarantees any
   requested branch count or number of accepted rounds.
5. Every change of presentation preserves future transitions, or an inverse
   admission can always undo an unsuccessful move. A valid transport must
   instead name its action on the complete state, including requirements.
6. Every outside problem has a faithful encoding into this process, and every
   requested change of representation or carrier is already an enabled move.

The formal layer uses the repository's actual Lean definitions and clearly
states their scope. The executable layer calls the existing Python engine;
it is not a replacement search algorithm. A finite computation does not prove
an unbounded executable refinement theorem. A stopped run is consistent with
the question's allowed blocked outcome; it is not by itself a refutation of
reuse. Missing definitions are not a proof of undecidability.

The exact executable examples request seven rounds, preserve all emitted
minimum classes, check every exported edge, and compare a restart from an
intermediate node. Counterexamples test restarting the driver, name freshness, inherited
requirements, supported candidate inputs, and resource limits separately.
