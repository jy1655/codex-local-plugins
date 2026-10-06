---
name: ios-memgraph-leaks
description: Use when analyzing iOS memory leaks, retain cycles, or unexpectedly retained objects using memory graphs exported from physical devices and before-and-after ownership evidence.
---

# iOS Memgraph Leaks

Analyze a physical-device `.memgraph` with the bundled summary helper and Apple's
`leaks` tool on macOS. Start from an existing capture when it covers the reported
object lifecycle; capture again when the build, flow, or unresolved question requires it.

## Core Workflow

1. Identify the object that should be released and the action that ends its lifetime.
2. Use a capture taken after that action, recording the device, OS, app build, and flow.
3. Summarize reported leaks and inspect the relevant app-owned types and retaining paths.
4. If a fix is requested, remove the evidenced retaining edge and compare the same
   lifecycle on the same physical device with comparable build settings and data.

## Capture from a physical device

Run or attach to the app on the connected iPhone or iPad in Xcode. Reproduce the
creation and release flow, click **Debug Memory Graph**, then choose
**File > Export Memory Graph** to save a `.memgraph` on the Mac.

Enable **Malloc Stack Logging** in the scheme's Run diagnostics before reproducing
only when allocation backtraces are needed. Record changed diagnostics and restore
temporary settings after capture. Store artifacts in a task-owned or user-chosen
folder outside the skill directory.

Host `leaks <pid>` inspects a Mac process; a device PID is not a remote capture target.
Pass the exported file to the analysis tools. If device or Xcode access is unavailable,
request the missing capture or access and continue source analysis without claiming
runtime proof.

## Summarize

Summarize an existing memgraph:

```bash
SKILL_DIR="<absolute path to this loaded skill folder>"
"$SKILL_DIR/scripts/summarize_memgraph_leaks.py" \
  /path/to/app.memgraph \
  --trace-limit 5 \
  --out /path/to/leak-summary.md
```

Use `--trace-limit` sparingly. Trace trees are useful root-cause evidence, but large memgraphs can produce noisy output. If a trace tree says `Found 0 roots referencing`, treat it as an unreachable/self-retained leak candidate and use the summary's grouped leak tree or `leaks --groupByType <file.memgraph>` to identify the retained fields and payload chain.

## Root Cause Rules

- Identify the first app-owned leaked type in the leak output or trace.
- Determine the intended lifetime: process, session, account, view, request, or task.
- Zero reported leaks does not rule out reachable but unwanted retained objects.
  Inspect their references in Xcode's memory graph or use Instruments Allocations
  when the symptom is persistent growth rather than unreachable allocations.
- Treat lazy or deferred allocation as a scope reduction, not a leak fix, unless the original eager allocation itself violated the intended lifetime.
- Prove retain-cycle claims with either a `traceTree` ownership path or an isolated reproduction.
- For unreachable/self-cycle leaks, `traceTree` may have no root path; use `leaks --groupByType` plus source verification to find the self-retaining edge.
- Do not claim success from a smaller file, lower total count, or lack of crashes;
  show that the affected object lifetime or retaining path is corrected. Compare types
  and ownership paths across captures, not raw addresses.
- Separate real root-cause branches from candidate/noise branches.
- Prefer deleting the retaining edge over adding broad cleanup code.

## Report

A useful leak report includes:

- the exact flow, physical device, OS, app build, and capture diagnostics
- the memgraph and summary paths
- app-owned leaked types and counts
- at least one ownership path, or grouped leak tree evidence when the object is unreachable from roots
- the smallest proposed or applied retaining-edge fix
- before/after evidence when a fix was made

If the memgraph shows only framework/runtime noise, say that and recommend the next narrower capture rather than inventing an app leak.

## References

- [Gathering information about memory use](https://developer.apple.com/documentation/xcode/gathering-information-about-memory-use): Xcode capture, export, and allocation backtraces.
- [Analyze heap memory](https://developer.apple.com/videos/play/wwdc2024/10173/): reachability, retained objects, and memory analysis tools.
