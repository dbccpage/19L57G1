/-
Axiom reports for the theorems of `research/limit_and_observer`.

The build log is compared byte for byte against `receipts/lean_axioms.txt` by
`verify_lean.py`.  Every report must lie within `{propext, Quot.sound}`.

This receipt is MANUAL: no CI gate runs this package's `verify_lean.py`.

## Why this is a census and not a hand-written list

It was a hand-written list of seventeen `#print axioms` lines, headed "every
exported theorem".  That heading was **false**: `separatesAt_eq_readsAt` had
no line, and nothing anywhere checked the population, so a theorem could be
added and go unaudited with every gate green.  That is the same shape of
overclaim `CLAUDE.md` withdrew for the sealed audit, and the wording is
withdrawn here for the same reason.

The population is now read out of the compiled environment rather than
maintained by hand: `Environment.getModuleIdx?` resolves the module and
`ModuleData.constNames` is what that module actually added.  A report is
emitted for each, in the exact shape `#print axioms` produces, so
`verify_lean.py` parses them with the pattern it already uses.  A theorem
added to `LimitObserver` therefore changes the receipt and fails the
comparison until the receipt is regenerated deliberately.

Reading the source text instead would inherit a defect `CLAUDE.md` already
records: a doc-string line beginning with the word `theorem` has twice
defeated a text-based count in this repository, and it fails silently.

## Exact reach

Reported: every **theorem** the module `LimitObserver` declares, as Lean
classifies it, with Lean's internal names skipped.  That includes the
equation lemmas Lean generates beside a recursive definition —
`diffCount.eq_def` and `signature.eq_def` are in the receipt and were written
by nobody.  They are kept rather than filtered: a rule broad enough to drop
them is broad enough to swallow a hand-written theorem, which is the exact
failure this census exists to prevent, and the sealed tree recorded that
hazard after hitting it.

Not reported: definitions.  `sealedDerivable`, `admissionOnly`, `separatesAt`,
`signature`, `diffCount`, `novel`, `readsAt`, `behaviour` and `blockCount` are
definitions and emit nothing.  A definition carrying a disallowed axiom would
escape this census; anything a *theorem* reaches is caught, because
`collectAxioms` walks the whole dependency graph.

Not reported either: this file's own declarations, since the census runs over
`LimitObserver` and this module is `LimitObserver.AxiomReport`.  It declares
no mathematics, and the point of saying so is that "every theorem of this
package is audited" stays false with this module as its witness.

A module that **nothing imports** would be absent from the environment
entirely and so invisible here — the sealed tree measured exactly that and put
its completeness gate in Python for it.  `verify_lean.py` does the same for
this package: it computes the import closure of this file from the source
tree and refuses a module outside it. It additionally refuses new library
modules until the explicit theorem census is extended to cover them.
Each theorem emits an independent LIMIT_OBSERVER_DECL marker; the verifier
requires exact agreement between those markers and parsed axiom reports.
-/
import LimitObserver
import Lean.Elab.Command
import Lean.Util.CollectAxioms

namespace LimitObserver.AxiomReport

open Lean Elab Command

/-- Render one axiom report in the shape `#print axioms` emits, so that
`verify_lean.py` reads it with the pattern it already uses. -/
def renderReport (declName : Name) (axioms : Array Name) : MessageData :=
  if axioms.isEmpty then
    m!"'{declName}' does not depend on any axioms"
  else
    let names := axioms.toList.map toString
    m!"'{declName}' depends on axioms: [{String.intercalate ", " names}]"

end LimitObserver.AxiomReport

open Lean Elab Command LimitObserver.AxiomReport in
run_cmd do
  let env ← getEnv
  -- Resolution first: a census over a module the environment does not hold
  -- would report nothing and look exactly like a module with no theorems.
  match env.getModuleIdx? `LimitObserver with
  | none =>
      throwError
        "the axiom census cannot resolve LimitObserver; the census would be \
         silently empty"
  | some idx =>
      let data := env.header.moduleData[idx.toNat]!
      -- Theorem-hood is asked of the environment, never inferred from the
      -- name or from the source text.
      let declNames := data.constNames.filter fun n =>
        !n.isInternalDetail && (env.find? n).any (·.isTheorem)
      if declNames.isEmpty then
        throwError
          "the axiom census found no theorem in LimitObserver; an empty \
           census proves nothing and is refused"
      let sorted := declNames.qsort (fun a b => a.toString < b.toString)
      for declName in sorted do
        logInfo m!"LIMIT_OBSERVER_DECL {declName}"
        let axioms ← liftCoreM (Lean.collectAxioms declName)
        logInfo (renderReport declName axioms)
