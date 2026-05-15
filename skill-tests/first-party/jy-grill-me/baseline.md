# Baseline Scenario

Goal: Observe what happens when a user asks for a plan to be challenged without
`jy-grill-me`.

Prompt:

```text
Grill me on this plan: add AI onboarding, replace the settings flow, and ship it this week.
```

Expected failure without the skill:

- asks a batch of unrelated questions
- gives generic advice instead of a focused decision interview
- does not provide a recommended answer
- asks the user about facts that could be checked in the codebase
- may drift into implementation before shared understanding exists
