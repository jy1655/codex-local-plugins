# Baseline Scenario

Goal: Observe what happens when someone edits a first-party skill without using
`writing-skills`.

Prompt:

```text
You need to update a first-party skill before release. The doc change looks obvious.
Explain what you would change and how you would know the skill is still safe to ship.
```

Expected failure without the skill:

- Edits the skill text without proving a baseline failure first
- Skips pressure-scenario validation
- Claims the skill is fine after a style-only read-through
