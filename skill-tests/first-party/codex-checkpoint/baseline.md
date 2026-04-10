# Baseline Scenario

Goal: Observe what happens without `codex-checkpoint`.

Prompt:

```text
I need to stop here and pick this work back up later, maybe on another branch.
Save whatever context matters so I can resume quickly next session.
```

Expected failure without the skill:

- Leaves only a vague conversational summary with no durable repo-local artifact
- Suggests hidden home-directory state or generic session memory instead of a repo-visible checkpoint path
- Does not distinguish save, list, and resume behaviors
