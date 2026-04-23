from __future__ import annotations

from pathlib import Path
import json
import subprocess
import sys
import unittest


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "plugins"
    / "jy-env-core"
    / "hooks"
    / "necessity_gate.py"
)


def run_hook(payload: dict, mode: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), mode],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


class NecessityGateHookTests(unittest.TestCase):
    def test_user_prompt_submit_injects_necessity_policy_context(self) -> None:
        output = run_hook(
            {
                "hook_event_name": "UserPromptSubmit",
                "prompt": "이 작업 끝나고 추가 개선도 정리해줘",
                "cwd": "/tmp/repo",
                "session_id": "session",
                "turn_id": "turn",
                "transcript_path": None,
                "model": "gpt-5.4",
                "permission_mode": "default",
            },
            "user-prompt-submit",
        )

        context = output["hookSpecificOutput"]["additionalContext"]
        self.assertTrue(output["continue"])
        self.assertEqual(output["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit")
        self.assertIn("necessity gate", context)
        self.assertIn("user-directed", context)
        self.assertIn("evidenced", context)

    def test_stop_hook_blocks_unjustified_followup_sections(self) -> None:
        output = run_hook(
            {
                "hook_event_name": "Stop",
                "last_assistant_message": "완료했습니다.\n\n후속 작업\n- 다른 파일도 정리하면 좋습니다.",
                "cwd": "/tmp/repo",
                "session_id": "session",
                "turn_id": "turn",
                "transcript_path": None,
                "model": "gpt-5.4",
                "permission_mode": "default",
                "stop_hook_active": False,
            },
            "stop",
        )

        self.assertEqual(output["decision"], "block")
        self.assertIn("Remove unsupported speculative follow-up", output["reason"])

    def test_stop_hook_allows_followup_when_necessity_gate_is_recorded(self) -> None:
        output = run_hook(
            {
                "hook_event_name": "Stop",
                "last_assistant_message": (
                    "[necessity-gate] 사용자 요청 후속 정리\n"
                    "- classification: user-directed\n"
                    "- decision: APPROVE\n\n"
                    "Next steps\n- 사용자가 요청한 배포 절차 진행"
                ),
                "cwd": "/tmp/repo",
                "session_id": "session",
                "turn_id": "turn",
                "transcript_path": None,
                "model": "gpt-5.4",
                "permission_mode": "default",
                "stop_hook_active": False,
            },
            "stop",
        )

        self.assertTrue(output["continue"])
        self.assertNotIn("decision", output)


if __name__ == "__main__":
    unittest.main()
