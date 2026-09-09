---
name: ios-debugger-agent
description: Use when building, launching, inspecting, automating, or debugging an iOS app on Simulator with the pinned XcodeBuildMCP server.
---

# iOS Debugger Agent

Use the `xcodebuildmcp` MCP server for simulator builds, launches, runtime logs, UI
inspection, interaction, and LLDB debugging.

## Build and Launch

Use these operations when the request needs a build or launch. For logs, an existing
screen, or a narrow debugger query, use that capability directly without rebuilding.

1. Call `mcp__xcodebuildmcp__session_show_defaults` before the first build, run, or
   test request.
2. If the project or workspace, scheme, or simulator is missing or wrong:
   - Call `mcp__xcodebuildmcp__list_sims`.
   - Prefer a booted matching simulator. Otherwise choose a canonical simulator name;
     `build_run_sim` can boot it when needed.
   - Call `mcp__xcodebuildmcp__session_set_defaults` with `projectPath` or
     `workspacePath`, `scheme`, and preferably `simulatorName`. Use `simulatorId` only
     for a machine-local selection. Set `configuration: "Debug"` and `useLatestOS:
     true` when those match the task.
3. After changing defaults, call `mcp__xcodebuildmcp__session_show_defaults` to verify
   the resolved values. Reuse unchanged defaults already verified in this session.
4. Call `mcp__xcodebuildmcp__build_run_sim`. Do not call separate boot or open tools
   as prerequisites.
5. Verify the launched UI with `mcp__xcodebuildmcp__snapshot_ui` or
   `mcp__xcodebuildmcp__screenshot`.

If the app is already installed and only a launch is needed, set `bundleId` through
`session_set_defaults` and call `mcp__xcodebuildmcp__launch_app_sim`. If the bundle ID
is unknown, call `mcp__xcodebuildmcp__get_sim_app_path` with `platform: "iOS
Simulator"`, then pass its app path to `mcp__xcodebuildmcp__get_app_bundle_id`.

## UI Interaction

- Call `snapshot_ui` before every interaction sequence.
- Use the returned `elementRef` with `tap` and with `type_text`.
- Pass both `elementRef` and `text` to `type_text`; use `replaceExisting: true` when
  replacing a field value.
- Use `gesture` with a documented preset for scrolling or edge swipes.
- Refresh `snapshot_ui` after an action before relying on changed screen state.
- Use `screenshot` when visual evidence matters.

## Runtime Logs

`build_run_sim` and `launch_app_sim` capture runtime logs automatically. Read the
runtime log path returned in the tool result and summarize only the lines relevant to
the reported behavior. Relaunch the app when a clean log boundary is required.

## Debugging

- Set `preferXcodebuild: true` through `session_set_defaults` only when incremental
  build behavior is suspected or the user requests standard `xcodebuild`.
- Attach LLDB with `debug_attach_sim` only after the app is running.
- Use breakpoints, stack inspection, variable inspection, and raw LLDB commands in the
  narrowest sequence needed for the diagnosis.
- Detach the debugger when the investigation is complete.

## Failure Handling

- On build failure, report the structured diagnostics before changing code or retrying.
- If the wrong app launches, re-check the active defaults, scheme, and bundle ID.
- If an `elementRef` becomes stale, capture a fresh `snapshot_ui` and use the new ref.
- If the MCP tools are absent, report which requested operation cannot be performed
  and continue any independent source analysis. Installing the optional jy-env-ios pack
  and starting a fresh Codex session makes its tools available.
