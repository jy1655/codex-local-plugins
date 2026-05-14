# jy-grill-me Verification Pack

Use this pack to verify that `jy-grill-me` pressure-tests a plan through a
one-question-at-a-time decision interview instead of rewriting the plan or starting
implementation.

Run order:

1. Read `baseline.md`.
2. Run the prompts in `pressure-scenarios.json`.
3. Record the outcome in `result-template.md`.

Passing behavior:

- asks exactly one focused decision question at a time
- includes why the question matters
- gives a recommended answer when evidence supports one
- checks codebase-answerable facts before asking the user
- keeps the session advisory and does not modify files
- if a longer loop is requested in Default mode, points the user to Plan Mode with Shift+Tab while still leaving the first useful question
