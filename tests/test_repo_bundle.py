from __future__ import annotations

from pathlib import Path
import json
import unittest


class RepoBundleTests(unittest.TestCase):
    def test_global_agents_instructions_include_codex_planning_routing(self) -> None:
        agents_path = Path(__file__).resolve().parents[1] / "instructions" / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")

        self.assertIn("## Skill Routing", text)
        self.assertIn("codex-autoplan", text)
        self.assertIn("codex-office-hours", text)
        self.assertIn("codex-plan-review", text)
        self.assertIn("codex-document-release", text)
        self.assertIn("Shift+Tab", text)

    def test_global_agents_instructions_include_checkpoint_routing(self) -> None:
        agents_path = Path(__file__).resolve().parents[1] / "instructions" / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")

        self.assertIn("codex-checkpoint", text)
        self.assertIn(".codex/checkpoints/", text)

    def test_global_agents_instructions_include_native_skill_discovery_surface(self) -> None:
        agents_path = Path(__file__).resolve().parents[1] / "instructions" / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")

        self.assertIn("~/.agents/skills/", text)
        self.assertIn("source-owned install surface", text)

    def test_codex_env_core_bundle_includes_korean_law_mcp(self) -> None:
        mcp_path = Path(__file__).resolve().parents[1] / "plugins" / "codex-env-core" / ".mcp.json"
        data = json.loads(mcp_path.read_text(encoding="utf-8"))

        server = data["mcpServers"]["korean-law"]
        self.assertEqual(server["command"], "npx")
        self.assertEqual(server["args"], ["-y", "korean-law-mcp"])

    def test_codex_env_core_bundle_includes_writing_skills(self) -> None:
        skill_root = Path(__file__).resolve().parents[1] / "plugins" / "codex-env-core" / "skills" / "writing-skills"

        self.assertTrue((skill_root / "SKILL.md").exists())
        self.assertTrue((skill_root / "references" / "skill-testing-guide.md").exists())
        self.assertTrue((skill_root / "references" / "graphviz-conventions.dot").exists())
        self.assertTrue((skill_root / "agents" / "openai.yaml").exists())

    def test_codex_env_core_bundle_includes_codex_planning_pack(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        skill_root = repo_root / "plugins" / "codex-env-core" / "skills"

        self.assertTrue((skill_root / "codex-office-hours" / "SKILL.md").exists())
        self.assertTrue((skill_root / "codex-office-hours" / "agents" / "openai.yaml").exists())
        self.assertTrue((skill_root / "codex-plan-review" / "SKILL.md").exists())
        self.assertTrue((skill_root / "codex-plan-review" / "agents" / "openai.yaml").exists())
        self.assertTrue((skill_root / "codex-autoplan" / "SKILL.md").exists())
        self.assertTrue((skill_root / "codex-autoplan" / "agents" / "openai.yaml").exists())
        self.assertTrue((skill_root / "_shared" / "codex-planning-pack.md").exists())

    def test_codex_env_core_bundle_includes_codex_checkpoint(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        skill_root = repo_root / "plugins" / "codex-env-core" / "skills" / "codex-checkpoint"

        self.assertTrue((skill_root / "SKILL.md").exists())
        self.assertTrue((skill_root / "agents" / "openai.yaml").exists())

    def test_codex_env_core_bundle_includes_codex_document_release(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        skill_root = repo_root / "plugins" / "codex-env-core" / "skills" / "codex-document-release"

        self.assertTrue((skill_root / "SKILL.md").exists())
        self.assertTrue((skill_root / "agents" / "openai.yaml").exists())

    def test_codex_env_core_bundle_includes_debugging_and_verification_workflow_skills(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        skill_root = repo_root / "plugins" / "codex-env-core" / "skills"

        for skill_name in [
            "systematic-debugging",
            "test-driven-development",
            "verification-before-completion",
        ]:
            with self.subTest(skill=skill_name):
                self.assertTrue((skill_root / skill_name / "SKILL.md").exists())
                self.assertTrue((skill_root / skill_name / "agents" / "openai.yaml").exists())

    def test_global_agents_instructions_include_execution_skill_routing(self) -> None:
        agents_path = Path(__file__).resolve().parents[1] / "instructions" / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")

        self.assertIn("## Execution Skill Routing", text)
        self.assertIn("review-work", text)
        self.assertIn("work-loop", text)
        self.assertIn("ai-slop-remover", text)
        self.assertIn("systematic-debugging", text)
        self.assertIn("test-driven-development", text)
        self.assertIn("verification-before-completion", text)

    def test_global_agents_instructions_include_advisory_skill_routing(self) -> None:
        agents_path = Path(__file__).resolve().parents[1] / "instructions" / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")

        self.assertIn("## Advisory and Research Skill Routing", text)
        self.assertIn("oracle-consult", text)
        self.assertIn("library-research", text)
        self.assertIn("codebase-explore", text)
        self.assertIn("intent-gate", text)

    def test_repo_no_longer_tracks_vendored_skill_runtime(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        self.assertFalse((repo_root / ".agents" / "skills").exists())


if __name__ == "__main__":
    unittest.main()
