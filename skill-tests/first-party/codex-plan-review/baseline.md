# Baseline Scenario

Goal: Observe what happens when a rough plan is reviewed without `codex-plan-review`.

Prompt:

```text
Here is the plan: add a new admin dashboard, improve alerts, and refactor the API. Review it quickly.
```

Expected failure without the skill:

- gives generic feedback instead of concrete findings
- does not identify missing interfaces, edge cases, or acceptance criteria
- leaves the plan too vague for another implementer to pick up safely
