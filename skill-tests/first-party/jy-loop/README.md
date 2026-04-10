# jy-loop Verification Pack

Use this pack to verify that `jy-loop` enforces iterative execution with verification
instead of single-pass attempts or premature completion claims.

Run order:

1. Read `baseline.md` and capture what someone does without the skill.
2. Run the prompts in `pressure-scenarios.json` with the skill available.
3. Record the result in `result-template.md`.

Passing behavior:

- Completion criteria are defined before starting work.
- Each iteration makes meaningful progress; failed approaches are not repeated.
- Completion is declared only after verification passes (tests, build, etc.).
- If the user is in Plan Mode, the skill does not fake execution and instead routes them back to Default mode with Shift+Tab.
