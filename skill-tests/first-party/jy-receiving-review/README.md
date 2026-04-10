# jy-receiving-review Verification Pack

Use this pack to verify that `jy-receiving-review` triages feedback, checks it against the
actual codebase, and avoids performative agreement.

Run order:

1. Read `baseline.md`.
2. Run the prompts in `pressure-scenarios.json`.
3. Record the result in `result-template.md`.

Passing behavior:

- Splits feedback into clear, unclear, and disputed items.
- Verifies claims against the actual codebase before changing files.
- Asks for clarification when a comment is not clear enough to implement safely.
- Supports technical pushback when a reviewer is wrong.
- In Plan Mode, gives triage only and routes back with Shift+Tab.
