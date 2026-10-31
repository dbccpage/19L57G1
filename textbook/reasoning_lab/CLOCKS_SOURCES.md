# Clocks and future readings: sources and scope

AuthorityEffect: None. Selected P202 teaching in
`research/p201_relational_spacetime`; no physical clock validation or
cross-language refinement theorem. The [six lessons](24_count_updates_and_ticks.md)
start with counter records before these optional source details.

## Which transition and readout?

| Item | Python owner | Lean owner |
|---|---|---|
| State | `RelationalState`: named integer registers, fast/slow counters with period metadata, step index | `CarrierState`: four unbounded Nat fields |
| A update | `a + 1` | `regA + 1` |
| B update | `(b + 1) % 4` | `regB + 1` |
| Fast clock update | ticks + 1 | clock_fast + 2 |
| Slow clock update | add 1 when the next step index is even | clock_slow + 1 |
| Readout | tuple of current register values | pair `(regA,regB)` |
| Future comparison | `are_future_equivalent`: finite horizon H, samples 0..H−1 | `FutureEquiv`: every k : Nat, including zero |

Owners are `research/p201_relational_spacetime/relational_spacetime.py`
and `research/p201_relational_spacetime/lean/RelationalSpacetime.lean`.
The native README, ledger and frozen receipt are preserved. Their broad
constant-rate wording is not promoted beyond the inspected definitions.

The Python pulse rule gives fast change 3 and slow change 1 over steps
0→3, but changes 3 and 2 over 1→4. Both are exact rational results;
they are not one constant interval ratio. In general its slow increment
over k updates starting at index t is
`floor((t+k)/2) − floor(t/2)`, while fast increments by k.
The book checks this formula on its declared finite population; it adds
no general Lean proof of the Python pulse schedule.

The native Lean theorem `relational_clock_ratio` instead proves
`fast change = 2 × slow change` for its own uniform rule. It is an
equation of differences, not a quotient of total counts. The book proves
slow change positive when k>0; at k=0 both changes are zero, and the
equation does not supply a defined ratio. Nat division’s separate
totalized programming convention is not used as a measurement rule.

## Readout equivalence and a declared contrast

The book proves `future_iff_current_readout` for the actual Lean
transition: A/B updates depend only on current A/B. Thus equal current
readouts give equal readouts for every k. Clocks can differ while all
of these selected readouts agree. This does not prove full-state equality
or equivalence under an enlarged observer.

The countdown is separately supplied teaching apparatus: a hidden Nat
remaining count decreases toward zero, and a lamp marks zero. For every
H, initial counts H and H+1 agree on samples k<H and differ at k=H.
`Textbook.Clocks.countdown_horizon_countermodel` proves that general
claim in Lean. It is not a P202 trajectory or a refutation of the
model-specific current-readout theorem. It refutes an unrestricted
finite-to-all-future inference across that countdown family.

The native all-future step-congruence theorem uses agreement at k+1
for every new k. The separate book `bounded_step_shift` keeps H shifted
comparisons from an H+1-sample premise. That bounded premise alone
does not establish the next untested sample. Extra model-specific
properties must be named rather than silently imported.

## Execution premises and native limits

`clocks.py` executes Python’s actual `step_relational`, readout helper
and rate function. Its explicit book-side state checks require exactly
ordered a/b registers, nonnegative integer fields and native period
labels 1/2. The raw dataclasses allow broader inputs: a missing b causes
KeyError, and changing period metadata does not configure the transition,
which resets those labels on its next step.

The raw future helper returns an empty tuple for horizon zero or a
negative horizon. The book rejects negatives; an empty comparison
provides no current agreement. The raw rate function merely subtracts
two supplied counter records and does not verify reachability or
interval direction. The desk obtains both endpoints through actual
replay of the selected rule.

The Lean-rule Python execution is an explicitly labelled book adapter
for the inspected four-field updates. Its finite cases are independently
checked against closed arithmetic formulas, while native Lean bodies
are re-elaborated separately. That is not a proved general refinement
between the two languages or between their different models.

## Checked scope

| Population | Count |
|---|---:|
| Recorded clock contexts | 28 |
| Recorded countdown horizons | 4 |
| Additional bounded clock runs | 1944 |
| Native Python readout-pair/horizon comparisons | 25920 |
| Additional countdown horizons | 33 |

Recorded contexts use two rules, start indices 0/1 and interval lengths
0..6. Additional runs use starts 0..5, lengths 0..8, initial A/B values
0..2, origins (0,0) or (10,3) and both rules. Every intermediate row is
compared to independent arithmetic. The readout population uses all
72 combinations of A/B in 0..2, clock fields 0/1 and starting index 0/1,
all 5,184 ordered state pairs and horizons 0..4. Horizons 0..32 check
the separate countdown. None of these populations bounds all Nat fields.

The handler fixture exercises 196 clock predictions and eight countdown
predictions, including wrong choices, zero intervals, empty samples,
prediction gates and resets. It supplies no browser-layout or learner
evidence. Changed practice checks odd start 3/span 5, nonzero counter
origins, countdown 4/5 and another pair of hidden clock fields.

## Selected Lean evidence

The exact P202 suffix beginning at `structure CarrierState` is
re-elaborated in its original namespace. P201’s earlier quantity prefix
is already consumed separately. Eight owner reports cover future
equivalence, the iteration equation, both progression formulas and
the difference-ratio equation. Eight additional book reports cover
the model-specific readout characterization, hidden clocks, nonzero
and zero changes, offsets, countdown and bounded shift.

The sixteen added axiom sets comprise ten empty sets and six exactly
`propext, Quot.sound`. With the preceding logic/P200/P201 portions the
existing driver checks 72 reports. This is selected source/book evidence,
not the owner’s seven-theorem inventory or a replacement research receipt.
Source-text hashes use UTF-8/LF normalization in `clocks.json`.

See [DEVELOPMENT](DEVELOPMENT.md) for reproduction. Composite systems,
physical tick correspondences, model identification from experimental
data, full accessibility coverage and independent beginner comprehension,
transfer and retention remain open. No physical durations or learner
scores are generated by these computations.
