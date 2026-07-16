from __future__ import annotations

from pathlib import Path
import json
import unittest


class RepoBundleTests(unittest.TestCase):
    def test_global_agents_instructions_include_codex_planning_routing(self) -> None:
        agents_path = Path(__file__).resolve().parents[1] / "instructions" / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")

        self.assertIn("## Skill Routing", text)
        self.assertIn("jy-autoplan", text)
        self.assertIn("jy-framing", text)
        self.assertIn("jy-grill-me", text)
        self.assertIn("jy-plan-review", text)
        self.assertIn("jy-writing-plans", text)
        self.assertIn("jy-worktrees", text)
        self.assertIn("jy-document-release", text)
        self.assertIn("jy-ship", text)
        self.assertIn("Shift+Tab", text)

    def test_global_agents_instructions_include_checkpoint_routing(self) -> None:
        agents_path = Path(__file__).resolve().parents[1] / "instructions" / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")

        self.assertIn("jy-checkpoint", text)
        self.assertIn(".codex/checkpoints/", text)

    def test_global_agents_instructions_include_native_skill_discovery_surface(self) -> None:
        agents_path = Path(__file__).resolve().parents[1] / "instructions" / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")

        self.assertIn("~/.agents/skills/", text)
        self.assertIn("~/plugins", text)
        self.assertIn("source-owned install surface", text)
        self.assertNotIn("repo-managed hook", text)

    def test_global_agents_instructions_include_user_language_response_rule(self) -> None:
        agents_path = Path(__file__).resolve().parents[1] / "instructions" / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")

        self.assertIn("## Response Language", text)
        self.assertIn("user's language", text)
        self.assertIn("output-language rule", text)

    def test_readme_groups_short_skill_names_by_role(self) -> None:
        readme_path = Path(__file__).resolve().parents[1] / "README.md"
        text = readme_path.read_text(encoding="utf-8")

        self.assertIn("## First-Party Skill Catalog", text)
        self.assertIn("### Planning", text)
        self.assertIn("### Execution", text)
        self.assertIn("### Audit", text)
        self.assertIn("### Research", text)
        self.assertIn("### Maintenance", text)
        self.assertIn("### Authoring", text)
        self.assertIn("`jy-autoplan`", text)
        self.assertIn("`jy-grill-me`", text)
        self.assertIn("`jy-writing-plans`", text)
        self.assertIn("`jy-worktrees`", text)
        self.assertIn("`jy-test-driven`", text)
        self.assertIn("`jy-executing-plans`", text)
        self.assertIn("`jy-receiving-review`", text)
        self.assertIn("`jy-review-all`", text)
        self.assertIn("`jy-ship`", text)
        self.assertIn("`jy-env-sync-admin`", text)
        self.assertIn("`jy-writing-skills`", text)

    def test_readme_language_switch_and_korean_doc_exist(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        english = (repo_root / "README.md").read_text(encoding="utf-8")
        korean_path = repo_root / "README.ko.md"
        korean = korean_path.read_text(encoding="utf-8")

        self.assertTrue(korean_path.exists())
        self.assertIn("./README.ko.md", english)
        self.assertIn("./README.md", korean)
        self.assertIn("Language-English", english)
        self.assertIn("Language-Korean", english)
        self.assertIn("## First-Party Skill Catalog", korean)

    def test_codex_env_core_bundle_has_no_mcp_server_definition(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        plugin_json = json.loads(
            (repo_root / "plugins" / "jy-env-core" / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )

        self.assertNotIn("mcpServers", plugin_json)
        self.assertFalse((repo_root / "plugins" / "jy-env-core" / ".mcp.json").exists())

    def test_plugin_metadata_and_license_match_this_repository(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        plugin_json = json.loads(
            (repo_root / "plugins" / "jy-env-core" / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        repository = "https://github.com/jy1655/codex-local-plugins"

        self.assertEqual(plugin_json["repository"], repository)
        self.assertEqual(plugin_json["homepage"], repository)
        self.assertEqual(plugin_json["interface"]["websiteURL"], repository)
        self.assertEqual(plugin_json["interface"]["developerName"], "JaeYoung Hwang")
        self.assertNotIn("privacyPolicyURL", plugin_json["interface"])
        self.assertNotIn("termsOfServiceURL", plugin_json["interface"])
        self.assertEqual(plugin_json["author"]["url"], "https://github.com/jy1655")
        self.assertNotIn("email", plugin_json["author"])
        license_text = (repo_root / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", license_text)
        self.assertIn("JaeYoung Hwang", license_text)

    def test_repo_uses_instruction_only_necessity_gate(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        manifest_text = (repo_root / "codex-env.toml").read_text(encoding="utf-8")
        agents_text = (repo_root / "instructions" / "AGENTS.md").read_text(encoding="utf-8")

        self.assertNotIn("[[hooks]]", manifest_text)
        self.assertFalse((repo_root / "hooks" / "necessity-gate.json").exists())
        self.assertFalse((repo_root / "plugins" / "jy-env-core" / "hooks" / "necessity_gate.py").exists())
        self.assertIn("## Necessity Gate", agents_text)

    def test_codex_env_core_bundle_includes_writing_skills(self) -> None:
        skill_root = Path(__file__).resolve().parents[1] / "plugins" / "jy-env-core" / "skills" / "jy-writing-skills"

        self.assertTrue((skill_root / "SKILL.md").exists())
        self.assertTrue((skill_root / "references" / "skill-testing-guide.md").exists())
        self.assertTrue((skill_root / "references" / "graphviz-conventions.dot").exists())
        self.assertTrue((skill_root / "agents" / "openai.yaml").exists())

    def test_codex_env_core_bundle_includes_codex_planning_skills(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        skill_root = repo_root / "plugins" / "jy-env-core" / "skills"

        self.assertTrue((skill_root / "jy-framing" / "SKILL.md").exists())
        self.assertTrue((skill_root / "jy-framing" / "agents" / "openai.yaml").exists())
        self.assertTrue((skill_root / "jy-plan-review" / "SKILL.md").exists())
        self.assertTrue((skill_root / "jy-plan-review" / "agents" / "openai.yaml").exists())
        self.assertTrue((skill_root / "jy-autoplan" / "SKILL.md").exists())
        self.assertTrue((skill_root / "jy-autoplan" / "agents" / "openai.yaml").exists())
        self.assertTrue((skill_root / "jy-writing-plans" / "SKILL.md").exists())
        self.assertTrue((skill_root / "jy-writing-plans" / "agents" / "openai.yaml").exists())
        self.assertTrue((skill_root / "jy-worktrees" / "SKILL.md").exists())
        self.assertTrue((skill_root / "jy-worktrees" / "agents" / "openai.yaml").exists())

    def test_plugin_skill_root_contains_only_discoverable_skill_directories(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        skill_root = repo_root / "plugins" / "jy-env-core" / "skills"

        for child in sorted(path for path in skill_root.iterdir() if path.is_dir()):
            with self.subTest(skill=child.name):
                self.assertTrue((child / "SKILL.md").is_file())
                self.assertTrue((child / "agents" / "openai.yaml").is_file())

    def test_codex_env_core_bundle_includes_codex_checkpoint(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        skill_root = repo_root / "plugins" / "jy-env-core" / "skills" / "jy-checkpoint"

        self.assertTrue((skill_root / "SKILL.md").exists())
        self.assertTrue((skill_root / "agents" / "openai.yaml").exists())

    def test_codex_env_core_bundle_includes_codex_document_release(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        skill_root = repo_root / "plugins" / "jy-env-core" / "skills" / "jy-document-release"

        self.assertTrue((skill_root / "SKILL.md").exists())
        self.assertTrue((skill_root / "agents" / "openai.yaml").exists())

    def test_codex_env_core_bundle_includes_ship_workflow(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        skill_root = repo_root / "plugins" / "jy-env-core" / "skills" / "jy-ship"

        self.assertTrue((skill_root / "SKILL.md").exists())
        self.assertTrue((skill_root / "agents" / "openai.yaml").exists())

    def test_codex_env_core_bundle_includes_debugging_and_verification_workflow_skills(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        skill_root = repo_root / "plugins" / "jy-env-core" / "skills"

        for skill_name in [
            "jy-debugging",
            "jy-test-driven",
            "jy-executing-plans",
            "jy-receiving-review",
            "jy-verification-before-completion",
        ]:
            with self.subTest(skill=skill_name):
                self.assertTrue((skill_root / skill_name / "SKILL.md").exists())
                self.assertTrue((skill_root / skill_name / "agents" / "openai.yaml").exists())

    def test_global_agents_instructions_include_execution_skill_routing(self) -> None:
        agents_path = Path(__file__).resolve().parents[1] / "instructions" / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")

        self.assertIn("## Execution Skill Routing", text)
        self.assertIn("jy-review-work", text)
        self.assertNotIn("jy-loop", text)
        self.assertIn("jy-slop-remover", text)
        self.assertIn("jy-debugging", text)
        self.assertIn("jy-test-driven", text)
        self.assertIn("jy-executing-plans", text)
        self.assertIn("jy-receiving-review", text)
        self.assertIn("jy-ship", text)
        self.assertIn("jy-verification-before-completion", text)

    def test_global_agents_instructions_include_advisory_skill_routing(self) -> None:
        agents_path = Path(__file__).resolve().parents[1] / "instructions" / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")

        self.assertIn("## Advisory and Research Skill Routing", text)
        self.assertIn("jy-consult", text)
        self.assertIn("jy-review-all", text)
        self.assertIn("jy-library-research", text)
        self.assertIn("jy-codebase-explore", text)
        self.assertNotIn("jy-intent-gate", text)

    def test_retired_routing_and_loop_skills_are_absent(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        skill_root = repo_root / "plugins" / "jy-env-core" / "skills"
        scenario_root = repo_root / "skill-tests" / "first-party"

        for skill_name in ["jy-intent-gate", "jy-loop"]:
            with self.subTest(skill=skill_name):
                self.assertFalse((skill_root / skill_name).exists())
                self.assertFalse((scenario_root / skill_name).exists())

    def test_codex_env_core_bundle_includes_change_guardrails_skill(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        skill_root = repo_root / "plugins" / "jy-env-core" / "skills" / "jy-change-guardrails"

        self.assertTrue((skill_root / "SKILL.md").exists())
        self.assertTrue((skill_root / "agents" / "openai.yaml").exists())

    def test_codex_env_core_bundle_includes_grill_me_skill(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        skill_root = repo_root / "plugins" / "jy-env-core" / "skills" / "jy-grill-me"

        self.assertTrue((skill_root / "SKILL.md").exists())
        self.assertTrue((skill_root / "agents" / "openai.yaml").exists())

    def test_codex_env_core_bundle_includes_review_all_skill(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        skill_root = repo_root / "plugins" / "jy-env-core" / "skills" / "jy-review-all"

        self.assertTrue((skill_root / "SKILL.md").exists())
        self.assertTrue((skill_root / "agents" / "openai.yaml").exists())

    def test_readme_lists_change_guardrails_in_execution_catalog(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        english = (repo_root / "README.md").read_text(encoding="utf-8")
        korean = (repo_root / "README.ko.md").read_text(encoding="utf-8")

        self.assertIn("`jy-change-guardrails`", english)
        self.assertIn("`jy-change-guardrails`", korean)

    def test_readme_lists_grill_me_in_planning_catalog(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        english = (repo_root / "README.md").read_text(encoding="utf-8")
        korean = (repo_root / "README.ko.md").read_text(encoding="utf-8")

        self.assertIn("`jy-grill-me`", english)
        self.assertIn("`jy-grill-me`", korean)

    def test_readme_lists_review_all_in_audit_catalog(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        english = (repo_root / "README.md").read_text(encoding="utf-8")
        korean = (repo_root / "README.ko.md").read_text(encoding="utf-8")

        self.assertIn("`jy-review-all`", english)
        self.assertIn("`jy-review-all`", korean)

    def test_repo_no_longer_tracks_vendored_skill_runtime(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        self.assertFalse((repo_root / ".agents" / "skills").exists())


if __name__ == "__main__":
    unittest.main()
