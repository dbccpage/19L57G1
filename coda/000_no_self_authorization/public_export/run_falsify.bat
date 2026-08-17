@echo off
cd /d "%~dp0\.."
echo [NSA-000] falsify notebook — AuthorityEffect None
set PYTHONPATH=src
python -m jupyter notebook jupyter_notebooks\01_falsify_nsa000.ipynb
