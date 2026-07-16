from __future__ import annotations

import unittest
from pathlib import Path
import tempfile

from codex_env_sync.cli import build_parser, main


class CliTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
