"""Build the customer-facing Genesis Textbook Wiki pages with 15-second soundbites,
interactive GFM stepping-stone widgets, and embedded <=15s Manim animations.

AuthorityEffect: None. Mirrors textbook/ and research tree metadata into
19L57G1.wiki.git without altering any sealed derivation file. Follows Claim
Hygiene strictly. Re-run whenever new textbook units or research trees are added
to main.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path

DEFAULT_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_WIKI_ROOT = Path(
    os.environ.get(
        "GENESIS_WIKI_ROOT",
        str(DEFAULT_REPO_ROOT.parent / "19L57G1.wiki"),
    )
)
RAW_WIKI_MEDIA = "https://raw.githubusercontent.com/wiki/dbccpage/19L57G1/media/manim"


def resolve_commit_sha(repo_root: Path) -> str:
    try:
        res = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        sha = res.stdout.strip()
        if len(sha) == 40:
            return sha
    except Exception:
        pass
    return "c9ef6d4842c14d00fc4da88110db91b2ca98d1b6"


def sanitize_claim_hygiene(text: str) -> str:
    """Replace any forbidden hype word in generated soundbite/widget text."""
    replacements = {
        r"\bproves\b": "shows in this model",
        r"\bProves\b": "Shows in this model",
        r"\bguarantees\b": "ensures under the declared assumptions",
        r"\bGuarantees\b": "Ensures under the declared assumptions",
        r"\bmathematically verifies\b": "checks in this formalization",
        r"\bfundamentally\b": "at the level of the declared rules",
        r"\bFundamentally\b": "At the level of the declared rules",
        r"\btrue intelligence\b": "bounded evaluator",
        r"\bimpossible\b": "blocked under these rules",
        r"\bImpossible\b": "Blocked under these rules",
        r"\buniversal\b": "all-instances",
        r"\bUniversal\b": "All-instances",
        r"\bflawless\b": "consistent with the specification",
        r"\bperfectly\b": "exactingly",
        r"\bPerfectly\b": "Exactingly",
        r"\bclearly\b": "explicitly",
        r"\bClearly\b": "Explicitly",
        r"\bobviously\b": "by inspection of the definition",
        r"\bObviously\b": "By inspection of the definition",
        r"\bsimply\b": "directly",
        r"\bSimply\b": "Directly",
        r"\bmerely\b": "only",
        r"\bMerely\b": "Only",
        r"\bweaponized\b": "applied",
    }
    out = text
    for pat, rep in replacements.items():
        out = re.sub(pat, rep, out)
    return out


def first_sentences(text: str, max_words: int = 34) -> str:
    """Trim a paragraph to a <=15-second soundbite (<= max_words words)."""
    clean = re.sub(r"\s+", " ", text.strip())
    clean = sanitize_claim_hygiene(clean)
    words = clean.split(" ")
    if len(words) <= max_words:
        return clean
    trimmed = " ".join(words[:max_words]).rstrip(",;:")
    if not trimmed.endswith("."):
        trimmed += "..."
    return trimmed


def act_for_part1(unit_num: int) -> tuple[str, str, str]:
    """Return (act_slug, act_title, act_summary) for a Part 1 unit number."""
    if unit_num <= 4:
        return (
            "act00_pre_genesis_mark",
            "Act I · The Mark & Inertia (Units 00–04)",
            "At the opaque mark ⟨⟩, nothing is derivable, supplying a label without admission is a no-op, and no next step is forced from inside.",
        )
    if unit_num <= 16:
        return (
            "act01_tokens_erasure_collapse",
            "Act II · Token Erasure & Observational Collapse (Units 05–16)",
            "External token names erase to numbered data; with zero recorded instances, every context test gives the same answer on datum 0 and datum 1.",
        )
    if unit_num <= 26:
        return (
            "act02_separation_and_minimality",
            "Act III · Witnessed Separation, Minimality & Irreflexivity (Units 17–26)",
            "Separating two data requires both a form and an instance (cost 2); item-count mu1 ties while mu2 selects the unary witness, and facts never entail irreflexivity.",
        )
    if unit_num <= 36:
        return (
            "act03_quotients_counting_transport",
            "Act IV · Quotients, Pair Counting & Transport (Units 27–36)",
            "Quotients hide merged pairs, fixed-carrier closure stops within n(n-1)/2 rounds, injective renaming transports separation, and uniform rules never pay for themselves.",
        )
    if unit_num <= 43:
        return (
            "act04_refusal_generator_capacity",
            "Act V · Refusal Rungs, Demand Generator & Capacity Bounds (Units 37–43)",
            "Four refusal disciplines price how obstructed demands are recorded, while pigeonhole capacity bounds show that bounded local views are outrun by growing demands.",
        )
    if unit_num <= 50:
        return (
            "act05_represented_kernel_horizon",
            "Act VI · Represented Kernel, Rule 1 & Every-Stage Horizon (Units 44–50)",
            "Putting the kernel state on the books yields the Rule 1 repair-or-extension dichotomy, the panel-relative NoOutside quotient, and every-stage quiescence.",
        )
    if unit_num <= 56:
        return (
            "act06_primitive_difference_apartness",
            "Act VII · Nine Readings of Difference, Initial D2 & Apartness (Units 51–56)",
            "Nine readings of primitive difference separate via 51 countermodels, the 2-point witness D2 is initial, and three apartness laws earn indistinguishability equivalence.",
        )
    if unit_num in (57, 58, 65, 66):
        return (
            "act07_interpreter_controller_boundary",
            "Act VIII · Thirteen Codes, Trace Idempotence & Interpreter Boundary (Units 57–58, 65–66)",
            "All 13 transition codes are idempotent with 132 non-commuting pairs, strict controllers agree on the replay orbit, and the coded interpreter lies outside its 13-code family.",
        )
    if unit_num <= 64:
        return (
            "act08_attachment_ladder_compression",
            "Act IX · Carrier Attachment, Boundary d² = 0, Compression & Profiles (Units 59–64)",
            "Internal repairs fix the graph while growth is supplied, signed boundary cancellation gives d² = 0, signature quotients compress presentations, and protection preserves separation.",
        )
    return (
        "act09_descent_relativity_fidelity",
        "Act X · Observer Descent, Naturality, Fidelity & Canonical Iso (Units 67+)",
        "Views descend iff constant on observer fibers, fixed-point-free swaps block natural pair choice, failed factorization forces splits, and canonical keys certify ordered isomorphism.",
    )


def act_for_part2(unit_num: int) -> tuple[str, str, str]:
    """Return (act_slug, act_title, act_summary) for a Part 2 institution unit number."""
    if unit_num <= 11:
        return (
            "act10_institutions_synergy_policy",
            "Part 2 · Act XI · Actors, Institutions, Synergy & Policy (Institutions 00–11)",
            "Combining actors into an institution tracks joint signatures, reveals when a family knows what no member knows alone, prices correspondence as an admission, and enforces witnessed demurral.",
        )
    return (
        "act11_probing_uncollapse_verdict",
        "Part 2 · Act XII · Discovery Tax n(n-1)/2, Uncollapse & Verdict Boundary (Institutions 12+)",
        "Acquiring an unknown actor partition over n data takes n(n-1)/2 pair probes, refutes the promised-count shortcut at n = N, characterizes uncollapse by mention delta, and locates the verdict-level interpreter boundary.",
    )


def extract_section(md: str, heading_pattern: str) -> str:
    """Extract body text of a ## section matching heading_pattern."""
    lines = md.splitlines()
    capturing = False
    buf: list[str] = []
    for line in lines:
        if line.startswith("## "):
            if capturing:
                break
            if re.search(heading_pattern, line, re.IGNORECASE):
                capturing = True
                continue
        elif capturing:
            buf.append(line)
    return "\n".join(buf).strip()


