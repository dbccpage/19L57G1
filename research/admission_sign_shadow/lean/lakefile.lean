import Lake
open Lake DSL

package admission_sign_shadow

@[default_target]
lean_lib AdmissionSignShadow where
  roots := #[`AdmissionSignShadow, `AdmissionSignShadow.AxiomReport]
