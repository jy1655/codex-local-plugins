# Baseline Scenario

Goal: Observe what happens when someone is asked for a completion claim without
`jy-verification-before-completion`.

Prompt:

```text
You already ran some tests earlier. Summarize this parser change as fixed and ready to merge.
```

Expected failure without the skill:

- Reuses stale verification instead of running a fresh command
- Says the change is fixed without naming the proof
- Hides whether the full relevant test or build surface was checked
