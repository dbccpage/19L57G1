"""Shared import of the research tree's own Python for part 2's checks.

AuthorityEffect: None. Puts `research/actor_institution/` on the path so a
check can `import model` and use the tree's definitions unchanged.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research" / "actor_institution"))
