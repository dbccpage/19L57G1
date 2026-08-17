@echo off
cd /d "%~dp0\.."
echo [NSA-000] enter notebook — AuthorityEffect None
set PYTHONPATH=src
python -m jupyter notebook jupyter_notebooks\00_enter_nsa000.ipynb
