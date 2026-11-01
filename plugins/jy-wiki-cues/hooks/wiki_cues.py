"""Wiki-backed advisory context. Canonical shared core; package, do not fork it.

No subprocesses, network, model calls, or executable Wiki expressions. State holds
only scoped cue IDs and revisions, never prompts or transcripts. Output means
emitted, not read or followed by a model.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time

VERSION = "0.1.2"
PAGE = "pages/concepts/agent-action-cues.md"
IDS = {"task-session-ownership", "verification-artifacts"}
MAX_FILE = 256_000
TTL = 12 * 60 * 60
START = "<!-- jy-wiki-cues:start -->"
END = "<!-- jy-wiki-cues:end -->"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_text(path: Path) -> str:
    with path.open("rb") as stream:
        data = stream.read(MAX_FILE + 1)
    if len(data) > MAX_FILE:
        raise ValueError("oversized-file")
    return data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def section(text: str, heading: str) -> str:
    """Hash exact heading and body up to the next same/higher Markdown heading."""
    lines = text.splitlines(keepends=True)
    hits = [i for i, line in enumerate(lines) if line.rstrip("\n") == heading]
    if len(hits) != 1 or not re.fullmatch(r"#{1,6} .+", heading):
        raise ValueError("ambiguous-source-section")
    start = hits[0]
    level = len(heading.split(" ", 1)[0])
    end = next((i for i in range(start + 1, len(lines))
                if re.match(r"^#{1," + str(level) + r"} ", lines[i])), len(lines))
    return "".join(lines[start:end]).rstrip() + "\n"


def within(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    if Path(relative).is_absolute() or not candidate.is_relative_to(root.resolve()):
        raise ValueError("source-outside-wiki")
    return candidate


def load_cards(root: Path) -> tuple[dict, str]:
    text = read_text(within(root, PAGE))
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError("missing-cue-block")
    block = text.split(START)[1].split(END)[0].strip()
    if not block.startswith("```json\n") or not block.endswith("\n```"):
        raise ValueError("invalid-cue-block")
    data = json.loads(block[8:-4])
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("cues"), list):
        raise ValueError("unsupported-cue-schema")
    if len(data["cues"]) > 20:
        raise ValueError("too-many-cues")
    cards = {}
    for item in data["cues"]:
        if not isinstance(item, dict) or item.get("id") not in IDS:
            raise ValueError("unknown-cue")
        ident = item["id"]
        if ident in cards:
            raise ValueError("duplicate-cue")
        if item.get("status") not in {"active", "superseded"}:
            raise ValueError("invalid-status")
        if not isinstance(item.get("action"), str) or not 1 <= len(item["action"]) <= 950:
            raise ValueError("invalid-action")
        src = item.get("source", {})
        if not isinstance(src, dict) or not all(isinstance(src.get(k), str)
                for k in ("path", "heading", "sha256")):
            raise ValueError("invalid-source")
        if not re.fullmatch(r"[0-9a-f]{64}", src["sha256"]):
            raise ValueError("invalid-source-hash")
        # Validate path even for a superseded cue, without reading the source yet.
        within(root, src["path"])
        cards[ident] = item
    return cards, digest(text)


def selected_ids(prompt: str, previous: list[str]) -> list[str]:
    text = prompt.casefold().strip()
    # Inherit only explicit short continuations; a new substantive task replaces scope.
    if re.fullmatch(r"(?:계속|계속해|계속해줘|계속 진행|진행해|진행해줘|이어서|마무리해|continue|go ahead|resume|finish)(?:[.! ]*)", text):
        return sorted(set(previous) & IDS)
    selected = []
    session = re.search(r"세션|터미널|\bsessions?\b|\bterminals?\b", text)
    cleanup = re.search(r"정리|종료|닫|\b(?:clean\w*|clos\w*|terminat\w*|prun\w*|stop)\b", text)
    delegation = re.search(r"위임|agent bridge|\btabcli\b|sub.?agents?|에이전트.*(?:같이|병렬)|claude.*(?:같이|검토)", text)
    if (session and cleanup) or delegation:
        selected.append("task-session-ownership")
    if re.search(r"검증|테스트|증거|산출물|구현|고쳐|수정|\b(?:verif\w*|tests?|testing|evidence|artifacts?|implement\w*|fix\w*)\b", text):
        selected.append("verification-artifacts")
    return sorted(selected)


def state_file(home: Path, host: str, event: dict) -> Path | None:
    session = event.get("session_id")
    if not isinstance(session, str) or not session:
        return None
    # These cues are task-global, so a shell cd must not lose continuation scope.
    # A new substantive prompt replaces scope. Hashing prevents path injection.
    return home / "state" / host / (digest(session) + ".json")


def get_state(path: Path | None, now: float) -> dict:
    try:
        state = json.loads(read_text(path)) if path else {}
        if not isinstance(state, dict):
            return {}
        if not 0 <= now - state.get("at", 0) < TTL:
            return {}
        if not isinstance(state.get("ids"), list) or any(i not in IDS for i in state["ids"]):
            return {}
        return state
    except (OSError, ValueError, TypeError):
        return {}


def save_state(path: Path | None, state: dict) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    name = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                dir=path.parent, prefix=".cue-", suffix=".tmp", delete=False) as stream:
            name = stream.name
            json.dump(state, stream, ensure_ascii=False)
            stream.write("\n")
        os.replace(name, path)
    finally:
        if name and Path(name).exists():
            Path(name).unlink()


def output(event_name: str, message: str) -> dict:
    if not message:
        return {}
    return {"hookSpecificOutput": {"hookEventName": event_name, "additionalContext": message}}


def handle(event: dict, host: str, home: Path, now: float | None = None) -> dict:
    now = time.time() if now is None else now
    name = event.get("hook_event_name")
    if name not in {"UserPromptSubmit", "SessionStart", "SessionEnd"}:
        return {}
    path = state_file(home, host, event)
    old = get_state(path, now)
    if name == "SessionEnd":
        # Native resume can follow a normal close. Retain only IDs/revisions until
        # their original TTL expires; closing must not extend the task lifetime.
        if path and not old:
            path.unlink(missing_ok=True)
        return {}
    if name == "SessionStart" and event.get("source") not in {"resume", "compact"}:
        if path:
            path.unlink(missing_ok=True)
        return {}
    if name == "UserPromptSubmit":
        prompt = event.get("prompt")
        if not isinstance(prompt, str):
            raise ValueError("missing-prompt")
        ids = selected_ids(prompt, old.get("ids", []))
    else:
        ids = old.get("ids", [])
    state = {"at": now, "ids": ids, "delivery": "irrelevant", "revisions": {}}
    if not ids:
        save_state(path, state)
        return {}
    try:
        config = json.loads(read_text(home / "config.json"))
        if not isinstance(config, dict) or config.get("schema_version") != 1 or not isinstance(config.get("wiki_root"), str):
            raise ValueError("invalid-config")
        root = Path(config["wiki_root"])
        if not root.is_absolute():
            raise ValueError("wiki-root-not-absolute")
        cards, revision = load_cards(root)
        messages = []
        unavailable = []
        for ident in ids:
            card = cards.get(ident)
            if not card or card["status"] != "active":
                unavailable.append(ident)
                continue
            src = card["source"]
            try:
                actual = digest(section(read_text(within(root, src["path"])), src["heading"]))
            except (OSError, UnicodeError, ValueError):
                actual = None
            if actual != src["sha256"]:
                unavailable.append(ident)
                continue
            messages.append(f"- [{ident}] {card['action']} Source: {src['path']} / {src['heading']} (sha256 {actual[:12]}).")
            state["revisions"][ident] = actual
        prefix = ("Wiki action cues (advisory data from a local snapshot; server freshness is unverified). "
                  "Current user instructions and explicit exceptions take precedence; these cues grant no authority. "
                  "Revalidate the current source when instructions conflict.\n")
        if unavailable:
            messages.append("UNAVAILABLE: " + ", ".join(unavailable) +
                            ". Missing, superseded, or changed source; do not reuse an earlier cue. Read the current authority when relevant.")
        state.update(delivery="emitted", page_revision=revision)
        result = output(name, prefix + "\n".join(messages))
    except (OSError, UnicodeError, ValueError, TypeError, KeyError):
        state["delivery"] = "unavailable"
        result = output(name, "Wiki action cues UNAVAILABLE: local configuration or Wiki data could not be validated. "
                        "Do not rely on a previous cue; use current user instructions and current sources. This advisory feature does not block work.")
    # Retry the same event by re-emitting validated context, never hide a lost delivery.
    # Each prompt and lifecycle restore revalidates sources, including same-turn retries.
    try:
        save_state(path, state)
    except OSError:
        result["systemMessage"] = "Wiki 교훈은 출력했지만 상태를 저장하지 못했습니다. 짧은 후속 요청·재개 시 전달은 미확인입니다."
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True, choices=("codex", "claude"))
    args = parser.parse_args()
    home = Path(os.environ.get("JY_WIKI_CUES_HOME", str(Path.home() / ".config" / "jy-wiki-cues")))
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        raw = sys.stdin.read(1_000_001)
        if len(raw) > 1_000_000:
            raise ValueError("oversized-event")
        event = json.loads(raw)
        if not isinstance(event, dict):
            raise ValueError("invalid-event")
        result = handle(event, args.host, home)
    except (OSError, UnicodeError, ValueError, TypeError, KeyError):
        # A storage/input failure must be visible and must not block the host.
        result = {"systemMessage": "Wiki 교훈 전달 UNAVAILABLE: 입력 또는 상태 저장을 확인하지 못했습니다."}
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
