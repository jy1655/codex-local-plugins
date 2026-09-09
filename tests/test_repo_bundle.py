from __future__ import annotations

from pathlib import Path
import json
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


def plugin_roots() -> list[Path]:
    return sorted(
        path.parent.parent
        for path in REPO_ROOT.glob("plugins/jy-env-*/.codex-plugin/plugin.json")
    )


def skill_paths() -> list[Path]:
    return sorted(REPO_ROOT.glob("plugins/jy-env-*/skills/*/SKILL.md"))


class RepoBundleTests(unittest.TestCase):
    def test_personalization_survives_workflow_archival(self) -> None:
        text = (REPO_ROOT / "instructions" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("in English", text)
        self.assertIn("in Korean", text)
        self.assertIn("independently of whether a workflow skill is installed", text)
        self.assertIn("user explicitly asks otherwise", text)
        for root in plugin_roots():
            manifest = json.loads((root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
            for field in ["displayName", "shortDescription", "longDescription"]:
                self.assertRegex(manifest["interface"][field], r"[가-힣]")
            for prompt in manifest["interface"]["defaultPrompt"]:
                self.assertRegex(prompt, r"[가-힣]")
        for path in skill_paths():
            text = (path.parent / "agents" / "openai.yaml").read_text(encoding="utf-8")
            for field in ["display_name", "short_description", "default_prompt"]:
                match = re.search(rf"^  {field}: (.+)$", text, re.MULTILINE)
                self.assertIsNotNone(match)
                self.assertRegex(match.group(1), r"[가-힣]")

    def test_global_agents_uses_session_skill_availability(self) -> None:
        text = (REPO_ROOT / "instructions" / "AGENTS.md").read_text(encoding="utf-8")

        self.assertIn("## Skill Availability", text)
        self.assertNotIn("## Pack Model", text)
        self.assertIn("actually available", text)
        self.assertNotIn("## Skill Routing", text)
        self.assertNotIn("## Execution Skill Routing", text)
        self.assertNotIn("## Advisory and Research Skill Routing", text)

    def test_global_agents_keeps_environment_safety_and_language(self) -> None:
        text = (REPO_ROOT / "instructions" / "AGENTS.md").read_text(encoding="utf-8")

        self.assertIn("source repository", text)
        self.assertIn("Do not edit `~/.codex/plugins/cache` directly", text)
        self.assertNotIn("~/.agents/skills/", text)
        self.assertNotIn("plugins/jy-env-*/skills/", text)
        self.assertIn("## Response Language", text)
        self.assertIn("user's language", text)
        self.assertIn("output-language rule", text)
        self.assertIn("LOCAL.md", text)
        self.assertNotIn("/Users/", text)
        self.assertNotIn("this Mac only", text)

    def test_global_agents_omits_repo_rules_and_duplicate_necessity_gate(self) -> None:
        manifest_text = (REPO_ROOT / "codex-env.toml").read_text(encoding="utf-8")
        agents_text = (REPO_ROOT / "instructions" / "AGENTS.md").read_text(encoding="utf-8")

        self.assertNotIn("[[hooks]]", manifest_text)
        self.assertFalse((REPO_ROOT / "hooks" / "necessity-gate.json").exists())
        self.assertNotIn("## Repo Rules", agents_text)
        self.assertNotIn("## Necessity Gate", agents_text)
        self.assertNotIn("[necessity-gate]", agents_text)

    def test_global_agents_prefers_native_context_and_limits_hard_gates(self) -> None:
        text = (REPO_ROOT / "instructions" / "AGENTS.md").read_text(encoding="utf-8")

        self.assertIn("## Native Capability and Gate Policy", text)
        self.assertIn("session state", text)
        self.assertIn("context compression", text)
        self.assertIn("concrete handoff", text)
        self.assertIn("required approvals", text)
        self.assertIn("permissions", text)
        self.assertIn("read-only exploration", text)
        self.assertIn("uncertainty or stale evidence", text)

    def test_global_agents_keeps_scope_and_safety_boundaries(self) -> None:
        text = (REPO_ROOT / "instructions" / "AGENTS.md").read_text(encoding="utf-8")

        self.assertIn("simplest approach", text)
        self.assertIn("demonstrated needs", text)
        self.assertIn("requested scope", text)
        self.assertIn("necessary checks", text)
        self.assertIn("Protect secrets", text)
        self.assertIn("least privilege", text)
        self.assertIn("owner's explicit approval", text)

    def test_skill_utility_evaluation_preserves_safety_boundaries(self) -> None:
        text = (REPO_ROOT / "skill-tests" / "UTILITY-EVAL.md").read_text(encoding="utf-8")

        self.assertIn("maximum task performance", text)
        self.assertIn("minimum context, routing, and procedural weight", text)
        self.assertIn("ablated baseline", text)
        self.assertIn("representative direct feedback", text)
        self.assertIn("does not authorize", text)
        self.assertIn("harness owner's explicit approval", text)

    def test_all_plugin_manifests_match_repository_metadata_and_limit_mcp_to_ios(self) -> None:
        repository = "https://github.com/jy1655/codex-local-plugins"
        self.assertEqual(
            {path.name for path in plugin_roots()},
            {
                "jy-env-core",
                "jy-env-ios",
            },
        )

        for plugin_root in plugin_roots():
            with self.subTest(plugin=plugin_root.name):
                plugin_json = json.loads(
                    (plugin_root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
                )
                self.assertEqual(plugin_json["name"], plugin_root.name)
                self.assertEqual(plugin_json["repository"], repository)
                self.assertEqual(plugin_json["homepage"], repository)
                self.assertEqual(plugin_json["interface"]["websiteURL"], repository)
                self.assertEqual(plugin_json["interface"]["developerName"], "JaeYoung Hwang")
                self.assertEqual(plugin_json["author"]["url"], "https://github.com/jy1655")
                self.assertNotIn("email", plugin_json["author"])
                if plugin_root.name == "jy-env-ios":
                    self.assertEqual(plugin_json["mcpServers"], "./.mcp.json")
                    self.assertTrue((plugin_root / ".mcp.json").is_file())
                else:
                    self.assertNotIn("mcpServers", plugin_json)
                    self.assertFalse((plugin_root / ".mcp.json").exists())

    def test_every_skill_directory_is_discoverable_and_unique(self) -> None:
        names: list[str] = []
        for skill_path in skill_paths():
            with self.subTest(skill=skill_path.parent.name):
                names.append(skill_path.parent.name)
                self.assertTrue((skill_path.parent / "agents" / "openai.yaml").is_file())

        self.assertEqual(len(names), 11)
        self.assertEqual(len(names), len(set(names)))

    def test_writing_skills_keeps_its_reference_assets(self) -> None:
        skill_root = REPO_ROOT / "archive" / "plugins" / "jy-env-delivery" / "skills" / "jy-writing-skills"

        self.assertTrue((skill_root / "SKILL.md").exists())
        self.assertTrue((skill_root / "references" / "skill-testing-guide.md").exists())
        self.assertTrue((skill_root / "references" / "graphviz-conventions.dot").exists())
        self.assertTrue((skill_root / "agents" / "openai.yaml").exists())

    def test_retired_and_provider_named_skills_are_absent(self) -> None:
        skill_names = {path.parent.name for path in skill_paths()}
        scenario_root = REPO_ROOT / "skill-tests" / "first-party"

        for skill_name in ["jy-intent-gate", "jy-loop", "jy-context7"]:
            with self.subTest(skill=skill_name):
                self.assertNotIn(skill_name, skill_names)
                self.assertFalse((scenario_root / skill_name).exists())

    def test_readmes_document_pack_installation_in_both_languages(self) -> None:
        english = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        korean = (REPO_ROOT / "README.ko.md").read_text(encoding="utf-8")

        self.assertIn("./README.ko.md", english)
        self.assertIn("./README.md", korean)
        for text in [english, korean]:
            self.assertIn("core-lite", text)
            self.assertIn("jy-env-planning", text)
            self.assertIn("jy-env-delivery", text)
            self.assertIn("jy-env-audit", text)
            self.assertIn("jy-env-ios", text)
            self.assertIn("Context7", text)
            self.assertIn("CONTEXT7_API_KEY", text)

    def test_repository_does_not_track_native_skill_overlay(self) -> None:
        self.assertFalse((REPO_ROOT / ".agents" / "skills").exists())

    def test_license_matches_plugin_publisher(self) -> None:
        license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", license_text)
        self.assertIn("JaeYoung Hwang", license_text)


if __name__ == "__main__":
    unittest.main()
