---
name: ios-debugger-agent
description: Use when building, launching, inspecting, automating, or debugging an iOS app on Simulator with the pinned XcodeBuildMCP CLI.
---

# iOS Debugger Agent

Use XcodeBuildMCP 2.7.0 on demand through the CLI. This pack does not register an MCP
server. Keep using the repository's normal test scripts for routine unit tests.

```sh
npx -y xcodebuildmcp@2.7.0 <workflow> <tool> [flags] --output json
```

Run commands from the app's repository so they share workspace defaults and any
stateful daemon. Inspect existing `.xcodebuildmcp/config.yaml` defaults before reusing
them; pass explicit flags for missing or incorrect values without rewriting project
configuration. Use `<workflow> <tool> --help` for the exact arguments. `--json` supplies
a JSON object of arguments; `--output json` selects structured results.

## Build and Launch

Use these operations when the request needs a build or launch. For logs, an existing
screen, or a narrow debugger query, use that capability directly without rebuilding.

1. Resolve the project or workspace and scheme from repository instructions or existing
   defaults. Use `simulator list` when selecting a simulator; prefer an available,
   booted match. Pass `--simulator-id` for a machine-local selection.
2. Use `simulator build-and-run` with `--project-path` or `--workspace-path`, `--scheme`,
   and the chosen simulator. Use `--configuration Debug` when appropriate. It boots the
   simulator when needed; separate boot or open commands are not prerequisites.
3. Verify the launched UI with `ui-automation snapshot-ui` or `ui-automation screenshot`.

For an installed app, use `simulator launch-app --bundle-id <id>` with the chosen
simulator. If the bundle ID is unknown, use `simulator get-app-path --platform 'iOS
Simulator'`, then `simulator get-app-bundle-id` with the returned app path.

## UI Interaction

- Use the `ui-automation` workflow and pass `--simulator-id` when not set in defaults.
- Capture `snapshot-ui` before an interaction sequence. Use its `elementRef` as
  `--element-ref` for `tap` or `type-text`; never invent a target.
- Pass both `--element-ref` and `--text` to `type-text`; use `--replace-existing` when
  replacing a field value. Quote user text safely for the shell.
- Use `gesture` with a documented preset, or `swipe` with `--within-element-ref` for a
  scrollable target from the current snapshot.
- Refresh `snapshot-ui` after navigation, scrolling, or layout changes before relying
  on changed screen state. Use `screenshot` when visual evidence matters.

## Runtime Logs

`simulator build-and-run` and `simulator launch-app` capture runtime logs automatically. Read the
runtime log path returned in the tool result and summarize only the lines relevant to
the reported behavior. Relaunch the app when a clean log boundary is required.

## Debugging

- Pass `--prefer-xcodebuild` only when incremental build behavior is suspected or the
  user requests standard `xcodebuild`.
- Use `debugging attach` only after the app is running.
- Use breakpoints, stack inspection, variable inspection, and raw LLDB commands in the
  narrowest sequence needed for the diagnosis.
- Use `debugging detach` when the investigation is complete.

Stateful log, video, and LLDB operations can start a workspace daemon on demand; CLI
use does not mean every process exits after each command. Do not stop another task's
daemon or simulator.

## Failure Handling

- On build failure, report the structured diagnostics before changing code or retrying.
- If the wrong app launches, re-check the effective flags, defaults, scheme, and bundle ID.
- If an `elementRef` becomes stale, capture a fresh `snapshot-ui` and use the new ref.
- If the CLI fails, inspect its diagnostics and report the unperformed operation.
  Continue independent source analysis; do not enable a persistent MCP server as a
  prerequisite.