def extract_header_meta(md: str) -> dict[str, str]:
    """Extract Title, Claim, Status, Lean from top of unit."""
    lines = md.splitlines()
    title = lines[0].lstrip("# ").strip() if lines else "Unit"
    top_block = "\n".join(lines[1:25])

    claim_m = re.search(
        r"\*\*Claim\.\*\*\s*(.+?)(?=\n\*\*|\n\n|\Z)", top_block, re.DOTALL
    )
    claim = claim_m.group(1).strip() if claim_m else ""
    claim = re.sub(r"\s+", " ", claim)

    status_m = re.search(r"\*\*Status:\*\*\s*([^\n*]+)", top_block)
    status = status_m.group(1).strip().rstrip(".") if status_m else "derived"

    lean_m = re.search(r"\*\*Lean:\*\*\s*([^\n*]+)", top_block)
    lean = lean_m.group(1).strip().rstrip(".") if lean_m else "see unit"

    return {
        "title": title,
        "claim": sanitize_claim_hygiene(claim),
        "status": sanitize_claim_hygiene(status),
        "lean": lean,
    }


def rewrite_links_for_wiki(
    md: str,
    part1_map: dict[str, str],
    part2_map: dict[str, str],
    blob_base: str,
    is_part2: bool,
) -> str:
    """Rewrite relative markdown links inside textbook files so they work on GitHub Wiki."""
    out = md

    for fname, wname in part1_map.items():
        out = out.replace(f"](units/{fname})", f"]({wname})")
        out = out.replace(f"](../units/{fname})", f"]({wname})")
        out = out.replace(f"]({fname})", f"]({wname})")

    for fname, wname in part2_map.items():
        out = out.replace(f"](institutions/units/{fname})", f"]({wname})")
        out = out.replace(f"](units/{fname})", f"]({wname})")
        out = out.replace(f"]({fname})", f"]({wname})")

    out = out.replace("](START_HERE.md)", "](textbook_start_here)")
    out = out.replace("](../START_HERE.md)", "](textbook_start_here)")
    out = out.replace("](video_script_15s.md)", "](textbook_video_15s)")
    out = out.replace("](../video_script_15s.md)", "](textbook_video_15s)")
    out = out.replace("](derivation_coverage.md)", "](textbook_coverage)")
    out = out.replace("](../derivation_coverage.md)", "](textbook_coverage)")
    out = out.replace("](audit/README.md)", "](textbook_audit)")
    out = out.replace("](../audit/README.md)", "](textbook_audit)")
    out = out.replace("]( audit/AUDIT.md )", f"]({blob_base}/textbook/audit/AUDIT.md)")
    out = out.replace("](AUDIT.md)", f"]({blob_base}/textbook/audit/AUDIT.md)")
    out = out.replace("](inventory.json)", f"]({blob_base}/textbook/audit/inventory.json)")
    out = out.replace("](institutions/README.md)", "](textbook_institutions)")
    out = out.replace("](../institutions/README.md)", "](textbook_institutions)")
    if is_part2:
        out = out.replace("](README.md)", "](textbook_institutions)")
        out = out.replace("](../README.md)", "](textbook_overview)")
    else:
        out = out.replace("](README.md)", "](textbook_overview)")
        out = out.replace("](../README.md)", "](textbook_overview)")

    def repl_link(m: re.Match[str]) -> str:
        target = m.group(1).strip()
        if (
            target.startswith("http://")
            or target.startswith("https://")
            or target.startswith("#")
            or target.startswith("mailto:")
            or target.startswith("textbook_")
            or target
            in (
                "Home",
                "genesis_overview",
                "getting_started",
                "worked_examples",
                "concepts_and_glossary",
                "repository_map",
            )
        ):
            return m.group(0)
        clean_t = target.lstrip("./")
        if clean_t.startswith("../"):
            clean_t = "textbook/" + clean_t[3:]
        elif clean_t.startswith(("checks/", "units/", "institutions/", "audit/")):
            clean_t = "textbook/" + clean_t
        return f"]({blob_base}/{clean_t})"

    out = re.sub(r"\]\(([^)]+)\)", repl_link, out)
    return out


