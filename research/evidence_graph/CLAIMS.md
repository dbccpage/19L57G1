# Claims

AuthorityEffect: None.

| Claim | Status | Statement | Evidence |
| --- | --- | --- | --- |
| CL-EG-CENSUS | VERIFIED_FINITE | The explicitly frozen population has 103 research trees and 23,426 public blocks across 375 files; each has a disposition. Scope is the configured public roots and source snapshot, not every future file. | source_population.json; evidence/summary.json; evidence/coverage.md; tests/test_artifacts.py |
| CL-EG-REPORTS | VERIFIED_FINITE | Fresh selected-package reports preserve 3,953 public compiled theorem types, term binders, axioms and module populations. A compiled type does not establish that public prose has the same scope. | evidence/capture.json; scope_reviews.json; compiled_report.lean.in |
| CL-EG-INDEPENDENT | VERIFIED_FINITE | Thirty-one recorded independent commands across 24 source trees have thirty passes and one coverage failure. Specialized checks, complete verifiers, builds and unexecuted commands remain distinct. | evidence/capture.json; evidence/coverage.md |
| CL-EG-DETERMINISM | VERIFIED_FINITE | With identical frozen source and evidence inputs, the graph and coverage outputs regenerate byte-identically; explicit source/population/scope mutations are rejected by the named controls. | graph.py; evidence/artifacts.json; tests/test_artifacts.py; tests/test_schema.py; tests/test_examples.py |
| CL-EG-RANK | CONDITIONAL | Given a DependencyPath whose edges strictly decrease the supplied natural rank, its endpoint has smaller rank, so no such path returns to its start. This is a theorem of the encoded path type only. | lean/ResearchEvidenceGraph.lean; lean/ResearchEvidenceGraph/AxiomReport.lean |
| CL-EG-CURRENT | VERIFIED_FINITE | Incremental current-head views invalidate changed sources and dependent records, retain the historical graph and refresh the full population. Unchanged historical inputs are not labeled a fresh replay. | refresh.py; tests/test_incremental.py |
| CL-EG-CORRECTIONS | VERIFIED_FINITE | The twelve Section 3 subjects are ingested from the merged corrected source snapshot `b55fc96a` as a separate version. Each binds its corrected source spans, scope, remaining obligations and disposition to twelve local checks run at that exact tree, all exiting 0. Every record's mathematical status stays OPEN, and the historical graph keeps its own snapshot. (2026-09-24; OPEN until then.) | corrections.py; correction_reviews.json; versions/section3.json; tests/test_corrections.py |
| CL-EG-HEADLINES | OPEN | Adequate support for every public headline is not established while unresolved scope rows remain. Inventory completion does not close this stronger condition. | evidence/coverage.json.gz; evidence/section3_handoff.json |
| CL-EG-BRIDGES | OPEN | The frontier rows and open transition maps require additional stated evidence. No autonomous successor, unrestricted adapter or broad conserved-quantity conclusion follows from this index. | evidence/handoff.json; evidence/graph.json.gz |
