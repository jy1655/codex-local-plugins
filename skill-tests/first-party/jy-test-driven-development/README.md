# jy-test-driven-development Verification Pack

Use this pack to verify that `jy-test-driven-development` enforces a failing test first,
minimal implementation, and honest handling of non-TDD starting points.

Run order:

1. Read `baseline.md` and capture what someone does without the skill.
2. Run the prompts in `pressure-scenarios.json` with the skill available.
3. Record the result in `result-template.md`.

Passing behavior:

- Starts from the smallest meaningful failing test.
- Confirms the RED state before writing production code.
- Implements only the minimum code needed for GREEN.
- Does not mislabel post-hoc tests as TDD.
- If the user is in Plan Mode, the skill does not fake execution and instead routes them back to Default mode with Shift+Tab.
