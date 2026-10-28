from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

SNIPPET = r"""
import Derivation.DiffAnchorCompat
import Derivation.FormTransportCompat
import Derivation.IsoBridgeCompat
import Derivation.IsoCanonCompat
import Derivation.IsoCollapseCompat

namespace Textbook.U74

open Derivation

-- 1. Gap 4 witness: sortPair changes an unordered pair (2, 0) to (0, 2)
theorem sortPair_unordered :
    sortPair (2, 0) = (0, 2) ∧ sortPair (2, 0) ≠ (2, 0) := by
  decide

-- 2. Gap 2 witness: rSingle and rDup have different insts list lengths (1 vs 2),
--    yet Iso.of_components constructs a concrete Minimality.Iso between them.
def rSingle : Regime where
  data := 2
  forms := [1]
  insts := [(0, [0])]
  rules := []
  reqs := [(0, 1)]

def rDup : Regime where
  data := 2
  forms := [1]
  insts := [(0, [0]), (0, [0])]
  rules := []
  reqs := [(0, 1)]

theorem rSingle_rDup_lengths_ne : rSingle.insts.length ≠ rDup.insts.length := by
  decide

def isoSingleDup : Iso rSingle rDup :=
  Iso.of_components rSingle rDup rfl rfl
    (fun i => by simp [rSingle, rDup])
    (fun f => by simp [rSingle, rDup])
    (fun q => by simp [rSingle, rDup])
    (fun q hq => by simp [rSingle] at hq; subst hq; decide)
    (fun q hq => by simp [rDup] at hq; subst hq; decide)

-- 3. Collapse transport across isoSingleDup via Iso.collapsed_transport
theorem rSingle_rDup_collapsed_iff {d e : Nat} (hd : d < 2) (he : e < 2) :
    collapsed rSingle d e ↔ collapsed rDup d e :=
  (Iso.collapsed_transport isoSingleDup hd he).symm

end Textbook.U74

#print axioms Textbook.U74.sortPair_unordered
#print axioms Textbook.U74.rSingle_rDup_lengths_ne
#print axioms Textbook.U74.isoSingleDup
#print axioms Textbook.U74.rSingle_rDup_collapsed_iff
-- Type-valued defs in IsoCollapse, IsoCanon, and IsoBridge (not emitted by ParkedAudit.isTheorem,
-- covered by ci/check_declaration_axioms.py and checked directly here):
#print axioms Derivation.Iso.symm
#print axioms Derivation.Iso.trans
#print axioms Derivation.relabel_iso
#print axioms Derivation.iso_of_relabel_eq
#print axioms Derivation.Iso.of_components
-- All 9 theorems in FormRenaming:
#print axioms Derivation.Regime.ext'
#print axioms Derivation.mapInstForm_gf
#print axioms Derivation.permForms_getD
#print axioms Derivation.permForms_length
#print axioms Derivation.renameForms_arity
#print axioms Derivation.renameForms_data
#print axioms Derivation.renameForms_forms_length
#print axioms Derivation.renameForms_gf
#print axioms Derivation.renameForms_reqs
-- All 11 theorems in FormTransport:
#print axioms Derivation.collapsed_congr
#print axioms Derivation.collapsed_renameDataForm
#print axioms Derivation.collapsed_renameForms
#print axioms Derivation.derivable_renameForms
#print axioms Derivation.mapCtxForm_f_g
#print axioms Derivation.mapInstForm_inj
#print axioms Derivation.plug_mapCtxForm
#print axioms Derivation.renameForms_forms
#print axioms Derivation.renameForms_insts
#print axioms Derivation.renameForms_rules
#print axioms Derivation.wfCtx_renameForms
-- All 10 theorems in IsoCanon:
#print axioms Derivation.mapReq_eq_sortPair
#print axioms Derivation.relabel_data
#print axioms Derivation.relabel_forms
#print axioms Derivation.relabel_insts
#print axioms Derivation.relabel_reqs
#print axioms Derivation.relabel_rules
#print axioms Derivation.sortPair_comm
#print axioms Derivation.sortPair_eq_minmax
#print axioms Derivation.sortPair_map_sortPair
#print axioms Derivation.sortPair_of_le
-- All 8 theorems in IsoCollapse:
#print axioms Derivation.Iso.collapsed_fwd
#print axioms Derivation.Iso.collapsed_transport
#print axioms Derivation.Iso.derivable_imap
#print axioms Derivation.Iso.plug_cmap
#print axioms Derivation.Iso.symm_dmap
#print axioms Derivation.Iso.wfCtx_cmap
#print axioms Derivation.map_eq_self_of_mem
#print axioms Derivation.plug_args_lt
"""

EXPECTED = {
    "Textbook.U74.sortPair_unordered": NONE,
    "Textbook.U74.rSingle_rDup_lengths_ne": NONE,
    "Textbook.U74.isoSingleDup": BOTH,
    "Textbook.U74.rSingle_rDup_collapsed_iff": BOTH,
    "Derivation.Iso.symm": BOTH,
    "Derivation.Iso.trans": BOTH,
    "Derivation.relabel_iso": BOTH,
    "Derivation.iso_of_relabel_eq": BOTH,
    "Derivation.Iso.of_components": BOTH,
    "Derivation.Regime.ext'": PROPEXT,
    "Derivation.mapInstForm_gf": NONE,
    "Derivation.permForms_getD": PROPEXT,
    "Derivation.permForms_length": BOTH,
    "Derivation.renameForms_arity": PROPEXT,
    "Derivation.renameForms_data": PROPEXT,
    "Derivation.renameForms_forms_length": BOTH,
    "Derivation.renameForms_gf": BOTH,
    "Derivation.renameForms_reqs": PROPEXT,
    "Derivation.collapsed_congr": PROPEXT,
    "Derivation.collapsed_renameDataForm": BOTH,
    "Derivation.collapsed_renameForms": BOTH,
    "Derivation.derivable_renameForms": BOTH,
    "Derivation.mapCtxForm_f_g": PROPEXT,
    "Derivation.mapInstForm_inj": PROPEXT,
    "Derivation.plug_mapCtxForm": NONE,
    "Derivation.renameForms_forms": PROPEXT,
    "Derivation.renameForms_insts": PROPEXT,
    "Derivation.renameForms_rules": PROPEXT,
    "Derivation.wfCtx_renameForms": BOTH,
    "Derivation.mapReq_eq_sortPair": PROPEXT,
    "Derivation.relabel_data": PROPEXT,
    "Derivation.relabel_forms": PROPEXT,
    "Derivation.relabel_insts": PROPEXT,
    "Derivation.relabel_reqs": PROPEXT,
    "Derivation.relabel_rules": PROPEXT,
    "Derivation.sortPair_comm": PROPEXT,
    "Derivation.sortPair_eq_minmax": PROPEXT,
    "Derivation.sortPair_map_sortPair": PROPEXT,
    "Derivation.sortPair_of_le": PROPEXT,
    "Derivation.Iso.collapsed_fwd": BOTH,
    "Derivation.Iso.collapsed_transport": BOTH,
    "Derivation.Iso.derivable_imap": BOTH,
    "Derivation.Iso.plug_cmap": BOTH,
    "Derivation.Iso.symm_dmap": BOTH,
    "Derivation.Iso.wfCtx_cmap": BOTH,
    "Derivation.map_eq_self_of_mem": PROPEXT,
    "Derivation.plug_args_lt": BOTH,
}


if __name__ == "__main__":
    raise SystemExit(main(SNIPPET, EXPECTED, "U74"))
