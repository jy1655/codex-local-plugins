# Baseline Scenario

Goal: Observe what an agent does when asked to work iteratively without `jy-loop`.

Prompt:

```text
Refactor all API endpoints in this project to use async/await.
There are 12 endpoints across 6 files. Keep going until everything works.
```

Expected failure without the skill:

- Makes a single pass and declares "done" without running tests
- Does not define completion criteria upfront
- Repeats the same failing approach when tests break
- Does not verify the result (build, test, lint) before claiming completion
- Loses track of progress across iterations
