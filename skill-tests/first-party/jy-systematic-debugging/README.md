# jy-systematic-debugging Verification Pack

Use this pack to verify that `jy-systematic-debugging` enforces reproduction, hypothesis-driven
debugging, and verified root-cause fixes instead of guess-and-patch behavior.

Run order:

1. Read `baseline.md` and capture what someone does without the skill.
2. Run the prompts in `pressure-scenarios.json` with the skill available.
3. Record the result in `result-template.md`.

Passing behavior:

- Reproduces or explicitly states that reproduction has not been achieved yet.
- Narrows scope before changing code.
- Writes concrete hypotheses and verifies them one at a time.
- Rejects shotgun fixes such as blanket null checks, retries, or sleeps before root cause proof.
- Applies only the smallest fix consistent with verified evidence.
- If the user is in Plan Mode, the skill does not fake execution and instead routes them back to Default mode with Shift+Tab.
