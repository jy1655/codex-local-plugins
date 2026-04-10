# jy-writing-skills Verification Pack

Use this pack to verify that `jy-writing-skills` still enforces TDD-style validation for
first-party skills and resists the common shortcuts of "just edit the doc" or "skip the
baseline test".

Run order:

1. Read `baseline.md` to capture how the work fails without the skill.
2. Run each pressure scenario from `pressure-scenarios.json`.
3. Record the before/after outcome in `result-template.md`.

Passing behavior:

- The operator insists on a baseline failure before claiming the skill is good.
- The operator keeps the frontmatter and section structure aligned with the documented rules.
- The operator treats core `SKILL.md` authoring as English-first unless there is a clear exception.
- The operator avoids stale skill namespace references and records the result explicitly.
