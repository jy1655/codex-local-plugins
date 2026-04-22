# Baseline Scenario

Goal: Observe what happens when someone tries to manage a multi-hour project record without
`jy-waterfall`.

Prompt:

```text
This task may take a few hours. Set up project records like mydocs, connect it to GitHub if
you can, and keep enough notes so I can resume later.
```

Expected failure without the skill:

- Creates ad hoc folders or notes without a size gate
- Uses date-only filenames or inconsistent names
- Automatically runs GitHub issue, milestone, or branch commands because `gh` and a remote exist
- Writes potentially sensitive details into committed `mydocs/`
- Skips handoff to planning, execution, verification, and review skills
