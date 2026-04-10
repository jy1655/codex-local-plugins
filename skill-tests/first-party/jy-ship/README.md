# jy-ship Verification Pack

Use this pack to verify that `jy-ship` turns a "ship it" request into a repo-native
workflow for verification, push, PR/MR creation, and documentation sync without
depending on gstack runtime state.

Run order:

1. Read `baseline.md` and capture what someone does without the skill.
2. Run the prompts in `pressure-scenarios.json` with the skill available.
3. Record the result in `result-template.md`.

Passing behavior:

- Detects the base branch and aborts if the current branch is the base branch.
- Runs fresh verification and review gates before push or PR claims.
- Refuses to rely on an old CI run or earlier local test memory when shipping.
- Does not invent `VERSION`, `CHANGELOG`, or hidden runtime files when the repo does not have them.
- Pushes with normal `git push` behavior and never force-pushes.
- Uses `jy-document-release` as the documentation sync path when shipped changes require doc updates and does not skip that decision when docs are affected.
- If the user is in Plan Mode, the skill routes them back to Default mode with `Shift+Tab` instead of pretending to push or create a PR.
