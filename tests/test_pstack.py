from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1] / "plugins/jy-env-core/skills/pstack"


class PstackPortTests(unittest.TestCase):
    def test_only_entrypoint_is_discoverable_and_provenance_matches_inventory(self) -> None:
        self.assertEqual(list(ROOT.rglob("SKILL.md")), [ROOT / "SKILL.md"])
        upstream = json.loads((ROOT / "UPSTREAM.json").read_text(encoding="utf-8"))
        self.assertRegex(upstream["revision"], r"^[0-9a-f]{40}$")
        records = upstream["files"] + upstream["excluded_files"]
        self.assertEqual(len(records), len({r["local"] for r in records}))
        for record in upstream["files"]:
            with self.subTest(source=record["source"]):
                self.assertRegex(record["sha256"], r"^[0-9a-f]{64}$")
                path = (ROOT / record["local"]).resolve()
                self.assertTrue(path.is_relative_to(ROOT.resolve()))
                self.assertTrue(path.is_file())
        for record in upstream["excluded_files"]:
            with self.subTest(excluded=record["source"]):
                self.assertRegex(record["sha256"], r"^[0-9a-f]{64}$")
                path = (ROOT / record["local"]).resolve()
                self.assertTrue(path.is_relative_to(ROOT.resolve()))
                self.assertFalse(path.exists())
                self.assertTrue(record["reason"])
        self.assertEqual(len(list((ROOT / "references/skills").glob("*/WORKFLOW.md"))), 54)
        self.assertEqual(len(list((ROOT / "references/skills/poteto-mode/playbooks").glob("*.md"))), 23)

    def test_concrete_local_markdown_links_resolve_inside_the_module(self) -> None:
        for path in ROOT.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if target.startswith(("https:", "http:", "mailto:", "#")) or target == "url" or "<" in target:
                    continue
                target_path = (path.parent / target.split("#", 1)[0]).resolve()
                with self.subTest(file=path.relative_to(ROOT), target=target):
                    self.assertTrue(target_path.is_relative_to(ROOT.resolve()))
                    self.assertTrue(target_path.exists())

    def test_runner_preserves_argument_boundaries_and_exit_status(self) -> None:
        spec = importlib.util.spec_from_file_location("pstack_runner", ROOT / "scripts/run_tool.py")
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        invoked = []

        def invoke(command: list[str], **kwargs: object) -> subprocess.CompletedProcess:
            entry = Path(command[1])
            self.assertEqual(command[0], "node")
            self.assertTrue(entry.is_relative_to(ROOT))
            self.assertTrue(entry.is_file())
            self.assertEqual(command[2:], ["/tmp/plan with spaces.md"])
            self.assertEqual(kwargs, {"check": False})
            invoked.append(entry)
            return subprocess.CompletedProcess(command, 7)

        with patch("sys.argv", ["run_tool.py", "check-plan", "/tmp/plan with spaces.md"]), \
             patch.object(runner.shutil, "which", return_value="/bin/node"), \
             patch.object(runner.subprocess, "run", side_effect=invoke):
            self.assertEqual(runner.main(), 7)
        self.assertEqual(len(invoked), 1)

    def test_removed_tools_are_rejected_before_runtime_lookup(self) -> None:
        for tool in ("watch-pr", "orch"):
            with self.subTest(tool=tool):
                result = subprocess.run(
                    [sys.executable, str(ROOT / "scripts/run_tool.py"), tool, "--help"],
                    env={"PATH": ""}, capture_output=True, text=True, encoding="utf-8",
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()
