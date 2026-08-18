---
name: agent-bridge-delegation
description: Use when the user explicitly asks to delegate work to a visible Codex, Claude, Agy, or Pi CLI session through the locally installed Agent Bridge, or to continue and close a session created for that delegation.
---

# Agent Bridge Delegation

## Overview

Use the installed Agent Bridge as a thin delegation transport. Keep provider decisions in the
provider CLI, use JSON output for correlation, and manage only the session created for the current
request.

## Preconditions

1. Resolve `agent-bridge` from `PATH`, retain its absolute path, and run that path with `--version`.
   On this Mac the expected path is `/Users/jy/.cargo/bin/agent-bridge`. The current installed
   contract is `agent-bridge 0.0.1`; if it differs, read that binary's `--help` and do not assume
   this procedure is current.
2. Confirm the requested provider CLI is installed and already authenticated.
3. Resolve `--workspace` to an absolute path.
4. Put the prompt in a private UTF-8 file and use `--prompt-file`; do not place substantial or
   sensitive prompts in argv.

## Delegation Workflow

Start one visible session and request JSON output:

```sh
/absolute/path/to/agent-bridge ask <codex|claude|agy|pi> \
  --workspace /absolute/workspace \
  --title "short purpose" \
  --prompt-file /absolute/private/prompt.txt \
  --terminal terminal \
  --json
```

On this Mac, `--terminal terminal` is the installed v0.0.1 live-verified path. Use another explicit
terminal only when the user requests it or that adapter is part of the task. Omit `--model` and
`--effort` to preserve provider defaults; pass them only when the user or task policy specifies
them. Known model aliases are Claude `Fable5`, Pi `Fable`, and Codex
`gpt-daybreak-blue-latest`.

Read the returned `session` value and send at most one follow-up turn at a time:

```sh
/absolute/path/to/agent-bridge tell session-XXXXXXXX \
  --prompt-file /absolute/private/follow-up.txt \
  --json
```

When the delegated work is complete, close only that session:

```sh
/absolute/path/to/agent-bridge close-session session-XXXXXXXX --explicit --json
```

Remove temporary prompt files after the command no longer needs them. Report the provider result,
session ID, and whether explicit close succeeded.

## Safety Boundaries

- Never add `--yolo` unless the user explicitly authorizes it for this new session.
- Do not resend after a timeout or uncertain delivery. Inspect the same absolute binary with
  `sessions --json` and report uncertainty instead.
- Do not close, reuse, or prune sessions that this invocation did not create. Run
  `prune-sessions` only on an explicit user request.
- Do not type into terminal surfaces directly or add a generic fallback around Agent Bridge.
- Native Windows uses `--terminal windows-console` and PowerShell 7. Version 0.0.1 passed CI and
  cross-build checks, but its current native Windows live path is not verified; label it
  `NOT-VERIFIED` until a live authenticated run passes.

Do not use this skill for ordinary single-agent work when the user did not ask for delegation or a
specific provider session.
