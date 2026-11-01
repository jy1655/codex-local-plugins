"""Behavioral contract tests for advisory selection and source invalidation."""
import importlib.util
import json
import os
import shlex
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CORE = Path(__file__).resolve().parents[1] / "plugins/jy-wiki-cues/hooks/wiki_cues.py"
spec = importlib.util.spec_from_file_location("wiki_cues", CORE)
cue = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cue)


class WikiCuesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="wiki-cues-test-한글-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.wiki = self.base / "wiki space"
        self.home.mkdir()
        self.wiki.mkdir()
        self.source = "## Current rule\nOnly task-owned sessions; honor explicit user scope.\n"
        (self.wiki / "policy.md").write_text(self.source, encoding="utf-8")
        self.cards = [dict(id=i, status="active", action=(
            "Only close task-owned sessions unless the user names another. No extra approval for owned sessions."
            if i == "task-session-ownership" else
            "Use the installed task-workspace helper for verification. Honor an explicitly user-selected output path; preserve evidence with Wiki readback before cleanup."),
            source=dict(path="policy.md", heading="## Current rule", sha256=cue.digest(self.source)))
            for i in sorted(cue.IDS)]
        self.write_page()
        (self.home / "config.json").write_text(json.dumps(dict(schema_version=1, wiki_root=str(self.wiki))), encoding="utf-8")

    def write_page(self):
        path = self.wiki / cue.PAGE
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(cue.START + "\n```json\n" + json.dumps(dict(schema_version=1, cues=self.cards)) + "\n```\n" + cue.END, encoding="utf-8")

    def event(self, prompt="세션 정리하고 검증해줘", **kw):
        return dict(hook_event_name="UserPromptSubmit", session_id="one", cwd=str(self.wiki), prompt=prompt, **kw)

    def run_event(self, event, host="codex", now=1000):
        return cue.handle(event, host, self.home, now)

    def context(self, result):
        return result.get("hookSpecificOutput", {}).get("additionalContext", "")

    def test_relevant_delivery_and_controls(self):
        text = self.context(self.run_event(self.event()))
        self.assertIn("[task-session-ownership]", text)
        self.assertIn("[verification-artifacts]", text)
        self.assertIn("Current user instructions", text)
        self.assertIn("freshness is unverified", text)
        self.assertLess(len(text), 3500)
        text = self.context(self.run_event(self.event("내가 지정한 output/result에 검증 결과를 저장해")))
        self.assertIn("explicitly user-selected", text)
        text = self.context(self.run_event(self.event("Close only this task's sessions")))
        self.assertIn("No extra approval", text)
        self.assertEqual(self.run_event(self.event("서울과 부산의 이름을 알려줘")), {})

    def test_turn_retries_new_turns_and_task_changes(self):
        event = self.event(turn_id="1")
        first = self.run_event(event)
        self.assertEqual(first, self.run_event(event))  # retry cannot hide lost output
        self.assertEqual(first, self.run_event(self.event(turn_id="2")))
        self.assertIn("[task-session-ownership]", self.context(self.run_event(self.event("계속"))))
        self.run_event(self.event("What is a triangle?"))
        self.assertEqual(self.run_event(self.event("계속")), {})

    def test_scoped_state_lifecycle_and_expiry(self):
        self.run_event(self.event())
        for key, value in (("session_id", "two"),):
            event = self.event("continue")
            event[key] = value
            self.assertEqual(self.run_event(event), {})
        self.assertEqual(self.run_event(self.event("continue"), host="claude"), {})
        for source in ("resume", "compact"):
            event = self.event()
            event.update(hook_event_name="SessionStart", source=source)
            self.assertIn("[task-session-ownership]", self.context(self.run_event(event)))
        self.assertEqual(self.run_event(self.event("continue"), now=1000 + cue.TTL), {})
        self.run_event(self.event())
        event.update(source="startup")
        self.assertEqual(self.run_event(event), {})
        self.assertEqual(self.run_event(self.event("continue")), {})

    def test_current_sources_rechecked_after_delivery_and_resume(self):
        self.run_event(self.event())
        (self.wiki / "policy.md").write_text("## Current rule\nChanged.\n", encoding="utf-8")
        result = self.context(self.run_event(self.event("continue")))
        self.assertIn("UNAVAILABLE", result)
        self.assertNotIn("Only close", result)
        (self.wiki / "policy.md").unlink()
        event = self.event()
        event.update(hook_event_name="SessionStart", source="resume")
        self.assertIn("UNAVAILABLE", self.context(self.run_event(event)))

    def test_resume_after_normal_session_end_restores_only_relevant_cues(self):
        event = self.event("검증해줘")
        self.run_event(event)
        event["hook_event_name"] = "SessionEnd"
        self.run_event(event)
        event.update(hook_event_name="SessionStart", source="resume")
        text = self.context(self.run_event(event))
        self.assertIn("[verification-artifacts]", text)
        self.assertNotIn("[task-session-ownership]", text)

    def test_same_session_continuation_survives_directory_change(self):
        self.run_event(self.event("검증해줘"))
        event = self.event("continue")
        event["cwd"] = str(self.wiki / "subdirectory")
        self.assertIn("[verification-artifacts]", self.context(self.run_event(event)))

    def test_superseded_and_deleted_cards(self):
        self.cards[0]["status"] = "superseded"
        self.cards.pop()
        self.write_page()
        text = self.context(self.run_event(self.event()))
        self.assertIn("UNAVAILABLE", text)
        self.assertNotIn("Only close", text)

    def test_corrupt_or_missing_data_is_visible_and_fail_open(self):
        for content in ("[]", "{}", "malformed"):
            (self.home / "config.json").write_text(content, encoding="utf-8")
            result = self.run_event(self.event())
            self.assertIn("UNAVAILABLE", self.context(result))
            self.assertNotIn("decision", result)
        self.assertEqual(self.run_event(self.event("hello")), {})

    def test_no_prompt_content_or_cwd_saved_and_host_isolated(self):
        event = self.event("검증해 SECRET_SENTINEL")
        self.run_event(event)
        state = cue.state_file(self.home, "codex", event)
        content = state.read_text(encoding="utf-8")
        self.assertNotIn("SECRET_SENTINEL", content)
        self.assertNotIn(str(self.wiki), content)
        self.run_event(event, host="claude")
        event["hook_event_name"] = "SessionEnd"
        self.run_event(event)
        self.assertTrue(state.exists())  # retained for native resume, without prompt data
        self.assertTrue(cue.state_file(self.home, "claude", event).exists())
        self.run_event(event, now=1000 + cue.TTL)
        self.assertFalse(state.exists())

    def test_paths_ids_and_markdown_are_not_executed(self):
        self.cards[0]["source"]["path"] = "../outside.md"
        self.write_page()
        self.assertIn("UNAVAILABLE", self.context(self.run_event(self.event())))
        event = self.event()
        event["session_id"] = "../../escape"
        self.assertTrue(cue.state_file(self.home, "codex", event).is_relative_to(self.home))
        with self.assertRaises(ValueError):
            cue.section(self.source * 2, "## Current rule")
        self.assertEqual(cue.section(self.source + "## Other\nExtra\n", "## Current rule"), self.source)

    def test_cli_utf8_and_invalid_input(self):
        env = dict(os.environ, JY_WIKI_CUES_HOME=str(self.home))
        for payload, expected in ((json.dumps(self.event(), ensure_ascii=False), "additionalContext"), ("[]", "UNAVAILABLE")):
            proc = subprocess.run([sys.executable, "-X", "utf8", str(CORE), "--host", "claude"],
                                  input=payload, capture_output=True, text=True, encoding="utf-8", env=env)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn(expected, proc.stdout)
            json.loads(proc.stdout)

    def test_windows_hook_cannot_import_code_from_workspace_or_pythonpath(self):
        poison = self.base / "untrusted workspace"
        poison.mkdir()
        marker = poison / "executed.txt"
        (poison / "tempfile.py").write_text(
            "from pathlib import Path\nPath('executed.txt').write_text('executed', encoding='utf-8')\nraise RuntimeError('workspace import')\n", encoding="utf-8")
        hooks = json.loads((CORE.parent / "hooks.json").read_text(encoding="utf-8"))
        command = hooks["hooks"]["UserPromptSubmit"][0]["hooks"][0]["commandWindows"]
        args = shlex.split(command)[2:]  # replace Windows py -3 with this test interpreter
        env = dict(os.environ, PLUGIN_ROOT=str(CORE.parent.parent), PYTHONPATH=str(poison), JY_WIKI_CUES_HOME=str(self.home))
        proc = subprocess.run([sys.executable, *args], cwd=poison, env=env,
                              input=json.dumps(self.event()), capture_output=True, text=True, encoding="utf-8")
        self.assertFalse(marker.exists(), "hook executed a Python module from the project directory")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("additionalContext", proc.stdout)


if __name__ == "__main__":
    unittest.main()
