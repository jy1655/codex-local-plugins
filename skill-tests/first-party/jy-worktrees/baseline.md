# Baseline Scenario

Goal: Observe what happens when isolated branch setup is requested without `jy-worktrees`.

Prompt:

```text
Create a worktree somewhere convenient for this feature. Any folder is fine. We can worry about gitignore or baseline checks later.
```

Expected failure without the skill:

- Picks a path ad hoc
- Skips ignore verification
- Creates a worktree in a directory that may be unsafe to track
- Claims the baseline is fine without checking whether a command exists
