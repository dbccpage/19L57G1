from __future__ import annotations

import json

from occurrence_lane import symbol_packet


def main() -> int:
    print(json.dumps(symbol_packet(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
