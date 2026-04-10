from __future__ import annotations

from pathlib import Path
import json
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
FIRST_PARTY_SKILL_ROOT = REPO_ROOT / "plugins" / "codex-env-core" / "skills"
SCENARIO_ROOT = REPO_ROOT / "skill-tests" / "first-party"


def first_party_skill_dirs() -> list[Path]:
    return sorted(path for path in FIRST_PARTY_SKILL_ROOT.iterdir() if (path / "SKILL.md").exists())


class FirstPartySkillScenarioTests(unittest.TestCase):
    def test_each_first_party_skill_has_a_scenario_pack(self) -> None:
        for skill_dir in first_party_skill_dirs():
            with self.subTest(skill=skill_dir.name):
                scenario_dir = SCENARIO_ROOT / skill_dir.name
                self.assertTrue((scenario_dir / "README.md").exists())
                self.assertTrue((scenario_dir / "baseline.md").exists())
                self.assertTrue((scenario_dir / "pressure-scenarios.json").exists())
                self.assertTrue((scenario_dir / "result-template.md").exists())

    def test_pressure_scenario_packs_define_at_least_two_cases(self) -> None:
        for skill_dir in first_party_skill_dirs():
            with self.subTest(skill=skill_dir.name):
                scenario_file = SCENARIO_ROOT / skill_dir.name / "pressure-scenarios.json"
                data = json.loads(scenario_file.read_text(encoding="utf-8"))
                self.assertGreaterEqual(len(data["scenarios"]), 2)

    def test_pressure_scenarios_capture_expected_behavior(self) -> None:
        for skill_dir in first_party_skill_dirs():
            with self.subTest(skill=skill_dir.name):
                scenario_file = SCENARIO_ROOT / skill_dir.name / "pressure-scenarios.json"
                data = json.loads(scenario_file.read_text(encoding="utf-8"))
                for scenario in data["scenarios"]:
                    self.assertIn("id", scenario)
                    self.assertIn("prompt", scenario)
                    self.assertIn("expected_without_skill", scenario)
                    self.assertIn("expected_with_skill", scenario)

    def test_mode_aware_skill_packs_cover_collaboration_mode_cases(self) -> None:
        mode_aware_skills = [
            "ai-slop-remover",
            "codex-office-hours",
            "codex-plan-review",
            "codex-autoplan",
            "codex-checkpoint",
            "codex-document-release",
            "intent-gate",
            "review-work",
            "work-loop",
        ]
        for skill_name in mode_aware_skills:
            with self.subTest(skill=skill_name):
                scenario_file = SCENARIO_ROOT / skill_name / "pressure-scenarios.json"
                text = scenario_file.read_text(encoding="utf-8")
                self.assertIn("Shift+Tab", text)
                self.assertIn("Plan Mode", text)




if __name__ == "__main__":
    unittest.main()
