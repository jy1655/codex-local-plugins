#!/usr/bin/env python3
"""Run local SkillSpector static analysis without inherited LLM/tracing secrets."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys


def scanner_environment(environ: dict[str, str]) -> dict[str, str]:
    # Preserve actual home/system paths, not provider credentials or trace endpoints.
    keys = {
        "PATH", "HOME", "LANG", "LC_ALL", "TMPDIR", "TMP", "TEMP",
        "SYSTEMROOT", "WINDIR", "USERPROFILE", "APPDATA", "LOCALAPPDATA",
        "SSL_CERT_FILE", "SSL_CERT_DIR",
    }
    result = {key: value for key, value in environ.items() if key.upper() in keys}
    result.update(LANGSMITH_TRACING="false", LANGCHAIN_TRACING_V2="false",
                  DO_NOT_TRACK="1")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args(argv)
    target = args.skill.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if not (target / "SKILL.md").is_file():
        parser.error("skill must be a local directory containing SKILL.md")
    if target == output or target in output.parents:
        parser.error("output must be outside the inspected skill directory")
    if not output.parent.is_dir() or output.exists():
        parser.error("output must be a new file in an existing verification directory")
    if args.timeout <= 0:
        parser.error("timeout must be positive")
    executable = shutil.which("skillspector")
    if executable is None:
        print("NOT-RUN: skillspector is not installed; continue source review.", file=sys.stderr)
        return 127
    command = [executable, "scan", str(target), "--no-llm", "--format", "json",
               "--output", str(output), "--fail-on-incomplete"]
    try:
        return subprocess.run(command, cwd=output.parent,
                              env=scanner_environment(dict(os.environ)),
                              timeout=args.timeout, check=False).returncode
    except subprocess.TimeoutExpired:
        print("FAILED: SkillSpector timed out; any report may be incomplete.", file=sys.stderr)
        return 124
    except OSError as exc:
        print(f"FAILED: could not run SkillSpector: {exc}", file=sys.stderr)
        return 126


if __name__ == "__main__":
    raise SystemExit(main())
