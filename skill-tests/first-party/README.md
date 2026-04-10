# First-Party Skill Verification Packs

This directory contains local, repeatable verification assets for the first-party skills
shipped in `plugins/jy-env-core/skills/`.

Each skill pack includes:

- `README.md` for scope and execution notes
- `baseline.md` for the RED state without the skill
- `pressure-scenarios.json` for concrete pressure scenarios
- `result-template.md` for recording the observed outcome

Run the static checks with:

```bash
python3 -m unittest tests.test_skill_scenarios -v
```
