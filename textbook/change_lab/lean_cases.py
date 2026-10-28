"""Book-Lean checks of the finite passage encoding; AuthorityEffect: None."""
from .run_lab import build_packet


def lean_list(values, item=str):
    return "[" + ", ".join(item(v) for v in values) + "]"


def lean_pair(pair):
    return "(" + ", ".join(map(str, pair)) + ")"


def lean_bool(value):
    return "true" if value else "false"


def lean_state(state):
    fields = ["occ := " + lean_list(state["occ"])]
    fields += [name + " := " + lean_list(state[name], lean_pair)
               for name in ("asserted", "wit", "prot", "refusals")]
    obs = state["obs"]
    fields.append("obs := " + ("none" if obs is None else "some " + lean_list(obs, lean_list)))
    fields += ["budget := " + str(state["budget"]), "licensed := " + lean_bool(state["licensed"]),
               "halted := " + lean_bool(state["halted"])]
    return "({ " + ", ".join(fields) + " } : PState)"


def lean_event(event):
    name, *args = event
    if name in ("admitOcc", "setBudget"):
        return f".{name} {args[0]}"
    if name in ("assertWit", "admitWit", "protect", "refuse"):
        return f".{name} {args[0]} {args[1]}"
    if name == "setLicense":
        return f".setLicense {lean_bool(args[0])}"
    if name == "addCol":
        return ".addCol " + lean_list(args[0])
    if name == "refineCol":
        return ".refineCol " + lean_list(args[0]) + " " + str(args[1])
    if name in ("halt", "declareObs"):
        return "." + name
    raise ValueError("Event not admitted by this teaching encoding")


def build_lean_checks():
    packet = build_packet()
    lines = ["import Derivation.PrimitivePassage", "namespace Textbook.PassageLab", "open PrimitivePassage"]
    names = []

    def theorem(name, proposition):
        lines.append(f"theorem {name} : {proposition} := by decide")
        names.append("Textbook.PassageLab." + name)

    for index, row in enumerate(packet["gate_records"]):
        s = lean_state(row["state"])
        theorem(f"gates_{index}", f"obstP {s} 1 2 = {lean_bool(row['active'])} ∧ "
                f"(retainedP {s} 1 2, protectedP {s} 1 2, declaredP {s}, zeroDeclP {s} 1 2) = "
                f"({lean_bool(row['retained'])}, {lean_bool(row['protected'])}, {lean_bool(row['declared'])}, {lean_bool(row['zero_total_convention'])})")
    for index, row in enumerate(packet["operations"].values()):
        s = lean_state(row["before"]["state"])
        for name in ("refine_C", "add_B"):
            event = lean_event(row[name]["event"])
            expected = lean_state(row[name]["after"]["state"])
            theorem(f"operation_{index}_{name}", f"step {s} ({event}) = {expected}")
        repairs = lean_list(row["before"]["repairs"], lambda m: "(" + lean_list(m[0]) + ", " + str(m[1]) + ")")
        proposals = lean_list(row["before"]["singleton_proposals"], lean_list)
        blocks = lean_list(row["before"]["next_blocks"], lambda block: lean_list(block, lean_event))
        theorem(f"families_{index}", f"repairFamily {s} 1 2 = {repairs} ∧ "
                f"extensionProposals {s} 1 2 = {proposals} ∧ nextFamilyP {s} = {blocks}")
    for index, row in enumerate(packet["canonical_columns"]):
        s = lean_state(packet["strong"]["state"])
        c = lean_list(row["column"])
        theorem(f"column_{index}", f"colOk {s} {c} = {lean_bool(row['structural_ok'])} ∧ "
                f"decide ({c} ∈ extensionProposals {s} 1 2) = {lean_bool(row['in_singleton_family'])} ∧ "
                f"step {s} (.addCol {c}) = {lean_state(row['after'])}")
    for label in ("timeline", "refusal_trace", "halt_trace"):
        rows = packet[label]
        for index in range(1, len(rows)):
            theorem(f"{label}_{index}", f"step {lean_state(rows[index-1]['state'])} "
                    f"({lean_event(rows[index]['event'])}) = {lean_state(rows[index]['state'])}")
    lines.append(r"""
theorem protected_sub_retained_step (s : PState)
    (hinv : ∀ p ∈ s.prot, p ∈ s.wit) (e : PEvent) :
    ∀ p ∈ (step s e).prot, p ∈ (step s e).wit := by
  cases e <;> simp only [step] <;> repeat' split
  all_goals
    first
      | exact hinv
      | (intro p hp
         simp only [List.mem_append]
         exact Or.inl (hinv p hp))
      | (rename_i i j hh hg
         intro p hp
         rcases List.mem_append.mp hp with hp' | hp'
         · exact hinv p hp'
         · have hmem : (i, j) ∈ s.wit := by
             simp only [Bool.and_eq_true, decide_eq_true_eq] at hg
             exact hg.1
           cases List.mem_singleton.mp hp'
           exact hmem)

theorem protected_sub_retained (h : List PEvent) :
    ∀ p ∈ (replayP h genesisP).prot, p ∈ (replayP h genesisP).wit := by
  suffices hgen : ∀ (s : PState), (∀ p ∈ s.prot, p ∈ s.wit) →
      ∀ p ∈ (replayP h s).prot, p ∈ (replayP h s).wit by
    exact hgen genesisP (by intro p hp; cases hp)
  induction h with
  | nil => intro s hs; exact hs
  | cons e rest ih =>
      intro s hs
      exact ih (step s e) (protected_sub_retained_step s hs e)
""")
    names += ["Textbook.PassageLab.protected_sub_retained_step", "Textbook.PassageLab.protected_sub_retained"]
    lines += ["end Textbook.PassageLab"] + ["#print axioms " + name for name in names]
    return "\n\n".join(lines) + "\n", names
