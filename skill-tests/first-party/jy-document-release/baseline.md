# Baseline Scenario

Goal: Observe what happens without `jy-document-release`.

Prompt:

```text
We just changed how a first-party skill behaves. Update the release docs so the repo matches what actually shipped.
```

Expected failure without the skill:

- Updates only one obvious file like `README.md` and misses instructions or verification assets
- Invents generic release artifacts that do not exist in this repo
- Writes vague prose without grounding in the actual changed surface
