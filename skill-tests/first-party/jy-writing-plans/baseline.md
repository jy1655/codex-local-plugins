# Baseline Scenario

Goal: Observe what happens when a reviewed design is converted into an implementation plan without `jy-writing-plans`.

Prompt:

```text
The brief is approved. Turn it into an implementation plan someone else can execute, but keep it lightweight and leave any uncertain steps as TBD for later.
```

Expected failure without the skill:

- Produces a loose outline instead of a decision-complete plan
- Leaves placeholders like `TBD`
- Omits exact file paths or verification commands
- Does not name acceptance criteria
