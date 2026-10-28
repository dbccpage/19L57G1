# Genesis Textbook Media, Widgets, and GitHub Wiki Mirror (`<= 15s` Standard)

**AuthorityEffect: None.** These scripts and interactive widgets package the
textbook (`textbook/units/` and `textbook/institutions/units/`) into
fifteen-second soundbites, interactive stepping-stone widgets, and `<= 15.0s`
Manim 0.19.2 animations mirrored on the repository's GitHub Wiki
(`https://github.com/dbccpage/19L57G1/wiki`, under the second side-panel
subsection `## Textbook`).

Nothing in this directory is an input to `prompt/`, `paper/`, `code/`,
`lean4/Derivation/`, or `artifacts/`, and nothing here alters the sealed
derivation.

---

## Contents

| File | Purpose |
|---|---|
| [`render_manim_suite.py`](render_manim_suite.py) | Renders the 12 Act animations (`act00`–`act11`) in Manim 0.19.2 as `.mp4` and looping `.gif` files, and checks with `ffprobe` that every animation is `<= 15.0` seconds. |
| [`build_wiki_textbook.py`](build_wiki_textbook.py) | Mirrors all Part 1 units (`U00`–`U74+`), all Part 2 institution units (`I00`–`I17+`), the synced research trees page (`textbook_research_trees.md`), and 6 hub/map pages into `19L57G1.wiki.git`, placing `## Textbook` as the second subsection in `_Sidebar.md`. |
| [`verify_wiki_textbook.py`](verify_wiki_textbook.py) | Verifies the `_Sidebar.md` heading order, all mirrored unit pages, all synced research trees on `main`, all internal Wiki page links, and the `<= 15.0s` duration cap on all 12 Manim animations. |
| [`genesis_15s_explorer.html`](genesis_15s_explorer.html) | Self-contained interactive HTML widget providing a 12-Act fifteen-second soundbite tour, a prediction challenge with streak counter, a live Part 1 Regime simulator, and a Part 2 Actor/Institution sandbox. |

---

## Twelve-Act Manim Animation Suite (`<= 15.0s` Verified)

| Act | Units | Scene Slug | Verified Duration |
|---|---|---|---|
| Act I | `Start Here`, `U00`–`U04` | `act00_pre_genesis_mark` | `14.07s` (`<= 15.0s`) |
| Act II | `U05`–`U16` | `act01_tokens_erasure_collapse` | `12.07s` (`<= 15.0s`) |
| Act III | `U17`–`U26` | `act02_separation_and_minimality` | `12.00s` (`<= 15.0s`) |
| Act IV | `U27`–`U36` | `act03_quotients_counting_transport` | `10.93s` (`<= 15.0s`) |
| Act V | `U37`–`U43` | `act04_refusal_generator_capacity` | `11.73s` (`<= 15.0s`) |
| Act VI | `U44`–`U50` | `act05_represented_kernel_horizon` | `10.93s` (`<= 15.0s`) |
| Act VII | `U51`–`U56` | `act06_primitive_difference_apartness` | `10.93s` (`<= 15.0s`) |
| Act VIII | `U57`–`U58`, `U65`–`U66` | `act07_interpreter_controller_boundary` | `10.93s` (`<= 15.0s`) |
| Act IX | `U59`–`U64` | `act08_attachment_ladder_compression` | `10.93s` (`<= 15.0s`) |
| Act X | `U67`–`U74` | `act09_descent_relativity_fidelity` | `10.93s` (`<= 15.0s`) |
| Part 2 · Act XI | `I00`–`I11` | `act10_institutions_synergy_policy` | `11.13s` (`<= 15.0s`) |
| Part 2 · Act XII | `I12`–`I17` | `act11_probing_uncollapse_verdict` | `10.93s` (`<= 15.0s`) |

---

## Reproducing the Animations and Wiki Mirror

Whenever new textbook units (`textbook/units/*.md` or `textbook/institutions/units/*.md`) or research trees (`research/*/`) are added to `main`, `python ci/check_textbook.py` (part of `python ci/run_gates.py`) automatically runs `build_wiki_textbook.py` and `verify_wiki_textbook.py`. To update the live GitHub Wiki checkout (`19L57G1.wiki.git`):

```powershell
# 1. Render all 12 Manim scenes (requires Python 3.12 with manim 0.19.2 and ffmpeg)
py -3.12 textbook/media/render_manim_suite.py

# 2. Build all mirrored Wiki pages, research tree sync page, and _Sidebar.md
python textbook/media/build_wiki_textbook.py --wiki-root path/to/19L57G1.wiki

# 3. Verify _Sidebar.md heading order, research tree sync, internal links, and <=15.0s video durations
python textbook/media/verify_wiki_textbook.py --wiki-root path/to/19L57G1.wiki
```
