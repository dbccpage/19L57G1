import Derivation.EndogenousFidelityGenerator
import Derivation.NoOutsideFidelity
import Derivation.DiffAnchor
open PresentationDescent FidelityClosure EndogenousFidelityGenerator
#print axioms FidelityClosure.holonomy_residual_refuses_faithful_network_descent
#print axioms EndogenousFidelityGenerator.generated_structure_is_failed_erasure
#print axioms NoOutsideFidelity.no_support_inverse_faithfully_erases_index
#print axioms DiffAnchor.colObs_deltaConstant
#check TranslationNetwork            -- universe level of the network structure
#check FaithfulNetworkDescent
-- A two-index network with one coherent step (identity on Bool): indices 0,1 become fidelity-related.
def twoNet : TranslationNetwork where
  Index := Bool
  Carrier := fun _ => Bool
  Attempt := fun i j => PLift (i = false ∧ j = true)
  pair := fun _ => ⟨fun b => some b, fun b => some b⟩
def twoTot : Totalization (twoNet.pair (i := false) (j := true) ⟨⟨rfl, rfl⟩⟩) :=
  ⟨id, id, fun _ => rfl, fun _ => rfl⟩
example : FidelityRel twoNet false true :=
  ⟨FidelityPath.step (N := twoNet) ⟨⟨rfl, rfl⟩⟩ twoTot ⟨fun _ => rfl, fun _ => rfl⟩⟩
-- A network with NO attempts: NoCoherentPath between distinct indices holds.
def emptyNet : TranslationNetwork :=
  { Index := Bool, Carrier := fun _ => Unit, Attempt := fun _ _ => Empty, pair := fun e => Empty.elim e }
theorem emptyNet_key : ∀ {i j : Bool}, FidelityPath emptyNet i j → i = j
  | _, _, .refl _ => rfl
  | _, _, .step a _ _ => Empty.elim a
  | _, _, .symm p => (emptyNet_key p).symm
  | _, _, .trans p q => (emptyNet_key p).trans (emptyNet_key q)
theorem emptyNet_no_path : NoCoherentPath emptyNet false true :=
  fun ⟨p⟩ => Bool.noConfusion (emptyNet_key p)
#eval PrimitivePassage.zeroP [] 0 1
#eval PrimitivePassage.zeroP [[0]] 0 1
#eval PrimitivePassage.zeroP [[0,1]] 0 1
