from __future__ import annotations

from pathlib import Path
import json
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_PACKS = {
    "jy-env-core": {
        "jy-change-guardrails",
        "jy-debugging",
        "jy-test-driven",
        "jy-verification-before-completion",
        "jy-codebase-explore",
        "jy-library-research",
        "jy-consult",
    },
    "jy-env-planning": {
        "jy-framing",
        "jy-grill-me",
        "jy-plan-review",
        "jy-writing-plans",
    },
    "jy-env-delivery": {
        "jy-executing-plans",
        "jy-worktrees",
        "jy-checkpoint",
        "jy-document-release",
        "jy-ship",
        "jy-waterfall",
        "jy-env-sync-admin",
        "jy-writing-skills",
    },
    "jy-env-audit": {
        "jy-explain-change",
        "jy-review-all",
        "jy-review-work",
        "jy-receiving-review",
        "jy-slop-remover",
    },
    "jy-env-ios": {
        "ios-app-intents",
        "ios-debugger-agent",
        "ios-ettrace-performance",
        "ios-memgraph-leaks",
        "ios-simulator-browser",
        "swiftui-liquid-glass",
        "swiftui-performance-audit",
        "swiftui-ui-patterns",
        "swiftui-view-refactor",
    },
}


class PackagingTests(unittest.TestCase):
    def test_first_party_skills_are_partitioned_without_duplication(self) -> None:
        actual: dict[str, set[str]] = {}
        for plugin_name in EXPECTED_PACKS:
            skill_root = REPO_ROOT / "plugins" / plugin_name / "skills"
            actual[plugin_name] = {
                path.parent.name
                for path in skill_root.glob("*/SKILL.md")
            }

        self.assertEqual(actual, EXPECTED_PACKS)
        all_skills = [skill for skills in actual.values() for skill in skills]
        self.assertEqual(len(all_skills), len(set(all_skills)))

    def test_marketplace_defaults_only_core_lite(self) -> None:
        marketplace = json.loads(
            (REPO_ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
        )
        policies = {
            entry["name"]: entry["policy"]["installation"]
            for entry in marketplace["plugins"]
        }

        self.assertEqual(
            policies,
            {
                "jy-env-core": "INSTALLED_BY_DEFAULT",
                "jy-env-planning": "AVAILABLE",
                "jy-env-delivery": "AVAILABLE",
                "jy-env-audit": "AVAILABLE",
                "jy-env-ios": "AVAILABLE",
            },
        )

    def test_each_pack_manifest_matches_its_directory(self) -> None:
        for plugin_name in EXPECTED_PACKS:
            with self.subTest(plugin=plugin_name):
                plugin_root = REPO_ROOT / "plugins" / plugin_name
                manifest = json.loads(
                    (plugin_root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
                )
                self.assertEqual(manifest["name"], plugin_name)
                self.assertEqual(manifest["skills"], "./skills/")
                if plugin_name == "jy-env-ios":
                    self.assertEqual(manifest["mcpServers"], "./.mcp.json")
                    self.assertTrue((plugin_root / ".mcp.json").is_file())
                else:
                    self.assertNotIn("mcpServers", manifest)
                    self.assertFalse((plugin_root / ".mcp.json").exists())

    def test_ios_pack_pins_current_xcodebuildmcp_contract(self) -> None:
        plugin_root = REPO_ROOT / "plugins" / "jy-env-ios"
        mcp = json.loads((plugin_root / ".mcp.json").read_text(encoding="utf-8"))
        server = mcp["mcpServers"]["xcodebuildmcp"]

        self.assertEqual(server["command"], "npx")
        self.assertEqual(server["args"], ["-y", "xcodebuildmcp@2.7.0", "mcp"])
        self.assertEqual(
            server["env"]["XCODEBUILDMCP_ENABLED_WORKFLOWS"],
            "simulator,ui-automation,debugging",
        )
        self.assertNotIn("@latest", json.dumps(server))
        self.assertNotIn(
            "logging",
            server["env"]["XCODEBUILDMCP_ENABLED_WORKFLOWS"].split(","),
        )

        skill_text = (
            plugin_root / "skills" / "ios-debugger-agent" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for current_name in [
            "session_show_defaults",
            "session_set_defaults",
            "snapshot_ui",
            "build_run_sim",
            "launch_app_sim",
        ]:
            self.assertIn(current_name, skill_text)
        for retired_name in [
            "session-set-defaults",
            "describe_ui",
            "start_sim_log_cap",
            "stop_sim_log_cap",
        ]:
            self.assertNotIn(retired_name, skill_text)
        self.assertIn("elementRef", skill_text)
        self.assertIn("runtime log", skill_text.lower())

    def test_library_research_uses_lazy_pinned_context7_cli(self) -> None:
        skill_path = (
            REPO_ROOT
            / "plugins"
            / "jy-env-core"
            / "skills"
            / "jy-library-research"
            / "SKILL.md"
        )
        text = skill_path.read_text(encoding="utf-8")

        self.assertRegex(text, r"npx --yes ctx7@\d+\.\d+\.\d+")
        self.assertIn("CTX7_TELEMETRY_DISABLED", text)
        self.assertIn("CONTEXT7_API_KEY", text)
        self.assertIn("ctx7 library", text)
        self.assertIn("ctx7 docs", text)
        self.assertNotIn("ctx7 setup", text)
        self.assertNotIn("ctx7 login", text)
        self.assertNotIn("--api-key", text)
        self.assertFalse(
            any(
                path.name == "jy-context7"
                for path in (REPO_ROOT / "plugins").glob("*/skills/*")
            )
        )

    def test_global_instructions_do_not_eagerly_route_optional_pack_skills(self) -> None:
        text = (REPO_ROOT / "instructions" / "AGENTS.md").read_text(encoding="utf-8")

        self.assertNotIn("## Skill Routing", text)
        self.assertNotIn("## Execution Skill Routing", text)
        self.assertNotIn("## Advisory and Research Skill Routing", text)
        self.assertIsNone(re.search(r"`jy-(autoplan|ship|review-all)`", text))


if __name__ == "__main__":
    unittest.main()
