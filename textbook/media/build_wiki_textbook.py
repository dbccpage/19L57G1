"""Build Genesis Textbook Wiki pages with complete lessons first, followed by
optional reading prompts, source records and <=15s Manim videos.

AuthorityEffect: None. Mirrors textbook/ and research tree metadata into
19L57G1.wiki.git without altering any sealed derivation file. Follows Claim
Hygiene strictly. Re-run whenever new textbook units or research trees are added
to main.
"""

from __future__ import annotations

import argparse
import os
import posixpath
import re
import subprocess
from pathlib import Path

from research_population import research_trees
from first_steps_wiki import build_first_steps
from search_lab_wiki import build_search_lab
from change_lab_wiki import build_change_lab
from reasoning_lab_wiki import build_reasoning_lab
from path_lab_wiki import build_path_lab
from map_lab_wiki import build_map_lab
from growth_lab_wiki import build_growth_lab
from boundary_lab_wiki import build_boundary_lab
from identification_lab_wiki import build_identification_lab
from number_lab_wiki import build_number_lab

DEFAULT_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_WIKI_ROOT = Path(
    os.environ.get(
        "GENESIS_WIKI_ROOT",
        str(DEFAULT_REPO_ROOT.parent / "19L57G1.wiki"),
    )
)
RAW_WIKI_MEDIA = "https://raw.githubusercontent.com/wiki/dbccpage/19L57G1/media/manim"
BEGINNER_ROUTES = ('first_steps', 'reasoning_lab', 'search_lab', 'change_lab',
                   'path_lab', 'map_lab', 'growth_lab', 'boundary_lab', 'identification_lab', 'number_lab')
READING_GUIDES = {
    'state_history_practice.md': 'textbook_state_history_practice',
    'state_history_answers.md': 'textbook_state_history_answers',
    'core_start_practice.md': 'textbook_core_start_practice',
    'core_start_answers.md': 'textbook_core_start_answers',
    'learning_path.md': 'textbook_learning_path',
    'reading_formal_statements.md': 'textbook_reading_formal',
    'reading_formal_practice.md': 'textbook_reading_formal_practice',
    'reading_formal_answers.md': 'textbook_reading_formal_answers',
}


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
    raise RuntimeError(f"Cannot resolve the source commit for {repo_root}; refusing to invent a snapshot pin")


def first_sentences(text: str, max_words: int = 34) -> str:
    """Keep complete prose sentences; never truncate a hypothesis or Markdown."""
    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    prose = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", prose)
    prose = re.sub(r"`+", "", prose).replace("|", "&#124;")
    prose = re.sub(r"(?m)^\s*(?:[-*>]+|\d+\.)\s+", "", prose)
    clean = re.sub(r"\s+", " ", prose.strip())
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", clean)
    selected: list[str] = []
    for sentence in sentences:
        if len(" ".join([*selected, sentence]).split()) > max_words:
            break
        selected.append(sentence)
    return " ".join(selected) or "Read the complete statement below for its definitions, hypotheses, and scope."


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
            "Act VIII · Effect Classes, Repeated Events & Interpreter Boundary (Units 57–58, 65–66)",
            "Thirteen effect classes summarize individual transitions; repeated concrete events are idempotent. A notes-diagonal escapes the separate 64-descriptor family without establishing an operational interpreter bridge.",
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
        "Exact acquisition of an arbitrary unknown actor partition has worst-case cost n(n-1)/2 pair probes, refutes the promised-count shortcut at n = N, characterizes uncollapse by mention delta, and locates the verdict-level interpreter boundary.",
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
    top_block = re.split(r"(?m)^## ", "\n".join(lines[1:]), maxsplit=1)[0]

    claim_m = re.search(
        r"\*\*Claim\.\*\*\s*(.+?)(?=\n\*\*|\n\n|\Z)", top_block, re.DOTALL
    )
    table_claim = re.search(r"(?m)^\|\s*\*\*Claim\*\*\s*\|\s*(.*?)\s*\|$", top_block)
    claim = claim_m.group(1).strip() if claim_m else (table_claim.group(1) if table_claim else "See the complete claim below.")
    claim = re.sub(r"\s+", " ", claim)

    status_m = re.search(r"\*\*Status:\*\*\s*(.+?)(?=\s+\*\*|\n\n|\Z)", top_block, re.DOTALL)
    table_status = re.search(r"(?m)^\|\s*\*\*Mark\*\*\s*\|\s*(.*?)\s*\|$", top_block)
    status = re.sub(r"\s+", " ", status_m.group(1)).strip().rstrip(".") if status_m else (table_status.group(1) if table_status else "See unit classification")

    lean_m = re.search(r"\*\*Lean:\*\*\s*(.+?)(?=\s+\*\*|\n\n|\Z)", top_block, re.DOTALL)
    lean = re.sub(r"\s+", " ", lean_m.group(1)).strip().rstrip(".") if lean_m else "See formal sources in the complete unit"

    return {
        "title": title,
        "claim": claim,
        "status": status,
        "lean": lean,
    }


