# The portable interface

An **export surface**: the objects this repository constructs that are
stable enough to be imported elsewhere, each pinned to the source it was
written against and each carrying its own honest scope.

## What this tree is, and the rule that makes it work

This is one half of a one-way bridge. It names only declarations this
repository builds, in this repository's own vocabulary. **Nothing
external is named here, and nothing external may be added.**

That rule is not decoration and it is not inherited politeness. It is
what makes the bridge a bridge rather than a merge. If a name from
another system enters this file, the direction collapses: the importing
system's carving starts steering the exporting system's exposition, and
the exporting side loses the ability to say which of its results are
structure and which are vocabulary. This repository has already paid
that cost once, through a supplied station vocabulary that reached its
prose but not its mathematics. The second time would not be so cheap.

Translation is therefore the **importer's** job, done on the importer's
side. This file is the thing being translated, not the translation.

## Verifying it

```powershell
python research/portable_interface/verify_pins.py
```

Two checks, and neither implies the other:

- every pinned module still hashes to its recorded SHA-256, so this file
  describes the sources it was written against;
- every exported name is actually declared in the module it is
  attributed to, so this file cannot cite a theorem that does not exist
  or has been renamed.

A hash pin proves the source did not move. It does **not** prove this
document names anything real. That is why the second check exists.

`--repin` rewrites the hashes from `HEAD` and verifies nothing; after a
repin, this document must be re-read by hand, because a moved source can
change what its declarations mean without changing whether they exist.

**Run by CI, with one exception.** The `research` job runs this pin
check, this tree's tests, and its strict typing on every pull request and
push to `main`. An earlier version of this paragraph said the tree was not
run by CI and was a purely manual receipt like its sibling; that was true
when written and is **WITHDRAWN** — the job landed in pull request #79,
after both research trees were left silently broken on `main` by two
pull requests that no gate read.

The exception is Lean. No job builds the sealed package on this tree's
behalf, so the axiom claims below remain a manual receipt and go stale
silently. That is the same residual the sibling tree records, and it is
not closed here.

## The exports

Twenty-six declarations across three pinned modules. Grouped by what
they do.

### The difference interface

| name | kind | what it is |
|---|---|---|
| `DiffObs` | STRUCTURE | An observer: a `delta` into a result type, a `Zero` predicate on results, and three laws — `zero_refl`, `zero_symm`, `zero_trans`. |
| `ZeroRel` | DEFINITION | `ZeroRel O x y` iff the observer's difference value is zero. |
| `zeroRel_equivalence` | THEOREM | The zero relation of any observer is an equivalence. |
| `ObsQuotient` | DEFINITION | The quotient by that relation. |
| `obsQuotient_eq_of_zero` | THEOREM | The quotient identifies exactly the zero pairs (soundness half). |

The transferable part is not the quotient — it is the **ordering**. The
equivalence is proved *before* the quotient is constructed, and the
quotient's definition depends on that proof, so the discipline is
enforced by the dependency graph rather than by anyone remembering it.
An importer that builds the quotient first has not imported this.

### The stage and its obstruction

| name | kind | what it is |
|---|---|---|
| `Stage` | STRUCTURE | Four **independent** fields: `live`, `retained`, `guarded`, `obs`. No coherence between them is assumed. |
| `ActiveObstruction` | DEFINITION | Exactly the conjunction `retained x y ∧ ZeroRel obs x y ∧ guarded x y`. |

Note `guarded`, not "protected" — the latter is a reserved word, and the
field has carried the native name from the start.

### The gate factorization

| name | kind | what it is |
|---|---|---|
| `obstP_factors` | THEOREM | The obstruction equals the conjunction of four total gates: retained, protected, observation declared, observer-zero on the pair. |
| `gate_zero_independent` | THEOREM | Countermodel: the zero gate does not follow from the other three. |
| `gate_declared_independent` | THEOREM | Countermodel: nor does the declared gate. |
| `gate_protection_independent` | THEOREM | Countermodel: nor does protection. |
| `gate_retention_independent` | THEOREM | Countermodel: nor does retention. |
| `obst_requires_observation` | THEOREM | Pre-observational states obstruct nothing, whatever is retained and protected. |

**This is the sharpest thing in the surface, and it is easy to import
wrongly.** `obstP_factors` alone is near-definitional — the gates are
defined so that it holds, and any Boolean splits as `true && c`. What
makes the four-way reading non-trivial is the four independence
theorems. Import the factorization without them and you have imported a
tautology wearing a result's clothes.

### The response rule

| name | kind | what it is |
|---|---|---|
| `two_rule` | THEOREM | Under its hypotheses: either the same-level repair family is nonempty, or it is empty and the extension-proposal family is nonempty. |
| `extension_always_available` | THEOREM | The extension family is provably nonempty where the rule needs it. |
| `extension_resolves` | THEOREM | The executed response kills the obstruction on re-evaluation. |

`two_rule` is **conditional**, on four hypotheses: the obstruction holds,
the two points are distinct, the first is in range, and the pair is
protected. It is not an unconditional dichotomy and must not be cited as
one. Refusal and the terminal are separately typed records, members of
neither family.

### Replay

