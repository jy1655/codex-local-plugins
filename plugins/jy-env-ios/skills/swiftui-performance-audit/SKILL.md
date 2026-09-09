---
name: swiftui-performance-audit
description: Use when auditing SwiftUI runtime performance to diagnose slow rendering, janky scrolling, expensive updates, hangs, or profiling needs.
---

# SwiftUI Performance Audit

## Quick start

Use the most relevant available evidence to diagnose the requested SwiftUI performance
issue. Start from a supplied trace when present, or inspect the affected code and symptoms.

## Evidence Selection

- Focus on the reported symptom: rendering, scrolling, CPU, memory, hangs, or view updates.
- Consult `references/code-smells.md` for a relevant source question and
  `references/profiling-intake.md` when a runtime capture is needed.
- Collect evidence with available, authorized tools. Ask the user only for material context
  or device access that cannot be obtained from the current workspace or tools.
- Use `references/report-template.md` when its structure helps; a narrow finding can be
  reported directly with its evidence and limits.

## 1. Intake

Collect:
- Target view or feature code.
- Symptoms and exact reproduction steps.
- Data flow: `@State`, `@Binding`, environment dependencies, and observable models.
- Whether the issue shows up on device or simulator, and whether it was observed in Debug or Release.

Use the reported symptoms to distinguish:
- CPU spike or battery drain
- Janky scrolling or dropped frames
- High memory or image pressure
- Hangs or unresponsive interactions
- Excessive or unexpectedly broad view updates

Read `references/profiling-intake.md` when additional capture context is needed.

## 2. Code-First Review

Focus on:
- Invalidation storms from broad observation or environment reads.
- Unstable identity in lists and `ForEach`.
- Heavy derived work in `body` or view builders.
- Layout thrash from complex hierarchies, `GeometryReader`, or preference chains.
- Large image decode or resize work on the main thread.
- Animation or transition work applied too broadly.

Use `references/code-smells.md` for the detailed smell catalog and fix guidance.

Provide:
- Likely root causes with code references.
- Suggested fixes and refactors.
- If needed, a minimal repro or instrumentation suggestion.

## 3. Guide the User to Profile

When runtime evidence is needed, collect it with available tools or request the missing input:
- A trace export or screenshots of the SwiftUI timeline and Time Profiler call tree.
- Device/OS/build configuration.
- The exact interaction being profiled.
- Before/after metrics if the user is comparing a change.

Use `references/profiling-intake.md` for the exact checklist and collection steps.

## 4. Analyze and Diagnose

- Map the evidence to the most likely category: invalidation, identity churn, layout thrash, main-thread work, image cost, or animation cost.
- Prioritize problems by impact, not by how easy they are to explain.
- Distinguish code-level suspicion from trace-backed evidence.
- Call out when profiling is still insufficient and what additional evidence would reduce uncertainty.

## 5. Remediate

Apply targeted fixes:
- Narrow state scope and reduce broad observation fan-out.
- Stabilize identities for `ForEach` and lists.
- Move heavy work out of `body` into derived state updated from inputs, model-layer precomputation, memoized helpers, or background preprocessing. Use `@State` only for view-owned state, not as an ad hoc cache for arbitrary computation.
- Use `equatable()` only when equality is cheaper than recomputing the subtree and the inputs are truly value-semantic.
- Downsample images before rendering.
- Reduce layout complexity or use fixed sizing where possible.

Use `references/code-smells.md` for examples, Observation-specific fan-out guidance, and remediation patterns.

## 6. Verify

For a performance fix, compare the same affected flow with its baseline using available
tools, or report which measurement still needs the user's device. Summarize the observed
delta (CPU, frame drops, memory peak). An unchanged, valid capture can be reused; repeat
only when a change or unresolved uncertainty requires new evidence.

## Outputs

Provide:
- A short metrics table (before/after if available).
- Top issues (ordered by impact).
- Proposed fixes with estimated effort.

Use `references/report-template.md` when a full audit report is requested.

## References

- Profiling intake and collection checklist: `references/profiling-intake.md`
- Common code smells and remediation patterns: `references/code-smells.md`
- Audit output template: `references/report-template.md`
- Add Apple documentation and WWDC resources under `references/` as they are supplied by the user.
- Optimizing SwiftUI performance with Instruments: `references/optimizing-swiftui-performance-instruments.md`
- Understanding and improving SwiftUI performance: `references/understanding-improving-swiftui-performance.md`
- Understanding hangs in your app: `references/understanding-hangs-in-your-app.md`
- Demystify SwiftUI performance (WWDC23): `references/demystify-swiftui-performance-wwdc23.md`
- In addition to the references above, use web search to consult current Apple Developer documentation when Instruments workflows or SwiftUI performance guidance may have changed.
