# Audit: Initiality

| field | value |
|---|---|
| Path | lean4/Derivation/Initiality.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | ab1c1ebd328f2c70 |
| Lines | 171 |
| Imported by root `Derivation.lean` | yes (line 27) |
| Imports | Derivation.Constitution, Derivation.NoOutside |
| Declarations | 11 def (4 probe worlds, 6 probes, compliantB), 11 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 11 lines; axioms seen: none / propext, Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

Stage VII asks in what sense the sealed kernel is the "most primitive" engine, and answers only inside a declared, finite comparison class: the 64 descriptors of `Constitution.ConstitutionDesc`, each run by the fixed family interpreter `interpStep`. Compliance is a declared six-probe battery, one Boolean probe per guard, each a single concrete world and event on which the sealed kernel is known (by `interp_describe` and the sealed theorems) to be a no-op. The module proves that switching off any one guard fails its probe (six load-bearing separations), that the kernel's descriptor is the unique compliant member of the 64 (`unique_compliant`, by `decide`), hence the unique minimum under any cost order on the compliant set, and that the panel extension of `NoOutside` projects back onto the kernel along every base event and history (a split retract). The header states the scope exactly: class-relative and battery-relative; categorical initiality is not claimed.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| dupWorld | 52 | def | data [5], nothing else | ADMITTED (probe world) |
| satWorld | 56 | def | two data, view [0], requirement (0,1) satisfied, budget 9 | ADMITTED |
| brokeWorld | 60 | def | two data, view [], requirement (0,1), budget 0 | ADMITTED |
| unlicensedWorld | 64 | def | as brokeWorld but budget 9 and license false | ADMITTED |
| probeDedup | 70 | def | re-admitting 5 to dupWorld is a no-op | ADMITTED (declared probe) |
| probeRequire | 73 | def | `require 0 0` on dupWorld is a no-op | ADMITTED |
| probeAccept | 76 | def | `mark [0] 1` on satWorld is a no-op | ADMITTED |
| probeBudget | 79 | def | `mark [] 0` on brokeWorld is a no-op | ADMITTED |
| probeLicense | 82 | def | `addView [0]` on unlicensedWorld is a no-op | ADMITTED |
| probeRefusal | 85 | def | `refuse 0 1` on satWorld is a no-op | ADMITTED |
| compliantB | 88 | def | conjunction of the six probes | ADMITTED (declared battery) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| dedup_load_bearing | 99 | kernelDesc passes probeDedup; with dedupAdmit off it fails | VERIFIED_FINITE / REFUTED (refutes "dedup is redundant") | propext, Quot.sound | S |
| require_guard_load_bearing | 103 | same for guardRequire / probeRequire | VERIFIED_FINITE / REFUTED | propext, Quot.sound | S |
| accept_guard_load_bearing | 107 | same for guardAccept / probeAccept | VERIFIED_FINITE / REFUTED | propext, Quot.sound | S |
| budget_gate_load_bearing | 111 | same for gateBudget / probeBudget | VERIFIED_FINITE / REFUTED | propext, Quot.sound | S |
| license_gate_load_bearing | 115 | same for gateLicense / probeLicense | VERIFIED_FINITE / REFUTED | propext, Quot.sound | S |
| refusal_certificate_load_bearing | 119 | same for certRefusal / probeRefusal | VERIFIED_FINITE / REFUTED | propext, Quot.sound | S |
| unique_compliant | 128 | allDescs.filter compliantB = [kernelDesc] | VERIFIED_FINITE (64 descriptors × 6 probes, decide) | propext, Quot.sound | S |
| minimum_unique_in_class | 136 | every compliant descriptor equals kernelDesc | VERIFIED_FINITE (corollary) | propext, Quot.sound | A |
| extension_retract | 154 | (stepC cw (base e)).base = step cw.base e (rfl) | FROZEN (definitional) | propext, Quot.sound | S |
| extension_retract_replay | 157 | (replayC (h.map base) cw).base = replay h cw.base | FROZEN | propext, Quot.sound | S |
| retract_section | 168 | (CWorld.mk w []).base = w (rfl) | FROZEN (definitional) | none | A |

Count check: 11 theorems, all in the artifact.

## 4. External and admitted assumptions

