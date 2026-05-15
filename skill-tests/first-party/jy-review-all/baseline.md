# Baseline Scenario

Goal: Observe what happens when a user asks for a whole-project review without
`jy-review-all`.

Prompt:

```text
Review this whole project and tell me what architecture or maintainability work we should do next.
```

Expected failure without the skill:

- reviews only the current diff or a few obvious files
- gives generic architecture advice without evidence
- does not separate architecture, testability, documentation, and maintainability findings
- starts proposing refactors or new docs before the user picks a candidate
- does not prioritize the findings or name the next skill handoff
