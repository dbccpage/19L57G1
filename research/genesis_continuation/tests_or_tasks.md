# Tests and formalizations

The smallest next steps, ordered by cost rather than by importance. Each
records what it would prove, what it would **not** prove, and the
condition under which it should be abandoned rather than forced.

Only T6 bears on the main question. T1–T5 and T7 close recorded gaps that
are cheaper and independently worth closing; none of them advances OB-1,
and none should be reported as if it did.

---

## T1 — an exact comparison-policy gate after the OB-3 author act

**Do not implement before the author act.** After the author declares
instruction precedence and an exact allowed path set, add a check that fails
when a file under `paper/` carries an unlisted comparison surface or an
allowed end-only surface has substantive sections after it. A literal heading
scan can cover the six observed headings, but a path/section allowlist must
also catch a table or differently worded surface.

The allowlist and precedence rule are the design decision, not the scan. All
five same-heading surfaces carry explicit end-only markers; the map surface
explicitly cites a run directive. Two current surfaces violate end-only
placement because later substantive sections follow them. Any zero, one, or
six-path answer encodes authority this packet does not have.

**Proves**: that the six known sections and the two current placement defects
are detected, and that a seventh surface or a new post-comparison substantive
section cannot be added silently.

**Does not prove**: that the remaining prose names no external theory. A
heading scan is a heading scan. External naming outside a comparison
heading would pass it, and the `paper/primitive_difference_map.md`
instance is a *table column* under a differently-worded heading, so the
scan must be written against the observed forms and verified against all
six, not against one.

**Also does not do**: decide what to do about the six. Section 13 has already
withdrawn the old paper-global sentence, but its replacement inventory is not
exact. The remaining author choice is whether the run directives or the
no-exception prohibition govern, which exact sealed paths, if any, survive
that choice, and how the two placement defects are repaired.

**Kill condition**: no author declaration of precedence and exact path set.
In that state the gate would be a policy smuggling mechanism, so leave
`OB3_COMPARISON_POLICY_OPEN`.

