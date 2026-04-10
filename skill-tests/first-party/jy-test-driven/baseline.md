# Baseline Scenario

Goal: Observe what happens when implementation starts without `jy-test-driven`.

Prompt:

```text
Add rate limiting to the login endpoint. Move quickly and write tests at the end once the code looks right.
```

Expected failure without the skill:

- Starts writing production code immediately
- Treats tests as cleanup work instead of the design entry point
- Skips verifying a RED failure before implementation
- Overbuilds configuration or helper abstractions before any tested behavior exists
