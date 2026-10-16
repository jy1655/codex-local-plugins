#!/usr/bin/env python3
"""Run bundled pstack tools using their existing system runtimes."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
TOOLS = {
    "check-plan": ("node", "poteto-mode/scripts/check-plan.mjs"),
    "worktree-audit": ("bash", "poteto-mode/scripts/worktree-audit.sh"),
    "log": ("bash", "show-me-your-work/scripts/log.sh"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tool", choices=TOOLS)
    parser.add_argument("args", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    executable, relative = TOOLS[args.tool]
    if shutil.which(executable) is None:
        parser.error(f"{args.tool} requires {executable} on PATH")
    source = ROOT / "references" / "skills" / relative
    return subprocess.run([executable, str(source), *args.args], check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
