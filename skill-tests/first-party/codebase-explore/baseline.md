# Baseline Scenario

Goal: Observe what an agent does when asked to explore unfamiliar code without `codebase-explore`.

Prompt:

```text
I need to understand how the notification system works in this project.
Find all the pieces — where notifications are created, sent, and consumed.
```

Expected failure without the skill:

- Runs a single grep for "notification" and stops
- Returns file paths without line numbers or context
- Misses related code that uses different terms (e.g., "alert", "message", "event")
- Does not trace the flow across layers (creation → sending → consumption)
- Does not provide a structural summary of how pieces connect
