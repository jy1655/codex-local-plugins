from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


HOOK_ROOT = Path(__file__).resolve().parents[1] / "plugins/jy-env-core/hooks"
sys.dont_write_bytecode = True
sys.path.insert(0, str(HOOK_ROOT))
import precompact_wiki as hook
from wiki_client import HandoffError, WikiClient


def summary():
    return {"goal": "압축 전에 Wiki에 현재 맥락을 보존한다.",
            **{key: [] for key in hook.SECTIONS}}


class MemoryWiki:
    def __init__(self):
        self.files = {}
        self.writes = []
        self.corrupt = False
        self.fail_page_once = False

    def tool(self, name, args, allow_missing=False):
        if name == "wiki_read":
            path = args["target"]
            if path not in self.files:
                if allow_missing:
                    return None
                raise HandoffError("not found")
            content = self.files[path]
            return {"path": path, "content": content + ("!" if self.corrupt else ""),
                    "revision": hook.digest(content), "frontmatter": {"created": "2026-10-29"}}
        path = "raw/" + args["name"] if name == "wiki_add_raw" else args["path"]
        if name == "wiki_add_raw" and path in self.files:
            raise HandoffError("already exists")
        if name == "wiki_write_page" and self.fail_page_once:
            self.fail_page_once = False
            raise HandoffError("page failed")
        if name == "wiki_write_page" and path in self.files:
            if args.get("expected_revision") != hook.digest(self.files[path]):
                raise HandoffError("revision conflict")
        self.writes.append(name)
        self.files[path] = args["content"]
        return {"saved": True, "path": path, "revision": hook.digest(args["content"])}


class PrecompactWikiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.transcript = Path(self.temp.name) / "rollout.jsonl"
        self.event = {"hook_event_name": "PreCompact", "trigger": "auto",
                      "session_id": "session-1", "turn_id": "turn-1", "model": "test-model",
                      "cwd": self.temp.name, "transcript_path": str(self.transcript)}

    def write_rows(self, rows):
        rows = [{"type": "session_meta", "payload": {"id": "session-1"}}, *rows]
        self.transcript.write_text("".join(json.dumps(x) + "\n" for x in rows), encoding="utf-8")

    def message(self, role, text, channel=None):
        return {"type": "response_item", "payload": {"type": "message", "role": role,
                "channel": channel, "content": [{"type": "input_text" if role == "user" else "output_text", "text": text}]}}

    def test_preserves_user_corrections_excludes_hidden_reasoning_and_limits_evidence(self):
        self.write_rows([
            self.message("user", "consider clear"), self.message("user", "do not clear"),
            self.message("assistant", "hidden", "analysis"),
            self.message("assistant", "pending runtime test", "commentary"),
            {"type": "response_item", "payload": {"type": "function_call", "name": "update_plan", "arguments": "unfinished"}},
            {"type": "response_item", "payload": {"type": "function_call_output", "output": "x" * 2000}},
        ])
        data, sha = hook.transcript_snapshot(self.event)
        parsed = json.loads(data)
        self.assertEqual([x["text"] for x in parsed["conversation"]],
                         ["consider clear", "do not clear", "pending runtime test"])
        self.assertEqual(parsed["recent_plans"], ["unfinished"])
        self.assertTrue(parsed["recent_tool_excerpts"][0]["truncated"])
        self.assertEqual(len(sha), 64)

    def test_previous_compaction_does_not_reintroduce_superseded_history(self):
        self.write_rows([self.message("user", "old request"),
                         {"type": "compacted", "payload": {"message": "prior checkpoint"}},
                         self.message("user", "new correction")])
        data, _ = hook.transcript_snapshot(self.event)
        self.assertNotIn("old request", data)
        self.assertIn("prior checkpoint", data)
        self.assertIn("new correction", data)

    def test_refuses_wrong_session_incomplete_source_and_oversized_input(self):
        self.write_rows([self.message("user", "goal")])
        with self.assertRaises(HandoffError):
            hook.transcript_snapshot({**self.event, "session_id": "another-session"})
        with patch.object(hook, "MAX_INPUT_CHARS", 1), self.assertRaises(HandoffError):
            hook.transcript_snapshot(self.event)
        with self.transcript.open("ab") as stream:
            stream.write(b'{"type":')
        with self.assertRaises(HandoffError):
            hook.transcript_snapshot(self.event)

    def test_rejects_model_tool_use_and_malformed_summary(self):
        for output in [json.dumps({"type": "item.completed", "item": {"type": "command_execution"}}),
                       json.dumps({"type": "turn.failed"}), "not json"]:
            with self.subTest(output=output), patch.object(hook, "run_process", return_value=output):
                with self.assertRaises(HandoffError):
                    hook.summarize("codex", self.event, "{}")

    def test_summary_command_is_ephemeral_and_does_not_inherit_tools(self):
        result = json.dumps({"type": "item.completed", "item": {
            "type": "agent_message", "text": json.dumps(summary())}})
        with patch.object(hook, "run_process", return_value=result) as execute:
            hook.summarize("codex", self.event, "{}")
        args = execute.call_args.args[0]
        self.assertIn("--ignore-user-config", args)
        self.assertIn("--ephemeral", args)
        self.assertIn("read-only", args)
        self.assertIn("hooks", args)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", args)
        self.assertNotIn("--dangerously-bypass-hook-trust", args)

    @patch.object(hook, "scan_content")
    def test_mismatched_readback_stops_before_publishing_page(self, _):
        client = MemoryWiki()
        client.corrupt = True
        with self.assertRaises(HandoffError):
            hook.save_handoff(client, self.event, "abc", summary(),
                              "raw/2026-10-29_checkpoint.md", "pages/concepts/checkpoint.md")
        self.assertEqual(client.writes, ["wiki_add_raw"])

    @patch.object(hook, "scan_content")
    def test_partial_save_recovery_reuses_raw_and_repeated_save_is_idempotent(self, _):
        client = MemoryWiki()
        client.fail_page_once = True
        raw, page = "raw/2026-10-29_checkpoint.md", "pages/concepts/checkpoint.md"
        with self.assertRaises(HandoffError):
            hook.save_handoff(client, self.event, "abc", summary(), raw, page)
        existing = client.tool("wiki_read", {"target": raw})
        for _ in range(2):
            hook.save_handoff(client, self.event, "abc", summary(), raw, page, existing)
        self.assertEqual(client.writes, ["wiki_add_raw", "wiki_write_page"])

    @patch.object(hook, "scan_content", side_effect=HandoffError("sensitive content"))
    def test_content_rejection_performs_no_writes(self, _):
        client = MemoryWiki()
        with self.assertRaises(HandoffError):
            hook.save_handoff(client, self.event, "abc", summary(),
                              "raw/2026-10-29_checkpoint.md", "pages/concepts/checkpoint.md")
        self.assertEqual(client.writes, [])

    def test_handled_failures_return_blocking_json_without_exception_details(self):
        for error in [HandoffError("save failed"), RuntimeError("sensitive response text")]:
            stream = io.StringIO()
            with patch.object(hook, "run", side_effect=error), patch.object(sys, "stdin", io.StringIO("{}")), contextlib.redirect_stdout(stream):
                hook.main()
            result = json.loads(stream.getvalue())
            self.assertFalse(result["continue"])
            self.assertNotIn("sensitive response text", stream.getvalue())

    def test_mcp_not_found_is_distinguished_from_permission_failure(self):
        client = object.__new__(WikiClient)
        client.thread_id = "ephemeral"
        for code in ["not_found", "invalid_scope"]:
            response = {"isError": True, "content": [{"type": "text", "text": json.dumps({"code": code})}]}
            with patch.object(client, "call", return_value=response):
                if code == "not_found":
                    self.assertIsNone(client.tool("wiki_read", {"target": "missing"}, allow_missing=True))
                else:
                    with self.assertRaises(HandoffError):
                        client.tool("wiki_read", {"target": "missing"}, allow_missing=True)


if __name__ == "__main__":
    unittest.main()
