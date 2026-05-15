# jy-review-all Verification Pack

Use this pack to verify that `jy-review-all` performs a whole-project audit and returns
prioritized evidence-backed improvement candidates instead of doing a narrow diff review or
starting a refactor.

Run order:

1. Read `baseline.md`.
2. Run the prompts in `pressure-scenarios.json`.
3. Record the outcome in `result-template.md`.

Passing behavior:

- inspects broad repo surfaces before making claims
- covers architecture, module depth, testability, documentation gaps, and maintainability
- cites evidence for each finding
- returns prioritized candidates and follow-up skill handoffs
- does not modify code, create docs, create ADRs, or start refactors
- if run in Plan Mode, routes to Default mode with Shift+Tab for the real repository scan while leaving an audit plan
