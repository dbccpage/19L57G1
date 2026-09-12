"""Test suite for Target X303 (Bounded Operational Agency)."""

from pathlib import Path
import sys

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
_CODE_DIR = _REPO_ROOT / "code"
if str(_CODE_DIR) not in sys.path:
    sys.path.insert(0, str(_CODE_DIR))
_X301_DIR = _REPO_ROOT / "research" / "x301_formal_semantics"
if str(_X301_DIR) not in sys.path:
    sys.path.insert(0, str(_X301_DIR))
