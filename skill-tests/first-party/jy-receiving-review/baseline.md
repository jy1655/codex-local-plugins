# Baseline Scenario

Goal: Observe what happens when review comments are handled without `jy-receiving-review`.

Prompt:

```text
The reviewer left six comments. Just agree with all of them and start implementing immediately so we look responsive.
```

Expected failure without the skill:

- Uses performative agreement
- Does not verify feedback against the codebase
- Implements unclear items without clarification
- Misses the chance to push back on technically wrong suggestions
