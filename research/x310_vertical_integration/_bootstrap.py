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

for _sub in (
    "target_a_execution",
    "p200_operational_protocols",
    "g014_observer_descent",
    "x300_observer_information",
    "x301_formal_semantics",
    "m114_solver_adapter",
    "x302_operational_reasoning",
    "x303_bounded_agency",
):
    _p = _REPO_ROOT / "research" / _sub
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import research.target_a_execution.runner as _tar_runner
sys.modules.setdefault("runner", _tar_runner)
import research.p200_operational_protocols.protocol as _p200_prot
sys.modules.setdefault("protocol", _p200_prot)
import research.p200_operational_protocols.embedded_observer as _p200_emb
sys.modules.setdefault("embedded_observer", _p200_emb)
