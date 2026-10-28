"""Deterministic lesson diagrams from recorded cases; AuthorityEffect: None."""
from html import escape
from math import hypot

SCENES = {
    "01_edge_ledger.svg": ("Four vertices and five admitted edges", "31_0_1", None),
    "02_closed_walk.svg": ("A closed walk, with no admitted face", "31_0_1", "31_1"),
    "03_one_face.svg": ("ABC admitted by a face step", "31_1_1", None),
    "04_two_faces.svg": ("Two faces; shared AC coefficient is zero", "31_3_1", None),
    "05_reversed_face.svg": ("Reverse ACD; shared AC coefficient is minus two", "31_3_-1", None),
}


def render_figures(packet):
    outputs = {}
    positions = ((70, 290), (70, 70), (370, 70), (370, 290))
    for name, (title, key, walk_key) in SCENES.items():
        case = packet["face_cases"][key]
        pieces = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 430" role="img" aria-label="{escape(title)}">',
                  f'<title>{escape(title)}</title>', '<rect width="440" height="430" fill="#fafbf7"/>',
                  '<defs><marker id="ref" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#52645d"/></marker><marker id="walk" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#19694e"/></marker></defs>']
        def text(x, y, value, size=18):
            pieces.append(f'<text x="{x}" y="{y}" text-anchor="middle" fill="#19322c" font-family="sans-serif" font-size="{size}">{escape(value)}</text>')
        for coefficient, face in case["face_chain"]:
            pts = " ".join(f"{positions[i][0]},{positions[i][1]}" for i in face)
            fill = "#cfe6d6" if coefficient > 0 else "#d6e4f2"
            pieces.append(f'<polygon points="{pts}" fill="{fill}"/>')
            text(sum(positions[i][0] for i in face) / 3, sum(positions[i][1] for i in face) / 3,
                 ("+" if coefficient > 0 else "−") + "".join(packet["vertices"][i] for i in face))
        for index, (a, b) in enumerate(packet["edges"]):
            if not case["edge_mask"] & (1 << index):
                continue
            x1, y1 = positions[a]
            x2, y2 = positions[b]
            length = hypot(x2-x1, y2-y1)
            ux, uy = (x2-x1)/length, (y2-y1)/length
            pieces.append(f'<line x1="{x1+22*ux}" y1="{y1+22*uy}" x2="{x2-25*ux}" y2="{y2-25*uy}" stroke="#52645d" stroke-width="2" marker-end="url(#ref)"/>')
        if walk_key:
            for a, b in packet["walk_cases"][walk_key]["steps"]:
                x1, y1 = positions[a]
                x2, y2 = positions[b]
                length = hypot(x2-x1, y2-y1)
                ux, uy = (x2-x1)/length, (y2-y1)/length
                d = f'M{x1+22*ux},{y1+22*uy} Q{(x1+x2)/2-18*uy},{(y1+y2)/2+18*ux} {x2-27*ux},{y2-27*uy}'
                pieces.append(f'<path d="{d}" fill="none" stroke="#19694e" stroke-width="3" marker-end="url(#walk)"/>')
        for i, (x, y) in enumerate(positions):
            pieces.append(f'<circle cx="{x}" cy="{y}" r="20" fill="white" stroke="#19322c" stroke-width="2"/>')
            text(x, y+6, packet["vertices"][i], 20)
        text(220, 345, "Admitted faces: " + (", ".join("".join(packet["vertices"][v] for v in face) for face in case["admitted_faces"]) or "none"), 16)
        if case["face_chain"]:
            ac = case["edge_coefficients"][2]["coefficient"]
            text(220, 375, f"AC stays admitted. Its boundary coefficient: {ac}.", 15)
        else:
            text(220, 375, "Reference arrows do not restrict traversal direction.", 15)
        text(220, 405, "Supplied diagram; placement is not a measured distance.", 14)
        outputs[name] = "\n".join(pieces + ["</svg>"]) + "\n"
    return outputs
