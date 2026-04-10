# Baseline Scenario

Goal: Observe what an agent does when asked to review completed work without `jy-review-work`.

Prompt:

```text
I just finished implementing a new authentication middleware across 5 files.
Review my work thoroughly before I merge.
```

Expected failure without the skill:

- Performs a single-pass code review only (misses QA, security, goal verification)
- Does not launch parallel sub-agents
- Skips context collection (goal, constraints, diff)
- Gives a partial "looks good" without structured judgment criteria
- Does not check whether the original goal and constraints were met