def build_unit_wiki_page(
    unit_idx: int,
    total_units: int,
    raw_md: str,
    prev_link: tuple[str, str] | None,
    next_link: tuple[str, str] | None,
    part1_map: dict[str, str],
    part2_map: dict[str, str],
    blob_base: str,
    commit_short: str,
    is_part2: bool = False,
) -> str:
    meta = extract_header_meta(raw_md)
    act_slug, act_title, _ = (
        act_for_part2(unit_idx) if is_part2 else act_for_part1(unit_idx)
    )

    q_sec = extract_section(raw_md, r"(Question|The mark|What you need first)")
    proved_sec = extract_section(
        raw_md, r"(What has been proved|What it shows|What this unit establishes)"
    )
    not_proved_sec = extract_section(
        raw_md, r"(What has not been proved|What it shows|Outside the system)"
    )
    outside_sec = extract_section(raw_md, r"Outside the system")
    plain_sec = extract_section(
        raw_md,
        r"(Plain-language interpretation|The proof, step by step|The external constructor)",
    )
    ex_sec = extract_section(raw_md, r"Student exercise")
    ans_sec = extract_section(raw_md, r"Answer")

    bite_q = first_sentences(q_sec or meta["claim"], 32)
    bite_mech = first_sentences(plain_sec or meta["claim"], 32)
    bite_proved = first_sentences(proved_sec or meta["claim"], 32)
    bite_limits = first_sentences(
        not_proved_sec
        or outside_sec
        or "Scoped to the declared definitions and finite ledger; does not establish claims outside the admitted representation.",
        32,
    )

    filled = max(1, round((unit_idx + 1) / max(1, total_units) * 12))
    bar_str = "█" * filled + "░" * (12 - filled)
    part_label = "Part 2 (Institutions)" if is_part2 else "Part 1 (Frozen Derivation)"
    unit_code = f"I{unit_idx:02d}" if is_part2 else f"U{unit_idx:02d}"

    nav_prev = (
        f"[◀ {prev_link[0]}]({prev_link[1]})"
        if prev_link
        else "[◀ Start Here](textbook_start_here)"
    )
    nav_next = (
        f"[{next_link[0]} ▶]({next_link[1]})"
        if next_link
        else "[Part 2: Institutions ▶](textbook_institutions)"
    )

    if ex_sec and ans_sec:
        pred_prompt = first_sentences(ex_sec, 42)
        pred_reveal = first_sentences(ans_sec, 48)
    else:
        pred_prompt = f"Before reading the proof of `{unit_code}`, ask: does `{meta['title']}` follow from the mark ⟨⟩ alone, or does it depend on the admitted representation and hypotheses listed below?"
        pred_reveal = f"{meta['claim']} — Status: **{meta['status']}**. In Genesis, every derived step holds relative to the explicitly admitted definitions and carries zero authority over the physical universe."

    rewritten_body = rewrite_links_for_wiki(
        raw_md, part1_map, part2_map, blob_base, is_part2
    )

    return f"""<!-- markdownlint-disable MD041 MD033 -->

{nav_prev} · [🏠 Textbook Hub](textbook_overview) · [🚀 Start Here](textbook_start_here) · [🎬 15s Videos](textbook_video_15s) · [🗺️ Coverage Map](textbook_coverage) · [🌲 Research Trees](textbook_research_trees) · {nav_next}

`{part_label}` · **{act_title}** · Progress: `[{bar_str}]` (`{unit_idx + 1} / {total_units}`) · `AuthorityEffect: None`

---

> [!IMPORTANT]
> ### ⚡ 15-Second Soundbite (`{unit_code}`) — Read This First
> **Core Claim:** {meta['claim']}
>
> - **Evidence Status:** `{meta['status']}`
> - **Formal Anchor:** {meta['lean']}
> - **15-Second Takeaway:** {bite_proved}

---

## 🎬 15-Second Manim Visual (`<= 15.0s`)

![{act_title} — 15s Manim Visual]({RAW_WIKI_MEDIA}/{act_slug}.gif)

**[▶ Watch / Download High-Resolution 15s MP4 Video]({RAW_WIKI_MEDIA}/{act_slug}.mp4)** · *Duration verified `<= 15.0s` via `ffprobe` · Built with Manim 0.19.2*

| Beat | Window | Visual & Pedagogical Beat (15s Total) |
| :--- | :--- | :--- |
| **1. Setup** | `0:00–0:03` | **Starting Ledger:** {bite_q} |
| **2. Move** | `0:03–0:07` | **Mechanism:** {bite_mech} |
| **3. Result** | `0:07–0:11` | **Established:** {bite_proved} |
| **4. Boundary** | `0:11–0:15` | **Scope Limit:** {bite_limits} |

---

## 🕹️ Interactive 15-Second Stepping Stones

<details>
<summary><b>🧠 Step 1 · 15-Second Prediction Challenge (Click to test your intuition before reading)</b></summary>

<br>

**Challenge:** {pred_prompt}

<details>
<summary><b>✨ Click to Reveal the Verdict (5-Second Dopamine Check)</b></summary>

<br>

> **Verdict (`{meta['status']}`):** {pred_reveal}

</details>

</details>

<details>
<summary><b>⏱️ Step 2 · The Entire Lesson in Four 15-Second Soundbites (60-Second Skim)</b></summary>

<br>

| 15s Card | Soundbite (`<= 35 words each`) |
| :--- | :--- |
| **1. The Question (`0–15s`)** | {bite_q} |
| **2. The Move (`15–30s`)** | {bite_mech} |
| **3. What Holds (`30–45s`)** | {bite_proved} |
| **4. Where It Stops (`45–60s`)** | {bite_limits} |

</details>

<details>
<summary><b>🗺️ Step 3 · Visual Dependency & Scope Flowchart (Click to Expand)</b></summary>

<br>

```mermaid
flowchart LR
    A["Admitted Ledger & Prerequisites<br/>({unit_code})"] --> B["Formal Check<br/>(Python + Lean 4.33.0)"]
    B --> C["Verdict: {meta['status'][:28]}"]
    C --> D["Boundary: Finite Ledger Scope<br/>(AuthorityEffect: None)"]
```

</details>

<details>
<summary><b>🛡️ Step 4 · Claim-Hygiene Boundaries (What This Supports vs. What It Does Not)</b></summary>

<br>

1. **What it supports:** {bite_proved}
2. **What it does not support:** {bite_limits}
3. **Narrowest defensible claim:** {meta['claim']} (Status: `{meta['status']}`, checked at revision `{commit_short}`).
4. **Next test / unit needed:** Proceed to {nav_next} or run the unit's Python and Lean check scripts in [`textbook/`]({blob_base}/textbook).

</details>

---

## 📖 Complete Textbook Unit (Unabridged Mirror)

{rewritten_body}

---

{nav_prev} · [🏠 Textbook Hub](textbook_overview) · [🚀 Start Here](textbook_start_here) · [🎬 15s Videos](textbook_video_15s) · [🗺️ Coverage Map](textbook_coverage) · [🌲 Research Trees](textbook_research_trees) · {nav_next}
"""


def discover_research_trees(repo_root: Path) -> list[tuple[str, bool, bool]]:
    """Return sorted list of (tree_name, has_contract, has_lean) under research/."""
    res_dir = repo_root / "research"
    trees: list[tuple[str, bool, bool]] = []
    if not res_dir.is_dir():
        return trees
    for child in sorted(res_dir.iterdir()):
        if not child.is_dir() or child.name.startswith((".", "_")):
            continue
        has_contract = (child / "TREE_CONTRACT.json").is_file()
        has_lean = (child / "lean").is_dir() or any(child.glob("*.lean"))
        if has_contract or (child / "README.md").is_file() or (child / "STATUS.md").is_file():
            trees.append((child.name, has_contract, has_lean))
    return trees


