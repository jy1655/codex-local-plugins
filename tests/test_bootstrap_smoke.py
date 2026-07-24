from __future__ import annotations

from pathlib import Path
import json
import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest

from codex_env_sync.apply import bootstrap_environment, clone_or_update_repo
from codex_env_sync.platforms import ManagedPaths


def write_bootstrap_repo(root: Path) -> None:
    (root / "instructions").mkdir(parents=True, exist_ok=True)
    plugins = [
        ("jy-env-core", "jy-debugging", "INSTALLED_BY_DEFAULT"),
        ("jy-env-planning", "jy-framing", "AVAILABLE"),
        ("jy-env-delivery", "jy-ship", "AVAILABLE"),
        ("jy-env-audit", "jy-review-all", "AVAILABLE"),
    ]

    (root / "codex-env.toml").write_text(
        textwrap.dedent(
            """\
            schema_version = 1
            name = "bootstrap-fixture"
            """
        )
        + "\n".join(
            textwrap.dedent(
                f"""
                [[plugins]]
                name = "{plugin_name}"
                source = "plugins/{plugin_name}"
                installation_policy = "{policy}"
                """
            ).strip()
            for plugin_name, _, policy in plugins
        )
        + textwrap.dedent(
            """

            [[instructions]]
            name = "global-agents"
            source = "instructions/AGENTS.md"
            target = ".codex/AGENTS.md"
            """
        )
        + "\n",
        encoding="utf-8",
    )
    for plugin_name, skill_name, _ in plugins:
        plugin_root = root / "plugins" / plugin_name
        skill_root = plugin_root / "skills" / skill_name
        (plugin_root / ".codex-plugin").mkdir(parents=True)
        skill_root.mkdir(parents=True)
        (plugin_root / ".codex-plugin" / "plugin.json").write_text(
            json.dumps(
                {
                    "name": plugin_name,
                    "version": "0.1.0",
                    "description": "fixture",
                    "skills": "./skills/",
                    "interface": {"category": "Productivity"},
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (skill_root / "SKILL.md").write_text(
            f"---\nname: {skill_name}\ndescription: fixture\n---\n",
            encoding="utf-8",
        )
    (root / "instructions" / "AGENTS.md").write_text("# smoke\n", encoding="utf-8")


def make_local_git_repo(root: Path) -> Path:
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
    return root


class BootstrapSmokeTests(unittest.TestCase):
    def test_bootstrap_smoke_for_all_supported_os_names(self) -> None:
        for os_name in ("darwin", "linux", "windows"):
            with self.subTest(os_name=os_name):
                with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
                    repo_root = Path(repo_dir)
                    write_bootstrap_repo(repo_root)
                    git_repo = make_local_git_repo(repo_root)

                    report = bootstrap_environment(
                        str(git_repo),
                        home=home_dir,
                        os_name=os_name,
                        install_defaults=False,
                    )

                    self.assertIsNotNone(report.managed_repo)
                    for plugin_name in [
                        "jy-env-core",
                        "jy-env-planning",
                        "jy-env-delivery",
                        "jy-env-audit",
                    ]:
                        self.assertTrue((Path(home_dir) / "plugins" / plugin_name).exists())
                        self.assertFalse((Path(home_dir) / "plugins" / plugin_name).is_symlink())
                    self.assertFalse((Path(home_dir) / ".agents" / "skills").exists())
                    self.assertTrue((Path(home_dir) / ".codex" / "AGENTS.md").exists())
                    marketplace = json.loads(
                        (Path(home_dir) / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
                    )
                    policies = {
                        entry["name"]: entry["policy"]["installation"]
                        for entry in marketplace["plugins"]
                    }
                    self.assertEqual(policies["jy-env-core"], "INSTALLED_BY_DEFAULT")
                    self.assertEqual(
                        {policy for name, policy in policies.items() if name != "jy-env-core"},
                        {"AVAILABLE"},
                    )
                    self.assertFalse((Path(home_dir) / ".codex" / "AGENTS.md").is_symlink())

    def test_clone_or_update_repo_separates_same_basename_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo_a = root / "src-a" / "shared-name"
            repo_b = root / "src-b" / "shared-name"
            repo_a.mkdir(parents=True, exist_ok=True)
            repo_b.mkdir(parents=True, exist_ok=True)
            (repo_a / "README.md").write_text("repo-a\n", encoding="utf-8")
            (repo_b / "README.md").write_text("repo-b\n", encoding="utf-8")
            git_repo_a = make_local_git_repo(repo_a)
            git_repo_b = make_local_git_repo(repo_b)

            paths = ManagedPaths.for_platform(os_name="linux", home=root / "home")

            cached_a = clone_or_update_repo(str(git_repo_a), paths)
            cached_b = clone_or_update_repo(str(git_repo_b), paths)

            self.assertNotEqual(cached_a, cached_b)
            self.assertEqual((cached_a / "README.md").read_text(encoding="utf-8"), "repo-a\n")
            self.assertEqual((cached_b / "README.md").read_text(encoding="utf-8"), "repo-b\n")

    @unittest.skipIf(os.name == "nt", "POSIX bootstrap script is not applicable on Windows")
    @unittest.skipUnless(shutil.which("bash"), "bash is not available")
    def test_posix_bootstrap_script_installs_a_snapshot(self) -> None:
        with (
            tempfile.TemporaryDirectory() as repo_dir,
            tempfile.TemporaryDirectory() as home_dir,
            tempfile.TemporaryDirectory() as bin_dir,
        ):
            repo_root = Path(repo_dir)
            write_bootstrap_repo(repo_root)
            source_package = Path(__file__).resolve().parents[1] / "codex_env_sync"
            shutil.copytree(
                source_package,
                repo_root / "codex_env_sync",
                ignore=shutil.ignore_patterns("__pycache__"),
            )
            git_repo = make_local_git_repo(repo_root)
            script = Path(__file__).resolve().parents[1] / "scripts" / "bootstrap.sh"
            fake_codex = Path(bin_dir) / "codex"
            fake_codex.write_text(
                "#!/usr/bin/env bash\nprintf '%s\\n' \"$*\" >> \"$HOME/codex-plugin-add.log\"\n",
                encoding="utf-8",
            )
            fake_codex.chmod(0o755)
            env = os.environ.copy()
            env["HOME"] = home_dir
            env["PATH"] = bin_dir + os.pathsep + env["PATH"]

            result = subprocess.run(
                ["bash", str(script), str(git_repo)],
                check=False,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            home_root = Path(home_dir)
            self.assertFalse((home_root / "plugins" / "jy-env-core").is_symlink())
            self.assertFalse((home_root / ".agents" / "skills").exists())
            self.assertFalse((home_root / ".codex" / "AGENTS.md").is_symlink())
            self.assertEqual(
                (home_root / "codex-plugin-add.log").read_text(encoding="utf-8"),
                "plugin add jy-env-core@personal-codex\n",
            )

    def test_powershell_bootstrap_does_not_persist_a_temporary_pythonpath(self) -> None:
        script = Path(__file__).resolve().parents[1] / "scripts" / "bootstrap.ps1"
        self.assertNotIn("$env:PYTHONPATH =", script.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
