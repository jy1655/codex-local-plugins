import importlib.util
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
