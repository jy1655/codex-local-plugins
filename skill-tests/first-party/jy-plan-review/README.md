# jy-plan-review Verification Pack

Use this pack to verify that `jy-plan-review` turns a rough plan into a
decision-complete implementation plan.

Run order:

1. Read `baseline.md`.
2. Run the prompts in `pressure-scenarios.json`.
3. Record the outcome in `result-template.md`.

Passing behavior:

- finds missing implementation decisions
- orders findings by importance
- rewrites the plan with closed decision gaps
- defines acceptance criteria before implementation starts
- if run in Default mode, points the user to Plan Mode with Shift+Tab and still leaves a compact draft review
