#!/usr/bin/env python3
"""Keep Claude's effort override out of Codex shell children (Python 3.11+)."""

import argparse
import copy
import json
import os
from pathlib import Path
import re
import stat
import tempfile
import tomllib


VARIABLE = "CLAUDE_CODE_EFFORT_LEVEL"


def update(text: str) -> str:
    before = tomllib.loads(text)
    expected = copy.deepcopy(before)
    policy = expected.setdefault("shell_environment_policy", {})
    if "filters" in policy:
        raise ValueError("Use a keyed exclude filter in this config; do not mix filters and exclude arrays")
    if any(key.casefold() == VARIABLE.casefold() for key in policy.get("set", {})):
        raise ValueError("Remove the explicit effort override from shell_environment_policy.set first")
    exclusions = policy.setdefault("exclude", [])
    if not isinstance(exclusions, list) or not all(isinstance(item, str) for item in exclusions):
        raise ValueError("shell_environment_policy.exclude must be a string array")
    if any(item.casefold() == VARIABLE.casefold() for item in exclusions):
        return text
    exclusions.append(VARIABLE)
    assignment = "exclude = " + json.dumps(exclusions) + "\n"
    lines = text.splitlines(keepends=True)
    start = next((i for i, line in enumerate(lines)
                  if re.fullmatch(r"\s*\[shell_environment_policy\]\s*(?:#.*)?", line.strip())), None)
    if start is None:
        # A parent table may legally be defined after its existing .set child.
        result = text.rstrip("\r\n") + "\n\n[shell_environment_policy]\n" + assignment
    else:
        stop = next((i for i in range(start + 1, len(lines))
                     if lines[i].lstrip().startswith("[")), len(lines))
        key = next((i for i in range(start + 1, stop)
                    if re.match(r"\s*exclude\s*=", lines[i])), None)
        if key is None:
            lines.insert(start + 1, assignment)
        else:
            for end in range(key + 1, stop + 1):
                try:
                    tomllib.loads("".join(lines[key:end]))
                except tomllib.TOMLDecodeError:
                    continue
                lines[key:end] = [assignment]
                break
            else:
                raise ValueError("Cannot safely locate the existing exclude array")
        result = "".join(lines)
    if tomllib.loads(result) != expected:
        raise ValueError("Unsupported TOML layout; no configuration was changed")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "config.toml")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = args.config.expanduser().resolve()
    original = target.read_bytes() if target.exists() else b""
    desired = update(original.decode("utf-8")).encode("utf-8")
    if original == desired:
        print(f"current: {VARIABLE} excluded")
        return
    if args.check:
        parser.exit(1, f"missing: {VARIABLE} exclusion\n")
    target.parent.mkdir(parents=True, exist_ok=True)
    mode = stat.S_IMODE(target.stat().st_mode) if target.exists() else 0o600
    with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            os.chmod(temporary, mode)
            stream.write(desired)
            stream.flush()
            if (target.read_bytes() if target.exists() else b"") != original:
                raise RuntimeError("Configuration changed during sync; retry after reviewing it")
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
    print(f"updated: {VARIABLE} excluded in {target}")


if __name__ == "__main__":
    main()