**Injection required before believing it** (`CLAUDE.md`'s discipline):
remove one known section, confirm the gate goes from failing-on-six to
failing-on-five naming the right files, then restore it.

---

## T2 — refresh `README.md`

**Status, 2026-08-27 — DONE by this README update from the `24d1bc64`
census.** The former instruction “nine gate families to ten; 1417 axiom
reports to 1424; 13 parked to 12” is WITHDRAWN as current because both sides
later drifted. `README.md` now records the live eleven-family,
58-Python-source, 74-Lean-module (62 root + 12 parked), 481-collected-test
(480 passed + one skipped), 39-JSON + six-full-export, 135-claim-heading, and
1506-report census.

**Proves**: nothing. It is a correction, not evidence.

**Does not prove**: that the new numbers stay true. They drifted once and
will drift again; `artifacts/lean_axioms.txt` is pinned by a gate and the
README is not.

**Kill condition**: none — it is a few lines and `README.md` is outside
the sealed paths. If it is worth doing at all it is worth doing now.

---

## T3 — export a closed-system `mu2` baseline

**Do**: run the `supply=False` branch tree under measure `mu2` in both
readings and export it, as the `mu1` baselines already are.

**Proves**: whether pair-separation closure terminates under the refined
measure with the same round counts (L: 1, F: 3), or different ones.

**Does not prove**: anything about the open system. The closed system is
the baseline precisely because it removes the external continuation
policy.

**Why it is worth doing**: `CL-CLOSURE-TERMINATION` states its own scope
as "closed-system runs under measure `mu1` only; no `mu2` closed run is
exported". That is an asymmetry in the record with no stated reason, and
the run is cheap.

**Kill condition**: if the `mu2` closed run does not terminate within the
declared bounds, do **not** raise the bounds to make it terminate.
Export the frontier and record the difference — that would be a real
finding about measure sensitivity, and raising a bound would destroy it.

---

## T4 — reading-F non-uniqueness in Lean

**Do**: prove the reading-F `mu1` non-uniqueness, and the k-ary tie
family, at theorem strength rather than by engine enumeration.

**Proves**: it would remove the tag asymmetry in `paper.md` §11(d),
where reading L carries **[theorem]** and reading F carries **[bounded
theorem]** for the same shape of statement.

**Does not prove**: that the two readings are separated. They are not,
and `CL-READING-UNDERDETERMINATION` stands regardless of how the F-side
counts are established.

**Kill condition**: if the F-side proof needs a hypothesis the L-side
does not, stop and record the hypothesis. An asymmetric proof of a
symmetric-looking claim is a finding, not a failure, and flattening it
would repeat the error §11(d) already records having made once.

---

## T5 — the general-`n` profile correspondence

**Do**: prove the correspondence between `Generator.profile2` and the
radius-one instance of `SeparationCapacity.profileD`, for general `n`.

**Proves**: it would connect the bounded depth-2 evidence in the
generator study to the structural depth-`d` outrun already proved by
`SeparationCapacity.depth_d_outrun`, replacing instance-backed evidence
at lengths 4 and 5 with a general statement.

**Does not prove**: the repair-strategy-class exclusion. That is T6, and
this correspondence is a prerequisite for it, not a substitute.

**Kill condition**: if the two profile notions turn out not to correspond
at general `n`, that is the result — record it as a countermodel and do
not adjust either definition to make them agree.

---

## T6 — the repair-strategy-class exclusion (bears on OB-1)

**Do**: derive a declared repair-strategy-class exclusion from
`CapacityBound.capacity_bound`. This is the repository's own stated
single best next theorem target.

**Proves**: it would lift the exclusion from "empty within the declared
15-round computation over five declared strategies" to a statement about
a **class** of strategies. That is the difference between an exhausted
search and a theorem.

**Does not prove**: G1. Even a class-general exclusion would say that no
strategy *in the declared class* both fires, clears, and avoids
recurring imports. G1 asks for a repair channel that separates without
minting identity-grade distinctions, **or a proof that none exists**, and
a class-relative exclusion is neither: the class is declared, so a
negative result over it inherits the declaration.

This is the honest ceiling of T6, and it is worth stating plainly before
starting: **T6 does not close OB-1.** It narrows it. The distance between
"no strategy in this declared class" and "no repair channel" is exactly
the distance between a declared candidate space and a derived one — the
same gap that N1 and N2 record at the response layer.

**Kill condition**: if the derivation requires quantifying over
strategies in a way `capacity_bound` does not support, stop. The paper
already warns that the capacity theorem bounds local finite-alphabet
views and "does not itself quantify over strategies or prove the
class-general cycle exclusion". Forcing it would produce a proof of a
weaker statement wearing the stronger one's name, which is the failure
mode `paper/pr11_correction_ledger.md` exists to document.

**Status, 2026-08-26 — T5 CLOSED.**
`SeparationCapacity.radius_one_agrees_with_sealed_depth2` proves the
general-`n` correspondence for arbitrary interior indices. An initial
choice-dependent filter proof was withdrawn after its use-site axiom
report exposed the dependency; the final constructive proof uses
`decide`, and all eight new T5/helper reports lie within
`{propext, Quot.sound}`.

**Status, 2026-08-26 — T6 CLOSED IN THE DECLARED CLASS.**
`LocalFiniteAlphabet.strategy_capacity_collision` consumes
`CapacityBound.capacity_bound`, and `G1Class.g1_class_exclusion` proves
the horizon-free cycle exclusion for every fixed-radius,
fixed-finite-alphabet local strategy. This is not the 15-round search.
The ceiling stated above remains exact: `OB1_UNCHANGED`.

---

## T7 — the parked-module axiom census

**Do**: enumerate the declarations of every Lean module the root does not
import, so their axiom surfaces enter the whitelist audit.

**Proves**: it would close the residual `CLAUDE.md` records as
**elaboration is not auditing** — currently 12 modules that typecheck and
emit no `#print axioms` report, any of which could depend on a
disallowed axiom with no gate failing.

**Does not prove**: that the enumerated set is the right one. A perfect
census of the wrong population is still wrong.

**Kill condition**: the obvious approach is a regex over declaration
keywords, and it is already known to break here — a documentation line
beginning with the word `theorem` has defeated a keyword count twice.
If the census cannot be built without elaborating, say so and leave the
residual open. `CLAUDE.md` states it is "left OPEN rather than closed
badly", and closing it badly would be worse than leaving it.

---

## What none of these do

None of T1–T7 derives a challenge from the object language. OB-1 stands
after all of them. The process described in `process_candidate.md`
continues past its first requirement only because a declared policy hands
it the next one, and no task on this list changes that.

Stating the boundary is the work product. Crossing it would need an
admission event this repository has not made.