| name | kind | what it is |
|---|---|---|
| `replay_deterministic` | THEOREM | Equal histories replay to equal states. |
| `replay_append` | THEOREM | Replay respects concatenation of histories. |

State is a function of represented history. This is what makes any
result here re-derivable from genesis rather than asserted.

### The equivariance obstruction

| name | kind | what it is |
|---|---|---|
| `Symmetry` | STRUCTURE | A carrier, a type of symbols, an action, and one field: **no point is fixed by every symbol**. No involution law, no group law, no identity, no inverses, no composition. |
| `no_selector_of_no_common_fixed_point` | THEOREM | The obstruction under the weakest premise it spends: no point fixed by every symbol. Stated over a bare action, not over `Symmetry`. |
| `no_common_fixed_point` | THEOREM | `Symmetry`'s field implies that premise. One direction only. |
| `no_orbit_constant_equivariant_selector` | THEOREM | Given an inhabitant, no selector is both orbit-constant and equivariant. A corollary of the two above. |
| `no_orbit_constant_equivariant_endomap` | THEOREM | The single-involution case, subsumed via `ofBreak`. |
| `no_fixed_point_free_involution_on_Tri` | THEOREM | No fixed-point-free involution exists on a three-point carrier. |
| `selector_exists_at_common_fixed_point` | THEOREM | Where a point IS fixed by every symbol, the constant selector at it is both — so the hypothesis is spent, not decorative. |
| `selector_iff_common_fixed_point` | THEOREM | **Exact characterization**: given an inhabitant, such a selector exists precisely when some point is fixed by every symbol. |

All **seven theorems** report *does not depend on any axioms* — not
`propext`, not `Quot.sound`. `Symmetry` is a structure and has no axiom
report; an earlier version of this paragraph said "all five report no
axiom dependency", counting the structure among the reports. That count
is **WITHDRAWN**: structures are not reported, and the number was wrong
besides.

The proof is two equations composed: orbit-constancy says the value does
not move when the argument does, equivariance says it moves exactly as
the argument does, and together they say it does not move at all.

**Import the characterization, not the field.** `Symmetry.no_common_fixed`
is *sufficient* for the obstruction but stronger than the argument spends
— `no_selector_of_no_common_fixed_point` needs only that no point is
fixed by every symbol, and `selector_iff_common_fixed_point` shows that
condition is exactly right in both directions. An earlier version of this
file, and the paper, described the field as "exactly what the obstruction
costs". That was wrong and is WITHDRAWN. An importer that reproduces the
field will have imported a hypothesis it does not need; the converse
direction is not constructively available, so the difference is real and
not a matter of presentation.

`no_fixed_point_free_involution_on_Tri` is why the general form is not
cosmetic: `Break` cannot be instantiated over a three-point carrier at
all, while `Symmetry` can. An earlier version explained this by the
general fact that a fixed-point-free involution pairs its carrier into
two-cycles, so a finite single-involution carrier has **even**
cardinality. That statement is **not proved** in the exporting
repository, is WITHDRAWN here, and must not be imported. Only the
three-point case is a theorem.

**The scope, which is the part most likely to be misread.** This says
that where a symmetry has no common fixed point, a selector cannot be
both blind to the symmetry and compatible with it. It does **not** say
that ties in this development are unbreakable. In this repository the
tied minimal responses are separated by an isomorphism invariant, and an
invariant measure already selects among them uniquely; the obstruction
bites *within* a tie class, where two concrete presentations are
exchanged by a transposition, not *across* classes. An importer that
carries this over as "choice can never be derived" will have imported
something the exporting side disproves.

## What an importer must NOT assume

This section is the reason the file exists. Everything above is only
safe to use with it.

- **`obstP_factors` is not a uniqueness claim.** It does not say the
  decomposition is the only one, and it does not say the four gates are
  jointly free — `obs_gates_not_both_false` refutes the latter.
- **The four independence theorems are countermodels, not a basis
  theorem.** They show no gate follows from the other three. They do not
  show the four are in any sense canonical or minimal.
- **`two_rule` is conditional.** See its hypotheses above.
- **`Stage`'s four fields are independent by construction, not by
  proof.** Nothing here says a coherent stage is impossible; the point
  is that coherence is never assumed.
- **The axioms of this tree are unchecked.** `verify_pins.py` does not
  build Lean. The sealed modules' `#print axioms` reports are audited by
  the sealed workflow, within `{propext, Quot.sound}` — but that audit
  covers the enumerated inventory, not this file's selection from it.
- **Nothing here is a claim about any system outside this repository.**
  A correspondence between one of these objects and an object elsewhere
  is a claim the importer makes and must justify on its own side. This
  file supplies no such correspondence and licenses none.

## Provenance

The station vocabulary of the passage these objects sit in was supplied,
not derived — see `paper/primitive_difference_passage.md`, which records
the supply and keeps the supplied labels separate from the native ones.
Of sixteen supplied names, two were ever Lean identifiers. Both appear
in this surface: `ZeroRel`, already classified native-or-core, and
`ActiveObstruction`, definitionally a conjunction of three native
`Stage` fields. Neither is load-bearing *as a name*, which is why they
export cleanly.
