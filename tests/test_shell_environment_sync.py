import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest


spec = importlib.util.spec_from_file_location(
    "shell_environment_sync", Path(__file__).parents[1] / "scripts/sync-shell-environment.py"
)
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class ShellEnvironmentSyncTests(unittest.TestCase):
    def test_preserves_existing_settings_and_set_child(self):
        text = '# local settings\nmodel = "unchanged"\n[shell_environment_policy.set]\nSAFE_FLAG = "1"\n'
        result = sync.update(text)
        self.assertTrue(result.startswith(text))
        config = tomllib.loads(result)
        self.assertEqual(config["model"], "unchanged")
        self.assertEqual(config["shell_environment_policy"]["set"], {"SAFE_FLAG": "1"})

    def test_preserves_multiline_exclusions_and_other_tables(self):
        text = '[shell_environment_policy]\nexclude = [\n "OLD_*", # existing policy\n]\ninherit = "core"\n[other]\nvalue = 3\n'
        result = tomllib.loads(sync.update(text))
        self.assertEqual(result["shell_environment_policy"]["exclude"], ["OLD_*", sync.VARIABLE])
        self.assertEqual(result["shell_environment_policy"]["inherit"], "core")
        self.assertEqual(result["other"], {"value": 3})

    def test_existing_parent_table(self):
        result = tomllib.loads(sync.update('[shell_environment_policy]\ninherit = "all"\n'))
        self.assertEqual(result["shell_environment_policy"]["exclude"], [sync.VARIABLE])

    def test_idempotent(self):
        text = sync.update("")
        self.assertEqual(sync.update(text), text)

    def test_existing_case_insensitive_exclusion(self):
        text = '[shell_environment_policy]\nexclude = ["claude_code_effort_level"]\n'
        self.assertEqual(sync.update(text), text)

    def test_rejects_set_that_would_restore_the_override(self):
        with self.assertRaises(ValueError):
            sync.update('[shell_environment_policy.set]\nCLAUDE_CODE_EFFORT_LEVEL = "max"\n')

    def test_rejects_mixed_filter_formats(self):
        with self.assertRaises(ValueError):
            sync.update('[shell_environment_policy.filters]\n"OTHER_*" = "exclude"\n')

    def test_rejects_invalid_toml(self):
        with self.assertRaises(ValueError):
            sync.update('[shell_environment_policy]\nexclude = [')

    def test_cli_replaces_existing_file_and_preserves_settings(self):
        with tempfile.TemporaryDirectory() as root:
            target = Path(root) / "config.toml"
            target.write_text('model = "unchanged"\n[shell_environment_policy]\nexclude = ["OLD_*"]\n',
                              encoding="utf-8")
            command = [sys.executable, "-X", "utf8", "-B", str(Path(sync.__file__)), "--config", str(target)]
            applied = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(applied.returncode, 0, applied.stderr)
            first = target.read_bytes()
            self.assertEqual(tomllib.loads(first.decode("utf-8")), {
                "model": "unchanged",
                "shell_environment_policy": {"exclude": ["OLD_*", sync.VARIABLE]},
            })
            checked = subprocess.run(command + ["--check"], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(checked.returncode, 0, checked.stderr)
            repeated = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(repeated.returncode, 0, repeated.stderr)
            self.assertEqual(target.read_bytes(), first)
            self.assertEqual(list(Path(root).iterdir()), [target])


if __name__ == "__main__":
    unittest.main()
