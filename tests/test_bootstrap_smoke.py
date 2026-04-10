from __future__ import annotations

from pathlib import Path
import json
import subprocess
import tempfile
import textwrap
import unittest

from codex_env_sync.apply import bootstrap_environment, clone_or_update_repo
from codex_env_sync.platforms import ManagedPaths


def write_bootstrap_repo(root: Path) -> None:
    (root / "plugins" / "jy-env-core" / ".codex-plugin").mkdir(parents=True, exist_ok=True)
    (root / "plugins" / "jy-env-core" / "skills" / "jy-env-sync-admin").mkdir(parents=True, exist_ok=True)
    (root / "instructions").mkdir(parents=True, exist_ok=True)

    (root / "codex-env.toml").write_text(
        textwrap.dedent(
            """
            schema_version = 1
            name = "bootstrap-fixture"

            [[plugins]]
            name = "jy-env-core"
            source = "plugins/jy-env-core"

            [[instructions]]
            name = "global-agents"
            source = "instructions/AGENTS.md"
            target = ".codex/AGENTS.md"
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    (root / "plugins" / "jy-env-core" / ".codex-plugin" / "plugin.json").write_text(
        json.dumps(
            {
                "name": "jy-env-core",
                "version": "0.1.0",
                "description": "fixture",
                "skills": "./skills/",
                "mcpServers": "./.mcp.json",
                "interface": {"category": "Productivity"},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (root / "plugins" / "jy-env-core" / ".mcp.json").write_text('{"mcpServers":{}}\n', encoding="utf-8")
    (root / "plugins" / "jy-env-core" / "skills" / "jy-env-sync-admin" / "SKILL.md").write_text(
        "---\nname: jy-env-sync-admin\ndescription: fixture\n---\n",
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

                    report = bootstrap_environment(str(git_repo), home=home_dir, os_name=os_name)

                    self.assertIsNotNone(report.managed_repo)
                    self.assertTrue((Path(home_dir) / "plugins" / "jy-env-core").exists())
                    self.assertTrue((Path(home_dir) / ".agents" / "skills" / "jy-env-core" / "jy-env-sync-admin" / "SKILL.md").exists())
                    self.assertTrue((Path(home_dir) / ".codex" / "AGENTS.md").exists())
                    self.assertTrue((Path(home_dir) / ".agents" / "plugins" / "marketplace.json").exists())

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


if __name__ == "__main__":
    unittest.main()
