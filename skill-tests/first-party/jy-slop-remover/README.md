# jy-slop-remover Verification Pack

Use this pack to verify that `jy-slop-remover` correctly distinguishes removable AI slop
from legitimate code patterns, and preserves functionality.

Run order:

1. Read `baseline.md` and capture what someone does without the skill.
2. Run the prompts in `pressure-scenarios.json` with the skill available.
3. Record the result in `result-template.md`.

Passing behavior:

- Only processes one file per invocation.
- Correctly identifies AI-generated code smells (obvious comments, over-defensive code, deep nesting).
- Preserves system boundary validation, business logic comments, and project conventions.
- Skips changes when in doubt about functionality impact.
- Reports what was removed and what was kept with reasons.
- If the user is in Plan Mode, the skill does not fake file edits and instead routes them back to Default mode with Shift+Tab.
