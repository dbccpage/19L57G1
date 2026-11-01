# Reproduce and review the reasoning route

AuthorityEffect: None. Run these from the repository root. No sealed
source or research receipt is written by this route.

```text
python textbook/reasoning_lab/run_lab.py --population
python textbook/checks/u00_reasoning_lab.py
python textbook/checks/u00_reasoning_lab_lean.py
python -m unittest discover -s textbook/reasoning_lab -p test_lab.py
```

The Lean command uses the existing built `Derivation.Compression` library
through the shared book-Lean runner. Build it with `lake build` in
`lean4/` if needed. The normal textbook job discovers the two check scripts.

The pinned local job uses Python 3.14.7 and `requirements.txt`:

```text
uv run --isolated --no-project --python 3.14.7 --with-requirements requirements.txt python ci/run_gates.py --job textbook --receipt artifacts2/reasoning_lab/textbook_gates.json
```

On this Windows host, set TEMP and TMP to a normal writable workspace
directory if sandbox-created temporary directories have restrictive ACLs.
This is an execution environment setting, not a test or source repair.

After an intentional, reviewed change to the teaching inputs:

```text
python textbook/reasoning_lab/run_lab.py --write
python textbook/reasoning_lab/build_results.py
```

Inspect the changes. Do not regenerate a record to hide a live disagreement.
The source map states exactly which finite populations and book proofs run.

The packet now includes twelve explicitly fictional evidence logs and
their five scoped statuses. `check_evidence_population` independently
checks 72 metadata/partial-answer cases by Boolean completion. The same
textbook Python wrapper runs it. The book-Lean wrapper checks thirteen
reports, adding the axiom-free application-incompatibility lemma.

Authoring tests reject converting ? to No, silently changing scope,
dropping the counterexample, publishing fictional rows as measurements,
and deleting the repeat conflict. They also reject malformed raw codes.
Do not use `--write` to replace or reinterpret genuine reader records;
this builder accepts only the supplied fictional fixtures.

Preview the self-contained desk:

```text
python -m http.server 8768 --bind 127.0.0.1 --directory textbook/reasoning_lab
```

Open `http://127.0.0.1:8768/results.html`. The desk selects recorded cases,
performs no Python execution or runtime data fetch, and stores no reader
responses. The Wiki build rewrites reading/download links.

Review all 288 conditional settings and 128 selected witness demands,
prediction gating and reset after scope changes, empty domains, negative
second answers, keyboard controls, narrow layout, and the rendered lessons.
Check stale packet/desk rejection with byte restoration and rejection of
an intentionally false book proof. Reader evidence remains a separate task.
Also check the evidence selector, raw-row display, prediction gating,
reset after case changes, uncertainty cases, protocol mismatch, and the
retained repeat. The optional physical worksheet is blank; no readings
or participant scores may be inferred from generating it.

For the operational continuation, run:

```text
python textbook/reasoning_lab/protocols.py --population
python -m unittest discover -s textbook/reasoning_lab -p "test*.py"
node textbook/reasoning_lab/test_protocol_controls.mjs
```

An intentional reviewed update uses `protocols.py --write`. It writes
only the new `protocols.json` and `protocols.html`; the shared renderer
accepts those explicit names while existing desks keep their defaults.
The original claim/evidence packet and desk retain their content.
The existing canonical reasoning wrappers check both packets and the
added exact research/book proofs, giving 45 axiom reports overall.
Never alter the expected sets to accept a failed proof or an extra axiom.

Thirty authoring tests cover the old and new routes. The new event-handler
fixture exercises 192 record predictions and 72 order predictions,
including gates, wrong feedback, shared setup resets and ensemble counts.
It supplies no browser-rendering or accessibility evidence.

In a real browser, check copying/constant/parity probes, stale and
overwritten records, same-target order dependence, disjoint updates,
disturbing readouts, the identity control, relay order, and both record
selections. Check prediction focus, narrow tables and arrow-key scrolling.
Keep model rows separate from physical observations and measured learning.

For the calibration continuation, run:

```text
python textbook/reasoning_lab/calibration.py --population
python -m unittest textbook.reasoning_lab.test_calibration
node textbook/reasoning_lab/test_calibration_controls.mjs
```

An intentional reviewed update uses `calibration.py --write`, which
writes only `calibration.json` and `calibration.html`. The shared builder
also supports this third explicitly named desk; older packets and desks
retain their content. Preview `calibration.html` through the same local
server. The reasoning wrappers check this packet and its bounded
population; the logic/P200/P201 portion contributes 56 exact reports,
before the P202 continuation below extends the combined driver.

Thirteen added authoring tests cover premise failures, mixed units,
zero numerator versus divisor, four false packet variants, stale desk
rejection and the actual handlers. The handler fixture exercises all
63 conversion predictions and 36 ratio/refusal predictions. None of
these fixtures supplies browser-layout evidence or a reader score.

In a browser, check both prediction gates, incorrect feedback, zero,
the 9/2 conversion, mixed-standard ratios, both refusals, same-ratio
changed magnitudes, resets, keyboard focus and table scrolling at a
phone width. Check the published reading/practice/answer links. The
blank worksheet remains blank; invented numbers are not observations.

For the clock/future-reading continuation:

```text
python textbook/reasoning_lab/clocks.py --population
python -m unittest textbook.reasoning_lab.test_clocks
node textbook/reasoning_lab/test_clock_controls.mjs
```

An intentional reviewed update uses `clocks.py --write`, writing only
`clocks.json` and `clocks.html`. Preview through the same server or the
published link. Earlier desks stay unchanged. Existing wrappers check
the clock packet/populations; the logic-through-clock portion contributes
72 reports before the composite continuation below.

Fifteen added authoring tests and two separate assembled Lean negative
variants exercise the boundaries. Actual handlers check 196 clock and
eight countdown predictions, not browser layout or learner outcomes.
The logic-through-clock authoring portion has 58 tests.

In a browser, compare both rules/starts, zero/one/odd intervals, the
difference from the pulse starting index, all countdown horizons, both gates, wrong
feedback and resets. Check table focus and arrow-key scrolling at phone
width and published practice/answer links. Never count model updates
as measured durations.


For the composite-system continuation:

```powershell
python textbook/reasoning_lab/composites.py --population
python -m unittest textbook.reasoning_lab.test_composites
node textbook/reasoning_lab/test_composite_controls.mjs
python textbook/checks/u00_reasoning_lab_lean.py
```

A reviewed `composites.py --write` updates only its JSON and HTML. The
existing wrappers check this packet, its declared populations and the
combined 114 exact reports. The whole native Lean body stays unchanged;
33 explicit owner reports and nine book reports add 42 empty axiom sets.
Eighteen added authoring tests bring the full Reasoning suite to 76.
The handler fixture checks 300 share and sixty graph choices. Two
separate assembled false Lean conclusions are rejected before recovery.

In the published browser, compare list/readout/relay order, equal shares
with different paired marks, constant probes, joint-write edges and an
undeclared read. Check both gates, wrong feedback, all context resets,
phone table focus and arrow scrolling. Keep rendering, supplied lists,
physical observations and beginner outcomes separate.
