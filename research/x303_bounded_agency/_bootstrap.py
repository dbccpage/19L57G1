"""Shared import bootstrap for this research tree. AuthorityEffect: None."""
from __future__ import annotations

from pathlib import Path
import sys

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
_CODE = _REPO_ROOT / "code"
if str(_CODE) not in sys.path:
    sys.path.insert(0, str(_CODE))
_X301 = _REPO_ROOT / "research" / "x301_formal_semantics"
if str(_X301) not in sys.path:
    sys.path.insert(0, str(_X301))
