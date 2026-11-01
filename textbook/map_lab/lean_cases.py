"""Native-definition map instances and quotient examples; AuthorityEffect: None."""
from .run_lab import FAMILIES, TARGETS, build_packet
from .native_paths_lean import build_native_checks


def ls(values, item=str):
    return "[" + ", ".join(item(v) for v in values) + "]"


def fn(values):
    return "(fun x => (" + ls(values) + " : List Nat).getD x 0)"


def build_checks():
    packet = build_packet()
    lines = [r"""
import Derivation.ObsDescent
namespace Textbook.MapLab
open Compression DiffInterface

def checkFib (D : List Nat) (p q : Nat → Nat) : Bool :=
  D.all (fun x => D.all (fun y => decide (p x = p y → q x = q y)))

theorem checkFib_iff (D : List Nat) (p q : Nat → Nat) :
    checkFib D p q = true ↔ FiberConstant D p q := by
  unfold checkFib
  rw [List.all_eq_true]
  constructor
  · intro h x hx y hy heq
    have hxy := List.all_eq_true.mp (h x hx) y hy
    exact (of_decide_eq_true hxy) heq
  · intro h x hx
    apply List.all_eq_true.mpr
    intro y hy
    exact decide_eq_true (h x hx y hy)

def checkLookup (D : List Nat) (p q g : Nat → Nat) : Bool :=
  D.all (fun x => decide (g (p x) = q x))

theorem lookup_supplies_factor (D : List Nat) (p q g : Nat → Nat)
    (h : checkLookup D p q g = true) : FactorsOn D p q := by
  refine ⟨g, ?_⟩
  simpa [checkLookup, List.all_eq_true] using h

theorem factor_chain (D : List Nat) (p q r : Nat → Nat)
    (hpq : FactorsOn D p q) (hqr : FactorsOn D q r) : FactorsOn D p r := by
  rcases hpq with ⟨g, hg⟩
  rcases hqr with ⟨h, hh⟩
  exact ⟨fun x => h (g x), fun x hx => (congrArg h (hg x hx)).trans (hh x hx)⟩
"""]
    names = ["Textbook.MapLab." + n for n in ("checkFib_iff", "lookup_supplies_factor", "factor_chain")]
    for mask in range(16):
        for family in range(4):
            for reverse in (0, 1):
                key = f"{mask}_{family}_0_{reverse}"
                row = packet["cases"][key]
                ident = f"{mask}_{family}_{reverse}"
                d, qfamily, p = "d"+ident, "q"+ident, "p"+ident
                lines += [f"def {d} : List Nat := {ls(row['domain'])}",
                          f"def {qfamily} : List (Nat → Nat) := {ls(FAMILIES[family], fn)}",
                          f"def {p} : Nat → Nat := {fn(row['presentation'])}"]
                parts = [f"{d}.map (pQ {d} {qfamily}) = {ls(row['aligned_representatives'])}",
                         f"{d}.map (sigList {qfamily}) = {ls(row['signatures'], ls)}",
                         f"classCount {d} {qfamily} = {row['class_count']}"]
                factors = []
                for target, q in enumerate(TARGETS):
                    result = packet["cases"][f"{mask}_{family}_{target}_{reverse}"]
                    truth = str(result["recoverable"]).lower()
                    parts.append(f"checkFib {d} {p} {fn(q)} = {truth}")
                    factors.append(f"(FactorsOn {d} {p} {fn(q)} ↔ ({truth} = true))")
                    if result["recoverable"]:
                        g = result["full_lookup_examples"][0]
                        parts.append(f"checkLookup {d} {p} {fn(q)} {fn(g)} = true")
                n = "representation_" + ident
                lines.append("theorem " + n + " :\n  " + " ∧\n  ".join(parts) + " := by decide")
                names.append("Textbook.MapLab." + n)
                n = "factorization_" + ident
                lines.append("theorem " + n + " :\n  " + " ∧\n  ".join(factors) + r""" := by
  simp only [factors_iff_fiberConstant, ← checkFib_iff] <;> decide
""")
                names.append("Textbook.MapLab." + n)
    lines.append(r"""
def blue4 (x : Fin 4) : Nat := ([1, 1, 0, 0] : List Nat).getD x.val 0
def triangle4 (x : Fin 4) : Nat := ([0, 1, 1, 0] : List Nat).getD x.val 0
def blueObserver := kernelObs blue4

theorem blue_class_constant : ObsDescent.ClassConstant blueObserver blue4 :=
  fun _ _ h => h

theorem blue_descends :
    ∃ F : ObsQuotient blueObserver → Nat,
      ∀ x, F (ObsQuotient.mk blueObserver x) = blue4 x :=
  (ObsDescent.descend_exists_iff blueObserver blue4).mpr blue_class_constant

theorem triangle_not_class_constant :
    ¬ ObsDescent.ClassConstant blueObserver triangle4 := by
  intro h
  have bad := h (0 : Fin 4) (1 : Fin 4) rfl
  change (0 : Nat) = 1 at bad
  exact Nat.noConfusion bad

theorem triangle_does_not_descend :
    ¬ ∃ F : ObsQuotient blueObserver → Nat,
      ∀ x, F (ObsQuotient.mk blueObserver x) = triangle4 x :=
  ObsDescent.descend_blocked_of_witness blueObserver triangle4
    (x := (0 : Fin 4)) (y := (1 : Fin 4)) rfl (by decide)

theorem pair_not_class_constant :
    ¬ ObsDescent.ClassConstant blueObserver (fun x => (blue4 x, triangle4 x)) := by
  intro h
  have bad := congrArg Prod.snd (h (0 : Fin 4) (1 : Fin 4) rfl)
  change (0 : Nat) = 1 at bad
  exact Nat.noConfusion bad

end Textbook.MapLab
""")
    names += ["Textbook.MapLab."+n for n in ("blue_class_constant", "blue_descends", "triangle_not_class_constant",
                                           "triangle_does_not_descend", "pair_not_class_constant")]
    native = ["Compression.factor_unique_on_image", "Compression.factor_not_unique_off_image",
              "ObsDescent.classConstant_pair_iff", "ObsDescent.descend_unique",
              "ObsDescent.descend_iff_factorsOn_all", "ObsDescent.fiberConstant_fixed_D_not_classConstant"]
    names += native
    lines += ["#print axioms " + n for n in names]
    native_source, native_names = build_native_checks()
    return "import Derivation.TraceAlgebra\nimport Derivation.ObsDescent\n" + native_source + "\n\n" + "\n\n".join(lines).replace('import Derivation.ObsDescent', '') + "\n", names + list(native_names)
