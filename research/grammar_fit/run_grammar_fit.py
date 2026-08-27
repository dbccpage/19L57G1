"""Write the grammar-fit receipt."""

from __future__ import annotations

import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from grammar_fit import write_receipt


if __name__ == "__main__":
    print(write_receipt().as_posix())
