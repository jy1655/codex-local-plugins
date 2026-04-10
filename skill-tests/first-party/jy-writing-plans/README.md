# jy-writing-plans Verification Pack

Use this pack to verify that `jy-writing-plans` turns stable requirements into a
decision-complete implementation plan, stores only plan docs, and rejects placeholders.

Run order:

1. Read `baseline.md` to capture the no-skill planning failure.
2. Run the prompts in `pressure-scenarios.json` with the skill available.
3. Record the outcome in `result-template.md`.

Passing behavior:

- Produces a taskized implementation plan, not just advice.
- Uses `docs/superpowers/plans/` as the document target.
- Includes file paths, verification commands, and acceptance criteria.
- Rejects `TBD` and similar placeholders.
- In Default mode, routes to Plan Mode with Shift+Tab when the request still needs back-and-forth planning.
