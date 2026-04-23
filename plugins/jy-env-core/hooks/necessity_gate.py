#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from typing import Any


FOLLOWUP_HEADING_RE = re.compile(
    r"(?im)^\s*(?:#{1,6}\s*)?(?:\*\*)?"
    r"(후속\s*작업|다음\s*단계|추가\s*(?:작업|개선|검토)|남은\s*작업|"
    r"TODO|Open Questions?|Open Issues?|Next Steps?|Follow[- ]?ups?)"
    r"(?:\*\*)?\s*:?\s*$"
)


POLICY_CONTEXT = """necessity gate policy:
Before defining any new task, new skill, new file, new audit cycle, TODO/open issue/follow-up item, or speculative cleanup that the user did not explicitly request, classify it as one of:
- user-directed: directly requested by the user
- reproducible: needed because a failing command, test, or bug reproduction proves it
- evidenced: needed because inspected repo evidence shows a concrete mismatch or broken dependency

Reject speculative padding such as "nice to have", broad cleanup, manufactured follow-up sections, and extra audit loops. If you keep a follow-up/TODO/open issue section in the final answer, include a concise [necessity-gate] block explaining the basis and decision."""


def _read_payload() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    data = json.loads(raw)
    if not isinstance(data, dict):
        return {}
    return data


def _emit(payload: dict[str, Any]) -> int:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return 0


def _continue() -> dict[str, Any]:
    return {"continue": True}


def user_prompt_submit() -> dict[str, Any]:
    return {
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": POLICY_CONTEXT,
        },
    }


def stop(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("stop_hook_active"):
        return _continue()

    message = payload.get("last_assistant_message")
    if not isinstance(message, str) or not message.strip():
        return _continue()

    if "[necessity-gate]" in message:
        return _continue()

    if FOLLOWUP_HEADING_RE.search(message):
        return {
            "decision": "block",
            "reason": (
                "Remove unsupported speculative follow-up/TODO/open issue sections, "
                "or add a concise [necessity-gate] block that classifies the item as "
                "user-directed, reproducible, or evidenced and explains why it should stay."
            ),
        }

    return _continue()


def main(argv: list[str]) -> int:
    try:
        payload = _read_payload()
        mode = argv[1] if len(argv) > 1 else payload.get("hook_event_name", "")
        normalized_mode = str(mode).replace("_", "-").lower()

        if normalized_mode in {"user-prompt-submit", "userpromptsubmit"}:
            return _emit(user_prompt_submit())
        if normalized_mode == "stop":
            return _emit(stop(payload))
        return _emit(_continue())
    except Exception as exc:  # pragma: no cover - fail open for live Codex sessions
        return _emit(
            {
                "continue": True,
                "systemMessage": f"necessity gate hook failed open: {exc}",
            }
        )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
