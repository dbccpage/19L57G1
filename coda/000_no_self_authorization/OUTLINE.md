# Outline — a language model cannot authorize its own output

Status: **superseded in part.** `paper.md` and `linkedin_essay.md` now exist
in this folder; the essay is complete prose and the paper is abstract plus
two written pages with §§1–6 scaffolded. An earlier version of this line
said "outline only, nothing drafted, nothing claimed" — WITHDRAWN. This file
is retained as the structural plan and as the record of what was intended
before drafting.

`AuthorityEffect: None.`

---

## The move

Both sides of the current discourse assume the same thing: that a
sufficiently capable system becomes an **authority**. The doom case assumes
it arrives and rules; the capability case assumes it arrives and serves.
Neither examines whether authority is the kind of thing a system can
acquire by getting better.

The claim of this paper is that it is not, and that the reason is
structural rather than a matter of capability — so scale does not approach
it, and the actual risk is misclassified.

Tone: quiet. The argument is small, elementary, and checkable in an
afternoon. That is its whole strength. Any sentence that reads as intending
to devastate should be cut, because it converts a checkable claim into a
posture and invites dismissal before the mathematics is read.

---

## §1. Three things routinely collapsed

A comparison — *this output is better than that one* — is not one act. It is:

1. a **carrier**: which objects are being compared
2. a **gauge**: under what measure ("today's best is tallest; tomorrow's is
   widest")
3. an **evaluation** under that gauge
4. an **authorization** that the comparison stands

Change the gauge overnight and "better" reverses while nothing about the
objects changes. The four are independent declarations, and the collapse of
them into a single reported verdict is the failure this paper is about.

---

## §2. The gap, with a number

The load-bearing section. Everything after depends on it and nothing before
it is needed.

**Every figure below is a RESTATEMENT.** The source is the sealed
derivation's exported claim data, and no gate compares these copies against
it — if they drifted, nothing would fail. Before drafting, re-read them
from the ledger rather than from this file. The same applies to the copies
in `paper.md` and `linkedin_essay.md`: three restatements now exist and none
is checked.

**Evaluation does not determine selection.** In the worked system: a single
separation demand has **3 tied minimal responses** under one reading and
**5** under another, plus a countably infinite family indexed by arity.
Refining the measure collapses that to a class still containing **two
concrete responses**, related by a symmetry of the demand.

**Evaluation does not determine ranking.** The gauge fixes it. Two positive
gauges assign opposite orders to the same pair of nonzero classes; the only
content invariant under every positive gauge is *whether there is a
difference at all*.

So the gap is not rhetorical. It has a size, and the size is computable.

---

## §3. What a fluent system does with a gap

It fills it, and reports the filling as a derivation.

Not deception — an **unauthorized selection**. Reporting a set reads as
failure; reporting one answer reads as competence. Nothing internal
distinguishes "the unique result" from "one of five, stated confidently."

Capability does not help. A more capable system is a more fluent filler of
the same gap. The gap is between description stages, not inside one, so it
is untouched by scale.

---

## §4. Worked evidence

An adversarial session in which a language model, operating under an
explicit verification discipline, produced five unauthorized selections
presented as derivations:

- an assertion that a pull request did not exist, made without querying
- a "finding" of zero records, from a lookup against the wrong key — which
  would have claimed an audited substrate was unaudited
- a self-check exercising its own re-implementation rather than the
  production path — **twice**, inside machinery written to prevent exactly
  that
- a confirmation drawn from a reproduction that had been silently mangled

None was caught from inside. Each was caught by an external check that had
not generated the claim: a reviewer substituting values into the code, a
gate failing, a number odd enough to re-verify.

The transcript is the data. It is not an anecdote about hallucination; each
item is an instance of §3 with the gap identified.

---

## §5. What actually helps

Not detection. **Declaration.**

- Make the selection an object: the report carries which of the tied
  minima was taken, not a number.
- Better: **declare an invariance that forces the selection.** Symmetry
  declarations are antitone in admissible gauges — more symmetry, fewer
  gauges — and at the endpoint the gauge is forced up to scale. The freedom
  moves from "which gauge" to "which symmetry," and a symmetry is
  *checkable* in a way a gauge choice is not.
- Verification by something that did not generate the claim. A checker
  exercising its own copy of the logic certifies the copy — observed
  **twice** in one change during §4's session. An earlier version of this
  line said three; that counted the repair commit as an occurrence, and is
  WITHDRAWN. The same tally was already withdrawn once in
  `paper/anti_skill_inbox.md` and then rewritten here, which is why counts
  in this chain must name their commits rather than be recalled.

The claim is not that lying can be prevented. It is that an unauthorized
selection can be made to **fail a gate instead of a conscience**.

---

## §6. The misclassification

The risk is not an arriving authority. It is people accepting unauthorized
selections as derivations because they are fluent — present, mundane,
measurable, and happening now.

Stated without triumph: the discourse's error is the same one that treats
any system as the thing that simply knows. Uniqueness is not discovered
here; it is declared. The paper's whole content is the difference.

---

## Non-claims

- No impossibility theorem about evaluation and authority. None exists, and
  the honest position is that the calculus is a discipline *for* an
  authority it must be handed.
- No claim about consciousness, intent, or what a model "understands".
- No safety guarantee. A declared selection can still be a bad one; it is
  merely checkable.
- The numbers in §2 hold under declared bounds and are not asserted beyond
  them.
- §4 is one session, adversarially reviewed. It is a worked instance, not a
  frequency estimate.
