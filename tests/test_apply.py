from __future__ import annotations

from pathlib import Path
import json
import tempfile
import textwrap
import unittest

from codex_env_sync.apply import apply_environment


def write_fixture_repo(
    root: Path,
    plugin_install_mode: str = "copy",
    instruction_install_mode: str = "copy",
) -> None:
    (root / "plugins" / "codex-env-core" / ".codex-plugin").mkdir(parents=True, exist_ok=True)
    (root / "plugins" / "codex-env-core" / "skills" / "env-sync-admin").mkdir(parents=True, exist_ok=True)
    (root / "instructions").mkdir(parents=True, exist_ok=True)

    (root / "codex-env.toml").write_text(
        textwrap.dedent(
            """
            schema_version = 1
            name = "fixture"

            [[plugins]]
            name = "codex-env-core"
            source = "plugins/codex-env-core"
            install_mode = "{plugin_install_mode}"

            [[instructions]]
            name = "global-agents"
            source = "instructions/AGENTS.md"
            target = ".codex/AGENTS.md"
            install_mode = "{instruction_install_mode}"
            """
        ).format(
            plugin_install_mode=plugin_install_mode,
            instruction_install_mode=instruction_install_mode,
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    (root / "plugins" / "codex-env-core" / ".codex-plugin" / "plugin.json").write_text(
        json.dumps(
            {
                "name": "codex-env-core",
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
    (root / "plugins" / "codex-env-core" / ".mcp.json").write_text('{"mcpServers":{}}\n', encoding="utf-8")
    (root / "plugins" / "codex-env-core" / "skills" / "env-sync-admin" / "SKILL.md").write_text(
        "---\nname: env-sync-admin\ndescription: fixture\n---\n",
        encoding="utf-8",
    )
    (root / "plugins" / "codex-env-core" / "payload.txt").write_text("fixture\n", encoding="utf-8")
    (root / "instructions" / "AGENTS.md").write_text("# fixture\n", encoding="utf-8")


def supports_symlinks() -> bool:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        source = root / "source.txt"
        destination = root / "destination.txt"
        source.write_text("ok\n", encoding="utf-8")
        try:
            destination.symlink_to(source)
        except (NotImplementedError, OSError):
            return False
        return destination.is_symlink() and destination.resolve() == source.resolve()


class ApplyEnvironmentTests(unittest.TestCase):
    def test_apply_writes_plugin_marketplace_and_instruction(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root)

            report = apply_environment(repo_root, home=home_root, os_name="darwin")

            plugin_json = home_root / "plugins" / "codex-env-core" / ".codex-plugin" / "plugin.json"
            agents_file = home_root / ".codex" / "AGENTS.md"
            marketplace = home_root / ".agents" / "plugins" / "marketplace.json"
            skill_file = home_root / ".agents" / "skills" / "codex-env-core" / "env-sync-admin" / "SKILL.md"

            self.assertTrue(plugin_json.exists())
            self.assertTrue(agents_file.exists())
            self.assertTrue(marketplace.exists())
            self.assertTrue(skill_file.exists())
            self.assertEqual(report.marketplace_action, "applied")

            second_report = apply_environment(repo_root, home=home_root, os_name="darwin")
            self.assertEqual(second_report.plugins[0].action, "skipped")
            self.assertEqual(second_report.instructions[0].action, "skipped")
            self.assertEqual(second_report.marketplace_action, "skipped")

    def test_apply_merges_local_plugin_mcp_overlay(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root, plugin_install_mode="symlink")

            overlay = home_root / ".codex-env-sync" / "local" / "plugins" / "codex-env-core.mcp.json"
            overlay.parent.mkdir(parents=True, exist_ok=True)
            overlay.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "korean-law": {
                                "env": {
                                    "LAW_OC": "test-token",
                                }
                            }
                        }
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            report = apply_environment(repo_root, home=home_root, os_name="linux")

            installed_mcp = home_root / "plugins" / "codex-env-core" / ".mcp.json"
            data = json.loads(installed_mcp.read_text(encoding="utf-8"))
            self.assertFalse((home_root / "plugins" / "codex-env-core").is_symlink())
            self.assertEqual(
                report.plugins[0].detail,
                "copied plugin bundle + merged local mcp overlay (symlink fallback due to local overlay)",
            )
            self.assertEqual(data["mcpServers"]["korean-law"]["env"]["LAW_OC"], "test-token")

            second_report = apply_environment(repo_root, home=home_root, os_name="linux")
            self.assertEqual(second_report.plugins[0].action, "skipped")
            self.assertEqual(
                second_report.plugins[0].detail,
                "content unchanged (symlink fallback due to local mcp overlay)",
            )

    def test_apply_preserves_existing_non_managed_marketplace_entries(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root)
            marketplace = home_root / ".agents" / "plugins" / "marketplace.json"
            marketplace.parent.mkdir(parents=True, exist_ok=True)
            marketplace.write_text(
                json.dumps(
                    {
                        "name": "personal-codex",
                        "interface": {"displayName": "Personal Codex"},
                        "plugins": [
                            {
                                "name": "existing-plugin",
                                "source": {"source": "local", "path": "./plugins/existing-plugin"},
                                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                                "category": "Productivity",
                            }
                        ],
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            apply_environment(repo_root, home=home_root, os_name="linux")

            data = json.loads(marketplace.read_text(encoding="utf-8"))
            names = [entry["name"] for entry in data["plugins"]]
            self.assertEqual(names, ["existing-plugin", "codex-env-core"])

    def test_apply_recovers_from_copy_mode_drift(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root, plugin_install_mode="copy", instruction_install_mode="copy")

            apply_environment(repo_root, home=home_root, os_name="linux")

            installed_payload = home_root / "plugins" / "codex-env-core" / "payload.txt"
            installed_agents = home_root / ".codex" / "AGENTS.md"
            installed_payload.write_text("drifted\n", encoding="utf-8")
            installed_agents.write_text("# drifted\n", encoding="utf-8")

            report = apply_environment(repo_root, home=home_root, os_name="linux")

            self.assertEqual(report.plugins[0].action, "applied")
            self.assertEqual(report.instructions[0].action, "applied")
            self.assertEqual(installed_payload.read_text(encoding="utf-8"), "fixture\n")
            self.assertEqual(installed_agents.read_text(encoding="utf-8"), "# fixture\n")

    def test_apply_removes_entries_no_longer_present_in_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root)

            apply_environment(repo_root, home=home_root, os_name="linux")

            (repo_root / "codex-env.toml").write_text(
                textwrap.dedent(
                    """
                    schema_version = 1
                    name = "fixture"
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            apply_environment(repo_root, home=home_root, os_name="linux")

            self.assertFalse((home_root / "plugins" / "codex-env-core").exists())
            self.assertFalse((home_root / ".codex" / "AGENTS.md").exists())
            self.assertFalse((home_root / ".agents" / "skills" / "codex-env-core").exists())

            marketplace = home_root / ".agents" / "plugins" / "marketplace.json"
            data = json.loads(marketplace.read_text(encoding="utf-8"))
            self.assertEqual(data["plugins"], [])

    @unittest.skipUnless(supports_symlinks(), "symlinks are not supported on this host")
    def test_apply_symlink_mode_links_to_repo_sources(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root, plugin_install_mode="symlink", instruction_install_mode="symlink")

            report = apply_environment(repo_root, home=home_root, os_name="darwin")

            plugin_root = home_root / "plugins" / "codex-env-core"
            agents_file = home_root / ".codex" / "AGENTS.md"
            skills_root = home_root / ".agents" / "skills" / "codex-env-core"

            self.assertEqual(report.plugins[0].detail, "symlinked plugin bundle")
            self.assertEqual(report.instructions[0].detail, "symlinked instruction artifact")
            self.assertTrue(plugin_root.is_symlink())
            self.assertTrue(agents_file.is_symlink())
            self.assertTrue(skills_root.is_symlink())
            self.assertEqual(plugin_root.resolve(), (repo_root / "plugins" / "codex-env-core").resolve())
            self.assertEqual(agents_file.resolve(), (repo_root / "instructions" / "AGENTS.md").resolve())
            self.assertEqual(skills_root.resolve(), (repo_root / "plugins" / "codex-env-core" / "skills").resolve())

            (repo_root / "instructions" / "AGENTS.md").write_text("# updated\n", encoding="utf-8")
            self.assertEqual(agents_file.read_text(encoding="utf-8"), "# updated\n")

            second_report = apply_environment(repo_root, home=home_root, os_name="darwin")
            self.assertEqual(second_report.plugins[0].action, "skipped")
            self.assertEqual(second_report.plugins[0].detail, "symlink unchanged")
            self.assertEqual(second_report.instructions[0].action, "skipped")
            self.assertEqual(second_report.instructions[0].detail, "symlink unchanged")


if __name__ == "__main__":
    unittest.main()
