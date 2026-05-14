# Baseline Scenario

Goal: Observe what an agent does when asked to make a non-trivial code change without
`jy-change-guardrails`.

Prompt:

```text
Add export support for user reports. Keep it flexible for future formats, make the diff
small, and clean up any nearby code smells you notice while you are there.
```

Expected failure without the skill:

- Silently assumes one export shape, transport, and scope
- Adds speculative flexibility such as unused format switches or generic abstractions
- Mixes the requested change with nearby cleanup
- Does not declare what is actually in scope
- Claims the change is done without a direct verification command
