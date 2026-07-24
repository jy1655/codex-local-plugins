from __future__ import annotations

from pathlib import Path
import tempfile
import textwrap
import unittest

from codex_env_sync.manifest import load_manifest


class ManifestTests(unittest.TestCase):
    def test_load_manifest_reads_reduced_v1_shape(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_path = Path(temp_dir) / "codex-env.toml"
            manifest_path.write_text(
                textwrap.dedent(
                    """
                    schema_version = 1
                    name = "example"

                    [[plugins]]
                    name = "core"
                    source = "plugins/core"
                    install_mode = "copy"
                    installation_policy = "INSTALLED_BY_DEFAULT"

                    [[instructions]]
                    name = "agents"
                    source = "instructions/AGENTS.md"
                    target = ".codex/AGENTS.md"

                    [platform_overrides.windows]
                    plugin_install_mode = "copy"
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            manifest = load_manifest(manifest_path)

        self.assertEqual(manifest.schema_version, 1)
        self.assertEqual(manifest.name, "example")
        self.assertEqual(len(manifest.plugins), 1)
        self.assertEqual(manifest.plugins[0].name, "core")
        self.assertEqual(manifest.plugins[0].installation_policy, "INSTALLED_BY_DEFAULT")
        self.assertEqual(manifest.instructions[0].target, ".codex/AGENTS.md")
        self.assertNotIn("hooks", manifest.__dataclass_fields__)
        self.assertEqual(manifest.plugin_mode_for("windows", manifest.plugins[0]), "copy")

    def test_load_manifest_rejects_unsupported_schema_before_apply(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_path = Path(temp_dir) / "codex-env.toml"
            manifest_path.write_text(
                textwrap.dedent(
                    """
                    schema_version = 999
                    name = "future"
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "Unsupported manifest schema version"):
                load_manifest(manifest_path)

    def test_legacy_plugin_entry_defaults_to_available(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_path = Path(temp_dir) / "codex-env.toml"
            manifest_path.write_text(
                textwrap.dedent(
                    """
                    schema_version = 1
                    name = "legacy"

                    [[plugins]]
                    name = "core"
                    source = "plugins/core"
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            manifest = load_manifest(manifest_path)

        self.assertEqual(manifest.plugins[0].installation_policy, "AVAILABLE")


if __name__ == "__main__":
    unittest.main()
