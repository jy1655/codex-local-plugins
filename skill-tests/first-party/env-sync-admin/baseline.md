# Baseline Scenario

Goal: Observe what a maintainer does without `env-sync-admin`.

Prompt:

```text
You changed a plugin file in this repo and the update is not visible in Codex yet.
You are in a hurry and only want the fastest fix.

Decide what to do next and explain why.
```

Expected failure without the skill:

- Edits `~/.codex/plugins/cache` directly
- Treats the repo like an arbitrary project bootstrap
- Skips `inspect`/`apply` and does not mention restarting Codex
