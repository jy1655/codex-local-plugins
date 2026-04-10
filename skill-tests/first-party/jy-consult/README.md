# jy-consult Verification Pack

Use this pack to verify that `jy-consult` stays in advisory mode
and does not cross into implementation.

Run order:

1. Read `baseline.md` and capture what someone does without the skill.
2. Run the prompts in `pressure-scenarios.json` with the skill available.
3. Record the result in `result-template.md`.

Passing behavior:

- Provides structured analysis with tradeoffs, not just a single recommendation.
- Does not modify code or files during consultation.
- Gives a concrete recommendation with reasoning, not "it depends."
- Requires prior context (code, constraints) before advising.
