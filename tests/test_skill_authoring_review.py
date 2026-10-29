from __future__ import annotations

import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = (Path(__file__).resolve().parents[1] / "plugins/jy-env-core/skills"
          / "skill-authoring-review/scripts/scan_skill.py")
spec = importlib.util.spec_from_file_location("scan_skill", SCRIPT)
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)


class SkillAuthoringReviewTests(unittest.TestCase):
    def test_environment_preserves_paths_without_provider_or_trace_secrets(self) -> None:
        result = scanner.scanner_environment({
            "PATH": "/bin", "HOME": "/real/home", "SystemRoot": "C:\\Windows",
            "OPENAI_API_KEY": "test-placeholder", "LANGSMITH_API_KEY": "test-placeholder",
            "LANGSMITH_ENDPOINT": "https://example.invalid", "LANGSMITH_TRACING": "true",
            "SKILLSPECTOR_PROVIDER": "claude_cli", "UNRECOGNIZED_SECRET": "test-placeholder",
        })
        self.assertEqual(result["HOME"], "/real/home")
        self.assertEqual(result["SystemRoot"], "C:\\Windows")
        self.assertFalse(any("KEY" in key or "SECRET" in key or "ENDPOINT" in key for key in result))
        self.assertNotIn("SKILLSPECTOR_PROVIDER", result)
        self.assertEqual(result["LANGSMITH_TRACING"], "false")

    def test_report_cannot_overwrite_source_or_enter_scanned_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "skill"
            target.mkdir()
            source = target / "SKILL.md"
            source.write_text("# Example", encoding="utf-8")
            with patch.object(scanner.subprocess, "run") as run:
                for output in (source, target / "report.json"):
                    with self.subTest(output=output), contextlib.redirect_stderr(io.StringIO()):
                        with self.assertRaises(SystemExit):
                            scanner.main([str(target), "--output", str(output)])
                run.assert_not_called()
            self.assertEqual(source.read_text(encoding="utf-8"), "# Example")

    def test_static_only_invocation_propagates_incomplete_exit_and_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "skill with spaces"
            target.mkdir()
            (target / "SKILL.md").write_text("# Example", encoding="utf-8")
            output = root / "report.json"
            args = [str(target), "--output", str(output)]
            with patch.object(scanner.shutil, "which", return_value="/tools/skillspector"):
                with patch.object(scanner.subprocess, "run", return_value=subprocess.CompletedProcess([], 1)) as run:
                    self.assertEqual(scanner.main(args), 1)
                    command = run.call_args.args[0]
                    self.assertEqual(command[2], str(target.resolve()))
                    self.assertIn("--no-llm", command)
                    self.assertIn("--fail-on-incomplete", command)
                    self.assertFalse(run.call_args.kwargs.get("shell", False))
                with patch.object(scanner.subprocess, "run", side_effect=subprocess.TimeoutExpired("scanner", 1)):
                    with contextlib.redirect_stderr(io.StringIO()):
                        self.assertEqual(scanner.main(args), 124)
            with patch.object(scanner.shutil, "which", return_value=None):
                with contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(scanner.main(args), 127)
