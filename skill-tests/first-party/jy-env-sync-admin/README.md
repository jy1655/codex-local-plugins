# jy-env-sync-admin Verification Pack

Use this pack to verify that `jy-env-sync-admin` keeps maintainers focused on the repo-owned
install surface instead of ad-hoc local fixes.

Run order:

1. Read `baseline.md` and capture what someone does without the skill.
2. Run the prompts in `pressure-scenarios.json` with the skill available.
3. Record the result in `result-template.md`.

Passing behavior:

- The operator stays inside the repo-owned install surface.
- The operator knows that Codex skill discovery is wired through `~/.agents/skills/`.
- The operator uses `inspect`, `apply`, or `bootstrap` instead of editing cache paths.
- The operator calls out when a fresh Codex session is required.
