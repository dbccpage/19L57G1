import Lean
import Derivation.Composing
import Derivation.DiffAnchor
import Derivation.DiffAnchorCompat
import Derivation.FormRenaming
import Derivation.FormTransport
import Derivation.FormTransportCompat
import Derivation.IsoBridge
import Derivation.IsoBridgeCompat
import Derivation.IsoCanon
import Derivation.IsoCanonCompat
import Derivation.IsoCollapse
import Derivation.IsoCollapseCompat

/-!
# Parked-module axiom census

## What this closes

`lake build` builds only `defaultTargets`, so the axiom whitelist in
`ci/check_lean_audit.py` saw only what `Derivation.lean` imports.  A module
outside that import closure still elaborated -- the `lean` job builds every
module as its own Lake target -- and its forbidden tokens were still scanned,
but it emitted no axiom report.  Such a module could therefore have depended
on `Classical.choice` with every gate green.  That residual was recorded as
OPEN in `CLAUDE.md`.

This module closes it for the twelve modules outside that closure, by
importing them and emitting one axiom report per declaration, in the exact
shape `#print axioms` produces, so the existing audit reads them with no
change to the gate.

## Why this is a second root and not an import of the first

The obvious repair -- have `Derivation.lean` import the parked modules -- is
impossible for five of the twelve, and the reason is worth recording because
it is not an oversight.  `DiffAnchorCompat`, `FormTransportCompat`,
`IsoBridgeCompat`, `IsoCanonCompat`, and `IsoCollapseCompat` each begin with
`import Derivation`: they are compatibility shims stated against the whole
development, so the root importing them is a genuine cycle, and Lake rejects
it as one.  Being unimportable by the root is what "parked" MEANT for those
five.

So the audit is a second `defaultTargets` entry instead.  `lake build` builds
both roots into the same log, which is what `ci/check_lean_audit.py` and
`ci/check_axiom_report.py` read, and no cycle arises because nothing imports
this file.

## Why the declarations are not enumerated by pattern

`CLAUDE.md` records that the obvious approach is the one already known to
break here: a doc-string line beginning with the word `theorem` has twice
defeated a text-based count of theorems.  Any census built by matching source
text inherits that defect, and it fails silently -- a missed declaration looks
exactly like a module with fewer declarations.

So the population is not read out of the source at all.  It is read out of the
compiled environment: `Environment.getModuleIdx?` resolves each module, and
`ModuleData.constNames` is the list of constants that module actually added.
Lean's own record of what it compiled is the enumeration, which is why a
comment, a doc-string, or a line wrap cannot move it.

## Exact reach

Reported: every **theorem** the twelve modules declare, as Lean classifies it
(`ConstantInfo.thmInfo`), not as a pattern guesses it.

Not reported: definitions, structures, and the constructors, recursors, and
`noConfusion` helpers Lean generates alongside an inductive.  Excluding them
is what keeps this artifact the theorem inventory that
`artifacts/lean_axioms.txt` and `code/derivation/completion.py` have always
taken it to be -- every one of the 1424 reports that predate this file is a
theorem -- and it keeps a single `inductive` from adding a dozen generated
names to a pinned artifact.

The residual that leaves, stated rather than glossed: a **definition** in a
parked module could carry `Classical.choice` without being reported here.  It
is inert where it matters.  `collectAxioms` walks the whole dependency graph,
so any theorem that uses such a definition -- directly or through further
definitions -- reports the axiom and fails the audit.  What escapes is a
non-theorem declaration that no theorem reaches, which is dead code.

That the twelve modules below are EVERY module outside the root's import
closure is a separate claim, held by a separate mechanism.  The `run_cmd` at
the foot of this file checks the list against the compiled environment, which
catches a listed module that has since joined the root's closure.  It cannot
catch the opposite case: a module that nothing at all imports is absent from
the environment, so Lean has no way to notice it is missing.

`ci/check_parked_audit.py` covers that, by enumerating from the source tree
instead -- census minus the root's transitive import closure must equal the
list below.  Both halves were proved by injection; the in-Lean check stayed
green for an unimported probe module while the Python gate named it.
-/

namespace ParkedAudit

open Lean Elab Command

/-- The modules audited here: exactly those that `Derivation.lean` does not
import.  Named explicitly rather than computed, so that a module leaving the
root's import closure does not silently join this list -- the mismatch is
meant to be a visible edit. -/
def parkedModules : Array Name := #[
  `Derivation.Composing,
  `Derivation.DiffAnchor,
  `Derivation.DiffAnchorCompat,
  `Derivation.FormRenaming,
  `Derivation.FormTransport,
  `Derivation.FormTransportCompat,
  `Derivation.IsoBridge,
  `Derivation.IsoBridgeCompat,
  `Derivation.IsoCanon,
  `Derivation.IsoCanonCompat,
  `Derivation.IsoCollapse,
  `Derivation.IsoCollapseCompat
]

