#!/usr/bin/env bash
cd "$(dirname "$0")/.."
echo "[NSA-000] enter notebook — AuthorityEffect None"
export PYTHONPATH=src
python -m jupyter notebook jupyter_notebooks/00_enter_nsa000.ipynb
