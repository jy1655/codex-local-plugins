from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .apply import MANIFEST_NAME, ApplyReport, apply_environment, bootstrap_environment
from .manifest import load_manifest
from .platforms import ManagedPaths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Portable Codex environment bootstrap and apply tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap = subparsers.add_parser("bootstrap", help="Clone the environment repo and apply it into the current home")
    bootstrap.add_argument("git_url", help="Git URL or local git path for the environment repo")
    bootstrap.add_argument("--home", help="Override the target home directory for testing")
    bootstrap.add_argument("--os-name", choices=["darwin", "linux", "windows"], help="Override detected platform")

    apply_cmd = subparsers.add_parser("apply", help="Apply the environment from an existing repo checkout")
    apply_cmd.add_argument("--repo-root", default=".", help="Path to the environment repo checkout")
    apply_cmd.add_argument("--home", help="Override the target home directory for testing")
    apply_cmd.add_argument("--os-name", choices=["darwin", "linux", "windows"], help="Override detected platform")

    inspect = subparsers.add_parser("inspect", help="Show resolved paths and manifest contents")
    inspect.add_argument("--repo-root", default=".", help="Path to the environment repo checkout")
    inspect.add_argument("--home", help="Override the target home directory for testing")
    inspect.add_argument("--os-name", choices=["darwin", "linux", "windows"], help="Override detected platform")
    return parser


def _render_report(report: ApplyReport) -> str:
    lines = [
        f"repo: {report.repo_root}",
        f"os: {report.os_name}",
    ]
    if report.managed_repo is not None:
        lines.append(f"managed_repo: {report.managed_repo}")
    lines.append(f"marketplace: {report.marketplace_action}")

    lines.append("plugins:")
    for item in report.plugins:
        lines.append(f"  - {item.name}: {item.action} ({item.detail}) -> {item.destination}")

    lines.append("instructions:")
    for item in report.instructions:
        lines.append(f"  - {item.name}: {item.action} ({item.detail}) -> {item.destination}")

    lines.append("next_step: start a fresh Codex session to pick up plugin and instruction changes")
    return "\n".join(lines)


def command_bootstrap(args: argparse.Namespace) -> int:
    report = bootstrap_environment(args.git_url, home=args.home, os_name=args.os_name)
    print(_render_report(report))
    return 0


def command_apply(args: argparse.Namespace) -> int:
    report = apply_environment(args.repo_root, home=args.home, os_name=args.os_name)
    print(_render_report(report))
    return 0


def command_inspect(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    manifest = load_manifest(repo_root / MANIFEST_NAME)
    paths = ManagedPaths.for_platform(os_name=args.os_name, home=args.home)
    lines = [
        f"repo: {repo_root}",
        f"os: {paths.os_name}",
        f"home: {paths.home}",
        f"plugin_root: {paths.plugin_root}",
        f"local_plugin_overlay_root: {paths.local_plugin_overlay_root}",
        f"marketplace_path: {paths.marketplace_path}",
        f"codex_home: {paths.codex_home}",
        f"state_path: {paths.state_path}",
        "plugins:",
    ]
    for plugin in manifest.plugins:
        lines.append(f"  - {plugin.name}: {plugin.source} ({manifest.plugin_mode_for(paths.os_name, plugin)})")
    lines.append("instructions:")
    for instruction in manifest.instructions:
        lines.append(
            f"  - {instruction.name}: {instruction.source} -> {instruction.target} "
            f"({manifest.instruction_mode_for(paths.os_name, instruction)})"
        )
    print("\n".join(lines))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "bootstrap":
            return command_bootstrap(args)
        if args.command == "apply":
            return command_apply(args)
        if args.command == "inspect":
            return command_inspect(args)
    except Exception as exc:  # pragma: no cover - surfaced in CLI tests
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.print_help()
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
