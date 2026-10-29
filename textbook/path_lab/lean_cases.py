"""Finite book instances against the actual cell calculus; AuthorityEffect: None."""
from .run_lab import EDGES, FACES, WALKS, build_packet


def ls(items, item=str):
    return "[" + ", ".join(item(i) for i in items) + "]"


def chain_literal(chain):
    return ls(chain, lambda row: "(" + str(row[0]) + ", " + ls(row[1]) + ")")


def history(mask, requests=0):
    events = [".addV " + str(v) for v in range(4)]
    events += [".addC 1 " + ls(edge) for i, edge in enumerate(EDGES) if mask & (1 << i)]
    events += [".addC 2 " + ls(face) for i, face in enumerate(FACES) if requests & (1 << i)]
    return "(nreplay " + ls(events) + " emptyN)"


def build_checks():
    packet = build_packet()
    source = ["import Derivation.BoundaryCancellation", "namespace Textbook.PathLab", "open LadderGeneral"]
    names = []

    def theorem(name, parts):
        names.append("Textbook.PathLab." + name)
        source.append("theorem " + name + " :\n  " + " ∧\n  ".join(parts) + " := by decide")

    for mask in range(32):
        for request in range(4):
            row = packet["face_cases"][f"{mask}_{request}_1"]
            current = history(mask, request)
            parts = [f"{current}.cells {dimension} = " + ls(row["after"].get(str(dimension), []), ls) for dimension in range(3)]
            for attempt in row["attempts"]:
                parts.append(f"shellN {history(mask)} 2 {ls(attempt['face'])} = " + str(attempt["guard"]).lower())
            for face in row["admitted_faces"]:
                parts.append(f"shellN {current} 2 {ls(face)} = false")
                parts.append(f"(stepN {current} 2 {ls(face)}).cells 2 = {current}.cells 2")
            for coefficient in (1, -1):
                item = packet["face_cases"][f"{mask}_{request}_{coefficient}"]
                chain = chain_literal(item["face_chain"])
                parts.append(f"pushN {chain} = {chain_literal(item['first_boundary'])}")
                parts.append(f"pushN (pushN {chain}) = {chain_literal(item['second_boundary'])}")
            theorem(f"faces_{mask}_{request}", parts)
        parts = []
        for index, walk in enumerate(WALKS):
            row = packet["walk_cases"][f"{mask}_{index}"]
            pairs = [sorted(pair) for pair in row["steps"]]
            checks = f"({ls(pairs, ls)} : List (List Nat)).all (fun edge => decide (edge ∈ {history(mask)}.cells 1))"
            parts.append(f"{checks} = " + str(row["valid"]).lower())
            if row["valid"]:
                ch = chain_literal(row["edge_chain"])
                parts += [f"coeffN [{v}] (pushN {ch}) = ({count} : Int)" for v, count in enumerate(row["endpoint_counts"])]
        theorem(f"walks_{mask}", parts)
    source += ["end Textbook.PathLab"]
    native = ["LadderGeneral.uniform_guarded_filler", "LadderGeneral.shell_no_self_fill",
              "BoundaryCancellation.d2_zero_unrestricted", "BoundaryCancellation.signless_countermodel"]
    names += native
    source += ["#print axioms " + name for name in names]
    return "\n\n".join(source) + "\n", names
