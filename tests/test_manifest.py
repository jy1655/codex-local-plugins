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
        self.assertEqual(manifest.instructions[0].target, ".codex/AGENTS.md")
        self.assertEqual(manifest.plugin_mode_for("windows", manifest.plugins[0]), "copy")


if __name__ == "__main__":
    unittest.main()
