from __future__ import annotations

import unittest
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import tempfile
from unittest.mock import patch

from codex_env_sync.cli import build_parser, main


def write_pack_fixture(root: Path) -> None:
    plugins = [
        ("jy-env-core", "INSTALLED_BY_DEFAULT"),
        ("jy-env-planning", "AVAILABLE"),
    ]
    manifest = [
        "schema_version = 1",
        'name = "fixture"',
        "",
    ]
    for plugin_name, installation_policy in plugins:
        manifest.extend(
            [
                "[[plugins]]",
                f'name = "{plugin_name}"',
                f'source = "plugins/{plugin_name}"',
                'install_mode = "copy"',
                f'installation_policy = "{installation_policy}"',
                "",
            ]
        )
        plugin_root = root / "plugins" / plugin_name / ".codex-plugin"
        plugin_root.mkdir(parents=True)
        (plugin_root / "plugin.json").write_text(
            json.dumps(
                {
                    "name": plugin_name,
                    "version": "0.1.0",
                    "description": "fixture",
                    "interface": {"category": "Productivity"},
                }
            ),
            encoding="utf-8",
        )
    (root / "codex-env.toml").write_text("\n".join(manifest), encoding="utf-8")


def initialize_git_repo(root: Path) -> None:
    subprocess.run(["git", "init", "-b", "main", str(root)], check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "-C", str(root), "add", "."], check=True, stdout=subprocess.DEVNULL)
    subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "-c",
            "user.name=Test User",
            "-c",
            "user.email=test@example.com",
            "commit",
            "-m",
            "fixture",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
    )


class CliTests(unittest.TestCase):
    def test_apply_installs_only_plugins_marked_installed_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            write_pack_fixture(repo_root)
            real_run = subprocess.run
            codex_calls: list[list[str]] = []

            def fake_codex(command: list[str], *args, **kwargs):
                if command and Path(command[0]).name in {"codex", "codex.exe", "codex.cmd"}:
                    codex_calls.append(list(command))
                    return subprocess.CompletedProcess(command, 0)
                return real_run(command, *args, **kwargs)

            resolved_codex = "/fake/bin/codex"
            with (
                patch("codex_env_sync.apply.shutil.which", return_value=resolved_codex),
                patch("subprocess.run", side_effect=fake_codex),
                redirect_stdout(io.StringIO()),
            ):
                result = main(
                    [
                        "apply",
                        "--repo-root",
                        str(repo_root),
                        "--home",
                        home_dir,
                        "--os-name",
                        "linux",
                    ]
                )

            self.assertEqual(result, 0)
            self.assertEqual(
                codex_calls,
                [[resolved_codex, "plugin", "add", "jy-env-core@personal-codex"]],
            )

    def test_bootstrap_installs_only_plugins_marked_installed_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            write_pack_fixture(repo_root)
            initialize_git_repo(repo_root)
            real_run = subprocess.run
            codex_calls: list[list[str]] = []

            def fake_codex(command: list[str], *args, **kwargs):
                if command and Path(command[0]).name in {"codex", "codex.exe", "codex.cmd"}:
                    codex_calls.append(list(command))
                    return subprocess.CompletedProcess(command, 0)
                return real_run(command, *args, **kwargs)

            resolved_codex = "/fake/bin/codex.cmd"
            with (
                patch("codex_env_sync.apply.shutil.which", return_value=resolved_codex),
                patch("subprocess.run", side_effect=fake_codex),
                redirect_stdout(io.StringIO()),
            ):
                result = main(
                    [
                        "bootstrap",
                        str(repo_root),
                        "--home",
                        home_dir,
                        "--os-name",
                        "windows",
                    ]
                )

            self.assertEqual(result, 0)
            self.assertEqual(
                codex_calls,
                [[resolved_codex, "plugin", "add", "jy-env-core@personal-codex"]],
            )

    def test_apply_accepts_explicit_snapshot_mode(self) -> None:
        args = build_parser().parse_args(["apply", "--repo-root", ".", "--snapshot"])

        self.assertEqual(args.command, "apply")
        self.assertTrue(args.snapshot)

    def test_inspect_runs_read_only_preflight_validation(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            (repo_root / "codex-env.toml").write_text(
                """schema_version = 1
name = "broken"

[[plugins]]
name = "missing"
source = "plugins/missing"
""",
                encoding="utf-8",
            )

            result = main(["inspect", "--repo-root", str(repo_root), "--home", home_dir])

            self.assertEqual(result, 1)
            self.assertFalse((Path(home_dir) / ".codex-env-sync").exists())

    def test_inspect_prints_plugin_installation_policy(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            plugin_root = repo_root / "plugins" / "core" / ".codex-plugin"
            plugin_root.mkdir(parents=True)
            (plugin_root / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "core",
                        "version": "0.1.0",
                        "description": "fixture",
                    }
                ),
                encoding="utf-8",
            )
            (repo_root / "codex-env.toml").write_text(
                """schema_version = 1
name = "fixture"

[[plugins]]
name = "core"
source = "plugins/core"
installation_policy = "INSTALLED_BY_DEFAULT"
""",
                encoding="utf-8",
            )
            output = io.StringIO()

            with redirect_stdout(output):
                result = main(["inspect", "--repo-root", str(repo_root), "--home", home_dir])

            self.assertEqual(result, 0)
            self.assertIn("INSTALLED_BY_DEFAULT", output.getvalue())


if __name__ == "__main__":
    unittest.main()
