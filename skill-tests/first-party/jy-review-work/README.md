# jy-review-work Verification Pack

Use this pack to verify that `jy-review-work` enforces the five-lens review protocol
instead of single-pass or partial reviews.

Run order:

1. Read `baseline.md` and capture what someone does without the skill.
2. Run the prompts in `pressure-scenarios.json` with the skill available.
3. Record the result in `result-template.md`.

Passing behavior:

- All 5 review lenses are covered before the final decision.
- Subagents are not auto-spawned unless the user explicitly asks for delegated agent work.
- Final judgment requires all 5 to PASS; any FAIL means overall FAIL.
- Context (goal, constraints, diff) is collected before review execution.
- If the user is in Plan Mode, the skill does not fake execution and instead routes them back to Default mode with Shift+Tab.
