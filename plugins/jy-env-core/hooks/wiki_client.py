"""Use Codex's existing MCP authentication without reading or copying credentials."""
from __future__ import annotations

import json
import os
from pathlib import Path
import queue
import signal
import subprocess
import threading
import time


class HandoffError(Exception):
    """A safe, user-visible failure (never include transcripts or credentials)."""


class WikiClient:
    def __init__(self, codex: str, cwd: str, timeout: float = 60):
        self.deadline = time.monotonic() + timeout
        self.messages = queue.Queue()
        self.sequence = 0
        self.thread_id = None
        self.process = subprocess.Popen(
            [codex, "app-server", "--stdio", "--disable", "hooks"],
            cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True, encoding="utf-8",
            start_new_session=(os.name != "nt"),
        )
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        try:
            for line in self.process.stdout:
                try:
                    self.messages.put(json.loads(line))
                except ValueError:
                    self.messages.put(None)
                    return
        finally:
            self.messages.put(None)

    def _send(self, message):
        try:
            self.process.stdin.write(json.dumps(message, ensure_ascii=False) + "\n")
            self.process.stdin.flush()
        except (OSError, BrokenPipeError):
            raise HandoffError("Codex MCP 연결이 종료되었습니다.") from None

    def call(self, method, params):
        self.sequence += 1
        request_id = self.sequence
        self._send({"id": request_id, "method": method, "params": params})
        while True:
            remaining = self.deadline - time.monotonic()
            if remaining <= 0:
                raise HandoffError("Wiki MCP 작업 제한 시간을 초과했습니다.")
            try:
                message = self.messages.get(timeout=remaining)
            except queue.Empty:
                raise HandoffError("Wiki MCP 응답 제한 시간을 초과했습니다.") from None
            if message is None:
                raise HandoffError("Codex MCP 응답을 읽지 못했습니다.")
            if "method" in message and "id" in message:
                # An unattended hook must not approve a new capability or OAuth flow.
                self._send({"id": message["id"], "error": {
                    "code": -32601, "message": "Interactive requests are unavailable in this hook."
                }})
            elif message.get("id") == request_id:
                if "error" in message:
                    raise HandoffError("Codex MCP 요청 실패: " + method)
                return message.get("result", {})

    def connect(self):
        self.call("initialize", {
            "clientInfo": {"name": "wiki_handoff", "version": "1.0.0"},
            "capabilities": {"experimentalApi": True, "explicitGatewayOauth": True},
        })
        self._send({"method": "initialized", "params": {}})
        result = self.call("thread/start", {
            "cwd": str(Path(__file__).resolve().parent),
            "ephemeral": True, "sandbox": "read-only", "approvalPolicy": "never",
            "config": {"features.hooks": False},
        })
        self.thread_id = result["thread"]["id"]
        # No turn/start: this thread only owns the authenticated MCP connection.
        self.call("mcpServerStatus/list", {
            "threadId": self.thread_id, "serverName": "wiki",
        })

    def tool(self, name, arguments, allow_missing=False):
        if name not in {"wiki_read", "wiki_add_raw", "wiki_write_page"}:
            raise HandoffError("허용하지 않은 Wiki 도구입니다.")
        result = self.call("mcpServer/tool/call", {
            "threadId": self.thread_id, "server": "wiki", "tool": name,
            "arguments": arguments,
        })
        value = result.get("structuredContent")
        if not isinstance(value, dict):
            try:
                value = json.loads(next(x["text"] for x in result.get("content", [])
                                        if x.get("type") == "text"))
            except (StopIteration, KeyError, ValueError):
                raise HandoffError("Wiki 도구 응답 형식이 예상과 다릅니다.") from None
        if result.get("isError"):
            error = value.get("error", {})
            code = (error.get("code") if isinstance(error, dict) else None) or value.get("code")
            if allow_missing and code == "not_found":
                return None
            raise HandoffError("Wiki 도구가 요청을 거부했습니다: " + name)
        return value

    def close(self):
        if self.process.poll() is None:
            if os.name != "nt":
                os.killpg(self.process.pid, signal.SIGTERM)
            else:
                self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                if os.name != "nt":
                    os.killpg(self.process.pid, signal.SIGKILL)
                else:
                    self.process.kill()
                self.process.wait(timeout=5)
        for stream in (self.process.stdin, self.process.stdout):
            if stream:
                stream.close()

    def __enter__(self):
        try:
            self.connect()
            return self
        except BaseException:
            self.close()
            raise

    def __exit__(self, *_):
        self.close()
