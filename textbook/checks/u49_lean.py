"""Unit 49 check: kernel-check the book's Lean for Unit 49.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u49_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Initiality

namespace Textbook.U49
open Represented Constitution Initiality

def storyH : List Event :=
  [.setBudget 9, .admitTok 10, .admitTok 20, .admitTok 30,
   .require 0 1, .require 0 2, .require 1 2, .addView [0]]

/-- The probes are the sealed step's own no-ops on the four probe worlds. -/
theorem probes_are_step_noops :
    step dupWorld (.admitTok 5) = dupWorld ∧ step dupWorld (.require 0 0) = dupWorld ∧
    step satWorld (.mark [0] 1) = satWorld ∧ step brokeWorld (.mark [] 0) = brokeWorld ∧
    step unlicensedWorld (.addView [0]) = unlicensedWorld ∧
    step satWorld (.refuse 0 1) = satWorld := by decide

theorem kernel_compliant : compliantB kernelDesc = true := by decide

/-- What each guard, switched off, does on its probe world. -/
theorem off_outcomes :
    (interpStep { kernelDesc with dedupAdmit := false } dupWorld (.admitTok 5)).data = [5, 5] ∧
    (interpStep { kernelDesc with guardRequire := false } dupWorld (.require 0 0)).reqs = [(0, 0)] ∧
    (interpStep { kernelDesc with guardAccept := false } satWorld (.mark [0] 1)).views = [[1, 0]] ∧
    (interpStep { kernelDesc with gateBudget := false } brokeWorld (.mark [] 0)).views = [[0]] ∧
    (interpStep { kernelDesc with gateBudget := false } brokeWorld (.mark [] 0)).budget = 0 ∧
    (interpStep { kernelDesc with gateLicense := false } unlicensedWorld (.addView [0])).views =
      [[], [0]] ∧
    (interpStep { kernelDesc with certRefusal := false } satWorld (.refuse 0 1)).refusals =
      [(0, 1)] := by decide

/-- The accept guard off breaks a satisfied requirement on the probe world:
the probe is an instance of preservation. -/
theorem accept_off_breaks :
    satB satWorld (0, 1) = true ∧
    satB (interpStep { kernelDesc with guardAccept := false } satWorld (.mark [0] 1)) (0, 1) =
      false := by decide

/-- Switching one guard off fails its own probe and no other. -/
theorem accept_off_passes_others :
    probeDedup { kernelDesc with guardAccept := false } = true ∧
    probeRequire { kernelDesc with guardAccept := false } = true ∧
    probeBudget { kernelDesc with guardAccept := false } = true ∧
    probeLicense { kernelDesc with guardAccept := false } = true ∧
    probeRefusal { kernelDesc with guardAccept := false } = true := by decide

/-- Two guards off: non-compliant, by the theorem rather than by the probes. -/
theorem two_off_not_compliant :
    (⟨true, true, true, false, true, false⟩ : ConstitutionDesc) ∉ allDescs.filter compliantB := by
  intro h
  have := minimum_unique_in_class _ h
  exact absurd this (by decide)

theorem compliant_count : (allDescs.filter compliantB).length = 1 := by
  rw [unique_compliant]
  rfl

/-- A cost order, defined here (Lean (book)): Genesis defines none in Lean.
On the compliant set it is constant, so every order agrees. -/
def costCap (d : ConstitutionDesc) : Nat :=
  (if d.dedupAdmit then 1 else 0) + (if d.guardRequire then 1 else 0) +
  (if d.guardAccept then 1 else 0) + (if d.gateBudget then 1 else 0) +
  (if d.gateLicense then 1 else 0) + (if d.certRefusal then 1 else 0)

theorem cost_values :
    costCap kernelDesc = 6 ∧ costCap ⟨false, false, false, false, false, false⟩ = 0 ∧
    costCap { kernelDesc with gateBudget := false } = 5 := by decide

theorem cost_constant_on_compliant :
    ∀ d ∈ allDescs.filter compliantB, costCap d = 6 := by
  intro d hd
  rw [minimum_unique_in_class d hd]
  rfl

/-- The retract on the story: base events through the panel kernel land
on the story, with the panel untouched. -/
theorem retract_on_story :
    (NoOutside.replayC (storyH.map .base) ⟨genesis, [[[0]]]⟩).base = replay storyH genesis :=
  extension_retract_replay storyH _

theorem retract_keeps_panel :
    (NoOutside.replayC (storyH.map .base) ⟨genesis, [[[0]]]⟩).panel = [[[0]]] := by decide

theorem section_instance : (NoOutside.CWorld.mk (replay storyH genesis) []).base =
    replay storyH genesis := retract_section _

end Textbook.U49

#print axioms Textbook.U49.probes_are_step_noops
#print axioms Textbook.U49.kernel_compliant
#print axioms Textbook.U49.off_outcomes
#print axioms Textbook.U49.accept_off_breaks
#print axioms Textbook.U49.accept_off_passes_others
#print axioms Textbook.U49.two_off_not_compliant
#print axioms Textbook.U49.compliant_count
#print axioms Textbook.U49.cost_values
#print axioms Textbook.U49.cost_constant_on_compliant
#print axioms Textbook.U49.retract_on_story
#print axioms Textbook.U49.retract_keeps_panel
#print axioms Textbook.U49.section_instance
#print axioms Initiality.dedup_load_bearing
#print axioms Initiality.require_guard_load_bearing
#print axioms Initiality.accept_guard_load_bearing
#print axioms Initiality.budget_gate_load_bearing
#print axioms Initiality.license_gate_load_bearing
#print axioms Initiality.refusal_certificate_load_bearing
#print axioms Initiality.unique_compliant
#print axioms Initiality.minimum_unique_in_class
#print axioms Initiality.extension_retract_replay
#print axioms Initiality.retract_section
"""

EXPECTED = {
    "Textbook.U49.probes_are_step_noops": BOTH,
    "Textbook.U49.kernel_compliant": BOTH,
    "Textbook.U49.off_outcomes": BOTH,
    "Textbook.U49.accept_off_breaks": BOTH,
    "Textbook.U49.accept_off_passes_others": BOTH,
    "Textbook.U49.two_off_not_compliant": BOTH,
    "Textbook.U49.compliant_count": BOTH,
    "Textbook.U49.cost_values": NONE,
    "Textbook.U49.cost_constant_on_compliant": BOTH,
    "Textbook.U49.retract_on_story": BOTH,
    "Textbook.U49.retract_keeps_panel": BOTH,
    "Textbook.U49.section_instance": BOTH,
    "Initiality.dedup_load_bearing": BOTH,
    "Initiality.require_guard_load_bearing": BOTH,
    "Initiality.accept_guard_load_bearing": BOTH,
    "Initiality.budget_gate_load_bearing": BOTH,
    "Initiality.license_gate_load_bearing": BOTH,
    "Initiality.refusal_certificate_load_bearing": BOTH,
    "Initiality.unique_compliant": BOTH,
    "Initiality.minimum_unique_in_class": BOTH,
    "Initiality.extension_retract_replay": BOTH,
    "Initiality.retract_section": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U49"))
