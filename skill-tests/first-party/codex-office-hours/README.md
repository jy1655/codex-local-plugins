# codex-office-hours Verification Pack

Use this pack to verify that `codex-office-hours` sharpens vague ideas into a concrete
brief instead of jumping straight to implementation.

Run order:

1. Read `baseline.md`.
2. Run the prompts in `pressure-scenarios.json` with the skill available.
3. Record what happened in `result-template.md`.

Passing behavior:

- identifies the target user and concrete problem
- narrows scope before implementation
- outputs a brief with success criteria and non-goals
- routes to the next planning step instead of coding
- if run in Default mode, guides the user into Plan Mode with Shift+Tab while still leaving a compact brief draft