- The comparison class (64 descriptors), the interpreter `interpStep`, the four probe worlds, the six probes and `compliantB` are all declared. Each probe is one world and one event; "compliance" means passing exactly these six no-op tests.
- Cost orders: none is defined in Lean. `minimum_unique_in_class` says only that the compliant set is a singleton; the docstring says the two orders (enabled-guard count; lexicographic) are "computed and compared in the Python mirror". So "minimum under both declared cost orders" is a Lean statement about a singleton plus a Python computation of the orders. Flag: cost function without Lean justification — but the conclusion does not depend on which order is used, so nothing is lost.
- Library: `decide` over `World` and `ConstitutionDesc` (BEq from `DecidableEq`), `List.filter`, structural recursion.
- Unearned identity: none. Unrestricted external universe: none. Unbounded function treated as internally available: none (all finite). Silently assumed observer: none; the probes are explicit. Unspecified correspondence between presentations: `extension_retract` is a projection on `CWorld`, declared. Admitted condition later described as forced: the probe battery is declared, and the paper says "declared" throughout; however see §11 on "load-bearing". Finite computation presented as universal: the "unique compliant" claim is finite (64 members) and is presented as class-relative; the terminal was renamed from INITIAL_KERNEL_PROVED to UNIQUE_PROBE_COMPLIANT_DESCRIPTOR_IN_DECLARED_TOGGLE_CLASS (`pr11_correction_ledger.md` C8).

## 5. Derived consequences

Not imported by any later Derivation module except `Horizon.lean` (which imports Initiality for its transitive closure but uses only Represented and Constitution names). Ledger CL-NC-INITIALITY; map row none directly (the "most primitive engine" question is answered in prose, §12 of `native_derivation_completion.md`).

## 6. Counterexamples and limitations

- The six `*_load_bearing` theorems are countermodels: each exhibits one descriptor (kernelDesc with one toggle off) and one probe that distinguishes it from the kernel.
- Not proved: categorical initiality (stated); minimality in any wider class; that the probe battery characterises the sealed theorems (each probe is one instance of a theorem's property, calibrated so that the kernel passes); that `extension_retract` is more than a projection equation (it is `rfl`, since `stepC` is defined componentwise); anything about descriptors that pass five of six probes being "closer" to the kernel.
- "Load-bearing" here means: switching the guard off changes the outcome on one specific probe world. It does not mean the guard is needed for any sealed theorem; the relation between probes and theorems is calibration by the author.

## 7. Axiom dependencies

All 11 within {propext, Quot.sound}; `retract_section` uses none. Theorems exceeding the set: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 11 theorems in the artifact and cited in CL-NC-INITIALITY. No probe run; `decide` theorems are kernel-checked by the build.

## 9. Related Python implementations

`code/derivation/completion.py`: `probe_results`, `compliant`, `cost_capabilities`, `cost_lex`, `minimality_report` (the 64-member compliance table and the two cost orders), artifact `completion_minimality.json`. Tests: `tests/test_completion.py::test_each_guard_is_load_bearing`, `test_unique_compliant_kernel_and_orders_agree`.

## 10. Textbook placement proposal

- Prerequisites: `ConstitutionDesc`, `interpStep`, `interp_describe`; the `CWorld` extension of NoOutside; what a probe (one world, one event, expected no-op) is.
- Substantive: the six separations (as one lesson: each guard does something), `unique_compliant`, the scope statement; `extension_retract_replay` as the conservative-extension fact.
- Auxiliary: the probe worlds and probe definitions, `minimum_unique_in_class`, `extension_retract`, `retract_section`.
- Lesson title: "Minimal among what? A six-probe singleton in a 64-member class." The one question: in what exact sense is the kernel the unique compliant engine, and what would it take to say more?
- Omit: `retract_section` and `extension_retract` as separate items (both `rfl`; mention in one sentence).

## 11. Interpretation findings

1. Header lines 25–26 "each guard is load-bearing — switching any one off violates its probe (six separation theorems, each a concrete countermodel)". Faithful: the Lean says exactly "violates its probe". But the module header's framing ("each probing the property the sealed kernel proves as a theorem") invites the reading that the guard is necessary for the theorem. The probes are single instances chosen by the author so that the all-on kernel passes; nothing in Lean connects `probeAccept` to `step_mark_sound` beyond the author's calibration. Classification: INTERPRETATION DEFECT (mild): "load-bearing" is probe-relative, which the header does say, but a textbook reader would naturally hear "theorem-relative".
2. Docstring of `minimum_unique_in_class` (line 131–135) "Minimality under both declared cost orders is immediate ... the two orders are computed and compared in the Python mirror". Lean defines no cost order. The ledger CL-NC-INITIALITY says "both declared cost orders agree on the singleton". True trivially for any order; the Lean theorem is only the singleton statement. Classification: none (the docstring says where the orders live); noted so the textbook does not attribute a cost-order theorem to Lean.
3. `extension_retract` is `rfl` and `retract_section` is `rfl`; the header calls the pair "a conservative-retract instance of the initiality property, in class". The substantive content is `extension_retract_replay` (an induction). Classification: INTERPRETATION DEFECT (mild): "the retract half of initiality" names a universal property; what is proved is that one declared projection commutes with one declared extension's base events. The pr11 ledger C8 already rescoped the terminal; the section title at line 144 still says "The retract half of initiality".
4. Vacuity: none; every probe world is concrete and every probe is decided true on kernelDesc.
