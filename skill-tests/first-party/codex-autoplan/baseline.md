# Baseline Scenario

Goal: Observe what happens when a user asks for "autoplan" without a Codex-native
planning orchestrator.

Prompt:

```text
Autoplan this. I have some notes, but I am not sure if they are even a real plan yet.
```

Expected failure without the skill:

- does not classify whether the request needs scoping or review
- gives mixed planning advice with no routing decision
- leaves the user unclear on the next step
