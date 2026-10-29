from __future__ import annotations

from contextlib import redirect_stdout, redirect_stderr
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from codex_env_sync.apply import apply_environment

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("task_workspace", REPO / "scripts/task-workspace.py")
workspace = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workspace)


class TaskWorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()

    def call(self, *args):
        output, error = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(error):
            code = workspace.main(list(map(str, args)))
        return code, output.getvalue(), error.getvalue()

    def create(self, name="work"):
        root = self.base / name
        self.assertEqual(self.call("create", "--purpose", "verification", "--path", root)[0], 0)
        return root

    def classify(self, root, name, disposition, *extra):
        return self.call("classify", root, "--file", name, "--disposition", disposition,
                         "--reason", "test fixture disposition", *extra)

    def test_default_is_unique_temporary_directory(self):
        with patch.object(workspace.tempfile, "gettempdir", return_value=str(self.base)):
            first = self.call("create", "--purpose", "verification", "--name", "check")
            second = self.call("create", "--purpose", "verification", "--name", "check")
        self.assertEqual(first[0], 0)
        self.assertEqual(second[0], 0)
        self.assertNotEqual(first[1], second[1])
        self.assertEqual(Path(first[1].strip()).parent, self.base)

    def test_output_denied_before_any_directory_is_created(self):
        for spelling in ("output", "OUTPUT"):
            root = self.base / spelling / "check"
            result = self.call("create", "--purpose", "verification", "--path", root)
            self.assertEqual(result[0], 2)
            self.assertFalse(root.parent.exists())
        with patch.object(workspace.tempfile, "gettempdir", return_value=str(self.base / "output")):
            self.assertEqual(self.call("create", "--purpose", "verification")[0], 2)

    def test_user_selected_output_and_deliverable_are_allowed(self):
        root = self.base / "output" / "explicit"
        self.assertEqual(self.call("create", "--purpose", "verification", "--path", root,
                                   "--user-selected-path")[0], 0)
        self.assertTrue(json.loads((root / workspace.MARKER).read_text(encoding="utf-8"))["user_selected_path"])
        delivered = root.parent / "delivery"
        self.assertEqual(self.call("create", "--purpose", "deliverable", "--path", delivered)[0], 0)
        self.assertEqual(list(delivered.iterdir()), [])
        self.assertEqual(self.call("create", "--purpose", "verification", "--user-selected-path")[0], 2)

    def test_custom_delivery_root_and_symlink_alias_are_checked(self):
        delivery = self.base / "delivery"
        self.assertEqual(self.call("create", "--purpose", "verification", "--path", delivery / "check",
                                   "--delivery-root", delivery)[0], 2)
        output = self.base / "output"
        output.mkdir()
        alias = self.base / "alias"
        try:
            alias.symlink_to(output, target_is_directory=True)
        except OSError:
            self.skipTest("symlinks unavailable")
        self.assertEqual(self.call("create", "--purpose", "verification", "--path", alias / "check")[0], 2)
        self.assertFalse((output / "check").exists())

    def test_existing_directory_and_unsafe_task_name_are_refused(self):
        root = self.create()
        (root / "keep.txt").write_bytes(b"user data")
        self.assertEqual(self.call("create", "--purpose", "verification", "--path", root)[0], 2)
        self.assertEqual(self.call("create", "--purpose", "verification", "--name", "../bad")[0], 2)
        self.assertEqual((root / "keep.txt").read_bytes(), b"user data")

    def test_unclassified_pending_and_removed_unclassified_fail_finish(self):
        root = self.create()
        (root / "download.zip").write_bytes(b"reproducible")
        self.assertEqual(self.call("finish", root)[0], 1)
        self.assertEqual(self.classify(root, "download.zip", "discard")[0], 0)
        self.assertEqual(self.call("finish", root)[0], 1)
        (root / "new.log").write_bytes(b"not classified")
        self.call("inventory", root)
        (root / "download.zip").unlink()
        (root / "new.log").unlink()
        code, output, _ = self.call("finish", root)
        self.assertEqual(code, 1)
        self.assertIn("unclassified-missing", output)

    def test_readback_compares_exact_bytes_and_requires_separate_copy(self):
        root = self.create()
        (root / "proof.json").write_bytes(b'{"ok":true}\r\n')
        readback = self.base / "readback.json"
        readback.write_bytes(b'{"ok":true}\n')
        opts = ("--wiki-path", "raw/2026-10-29_proof.json", "--readback")
        self.assertEqual(self.classify(root, "proof.json", "wiki", *opts, readback)[0], 2)
        self.assertEqual(self.classify(root, "proof.json", "wiki", *opts, root / "proof.json")[0], 2)
        readback.write_bytes((root / "proof.json").read_bytes())
        self.assertEqual(self.classify(root, "proof.json", "wiki", *opts, readback)[0], 0)
        self.assertEqual(self.call("finish", root)[0], 1)
        (root / "proof.json").unlink()
        code, output, _ = self.call("finish", root)
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(output)["files"]["proof.json"]["readback_verified"])

    def test_changed_file_invalidates_disposition(self):
        root = self.create()
        file = root / "download"
        file.write_bytes(b"old")
        self.classify(root, "download", "discard")
        file.write_bytes(b"changed")
        code, output, _ = self.call("finish", root)
        self.assertEqual(code, 1)
        self.assertIn("unclassified", output)
        self.assertEqual(file.read_bytes(), b"changed")

    def test_explicit_retention_is_verified_and_never_deleted(self):
        root = self.create()
        file = root / "original.pdf"
        file.write_bytes(b"original")
        self.assertEqual(self.classify(root, file.name, "keep")[0], 0)
        self.assertEqual(self.call("finish", root)[0], 0)
        self.assertTrue(file.exists())
        file.unlink()
        self.assertEqual(self.call("finish", root)[0], 1)

    def test_path_escape_and_external_symlink_are_refused(self):
        root = self.create()
        outside = self.base / "outside"
        outside.write_bytes(b"user")
        self.assertEqual(self.classify(root, "../outside", "discard")[0], 2)
        try:
            (root / "link").symlink_to(outside)
        except OSError:
            self.skipTest("symlinks unavailable")
        self.assertEqual(self.call("finish", root)[0], 2)
        self.assertEqual(outside.read_bytes(), b"user")

    def test_installed_helper_runs_in_symlink_and_snapshot_modes(self):
        for platform, snapshot in (("darwin", False), ("windows", False), ("windows", True)):
            with self.subTest(platform=platform, snapshot=snapshot):
                home = self.base / f"home-{platform}-{snapshot}"
                # Windows copy mode is exercised on every host, without claiming
                # that this is a native Windows runtime test.
                if platform == "darwin":
                    try:
                        (self.base / "symlink-probe").symlink_to(REPO, target_is_directory=True)
                    except OSError:
                        continue
                apply_environment(REPO, home=home, os_name=platform, snapshot=snapshot)
                installed = home / ".codex/tools/task-workspace.py"
                self.assertEqual(installed.is_symlink(), platform == "darwin")
                self.assertEqual(installed.read_bytes(), (REPO / "scripts/task-workspace.py").read_bytes())
                result = subprocess.run([sys.executable, str(installed), "create", "--purpose", "verification",
                                         "--path", str(home / "output" / "check")], capture_output=True)
                self.assertEqual(result.returncode, 2)
                self.assertFalse((home / "output").exists())


if __name__ == "__main__":
    unittest.main()