def rewrite_links_for_wiki(
    md: str,
    part1_map: dict[str, str],
    part2_map: dict[str, str],
    blob_base: str,
    is_part2: bool,
    source_dir: str = "textbook",
) -> str:
    """Resolve links against the source directory before mapping Wiki pages."""
    targets = {f"textbook/units/{name}": slug for name, slug in part1_map.items()}
    targets.update({f"textbook/institutions/units/{name}": slug for name, slug in part2_map.items()})
    targets.update({"textbook/START_HERE.md": "textbook_start_here",
                    "textbook/README.md": "textbook_overview",
                    "textbook/institutions/README.md": "textbook_institutions",
                    "textbook/video_script_15s.md": "textbook_video_15s",
                    "textbook/derivation_coverage.md": "textbook_coverage",
                    "textbook/audit/README.md": "textbook_audit"})
    targets.update({'textbook/'+name: slug for name, slug in READING_GUIDES.items()})

    def rewrite(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        if target.startswith(("https://", "http://", "mailto:", "#", "textbook_")):
            return match.group(0)
        if target in ("Home", "genesis_overview", "getting_started", "worked_examples",
                      "concepts_and_glossary", "repository_map"):
            return match.group(0)
        path, sep, anchor = target.partition("#")
        resolved = posixpath.normpath(posixpath.join(source_dir, path))
        parts = resolved.split('/')
        if (len(parts) == 3 and parts[0] == 'textbook' and parts[1] in BEGINNER_ROUTES
                and parts[2].endswith('.md') and not parts[2].startswith('REVIEW_')):
            stem = parts[2][:-3]
            dest = 'textbook_'+parts[1]+('' if stem == 'README' else '_'+stem.lower())
            return f"]({dest}{sep}{anchor})"
        dest = targets.get(resolved, f"{blob_base}/{resolved}")
        return f"]({dest}{sep}{anchor})"

    # Examples inside fenced code are literal text, not navigable links.
    pieces = re.split(r"(```.*?```)", md, flags=re.DOTALL)
    return "".join(piece if piece.startswith("```") else re.sub(r"\]\(([^)]+)\)", rewrite, piece)
                   for piece in pieces)


def first_pass_heading(raw_md: str) -> str:
    headings = re.findall(r'^## (First pass[^\n]*)$', raw_md, re.MULTILINE)
    if len(headings) != 1:
        raise ValueError('Expected one First pass heading')
    return headings[0]


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
    act_slug, act_title, _ = (
        act_for_part2(unit_idx) if is_part2 else act_for_part1(unit_idx)
    )
    part_label = "Part 2 · Institutions" if is_part2 else "Part 1 · Derivation"
    unit_code = f"I{unit_idx:02d}" if is_part2 else f"U{unit_idx:02d}"
    source_dir = "textbook/institutions/units" if is_part2 else "textbook/units"
    unit_map = part2_map if is_part2 else part1_map
    names = [name for name in unit_map if re.match(rf"^{unit_idx:02d}_", name)]
    if len(names) != 1:
        raise ValueError(f"Expected one source file for {unit_code}, got {names}")
    source_url = f"{blob_base}/{source_dir}/{names[0]}"
    first_pass_heading(raw_md)
    nav_prev = f"[◀ {prev_link[0]}]({prev_link[1]})" if prev_link else "[◀ Start Here](textbook_start_here)"
    nav_next = f"[{next_link[0]} ▶]({next_link[1]})" if next_link else "[Textbook Hub ▶](textbook_overview)"
    navigation = f"{nav_prev} · [Reading path](textbook_learning_path) · [Read the notation](textbook_reading_formal) · [Textbook Hub](textbook_overview) · {nav_next}"
    rewritten_body = rewrite_links_for_wiki(
        raw_md, part1_map, part2_map, blob_base, is_part2, source_dir,
    )
    return f"""<!-- markdownlint-disable MD041 MD033 -->

{navigation}

`{part_label}` · `{unit_code}` · Lesson {unit_idx + 1} of {total_units}

Begin with the **First pass** example below. The lesson states its definitions, conditions and limits.

{rewritten_body}

---

<details>
<summary>Act video (optional)</summary>

**{act_title}**

This video previews several lessons. Pause it as needed and use the worked examples above for this Unit's conditions and reasoning.

![{act_title} — 15s Manim Visual]({RAW_WIKI_MEDIA}/{act_slug}.gif)

[Watch or download the MP4]({RAW_WIKI_MEDIA}/{act_slug}.mp4) · Verified duration at most 15 seconds · [All Act videos](textbook_video_15s)

</details>

<details>
<summary>Questions to use while reading (optional)</summary>

1. What are the inputs and the question in this lesson?
2. Which definitions or rules were supplied?
3. Which conditions are needed for the stated conclusion?
4. Can you explain the worked example, then change one part?
5. What evidence supports the claim, and what remains unestablished?

</details>

<details>
<summary>Source edition and checks (optional)</summary>

This page preserves the complete lesson from [source edition `{commit_short}`]({source_url}). The lesson names its definitions, proof sources and local checks. Publishing a page does not run those checks.

[Coverage map](textbook_coverage) · [Research trees](textbook_research_trees) · `AuthorityEffect: None`

</details>

---

{navigation}
"""


def discover_research_trees(repo_root: Path) -> list[tuple[str, bool, bool]]:
    """Return the canonical tracked-tree population and file-presence flags."""
    return research_trees(repo_root)


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
        "standing_commitment": "[Growth lab: introductory lessons](textbook_growth_lab)",
        "boundary_seed": "[Boundary lab: declared division and readings](textbook_boundary_lab_00_start_before_the_marks)",
        "side_free": "[Boundary lab: permission and price menu](textbook_boundary_lab_04_price_a_fixed_menu)",
        "oriented_boundary": "[Boundary lab: stipulated report model](textbook_boundary_lab_02_compare_two_answers)",
        "identification_dual": "[Same-record lab: selected matching examples](textbook_identification_lab)",
        "qm_bridge": "[Number lab: selected finite readout examples](textbook_number_lab_05_two_coordinates)",
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
> ### ⚡ Post-Seal Research Trees at source snapshot (`{commit_short}`)
> This page is regenerated by `python textbook/media/build_wiki_textbook.py`. It inventories all **{len(research_trees)}** research trees listed under [`research/`]({blob_base}/research) and links dedicated [institution lessons](textbook_institutions), the [Growth lab](textbook_growth_lab), and selected [Boundary lab](textbook_boundary_lab), [Same-record lab](textbook_identification_lab), and [Number lab](textbook_number_lab) introductions. A directory or source link is not validation or complete teaching coverage. `AuthorityEffect: None`.

---

## Research Trees at the source snapshot (`{len(research_trees)}` Trees)

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

[Genesis Wiki](Home) · [Textbook hub](textbook_overview) · [Reading formal statements](textbook_reading_formal) · [Video gallery](textbook_video_15s)

{start_rewritten}

---

## Optional video preview

This short Act overview previews the source's opening chapters. Take the
time each written definition needs; the video duration is not a reading target.

![The opaque mark and the admitted formal representation]({RAW_WIKI_MEDIA}/act00_pre_genesis_mark.gif)

[Watch or download the MP4]({RAW_WIKI_MEDIA}/act00_pre_genesis_mark.mp4) · [Read the spoken script](textbook_video_15s).
The existing media verifier checks the video and GIF durations.

Source edition: [{commit_short}](https://github.com/dbccpage/19L57G1/commit/{commit_sha}). Teaching apparatus; `AuthorityEffect: None`.
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
> ### 🎬 Video previews are `<= 15 Seconds`; written lessons are self-paced
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
> ### Begin with a concrete example (`AuthorityEffect: None`)
> - **Part 1 ([Units 00–{part1_entries[-1][0]:02d}](textbook_u00_mark_and_constructor)):** Formal chapters and a source-placement map for **75 frozen Lean 4 modules** in `lean4/Derivation/`. A source reference does not certify complete teaching coverage.
> - **Part 2 ([Institutions 00–{part2_entries[-1][0]:02d}](textbook_institutions)):** Post-freeze research suites (`actor_institution`, `two_theorems`, `uncollapse`, `interpreter_verdict`) plus the synced [Research Trees Index](textbook_research_trees).
> - **How to study:** Start with **[First steps](textbook_first_steps)** and **[Start Here](textbook_start_here)**. Work through examples and predictions at your own pace, then inspect the definitions, hypotheses, Python, and Lean. Short Act videos are previews, not a study-time target.

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
        inst_readme_raw, part1_map, part2_map, blob_base, True, "textbook/institutions"
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
> ### Part 2: Actors & Institutions (`Units 00–{part2_entries[-1][0]:02d}`)
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
> ### Derivation source-placement map (`AuthorityEffect: None`)
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
        audit_raw, part1_map, part2_map, blob_base, False, "textbook/audit"
    )
    audit_page = f"""<!-- markdownlint-disable MD041 MD033 -->

[🏠 Genesis Wiki Home](Home) · [🚀 Start Here](textbook_start_here) · [📚 Textbook Hub](textbook_overview) · [🗺️ Coverage Matrix](textbook_coverage) · **[🔍 75-Module Source Audit](textbook_audit)** · [🌲 Research Trees](textbook_research_trees)

---

> [!IMPORTANT]
> ### 75-module source audit (`AuthorityEffect: None`)
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

- [Start here](textbook_start_here)
- [Read a formal statement, one piece at a time](textbook_reading_formal)
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

> [!TIP]
> **What you'll take away:** A proposal is not an admission. A computed minimum is not authorization. A finite receipt is not an unbounded theorem.
>
> **Ten minutes:** [First steps](textbook_first_steps) → [Presentations and families]({part2_entries[0][2]}) → [Limitations](limitations_and_open_obligations).
>
> **The full course:** {len(part1_entries) + len(part2_entries)} units; the claim ledgers say which results are Lean-checked and which remain open.

Genesis (`19L57G1`) studies what follows from an opaque seed `<>` under declared finite challenges, what has to be admitted separately, and where the evidence stops. It contains a replayable admission kernel, deterministic searches, Lean 4 proofs, claim ledgers, a **{len(part1_entries) + len(part2_entries)}-unit formal textbook** with separate beginner routes, and a post-seal research estate.

This Wiki is an explanatory map and mirrored textbook of the published repository, not an amendment to its sealed experiment, a new derivation, or a certification of all its claims. `AuthorityEffect: None`.

---

> [!IMPORTANT]
> ### New to Genesis? Start with a concrete question
> **No prior study is assumed.** Start with concrete examples, then read the definitions and formal statements in order. The short videos preview groups of lessons; pause them and take as much time as each explanation needs.
>
> 👉 **[Start here](textbook_start_here)** · **[📚 Textbook Hub (Units 00–{part1_entries[-1][0]:02d})](textbook_overview)** · **[🏛️ Part 2: Actors & Institutions (00–{part2_entries[-1][0]:02d})](textbook_institutions)** · **[🎬 15s Manim Video Gallery](textbook_video_15s)** · **[🌲 Synced Research Trees ({len(research_trees)})](textbook_research_trees)**

![Pre-Genesis and the Opaque Mark <> (15s Manim Visual)]({RAW_WIKI_MEDIA}/act00_pre_genesis_mark.gif)

---

## Start with your question

| I want to... | Start here | Continue with |
| --- | --- | --- |
| **Learn through small worked examples at your own pace** | **[First steps](textbook_first_steps)** | **[Textbook: Start Here](textbook_start_here)**, **[Textbook Hub](textbook_overview)**, **[Video previews](textbook_video_15s)** |
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

- [Textbook Hub](textbook_overview) and [Derivation Coverage Matrix](textbook_coverage): formal chapters, a source-placement map for 75 frozen modules, selected research lessons, and `<= 15s` video previews. Written study has no time target; source placement is not complete teaching coverage.
- [Synced Research Trees](textbook_research_trees): all {len(research_trees)} research directories at this source snapshot.
- [Repository map](repository_map): every top-level area and complete tracked-file indexes.
- [Python module reference](python_module_reference): public top-level definitions across the computational modules.
- [Research tree index](research_tree_index): every tree in the canonical generated research index, with per-tree source, test, Lean, report, and verifier maps.
- [Local validation](local_validation): the twelve existing gate families; hosted CI is permanently disabled by author decision.
- [Troubleshooting](troubleshooting) and [FAQ](faq): practical answers without weakening evidence boundaries.

## Snapshot and current status

Textbook & Audit edition generated from source snapshot [`{commit_short}`](https://github.com/dbccpage/19L57G1/commit/{commit_sha}); core repository reference pages reflect [`85a83ae7ce64`](https://github.com/dbccpage/19L57G1/commit/85a83ae7ce64dc2123ff218568a4ecd37e566d33) (2026-10-23). All tracked toolchain files pin Lean 4.33.0.

The closeout records three independent axes: research program **CLOSED_WITH_OPEN_OBSTRUCTIONS**, Alpha reference **READY_WITHIN_DECLARED_SCOPE**, and original seed completion gate **UNSATISFIED**. These are attributed closeout dispositions, not a new whole-repository verification run. [Review scope and findings](review_scope_and_findings) explains the dated evidence, documentation discrepancies, and checks actually performed for this Wiki.
"""
    (wiki_root / "Home.md").write_text(home_md, encoding="utf-8", newline="\n")

    # 12. Update _Footer.md
    footer_md = f"""<!-- markdownlint-disable MD041 -->

[Genesis Home](Home) · [Textbook Start Here](textbook_start_here) · [Textbook Hub](textbook_overview) · [15s Videos](textbook_video_15s) · [Synced Research Trees](textbook_research_trees) · [Source Contract](source_contract)

Source edition: [{commit_short}](https://github.com/dbccpage/19L57G1/commit/{commit_sha}), updated 2026-10-28. Separate explanatory documentation and textbook mirror. `AuthorityEffect: None`. No new derivation, source amendment, or whole-repository certification is implied.
"""
    (wiki_root / "_Footer.md").write_text(footer_md, encoding="utf-8", newline="\n")

    # Curated explanations live beside this generator so regeneration keeps
    # their wording fixes. Their historical source links retain their pins.
    for guide in sorted((repo_root / "textbook/media/wiki_guides").glob("*.md")):
        (wiki_root / guide.name).write_text(
            guide.read_text(encoding="utf-8"), encoding="utf-8", newline="\n"
        )

    for name, slug in READING_GUIDES.items():
        source = repo_root / 'textbook' / name
        body = rewrite_links_for_wiki(source.read_text(encoding='utf-8'), part1_map,
                                     part2_map, blob_base, False, 'textbook')
        prefix = '[Genesis Wiki](Home) · [Start here](textbook_start_here) · [Reading formal statements](textbook_reading_formal)\n\n'
        suffix = f'\n\n---\n\nSource snapshot: [`{commit_short}`]({blob_base}/textbook/{name}). Teaching apparatus; `AuthorityEffect: None`.\n'
        (wiki_root / (slug+'.md')).write_text(prefix+body+suffix,encoding='utf-8',newline='\n')

    return {
        "part1": len(part1_entries),
        "part2": len(part2_entries),
        "research_trees": len(research_trees),
        "hubs": 7,
        "first_steps": build_first_steps(repo_root, wiki_root, commit_sha),
        "search_lab": build_search_lab(repo_root, wiki_root, commit_sha),
        "change_lab": build_change_lab(repo_root, wiki_root, commit_sha),
        "reasoning_lab": build_reasoning_lab(repo_root, wiki_root, commit_sha),
        "path_lab": build_path_lab(repo_root, wiki_root, commit_sha),
        "map_lab": build_map_lab(repo_root, wiki_root, commit_sha),
        "growth_lab": build_growth_lab(repo_root, wiki_root, commit_sha),
        "boundary_lab": build_boundary_lab(repo_root, wiki_root, commit_sha),
        "identification_lab": build_identification_lab(repo_root, wiki_root, commit_sha),
        "number_lab": build_number_lab(repo_root, wiki_root, commit_sha),
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
