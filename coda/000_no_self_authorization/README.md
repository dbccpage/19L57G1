# NSA-000 — Better Than What?

**Title:** Better Than What? Measuring the Gap Between Evaluation and Selection
**Author:** Jeremy H. Carroll
**Status:** Pre-print draft (v0.1). No DOI until the author mints Zenodo.
**AuthorityEffect:** `None`

## Ladder

| Tier | Surface |
| --- | --- |
| 1. Pictures | `public_export/fig_sandcastles.png`, `fig_tie.png` |
| 2. Enter / break | `jupyter_notebooks/00_enter_nsa000.ipynb`, `01_falsify_nsa000.ipynb` |
| 3. Monograph | `000_no_self_authorization.md`, claim ledger, change log |
| Public face | `linkedin_essay.md` (boring on purpose) |
| Attacks | `attack_list.md` — unanswered rows first |
| Situating | `situating.md` — permitted, not written |

```text
Paper claim (ledger row)
        │
        ├─► Python illustration   src/nsa000/   ── pytest tests/
        └─► Jupyter               00_enter / 01_falsify
```

Lean is not in this package. Cited counts are sealed-derivation
keys in `coda/figures.md`.

## Run

From this folder:

```powershell
$env:PYTHONPATH = "src"
python -m pytest tests -q
python -m coverage run -m pytest tests -q
python -m coverage report --fail-under=100
python -m coverage run -m pytest tests -q; python src/nsa000/../nsa000 2>$null
python -c "from pathlib import Path; from nsa000.figures import write_default; write_default(Path('public_export'))"
public_export\run_paper.bat
```

```bash
PYTHONPATH=src python -m pytest tests -q
PYTHONPATH=src python -m coverage run -m pytest tests -q
PYTHONPATH=src python -m coverage report --fail-under=100
./public_export/run_paper.sh
```

## License

Text and figures: CC-BY-4.0. Code and notebooks: Apache-2.0.
