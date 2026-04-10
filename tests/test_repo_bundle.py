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
        self.assertIn("source-owned install surface", text)

    def test_readme_groups_short_skill_names_by_role(self) -> None:
        readme_path = Path(__file__).resolve().parents[1] / "README.md"
        text = readme_path.read_text(encoding="utf-8")

        self.assertIn("## First-Party Skill Catalog", text)
        self.assertIn("### Planning", text)
        self.assertIn("### Execution", text)
        self.assertIn("### Routing", text)
        self.assertIn("### Research", text)
        self.assertIn("### Maintenance", text)
        self.assertIn("### Authoring", text)
        self.assertIn("`jy-autoplan`", text)
        self.assertIn("`jy-writing-plans`", text)
        self.assertIn("`jy-worktrees`", text)
        self.assertIn("`jy-test-driven`", text)
        self.assertIn("`jy-executing-plans`", text)
        self.assertIn("`jy-receiving-review`", text)
        self.assertIn("`jy-intent-gate`", text)
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

    def test_codex_env_core_bundle_includes_korean_law_mcp(self) -> None:
        mcp_path = Path(__file__).resolve().parents[1] / "plugins" / "jy-env-core" / ".mcp.json"
        data = json.loads(mcp_path.read_text(encoding="utf-8"))

        server = data["mcpServers"]["korean-law"]
        self.assertEqual(server["command"], "npx")
        self.assertEqual(server["args"], ["-y", "korean-law-mcp"])

    def test_codex_env_core_bundle_includes_writing_skills(self) -> None:
        skill_root = Path(__file__).resolve().parents[1] / "plugins" / "jy-env-core" / "skills" / "jy-writing-skills"

        self.assertTrue((skill_root / "SKILL.md").exists())
        self.assertTrue((skill_root / "references" / "skill-testing-guide.md").exists())
        self.assertTrue((skill_root / "references" / "graphviz-conventions.dot").exists())
        self.assertTrue((skill_root / "agents" / "openai.yaml").exists())

    def test_codex_env_core_bundle_includes_codex_planning_pack(self) -> None:
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
        self.assertTrue((skill_root / "_shared" / "jy-planning-pack.md").exists())

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
        self.assertIn("jy-loop", text)
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
        self.assertIn("jy-library-research", text)
        self.assertIn("jy-codebase-explore", text)
        self.assertIn("jy-intent-gate", text)

    def test_repo_no_longer_tracks_vendored_skill_runtime(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        self.assertFalse((repo_root / ".agents" / "skills").exists())


if __name__ == "__main__":
    unittest.main()
