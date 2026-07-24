from __future__ import annotations

from pathlib import Path
import json
import shutil
import tempfile
import textwrap
import unittest

from codex_env_sync.apply import apply_environment, hash_path


def write_fixture_repo(
    root: Path,
    plugin_install_mode: str = "copy",
    instruction_install_mode: str = "copy",
) -> None:
    (root / "plugins" / "jy-env-core" / ".codex-plugin").mkdir(parents=True, exist_ok=True)
    (root / "plugins" / "jy-env-core" / "skills" / "jy-env-sync-admin").mkdir(parents=True, exist_ok=True)
    (root / "instructions").mkdir(parents=True, exist_ok=True)
    manifest_text = textwrap.dedent(
        """
            schema_version = 1
            name = "fixture"

            [[plugins]]
            name = "jy-env-core"
            source = "plugins/jy-env-core"
            install_mode = "{plugin_install_mode}"
            installation_policy = "INSTALLED_BY_DEFAULT"

            [[instructions]]
            name = "global-agents"
            source = "instructions/AGENTS.md"
            target = ".codex/AGENTS.md"
            install_mode = "{instruction_install_mode}"
            """
    )
    (root / "codex-env.toml").write_text(
        manifest_text.format(
            plugin_install_mode=plugin_install_mode,
            instruction_install_mode=instruction_install_mode,
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
                "interface": {"category": "Productivity"},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (root / "plugins" / "jy-env-core" / "skills" / "jy-env-sync-admin" / "SKILL.md").write_text(
        "---\nname: jy-env-sync-admin\ndescription: fixture\n---\n",
        encoding="utf-8",
    )
    (root / "plugins" / "jy-env-core" / "payload.txt").write_text("fixture\n", encoding="utf-8")
    (root / "instructions" / "AGENTS.md").write_text("# fixture\n", encoding="utf-8")


def add_optional_pack(root: Path, name: str = "jy-env-planning") -> None:
    plugin_root = root / "plugins" / name
    skill_root = plugin_root / "skills" / "jy-framing"
    (plugin_root / ".codex-plugin").mkdir(parents=True, exist_ok=True)
    skill_root.mkdir(parents=True, exist_ok=True)
    (plugin_root / ".codex-plugin" / "plugin.json").write_text(
        json.dumps(
            {
                "name": name,
                "version": "0.1.0",
                "description": "fixture optional pack",
                "skills": "./skills/",
                "interface": {"category": "Productivity"},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (skill_root / "SKILL.md").write_text(
        "---\nname: jy-framing\ndescription: fixture\n---\n",
        encoding="utf-8",
    )
    manifest_path = root / "codex-env.toml"
    manifest_path.write_text(
        manifest_path.read_text(encoding="utf-8")
        + textwrap.dedent(
            f"""

            [[plugins]]
            name = "{name}"
            source = "plugins/{name}"
            install_mode = "copy"
            installation_policy = "AVAILABLE"
            """
        ),
        encoding="utf-8",
    )


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
    def test_apply_stages_optional_packs_without_native_skill_overlays(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root)
            add_optional_pack(repo_root)

            apply_environment(repo_root, home=home_root, os_name="linux")

            self.assertTrue((home_root / "plugins" / "jy-env-core").is_dir())
            self.assertTrue((home_root / "plugins" / "jy-env-planning").is_dir())
            self.assertFalse((home_root / ".agents" / "skills" / "jy-env-core").exists())
            self.assertFalse((home_root / ".agents" / "skills" / "jy-env-planning").exists())

            marketplace = json.loads(
                (home_root / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
            )
            policies = {
                entry["name"]: entry["policy"]["installation"]
                for entry in marketplace["plugins"]
            }
            self.assertEqual(
                policies,
                {
                    "jy-env-core": "INSTALLED_BY_DEFAULT",
                    "jy-env-planning": "AVAILABLE",
                },
            )

    def test_apply_removes_legacy_managed_skill_overlay(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root)
            legacy_skills = home_root / ".agents" / "skills" / "jy-env-core"
            legacy_skills.mkdir(parents=True)
            (legacy_skills / "legacy.txt").write_text("managed\n", encoding="utf-8")
            installed_hash = hash_path(legacy_skills)
            state_path = home_root / ".codex-env-sync" / "state.json"
            state_path.parent.mkdir(parents=True)
            state_path.write_text(
                json.dumps(
                    {
                        "plugins": {},
                        "skills": {
                            "jy-env-core": {
                                "mode": "copy",
                                "installed_hash": installed_hash,
                            }
                        },
                        "instructions": {},
                        "hooks": {},
                        "last_apply": None,
                    }
                ),
                encoding="utf-8",
            )

            report = apply_environment(repo_root, home=home_root, os_name="linux")

            self.assertFalse(legacy_skills.exists())
            self.assertEqual(report.skills[0].detail, "removed stale managed skill link")

    def test_apply_refuses_to_remove_modified_legacy_skill_overlay(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root)
            legacy_skills = home_root / ".agents" / "skills" / "jy-env-core"
            legacy_skills.mkdir(parents=True)
            legacy_file = legacy_skills / "legacy.txt"
            legacy_file.write_text("managed\n", encoding="utf-8")
            installed_hash = hash_path(legacy_skills)
            legacy_file.write_text("user change\n", encoding="utf-8")
            state_path = home_root / ".codex-env-sync" / "state.json"
            state_path.parent.mkdir(parents=True)
            state_path.write_text(
                json.dumps(
                    {
                        "plugins": {},
                        "skills": {
                            "jy-env-core": {
                                "mode": "copy",
                                "installed_hash": installed_hash,
                            }
                        },
                        "instructions": {},
                        "hooks": {},
                        "last_apply": None,
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "modified managed skill surface"):
                apply_environment(repo_root, home=home_root, os_name="linux")

            self.assertEqual(legacy_file.read_text(encoding="utf-8"), "user change\n")

    def test_preflight_rejects_unknown_plugin_installation_policy(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root)
            manifest_path = repo_root / "codex-env.toml"
            manifest_path.write_text(
                manifest_path.read_text(encoding="utf-8").replace(
                    'installation_policy = "INSTALLED_BY_DEFAULT"',
                    'installation_policy = "SOMETIMES"',
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "Unsupported plugin installation policy"):
                apply_environment(repo_root, home=home_root, os_name="linux")

            self.assertFalse((home_root / "plugins" / "jy-env-core").exists())

    def test_apply_writes_plugin_marketplace_and_instruction(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root)

            report = apply_environment(repo_root, home=home_root, os_name="darwin")

            plugin_json = home_root / "plugins" / "jy-env-core" / ".codex-plugin" / "plugin.json"
            agents_file = home_root / ".codex" / "AGENTS.md"
            marketplace = home_root / ".agents" / "plugins" / "marketplace.json"

            self.assertTrue(plugin_json.exists())
            self.assertTrue(agents_file.exists())
            self.assertTrue(marketplace.exists())
            self.assertFalse((home_root / ".agents" / "skills" / "jy-env-core").exists())
            self.assertEqual(report.marketplace_action, "applied")

            second_report = apply_environment(repo_root, home=home_root, os_name="darwin")
            self.assertEqual(second_report.plugins[0].action, "skipped")
            self.assertEqual(second_report.instructions[0].action, "skipped")
            self.assertEqual(second_report.marketplace_action, "skipped")

            state = json.loads((home_root / ".codex-env-sync" / "state.json").read_text(encoding="utf-8"))
            self.assertNotIn("overlay_hash", state["plugins"]["jy-env-core"])

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
            self.assertEqual(names, ["existing-plugin", "jy-env-core"])

    def test_apply_recovers_from_copy_mode_drift(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root, plugin_install_mode="copy", instruction_install_mode="copy")

            apply_environment(repo_root, home=home_root, os_name="linux")

            installed_payload = home_root / "plugins" / "jy-env-core" / "payload.txt"
            installed_agents = home_root / ".codex" / "AGENTS.md"
            installed_payload.write_text("drifted\n", encoding="utf-8")
            installed_agents.write_text("# drifted\n", encoding="utf-8")

            report = apply_environment(repo_root, home=home_root, os_name="linux")

            self.assertEqual(report.plugins[0].action, "applied")
            self.assertEqual(report.instructions[0].action, "applied")
            self.assertEqual(installed_payload.read_text(encoding="utf-8"), "fixture\n")
            self.assertEqual(installed_agents.read_text(encoding="utf-8"), "# fixture\n")

    def test_apply_removes_legacy_managed_hook_state_without_touching_user_hooks(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root)

            hooks_path = home_root / ".codex" / "hooks.json"
            hooks_path.parent.mkdir(parents=True, exist_ok=True)
            hooks_path.write_text(
                json.dumps(
                    {
                        "hooks": {
                            "Stop": [
                                {
                                    "hooks": [
                                    {
                                        "type": "command",
                                        "command": "printf user-stop-hook",
                                    },
                                    {
                                        "type": "command",
                                        "command": "python3 old-hook.py stop # [codex-env-sync:necessity-gate]",
                                    }
                                    ]
                                }
                            ]
                        }
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            state_path = home_root / ".codex-env-sync" / "state.json"
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text(
                json.dumps(
                    {
                        "plugins": {},
                        "skills": {},
                        "instructions": {},
                        "hooks": {
                            "necessity-gate": {
                                "target": str(hooks_path),
                                "managed_hooks": {"hooks": {}},
                            }
                        },
                        "last_apply": None,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            report = apply_environment(repo_root, home=home_root, os_name="linux")

            data = json.loads(hooks_path.read_text(encoding="utf-8"))
            commands = [
                hook["command"]
                for groups in data["hooks"].values()
                for group in groups
                for hook in group["hooks"]
                if hook["type"] == "command"
            ]
            self.assertEqual(report.hooks[0].action, "removed")
            self.assertIn("printf user-stop-hook", commands)
            self.assertFalse(any("[codex-env-sync:necessity-gate]" in command for command in commands))
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["hooks"], {})

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

            self.assertFalse((home_root / "plugins" / "jy-env-core").exists())
            self.assertFalse((home_root / ".codex" / "AGENTS.md").exists())
            self.assertFalse((home_root / ".agents" / "skills" / "jy-env-core").exists())

            marketplace = home_root / ".agents" / "plugins" / "marketplace.json"
            data = json.loads(marketplace.read_text(encoding="utf-8"))
            self.assertEqual(data["plugins"], [])

    def test_apply_removes_old_plugin_surface_after_plugin_rename(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root)

            legacy_plugin_root = repo_root / "plugins" / "codex-env-core"
            legacy_plugin_root.mkdir(parents=True, exist_ok=True)
            (legacy_plugin_root / ".codex-plugin").mkdir(parents=True, exist_ok=True)
            (legacy_plugin_root / ".codex-plugin" / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "codex-env-core",
                        "version": "0.1.0",
                        "description": "legacy",
                        "skills": "./skills/",
                        "interface": {"category": "Productivity"},
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (legacy_plugin_root / "skills" / "env-sync-admin").mkdir(parents=True, exist_ok=True)
            (legacy_plugin_root / "skills" / "env-sync-admin" / "SKILL.md").write_text(
                "---\nname: env-sync-admin\ndescription: fixture\n---\n",
                encoding="utf-8",
            )

            (repo_root / "codex-env.toml").write_text(
                textwrap.dedent(
                    """
                    schema_version = 1
                    name = "fixture"

                    [[plugins]]
                    name = "codex-env-core"
                    source = "plugins/codex-env-core"
                    install_mode = "copy"

                    [[instructions]]
                    name = "global-agents"
                    source = "instructions/AGENTS.md"
                    target = ".codex/AGENTS.md"
                    install_mode = "copy"
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            apply_environment(repo_root, home=home_root, os_name="linux")

            shutil.rmtree(legacy_plugin_root)
            write_fixture_repo(repo_root)

            apply_environment(repo_root, home=home_root, os_name="linux")

            self.assertFalse((home_root / "plugins" / "codex-env-core").exists())
            self.assertFalse((home_root / ".agents" / "skills" / "codex-env-core").exists())
            self.assertTrue((home_root / "plugins" / "jy-env-core").exists())
            self.assertFalse((home_root / ".agents" / "skills" / "jy-env-core").exists())

    @unittest.skipUnless(supports_symlinks(), "symlinks are not supported on this host")
    def test_apply_symlink_mode_links_to_repo_sources(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root, plugin_install_mode="symlink", instruction_install_mode="symlink")

            report = apply_environment(repo_root, home=home_root, os_name="darwin")

            plugin_root = home_root / "plugins" / "jy-env-core"
            agents_file = home_root / ".codex" / "AGENTS.md"

            self.assertEqual(report.plugins[0].detail, "symlinked plugin bundle")
            self.assertEqual(report.instructions[0].detail, "symlinked instruction artifact")
            self.assertTrue(plugin_root.is_symlink())
            self.assertTrue(agents_file.is_symlink())
            self.assertEqual(plugin_root.resolve(), (repo_root / "plugins" / "jy-env-core").resolve())
            self.assertEqual(agents_file.resolve(), (repo_root / "instructions" / "AGENTS.md").resolve())
            self.assertFalse((home_root / ".agents" / "skills" / "jy-env-core").exists())

            (repo_root / "instructions" / "AGENTS.md").write_text("# updated\n", encoding="utf-8")
            self.assertEqual(agents_file.read_text(encoding="utf-8"), "# updated\n")

            second_report = apply_environment(repo_root, home=home_root, os_name="darwin")
            self.assertEqual(second_report.plugins[0].action, "skipped")
            self.assertEqual(second_report.plugins[0].detail, "symlink unchanged")
            self.assertEqual(second_report.instructions[0].action, "skipped")
            self.assertEqual(second_report.instructions[0].detail, "symlink unchanged")

    def test_snapshot_apply_copies_all_live_surfaces_on_posix(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root, plugin_install_mode="symlink", instruction_install_mode="symlink")

            report = apply_environment(repo_root, home=home_root, os_name="darwin", snapshot=True)

            plugin_root = home_root / "plugins" / "jy-env-core"
            agents_file = home_root / ".codex" / "AGENTS.md"
            self.assertEqual(report.plugins[0].detail, "copied plugin bundle")
            self.assertEqual(report.skills, [])
            self.assertEqual(report.instructions[0].detail, "copied instruction artifact")
            self.assertFalse(plugin_root.is_symlink())
            self.assertFalse(agents_file.is_symlink())
            self.assertFalse((home_root / ".agents" / "skills" / "jy-env-core").exists())

            (repo_root / "instructions" / "AGENTS.md").write_text("# changed after snapshot\n", encoding="utf-8")
            self.assertEqual(agents_file.read_text(encoding="utf-8"), "# fixture\n")

    def test_preflight_rejects_missing_new_source_before_removing_stale_install(self) -> None:
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

                    [[plugins]]
                    name = "replacement"
                    source = "plugins/missing"
                    install_mode = "copy"
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "Plugin source does not exist"):
                apply_environment(repo_root, home=home_root, os_name="linux")

            self.assertTrue((home_root / "plugins" / "jy-env-core").exists())
            self.assertFalse((home_root / ".agents" / "skills" / "jy-env-core").exists())
            self.assertTrue((home_root / ".codex" / "AGENTS.md").exists())

    def test_preflight_preserves_drifted_stale_install_instead_of_deleting_it(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as home_dir:
            repo_root = Path(repo_dir)
            home_root = Path(home_dir)
            write_fixture_repo(repo_root, plugin_install_mode="copy", instruction_install_mode="copy")
            apply_environment(repo_root, home=home_root, os_name="linux")

            installed_payload = home_root / "plugins" / "jy-env-core" / "payload.txt"
            installed_payload.write_text("user-owned replacement\n", encoding="utf-8")
            (repo_root / "codex-env.toml").write_text("schema_version = 1\nname = \"fixture\"\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Refusing to remove modified managed plugin"):
                apply_environment(repo_root, home=home_root, os_name="linux")

            self.assertEqual(installed_payload.read_text(encoding="utf-8"), "user-owned replacement\n")
            self.assertFalse((home_root / ".agents" / "skills" / "jy-env-core").exists())
            self.assertTrue((home_root / ".codex" / "AGENTS.md").exists())


if __name__ == "__main__":
    unittest.main()
