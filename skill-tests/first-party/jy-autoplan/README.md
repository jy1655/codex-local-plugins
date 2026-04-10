# jy-autoplan Verification Pack

Use this pack to verify that `jy-autoplan` chooses the right planning step and returns
one consolidated planning result.

Run order:

1. Read `baseline.md`.
2. Run the prompts in `pressure-scenarios.json`.
3. Record the outcome in `result-template.md`.

Passing behavior:

- correctly classifies planning maturity
- distinguishes `idea-stage`, `plan-stage`, and `execution-ready`
- routes to the right Codex planning skill
- returns one combined result instead of fragmented advice
- states the next step clearly
- handles Default mode by routing the user into Plan Mode with Shift+Tab when interactive planning is required
- does not force execution-ready work into the planning pack
