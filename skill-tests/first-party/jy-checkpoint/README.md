# jy-checkpoint Verification Pack

Use this pack to verify that `jy-checkpoint` creates durable repo-local handoff notes
instead of relying on vague chat memory or hidden home-directory state.

Run order:

1. Read `baseline.md`.
2. Run the prompts in `pressure-scenarios.json`.
3. Record the outcome in `result-template.md`.

Passing behavior:

- saves new checkpoint notes under `.codex/checkpoints/`
- treats checkpoints as append-only Markdown files
- resumes from the latest relevant checkpoint when no explicit target is given
- warns on branch mismatch without blocking resume
- renders save/list/resume summaries in the user's language by default
- handles Plan Mode honestly by using `Shift+Tab` for real save execution
