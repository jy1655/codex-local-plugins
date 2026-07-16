# First-Party Skill Pressure Scenarios

This directory stores manual evaluation inputs for the first-party skills under
`plugins/jy-env-core/skills/`. Each skill has one `pressure-scenarios.json` file.

These files are not proof that an agent run passed. CI validates only their presence and
schema. Record behavioral results outside this tree only when the scenarios were actually
run against a named model and configuration.

## Manual Schema

Each JSON document contains one top-level `scenarios` array with at least two objects.
Every scenario has exactly these non-empty string fields:

- `id`: stable identifier within the skill
- `title`: short description of the pressure case
- `prompt`: input to run manually
- `expected_without_skill`: likely failure mode
- `expected_with_skill`: behavior the skill should produce

Validate the assets with:

```bash
python3 -m unittest tests.test_skill_scenarios -v
```