/-- The transitive import closure of a module, from the compiled environment.

Computed by iterating a one-step expansion once per loaded module, which
bounds the longest possible import chain.  An unbounded recursive walk would
be the natural phrasing, but the keyword that permits one is on the forbidden
list in `ci/check_lean_audit.py`, and this repository would rather carry an
explicit bound than an escape hatch.

(That list is matched as plain text over the whole file, comments included,
so this paragraph must not spell the keyword.  It was written spelling it,
and the gate failed on its own doc-string -- which is the documented hazard
working, not a surprise.) -/
def importClosure (env : Environment) (root : Name) : NameSet := Id.run do
  let mut seen : NameSet := NameSet.empty.insert root
  for _ in [0:env.header.moduleNames.size] do
    let mut next := seen
    for m in seen.toList do
      match env.getModuleIdx? m with
      | none => pure ()
      | some i =>
        for imp in env.header.moduleData[i.toNat]!.imports do
          next := next.insert imp.module
    seen := next
  return seen

/-- Every `Derivation.*` module the root does not reach, read off the
environment rather than maintained by hand.

The explicit list is still what the audit iterates, so that a module joining
or leaving the root's closure is a visible edit here rather than a silent
change in coverage; this compares the two on every build.

What it catches: a listed module that has since JOINED the root's import
closure, and a module imported at the head of this file but left out of the
list.

What it cannot catch, and the reason the completeness gate is Python: a
module that NOTHING imports -- not the root, not this file -- is absent from
the compiled environment entirely, so there is no name here to compare
against. `ci/check_parked_audit.py` enumerates from the source tree for
exactly that case. This limit is measured, not assumed: an unimported probe
module left this check green and failed the Python one. -/
def expectedParked (env : Environment) : Array Name := Id.run do
  let closure := importClosure env `Derivation
  let mut out : Array Name := #[]
  for m in env.header.moduleNames do
    if (`Derivation).isPrefixOf m && m != `Derivation && !closure.contains m then
      out := out.push m
  return out.qsort (fun a b => a.toString < b.toString)

/-- True for the injectivity and size lemmas Lean generates beside a
constructor -- `Composing.Web.mk.inj`, `.injEq`, `.sizeOf_spec`.  They are
genuine theorems, so `ConstantInfo.isTheorem` admits them, but they are not
written in the source and so have no statement for the claim inventory in
`code/derivation/completion.py` to extract.

The test is asked of the environment, not of the name: strip the last
component and check whether what remains is a CONSTRUCTOR.  A hand-written
theorem cannot be a child of a constructor, and a new generated form would be
caught by the same test without this file needing a new suffix added to a
list. -/
def isConstructorDerived (env : Environment) : Name → Bool
  | .str parent _ =>
    match env.find? parent with
    | some (.ctorInfo _) => true
    | _ => false
  | _ => false

/-- Render one axiom report in the shape `#print axioms` emits, so that
`ci/check_lean_audit.py` and `ci/check_axiom_report.py` parse it with the
patterns they already use. -/
def renderReport (declName : Name) (axioms : Array Name) : MessageData :=
  if axioms.isEmpty then
    m!"'{declName}' does not depend on any axioms"
  else
    let names := axioms.toList.map toString
    m!"'{declName}' depends on axioms: [{String.intercalate ", " names}]"

end ParkedAudit

open Lean Elab Command ParkedAudit in
run_cmd do
  let env ← getEnv
  -- The list is checked against the environment before it is used, so a
  -- module parked later cannot quietly go unaudited.
  let expected := expectedParked env
  let declared := parkedModules.qsort (fun a b => a.toString < b.toString)
  if expected != declared then
    let missing := expected.filter (fun m => !declared.contains m)
    let extra := declared.filter (fun m => !expected.contains m)
    throwError
      "parkedModules disagrees with the environment.\n\
       outside the root's import closure but NOT audited: {missing.toList}\n\
       audited but INSIDE the root's import closure: {extra.toList}\n\
       Add or remove the module in lean4/ParkedAudit.lean, then regenerate \
       artifacts/lean_axioms.txt."
  for modName in parkedModules do
    match env.getModuleIdx? modName with
    | none =>
      throwError "parked audit names a module that is not imported: {modName}"
    | some idx =>
      let data := env.header.moduleData[idx.toNat]!
      -- Theorem-hood is asked of the environment, never inferred from the
      -- name or the source text.
      let declNames := data.constNames.filter fun n =>
        !n.isInternalDetail
          && (env.find? n).any (·.isTheorem)
          && !isConstructorDerived env n
      let sorted := declNames.qsort (fun a b => a.toString < b.toString)
      for declName in sorted do
        let axioms ← liftCoreM (Lean.collectAxioms declName)
        logInfo (renderReport declName axioms)
