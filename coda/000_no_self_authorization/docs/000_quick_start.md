# Quick start — NSA-000

**AuthorityEffect:** None.

1. Open `jupyter_notebooks/00_enter_nsa000.ipynb` (or
   `public_export/run_paper.bat`).
2. Move the sandcastle sliders. Height and width elect opposite
   winners from the same two objects.
3. Open `01_falsify_nsa000.ipynb` and run the deliberate
   breaks: empty evaluation, pick not in the set, silent
   singleton from a three-way tie.
4. Read `000_no_self_authorization.md` if you want the
   measurement and the Hilbert stop.

```powershell
cd coda/000_no_self_authorization
$env:PYTHONPATH = "src"
python -m pytest tests -q
python -m coverage run -m pytest tests -q
python -m coverage report --fail-under=100
```
