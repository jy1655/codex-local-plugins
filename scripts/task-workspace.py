#!/usr/bin/env python3
"""Create task directories and account for verification files without deleting them.

Readback provenance and retention eligibility are the caller's responsibility. This
tool checks bytes, paths and disposition; it does not authenticate a Wiki response.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile

MARKER = ".task-workspace.json"


def fingerprint(path: Path) -> dict:
    before = path.stat()
    if path.is_symlink() or not stat.S_ISREG(before.st_mode):
        raise ValueError(f"not a regular file: {path}")
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(block)
            digest.update(block)
    after = path.stat()
    if (before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
        raise ValueError(f"file changed while hashing: {path}")
    return {"size": size, "sha256": digest.hexdigest()}


def delivery_path(path: Path, roots: list[Path]) -> bool:
    # Check the spelling AND resolved ancestors: neither an alias into output nor
    # an output symlink pointing elsewhere should silently bypass the choice.
    lexical = Path(os.path.abspath(path.expanduser()))
    resolved = lexical.resolve()
    return any(part.casefold() == "output" for p in (lexical, resolved) for part in p.parts) or any(
        resolved == root.resolve() or root.resolve() in resolved.parents for root in roots
    )


def save(root: Path, state: dict) -> None:
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=root, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            json.dump(state, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        except BaseException:
            temporary.unlink()
            raise
    try:
        temporary.replace(root / MARKER)
    finally:
        temporary.unlink(missing_ok=True)


def load(root: Path) -> dict:
    marker = root / MARKER
    if marker.is_symlink():
        raise ValueError("workspace marker must not be a symlink")
    state = json.loads(marker.read_text(encoding="utf-8"))
    if state.get("version") != 1 or state.get("root") != str(root) or state.get("purpose") != "verification":
        raise ValueError("not a verification workspace created by this tool")
    return state


def scan(root: Path) -> dict[str, dict]:
    def fail(error: OSError) -> None:
        raise error

    files = {}
    for directory, dirs, names in os.walk(root, followlinks=False, onerror=fail):
        parent = Path(directory)
        for name in dirs:
            if (parent / name).is_symlink():
                raise ValueError(f"symlink directory requires manual handling: {parent / name}")
        for name in names:
            path = parent / name
            if path == root / MARKER:
                continue
            files[path.relative_to(root).as_posix()] = fingerprint(path)
    return files


def observe(state: dict, current: dict) -> None:
    # Keep disappeared observations: removing an unclassified file is not closure.
    for name, identity in current.items():
        previous = state["files"].get(name)
        if previous is None or any(previous.get(k) != v for k, v in identity.items()):
            state["files"][name] = dict(identity)


def report(state: dict, current: dict) -> dict:
    unresolved = []
    for name, entry in sorted(state["files"].items()):
        disposition = entry.get("disposition")
        if disposition is None:
            unresolved.append({"path": name, "status": "unclassified" if name in current else "unclassified-missing"})
        elif disposition in {"wiki", "discard"} and name in current:
            unresolved.append({"path": name, "status": "pending-removal", "disposition": disposition})
        elif disposition == "keep" and name not in current:
            unresolved.append({"path": name, "status": "retained-file-missing"})
    return {"root": state["root"], "files": state["files"], "unresolved": unresolved, "complete": not unresolved}


def create(args: argparse.Namespace) -> int:
    if args.user_selected_path and args.path is None:
        raise ValueError("--user-selected-path requires --path")
    if args.purpose == "deliverable" and args.path is None:
        raise ValueError("deliverable requires an explicit --path")
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", args.name):
        raise ValueError("name must be a simple task name, without path separators")
    base = Path(args.path).expanduser() if args.path else Path(tempfile.gettempdir())
    if args.purpose == "verification" and delivery_path(base, [Path(p).expanduser() for p in args.delivery_root]):
        if not args.user_selected_path:
            raise ValueError("verification destination is under output/delivery root; use a temporary directory, or --user-selected-path only for a user's explicit choice")
    if args.path:
        root = base.resolve()
        root.mkdir(parents=True, exist_ok=False)
    else:
        root = Path(tempfile.mkdtemp(prefix=f"{args.name}-", dir=base)).resolve()
    if args.purpose == "verification":
        save(root, {"version": 1, "root": str(root), "purpose": args.purpose,
                    "user_selected_path": args.user_selected_path, "files": {}})
    print(root)
    return 0


def manage(args: argparse.Namespace) -> int:
    root = Path(args.workspace).expanduser().resolve()
    state = load(root)
    current = scan(root)
    observe(state, current)
    if args.command == "classify":
        file = Path(args.file)
        if file.is_absolute() or ".." in file.parts:
            raise ValueError("file must be a workspace-relative path without '..'")
        name = file.as_posix()
        if name not in current:
            raise ValueError("classify an existing file before removing it")
        if not args.reason.strip():
            raise ValueError("a disposition reason is required")
        # Reclassification must not carry an earlier Wiki receipt into a different disposition.
        entry = state["files"][name] = dict(current[name])
        entry.update(disposition=args.disposition, reason=args.reason)
        if args.disposition == "wiki":
            if not args.wiki_path or not args.readback:
                raise ValueError("wiki disposition requires --wiki-path and --readback")
            target = Path(args.wiki_path)
            if target.is_absolute() or ".." in target.parts or not args.wiki_path.startswith("raw/"):
                raise ValueError("wiki-path must be a relative raw/ file")
            readback = Path(args.readback).expanduser().resolve()
            if readback == (root / name).resolve() or readback.samefile(root / name):
                raise ValueError("readback must be a separately fetched Wiki copy")
            if fingerprint(readback) != current[name]:
                raise ValueError("Wiki readback size/SHA-256 does not match the source bytes")
            entry.update(wiki_path=target.as_posix(), readback_verified=True)
        elif args.wiki_path or args.readback:
            raise ValueError("Wiki options require the wiki disposition")
    result = report(state, current)
    save(root, state)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if args.command == "finish" and not result["complete"] else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    make = commands.add_parser("create", help="create a new task directory; verification defaults to OS temp")
    make.add_argument("--purpose", required=True, choices=("verification", "deliverable"))
    make.add_argument("--name", default="verification")
    make.add_argument("--path")
    make.add_argument("--delivery-root", action="append", default=[], help="additional delivery root to protect")
    make.add_argument("--user-selected-path", action="store_true", help="the user explicitly selected this destination")
    for name in ("inventory", "classify", "finish"):
        command = commands.add_parser(name)
        command.add_argument("workspace")
        if name == "classify":
            command.add_argument("--file", required=True)
            command.add_argument("--disposition", choices=("wiki", "discard", "keep"), required=True)
            command.add_argument("--reason", required=True)
            command.add_argument("--wiki-path")
            command.add_argument("--readback", help="separately fetched Wiki file; bytes are compared without newline conversion")
    args = parser.parse_args(argv)
    try:
        return create(args) if args.command == "create" else manage(args)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
