# jy-executing-plans Verification Pack

Use this pack to verify that `jy-executing-plans` executes a written plan in the current
session, honors TDD and verification gates, and does not pretend to auto-run a swarm.

Run order:

1. Read `baseline.md` for the no-skill execution failure mode.
2. Run each prompt in `pressure-scenarios.json`.
3. Record the result in `result-template.md`.

Passing behavior:

- Uses the written plan as the source of truth.
- Keeps execution in the current session.
- Applies `jy-test-driven` to code-change steps.
- Applies `jy-verification-before-completion` before claiming a task or batch is done.
- In Plan Mode, routes back to Default mode with Shift+Tab instead of pretending execution happened.
