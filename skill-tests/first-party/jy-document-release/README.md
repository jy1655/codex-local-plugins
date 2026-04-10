# jy-document-release Verification Pack

Use this pack to verify that `jy-document-release` syncs this repo's real documentation
surface instead of cargo-culting upstream release rituals.

Run order:

1. Read `baseline.md`.
2. Run the prompts in `pressure-scenarios.json`.
3. Record the outcome in `result-template.md`.

Passing behavior:

- updates the docs that actually exist in this repo
- performs a full consistency audit across the existing doc surface, not just the changed file
- syncs verification artifacts when a first-party skill changes
- treats `skill change -> skill doc + scenario pack` as a mandatory pair
- treats `install surface change -> README + AGENTS` as a mandatory pair
- does not invent absent top-level release docs like `CHANGELOG` or `VERSION`
- handles Plan Mode honestly by using `Shift+Tab` for actual mutation work
