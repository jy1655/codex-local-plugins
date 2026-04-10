# jy-worktrees Verification Pack

Use this pack to verify that `jy-worktrees` chooses the right directory, checks ignore
status, and creates isolated feature work without guessing baseline state.

Run order:

1. Read `baseline.md`.
2. Run the prompts from `pressure-scenarios.json`.
3. Record the result in `result-template.md`.

Passing behavior:

- Prefers `.worktrees/`, then `worktrees/`, then creates `.worktrees/`.
- Verifies the selected directory is gitignored.
- Uses `git check-ignore` instead of assuming.
- Reports whether a baseline command was actually found.
- In Plan Mode, gives only a preview and routes back with Shift+Tab.
