"""允许 ``python -m agent_pitfalls_cli`` 启动。"""

from __future__ import annotations

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())