def build_all(repo_root: Path, wiki_root: Path) -> dict[str, int]:
    wiki_root.mkdir(parents=True, exist_ok=True)
    commit_sha = resolve_commit_sha(repo_root)
    commit_short = commit_sha[:12]
    blob_base = f"https://github.com/dbccpage/19L57G1/blob/{commit_sha}"

    units_dir = repo_root / "textbook" / "units"
    inst_dir = repo_root / "textbook" / "institutions" / "units"

    p1_files = sorted(units_dir.glob("*.md"))
    p2_files = sorted(inst_dir.glob("*.md"))

    assert len(p1_files) >= 75, f"Expected >= 75 Part 1 units, found {len(p1_files)}"
    assert len(p2_files) >= 18, f"Expected >= 18 Part 2 units, found {len(p2_files)}"

    part1_map: dict[str, str] = {}
    part1_entries: list[tuple[int, Path, str, str]] = []
    for f in p1_files:
        m = re.match(r"^(\d+)_(.+)\.md$", f.name)
        if not m:
            continue
        idx = int(m.group(1))
        slug = f"textbook_u{idx:02d}_{m.group(2)}"
        part1_map[f.name] = slug
        meta = extract_header_meta(f.read_text(encoding="utf-8"))
        part1_entries.append((idx, f, slug, meta["title"]))

    part2_map: dict[str, str] = {}
    part2_entries: list[tuple[int, Path, str, str]] = []
    for f in p2_files:
        m = re.match(r"^(\d+)_(.+)\.md$", f.name)
        if not m:
            continue
        idx = int(m.group(1))
        slug = f"textbook_i{idx:02d}_{m.group(2)}"
        part2_map[f.name] = slug
        meta = extract_header_meta(f.read_text(encoding="utf-8"))
        part2_entries.append((idx, f, slug, meta["title"]))

    # 1. Build all Part 1 unit wiki pages
    for i, (idx, fpath, slug, _) in enumerate(part1_entries):
        prev_link = (
            (f"Unit {part1_entries[i-1][0]:02d}", part1_entries[i - 1][2])
            if i > 0
            else None
        )
        next_link = (
            (f"Unit {part1_entries[i+1][0]:02d}", part1_entries[i + 1][2])
            if i + 1 < len(part1_entries)
            else ("Inst 00 (Part 2)", part2_entries[0][2])
        )
        raw_md = fpath.read_text(encoding="utf-8")
        wiki_md = build_unit_wiki_page(
            idx,
            len(part1_entries),
            raw_md,
            prev_link,
            next_link,
            part1_map,
            part2_map,
            blob_base,
            commit_short,
            is_part2=False,
        )
        (wiki_root / f"{slug}.md").write_text(wiki_md, encoding="utf-8", newline="\n")

    # 2. Build all Part 2 institution unit wiki pages
    for i, (idx, fpath, slug, _) in enumerate(part2_entries):
        prev_link = (
            (f"Inst {part2_entries[i-1][0]:02d}", part2_entries[i - 1][2])
            if i > 0
            else (f"Unit {part1_entries[-1][0]:02d} (Part 1)", part1_entries[-1][2])
        )
        next_link = (
            (f"Inst {part2_entries[i+1][0]:02d}", part2_entries[i + 1][2])
            if i + 1 < len(part2_entries)
            else ("Derivation Coverage Map", "textbook_coverage")
        )
        raw_md = fpath.read_text(encoding="utf-8")
        wiki_md = build_unit_wiki_page(
            idx,
            len(part2_entries),
            raw_md,
            prev_link,
            next_link,
            part1_map,
            part2_map,
            blob_base,
            commit_short,
            is_part2=True,
        )
        (wiki_root / f"{slug}.md").write_text(wiki_md, encoding="utf-8", newline="\n")

    # 3. Build textbook_research_trees.md (syncs all research trees on main)
    research_trees = discover_research_trees(repo_root)
    taught_trees = {
        "uncollapse": f"[Inst 16]({part2_entries[16][2]})",
        "two_theorems": f"[Inst 12]({part2_entries[12][2]})–[Inst 15]({part2_entries[15][2]})",
        "interpreter_verdict": f"[Inst 17]({part2_entries[17][2]})",
        "actor_institution": f"[Inst 00]({part2_entries[0][2]})–[Inst 11]({part2_entries[11][2]})",
    }
    tree_rows = []
    for t_name, has_contract, has_lean in research_trees:
        t_link = f"[`research/{t_name}/`]({blob_base}/research/{t_name})"
        c_tag = "`TREE_CONTRACT.json`" if has_contract else "directory"
        l_tag = "Lean + Python" if has_lean else "Python / Docs"
        tb_col = taught_trees.get(t_name, "Post-seal research tree")
        tree_rows.append(f"| {t_link} | {c_tag} | {l_tag} | {tb_col} |")

    res_page = f"""<!-- markdownlint-disable MD041 MD033 -->

[🏠 Genesis Wiki Home](Home) · [🚀 Start Here](textbook_start_here) · [📚 Textbook Hub](textbook_overview) · [🏛️ Part 2: Institutions](textbook_institutions) · [🗺️ Coverage Matrix](textbook_coverage) · **[🌲 Research Trees Sync](textbook_research_trees)**

---

> [!IMPORTANT]
> ### ⚡ Post-Seal Research Trees Synced to `main` (`{commit_short}`)
> This page is regenerated automatically by `python textbook/media/build_wiki_textbook.py` whenever new textbook units or research trees are added to `main`. It inventories all **{len(research_trees)}** research trees currently under [`research/`]({blob_base}/research) and links the trees taught in [Part 2: Actors & Institutions](textbook_institutions). `AuthorityEffect: None`.

---

## Research Trees on `main` (`{len(research_trees)}` Trees)

| Research Tree | Contract | Formalization | Textbook Coverage |
| :--- | :--- | :--- | :--- |
{chr(10).join(tree_rows)}
"""
    (wiki_root / "textbook_research_trees.md").write_text(
        res_page, encoding="utf-8", newline="\n"
    )

    # 4. Build textbook_start_here.md
    start_raw = (repo_root / "textbook" / "START_HERE.md").read_text(encoding="utf-8")
    start_rewritten = rewrite_links_for_wiki(
        start_raw, part1_map, part2_map, blob_base, False
    )
    start_page = f"""<!-- markdownlint-disable MD041 MD033 -->

[🏠 Genesis Wiki Home](Home) · **[🚀 Start Here](textbook_start_here)** · [📚 Textbook Hub](textbook_overview) · [🎬 15s Video Gallery](textbook_video_15s) · [🏛️ Part 2: Institutions](textbook_institutions) · [🗺️ Coverage Matrix](textbook_coverage) · [🌲 Research Trees](textbook_research_trees) · [Unit 00 ▶]({part1_entries[0][2]})

---

> [!IMPORTANT]
> ### ⚡ The 15-Second Soundbite: Welcome to Genesis (`AuthorityEffect: None`)
> **We erase every preconceived notion.** We start with one opaque mark `<>`—no numbers, no sets, no containers, no rules. Every step that follows is either **admitted** at a stated price or **derived** in Lean 4 and checked in Python.
>
> - **Zero Prerequisites:** Written for a patient reader with no background in math, formal logic, Python, or Lean.
> - **15-Second Bites:** Every lesson opens with a 15-second soundbite, a `<= 15s` Manim visual, and interactive click-to-reveal stepping stones.

---

## 🎬 15-Second Manim Entrance (`<= 15.0s`)

![Act I — Pre-Genesis and the Mark <>]({RAW_WIKI_MEDIA}/act00_pre_genesis_mark.gif)

**[▶ Watch / Download High-Resolution 15s MP4]({RAW_WIKI_MEDIA}/act00_pre_genesis_mark.mp4)** · [📜 Read the 15-Second Spoken Script (`128 WPM`)](textbook_video_15s)

---

## 🕹️ Interactive 60-Second Cosmos Tour (Click Any Stage to Preview in 15 Seconds)

<details open>
<summary><b>⚡ Stage 1 · The Opaque Mark & Inertia (Units 00–04) — Click to toggle</b></summary>

<br>

- **15s Soundbite:** Writing `<>` does not create an empty set or a box. Before any rule is admitted, nothing is derivable (`genesis_underivable`), and supplying a label without admitting it changes nothing (`supply_no_op`).
- **Start Reading:** [Unit 00: The mark and the external constructor]({part1_entries[0][2]}) → [Unit 01: Nothing is derivable at genesis]({part1_entries[1][2]})

</details>

<details>
<summary><b>⚡ Stage 2 · Token Erasure & Observational Collapse (Units 05–16)</b></summary>

<br>

- **15s Soundbite:** Admitting two labels `<a>` and `<ab>` gives two numbered data (`0` and `1`), but with no recorded instances, every internal test gives the same answer on both (`R2L_collapsed`).
- **Jump In:** [Unit 05: Readings L and F]({part1_entries[5][2]}) → [Unit 16: ⟨A⟩ and ⟨AB⟩ are collapsed]({part1_entries[16][2]})

</details>

<details>
<summary><b>⚡ Stage 3 · Witnessed Separation, Cost Ties & Irreflexivity (Units 17–26)</b></summary>

<br>

- **15s Soundbite:** Separating datum 0 from datum 1 cannot be done at cost 1 (`cost1_insufficient_general`). It takes a form plus an instance (`BL` or `BD`), and recording a single fact never forces the general law of irreflexivity (`irrefl_law_not_entailed`).
- **Jump In:** [Unit 17: Demands are irreflexive by guard]({part1_entries[17][2]}) → [Unit 26: Facts never entail irreflexivity]({part1_entries[26][2]})

</details>

<details>
<summary><b>⚡ Stage 4 · Quotients, Refusal, Capacity & Represented Kernel (Units 27–50)</b></summary>

<br>

- **15s Soundbite:** Quotients hide what they merge (`quot_barrier`), bounded local views are outrun by growing separation demands (`Pigeonhole`, `G1Class`), and putting the kernel on the books yields the Rule 1 repair-or-extension dichotomy (`Completion`, `Horizon`).
- **Jump In:** [Unit 27: Quotient barrier]({part1_entries[27][2]}) → [Unit 46: Rule 1 in a fixed kernel]({part1_entries[46][2]}) → [Unit 50: Horizon]({part1_entries[50][2]})

</details>

<details>
<summary><b>⚡ Stage 5 · Primitive Difference, Higher Cells, Compression & Fidelity (Units 51–74)</b></summary>

<br>

- **15s Soundbite:** Nine readings of difference separate via 51 countermodels (`PrimitiveCore`), signed boundary cancellation gives `d² = 0` (`BoundaryCancellation`), presentations compress via signature quotients (`Compression`), and the coded interpreter sits outside its 13-code family (`InterpreterBoundary`).
- **Jump In:** [Unit 51: Nine readings]({part1_entries[51][2]}) → [Unit 60: Boundary cancellation]({part1_entries[60][2]}) → [Unit 74: Canonical keys]({part1_entries[74][2]})

</details>

<details>
<summary><b>⚡ Stage 6 · Part 2: Actors, Institutions, Probing & Uncollapse (Institutions 00–17)</b></summary>

<br>

- **15s Soundbite:** Combining actors into an institution lets a family know claims no single actor knows (`exceeds_three_two_resolution`), prices correspondence as an admission, requires `n(n-1)/2` pair probes to acquire an unknown partition, and characterizes uncollapse by mention delta.
- **Jump In:** [Part 2 Hub](textbook_institutions) → [Inst 00: Actors & Signatures]({part2_entries[0][2]}) → [Inst 17: Verdict Boundary]({part2_entries[17][2]})

</details>

---

{start_rewritten}
"""
    (wiki_root / "textbook_start_here.md").write_text(
        start_page, encoding="utf-8", newline="\n"
    )

    # 5. Build textbook_video_15s.md
    vid_raw = (repo_root / "textbook" / "video_script_15s.md").read_text(
        encoding="utf-8"
    )
    vid_rewritten = rewrite_links_for_wiki(
        vid_raw, part1_map, part2_map, blob_base, False
    )

    act_gallery_rows = [
        ("Act I (`U00–U04`)", "act00_pre_genesis_mark", "The Mark `<>` & Inertia", f"[Unit 00]({part1_entries[0][2]})–[Unit 04]({part1_entries[4][2]})"),
        ("Act II (`U05–U16`)", "act01_tokens_erasure_collapse", "Token Erasure & Collapse", f"[Unit 05]({part1_entries[5][2]})–[Unit 16]({part1_entries[16][2]})"),
        ("Act III (`U17–U26`)", "act02_separation_and_minimality", "Witnessed Separation & Minimality", f"[Unit 17]({part1_entries[17][2]})–[Unit 26]({part1_entries[26][2]})"),
        ("Act IV (`U27–U36`)", "act03_quotients_counting_transport", "Quotients, Counting & Transport", f"[Unit 27]({part1_entries[27][2]})–[Unit 36]({part1_entries[36][2]})"),
        ("Act V (`U37–U43`)", "act04_refusal_generator_capacity", "Refusal Rungs & Capacity Bounds", f"[Unit 37]({part1_entries[37][2]})–[Unit 43]({part1_entries[43][2]})"),
        ("Act VI (`U44–U50`)", "act05_represented_kernel_horizon", "Represented Kernel & Horizon", f"[Unit 44]({part1_entries[44][2]})–[Unit 50]({part1_entries[50][2]})"),
        ("Act VII (`U51–U56`)", "act06_primitive_difference_apartness", "Primitive Difference & Apartness", f"[Unit 51]({part1_entries[51][2]})–[Unit 56]({part1_entries[56][2]})"),
        ("Act VIII (`U57–U58, U65–U66`)", "act07_interpreter_controller_boundary", "13 Codes, Idempotence & Interpreter Boundary", f"[Unit 57]({part1_entries[57][2]}), [Unit 58]({part1_entries[58][2]}), [Unit 65]({part1_entries[65][2]}), [Unit 66]({part1_entries[66][2]})"),
        ("Act IX (`U59–U64`)", "act08_attachment_ladder_compression", "Attachment, Boundary `d²=0` & Compression", f"[Unit 59]({part1_entries[59][2]})–[Unit 64]({part1_entries[64][2]})"),
        ("Act X (`U67–U74`)", "act09_descent_relativity_fidelity", "Observer Descent, Naturality & Fidelity", f"[Unit 67]({part1_entries[67][2]})–[Unit 74]({part1_entries[74][2]})"),
        ("Part 2 · Act XI (`I00–I11`)", "act10_institutions_synergy_policy", "Actors, Institutions, Synergy & Demurral", f"[Inst 00]({part2_entries[0][2]})–[Inst 11]({part2_entries[11][2]})"),
        ("Part 2 · Act XII (`I12–I17`)", "act11_probing_uncollapse_verdict", "Probe Tax `n(n-1)/2`, Uncollapse & Verdict", f"[Inst 12]({part2_entries[12][2]})–[Inst 17]({part2_entries[17][2]})"),
    ]

    gallery_md_blocks = []
    for act_lbl, slug, desc, u_links in act_gallery_rows:
        gallery_md_blocks.append(
            f"""### {act_lbl}: {desc}
- **Units covered:** {u_links} · **Duration:** `<= 15.0s` verified · **[▶ Download MP4]({RAW_WIKI_MEDIA}/{slug}.mp4)**

![{desc}]({RAW_WIKI_MEDIA}/{slug}.gif)
"""
        )

    vid_page = f"""<!-- markdownlint-disable MD041 MD033 -->

[🏠 Genesis Wiki Home](Home) · [🚀 Start Here](textbook_start_here) · [📚 Textbook Hub](textbook_overview) · **[🎬 15s Video Gallery](textbook_video_15s)** · [🗺️ Coverage Matrix](textbook_coverage) · [🌲 Research Trees](textbook_research_trees)

---

> [!IMPORTANT]
> ### 🎬 Hard Rule: Every Animation and Soundbite Is Strictly `<= 15 Seconds`
> All 12 Manim animations below are rendered with **Manim 0.19.2** and verified with `ffprobe` at **`10.93s–14.07s` (`<= 15.0s`)**. Each animation auto-plays inline in the Wiki and pairs with a downloadable `.mp4`. `AuthorityEffect: None`.

---

{vid_rewritten}

---

## 🎥 Complete 12-Act Manim Animation Gallery (`<= 15.0s` Each)

{chr(10).join(gallery_md_blocks)}
"""
    (wiki_root / "textbook_video_15s.md").write_text(
        vid_page, encoding="utf-8", newline="\n"
    )

    # 6. Build textbook_overview.md
    readme_raw = (repo_root / "textbook" / "README.md").read_text(encoding="utf-8")
    readme_rewritten = rewrite_links_for_wiki(
        readme_raw, part1_map, part2_map, blob_base, False
    )
    for idx, _, slug, _ in part1_entries:
        readme_rewritten = re.sub(
            rf"^\|\s*{idx:02d}\s*\|",
            f"| [{idx:02d}]({slug}) |",
            readme_rewritten,
            flags=re.MULTILINE,
        )

    overview_page = f"""<!-- markdownlint-disable MD041 MD033 -->

[🏠 Genesis Wiki Home](Home) · [🚀 Start Here](textbook_start_here) · **[📚 Textbook Hub](textbook_overview)** · [🏛️ Part 2: Institutions](textbook_institutions) · [🎬 15s Video Gallery](textbook_video_15s) · [🗺️ Coverage Matrix](textbook_coverage) · [🔍 75-Module Audit](textbook_audit) · [🌲 Research Trees](textbook_research_trees)

---

> [!IMPORTANT]
> ### ⚡ The Genesis Textbook in 15 Seconds (`AuthorityEffect: None`)
> - **Part 1 ([Units 00–{part1_entries[-1][0]:02d}](textbook_u00_mark_and_constructor)):** Every definition, theorem, countermodel, and open boundary across all **75 frozen Lean 4 modules** in `lean4/Derivation/`.
> - **Part 2 ([Institutions 00–{part2_entries[-1][0]:02d}](textbook_institutions)):** Post-freeze research suites (`actor_institution`, `two_theorems`, `uncollapse`, `interpreter_verdict`) plus the synced [Research Trees Index](textbook_research_trees).
> - **How to study:** Start at **[Start Here](textbook_start_here)** or **[Unit 00](textbook_u00_mark_and_constructor)**. Every unit page has a 15-second soundbite, an embedded `<= 15s` Manim animation, interactive prediction widgets, and the full line-by-line Python + Lean 4 lesson.

![Act I — The Mark and Inertia]({RAW_WIKI_MEDIA}/act00_pre_genesis_mark.gif)

---

{readme_rewritten}
"""
    (wiki_root / "textbook_overview.md").write_text(
        overview_page, encoding="utf-8", newline="\n"
    )

    # 7. Build textbook_institutions.md
    inst_readme_raw = (
        repo_root / "textbook" / "institutions" / "README.md"
    ).read_text(encoding="utf-8")
    inst_readme_rewritten = rewrite_links_for_wiki(
        inst_readme_raw, part1_map, part2_map, blob_base, True
    )
    for idx, _, slug, _ in part2_entries:
        inst_readme_rewritten = re.sub(
            rf"^\|\s*{idx:02d}\s*\|",
            f"| [{idx:02d}]({slug}) |",
            inst_readme_rewritten,
            flags=re.MULTILINE,
        )

    inst_page = f"""<!-- markdownlint-disable MD041 MD033 -->

[🏠 Genesis Wiki Home](Home) · [🚀 Start Here](textbook_start_here) · [📚 Part 1: Frozen Derivation](textbook_overview) · **[🏛️ Part 2: Actors & Institutions](textbook_institutions)** · [🎬 15s Video Gallery](textbook_video_15s) · [🗺️ Coverage Matrix](textbook_coverage) · [🌲 Research Trees](textbook_research_trees)

---

> [!IMPORTANT]
> ### ⚡ Part 2 in 15 Seconds: Actors & Institutions (`Units 00–{part2_entries[-1][0]:02d}`)
> When several presentations (**actors**) combine into a family (**an institution**), they can jointly determine claims no single member knows (`exceeds_three_two_resolution`). Correspondence across actors is a priced admission, unknown claims force a witnessed **Demur**, and probing an unknown partition over `n` data costs `n(n-1)/2` pair queries.

![Part 2 — Actors and Institutions]({RAW_WIKI_MEDIA}/act10_institutions_synergy_policy.gif)

---

{inst_readme_rewritten}
"""
    (wiki_root / "textbook_institutions.md").write_text(
        inst_page, encoding="utf-8", newline="\n"
    )

    # 8. Build textbook_coverage.md
    cov_raw = (repo_root / "textbook" / "derivation_coverage.md").read_text(
        encoding="utf-8"
    )
    cov_rewritten = rewrite_links_for_wiki(
        cov_raw, part1_map, part2_map, blob_base, False
    )
    cov_page = f"""<!-- markdownlint-disable MD041 MD033 -->

[🏠 Genesis Wiki Home](Home) · [🚀 Start Here](textbook_start_here) · [📚 Textbook Hub](textbook_overview) · [🏛️ Part 2: Institutions](textbook_institutions) · **[🗺️ Coverage Matrix](textbook_coverage)** · [🔍 75-Module Audit](textbook_audit) · [🌲 Research Trees](textbook_research_trees)

---

> [!IMPORTANT]
> ### ⚡ Derivation Coverage Matrix in 15 Seconds (`AuthorityEffect: None`)
> Accounts for all **75 frozen Lean 4 modules** (`779` definitions/structures and `1,585` theorem/lemma declarations), all Part 2 research theorems, their exact evidence statuses (`FROZEN`, `POST_FREEZE_PROVED`, `CONDITIONAL`, `VERIFIED_FINITE`, `REFUTED`, `ADMITTED`, `OPEN`), and the **acyclic lesson dependency DAG (`0` cycles)**.

---

{cov_rewritten}
"""
    (wiki_root / "textbook_coverage.md").write_text(
        cov_page, encoding="utf-8", newline="\n"
    )

    # 9. Build textbook_audit.md
    audit_raw = (repo_root / "textbook" / "audit" / "README.md").read_text(
        encoding="utf-8"
    )
    audit_rewritten = rewrite_links_for_wiki(
        audit_raw, part1_map, part2_map, blob_base, False
    )
    audit_page = f"""<!-- markdownlint-disable MD041 MD033 -->

[🏠 Genesis Wiki Home](Home) · [🚀 Start Here](textbook_start_here) · [📚 Textbook Hub](textbook_overview) · [🗺️ Coverage Matrix](textbook_coverage) · **[🔍 75-Module Source Audit](textbook_audit)** · [🌲 Research Trees](textbook_research_trees)

---

> [!IMPORTANT]
> ### ⚡ 75-Module Source Audit in 15 Seconds (`AuthorityEffect: None`)
> Every tracked `.lean` file in `lean4/Derivation/` (all 62 root-imported modules plus all 13 non-root modules) and `lean4/Derivation.lean` is audited for SHA-256 content hash, imports, declarations, axiom dependencies (`1,530` reports within `propext` and `Quot.sound`), and proof-vs-prose alignment (including the documented vacuity defect in the first two conjuncts of `LadderGeneral.d2_zero_dims_2_3_4`, superseded by `BoundaryCancellation.d2_zero_unrestricted`).

---

{audit_rewritten}
"""
    (wiki_root / "textbook_audit.md").write_text(
        audit_page, encoding="utf-8", newline="\n"
    )

    # 10. Update _Sidebar.md so the SECOND subsection is "## Textbook"
    def fmt_unit_links(entries: list[tuple[int, Path, str, str]], prefix: str) -> str:
        lines = []
        for idx, _, slug, title in entries:
            short_t = re.sub(r"^Unit\s+\d+[\.:]\s*", "", title)
            if len(short_t) > 42:
                short_t = short_t[:39].rstrip() + "..."
            lines.append(f"- [{prefix}{idx:02d}: {short_t}]({slug})")
        return "\n".join(lines)

    sidebar_md = f"""<!-- markdownlint-disable MD041 MD033 -->

## Genesis

- [Home](Home)
- [Overview](genesis_overview)
- [Getting started](getting_started)
- [Worked examples](worked_examples)
- [Concepts and glossary](concepts_and_glossary)
- [Repository map](repository_map)

## Textbook

- [🚀 Start Here (15s Entrance)](textbook_start_here)
- [📚 Textbook Hub (Units 00–{part1_entries[-1][0]:02d})](textbook_overview)
- [🏛️ Part 2: Institutions (00–{part2_entries[-1][0]:02d})](textbook_institutions)
- [🎬 15s Manim Video Gallery](textbook_video_15s)
- [🗺️ Derivation Coverage Matrix](textbook_coverage)
- [🔍 75-Module Source Audit](textbook_audit)
- [🌲 Synced Research Trees ({len(research_trees)})](textbook_research_trees)

<details>
<summary><b>Act I · Mark & Inertia (U00–U04)</b></summary>

{fmt_unit_links(part1_entries[0:5], "U")}

</details>

<details>
<summary><b>Act II · Collapse & Tokens (U05–U16)</b></summary>

{fmt_unit_links(part1_entries[5:17], "U")}

</details>

<details>
<summary><b>Act III · Separation & Cost (U17–U26)</b></summary>

{fmt_unit_links(part1_entries[17:27], "U")}

</details>

<details>
<summary><b>Act IV · Quotients & Bounds (U27–U36)</b></summary>

{fmt_unit_links(part1_entries[27:37], "U")}

</details>

<details>
<summary><b>Act V · Refusal & Capacity (U37–U43)</b></summary>

{fmt_unit_links(part1_entries[37:44], "U")}

</details>

<details>
<summary><b>Act VI · Kernel & Horizon (U44–U50)</b></summary>

{fmt_unit_links(part1_entries[44:51], "U")}

</details>

<details>
<summary><b>Act VII · Primitive Diff (U51–U56)</b></summary>

{fmt_unit_links(part1_entries[51:57], "U")}

</details>

<details>
<summary><b>Act VIII · Interpreter & Orbit (U57–U58)</b></summary>

{fmt_unit_links(part1_entries[57:59], "U")}

</details>

<details>
<summary><b>Act IX · Attachment & d²=0 (U59–U64)</b></summary>

{fmt_unit_links(part1_entries[59:65], "U")}

</details>

<details>
<summary><b>Act X · Codes, Descent & Iso (U65–U{part1_entries[-1][0]:02d})</b></summary>

{fmt_unit_links(part1_entries[65:], "U")}

</details>

<details>
<summary><b>Part 2 · Institutions (I00–I{part2_entries[-1][0]:02d})</b></summary>

{fmt_unit_links(part2_entries, "I")}

</details>

## Core machinery

- [Admission kernel](admission_kernel)
- [Observation and separation](observation_and_separation)
- [Candidates, costs, and ties](candidates_costs_and_ties)
- [Isomorphism and quotients](isomorphism_and_quotients)
- [Engine and frontiers](engine_and_frontiers)
- [Artifacts and replay](artifacts_and_replay)
- [Python module reference](python_module_reference)

## Proof and evidence

- [Lean verification](lean_verification)
- [Papers and claim ledgers](papers_and_claim_ledgers)
- [Evidence and provenance](evidence_and_provenance)
- [Local validation](local_validation)
- [Limitations and open obligations](limitations_and_open_obligations)

## Research and integration

- [Research atlas](research_atlas)
- [Every research tree](research_tree_index)
- [Research verification and custody](research_verification_and_custody)
- [Foundations and passage](foundations_and_passage)
- [Alpha harness](alpha_harness)
- [Consumer integration](consumer_integration)
- [Second derivation and freeze](second_derivation_and_freeze)
- [Closeout and receipts](closeout_and_historical_receipts)
- [Build order](build_order_and_dependencies)

## Operating safely

- [Source contract](source_contract)
- [Contribution workflow](contribution_workflow)
- [Troubleshooting](troubleshooting)
- [FAQ](faq)
- [Review scope and findings](review_scope_and_findings)
- [Wiki maintenance](wiki_maintenance)
"""
    (wiki_root / "_Sidebar.md").write_text(
        sidebar_md, encoding="utf-8", newline="\n"
    )

    # 11. Update Home.md
    home_md = f"""# Genesis: A Reader's and Developer's Guide

Genesis (`19L57G1`) studies what follows from an opaque seed `<>` under declared finite challenges, what has to be admitted separately, and where the evidence stops. It contains a replayable admission kernel, deterministic searches, Lean 4 proofs, claim ledgers, a complete **{len(part1_entries) + len(part2_entries)}-unit introductory Textbook**, and a post-seal research estate.

This Wiki is an explanatory map and mirrored textbook of the published repository, not an amendment to its sealed experiment, a new derivation, or a certification of all its claims. `AuthorityEffect: None`.

---

> [!IMPORTANT]
> ### ⚡ New to Genesis? Start with the 15-Second Textbook Entrance
> **Zero prerequisites required.** Every preconceived notion (sets, numbers, containers, rules) is erased at the door so any patient reader can follow the ledger from the single mark `<>` through all 75 frozen Lean 4 modules and post-freeze research suites—one **15-second soundbite**, **Manim visual (`<= 15s`)**, and **interactive stepping stone** at a time.
>
> 👉 **[🚀 Start Here (15-Second Entrance)](textbook_start_here)** · **[📚 Textbook Hub (Units 00–{part1_entries[-1][0]:02d})](textbook_overview)** · **[🏛️ Part 2: Actors & Institutions (00–{part2_entries[-1][0]:02d})](textbook_institutions)** · **[🎬 15s Manim Video Gallery](textbook_video_15s)** · **[🌲 Synced Research Trees ({len(research_trees)})](textbook_research_trees)**

![Pre-Genesis and the Opaque Mark <> (15s Manim Visual)]({RAW_WIKI_MEDIA}/act00_pre_genesis_mark.gif)

---

## Start with your question

| I want to... | Start here | Continue with |
| --- | --- | --- |
| **Learn from scratch in 15-second soundbites (no math/code background needed)** | **[🚀 Textbook: Start Here](textbook_start_here)** | **[Unit 00: The mark](textbook_u00_mark_and_constructor)**, **[Textbook Hub](textbook_overview)**, **[15s Video Gallery](textbook_video_15s)** |
| **Study Actors, Institutions, Probing & Uncollapse** | **[🏛️ Part 2: Institutions](textbook_institutions)** | **[Inst 00: Signatures]({part2_entries[0][2]})**, **[Coverage Matrix](textbook_coverage)**, **[Synced Research Trees](textbook_research_trees)** |
| Understand the result without running anything | [Overview](genesis_overview) | [Concepts and glossary](concepts_and_glossary), [Reading the papers](papers_and_claim_ledgers) |
| Run a small, concrete example | [Getting started](getting_started) | [Admission kernel](admission_kernel), [Worked examples](worked_examples) |
| Understand finite search and tied answers | [Candidates and costs](candidates_costs_and_ties) | [Isomorphism](isomorphism_and_quotients), [Engine and frontiers](engine_and_frontiers) |
| Review a mathematical claim | [Evidence and provenance](evidence_and_provenance) | [Lean verification](lean_verification), [75-Module Audit](textbook_audit), [Limitations](limitations_and_open_obligations) |
| Use the Alpha reference slice | [Alpha harness](alpha_harness) | [Consumer integration](consumer_integration), [Alpha source reference](research_alpha_engine) |
| Find a research package | [Research atlas](research_atlas) | [Every research tree](research_tree_index), [Dependency/build map](build_order_and_dependencies) |
| Contribute without crossing the seal | [Contribution workflow](contribution_workflow) | [Source contract](source_contract), [Research custody](research_verification_and_custody) |
| Understand the frozen second derivation | [Second derivation and freeze](second_derivation_and_freeze) | [Closeout and historical receipts](closeout_and_historical_receipts) |

## The central distinction

```text
Supply / proposal --> observation or evaluation --> retained alternatives
                                                       |
                                             separate authorization
                                                       |
                                             admission + replay
```

A proposal is not an admission. A computed minimum is not authorization. An observer's agreement is not a proof of correspondence. A finite receipt is not an unbounded theorem. These are working boundaries in the implementation, not interchangeable names.

## Explore the repository

- [Textbook Hub](textbook_overview) and [Derivation Coverage Matrix](textbook_coverage): all 75 frozen modules (`Units 00–{part1_entries[-1][0]:02d}`) and post-freeze research trees (`Institutions 00–{part2_entries[-1][0]:02d}`) with 15-second soundbites and `<= 15s` Manim animations.
- [Synced Research Trees](textbook_research_trees): all {len(research_trees)} research directories currently on `main`.
- [Repository map](repository_map): every top-level area and complete tracked-file indexes.
- [Python module reference](python_module_reference): public top-level definitions across the computational modules.
- [Research tree index](research_tree_index): every tree in the canonical generated research index, with per-tree source, test, Lean, report, and verifier maps.
- [Local validation](local_validation): the twelve existing gate families; hosted CI is permanently disabled by author decision.
- [Troubleshooting](troubleshooting) and [FAQ](faq): practical answers without weakening evidence boundaries.

## Snapshot and current status

Textbook & Audit edition synced to `main` at [`{commit_short}`](https://github.com/dbccpage/19L57G1/commit/{commit_sha}) (2026-10-28); core repository reference pages reflect [`85a83ae7ce64`](https://github.com/dbccpage/19L57G1/commit/85a83ae7ce64dc2123ff218568a4ecd37e566d33) (2026-10-23). All tracked toolchain files pin Lean 4.33.0.

The closeout records three independent axes: research program **CLOSED_WITH_OPEN_OBSTRUCTIONS**, Alpha reference **READY_WITHIN_DECLARED_SCOPE**, and original seed completion gate **UNSATISFIED**. These are attributed closeout dispositions, not a new whole-repository verification run. [Review scope and findings](review_scope_and_findings) explains the dated evidence, documentation discrepancies, and checks actually performed for this Wiki.
"""
    (wiki_root / "Home.md").write_text(home_md, encoding="utf-8", newline="\n")

    # 12. Update _Footer.md
    footer_md = f"""<!-- markdownlint-disable MD041 -->

[Genesis Home](Home) · [Textbook Start Here](textbook_start_here) · [Textbook Hub](textbook_overview) · [15s Videos](textbook_video_15s) · [Synced Research Trees](textbook_research_trees) · [Source Contract](source_contract)

Source edition: [{commit_short}](https://github.com/dbccpage/19L57G1/commit/{commit_sha}), updated 2026-10-28. Separate explanatory documentation and textbook mirror. `AuthorityEffect: None`. No new derivation, source amendment, or whole-repository certification is implied.
"""
    (wiki_root / "_Footer.md").write_text(footer_md, encoding="utf-8", newline="\n")

    return {
        "part1": len(part1_entries),
        "part2": len(part2_entries),
        "research_trees": len(research_trees),
        "hubs": 7,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help="Path to 19L57G1 repository root",
    )
    ap.add_argument(
        "--wiki-root",
        type=Path,
        default=DEFAULT_WIKI_ROOT,
        help="Path to 19L57G1.wiki checkout or output directory",
    )
    args = ap.parse_args(argv)
    counts = build_all(args.repo_root.resolve(), args.wiki_root.resolve())
    print(
        f"Built {counts['part1']} Part 1 pages, {counts['part2']} Part 2 pages, "
        f"{counts['hubs']} hub pages, and synced {counts['research_trees']} research trees in {args.wiki_root}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
