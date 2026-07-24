from __future__ import annotations

from pathlib import Path
import json
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_ROOT = REPO_ROOT / "skill-tests" / "first-party"


def first_party_skill_dirs() -> list[Path]:
    return sorted(
        path.parent
        for path in REPO_ROOT.glob("plugins/jy-env-*/skills/*/SKILL.md")
    )


def scenario_dirs() -> list[Path]:
    return sorted(path for path in SCENARIO_ROOT.iterdir() if path.is_dir())


class FirstPartySkillScenarioAssetTests(unittest.TestCase):
    def test_each_first_party_skill_has_one_pressure_scenario_asset(self) -> None:
        skill_names = {path.name for path in first_party_skill_dirs()}
        scenario_names = {path.name for path in scenario_dirs()}
        self.assertEqual(scenario_names, skill_names)

        for scenario_dir in scenario_dirs():
            with self.subTest(skill=scenario_dir.name):
                files = sorted(path.name for path in scenario_dir.iterdir() if path.is_file())
                self.assertEqual(files, ["pressure-scenarios.json"])

    def test_pressure_scenario_assets_follow_the_manual_schema(self) -> None:
        all_ids: set[str] = set()
        required_fields = {
            "id",
            "title",
            "prompt",
            "expected_without_skill",
            "expected_with_skill",
        }

        for skill_dir in first_party_skill_dirs():
            with self.subTest(skill=skill_dir.name):
                scenario_file = SCENARIO_ROOT / skill_dir.name / "pressure-scenarios.json"
                data = json.loads(scenario_file.read_text(encoding="utf-8"))
                self.assertEqual(set(data), {"scenarios"})
                self.assertIsInstance(data["scenarios"], list)
                self.assertGreaterEqual(len(data["scenarios"]), 2)

                for scenario in data["scenarios"]:
                    self.assertEqual(set(scenario), required_fields)
                    for field in required_fields:
                        self.assertIsInstance(scenario[field], str)
                        self.assertTrue(scenario[field].strip())
                    scenario_id = f"{skill_dir.name}:{scenario['id']}"
                    self.assertNotIn(scenario_id, all_ids)
                    all_ids.add(scenario_id)

    def test_mode_aware_assets_include_plan_mode_pressure(self) -> None:
        mode_aware_skills = [
            "jy-slop-remover",
            "jy-framing",
            "jy-plan-review",
            "jy-autoplan",
            "jy-grill-me",
            "jy-writing-plans",
            "jy-worktrees",
            "jy-checkpoint",
            "jy-document-release",
            "jy-review-all",
            "jy-review-work",
            "jy-debugging",
            "jy-test-driven",
            "jy-executing-plans",
            "jy-receiving-review",
            "jy-ship",
            "jy-waterfall",
            "jy-verification-before-completion",
        ]
        for skill_name in mode_aware_skills:
            with self.subTest(skill=skill_name):
                text = (SCENARIO_ROOT / skill_name / "pressure-scenarios.json").read_text(encoding="utf-8")
                self.assertIn("Shift+Tab", text)
                self.assertIn("Plan Mode", text)

    def test_ship_asset_covers_stale_verification_and_pre_push_doc_sync(self) -> None:
        text = (SCENARIO_ROOT / "jy-ship" / "pressure-scenarios.json").read_text(encoding="utf-8")
        self.assertIn("stale CI result", text)
        self.assertIn("jy-document-release", text)
        self.assertIn("before final verification and push", text)

    def test_waterfall_asset_covers_approval_time_and_secret_gates(self) -> None:
        text = (SCENARIO_ROOT / "jy-waterfall" / "pressure-scenarios.json").read_text(encoding="utf-8")
        self.assertIn("explicit approval", text)
        self.assertIn("must not run `gh issue create`", text)
        self.assertIn("YYYYMMDDTHHMM", text)
        self.assertIn("2-3 hours", text)
        self.assertIn("secret", text)
        self.assertIn("private repo", text)
        self.assertIn("gitignored", text)
        self.assertIn("Plan Mode", text)


if __name__ == "__main__":
    unittest.main()
