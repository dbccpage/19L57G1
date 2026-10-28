import Derivation.Represented
open Represented
-- a world with a violated requirement and an empty menu: the obstruction branch
def obsW : World := { data := [10, 20], views := [], reqs := [(0, 1)], refusals := [], budget := 0, augLicensed := false, notes := [] }
example : violB obsW (0,1) = true ∧ repairFamily obsW (0,1) = [] ∧ obstructedB obsW (0,1) = true ∧ augOkB obsW [0] = true := by decide
-- budget and license are set by unguarded events: any stream can replenish
example : (step obsW (.setBudget 5)).budget = 5 ∧ (step obsW (.setAugLicense true)).augLicensed = true := by decide
-- with budget 0 / license false the addView is a no-op even though augOk holds
example : step obsW (.addView [0]) = obsW := by decide
-- refusal is recordable here (certificate present)
example : (0,1) ∈ (step obsW (.refuse 0 1)).refusals := by decide
#print axioms represented_progress
#print axioms support_determines
#print axioms wit_no_infinite
#print axioms cert_not_correspondence
#print axioms refusal_needs_certificate
