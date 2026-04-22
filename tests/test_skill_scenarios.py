from __future__ import annotations

from pathlib import Path
import json
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
FIRST_PARTY_SKILL_ROOT = REPO_ROOT / "plugins" / "jy-env-core" / "skills"
SCENARIO_ROOT = REPO_ROOT / "skill-tests" / "first-party"


def first_party_skill_dirs() -> list[Path]:
    return sorted(path for path in FIRST_PARTY_SKILL_ROOT.iterdir() if (path / "SKILL.md").exists())


class FirstPartySkillScenarioTests(unittest.TestCase):
    def test_new_workflow_skills_have_scenario_packs(self) -> None:
        for skill_name in [
            "jy-debugging",
            "jy-test-driven",
            "jy-writing-plans",
            "jy-worktrees",
            "jy-executing-plans",
            "jy-receiving-review",
            "jy-ship",
            "jy-waterfall",
            "jy-verification-before-completion",
        ]:
            with self.subTest(skill=skill_name):
                scenario_dir = SCENARIO_ROOT / skill_name
                self.assertTrue((FIRST_PARTY_SKILL_ROOT / skill_name / "SKILL.md").exists())
                self.assertTrue((scenario_dir / "README.md").exists())
                self.assertTrue((scenario_dir / "baseline.md").exists())
                self.assertTrue((scenario_dir / "pressure-scenarios.json").exists())
                self.assertTrue((scenario_dir / "result-template.md").exists())

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
            "jy-slop-remover",
            "jy-framing",
            "jy-plan-review",
            "jy-autoplan",
            "jy-writing-plans",
            "jy-worktrees",
            "jy-checkpoint",
            "jy-document-release",
            "jy-intent-gate",
            "jy-review-work",
            "jy-loop",
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
                scenario_file = SCENARIO_ROOT / skill_name / "pressure-scenarios.json"
                text = scenario_file.read_text(encoding="utf-8")
                self.assertIn("Shift+Tab", text)
                self.assertIn("Plan Mode", text)

    def test_ship_pressure_pack_covers_stale_verification_and_doc_sync_shortcuts(self) -> None:
        scenario_file = SCENARIO_ROOT / "jy-ship" / "pressure-scenarios.json"
        text = scenario_file.read_text(encoding="utf-8")

        self.assertIn("old CI run", text)
        self.assertIn("jy-document-release", text)
        self.assertIn("docs", text)

    def test_korean_law_search_pack_covers_real_world_two_part_answers(self) -> None:
        scenario_file = SCENARIO_ROOT / "jy-korean-law-search" / "pressure-scenarios.json"
        result_template = (SCENARIO_ROOT / "jy-korean-law-search" / "result-template.md").read_text(encoding="utf-8")
        baseline = (SCENARIO_ROOT / "jy-korean-law-search" / "baseline.md").read_text(encoding="utf-8")
        text = scenario_file.read_text(encoding="utf-8")

        self.assertIn("실제 분쟁", baseline)
        self.assertIn("pure legal lookup", text)
        self.assertIn("real-world", text)
        self.assertIn("General legal answer", text)
        self.assertIn("Practical answer", text)
        self.assertIn("does not force the two-part answer shape", text)
        self.assertIn("directly relevant precedent", text)
        self.assertIn("For a pure legal lookup, did it avoid forcing the general legal answer / practical answer split", result_template)
        self.assertIn("Did it separate the general legal answer from the practical answer", result_template)
        self.assertIn("Did it hold back the practical answer when directly relevant support was missing", result_template)

    def test_waterfall_pressure_pack_covers_approval_time_and_secret_gates(self) -> None:
        scenario_file = SCENARIO_ROOT / "jy-waterfall" / "pressure-scenarios.json"
        text = scenario_file.read_text(encoding="utf-8")

        self.assertIn("explicit approval", text)
        self.assertIn("must not run `gh issue create`", text)
        self.assertIn("YYYYMMDDTHHMM", text)
        self.assertIn("2-3 hours", text)
        self.assertIn("secret", text)
        self.assertIn("private repo", text)
        self.assertIn("gitignored", text)
        self.assertIn("Plan Mode", text)

    def test_output_template_skill_packs_track_response_language(self) -> None:
        for skill_name in [
            "jy-ship",
            "jy-checkpoint",
            "jy-document-release",
            "jy-env-sync-admin",
        ]:
            with self.subTest(skill=skill_name):
                readme = (SCENARIO_ROOT / skill_name / "README.md").read_text(encoding="utf-8")
                result_template = (SCENARIO_ROOT / skill_name / "result-template.md").read_text(encoding="utf-8")
                self.assertIn("user's language", readme)
                self.assertIn("Observed response language", result_template)




if __name__ == "__main__":
    unittest.main()
