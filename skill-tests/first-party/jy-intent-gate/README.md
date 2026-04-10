# jy-intent-gate Verification Pack

Use this pack to verify that `jy-intent-gate` correctly classifies ambiguous requests
and routes to the appropriate strategy instead of defaulting to implementation.

Run order:

1. Read `baseline.md` and capture what someone does without the skill.
2. Run the prompts in `pressure-scenarios.json` with the skill available.
3. Record the result in `result-template.md`.

Passing behavior:

- Separates literal request from actual intent.
- Classifies into the correct intent type (Research, Implementation, Investigation, Fix, Evaluation, Refactoring).
- Decomposes compound requests into ordered sub-intents.
- Follows the strategy matching the classified intent, not the literal wording.
- Skips classification for unambiguous simple requests.
- Handles Plan Mode vs Default mode explicitly when the routed strategy depends on collaboration mode.
