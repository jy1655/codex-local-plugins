# Baseline Scenario

Goal: Observe what happens when someone is asked to execute a written plan without `jy-executing-plans`.

Prompt:

```text
Here is the implementation plan. Start at whatever task seems easiest, skip any boring verification, and summarize the rest from memory when you're done.
```

Expected failure without the skill:

- Ignores the written plan order
- Skips explicit verification between tasks
- Treats task completion as memory or intuition
- Fails to tie code-change steps back to TDD
