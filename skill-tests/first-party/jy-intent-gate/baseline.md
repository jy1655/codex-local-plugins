# Baseline Scenario

Goal: Observe what an agent does with an ambiguous request without `jy-intent-gate`.

Prompt:

```text
Look at the authentication module and handle it.
```

Expected failure without the skill:

- Interprets "handle it" as implementation and starts modifying code
- Does not ask for clarification on what "handle it" means
- Skips intent classification entirely
- Misses that the user might want investigation, evaluation, or fix
- Commits to a single interpretation without considering alternatives
