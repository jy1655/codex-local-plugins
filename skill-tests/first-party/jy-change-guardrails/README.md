# jy-change-guardrails Verification Pack

Use this pack to verify that `jy-change-guardrails` surfaces assumptions, avoids
overengineering, keeps diffs tightly scoped, and stays mode-aware.

Run order:

1. Read `baseline.md` and capture what someone does without the skill.
2. Run the prompts in `pressure-scenarios.json` with the skill available.
3. Record the result in `result-template.md`.

Passing behavior:

- Separates explicit requirements from inferred assumptions.
- Names competing interpretations instead of picking silently.
- Chooses the smallest valid change instead of speculative abstractions.
- Declares an edit boundary and avoids unrelated cleanup.
- Ties the work to a direct verification command.
- If the user is in Plan Mode, the skill does not fake execution and routes them back to Default mode with Shift+Tab.
